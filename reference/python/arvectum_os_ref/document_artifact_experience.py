"""P4.06 — bounded Document / Artifact workspace experience.

This module is an internal, reversible presentation/resolution adapter over the
existing CAP-001 Document & Artifact Governance incubation slice, P3.07
cross-capability enforcement and P4.02 workspace shell. It does not create a
DMS, object store, content API, OCR/signing provider, public route/wire contract,
authorization engine, document-approval workflow, durable read model or new
canonical-state owner.

The adapter preserves Accepted RFC-0008 distinctions among logical Document
identity, immutable Document Version identity, concrete Artifact identity and
replaceable storage locator. Working/draft candidates remain non-canonical;
transient/generated artifacts are never promoted by this surface. Exact
consequential reliance is available only for an explicitly selected exact
admitted Document Version and governed Artifact after current source and
purpose/right/classification enforcement.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .canonical import AuthorityMode
from .canonical_inspection import CurrentSourceAuthorization
from .canonical_lineage import CanonicalLineage, CanonicalVersionNotFoundError
from .cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
    resolve_document_for_access,
)
from .document_artifact_governance import (
    DOCUMENT_SEMANTIC_TYPE,
    AdmittedDocumentVersion,
    ArtifactContent,
    ArtifactState,
    DocumentVersionCandidate,
    ExactDocumentReliance,
    HandlingConstraints,
    resolve_exact_document_reliance,
)
from .identity import Identity
from .security import ActorContext, OrganizationScope
from .workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
)


class DocumentWorkspaceBlockCode(str, Enum):
    REFERENCE_REQUIRED = "reference-required"
    ACCESS_DENIED = "access-denied"
    HANDLING_ACCESS_DENIED = "handling-access-denied"
    SOURCE_UNAVAILABLE = "source-unavailable"
    SOURCE_AMBIGUOUS = "source-ambiguous"
    VERSION_UNAVAILABLE = "version-unavailable"
    ADMISSION_EVIDENCE_UNAVAILABLE = "admission-evidence-unavailable"
    UNSUPPORTED_AUTHORITY = "unsupported-authority"


class DocumentReferenceBasis(str, Enum):
    CANONICAL_HEAD = "Canonical Head"
    EXACT_VERSION = "Exact Version"


class DocumentCanonicalState(str, Enum):
    ADMITTED = "Admitted canonical Document Version"
    WORKING_CANDIDATE = "Working/Draft Candidate — non-canonical"


class ExactRelianceAvailability(str, Enum):
    AVAILABLE = "Available for exact governed reliance"
    REQUIRES_EXACT_VERSION = "Select an exact admitted Document Version before consequential reliance"


@dataclass(frozen=True, slots=True)
class DocumentWorkspaceSourceSet:
    """Current document sources supplied by their existing semantic owners."""

    lineages: tuple[CanonicalLineage, ...]
    admitted_versions: tuple[AdmittedDocumentVersion, ...]
    working_candidates: tuple[DocumentVersionCandidate, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.lineages, tuple) or any(
            not isinstance(value, CanonicalLineage) for value in self.lineages
        ):
            raise ValueError("lineages must contain CanonicalLineage values")
        if not isinstance(self.admitted_versions, tuple) or any(
            not isinstance(value, AdmittedDocumentVersion)
            for value in self.admitted_versions
        ):
            raise ValueError(
                "admitted_versions must contain AdmittedDocumentVersion values"
            )
        if not isinstance(self.working_candidates, tuple) or any(
            not isinstance(value, DocumentVersionCandidate)
            for value in self.working_candidates
        ):
            raise ValueError(
                "working_candidates must contain DocumentVersionCandidate values"
            )


@dataclass(frozen=True, slots=True)
class ArtifactWorkspaceInspection:
    artifact_id: Identity
    state: ArtifactState
    media_type: str
    rendition_role: str
    designated_rendition: bool
    integrity_ref: str
    source_artifact_ids: tuple[Identity, ...]
    transformation: str | None
    handling: HandlingConstraints
    storage_locator_present: bool
    storage_locator_exposed: bool
    exact_reliance: ExactRelianceAvailability


@dataclass(frozen=True, slots=True)
class WorkingCandidateInspection:
    version_id: Identity
    lifecycle_status: str | None
    canonical_state: DocumentCanonicalState
    contains_artifacts: bool
    contains_transient_artifacts: bool
    artifact_metadata_visible: bool
    promotion_available: bool
    promotion_status_text: str


@dataclass(frozen=True, slots=True)
class DocumentWorkspaceInspection:
    organization: OrganizationScope
    actor: ActorContext
    document_id: Identity
    reference_basis: DocumentReferenceBasis
    displayed_version_id: Identity
    head_version_id: Identity
    lifecycle_status: str | None
    authority_mode: AuthorityMode
    authority_scope: str
    authoritative_source_text: str
    canonical_state: DocumentCanonicalState
    designated_rendition_role: str | None
    artifacts: tuple[ArtifactWorkspaceInspection, ...]
    working_candidates: tuple[WorkingCandidateInspection, ...]
    authorization_decision_version_id: Identity
    access_purpose: str
    required_right: str
    allowed_classifications: tuple[str, ...]
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE


@dataclass(frozen=True, slots=True)
class DocumentWorkspaceBlockedState:
    code: DocumentWorkspaceBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, DocumentWorkspaceBlockCode):
            raise ValueError("blocked document workspace state requires an explicit code")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("blocked document workspace state requires textual meaning")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("document workspace presentation cannot become authoritative")
        if self.governed_content_visible:
            raise ValueError("blocked document workspace state must expose no governed content")


DocumentWorkspaceResult = DocumentWorkspaceInspection | DocumentWorkspaceBlockedState


def _represented_principal_id(actor: ActorContext) -> Identity | None:
    if actor.represented_principal is None:
        return None
    return actor.represented_principal.principal_id


def _matching_authorizations_for_context(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    subject_id: Identity,
    decisions: tuple[CurrentSourceAuthorization, ...],
) -> tuple[CurrentSourceAuthorization, ...]:
    actual = actor.actual_principal.principal_id
    represented = _represented_principal_id(actor)
    return tuple(
        decision
        for decision in decisions
        if decision.organization == organization
        and decision.resource_subject_id == subject_id
        and decision.actor_actual_principal_id == actual
        and decision.represented_principal_id == represented
    )


def _access_request_matches_workspace(
    *, workspace: WorkspaceShellState, access_request: AccessRequest
) -> bool:
    return (
        access_request.actor == workspace.actor
        and access_request.organization == workspace.organization
    )


def _artifact_inspection(
    artifact: ArtifactContent,
    *,
    designated_rendition_role: str | None,
    exact_version_selected: bool,
) -> ArtifactWorkspaceInspection:
    if artifact.state is not ArtifactState.GOVERNED:
        raise ValueError("workspace Artifact inspection requires governed Artifact state")
    reliance = (
        ExactRelianceAvailability.AVAILABLE
        if exact_version_selected
        else ExactRelianceAvailability.REQUIRES_EXACT_VERSION
    )
    return ArtifactWorkspaceInspection(
        artifact_id=artifact.artifact_id,
        state=artifact.state,
        media_type=artifact.media_type,
        rendition_role=artifact.rendition_role,
        designated_rendition=(
            designated_rendition_role is not None
            and artifact.rendition_role == designated_rendition_role
        ),
        integrity_ref=artifact.integrity_ref,
        source_artifact_ids=artifact.source_artifact_ids,
        transformation=artifact.transformation,
        handling=artifact.handling,
        storage_locator_present=artifact.storage_locator is not None,
        storage_locator_exposed=False,
        exact_reliance=reliance,
    )


def _candidate_inspection(candidate: DocumentVersionCandidate) -> WorkingCandidateInspection:
    """Expose candidate state without leaking unadmitted Artifact metadata."""

    return WorkingCandidateInspection(
        version_id=candidate.canonical_record.version_id,
        lifecycle_status=candidate.canonical_record.lifecycle_status,
        canonical_state=DocumentCanonicalState.WORKING_CANDIDATE,
        contains_artifacts=bool(candidate.artifacts),
        contains_transient_artifacts=any(
            artifact.state is ArtifactState.TRANSIENT for artifact in candidate.artifacts
        ),
        artifact_metadata_visible=False,
        promotion_available=False,
        promotion_status_text=(
            "Not admitted. Artifact metadata remains withheld on this non-canonical candidate "
            "surface. P4.06 exposes no promotion control; consequential admission requires an "
            "applicable Governed Execution path owned outside this workspace adapter."
        ),
    )


def _visible_artifacts(
    *,
    admitted: AdmittedDocumentVersion,
    access_request: AccessRequest,
    exact_version_selected: bool,
) -> tuple[ArtifactWorkspaceInspection, ...]:
    allowed: list[ArtifactContent] = []
    for artifact in admitted.artifacts:
        try:
            resolve_document_for_access(
                admitted=admitted,
                artifact_id=artifact.artifact_id,
                request=access_request,
            )
        except CrossCapabilityEnforcementError:
            continue
        allowed.append(artifact)

    designated_visible = any(
        artifact.rendition_role == admitted.designated_rendition_role
        for artifact in allowed
    )
    designated_role = admitted.designated_rendition_role if designated_visible else None
    return tuple(
        _artifact_inspection(
            artifact,
            designated_rendition_role=designated_role,
            exact_version_selected=exact_version_selected,
        )
        for artifact in allowed
    )


def inspect_document_workspace(
    *,
    workspace: WorkspaceShellState,
    sources: DocumentWorkspaceSourceSet,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
) -> DocumentWorkspaceResult:
    """Inspect one governed Document through the current scoped workspace reference.

    Current source authorization is consumed before source/version resolution so
    protected object or version existence cannot be inferred through differing
    source errors. P3.07 purpose/right/classification enforcement is then applied
    independently to each governed Artifact before Artifact metadata is rendered.
    Restricted Artifact metadata is omitted without counts. Content bytes, content
    references and storage locators are never exposed by this bounded surface.
    """

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("document inspection requires an open WorkspaceShellState")
    if not isinstance(sources, DocumentWorkspaceSourceSet):
        raise ValueError("sources must be a DocumentWorkspaceSourceSet")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization)
        for value in source_authorizations
    ):
        raise ValueError(
            "source_authorizations must contain CurrentSourceAuthorization values"
        )
    if not isinstance(access_request, AccessRequest):
        raise ValueError("access_request must be an explicit AccessRequest")
    if not _access_request_matches_workspace(
        workspace=workspace, access_request=access_request
    ):
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.ACCESS_DENIED,
            status_text=(
                "The current Artifact access context does not match the workspace Actor and "
                "Organization. No protected document metadata is shown."
            ),
        )

    reference = workspace.current_reference
    if reference is None:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.REFERENCE_REQUIRED,
            status_text="Select a Document Subject or exact Document Version to inspect.",
        )
    if workspace.active_destination is not WorkspaceDestination.DOCUMENTS:
        raise ValueError("document inspection requires the Documents workspace destination")
    if not isinstance(reference, (SubjectNavigationReference, ExactVersionNavigationReference)):
        raise ValueError("workspace reference type is unsupported")

    decisions = _matching_authorizations_for_context(
        organization=workspace.organization,
        actor=workspace.actor,
        subject_id=reference.subject_id,
        decisions=source_authorizations,
    )
    if len(decisions) != 1 or not decisions[0].allowed:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.ACCESS_DENIED,
            status_text=(
                "Current access to the requested Document source is not established. "
                "No protected document metadata is shown."
            ),
        )
    authorization = decisions[0]

    matching_lineages = tuple(
        lineage
        for lineage in sources.lineages
        if lineage.subject_id == reference.subject_id
        and lineage.records[0].organization == workspace.organization
    )
    if not matching_lineages:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.SOURCE_UNAVAILABLE,
            status_text="The authorized Document source is unavailable in the current bounded source set.",
        )
    if len(matching_lineages) != 1:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.SOURCE_AMBIGUOUS,
            status_text="The authorized Document source is ambiguous and cannot be inspected safely.",
        )

    lineage = matching_lineages[0]
    if lineage.head.semantic_type != DOCUMENT_SEMANTIC_TYPE:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.SOURCE_UNAVAILABLE,
            status_text="The authorized governed source is not a Document source.",
        )

    if isinstance(reference, ExactVersionNavigationReference):
        try:
            displayed_record = lineage.resolve_version(reference.version_id)
        except CanonicalVersionNotFoundError:
            return DocumentWorkspaceBlockedState(
                code=DocumentWorkspaceBlockCode.VERSION_UNAVAILABLE,
                status_text="The requested exact Document Version is unavailable.",
            )
        reference_basis = DocumentReferenceBasis.EXACT_VERSION
        exact_version_selected = True
    else:
        displayed_record = lineage.head
        reference_basis = DocumentReferenceBasis.CANONICAL_HEAD
        exact_version_selected = False

    admitted_matches = tuple(
        admitted
        for admitted in sources.admitted_versions
        if admitted.document_id == displayed_record.subject_id
        and admitted.version_id == displayed_record.version_id
        and admitted.canonical_record == displayed_record
    )
    if len(admitted_matches) != 1:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.ADMISSION_EVIDENCE_UNAVAILABLE,
            status_text=(
                "The exact canonical Document Version lacks one unambiguous CAP-001 admitted "
                "manifest in the current source set. Artifact presentation is unavailable."
            ),
        )
    admitted = admitted_matches[0]

    if displayed_record.authority_mode is not AuthorityMode.NATIVE:
        # The current CanonicalRecord reference harness only admits Native mode.
        # If that changes later, this adapter must receive governed external
        # authority metadata rather than inventing it from locator/vendor text.
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.UNSUPPORTED_AUTHORITY,
            status_text=(
                "External document authority requires governed source metadata not carried by "
                "the current bounded reference source. No external source is inferred."
            ),
        )

    artifacts = _visible_artifacts(
        admitted=admitted,
        access_request=access_request,
        exact_version_selected=exact_version_selected,
    )
    if not artifacts:
        return DocumentWorkspaceBlockedState(
            code=DocumentWorkspaceBlockCode.HANDLING_ACCESS_DENIED,
            status_text=(
                "No governed Artifact metadata is accessible under the current declared "
                "purpose, required right and allowed classification context."
            ),
        )

    designated_visible = any(row.designated_rendition for row in artifacts)
    candidates = tuple(
        _candidate_inspection(candidate)
        for candidate in sources.working_candidates
        if candidate.canonical_record.subject_id == displayed_record.subject_id
        and candidate.canonical_record.organization == workspace.organization
        and candidate.canonical_record.version_id != displayed_record.version_id
    )

    return DocumentWorkspaceInspection(
        organization=workspace.organization,
        actor=workspace.actor,
        document_id=displayed_record.subject_id,
        reference_basis=reference_basis,
        displayed_version_id=displayed_record.version_id,
        head_version_id=lineage.head.version_id,
        lifecycle_status=displayed_record.lifecycle_status,
        authority_mode=displayed_record.authority_mode,
        authority_scope=displayed_record.authority_scope,
        authoritative_source_text="Arvectum OS Native governed Document source",
        canonical_state=DocumentCanonicalState.ADMITTED,
        designated_rendition_role=(
            admitted.designated_rendition_role if designated_visible else None
        ),
        artifacts=artifacts,
        working_candidates=candidates,
        authorization_decision_version_id=authorization.decision_version_id,
        access_purpose=access_request.purpose,
        required_right=access_request.required_right,
        allowed_classifications=access_request.allowed_classifications,
    )


def resolve_workspace_exact_reliance(
    *,
    inspection: DocumentWorkspaceInspection,
    sources: DocumentWorkspaceSourceSet,
    artifact_id: Identity,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    access_request: AccessRequest,
) -> ExactDocumentReliance:
    """Resolve exact governed reliance after rechecking current access context.

    Subject/Head browsing is intentionally insufficient for consequential reliance.
    The operator must explicitly inspect an exact Document Version first. Current
    source authorization and P3.07 Artifact handling constraints are re-evaluated
    before the existing CAP-001 exact-reliance resolver is invoked.
    """

    if not isinstance(inspection, DocumentWorkspaceInspection):
        raise ValueError("exact reliance requires a successful document inspection")
    if inspection.reference_basis is not DocumentReferenceBasis.EXACT_VERSION:
        raise ValueError("exact governed reliance requires an explicit exact Document Version")
    if not isinstance(sources, DocumentWorkspaceSourceSet):
        raise ValueError("sources must be a DocumentWorkspaceSourceSet")
    if not isinstance(artifact_id, Identity):
        raise ValueError("artifact_id must be an Identity")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization)
        for value in source_authorizations
    ):
        raise ValueError(
            "source_authorizations must contain CurrentSourceAuthorization values"
        )
    if not isinstance(access_request, AccessRequest):
        raise ValueError("access_request must be an explicit AccessRequest")
    if (
        access_request.actor != inspection.actor
        or access_request.organization != inspection.organization
    ):
        raise PermissionError("current Artifact access context does not match inspected Actor/Organization")

    decisions = _matching_authorizations_for_context(
        organization=inspection.organization,
        actor=inspection.actor,
        subject_id=inspection.document_id,
        decisions=source_authorizations,
    )
    if len(decisions) != 1 or not decisions[0].allowed:
        raise PermissionError("current Document source access is not established")

    matching_lineages = tuple(
        lineage
        for lineage in sources.lineages
        if lineage.subject_id == inspection.document_id
        and lineage.records[0].organization == inspection.organization
    )
    if len(matching_lineages) != 1:
        raise ValueError("exact governed Document lineage is not uniquely resolvable")

    admitted_matches = tuple(
        admitted
        for admitted in sources.admitted_versions
        if admitted.document_id == inspection.document_id
        and admitted.version_id == inspection.displayed_version_id
        and admitted.canonical_record.organization == inspection.organization
    )
    if len(admitted_matches) != 1:
        raise ValueError("exact admitted Document Version is not uniquely resolvable")
    admitted = admitted_matches[0]

    artifact_rows = tuple(
        artifact for artifact in inspection.artifacts if artifact.artifact_id == artifact_id
    )
    if len(artifact_rows) != 1:
        raise ValueError("selected Artifact is not visible in the exact Document Version")
    if artifact_rows[0].exact_reliance is not ExactRelianceAvailability.AVAILABLE:
        raise ValueError("selected Artifact is not admitted for exact governed reliance")

    # Re-evaluate the current request against CAP-001 handling constraints. The
    # returned content reference is deliberately not surfaced by the workspace;
    # this call is authorization evidence for the exact selected Artifact.
    resolve_document_for_access(
        admitted=admitted,
        artifact_id=artifact_id,
        request=access_request,
    )

    return resolve_exact_document_reliance(
        lineage=matching_lineages[0],
        admitted_versions=sources.admitted_versions,
        document_version_id=inspection.displayed_version_id,
        artifact_id=artifact_id,
    )


def render_document_workspace_html(result: DocumentWorkspaceResult) -> str:
    """Render inert, escaped document/artifact governance semantics as HTML."""

    if isinstance(result, DocumentWorkspaceBlockedState):
        return (
            '<section data-document-workspace="blocked">'
            '<h2>Document workspace unavailable</h2>'
            f'<p role="alert">{escape(result.status_text)}</p>'
            '<p>No governed Document or Artifact metadata is exposed.</p>'
            '</section>'
        )
    if not isinstance(result, DocumentWorkspaceInspection):
        raise ValueError("result must be a document workspace result")

    document_id = escape(result.document_id.value)
    displayed_version = escape(result.displayed_version_id.value)
    head_version = escape(result.head_version_id.value)
    lifecycle = escape(result.lifecycle_status or "not declared")
    authority_mode = escape(result.authority_mode.value)
    authority_scope = escape(result.authority_scope)
    authority_source = escape(result.authoritative_source_text)
    authorization_version = escape(result.authorization_decision_version_id.value)
    classifications = ", ".join(
        escape(value) for value in result.allowed_classifications
    )
    designated_role = escape(result.designated_rendition_role or "restricted/not visible")

    artifact_rows: list[str] = []
    for artifact in result.artifacts:
        source_ids = ", ".join(escape(value.value) for value in artifact.source_artifact_ids) or "none"
        transformation = escape(artifact.transformation or "none")
        rights = ", ".join(escape(value) for value in artifact.handling.rights)
        artifact_rows.append(
            '<tr>'
            f'<td>{escape(artifact.artifact_id.value)}</td>'
            f'<td>{escape(artifact.state.value)}</td>'
            f'<td>{escape(artifact.rendition_role)}</td>'
            f'<td>{"yes" if artifact.designated_rendition else "no"}</td>'
            f'<td>{escape(artifact.media_type)}</td>'
            f'<td>{escape(artifact.integrity_ref)}</td>'
            f'<td>{source_ids}</td>'
            f'<td>{transformation}</td>'
            f'<td>{escape(artifact.handling.classification)}</td>'
            f'<td>{escape(artifact.handling.purpose)}</td>'
            f'<td>{rights}</td>'
            f'<td>{escape(artifact.handling.retention_rule)}</td>'
            f'<td>{"present, value hidden" if artifact.storage_locator_present else "none"}</td>'
            f'<td>{escape(artifact.exact_reliance.value)}</td>'
            '</tr>'
        )

    candidate_blocks: list[str] = []
    for candidate in result.working_candidates:
        candidate_blocks.append(
            '<article data-canonical-state="working-candidate">'
            f'<h4>Working/Draft Candidate {escape(candidate.version_id.value)}</h4>'
            '<p>Non-canonical candidate. Its existence or generation does not admit it as a '
            'Document Version or organizational asset.</p>'
            f'<p>Contains artifacts: {"yes" if candidate.contains_artifacts else "no"}; '
            f'contains transient artifacts: {"yes" if candidate.contains_transient_artifacts else "no"}; '
            'Artifact metadata visible here: no.</p>'
            f'<p>{escape(candidate.promotion_status_text)}</p>'
            '</article>'
        )

    candidates_html = "".join(candidate_blocks) or (
        '<p data-working-candidates="none">No working/draft candidates are supplied.</p>'
    )

    return (
        '<section data-document-workspace="open" data-presentation-authority="non-authoritative">'
        '<h2>Document / Artifact workspace</h2>'
        '<p>Logical Document identity, immutable Document Version identity, Artifact identity, '
        'content integrity reference and storage locator are distinct concepts.</p>'
        '<dl>'
        f'<dt>Document Subject</dt><dd>{document_id}</dd>'
        f'<dt>Displayed Version</dt><dd>{displayed_version}</dd>'
        f'<dt>Reference basis</dt><dd>{escape(result.reference_basis.value)}</dd>'
        f'<dt>Canonical Head</dt><dd>{head_version}</dd>'
        f'<dt>Canonical state</dt><dd>{escape(result.canonical_state.value)}</dd>'
        f'<dt>Lifecycle</dt><dd>{lifecycle}</dd>'
        f'<dt>Authority mode</dt><dd>{authority_mode}</dd>'
        f'<dt>Authority scope</dt><dd>{authority_scope}</dd>'
        f'<dt>Authoritative source</dt><dd>{authority_source}</dd>'
        f'<dt>Source-access decision version</dt><dd>{authorization_version}</dd>'
        f'<dt>Access purpose</dt><dd>{escape(result.access_purpose)}</dd>'
        f'<dt>Required right</dt><dd>{escape(result.required_right)}</dd>'
        f'<dt>Allowed classifications</dt><dd>{classifications}</dd>'
        f'<dt>Visible designated rendition</dt><dd>{designated_role}</dd>'
        '</dl>'
        '<table><caption>Governed Artifact renditions visible under the current access context</caption>'
        '<thead><tr>'
        '<th>Artifact</th><th>State</th><th>Rendition</th><th>Designated</th>'
        '<th>Media type</th><th>Integrity</th><th>Derived from</th><th>Transformation</th>'
        '<th>Classification</th><th>Purpose</th><th>Rights</th><th>Retention</th>'
        '<th>Storage locator</th><th>Exact reliance</th>'
        '</tr></thead>'
        f'<tbody>{"".join(artifact_rows)}</tbody></table>'
        '<p data-access-note="true">Only Artifacts permitted by the current purpose/right/'
        'classification context are listed. Restricted Artifacts are omitted without counts or '
        'metadata. Retention is shown as governance meaning and is not modified by this surface.</p>'
        '<p data-minimization-note="true">Storage locator values and content references/bytes are '
        'not exposed by this bounded workspace surface. Presentation of governance metadata does '
        'not grant content retrieval, disclosure, export or Organizational Authority.</p>'
        '<h3>Working / draft candidates</h3>'
        f'{candidates_html}'
        '<p data-promotion-note="true">Generated or transient artifacts are not silently promoted. '
        'P4.06 exposes no admission/promotion control; consequential canonical admission must use '
        'an applicable Governed Execution path.</p>'
        '</section>'
    )
