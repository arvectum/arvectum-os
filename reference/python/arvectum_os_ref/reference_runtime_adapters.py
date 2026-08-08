"""Reference-only adapters for the provisional Core Runtime composition.

This module is the explicit boundary between the reusable P2 runtime
composition and the bounded Phase 1 semantic implementations.  The adapter set
is intentionally internal, reversible and non-public.  It may be replaced as
Phase 2 generalizes individual runtime responsibilities.

Keeping this binding outside ``runtime.py`` prevents the reusable composition
root from selecting historical P1 fixture implementations by default while
preserving the already-proven behavior of the reference scenario.
"""

from __future__ import annotations

from .events import admit_p1_07_event, build_p1_07_event_candidate
from .execution import start_p1_04_execution
from .gates import admit_p1_05_ready_execution, build_p1_05_gate_decision
from .mutation import execute_p1_06_canonical_mutation
from .observation import build_p1_09_observation
from .provenance import build_p1_08_reconstruction_evidence
from .runtime import RuntimeOperations


def reference_runtime_operations() -> RuntimeOperations:
    """Bind the bounded Phase 1 semantic implementations explicitly.

    This factory is fixture/reference infrastructure, not a default platform
    runtime, plugin interface, stable SDK surface or cross-product contract.
    """

    return RuntimeOperations(
        start_execution=start_p1_04_execution,
        build_gate_decision=build_p1_05_gate_decision,
        admit_ready_execution=admit_p1_05_ready_execution,
        execute_canonical_mutation=execute_p1_06_canonical_mutation,
        build_event_candidate=build_p1_07_event_candidate,
        admit_event=admit_p1_07_event,
        build_reconstruction_evidence=build_p1_08_reconstruction_evidence,
        build_observation=build_p1_09_observation,
    )
