"""P4.07 — bounded Memory / Knowledge / Search discovery experience.

Internal, reversible presentation/resolution adapter over existing CAP-002,
CAP-003, P3.07 and P4.02 semantics. It is not a public API, search/vector/RAG
contract, durable read model, ranking policy, authorization engine, Knowledge
promotion workflow, frontend boundary or Active Platform Capability.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .canonical import AuthorityMode, CanonicalRecord
from .canonical_inspection import CurrentSourceAuthorization
from .canonical_lineage import CanonicalLineage
from .cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
    resolve_search_hit_for_access,
    retrieve_knowledge_for_access,
    search_for_access,
)
from .identity import Identity
from .memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE,
    ExactKnowledgeReliance,
    KnowledgeCandidate,
    KnowledgeConstraints,
    LearningRole,
    MemoryItem,
    Observation,
    ValidatedKnowledge,
    resolve_exact_knowledge_reliance,
)
from .search_index_projection import (
    GovernedSearchSource,
    ProjectionSourceState,
    SearchHit,
    SearchProjection,
)
from .security import ActorContext, OrganizationScope
from .workspace_shell import PresentationAuthority, WorkspaceDestination, WorkspaceShellState


class KnowledgeDiscoveryError(ValueError):
    pass


class KnowledgeRelianceError(KnowledgeDiscoveryError):
    pass


class DiscoveryBlockCode(str, Enum):
    ACCESS_CONTEXT_MISMATCH = "access-context-mismatch"
    DESTINATION_MISMATCH = "destination-mismatch"


class CanonicalKnowledgeState(str, Enum):
    NON_CANONICAL = "Non-canonical learning state"
    MEMORY = "Governed Organizational Memory"
    KNOWLEDGE = "Validated Knowledge"


class ExactRelianceState(str, Enum):
    NOT_APPLICABLE = "Not applicable"
    AVAILABLE = "Available after explicit exact Knowledge Version selection"
    STALE = "Unavailable under current freshness state"


class DiscoveryAuthority(str, Enum):
    DERIVED = "Derived discovery/projection — non-authoritative"


@dataclass(frozen=True, slots=True)
class ObservationSource:
    observation: Observation
    constraints: KnowledgeConstraints

    def __post_init__(self) -> None:
        if not isinstance(self.observation, Observation):
            raise ValueError("observation must be explicit")
        if not isinstance(self.constraints, KnowledgeConstraints):
            raise ValueError("observation constraints must be explicit")


@dataclass(frozen=True, slots=True)
class MemoryKnowledgeSearchSources:
    observations: tuple[ObservationSource, ...] = ()
    memories: tuple[MemoryItem, ...] = ()
    candidates: tuple[KnowledgeCandidate, ...] = ()
    knowledge: tuple[ValidatedKnowledge, ...] = ()
    knowledge_lineages: tuple[CanonicalLineage, ...] = ()
    search_projection: SearchProjection | None = None
    search_sources: tuple[GovernedSearchSource, ...] = ()

    def __post_init__(self) -> None:
        checks = (
            (self.observations, ObservationSource, "observations"),
            (self.memories, MemoryItem, "memories"),
            (self.candidates, KnowledgeCandidate, "candidates"),
            (self.knowledge, ValidatedKnowledge, "knowledge"),
            (self.knowledge_lineages, CanonicalLineage, "knowledge_lineages"),
            (self.search_sources, GovernedSearchSource, "search_sources"),
        )
        for values, expected, label in checks:
            if not isinstance(values, tuple) or any(not isinstance(v, expected) for v in values):
                raise ValueError(f"{label} must contain only {expected.__name__} values")
        if self.search_projection is not None and not isinstance(self.search_projection, SearchProjection):
            raise ValueError("search_projection must be a SearchProjection")


@dataclass(frozen=True, slots=True)
class LearningItemView:
    role: LearningRole
    resource_id: Identity
    subject_id: Identity | None
    version_id: Identity | None
    canonical_state: CanonicalKnowledgeState
    text: str
    provenance_refs: tuple[Identity, ...]
    classification: str
    purpose: str
    rights: tuple[str, ...]
    freshness_state: str
    lifecycle_status: str | None
    authority_mode: AuthorityMode | None
    authority_scope: str | None
    validation_result: str | None
    approval_ref: Identity | None
    promotion_available: bool
    exact_reliance: ExactRelianceState
    status_text: str


@dataclass(frozen=True, slots=True)
class KnowledgeWorkspaceView:
    organization: OrganizationScope
    actor: ActorContext
    items: tuple[LearningItemView, ...]
    access_purpose: str
    required_right: str
    allowed_classifications: tuple[str, ...]
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE


@dataclass(frozen=True, slots=True)
class SearchHitView:
    source_subject_id: Identity
    source_version_id: Identity
    semantic_type: str
    role_text: str
    authority_mode: AuthorityMode
    authority_scope: str
    lifecycle_status: str | None
    provenance_refs: tuple[Identity, ...]
    classification: str
    purpose: str
    rights: tuple[str, ...]
    retention_rule: str
    freshness_state: str | None
    preview: str
    projection_state: ProjectionSourceState
    discovery_authority: DiscoveryAuthority
    exact_reliance: ExactRelianceState


@dataclass(frozen=True, slots=True)
class SearchDiscoveryView:
    organization: OrganizationScope
    actor: ActorContext
    query_text: str
    hits: tuple[SearchHitView, ...]
    access_purpose: str
    required_right: str
    allowed_classifications: tuple[str, ...]
    projection_status_text: str
    discovery_authority: DiscoveryAuthority = DiscoveryAuthority.DERIVED
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE


@dataclass(frozen=True, slots=True)
class DiscoveryBlockedState:
    code: DiscoveryBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, DiscoveryBlockCode) or not self.status_text.strip():
            raise ValueError("blocked state requires explicit code and text")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("workspace presentation cannot become authoritative")
        if self.governed_content_visible:
            raise ValueError("blocked state must expose no governed content")


KnowledgeWorkspaceResult = KnowledgeWorkspaceView | DiscoveryBlockedState
SearchDiscoveryResult = SearchDiscoveryView | DiscoveryBlockedState


def _represented_id(actor: ActorContext) -> Identity | None:
    return None if actor.represented_principal is None else actor.represented_principal.principal_id


def _request_matches(workspace: WorkspaceShellState, request: AccessRequest) -> bool:
    return request.actor == workspace.actor and request.organization == workspace.organization


def _authorization_matches(
    workspace: WorkspaceShellState,
    subject_id: Identity,
    decisions: tuple[CurrentSourceAuthorization, ...],
) -> tuple[CurrentSourceAuthorization, ...]:
    return tuple(
        decision
        for decision in decisions
        if decision.organization == workspace.organization
        and decision.resource_subject_id == subject_id
        and decision.actor_actual_principal_id == workspace.actor.actual_principal.principal_id
        and decision.represented_principal_id == _represented_id(workspace.actor)
    )


def _allowed(
    workspace: WorkspaceShellState,
    subject_id: Identity,
    decisions: tuple[CurrentSourceAuthorization, ...],
) -> bool:
    matches = _authorization_matches(workspace, subject_id, decisions)
    return len(matches) == 1 and matches[0].allowed


def _constraints_allow(
    organization: OrganizationScope,
    constraints: KnowledgeConstraints,
    request: AccessRequest,
    *,
    allow_stale: bool,
) -> bool:
    return (
        organization == request.organization
        and constraints.purpose == request.purpose
        and request.required_right in constraints.rights
        and constraints.classification in request.allowed_classifications
        and (allow_stale or constraints.freshness_state.casefold() == "current")
    )


def _payload(record: CanonicalRecord, key: str) -> str:
    values = dict(record.payload)
    if values.get(key):
        return values[key]
    return next((value for _, value in record.payload if value), "(content referenced outside bounded payload)")


def _item(
    *,
    role: LearningRole,
    resource_id: Identity,
    subject_id: Identity | None,
    version_id: Identity | None,
    state: CanonicalKnowledgeState,
    text: str,
    provenance: tuple[Identity, ...],
    constraints: KnowledgeConstraints,
    lifecycle: str | None = None,
    authority_mode: AuthorityMode | None = None,
    authority_scope: str | None = None,
    validation: str | None = None,
    approval: Identity | None = None,
    reliance: ExactRelianceState = ExactRelianceState.NOT_APPLICABLE,
    status: str,
) -> LearningItemView:
    return LearningItemView(
        role, resource_id, subject_id, version_id, state, text, provenance,
        constraints.classification, constraints.purpose, constraints.rights,
        constraints.freshness_state, lifecycle, authority_mode, authority_scope,
        validation, approval, False, reliance, status,
    )


def inspect_knowledge_workspace(
    *,
    workspace: WorkspaceShellState,
    sources: MemoryKnowledgeSearchSources,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
) -> KnowledgeWorkspaceResult:
    """Show permitted epistemic roles; omitted items expose neither identity nor count."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("inspection requires an open WorkspaceShellState")
    if not isinstance(sources, MemoryKnowledgeSearchSources):
        raise ValueError("sources must be MemoryKnowledgeSearchSources")
    if not isinstance(access_request, AccessRequest):
        raise ValueError("access_request must be explicit")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization) for value in source_authorizations
    ):
        raise ValueError("source_authorizations must be explicit")

    if not _request_matches(workspace, access_request):
        return DiscoveryBlockedState(
            DiscoveryBlockCode.ACCESS_CONTEXT_MISMATCH,
            "The retrieval context does not match the workspace Actor and Organization. "
            "No Memory or Knowledge metadata is shown.",
        )
    if workspace.active_destination is not WorkspaceDestination.KNOWLEDGE:
        return DiscoveryBlockedState(
            DiscoveryBlockCode.DESTINATION_MISMATCH,
            "Open the Knowledge workspace destination to inspect Memory and Knowledge.",
        )

    items: list[LearningItemView] = []
    for source in sources.observations:
        value = source.observation
        if _allowed(workspace, value.observation_id, source_authorizations) and _constraints_allow(
            value.organization, source.constraints, access_request, allow_stale=True
        ):
            items.append(_item(
                role=LearningRole.OBSERVATION,
                resource_id=value.observation_id,
                subject_id=None,
                version_id=None,
                state=CanonicalKnowledgeState.NON_CANONICAL,
                text=value.assertion,
                provenance=value.source_refs,
                constraints=source.constraints,
                status="Observation is evidence/input for evaluation, not validated Knowledge.",
            ))

    for value in sources.memories:
        record = value.canonical_record
        if _allowed(workspace, record.subject_id, source_authorizations) and _constraints_allow(
            record.organization, value.constraints, access_request, allow_stale=True
        ):
            items.append(_item(
                role=LearningRole.MEMORY,
                resource_id=record.subject_id,
                subject_id=record.subject_id,
                version_id=record.version_id,
                state=CanonicalKnowledgeState.MEMORY,
                text=_payload(record, "summary"),
                provenance=value.source_refs,
                constraints=value.constraints,
                lifecycle=record.lifecycle_status,
                authority_mode=record.authority_mode,
                authority_scope=record.authority_scope,
                status=(
                    f"Memory preserves remembered role '{value.remembered_role.value}' "
                    "without silently validating it."
                ),
            ))

    for value in sources.candidates:
        if _allowed(workspace, value.candidate_id, source_authorizations) and _constraints_allow(
            value.organization, value.constraints, access_request, allow_stale=True
        ):
            items.append(_item(
                role=LearningRole.CANDIDATE,
                resource_id=value.candidate_id,
                subject_id=value.subject_id,
                version_id=None,
                state=CanonicalKnowledgeState.NON_CANONICAL,
                text=value.proposition,
                provenance=value.evidence_refs,
                constraints=value.constraints,
                validation=value.validation_result,
                approval=value.approval_ref,
                status=(
                    "Knowledge Candidate remains non-Knowledge. Browsing, AI output, validation "
                    "or displayed approval evidence performs no promotion."
                ),
            ))

    eligible = {
        (p.source_subject_id, p.source_version_id)
        for p in retrieve_knowledge_for_access(
            knowledge=sources.knowledge, request=access_request, allow_stale=True
        )
    }
    for value in sources.knowledge:
        record = value.canonical_record
        if (value.subject_id, value.version_id) not in eligible:
            continue
        if not _allowed(workspace, value.subject_id, source_authorizations):
            continue
        current = value.constraints.freshness_state.casefold() == "current"
        items.append(_item(
            role=LearningRole.KNOWLEDGE,
            resource_id=value.subject_id,
            subject_id=value.subject_id,
            version_id=value.version_id,
            state=CanonicalKnowledgeState.KNOWLEDGE,
            text=_payload(record, "proposition"),
            provenance=value.evidence_refs,
            constraints=value.constraints,
            lifecycle=record.lifecycle_status,
            authority_mode=record.authority_mode,
            authority_scope=record.authority_scope,
            validation=value.validation_result,
            approval=value.approval_ref,
            reliance=ExactRelianceState.AVAILABLE if current else ExactRelianceState.STALE,
            status=(
                "Validated organizational understanding within its declared scope. "
                "Exact version, freshness, provenance and applicability remain material."
            ),
        ))

    return KnowledgeWorkspaceView(
        workspace.organization,
        workspace.actor,
        tuple(items),
        access_request.purpose,
        access_request.required_right,
        access_request.allowed_classifications,
    )


def _source_for_hit(
    hit: SearchHit,
    sources: MemoryKnowledgeSearchSources,
    organization: OrganizationScope,
) -> GovernedSearchSource | None:
    matches = tuple(
        source for source in sources.search_sources
        if source.organization == organization
        and source.subject_id == hit.source_subject_id
        and source.version_id == hit.source_version_id
        and source.canonical_record.semantic_type == hit.source_semantic_type
    )
    return matches[0] if len(matches) == 1 else None


def _knowledge_exact(
    sources: MemoryKnowledgeSearchSources,
    subject_id: Identity,
    version_id: Identity,
) -> ValidatedKnowledge | None:
    matches = tuple(
        value for value in sources.knowledge
        if value.subject_id == subject_id and value.version_id == version_id
    )
    return matches[0] if len(matches) == 1 else None


def _preview(text: str, limit: int = 180) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def discover_search(
    *,
    workspace: WorkspaceShellState,
    sources: MemoryKnowledgeSearchSources,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
    query_text: str,
) -> SearchDiscoveryResult:
    """Present only current, authorized exact-source hits from derived CAP-003 state."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("search requires an open WorkspaceShellState")
    if not isinstance(sources, MemoryKnowledgeSearchSources):
        raise ValueError("sources must be MemoryKnowledgeSearchSources")
    if (
        not isinstance(access_request, AccessRequest)
        or not isinstance(query_text, str)
        or not query_text.strip()
    ):
        raise ValueError("access_request and query_text must be explicit")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization) for value in source_authorizations
    ):
        raise ValueError("source_authorizations must be explicit")

    if not _request_matches(workspace, access_request):
        return DiscoveryBlockedState(
            DiscoveryBlockCode.ACCESS_CONTEXT_MISMATCH,
            "The discovery context does not match the workspace Actor and Organization. "
            "No search metadata is shown.",
        )
    if workspace.active_destination is not WorkspaceDestination.DISCOVER:
        return DiscoveryBlockedState(
            DiscoveryBlockCode.DESTINATION_MISMATCH,
            "Open the Discover workspace destination to run governed discovery.",
        )
    if sources.search_projection is None:
        return SearchDiscoveryView(
            workspace.organization, workspace.actor, query_text, (),
            access_request.purpose, access_request.required_right,
            access_request.allowed_classifications,
            "Derived search projection unavailable; no inference is made about canonical source absence.",
        )

    hits: list[SearchHitView] = []
    raw = search_for_access(
        projection=sources.search_projection,
        current_sources=sources.search_sources,
        query_text=query_text,
        request=access_request,
    )
    for hit in raw:
        if not _allowed(workspace, hit.source_subject_id, source_authorizations):
            continue
        try:
            record = resolve_search_hit_for_access(
                hit=hit, current_sources=sources.search_sources, request=access_request
            )
        except CrossCapabilityEnforcementError:
            continue
        source = _source_for_hit(hit, sources, workspace.organization)
        if source is None or source.canonical_record != record:
            continue

        role_text = "Governed source"
        freshness: str | None = None
        reliance = ExactRelianceState.NOT_APPLICABLE
        if hit.source_semantic_type == KNOWLEDGE_SEMANTIC_TYPE:
            knowledge = _knowledge_exact(sources, hit.source_subject_id, hit.source_version_id)
            if knowledge is None or knowledge.canonical_record != record:
                continue
            eligible = retrieve_knowledge_for_access(
                knowledge=(knowledge,), request=access_request, allow_stale=True
            )
            if len(eligible) != 1 or knowledge.constraints.freshness_state.casefold() != "current":
                # A synchronized search projection cannot make stale/review-required
                # Knowledge look current.
                continue
            role_text = LearningRole.KNOWLEDGE.value
            freshness = knowledge.constraints.freshness_state
            reliance = ExactRelianceState.AVAILABLE
        else:
            memories = tuple(v for v in sources.memories if v.canonical_record == record)
            if len(memories) == 1:
                role_text = LearningRole.MEMORY.value
                freshness = memories[0].constraints.freshness_state

        hits.append(SearchHitView(
            hit.source_subject_id,
            hit.source_version_id,
            hit.source_semantic_type,
            role_text,
            record.authority_mode,
            record.authority_scope,
            record.lifecycle_status,
            record.provenance_refs,
            source.constraints.classification,
            source.constraints.purpose,
            source.constraints.rights,
            source.constraints.retention_rule,
            freshness,
            _preview(source.searchable_text),
            hit.state,
            DiscoveryAuthority.DERIVED,
            reliance,
        ))

    return SearchDiscoveryView(
        workspace.organization,
        workspace.actor,
        query_text,
        tuple(hits),
        access_request.purpose,
        access_request.required_right,
        access_request.allowed_classifications,
        "Derived projection was re-evaluated against current exact governed sources and access context.",
    )


def _require_authorized(
    workspace: WorkspaceShellState,
    subject_id: Identity,
    decisions: tuple[CurrentSourceAuthorization, ...],
) -> None:
    if not _allowed(workspace, subject_id, decisions):
        raise KnowledgeRelianceError("current exact Knowledge source access is not uniquely authorized")


def _lineage(
    sources: MemoryKnowledgeSearchSources,
    organization: OrganizationScope,
    subject_id: Identity,
    version_id: Identity,
) -> CanonicalLineage:
    matches = tuple(
        lineage for lineage in sources.knowledge_lineages
        if lineage.subject_id == subject_id
        and lineage.records
        and lineage.records[0].organization == organization
        and any(record.version_id == version_id for record in lineage.records)
    )
    if len(matches) != 1:
        raise KnowledgeRelianceError("exact Knowledge Version lineage is not uniquely resolvable")
    return matches[0]


def _resolve_knowledge(
    *,
    workspace: WorkspaceShellState,
    sources: MemoryKnowledgeSearchSources,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
    subject_id: Identity,
    version_id: Identity,
) -> ExactKnowledgeReliance:
    if not _request_matches(workspace, access_request):
        raise KnowledgeRelianceError("current access context does not match the workspace")
    _require_authorized(workspace, subject_id, source_authorizations)
    value = _knowledge_exact(sources, subject_id, version_id)
    if value is None:
        raise KnowledgeRelianceError("exact validated Knowledge Version is unavailable")
    if len(retrieve_knowledge_for_access(
        knowledge=(value,), request=access_request, allow_stale=False
    )) != 1:
        raise KnowledgeRelianceError(
            "current purpose/right/classification/freshness context does not permit reliance"
        )
    return resolve_exact_knowledge_reliance(
        lineage=_lineage(sources, workspace.organization, subject_id, version_id),
        validated=sources.knowledge,
        version_id=version_id,
    )


def resolve_exact_knowledge_from_workspace(
    *,
    item: LearningItemView,
    workspace: WorkspaceShellState,
    sources: MemoryKnowledgeSearchSources,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
    selected_version_id: Identity,
) -> ExactKnowledgeReliance:
    """Consequential reliance requires explicit exact selection and current rechecks."""

    if item.role is not LearningRole.KNOWLEDGE or item.subject_id is None or item.version_id is None:
        raise KnowledgeRelianceError("only validated Knowledge has exact Knowledge reliance")
    if item.exact_reliance is not ExactRelianceState.AVAILABLE:
        raise KnowledgeRelianceError("Knowledge freshness state does not permit reliance")
    if selected_version_id != item.version_id:
        raise KnowledgeRelianceError("operator must select the exact displayed Knowledge Version")
    return _resolve_knowledge(
        workspace=workspace,
        sources=sources,
        source_authorizations=source_authorizations,
        access_request=access_request,
        subject_id=item.subject_id,
        version_id=selected_version_id,
    )


def resolve_exact_knowledge_from_search(
    *,
    hit: SearchHitView,
    workspace: WorkspaceShellState,
    sources: MemoryKnowledgeSearchSources,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
    selected_version_id: Identity,
) -> ExactKnowledgeReliance:
    """A derived hit exits search only through exact current source + CAP-002 reliance."""

    if hit.role_text != LearningRole.KNOWLEDGE.value or hit.exact_reliance is not ExactRelianceState.AVAILABLE:
        raise KnowledgeRelianceError("discovered source is not eligible validated Knowledge")
    if selected_version_id != hit.source_version_id:
        raise KnowledgeRelianceError("operator must select the exact discovered Knowledge Version")
    if not _request_matches(workspace, access_request):
        raise KnowledgeRelianceError("current access context does not match the workspace")
    _require_authorized(workspace, hit.source_subject_id, source_authorizations)
    try:
        record = resolve_search_hit_for_access(
            hit=SearchHit(
                hit.source_subject_id,
                hit.source_version_id,
                hit.semantic_type,
                ProjectionSourceState.CURRENT,
            ),
            current_sources=sources.search_sources,
            request=access_request,
        )
    except CrossCapabilityEnforcementError as exc:
        raise KnowledgeRelianceError(str(exc)) from exc
    if record.version_id != selected_version_id:
        raise KnowledgeRelianceError("derived discovery no longer resolves to the selected exact Version")
    return _resolve_knowledge(
        workspace=workspace,
        sources=sources,
        source_authorizations=source_authorizations,
        access_request=access_request,
        subject_id=hit.source_subject_id,
        version_id=selected_version_id,
    )


def _id(value: Identity | None) -> str:
    return "—" if value is None else escape(value.value)


def _refs(values: tuple[Identity, ...]) -> str:
    return "—" if not values else ", ".join(escape(value.value) for value in values)


def render_knowledge_workspace_html(result: KnowledgeWorkspaceResult) -> str:
    if isinstance(result, DiscoveryBlockedState):
        return (
            '<section data-p4-07-state="blocked"><h2>Memory / Knowledge unavailable</h2>'
            f'<p role="alert">{escape(result.status_text)}</p></section>'
        )
    if not isinstance(result, KnowledgeWorkspaceView):
        raise ValueError("invalid Knowledge workspace result")

    cards: list[str] = []
    for item in result.items:
        authority = (
            "not a canonical authority record"
            if item.authority_mode is None
            else f"{escape(item.authority_mode.value)} / {escape(item.authority_scope or '—')}"
        )
        cards.append(
            f'<article data-role="{escape(item.role.name.lower())}"><h3>{escape(item.role.value)}</h3><dl>'
            f'<dt>Resource</dt><dd>{_id(item.resource_id)}</dd>'
            f'<dt>Subject</dt><dd>{_id(item.subject_id)}</dd>'
            f'<dt>Exact Version</dt><dd>{_id(item.version_id)}</dd>'
            f'<dt>Canonical state</dt><dd>{escape(item.canonical_state.value)}</dd>'
            f'<dt>Authority</dt><dd>{authority}</dd>'
            f'<dt>Lifecycle</dt><dd>{escape(item.lifecycle_status or "—")}</dd>'
            f'<dt>Freshness</dt><dd>{escape(item.freshness_state)}</dd>'
            f'<dt>Purpose</dt><dd>{escape(item.purpose)}</dd>'
            f'<dt>Classification</dt><dd>{escape(item.classification)}</dd>'
            f'<dt>Rights</dt><dd>{escape(", ".join(item.rights))}</dd>'
            f'<dt>Provenance</dt><dd>{_refs(item.provenance_refs)}</dd>'
            f'<dt>Validation</dt><dd>{escape(item.validation_result or "—")}</dd>'
            f'<dt>Approval reference</dt><dd>{_id(item.approval_ref)}</dd>'
            f'<dt>Promotion available here</dt><dd>{"yes" if item.promotion_available else "no"}</dd>'
            f'<dt>Exact reliance</dt><dd>{escape(item.exact_reliance.value)}</dd></dl>'
            f'<p>{escape(item.text)}</p><p>{escape(item.status_text)}</p></article>'
        )
    return (
        '<section data-p4-07-surface="knowledge" data-presentation-authority="non-authoritative">'
        '<h2>Memory / Knowledge</h2><p><strong>Epistemic roles remain distinct.</strong> '
        'Observation, Organizational Memory, Knowledge Candidate and validated Knowledge '
        'are not interchangeable.</p>'
        f'<p>Purpose: {escape(result.access_purpose)} / right: {escape(result.required_right)} / '
        f'classifications: {escape(", ".join(result.allowed_classifications))}</p>'
        '<p>Unauthorized or handling-ineligible items are omitted without protected counts.</p>'
        + "".join(cards)
        + '<p data-authority-note="true">Browsing, AI output and displayed evidence do not '
        'promote a candidate or create Knowledge authority.</p></section>'
    )


def render_search_discovery_html(result: SearchDiscoveryResult) -> str:
    if isinstance(result, DiscoveryBlockedState):
        return (
            '<section data-p4-07-state="blocked"><h2>Discovery unavailable</h2>'
            f'<p role="alert">{escape(result.status_text)}</p></section>'
        )
    if not isinstance(result, SearchDiscoveryView):
        raise ValueError("invalid Search discovery result")

    cards: list[str] = []
    for hit in result.hits:
        cards.append(
            '<article data-discovery-result="derived">'
            f'<h3>{escape(hit.role_text)}</h3><dl>'
            f'<dt>Source Subject</dt><dd>{_id(hit.source_subject_id)}</dd>'
            f'<dt>Exact Source Version</dt><dd>{_id(hit.source_version_id)}</dd>'
            f'<dt>Semantic type</dt><dd>{escape(hit.semantic_type)}</dd>'
            f'<dt>Projection state</dt><dd>{escape(hit.projection_state.value)}</dd>'
            f'<dt>Discovery authority</dt><dd>{escape(hit.discovery_authority.value)}</dd>'
            f'<dt>Source authority</dt><dd>{escape(hit.authority_mode.value)} / {escape(hit.authority_scope)}</dd>'
            f'<dt>Freshness</dt><dd>{escape(hit.freshness_state or "source-owned / not carried")}</dd>'
            f'<dt>Purpose</dt><dd>{escape(hit.purpose)}</dd>'
            f'<dt>Classification</dt><dd>{escape(hit.classification)}</dd>'
            f'<dt>Rights</dt><dd>{escape(", ".join(hit.rights))}</dd>'
            f'<dt>Retention</dt><dd>{escape(hit.retention_rule)}</dd>'
            f'<dt>Provenance</dt><dd>{_refs(hit.provenance_refs)}</dd>'
            f'<dt>Exact Knowledge reliance</dt><dd>{escape(hit.exact_reliance.value)}</dd></dl>'
            f'<p data-preview="minimized">{escape(hit.preview)}</p>'
            '<p data-ranking-authority="none">Search match/order is a discovery signal only; '
            'it does not establish truth, validation, permission, approval or Organizational Authority.</p>'
            '</article>'
        )
    return (
        '<section data-p4-07-surface="discover" data-presentation-authority="non-authoritative">'
        f'<h2>Discover</h2><p>Query: {escape(result.query_text)}</p>'
        f'<p>Discovery state: {escape(result.discovery_authority.value)}.</p>'
        f'<p>Projection status: {escape(result.projection_status_text)}</p>'
        f'<p>Purpose: {escape(result.access_purpose)} / right: {escape(result.required_right)} / '
        f'classifications: {escape(", ".join(result.allowed_classifications))}</p>'
        '<p>Unauthorized, wrong-Organization, stale, missing, ambiguous or handling-ineligible '
        'sources are omitted without protected counts.</p>'
        + "".join(cards)
        + '<p data-authority-note="true">Search/index/RAG-like discovery remains derived; '
        'browsing does not promote Knowledge.</p></section>'
    )
