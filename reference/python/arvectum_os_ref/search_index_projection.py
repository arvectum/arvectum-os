"""P3.05 — bounded CAP-003 Search / Index Projection incubation slice.

Internal, in-memory and domain-neutral reference semantics only. This module is
not a public API, search-engine contract, ranking/relevance contract, durable
projection store or Active Platform Capability.

The projection is disposable derived state. It stores exact governed source
Subject/Version attribution, never becomes canonical authority, and must be
resolved against the current governed source set before discovery or reliance.
Stale, missing or ambiguous projection state fails closed for ordinary query.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .canonical import CanonicalRecord
from .identity import Identity
from .security import OrganizationScope


class SearchIndexProjectionError(ValueError):
    """The bounded CAP-003 contract cannot satisfy the requested operation."""


class ProjectionBuildError(SearchIndexProjectionError):
    """A derived projection cannot be built unambiguously from governed sources."""


class ProjectionQueryError(SearchIndexProjectionError):
    """A bounded discovery query cannot be evaluated safely."""


class ProjectionResolutionError(SearchIndexProjectionError):
    """A discovery result cannot be resolved safely to governed source state."""


class ProjectionSourceState(str, Enum):
    """Synchronization state of one derived entry against the governed source set."""

    CURRENT = "Current"
    STALE = "Stale"
    MISSING = "Missing"
    AMBIGUOUS = "Ambiguous"


@dataclass(frozen=True, slots=True)
class DiscoveryConstraints:
    """Bounded RFC-0003 handling constraints supplied by the governed source owner."""

    purpose: str
    classification: str
    rights: tuple[str, ...]
    retention_rule: str

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (self.purpose, self.classification, self.retention_rule)
        ):
            raise ValueError(
                "purpose, classification and retention_rule must be explicit"
            )
        if not isinstance(self.rights, tuple) or not self.rights or any(
            not isinstance(value, str) or not value.strip() for value in self.rights
        ):
            raise ValueError("rights must contain explicit permitted-use references")


@dataclass(frozen=True, slots=True)
class GovernedSearchSource:
    """Current governed source version selected by its owning semantic boundary.

    CAP-003 does not decide Canonical Head, Effective Version, Knowledge lifecycle,
    document admission or source authority. The owning source boundary supplies
    the exact currently eligible Canonical Record plus discovery constraints and
    bounded searchable material.
    """

    canonical_record: CanonicalRecord
    searchable_text: str
    constraints: DiscoveryConstraints

    def __post_init__(self) -> None:
        if not isinstance(self.canonical_record, CanonicalRecord):
            raise ValueError("governed search source requires a CanonicalRecord")
        if not isinstance(self.searchable_text, str) or not self.searchable_text.strip():
            raise ValueError("searchable_text must be explicit")
        if not isinstance(self.constraints, DiscoveryConstraints):
            raise ValueError("discovery constraints must be explicit")

    @property
    def organization(self) -> OrganizationScope:
        return self.canonical_record.organization

    @property
    def subject_id(self) -> Identity:
        return self.canonical_record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.canonical_record.version_id


@dataclass(frozen=True, slots=True)
class ProjectionEntry:
    """Disposable discovery representation; never canonical authority."""

    source_subject_id: Identity
    source_version_id: Identity
    source_semantic_type: str
    organization: OrganizationScope
    searchable_text: str


@dataclass(frozen=True, slots=True)
class SearchProjection:
    """Rebuildable in-memory read model over exact governed source versions."""

    entries: tuple[ProjectionEntry, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.entries, tuple):
            raise ValueError("projection entries must be an immutable tuple")
        exact_refs: set[tuple[Identity, Identity]] = set()
        for entry in self.entries:
            if not isinstance(entry, ProjectionEntry):
                raise ValueError("projection may contain only ProjectionEntry values")
            exact_ref = (entry.source_subject_id, entry.source_version_id)
            if exact_ref in exact_refs:
                raise ValueError("projection must not contain duplicate exact source references")
            exact_refs.add(exact_ref)


@dataclass(frozen=True, slots=True)
class ProjectionDiagnostic:
    """Non-content diagnostic for reconciliation/rebuild decisions."""

    source_subject_id: Identity
    source_version_id: Identity
    state: ProjectionSourceState


@dataclass(frozen=True, slots=True)
class SearchHit:
    """Non-authoritative discovery hit with exact governed source attribution."""

    source_subject_id: Identity
    source_version_id: Identity
    source_semantic_type: str
    state: ProjectionSourceState

    def __post_init__(self) -> None:
        if self.state is not ProjectionSourceState.CURRENT:
            raise ValueError("ordinary SearchHit values may represent only Current source state")


def _source_key(source: GovernedSearchSource) -> tuple[OrganizationScope, Identity]:
    return source.organization, source.subject_id


def _matching_current_sources(
    entry: ProjectionEntry,
    current_sources: tuple[GovernedSearchSource, ...],
) -> tuple[GovernedSearchSource, ...]:
    return tuple(
        source
        for source in current_sources
        if source.organization == entry.organization
        and source.subject_id == entry.source_subject_id
    )


def assess_projection_entry(
    *,
    entry: ProjectionEntry,
    current_sources: tuple[GovernedSearchSource, ...],
) -> ProjectionSourceState:
    """Classify projection state without upgrading the projection into authority."""

    if not isinstance(entry, ProjectionEntry):
        raise TypeError("projection state assessment requires a ProjectionEntry")
    if not isinstance(current_sources, tuple) or any(
        not isinstance(source, GovernedSearchSource) for source in current_sources
    ):
        raise TypeError("current_sources must be governed source values")

    matches = _matching_current_sources(entry, current_sources)
    if not matches:
        return ProjectionSourceState.MISSING
    if len(matches) != 1:
        return ProjectionSourceState.AMBIGUOUS

    current = matches[0]
    if current.canonical_record.semantic_type != entry.source_semantic_type:
        return ProjectionSourceState.AMBIGUOUS
    if current.version_id != entry.source_version_id:
        return ProjectionSourceState.STALE
    return ProjectionSourceState.CURRENT


def rebuild_projection(*, sources: tuple[GovernedSearchSource, ...]) -> SearchProjection:
    """Build disposable discovery state from a unique current governed source set."""

    if not isinstance(sources, tuple) or any(
        not isinstance(source, GovernedSearchSource) for source in sources
    ):
        raise ProjectionBuildError("sources must be an immutable governed source tuple")

    seen_subjects: set[tuple[OrganizationScope, Identity]] = set()
    entries: list[ProjectionEntry] = []
    for source in sources:
        key = _source_key(source)
        if key in seen_subjects:
            raise ProjectionBuildError(
                "current governed source set is ambiguous for one Organization/Subject"
            )
        seen_subjects.add(key)
        entries.append(
            ProjectionEntry(
                source_subject_id=source.subject_id,
                source_version_id=source.version_id,
                source_semantic_type=source.canonical_record.semantic_type,
                organization=source.organization,
                searchable_text=source.searchable_text,
            )
        )
    return SearchProjection(tuple(entries))


def inspect_projection(
    *,
    projection: SearchProjection,
    current_sources: tuple[GovernedSearchSource, ...],
) -> tuple[ProjectionDiagnostic, ...]:
    """Expose reconciliation state without returning projected content."""

    if not isinstance(projection, SearchProjection):
        raise TypeError("projection must be a SearchProjection")
    return tuple(
        ProjectionDiagnostic(
            source_subject_id=entry.source_subject_id,
            source_version_id=entry.source_version_id,
            state=assess_projection_entry(entry=entry, current_sources=current_sources),
        )
        for entry in projection.entries
    )


def _resolve_current_source(
    *,
    subject_id: Identity,
    version_id: Identity,
    semantic_type: str,
    organization: OrganizationScope,
    current_sources: tuple[GovernedSearchSource, ...],
) -> GovernedSearchSource:
    matches = tuple(
        source
        for source in current_sources
        if source.organization == organization and source.subject_id == subject_id
    )
    if not matches:
        raise ProjectionResolutionError("governed source is missing")
    if len(matches) != 1:
        raise ProjectionResolutionError("governed source is ambiguous")
    source = matches[0]
    if source.canonical_record.semantic_type != semantic_type:
        raise ProjectionResolutionError("governed source semantic type is ambiguous")
    if source.version_id != version_id:
        raise ProjectionResolutionError(
            "projection is stale; exact governed source version must not be substituted"
        )
    return source


def query_projection(
    *,
    projection: SearchProjection,
    current_sources: tuple[GovernedSearchSource, ...],
    query_text: str,
    organization: OrganizationScope,
    purpose: str,
    required_right: str,
    allowed_classifications: tuple[str, ...],
) -> tuple[SearchHit, ...]:
    """Return only Current, eligible, exact-attribution discovery hits.

    Matching is intentionally a trivial case-insensitive substring fixture, not a
    ranking/relevance/query-language contract. Current governed source constraints
    are re-evaluated before projected text is matched so stale access metadata is
    not trusted merely because it remains in a projection.
    """

    if not isinstance(projection, SearchProjection):
        raise ProjectionQueryError("projection must be explicit")
    if not isinstance(current_sources, tuple) or any(
        not isinstance(source, GovernedSearchSource) for source in current_sources
    ):
        raise ProjectionQueryError("current governed sources must be explicit")
    if not isinstance(organization, OrganizationScope):
        raise ProjectionQueryError("Organization scope is required; no default is permitted")
    if not isinstance(query_text, str) or not query_text.strip():
        raise ProjectionQueryError("query_text must be explicit")
    if not isinstance(purpose, str) or not purpose.strip():
        raise ProjectionQueryError("purpose must be explicit")
    if not isinstance(required_right, str) or not required_right.strip():
        raise ProjectionQueryError("required_right must be explicit")
    if not isinstance(allowed_classifications, tuple) or not allowed_classifications or any(
        not isinstance(value, str) or not value.strip()
        for value in allowed_classifications
    ):
        raise ProjectionQueryError("allowed_classifications must be explicit")

    needle = query_text.casefold()
    hits: list[SearchHit] = []
    for entry in projection.entries:
        if entry.organization != organization:
            continue
        if assess_projection_entry(entry=entry, current_sources=current_sources) is not ProjectionSourceState.CURRENT:
            continue

        source = _resolve_current_source(
            subject_id=entry.source_subject_id,
            version_id=entry.source_version_id,
            semantic_type=entry.source_semantic_type,
            organization=organization,
            current_sources=current_sources,
        )
        constraints = source.constraints
        if constraints.purpose != purpose:
            continue
        if required_right not in constraints.rights:
            continue
        if constraints.classification not in allowed_classifications:
            continue
        if needle not in entry.searchable_text.casefold():
            continue

        hits.append(
            SearchHit(
                source_subject_id=entry.source_subject_id,
                source_version_id=entry.source_version_id,
                source_semantic_type=entry.source_semantic_type,
                state=ProjectionSourceState.CURRENT,
            )
        )
    return tuple(hits)


def resolve_search_hit_for_reliance(
    *,
    hit: SearchHit,
    current_sources: tuple[GovernedSearchSource, ...],
    organization: OrganizationScope,
    source_access_authorized: bool,
) -> CanonicalRecord:
    """Exit the projection boundary by resolving one exact governed source version.

    A search hit does not grant source access or Organizational Authority. The
    caller must supply an already-evaluated source access decision. This bounded
    boolean is test-harness evidence only; P3.07 owns broader cross-capability
    authorization/rights enforcement composition.
    """

    if not isinstance(hit, SearchHit):
        raise ProjectionResolutionError("reliance requires an exact SearchHit")
    if not isinstance(organization, OrganizationScope):
        raise ProjectionResolutionError("Organization scope must be explicit")
    if source_access_authorized is not True:
        raise ProjectionResolutionError(
            "discovery visibility does not grant access to the governed source"
        )

    source = _resolve_current_source(
        subject_id=hit.source_subject_id,
        version_id=hit.source_version_id,
        semantic_type=hit.source_semantic_type,
        organization=organization,
        current_sources=current_sources,
    )
    return source.canonical_record
