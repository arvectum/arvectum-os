"""Render the bounded P4.05 Governed Execution / gate action demo.

Usage from ``reference/python``::

    python examples/p4_05_governed_execution_demo.py > /tmp/arvectum-p4-05.html

The output is static demonstration HTML only. It establishes no HTTP route,
frontend framework, public API/BFF, IAM/session mechanism, decision authority,
durable runtime store or alternate canonical mutation path.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from arvectum_os_ref.canonical import build_p1_02_native_record
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.execution_action_experience import (
    inspect_governed_execution,
    render_governed_execution_html,
)
from arvectum_os_ref.governed_execution import (
    GovernedExecutionLineage,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    start_governed_execution,
    transition_governed_execution,
    GovernedExecutionLifecycle,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.runtime_consistency import RuntimeConsistencyState
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow
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


def build_demo() -> str:
    organization = OrganizationScope(
        Identity("organization", "demo-organization", "platform")
    )
    principal = Principal(Identity("principal", "demo-operator", "platform"))
    actor = ActorContext(principal, organization)
    target = build_p1_02_native_record(organization=organization, actor=actor)
    workflow = build_p1_03_workflow(
        organization=organization,
        actor=actor,
        target_record=target,
    )
    contract_pin = GovernedVersionPin(
        subject_id=_id("product-contract-subject", "demo-product-contract"),
        version_id=_id("product-contract-version", "demo-product-contract-v3"),
        semantic_type="platform.product-contract",
        authority_scope="platform.product-contract/boundary",
        lifecycle_status="Provisional",
    )
    required_gates = (
        GovernedGateKind.AUTHORIZATION,
        GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
        GovernedGateKind.CONSEQUENTIAL_APPROVAL,
    )
    created = start_governed_execution(
        organization=organization,
        actor=actor,
        workflow=workflow,
        operation_name="update-reference-subject",
        material_inputs=(target,),
        required_gates=required_gates,
        execution_id=_id("execution-subject", "execution-demo"),
        version_id=_id("execution-version", "execution-demo-v1"),
        created_at=datetime(2026, 8, 8, 15, 0, tzinfo=UTC),
        product_contract=contract_pin,
    )
    awaiting = await_required_gates(
        created,
        version_id=_id("execution-version", "execution-demo-v2"),
        actor=actor,
        created_at=datetime(2026, 8, 8, 15, 1, tzinfo=UTC),
    )
    decisions = tuple(
        build_governed_gate_decision(
            execution=awaiting,
            kind=kind,
            outcome=GovernedGateOutcome.ALLOW,
            decision_actor=actor,
            basis_ref=_id("gate-basis", f"{kind.value.lower()}-basis"),
            decision_id=_id("gate-decision-subject", f"{kind.value.lower()}-decision"),
            version_id=_id("gate-decision-version", f"{kind.value.lower()}-decision-v1"),
            created_at=datetime(2026, 8, 8, 15, 2, tzinfo=UTC),
        )
        for kind in required_gates
    )
    ready = admit_ready_execution(
        awaiting,
        decisions=decisions,
        version_id=_id("execution-version", "execution-demo-v3"),
        actor=actor,
        created_at=datetime(2026, 8, 8, 15, 3, tzinfo=UTC),
    )
    running = transition_governed_execution(
        ready,
        lifecycle=GovernedExecutionLifecycle.RUNNING,
        version_id=_id("execution-version", "execution-demo-v4"),
        actor=actor,
        created_at=datetime(2026, 8, 8, 15, 4, tzinfo=UTC),
    )

    shell = open_workspace_shell(actor)
    if not isinstance(shell, WorkspaceShellState):
        raise RuntimeError("demo shell unexpectedly failed to resolve Organization context")
    execution_state = navigate_workspace(
        shell,
        destination=WorkspaceDestination.EXECUTIONS,
        reference=SubjectNavigationReference(organization, created.execution_subject_id),
    )
    authorization = CurrentSourceAuthorization(
        organization=organization,
        actor_actual_principal_id=principal.principal_id,
        resource_subject_id=created.execution_subject_id,
        decision_version_id=_id("source-authorization-version", "inspect-execution-v1"),
        allowed=True,
    )
    runtime_state = RuntimeConsistencyState(canonical_records=(target,))

    awaiting_view = inspect_governed_execution(
        execution_state,
        lineages=(GovernedExecutionLineage((created, awaiting)),),
        authorizations=(authorization,),
        runtime_state=runtime_state,
    )
    ready_view = inspect_governed_execution(
        execution_state,
        lineages=(GovernedExecutionLineage((created, awaiting, ready, running)),),
        authorizations=(authorization,),
        runtime_state=runtime_state,
    )

    title = escape("Arvectum OS — P4.05 Governed Execution demo")
    return "".join(
        (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            f'<title>{title}</title></head><body><main>',
            '<h1>P4.05 bounded Governed Execution / gate / action experience</h1>',
            '<p>The first panel fails closed while required gates are unresolved. ',
            'The second panel exposes exact allow decisions separately and shows ',
            'that action intent may be prepared, while canonical mutation still ',
            'belongs only to the existing governed runtime path.</p>',
            '<h2>Awaiting required gates</h2>',
            render_governed_execution_html(awaiting_view),
            '<h2>Ready governed action context</h2>',
            render_governed_execution_html(ready_view),
            '</main></body></html>',
        )
    )


if __name__ == "__main__":
    print(build_demo())
