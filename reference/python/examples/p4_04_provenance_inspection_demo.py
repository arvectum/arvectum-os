"""Render the bounded P4.04 Version/Event/provenance reconstruction demo.

Usage from ``reference/python``::

    python examples/p4_04_provenance_inspection_demo.py > /tmp/arvectum-p4-04.html

The output is static demonstration HTML only. It establishes no HTTP route,
frontend framework, public API/BFF, durable Event/read-model store, telemetry
backend, IAM/session mechanism or replay executor. Current authorization and
evidence constraints are explicit caller-supplied handoffs from the owning
security/data-governance boundaries.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from arvectum_os_ref.audit_reconstruction_support import EvidenceAvailability, EvidenceDisposition
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.event_provenance import CanonicalEvent, ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.provenance_inspection import (
    inspect_version_event_provenance,
    render_provenance_inspection_html,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


UTC = timezone.utc


def _id(namespace: str, value: str) -> Identity:
    return Identity(namespace, value, "demo-organization")


def _pin(
    namespace: str,
    subject_value: str,
    version_value: str,
    semantic_type: str,
    *,
    lifecycle_status: str = "Established",
) -> GovernedVersionPin:
    return GovernedVersionPin(
        subject_id=_id(namespace, subject_value),
        version_id=_id(f"{namespace}-version", version_value),
        semantic_type=semantic_type,
        authority_scope=f"{semantic_type}/state",
        lifecycle_status=lifecycle_status,
    )


def build_demo() -> str:
    organization = OrganizationScope(
        Identity("organization", "demo-organization", "platform")
    )
    principal = Principal(Identity("principal", "demo-operator", "platform"))
    actor = ActorContext(principal, organization)
    execution_id = _id("execution-subject", "execution-demo")
    execution_v1 = GovernedVersionPin(
        subject_id=execution_id,
        version_id=_id("execution-version", "execution-demo-v1"),
        semantic_type="platform.execution-context",
        authority_scope="platform.execution-context/state",
        lifecycle_status="Running",
    )
    execution_v2 = GovernedVersionPin(
        subject_id=execution_id,
        version_id=_id("execution-version", "execution-demo-v2"),
        semantic_type="platform.execution-context",
        authority_scope="platform.execution-context/state",
        lifecycle_status="Succeeded",
    )
    workflow = _pin("workflow", "workflow-demo", "workflow-demo-v1", "platform.workflow")
    material = _pin("subject", "standard-demo", "standard-demo-v3", "example.standard")
    gate = _pin(
        "gate-decision",
        "approval-demo",
        "approval-demo-v1",
        "platform.authorization-decision",
        lifecycle_status="Allow",
    )
    result = _pin("result", "result-demo", "result-demo-v1", "example.result")
    event_pin = _pin("event", "event-demo", "event-demo-v1", "platform.event", lifecycle_status="Admitted")

    manifest = ReconstructionManifest(
        organization=organization,
        execution_subject_id=execution_id,
        initiating_actor_id=principal.principal_id,
        operation_name="apply-standard",
        workflow=workflow,
        material_inputs=(material,),
        gate_decisions=(gate,),
        execution_versions=(execution_v1, execution_v2),
        results=(result,),
        events=(event_pin,),
        event_types=(("platform.canonical-mutation.succeeded", "1"),),
        correlation_refs=(execution_id,),
        causation_refs=(execution_v2.version_id,),
        provenance_refs=(
            principal.principal_id,
            execution_id,
            workflow.subject_id,
            workflow.version_id,
            material.subject_id,
            material.version_id,
            gate.subject_id,
            gate.version_id,
            execution_v1.version_id,
            execution_v2.version_id,
            result.subject_id,
            result.version_id,
            event_pin.subject_id,
            event_pin.version_id,
        ),
    )

    occurred_at = datetime(2026, 8, 8, 14, 5, tzinfo=UTC)
    recorded_at = datetime(2026, 8, 8, 14, 6, tzinfo=UTC)
    producer = Identity("principal", "demo-event-producer", "platform")
    event_record = CanonicalRecord(
        subject_id=event_pin.subject_id,
        version_id=event_pin.version_id,
        semantic_type="platform.event",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.event/governed-outcome",
        accountable_owner_id=principal.principal_id,
        creation_actor=actor,
        created_at=recorded_at,
        provenance_refs=(
            producer,
            principal.principal_id,
            execution_id,
            execution_v2.version_id,
            result.subject_id,
            result.version_id,
        ),
        integrity_metadata=(("representation", "p4.04-static-demo"),),
        lifecycle_status="Admitted",
    )
    event = CanonicalEvent(
        record=event_record,
        event_type="platform.canonical-mutation.succeeded",
        event_schema_version="1",
        authoritative_source="Arvectum OS",
        occurred_at=occurred_at,
        recorded_at=recorded_at,
        producer_id=producer,
        initiating_actor_id=principal.principal_id,
        execution_subject_id=execution_id,
        execution_version_id=execution_v2.version_id,
        related_subject_ids=(result.subject_id,),
        related_version_ids=(result.version_id,),
        correlation_refs=(execution_id,),
        causation_refs=(execution_v2.version_id,),
        classification="internal",
        access_scope="audit-review",
    )

    state = open_workspace_shell(actor)
    if not isinstance(state, WorkspaceShellState):
        raise RuntimeError("demo shell unexpectedly failed to resolve Organization context")
    evidence_state = navigate_workspace(
        state,
        destination=WorkspaceDestination.EVIDENCE,
        reference=SubjectNavigationReference(organization, execution_id),
    )
    authorization = CurrentSourceAuthorization(
        organization=organization,
        actor_actual_principal_id=principal.principal_id,
        resource_subject_id=execution_id,
        decision_version_id=_id("authorization-decision-version", "demo-allow-execution"),
        allowed=True,
    )
    access_request = AccessRequest(
        actor=actor,
        purpose="audit-review",
        required_right="inspect-evidence",
        allowed_classifications=("internal",),
    )
    evidence_version_ids = (
        workflow.version_id,
        material.version_id,
        gate.version_id,
        execution_v1.version_id,
        execution_v2.version_id,
        result.version_id,
        event_pin.version_id,
    )
    constraints = tuple(
        (version_id, "audit-review", ("inspect-evidence",), "internal")
        for version_id in evidence_version_ids
    )

    complete = inspect_version_event_provenance(
        evidence_state,
        manifest=manifest,
        canonical_events=(event,),
        access_request=access_request,
        evidence_constraints=constraints,
        authorizations=(authorization,),
    )
    incomplete = inspect_version_event_provenance(
        evidence_state,
        manifest=manifest,
        canonical_events=(event,),
        access_request=access_request,
        evidence_constraints=constraints,
        authorizations=(authorization,),
        source_dispositions=(
            EvidenceDisposition(
                version_id=result.version_id,
                availability=EvidenceAvailability.MISSING,
                reason="historical result payload is unavailable in this bounded demo",
            ),
        ),
    )

    title = escape("Arvectum OS — P4.04 provenance inspection demo")
    return "".join(
        (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{title}</title></head><body><main>',
            '<h1>P4.04 bounded Version / Event / provenance experience</h1>',
            '<p>The first panel shows complete retained authorized evidence. The second ',
            'uses the same governed reconstruction with one explicitly missing result ',
            'evidence item; no missing history is inferred or repaired.</p>',
            render_provenance_inspection_html(complete),
            render_provenance_inspection_html(incomplete),
            '</main></body></html>',
        )
    )


if __name__ == "__main__":
    print(build_demo())
