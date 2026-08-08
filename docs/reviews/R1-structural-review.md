# R1 — Structural Review

Status: `Complete`
Date: `2026-08-08`
Task classification: `platform`
Engineering gate: `R1`
Trigger: after `P2.01`, before substantive `P2.02`
Constitution: `1.2.0` (`Ratified`)
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Engineering-quality decision: [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md)
Phase 2 roadmap: [`PHASE-2-CORE-RUNTIME.md`](../roadmap/PHASE-2-CORE-RUNTIME.md)
Predecessor implementation: `P2.01 — Runtime boundary extraction and reusable composition baseline`
Review PR: `#19 — R1: Structural Review after P2.01`

## 1. Purpose and scope

R1 reviews the first reusable runtime extraction before further Core Runtime semantics accumulate around it.

The canonical scope is intentionally structural rather than performance-oriented:

- runtime / reference-fixture / test boundaries;
- scenario-specific leakage into reusable runtime code;
- dependency direction and cycles;
- duplicated orchestration;
- accidental internal APIs;
- obsolete P1-only structure where removal is evidence-backed;
- adapter and package-topology reversibility;
- behavior preservation through executable tests.

R1 does not implement P2.02 Head / Effective Version semantics and does not select persistence, transaction, broker, IAM/policy, workflow-engine, service-topology, public API/SDK or durable serialization technology.

## 2. Canonical checks

The review was performed against:

- Constitution `1.2.0`;
- RFC Index with RFC-0001 through RFC-0008 `1.0.0` recorded as `Accepted`;
- RFC-0001 `Arvectum OS Architecture`;
- RFC-0002 `Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability`;
- RFC-0005 `Governed Execution and Workflow Model`;
- RFC-0006 `Event, Provenance and Observability Model`;
- RFC-0007 `Memory, Knowledge and Governed Learning Lifecycle`;
- the approved Engineering Quality and Refactoring Gates decision;
- the P2.01 implementation, tests and roadmap evidence.

RFC-0004 and RFC-0008 remain part of the Accepted baseline, but R1 introduces no real product/platform reliance and no document/artifact runtime contract requiring additional implementation work from those RFCs.

No relevant Accepted ADR constrains this bounded in-memory, non-public structural refactoring.

## 3. Review result

**Result: `PASS — R1 completed for the P2.01 structural scope.`**

P2.02 may proceed after this review is merged and canonical roadmap state is synchronized.

The review found one material structural issue in the P2.01 extraction and remediated it. Remaining P1 fixture specificity is now contained behind an explicit reference-adapter boundary and is not a blocker for P2.02.

## 4. Findings and dispositions

| ID | Finding | Severity | Disposition |
|---|---|---:|---|
| `R1-F1` | `RuntimeComposition` selected historical P1 semantic helpers through a default adapter factory inside `runtime.py`. This made reusable runtime orchestration own a scenario-era implementation binding. | Material | **Resolved.** The P1 binding moved to `reference_runtime_adapters.py`; `RuntimeComposition` now requires explicit `RuntimeOperations`. |
| `R1-F2` | P1 semantic helper implementations still contain deterministic reference IDs/timestamps such as the `reference-subject-maintenance-execution-1-*` lineage. | Medium | **Contained / non-blocking.** These remain reference-only adapter behavior. R1 does not generalize P2.04/P2.05 semantics prematurely. |
| `R1-F3` | The package root `arvectum_os_ref.__init__` re-exports multiple P1 helper functions/types and therefore resembles an API surface. | Low | **Accepted for current harness.** The package is explicitly provisional/non-public and Phase 1 tests rely on this convenience surface. Do not treat it as a stable cross-product contract; review again at R3 or an earlier stable-boundary gate. |
| `R1-F4` | Potential dependency cycles after runtime extraction. | — | **No material cycle found.** Dependency direction remains from foundational value/governed types toward higher orchestration/evidence layers; the reference scenario sits above runtime composition and explicit reference adapters. |
| `R1-F5` | Potential duplicated orchestration between scenario and runtime. | — | **No duplicate orchestration remains.** The scenario builds deterministic inputs and delegates once; the P1.04–P1.09 sequence is owned by `RuntimeComposition`. |
| `R1-F6` | Potential obsolete P1-only modules after P2.01 extraction. | — | **No removal justified yet.** P1 modules remain executable evidence for M1 and are still used by the explicit reference adapter set and regression tests. Removing them now would reduce evidence and increase migration churn without demonstrated value. |
| `R1-F7` | Potential ADR trigger from the structural refactor. | — | **No ADR required.** No stable/public interface, durable dependency, material migration commitment or technology selection is introduced. |
| `R1-F8` | Performance optimization opportunity. | — | **Not pursued by design.** R1 found no measured or correctness/security-relevant performance issue; the approved gate decision makes performance optimization out of scope here. |

## 5. Structural remediation

### 5.1 Explicit reference adapter layer

Added:

- `reference/python/arvectum_os_ref/reference_runtime_adapters.py`.

The module explicitly binds the bounded P1 semantic implementations into `RuntimeOperations` for reference-fixture use only.

It is not a default platform runtime, plugin interface, stable SDK surface or Product Contract.

### 5.2 Runtime composition no longer selects P1 implementation

Updated:

- `reference/python/arvectum_os_ref/runtime.py`.

`RuntimeComposition` now requires an explicit `RuntimeOperations` instance. The reusable runtime module no longer imports or binds:

- `start_p1_04_execution`;
- `build_p1_05_gate_decision`;
- `admit_p1_05_ready_execution`;
- `execute_p1_06_canonical_mutation`;
- `build_p1_07_event_candidate`;
- `admit_p1_07_event`;
- `build_p1_08_reconstruction_evidence`;
- `build_p1_09_observation`.

This preserves orchestration ownership while preventing the provisional Core Runtime composition root from silently treating P1 helper layout as its default implementation contract.

### 5.3 Reference scenario owns reference binding

Updated:

- `reference/python/arvectum_os_ref/reference_scenario.py`.

The deterministic scenario still owns Organization/Actor fixtures, initial record/workflow construction, governed basis references and successor payload. It now also explicitly selects `reference_runtime_operations()` when no custom runtime is supplied.

The scenario continues to delegate governed execution exactly once through `RuntimeComposition`.

### 5.4 Structural fitness evidence

Updated:

- `reference/python/tests/test_p2_01_runtime_composition.py`.

Added executable checks that:

1. `RuntimeComposition` cannot be instantiated without an explicit adapter set;
2. reusable `runtime.py` does not bind historical P1 operation functions or import the reference adapter/scenario modules.

Existing P2.01 boundary, exact-version, authority, Event/provenance, Observation and fail-closed tests remain intact.

## 6. Dependency review

The reviewed bounded dependency direction is:

```text
Identity
  ↓
Organization / Actor context
  ↓
Canonical Record envelope
  ↓
Workflow / Execution governed types
  ↓
Gate / Mutation / Event / Provenance / Observation semantics
  ↓
reference_runtime_adapters  ── binds current P1 implementations
             ↓
        RuntimeComposition  ── owns orchestration, requires explicit operations
             ↑
      reference_scenario    ── owns deterministic fixture setup and binding choice
             ↓
     portability / fitness evidence
```

The diagram describes the bounded reference implementation structure, not a permanent package/service topology.

No product-domain module enters the shared runtime boundary.

## 7. Behavior-preservation evidence

GitHub Actions verification for the R1 executable code head `e0c71c1c80b658711a7420ffb7d59248ce741fb8`:

- workflow: `Reference Python CI`;
- run: `#23`;
- job: `Full reference test suite`;
- command: `python -m unittest discover -s tests -v`;
- result: `Ran 140 tests in 0.257s` / `OK`;
- conclusion: `success`.

The two additional tests are structural fitness checks introduced by R1. All previous P1/P2.01 behavioral tests continue to pass.

## 8. Architecture and governance disposition

R1 remains compatible with Constitution `1.2.0` and the Accepted RFC baseline because it reduces accidental coupling while preserving:

- explicit Organization scope;
- exact immutable Version Identity reliance;
- separate Authorization and Organizational Authority evidence;
- Governed Execution before consequential canonical mutation;
- immutable execution and canonical-state lineage;
- Event receipt/admission and reconstruction semantics;
- Observation non-promotion to Knowledge;
- non-authoritative portability/projection behavior;
- technology and package-topology reversibility.

R1 does not:

- amend the Constitution or any Accepted RFC;
- create a Product Contract;
- activate a Platform Capability;
- establish production readiness or full-platform conformance;
- establish a stable public/cross-product API;
- select persistence, broker, IAM/policy, workflow-engine or deployment technology;
- establish SLA/support/commercial commitments.

No new RFC, ADR, policy or Product Contract is required for the R1 remediation itself.

## 9. Carried-forward structural debt

The following items are intentionally not resolved by R1:

1. P1 helper implementations retain deterministic reference identifiers/timestamps. They are now contained behind `reference_runtime_adapters.py` and must not be mistaken for generalized runtime identity/time allocation semantics.
2. The package-root P1 re-export surface remains provisional/non-public and should not become a cross-product dependency. Revisit at R3 or sooner if a stable-boundary trigger appears.
3. P2.04 remains responsible for genuinely reusable Governed Execution/gate lifecycle semantics rather than merely renaming P1 helpers.
4. P2.05 remains responsible for genuinely reusable Event/provenance/reconstruction runtime semantics.
5. P2.09/R3 must use evidence from a second materially distinct workflow before deciding which abstractions are truly reusable.

These are bounded future-work constraints, not blockers for P2.02.

## 10. Exit decision

R1 exit conditions are satisfied:

- runtime / fixture / test boundaries reviewed;
- scenario-specific runtime binding detected and removed from reusable runtime core;
- dependency direction reviewed with no material cycle;
- duplicated orchestration not present;
- accidental public/stable API risk reviewed and contained;
- no P1 module removal justified by evidence;
- adapter/package topology remains reversible;
- behavior preserved by 140 passing tests;
- no ADR gate crossed.

**R1 is complete.**

Next canonical implementation action after roadmap synchronization:

> `P2.02 — Canonical Record lineage, Head and Effective Version runtime`.
