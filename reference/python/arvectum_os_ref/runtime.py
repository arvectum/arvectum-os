"""P2.01 historical reference-composition compatibility boundary.

R3 disposition (2026-08-08): this module is retained to preserve the executable
Phase 1/P2.01 regression evidence, but it is **not** the reusable Phase 2 Core
Runtime entry point.  The P2.09 second-workflow proof demonstrated that genuine
reuse occurs through the domain-neutral semantic owners introduced later in
Phase 2, especially P2.04 Governed Execution and P2.07 Product Contract entry.

The request/result shape below intentionally remains limited to the original P1
canonical-mutation scenario: one material input, Authorization plus
Organizational Authority decisions, one canonical successor, one Event,
reconstruction evidence and one unvalidated Observation.  New workflows MUST
NOT extend this compatibility shape merely to make it look general; they should
compose the reusable semantic owners appropriate to their declared effects and
gates.

The boundary remains internal, provisional and reference-only.  It does not
select persistence, a workflow engine, broker, IAM provider, service topology,
public API/SDK or a durable serialization contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .canonical import CanonicalRecord
from .events import CanonicalEvent, EventAdmissionResult, EventCandidate
from .execution import ExecutionContext
from .gates import GateDecision, GateKind, GateOutcome
from .identity import Identity
from .mutation import CanonicalMutationResult
from .observation import Observation
from .provenance import ReconstructionEvidence
from .security import ActorContext, OrganizationScope
from .workflow import WorkflowDefinition


StartExecution = Callable[..., ExecutionContext]
BuildGateDecision = Callable[..., GateDecision]
AdmitReadyExecution = Callable[..., ExecutionContext]
ExecuteCanonicalMutation = Callable[..., CanonicalMutationResult]
BuildEventCandidate = Callable[..., EventCandidate]
AdmitEvent = Callable[..., EventAdmissionResult]
BuildReconstructionEvidence = Callable[..., ReconstructionEvidence]
BuildObservation = Callable[..., Observation]


@dataclass(frozen=True, slots=True)
class RuntimeOperations:
    """Reference-compatibility adapters used by the historical P2.01 composition.

    R3 explicitly rejects this callable bundle as a generalized plugin or Core
    Runtime extension contract.  It remains only so the already-proven P1/P2.01
    scenario can keep its explicit reference binding without rewriting history.
    """

    start_execution: StartExecution
    build_gate_decision: BuildGateDecision
    admit_ready_execution: AdmitReadyExecution
    execute_canonical_mutation: ExecuteCanonicalMutation
    build_event_candidate: BuildEventCandidate
    admit_event: AdmitEvent
    build_reconstruction_evidence: BuildReconstructionEvidence
    build_observation: BuildObservation


@dataclass(frozen=True, slots=True)
class RuntimeExecutionRequest:
    """Scenario-specific request retained for P1/P2.01 regression evidence.

    Deterministic fixture construction is intentionally outside this type.  The
    caller supplies the exact inputs required by the original P1 canonical
    mutation path.  R3 intentionally does not add variable gate sets, multiple
    material inputs, Product Contract declarations or external/commitment effect
    semantics to this compatibility request; those belong to the reusable Phase
    2 semantic owners already exercised by P2.09.
    """

    organization: OrganizationScope
    actor: ActorContext
    decision_actor: ActorContext
    workflow: WorkflowDefinition
    material_input: CanonicalRecord
    authorization_basis_ref: Identity
    organizational_authority_basis_ref: Identity
    new_version_id: Identity
    new_payload: tuple[tuple[str, str], ...]
    authorization_outcome: GateOutcome = GateOutcome.ALLOW
    organizational_authority_outcome: GateOutcome = GateOutcome.ALLOW

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("runtime request Organization scope must be explicit")
        if not isinstance(self.actor, ActorContext) or not isinstance(
            self.decision_actor, ActorContext
        ):
            raise ValueError("runtime request actors must be attributable ActorContext values")
        if self.actor.organization != self.organization:
            raise ValueError("runtime actor must share the request Organization scope")
        if self.decision_actor.organization != self.organization:
            raise ValueError("runtime decision actor must share the request Organization scope")
        if not isinstance(self.workflow, WorkflowDefinition):
            raise ValueError("runtime request must supply an exact Workflow definition")
        if self.workflow.organization != self.organization:
            raise ValueError("runtime Workflow must share the request Organization scope")
        if not isinstance(self.material_input, CanonicalRecord):
            raise ValueError("runtime request must supply an exact material Canonical Record")
        if self.material_input.organization != self.organization:
            raise ValueError("runtime material input must share the request Organization scope")
        for label, reference in (
            ("authorization basis", self.authorization_basis_ref),
            ("Organizational Authority basis", self.organizational_authority_basis_ref),
            ("new canonical Version Identity", self.new_version_id),
        ):
            if not isinstance(reference, Identity):
                raise ValueError(f"{label} must be an explicit Identity")
            if reference.scope != self.organization.organization_id.value:
                raise ValueError(f"{label} must share the request Organization scope")
        if not isinstance(self.authorization_outcome, GateOutcome):
            raise ValueError("Authorization outcome must be explicit")
        if not isinstance(self.organizational_authority_outcome, GateOutcome):
            raise ValueError("Organizational Authority outcome must be explicit")
        if not isinstance(self.new_payload, tuple):
            raise ValueError("new canonical payload must be an immutable tuple")


@dataclass(frozen=True, slots=True)
class RuntimeExecutionResult:
    """Scenario-specific evidence returned by the historical P1/P2.01 path."""

    awaiting_execution: ExecutionContext
    authorization: GateDecision
    organizational_authority: GateDecision
    ready_execution: ExecutionContext
    mutation: CanonicalMutationResult
    event_admission: EventAdmissionResult
    reconstruction: ReconstructionEvidence
    observation: Observation

    def __post_init__(self) -> None:
        if not isinstance(self.awaiting_execution, ExecutionContext):
            raise ValueError("runtime result must preserve AwaitingGate execution evidence")
        if not isinstance(self.authorization, GateDecision) or not isinstance(
            self.organizational_authority, GateDecision
        ):
            raise ValueError("runtime result must preserve separate governed gate decisions")
        if not isinstance(self.ready_execution, ExecutionContext):
            raise ValueError("runtime result must preserve Ready execution evidence")
        if not isinstance(self.mutation, CanonicalMutationResult):
            raise ValueError("runtime result must preserve canonical mutation evidence")
        if not isinstance(self.event_admission, EventAdmissionResult):
            raise ValueError("runtime result must preserve canonical Event admission evidence")
        if not isinstance(self.reconstruction, ReconstructionEvidence):
            raise ValueError("runtime result must preserve reconstruction evidence")
        if not isinstance(self.observation, Observation):
            raise ValueError("runtime result must preserve the unvalidated Observation")

        organization = self.awaiting_execution.organization
        governed_organizations = (
            self.authorization.record.organization,
            self.organizational_authority.record.organization,
            self.ready_execution.organization,
            self.mutation.resulting_record.organization,
            self.mutation.execution.organization,
            self.event_admission.event.record.organization,
            self.reconstruction.organization,
            self.observation.record.organization,
        )
        if any(item != organization for item in governed_organizations):
            raise ValueError("runtime result evidence must remain within one Organization scope")

    @property
    def event(self) -> CanonicalEvent:
        return self.event_admission.event


@dataclass(frozen=True, slots=True)
class RuntimeComposition:
    """Historical P1/P2.01 reference composition retained for compatibility evidence.

    The caller still selects an explicit ``RuntimeOperations`` adapter set, as
    established by R1.  R3 clarifies that this composition is not the reusable
    Core Runtime orchestrator and MUST NOT be expanded to absorb the materially
    different P2.09 workflow.  New reuse should occur through the semantic
    runtime boundaries introduced by P2.02–P2.08, especially Product Contract
    validation plus Governed Execution for product/platform interaction.
    """

    operations: RuntimeOperations

    def __post_init__(self) -> None:
        if not isinstance(self.operations, RuntimeOperations):
            raise TypeError("runtime composition requires explicit RuntimeOperations")

    def execute(self, request: RuntimeExecutionRequest) -> RuntimeExecutionResult:
        if not isinstance(request, RuntimeExecutionRequest):
            raise TypeError("runtime composition requires a RuntimeExecutionRequest")

        awaiting = self.operations.start_execution(
            organization=request.organization,
            actor=request.actor,
            workflow=request.workflow,
            material_input=request.material_input,
        )
        authorization = self.operations.build_gate_decision(
            execution=awaiting,
            kind=GateKind.AUTHORIZATION,
            outcome=request.authorization_outcome,
            decision_actor=request.decision_actor,
            basis_ref=request.authorization_basis_ref,
        )
        organizational_authority = self.operations.build_gate_decision(
            execution=awaiting,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=request.organizational_authority_outcome,
            decision_actor=request.decision_actor,
            basis_ref=request.organizational_authority_basis_ref,
        )
        ready = self.operations.admit_ready_execution(
            execution=awaiting,
            authorization=authorization,
            organizational_authority=organizational_authority,
        )
        mutation = self.operations.execute_canonical_mutation(
            execution=ready,
            workflow=request.workflow,
            authorization=authorization,
            organizational_authority=organizational_authority,
            current_record=request.material_input,
            new_version_id=request.new_version_id,
            new_payload=request.new_payload,
        )
        candidate = self.operations.build_event_candidate(mutation=mutation)
        event_admission = self.operations.admit_event(
            candidate=candidate,
            mutation=mutation,
        )
        reconstruction = self.operations.build_reconstruction_evidence(
            input_record=request.material_input,
            workflow=request.workflow,
            awaiting_execution=awaiting,
            authorization=authorization,
            organizational_authority=organizational_authority,
            ready_execution=ready,
            mutation=mutation,
            event=event_admission.event,
        )
        observation = self.operations.build_observation(
            evidence=reconstruction,
            event=event_admission.event,
            mutation=mutation,
        )
        return RuntimeExecutionResult(
            awaiting_execution=awaiting,
            authorization=authorization,
            organizational_authority=organizational_authority,
            ready_execution=ready,
            mutation=mutation,
            event_admission=event_admission,
            reconstruction=reconstruction,
            observation=observation,
        )
