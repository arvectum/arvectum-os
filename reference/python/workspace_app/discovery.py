from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Protocol
from urllib.parse import quote

import p7_06_ui1_live_workspace as ui1
import p7_06_ui4_owner_preflight as ui4

from .access import AccessContext


class DiscoveryError(RuntimeError):
    """Fail-closed error while producing the P9.05 discovery projection."""


class ObjectUnavailable(DiscoveryError):
    """The requested opaque object reference cannot be safely resolved."""


class DiscoveryKind(str, Enum):
    RECORD = "record"
    DOCUMENT = "document"
    KNOWLEDGE = "knowledge"
    EXECUTION = "execution"


class DiscoveryFreshness(str, Enum):
    FRESH = "fresh"
    DEGRADED = "degraded"


MAX_QUERY_LENGTH = 160
MAX_VISIBLE_RESULTS = 200


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bounded_text(value: str, *, field: str, limit: int = 320) -> str:
    if not isinstance(value, str):
        raise DiscoveryError(f"{field} must be text")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > limit or "\x00" in normalized:
        raise DiscoveryError(f"{field} is empty or outside the bounded presentation contract")
    return normalized


def _normalize_query(value: str) -> str:
    if not isinstance(value, str):
        raise DiscoveryError("search query must be text")
    normalized = " ".join(value.split())
    if len(normalized) > MAX_QUERY_LENGTH or "\x00" in normalized:
        raise DiscoveryError("search query is outside the bounded application contract")
    return normalized


def _object_id(subject_identity: str, version_identity: str) -> str:
    source = f"{subject_identity}\n{version_identity}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()[:20]


def _human_semantic_label(semantic_type: str) -> str:
    raw = _bounded_text(semantic_type, field="semantic_type", limit=160)
    token = raw.rsplit(".", 1)[-1].replace("_", "-")
    return " ".join(part.capitalize() for part in token.split("-") if part) or "Record"


def _kind_for(semantic_type: str) -> DiscoveryKind:
    semantic = semantic_type.casefold()
    if "document" in semantic or "artifact" in semantic:
        return DiscoveryKind.DOCUMENT
    if "knowledge" in semantic or "memory" in semantic or "observation" in semantic or "learning" in semantic:
        return DiscoveryKind.KNOWLEDGE
    if "execution" in semantic or "workflow" in semantic:
        return DiscoveryKind.EXECUTION
    return DiscoveryKind.RECORD


def _knowledge_role(semantic_type: str) -> str | None:
    semantic = semantic_type.casefold()
    if "observation" in semantic:
        return "Observation — not validated Knowledge"
    if "memory" in semantic:
        return "Organizational Memory — not automatically validated Knowledge"
    if "candidate" in semantic:
        return "Knowledge Candidate — not validated Knowledge"
    if "knowledge" in semantic:
        return "Knowledge"
    if "learning" in semantic:
        return "Governed learning record"
    return None


@dataclass(frozen=True, slots=True)
class DiscoverySourceItem:
    semantic_type: str
    schema_version: str
    subject_identity: str
    version_identity: str
    authority_mode: str
    authority_scope: str
    authoritative_source: str | None
    classification: str
    lifecycle_status: str | None
    validation_status: str | None
    provenance_refs: tuple[str, ...]
    source_release_sha: str

    def __post_init__(self) -> None:
        for field in (
            "semantic_type",
            "schema_version",
            "subject_identity",
            "version_identity",
            "authority_mode",
            "authority_scope",
            "classification",
            "source_release_sha",
        ):
            _bounded_text(getattr(self, field), field=field, limit=1024)
        if self.authoritative_source is not None:
            _bounded_text(self.authoritative_source, field="authoritative_source")
        if self.lifecycle_status is not None:
            _bounded_text(self.lifecycle_status, field="lifecycle_status", limit=160)
        if self.validation_status is not None:
            _bounded_text(self.validation_status, field="validation_status", limit=320)
        if not isinstance(self.provenance_refs, tuple) or any(
            not isinstance(value, str) or not value.strip() for value in self.provenance_refs
        ):
            raise DiscoveryError("provenance_refs must be immutable non-empty text references")

    @property
    def object_id(self) -> str:
        return _object_id(self.subject_identity, self.version_identity)

    @property
    def kind(self) -> DiscoveryKind:
        return _kind_for(self.semantic_type)


@dataclass(frozen=True, slots=True)
class DiscoverySourceContext:
    items: tuple[DiscoverySourceItem, ...]
    observed_at: str
    release_sha: str
    preflight: ui4.UI4OwnerPreflight | None = None

    def __post_init__(self) -> None:
        _bounded_text(self.observed_at, field="observed_at", limit=64)
        _bounded_text(self.release_sha, field="release_sha", limit=160)
        if not isinstance(self.items, tuple) or any(not isinstance(item, DiscoverySourceItem) for item in self.items):
            raise DiscoveryError("items must be immutable DiscoverySourceItem values")
        ids = tuple(item.object_id for item in self.items)
        if len(set(ids)) != len(ids):
            raise DiscoveryError("opaque discovery identifiers must resolve unambiguously")


@dataclass(frozen=True, slots=True)
class DiscoveryHealth:
    state: DiscoveryFreshness
    code: str
    message: str
    observed_at: str

    def to_payload(self) -> dict[str, str]:
        return {
            "state": self.state.value,
            "code": _bounded_text(self.code, field="health.code", limit=80),
            "message": _bounded_text(self.message, field="health.message"),
            "observed_at": _bounded_text(self.observed_at, field="health.observed_at", limit=64),
        }


@dataclass(frozen=True, slots=True)
class DiscoveryResult:
    object_id: str
    kind: DiscoveryKind
    semantic_role: str
    title: str
    summary: str
    source_label: str
    authority_mode: str
    state_label: str
    knowledge_role: str | None = None

    @property
    def open_href(self) -> str:
        return f"/objects/{quote(self.object_id, safe='')}"

    def to_payload(self) -> dict[str, object]:
        return {
            "id": self.object_id,
            "kind": self.kind.value,
            "semantic_role": self.semantic_role,
            "title": self.title,
            "summary": self.summary,
            "source": self.source_label,
            "authority_mode": self.authority_mode,
            "state": self.state_label,
            "knowledge_role": self.knowledge_role,
            "open_href": self.open_href,
            "interaction": "inspect-only",
            "authority_provided": False,
        }


@dataclass(frozen=True, slots=True)
class DiscoveryProjection:
    generated_at: str
    query: str
    kind_filter: DiscoveryKind | None
    health: DiscoveryHealth
    results: tuple[DiscoveryResult, ...]

    def to_payload(self) -> dict[str, object]:
        return {
            "schema": "arvectum.workspace.discovery/1",
            "generated_at": self.generated_at,
            "query": self.query,
            "kind_filter": self.kind_filter.value if self.kind_filter else None,
            "projection": {
                "derived": True,
                "canonical_authority": False,
                "organizational_authority_provided": False,
                "consequential_action_available": False,
                "search_result_is_authority": False,
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "denied_result_counts_exposed": False,
                "protected_snippets_minimized": True,
            },
            "health": self.health.to_payload(),
            "results": [result.to_payload() for result in self.results],
        }


@dataclass(frozen=True, slots=True)
class ObjectDetail:
    object_id: str
    kind: DiscoveryKind
    semantic_role: str
    title: str
    summary: str
    source_label: str
    authority_mode: str
    authority_scope: str
    lifecycle_status: str | None
    validation_status: str | None
    classification: str
    knowledge_role: str | None
    subject_identity: str
    version_identity: str
    schema_version: str
    source_release_sha: str
    provenance_refs: tuple[str, ...]
    related_execution_subject: str | None = None
    related_execution_version: str | None = None
    related_event_version: str | None = None
    related_checkpoint: str | None = None
    preflight_outcome: str | None = None
    preflight_waiting_gates: tuple[str, ...] = ()

    def to_payload(self) -> dict[str, object]:
        process = (
            "This object is connected to retained governed execution/provenance evidence. "
            "Any consequential continuation must use the governed-action path and revalidate current gates."
            if self.related_execution_version
            else "This view is read-only. Any consequential continuation must resolve current governed state at the command boundary."
        )
        next_step = (
            "Inspect the waiting governance gates before any consequential action."
            if self.preflight_outcome == "Waiting"
            else "Use the technical details only when exact identity/version/provenance evidence is needed."
        )
        return {
            "schema": "arvectum.workspace.object-context/1",
            "id": self.object_id,
            "kind": self.kind.value,
            "semantic_role": self.semantic_role,
            "title": self.title,
            "summary": self.summary,
            "source": self.source_label,
            "knowledge_role": self.knowledge_role,
            "authority": {
                "mode": self.authority_mode,
                "scope": self.authority_scope,
                "authoritative_source": self.source_label,
                "organizational_authority_provided": False,
                "visibility_implies_permission": False,
            },
            "state": {
                "lifecycle": self.lifecycle_status,
                "validation": self.validation_status,
                "classification": self.classification,
            },
            "context": {
                "meaning": self.summary,
                "process": process,
                "next_step": next_step,
                "interaction": "inspect-only",
                "consequential_action_available": False,
            },
            "technical": {
                "subject_identity": self.subject_identity,
                "version_identity": self.version_identity,
                "schema_version": self.schema_version,
                "source_release_sha": self.source_release_sha,
                "provenance_refs": list(self.provenance_refs),
                "related_execution_subject": self.related_execution_subject,
                "related_execution_version": self.related_execution_version,
                "related_event_version": self.related_event_version,
                "related_checkpoint": self.related_checkpoint,
            },
            "governed_preflight": {
                "outcome": self.preflight_outcome,
                "waiting_gates": list(self.preflight_waiting_gates),
                "authority_provided": False,
            }
            if self.preflight_outcome is not None
            else None,
            "projection": {
                "presentation_authority": "non-authoritative",
                "current_source_revalidated": True,
                "exact_version_exposed_on_demand": True,
            },
        }


class DiscoveryProvider(Protocol):
    def search(self, access: AccessContext, *, query: str = "", kind: DiscoveryKind | None = None) -> DiscoveryProjection:
        ...

    def inspect(self, access: AccessContext, object_id: str) -> ObjectDetail:
        ...


def _source_label(item: DiscoverySourceItem) -> str:
    if item.authoritative_source:
        return _bounded_text(item.authoritative_source, field="authoritative_source")
    if item.authority_mode.casefold() == "native":
        return "Arvectum OS governed state"
    return "Authoritative source not declared in retained metadata"


def _state_label(item: DiscoverySourceItem) -> str:
    if item.lifecycle_status and item.validation_status:
        return f"{item.lifecycle_status} · {item.validation_status}"
    return item.lifecycle_status or item.validation_status or "Governed state; no lifecycle/validation label declared"


def _summary(item: DiscoverySourceItem) -> str:
    role = _human_semantic_label(item.semantic_type)
    source = _source_label(item)
    if item.kind is DiscoveryKind.KNOWLEDGE:
        knowledge = _knowledge_role(item.semantic_type) or "Knowledge-related governed record"
        return f"{knowledge}. Governed {role} available from {source}."
    return f"Governed {role} available from {source}."


def _title(item: DiscoverySourceItem) -> str:
    role = _human_semantic_label(item.semantic_type)
    source = _source_label(item)
    authority_scope = " ".join(item.authority_scope.split())
    if authority_scope and authority_scope.casefold() not in {"native", "platform", "organization"}:
        return f"{role} — {authority_scope}"
    return f"{role} — {source}"


def _result(item: DiscoverySourceItem) -> DiscoveryResult:
    return DiscoveryResult(
        object_id=item.object_id,
        kind=item.kind,
        semantic_role=_human_semantic_label(item.semantic_type),
        title=_title(item),
        summary=_summary(item),
        source_label=_source_label(item),
        authority_mode=item.authority_mode,
        state_label=_state_label(item),
        knowledge_role=_knowledge_role(item.semantic_type),
    )


def _search_haystack(item: DiscoverySourceItem) -> str:
    # Exact technical references may improve recall for human identifiers embedded
    # in governed external references (for example an external notice number), but
    # they are never returned by the search result projection itself.
    values = (
        _title(item),
        _summary(item),
        _source_label(item),
        item.semantic_type,
        item.authority_scope,
        item.lifecycle_status or "",
        item.validation_status or "",
        item.subject_identity,
        item.version_identity,
    )
    return " ".join(values).casefold()


def project_discovery(
    source: DiscoverySourceContext,
    *,
    query: str = "",
    kind: DiscoveryKind | None = None,
) -> DiscoveryProjection:
    normalized = _normalize_query(query)
    if kind is not None and not isinstance(kind, DiscoveryKind):
        raise DiscoveryError("kind filter must be explicit")
    needle = normalized.casefold()
    matched: list[DiscoverySourceItem] = []
    for item in source.items:
        if kind is not None and item.kind is not kind:
            continue
        if needle and needle not in _search_haystack(item):
            continue
        matched.append(item)
    if len(matched) > MAX_VISIBLE_RESULTS:
        raise DiscoveryError("authorized discovery result set exceeds the bounded P9.05 limit")
    matched.sort(key=lambda item: (_title(item).casefold(), item.kind.value, item.object_id))
    return DiscoveryProjection(
        generated_at=_utc_now(),
        query=normalized,
        kind_filter=kind,
        health=DiscoveryHealth(
            DiscoveryFreshness.FRESH,
            "OK",
            "Search was rebuilt from the current authorized governed source snapshot.",
            source.observed_at,
        ),
        results=tuple(_result(item) for item in matched),
    )


def inspect_discovery(source: DiscoverySourceContext, object_id: str) -> ObjectDetail:
    opaque = _bounded_text(object_id, field="object_id", limit=40)
    if len(opaque) != 20 or any(ch not in "0123456789abcdef" for ch in opaque):
        raise ObjectUnavailable("object is unavailable")
    matches = tuple(item for item in source.items if item.object_id == opaque)
    if len(matches) != 1:
        raise ObjectUnavailable("object is unavailable")
    item = matches[0]

    related_execution_subject = None
    related_execution_version = None
    related_event_version = None
    related_checkpoint = None
    preflight_outcome = None
    waiting_gates: tuple[str, ...] = ()
    preflight = source.preflight
    if preflight is not None and preflight.subject_identity == item.subject_identity and preflight.version_identity == item.version_identity:
        related_execution_subject = preflight.execution_subject
        related_execution_version = preflight.execution_version
        related_event_version = preflight.event_version
        related_checkpoint = preflight.checkpoint_id
        preflight_outcome = preflight.outcome
        waiting_gates = tuple(gate.name for gate in preflight.gates if gate.state == "Waiting")

    return ObjectDetail(
        object_id=item.object_id,
        kind=item.kind,
        semantic_role=_human_semantic_label(item.semantic_type),
        title=_title(item),
        summary=_summary(item),
        source_label=_source_label(item),
        authority_mode=item.authority_mode,
        authority_scope=item.authority_scope,
        lifecycle_status=item.lifecycle_status,
        validation_status=item.validation_status,
        classification=item.classification,
        knowledge_role=_knowledge_role(item.semantic_type),
        subject_identity=item.subject_identity,
        version_identity=item.version_identity,
        schema_version=item.schema_version,
        source_release_sha=item.source_release_sha,
        provenance_refs=item.provenance_refs,
        related_execution_subject=related_execution_subject,
        related_execution_version=related_execution_version,
        related_event_version=related_event_version,
        related_checkpoint=related_checkpoint,
        preflight_outcome=preflight_outcome,
        preflight_waiting_gates=waiting_gates,
    )


class RuntimeDiscoveryProvider:
    """Read-only P9.05 adapter over already-proven P7.04/P7.06 live sources.

    It deliberately has no durable search database. Each query/inspection rebuilds
    from the current authorized exact-release snapshot. This keeps the initial
    implementation reversible and prevents a mutable index from becoming a second
    source of truth. A later read model can replace this implementation without
    changing the browser-facing P9.05 semantics.
    """

    def __init__(self, runtime_root: Path):
        self.runtime_root = runtime_root.expanduser()

    def _load(self, access: AccessContext) -> DiscoverySourceContext:
        if not isinstance(access, AccessContext):
            raise DiscoveryError("server-authorized AccessContext is required")
        credential_file = self.runtime_root / "secrets" / "p7-04" / f"{access.credential_id}.secret"
        try:
            snapshot = ui1.build_live_snapshot(
                self.runtime_root,
                organization=access.organization,
                principal=access.actor,
                credential_id=access.credential_id,
                credential_file=credential_file,
            )
        except (ui1.UI1AccessDenied, ui1.UI1IntegrityError, ui1.UI1BoundaryError, OSError, ValueError) as exc:
            raise DiscoveryError("current governed discovery source is unavailable") from exc

        items = tuple(
            DiscoverySourceItem(
                semantic_type=item.semantic_type,
                schema_version=item.schema_version,
                subject_identity=item.subject_identity,
                version_identity=item.version_identity,
                authority_mode=item.authority_mode,
                authority_scope=item.authority_scope,
                authoritative_source=item.authoritative_source,
                classification=item.classification,
                lifecycle_status=item.lifecycle_status,
                validation_status=item.validation_status,
                provenance_refs=item.provenance_refs,
                source_release_sha=item.source_release_sha,
            )
            for item in snapshot.items
        )

        preflight: ui4.UI4OwnerPreflight | None = None
        try:
            candidate = ui4.build_owner_preflight(
                self.runtime_root,
                organization=access.organization,
                principal=access.actor,
                credential_id=access.credential_id,
                credential_file=credential_file,
            )
        except (
            ui4.UI4Error,
            ui4.ui1.UI1Error,
            ui4.ui2.UI2AccessDenied,
            OSError,
            ValueError,
        ):
            # Generic discovery remains useful when the optional exact F1 context
            # adapter is unavailable. We do not turn a failed enrichment into a
            # claim about a protected object's existence or state.
            candidate = None
        if candidate is not None and any(
            item.subject_identity == candidate.subject_identity and item.version_identity == candidate.version_identity
            for item in items
        ):
            preflight = candidate

        return DiscoverySourceContext(
            items=items,
            observed_at=_utc_now(),
            release_sha=snapshot.release_sha,
            preflight=preflight,
        )

    def search(self, access: AccessContext, *, query: str = "", kind: DiscoveryKind | None = None) -> DiscoveryProjection:
        try:
            source = self._load(access)
        except DiscoveryError:
            now = _utc_now()
            return DiscoveryProjection(
                generated_at=now,
                query=_normalize_query(query),
                kind_filter=kind,
                health=DiscoveryHealth(
                    DiscoveryFreshness.DEGRADED,
                    "DISCOVERY_SOURCE_UNAVAILABLE",
                    "Current protected discovery sources could not be revalidated. Results are withheld.",
                    now,
                ),
                results=(),
            )
        return project_discovery(source, query=query, kind=kind)

    def inspect(self, access: AccessContext, object_id: str) -> ObjectDetail:
        try:
            source = self._load(access)
        except DiscoveryError as exc:
            raise ObjectUnavailable("object is unavailable") from exc
        return inspect_discovery(source, object_id)


__all__ = [
    "DiscoveryError",
    "DiscoveryFreshness",
    "DiscoveryHealth",
    "DiscoveryKind",
    "DiscoveryProjection",
    "DiscoveryProvider",
    "DiscoveryResult",
    "DiscoverySourceContext",
    "DiscoverySourceItem",
    "ObjectDetail",
    "ObjectUnavailable",
    "RuntimeDiscoveryProvider",
    "inspect_discovery",
    "project_discovery",
]
