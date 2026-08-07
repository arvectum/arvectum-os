"""P1.02 — Native subject and first immutable Canonical Record version.

This module implements only the bounded RFC-0002 semantics required by P1.02.
It is an in-memory reference model, not a persistence or public wire contract.
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


@dataclass(frozen=True, slots=True)
class CanonicalRecord:
    """Immutable governed representation of one logical subject at one version.

    P1.02 intentionally admits only ``Native`` records. External Reference and
    Governed Replica require authority contracts that are outside this work item.
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

    def __post_init__(self) -> None:
        if not isinstance(self.subject_id, Identity):
            raise ValueError("subject_id must be an Identity")
        if not isinstance(self.version_id, Identity):
            raise ValueError("version_id must be an Identity")
        if self.subject_id == self.version_id:
            raise ValueError("Subject Identity and Version Identity are distinct semantic roles")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("organization scope must be explicit")
        if self.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError(
                "P1.02 implements Native authority only; external modes require an explicit authority contract"
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
        if not isinstance(self.created_at, datetime) or self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")
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
