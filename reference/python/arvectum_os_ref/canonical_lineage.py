"""P2.02 — Canonical Record lineage, Head and Effective Version runtime.

This module implements a bounded, domain-neutral in-memory resolver for Accepted
RFC-0002 lineage semantics. It deliberately does not introduce a persistence
model, mutable current-state pointer, database concurrency contract, public SDK
or Product Contract.

Callers provide already-admitted canonical versions for one subject and authority
scope. The resolver validates that they form one unambiguous predecessor chain,
identifies the Canonical Head from lineage position, resolves temporal Effective
Version explicitly, and supports exact Version Identity lookup for consequential
pinning. Material ambiguity fails closed.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .canonical import CanonicalRecord
from .identity import Identity


class CanonicalLineageResolutionError(ValueError):
    """Canonical lineage cannot be resolved without violating RFC-0002 semantics."""


class CanonicalLineageConflictError(CanonicalLineageResolutionError):
    """Supplied admitted versions do not form one unambiguous canonical chain."""


class CanonicalVersionNotFoundError(CanonicalLineageResolutionError):
    """An exact requested Version Identity is absent from the supplied lineage."""


class EffectiveVersionResolutionError(CanonicalLineageResolutionError):
    """A temporal Effective Version cannot be resolved deterministically."""


class NoEffectiveVersionError(EffectiveVersionResolutionError):
    """No supplied canonical version is applicable at the evaluation time."""


class AmbiguousEffectiveVersionError(EffectiveVersionResolutionError):
    """More than one supplied canonical version is applicable at the evaluation time."""


def _require_aware_datetime(value: datetime, *, label: str) -> None:
    if (
        not isinstance(value, datetime)
        or value.tzinfo is None
        or value.utcoffset() is None
    ):
        raise ValueError(f"{label} must be timezone-aware")


def _is_effective_at(record: CanonicalRecord, at: datetime) -> bool:
    if record.effective_from is not None and at < record.effective_from:
        return False
    if record.effective_until is not None and at >= record.effective_until:
        return False
    return True


@dataclass(frozen=True, slots=True)
class CanonicalLineage:
    """One validated canonical predecessor chain for one governed subject.

    ``records`` are treated as admitted canonical versions, not drafts or
    competing candidates. A branch, missing predecessor, disconnected version,
    duplicate Version Identity or mixed subject/authority scope is therefore a
    material conflict and is rejected rather than normalized heuristically.
    """

    records: tuple[CanonicalRecord, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.records, tuple) or not self.records:
            raise CanonicalLineageConflictError(
                "canonical lineage requires at least one admitted Canonical Record"
            )
        if any(not isinstance(record, CanonicalRecord) for record in self.records):
            raise CanonicalLineageConflictError(
                "canonical lineage may contain only CanonicalRecord versions"
            )

        first = self.records[0]
        stable_semantics = (
            ("Subject Identity", lambda record: record.subject_id),
            ("Organization scope", lambda record: record.organization),
            ("authority scope", lambda record: record.authority_scope),
            ("authority mode", lambda record: record.authority_mode),
            ("semantic type", lambda record: record.semantic_type),
        )
        for label, selector in stable_semantics:
            expected = selector(first)
            if any(selector(record) != expected for record in self.records[1:]):
                raise CanonicalLineageConflictError(
                    f"canonical lineage must preserve one {label}"
                )

        by_version: dict[Identity, CanonicalRecord] = {}
        for record in self.records:
            if record.version_id in by_version:
                raise CanonicalLineageConflictError(
                    f"duplicate canonical Version Identity: {record.version_id.value}"
                )
            by_version[record.version_id] = record

        roots = [
            record for record in self.records if record.predecessor_version_id is None
        ]
        if len(roots) != 1:
            raise CanonicalLineageConflictError(
                "canonical lineage must contain exactly one initial version"
            )

        children: dict[Identity, CanonicalRecord] = {}
        for record in self.records:
            predecessor = record.predecessor_version_id
            if predecessor is None:
                continue
            if predecessor not in by_version:
                raise CanonicalLineageConflictError(
                    "canonical lineage contains a version with an unknown predecessor"
                )
            if predecessor in children:
                raise CanonicalLineageConflictError(
                    "canonical lineage contains competing admitted successors for one predecessor"
                )
            children[predecessor] = record

        visited: set[Identity] = set()
        cursor = roots[0]
        while True:
            if cursor.version_id in visited:
                raise CanonicalLineageConflictError(
                    "canonical lineage contains a predecessor cycle"
                )
            visited.add(cursor.version_id)
            successor = children.get(cursor.version_id)
            if successor is None:
                break
            cursor = successor

        if len(visited) != len(self.records):
            raise CanonicalLineageConflictError(
                "canonical lineage contains disconnected or cyclic admitted versions"
            )

    @property
    def subject_id(self) -> Identity:
        return self.records[0].subject_id

    @property
    def head(self) -> CanonicalRecord:
        """Return the unique latest admitted version in predecessor order."""

        predecessor_ids = {
            record.predecessor_version_id
            for record in self.records
            if record.predecessor_version_id is not None
        }
        candidates = [
            record for record in self.records if record.version_id not in predecessor_ids
        ]
        if len(candidates) != 1:
            # Structural validation should make this unreachable, but keep the
            # resolution boundary fail-closed if invariants change later.
            raise CanonicalLineageConflictError(
                "canonical lineage does not expose exactly one Canonical Head"
            )
        return candidates[0]

    def resolve_version(self, version_id: Identity) -> CanonicalRecord:
        """Resolve one exact immutable Version Identity without current-state inference."""

        if not isinstance(version_id, Identity):
            raise TypeError("exact canonical version resolution requires an Identity")
        for record in self.records:
            if record.version_id == version_id:
                return record
        raise CanonicalVersionNotFoundError(
            f"canonical Version Identity is not present in lineage: {version_id.value}"
        )

    def resolve_effective(self, *, at: datetime) -> CanonicalRecord:
        """Resolve the unique temporally applicable canonical version at ``at``.

        Applicability uses each immutable record's optional half-open effective
        period ``[effective_from, effective_until)``. Missing bounds are
        unbounded. The resolver intentionally has no last-write-wins fallback:
        zero candidates or overlapping candidates are explicit errors.
        """

        _require_aware_datetime(at, label="effective-version evaluation time")
        candidates = [record for record in self.records if _is_effective_at(record, at)]
        if not candidates:
            raise NoEffectiveVersionError(
                "no canonical version is effective at the declared evaluation time"
            )
        if len(candidates) != 1:
            raise AmbiguousEffectiveVersionError(
                "multiple canonical versions are effective at the declared evaluation time"
            )
        return candidates[0]
