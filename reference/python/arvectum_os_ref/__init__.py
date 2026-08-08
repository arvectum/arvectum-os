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
    "OperationSideEffectClass",
    "OrganizationScope",
    "Principal",
    "WorkflowDefinition",
    "WorkflowLifecycle",
    "WorkflowOperation",
    "admit_p1_05_ready_execution",
    "admit_p1_07_event",
    "build_p1_02_native_record",
    "build_p1_03_workflow",
    "build_p1_05_gate_decision",
    "build_p1_07_event_candidate",
    "evaluate_p1_05_gates",
    "execute_p1_06_canonical_mutation",
    "start_p1_04_execution",
]
