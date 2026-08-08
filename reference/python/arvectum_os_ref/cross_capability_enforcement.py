"""P3.07 — bounded cross-capability security, rights and Organization enforcement.

This internal reference slice composes the already-incubating CAP-001..CAP-004
semantics under one explicit access context. It is deliberately not an IAM,
PDP/PEP, policy-language, public API, stable entitlement model or production
security mechanism. It proves fail-closed composition only.
"""

from __future__ import annotations

from dataclasses import dataclass

from .audit_reconstruction_support import (
    AuditReconstructionView,
    EvidenceAvailability,
    EvidenceDisposition,
    reconstruct_audit_view,
)
from .document_artifact_governance import AdmittedDocumentVersion, ExactDocumentReliance
from .event_provenance import ReconstructionManifest
from .identity import Identity
from .memory_knowledge_governance import RetrievalProjection, ValidatedKnowledge
from .search_index_projection import (
    GovernedSearchSource,
    SearchHit,
    SearchProjection,
    query_projection,
    resolve_search_hit_for_reliance,
)
from .security import ActorContext, OrganizationScope


class CrossCapabilityEnforcementError(PermissionError):
    """The bounded P3.07 access context cannot safely permit an operation."""


@dataclass(frozen=True, slots=True)
class AccessRequest:
    """Explicit current request context; no ambient Organization or permission fallback."""

    actor: ActorContext
    purpose: str
    required_right: str
    allowed_classifications: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.actor, ActorContext):
            raise ValueError("actor context must be explicit")
        if not isinstance(self.purpose, str) or not self.purpose.strip():
            raise ValueError("purpose must be explicit")
        if not isinstance(self.required_right, str) or not self.required_right.strip():
            raise ValueError("required_right must be explicit")
        if not isinstance(self.allowed_classifications, tuple) or not self.allowed_classifications:
            raise ValueError("allowed_classifications must be explicit")
        if any(not isinstance(value, str) or not value.strip() for value in self.allowed_classifications):
            raise ValueError("allowed_classifications must contain explicit values")

    @property
    def organization(self) -> OrganizationScope:
        return self.actor.organization


def _require_constraints(*, organization: OrganizationScope, resource_organization: OrganizationScope, purpose: str, rights: tuple[str, ...], classification: str, request: AccessRequest) -> None:
    if organization != request.organization or resource_organization != request.organization:
        raise CrossCapabilityEnforcementError("cross-Organization access is denied by default")
    if purpose != request.purpose:
        raise CrossCapabilityEnforcementError("declared purpose is not permitted for this resource")
    if request.required_right not in rights:
        raise CrossCapabilityEnforcementError("required permitted-use right is absent")
    if classification not in request.allowed_classifications:
        raise CrossCapabilityEnforcementError("resource classification is not permitted")


def resolve_document_for_access(*, admitted: AdmittedDocumentVersion, artifact_id: Identity, request: AccessRequest) -> ExactDocumentReliance:
    """Resolve CAP-001 exact governed content only after current request enforcement."""

    if admitted.canonical_record.organization != request.organization:
        raise CrossCapabilityEnforcementError("cross-Organization Document access is denied")
    artifact = admitted.resolve_artifact(artifact_id)
    _require_constraints(
        organization=admitted.canonical_record.organization,
        resource_organization=artifact.organization,
        purpose=artifact.handling.purpose,
        rights=artifact.handling.rights,
        classification=artifact.handling.classification,
        request=request,
    )
    return ExactDocumentReliance(
        document_id=admitted.document_id,
        document_version_id=admitted.version_id,
        artifact_id=artifact.artifact_id,
        content_ref=artifact.content_ref,
        integrity_ref=artifact.integrity_ref,
        rendition_role=artifact.rendition_role,
        handling=artifact.handling,
    )


def retrieve_knowledge_for_access(*, knowledge: tuple[ValidatedKnowledge, ...], request: AccessRequest, allow_stale: bool = False) -> tuple[RetrievalProjection, ...]:
    """Apply one current access context to CAP-002 retrieval without rank authority."""

    results: list[RetrievalProjection] = []
    for item in knowledge:
        if item.canonical_record.organization != request.organization:
            continue
        constraints = item.constraints
        if constraints.purpose != request.purpose:
            continue
        if request.required_right not in constraints.rights:
            continue
        if constraints.classification not in request.allowed_classifications:
            continue
        if not allow_stale and constraints.freshness_state.lower() != "current":
            continue
        proposition = dict(item.canonical_record.payload).get("proposition", "")
        results.append(RetrievalProjection(item.subject_id, item.version_id, proposition, 1.0))
    return tuple(results)


def search_for_access(*, projection: SearchProjection, current_sources: tuple[GovernedSearchSource, ...], query_text: str, request: AccessRequest) -> tuple[SearchHit, ...]:
    """Compose CAP-003 discovery with the same Organization/purpose/right/classification context."""

    return query_projection(
        projection=projection,
        current_sources=current_sources,
        query_text=query_text,
        organization=request.organization,
        purpose=request.purpose,
        required_right=request.required_right,
        allowed_classifications=request.allowed_classifications,
    )


def resolve_search_hit_for_access(*, hit: SearchHit, current_sources: tuple[GovernedSearchSource, ...], request: AccessRequest):
    """Re-evaluate source constraints before exiting CAP-003; discovery never grants source access."""

    matches = tuple(
        source for source in current_sources
        if source.organization == request.organization
        and source.subject_id == hit.source_subject_id
        and source.version_id == hit.source_version_id
        and source.canonical_record.semantic_type == hit.source_semantic_type
    )
    if len(matches) != 1:
        raise CrossCapabilityEnforcementError("exact governed search source is not uniquely accessible")
    source = matches[0]
    _require_constraints(
        organization=request.organization,
        resource_organization=source.organization,
        purpose=source.constraints.purpose,
        rights=source.constraints.rights,
        classification=source.constraints.classification,
        request=request,
    )
    return resolve_search_hit_for_reliance(
        hit=hit,
        current_sources=current_sources,
        organization=request.organization,
        source_access_authorized=True,
    )


def reconstruct_audit_for_access(*, manifest: ReconstructionManifest, request: AccessRequest, evidence_constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...]) -> AuditReconstructionView:
    """Build CAP-004 view while redacting evidence that the current request may not inspect.

    Evidence constraints are a bounded test-harness handoff from the owning source
    controls: (version_id, purpose, rights, classification). Unknown or duplicate
    references fail closed. This is not a policy store or entitlement schema.
    """

    if manifest.organization != request.organization:
        raise CrossCapabilityEnforcementError("cross-Organization reconstruction is denied")
    if not isinstance(evidence_constraints, tuple):
        raise CrossCapabilityEnforcementError("evidence constraints must be explicit")
    ids = [row[0] for row in evidence_constraints]
    if len(set(ids)) != len(ids):
        raise CrossCapabilityEnforcementError("evidence constraints must be unique by Version Identity")

    dispositions: list[EvidenceDisposition] = []
    for version_id, purpose, rights, classification in evidence_constraints:
        if not isinstance(version_id, Identity):
            raise CrossCapabilityEnforcementError("evidence constraint requires exact Version Identity")
        permitted = (
            purpose == request.purpose
            and request.required_right in rights
            and classification in request.allowed_classifications
        )
        if not permitted:
            dispositions.append(EvidenceDisposition(
                version_id=version_id,
                availability=EvidenceAvailability.REDACTED,
                reason="current Organization/purpose/right/classification access context does not permit evidence disclosure",
            ))
    try:
        return reconstruct_audit_view(
            manifest=manifest,
            organization=request.organization,
            dispositions=tuple(dispositions),
        )
    except ValueError as exc:
        raise CrossCapabilityEnforcementError(str(exc)) from exc
