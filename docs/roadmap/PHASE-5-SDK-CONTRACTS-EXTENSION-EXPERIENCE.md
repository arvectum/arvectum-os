# Phase 5 — SDK, Contracts and Extension Experience

Status: `Active`
Version: `1.3.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M5 — Repeatable product/extension integration`

## 1. Purpose

Phase 5 turns the governed runtime, shared-capability and workspace evidence from M1–M4 into a repeatable integration experience for products and extensions without prematurely declaring public/stable compatibility boundaries.

The phase must prove that a materially distinct integration can be created through explicit Product Contracts, reusable integration tooling and conformance evidence rather than private imports, copied internals or accidental platform coupling.

Phase 5 is not a commitment to publish a public SDK, public API, marketplace, plugin runtime, stable wire protocol or final developer platform. Those boundaries become stable/public only through their applicable evidence and governance.

## 2. Canonical basis

Phase 5 is bounded by:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
3. RFC-0004 — explicit Product Contract boundary, lifecycle separation and hidden-coupling prohibition;
4. M2 — reusable governed Core Runtime baseline;
5. M3 — CAP-001 through CAP-004 retained as `Incubating / Provisional` shared capabilities;
6. M4 — coherent governed workspace baseline and one bounded Product Contract-backed composition proof;
7. P4.08 Product Contract remains `Provisional 0.1.0` and is evidence, not a Stable compatibility promise;
8. P4.12 — `PASS`, M4 achieved for the bounded governed-workspace reference scope;
9. [`P5.01 integration boundary revalidation`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`; Product Contract/dependency/operation/version semantics are the revalidated boundary and current Python import/module shapes remain internal evidence only;
10. [`P5.02 Product Contract declaration/validation review`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`; the existing Product Contract semantic owner remains the single executable declaration model and the internal validator adds machine-checkable fail-closed evidence without creating a Stable/public schema;
11. [`R13 Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation; derived validation evidence now preserves dependency provider/consumer/failure responsibilities and operation failure semantics so later dependency/version tooling cannot normalize a narrower projection into a competing contract source.

## 3. Phase boundary

### In scope

- revalidate the integration boundary from actual M4 evidence;
- define an internal integration/developer experience around Product Contracts and governed platform reliance;
- machine-check Product Contract declarations and exact dependency/version pins where useful;
- provide bounded scaffolding/templates/helpers only after their boundary is evidenced;
- provide local conformance/fitness fixtures for product/extension integrations;
- prove repeatable integration with a materially distinct second integration;
- preserve Organization, identity, authorization, Organizational Authority, provenance, portability and capability-lifecycle semantics;
- define compatibility/migration/deprecation semantics only to the degree actually justified by relied-upon boundaries;
- reassess ADR and public/stable contract gates before M5 closure.

### Explicitly out of scope unless separately justified

- declaring a public SDK or public API merely because Phase 5 is named SDK/Contracts;
- promoting any Product Contract to `Stable` without lifecycle evidence;
- promoting CAP-001 through CAP-004 to `Active` merely because tooling consumes them;
- generic plugin/marketplace runtime;
- cross-organization extension distribution;
- production package registry/support/SLA commitments;
- fixed REST/GraphQL/gRPC/BFF or serialization/wire topology;
- fixed language-specific SDK as permanent architecture;
- extension registration as authorization or Organizational Authority;
- hiding product-domain semantics inside shared SDK helpers.

## 4. Work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P5.01` | Integration boundary revalidation + developer journeys | 🟩 Complete | `██████████ 100%` |
| `P5.02` | Product Contract declaration model + machine-checkable validation baseline | 🟩 Complete | `██████████ 100%` |
| `P5.03` | Governed dependency/version resolution + compatibility semantics | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.04` | Integration composition API/facade boundary | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.05` | Scaffolding/templates + local integration harness | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.06` | Security, authority, rights + Organization-scope integration guards | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.07` | Event/provenance/portability integration support | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.08` | Workspace/capability integration adapters without private coupling | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.09` | Second materially distinct integration reuse proof | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.10` | Phase 5 conformance + architecture fitness matrix | ⬜ Cross-cutting | `░░░░░░░░░░ 0%` |
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.12` | Phase 5 / M5 closure review | ⬜ Planned | `░░░░░░░░░░ 0%` |

P5.01 completion evidence:

- [`P5-01-integration-boundary-revalidation-developer-journeys.md`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`;
- J1 = governed read/composition consumer;
- J2 = consequential product action through exact Product Contract continuity and Governed Execution;
- J3 = read-only evidence/reconstruction extension candidate, explicitly not yet the P5.09 second-integration proof;
- current Python imports, module paths, dataclass shapes, operation-token spellings and monorepo package layout remain internal/provisional evidence rather than a Stable/public SDK contract.

P5.02 completion evidence:

- [`P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`;
- the existing RFC-0004 `ProductContract` remains the single executable declaration model for the bounded reference implementation;
- an internal/provisional whole-declaration validator preserves exact Product Contract/Product/dependency/operation/canonical-access semantics and fail-closes missing boundary requirements;
- validation evidence grants no Authentication, Authorization, Organizational Authority, approval, permission or capability activation;
- dependency `provisional` remains a Product Contract reliance/support qualifier and does not replace the capability catalog lifecycle;
- no YAML/JSON/protobuf/OpenAPI/public SDK/API/wire/package/registry boundary was selected;
- hosted `Reference Python CI` run `#205` passed the full reference suite.

R13 completion evidence:

- [`R13-integration-boundary-review.md`](../reviews/R13-integration-boundary-review.md) — `PASS` after one material boundary-projection completeness finding was remediated;
- R13-F1 fixed derived validation evidence that omitted Product Contract dependency provider/consumer/failure responsibilities and operation failure behavior;
- the validator still accepts the existing `ProductContract` as its semantic owner and returns immutable derived evidence rather than an independently editable contract source;
- validation/admission evidence remains separate from Authorization, Organizational Authority and capability lifecycle;
- no Stable/public representation, version-negotiation protocol or ADR-triggering mechanism was selected;
- `reference/python/tests/test_r13_integration_boundary_review.py` records deterministic regression evidence for the fixed boundary invariants;
- no new hosted CI run is claimed for the direct-push R13 head; the last observed hosted full-suite baseline remains P5.02 `#205`.

## 5. Engineering gates

Engineering reviews are gates, not equal-weight roadmap work items.

- `R13 — Integration Boundary Review` — **Complete / PASS after R13-F1 remediation**. Product Contract remains the single governed semantic owner; derived validation evidence preserves boundary responsibilities without becoming a second contract system.
- `R14 — Developer Safety / Contract Health Review` — after P5.06. Review fail-closed behavior, authority separation, error semantics and coupling pressure.
- `R15 — Reuse / Developer Experience Refactoring Review` — after P5.09. Refactor only from demonstrated second-integration reuse evidence.
- `R16 — M5 Integration Hardening` — after P5.10 and before P5.11. Resolve material conformance, compatibility, security and maintainability findings.

Performance optimization remains evidence-backed; do not optimize package/API/runtime mechanics without benchmark/profile evidence except correctness, security or resource-exhaustion defects.

## 6. Dependency-aware sequence

```text
M4 ✓
 ↓
P5.01 Integration boundary + developer journeys ✓
 ↓
P5.02 Product Contract declaration/validation ✓
 ↓
R13 Integration Boundary Review ✓
 ↓
P5.03 Dependency/version + compatibility semantics ← current
 ↓
P5.04 Composition API/facade boundary
 ↓
P5.05 Scaffolding/templates + local harness
 ↓
P5.06 Security/authority/rights guards
 ↓
R14 Developer Safety / Contract Health
 ↓
P5.07 Event/provenance/portability support
 ↓
P5.08 Workspace/capability adapters
 ↓
P5.09 Second integration reuse proof
 ↓
R15 Reuse / DX Refactoring
 ↓
P5.10 Conformance + fitness matrix
 ↓
R16 M5 Hardening
 ↓
P5.11 Compatibility / ADR / public-boundary review
 ↓
P5.12 M5 closure
 ↓
M5
```

P5.10 accumulates evidence throughout the phase.

## 7. Work-item intent and exit evidence

### P5.01 — Integration boundary revalidation + developer journeys

Status: `Complete` — [`review evidence`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md).

P5.01 revalidated Phase 5 against actual M4 evidence and identified the smallest real integration journeys worth supporting. The Product Contract remains the governed boundary authority; exact dependency/operation/version semantics are relied-upon integration semantics; current repository import/module/dataclass shape remains implementation-private.

Exit evidence:

- at least two bounded integration journeys are described — `PASS` (J1 and J2; J3 retained as a non-binding future reuse candidate);
- private/internal coupling points are explicitly prohibited — `PASS`;
- no public/stable compatibility promise is inferred — `PASS`;
- candidate tooling surfaces are classified as internal/provisional until proven otherwise — `PASS`.

P5.01 changes no runtime behavior and intentionally does not create an SDK/declaration implementation ahead of P5.02.

### P5.02 — Product Contract declaration model + machine-checkable validation baseline

Status: `Complete` — [`review evidence`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md).

P5.02 validates the existing RFC-0004 Product Contract declaration as a whole rather than creating a second manifest/schema system. The implementation is internal/provisional and intentionally supports only the current P4.08 `Provisional` reference baseline.

Exit evidence:

- exact contract identity/version and declared capability/dependency versions and operations can be validated — `PASS`;
- required authority/security/data/canonical-access/portability/review/exit declarations fail closed when missing or invalid — `PASS`;
- tooling does not create permission or Organizational Authority — `PASS`;
- Product Contract lifecycle remains distinct from capability lifecycle — `PASS`;
- hidden product/platform coupling mechanisms are rejected — `PASS`;
- no stable/public representation or ADR-triggering mechanism is selected — `PASS`;
- hosted full reference CI — `PASS` (`#205`).

### P5.03 — Governed dependency/version resolution + compatibility semantics

**Current canonical action.** Make relied-upon contract/capability versions explicit and reject ambiguous or unsupported reliance while preserving the exact RFC-0004 Product Contract as the semantic owner.

R13 handoff constraints for P5.03:

- a resolver must consume exact Product Contract Version and dependency contract-version identity rather than infer compatibility from Python package/module/dataclass shape;
- dependency provider responsibility, consumer responsibility, dependency failure behavior and operation failure behavior remain boundary semantics and must not be lost by resolver projections;
- P5.02 validation evidence is derived inspection/validation evidence, not an independently evolving dependency contract;
- unsupported/deprecated/retired behavior must be deterministic and based on governed evidence rather than guessed lifecycle state;
- Product Contract resolution grants no Authorization or Organizational Authority and does not alter capability lifecycle;
- durable public/stable version-negotiation or migration protocol choices re-open the ADR/governance gate before material reliance.

Exit evidence:

- exact dependency/version pins are inspectable;
- compatibility decisions are explicit rather than guessed from package versions;
- deprecated/retired/unsupported dependencies have deterministic behavior;
- migration obligations are recorded when a relied-upon boundary actually changes.

### P5.04 — Integration composition API/facade boundary

Extract the smallest reusable integration-facing boundary that composes governed runtime/capability/workspace semantics without exposing private implementation structure.

Exit evidence:

- product code does not import private runtime/capability internals for the proved journeys;
- the facade delegates authority/canonical-state decisions to existing semantic owners;
- no language/network/wire choice is declared stable merely by implementation.

### P5.05 — Scaffolding/templates + local integration harness

Provide reversible helpers that reduce repeated setup for a bounded integration while keeping generated/templated code understandable and replaceable.

Exit evidence:

- a new bounded integration can be initialized without copying an existing product implementation;
- generated/template artifacts identify provisional boundaries;
- local tests can run without production infrastructure assumptions.

### P5.06 — Security, authority, rights + Organization-scope integration guards

Prove that integration convenience cannot bypass RFC-0003/RFC-0005 gates.

Exit evidence:

- wrong-Organization, missing/denied authorization and missing Organizational Authority paths fail closed;
- extension registration or contract admission grants no authority;
- minimization/purpose/right constraints remain enforced by their semantic owners;
- stale authorization/contract continuity cannot self-advance.

### P5.07 — Event/provenance/portability integration support

Expose bounded helpers/fixtures for correct event attribution, provenance and portable semantic state without turning telemetry or serialization into authority.

Exit evidence:

- integration-originated governed actions remain attributable to exact actor/execution/contract/version context;
- derived telemetry remains non-authoritative;
- portable fixtures preserve semantic identities and relationships without requiring a specific infrastructure vendor.

### P5.08 — Workspace/capability integration adapters without private coupling

Demonstrate integration with the M3/M4 surfaces through explicit boundaries, preserving Incubating capability status and product ownership of product semantics.

Exit evidence:

- CAP-001..CAP-004 and workspace composition are consumed without internal imports/private state;
- capability-specific authority/freshness/rights semantics remain owned by capabilities;
- product-specific task/disposition semantics remain outside shared platform abstractions.

### P5.09 — Second materially distinct integration reuse proof

Build a second bounded integration materially different from the first to validate reuse rather than self-confirming abstraction.

Exit evidence:

- both integrations use the same declared integration boundary/tooling;
- no copy/paste of implementation-private platform code is required;
- differences remain product-owned where appropriate;
- reuse evidence is sufficient to identify abstractions worth retaining or deleting.

### P5.10 — Phase 5 conformance + architecture fitness matrix

Accumulate positive and negative evidence across the phase.

Minimum matrix:

- Product Contract declaration/version identity;
- dependency/version continuity;
- dependency provider/consumer/failure responsibility continuity;
- hidden-coupling prohibition;
- Organization isolation;
- Authorization vs Organizational Authority separation;
- governed canonical mutation path;
- event/provenance attribution;
- rights/minimization/data-governance continuity;
- portability;
- capability/Product Contract lifecycle separation;
- unsupported/deprecated dependency behavior;
- second-integration reuse;
- no accidental public/stable compatibility promise.

### P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review

Review accumulated implementation for accidental architecture and compatibility commitments.

Explicit gates include:

- language-specific SDK/package boundary;
- stable/public API or wire/serialization contract;
- package registry/distribution topology;
- plugin loading/sandboxing/isolation mechanism;
- extension registry/discovery topology;
- version negotiation/migration protocol;
- generated-code compatibility boundary;
- separately deployable integration service;
- stable design-system/component integration contract.

Create ADR/RFC/policy only if the corresponding threshold is actually crossed.

### P5.12 — Phase 5 / M5 closure review

Close only on repository evidence.

Result must distinguish roadmap completion from Product Contract stability, capability lifecycle, operational readiness, conformance maturity and public/commercial commitments.

## 8. M5 exit criteria

`M5 — Repeatable product/extension integration` is achieved only if all applicable conditions pass:

1. a bounded integration boundary exists above implementation-private internals;
2. RFC-0004 Product Contract declarations used by that boundary are explicit and machine-checkable where useful;
3. exact relied-upon dependency/version identity is preserved;
4. hidden product/platform coupling is rejected by tests/review;
5. security, Organization isolation, Authorization and Organizational Authority semantics remain fail-closed;
6. governed actions preserve Event/provenance attribution and canonical-state rules;
7. portability evidence does not depend on one durable vendor mechanism;
8. a second materially distinct integration reuses the same integration tooling/boundary;
9. product-specific semantics remain product-owned;
10. CAP-001..CAP-004 lifecycle is not inflated by integration convenience;
11. P5.10 fitness matrix passes;
12. R13–R16 material findings are resolved or explicitly bounded;
13. P5.11 dispositions every crossed ADR/public-compatibility gate;
14. P5.12 closure review passes.

M5 does not require a public SDK, Stable Product Contract or production deployment. If evidence during P5 justifies such a boundary, it must be governed separately before that claim is made.

## 9. Current canonical action

> **P5.03 — Governed dependency/version resolution + compatibility semantics.**

P5.03 must consume the exact RFC-0004 Product Contract boundary and the fixed R13 invariants. It must make compatibility decisions explicit, preserve dependency/operation responsibility and failure semantics, reject ambiguous or unsupported reliance, and avoid turning Python package/module/dataclass structure or a new resolver representation into a Stable/public compatibility contract.
