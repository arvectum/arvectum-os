"""Canonical Record reference semantics for P1.02, P2.02 and P6.03.

The module remains a bounded in-memory reference model, not a persistence or
public wire contract. P2.02 extends the immutable Canonical Record envelope with
optional temporal applicability metadata so a lineage resolver can distinguish
Canonical Head from Effective Version without changing historical versions.

P6.03 adds the minimum RFC-0002 external-authority declaration needed by the
first real Product Contract validation target. External Reference and Governed
Replica remain explicit authority modes and require a complete bounded external
authority contract; missing or ambiguous authority evidence fails closed. This
is reference semantics only and does not select synchronization infrastructure,
a registry client, storage, transport or a Stable/public schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .identity import Identity
from .security import ActorContext, OrganizationScope


class AuthorityMode(str, Enum):
    """RFC-0001/RFC-0002 authority modes."""

    NATIVE = "Native"
    EXTERNAL_REFERENCE = "External Reference"
    GOVERNED_REPLICA = "Governed Replica"


def _require_aware_datetime(value: datetime, *, label: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")


def _require_text(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be explicit")


@dataclass(frozen=True, slots=True)
class ExternalAuthorityContract:
    """Bounded RFC-0002 authority mapping for one external fact scope.

    The object records organizational semantics only. It is not a connector,
    credential, synchronization runtime, SLA, legal-rights assertion or proof
    that the external source is currently available.
    """

    authoritative_system: str
    external_object_ref: str
    authority_scope: str
    retrieval_or_sync: str
    freshness_expectation: str
    source_version_semantics: str
    conflict_rule: str
    failure_behavior: str
    permitted_transformations: tuple[str, ...]
    retention_deletion: str
    portability: str

    def __post_init__(self) -> None:
        for label, value in (
            ("authoritative_system", self.authoritative_system),
            ("external_object_ref", self.external_object_ref),
            ("authority_scope", self.authority_scope),
            ("retrieval_or_sync", self.retrieval_or_sync),
            ("freshness_expectation", self.freshness_expectation),
            ("source_version_semantics", self.source_version_semantics),
            ("conflict_rule", self.conflict_rule),
            ("failure_behavior", self.failure_behavior),
            ("retention_deletion", self.retention_deletion),
            ("portability", self.portability),
        ):
            _require_text(value, label=f"external authority {label}")
        if not isinstance(self.permitted_transformations, tuple):
            raise ValueError("external authority permitted_transformations must be an immutable tuple")
        if any(not isinstance(value, str) or not value.strip() for value in self.permitted_transformations):
            raise ValueError("external authority permitted_transformations must contain explicit values")


@dataclass(frozen=True, slots=True)
class CanonicalRecord:
    """Immutable governed representation of one logical subject at one version.

    The optional ``effective_from`` / ``effective_until`` bounds describe
    temporal applicability where a governed schema uses time-based effective
    version resolution. Missing bounds are unbounded on that side. P2.02 uses
    half-open intervals ``[effective_from, effective_until)``; the resolver
    refuses overlapping applicability instead of silently guessing.

    ``external_authority`` is mandatory for External Reference and Governed
    Replica records and forbidden for Native records so the reference model
    cannot silently create competing authority.
    """

    subject_id: Identity
    version_id: Identity
    semantic_type: str
    schema_version: str
    organization: OrganizationScope
    authority_mode: AuthorityMode
    authority_scope: str
    accountable_owner_id: Identity
    creation_actor: ActorContext
    created_at: datetime
    provenance_refs: tuple[Identity, ...]
    integrity_metadata: tuple[tuple[str, str], ...]
    payload: tuple[tuple[str, str], ...] = ()
    lifecycle_status: str | None = None
    predecessor_version_id: Identity | None = None
    effective_from: datetime | None = None
    effective_until: datetime | None = None
    external_authority: ExternalAuthorityContract | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.subject_id, Identity):
            raise ValueError("subject_id must be an Identity")
        if not isinstance(self.version_id, Identity):
            raise ValueError("version_id must be an Identity")
        if self.subject_id == self.version_id:
            raise ValueError("Subject Identity and Version Identity are distinct semantic roles")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("organization scope must be explicit")
        if not isinstance(self.authority_mode, AuthorityMode):
            raise ValueError("authority_mode must be explicit")
        if self.authority_mode is AuthorityMode.NATIVE:
            if self.external_authority is not None:
                raise ValueError("Native Canonical Record must not carry an external authority contract")
        else:
            if not isinstance(self.external_authority, ExternalAuthorityContract):
                raise ValueError(
                    "External Reference and Governed Replica require an explicit ExternalAuthorityContract"
                )
            if self.external_authority.authority_scope != self.authority_scope:
                raise ValueError(
                    "external authority contract and Canonical Record must declare the same authority scope"
                )
        if not isinstance(self.semantic_type, str) or not self.semantic_type.strip():
            raise ValueError("semantic_type must be a non-empty string")
        if not isinstance(self.schema_version, str) or not self.schema_version.strip():
            raise ValueError("schema_version must be a non-empty string")
        if not isinstance(self.authority_scope, str) or not self.authority_scope.strip():
            raise ValueError("authority_scope must be explicit")
        if not isinstance(self.accountable_owner_id, Identity):
            raise ValueError("accountable_owner_id must be an Identity")
        if not isinstance(self.creation_actor, ActorContext):
            raise ValueError("creation_actor must be attributable")
        if self.creation_actor.organization != self.organization:
            raise ValueError("creation actor and Canonical Record must share Organization scope")
        if not isinstance(self.created_at, datetime):
            raise ValueError("created_at must be timezone-aware")
        _require_aware_datetime(self.created_at, label="created_at")
        if not isinstance(self.provenance_refs, tuple) or not self.provenance_refs:
            raise ValueError("provenance_refs must contain attributable governed references")
        if any(not isinstance(ref, Identity) for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain only Identity references")
        if not isinstance(self.integrity_metadata, tuple) or not self.integrity_metadata:
            raise ValueError("integrity_metadata must be explicit and proportionate to consequence")
        if any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) and value.strip() for value in item)
            for item in self.integrity_metadata
        ):
            raise ValueError("integrity_metadata must contain non-empty string key/value pairs")
        if not isinstance(self.payload, tuple) or any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) for value in item)
            for item in self.payload
        ):
            raise ValueError("bounded payload must use immutable string key/value pairs")
        if self.predecessor_version_id is not None:
            if not isinstance(self.predecessor_version_id, Identity):
                raise ValueError("predecessor_version_id must be an Identity when supplied")
            if self.predecessor_version_id == self.version_id:
                raise ValueError("a Canonical Record version cannot reference itself as predecessor")
        for label, bound in (
            ("effective_from", self.effective_from),
            ("effective_until", self.effective_until),
        ):
            if bound is not None:
                if not isinstance(bound, datetime):
                    raise ValueError(f"{label} must be a datetime when supplied")
                _require_aware_datetime(bound, label=label)
        if (
            self.effective_from is not None
            and self.effective_until is not None
            and self.effective_until <= self.effective_from
        ):
            raise ValueError("effective_until must be later than effective_from")


def build_p1_02_native_record(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
) -> CanonicalRecord:
    """Build the deterministic first Native canonical version used by fitness tests."""

    return CanonicalRecord(
        subject_id=Identity("canonical-subject", "subject-1", organization.organization_id.value),
        version_id=Identity("canonical-version", "subject-1-v1", organization.organization_id.value),
        semantic_type="reference.subject",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="reference.subject/state",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=datetime.fromisoformat("2026-08-07T18:50:00+00:00"),
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(("label", "domain-neutral reference subject"),),
        lifecycle_status="established",
        predecessor_version_id=None,
    )
