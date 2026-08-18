"""P7.06-UI2 exact source-reconstruction presentation.

RFC-0006 reconstruction is evidence reconstruction, not side-effect replay.
UI2 consumes the existing CAP-004 ``AuditReconstructionView`` rather than
rendering a raw ReconstructionManifest, so current redaction/retention evidence
availability remains authoritative for disclosure.  The view is additionally
bound to the exact canonical source Version being inspected; UI2 never invents
reconstruction evidence from the current action Execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .audit_reconstruction_support import (
    AuditEvidenceItem,
    AuditReconstructionView,
    EvidenceAvailability,
)
from .canonical import CanonicalRecord
from .identity import Identity
from .security import OrganizationScope


class SourceReconstructionState(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"


@dataclass(frozen=True, slots=True)
class SourceReconstructionView:
    """Non-authoritative exact source binding over a CAP-004 audit view."""

    state: SourceReconstructionState
    source_subject_id: Identity
    source_version_id: Identity
    audit_view: AuditReconstructionView | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.state, SourceReconstructionState):
            raise ValueError("source reconstruction state must be explicit")
        if not isinstance(self.source_subject_id, Identity) or not isinstance(
            self.source_version_id, Identity
        ):
            raise ValueError("source reconstruction must preserve exact source identity")
        if self.state is SourceReconstructionState.UNAVAILABLE:
            if self.audit_view is not None:
                raise ValueError("unavailable reconstruction must not carry audit evidence")
            return
        if not isinstance(self.audit_view, AuditReconstructionView):
            raise ValueError("available reconstruction requires CAP-004 AuditReconstructionView")


def build_source_reconstruction_view(
    *,
    organization: OrganizationScope,
    source_record: CanonicalRecord,
    audit_view: AuditReconstructionView | None,
) -> SourceReconstructionView:
    """Bind optional authorized reconstruction evidence to one exact source Version.

    ``None`` means the trusted runtime has not established a currently viewable
    reconstruction for this exact source Version.  UI2 renders that state as
    unavailable and does not infer evidence from the in-flight action.
    """

    if not isinstance(organization, OrganizationScope):
        raise ValueError("source reconstruction requires explicit Organization")
    if not isinstance(source_record, CanonicalRecord):
        raise ValueError("source reconstruction requires an exact CanonicalRecord")
    if source_record.organization != organization:
        raise ValueError("source reconstruction source must share Organization scope")
    if audit_view is None:
        return SourceReconstructionView(
            state=SourceReconstructionState.UNAVAILABLE,
            source_subject_id=source_record.subject_id,
            source_version_id=source_record.version_id,
        )
    if not isinstance(audit_view, AuditReconstructionView):
        raise ValueError("source reconstruction evidence must be a CAP-004 AuditReconstructionView")
    if audit_view.organization != organization:
        raise ValueError("source reconstruction view must share Organization scope")

    exact_result = next(
        (
            item
            for item in audit_view.evidence
            if item.role == "result" and item.version_id == source_record.version_id
        ),
        None,
    )
    if exact_result is None:
        raise ValueError("reconstruction view does not reconstruct the exact inspected source Version")
    if (
        exact_result.availability is EvidenceAvailability.AVAILABLE
        and exact_result.source is not None
        and exact_result.source.subject_id != source_record.subject_id
    ):
        raise ValueError("available reconstruction result does not preserve source Subject Identity")

    execution_refs = {
        audit_view.execution_subject_id,
        *(
            item.version_id
            for item in audit_view.evidence
            if item.role == "execution-version"
        ),
    }
    if not execution_refs.intersection(source_record.provenance_refs):
        raise ValueError("source Version provenance does not preserve the reconstructed Execution")

    return SourceReconstructionView(
        state=SourceReconstructionState.AVAILABLE,
        source_subject_id=source_record.subject_id,
        source_version_id=source_record.version_id,
        audit_view=audit_view,
    )


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def _evidence_html(item: AuditEvidenceItem) -> str:
    availability = escape(item.availability.value)
    if item.availability is EvidenceAvailability.AVAILABLE:
        assert item.source is not None
        return (
            "<li>"
            f"Role {escape(item.role)} — <strong>{availability}</strong>; "
            f"Subject {escape(_identity_text(item.source.subject_id))}; "
            f"exact Version {escape(_identity_text(item.source.version_id))}; "
            f"semantic type {escape(item.source.semantic_type)}; "
            f"authority scope {escape(item.source.authority_scope)}"
            "</li>"
        )
    assert item.reason is not None
    return (
        "<li>"
        f"Role {escape(item.role)} — <strong>{availability}</strong>; "
        f"exact Version {escape(_identity_text(item.version_id))}; "
        f"reason {escape(item.reason)}. Governed source details are not disclosed."
        "</li>"
    )


def render_source_reconstruction_html(view: SourceReconstructionView) -> str:
    if not isinstance(view, SourceReconstructionView):
        raise ValueError("reconstruction rendering requires SourceReconstructionView")
    if view.state is SourceReconstructionState.UNAVAILABLE:
        return (
            '<section data-source-reconstruction="unavailable">'
            "<h4>Source reconstruction</h4>"
            "<p><strong>Unavailable for this exact source Version.</strong> "
            "No authorized CAP-004 reconstruction view was established by the trusted runtime. "
            "UI2 does not infer one from the current action and does not replay side effects.</p>"
            "</section>"
        )

    audit = view.audit_view
    assert audit is not None
    evidence = "".join(_evidence_html(item) for item in audit.evidence)
    correlations = "".join(
        f"<li>{escape(_identity_text(ref))}</li>" for ref in audit.correlation_refs
    )
    causations = "".join(
        f"<li>{escape(_identity_text(ref))}</li>" for ref in audit.causation_refs
    )
    return (
        '<section data-source-reconstruction="available">'
        "<h4>Source reconstruction</h4>"
        "<p><strong>Available from authorized CAP-004 / RFC-0006 governed evidence.</strong><br>"
        f"Operation: {escape(audit.operation_name)}<br>"
        f"Execution Subject: {escape(_identity_text(audit.execution_subject_id))}<br>"
        f"Initiating Actor: {escape(_identity_text(audit.initiating_actor_id))}<br>"
        f"Evidence complete: {'yes' if audit.complete else 'no'}</p>"
        f"<h5>Governed reconstruction evidence</h5><ul>{evidence}</ul>"
        f"<h5>Correlation references</h5><ul>{correlations}</ul>"
        f"<h5>Causation references</h5><ul>{causations}</ul>"
        "<p>Unavailable/redacted/deleted evidence remains unavailable in this UI; "
        "UI2 does not recover or disclose its hidden governed source pin.</p>"
        "<p>Reconstruction is read-only evidence reconstruction. Historical inspection never "
        "repeats an external or consequential effect.</p>"
        "</section>"
    )
