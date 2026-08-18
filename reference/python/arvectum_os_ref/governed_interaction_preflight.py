"""P7.06-UI2 — bounded governed-interaction preflight composition.

This module composes already-proven Phase-4 workspace, Governed Execution and
R10 operator-safety semantics.  It is intentionally not an authorization
engine, Organizational Authority source, approval policy, canonical store,
public API or second mutation path.

A caller supplies one typed ``GovernedInteractionCase`` from trusted runtime
state.  Browser/client fields never create gate evidence, candidate records or
authority.  Preflight is recomputed immediately before execution and the only
consequential path delegates through ``operator_safety.py`` to the existing
Governed Execution/runtime-consistency boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .canonical import CanonicalRecord
from .canonical_inspection import CurrentSourceAuthorization
from .event_provenance import EventReceipt
from .execution_action_experience import (
    ActionCommitStatus,
    ActionReadiness,
    ExecutionGateInspection,
    GovernedExecutionInspection,
    GovernedExecutionInspectionBlockedState,
    inspect_governed_execution,
)
from .governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLineage,
    GovernedGateKind,
    GovernedGateOutcome,
)
from .identity import Identity
from .operator_safety import (
    execute_operator_canonical_mutation_action,
    prepare_operator_canonical_mutation_action,
)
from .runtime_consistency import (
    ConsequentialOutcome,
    RetrySemantics,
    RuntimeConsistencyState,
)
from .security import ActorContext, OrganizationScope
from .workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
)

CORE_PREFLIGHT_GATES: tuple[GovernedGateKind, ...] = (
    GovernedGateKind.AUTHORIZATION,
    GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
    GovernedGateKind.DATA_GOVERNANCE,
    GovernedGateKind.CONSEQUENTIAL_APPROVAL,
)


class PreflightGateState(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"
    WAITING = "Waiting"
    NOT_REQUIRED = "Not required"


class GovernedInteractionOutcome(str, Enum):
    READY = "Ready"
    WAITING = "Waiting"
    BLOCKED = "Blocked"
    RECONCILIATION_REQUIRED = "Reconciliation required"
    SUCCEEDED = "Succeeded"


@dataclass(frozen=True, slots=True)
class GovernedInteractionCase:
    """Trusted, typed input for one bounded operator interaction.

    ``interaction_id`` is only a transient lookup key.  It is not authority,
    approval, idempotency evidence or canonical identity.
    """

    interaction_id: str
    organization: OrganizationScope
    actor: ActorContext
    source_record: CanonicalRecord
    execution_lineage: GovernedExecutionLineage
    runtime_state: RuntimeConsistencyState
    candidate: CanonicalRecord
    event_receipt: EventReceipt
    source_authorizations: tuple[CurrentSourceAuthorization, ...]
    retry_semantics: RetrySemantics
    retry_token: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.interaction_id, str) or not self.interaction_id.strip():
            raise ValueError("interaction_id must be a non-empty transient identifier")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("interaction Organization must be explicit")
        if not isinstance(self.actor, ActorContext) or self.actor.organization != self.organization:
            raise ValueError("interaction Actor must share the explicit Organization")
        if not isinstance(self.source_record, CanonicalRecord):
            raise ValueError("interaction source must be an exact CanonicalRecord Version")
        if self.source_record.organization != self.organization:
            raise ValueError("interaction source must share Organization scope")
        if not isinstance(self.execution_lineage, GovernedExecutionLineage):
            raise ValueError("interaction requires exact Governed Execution lineage")
        execution = self.execution_lineage.head()
        if execution.organization != self.organization:
            raise ValueError("interaction Execution must share Organization scope")
        if execution.initiating_actor != self.actor:
            raise ValueError("interaction Execution must preserve the attributable initiating Actor")
        if not isinstance(self.runtime_state, RuntimeConsistencyState):
            raise ValueError("interaction requires current RuntimeConsistencyState")
        if self.runtime_state.head.organization != self.organization:
            raise ValueError("runtime target must share Organization scope")
        if self.runtime_state.head.version_id != self.source_record.version_id:
            raise ValueError("interaction source must be the exact current runtime Canonical Head")
        if self.runtime_state.head.subject_id != self.source_record.subject_id:
            raise ValueError("interaction source Subject must match current runtime target")
        if not any(pin.version_id == self.source_record.version_id for pin in execution.material_inputs):
            raise ValueError("Execution must pin the exact source Version as a material input")
        if not isinstance(self.candidate, CanonicalRecord):
            raise ValueError("interaction candidate must be an exact CanonicalRecord")
        if self.candidate.organization != self.organization:
            raise ValueError("interaction candidate must share Organization scope")
        if self.candidate.subject_id != self.source_record.subject_id:
            raise ValueError("candidate must preserve the source Subject Identity")
        if self.candidate.predecessor_version_id != self.source_record.version_id:
            raise ValueError("candidate must declare the exact source Version as predecessor")
        if not isinstance(self.event_receipt, EventReceipt):
            raise ValueError("interaction Event receipt must be typed governed evidence")
        if self.event_receipt.organization != self.organization:
            raise ValueError("interaction Event receipt must share Organization scope")
        if self.event_receipt.execution_subject_id != execution.execution_subject_id:
            raise ValueError("Event receipt must preserve exact Execution Subject")
        if self.event_receipt.execution_version_id != execution.execution_version_id:
            raise ValueError("Event receipt must preserve exact Execution Version")
        if self.candidate.subject_id not in self.event_receipt.related_subject_ids:
            raise ValueError("Event receipt must reference candidate Subject")
        if self.candidate.version_id not in self.event_receipt.related_version_ids:
            raise ValueError("Event receipt must reference candidate exact Version")
        if not isinstance(self.source_authorizations, tuple) or any(
            not isinstance(item, CurrentSourceAuthorization)
            for item in self.source_authorizations
        ):
            raise ValueError("source_authorizations must be typed immutable evidence")
        if not isinstance(self.retry_semantics, RetrySemantics):
            raise ValueError("retry semantics must be explicit")


@dataclass(frozen=True, slots=True)
class PreflightGateView:
    kind: GovernedGateKind
    state: PreflightGateState
    decision_version_id: Identity | None = None
    decision_actor_id: Identity | None = None
    basis_ref: Identity | None = None
    evaluated_execution_version_id: Identity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, GovernedGateKind):
            raise ValueError("preflight gate kind must be explicit")
        if not isinstance(self.state, PreflightGateState):
            raise ValueError("preflight gate state must be explicit")
        evidence = (
            self.decision_version_id,
            self.decision_actor_id,
            self.basis_ref,
            self.evaluated_execution_version_id,
        )
        if self.state in {PreflightGateState.ALLOW, PreflightGateState.DENY}:
            if any(not isinstance(value, Identity) for value in evidence):
                raise ValueError("resolved gate view requires exact decision evidence")
        elif any(value is not None for value in evidence):
            raise ValueError("waiting/not-required gate view must not manufacture evidence")


@dataclass(frozen=True, slots=True)
class GovernedInteractionPreflight:
    outcome: GovernedInteractionOutcome
    status_text: str
    organization: OrganizationScope
    actor: ActorContext
    source_subject_id: Identity
    source_version_id: Identity
    source_semantic_type: str
    source_authority_mode: str
    source_authority_scope: str
    source_provenance_refs: tuple[Identity, ...]
    execution_subject_id: Identity
    execution_version_id: Identity
    workflow_subject_id: Identity
    workflow_version_id: Identity
    product_contract_subject_id: Identity | None
    product_contract_version_id: Identity | None
    gates: tuple[PreflightGateView, ...]
    action_readiness: ActionReadiness
    source_authorization_decision_version_id: Identity
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, GovernedInteractionOutcome):
            raise ValueError("preflight outcome must be explicit")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("preflight requires truthful status text")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("preflight Organization must be explicit")
        if not isinstance(self.actor, ActorContext) or self.actor.organization != self.organization:
            raise ValueError("preflight Actor must preserve Organization scope")
        for value in (
            self.source_subject_id,
            self.source_version_id,
            self.execution_subject_id,
            self.execution_version_id,
            self.workflow_subject_id,
            self.workflow_version_id,
            self.source_authorization_decision_version_id,
        ):
            if not isinstance(value, Identity):
                raise ValueError("preflight must preserve exact governed identities")
        if not isinstance(self.gates, tuple) or len(self.gates) != len(CORE_PREFLIGHT_GATES):
            raise ValueError("preflight must render the four core gate concepts independently")
        if tuple(row.kind for row in self.gates) != CORE_PREFLIGHT_GATES:
            raise ValueError("preflight core gate order/identity must remain explicit")
        if not isinstance(self.action_readiness, ActionReadiness):
            raise ValueError("preflight action readiness must be explicit")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("preflight presentation cannot become authority")


@dataclass(frozen=True, slots=True)
class GovernedInteractionBlocked:
    outcome: GovernedInteractionOutcome
    status_text: str
    governed_content_visible: bool = False
    action_available: bool = False
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if self.outcome is not GovernedInteractionOutcome.BLOCKED:
            raise ValueError("generic blocked state must remain Blocked")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("blocked state requires safe status text")
        if self.governed_content_visible or self.action_available:
            raise ValueError("blocked state must fail closed without protected content")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("blocked presentation cannot become authority")


GovernedInteractionPreflightResult = GovernedInteractionPreflight | GovernedInteractionBlocked


@dataclass(frozen=True, slots=True)
class GovernedInteractionExecutionResult:
    outcome: GovernedInteractionOutcome
    status_text: str
    preflight: GovernedInteractionPreflightResult
    runtime_state: RuntimeConsistencyState
    committed_record_version_id: Identity | None = None
    event_version_id: Identity | None = None
    duplicate: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, GovernedInteractionOutcome):
            raise ValueError("interaction execution outcome must be explicit")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("interaction execution requires status text")
        if not isinstance(self.runtime_state, RuntimeConsistencyState):
            raise ValueError("interaction execution must preserve resulting runtime state")
        if not isinstance(self.duplicate, bool):
            raise ValueError("duplicate state must be explicit")
        if self.outcome is GovernedInteractionOutcome.SUCCEEDED:
            if not isinstance(self.committed_record_version_id, Identity):
                raise ValueError("succeeded interaction must preserve exact result Version")
            if not isinstance(self.event_version_id, Identity):
                raise ValueError("succeeded interaction must preserve exact Event Version")
        elif self.committed_record_version_id is not None or self.event_version_id is not None:
            raise ValueError("non-success interaction must not claim committed identities")


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def _gate_view(kind: GovernedGateKind, rows: tuple[ExecutionGateInspection, ...]) -> PreflightGateView:
    match = next((row for row in rows if row.kind is kind), None)
    if match is None:
        return PreflightGateView(kind=kind, state=PreflightGateState.NOT_REQUIRED)
    if match.outcome is None:
        return PreflightGateView(kind=kind, state=PreflightGateState.WAITING)
    state = (
        PreflightGateState.ALLOW
        if match.outcome is GovernedGateOutcome.ALLOW
        else PreflightGateState.DENY
    )
    return PreflightGateView(
        kind=kind,
        state=state,
        decision_version_id=match.decision_version_id,
        decision_actor_id=match.decision_actor_id,
        basis_ref=match.basis_ref,
        evaluated_execution_version_id=match.evaluated_execution_version_id,
    )


def _outcome_for_inspection(inspection: GovernedExecutionInspection) -> tuple[GovernedInteractionOutcome, str]:
    if any(item.outcome is ConsequentialOutcome.UNCERTAIN for item in inspection.attempts):
        return (
            GovernedInteractionOutcome.RECONCILIATION_REQUIRED,
            "A prior consequential attempt is uncertain. Reconciliation is required before retry.",
        )
    if any(item.outcome is ConsequentialOutcome.SUCCEEDED for item in inspection.attempts):
        return (
            GovernedInteractionOutcome.SUCCEEDED,
            "Governed evidence records a succeeded consequential attempt for this Execution.",
        )
    if inspection.action_readiness is ActionReadiness.AWAITING_REQUIRED_GATES:
        return (
            GovernedInteractionOutcome.WAITING,
            "One or more required gate decisions are unresolved; the action remains waiting.",
        )
    if inspection.action_readiness is ActionReadiness.READY_TO_REQUEST_CANONICAL_COMMIT:
        return (
            GovernedInteractionOutcome.READY,
            "Preflight is ready to assemble a transient governed action intent.",
        )
    return (
        GovernedInteractionOutcome.BLOCKED,
        f"Governed action is blocked: {inspection.action_readiness.value}.",
    )


def build_governed_interaction_preflight(
    workspace: WorkspaceShellState,
    *,
    case: GovernedInteractionCase,
) -> GovernedInteractionPreflightResult:
    """Recompute one exact, non-authoritative preflight from governed evidence."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("UI2 preflight requires an open WorkspaceShellState")
    if not isinstance(case, GovernedInteractionCase):
        raise ValueError("UI2 preflight requires a typed GovernedInteractionCase")
    if workspace.organization != case.organization or workspace.actor != case.actor:
        return GovernedInteractionBlocked(
            outcome=GovernedInteractionOutcome.BLOCKED,
            status_text="Governed interaction is unavailable for the current operator context.",
        )

    execution = case.execution_lineage.head()
    execution_workspace = navigate_workspace(
        workspace,
        destination=WorkspaceDestination.EXECUTIONS,
        reference=ExactVersionNavigationReference(
            workspace.organization,
            execution.execution_subject_id,
            execution.execution_version_id,
        ),
    )
    inspected = inspect_governed_execution(
        execution_workspace,
        lineages=(case.execution_lineage,),
        authorizations=case.source_authorizations,
        runtime_state=case.runtime_state,
    )
    if isinstance(inspected, GovernedExecutionInspectionBlockedState):
        return GovernedInteractionBlocked(
            outcome=GovernedInteractionOutcome.BLOCKED,
            status_text="Governed interaction is unavailable for the current source-access context.",
        )
    if not isinstance(inspected, GovernedExecutionInspection):
        raise ValueError("unexpected Governed Execution inspection result")

    gates = tuple(_gate_view(kind, inspected.gates) for kind in CORE_PREFLIGHT_GATES)
    outcome, status_text = _outcome_for_inspection(inspected)
    contract = inspected.product_contract
    return GovernedInteractionPreflight(
        outcome=outcome,
        status_text=status_text,
        organization=workspace.organization,
        actor=workspace.actor,
        source_subject_id=case.source_record.subject_id,
        source_version_id=case.source_record.version_id,
        source_semantic_type=case.source_record.semantic_type,
        source_authority_mode=case.source_record.authority_mode.value,
        source_authority_scope=case.source_record.authority_scope,
        source_provenance_refs=case.source_record.provenance_refs,
        execution_subject_id=inspected.execution_subject_id,
        execution_version_id=inspected.displayed_execution_version_id,
        workflow_subject_id=inspected.workflow.subject_id,
        workflow_version_id=inspected.workflow.version_id,
        product_contract_subject_id=None if contract is None else contract.subject_id,
        product_contract_version_id=None if contract is None else contract.version_id,
        gates=gates,
        action_readiness=inspected.action_readiness,
        source_authorization_decision_version_id=(
            inspected.source_authorization_decision_version_id
        ),
    )


def execute_governed_interaction(
    workspace: WorkspaceShellState,
    *,
    case: GovernedInteractionCase,
) -> GovernedInteractionExecutionResult:
    """Re-preflight, prepare transient intent, then delegate through R10 safety."""

    preflight = build_governed_interaction_preflight(workspace, case=case)
    if not isinstance(preflight, GovernedInteractionPreflight):
        return GovernedInteractionExecutionResult(
            outcome=GovernedInteractionOutcome.BLOCKED,
            status_text=preflight.status_text,
            preflight=preflight,
            runtime_state=case.runtime_state,
        )
    if preflight.outcome is not GovernedInteractionOutcome.READY:
        return GovernedInteractionExecutionResult(
            outcome=preflight.outcome,
            status_text=preflight.status_text,
            preflight=preflight,
            runtime_state=case.runtime_state,
        )

    execution: GovernedExecutionContext = case.execution_lineage.head()
    # Reconstruct the exact inspected execution state rather than trusting UI state.
    execution_workspace = navigate_workspace(
        workspace,
        destination=WorkspaceDestination.EXECUTIONS,
        reference=ExactVersionNavigationReference(
            workspace.organization,
            execution.execution_subject_id,
            execution.execution_version_id,
        ),
    )
    inspected = inspect_governed_execution(
        execution_workspace,
        lineages=(case.execution_lineage,),
        authorizations=case.source_authorizations,
        runtime_state=case.runtime_state,
    )
    if not isinstance(inspected, GovernedExecutionInspection):
        return GovernedInteractionExecutionResult(
            outcome=GovernedInteractionOutcome.BLOCKED,
            status_text="Governed interaction changed during preflight; re-inspection is required.",
            preflight=preflight,
            runtime_state=case.runtime_state,
        )

    try:
        intent = prepare_operator_canonical_mutation_action(
            workspace=workspace,
            inspection=inspected,
            execution=execution,
            runtime_state=case.runtime_state,
            candidate=case.candidate,
            event_receipt=case.event_receipt,
            retry_semantics=case.retry_semantics,
            retry_token=case.retry_token,
            source_authorizations=case.source_authorizations,
        )
    except PermissionError:
        return GovernedInteractionExecutionResult(
            outcome=GovernedInteractionOutcome.BLOCKED,
            status_text="Governed action could not be prepared from the current exact evidence.",
            preflight=preflight,
            runtime_state=case.runtime_state,
        )

    action = execute_operator_canonical_mutation_action(
        workspace=workspace,
        intent=intent,
        runtime_state=case.runtime_state,
        source_authorizations=case.source_authorizations,
    )
    if action.status in {ActionCommitStatus.COMMITTED, ActionCommitStatus.IDEMPOTENT_DUPLICATE}:
        return GovernedInteractionExecutionResult(
            outcome=GovernedInteractionOutcome.SUCCEEDED,
            status_text=action.status_text,
            preflight=preflight,
            runtime_state=action.state,
            committed_record_version_id=action.committed_record_version_id,
            event_version_id=action.event_version_id,
            duplicate=action.duplicate,
        )
    if action.status is ActionCommitStatus.RECONCILIATION_REQUIRED:
        outcome = GovernedInteractionOutcome.RECONCILIATION_REQUIRED
    else:
        outcome = GovernedInteractionOutcome.BLOCKED
    return GovernedInteractionExecutionResult(
        outcome=outcome,
        status_text=action.status_text,
        preflight=preflight,
        runtime_state=action.state,
    )


def _gate_html(row: PreflightGateView) -> str:
    evidence = row.state.value
    if row.state in {PreflightGateState.ALLOW, PreflightGateState.DENY}:
        assert row.decision_version_id is not None
        assert row.decision_actor_id is not None
        assert row.basis_ref is not None
        assert row.evaluated_execution_version_id is not None
        evidence += (
            f"; decision Version {escape(_identity_text(row.decision_version_id))}"
            f"; decision Actor {escape(_identity_text(row.decision_actor_id))}"
            f"; basis {escape(_identity_text(row.basis_ref))}"
            f"; evaluated Execution Version "
            f"{escape(_identity_text(row.evaluated_execution_version_id))}"
        )
    return (
        "<tr>"
        f"<th scope=\"row\">{escape(row.kind.value)}</th>"
        f"<td>{escape(row.state.value)}</td>"
        f"<td>{evidence}</td>"
        "</tr>"
    )


def render_governed_interaction_preflight_html(
    result: GovernedInteractionPreflightResult,
    *,
    interaction_id: str | None = None,
    csrf_token: str | None = None,
) -> str:
    """Render inert evidence plus an optional transient request form.

    Presence of a form is presentation only.  The server must reauthorize and
    recompute preflight before invoking ``execute_governed_interaction``.
    """

    if isinstance(result, GovernedInteractionBlocked):
        return (
            '<section data-interaction-state="blocked">'
            "<h2>Governed interaction unavailable</h2>"
            f'<p role="alert">{escape(result.status_text)}</p>'
            "<p>No protected Subject, Version, gate evidence or action is exposed.</p>"
            "</section>"
        )
    if not isinstance(result, GovernedInteractionPreflight):
        raise ValueError("result must be a governed interaction preflight result")

    provenance = "".join(
        f"<li>{escape(_identity_text(value))}</li>"
        for value in result.source_provenance_refs
    )
    contract = (
        "<p>Product Contract: none declared in this Execution.</p>"
        if result.product_contract_version_id is None
        else (
            "<p>Product Contract Subject: "
            f"{escape(_identity_text(result.product_contract_subject_id))}<br>"
            "Exact Product Contract Version: "
            f"{escape(_identity_text(result.product_contract_version_id))}</p>"
        )
    )
    form = ""
    if (
        result.outcome is GovernedInteractionOutcome.READY
        and isinstance(interaction_id, str)
        and interaction_id
        and isinstance(csrf_token, str)
        and csrf_token
    ):
        form = (
            '<form method="post" action="/interaction/execute" data-authority="none">'
            f'<input type="hidden" name="interaction_id" value="{escape(interaction_id, quote=True)}">'
            f'<input type="hidden" name="csrf" value="{escape(csrf_token, quote=True)}">'
            '<button type="submit">Request governed action</button>'
            "</form>"
            "<p>Button state is not a security boundary. Authorization and governed "
            "evidence are rechecked on submission.</p>"
        )
    else:
        form = "<p>No governed action request is currently available.</p>"

    return (
        f'<section data-interaction-state="{escape(result.outcome.value.lower().replace(" ", "-"))}" '
        'data-presentation-authority="non-authoritative">'
        "<h2>Governed interaction preflight</h2>"
        f"<p><strong>{escape(result.status_text)}</strong></p>"
        "<h3>Exact source</h3>"
        f"<p>Subject: {escape(_identity_text(result.source_subject_id))}<br>"
        f"Exact Version: {escape(_identity_text(result.source_version_id))}<br>"
        f"Semantic type: {escape(result.source_semantic_type)}<br>"
        f"Authority: {escape(result.source_authority_mode)} / "
        f"{escape(result.source_authority_scope)}</p>"
        "<h4>Provenance</h4><ul>"
        f"{provenance}</ul>"
        "<h3>Related Governed Execution</h3>"
        f"<p>Execution Subject: {escape(_identity_text(result.execution_subject_id))}<br>"
        f"Exact Execution Version: {escape(_identity_text(result.execution_version_id))}<br>"
        f"Workflow Subject: {escape(_identity_text(result.workflow_subject_id))}<br>"
        f"Exact Workflow Version: {escape(_identity_text(result.workflow_version_id))}</p>"
        f"{contract}"
        "<h3>Independent preflight gates</h3>"
        "<p>Authorization, Organizational Authority, Data Governance and "
        "Consequential Approval remain separate. Technical access does not satisfy them.</p>"
        "<table><thead><tr><th>Gate</th><th>State</th><th>Exact evidence</th></tr></thead><tbody>"
        + "".join(_gate_html(row) for row in result.gates)
        + "</tbody></table>"
        "<h3>Action readiness</h3>"
        f"<p>{escape(result.action_readiness.value)}</p>"
        f"{form}"
        '<p data-authority-note="true">This preflight is non-authoritative presentation. '
        "The transient intent is not approval and only the existing Governed Execution "
        "runtime path may commit a consequential effect.</p>"
        "</section>"
    )


def render_governed_interaction_result_html(result: GovernedInteractionExecutionResult) -> str:
    if not isinstance(result, GovernedInteractionExecutionResult):
        raise ValueError("result must be GovernedInteractionExecutionResult")
    exact = ""
    if result.outcome is GovernedInteractionOutcome.SUCCEEDED:
        assert result.committed_record_version_id is not None
        assert result.event_version_id is not None
        exact = (
            f"<p>Committed exact Version: "
            f"{escape(_identity_text(result.committed_record_version_id))}<br>"
            f"Evidence Event Version: {escape(_identity_text(result.event_version_id))}<br>"
            f"Idempotent duplicate: {'yes' if result.duplicate else 'no'}</p>"
        )
    return (
        f'<section data-interaction-result="{escape(result.outcome.value.lower().replace(" ", "-"))}">'
        "<h2>Governed interaction result</h2>"
        f'<p role="status"><strong>{escape(result.outcome.value)}</strong>: '
        f"{escape(result.status_text)}</p>"
        f"{exact}"
        "<p>Outcome is rendered from governed runtime evidence; the UI does not project "
        "optimistic success.</p>"
        "</section>"
    )
