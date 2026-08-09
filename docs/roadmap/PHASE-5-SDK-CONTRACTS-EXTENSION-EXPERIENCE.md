# Phase 5 — SDK, Contracts and Extension Experience

Status: `Active`
Version: `1.9.0`
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
11. [`R13 Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation; derived validation evidence now preserves dependency provider/consumer/failure responsibilities and operation failure semantics so later dependency/version tooling cannot normalize a narrower projection into a competing contract source;
12. [`P5.03 governed dependency/version resolution review`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`; exact Product Contract/dependency version continuity plus explicit governed support evidence now produces deterministic compatibility decisions without SemVer/package inference, automatic fallback, authority grants or a Stable/public negotiation boundary;
13. [`P5.04 integration composition facade review`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`; a bounded internal/provisional facade now composes P5.02/P5.03, capability admission, non-authoritative workspace entry and Product Contract-backed Governed Execution while delegating all authority/canonical-state decisions to their existing semantic owners;
14. [`P5.05 scaffolding/templates + local harness review`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`; bounded readable scaffolding and an in-process harness consume the P5.04 facade without copying product implementation, creating a second contract source or requiring production infrastructure;
15. [`P5.06 security/authority/rights Organization-scope integration-guard review`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`; wrong-Organization, missing/denied Authorization/Organizational Authority, purpose/right and stale-continuity paths fail closed through existing semantic owners, with hosted `Reference Python CI #223` passing 634 tests;
16. [`R14 Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation; normal facade construction is forced through P5.02/P5.03 and dependency-backed J1/J2 actions require explicit current governed provider/version evidence instead of silently reusing composition-time compatibility; hosted `Reference Python CI #232` passes the full 644-test reference suite;
17. [`P5.07 Event/provenance/portability integration-support review`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`; bounded integration evidence now preserves exact Actor/Product/Product Contract/Execution/Event attribution, delegates canonical Event semantics to P2.05, keeps telemetry non-authoritative and portable semantic fixtures non-canonical/vendor-neutral; hosted `Reference Python CI #237` passes the full 653-test reference suite.

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
| `P5.03` | Governed dependency/version resolution + compatibility semantics | 🟩 Complete | `██████████ 100%` |
| `P5.04` | Integration composition API/facade boundary | 🟩 Complete | `██████████ 100%` |
| `P5.05` | Scaffolding/templates + local integration harness | 🟩 Complete | `██████████ 100%` |
| `P5.06` | Security, authority, rights + Organization-scope integration guards | 🟩 Complete | `██████████ 100%` |
| `P5.07` | Event/provenance/portability integration support | 🟩 Complete | `██████████ 100%` |
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

P5.03 completion evidence:

- [`P5-03-governed-dependency-version-resolution-compatibility-semantics.md`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`;
- an internal/provisional static resolver consumes the exact RFC-0004 `ProductContract` semantic owner plus the exact effective Product Contract Version pin;
- exact declared dependency versions resolve only from explicit governed provider/version support evidence; no SemVer/package/module/dataclass inference or automatic fallback is used;
- `Compatible`, `VersionMismatch`, `Unsupported`, `Deprecated`, `Retired` and `Ambiguous` decisions are explicit and deterministic;
- dependency provider/consumer/failure responsibilities and operation failure behavior remain present in compatibility evidence;
- deprecated/retired support evidence requires explicit migration obligations and version mismatch records a Product Contract revision obligation;
- resolution grants no Authorization or Organizational Authority and does not alter capability lifecycle;
- `reference/python/tests/test_p5_03_product_contract_dependency_resolution.py` adds 12 focused regression/fitness cases;
- hosted `Reference Python CI #217` passed on the final P5.03 PR head before merge.

P5.04 completion evidence:

- [`P5-04-integration-composition-api-facade-boundary.md`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`;
- `reference/python/arvectum_os_ref/integration_composition.py` adds the smallest internal/provisional integration-facing composition seam justified by J1/J2;
- facade construction consumes the exact RFC-0004 Product Contract, P5.02 declaration validation and P5.03 exact compatibility evidence;
- capability admission, workspace authority and Governed Execution remain delegated to their existing semantic owners;
- `reference/python/bounded_product_ref/integration_journeys.py` proves J1/J2 product entry with exactly one Arvectum OS import boundary: the integration facade;
- product/domain semantics remain outside the platform facade and capability-specific adapters remain P5.08 scope;
- no Stable/public Python/API/wire/package/network boundary or capability lifecycle transition is created;
- `reference/python/tests/test_p5_04_integration_composition_facade.py` adds 12 focused regression/fitness cases;
- hosted `Reference Python CI #222` passed the full 615-test reference suite on the final synchronized P5.04 PR head.

P5.05 completion evidence:

- [`P5-05-scaffolding-templates-local-integration-harness.md`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`;
- `reference/python/arvectum_os_ref/integration_scaffolding.py` adds a tiny explicit provisional template and local in-process harness over P5.04;
- rendered entry code imports Arvectum OS only through `arvectum_os_ref.integration_composition` and remains readable/replaceable rather than becoming a generated-code compatibility contract;
- the local harness consumes the exact Product Contract, Actor, effective Product Contract Version and explicit governed provider/version evidence, then delegates composition to P5.04;
- the harness preserves exact Product Contract Version continuity into a `NON_AUTHORITATIVE` workspace;
- Product Contract construction, dependency resolution, authorization/authority, capability lifecycle and product-domain semantics remain with their existing owners;
- no database, broker, IAM provider, object store, registry, network endpoint or deployable service is required;
- `reference/python/tests/test_p5_05_integration_scaffolding_local_harness.py` adds 8 focused regression/fitness cases;
- hosted P5.05 execution evidence is covered by the next full-suite run and is included in P5.06 `Reference Python CI #223`.

P5.06 completion evidence:

- [`P5-06-security-authority-rights-organization-scope-integration-guards.md`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`;
- no second authorization, Organizational Authority, rights/policy or IAM subsystem was introduced; P5.06 exercises the existing semantic owners through P5.04/P5.05;
- wrong-Organization actor and capability-request paths fail closed;
- Product Contract/capability admission remains non-authoritative and grants no permission, approval or Organizational Authority;
- an admitted CAP-001 request with a mismatched current right remains rejected by the P3.07 access semantic owner;
- missing required Authorization/Organizational Authority remain unresolved, explicit Authorization denial blocks `Ready`, and all independent required RFC-0005 gates must allow before `Ready`;
- stale gate decisions are rejected after re-evaluation and stale effective Product Contract Version continuity is rejected before composition;
- P5.05 local harness remains `NON_AUTHORITATIVE`;
- `reference/python/tests/test_p5_06_security_authority_rights_integration_guards.py` adds 11 focused cross-layer regression/fitness cases;
- hosted `Reference Python CI #223` passed the full 634-test reference suite.

R14 completion evidence:

- [`R14-developer-safety-contract-health-review.md`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after two material findings were remediated;
- R14-F1 closes direct facade construction as a normal path around the P5.02/P5.03 governed composition factory through typed `IntegrationCompositionConstructionError`;
- R14-F2 prevents composition-time compatibility from self-advancing after provider-support state changes;
- dependency-backed `admit_capability()` and `start_governed_execution()` now require explicit current governed dependency/version evidence and re-run the existing P5.03 resolver;
- missing current evidence fails closed through typed `IntegrationCompositionEvidenceRequiredError`;
- current P5.03 `Deprecated`, `Retired`, `Unsupported`, `VersionMismatch` and `Ambiguous` failures remain owned by and propagate from P5.03;
- Authorization, Organizational Authority, purpose/right/classification and Data Governance remain separate existing semantic owners;
- product-owned J1/J2 helpers still import exactly one platform integration module and pass provider evidence opaquely;
- no provider registry, TTL/freshness protocol, public compatibility service or Stable/public SDK/API/wire/package boundary is selected;
- `reference/python/tests/test_r14_developer_safety_contract_health_review.py` adds 10 focused regression/fitness cases;
- hosted `Reference Python CI #232` passed the full 644-test reference suite with `OK`, including all 10 R14 regression cases and the adapted P5.04/P5.06 callers.

P5.07 completion evidence:

- [`P5-07-event-provenance-portability-integration-support.md`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`;
- `reference/python/arvectum_os_ref/integration_evidence.py` adds a bounded internal/provisional helper over the R14-hardened integration facade;
- canonical Event admission, duplicate-delivery semantics and Event identity conflicts remain delegated to the P2.05 Event/provenance owner;
- exact actual/represented Actor, Product, Product Contract Subject/Version and Execution Subject/Version attribution is preserved in Event provenance;
- correlation preserves stable Execution Identity and causation preserves exact causal Execution Context Version;
- derived telemetry is explicitly `derived-non-authoritative` and grants no permission, authority or approval;
- portable semantic fixtures are explicitly `derived-non-canonical`, preserve identity roles/semantic links and never fabricate Canonical Typed Relationships;
- no JSON/YAML/protobuf/OpenAPI, broker, Event store, tracing backend, schema registry, export endpoint, freshness registry or public SDK/API boundary is selected;
- `reference/python/tests/test_p5_07_event_provenance_portability_integration_support.py` adds 9 focused regression/fitness cases;
- hosted `Reference Python CI #237` passed the full 653-test reference suite with `OK`.

## 5. Engineering gates

Engineering reviews are gates, not equal-weight roadmap work items.

- `R13 — Integration Boundary Review` — **Complete / PASS after R13-F1 remediation**. Product Contract remains the single governed semantic owner; derived validation evidence preserves boundary responsibilities without becoming a second contract system.
- `R14 — Developer Safety / Contract Health Review` — **Complete / PASS after R14-F1/R14-F2 remediation**. Normal facade construction cannot bypass P5.02/P5.03, and dependency-backed J1/J2 reliance cannot silently reuse composition-time provider compatibility.
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
P5.03 Dependency/version + compatibility semantics ✓
 ↓
P5.04 Composition API/facade boundary ✓
 ↓
P5.05 Scaffolding/templates + local harness ✓
 ↓
P5.06 Security/authority/rights guards ✓
 ↓
R14 Developer Safety / Contract Health ✓
 ↓
P5.07 Event/provenance/portability support ✓
 ↓
P5.08 Workspace/capability adapters ← current
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

Status: `Complete` — [`review evidence`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md).

P5.03 adds the smallest reversible exact-version compatibility mechanism justified by the current Provisional boundary: the resolver consumes the exact RFC-0004 Product Contract and exact effective Product Contract Version, then evaluates each declared dependency only against explicit governed provider/version support evidence.

Exit evidence:

- exact dependency/version pins are inspectable — `PASS`;
- compatibility decisions are explicit rather than guessed from package versions — `PASS`;
- deprecated/retired/unsupported/ambiguous dependencies have deterministic fail-closed behavior — `PASS`;
- migration obligations are recorded when a relied-upon boundary changes or is deprecated/retired — `PASS`;
- R13 provider/consumer/dependency/operation failure semantics remain preserved — `PASS`;
- no fallback version, Stable/public negotiation protocol, permission/authority grant or capability-lifecycle transition is created — `PASS`;
- focused P5.03 executable regression evidence is committed — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #217`).

### P5.04 — Integration composition API/facade boundary

Status: `Complete` — [`review evidence`](../reviews/P5-04-integration-composition-api-facade-boundary.md).

P5.04 extracts the smallest reusable integration-facing composition boundary justified by J1/J2 without exposing product code to the implementation-private runtime/capability/workspace module graph.

Exit evidence:

- product-owned P5.04 J1/J2 journey code imports no private runtime/capability/workspace implementation modules — `PASS`;
- the product journey sees Arvectum OS through one internal/provisional integration facade module — `PASS`;
- facade construction consumes exact P5.02 declaration and P5.03 dependency/version resolution semantics — `PASS`;
- exact Product Contract/Product/dependency/version/operation continuity remains fail-closed — `PASS`;
- capability admission, workspace authority and consequential execution delegate to existing semantic owners — `PASS`;
- facade construction/admission grants no Authorization, Organizational Authority or capability activation — `PASS`;
- product-domain semantics remain product-owned and capability-specific adapters remain P5.08 scope — `PASS`;
- no language/network/wire/package choice is declared Stable/public merely by implementation — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #222`, 615 tests, OK).

R14 later hardens this boundary by restricting normal construction to the governed P5.02/P5.03 factory path and requiring current governed provider/version evidence at dependency-backed actions.

### P5.05 — Scaffolding/templates + local integration harness

Status: `Complete` — [`review evidence`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md).

P5.05 provides reversible helpers that reduce repeated setup for a bounded integration while keeping generated/templated code understandable, replaceable and explicitly provisional. Both helpers consume the P5.04 facade boundary instead of copying the bounded product implementation.

Exit evidence:

- a new bounded integration can be initialized without copying an existing product implementation — `PASS`;
- generated/template artifacts identify provisional boundaries — `PASS`;
- local tests require no production infrastructure assumptions — `PASS` by implementation/test design;
- Product Contract and dependency/version semantics remain owned by RFC-0004/P5.02/P5.03 rather than the scaffold — `PASS`;
- exact Product Contract Version continuity and non-authoritative workspace presentation are preserved — `PASS`;
- scaffolding/harness grants no Authorization, Organizational Authority, capability activation or operational readiness — `PASS`;
- no Stable/public SDK/API/wire/package/generated-code compatibility boundary is created — `PASS`;
- focused P5.05 executable regression evidence is committed — `PASS`;
- hosted execution is covered by `Reference Python CI #223` as part of the accumulated full suite.

### P5.06 — Security, authority, rights + Organization-scope integration guards

Status: `Complete` — [`review evidence`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md).

P5.06 proves that integration convenience cannot bypass RFC-0003/RFC-0005 gates without adding a parallel security/authority subsystem.

Exit evidence:

- wrong-Organization, missing/denied authorization and missing Organizational Authority paths fail closed — `PASS`;
- extension registration or contract/capability admission grants no authority — `PASS` for the exercised Product Contract/capability/facade boundary; no registration authority grant is introduced by the current extension model;
- minimization/purpose/right constraints remain enforced by their semantic owners — `PASS`;
- stale authorization/gate-decision and Product Contract continuity cannot self-advance — `PASS`;
- P5.04/P5.05 convenience surfaces remain non-authoritative and delegate to existing semantic owners — `PASS`;
- no second IAM/PDP/PEP, authority registry or policy engine is introduced — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #223`, 634 tests, `OK`).

### P5.07 — Event/provenance/portability integration support

Status: `Complete` — [`review evidence`](../reviews/P5-07-event-provenance-portability-integration-support.md).

P5.07 exposes the smallest bounded integration helper for correct Event attribution, provenance and portable semantic state through the R14-hardened composition path while preserving the existing P2.05 Event/provenance semantic owner.

Exit evidence:

- integration-originated governed actions remain attributable to exact actor/execution/contract/version context — `PASS`;
- represented-actor attribution is preserved without erasing the actual actor — `PASS`;
- derived telemetry remains explicitly non-authoritative — `PASS`;
- portable fixtures preserve semantic identities, role distinctions and relationships without fabricating Canonical Typed Relationships — `PASS`;
- duplicate/conflicting Event delivery semantics remain owned by P2.05 — `PASS`;
- no specific infrastructure vendor, broker/store/tracing backend or serialization/wire contract is required — `PASS`;
- no permission, Organizational Authority, approval, capability lifecycle or Stable/public boundary is inferred — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #237`, 653 tests, `OK`).

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
- current dependency-support evidence / stale-evidence fail-closed behavior;
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
- version negotiation/migration/freshness protocol;
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

> **P5.08 — Workspace/capability integration adapters without private coupling.**

P5.08 should demonstrate consumption of M3/M4 workspace/capability surfaces through explicit integration boundaries without private imports or shared-state shortcuts. Capability-specific authority, freshness, rights and data-governance semantics must remain with their existing owners, while product-specific task/disposition semantics remain product-owned. CAP-001 through CAP-004 remain `Incubating / Provisional`; P5.08 does not promote them or create a Stable/public adapter contract merely by implementation.
