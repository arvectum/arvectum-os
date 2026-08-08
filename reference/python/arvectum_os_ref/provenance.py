"""P1.08 — provenance, causation and reconstruction evidence.

This module reconstructs the already-completed bounded P1.06/P1.07 operation
from exact immutable governed records. It does not create new canonical state,
mutate sealed execution/Event history, resolve mutable projections, define a
portable fixture, or promote operational evidence into Observation/Knowledge.

The returned ``ReconstructionEvidence`` is a derived immutable manifest of
version-identifiable references. It is deliberately non-canonical and
non-authoritative: authority remains with the referenced governed records and
their Accepted semantics.
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
    """The supplied governed evidence cannot reconstruct the bounded operation."""


def _ordered_unique(identities: tuple[Identity, ...]) -> tuple[Identity, ...]:
    seen: set[Identity] = set()
    ordered: list[Identity] = []
    for identity in identities:
        if identity not in seen:
            seen.add(identity)
            ordered.append(identity)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class ReconstructionEvidence:
    """Read-only, non-canonical manifest of exact P1.08 reconstruction evidence."""

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
        if not isinstance(self.organization, OrganizationScope):
            raise ReconstructionEvidenceError("reconstruction Organization scope must be explicit")
        if not isinstance(self.initiating_actor_id, Identity):
            raise ReconstructionEvidenceError("reconstruction initiating actor must be an Identity")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ReconstructionEvidenceError("reconstruction operation_name must be explicit")
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ReconstructionEvidenceError("reconstruction must pin the exact Workflow version")
        if len(self.material_inputs) != 1 or any(
            not isinstance(item, GovernedVersionPin) for item in self.material_inputs
        ):
            raise ReconstructionEvidenceError("P1.08 requires exactly one material input version pin")
        if len(self.gate_decisions) != 2 or any(
            not isinstance(item, GovernedVersionPin) for item in self.gate_decisions
        ):
            raise ReconstructionEvidenceError("P1.08 requires the two exact governed gate decision pins")
        if len(self.execution_versions) != 3 or any(
            not isinstance(item, GovernedVersionPin) for item in self.execution_versions
        ):
            raise ReconstructionEvidenceError(
                "P1.08 requires AwaitingGate, Ready and Succeeded execution version pins"
            )
        if len(self.canonical_effects) != 1 or any(
            not isinstance(item, GovernedVersionPin) for item in self.canonical_effects
        ):
            raise ReconstructionEvidenceError("P1.08 requires exactly one canonical effect pin")
        if len(self.events) != 1 or any(
            not isinstance(item, GovernedVersionPin) for item in self.events
        ):
            raise ReconstructionEvidenceError("P1.08 requires exactly one canonical Event pin")
        if not isinstance(self.event_type, str) or not self.event_type.strip():
            raise ReconstructionEvidenceError("reconstruction Event type must be explicit")
        if not isinstance(self.event_schema_version, str) or not self.event_schema_version.strip():
            raise ReconstructionEvidenceError("reconstruction Event schema version must be explicit")
        if not self.correlation_refs or any(
            not isinstance(item, Identity) for item in self.correlation_refs
        ):
            raise ReconstructionEvidenceError("reconstruction correlation references must be explicit")
        if not self.causation_refs or any(
            not isinstance(item, Identity) for item in self.causation_refs
        ):
            raise ReconstructionEvidenceError("reconstruction causation references must be explicit")
        if not self.provenance_refs or any(
            not isinstance(item, Identity) for item in self.provenance_refs
        ):
            raise ReconstructionEvidenceError("reconstruction provenance references must be explicit")
        if len(set(self.provenance_refs)) != len(self.provenance_refs):
            raise ReconstructionEvidenceError("reconstruction provenance references must be de-duplicated")

        organization_scope = self.organization.organization_id.value
        pins = (
            self.workflow,
            *self.material_inputs,
            *self.gate_decisions,
            *self.execution_versions,
            *self.canonical_effects,
            *self.events,
        )
        governed_identities = tuple(
            identity for pin in pins for identity in (pin.subject_id, pin.version_id)
        ) + self.correlation_refs + self.causation_refs
        if any(identity.scope != organization_scope for identity in governed_identities):
            raise ReconstructionEvidenceError(
                "versioned reconstruction, correlation and causation references must share Organization scope"
            )


def _require_same_organization(
    *,
    organization: OrganizationScope,
    records: tuple[CanonicalRecord, ...],
) -> None:
    if any(record.organization != organization for record in records):
        raise ReconstructionEvidenceError(
            "all governed records used for P1.08 reconstruction must share Organization scope"
        )


def _require_execution_lineage(
    *,
    awaiting: ExecutionContext,
    ready: ExecutionContext,
    terminal: ExecutionContext,
) -> None:
    if awaiting.record.lifecycle_status != ExecutionLifecycle.AWAITING_GATE.value:
        raise ReconstructionEvidenceError("reconstruction must start from the AwaitingGate execution version")
    if ready.record.lifecycle_status != ExecutionLifecycle.READY.value:
        raise ReconstructionEvidenceError("reconstruction must include the immutable Ready execution version")
    if terminal.record.lifecycle_status != ExecutionLifecycle.SUCCEEDED.value:
        raise ReconstructionEvidenceError("reconstruction must end at the sealed Succeeded execution version")
    if not (
        awaiting.execution_subject_id
        == ready.execution_subject_id
        == terminal.execution_subject_id
    ):
        raise ReconstructionEvidenceError("all reconstructed execution versions must share one Execution Identity")
    if ready.record.predecessor_version_id != awaiting.execution_version_id:
        raise ReconstructionEvidenceError("Ready execution must preserve exact AwaitingGate predecessor lineage")
    if terminal.record.predecessor_version_id != ready.execution_version_id:
        raise ReconstructionEvidenceError("Succeeded execution must preserve exact Ready predecessor lineage")
    if len({awaiting.execution_version_id, ready.execution_version_id, terminal.execution_version_id}) != 3:
        raise ReconstructionEvidenceError("governance-significant execution versions must remain distinct")


def _require_exact_governed_inputs(
    *,
    input_record: CanonicalRecord,
    workflow: WorkflowDefinition,
    awaiting: ExecutionContext,
    ready: ExecutionContext,
    terminal: ExecutionContext,
) -> tuple[GovernedVersionPin, GovernedVersionPin]:
    workflow_pin = GovernedVersionPin.from_record(workflow.record)
    input_pin = GovernedVersionPin.from_record(input_record)
    executions = (awaiting, ready, terminal)
    if any(execution.workflow != workflow_pin for execution in executions):
        raise ReconstructionEvidenceError("every execution version must preserve the exact Workflow version pin")
    if any(execution.material_inputs != (input_pin,) for execution in executions):
        raise ReconstructionEvidenceError("every execution version must preserve the exact material input version pin")
    if not (
        awaiting.operation_name == ready.operation_name == terminal.operation_name
    ):
        raise ReconstructionEvidenceError("execution lineage must preserve one stable semantic operation")
    return workflow_pin, input_pin


def _require_gate_evidence(
    *,
    awaiting: ExecutionContext,
    ready: ExecutionContext,
    terminal: ExecutionContext,
    authorization: GateDecision,
    organizational_authority: GateDecision,
) -> tuple[GovernedVersionPin, GovernedVersionPin]:
    expected = (
        (authorization, GateKind.AUTHORIZATION),
        (organizational_authority, GateKind.ORGANIZATIONAL_AUTHORITY),
    )
    input_pin = awaiting.material_inputs[0]
    actor_id = awaiting.initiating_actor.actual_principal.principal_id

    for decision, kind in expected:
        if decision.kind is not kind:
            raise ReconstructionEvidenceError(f"reconstruction requires exact {kind.value} decision evidence")
        if decision.outcome is not GateOutcome.ALLOW:
            raise ReconstructionEvidenceError(f"reconstructed {kind.value} decision must explicitly Allow")
        if decision.subject_principal_id != actor_id:
            raise ReconstructionEvidenceError("gate decision must apply to the initiating Principal")
        if decision.execution_subject_id != awaiting.execution_subject_id:
            raise ReconstructionEvidenceError("gate decision must reference the reconstructed Execution Identity")
        if decision.evaluated_execution_version_id != awaiting.execution_version_id:
            raise ReconstructionEvidenceError("gate decision must reference the exact AwaitingGate execution version")
        if decision.workflow_version_id != awaiting.workflow.version_id:
            raise ReconstructionEvidenceError("gate decision must preserve the exact Workflow Version Identity")
        if decision.operation_name != awaiting.operation_name:
            raise ReconstructionEvidenceError("gate decision must preserve the exact reconstructed operation")
        if (
            decision.target_subject_id != input_pin.subject_id
            or decision.target_version_id != input_pin.version_id
        ):
            raise ReconstructionEvidenceError("gate decision must preserve the exact material target version")
        required_gate_provenance = {
            decision.basis_ref,
            awaiting.execution_subject_id,
            awaiting.execution_version_id,
            awaiting.workflow.version_id,
            input_pin.subject_id,
            input_pin.version_id,
        }
        if not required_gate_provenance.issubset(set(decision.record.provenance_refs)):
            raise ReconstructionEvidenceError("gate decision provenance is incomplete for bounded reconstruction")

    gate_pins = (authorization.version_pin, organizational_authority.version_pin)
    if ready.gate_decisions != gate_pins or terminal.gate_decisions != gate_pins:
        raise ReconstructionEvidenceError(
            "Ready and Succeeded execution versions must preserve the two exact gate decision pins"
        )
    return gate_pins


def _require_mutation_evidence(
    *,
    input_record: CanonicalRecord,
    workflow_pin: GovernedVersionPin,
    ready: ExecutionContext,
    mutation: CanonicalMutationResult,
    gate_pins: tuple[GovernedVersionPin, GovernedVersionPin],
) -> GovernedVersionPin:
    input_pin = GovernedVersionPin.from_record(input_record)
    if mutation.previous_version != input_pin:
        raise ReconstructionEvidenceError("mutation must preserve the exact material predecessor version")
    if mutation.execution.record.predecessor_version_id != ready.execution_version_id:
        raise ReconstructionEvidenceError("terminal mutation execution must descend from the exact Ready version")

    result = mutation.resulting_record
    result_pin = GovernedVersionPin.from_record(result)
    if result.subject_id != input_record.subject_id:
        raise ReconstructionEvidenceError("canonical mutation result must preserve the target Subject Identity")
    if result.predecessor_version_id != input_record.version_id:
        raise ReconstructionEvidenceError("canonical mutation result must preserve exact predecessor lineage")
    if mutation.execution.canonical_effects != (result_pin,):
        raise ReconstructionEvidenceError("terminal execution must pin the exact resulting canonical version")

    required_result_provenance = {
        input_record.subject_id,
        input_record.version_id,
        ready.execution_subject_id,
        ready.execution_version_id,
        workflow_pin.subject_id,
        workflow_pin.version_id,
        *(identity for pin in gate_pins for identity in (pin.subject_id, pin.version_id)),
    }
    if not required_result_provenance.issubset(set(result.provenance_refs)):
        raise ReconstructionEvidenceError("result provenance is incomplete for bounded reconstruction")

    required_terminal_provenance = {
        input_record.subject_id,
        input_record.version_id,
        result.subject_id,
        result.version_id,
        workflow_pin.subject_id,
        workflow_pin.version_id,
        *(identity for pin in gate_pins for identity in (pin.subject_id, pin.version_id)),
    }
    if not required_terminal_provenance.issubset(set(mutation.execution.record.provenance_refs)):
        raise ReconstructionEvidenceError("terminal execution provenance is incomplete for bounded reconstruction")
    return result_pin


def _require_event_evidence(
    *,
    event: CanonicalEvent,
    terminal: ExecutionContext,
    result_pin: GovernedVersionPin,
) -> GovernedVersionPin:
    actor_id = terminal.initiating_actor.actual_principal.principal_id
    if event.execution_subject_id != terminal.execution_subject_id:
        raise ReconstructionEvidenceError("Event must preserve the exact Execution Subject Identity")
    if event.execution_version_id != terminal.execution_version_id:
        raise ReconstructionEvidenceError("Event must preserve the exact terminal Execution Context version")
    if event.related_subject_ids != (result_pin.subject_id,):
        raise ReconstructionEvidenceError("Event must preserve the exact resulting Subject Identity")
    if event.related_version_ids != (result_pin.version_id,):
        raise ReconstructionEvidenceError("Event must preserve the exact resulting Version Identity")
    if event.correlation_refs != (terminal.execution_subject_id,):
        raise ReconstructionEvidenceError(
            "P1.08 correlation must identify the stable Execution Identity without asserting causation"
        )
    if event.causation_refs != (terminal.execution_version_id,):
        raise ReconstructionEvidenceError(
            "P1.08 causation must identify the exact terminal execution version that caused the Event"
        )
    if event.producer_id != actor_id or event.initiating_actor_id != actor_id:
        raise ReconstructionEvidenceError("Event attribution must preserve the initiating Principal")
    if event.event_type != "platform.canonical-mutation.succeeded":
        raise ReconstructionEvidenceError("P1.08 bounded Event type must describe successful canonical mutation")
    if event.event_schema_version != "1":
        raise ReconstructionEvidenceError("P1.08 bounded Event schema version must remain explicit")
    expected_payload = (
        ("operation", terminal.operation_name),
        ("outcome", ExecutionLifecycle.SUCCEEDED.value),
    )
    if event.record.payload != expected_payload:
        raise ReconstructionEvidenceError("Event payload must preserve the reconstructed operation outcome")
    required_event_provenance = {
        actor_id,
        terminal.execution_subject_id,
        terminal.execution_version_id,
        result_pin.subject_id,
        result_pin.version_id,
    }
    if not required_event_provenance.issubset(set(event.record.provenance_refs)):
        raise ReconstructionEvidenceError("Event provenance is incomplete for bounded reconstruction")
    return GovernedVersionPin.from_record(event.record)


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
    """Validate and expose the exact immutable evidence graph for P1.06/P1.07.

    This function is observational only. It neither executes nor replays the
    mutation, emits/admit Events, updates canonical history, resolves a mutable
    projection, nor creates an Observation/Knowledge object.
    """

    if not isinstance(input_record, CanonicalRecord):
        raise ReconstructionEvidenceError("P1.08 requires the exact initial Canonical Record version")
    if not isinstance(workflow, WorkflowDefinition):
        raise ReconstructionEvidenceError("P1.08 requires the exact Workflow definition")
    if not all(
        isinstance(execution, ExecutionContext)
        for execution in (awaiting_execution, ready_execution, mutation.execution)
    ):
        raise ReconstructionEvidenceError("P1.08 requires exact Execution Context versions")
    if not isinstance(authorization, GateDecision) or not isinstance(
        organizational_authority, GateDecision
    ):
        raise ReconstructionEvidenceError("P1.08 requires explicit governed gate decision evidence")
    if not isinstance(mutation, CanonicalMutationResult):
        raise ReconstructionEvidenceError("P1.08 requires the exact P1.06 mutation result")
    if not isinstance(event, CanonicalEvent):
        raise ReconstructionEvidenceError("P1.08 requires the exact admitted P1.07 canonical Event")

    terminal_execution = mutation.execution
    organization = input_record.organization
    _require_same_organization(
        organization=organization,
        records=(
            input_record,
            workflow.record,
            awaiting_execution.record,
            authorization.record,
            organizational_authority.record,
            ready_execution.record,
            mutation.resulting_record,
            terminal_execution.record,
            event.record,
        ),
    )
    _require_execution_lineage(
        awaiting=awaiting_execution,
        ready=ready_execution,
        terminal=terminal_execution,
    )
    workflow_pin, input_pin = _require_exact_governed_inputs(
        input_record=input_record,
        workflow=workflow,
        awaiting=awaiting_execution,
        ready=ready_execution,
        terminal=terminal_execution,
    )

    actor_id = awaiting_execution.initiating_actor.actual_principal.principal_id
    if (
        ready_execution.initiating_actor.actual_principal.principal_id != actor_id
        or terminal_execution.initiating_actor.actual_principal.principal_id != actor_id
    ):
        raise ReconstructionEvidenceError("execution lineage must preserve the initiating Principal")

    gate_pins = _require_gate_evidence(
        awaiting=awaiting_execution,
        ready=ready_execution,
        terminal=terminal_execution,
        authorization=authorization,
        organizational_authority=organizational_authority,
    )
    result_pin = _require_mutation_evidence(
        input_record=input_record,
        workflow_pin=workflow_pin,
        ready=ready_execution,
        mutation=mutation,
        gate_pins=gate_pins,
    )
    event_pin = _require_event_evidence(
        event=event,
        terminal=terminal_execution,
        result_pin=result_pin,
    )

    awaiting_pin = GovernedVersionPin.from_record(awaiting_execution.record)
    ready_pin = GovernedVersionPin.from_record(ready_execution.record)
    terminal_pin = GovernedVersionPin.from_record(terminal_execution.record)

    provenance_refs = _ordered_unique(
        (
            actor_id,
            workflow_pin.subject_id,
            workflow_pin.version_id,
            input_pin.subject_id,
            input_pin.version_id,
            authorization.record.subject_id,
            authorization.record.version_id,
            authorization.basis_ref,
            organizational_authority.record.subject_id,
            organizational_authority.record.version_id,
            organizational_authority.basis_ref,
            awaiting_pin.subject_id,
            awaiting_pin.version_id,
            ready_pin.version_id,
            terminal_pin.version_id,
            result_pin.subject_id,
            result_pin.version_id,
            event_pin.subject_id,
            event_pin.version_id,
        )
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
