"""P2.04 — reusable Governed Execution lifecycle and gate orchestration runtime.

This module generalizes the Phase 1 execution/gate proof as bounded, domain-neutral,
in-memory runtime semantics.  It deliberately does not select a workflow engine,
persistence layer, IAM/policy provider, Event/provenance backend, transaction model,
public API/SDK, or Product Contract schema/validator.

The runtime preserves RFC-0005's important separations:

* Workflow and Execution Context are distinct governed subjects;
* governance-significant execution transitions create immutable Canonical Record
  versions under one stable Execution Identity;
* exact Workflow, material-input and (when supplied) Product Contract versions are
  pinned before consequential reliance;
* actor assurance, authorization, Organizational Authority, data governance,
  validation and consequential approval remain distinct gate concepts;
* required gates fail closed when missing or denied;
* terminal execution history is sealed;
* admission for a consequential side effect is explicit and cannot be inferred from
  technical ability, an Identity, a relationship, or Product Contract possession.

P2.05 remains responsible for complete Event/provenance/reconstruction behavior and
P2.06 remains responsible for durable consistency, idempotency and concurrency.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .canonical_lineage import CanonicalLineage
from .execution import GovernedVersionPin
from .identity import Identity
from .security import ActorContext, OrganizationScope
from .workflow import OperationSideEffectClass, WorkflowDefinition, WorkflowLifecycle


EXECUTION_RECORD_SEMANTIC_TYPE: Final = "platform.execution-context"
GATE_DECISION_SEMANTIC_TYPE: Final = "platform.execution-gate-decision"
GATE_DECISION_AUTHORITY_SCOPE: Final = "platform.governed-execution/gate-decision"


class GovernedExecutionLifecycle(str, Enum):
    """RFC-0005 semantic execution conditions exercised by the P2.04 runtime."""

    CREATED = "Created"
    AWAITING_GATE = "AwaitingGate"
    READY = "Ready"
    RUNNING = "Running"
    WAITING = "Waiting"
    SUSPENDED = "Suspended"
    COMPENSATING = "Compensating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELLED = "Cancelled"
    COMPENSATED = "Compensated"
    PARTIALLY_COMPENSATED = "PartiallyCompensated"


TERMINAL_EXECUTION_STATES: Final[frozenset[GovernedExecutionLifecycle]] = frozenset(
    {
        GovernedExecutionLifecycle.SUCCEEDED,
        GovernedExecutionLifecycle.FAILED,
        GovernedExecutionLifecycle.CANCELLED,
        GovernedExecutionLifecycle.COMPENSATED,
        GovernedExecutionLifecycle.PARTIALLY_COMPENSATED,
    }
)


class GovernedGateKind(str, Enum):
    """Independent RFC-0005/RFC-0003 gate concepts; one never implies another."""

    ACTOR_ASSURANCE = "ActorAssurance"
    AUTHORIZATION = "Authorization"
    ORGANIZATIONAL_AUTHORITY = "OrganizationalAuthority"
    DATA_GOVERNANCE = "DataGovernance"
    VALIDATION = "Validation"
    CONSEQUENTIAL_APPROVAL = "ConsequentialApproval"


class GovernedGateOutcome(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"


class GovernedExecutionRuntimeError(RuntimeError):
    """Base error for bounded P2.04 runtime invariants."""


class RequiredGateUnresolvedError(PermissionError, GovernedExecutionRuntimeError):
    """One or more explicitly required gates have no exact decision evidence."""


class RequiredGateDeniedError(PermissionError, GovernedExecutionRuntimeError):
    """One or more explicitly required gates denied the execution."""


class TerminalExecutionSealedError(GovernedExecutionRuntimeError):
    """A caller attempted to mutate or advance sealed terminal execution history."""


class ExecutionTransitionError(GovernedExecutionRuntimeError):
    """The requested governance-significant lifecycle transition is invalid."""


class ConsequentialOperationNotAdmittedError(PermissionError, GovernedExecutionRuntimeError):
    """A consequential side effect was attempted outside admitted Governed Execution."""


_CONSEQUENTIAL_SIDE_EFFECTS: Final[frozenset[OperationSideEffectClass]] = frozenset(
    {
        OperationSideEffectClass.CANONICAL_MUTATION,
        OperationSideEffectClass.EXTERNAL_MUTATION,
        OperationSideEffectClass.COMMITMENT,
    }
)


_ALLOWED_TRANSITIONS: Final[
    dict[GovernedExecutionLifecycle, frozenset[GovernedExecutionLifecycle]]
] = {
    GovernedExecutionLifecycle.CREATED: frozenset(
        {
            GovernedExecutionLifecycle.AWAITING_GATE,
            GovernedExecutionLifecycle.READY,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.AWAITING_GATE: frozenset(
        {
            GovernedExecutionLifecycle.READY,
            GovernedExecutionLifecycle.WAITING,
            GovernedExecutionLifecycle.SUSPENDED,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.READY: frozenset(
        {
            GovernedExecutionLifecycle.RUNNING,
            GovernedExecutionLifecycle.WAITING,
            GovernedExecutionLifecycle.SUSPENDED,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.RUNNING: frozenset(
        {
            GovernedExecutionLifecycle.WAITING,
            GovernedExecutionLifecycle.SUSPENDED,
            GovernedExecutionLifecycle.COMPENSATING,
            GovernedExecutionLifecycle.SUCCEEDED,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.WAITING: frozenset(
        {
            GovernedExecutionLifecycle.RUNNING,
            GovernedExecutionLifecycle.AWAITING_GATE,
            GovernedExecutionLifecycle.SUSPENDED,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.SUSPENDED: frozenset(
        {
            GovernedExecutionLifecycle.RUNNING,
            GovernedExecutionLifecycle.AWAITING_GATE,
            GovernedExecutionLifecycle.WAITING,
            GovernedExecutionLifecycle.FAILED,
            GovernedExecutionLifecycle.CANCELLED,
        }
    ),
    GovernedExecutionLifecycle.COMPENSATING: frozenset(
        {
            GovernedExecutionLifecycle.COMPENSATED,
            GovernedExecutionLifecycle.PARTIALLY_COMPENSATED,
            GovernedExecutionLifecycle.FAILED,
        }
    ),
    GovernedExecutionLifecycle.SUCCEEDED: frozenset(),
    GovernedExecutionLifecycle.FAILED: frozenset(),
    GovernedExecutionLifecycle.CANCELLED: frozenset(),
    GovernedExecutionLifecycle.COMPENSATED: frozenset(),
    GovernedExecutionLifecycle.PARTIALLY_COMPENSATED: frozenset(),
}


def _require_timezone_aware(value: datetime, *, label: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be a timezone-aware datetime")


def _unique_refs(*refs: Identity) -> tuple[Identity, ...]:
    ordered: list[Identity] = []
    seen: set[Identity] = set()
    for ref in refs:
        if not isinstance(ref, Identity):
            raise ValueError("governed execution provenance references must be Identity values")
        if ref not in seen:
            ordered.append(ref)
            seen.add(ref)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class GovernedGateDecision:
    """One immutable decision about one exact gate for one execution version."""

    record: CanonicalRecord
    kind: GovernedGateKind
    outcome: GovernedGateOutcome
    basis_ref: Identity
    execution_subject_id: Identity
    evaluated_execution_version_id: Identity
    workflow_version_id: Identity
    operation_name: str
    material_input_version_ids: tuple[Identity, ...]
    product_contract_version_id: Identity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("governed gate decision must use a CanonicalRecord envelope")
        if self.record.semantic_type != GATE_DECISION_SEMANTIC_TYPE:
            raise ValueError("gate decision semantic_type must be platform.execution-gate-decision")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("bounded P2.04 gate decision evidence uses Native authority")
        if self.record.authority_scope != GATE_DECISION_AUTHORITY_SCOPE:
            raise ValueError("gate decision authority scope must match P2.04 governed gate evidence")
        if not isinstance(self.kind, GovernedGateKind):
            raise ValueError("gate kind must be explicit")
        if not isinstance(self.outcome, GovernedGateOutcome):
            raise ValueError("gate outcome must be explicit")
        if self.record.lifecycle_status != self.outcome.value:
            raise ValueError("gate decision lifecycle status must match gate outcome")
        if not isinstance(self.basis_ref, Identity):
            raise ValueError("gate decision must preserve an explicit governed basis reference")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("gate decision operation_name must be explicit")
        if not isinstance(self.material_input_version_ids, tuple) or not self.material_input_version_ids:
            raise ValueError("gate decision must preserve exact material input Version Identities")
        if any(not isinstance(item, Identity) for item in self.material_input_version_ids):
            raise ValueError("gate material input references must be Identity values")
        if len(set(self.material_input_version_ids)) != len(self.material_input_version_ids):
            raise ValueError("gate material input Version Identities must not be duplicated")
        if self.product_contract_version_id is not None and not isinstance(
            self.product_contract_version_id, Identity
        ):
            raise ValueError("Product Contract Version Identity must be explicit when supplied")

        organization_scope = self.record.organization.organization_id.value
        scoped_refs = (
            self.record.subject_id,
            self.record.version_id,
            self.basis_ref,
            self.execution_subject_id,
            self.evaluated_execution_version_id,
            self.workflow_version_id,
            *self.material_input_version_ids,
            *(
                (self.product_contract_version_id,)
                if self.product_contract_version_id is not None
                else ()
            ),
        )
        if any(item.scope != organization_scope for item in scoped_refs):
            raise ValueError("governed gate decision references must share Organization scope")
        if self.record.subject_id == self.record.version_id:
            raise ValueError("gate decision Subject and Version Identity must remain distinct")

        required_provenance = set(scoped_refs[2:])
        if not required_provenance.issubset(set(self.record.provenance_refs)):
            raise ValueError("gate decision provenance must preserve exact governed reliance references")

    @property
    def version_pin(self) -> GovernedVersionPin:
        return GovernedVersionPin.from_record(self.record)


@dataclass(frozen=True, slots=True)
class GovernedExecutionContext:
    """One immutable governance-significant version of one governed execution."""

    record: CanonicalRecord
    workflow: GovernedVersionPin
    operation_name: str
    operation_side_effects: tuple[OperationSideEffectClass, ...]
    material_inputs: tuple[GovernedVersionPin, ...]
    required_gates: tuple[GovernedGateKind, ...]
    gate_decisions: tuple[GovernedGateDecision, ...] = ()
    product_contract: GovernedVersionPin | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Governed Execution Context must use a CanonicalRecord envelope")
        if self.record.semantic_type != EXECUTION_RECORD_SEMANTIC_TYPE:
            raise ValueError("Execution Context semantic_type must be platform.execution-context")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("Arvectum OS Execution Context must use Native authority")
        try:
            lifecycle = GovernedExecutionLifecycle(self.record.lifecycle_status)
        except (TypeError, ValueError) as exc:
            raise ValueError("Execution Context lifecycle_status must be an RFC-0005 condition") from exc
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ValueError("exact effective Workflow version pin must be explicit")
        if self.workflow.semantic_type != "platform.workflow":
            raise ValueError("workflow pin must reference a platform.workflow version")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("operation_name must be explicit")
        if not isinstance(self.operation_side_effects, tuple) or not self.operation_side_effects:
            raise ValueError("operation side-effect semantics must be explicit")
        if any(not isinstance(item, OperationSideEffectClass) for item in self.operation_side_effects):
            raise ValueError("operation_side_effects must contain OperationSideEffectClass values")
        if len(set(self.operation_side_effects)) != len(self.operation_side_effects):
            raise ValueError("operation_side_effects must not contain duplicates")
        if not isinstance(self.material_inputs, tuple) or not self.material_inputs:
            raise ValueError("at least one exact material input version must be pinned")
        if any(not isinstance(item, GovernedVersionPin) for item in self.material_inputs):
            raise ValueError("material_inputs must contain GovernedVersionPin values")
        if len({item.version_id for item in self.material_inputs}) != len(self.material_inputs):
            raise ValueError("material input Version Identities must not be duplicated")
        if not isinstance(self.required_gates, tuple):
            raise ValueError("required_gates must be an immutable tuple")
        if any(not isinstance(item, GovernedGateKind) for item in self.required_gates):
            raise ValueError("required_gates must contain GovernedGateKind values")
        if len(set(self.required_gates)) != len(self.required_gates):
            raise ValueError("required gates must not contain duplicates")
        if not isinstance(self.gate_decisions, tuple) or any(
            not isinstance(item, GovernedGateDecision) for item in self.gate_decisions
        ):
            raise ValueError("gate_decisions must contain GovernedGateDecision values")
        if len({item.kind for item in self.gate_decisions}) != len(self.gate_decisions):
            raise ValueError("one execution version must not pin duplicate decisions for one gate kind")
        if any(item.kind not in self.required_gates for item in self.gate_decisions):
            raise ValueError("execution must not claim gate decisions outside its required gate set")
        if self.product_contract is not None and not isinstance(
            self.product_contract, GovernedVersionPin
        ):
            raise ValueError("Product Contract reliance must use an exact governed version pin")

        organization_scope = self.record.organization.organization_id.value
        pins = (
            self.workflow,
            *self.material_inputs,
            *((self.product_contract,) if self.product_contract is not None else ()),
            *(decision.version_pin for decision in self.gate_decisions),
        )
        if any(
            pin.subject_id.scope != organization_scope or pin.version_id.scope != organization_scope
            for pin in pins
        ):
            raise ValueError("Execution Context and all governed pins must share Organization scope")
        if self.record.subject_id == self.workflow.subject_id:
            raise ValueError("Workflow and Execution Context must have distinct Subject Identities")
        if lifecycle is GovernedExecutionLifecycle.CREATED:
            if self.record.predecessor_version_id is not None:
                raise ValueError("Created execution must be the initial canonical version")
            if self.gate_decisions:
                raise ValueError("Created execution must not claim gate decisions")
        elif self.record.predecessor_version_id is None:
            raise ValueError("governance-significant successor execution must preserve predecessor lineage")

        for decision in self.gate_decisions:
            if decision.record.organization != self.organization:
                raise ValueError("execution and gate decisions must share Organization scope")
            if decision.execution_subject_id != self.execution_subject_id:
                raise ValueError("gate decision must reference the same stable Execution Identity")
            if decision.workflow_version_id != self.workflow.version_id:
                raise ValueError("gate decision must preserve the exact Workflow version")
            if decision.operation_name != self.operation_name:
                raise ValueError("gate decision operation must match execution operation")
            if set(decision.material_input_version_ids) != {
                item.version_id for item in self.material_inputs
            }:
                raise ValueError("gate decision must preserve the exact material input versions")
            expected_contract = (
                self.product_contract.version_id if self.product_contract is not None else None
            )
            if decision.product_contract_version_id != expected_contract:
                raise ValueError("gate decision Product Contract attribution must match execution")
            if decision.record.version_id not in self.record.provenance_refs:
                raise ValueError("execution provenance must preserve exact gate decision versions")

        if lifecycle in (GovernedExecutionLifecycle.READY, GovernedExecutionLifecycle.RUNNING):
            if not self.gates_satisfied:
                raise ValueError("Ready/Running execution requires every required gate to allow")

    @property
    def lifecycle(self) -> GovernedExecutionLifecycle:
        return GovernedExecutionLifecycle(self.record.lifecycle_status)

    @property
    def execution_subject_id(self) -> Identity:
        return self.record.subject_id

    @property
    def execution_version_id(self) -> Identity:
        return self.record.version_id

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    @property
    def initiating_actor(self) -> ActorContext:
        return self.record.creation_actor

    @property
    def is_terminal(self) -> bool:
        return self.lifecycle in TERMINAL_EXECUTION_STATES

    @property
    def gates_satisfied(self) -> bool:
        by_kind = {decision.kind: decision for decision in self.gate_decisions}
        return all(
            kind in by_kind and by_kind[kind].outcome is GovernedGateOutcome.ALLOW
            for kind in self.required_gates
        )

    @property
    def unresolved_gates(self) -> tuple[GovernedGateKind, ...]:
        resolved = {decision.kind for decision in self.gate_decisions}
        return tuple(kind for kind in self.required_gates if kind not in resolved)


@dataclass(frozen=True, slots=True)
class GovernedGateEvaluation:
    """Fail-closed evaluation result for one exact AwaitingGate execution version."""

    required_gates: tuple[GovernedGateKind, ...]
    decisions: tuple[GovernedGateDecision, ...]

    @property
    def unresolved_gates(self) -> tuple[GovernedGateKind, ...]:
        decided = {decision.kind for decision in self.decisions}
        return tuple(kind for kind in self.required_gates if kind not in decided)

    @property
    def denied_gates(self) -> tuple[GovernedGateKind, ...]:
        return tuple(
            decision.kind
            for decision in self.decisions
            if decision.kind in self.required_gates
            and decision.outcome is GovernedGateOutcome.DENY
        )

    @property
    def can_proceed(self) -> bool:
        return not self.unresolved_gates and not self.denied_gates


@dataclass(frozen=True, slots=True)
class GovernedExecutionLineage:
    """History-preserving lineage view over immutable P2.04 execution versions."""

    versions: tuple[GovernedExecutionContext, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.versions, tuple) or not self.versions:
            raise ValueError("execution lineage requires at least one immutable version")
        if any(not isinstance(item, GovernedExecutionContext) for item in self.versions):
            raise ValueError("execution lineage may contain only GovernedExecutionContext values")
        execution_ids = {item.execution_subject_id for item in self.versions}
        if len(execution_ids) != 1:
            raise ValueError("execution lineage must contain one stable Execution Identity")
        CanonicalLineage(tuple(item.record for item in self.versions))

        by_version = {item.execution_version_id: item for item in self.versions}
        for item in self.versions:
            if item.is_terminal:
                successor_exists = any(
                    other.record.predecessor_version_id == item.execution_version_id
                    for other in self.versions
                )
                if successor_exists:
                    raise TerminalExecutionSealedError(
                        "terminal execution version must remain sealed in canonical lineage"
                    )
            predecessor = item.record.predecessor_version_id
            if predecessor is not None and predecessor not in by_version:
                raise ValueError("execution lineage predecessor must be present")

    @property
    def execution_subject_id(self) -> Identity:
        return self.versions[0].execution_subject_id

    def head(self) -> GovernedExecutionContext:
        head_record = CanonicalLineage(tuple(item.record for item in self.versions)).head
        for item in self.versions:
            if item.execution_version_id == head_record.version_id:
                return item
        raise AssertionError("validated execution lineage head must resolve")

    def exact(self, version_id: Identity) -> GovernedExecutionContext:
        for item in self.versions:
            if item.execution_version_id == version_id:
                return item
        raise KeyError(f"execution Version Identity not found: {version_id}")


def _validate_execution_operation(
    *,
    workflow: WorkflowDefinition,
    operation_name: str,
    material_inputs: tuple[CanonicalRecord, ...],
) -> tuple[OperationSideEffectClass, ...]:
    if not isinstance(operation_name, str) or not operation_name.strip():
        raise ValueError("operation_name must be explicit")
    if not isinstance(material_inputs, tuple) or not material_inputs:
        raise ValueError("at least one exact material input Canonical Record is required")
    if any(not isinstance(item, CanonicalRecord) for item in material_inputs):
        raise ValueError("material_inputs must contain CanonicalRecord versions")
    operations = tuple(
        operation for operation in workflow.operations if operation.semantic_name == operation_name
    )
    if len(operations) != 1:
        raise ValueError("exact Workflow version must declare the requested operation exactly once")
    operation = operations[0]
    matches_target = any(
        item.subject_id == operation.target_subject_id
        and item.semantic_type == operation.target_semantic_type
        for item in material_inputs
    )
    if not matches_target:
        raise ValueError("requested Workflow operation target must be among exact material inputs")
    return operation.side_effect_classes


def start_governed_execution(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    workflow: WorkflowDefinition,
    operation_name: str,
    material_inputs: tuple[CanonicalRecord, ...],
    required_gates: tuple[GovernedGateKind, ...],
    execution_id: Identity,
    version_id: Identity,
    created_at: datetime,
    product_contract: GovernedVersionPin | None = None,
) -> GovernedExecutionContext:
    """Create the initial immutable ``Created`` Execution Context version.

    Product Contract attribution is deliberately only an exact version pin here.
    P2.07 remains responsible for validating Product Contract shape, lifecycle and
    declared product/platform boundary semantics.
    """

    if not isinstance(organization, OrganizationScope):
        raise ValueError("Execution Organization scope must be explicit")
    if not isinstance(actor, ActorContext) or actor.organization != organization:
        raise ValueError("Execution actor must share Organization scope")
    if not isinstance(workflow, WorkflowDefinition) or workflow.organization != organization:
        raise ValueError("exact Workflow definition must share Organization scope")
    if workflow.record.lifecycle_status != WorkflowLifecycle.APPROVED.value:
        raise ValueError("ordinary P2.04 execution requires an explicitly Approved Workflow version")
    if any(item.organization != organization for item in material_inputs):
        raise ValueError("all material inputs must share the Execution Organization scope")
    if not isinstance(required_gates, tuple) or any(
        not isinstance(item, GovernedGateKind) for item in required_gates
    ):
        raise ValueError("required_gates must explicitly contain GovernedGateKind values")
    if len(set(required_gates)) != len(required_gates):
        raise ValueError("required gates must not contain duplicates")
    if not isinstance(execution_id, Identity) or not isinstance(version_id, Identity):
        raise ValueError("Execution Subject and Version Identities must be explicit")
    if execution_id == version_id:
        raise ValueError("Execution Subject Identity and Version Identity are distinct roles")
    if execution_id.scope != organization.organization_id.value or version_id.scope != execution_id.scope:
        raise ValueError("Execution identities must share Organization scope")
    _require_timezone_aware(created_at, label="execution created_at")
    if product_contract is not None:
        if not isinstance(product_contract, GovernedVersionPin):
            raise ValueError("Product Contract attribution must use a GovernedVersionPin")
        if (
            product_contract.subject_id.scope != organization.organization_id.value
            or product_contract.version_id.scope != organization.organization_id.value
        ):
            raise ValueError("Product Contract pin must share Execution Organization scope")

    side_effects = _validate_execution_operation(
        workflow=workflow,
        operation_name=operation_name,
        material_inputs=material_inputs,
    )
    if any(item in _CONSEQUENTIAL_SIDE_EFFECTS for item in side_effects) and (
        GovernedGateKind.AUTHORIZATION not in required_gates
    ):
        raise ValueError("consequential operation must declare an explicit Authorization gate")

    workflow_pin = GovernedVersionPin.from_record(workflow.record)
    input_pins = tuple(GovernedVersionPin.from_record(item) for item in material_inputs)
    provenance = _unique_refs(
        actor.actual_principal.principal_id,
        workflow_pin.subject_id,
        workflow_pin.version_id,
        *(identity for pin in input_pins for identity in (pin.subject_id, pin.version_id)),
        *(
            (product_contract.subject_id, product_contract.version_id)
            if product_contract is not None
            else ()
        ),
    )
    record = CanonicalRecord(
        subject_id=execution_id,
        version_id=version_id,
        semantic_type=EXECUTION_RECORD_SEMANTIC_TYPE,
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.governed-execution/context",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=provenance,
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(("operation", operation_name),),
        lifecycle_status=GovernedExecutionLifecycle.CREATED.value,
        predecessor_version_id=None,
    )
    return GovernedExecutionContext(
        record=record,
        workflow=workflow_pin,
        operation_name=operation_name,
        operation_side_effects=side_effects,
        material_inputs=input_pins,
        required_gates=required_gates,
        gate_decisions=(),
        product_contract=product_contract,
    )


def _successor_record(
    execution: GovernedExecutionContext,
    *,
    lifecycle: GovernedExecutionLifecycle,
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
    gate_decisions: tuple[GovernedGateDecision, ...] | None = None,
    additional_provenance_refs: tuple[Identity, ...] = (),
) -> CanonicalRecord:
    if execution.is_terminal:
        raise TerminalExecutionSealedError("terminal Execution Context history is sealed")
    if not isinstance(lifecycle, GovernedExecutionLifecycle):
        raise ValueError("target execution lifecycle must be explicit")
    allowed = _ALLOWED_TRANSITIONS[execution.lifecycle]
    if lifecycle not in allowed:
        raise ExecutionTransitionError(
            f"execution transition {execution.lifecycle.value} -> {lifecycle.value} is not admitted"
        )
    if not isinstance(version_id, Identity):
        raise ValueError("successor execution Version Identity must be explicit")
    if version_id == execution.execution_version_id or version_id == execution.execution_subject_id:
        raise ValueError("successor Execution Context requires a distinct Version Identity")
    if version_id.scope != execution.organization.organization_id.value:
        raise ValueError("successor execution Version Identity must share Organization scope")
    if not isinstance(actor, ActorContext) or actor.organization != execution.organization:
        raise ValueError("execution transition actor must share Organization scope")
    _require_timezone_aware(created_at, label="execution transition created_at")
    if not isinstance(additional_provenance_refs, tuple):
        raise ValueError("additional_provenance_refs must be an immutable tuple")

    effective_decisions = execution.gate_decisions if gate_decisions is None else gate_decisions
    decision_refs = tuple(decision.record.version_id for decision in effective_decisions)
    provenance = _unique_refs(
        *execution.record.provenance_refs,
        execution.execution_version_id,
        actor.actual_principal.principal_id,
        *decision_refs,
        *additional_provenance_refs,
    )
    return CanonicalRecord(
        subject_id=execution.execution_subject_id,
        version_id=version_id,
        semantic_type=execution.record.semantic_type,
        schema_version=execution.record.schema_version,
        organization=execution.organization,
        authority_mode=execution.record.authority_mode,
        authority_scope=execution.record.authority_scope,
        accountable_owner_id=execution.record.accountable_owner_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=provenance,
        integrity_metadata=execution.record.integrity_metadata,
        payload=execution.record.payload,
        lifecycle_status=lifecycle.value,
        predecessor_version_id=execution.execution_version_id,
    )


def await_required_gates(
    execution: GovernedExecutionContext,
    *,
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
) -> GovernedExecutionContext:
    """Enter/re-enter ``AwaitingGate`` and invalidate any prior gate evidence."""

    if execution.lifecycle not in {
        GovernedExecutionLifecycle.CREATED,
        GovernedExecutionLifecycle.WAITING,
        GovernedExecutionLifecycle.SUSPENDED,
    }:
        raise ExecutionTransitionError("AwaitingGate may be entered from Created/Waiting/Suspended")
    if not execution.required_gates:
        raise ExecutionTransitionError("execution with no required gates should be admitted directly")
    record = _successor_record(
        execution,
        lifecycle=GovernedExecutionLifecycle.AWAITING_GATE,
        version_id=version_id,
        actor=actor,
        created_at=created_at,
        gate_decisions=(),
    )
    return GovernedExecutionContext(
        record=record,
        workflow=execution.workflow,
        operation_name=execution.operation_name,
        operation_side_effects=execution.operation_side_effects,
        material_inputs=execution.material_inputs,
        required_gates=execution.required_gates,
        gate_decisions=(),
        product_contract=execution.product_contract,
    )


def build_governed_gate_decision(
    *,
    execution: GovernedExecutionContext,
    kind: GovernedGateKind,
    outcome: GovernedGateOutcome,
    decision_actor: ActorContext,
    basis_ref: Identity,
    decision_id: Identity,
    version_id: Identity,
    created_at: datetime,
) -> GovernedGateDecision:
    """Record immutable gate evidence for the exact AwaitingGate execution version.

    This function records supplied governed decision evidence.  It intentionally
    does not define IAM policy, delegation issuance or who is organizationally
    entitled to make the decision; those remain governed by their applicable
    authority/policy mechanisms.
    """

    if execution.lifecycle is not GovernedExecutionLifecycle.AWAITING_GATE:
        raise ValueError("gate decisions must evaluate the exact AwaitingGate execution version")
    if not isinstance(kind, GovernedGateKind) or kind not in execution.required_gates:
        raise ValueError("gate decision kind must be one of the execution's required gates")
    if not isinstance(outcome, GovernedGateOutcome):
        raise ValueError("gate outcome must be explicit")
    if not isinstance(decision_actor, ActorContext) or decision_actor.organization != execution.organization:
        raise ValueError("gate decision actor must share Organization scope")
    if not isinstance(basis_ref, Identity) or basis_ref.scope != execution.organization.organization_id.value:
        raise ValueError("gate decision basis must be an Organization-scoped governed reference")
    if not isinstance(decision_id, Identity) or not isinstance(version_id, Identity):
        raise ValueError("gate decision Subject and Version Identities must be explicit")
    if decision_id == version_id:
        raise ValueError("gate decision Subject Identity and Version Identity are distinct roles")
    if (
        decision_id.scope != execution.organization.organization_id.value
        or version_id.scope != execution.organization.organization_id.value
    ):
        raise ValueError("gate decision identities must share Organization scope")
    _require_timezone_aware(created_at, label="gate decision created_at")

    material_versions = tuple(item.version_id for item in execution.material_inputs)
    contract_version = (
        execution.product_contract.version_id if execution.product_contract is not None else None
    )
    provenance = _unique_refs(
        decision_actor.actual_principal.principal_id,
        basis_ref,
        execution.execution_subject_id,
        execution.execution_version_id,
        execution.workflow.version_id,
        *material_versions,
        *((contract_version,) if contract_version is not None else ()),
    )
    record = CanonicalRecord(
        subject_id=decision_id,
        version_id=version_id,
        semantic_type=GATE_DECISION_SEMANTIC_TYPE,
        schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=GATE_DECISION_AUTHORITY_SCOPE,
        accountable_owner_id=decision_actor.actual_principal.principal_id,
        creation_actor=decision_actor,
        created_at=created_at,
        provenance_refs=provenance,
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(("gate_kind", kind.value), ("operation", execution.operation_name)),
        lifecycle_status=outcome.value,
        predecessor_version_id=None,
    )
    return GovernedGateDecision(
        record=record,
        kind=kind,
        outcome=outcome,
        basis_ref=basis_ref,
        execution_subject_id=execution.execution_subject_id,
        evaluated_execution_version_id=execution.execution_version_id,
        workflow_version_id=execution.workflow.version_id,
        operation_name=execution.operation_name,
        material_input_version_ids=material_versions,
        product_contract_version_id=contract_version,
    )


def _validate_gate_for_execution(
    execution: GovernedExecutionContext,
    decision: GovernedGateDecision,
) -> None:
    if decision.kind not in execution.required_gates:
        raise ValueError("gate decision kind is not required by this execution")
    if decision.record.organization != execution.organization:
        raise ValueError("gate decision and execution must share Organization scope")
    if decision.execution_subject_id != execution.execution_subject_id:
        raise ValueError("gate decision must reference the exact Execution Identity")
    if decision.evaluated_execution_version_id != execution.execution_version_id:
        raise ValueError("gate decision must reference the exact execution Version Identity evaluated")
    if decision.workflow_version_id != execution.workflow.version_id:
        raise ValueError("gate decision must reference the exact Workflow Version Identity")
    if decision.operation_name != execution.operation_name:
        raise ValueError("gate decision operation must match execution operation")
    if set(decision.material_input_version_ids) != {
        item.version_id for item in execution.material_inputs
    }:
        raise ValueError("gate decision must reference every exact material input version")
    expected_contract = (
        execution.product_contract.version_id if execution.product_contract is not None else None
    )
    if decision.product_contract_version_id != expected_contract:
        raise ValueError("gate decision must preserve exact applicable Product Contract version")


def evaluate_required_gates(
    *,
    execution: GovernedExecutionContext,
    decisions: tuple[GovernedGateDecision, ...],
) -> GovernedGateEvaluation:
    """Validate exact decision attribution and evaluate required gates fail-closed."""

    if execution.lifecycle is not GovernedExecutionLifecycle.AWAITING_GATE:
        raise ValueError("required gates can only evaluate an AwaitingGate execution version")
    if not isinstance(decisions, tuple) or any(
        not isinstance(item, GovernedGateDecision) for item in decisions
    ):
        raise ValueError("decisions must be an immutable tuple of GovernedGateDecision values")
    if len({item.kind for item in decisions}) != len(decisions):
        raise ValueError("at most one decision may be supplied for each required gate kind")
    for decision in decisions:
        _validate_gate_for_execution(execution, decision)
    return GovernedGateEvaluation(required_gates=execution.required_gates, decisions=decisions)


def admit_ready_execution(
    execution: GovernedExecutionContext,
    *,
    decisions: tuple[GovernedGateDecision, ...] = (),
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
) -> GovernedExecutionContext:
    """Create immutable ``Ready`` state only after every required gate explicitly allows."""

    if execution.lifecycle is GovernedExecutionLifecycle.CREATED:
        if execution.required_gates:
            raise RequiredGateUnresolvedError("required gates must be evaluated from AwaitingGate")
        evaluation = GovernedGateEvaluation(required_gates=(), decisions=())
    elif execution.lifecycle is GovernedExecutionLifecycle.AWAITING_GATE:
        evaluation = evaluate_required_gates(execution=execution, decisions=decisions)
    else:
        raise ExecutionTransitionError("Ready admission requires Created(no gates) or AwaitingGate")

    if evaluation.unresolved_gates:
        names = ", ".join(item.value for item in evaluation.unresolved_gates)
        raise RequiredGateUnresolvedError(f"required execution gates unresolved: {names}")
    if evaluation.denied_gates:
        names = ", ".join(item.value for item in evaluation.denied_gates)
        raise RequiredGateDeniedError(f"required execution gates denied: {names}")

    record = _successor_record(
        execution,
        lifecycle=GovernedExecutionLifecycle.READY,
        version_id=version_id,
        actor=actor,
        created_at=created_at,
        gate_decisions=evaluation.decisions,
    )
    return GovernedExecutionContext(
        record=record,
        workflow=execution.workflow,
        operation_name=execution.operation_name,
        operation_side_effects=execution.operation_side_effects,
        material_inputs=execution.material_inputs,
        required_gates=execution.required_gates,
        gate_decisions=evaluation.decisions,
        product_contract=execution.product_contract,
    )


def transition_governed_execution(
    execution: GovernedExecutionContext,
    *,
    lifecycle: GovernedExecutionLifecycle,
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
    additional_provenance_refs: tuple[Identity, ...] = (),
) -> GovernedExecutionContext:
    """Create one immutable governance-significant successor transition.

    ``Ready`` and re-entry into ``AwaitingGate`` are intentionally reserved for
    ``admit_ready_execution`` and ``await_required_gates`` so generic transition
    mechanics cannot bypass required gate orchestration.
    """

    if lifecycle in {
        GovernedExecutionLifecycle.READY,
        GovernedExecutionLifecycle.AWAITING_GATE,
    }:
        raise ExecutionTransitionError("Ready/AwaitingGate transitions require gate-specific APIs")
    if lifecycle is GovernedExecutionLifecycle.RUNNING and not execution.gates_satisfied:
        raise RequiredGateUnresolvedError("Running execution requires every declared gate to allow")
    if lifecycle in {
        GovernedExecutionLifecycle.SUCCEEDED,
        GovernedExecutionLifecycle.COMPENSATING,
        GovernedExecutionLifecycle.COMPENSATED,
        GovernedExecutionLifecycle.PARTIALLY_COMPENSATED,
    } and any(item in _CONSEQUENTIAL_SIDE_EFFECTS for item in execution.operation_side_effects):
        if not execution.gates_satisfied:
            raise RequiredGateUnresolvedError(
                "consequential execution cannot complete/compensate without admitted required gates"
            )

    record = _successor_record(
        execution,
        lifecycle=lifecycle,
        version_id=version_id,
        actor=actor,
        created_at=created_at,
        additional_provenance_refs=additional_provenance_refs,
    )
    return GovernedExecutionContext(
        record=record,
        workflow=execution.workflow,
        operation_name=execution.operation_name,
        operation_side_effects=execution.operation_side_effects,
        material_inputs=execution.material_inputs,
        required_gates=execution.required_gates,
        gate_decisions=execution.gate_decisions,
        product_contract=execution.product_contract,
    )


def resume_governed_execution(
    execution: GovernedExecutionContext,
    *,
    gates_still_valid: bool,
    version_id: Identity,
    actor: ActorContext,
    created_at: datetime,
) -> GovernedExecutionContext:
    """Resume Waiting/Suspended work or explicitly force stale-gate re-evaluation."""

    if execution.lifecycle not in {
        GovernedExecutionLifecycle.WAITING,
        GovernedExecutionLifecycle.SUSPENDED,
    }:
        raise ExecutionTransitionError("only Waiting/Suspended execution can resume")
    if not isinstance(gates_still_valid, bool):
        raise ValueError("resume must explicitly state whether prior gate assumptions remain valid")
    if gates_still_valid:
        return transition_governed_execution(
            execution,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=version_id,
            actor=actor,
            created_at=created_at,
        )
    return await_required_gates(
        execution,
        version_id=version_id,
        actor=actor,
        created_at=created_at,
    )


def require_consequential_operation_admission(
    execution: GovernedExecutionContext | None,
    *,
    side_effect_class: OperationSideEffectClass,
) -> None:
    """Fail closed unless a consequential effect is inside admitted Governed Execution.

    This is a semantic guard only.  P2.06 will define broader consistency,
    idempotency and conflict behavior for real mutation/commit boundaries.
    """

    if not isinstance(side_effect_class, OperationSideEffectClass):
        raise ValueError("side_effect_class must be explicit")
    if side_effect_class not in _CONSEQUENTIAL_SIDE_EFFECTS:
        raise ValueError("this guard is only for consequential operation side-effect classes")
    if not isinstance(execution, GovernedExecutionContext):
        raise ConsequentialOperationNotAdmittedError(
            "consequential operation requires an explicit Governed Execution Context"
        )
    if execution.lifecycle not in {
        GovernedExecutionLifecycle.READY,
        GovernedExecutionLifecycle.RUNNING,
    }:
        raise ConsequentialOperationNotAdmittedError(
            "consequential operation requires Ready or Running admitted execution state"
        )
    if side_effect_class not in execution.operation_side_effects:
        raise ConsequentialOperationNotAdmittedError(
            "requested consequential side effect is not declared by the exact Workflow operation"
        )
    if not execution.gates_satisfied:
        raise ConsequentialOperationNotAdmittedError(
            "consequential operation requires all declared execution gates to allow"
        )
