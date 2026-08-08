"""Bounded Arvectum OS reference implementation harness.

This package is intentionally provisional and is not a public platform contract.
"""

from .canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from .events import (
    CanonicalEvent,
    EventAdmissionResult,
    EventCandidate,
    EventIdentityConflictError,
    admit_p1_07_event,
    build_p1_07_event_candidate,
)
from .execution import (
    ExecutionContext,
    ExecutionLifecycle,
    GovernedVersionPin,
    start_p1_04_execution,
)
from .fitness import (
    ProjectionAuthorityError,
    ProjectionEntry,
    ProjectionSnapshot,
    ReplayProjectionError,
    pin_p1_11_projection_source,
    rebuild_p1_11_projection,
)
from .gates import (
    GateDecision,
    GateEvaluation,
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
    evaluate_p1_05_gates,
)
from .identity import Identity
from .mutation import (
    CanonicalConflictError,
    CanonicalMutationResult,
    execute_p1_06_canonical_mutation,
)
from .observation import (
    KnowledgePromotionRequiredError,
    Observation,
    ObservationCreationError,
    ObservationEpistemicStatus,
    build_p1_09_observation,
    require_explicit_knowledge_promotion,
)
from .portability import (
    PortableFixtureExportError,
    PortableSemanticFixture,
    export_p1_10_semantic_fixture,
)
from .provenance import (
    ReconstructionEvidence,
    ReconstructionEvidenceError,
    build_p1_08_reconstruction_evidence,
)
from .security import ActorContext, OrganizationScope, Principal
from .workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
    build_p1_03_workflow,
)

__all__ = [
    "ActorContext",
    "AuthorityMode",
    "CanonicalConflictError",
    "CanonicalEvent",
    "CanonicalMutationResult",
    "CanonicalRecord",
    "EventAdmissionResult",
    "EventCandidate",
    "EventIdentityConflictError",
    "ExecutionContext",
    "ExecutionLifecycle",
    "GateDecision",
    "GateEvaluation",
    "GateKind",
    "GateOutcome",
    "GovernedVersionPin",
    "Identity",
    "KnowledgePromotionRequiredError",
    "Observation",
    "ObservationCreationError",
    "ObservationEpistemicStatus",
    "OperationSideEffectClass",
    "OrganizationScope",
    "PortableFixtureExportError",
    "PortableSemanticFixture",
    "Principal",
    "ProjectionAuthorityError",
    "ProjectionEntry",
    "ProjectionSnapshot",
    "ReconstructionEvidence",
    "ReconstructionEvidenceError",
    "ReplayProjectionError",
    "WorkflowDefinition",
    "WorkflowLifecycle",
    "WorkflowOperation",
    "admit_p1_05_ready_execution",
    "admit_p1_07_event",
    "build_p1_02_native_record",
    "build_p1_03_workflow",
    "build_p1_05_gate_decision",
    "build_p1_07_event_candidate",
    "build_p1_08_reconstruction_evidence",
    "build_p1_09_observation",
    "evaluate_p1_05_gates",
    "execute_p1_06_canonical_mutation",
    "export_p1_10_semantic_fixture",
    "pin_p1_11_projection_source",
    "rebuild_p1_11_projection",
    "require_explicit_knowledge_promotion",
    "start_p1_04_execution",
]
