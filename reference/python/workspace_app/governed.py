from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol

import p7_06_ui4_owner_preflight as ui4

from .access import AccessContext


class GovernedExperienceError(RuntimeError):
    """Fail-closed error while resolving or running the P9.06 governed experience."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _text(value: str, *, field: str, limit: int = 1024) -> str:
    if not isinstance(value, str):
        raise GovernedExperienceError(f"{field} must be text")
    normalized = " ".join(value.split())
    if not normalized or len(normalized) > limit or "\x00" in normalized:
        raise GovernedExperienceError(f"{field} is outside the bounded governed-experience contract")
    return normalized


@dataclass(frozen=True, slots=True)
class GovernedGateView:
    name: str
    state: str
    basis: str

    def to_payload(self) -> dict[str, str]:
        return {
            "name": _text(self.name, field="gate.name", limit=120),
            "state": _text(self.state, field="gate.state", limit=80),
            "basis": _text(self.basis, field="gate.basis", limit=600),
        }


@dataclass(frozen=True, slots=True)
class GovernedExperienceProjection:
    generated_at: str
    release_sha: str
    source: str
    authority_mode: str
    authority_scope: str
    validation_status: str
    execution_subject: str
    execution_version: str
    event_version: str
    source_subject: str
    source_version: str
    checkpoint_id: str
    provenance_refs: tuple[str, ...]
    gates: tuple[GovernedGateView, ...]
    outcome: str

    def to_payload(self) -> dict[str, object]:
        waiting = tuple(gate.name for gate in self.gates if gate.state.casefold() == "waiting")
        return {
            "schema": "arvectum.workspace.governed-experience/1",
            "generated_at": self.generated_at,
            "presentation": {
                "title": "EIS document governed execution",
                "summary": (
                    "A real retained execution/provenance chain for an EIS-backed governed document. "
                    "The authoritative external source remains ЕИС / zakupki.gov.ru."
                ),
                "source": self.source,
                "authority_mode": self.authority_mode,
                "authority_scope": self.authority_scope,
                "validation_status": self.validation_status,
            },
            "execution": {
                "status": self.outcome,
                "meaning": (
                    "Required action decisions are still unresolved, so the execution remains fail-closed."
                    if waiting
                    else "Current governed decision evidence was resolved by the authoritative runtime adapter."
                ),
                "waiting_decisions": list(waiting),
                "technical_identity_available": True,
            },
            "decisions": [gate.to_payload() for gate in self.gates],
            "action": {
                "kind": "governed-preflight",
                "label": "Run governed preflight",
                "available": True,
                "consequential": False,
                "canonical_mutation_requested": False,
                "external_effect_requested": False,
                "authority_provided": False,
                "explanation": (
                    "Re-check the real retained execution and all four governance gates now. "
                    "The preflight records minimized local evidence but cannot grant authority or approval."
                ),
            },
            "technical": {
                "release_sha": self.release_sha,
                "source_subject": self.source_subject,
                "source_version": self.source_version,
                "execution_subject": self.execution_subject,
                "execution_version": self.execution_version,
                "event_version": self.event_version,
                "checkpoint_id": self.checkpoint_id,
                "provenance_refs": list(self.provenance_refs),
            },
            "scope": {
                "organization_resolved_server_side": True,
                "actor_resolved_server_side": True,
                "current_access_revalidated": True,
                "organizational_authority_provided": False,
                "visibility_implies_permission": False,
            },
        }


@dataclass(frozen=True, slots=True)
class GovernedPreflightResult:
    recorded_at: str
    outcome: str
    evidence_sha256: str

    def to_payload(self) -> dict[str, object]:
        return {
            "schema": "arvectum.workspace.governed-preflight-result/1",
            "recorded_at": self.recorded_at,
            "outcome": self.outcome,
            "status_text": (
                "Preflight executed: WAITING / fail-closed. Missing governance decisions were not manufactured."
            ),
            "canonical_mutation_requested": False,
            "canonical_mutation_performed": False,
            "external_effect_requested": False,
            "external_effect_performed": False,
            "organizational_authority_provided": False,
            "consequential_approval_provided": False,
            "evidence": {
                "classification": "owner-local non-canonical proof evidence",
                "sha256": self.evidence_sha256,
            },
        }


class GovernedExperienceProvider(Protocol):
    def inspect(self, access: AccessContext) -> GovernedExperienceProjection:
        ...

    def run_preflight(self, access: AccessContext) -> GovernedPreflightResult:
        ...


def project_owner_preflight(preflight: ui4.UI4OwnerPreflight) -> GovernedExperienceProjection:
    if not isinstance(preflight, ui4.UI4OwnerPreflight):
        raise GovernedExperienceError("typed real owner preflight is required")
    gates = tuple(GovernedGateView(row.name, row.state, row.basis) for row in preflight.gates)
    expected = ("Authorization", "Organizational Authority", "Data Governance", "Consequential Approval")
    if tuple(gate.name for gate in gates) != expected:
        raise GovernedExperienceError("real preflight does not preserve the four required decision concepts")
    return GovernedExperienceProjection(
        generated_at=_utc_now(),
        release_sha=_text(preflight.release_sha, field="release_sha", limit=160),
        source=_text(preflight.authoritative_source, field="authoritative_source", limit=320),
        authority_mode=_text(preflight.authority_mode, field="authority_mode", limit=120),
        authority_scope=_text(preflight.authority_scope, field="authority_scope", limit=320),
        validation_status=_text(preflight.validation_status, field="validation_status", limit=600),
        execution_subject=_text(preflight.execution_subject, field="execution_subject"),
        execution_version=_text(preflight.execution_version, field="execution_version"),
        event_version=_text(preflight.event_version, field="event_version"),
        source_subject=_text(preflight.subject_identity, field="subject_identity"),
        source_version=_text(preflight.version_identity, field="version_identity"),
        checkpoint_id=_text(preflight.checkpoint_id, field="checkpoint_id"),
        provenance_refs=tuple(_text(value, field="provenance_ref") for value in preflight.provenance_refs),
        gates=gates,
        outcome=_text(preflight.outcome, field="outcome", limit=80),
    )


class RuntimeGovernedExperienceProvider:
    """P9.06 adapter over the already-proven real P7.06-UI4 owner preflight.

    Every inspect/run rebuilds from the current exact-release retained runtime.
    Browser state supplies no candidate record, authority, gate decision, approval,
    retry token or external-effect instruction. The only write performed by the
    bounded P9.06 action is UI4's minimized owner-local non-canonical proof receipt.
    """

    def __init__(self, runtime_root: Path):
        self.runtime_root = runtime_root.expanduser()

    def _preflight(self, access: AccessContext) -> ui4.UI4OwnerPreflight:
        if not isinstance(access, AccessContext):
            raise GovernedExperienceError("server-authorized AccessContext is required")
        credential_file = self.runtime_root / "secrets" / "p7-04" / f"{access.credential_id}.secret"
        try:
            return ui4.build_owner_preflight(
                self.runtime_root,
                organization=access.organization,
                principal=access.actor,
                credential_id=access.credential_id,
                credential_file=credential_file,
            )
        except (ui4.UI4Error, ui4.ui1.UI1Error, ui4.ui2.UI2AccessDenied, OSError, ValueError) as exc:
            raise GovernedExperienceError("current governed interaction evidence is unavailable") from exc

    def inspect(self, access: AccessContext) -> GovernedExperienceProjection:
        return project_owner_preflight(self._preflight(access))

    def run_preflight(self, access: AccessContext) -> GovernedPreflightResult:
        # Rebuild immediately at the command boundary; never trust prior GET/button state.
        preflight = self._preflight(access)
        if preflight.outcome != "Waiting" or any(row.state != "Waiting" for row in preflight.gates):
            raise GovernedExperienceError("bounded P9.06 action is admitted only for the proven fail-closed Waiting case")
        try:
            receipt = ui4.record_browser_preflight(self.runtime_root, preflight)
        except (ui4.UI4Error, OSError, ValueError) as exc:
            raise GovernedExperienceError("governed preflight evidence could not be recorded") from exc
        return GovernedPreflightResult(
            recorded_at=_utc_now(),
            outcome="Waiting",
            evidence_sha256=_text(receipt.sha256, field="evidence_sha256", limit=64),
        )


__all__ = [
    "GovernedExperienceError",
    "GovernedExperienceProjection",
    "GovernedExperienceProvider",
    "GovernedGateView",
    "GovernedPreflightResult",
    "RuntimeGovernedExperienceProvider",
    "project_owner_preflight",
]
