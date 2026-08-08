"""P2.03 — Typed Relationship runtime.

This module exercises the Accepted RFC-0002 Typed Relationship model as bounded,
domain-neutral, in-memory runtime behavior. A relationship version is represented
as a Canonical Record specialization through composition: the CanonicalRecord
envelope carries stable Relationship Identity / immutable Version Identity and
governance metadata, while the relationship-specific fields preserve the exact
relationship type and directed endpoint semantics.

The implementation deliberately selects no graph database, durable store, public
wire format, authorization engine or Organizational Authority mechanism. Traversal
operates only over exact immutable relationship versions supplied by the caller;
it never silently resolves a head/effective version and relationship existence is
not an intrinsic permission or authority grant.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .canonical_lineage import CanonicalLineage
from .identity import Identity
from .security import ActorContext, OrganizationScope


RELATIONSHIP_RECORD_SEMANTIC_TYPE: Final = "platform.typed-relationship"


class EndpointReferenceRole(str, Enum):
    """RFC-0002 endpoint reference role; never inferred from Identity syntax."""

    SUBJECT_IDENTITY = "SubjectIdentity"
    VERSION_IDENTITY = "VersionIdentity"


class TraversalDirection(str, Enum):
    """Explicit direction relative to the relationship assertion."""

    OUTBOUND = "outbound"
    INBOUND = "inbound"


class RelationshipRuntimeError(ValueError):
    """Base error for bounded Typed Relationship runtime invariants."""


class RelationshipIdentityChangeRequiredError(RelationshipRuntimeError):
    """A requested semantic change requires a new Relationship Identity."""


class RelationshipLineageConflictError(RelationshipRuntimeError):
    """Relationship versions cannot form one logical assertion lineage."""


class RelationshipVersionNotFoundError(RelationshipRuntimeError):
    """An exact requested relationship Version Identity is absent."""


@dataclass(frozen=True, slots=True)
class RelationshipEndpoint:
    """One explicit relationship endpoint and its semantic reference role."""

    reference_role: EndpointReferenceRole
    identity: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.reference_role, EndpointReferenceRole):
            raise ValueError("relationship endpoint reference role must be explicit")
        if not isinstance(self.identity, Identity):
            raise ValueError("relationship endpoint identity must be an Identity")


@dataclass(frozen=True, slots=True)
class RelationshipTypeReference:
    """Version-identifiable governed relationship-type definition reference."""

    type_id: Identity
    version_id: Identity
    semantic_name: str
    schema_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.type_id, Identity):
            raise ValueError("relationship type_id must be an Identity")
        if not isinstance(self.version_id, Identity):
            raise ValueError("relationship type version_id must be an Identity")
        if self.type_id == self.version_id:
            raise ValueError("relationship Type Identity and type Version Identity are distinct roles")
        if self.type_id.scope != self.version_id.scope:
            raise ValueError("relationship type identity and version identity must share scope")
        if not isinstance(self.semantic_name, str) or not self.semantic_name.strip():
            raise ValueError("relationship type semantic_name must be explicit")
        if not isinstance(self.schema_version, str) or not self.schema_version.strip():
            raise ValueError("relationship type schema_version must be explicit")


@dataclass(frozen=True, slots=True)
class TypedRelationship:
    """One immutable canonical version of one directed relationship assertion."""

    record: CanonicalRecord
    relationship_type: RelationshipTypeReference
    source: RelationshipEndpoint
    target: RelationshipEndpoint

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Typed Relationship must use a CanonicalRecord envelope")
        if self.record.semantic_type != RELATIONSHIP_RECORD_SEMANTIC_TYPE:
            raise ValueError(
                "Typed Relationship Canonical Record semantic_type must be platform.typed-relationship"
            )
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("bounded P2.03 Typed Relationship runtime supports Native authority only")
        if not isinstance(self.relationship_type, RelationshipTypeReference):
            raise ValueError("relationship type definition reference must be explicit")
        if not isinstance(self.source, RelationshipEndpoint):
            raise ValueError("relationship source endpoint must be explicit")
        if not isinstance(self.target, RelationshipEndpoint):
            raise ValueError("relationship target endpoint must be explicit")

        organization_scope = self.record.organization.organization_id.value
        relationship_identities = (
            self.record.subject_id,
            self.record.version_id,
            self.source.identity,
            self.target.identity,
        )
        if any(identity.scope != organization_scope for identity in relationship_identities):
            raise ValueError(
                "bounded Typed Relationship and both endpoints must share Organization scope"
            )

        required_provenance = {
            self.relationship_type.type_id,
            self.relationship_type.version_id,
            self.source.identity,
            self.target.identity,
        }
        if not required_provenance.issubset(set(self.record.provenance_refs)):
            raise ValueError(
                "Typed Relationship provenance must preserve type and exact endpoint references"
            )
        if self.record.lifecycle_status is not None and (
            not isinstance(self.record.lifecycle_status, str)
            or not self.record.lifecycle_status.strip()
        ):
            raise ValueError("relationship lifecycle_status must be non-empty when supplied")

    @property
    def relationship_id(self) -> Identity:
        """Stable Relationship Identity (RFC-0002 Subject Identity role)."""

        return self.record.subject_id

    @property
    def relationship_version_id(self) -> Identity:
        """Exact immutable Version Identity for this relationship version."""

        return self.record.version_id

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    @property
    def intrinsically_grants_authorization(self) -> bool:
        """Relationship existence alone is never an RFC-0003 authorization grant."""

        return False

    @property
    def intrinsically_grants_organizational_authority(self) -> bool:
        """Relationship existence alone is never Organizational Authority."""

        return False


def _unique_refs(*refs: Identity) -> tuple[Identity, ...]:
    ordered: list[Identity] = []
    seen: set[Identity] = set()
    for ref in refs:
        if not isinstance(ref, Identity):
            raise ValueError("relationship provenance references must be Identity values")
        if ref not in seen:
            ordered.append(ref)
            seen.add(ref)
    return tuple(ordered)


def create_typed_relationship(
    *,
    relationship_id: Identity,
    version_id: Identity,
    relationship_type: RelationshipTypeReference,
    source: RelationshipEndpoint,
    target: RelationshipEndpoint,
    organization: OrganizationScope,
    actor: ActorContext,
    authority_scope: str,
    created_at: datetime,
    lifecycle_status: str | None = "Active",
    effective_from: datetime | None = None,
    effective_until: datetime | None = None,
    payload: tuple[tuple[str, str], ...] = (),
    additional_provenance_refs: tuple[Identity, ...] = (),
    integrity_metadata: tuple[tuple[str, str], ...] = (
        ("representation", "frozen-in-memory-reference"),
    ),
) -> TypedRelationship:
    """Create one initial canonical Typed Relationship version.

    Relationship Identity is supplied independently; it is intentionally not
    derived from the source/type/target tuple because RFC-0002 permits multiple
    assertion instances over an otherwise identical tuple.
    """

    if not isinstance(relationship_id, Identity):
        raise ValueError("relationship_id must be an Identity")
    if not isinstance(version_id, Identity):
        raise ValueError("relationship version_id must be an Identity")
    if relationship_id == version_id:
        raise ValueError("Relationship Identity and Version Identity must be distinct")
    if not isinstance(relationship_type, RelationshipTypeReference):
        raise ValueError("relationship_type must be a RelationshipTypeReference")
    if not isinstance(source, RelationshipEndpoint) or not isinstance(
        target, RelationshipEndpoint
    ):
        raise ValueError("source and target endpoints must be explicit")
    if not isinstance(additional_provenance_refs, tuple):
        raise ValueError("additional_provenance_refs must be an immutable tuple")

    provenance_refs = _unique_refs(
        actor.actual_principal.principal_id,
        relationship_type.type_id,
        relationship_type.version_id,
        source.identity,
        target.identity,
        *additional_provenance_refs,
    )
    record = CanonicalRecord(
        subject_id=relationship_id,
        version_id=version_id,
        semantic_type=RELATIONSHIP_RECORD_SEMANTIC_TYPE,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=authority_scope,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=provenance_refs,
        integrity_metadata=integrity_metadata,
        payload=payload,
        lifecycle_status=lifecycle_status,
        predecessor_version_id=None,
        effective_from=effective_from,
        effective_until=effective_until,
    )
    return TypedRelationship(
        record=record,
        relationship_type=relationship_type,
        source=source,
        target=target,
    )


_UNCHANGED = object()


def version_typed_relationship(
    previous: TypedRelationship,
    *,
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
    relationship_type: RelationshipTypeReference | None = None,
    source: RelationshipEndpoint | None = None,
    target: RelationshipEndpoint | None = None,
    lifecycle_status: str | None | object = _UNCHANGED,
    effective_from: datetime | None | object = _UNCHANGED,
    effective_until: datetime | None | object = _UNCHANGED,
    payload: tuple[tuple[str, str], ...] | None = None,
    additional_provenance_refs: tuple[Identity, ...] = (),
) -> TypedRelationship:
    """Create an immutable successor version of the same logical assertion.

    Endpoint identity/role and semantic relationship type are identity-defining.
    Changing them is rejected so callers must create a new Relationship Identity.
    A new immutable version of the same type definition is allowed when the
    semantic type remains the same, matching RFC-0002 backward-compatible type
    evolution semantics.
    """

    if not isinstance(previous, TypedRelationship):
        raise ValueError("previous must be a TypedRelationship")
    if not isinstance(version_id, Identity):
        raise ValueError("relationship version_id must be an Identity")
    if version_id == previous.relationship_id:
        raise ValueError("Relationship Identity and Version Identity must be distinct")
    if version_id == previous.relationship_version_id:
        raise ValueError("successor relationship version must have a new Version Identity")
    if version_id.scope != previous.relationship_id.scope:
        raise ValueError("relationship successor Version Identity must share Organization scope")
    if actor.organization != previous.organization:
        raise ValueError("relationship version actor must share Organization scope")

    next_type = relationship_type or previous.relationship_type
    next_source = source or previous.source
    next_target = target or previous.target

    if (
        next_type.type_id != previous.relationship_type.type_id
        or next_type.semantic_name != previous.relationship_type.semantic_name
    ):
        raise RelationshipIdentityChangeRequiredError(
            "semantic relationship type change requires a new Relationship Identity"
        )
    if next_source != previous.source:
        raise RelationshipIdentityChangeRequiredError(
            "source identity or source reference role change requires a new Relationship Identity"
        )
    if next_target != previous.target:
        raise RelationshipIdentityChangeRequiredError(
            "target identity or target reference role change requires a new Relationship Identity"
        )

    next_lifecycle = (
        previous.record.lifecycle_status
        if lifecycle_status is _UNCHANGED
        else lifecycle_status
    )
    next_effective_from = (
        previous.record.effective_from if effective_from is _UNCHANGED else effective_from
    )
    next_effective_until = (
        previous.record.effective_until if effective_until is _UNCHANGED else effective_until
    )
    next_payload = previous.record.payload if payload is None else payload

    provenance_refs = _unique_refs(
        actor.actual_principal.principal_id,
        next_type.type_id,
        next_type.version_id,
        next_source.identity,
        next_target.identity,
        previous.relationship_version_id,
        *additional_provenance_refs,
    )
    record = CanonicalRecord(
        subject_id=previous.relationship_id,
        version_id=version_id,
        semantic_type=RELATIONSHIP_RECORD_SEMANTIC_TYPE,
        schema_version=previous.record.schema_version,
        organization=previous.organization,
        authority_mode=previous.record.authority_mode,
        authority_scope=previous.record.authority_scope,
        accountable_owner_id=previous.record.accountable_owner_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=provenance_refs,
        integrity_metadata=previous.record.integrity_metadata,
        payload=next_payload,
        lifecycle_status=next_lifecycle,  # type: ignore[arg-type]
        predecessor_version_id=previous.relationship_version_id,
        effective_from=next_effective_from,  # type: ignore[arg-type]
        effective_until=next_effective_until,  # type: ignore[arg-type]
    )
    return TypedRelationship(
        record=record,
        relationship_type=next_type,
        source=next_source,
        target=next_target,
    )


@dataclass(frozen=True, slots=True)
class TypedRelationshipLineage:
    """Validated immutable versions of one logical relationship assertion."""

    relationships: tuple[TypedRelationship, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.relationships, tuple) or not self.relationships:
            raise RelationshipLineageConflictError(
                "relationship lineage requires at least one canonical relationship version"
            )
        if any(
            not isinstance(relationship, TypedRelationship)
            for relationship in self.relationships
        ):
            raise RelationshipLineageConflictError(
                "relationship lineage may contain only TypedRelationship versions"
            )

        first = self.relationships[0]
        stable_assertion_semantics = (
            ("Relationship Identity", lambda item: item.relationship_id),
            ("relationship type identity", lambda item: item.relationship_type.type_id),
            ("semantic relationship type", lambda item: item.relationship_type.semantic_name),
            ("source endpoint", lambda item: item.source),
            ("target endpoint", lambda item: item.target),
        )
        for label, selector in stable_assertion_semantics:
            expected = selector(first)
            if any(
                selector(relationship) != expected
                for relationship in self.relationships[1:]
            ):
                raise RelationshipLineageConflictError(
                    f"relationship lineage must preserve one {label}"
                )

        try:
            CanonicalLineage(tuple(item.record for item in self.relationships))
        except ValueError as exc:
            raise RelationshipLineageConflictError(str(exc)) from exc

    @property
    def relationship_id(self) -> Identity:
        return self.relationships[0].relationship_id

    @property
    def _canonical_lineage(self) -> CanonicalLineage:
        return CanonicalLineage(tuple(item.record for item in self.relationships))

    @property
    def head(self) -> TypedRelationship:
        head_version_id = self._canonical_lineage.head.version_id
        return self.resolve_version(head_version_id)

    def resolve_version(self, version_id: Identity) -> TypedRelationship:
        if not isinstance(version_id, Identity):
            raise TypeError("exact relationship version resolution requires an Identity")
        for relationship in self.relationships:
            if relationship.relationship_version_id == version_id:
                return relationship
        raise RelationshipVersionNotFoundError(
            f"relationship Version Identity is not present in lineage: {version_id.value}"
        )

    def resolve_effective(self, *, at: datetime) -> TypedRelationship:
        resolved = self._canonical_lineage.resolve_effective(at=at)
        return self.resolve_version(resolved.version_id)


@dataclass(frozen=True, slots=True)
class RelationshipTraversalMatch:
    """One semantic traversal result over an exact relationship version."""

    relationship: TypedRelationship
    matched_endpoint: RelationshipEndpoint
    opposite_endpoint: RelationshipEndpoint
    direction: TraversalDirection


def traverse_relationships(
    relationships: tuple[TypedRelationship, ...],
    *,
    endpoint: RelationshipEndpoint,
    direction: TraversalDirection,
) -> tuple[RelationshipTraversalMatch, ...]:
    """Traverse exact immutable relationship versions without hidden resolution.

    The function is intentionally a tuple scan, proving reusable traversal
    semantics without introducing a graph-database or index authority assumption.
    Subject-level and version-pinned endpoints compare as different values even
    when they carry the same underlying Identity.
    """

    if not isinstance(relationships, tuple):
        raise TypeError("relationships must be supplied as an immutable tuple")
    if any(not isinstance(item, TypedRelationship) for item in relationships):
        raise TypeError("relationships may contain only TypedRelationship versions")
    if not isinstance(endpoint, RelationshipEndpoint):
        raise TypeError("traversal endpoint must be a RelationshipEndpoint")
    if not isinstance(direction, TraversalDirection):
        raise TypeError("traversal direction must be explicit")

    matches: list[RelationshipTraversalMatch] = []
    for relationship in relationships:
        if direction is TraversalDirection.OUTBOUND:
            matched = relationship.source
            opposite = relationship.target
        else:
            matched = relationship.target
            opposite = relationship.source
        if matched == endpoint:
            matches.append(
                RelationshipTraversalMatch(
                    relationship=relationship,
                    matched_endpoint=matched,
                    opposite_endpoint=opposite,
                    direction=direction,
                )
            )
    return tuple(matches)
