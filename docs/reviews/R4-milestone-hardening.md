# R4 — Milestone Hardening

Status: `Complete`
Date: `2026-08-08`
Gate: `R4 — Milestone Hardening`
Task classification: `platform`
Trigger: after final applicable `P2.10` evidence, before `P2.11` / `P2.12`
Result: **`PASS — Phase 2 semantic-owner runtime is hardened for the declared M2 reference scope; no material defect or new ADR trigger remains open.`**

## 1. Scope

R4 is the final full Phase 2 code-health review before the ADR/runtime-boundary review and the M2 closure decision.

The review covers the complete semantic-owner runtime accumulated through P2.02–P2.09 and the P2.10 fitness matrix, with emphasis on:

- architecture and dependency boundaries;
- correctness and invariant preservation;
- security, privacy, Organization isolation and authority semantics;
- maintainability and accidental API/extension pressure;
- executable evidence quality;
- migration and reversibility;
- performance only where reproducible evidence demonstrates a material problem;
- previously carried R2/R3 debt that could have become material by the final Phase 2 code head.

R4 is an engineering checkpoint. It does not amend an Accepted RFC, create an ADR by itself, establish a stable public API/SDK, activate a Platform Capability, claim production readiness or establish full-platform conformance.

## 2. Canonical authority checked

R4 was performed against the canonical repository state and the following higher-authority material:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index;
- RFC-0001 through RFC-0008 `1.0.0` — `Accepted`;
- `DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES` — `Approved`;
- R1 Structural Review;
- R2 Runtime Health Review;
- R3 Reuse Refactoring Review;
- P2.10 Core Runtime Architecture Fitness Matrix;
- current Phase 2 and root roadmaps;
- current reference Python implementation and tests.

No conflict with the Constitution or Accepted RFC baseline was found.

No relevant Accepted ADR currently constrains the bounded in-memory reference implementation. Existing ADR gates for durable persistence/transactions/concurrency, Event delivery, IAM/enforcement, durable replay/projection storage, stable serialization/public interfaces and service topology remain uncrossed.

## 3. Review result

**Result: `PASS`.**

The final Phase 2 semantic-owner structure remains coherent:

```text
Canonical Record / Canonical Lineage
        ├── Typed Relationship runtime
        ├── Governed Execution runtime
        └── Runtime Consistency state

Product Contract validation
        ↓
Governed Execution
        ↓
consequential admission
        ├── canonical mutation + Event/provenance path
        └── external consequence / commitment path

Portability package / reconstruction
        ↓
non-authoritative projection only
```

The historical P2.01 `RuntimeComposition` remains compatibility evidence only and is not the demonstrated reusable Core Runtime boundary.

No competing lineage, execution, Event-admission, Product Contract or idempotency engine was found. No product-domain behavior was found in the shared semantic-owner runtime. No durable infrastructure or stable public-interface choice has entered the bounded runtime.

## 4. Findings and dispositions

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| `R4-F1` | Pass | P2.02–P2.08 semantic-owner modules do not depend on historical P2.01 `runtime.py`, `reference_runtime_adapters.py` or `reference_scenario.py`. | Added an executable dependency guard. Preserve R3 disposition. |
| `R4-F2` | Low / boundary hygiene | Package-root `__init__.py` still exposes historical P1 convenience symbols, but explicitly declares the package provisional and not a public platform contract. P2 semantic-owner types are not promoted through that root surface. | No churn-only pruning. Added a regression guard preventing accidental P2/public-surface promotion. Revisit only before a real stable public/cross-product boundary. |
| `R4-F3` | Medium, bounded | R2/R3 carried `RuntimeConsistencyState` aggregate-admission debt remains real for arbitrary durable/deserialized snapshots, but Phase 2 still has no persistence/deserialization/public-state boundary and the type is not package-root exported. | Not material within M2 reference scope. Keep internal/non-durable status explicit and guarded. P2.11 must treat any future durable/deserialization reliance as an ADR/runtime-boundary trigger before use. |
| `R4-F4` | Security/reversibility pass | Shared runtime modules do not import process execution, network clients, unsafe object-deserialization mechanisms or multiprocessing facilities. | Added executable AST guards. No runtime mechanism added. |
| `R4-F5` | Authority pass | No shared runtime helper auto-approves/bypasses gates or creates an `allow_all_gates`-style authority shortcut. | Added an executable guard. Test-only explicit decision fabrication remains test-local per R3. |
| `R4-F6` | Migration/reversibility pass | No public web/RPC framework or stable binary serialization technology is selected inside the semantic-owner runtime. | Added executable guard. Existing ADR gate remains uncrossed. |
| `R4-F7` | Evidence pass | P2.10 already consolidates 14 architecture-fitness dimensions over 299 tests and guards product-domain leakage plus durable-infrastructure selection. | R4 supplements rather than duplicates P2.10 with final code-health/stable-boundary guards. |
| `R4-F8` | Performance pass | No measured latency, throughput, resource-exhaustion or security hotspot justifies optimization. The full reference suite is sub-second at the P2.10 baseline. | No speculative cache/index/concurrency/performance architecture introduced. |

## 5. Implemented R4 hardening

R4 intentionally makes only evidence-backed changes:

1. adds `reference/python/tests/test_r4_milestone_hardening.py`;
2. locks the semantic-owner dependency boundary away from historical P2.01 composition modules;
3. verifies the package root remains explicitly provisional and does not export the P2 semantic-owner runtime surface;
4. verifies `RuntimeConsistencyState` remains outside the package-root convenience surface and retains its explicit non-durable scope statement;
5. guards against process/network/unsafe-deserialization dependencies in shared runtime modules;
6. guards against dynamic `eval`/`exec`/`compile`/`__import__` execution in the shared runtime;
7. guards against implicit gate-bypass/auto-approval APIs;
8. guards against accidental selection of a public web/RPC framework or stable serialization technology.

No semantic runtime contract is broadened and no Accepted RFC is edited.

## 6. Carried debt disposition

### 6.1 Package-root convenience exports

R3 deferred package-root cleanup until stable-boundary hardening. R4 finds no current stable/public boundary to harden: the package root explicitly says it is provisional and not public, and the P2 semantic-owner surface is not exported there.

Removing historical P1 convenience exports now would create compatibility churn without an evidence-backed external consumer or stable-boundary benefit.

Disposition: **retain, guarded, not public**. Revisit before any stable public/cross-product API/SDK commitment.

### 6.2 RuntimeConsistencyState aggregate admission

R2 identified that arbitrary/deserialized construction is not a durable integrity boundary. That remains true. The trigger for mandatory hardening has still not occurred because Phase 2 selects no durable storage, deserialization contract or trusted external construction path.

Adding a durable aggregate loader, serialization format or persistence validation framework in R4 would cross from hardening into speculative architecture and could prejudge P2.11/ADR decisions.

Disposition: **retain internal bounded snapshot semantics**. Any future durable/deserialized reliance must first pass P2.11's ADR/runtime-boundary gate.

### 6.3 Error and validation taxonomy

R2/R3 deliberately kept local semantic ownership because similar Python shape did not prove one shared external contract. No new caller evidence or public boundary has appeared by R4.

Disposition: **no global error/validation abstraction**.

## 7. Security, privacy, isolation and authority review

Within the declared bounded reference scope:

- Organization-local scope remains fail-closed in the P2.03/P2.04/P2.07 evidence;
- Product Contract validation does not grant Authorization or Organizational Authority;
- consequential effects still require admitted Governed Execution;
- test-only gate decisions are not promoted into runtime authority;
- projections/reconstructed portability state remain non-authoritative;
- no network/process/deserialization side channel is introduced by the shared runtime;
- no cross-organization sharing contract is implied.

R4 does not claim production security certification, IAM enforcement completeness or full RFC-0003 conformance.

## 8. Maintainability and dependency review

The reusable Phase 2 shape remains semantic-owner composition rather than one universal orchestrator.

R4 found no evidence supporting:

- a new common validation framework;
- a common global error hierarchy;
- a generic workflow runner;
- a plugin/extension framework around P2.01 `RuntimeOperations`;
- a shared gate-decision fabricator;
- a durable repository/transaction abstraction;
- a test fixture factory promoted into runtime code.

The absence of those abstractions is intentional and consistent with R3's `validated reuse over speculative generality` result.

## 9. Performance disposition

No performance optimization is performed.

The governing engineering-quality decision requires evidence-backed optimization. P2.10's complete 299-test reference suite executed in `0.701s`, and no benchmark, profile, correctness/resource-exhaustion issue or security bottleneck indicates a material hotspot.

Adding caches, indexes, concurrency primitives, persistence shortcuts or precomputed runtime state would therefore add architectural weight without demonstrated value.

## 10. ADR gate assessment

**No new ADR is required to close R4.**

R4 does not select or materially rely on:

- durable persistence/database topology;
- transaction, locking or concurrency technology;
- durable idempotency storage;
- Event delivery/store or outbox/inbox topology;
- IAM/policy enforcement technology;
- workflow engine/scheduler/queue;
- stable public/cross-product API/SDK;
- durable serialization/schema contract;
- durable projection/replay storage;
- service/process topology;
- extension/plugin technology.

P2.11 remains responsible for the explicit ADR-gate and runtime-boundary hardening review over this R4-hardened code head.

## 11. R4 exit assessment

R4 exit conditions are satisfied:

1. the complete Phase 2 semantic-owner runtime has been reviewed after final P2.10 evidence;
2. architecture/dependency boundaries remain coherent and historical P2.01 composition is contained;
3. no material correctness, security, privacy, isolation or authority defect is open within the declared M2 reference scope;
4. carried R2/R3 debt is either guarded and explicitly bounded or tied to a future stable/durable boundary trigger;
5. no product-domain logic has entered the shared runtime;
6. no speculative abstraction or unsupported performance optimization was introduced;
7. no concrete ADR trigger has been crossed;
8. executable R4 hardening guards have been added and must pass with the full suite before closure.

**Final R4 decision: `PASS`.**

## 12. Next canonical action

Proceed to **`P2.11 — ADR-gate and runtime-boundary hardening review`** after R4 changes are merged and canonical roadmap synchronization records the gate complete.

R4 completion does not claim `M2` achieved. M2 remains contingent on P2.11 and P2.12.
