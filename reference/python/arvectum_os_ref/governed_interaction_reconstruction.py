"""P7.06-UI2 exact source-reconstruction presentation.

RFC-0006 reconstruction is evidence reconstruction, not side-effect replay.  This
module consumes the existing ``ReconstructionManifest`` primitive and binds it
to the exact canonical source Version being inspected by UI2.  It deliberately
does not construct reconstruction manifests from browser/UI data and does not
infer reconstruction when governed evidence is absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .canonical import CanonicalRecord
from .event_provenance import ReconstructionManifest
from .identity import Identity
from .security import OrganizationScope


class SourceReconstructionState(str, Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"


@dataclass(frozen=True, slots=True)
class SourceReconstructionView:
    """Non-authoritative, exact-reference view over RFC-0006 reconstruction."""

    state: SourceReconstructionState
    source_subject_id: Identity
    source_version_id: Identity
    operation_name: str | None = None
    execution_subject_id: Identity | None = None
    execution_version_id: Identity | None = None
    workflow_subject_id: Identity | None = None
    workflow_version_id: Identity | None = None
    event_versions: tuple[tuple[Identity, Identity, str, str], ...] = ()
    result_versions: tuple[tuple[Identity, Identity], ...] = ()
    provenance_refs: tuple[Identity, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.state, SourceReconstructionState):
            raise ValueError("source reconstruction state must be explicit")
        if not isinstance(self.source_subject_id, Identity) or not isinstance(
            self.source_version_id, Identity
        ):
            raise ValueError("source reconstruction must preserve exact source identity")
        details = (
            self.operation_name,
            self.execution_subject_id,
            self.execution_version_id,
            self.workflow_subject_id,
            self.workflow_version_id,
        )
        if self.state is SourceReconstructionState.UNAVAILABLE:
            if any(value is not None for value in details):
                raise ValueError("unavailable reconstruction must not manufacture governed details")
            if self.event_versions or self.result_versions or self.provenance_refs:
                raise ValueError("unavailable reconstruction must not manufacture evidence")
            return
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("available reconstruction requires an exact operation")
        if any(not isinstance(value, Identity) for value in details[1:]):
            raise ValueError("available reconstruction requires exact governed versions")
        if not self.result_versions or not self.event_versions or not self.provenance_refs:
            raise ValueError("available reconstruction requires result, Event and provenance evidence")


def build_source_reconstruction_view(
    *,
    organization: OrganizationScope,
    source_record: CanonicalRecord,
    manifest: ReconstructionManifest | None,
) -> SourceReconstructionView:
    """Bind optional RFC-0006 reconstruction evidence to one exact source Version.

    ``None`` means the runtime has not established a reusable reconstruction
    manifest for this exact source Version.  That is rendered truthfully as
    unavailable; UI2 never fabricates a manifest from the current in-flight
    action Execution.
    """

    if not isinstance(organization, OrganizationScope):
        raise ValueError("source reconstruction requires explicit Organization")
    if not isinstance(source_record, CanonicalRecord):
        raise ValueError("source reconstruction requires an exact CanonicalRecord")
    if source_record.organization != organization:
        raise ValueError("source reconstruction source must share Organization scope")
    if manifest is None:
        return SourceReconstructionView(
            state=SourceReconstructionState.UNAVAILABLE,
            source_subject_id=source_record.subject_id,
            source_version_id=source_record.version_id,
        )
    if not isinstance(manifest, ReconstructionManifest):
        raise ValueError("source reconstruction evidence must be an RFC-0006 ReconstructionManifest")
    if manifest.organization != organization:
        raise ValueError("source reconstruction manifest must share Organization scope")

    exact_source_result = any(
        pin.subject_id == source_record.subject_id and pin.version_id == source_record.version_id
        for pin in manifest.results
    )
    if not exact_source_result:
        raise ValueError("reconstruction manifest does not reconstruct the exact inspected source Version")

    execution_refs = {
        manifest.execution_subject_id,
        *(pin.version_id for pin in manifest.execution_versions),
    }
    if not execution_refs.intersection(source_record.provenance_refs):
        raise ValueError("source Version provenance does not preserve the reconstructed Execution")

    terminal_pin = manifest.execution_versions[-1]
    event_versions = tuple(
        (pin.subject_id, pin.version_id, event_type, schema_version)
        for pin, (event_type, schema_version) in zip(
            manifest.events,
            manifest.event_types,
            strict=True,
        )
    )
    result_versions = tuple((pin.subject_id, pin.version_id) for pin in manifest.results)
    return SourceReconstructionView(
        state=SourceReconstructionState.AVAILABLE,
        source_subject_id=source_record.subject_id,
        source_version_id=source_record.version_id,
        operation_name=manifest.operation_name,
        execution_subject_id=manifest.execution_subject_id,
        execution_version_id=terminal_pin.version_id,
        workflow_subject_id=manifest.workflow.subject_id,
        workflow_version_id=manifest.workflow.version_id,
        event_versions=event_versions,
        result_versions=result_versions,
        provenance_refs=manifest.provenance_refs,
    )


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def render_source_reconstruction_html(view: SourceReconstructionView) -> str:
    if not isinstance(view, SourceReconstructionView):
        raise ValueError("reconstruction rendering requires SourceReconstructionView")
    if view.state is SourceReconstructionState.UNAVAILABLE:
        return (
            '<section data-source-reconstruction="unavailable">'
            "<h4>Source reconstruction</h4>"
            "<p><strong>Unavailable for this exact source Version.</strong> "
            "No reusable RFC-0006 ReconstructionManifest was established by the trusted runtime. "
            "UI2 does not infer one from the current action and does not replay side effects.</p>"
            "</section>"
        )

    assert view.operation_name is not None
    assert view.execution_subject_id is not None
    assert view.execution_version_id is not None
    assert view.workflow_subject_id is not None
    assert view.workflow_version_id is not None
    events = "".join(
        "<li>"
        f"Event Subject {_identity_text(subject)}; exact Version {_identity_text(version)}; "
        f"type {escape(event_type)}; schema {escape(schema_version)}"
        "</li>"
        for subject, version, event_type, schema_version in view.event_versions
    )
    results = "".join(
        f"<li>Subject {escape(_identity_text(subject))}; exact Version {escape(_identity_text(version))}</li>"
        for subject, version in view.result_versions
    )
    provenance = "".join(
        f"<li>{escape(_identity_text(ref))}</li>" for ref in view.provenance_refs
    )
    return (
        '<section data-source-reconstruction="available">'
        "<h4>Source reconstruction</h4>"
        "<p><strong>Available from exact RFC-0006 governed evidence.</strong><br>"
        f"Operation: {escape(view.operation_name)}<br>"
        f"Execution Subject: {escape(_identity_text(view.execution_subject_id))}<br>"
        f"Exact reconstructed Execution Version: {escape(_identity_text(view.execution_version_id))}<br>"
        f"Workflow Subject: {escape(_identity_text(view.workflow_subject_id))}<br>"
        f"Exact Workflow Version: {escape(_identity_text(view.workflow_version_id))}</p>"
        f"<h5>Exact results</h5><ul>{results}</ul>"
        f"<h5>Admitted canonical Events</h5><ul>{events}</ul>"
        f"<h5>Reconstruction provenance</h5><ul>{provenance}</ul>"
        "<p>Reconstruction is read-only evidence reconstruction. Historical inspection never "
        "repeats an external or consequential effect.</p>"
        "</section>"
    )
