"""P4.04 — bounded Version, Event, provenance and reconstruction experience.

Internal read-only presentation boundary over existing RFC-0006 Event/provenance,
CAP-004 Audit/Reconstruction Support and P3.07 current access enforcement. It is
not an Event store, telemetry backend, replay executor, durable read model,
public API/SDK, IAM/PDP, Product Contract or canonical mutation path.

The boundary deliberately keeps canonical Event history separate from raw
telemetry, preserves correlation versus causation and exact relied-upon Version
Identities, exposes retained-evidence limitations honestly, and labels every
reconstruction/replay description as derived and non-authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .audit_reconstruction_support import (
    AuditReconstructionView,
    EvidenceAvailability,
    EvidenceDisposition,
    reconstruct_audit_view,
)
from .canonical import AuthorityMode
from .canonical_inspection import CurrentSourceAuthorization
from .cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
    reconstruct_audit_for_access,
)
from .event_provenance import CanonicalEvent, ReconstructionManifest
from .identity import Identity
from .workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceShellState,
)


class ProvenanceReferenceBasis(str, Enum):
    EXECUTION_SUBJECT = "Execution Subject"
    EXACT_EXECUTION_VERSION = "Exact Execution Version"


class ProvenanceInspectionBlockCode(str, Enum):
    REFERENCE_REQUIRED = "reference-required"
    ACCESS_DENIED = "access-denied"
    SOURCE_UNAVAILABLE = "source-unavailable"
    VERSION_UNAVAILABLE = "version-unavailable"
    EVIDENCE_INCONSISTENT = "evidence-inconsistent"


class ReconstructionPresentationAuthority(str, Enum):
    DERIVED_NON_AUTHORITATIVE = "Derived, read-only, non-authoritative reconstruction"


class ReplayPresentationMode(str, Enum):
    PROJECTION_ONLY = "Derived projection replay only; no consequential side effects"


@dataclass(frozen=True, slots=True)
class EventHistoryInspection:
    """Authorized canonical Event metadata; never raw telemetry."""

    event_id: Identity
    version_id: Identity
    event_type: str
    event_schema_version: str
    authority_mode: AuthorityMode
    authority_scope: str
    authoritative_source: str
    occurred_at_text: str
    recorded_at_text: str
    producer_id: Identity
    initiating_actor_id: Identity
    execution_subject_id: Identity
    execution_version_id: Identity
    related_subject_ids: tuple[Identity, ...]
    related_version_ids: tuple[Identity, ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    classification: str
    access_scope: str


@dataclass(frozen=True, slots=True)
class ProvenanceInspection:
    """Disposable operator view over already-governed reconstruction evidence."""

    reference_basis: ProvenanceReferenceBasis
    selected_execution_version_id: Identity | None
    audit_view: AuditReconstructionView
    events: tuple[EventHistoryInspection, ...]
    provenance_refs: tuple[Identity, ...]
    telemetry_included: bool = False
    reconstruction_authority: ReconstructionPresentationAuthority = (
        ReconstructionPresentationAuthority.DERIVED_NON_AUTHORITATIVE
    )
    replay_mode: ReplayPresentationMode = ReplayPresentationMode.PROJECTION_ONLY
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if not isinstance(self.reference_basis, ProvenanceReferenceBasis):
            raise ValueError("P4.04 reference basis must be explicit")
        if self.selected_execution_version_id is not None and not isinstance(
            self.selected_execution_version_id, Identity
        ):
            raise ValueError("selected Execution Version must be an Identity when supplied")
        if not isinstance(self.audit_view, AuditReconstructionView):
            raise ValueError("P4.04 requires a derived AuditReconstructionView")
        if not isinstance(self.events, tuple) or any(
            not isinstance(event, EventHistoryInspection) for event in self.events
        ):
            raise ValueError("P4.04 Event history must be an immutable typed tuple")
        if not isinstance(self.provenance_refs, tuple) or any(
            not isinstance(ref, Identity) for ref in self.provenance_refs
        ):
            raise ValueError("P4.04 provenance references must be explicit Identity values")
        if self.telemetry_included:
            raise ValueError("P4.04 canonical Event history must not silently include raw telemetry")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("P4.04 presentation cannot become canonical authority")
        if self.reconstruction_authority is not ReconstructionPresentationAuthority.DERIVED_NON_AUTHORITATIVE:
            raise ValueError("reconstruction presentation must remain explicitly non-authoritative")
        if self.replay_mode is not ReplayPresentationMode.PROJECTION_ONLY:
            raise ValueError("P4.04 replay presentation cannot expose consequential replay")


@dataclass(frozen=True, slots=True)
class ProvenanceInspectionBlockedState:
    """Fail-closed no-content state that reveals no protected evidence metadata."""

    code: ProvenanceInspectionBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, ProvenanceInspectionBlockCode):
            raise ValueError("blocked provenance state requires an explicit code")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("blocked provenance state requires textual meaning")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("blocked presentation cannot become authoritative")
        if self.governed_content_visible:
            raise ValueError("blocked provenance state must expose no governed content")


ProvenanceInspectionResult = ProvenanceInspection | ProvenanceInspectionBlockedState


def _represented_id(state: WorkspaceShellState) -> Identity | None:
    represented = state.actor.represented_principal
    return None if represented is None else represented.principal_id


def _current_authorization(
    *,
    state: WorkspaceShellState,
    resource_subject_id: Identity,
    authorizations: tuple[CurrentSourceAuthorization, ...],
) -> CurrentSourceAuthorization | None:
    if not isinstance(authorizations, tuple):
        return None
    matches = tuple(
        decision
        for decision in authorizations
        if isinstance(decision, CurrentSourceAuthorization)
        and decision.organization == state.organization
        and decision.actor_actual_principal_id == state.actor.actual_principal.principal_id
        and decision.represented_principal_id == _represented_id(state)
        and decision.resource_subject_id == resource_subject_id
    )
    if len(matches) != 1 or matches[0].allowed is not True:
        return None
    return matches[0]


def _blocked(code: ProvenanceInspectionBlockCode, text: str) -> ProvenanceInspectionBlockedState:
    return ProvenanceInspectionBlockedState(code=code, status_text=text)


def _merge_evidence_dispositions(
    *,
    manifest: ReconstructionManifest,
    access_view: AuditReconstructionView,
    source_dispositions: tuple[EvidenceDisposition, ...],
) -> AuditReconstructionView:
    """Preserve access redaction, then apply declared retention/availability gaps.

    Access denial dominates a source-retention disposition so a caller cannot
    learn whether denied evidence was deleted, missing or otherwise unavailable
    behind the current access boundary.
    """

    if not isinstance(source_dispositions, tuple) or any(
        not isinstance(item, EvidenceDisposition) for item in source_dispositions
    ):
        raise ValueError("source evidence dispositions must be an immutable typed tuple")
    if len({item.version_id for item in source_dispositions}) != len(source_dispositions):
        raise ValueError("source evidence dispositions must be unique by Version Identity")
    if any(item.availability is EvidenceAvailability.REDACTED for item in source_dispositions):
        raise ValueError("source dispositions cannot manufacture access redaction")

    known = {item.version_id for item in access_view.evidence}
    if any(item.version_id not in known for item in source_dispositions):
        raise ValueError("source disposition references evidence outside the governed reconstruction")

    source_by_version = {item.version_id: item for item in source_dispositions}
    merged: list[EvidenceDisposition] = []
    for item in access_view.evidence:
        if item.availability is EvidenceAvailability.REDACTED:
            merged.append(
                EvidenceDisposition(
                    version_id=item.version_id,
                    availability=EvidenceAvailability.REDACTED,
                    reason=item.reason,
                )
            )
            continue
        source = source_by_version.get(item.version_id)
        if source is not None and source.availability is not EvidenceAvailability.AVAILABLE:
            merged.append(source)

    return reconstruct_audit_view(
        manifest=manifest,
        organization=access_view.organization,
        dispositions=tuple(merged),
    )


def _event_history(
    *,
    manifest: ReconstructionManifest,
    audit_view: AuditReconstructionView,
    canonical_events: tuple[CanonicalEvent, ...],
) -> tuple[EventHistoryInspection, ...]:
    if not isinstance(canonical_events, tuple) or any(
        not isinstance(event, CanonicalEvent) for event in canonical_events
    ):
        raise ValueError("canonical_events must be an immutable tuple of CanonicalEvent values")
    if len({event.version_id for event in canonical_events}) != len(canonical_events):
        raise ValueError("canonical Event source must not duplicate Version Identities")

    visible_event_versions = {
        item.version_id
        for item in audit_view.evidence
        if item.role == "event" and item.availability is EvidenceAvailability.AVAILABLE
    }
    declared_event_versions = tuple(pin.version_id for pin in manifest.events)
    event_type_by_version = {
        pin.version_id: manifest.event_types[index]
        for index, pin in enumerate(manifest.events)
    }
    supplied = {event.version_id: event for event in canonical_events}

    if any(version_id not in declared_event_versions for version_id in supplied):
        raise ValueError("canonical Event source contains an Event outside the reconstruction manifest")
    if set(supplied) != visible_event_versions:
        raise ValueError(
            "canonical Event source must contain exactly the currently visible Event evidence versions"
        )

    execution_version_ids = {pin.version_id for pin in manifest.execution_versions}
    result: list[EventHistoryInspection] = []
    for version_id in declared_event_versions:
        if version_id not in visible_event_versions:
            continue
        event = supplied[version_id]
        expected_type, expected_schema = event_type_by_version[version_id]
        if (event.event_type, event.event_schema_version) != (expected_type, expected_schema):
            raise ValueError("canonical Event type/schema does not match reconstruction evidence")
        if event.organization != manifest.organization:
            raise ValueError("canonical Event Organization does not match reconstruction")
        if event.execution_subject_id != manifest.execution_subject_id:
            raise ValueError("canonical Event does not belong to the reconstructed Execution")
        if event.execution_version_id not in execution_version_ids:
            raise ValueError("canonical Event references an Execution Version outside reconstruction")
        result.append(
            EventHistoryInspection(
                event_id=event.event_id,
                version_id=event.version_id,
                event_type=event.event_type,
                event_schema_version=event.event_schema_version,
                authority_mode=event.record.authority_mode,
                authority_scope=event.record.authority_scope,
                authoritative_source=event.authoritative_source,
                occurred_at_text=event.occurred_at.isoformat(),
                recorded_at_text=event.recorded_at.isoformat(),
                producer_id=event.producer_id,
                initiating_actor_id=event.initiating_actor_id,
                execution_subject_id=event.execution_subject_id,
                execution_version_id=event.execution_version_id,
                related_subject_ids=event.related_subject_ids,
                related_version_ids=event.related_version_ids,
                correlation_refs=event.correlation_refs,
                causation_refs=event.causation_refs,
                classification=event.classification,
                access_scope=event.access_scope,
            )
        )
    return tuple(result)


def inspect_version_event_provenance(
    state: WorkspaceShellState,
    *,
    manifest: ReconstructionManifest,
    canonical_events: tuple[CanonicalEvent, ...],
    access_request: AccessRequest,
    evidence_constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...],
    authorizations: tuple[CurrentSourceAuthorization, ...],
    source_dispositions: tuple[EvidenceDisposition, ...] = (),
) -> ProvenanceInspectionResult:
    """Resolve one authorized execution evidence view without replay or mutation.

    Security order is intentional: source authorization is consumed first; then
    P3.07 re-evaluates current Organization/purpose/right/classification for every
    exact reconstruction evidence Version; only after that may this presentation
    distinguish whether a requested exact Execution Version exists in the
    authorized reconstruction.
    """

    if not isinstance(state, WorkspaceShellState):
        raise ValueError("P4.04 inspection requires an open WorkspaceShellState")
    reference = state.current_reference
    if not isinstance(reference, (SubjectNavigationReference, ExactVersionNavigationReference)):
        return _blocked(
            ProvenanceInspectionBlockCode.REFERENCE_REQUIRED,
            "An explicit Execution reference is required before evidence can be inspected.",
        )

    requested_subject_id = reference.subject_id
    if _current_authorization(
        state=state,
        resource_subject_id=requested_subject_id,
        authorizations=authorizations,
    ) is None:
        return _blocked(
            ProvenanceInspectionBlockCode.ACCESS_DENIED,
            "Evidence is unavailable for the current governed access context.",
        )

    if not isinstance(manifest, ReconstructionManifest):
        return _blocked(
            ProvenanceInspectionBlockCode.SOURCE_UNAVAILABLE,
            "Governed reconstruction evidence is unavailable for this reference.",
        )
    if manifest.organization != state.organization or manifest.execution_subject_id != requested_subject_id:
        return _blocked(
            ProvenanceInspectionBlockCode.SOURCE_UNAVAILABLE,
            "Governed reconstruction evidence is unavailable for this reference.",
        )

    if not isinstance(access_request, AccessRequest):
        return _blocked(
            ProvenanceInspectionBlockCode.ACCESS_DENIED,
            "Evidence is unavailable for the current governed access context.",
        )
    if access_request.actor != state.actor or access_request.organization != state.organization:
        return _blocked(
            ProvenanceInspectionBlockCode.ACCESS_DENIED,
            "Evidence is unavailable for the current governed access context.",
        )

    try:
        access_view = reconstruct_audit_for_access(
            manifest=manifest,
            request=access_request,
            evidence_constraints=evidence_constraints,
        )
        audit_view = _merge_evidence_dispositions(
            manifest=manifest,
            access_view=access_view,
            source_dispositions=source_dispositions,
        )
    except (CrossCapabilityEnforcementError, ValueError):
        return _blocked(
            ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT,
            "Authorized evidence cannot be reconstructed consistently from the supplied governed sources.",
        )

    reference_basis = ProvenanceReferenceBasis.EXECUTION_SUBJECT
    selected_execution_version_id: Identity | None = None
    if isinstance(reference, ExactVersionNavigationReference):
        execution_versions = {pin.version_id for pin in manifest.execution_versions}
        if reference.version_id not in execution_versions:
            return _blocked(
                ProvenanceInspectionBlockCode.VERSION_UNAVAILABLE,
                "The requested exact Execution Version is unavailable in the authorized reconstruction.",
            )
        reference_basis = ProvenanceReferenceBasis.EXACT_EXECUTION_VERSION
        selected_execution_version_id = reference.version_id

    try:
        event_history = _event_history(
            manifest=manifest,
            audit_view=audit_view,
            canonical_events=canonical_events,
        )
    except ValueError:
        return _blocked(
            ProvenanceInspectionBlockCode.EVIDENCE_INCONSISTENT,
            "Authorized evidence cannot be reconstructed consistently from the supplied governed sources.",
        )

    return ProvenanceInspection(
        reference_basis=reference_basis,
        selected_execution_version_id=selected_execution_version_id,
        audit_view=audit_view,
        events=event_history,
        provenance_refs=manifest.provenance_refs,
    )


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def _render_identity_list(values: tuple[Identity, ...]) -> str:
    if not values:
        return "<span>None declared</span>"
    return "<ul>" + "".join(
        f"<li>{escape(_identity_text(value))}</li>" for value in values
    ) + "</ul>"


def _render_event(event: EventHistoryInspection) -> str:
    """Render one Event as a readable definition list instead of a wide table."""

    return "".join(
        (
            '<article data-event-history="canonical-event">',
            f'<h3>{escape(event.event_type)} / schema {escape(event.event_schema_version)}</h3>',
            '<dl>',
            f'<dt>Event Identity</dt><dd>{escape(_identity_text(event.event_id))}</dd>',
            f'<dt>Exact Event Version</dt><dd>{escape(_identity_text(event.version_id))}</dd>',
            f'<dt>Occurred</dt><dd>{escape(event.occurred_at_text)}</dd>',
            f'<dt>Recorded/admitted</dt><dd>{escape(event.recorded_at_text)}</dd>',
            f'<dt>Producer</dt><dd>{escape(_identity_text(event.producer_id))}</dd>',
            f'<dt>Initiating actor</dt><dd>{escape(_identity_text(event.initiating_actor_id))}</dd>',
            f'<dt>Execution</dt><dd>{escape(_identity_text(event.execution_subject_id))}</dd>',
            f'<dt>Causal Execution Version</dt><dd>{escape(_identity_text(event.execution_version_id))}</dd>',
            f'<dt>Authority</dt><dd>{escape(event.authority_mode.value)} / '
            f'{escape(event.authority_scope)} / source {escape(event.authoritative_source)}</dd>',
            f'<dt>Classification / access scope</dt><dd>{escape(event.classification)} / '
            f'{escape(event.access_scope)}</dd>',
            '<dt>Related Subject references</dt><dd>',
            _render_identity_list(event.related_subject_ids),
            '</dd><dt>Related exact Version references</dt><dd>',
            _render_identity_list(event.related_version_ids),
            '</dd><dt>Correlation references</dt><dd>',
            _render_identity_list(event.correlation_refs),
            '</dd><dt>Causation references</dt><dd>',
            _render_identity_list(event.causation_refs),
            '</dd></dl></article>',
        )
    )


def render_provenance_inspection_html(result: ProvenanceInspectionResult) -> str:
    """Render inert accessible HTML; establishes no route, API or action semantics."""

    if isinstance(result, ProvenanceInspectionBlockedState):
        return "".join(
            (
                '<main data-provenance-state="blocked">',
                '<h1>Evidence unavailable</h1>',
                f'<p role="alert">{escape(result.status_text)}</p>',
                '<p>Presentation state only; no governed evidence metadata is exposed.</p>',
                '</main>',
            )
        )
    if not isinstance(result, ProvenanceInspection):
        raise ValueError("result must be a P4.04 provenance inspection result")

    audit = result.audit_view
    completeness = "Complete within retained authorized evidence" if audit.complete else "Incomplete"
    selected = "Execution Subject"
    if result.selected_execution_version_id is not None:
        selected = "Exact Execution Version " + _identity_text(result.selected_execution_version_id)

    evidence_rows: list[str] = []
    limitation_rows: list[str] = []
    for item in audit.evidence:
        if item.source is not None:
            source = " / ".join(
                (
                    escape(_identity_text(item.source.subject_id)),
                    "exact Version " + escape(_identity_text(item.source.version_id)),
                    escape(item.source.semantic_type),
                )
            )
        else:
            source = "Exact Version " + escape(_identity_text(item.version_id)) + " / source not disclosed"
        evidence_rows.append(
            "".join(
                (
                    "<tr>",
                    f"<td>{escape(item.role)}</td>",
                    f"<td>{escape(item.availability.value)}</td>",
                    f"<td>{source}</td>",
                    f"<td>{escape(item.reason or '—')}</td>",
                    "</tr>",
                )
            )
        )
        if item.availability is not EvidenceAvailability.AVAILABLE:
            limitation_rows.append(
                f"<li>{escape(item.role)} — {escape(item.availability.value)}: "
                f"{escape(item.reason or 'evidence is not available')}</li>"
            )

    event_content = (
        "".join(_render_event(event) for event in result.events)
        if result.events
        else '<p>No currently visible canonical Event metadata is available.</p>'
    )
    limitations = (
        '<ul>' + "".join(limitation_rows) + '</ul>'
        if limitation_rows
        else '<p>No retained-evidence limitation is declared in the current authorized reconstruction.</p>'
    )

    return "".join(
        (
            '<main data-provenance-state="open" data-presentation-authority="non-authoritative">',
            '<header><h1>Version, Event, provenance &amp; reconstruction</h1>',
            f'<p>Organization: {escape(audit.organization.organization_id.value)}</p>',
            f'<p>Selection basis: {escape(selected)}</p>',
            f'<p>Execution: {escape(_identity_text(audit.execution_subject_id))}</p>',
            f'<p>Initiating actor: {escape(_identity_text(audit.initiating_actor_id))}</p>',
            f'<p>Operation: {escape(audit.operation_name)}</p></header>',
            '<section aria-labelledby="reconstruction-status"><h2 id="reconstruction-status">Reconstruction status</h2>',
            f'<p><strong>{escape(completeness)}</strong></p>',
            '<p>Derived, read-only, non-authoritative reconstruction. This view is not canonical state, ',
            'does not repair history and cannot authorize or perform a consequential action.</p>',
            '<p>Replay is described only for rebuilding a derived non-authoritative projection. ',
            'No replay is executed by this view; a new consequential action requires a new Governed Execution.</p>',
            '</section>',
            '<section aria-labelledby="evidence"><h2 id="evidence">Exact relied-upon versions</h2>',
            '<table><caption>Governed reconstruction evidence</caption>',
            '<thead><tr><th>Role</th><th>Availability</th><th>Exact governed source</th><th>Limitation</th></tr></thead>',
            '<tbody>',
            "".join(evidence_rows),
            '</tbody></table></section>',
            '<section aria-labelledby="events"><h2 id="events">Canonical Event history</h2>',
            '<p>Canonical Events are shown separately from raw logs, metrics, traces and other operational telemetry. ',
            'Occurrence time and recording/admission time are distinct; display order is not asserted as a universal total order.</p>',
            event_content,
            '</section>',
            '<section aria-labelledby="correlation"><h2 id="correlation">Correlation and causation</h2>',
            '<h3>Correlation references</h3>',
            _render_identity_list(audit.correlation_refs),
            '<h3>Causation references</h3>',
            _render_identity_list(audit.causation_refs),
            '<p>Correlation is not causation; neither is Authorization or Organizational Authority.</p></section>',
            '<section aria-labelledby="provenance"><h2 id="provenance">Provenance chain references</h2>',
            _render_identity_list(result.provenance_refs),
            '<p>These are traceability references, not independent grants of access, reuse rights or authority.</p></section>',
            '<section aria-labelledby="limitations"><h2 id="limitations">Known reconstruction limitations</h2>',
            limitations,
            '<p>Deletion, minimization, redaction, missing evidence, uncertainty or unavailable dependencies reduce the supported ',
            'reconstruction claim; the interface does not infer or fabricate missing history.</p></section>',
            '<footer><p>Presentation state only. Raw telemetry is excluded and this reconstruction never becomes a source of truth.</p></footer>',
            '</main>',
        )
    )
