"""P4.05 — bounded Governed Execution, gate and approval/action experience.

This module is an internal Workspace / Operator Experience adapter over the
existing RFC-0005 Governed Execution and P2.06 runtime-consistency semantic
owners.  It is deliberately not an authorization engine, decision-authority
policy, workflow engine, mutation store, public API/SDK, route/wire contract,
frontend framework, Product Contract validator or canonical-state owner.

The surface keeps read access distinct from action authority, keeps action
intent distinct from committed canonical mutation, exposes exact relied-upon
versions and separate gate evidence, and delegates the only exercised
consequential commit to ``runtime_consistency.commit_canonical_mutation``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .canonical import CanonicalRecord
from .canonical_inspection import CurrentSourceAuthorization
from .event_provenance import EventReceipt
from .execution import GovernedVersionPin
from .governed_execution import (
    ConsequentialOperationNotAdmittedError,
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedExecutionLineage,
    GovernedGateDecision,
    GovernedGateKind,
    GovernedGateOutcome,
)
from .identity import Identity
from .runtime_consistency import (
    CanonicalCommitResult,
    CanonicalSuccessorConflictError,
    ConsequentialAttempt,
    ConsequentialOutcome,
    DuplicateEventCommitConflictError,
    IdempotencyKeyConflictError,
    ReconciliationRequiredError,
    RetrySemantics,
    RuntimeConsistencyState,
    StaleCanonicalHeadError,
    StaleExecutionInputError,
    commit_canonical_mutation,
)
from .security import ActorContext, OrganizationScope
from .workflow import OperationSideEffectClass
from .workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceShellState,
)


class ExecutionInspectionBlockCode(str, Enum):
    REFERENCE_REQUIRED = "reference-required"
    ACCESS_DENIED = "access-denied"
    SOURCE_UNAVAILABLE = "source-unavailable"
    SOURCE_AMBIGUOUS = "source-ambiguous"
    VERSION_UNAVAILABLE = "version-unavailable"
    EXECUTION_INCONSISTENT = "execution-inconsistent"


class ExecutionReferenceBasis(str, Enum):
    EXECUTION_HEAD = "Execution Head"
    EXACT_EXECUTION_VERSION = "Exact Execution Version"


class ActionReadiness(str, Enum):
    READY_TO_REQUEST_CANONICAL_COMMIT = "Ready to request governed canonical commit"
    AWAITING_REQUIRED_GATES = "Awaiting required gate decisions"
    GATE_DENIED = "Blocked by denied required gate"
    EXECUTION_STATE_BLOCKED = "Execution state does not admit consequential action"
    HISTORICAL_READ_ONLY = "Historical execution version is inspection-only"
    ACTOR_CONTEXT_BLOCKED = "Current operator is not the attributable execution actor"
    NON_CANONICAL_ACTION = "Operation is inspectable but canonical commit is not its side effect"


class ActionCommitStatus(str, Enum):
    COMMITTED = "Committed through governed runtime"
    IDEMPOTENT_DUPLICATE = "Already committed; duplicate effect suppressed"
    STALE_OR_CONFLICT = "Blocked by stale state or immutable conflict"
    IDEMPOTENCY_CONFLICT = "Blocked by idempotency conflict"
    RECONCILIATION_REQUIRED = "Blocked pending reconciliation of uncertain outcome"
    NOT_ADMITTED = "Blocked because Governed Execution does not admit the effect"


@dataclass(frozen=True, slots=True)
class ExecutionGateInspection:
    kind: GovernedGateKind
    required: bool
    outcome: GovernedGateOutcome | None
    decision_version_id: Identity | None
    decision_actor_id: Identity | None
    basis_ref: Identity | None
    evaluated_execution_version_id: Identity | None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, GovernedGateKind):
            raise ValueError("gate inspection kind must be explicit")
        if self.required is not True:
            raise ValueError("P4.05 gate rows represent explicitly required gates only")
        if self.outcome is None:
            if any(
                item is not None
                for item in (
                    self.decision_version_id,
                    self.decision_actor_id,
                    self.basis_ref,
                    self.evaluated_execution_version_id,
                )
            ):
                raise ValueError("unresolved gate must not manufacture decision evidence")
            return
        if not isinstance(self.outcome, GovernedGateOutcome):
            raise ValueError("resolved gate outcome must be explicit")
        for label, item in (
            ("decision_version_id", self.decision_version_id),
            ("decision_actor_id", self.decision_actor_id),
            ("basis_ref", self.basis_ref),
            ("evaluated_execution_version_id", self.evaluated_execution_version_id),
        ):
            if not isinstance(item, Identity):
                raise ValueError(f"resolved gate {label} must be an exact Identity")


@dataclass(frozen=True, slots=True)
class ConsequentialAttemptInspection:
    execution_version_id: Identity
    side_effect_class: OperationSideEffectClass
    retry_semantics: RetrySemantics
    retry_token_present: bool
    outcome: ConsequentialOutcome
    result_version_id: Identity | None
    event_version_id: Identity | None
    reconciliation_required: bool

    def __post_init__(self) -> None:
        if not isinstance(self.execution_version_id, Identity):
            raise ValueError("attempt inspection requires exact Execution Version Identity")
        if not isinstance(self.side_effect_class, OperationSideEffectClass):
            raise ValueError("attempt inspection side effect must be explicit")
        if not isinstance(self.retry_semantics, RetrySemantics):
            raise ValueError("attempt inspection retry semantics must be explicit")
        if not isinstance(self.retry_token_present, bool):
            raise ValueError("attempt inspection retry-token presence must be explicit")
        if not isinstance(self.outcome, ConsequentialOutcome):
            raise ValueError("attempt inspection outcome must be explicit")
        if self.reconciliation_required != (self.outcome is ConsequentialOutcome.UNCERTAIN):
            raise ValueError("reconciliation requirement must reflect explicit uncertain outcome")


@dataclass(frozen=True, slots=True)
class GovernedExecutionInspection:
    organization: OrganizationScope
    actor: ActorContext
    execution_subject_id: Identity
    displayed_execution_version_id: Identity
    head_execution_version_id: Identity
    reference_basis: ExecutionReferenceBasis
    lifecycle: GovernedExecutionLifecycle
    operation_name: str
    operation_side_effects: tuple[OperationSideEffectClass, ...]
    workflow: GovernedVersionPin
    material_inputs: tuple[GovernedVersionPin, ...]
    product_contract: GovernedVersionPin | None
    gates: tuple[ExecutionGateInspection, ...]
    unresolved_gates: tuple[GovernedGateKind, ...]
    denied_gates: tuple[GovernedGateKind, ...]
    attempts: tuple[ConsequentialAttemptInspection, ...]
    action_readiness: ActionReadiness
    source_authorization_decision_version_id: Identity
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("execution inspection Organization must be explicit")
        if not isinstance(self.actor, ActorContext) or self.actor.organization != self.organization:
            raise ValueError("execution inspection Actor must share Organization scope")
        for item in (
            self.execution_subject_id,
            self.displayed_execution_version_id,
            self.head_execution_version_id,
            self.source_authorization_decision_version_id,
        ):
            if not isinstance(item, Identity):
                raise ValueError("execution inspection identities must be explicit")
        if not isinstance(self.reference_basis, ExecutionReferenceBasis):
            raise ValueError("execution inspection reference basis must be explicit")
        if not isinstance(self.lifecycle, GovernedExecutionLifecycle):
            raise ValueError("execution inspection lifecycle must be explicit")
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ValueError("execution inspection must preserve exact Workflow version")
        if not isinstance(self.material_inputs, tuple) or not self.material_inputs:
            raise ValueError("execution inspection must preserve exact material inputs")
        if any(not isinstance(item, GovernedVersionPin) for item in self.material_inputs):
            raise ValueError("material inputs must be exact governed version pins")
        if self.product_contract is not None and not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("Product Contract must remain an exact governed version pin")
        if not isinstance(self.gates, tuple) or any(
            not isinstance(item, ExecutionGateInspection) for item in self.gates
        ):
            raise ValueError("gate inspection must be an immutable typed tuple")
        if not isinstance(self.attempts, tuple) or any(
            not isinstance(item, ConsequentialAttemptInspection) for item in self.attempts
        ):
            raise ValueError("attempt inspection must be an immutable typed tuple")
        if not isinstance(self.action_readiness, ActionReadiness):
            raise ValueError("action readiness must be explicit")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("P4.05 presentation cannot become canonical authority")


@dataclass(frozen=True, slots=True)
class GovernedExecutionInspectionBlockedState:
    code: ExecutionInspectionBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False
    action_available: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, ExecutionInspectionBlockCode):
            raise ValueError("blocked execution inspection requires explicit code")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("blocked execution inspection requires textual meaning")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("blocked execution presentation cannot become authority")
        if self.governed_content_visible or self.action_available:
            raise ValueError("blocked execution inspection must fail closed")


GovernedExecutionInspectionResult = GovernedExecutionInspection | GovernedExecutionInspectionBlockedState


@dataclass(frozen=True, slots=True)
class CanonicalMutationActionIntent:
    """Transient request for one exact already-governed canonical mutation.

    The intent is not approval and is not canonical state.  It binds an exact
    admitted Execution Context, current expected Canonical Head, immutable
    candidate and Event receipt so execution can be delegated without the
    presentation layer implementing a second mutation path.
    """

    organization: OrganizationScope
    request_actor: ActorContext
    execution: GovernedExecutionContext
    expected_head_version_id: Identity
    candidate: CanonicalRecord
    event_receipt: EventReceipt
    retry_semantics: RetrySemantics
    retry_token: str | None
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    committed: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("action intent Organization must be explicit")
        if not isinstance(self.request_actor, ActorContext) or self.request_actor.organization != self.organization:
            raise ValueError("action intent Actor must share Organization scope")
        if not isinstance(self.execution, GovernedExecutionContext) or self.execution.organization != self.organization:
            raise ValueError("action intent requires exact governed Execution Context")
        if self.request_actor != self.execution.initiating_actor:
            raise ValueError(
                "bounded P4.05 action adapter only invokes an execution for its attributable initiating Actor"
            )
        if not isinstance(self.expected_head_version_id, Identity):
            raise ValueError("action intent expected Canonical Head must be exact")
        if not isinstance(self.candidate, CanonicalRecord) or self.candidate.organization != self.organization:
            raise ValueError("action intent candidate must be an Organization-scoped Canonical Record")
        if not isinstance(self.event_receipt, EventReceipt) or self.event_receipt.organization != self.organization:
            raise ValueError("action intent Event receipt must share Organization scope")
        if not isinstance(self.retry_semantics, RetrySemantics):
            raise ValueError("action intent retry semantics must be explicit")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE or self.committed:
            raise ValueError("action intent remains transient/non-authoritative until runtime commit")
        if self.candidate.predecessor_version_id != self.expected_head_version_id:
            raise ValueError("candidate must declare the exact expected Canonical Head as predecessor")
        if self.event_receipt.execution_subject_id != self.execution.execution_subject_id:
            raise ValueError("Event receipt must reference the exact action Execution Identity")
        if self.event_receipt.execution_version_id != self.execution.execution_version_id:
            raise ValueError("Event receipt must reference the exact action Execution Version")
        if self.candidate.subject_id not in self.event_receipt.related_subject_ids:
            raise ValueError("Event receipt must preserve the candidate Subject Identity")
        if self.candidate.version_id not in self.event_receipt.related_version_ids:
            raise ValueError("Event receipt must preserve the candidate exact Version Identity")


@dataclass(frozen=True, slots=True)
class CanonicalMutationActionResult:
    status: ActionCommitStatus
    status_text: str
    state: RuntimeConsistencyState
    committed_record_version_id: Identity | None = None
    event_version_id: Identity | None = None
    duplicate: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.status, ActionCommitStatus):
            raise ValueError("action result status must be explicit")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("action result requires textual meaning")
        if not isinstance(self.state, RuntimeConsistencyState):
            raise ValueError("action result must preserve current runtime state")
        if not isinstance(self.duplicate, bool):
            raise ValueError("action result duplicate state must be explicit")
        success = self.status in {
            ActionCommitStatus.COMMITTED,
            ActionCommitStatus.IDEMPOTENT_DUPLICATE,
        }
        if success:
            if not isinstance(self.committed_record_version_id, Identity) or not isinstance(
                self.event_version_id, Identity
            ):
                raise ValueError("successful action result requires exact result and Event versions")
        elif self.committed_record_version_id is not None or self.event_version_id is not None:
            raise ValueError("blocked action result must not claim committed governed versions")


def _represented_id(actor: ActorContext) -> Identity | None:
    represented = actor.represented_principal
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
        and decision.represented_principal_id == _represented_id(state.actor)
        and decision.resource_subject_id == resource_subject_id
    )
    if len(matches) != 1 or matches[0].allowed is not True:
        return None
    return matches[0]


def _blocked(
    code: ExecutionInspectionBlockCode,
    text: str,
) -> GovernedExecutionInspectionBlockedState:
    return GovernedExecutionInspectionBlockedState(code=code, status_text=text)


def _source_lineage(
    *,
    lineages: tuple[GovernedExecutionLineage, ...],
    organization: OrganizationScope,
    execution_subject_id: Identity,
) -> GovernedExecutionLineage | None:
    if not isinstance(lineages, tuple) or any(
        not isinstance(item, GovernedExecutionLineage) for item in lineages
    ):
        return None
    matches = tuple(
        lineage
        for lineage in lineages
        if lineage.execution_subject_id == execution_subject_id
        and lineage.versions[0].organization == organization
    )
    if len(matches) != 1:
        return None
    return matches[0]


def _gate_rows(execution: GovernedExecutionContext) -> tuple[ExecutionGateInspection, ...]:
    decisions = {decision.kind: decision for decision in execution.gate_decisions}
    rows: list[ExecutionGateInspection] = []
    for kind in execution.required_gates:
        decision = decisions.get(kind)
        if decision is None:
            rows.append(
                ExecutionGateInspection(
                    kind=kind,
                    required=True,
                    outcome=None,
                    decision_version_id=None,
                    decision_actor_id=None,
                    basis_ref=None,
                    evaluated_execution_version_id=None,
                )
            )
            continue
        rows.append(
            ExecutionGateInspection(
                kind=kind,
                required=True,
                outcome=decision.outcome,
                decision_version_id=decision.record.version_id,
                decision_actor_id=decision.record.creation_actor.actual_principal.principal_id,
                basis_ref=decision.basis_ref,
                evaluated_execution_version_id=decision.evaluated_execution_version_id,
            )
        )
    return tuple(rows)


def _attempt_rows(
    execution_subject_id: Identity,
    runtime_state: RuntimeConsistencyState | None,
) -> tuple[ConsequentialAttemptInspection, ...]:
    if runtime_state is None:
        return ()
    if not isinstance(runtime_state, RuntimeConsistencyState):
        raise ValueError("runtime_state must be RuntimeConsistencyState when supplied")
    relevant = tuple(
        item for item in runtime_state.attempts if item.execution_subject_id == execution_subject_id
    )
    return tuple(
        ConsequentialAttemptInspection(
            execution_version_id=item.execution_version_id,
            side_effect_class=item.side_effect_class,
            retry_semantics=item.retry_semantics,
            retry_token_present=item.retry_token is not None,
            outcome=item.outcome,
            result_version_id=item.result_version_id,
            event_version_id=item.event_version_id,
            reconciliation_required=item.outcome is ConsequentialOutcome.UNCERTAIN,
        )
        for item in relevant
    )


def _readiness(
    *,
    state: WorkspaceShellState,
    execution: GovernedExecutionContext,
    is_head: bool,
) -> ActionReadiness:
    if not is_head:
        return ActionReadiness.HISTORICAL_READ_ONLY
    if state.actor != execution.initiating_actor:
        # This is intentionally a bounded adapter safety rule, not a general
        # decision-authority policy. It prevents the UI from letting a different
        # read-authorized Actor invoke an execution whose action actor semantics
        # have not been separately governed in this reference slice.
        return ActionReadiness.ACTOR_CONTEXT_BLOCKED
    denied = tuple(
        decision.kind
        for decision in execution.gate_decisions
        if decision.kind in execution.required_gates
        and decision.outcome is GovernedGateOutcome.DENY
    )
    if denied:
        return ActionReadiness.GATE_DENIED
    if execution.unresolved_gates:
        return ActionReadiness.AWAITING_REQUIRED_GATES
    if execution.lifecycle not in {
        GovernedExecutionLifecycle.READY,
        GovernedExecutionLifecycle.RUNNING,
    }:
        return ActionReadiness.EXECUTION_STATE_BLOCKED
    if OperationSideEffectClass.CANONICAL_MUTATION not in execution.operation_side_effects:
        return ActionReadiness.NON_CANONICAL_ACTION
    return ActionReadiness.READY_TO_REQUEST_CANONICAL_COMMIT


def inspect_governed_execution(
    state: WorkspaceShellState,
    *,
    lineages: tuple[GovernedExecutionLineage, ...],
    authorizations: tuple[CurrentSourceAuthorization, ...],
    runtime_state: RuntimeConsistencyState | None = None,
) -> GovernedExecutionInspectionResult:
    """Resolve one authorized execution view without granting action authority.

    Source authorization is consumed before source/exact-Version existence is
    disclosed.  That decision allows inspection only; gate evidence and the
    exact Governed Execution state independently determine action readiness.
    """

    if not isinstance(state, WorkspaceShellState):
        raise ValueError("P4.05 inspection requires an open WorkspaceShellState")
    reference = state.current_reference
    if not isinstance(reference, (SubjectNavigationReference, ExactVersionNavigationReference)):
        return _blocked(
            ExecutionInspectionBlockCode.REFERENCE_REQUIRED,
            "An explicit Execution reference is required before governed execution can be inspected.",
        )

    requested_subject_id = reference.subject_id
    authorization = _current_authorization(
        state=state,
        resource_subject_id=requested_subject_id,
        authorizations=authorizations,
    )
    if authorization is None:
        return _blocked(
            ExecutionInspectionBlockCode.ACCESS_DENIED,
            "Governed Execution is unavailable for the current source-access context.",
        )

    lineage = _source_lineage(
        lineages=lineages,
        organization=state.organization,
        execution_subject_id=requested_subject_id,
    )
    if lineage is None:
        # Keep ambiguity and absence indistinguishable on this protected surface.
        return _blocked(
            ExecutionInspectionBlockCode.SOURCE_UNAVAILABLE,
            "Governed Execution source is unavailable for this reference.",
        )

    head = lineage.head()
    reference_basis = ExecutionReferenceBasis.EXECUTION_HEAD
    displayed = head
    if isinstance(reference, ExactVersionNavigationReference):
        try:
            displayed = lineage.exact(reference.version_id)
        except KeyError:
            return _blocked(
                ExecutionInspectionBlockCode.VERSION_UNAVAILABLE,
                "The requested exact Execution Version is unavailable in the authorized source.",
            )
        reference_basis = ExecutionReferenceBasis.EXACT_EXECUTION_VERSION

    if runtime_state is not None:
        try:
            attempts = _attempt_rows(requested_subject_id, runtime_state)
        except ValueError:
            return _blocked(
                ExecutionInspectionBlockCode.EXECUTION_INCONSISTENT,
                "Execution runtime evidence cannot be interpreted consistently.",
            )
        if runtime_state.head.organization != state.organization:
            return _blocked(
                ExecutionInspectionBlockCode.EXECUTION_INCONSISTENT,
                "Execution runtime evidence cannot be interpreted consistently.",
            )
    else:
        attempts = ()

    gates = _gate_rows(displayed)
    unresolved = tuple(row.kind for row in gates if row.outcome is None)
    denied = tuple(row.kind for row in gates if row.outcome is GovernedGateOutcome.DENY)
    return GovernedExecutionInspection(
        organization=state.organization,
        actor=state.actor,
        execution_subject_id=displayed.execution_subject_id,
        displayed_execution_version_id=displayed.execution_version_id,
        head_execution_version_id=head.execution_version_id,
        reference_basis=reference_basis,
        lifecycle=displayed.lifecycle,
        operation_name=displayed.operation_name,
        operation_side_effects=displayed.operation_side_effects,
        workflow=displayed.workflow,
        material_inputs=displayed.material_inputs,
        product_contract=displayed.product_contract,
        gates=gates,
        unresolved_gates=unresolved,
        denied_gates=denied,
        attempts=attempts,
        action_readiness=_readiness(
            state=state,
            execution=displayed,
            is_head=displayed.execution_version_id == head.execution_version_id,
        ),
        source_authorization_decision_version_id=authorization.decision_version_id,
    )


def prepare_canonical_mutation_action(
    *,
    workspace: WorkspaceShellState,
    inspection: GovernedExecutionInspection,
    execution: GovernedExecutionContext,
    runtime_state: RuntimeConsistencyState,
    candidate: CanonicalRecord,
    event_receipt: EventReceipt,
    retry_semantics: RetrySemantics,
    retry_token: str | None = None,
) -> CanonicalMutationActionIntent:
    """Create transient intent only; this function never mutates canonical state."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("action preparation requires an open WorkspaceShellState")
    if not isinstance(inspection, GovernedExecutionInspection):
        raise PermissionError("action preparation requires an authorized execution inspection")
    if inspection.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
        raise PermissionError("presentation authority cannot authorize a consequential action")
    if inspection.organization != workspace.organization or inspection.actor != workspace.actor:
        raise PermissionError("action inspection must belong to the current Workspace context")
    if inspection.action_readiness is not ActionReadiness.READY_TO_REQUEST_CANONICAL_COMMIT:
        raise PermissionError(f"governed action is not ready: {inspection.action_readiness.value}")
    if not isinstance(execution, GovernedExecutionContext):
        raise ValueError("action preparation requires exact governed Execution Context")
    if execution.execution_version_id != inspection.displayed_execution_version_id:
        raise PermissionError("action must bind the exact displayed admitted Execution Version")
    if execution.execution_version_id != inspection.head_execution_version_id:
        raise PermissionError("historical Execution Version cannot request a consequential action")
    if execution.execution_subject_id != inspection.execution_subject_id:
        raise PermissionError("action Execution Identity does not match authorized inspection")
    if workspace.actor != execution.initiating_actor:
        raise PermissionError("current Actor cannot invoke this bounded execution action")
    if not isinstance(runtime_state, RuntimeConsistencyState):
        raise ValueError("action preparation requires current RuntimeConsistencyState")
    if runtime_state.head.organization != workspace.organization:
        raise PermissionError("runtime canonical target is outside current Organization scope")

    return CanonicalMutationActionIntent(
        organization=workspace.organization,
        request_actor=workspace.actor,
        execution=execution,
        expected_head_version_id=runtime_state.head.version_id,
        candidate=candidate,
        event_receipt=event_receipt,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
    )


def execute_canonical_mutation_action(
    *,
    workspace: WorkspaceShellState,
    intent: CanonicalMutationActionIntent,
    runtime_state: RuntimeConsistencyState,
) -> CanonicalMutationActionResult:
    """Delegate one exact action to the existing governed runtime mutation path."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("action execution requires an open WorkspaceShellState")
    if not isinstance(intent, CanonicalMutationActionIntent):
        raise ValueError("action execution requires a prepared CanonicalMutationActionIntent")
    if workspace.organization != intent.organization or workspace.actor != intent.request_actor:
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.NOT_ADMITTED,
            status_text="Current Workspace Actor/Organization no longer matches the prepared action intent.",
            state=runtime_state,
        )
    if not isinstance(runtime_state, RuntimeConsistencyState):
        raise ValueError("action execution requires current RuntimeConsistencyState")

    try:
        result: CanonicalCommitResult = commit_canonical_mutation(
            state=runtime_state,
            execution=intent.execution,
            expected_head_version_id=intent.expected_head_version_id,
            candidate=intent.candidate,
            event_receipt=intent.event_receipt,
            retry_semantics=intent.retry_semantics,
            retry_token=intent.retry_token,
        )
    except (StaleCanonicalHeadError, StaleExecutionInputError, CanonicalSuccessorConflictError, DuplicateEventCommitConflictError) as exc:
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.STALE_OR_CONFLICT,
            status_text=f"Governed commit was blocked without mutation: {exc}",
            state=runtime_state,
        )
    except IdempotencyKeyConflictError as exc:
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.IDEMPOTENCY_CONFLICT,
            status_text=f"Governed commit was blocked without mutation: {exc}",
            state=runtime_state,
        )
    except ReconciliationRequiredError as exc:
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.RECONCILIATION_REQUIRED,
            status_text=f"Governed commit requires reconciliation before retry: {exc}",
            state=runtime_state,
        )
    except ConsequentialOperationNotAdmittedError as exc:
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.NOT_ADMITTED,
            status_text=f"Governed commit was not admitted: {exc}",
            state=runtime_state,
        )

    status = (
        ActionCommitStatus.IDEMPOTENT_DUPLICATE
        if result.duplicate
        else ActionCommitStatus.COMMITTED
    )
    text = (
        "The exact governed effect was already committed; retry was recognized and no duplicate effect was created."
        if result.duplicate
        else "The exact canonical mutation was committed by the existing Governed Execution runtime path."
    )
    return CanonicalMutationActionResult(
        status=status,
        status_text=text,
        state=result.state,
        committed_record_version_id=result.record.version_id,
        event_version_id=result.event.version_id,
        duplicate=result.duplicate,
    )


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def _pin_html(label: str, pin: GovernedVersionPin) -> str:
    lifecycle = "" if pin.lifecycle_status is None else f"; lifecycle {escape(pin.lifecycle_status)}"
    return (
        f"<li><strong>{escape(label)}</strong>: Subject {escape(_identity_text(pin.subject_id))}; "
        f"exact Version {escape(_identity_text(pin.version_id))}; "
        f"type {escape(pin.semantic_type)}{lifecycle}</li>"
    )


def render_governed_execution_html(result: GovernedExecutionInspectionResult) -> str:
    """Render inert accessible HTML; no UI role/title or button becomes authority."""

    if isinstance(result, GovernedExecutionInspectionBlockedState):
        return (
            '<main data-execution-state="blocked">'
            '<h1>Governed Execution unavailable</h1>'
            f'<p role="alert">{escape(result.status_text)}</p>'
            '<p>No governed execution content or action is exposed.</p>'
            '</main>'
        )
    if not isinstance(result, GovernedExecutionInspection):
        raise ValueError("result must be a P4.05 execution inspection result")

    product_contract = (
        "<p>Product Contract: none applicable in the supplied execution evidence.</p>"
        if result.product_contract is None
        else "<ul>" + _pin_html("Product Contract", result.product_contract) + "</ul>"
    )
    material = "<ul>" + "".join(
        _pin_html("Material input", pin) for pin in result.material_inputs
    ) + "</ul>"

    gate_rows: list[str] = []
    for gate in result.gates:
        if gate.outcome is None:
            evidence = "Unresolved — no exact gate decision evidence supplied"
        else:
            evidence = (
                f"{escape(gate.outcome.value)}; decision Version "
                f"{escape(_identity_text(gate.decision_version_id))}; decision Actor "
                f"{escape(_identity_text(gate.decision_actor_id))}; basis "
                f"{escape(_identity_text(gate.basis_ref))}; evaluated Execution Version "
                f"{escape(_identity_text(gate.evaluated_execution_version_id))}"
            )
        gate_rows.append(
            "<tr>"
            f"<th scope=\"row\">{escape(gate.kind.value)}</th>"
            "<td>Required</td>"
            f"<td>{evidence}</td>"
            "</tr>"
        )

    attempt_rows: list[str] = []
    for attempt in result.attempts:
        attempt_rows.append(
            "<tr>"
            f"<td>{escape(_identity_text(attempt.execution_version_id))}</td>"
            f"<td>{escape(attempt.side_effect_class.value)}</td>"
            f"<td>{escape(attempt.retry_semantics.value)}</td>"
            f"<td>{'Yes' if attempt.retry_token_present else 'No'}</td>"
            f"<td>{escape(attempt.outcome.value)}</td>"
            f"<td>{'Required' if attempt.reconciliation_required else 'No'}</td>"
            "</tr>"
        )
    attempts = (
        "<p>No consequential attempt evidence is supplied for this Execution.</p>"
        if not attempt_rows
        else (
            '<table><caption>Retry, idempotency and uncertainty evidence</caption>'
            '<thead><tr><th>Execution Version</th><th>Effect</th><th>Retry semantics</th>'
            '<th>Duplicate-protection token present</th><th>Outcome</th><th>Reconciliation</th>'
            '</tr></thead><tbody>' + "".join(attempt_rows) + "</tbody></table>"
        )
    )

    side_effects = ", ".join(item.value for item in result.operation_side_effects)
    return (
        '<main data-execution-state="visible" data-presentation-authority="non-authoritative">'
        '<h1>Governed Execution</h1>'
        f'<p>Execution Subject: {escape(_identity_text(result.execution_subject_id))}</p>'
        f'<p>Displayed exact Execution Version: {escape(_identity_text(result.displayed_execution_version_id))}</p>'
        f'<p>Execution Head: {escape(_identity_text(result.head_execution_version_id))}</p>'
        f'<p>Reference basis: {escape(result.reference_basis.value)}</p>'
        f'<p>Lifecycle: {escape(result.lifecycle.value)}</p>'
        f'<p>Operation: {escape(result.operation_name)}; side effects: {escape(side_effects)}</p>'
        '<section><h2>Exact governed reliance</h2><ul>'
        + _pin_html("Workflow", result.workflow)
        + '</ul><h3>Material inputs</h3>'
        + material
        + '<h3>Product Contract</h3>'
        + product_contract
        + '</section>'
        '<section><h2>Required gates</h2>'
        '<p>Authorization, Organizational Authority and Consequential Approval are separate decisions. '
        'A UI title, role label, source-access permission or another passed gate does not satisfy them.</p>'
        '<table><thead><tr><th>Gate</th><th>Requirement</th><th>Exact decision evidence</th></tr></thead><tbody>'
        + "".join(gate_rows)
        + '</tbody></table></section>'
        '<section><h2>Action readiness</h2>'
        f'<p>{escape(result.action_readiness.value)}</p>'
        '<p>Action intent is transient and distinct from committed canonical mutation. '
        'Only the existing Governed Execution runtime mutation path may commit the effect.</p>'
        '</section>'
        '<section><h2>Retry / conflict / uncertainty</h2>'
        + attempts
        + '<p>Uncertain consequential outcomes require reconciliation; blind retry is not presented as safe.</p>'
        '</section>'
        '<p data-authority-note="true">This workspace view is non-authoritative presentation. '
        'Inspection access is not Authorization, Organizational Authority or approval.</p>'
        '</main>'
    )
