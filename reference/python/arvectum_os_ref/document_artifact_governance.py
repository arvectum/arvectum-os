"""P3.03 — bounded CAP-001 Document & Artifact Governance incubation slice.

This module implements a deliberately small, in-memory and domain-neutral slice
of Accepted RFC-0008 above the Phase 2 Core Runtime semantic owners. It is an
internal Provisional capability implementation, not a public SDK/API, DMS,
object-store contract, stable serialization surface or production capability.

The slice proves only the CAP-001 responsibilities admitted by P3.02:
logical Document identity, immutable admitted Document Version identity,
Artifact/content identity, derivation provenance, exact-version reliance,
handling-constraint propagation and transient-versus-governed distinction.
Storage locators remain replaceable retrieval details and never become authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .canonical import CanonicalRecord
from .canonical_lineage import CanonicalLineage
from .identity import Identity
from .security import OrganizationScope


DOCUMENT_SEMANTIC_TYPE = "platform.document"


class DocumentArtifactGovernanceError(ValueError):
    """The bounded CAP-001 contract cannot satisfy the requested operation."""


class DocumentAdmissionError(DocumentArtifactGovernanceError):
    """A candidate cannot be admitted as an immutable governed Document Version."""


class DocumentRelianceError(DocumentArtifactGovernanceError):
    """Exact governed Document/Artifact reliance cannot be resolved safely."""


class ArtifactState(str, Enum):
    TRANSIENT = "Transient"
    GOVERNED = "Governed"


@dataclass(frozen=True, slots=True)
class HandlingConstraints:
    """Bounded RFC-0003 handling references propagated through derivation."""

    classification: str
    purpose: str
    rights: tuple[str, ...]
    retention_rule: str

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (self.classification, self.purpose, self.retention_rule)
        ):
            raise ValueError("classification, purpose and retention_rule must be explicit")
        if not isinstance(self.rights, tuple) or not self.rights or any(
            not isinstance(value, str) or not value.strip() for value in self.rights
        ):
            raise ValueError("rights must contain explicit permitted-use references")


@dataclass(frozen=True, slots=True)
class ArtifactContent:
    """One concrete content-bearing representation associated with a document."""

    artifact_id: Identity
    organization: OrganizationScope
    content_ref: str
    media_type: str
    integrity_ref: str
    rendition_role: str
    handling: HandlingConstraints
    state: ArtifactState = ArtifactState.TRANSIENT
    source_artifact_ids: tuple[Identity, ...] = ()
    transformation: str | None = None
    storage_locator: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.artifact_id, Identity):
            raise ValueError("artifact_id must be an Identity")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("artifact Organization scope must be explicit")
        for label, value in (
            ("content_ref", self.content_ref),
            ("media_type", self.media_type),
            ("integrity_ref", self.integrity_ref),
            ("rendition_role", self.rendition_role),
        ):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be explicit")
        if not isinstance(self.handling, HandlingConstraints):
            raise ValueError("artifact handling constraints must be explicit")
        if not isinstance(self.state, ArtifactState):
            raise ValueError("artifact state must be explicit")
        if not isinstance(self.source_artifact_ids, tuple) or any(
            not isinstance(source, Identity) for source in self.source_artifact_ids
        ):
            raise ValueError("source_artifact_ids must contain Identity references")
        if self.transformation is not None and not self.transformation.strip():
            raise ValueError("transformation must be non-empty when supplied")
        if self.source_artifact_ids and self.transformation is None:
            raise ValueError("derived artifacts must declare the transformation")

    def derive(
        self,
        *,
        artifact_id: Identity,
        content_ref: str,
        media_type: str,
        integrity_ref: str,
        rendition_role: str,
        transformation: str,
        storage_locator: str | None = None,
    ) -> "ArtifactContent":
        """Create a transient derived Artifact with inherited handling constraints."""

        return ArtifactContent(
            artifact_id=artifact_id,
            organization=self.organization,
            content_ref=content_ref,
            media_type=media_type,
            integrity_ref=integrity_ref,
            rendition_role=rendition_role,
            handling=self.handling,
            state=ArtifactState.TRANSIENT,
            source_artifact_ids=(self.artifact_id,),
            transformation=transformation,
            storage_locator=storage_locator,
        )


@dataclass(frozen=True, slots=True)
class DocumentVersionCandidate:
    """Mutable-workflow checkpoint input represented as immutable candidate evidence."""

    canonical_record: CanonicalRecord
    artifacts: tuple[ArtifactContent, ...]
    designated_rendition_role: str

    def __post_init__(self) -> None:
        if not isinstance(self.canonical_record, CanonicalRecord):
            raise ValueError("candidate requires a CanonicalRecord envelope")
        if self.canonical_record.semantic_type != DOCUMENT_SEMANTIC_TYPE:
            raise ValueError("candidate Canonical Record must use the document semantic type")
        if not isinstance(self.artifacts, tuple) or not self.artifacts:
            raise ValueError("candidate requires at least one Artifact representation")
        if not isinstance(self.designated_rendition_role, str) or not self.designated_rendition_role.strip():
            raise ValueError("designated rendition role must be explicit")


@dataclass(frozen=True, slots=True)
class AdmittedDocumentVersion:
    """One exact immutable governed Document Version plus its bounded manifest."""

    canonical_record: CanonicalRecord
    artifacts: tuple[ArtifactContent, ...]
    designated_rendition_role: str

    @property
    def document_id(self) -> Identity:
        return self.canonical_record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.canonical_record.version_id

    def resolve_artifact(self, artifact_id: Identity) -> ArtifactContent:
        matches = [artifact for artifact in self.artifacts if artifact.artifact_id == artifact_id]
        if len(matches) != 1:
            raise DocumentRelianceError("exact governed Artifact Identity is not uniquely resolvable")
        return matches[0]


@dataclass(frozen=True, slots=True)
class ExactDocumentReliance:
    """Exact governed source/version evidence used by consequential callers."""

    document_id: Identity
    document_version_id: Identity
    artifact_id: Identity
    content_ref: str
    integrity_ref: str
    rendition_role: str
    handling: HandlingConstraints


def admit_document_version(candidate: DocumentVersionCandidate) -> AdmittedDocumentVersion:
    """Admit a bounded immutable Document Version without selecting storage technology."""

    record = candidate.canonical_record
    seen_artifact_ids: set[Identity] = set()
    roles: set[str] = set()
    governed_artifacts: list[ArtifactContent] = []

    for artifact in candidate.artifacts:
        if artifact.organization != record.organization:
            raise DocumentAdmissionError("Document and Artifact must share Organization scope")
        if artifact.artifact_id in seen_artifact_ids:
            raise DocumentAdmissionError("Artifact Identity must be unique within the manifest")
        seen_artifact_ids.add(artifact.artifact_id)
        roles.add(artifact.rendition_role)
        governed_artifacts.append(
            ArtifactContent(
                artifact_id=artifact.artifact_id,
                organization=artifact.organization,
                content_ref=artifact.content_ref,
                media_type=artifact.media_type,
                integrity_ref=artifact.integrity_ref,
                rendition_role=artifact.rendition_role,
                handling=artifact.handling,
                state=ArtifactState.GOVERNED,
                source_artifact_ids=artifact.source_artifact_ids,
                transformation=artifact.transformation,
                storage_locator=artifact.storage_locator,
            )
        )

    if candidate.designated_rendition_role not in roles:
        raise DocumentAdmissionError("designated rendition role must resolve to a manifest Artifact")

    return AdmittedDocumentVersion(
        canonical_record=record,
        artifacts=tuple(governed_artifacts),
        designated_rendition_role=candidate.designated_rendition_role,
    )


def resolve_exact_document_reliance(
    *,
    lineage: CanonicalLineage,
    admitted_versions: tuple[AdmittedDocumentVersion, ...],
    document_version_id: Identity,
    artifact_id: Identity,
) -> ExactDocumentReliance:
    """Resolve exact admitted Document + Artifact state; never infer Head/Effective reliance."""

    exact_record = lineage.resolve_version(document_version_id)
    if exact_record.semantic_type != DOCUMENT_SEMANTIC_TYPE:
        raise DocumentRelianceError("exact canonical source is not a governed Document")

    matches = [
        version
        for version in admitted_versions
        if version.version_id == document_version_id
        and version.document_id == exact_record.subject_id
    ]
    if len(matches) != 1:
        raise DocumentRelianceError("exact admitted Document Version is not uniquely resolvable")

    admitted = matches[0]
    if admitted.canonical_record != exact_record:
        raise DocumentRelianceError("admitted Document Version does not match exact canonical source")
    artifact = admitted.resolve_artifact(artifact_id)
    if artifact.state is not ArtifactState.GOVERNED:
        raise DocumentRelianceError("consequential reliance requires a governed Artifact")

    return ExactDocumentReliance(
        document_id=admitted.document_id,
        document_version_id=admitted.version_id,
        artifact_id=artifact.artifact_id,
        content_ref=artifact.content_ref,
        integrity_ref=artifact.integrity_ref,
        rendition_role=artifact.rendition_role,
        handling=artifact.handling,
    )
