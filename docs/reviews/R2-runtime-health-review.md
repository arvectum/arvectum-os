# R2 — Runtime Health Review

Status: `Complete`  
Date: `2026-08-08`  
Scope: Phase 2 Core Runtime after `P2.06`, before substantive `P2.07`  
Task classification: `platform`  
Owner: `ООО «Арвектум»`

## 1. Purpose and scope

This review executes the mandatory `R2 — Runtime Health Review` established by the Approved engineering-quality decision after P2.06 and before substantive P2.07 work.

The reviewed runtime spine is:

- Canonical lineage, Canonical Head and exact/effective version resolution;
- Typed Relationship identity, versioning, traversal and lineage semantics;
- Governed Execution lifecycle, gates and consequential-operation admission;
- Event receipt/admission, Event identity conflict, provenance and reconstruction;
- runtime consistency, stale-head protection, retry/idempotency, uncertainty and bounded logical atomicity.

R2 is a code-health and semantic-cohesion gate. It does not create a new architecture contract, select durable infrastructure or turn the bounded reference runtime into an `Active` Platform Capability.

## 2. Canonical checks performed

R2 was reviewed against:

- Constitution `1.2.0` — `Ratified`;
- RFC Index current state;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`;
- RFC-0004 `1.0.0` — `Accepted`;
- RFC-0005 `1.0.0` — `Accepted`;
- RFC-0006 `1.0.0` — `Accepted`;
- `DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES` — `Approved`;
- Phase 2 Core Runtime roadmap `1.1.6` and accumulated P2.02–P2.06 implementation/test evidence.

No Accepted RFC is changed by R2.

No relevant Accepted ADR currently constrains the bounded runtime implementation reviewed here. The durable persistence/transaction/concurrency, Event-delivery, IAM/enforcement and stable public-interface ADR gates remain uncrossed because the implementation is still internal, in-memory, reversible and technology-neutral.

## 3. Review result

**Result: `Pass with bounded debt`.**

No material correctness, security, tenant-isolation, dependency-direction or architectural-responsibility defect was found that blocks P2.07.

The accumulated runtime has one coherent semantic ownership structure:

```text
CanonicalRecord
    ↓
CanonicalLineage
    ├── TypedRelationshipLineage
    ├── GovernedExecutionLineage
    └── RuntimeConsistencyState

GovernedExecution
    ↓ consequential admission
Event admission / provenance
    ↓
Runtime consistency / retry / conflict boundary
```

The implementation does not contain a second competing Canonical lineage engine, Event-admission engine, execution-transition engine or idempotency engine.

## 4. Findings and dispositions

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| `R2-F1` | Pass | Canonical lineage semantics have one reusable owner. Relationships, Governed Execution and Runtime Consistency reuse `CanonicalLineage` rather than implementing competing Head/version-chain rules. | Keep current ownership. New cross-cutting fitness tests make this dependency explicit. |
| `R2-F2` | Low | Small validation helpers are repeated across modules: timezone-aware datetime checks, ordered/unique identity references, tuple/string-pair shape checks. | **Do not extract a shared validation utility yet.** Current helpers carry different semantic labels, non-empty rules and failure contexts. A generic utility now would be speculative abstraction. Revisit at R3 only if the second workflow demonstrates stable reusable semantics rather than coincidental syntax reuse. |
| `R2-F3` | Pass | Governed Execution transition logic is centralized through `_ALLOWED_TRANSITIONS` and `_successor_record`; gate validation appears both at candidate-evaluation and constructed-context boundaries. | Keep both validation boundaries. They protect different trust points and are not competing lifecycle engines. |
| `R2-F4` | Low | Exact-resolution error taxonomy is not fully uniform: Canonical/Relationship resolution use semantic `ValueError` subclasses while `GovernedExecutionLineage.exact()` currently uses plain `KeyError`; other runtime modules expose their own semantic error families. | Bounded internal debt. Do not introduce a platform-wide error abstraction before a stable/public runtime boundary exists. Reconcile before a stable public API/SDK or at R3 if reuse evidence makes a common resolution contract necessary. |
| `R2-F5` | Low | One P2.06 negative-path test uses broad `RuntimeError` for an Event-admission conflict, so that test is less specific than the surrounding semantic-error tests. | Bounded test-specificity debt; tighten when that path is next modified or at R3. It does not hide a current failing behavior because Event-specific conflict tests already exercise the precise error family. |
| `R2-F6` | Medium, bounded | `RuntimeConsistencyState` validates canonical lineage and contained value types but is not a complete durable integrity boundary for arbitrary caller-constructed snapshots; it does not independently cross-validate every successful canonical-attempt result/Event reference at construction time. Normal commit paths create consistent immutable snapshots and duplicate resolution fails explicitly if committed evidence is missing. | Keep the object explicitly internal/reference-only and do not treat arbitrary deserialized construction as trusted canonical state. Before durable persistence, external deserialization or a stable public state contract is materially relied upon, harden aggregate-state admission under the applicable ADR/runtime boundary. This does not block P2.07 because P2.07 remains a bounded Product Contract validation boundary and must not turn this internal state object into a durable/public contract. |
| `R2-F7` | Pass | P2.05 Event identity/content conflict and P2.06 retry-token/idempotency conflict are separate semantic concerns and are not duplicate implementations. | Keep separation: Event admission owns immutable Event occurrence identity; runtime consistency owns invocation/retry conflict semantics. |
| `R2-F8` | Pass | No database, broker, queue, lock/CAS, durable idempotency store, transaction manager, IAM provider, workflow engine or public SDK dependency has entered the accumulated runtime spine. | No ADR required by R2. Stop and govern the concrete choice if later work materially relies on one. |

## 5. Dependency and module cohesion review

The current dependency direction remains coherent for the bounded reference runtime:

- `canonical_lineage.py` owns generic canonical-chain and exact/effective resolution semantics;
- `relationships.py` reuses canonical lineage and adds only relationship-specific identity/type/endpoint semantics;
- `governed_execution.py` reuses canonical lineage and owns lifecycle, gate evidence and consequential admission;
- `event_provenance.py` consumes exact Governed Execution evidence and owns Event receipt/admission, Event conflict and reconstruction;
- `runtime_consistency.py` composes canonical lineage, Governed Execution admission and Event admission to enforce stale-head, retry/idempotency, uncertainty and logical commit semantics.

No circular architectural-responsibility dependency was identified in the reviewed spine.

No product-domain behavior was found in these shared runtime modules.

## 6. Validation, state-transition, error and conflict reconciliation

R2 deliberately does **not** create one global validation or error framework.

The semantic boundaries after review are:

- **shape/invariant validation** stays close to the value object that owns the invariant;
- **canonical version-chain conflict** belongs to `CanonicalLineage`;
- **relationship semantic drift** belongs to `relationships`;
- **execution lifecycle/gate failure** belongs to `governed_execution`;
- **Event identity/version conflict** belongs to `event_provenance`;
- **stale-head, retry-token, duplicate-effect and reconciliation conflict** belongs to `runtime_consistency`.

This preserves domain-neutral ownership without turning similar Python guard clauses into a premature shared abstraction.

## 7. Cross-cutting test evidence

R2 adds `reference/python/tests/test_r2_runtime_health.py` with six focused cross-cutting checks:

1. Runtime Consistency reuses Canonical lineage, Event admission and Governed Execution admission owners rather than redeclaring them.
2. Typed Relationship runtime reuses Canonical lineage.
3. The accumulated runtime spine does not import selected durable database/broker/workflow infrastructure.
4. Runtime error families remain semantically scoped rather than collapsed into a premature global error API.
5. `RuntimeConsistencyState` reuses fail-closed Canonical lineage branch-conflict validation.
6. Exact historical version resolution remains distinct from Canonical Head resolution.

GitHub Actions evidence for PR `#25`, executable head `c519e6fb3fe9d9b333382786740a37c3a477c06b`:

- workflow: `Reference Python CI` run `#43`;
- job: `Full reference test suite`;
- result: `success`;
- `Ran 247 tests in 0.415s`;
- `OK`.

The prior P2.06 baseline was 241 tests; R2 adds 6 cross-cutting tests without changing runtime behavior.

## 8. Performance disposition

No profiling or benchmark suite is introduced by R2.

Reason:

- the reviewed runtime is intentionally bounded and in-memory;
- no material runtime-latency or throughput problem is evidenced;
- the complete 247-test reference suite executes in well under one second in current CI;
- introducing caches, indexes, concurrency primitives or performance abstractions now would be speculative and could pre-empt later ADR decisions.

Performance work remains evidence-triggered.

## 9. ADR disposition

**No ADR is required to close R2.**

R2 found no material reliance on a concrete:

- durable persistence model;
- transaction or locking/CAS mechanism;
- idempotency store;
- outbox/inbox or Event-delivery topology;
- message broker or distributed coordinator;
- IAM/policy enforcement provider;
- public API/SDK or serialization contract;
- runtime deployment topology.

If P2.07 or later work makes one of those choices materially constraining, the engineering-quality decision requires stopping at the ADR gate before further reliance.

`R2-F6` is specifically a warning not to promote the current in-memory aggregate state into a durable or public boundary accidentally.

## 10. Carried-forward bounded debt

The following debt is explicitly carried forward and is not a P2.07 blocker:

1. local validation helper duplication may be reconsidered at R3 after second-workflow reuse evidence;
2. exact-resolution error taxonomy should be reconciled before a stable public runtime interface, or earlier if R3 demonstrates a common consumer contract;
3. the broad P2.06 Event-conflict assertion should be tightened on next relevant test edit or at R3;
4. arbitrary/deserialized `RuntimeConsistencyState` must not be treated as a durable trusted integrity boundary without explicit aggregate-state admission hardening and any required ADR.

None of these items changes Accepted architecture or authorizes a stable external contract.

## 11. Exit decision

R2 exit criteria are satisfied:

1. accumulated semantic-runtime ownership has been reviewed;
2. duplicated-looking validation/state/conflict logic has been reconciled by explicit semantic ownership rather than speculative abstraction;
3. module cohesion and dependency direction remain acceptable;
4. cross-cutting test evidence is green;
5. no material performance issue justifies profiling/optimization work;
6. no concrete ADR trigger has been crossed;
7. bounded debt has explicit scope and future trigger.

**R2 is complete. Substantive `P2.07 — Product Contract runtime validation boundary` may proceed after this review and its roadmap synchronization are merged to `main`.**

This review does not claim production readiness, full-platform conformance, durable runtime integrity, a stable public runtime API or an `Active` Platform Capability.
