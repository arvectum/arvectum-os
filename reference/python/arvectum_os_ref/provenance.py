"""P1.08 — provenance, causation and reconstruction evidence.

The bounded reference slice already has immutable evidence from P1.02–P1.07.
This module verifies that evidence as one coherent operation and exposes a
frozen, version-identifiable reconstruction manifest.

The manifest is deliberately non-canonical and non-authoritative. Building it
must not replay the mutation, emit/admit another Event, mutate sealed history,
resolve a mutable projection, define the P1.10 portable fixture, or create an
Observation/Knowledge object.
"""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import CanonicalRecord
from .events import CanonicalEvent
from .execution import ExecutionContext, ExecutionLifecycle, GovernedVersionPin
from .gates import GateDecision, GateKind, GateOutcome
from .identity import Identity
from .mutation import CanonicalMutationResult
from .security import OrganizationScope
from .workflow import WorkflowDefinition


class ReconstructionEvidenceError(ValueError):
    """Supplied governed evidence cannot reconstruct the bounded operation."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ReconstructionEvidenceError(message)


def _ordered_unique(*groups: tuple[Identity, ...]) -> tuple[Identity, ...]:
    seen: set[Identity] = set()
    result: list[Identity] = []
    for group in groups:
        for identity in group:
            if identity not in seen:
                seen.add(identity)
                result.append(identity)
    return tuple(result)


def _contains(record: CanonicalRecord, *refs: Identity) -> bool:
    return set(refs).issubset(set(record.provenance_refs))


@dataclass(frozen=True, slots=True)
class ReconstructionEvidence:
    """Read-only manifest of exact references sufficient for bounded reconstruction."""

    organization: OrganizationScope
    initiating_actor_id: Identity
    operation_name: str
    workflow: GovernedVersionPin
    material_inputs: tuple[GovernedVersionPin, ...]
    gate_decisions: tuple[GovernedVersionPin, ...]
    execution_versions: tuple[GovernedVersionPin, ...]
    canonical_effects: tuple[GovernedVersionPin, ...]
    events: tuple[GovernedVersionPin, ...]
    event_type: str
    event_schema_version: str
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    provenance_refs: tuple[Identity, ...]

    def __post_init__(self) -> None:
        _require(
            isinstance(self.organization, OrganizationScope),
            "reconstruction Organization scope must be explicit",
        )
        _require(
            isinstance(self.initiating_actor_id, Identity),
            "reconstruction initiating actor must be an Identity",
        )
        _require(
            isinstance(self.operation_name, str) and bool(self.operation_name.strip()),
            "reconstruction operation_name must be explicit",
        )
        _require(
            isinstance(self.workflow, GovernedVersionPin),
            "reconstruction must pin the exact Workflow version",
        )

        pin_groups = (
            ("material input", self.material_inputs, 1),
            ("gate decision", self.gate_decisions, 2),
            ("execution", self.execution_versions, 3),
            ("canonical effect", self.canonical_effects, 1),
            ("Event", self.events, 1),
        )
        for label, pins, expected_count in pin_groups:
            _require(
                isinstance(pins, tuple)
                and len(pins) == expected_count
                and all(isinstance(pin, GovernedVersionPin) for pin in pins),
                f"P1.08 requires exactly {expected_count} {label} version pin(s)",
            )

        _require(
            isinstance(self.event_type, str) and bool(self.event_type.strip()),
            "reconstruction Event type must be explicit",
        )
        _require(
            isinstance(self.event_schema_version, str)
            and bool(self.event_schema_version.strip()),
            "reconstruction Event schema version must be explicit",
        )
        for label, refs in (
            ("correlation", self.correlation_refs),
            ("causation", self.causation_refs),
            ("provenance", self.provenance_refs),
        ):
            _require(
                isinstance(refs, tuple)
                and bool(refs)
                and all(isinstance(ref, Identity) for ref in refs),
                f"reconstruction {label} references must be explicit Identity values",
            )
        _require(
            len(set(self.provenance_refs)) == len(self.provenance_refs),
            "reconstruction provenance references must be de-duplicated",
        )

        organization_scope = self.organization.organization_id.value
        pins = (
            self.workflow,
            *self.material_inputs,
            *self.gate_decisions,
            *self.execution_versions,
            *self.canonical_effects,
            *self.events,
        )
        governed_refs = tuple(
            ref for pin in pins for ref in (pin.subject_id, pin.version_id)
        ) + self.correlation_refs + self.causation_refs
        _require(
            all(ref.scope == organization_scope for ref in governed_refs),
            "versioned reconstruction, correlation and causation references must share Organization scope",
        )


def build_p1_08_reconstruction_evidence(
    *,
    input_record: CanonicalRecord,
    workflow: WorkflowDefinition,
    awaiting_execution: ExecutionContext,
    authorization: GateDecision,
    organizational_authority: GateDecision,
    ready_execution: ExecutionContext,
    mutation: CanonicalMutationResult,
    event: CanonicalEvent,
) -> ReconstructionEvidence:
    """Validate exact P1.02–P1.07 evidence without creating new governed state."""

    # Fail closed on shape before dereferencing nested fields.
    _require(
        isinstance(input_record, CanonicalRecord),
        "P1.08 requires the exact initial Canonical Record version",
    )
    _require(
        isinstance(workflow, WorkflowDefinition),
        "P1.08 requires the exact Workflow definition",
    )
    _require(
        isinstance(awaiting_execution, ExecutionContext)
        and isinstance(ready_execution, ExecutionContext),
        "P1.08 requires exact pre-terminal Execution Context versions",
    )
    _require(
        isinstance(authorization, GateDecision)
        and isinstance(organizational_authority, GateDecision),
        "P1.08 requires explicit governed gate decision evidence",
    )
    _require(
        isinstance(mutation, CanonicalMutationResult),
        "P1.08 requires the exact P1.06 mutation result",
    )
    _require(
        isinstance(event, CanonicalEvent),
        "P1.08 requires the exact admitted P1.07 canonical Event",
    )

    terminal_execution = mutation.execution
    _require(
        isinstance(terminal_execution, ExecutionContext),
        "P1.08 mutation must expose the exact terminal Execution Context",
    )

    organization = input_record.organization
    governed_records = (
        workflow.record,
        awaiting_execution.record,
        authorization.record,
        organizational_authority.record,
        ready_execution.record,
        mutation.resulting_record,
        terminal_execution.record,
        event.record,
    )
    _require(
        all(record.organization == organization for record in governed_records),
        "all governed records used for P1.08 reconstruction must share Organization scope",
    )

    # Execution Identity and immutable governance-significant version lineage.
    _require(
        awaiting_execution.record.lifecycle_status == ExecutionLifecycle.AWAITING_GATE.value,
        "reconstruction must start from the AwaitingGate execution version",
    )
    _require(
        ready_execution.record.lifecycle_status == ExecutionLifecycle.READY.value,
        "reconstruction must include the immutable Ready execution version",
    )
    _require(
        terminal_execution.record.lifecycle_status == ExecutionLifecycle.SUCCEEDED.value,
        "reconstruction must end at the sealed Succeeded execution version",
    )
    _require(
        awaiting_execution.execution_subject_id
        == ready_execution.execution_subject_id
        == terminal_execution.execution_subject_id,
        "all reconstructed execution versions must share one Execution Identity",
    )
    _require(
        ready_execution.record.predecessor_version_id
        == awaiting_execution.execution_version_id,
        "Ready execution must preserve exact AwaitingGate predecessor lineage",
    )
    _require(
        terminal_execution.record.predecessor_version_id
        == ready_execution.execution_version_id,
        "Succeeded execution must preserve exact Ready predecessor lineage",
    )
    _require(
        len(
            {
                awaiting_execution.execution_version_id,
                ready_execution.execution_version_id,
                terminal_execution.execution_version_id,
            }
        )
        == 3,
        "governance-significant execution versions must remain distinct",
    )

    # Exact version-pinned Workflow, input and stable semantic operation.
    workflow_pin = GovernedVersionPin.from_record(workflow.record)
    input_pin = GovernedVersionPin.from_record(input_record)
    executions = (awaiting_execution, ready_execution, terminal_execution)
    _require(
        all(execution.workflow == workflow_pin for execution in executions),
        "every execution version must preserve the exact Workflow version pin",
    )
    _require(
        all(execution.material_inputs == (input_pin,) for execution in executions),
        "every execution version must preserve the exact material input version pin",
    )
    _require(
        awaiting_execution.operation_name
        == ready_execution.operation_name
        == terminal_execution.operation_name,
        "execution lineage must preserve one stable semantic operation",
    )

    actor_id = awaiting_execution.initiating_actor.actual_principal.principal_id
    _require(
        ready_execution.initiating_actor.actual_principal.principal_id == actor_id
        and terminal_execution.initiating_actor.actual_principal.principal_id == actor_id,
        "execution lineage must preserve the initiating Principal",
    )

    # Separate Authorization and Organizational Authority evidence.
    expected_gates = (
        (authorization, GateKind.AUTHORIZATION),
        (organizational_authority, GateKind.ORGANIZATIONAL_AUTHORITY),
    )
    for decision, kind in expected_gates:
        _require(
            decision.kind is kind,
            f"reconstruction requires exact {kind.value} decision evidence",
        )
        _require(
            decision.outcome is GateOutcome.ALLOW,
            f"reconstructed {kind.value} decision must explicitly Allow",
        )
        _require(
            decision.subject_principal_id == actor_id,
            "gate decision must apply to the initiating Principal",
        )
        _require(
            decision.execution_subject_id == awaiting_execution.execution_subject_id
            and decision.evaluated_execution_version_id
            == awaiting_execution.execution_version_id,
            "gate decision must reference the exact AwaitingGate execution version",
        )
        _require(
            decision.workflow_version_id == workflow_pin.version_id,
            "gate decision must preserve the exact Workflow Version Identity",
        )
        _require(
            decision.operation_name == awaiting_execution.operation_name,
            "gate decision must preserve the exact reconstructed operation",
        )
        _require(
            decision.target_subject_id == input_pin.subject_id
            and decision.target_version_id == input_pin.version_id,
            "gate decision must preserve the exact material target version",
        )
        _require(
            _contains(
                decision.record,
                decision.basis_ref,
                awaiting_execution.execution_subject_id,
                awaiting_execution.execution_version_id,
                workflow_pin.version_id,
                input_pin.subject_id,
                input_pin.version_id,
            ),
            "gate decision provenance is incomplete for bounded reconstruction",
        )

    gate_pins = (authorization.version_pin, organizational_authority.version_pin)
    _require(
        ready_execution.gate_decisions == gate_pins
        and terminal_execution.gate_decisions == gate_pins,
        "Ready and Succeeded execution versions must preserve the two exact gate decision pins",
    )

    # Canonical mutation lineage and its provenance.
    _require(
        mutation.previous_version == input_pin,
        "mutation must preserve the exact material predecessor version",
    )
    result = mutation.resulting_record
    result_pin = GovernedVersionPin.from_record(result)
    _require(
        result.subject_id == input_record.subject_id
        and result.predecessor_version_id == input_record.version_id,
        "canonical mutation result must preserve exact Subject/predecessor lineage",
    )
    _require(
        terminal_execution.canonical_effects == (result_pin,),
        "terminal execution must pin the exact resulting canonical version",
    )

    gate_refs = tuple(
        ref for pin in gate_pins for ref in (pin.subject_id, pin.version_id)
    )
    _require(
        _contains(
            result,
            input_record.subject_id,
            input_record.version_id,
            ready_execution.execution_subject_id,
            ready_execution.execution_version_id,
            workflow_pin.subject_id,
            workflow_pin.version_id,
            *gate_refs,
        ),
        "result provenance is incomplete for bounded reconstruction",
    )
    _require(
        _contains(
            terminal_execution.record,
            input_record.subject_id,
            input_record.version_id,
            result.subject_id,
            result.version_id,
            workflow_pin.subject_id,
            workflow_pin.version_id,
            *gate_refs,
        ),
        "terminal execution provenance is incomplete for bounded reconstruction",
    )

    # Event attribution, result linkage, correlation and causation remain distinct.
    _require(
        event.execution_subject_id == terminal_execution.execution_subject_id
        and event.execution_version_id == terminal_execution.execution_version_id,
        "Event must preserve the exact terminal Execution Context reference",
    )
    _require(
        event.related_subject_ids == (result.subject_id,)
        and event.related_version_ids == (result.version_id,),
        "Event must preserve the exact resulting canonical version",
    )
    _require(
        event.correlation_refs == (terminal_execution.execution_subject_id,),
        "P1.08 correlation must identify the stable Execution Identity without asserting causation",
    )
    _require(
        event.causation_refs == (terminal_execution.execution_version_id,),
        "P1.08 causation must identify the exact terminal execution version",
    )
    _require(
        event.producer_id == actor_id and event.initiating_actor_id == actor_id,
        "Event attribution must preserve the initiating Principal",
    )
    _require(
        event.event_type == "platform.canonical-mutation.succeeded"
        and event.event_schema_version == "1",
        "P1.08 Event type/schema must remain the exact bounded P1.07 semantics",
    )
    _require(
        event.record.payload
        == (
            ("operation", terminal_execution.operation_name),
            ("outcome", ExecutionLifecycle.SUCCEEDED.value),
        ),
        "Event payload must preserve the reconstructed operation outcome",
    )
    _require(
        _contains(
            event.record,
            actor_id,
            terminal_execution.execution_subject_id,
            terminal_execution.execution_version_id,
            result.subject_id,
            result.version_id,
        ),
        "Event provenance is incomplete for bounded reconstruction",
    )

    awaiting_pin = GovernedVersionPin.from_record(awaiting_execution.record)
    ready_pin = GovernedVersionPin.from_record(ready_execution.record)
    terminal_pin = GovernedVersionPin.from_record(terminal_execution.record)
    event_pin = GovernedVersionPin.from_record(event.record)

    provenance_refs = _ordered_unique(
        (actor_id,),
        (workflow_pin.subject_id, workflow_pin.version_id),
        (input_pin.subject_id, input_pin.version_id),
        (
            authorization.record.subject_id,
            authorization.record.version_id,
            authorization.basis_ref,
            organizational_authority.record.subject_id,
            organizational_authority.record.version_id,
            organizational_authority.basis_ref,
        ),
        (
            awaiting_pin.subject_id,
            awaiting_pin.version_id,
            ready_pin.version_id,
            terminal_pin.version_id,
        ),
        (result_pin.subject_id, result_pin.version_id),
        (event_pin.subject_id, event_pin.version_id),
    )

    return ReconstructionEvidence(
        organization=organization,
        initiating_actor_id=actor_id,
        operation_name=terminal_execution.operation_name,
        workflow=workflow_pin,
        material_inputs=(input_pin,),
        gate_decisions=gate_pins,
        execution_versions=(awaiting_pin, ready_pin, terminal_pin),
        canonical_effects=(result_pin,),
        events=(event_pin,),
        event_type=event.event_type,
        event_schema_version=event.event_schema_version,
        correlation_refs=event.correlation_refs,
        causation_refs=event.causation_refs,
        provenance_refs=provenance_refs,
    )
