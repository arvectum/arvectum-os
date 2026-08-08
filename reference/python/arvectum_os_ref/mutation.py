"""P1.06 — governed CanonicalMutation and second immutable target version.

The boundary is deliberately in-memory and domain-neutral. It consumes the
exact Workflow/material-input pins and exact P1.05 gate decision evidence
already admitted into the Ready Execution Context. It does not resolve a
mutable ``current`` Workflow or target version, introduce persistence, or emit
a canonical Event; Event admission remains P1.07.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .canonical import CanonicalRecord
from .execution import ExecutionContext, ExecutionLifecycle, GovernedVersionPin
from .gates import GateDecision, GateKind, GateOutcome
from .identity import Identity
from .workflow import OperationSideEffectClass, WorkflowDefinition


class CanonicalConflictError(RuntimeError):
    """The admitted current target no longer matches the exact pinned input."""


@dataclass(frozen=True, slots=True)
class CanonicalMutationResult:
    """Immutable bounded result of one successfully governed canonical mutation."""

    previous_version: GovernedVersionPin
    resulting_record: CanonicalRecord
    execution: ExecutionContext

    def __post_init__(self) -> None:
        if self.resulting_record.subject_id != self.previous_version.subject_id:
            raise ValueError("mutation result must preserve the target Subject Identity")
        if self.resulting_record.predecessor_version_id != self.previous_version.version_id:
            raise ValueError("mutation result must preserve exact predecessor lineage")
        if self.resulting_record.version_id == self.previous_version.version_id:
            raise ValueError("mutation result must use a distinct immutable Version Identity")
        if self.execution.record.lifecycle_status != ExecutionLifecycle.SUCCEEDED.value:
            raise ValueError(
                "mutation result must expose the terminal Succeeded Execution Context version"
            )
        if len(self.execution.canonical_effects) != 1:
            raise ValueError("mutation result execution must pin exactly one canonical effect")
        if self.execution.canonical_effects[0] != GovernedVersionPin.from_record(
            self.resulting_record
        ):
            raise ValueError(
                "mutation result execution must pin the exact resulting Canonical Record version"
            )


def _require_exact_workflow(
    *,
    execution: ExecutionContext,
    workflow: WorkflowDefinition,
) -> None:
    if workflow.organization != execution.organization:
        raise ValueError("supplied Workflow and Ready execution must share Organization scope")
    if (
        workflow.record.subject_id != execution.workflow.subject_id
        or workflow.record.version_id != execution.workflow.version_id
    ):
        raise ValueError("P1.06 must consume the exact Workflow version pinned by the execution")

    material = execution.material_inputs[0]
    matching = tuple(
        operation
        for operation in workflow.operations
        if operation.semantic_name == execution.operation_name
        and operation.target_subject_id == material.subject_id
        and operation.target_semantic_type == material.semantic_type
        and OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes
    )
    if len(matching) != 1:
        raise ValueError(
            "pinned Workflow must declare exactly the executed CanonicalMutation operation"
        )


def _require_exact_gate_decision(
    *,
    execution: ExecutionContext,
    decision: GateDecision,
    expected_kind: GateKind,
) -> None:
    if decision.kind is not expected_kind:
        raise ValueError(f"expected {expected_kind.value} decision evidence")
    if decision.outcome is not GateOutcome.ALLOW:
        raise PermissionError(f"{expected_kind.value} must explicitly allow the mutation")

    by_type = {pin.semantic_type: pin for pin in execution.gate_decisions}
    expected_pin = by_type.get(decision.record.semantic_type)
    if expected_pin is None or expected_pin != decision.version_pin:
        raise ValueError(
            "P1.06 must consume the exact gate decision version pinned by Ready execution"
        )
    if decision.record.organization != execution.organization:
        raise ValueError("gate decision and execution must share Organization scope")
    if decision.subject_principal_id != execution.initiating_actor.actual_principal.principal_id:
        raise ValueError("gate decision must apply to the initiating Principal")
    if decision.execution_subject_id != execution.execution_subject_id:
        raise ValueError("gate decision must reference the exact Execution Subject Identity")
    if decision.evaluated_execution_version_id != execution.record.predecessor_version_id:
        raise ValueError(
            "gate decision must reference the exact AwaitingGate execution version admitted into Ready"
        )
    if decision.workflow_version_id != execution.workflow.version_id:
        raise ValueError("gate decision must reference the exact pinned Workflow Version Identity")
    if decision.operation_name != execution.operation_name:
        raise ValueError("gate decision operation must match the Ready execution operation")

    material = execution.material_inputs[0]
    if (
        decision.target_subject_id != material.subject_id
        or decision.target_version_id != material.version_id
    ):
        raise ValueError(
            "gate decision must reference the exact pinned target Subject and Version Identity"
        )


def execute_p1_06_canonical_mutation(
    *,
    execution: ExecutionContext | None,
    workflow: WorkflowDefinition,
    authorization: GateDecision,
    organizational_authority: GateDecision,
    current_record: CanonicalRecord,
    new_version_id: Identity,
    new_payload: tuple[tuple[str, str], ...],
) -> CanonicalMutationResult:
    """Execute the bounded mutation only through the exact Ready governed evidence.

    ``current_record`` is the caller-supplied admitted current target version for
    this in-memory harness. It is checked against the already-pinned material
    input; it is not resolved dynamically. A mismatch is a canonical conflict.
    """

    if not isinstance(execution, ExecutionContext):
        raise PermissionError(
            "consequential canonical mutation requires an explicit Execution Context"
        )
    if execution.record.lifecycle_status != ExecutionLifecycle.READY.value:
        raise PermissionError(
            "P1.06 canonical mutation requires the immutable Ready Execution Context version"
        )
    if len(execution.material_inputs) != 1:
        raise ValueError("P1.06 bounded slice requires exactly one material input")
    if len(execution.gate_decisions) != 2:
        raise PermissionError(
            "P1.06 requires exact P1.05 Authorization and Organizational Authority evidence"
        )

    _require_exact_workflow(execution=execution, workflow=workflow)
    _require_exact_gate_decision(
        execution=execution,
        decision=authorization,
        expected_kind=GateKind.AUTHORIZATION,
    )
    _require_exact_gate_decision(
        execution=execution,
        decision=organizational_authority,
        expected_kind=GateKind.ORGANIZATIONAL_AUTHORITY,
    )

    material = execution.material_inputs[0]
    if current_record.organization != execution.organization:
        raise ValueError("current target and execution must share Organization scope")
    if current_record.subject_id != material.subject_id:
        raise ValueError("current target must be the Subject Identity pinned by the execution")
    if (
        current_record.semantic_type != material.semantic_type
        or current_record.authority_scope != material.authority_scope
    ):
        raise ValueError("current target semantics must match the exact material-input pin")
    if current_record.version_id != material.version_id:
        raise CanonicalConflictError(
            "current canonical version differs from the exact material input pinned before consequential reliance"
        )
    if not isinstance(new_version_id, Identity):
        raise ValueError("new_version_id must be an explicit Identity")
    if new_version_id.scope != execution.organization.organization_id.value:
        raise ValueError("new canonical Version Identity must share Organization scope")
    if new_version_id == current_record.version_id:
        raise ValueError("canonical mutation must create a distinct immutable Version Identity")
    if new_payload == current_record.payload:
        raise ValueError("P1.06 bounded mutation must change governed target state")

    gate_refs = tuple(
        identity
        for pin in execution.gate_decisions
        for identity in (pin.subject_id, pin.version_id)
    )
    resulting_record = CanonicalRecord(
        subject_id=current_record.subject_id,
        version_id=new_version_id,
        semantic_type=current_record.semantic_type,
        schema_version=current_record.schema_version,
        organization=current_record.organization,
        authority_mode=current_record.authority_mode,
        authority_scope=current_record.authority_scope,
        accountable_owner_id=current_record.accountable_owner_id,
        creation_actor=execution.initiating_actor,
        created_at=datetime.fromisoformat("2026-08-08T04:10:00+00:00"),
        provenance_refs=(
            current_record.subject_id,
            current_record.version_id,
            execution.execution_subject_id,
            execution.execution_version_id,
            execution.workflow.subject_id,
            execution.workflow.version_id,
            *gate_refs,
        ),
        integrity_metadata=current_record.integrity_metadata,
        payload=new_payload,
        lifecycle_status=current_record.lifecycle_status,
        predecessor_version_id=current_record.version_id,
    )
    effect_pin = GovernedVersionPin.from_record(resulting_record)

    terminal_record = CanonicalRecord(
        subject_id=execution.execution_subject_id,
        version_id=Identity(
            "execution-version",
            "reference-subject-maintenance-execution-1-v3",
            execution.organization.organization_id.value,
        ),
        semantic_type=execution.record.semantic_type,
        schema_version=execution.record.schema_version,
        organization=execution.organization,
        authority_mode=execution.record.authority_mode,
        authority_scope=execution.record.authority_scope,
        accountable_owner_id=execution.record.accountable_owner_id,
        creation_actor=execution.initiating_actor,
        created_at=datetime.fromisoformat("2026-08-08T04:11:00+00:00"),
        provenance_refs=(
            *execution.record.provenance_refs,
            current_record.subject_id,
            current_record.version_id,
            resulting_record.subject_id,
            resulting_record.version_id,
        ),
        integrity_metadata=execution.record.integrity_metadata,
        payload=execution.record.payload,
        lifecycle_status=ExecutionLifecycle.SUCCEEDED.value,
        predecessor_version_id=execution.execution_version_id,
    )
    terminal_execution = ExecutionContext(
        record=terminal_record,
        workflow=execution.workflow,
        operation_name=execution.operation_name,
        material_inputs=execution.material_inputs,
        gate_decisions=execution.gate_decisions,
        canonical_effects=(effect_pin,),
    )

    return CanonicalMutationResult(
        previous_version=material,
        resulting_record=resulting_record,
        execution=terminal_execution,
    )
