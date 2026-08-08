"""P4.03 — bounded Canonical Record / Relationship inspection experience.

Internal read-only presentation/resolution boundary over Accepted RFC-0002
Canonical Record, lineage and Typed Relationship semantics. It is deliberately
not a public API/SDK, route or wire schema, durable read model, authorization
engine, policy engine, graph database, Product Contract or mutation path.

Workspace references express operator intent only. Before governed source
resolution, the caller must supply one current authorization decision bound to
the exact Actor, Organization and requested Subject Identity. The source is then
resolved from its own governed Organization metadata; ``Identity.scope`` text,
identifier syntax and presentation wrappers are never treated as proof of
membership, access or authority.

Canonical Head, Effective Version and an exact historical Version remain
separate concepts. Missing/ambiguous Effective Version is explicit and never
falls back to Head. Relationship visibility likewise grants neither
Authorization nor Organizational Authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from html import escape

from .canonical import AuthorityMode, CanonicalRecord
from .canonical_lineage import (
    AmbiguousEffectiveVersionError,
    CanonicalLineage,
    CanonicalVersionNotFoundError,
    NoEffectiveVersionError,
)
from .identity import Identity
from .relationships import (
    EndpointReferenceRole,
    RelationshipVersionNotFoundError,
    TraversalDirection,
    TypedRelationship,
    TypedRelationshipLineage,
)
from .security import ActorContext, OrganizationScope
from .workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceShellState,
)


class InspectionObjectKind(str, Enum):
    RECORD = "Canonical Record"
    RELATIONSHIP = "Typed Relationship"


class InspectionReferenceBasis(str, Enum):
    CANONICAL_HEAD = "Canonical Head"
    EXACT_VERSION = "Exact Version"


class EffectiveResolutionStatus(str, Enum):
    RESOLVED = "Resolved"
    MISSING = "Missing"
    AMBIGUOUS = "Ambiguous"


class SourceValidationState(str, Enum):
    """Bounded structural meaning; never a business approval claim."""

    STRUCTURALLY_VALIDATED = "Structurally validated canonical lineage"


class InspectionBlockCode(str, Enum):
    REFERENCE_REQUIRED = "reference-required"
    SOURCE_UNAVAILABLE = "source-unavailable"
    SOURCE_AMBIGUOUS = "source-ambiguous"
    ACCESS_DENIED = "access-denied"
    VERSION_UNAVAILABLE = "version-unavailable"


@dataclass(frozen=True, slots=True)
class CurrentSourceAuthorization:
    """Caller-supplied current source-access decision evidence.

    This bounded harness value consumes an authorization result; it does not
    decide permissions. Purpose/right/classification policy remains owned by the
    applicable authorization/data-governance boundary.
    """

    organization: OrganizationScope
    actor_actual_principal_id: Identity
    resource_subject_id: Identity
    decision_version_id: Identity
    allowed: bool
    represented_principal_id: Identity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("authorization Organization scope must be explicit")
        for label, value in (
            ("actor_actual_principal_id", self.actor_actual_principal_id),
            ("resource_subject_id", self.resource_subject_id),
            ("decision_version_id", self.decision_version_id),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.represented_principal_id is not None and not isinstance(
            self.represented_principal_id, Identity
        ):
            raise ValueError("represented_principal_id must be an Identity when supplied")
        if not isinstance(self.allowed, bool):
            raise ValueError("authorization decision must be explicit")


@dataclass(frozen=True, slots=True)
class GovernedInspectionSourceSet:
    """Current governed sources supplied by their owning runtime boundaries."""

    record_lineages: tuple[CanonicalLineage, ...] = ()
    relationship_lineages: tuple[TypedRelationshipLineage, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.record_lineages, tuple) or any(
            not isinstance(value, CanonicalLineage) for value in self.record_lineages
        ):
            raise ValueError("record_lineages must contain CanonicalLineage values")
        if not isinstance(self.relationship_lineages, tuple) or any(
            not isinstance(value, TypedRelationshipLineage)
            for value in self.relationship_lineages
        ):
            raise ValueError(
                "relationship_lineages must contain TypedRelationshipLineage values"
            )


@dataclass(frozen=True, slots=True)
class EffectiveVersionInspection:
    status: EffectiveResolutionStatus
    evaluated_at: datetime
    version_id: Identity | None
    status_text: str


@dataclass(frozen=True, slots=True)
class AuthorityInspection:
    mode: AuthorityMode
    authority_scope: str
    authoritative_source_text: str


@dataclass(frozen=True, slots=True)
class ImmutableVersionInspection:
    version_id: Identity
    predecessor_version_id: Identity | None
    created_at: datetime
    lifecycle_status: str | None
    effective_from: datetime | None
    effective_until: datetime | None
    schema_version: str
    is_head: bool
    is_effective: bool
    is_displayed: bool


@dataclass(frozen=True, slots=True)
class RelationshipGraphEdgeInspection:
    relationship_id: Identity
    head_version_id: Identity
    effective: EffectiveVersionInspection
    relationship_type_id: Identity
    relationship_type_version_id: Identity
    relationship_type_name: str
    direction: TraversalDirection
    matched_endpoint_role: EndpointReferenceRole
    matched_endpoint_id: Identity
    opposite_endpoint_role: EndpointReferenceRole
    opposite_endpoint_id: Identity
    lifecycle_status: str | None
    accountable_owner_id: Identity
    authority: AuthorityInspection


@dataclass(frozen=True, slots=True)
class CanonicalRecordInspection:
    object_kind: InspectionObjectKind
    organization: OrganizationScope
    actor: ActorContext
    subject_id: Identity
    reference_basis: InspectionReferenceBasis
    displayed_version_id: Identity
    head_version_id: Identity
    effective: EffectiveVersionInspection
    semantic_type: str
    schema_version: str
    lifecycle_status: str | None
    accountable_owner_id: Identity
    authority: AuthorityInspection
    validation_state: SourceValidationState
    payload: tuple[tuple[str, str], ...]
    immutable_versions: tuple[ImmutableVersionInspection, ...]
    relationships: tuple[RelationshipGraphEdgeInspection, ...]
    authorization_decision_version_id: Identity
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE


@dataclass(frozen=True, slots=True)
class RelationshipInspection:
    object_kind: InspectionObjectKind
    organization: OrganizationScope
    actor: ActorContext
    relationship_id: Identity
    reference_basis: InspectionReferenceBasis
    displayed_version_id: Identity
    head_version_id: Identity
    effective: EffectiveVersionInspection
    relationship_type_id: Identity
    relationship_type_version_id: Identity
    relationship_type_name: str
    relationship_type_schema_version: str
    source_role: EndpointReferenceRole
    source_id: Identity
    target_role: EndpointReferenceRole
    target_id: Identity
    lifecycle_status: str | None
    accountable_owner_id: Identity
    authority: AuthorityInspection
    validation_state: SourceValidationState
    payload: tuple[tuple[str, str], ...]
    immutable_versions: tuple[ImmutableVersionInspection, ...]
    authorization_decision_version_id: Identity
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE


@dataclass(frozen=True, slots=True)
class CanonicalInspectionBlockedState:
    """Fail-closed state carrying no governed source content."""

    code: InspectionBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, InspectionBlockCode):
            raise ValueError("inspection block code must be explicit")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("inspection blocked state requires textual meaning")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("inspection presentation cannot become canonical authority")
        if self.governed_content_visible:
            raise ValueError("blocked inspection state must expose no governed content")


CanonicalInspectionResult = (
    CanonicalRecordInspection | RelationshipInspection | CanonicalInspectionBlockedState
)
NavigationReference = SubjectNavigationReference | ExactVersionNavigationReference
InspectionLineage = CanonicalLineage | TypedRelationshipLineage


def _require_aware_datetime(value: datetime) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("effective_at must be a timezone-aware datetime")


def _actor_represented_id(actor: ActorContext) -> Identity | None:
    return (
        None
        if actor.represented_principal is None
        else actor.represented_principal.principal_id
    )


def _matching_authorization(
    *,
    authorizations: tuple[CurrentSourceAuthorization, ...],
    actor: ActorContext,
    organization: OrganizationScope,
    resource_subject_id: Identity,
) -> CurrentSourceAuthorization | None:
    matches = tuple(
        decision
        for decision in authorizations
        if decision.organization == organization
        and decision.actor_actual_principal_id == actor.actual_principal.principal_id
        and decision.represented_principal_id == _actor_represented_id(actor)
        and decision.resource_subject_id == resource_subject_id
    )
    if len(matches) != 1 or matches[0].allowed is not True:
        return None
    return matches[0]


def _relationship_record(lineage: TypedRelationshipLineage) -> CanonicalRecord:
    return lineage.relationships[0].record


def _source_candidates(
    *,
    sources: GovernedInspectionSourceSet,
    organization: OrganizationScope,
    subject_id: Identity,
) -> tuple[tuple[InspectionObjectKind, InspectionLineage], ...]:
    """Use source-owned Organization metadata; never infer it from Identity.scope."""

    matches: list[tuple[InspectionObjectKind, InspectionLineage]] = []
    for lineage in sources.record_lineages:
        if lineage.records[0].organization == organization and lineage.subject_id == subject_id:
            matches.append((InspectionObjectKind.RECORD, lineage))
    for lineage in sources.relationship_lineages:
        source_record = _relationship_record(lineage)
        if source_record.organization == organization and lineage.relationship_id == subject_id:
            matches.append((InspectionObjectKind.RELATIONSHIP, lineage))
    return tuple(matches)


def _authority(record: CanonicalRecord) -> AuthorityInspection:
    source_text = {
        AuthorityMode.NATIVE: "Native Arvectum OS canonical source",
        AuthorityMode.EXTERNAL_REFERENCE: "External authoritative source reference",
        AuthorityMode.GOVERNED_REPLICA: "Governed replica of an external authoritative source",
    }[record.authority_mode]
    return AuthorityInspection(record.authority_mode, record.authority_scope, source_text)


def _effective_record(
    lineage: CanonicalLineage, *, at: datetime
) -> tuple[EffectiveVersionInspection, CanonicalRecord | None]:
    try:
        value = lineage.resolve_effective(at=at)
    except NoEffectiveVersionError:
        return (
            EffectiveVersionInspection(
                EffectiveResolutionStatus.MISSING,
                at,
                None,
                "No canonical version is effective at the declared evaluation time.",
            ),
            None,
        )
    except AmbiguousEffectiveVersionError:
        return (
            EffectiveVersionInspection(
                EffectiveResolutionStatus.AMBIGUOUS,
                at,
                None,
                "Multiple canonical versions are effective; no version was selected.",
            ),
            None,
        )
    return (
        EffectiveVersionInspection(
            EffectiveResolutionStatus.RESOLVED,
            at,
            value.version_id,
            "A unique Effective Version was resolved from governed applicability.",
        ),
        value,
    )


def _effective_relationship(
    lineage: TypedRelationshipLineage, *, at: datetime
) -> tuple[EffectiveVersionInspection, TypedRelationship | None]:
    try:
        value = lineage.resolve_effective(at=at)
    except NoEffectiveVersionError:
        return (
            EffectiveVersionInspection(
                EffectiveResolutionStatus.MISSING,
                at,
                None,
                "No relationship version is effective at the declared evaluation time.",
            ),
            None,
        )
    except AmbiguousEffectiveVersionError:
        return (
            EffectiveVersionInspection(
                EffectiveResolutionStatus.AMBIGUOUS,
                at,
                None,
                "Multiple relationship versions are effective; no version was selected.",
            ),
            None,
        )
    return (
        EffectiveVersionInspection(
            EffectiveResolutionStatus.RESOLVED,
            at,
            value.relationship_version_id,
            "A unique Effective Version was resolved from governed applicability.",
        ),
        value,
    )


def _ordered_records(records: tuple[CanonicalRecord, ...]) -> tuple[CanonicalRecord, ...]:
    root = next(value for value in records if value.predecessor_version_id is None)
    child_by_predecessor = {
        value.predecessor_version_id: value
        for value in records
        if value.predecessor_version_id is not None
    }
    ordered = [root]
    cursor = root
    while cursor.version_id in child_by_predecessor:
        cursor = child_by_predecessor[cursor.version_id]
        ordered.append(cursor)
    return tuple(ordered)


def _history(
    records: tuple[CanonicalRecord, ...],
    *,
    head_version_id: Identity,
    effective_version_id: Identity | None,
    displayed_version_id: Identity,
) -> tuple[ImmutableVersionInspection, ...]:
    return tuple(
        ImmutableVersionInspection(
            version_id=value.version_id,
            predecessor_version_id=value.predecessor_version_id,
            created_at=value.created_at,
            lifecycle_status=value.lifecycle_status,
            effective_from=value.effective_from,
            effective_until=value.effective_until,
            schema_version=value.schema_version,
            is_head=value.version_id == head_version_id,
            is_effective=value.version_id == effective_version_id,
            is_displayed=value.version_id == displayed_version_id,
        )
        for value in _ordered_records(records)
    )


def _record_focus(
    lineage: CanonicalLineage, reference: NavigationReference
) -> tuple[InspectionReferenceBasis, CanonicalRecord] | None:
    if isinstance(reference, SubjectNavigationReference):
        return InspectionReferenceBasis.CANONICAL_HEAD, lineage.head
    try:
        return InspectionReferenceBasis.EXACT_VERSION, lineage.resolve_version(reference.version_id)
    except CanonicalVersionNotFoundError:
        return None


def _relationship_focus(
    lineage: TypedRelationshipLineage, reference: NavigationReference
) -> tuple[InspectionReferenceBasis, TypedRelationship] | None:
    if isinstance(reference, SubjectNavigationReference):
        return InspectionReferenceBasis.CANONICAL_HEAD, lineage.head
    try:
        return InspectionReferenceBasis.EXACT_VERSION, lineage.resolve_version(reference.version_id)
    except RelationshipVersionNotFoundError:
        return None


def _relationship_edges(
    *,
    record: CanonicalRecord,
    sources: GovernedInspectionSourceSet,
    authorizations: tuple[CurrentSourceAuthorization, ...],
    actor: ActorContext,
    organization: OrganizationScope,
    effective_at: datetime,
) -> tuple[RelationshipGraphEdgeInspection, ...]:
    """Return only independently authorized edges; omitted edges reveal no count."""

    identity_by_role = {
        EndpointReferenceRole.SUBJECT_IDENTITY: record.subject_id,
        EndpointReferenceRole.VERSION_IDENTITY: record.version_id,
    }
    edges: list[RelationshipGraphEdgeInspection] = []
    for lineage in sources.relationship_lineages:
        source_record = _relationship_record(lineage)
        if source_record.organization != organization:
            continue
        if _matching_authorization(
            authorizations=authorizations,
            actor=actor,
            organization=organization,
            resource_subject_id=lineage.relationship_id,
        ) is None:
            continue

        head = lineage.head
        effective, _ = _effective_relationship(lineage, at=effective_at)
        for direction, matched, opposite in (
            (TraversalDirection.OUTBOUND, head.source, head.target),
            (TraversalDirection.INBOUND, head.target, head.source),
        ):
            if matched.identity != identity_by_role[matched.reference_role]:
                continue
            edges.append(
                RelationshipGraphEdgeInspection(
                    relationship_id=head.relationship_id,
                    head_version_id=head.relationship_version_id,
                    effective=effective,
                    relationship_type_id=head.relationship_type.type_id,
                    relationship_type_version_id=head.relationship_type.version_id,
                    relationship_type_name=head.relationship_type.semantic_name,
                    direction=direction,
                    matched_endpoint_role=matched.reference_role,
                    matched_endpoint_id=matched.identity,
                    opposite_endpoint_role=opposite.reference_role,
                    opposite_endpoint_id=opposite.identity,
                    lifecycle_status=head.record.lifecycle_status,
                    accountable_owner_id=head.record.accountable_owner_id,
                    authority=_authority(head.record),
                )
            )
    return tuple(edges)


def inspect_current_workspace_reference(
    state: WorkspaceShellState,
    *,
    sources: GovernedInspectionSourceSet,
    authorizations: tuple[CurrentSourceAuthorization, ...],
    effective_at: datetime,
) -> CanonicalInspectionResult:
    """Resolve the current workspace reference as an authorized read-only view."""

    if not isinstance(state, WorkspaceShellState):
        raise ValueError("canonical inspection requires an open WorkspaceShellState")
    if not isinstance(sources, GovernedInspectionSourceSet):
        raise ValueError("sources must be a GovernedInspectionSourceSet")
    if not isinstance(authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization) for value in authorizations
    ):
        raise ValueError("authorizations must contain CurrentSourceAuthorization values")
    _require_aware_datetime(effective_at)

    reference = state.current_reference
    if not isinstance(reference, (SubjectNavigationReference, ExactVersionNavigationReference)):
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.REFERENCE_REQUIRED,
            "Choose a governed Subject or exact Version before inspection.",
        )
    if reference.organization != state.organization:
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.SOURCE_UNAVAILABLE,
            "The governed source is unavailable in the current Organization context.",
        )

    # Authorization is checked before existence, multiplicity or exact-version
    # resolution so an unauthorized caller cannot use status differences as a
    # resource-discovery oracle. This decision does not prove source membership;
    # source-owned Organization metadata is checked independently below.
    authorization = _matching_authorization(
        authorizations=authorizations,
        actor=state.actor,
        organization=state.organization,
        resource_subject_id=reference.subject_id,
    )
    if authorization is None:
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.ACCESS_DENIED,
            "Current source access is not authorized for this inspection.",
        )

    candidates = _source_candidates(
        sources=sources,
        organization=state.organization,
        subject_id=reference.subject_id,
    )
    if not candidates:
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.SOURCE_UNAVAILABLE,
            "The governed source is unavailable in the current Organization context.",
        )
    if len(candidates) != 1:
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.SOURCE_AMBIGUOUS,
            "The governed source cannot be resolved unambiguously; no source content was selected.",
        )

    object_kind, lineage = candidates[0]
    if object_kind is InspectionObjectKind.RECORD:
        assert isinstance(lineage, CanonicalLineage)
        focus = _record_focus(lineage, reference)
        if focus is None:
            return CanonicalInspectionBlockedState(
                InspectionBlockCode.VERSION_UNAVAILABLE,
                "The requested exact Version is unavailable. No Canonical Head fallback was applied.",
            )
        reference_basis, displayed = focus
        head = lineage.head
        effective, effective_record = _effective_record(lineage, at=effective_at)
        effective_version_id = None if effective_record is None else effective_record.version_id
        return CanonicalRecordInspection(
            object_kind=InspectionObjectKind.RECORD,
            organization=displayed.organization,
            actor=state.actor,
            subject_id=displayed.subject_id,
            reference_basis=reference_basis,
            displayed_version_id=displayed.version_id,
            head_version_id=head.version_id,
            effective=effective,
            semantic_type=displayed.semantic_type,
            schema_version=displayed.schema_version,
            lifecycle_status=displayed.lifecycle_status,
            accountable_owner_id=displayed.accountable_owner_id,
            authority=_authority(displayed),
            validation_state=SourceValidationState.STRUCTURALLY_VALIDATED,
            payload=displayed.payload,
            immutable_versions=_history(
                lineage.records,
                head_version_id=head.version_id,
                effective_version_id=effective_version_id,
                displayed_version_id=displayed.version_id,
            ),
            relationships=_relationship_edges(
                record=displayed,
                sources=sources,
                authorizations=authorizations,
                actor=state.actor,
                organization=state.organization,
                effective_at=effective_at,
            ),
            authorization_decision_version_id=authorization.decision_version_id,
        )

    assert isinstance(lineage, TypedRelationshipLineage)
    focus = _relationship_focus(lineage, reference)
    if focus is None:
        return CanonicalInspectionBlockedState(
            InspectionBlockCode.VERSION_UNAVAILABLE,
            "The requested exact Version is unavailable. No Relationship Head fallback was applied.",
        )
    reference_basis, displayed = focus
    head = lineage.head
    effective, effective_relationship = _effective_relationship(lineage, at=effective_at)
    effective_version_id = (
        None
        if effective_relationship is None
        else effective_relationship.relationship_version_id
    )
    return RelationshipInspection(
        object_kind=InspectionObjectKind.RELATIONSHIP,
        organization=displayed.organization,
        actor=state.actor,
        relationship_id=displayed.relationship_id,
        reference_basis=reference_basis,
        displayed_version_id=displayed.relationship_version_id,
        head_version_id=head.relationship_version_id,
        effective=effective,
        relationship_type_id=displayed.relationship_type.type_id,
        relationship_type_version_id=displayed.relationship_type.version_id,
        relationship_type_name=displayed.relationship_type.semantic_name,
        relationship_type_schema_version=displayed.relationship_type.schema_version,
        source_role=displayed.source.reference_role,
        source_id=displayed.source.identity,
        target_role=displayed.target.reference_role,
        target_id=displayed.target.identity,
        lifecycle_status=displayed.record.lifecycle_status,
        accountable_owner_id=displayed.record.accountable_owner_id,
        authority=_authority(displayed.record),
        validation_state=SourceValidationState.STRUCTURALLY_VALIDATED,
        payload=displayed.record.payload,
        immutable_versions=_history(
            tuple(value.record for value in lineage.relationships),
            head_version_id=head.relationship_version_id,
            effective_version_id=effective_version_id,
            displayed_version_id=displayed.relationship_version_id,
        ),
        authorization_decision_version_id=authorization.decision_version_id,
    )


def _identity_text(value: Identity) -> str:
    return f"{value.namespace}:{value.value} [{value.scope}]"


def _datetime_text(value: datetime | None) -> str:
    return "—" if value is None else value.isoformat()


def _effective_html(value: EffectiveVersionInspection) -> str:
    version = "—" if value.version_id is None else escape(_identity_text(value.version_id))
    return (
        '<section data-inspection-section="effective-version"><h2>Effective Version</h2>'
        f'<p>Status: <strong>{escape(value.status.value)}</strong></p>'
        f'<p>Evaluated at: {escape(value.evaluated_at.isoformat())}</p>'
        f'<p>Version: {version}</p><p>{escape(value.status_text)}</p></section>'
    )


def _authority_html(value: AuthorityInspection) -> str:
    return (
        '<section data-inspection-section="authority"><h2>Authority</h2>'
        f'<p>Authority mode: {escape(value.mode.value)}</p>'
        f'<p>Authoritative source: {escape(value.authoritative_source_text)}</p>'
        f'<p>Authority scope: {escape(value.authority_scope)}</p></section>'
    )


def _payload_html(payload: tuple[tuple[str, str], ...]) -> str:
    if not payload:
        return '<p data-inspection-payload="empty">No payload fields in this bounded view.</p>'
    rows = "".join(
        f"<tr><th>{escape(key)}</th><td>{escape(value)}</td></tr>"
        for key, value in payload
    )
    return (
        '<table data-inspection-payload="read-only"><caption>Displayed version payload</caption>'
        f"<tbody>{rows}</tbody></table>"
    )


def _history_html(values: tuple[ImmutableVersionInspection, ...]) -> str:
    rows: list[str] = []
    for value in values:
        labels = []
        if value.is_displayed:
            labels.append("Displayed")
        if value.is_head:
            labels.append("Head")
        if value.is_effective:
            labels.append("Effective")
        meaning = ", ".join(labels) if labels else "Historical"
        predecessor = (
            "—"
            if value.predecessor_version_id is None
            else escape(_identity_text(value.predecessor_version_id))
        )
        rows.append(
            "<tr>"
            f"<td>{escape(_identity_text(value.version_id))}</td>"
            f"<td>{escape(meaning)}</td>"
            f"<td>{escape(value.lifecycle_status or '—')}</td>"
            f"<td>{escape(value.schema_version)}</td>"
            f"<td>{predecessor}</td>"
            f"<td>{escape(_datetime_text(value.effective_from))}</td>"
            f"<td>{escape(_datetime_text(value.effective_until))}</td>"
            "</tr>"
        )
    return (
        '<section data-inspection-section="immutable-history"><h2>Immutable version history</h2>'
        '<table><caption>Exact immutable Canonical Record versions</caption>'
        '<thead><tr><th>Version Identity</th><th>Meaning</th><th>Lifecycle</th>'
        '<th>Schema</th><th>Predecessor</th><th>Effective from</th>'
        '<th>Effective until</th></tr></thead><tbody>'
        + "".join(rows)
        + "</tbody></table></section>"
    )


def _graph_html(values: tuple[RelationshipGraphEdgeInspection, ...]) -> str:
    if not values:
        return (
            '<section data-inspection-section="relationships"><h2>Relationship context</h2>'
            '<p>No authorized relationship context is available for the displayed version. '
            'No hidden relationship count is disclosed.</p></section>'
        )
    items = []
    for value in values:
        effective_text = value.effective.status.value
        if value.effective.version_id is not None:
            effective_text += f": {_identity_text(value.effective.version_id)}"
        items.append(
            '<li data-relationship-edge="true">'
            f'<strong>{escape(value.relationship_type_name)}</strong> — '
            f'{escape(value.direction.value)}; matched endpoint '
            f'{escape(value.matched_endpoint_role.value)} '
            f'{escape(_identity_text(value.matched_endpoint_id))}; opposite endpoint '
            f'{escape(value.opposite_endpoint_role.value)} '
            f'{escape(_identity_text(value.opposite_endpoint_id))}. '
            f'Relationship: {escape(_identity_text(value.relationship_id))}; '
            f'Head: {escape(_identity_text(value.head_version_id))}; '
            f'Effective: {escape(effective_text)}; '
            f'Lifecycle: {escape(value.lifecycle_status or "—")}.</li>'
        )
    return (
        '<section data-inspection-section="relationships"><h2>Relationship context</h2><ul>'
        + "".join(items)
        + "</ul></section>"
    )


def render_canonical_inspection_html(result: CanonicalInspectionResult) -> str:
    """Render readable inert HTML with no route/action/mutation contract."""

    if isinstance(result, CanonicalInspectionBlockedState):
        return (
            '<section data-canonical-inspection="blocked"><h1>Governed object unavailable</h1>'
            f'<p role="alert">{escape(result.status_text)}</p>'
            '<p>No governed source content is exposed.</p></section>'
        )

    if isinstance(result, CanonicalRecordInspection):
        return (
            '<article data-canonical-inspection="record" '
            'data-presentation-authority="non-authoritative">'
            '<header><h1>Canonical Record inspection</h1>'
            f'<p>Subject Identity: {escape(_identity_text(result.subject_id))}</p>'
            f'<p>Displayed version: {escape(_identity_text(result.displayed_version_id))} '
            f'({escape(result.reference_basis.value)})</p>'
            f'<p>Canonical Head: {escape(_identity_text(result.head_version_id))}</p>'
            f'<p>Organization: {escape(_identity_text(result.organization.organization_id))}</p>'
            f'<p>Accountable owner: {escape(_identity_text(result.accountable_owner_id))}</p>'
            f'<p>Semantic type: {escape(result.semantic_type)} / schema {escape(result.schema_version)}</p>'
            f'<p>Lifecycle: {escape(result.lifecycle_status or "—")}</p>'
            f'<p>Source validation: {escape(result.validation_state.value)}; '
            'this is not business approval or Organizational Authority.</p></header>'
            + _effective_html(result.effective)
            + _authority_html(result.authority)
            + '<section data-inspection-section="payload"><h2>Displayed version</h2>'
            + _payload_html(result.payload)
            + "</section>"
            + _history_html(result.immutable_versions)
            + _graph_html(result.relationships)
            + '<footer><p>Read-only non-authoritative presentation. Identity possession, '
            'relationship existence and visibility do not grant access, approval or '
            'Organizational Authority.</p></footer></article>'
        )

    if not isinstance(result, RelationshipInspection):
        raise ValueError("result must be a canonical inspection result")
    return (
        '<article data-canonical-inspection="relationship" '
        'data-presentation-authority="non-authoritative">'
        '<header><h1>Typed Relationship inspection</h1>'
        f'<p>Relationship Identity: {escape(_identity_text(result.relationship_id))}</p>'
        f'<p>Displayed version: {escape(_identity_text(result.displayed_version_id))} '
        f'({escape(result.reference_basis.value)})</p>'
        f'<p>Relationship Head: {escape(_identity_text(result.head_version_id))}</p>'
        f'<p>Organization: {escape(_identity_text(result.organization.organization_id))}</p>'
        f'<p>Accountable owner: {escape(_identity_text(result.accountable_owner_id))}</p>'
        f'<p>Lifecycle: {escape(result.lifecycle_status or "—")}</p>'
        f'<p>Source validation: {escape(result.validation_state.value)}; '
        'this is not business approval or Organizational Authority.</p></header>'
        + _effective_html(result.effective)
        + _authority_html(result.authority)
        + '<section data-inspection-section="relationship-semantics"><h2>Relationship semantics</h2>'
        f'<p>Type: {escape(result.relationship_type_name)} — '
        f'{escape(_identity_text(result.relationship_type_id))} / type version '
        f'{escape(_identity_text(result.relationship_type_version_id))} / schema '
        f'{escape(result.relationship_type_schema_version)}</p>'
        f'<p>Source endpoint: {escape(result.source_role.value)} '
        f'{escape(_identity_text(result.source_id))}</p>'
        f'<p>Target endpoint: {escape(result.target_role.value)} '
        f'{escape(_identity_text(result.target_id))}</p></section>'
        + '<section data-inspection-section="payload"><h2>Displayed relationship version</h2>'
        + _payload_html(result.payload)
        + "</section>"
        + _history_html(result.immutable_versions)
        + '<footer><p>Read-only non-authoritative presentation. Relationship existence '
        'does not grant Authorization or Organizational Authority.</p></footer></article>'
    )
