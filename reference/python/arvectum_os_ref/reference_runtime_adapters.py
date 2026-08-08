"""Reference-only adapters for the historical P2.01 compatibility composition.

R1 moved this binding out of ``runtime.py`` so the P2.01 composition did not
silently select the Phase 1 implementation.  R3 subsequently established, using
the materially distinct P2.09 workflows, that this adapter bundle is not the
reusable Phase 2 Core Runtime seam.  It remains only to preserve bounded
Phase 1/P2.01 regression evidence.

New workflows MUST NOT use this module as a platform plugin or generalized
runtime-extension interface.  Genuine Phase 2 reuse occurs through the later
domain-neutral semantic owners such as Product Contract validation, Governed
Execution, Event/provenance and runtime consistency.
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
    """Bind the bounded Phase 1 implementations for regression evidence only.

    This factory is reference infrastructure, not a default platform runtime,
    plugin interface, stable SDK surface or cross-product contract.
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
