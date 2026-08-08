"""P1.11 — bounded replay and projection architecture-fitness evidence.

This module closes the two remaining Phase 1 fitness obligations without
introducing a production replay engine, durable projection/index technology or
new source of organizational authority.

``rebuild_p1_11_projection`` consumes the already-derived P1.10 portable
semantic fixture and produces only an immutable, non-authoritative read model.
It has no Governed Execution, canonical mutation, Event-admission or external
side-effect path.

``pin_p1_11_projection_source`` makes the authority boundary executable: a
projection entry is useful for discovery, but consequential reliance still
requires the exact canonical source version supplied independently as a
``CanonicalRecord``. The resulting ``GovernedVersionPin`` is derived from that
canonical source, never from the projection itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .canonical import CanonicalRecord
from .execution import GovernedVersionPin
from .identity import Identity
from .portability import PortableSemanticFixture


class ReplayProjectionError(ValueError):
    """The bounded P1.11 replay/projection evidence is invalid or unsafe."""


class ProjectionAuthorityError(ValueError):
    """A derived projection was presented as if it were governed authority."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReplayProjectionError(message)


def _identity(value: Any, *, label: str) -> Identity:
    _require(isinstance(value, dict), f"{label} must be an explicit identity mapping")
    _require(
        set(value) == {"namespace", "value", "scope"},
        f"{label} must preserve namespace, value and scope exactly",
    )
    try:
        return Identity(
            namespace=value["namespace"],
            value=value["value"],
            scope=value["scope"],
        )
    except (TypeError, ValueError) as exc:
        raise ReplayProjectionError(f"{label} is not a valid Identity") from exc


@dataclass(frozen=True, slots=True)
class ProjectionEntry:
    """One derived lookup entry attributable to one exact canonical source version."""

    source_role: str
    subject_id: Identity
    source_version_id: Identity
    semantic_type: str
    authority_scope: str
    lifecycle_status: str | None
    canonical_authority: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.source_role, str) or not self.source_role.strip():
            raise ReplayProjectionError("projection source_role must be explicit")
        if not isinstance(self.subject_id, Identity) or not isinstance(
            self.source_version_id, Identity
        ):
            raise ReplayProjectionError("projection source identities must be explicit")
        if self.subject_id == self.source_version_id:
            raise ReplayProjectionError(
                "projection Subject Identity and source Version Identity must remain distinct"
            )
        if self.subject_id.scope != self.source_version_id.scope:
            raise ReplayProjectionError(
                "projection Subject/Version Identity scope must match"
            )
        if not isinstance(self.semantic_type, str) or not self.semantic_type.strip():
            raise ReplayProjectionError("projection semantic_type must be explicit")
        if not isinstance(self.authority_scope, str) or not self.authority_scope.strip():
            raise ReplayProjectionError("projection authority_scope attribution must be explicit")
        if self.lifecycle_status is not None and (
            not isinstance(self.lifecycle_status, str) or not self.lifecycle_status.strip()
        ):
            raise ReplayProjectionError(
                "projection lifecycle_status must be non-empty when supplied"
            )
        if self.canonical_authority is not False:
            raise ProjectionAuthorityError(
                "derived projection entries cannot claim canonical authority"
            )


@dataclass(frozen=True, slots=True)
class ProjectionSnapshot:
    """Immutable non-authoritative projection rebuilt from one P1.10 fixture."""

    source_fixture_scope: str
    source_record_versions: tuple[Identity, ...]
    entries: tuple[ProjectionEntry, ...]
    replay_mode: str = "projection-rebuild"
    canonical_authority: bool = False
    consequential_side_effects_created: int = 0

    def __post_init__(self) -> None:
        if self.source_fixture_scope != "P1.01-P1.10":
            raise ReplayProjectionError(
                "P1.11 projection replay requires the exact bounded P1.10 fixture scope"
            )
        if not isinstance(self.source_record_versions, tuple) or not self.source_record_versions:
            raise ReplayProjectionError("projection replay must preserve source Version Identities")
        if any(not isinstance(item, Identity) for item in self.source_record_versions):
            raise ReplayProjectionError("projection source versions must be Identity values")
        if len(set(self.source_record_versions)) != len(self.source_record_versions):
            raise ReplayProjectionError("projection replay cannot collapse duplicate source versions")
        if not isinstance(self.entries, tuple) or not self.entries:
            raise ReplayProjectionError("projection replay must produce explicit derived entries")
        if any(not isinstance(item, ProjectionEntry) for item in self.entries):
            raise ReplayProjectionError("projection snapshot entries must be ProjectionEntry values")
        if tuple(entry.source_version_id for entry in self.entries) != self.source_record_versions:
            raise ReplayProjectionError(
                "projection entries must remain attributable to the exact source version manifest"
            )
        if self.replay_mode != "projection-rebuild":
            raise ReplayProjectionError("P1.11 replay mode is limited to projection rebuild")
        if self.canonical_authority is not False:
            raise ProjectionAuthorityError("a derived projection snapshot cannot become canonical authority")
        if self.consequential_side_effects_created != 0:
            raise ReplayProjectionError(
                "projection replay must not claim or create consequential side effects"
            )

    def entries_for_subject(self, subject_id: Identity) -> tuple[ProjectionEntry, ...]:
        """Return all matching source versions without resolving a canonical/effective head."""

        if not isinstance(subject_id, Identity):
            raise TypeError("projection lookup requires an Identity")
        return tuple(entry for entry in self.entries if entry.subject_id == subject_id)


def rebuild_p1_11_projection(*, fixture: PortableSemanticFixture) -> ProjectionSnapshot:
    """Replay the P1.10 semantic fixture only into a derived non-authoritative read model.

    The function deliberately has no callback, operation executor, mutation boundary,
    Event admission path or external-effect adapter. A new consequential action must
    therefore enter through a separate Governed Execution; historical replay cannot
    silently execute it here.
    """

    if not isinstance(fixture, PortableSemanticFixture):
        raise TypeError("P1.11 replay requires a PortableSemanticFixture")

    document = fixture.to_mapping()
    fixture_metadata = document.get("fixture")
    _require(isinstance(fixture_metadata, dict), "fixture metadata must be explicit")
    _require(
        fixture_metadata.get("scope") == "P1.01-P1.10",
        "P1.11 replay requires the exact bounded P1.10 fixture scope",
    )
    _require(
        fixture_metadata.get("canonical_authority") is False,
        "replayed fixture must remain explicitly non-canonical",
    )
    _require(
        fixture_metadata.get("derived_representation") is True,
        "replayed fixture must remain an explicitly derived representation",
    )

    portability = document.get("portability")
    _require(isinstance(portability, dict), "portability boundary must be explicit")
    _require(
        portability.get("canonical_authority") is False,
        "portable replay input cannot establish canonical authority",
    )

    semantic_links = document.get("semantic_links")
    _require(isinstance(semantic_links, list), "semantic links must be an explicit list")
    _require(
        all(
            isinstance(link, dict) and link.get("canonical_typed_relationship") is False
            for link in semantic_links
        ),
        "derived replay links cannot be reinterpreted as canonical Typed Relationships",
    )

    manifest = document.get("manifest")
    records = document.get("records")
    _require(isinstance(manifest, dict), "fixture manifest must be explicit")
    _require(isinstance(records, list) and records, "fixture records must be explicit")
    _require(
        manifest.get("record_count") == len(records),
        "fixture record manifest must match the replayed records",
    )
    manifest_versions = manifest.get("record_versions")
    _require(isinstance(manifest_versions, list), "fixture Version Identity manifest must be explicit")

    source_versions = tuple(
        _identity(value, label="manifest Version Identity") for value in manifest_versions
    )
    _require(
        len(source_versions) == len(records),
        "fixture Version Identity manifest must cover every replayed record exactly once",
    )
    _require(
        len(set(source_versions)) == len(source_versions),
        "fixture replay must reject duplicate immutable Version Identities",
    )

    entries: list[ProjectionEntry] = []
    for index, item in enumerate(records):
        _require(isinstance(item, dict), f"record {index} must be an explicit mapping")
        role = item.get("role")
        envelope = item.get("canonical_record")
        _require(isinstance(role, str) and role.strip(), f"record {index} role must be explicit")
        _require(isinstance(envelope, dict), f"record {role} canonical envelope must be explicit")

        subject_id = _identity(
            envelope.get("subject_identity"), label=f"record {role} Subject Identity"
        )
        version_id = _identity(
            envelope.get("version_identity"), label=f"record {role} Version Identity"
        )
        authority = envelope.get("authority")
        _require(isinstance(authority, dict), f"record {role} authority attribution must be explicit")
        semantic_type = envelope.get("semantic_type")
        authority_scope = authority.get("scope")
        lifecycle_status = envelope.get("lifecycle_status")

        entry = ProjectionEntry(
            source_role=role,
            subject_id=subject_id,
            source_version_id=version_id,
            semantic_type=semantic_type,
            authority_scope=authority_scope,
            lifecycle_status=lifecycle_status,
        )
        entries.append(entry)

    replayed_versions = tuple(entry.source_version_id for entry in entries)
    _require(
        replayed_versions == source_versions,
        "projection replay must preserve exact manifest Version Identity order and attribution",
    )

    return ProjectionSnapshot(
        source_fixture_scope=fixture_metadata["scope"],
        source_record_versions=source_versions,
        entries=tuple(entries),
    )


def pin_p1_11_projection_source(
    *,
    projection_entry: ProjectionEntry,
    canonical_source: CanonicalRecord,
) -> GovernedVersionPin:
    """Return an exact pin only after independently supplied canonical-source validation.

    A projection cannot mint a governed pin. The canonical source must match the
    projection's Subject Identity, exact source Version Identity, semantic type,
    authority scope and lifecycle attribution before ``GovernedVersionPin`` is
    created from the Canonical Record itself.
    """

    if not isinstance(projection_entry, ProjectionEntry):
        raise TypeError("projection_entry must be a ProjectionEntry")
    if not isinstance(canonical_source, CanonicalRecord):
        raise ProjectionAuthorityError(
            "projection results cannot substitute for an exact CanonicalRecord source version"
        )

    mismatches: list[str] = []
    if canonical_source.subject_id != projection_entry.subject_id:
        mismatches.append("Subject Identity")
    if canonical_source.version_id != projection_entry.source_version_id:
        mismatches.append("Version Identity")
    if canonical_source.semantic_type != projection_entry.semantic_type:
        mismatches.append("semantic type")
    if canonical_source.authority_scope != projection_entry.authority_scope:
        mismatches.append("authority scope")
    if canonical_source.lifecycle_status != projection_entry.lifecycle_status:
        mismatches.append("lifecycle status")
    if mismatches:
        raise ProjectionAuthorityError(
            "projection attribution does not match the exact canonical source: "
            + ", ".join(mismatches)
        )

    return GovernedVersionPin.from_record(canonical_source)
