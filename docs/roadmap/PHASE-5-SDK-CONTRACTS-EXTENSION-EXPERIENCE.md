# Phase 5 — SDK, Contracts and Extension Experience

Status: `Active`
Version: `1.13.0`
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
14. [`P5.05 scaffolding/templates + local harness review`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`; bounded readable scaffolding and an in-process harness consume the governed composition path without copying product implementation, creating a second contract source or requiring production infrastructure; R15 later aligns their developer-facing entry with the demonstrated adapter seam;
15. [`P5.06 security/authority/rights Organization-scope integration-guard review`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`; wrong-Organization, missing/denied Authorization/Organizational Authority, purpose/right and stale-continuity paths fail closed through existing semantic owners, with hosted `Reference Python CI #223` passing 634 tests;
16. [`R14 Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation; normal facade construction is forced through P5.02/P5.03 and dependency-backed J1/J2 actions require explicit current governed provider/version evidence instead of silently reusing composition-time compatibility; hosted `Reference Python CI #232` passes the full 644-test reference suite;
17. [`P5.07 Event/provenance/portability integration-support review`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`; bounded integration evidence now preserves exact Actor/Product/Product Contract/Execution/Event attribution, delegates canonical Event semantics to P2.05, keeps telemetry non-authoritative and portable semantic fixtures non-canonical/vendor-neutral; hosted `Reference Python CI #237` passes the full 653-test reference suite;
18. [`P5.08 workspace/capability integration-adapter review`](../reviews/P5-08-workspace-capability-integration-adapters.md) — `PASS`; product-side integration now consumes workspace/CAP-001..CAP-004 through one internal/provisional adapter seam without private coupling, and hosted `Reference Python CI #242` supplies the previously pending full-suite verification;
19. [`P5.09 second materially distinct integration reuse proof`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md) — `PASS`; a read-only CAP-004 evidence/reconstruction extension reuses the same Product Contract/composition/adapter boundary as the first product, exposes no workspace or canonical mutation path, and refines one overfitted internal P5.02 read-only assumption without weakening direct canonical-read or mutation gates; hosted `Reference Python CI #242` passes the full 675-test suite;
20. [`R15 Reuse / Developer Experience Refactoring Review`](../reviews/R15-reuse-developer-experience-refactoring-review.md) — `PASS` after R15-F1/R15-F2 remediation; the demonstrated shared adapter state is narrowed to facade + capability delegation, workspace becomes an explicit optional consumer binding, and P5.05 scaffold/harness guidance is aligned with the reused adapter seam without creating a public/stable boundary; hosted `Reference Python CI #251` passes the 682-test R15 code/refactoring head;
21. [`P5.10 Phase 5 conformance + architecture fitness matrix`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`; all 15 required cross-cutting dimensions have positive and negative executable anchors across P5.02–P5.09 and R13–R15, the matrix remains an evidence index rather than a semantic owner, and hosted `Reference Python CI #256` passes 688 tests on the P5.10 implementation head;
22. [`R16 M5 Integration Hardening Review`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation; capability-adapter construction now requires exact equality with the P5.02 declaration evidence already validated by the facade, so alternate same-version Product Contract semantics fail closed while all P5.10 `CF-01` through `CF-15` evidence remains green; hosted `Reference Python CI #262` passes the full 695-test implementation-head suite.

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
| `P5.08` | Workspace/capability integration adapters without private coupling | 🟩 Complete | `██████████ 100%` |
| `P5.09` | Second materially distinct integration reuse proof | 🟩 Complete | `██████████ 100%` |
| `P5.10` | Phase 5 conformance + architecture fitness matrix | 🟩 Complete | `██████████ 100%` |
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.12` | Phase 5 / M5 closure review | ⬜ Planned | `░░░░░░░░░░ 0%` |

P5.01 completion evidence:

- [`P5-01-integration-boundary-revalidation-developer-journeys.md`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`;
- J1 = governed read/composition consumer;
- J2 = consequential product action through exact Product Contract continuity and Governed Execution;
- J3 = read-only evidence/reconstruction extension candidate, now realized by P5.09 as the second materially distinct reuse proof;
- current Python imports, module paths, dataclass shapes, operation-token spellings and monorepo package layout remain internal/provisional evidence rather than a Stable/public SDK contract.

P5.02 completion evidence:

- [`P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`;
- the existing RFC-0004 `ProductContract` remains the single executable declaration model for the bounded reference implementation;
- an internal/provisional whole-declaration validator preserves exact Product Contract/Product/dependency/operation/canonical-access semantics and fail-closes missing boundary requirements;
- P5.09-F1 later refines the internal implementation assumption that every read-only operation must expose direct canonical access: derived read-only views may declare no direct canonical access, while any declared direct canonical access and all canonical mutation requirements remain fail-closed;
- validation evidence grants no Authentication, Authorization, Organizational Authority, approval, permission or capability activation;
- dependency `provisional` remains a Product Contract reliance/support qualifier and does not replace the capability catalog lifecycle;
- no YAML/JSON/protobuf/OpenAPI/public SDK/API/wire/package/registry boundary was selected;
- hosted `Reference Python CI` run `#205` passed the full reference suite; P5.09's refinement is covered by hosted `Reference Python CI #242` and R15 regression evidence by `#251`.

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
- `reference/python/arvectum_os_ref/integration_scaffolding.py` adds a tiny explicit provisional template and local in-process harness over the existing governed composition path;
- after R15, rendered entry code imports Arvectum OS through `arvectum_os_ref.integration_adapters` and opts into workspace explicitly, remaining readable/replaceable rather than becoming a generated-code compatibility contract;
- the local harness consumes the exact Product Contract, Actor, effective Product Contract Version and explicit governed provider/version evidence, composes `IntegrationAdapters`, then binds a `NON_AUTHORITATIVE` workspace explicitly;
- `LocalIntegrationHarnessResult` stores the shared adapter core; `facade` remains only an internal compatibility accessor over `adapters.facade`;
- Product Contract construction, dependency resolution, authorization/authority, capability lifecycle and product-domain semantics remain with their existing owners;
- no database, broker, IAM provider, object store, registry, network endpoint or deployable service is required;
- `reference/python/tests/test_p5_05_integration_scaffolding_local_harness.py` retains focused regression/fitness coverage and is exercised by R15 `Reference Python CI #251`.

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
- hosted `Reference Python CI #223` passed the full 634-test reference suite; R15 `#251` confirms accumulated guards remain green after scaffold/adapter refactoring.

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
- hosted `Reference Python CI #232` passed the full 644-test reference suite with `OK`, and R15 `#251` preserves those regressions.

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

P5.08 completion evidence:

- [`P5-08-workspace-capability-integration-adapters.md`](../reviews/P5-08-workspace-capability-integration-adapters.md) — `PASS`;
- `reference/python/arvectum_os_ref/integration_adapters.py` exposes the smallest internal/provisional integration-facing adapter seam above the R14-hardened composition facade;
- the first bounded product adapter journey imports Arvectum OS only through `arvectum_os_ref.integration_adapters` and does not import workspace/capability private implementation modules;
- workspace navigation remains non-authoritative and Organization-scoped; capability-specific authority/freshness/rights semantics remain with existing semantic owners;
- current governed provider/version evidence remains required at dependency-backed adapter calls;
- R15 later narrows shared stored adapter state to `facade + capabilities`; workspace remains available through an explicit optional binding rather than being carried eagerly by every consumer;
- R16 later binds capability-adapter construction to the exact P5.02 declaration evidence already validated by the facade, preventing alternate same-version Product Contract semantics from entering capability delegation;
- no capability promotion, Stable/public SDK/API/package or new authority source is created;
- hosted `Reference Python CI #262` passes the accumulated 695-test suite after R16 hardening.

P5.09 completion evidence:

- [`P5-09-second-materially-distinct-integration-reuse-proof.md`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md) — `PASS`;
- the second consumer is an Organization-scoped read-only evidence/reconstruction extension with its own `Provisional 0.1.0` Product Contract and only CAP-004 dependency;
- the second extension journey imports the same `arvectum_os_ref.integration_adapters` module as the first bounded product journey and imports no private CAP-004/Event/workspace/canonical-state implementation modules;
- the second integration has no workspace, task/disposition or canonical-mutation behavior and therefore is materially distinct rather than a renamed first consumer;
- CAP-004 Organization/purpose/right/classification/redaction semantics remain owned by CAP-004/P3.07 and current provider/version evidence remains required by R14/P5.08;
- P5.09-F1 removes an overfitted internal P5.02 assumption that every read-only operation must declare direct canonical Read access; derived read-only views may now truthfully declare no direct canonical access, while declared direct reads and canonical mutation remain fail-closed;
- reuse evidence supports retaining Product Contract + exact dependency resolution + composition + adapter seams and rejecting premature public SDK/plugin/registry/DTO generalization;
- no Product Contract or capability lifecycle promotion is inferred from second-consumer success;
- hosted `Reference Python CI #242` passes all 675 tests with `OK`; R15 `#251` explicitly re-exercises the P5.09-F1 distinction and R16 `#262` preserves the same second-consumer path after adapter hardening.

R15 completion evidence:

- [`R15-reuse-developer-experience-refactoring-review.md`](../reviews/R15-reuse-developer-experience-refactoring-review.md) — `PASS` after two bounded findings were remediated;
- R15-F1 removes first-consumer workspace presentation from shared `IntegrationAdapters` stored state: the demonstrated cross-consumer core is the exact facade plus capability delegation;
- workspace is now an explicit optional binding through `compose_workspace_adapter(...)`; the lazy `adapters.workspace` property remains only as internal compatibility convenience;
- R15-F2 aligns P5.05 scaffolding/local harness with the adapter seam proven by both P5.08/P5.09 consumers rather than teaching the lower-level facade as the default integration entry;
- P5.09-F1 remains intact and gets focused regression coverage for derived read-only versus direct canonical access;
- R14 explicit current governed provider/version evidence remains required; no cache/freshness registry or automatic compatibility self-advance is introduced;
- no public SDK/API/package/wire/registry/plugin-runtime/DTO boundary, Product Contract stabilization, capability promotion, new authority source, readiness or conformance claim is created;
- no Constitution/RFC amendment or ADR is required because the refactor remains internal/provisional below existing semantic owners;
- `reference/python/tests/test_r15_reuse_developer_experience_refactoring_review.py` adds 7 focused review regressions;
- hosted `Reference Python CI #251` passes the 682-test reference suite on the R15 code/refactoring head.

P5.10 completion evidence:

- [`P5-10-phase-5-conformance-architecture-fitness-matrix.md`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`;
- all 15 minimum Phase 5 matrix dimensions are represented exactly once as `CF-01` through `CF-15`;
- every matrix row carries both positive and negative/fail-closed executable evidence;
- the executable index resolves anchors across P5.02, R13, P5.03, P5.04, P5.05, P5.06, P5.07, P5.08, P5.09, R14 and R15 instead of allowing P5.10 to self-certify semantics;
- Product Contract identity/version, exact dependency responsibilities, current provider support, hidden-coupling prohibition, Organization isolation, authority separation, governed mutation, Event/provenance, rights/minimization, portability, lifecycle separation, deprecated/unsupported behavior, second-consumer reuse and no-public/stable-boundary invariants all have executable positive/negative evidence;
- P5.10 remains an evidence index and does not become a second semantic owner, compatibility service, permission/authority source or lifecycle/public-boundary decision;
- no Constitution/RFC amendment or ADR is required by the matrix itself;
- hosted `Reference Python CI #256` passes 688 tests with `OK` on the P5.10 implementation head; R16 `#262` re-runs the full accumulated matrix together with focused hardening regressions and remains green.

R16 completion evidence:

- [`R16-m5-integration-hardening.md`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation;
- R16 uses P5.10 `CF-01` through `CF-15` as a regression/evidence index rather than replacing their semantic owners;
- R16-F1 identified that a capability adapter could receive a separate same-version `ProductContract` value whose deeper declaration semantics differed from the declaration already validated by the facade;
- `IntegrationCapabilityAdapter` now reuses `validate_product_contract_declaration()` and requires exact equality with `facade.declaration_evidence` before any capability-specific delegation;
- same-version bounded-scope drift and dependency consumer-responsibility drift fail closed through focused regressions;
- R14 current governed provider/version evidence, Organization isolation, rights/minimization, Governed Execution, Event/provenance and second-consumer reuse remain unchanged and green;
- the remediation creates no permission, Organizational Authority, approval, new Product Contract model, registry, stable/public SDK/API/package/wire boundary, Product Contract stabilization or capability promotion;
- no RFC/ADR is required because the correction is a bounded internal/provisional continuity check using an existing semantic owner;
- hosted `Reference Python CI #262` passes 695 tests with `OK`, including all 7 focused R16 cases and the complete accumulated P5.10 matrix evidence.

## 5. Engineering gates

Engineering reviews are gates, not equal-weight roadmap work items.

- `R13 — Integration Boundary Review` — **Complete / PASS after R13-F1 remediation**. Product Contract remains the single governed semantic owner; derived validation evidence preserves boundary responsibilities without becoming a second contract system.
- `R14 — Developer Safety / Contract Health Review` — **Complete / PASS after R14-F1/R14-F2 remediation**. Normal facade construction cannot bypass P5.02/P5.03, and dependency-backed J1/J2 reliance cannot silently reuse composition-time provider compatibility.
- `R15 — Reuse / Developer Experience Refactoring Review` — **Complete / PASS after R15-F1/R15-F2 remediation**. Shared adapter state is narrowed to demonstrated reuse, workspace is optional, P5.09-F1 is preserved and scaffolding follows the reused adapter seam without public-boundary inflation.
- `R16 — M5 Integration Hardening` — **Complete / PASS after R16-F1 remediation**. The adapter seam now fails closed on alternate same-version Product Contract declaration semantics while preserving existing semantic owners and all P5.10 evidence.

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
P5.08 Workspace/capability adapters ✓
 ↓
P5.09 Second integration reuse proof ✓
 ↓
R15 Reuse / DX Refactoring ✓
 ↓
P5.10 Conformance + fitness matrix ✓
 ↓
R16 M5 Hardening ✓
 ↓
P5.11 Compatibility / ADR / public-boundary review ← current
 ↓
P5.12 M5 closure
 ↓
M5
```

P5.10 supplies the accumulated evidence index and R16 has hardened that surface. P5.11 is now the current gate for deciding whether any implementation mechanism has actually crossed an ADR or Stable/public compatibility threshold.

## 7. Work-item intent and exit evidence

### P5.01 — Integration boundary revalidation + developer journeys

Status: `Complete` — [`review evidence`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md).

P5.01 revalidated Phase 5 against actual M4 evidence and identified the smallest real integration journeys worth supporting. The Product Contract remains the governed boundary authority; exact dependency/operation/version semantics are relied-upon integration semantics; current repository import/module/dataclass shape remains implementation-private.

Exit evidence:

- at least two bounded integration journeys are described — `PASS` (J1 and J2; J3 retained as a future reuse candidate and realized by P5.09);
- private/internal coupling points are explicitly prohibited — `PASS`;
- no public/stable compatibility promise is inferred — `PASS`;
- candidate tooling surfaces are classified as internal/provisional until proven otherwise — `PASS`.

P5.01 changes no runtime behavior and intentionally does not create an SDK/declaration implementation ahead of P5.02.

### P5.02 — Product Contract declaration model + machine-checkable validation baseline

Status: `Complete` — [`review evidence`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md).

P5.02 validates the existing RFC-0004 Product Contract declaration as a whole rather than creating a second manifest/schema system. The implementation is internal/provisional and intentionally supports the current Provisional reference baseline. P5.09 later refines only the implementation assumption that every read-only operation necessarily exposes direct canonical access; derived read-only views may declare none, without changing direct-read or mutation gates. R15 preserves that distinction unchanged.

Exit evidence:

- exact contract identity/version and declared capability/dependency versions and operations can be validated — `PASS`;
- required authority/security/data and applicable canonical-access/portability/review/exit declarations fail closed when missing or invalid — `PASS`;
- tooling does not create permission or Organizational Authority — `PASS`;
- Product Contract lifecycle remains distinct from capability lifecycle — `PASS`;
- hidden product/platform coupling mechanisms are rejected — `PASS`;
- no stable/public representation or ADR-triggering mechanism is selected — `PASS`;
- hosted full reference CI — `PASS` (`#205`; P5.09 refinement covered by `#242`; R15 preservation covered by `#251`; R16 continuity hardening covered by `#262`).

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
- hosted full reference CI — `PASS` (`Reference Python CI #217`; accumulated R16 `#262` remains green).

### P5.04 — Integration composition API/facade boundary

Status: `Complete` — [`review evidence`](../reviews/P5-04-integration-composition-api-facade-boundary.md).

P5.04 extracts the smallest reusable integration-facing composition boundary justified by J1/J2 without exposing product code to the implementation-private runtime/capability/workspace module graph.

Exit evidence:

- product-owned P5.04 J1/J2 journey code imports no private runtime/capability/workspace implementation modules — `PASS`;
- the product journey sees Arvectum OS through one internal/provisional integration facade module — `PASS` for the P5.04 evidence slice; P5.08/R15 later establish the higher adapter-facing default for bounded integration consumers;
- facade construction consumes exact P5.02 declaration and P5.03 dependency/version resolution semantics — `PASS`;
- exact Product Contract/Product/dependency/version/operation continuity remains fail-closed — `PASS`;
- capability admission, workspace authority and consequential execution delegate to existing semantic owners — `PASS`;
- facade construction/admission grants no Authorization, Organizational Authority or capability activation — `PASS`;
- product-domain semantics remain product-owned and capability-specific adapters remain P5.08 scope — `PASS`;
- no language/network/wire/package choice is declared Stable/public merely by implementation — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #222`, 615 tests, OK; accumulated R16 `#262` remains green).

R14 later hardens this boundary by restricting normal construction to the governed P5.02/P5.03 factory path and requiring current governed provider/version evidence at dependency-backed actions. R15 leaves this semantic composition path intact below the adapter seam, and R16 binds that seam back to the exact validated declaration evidence.

### P5.05 — Scaffolding/templates + local integration harness

Status: `Complete` — [`review evidence`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md), refined by [`R15`](../reviews/R15-reuse-developer-experience-refactoring-review.md).

P5.05 provides reversible helpers that reduce repeated setup for a bounded integration while keeping generated/templated code understandable, replaceable and explicitly provisional. R15 aligns the current developer-facing scaffold with the P5.08/P5.09 adapter seam demonstrated by both consumers.

Exit evidence:

- a new bounded integration can be initialized without copying an existing product implementation — `PASS`;
- generated/template artifacts identify provisional boundaries — `PASS`;
- local tests require no production infrastructure assumptions — `PASS` by implementation/test design;
- Product Contract and dependency/version semantics remain owned by RFC-0004/P5.02/P5.03 rather than the scaffold — `PASS`;
- the current starter imports only `arvectum_os_ref.integration_adapters` and workspace is an explicit consumer opt-in — `PASS` after R15-F2;
- exact Product Contract Version continuity and non-authoritative workspace presentation are preserved — `PASS`;
- scaffolding/harness grants no Authorization, Organizational Authority, capability activation or operational readiness — `PASS`;
- no Stable/public SDK/API/wire/package/generated-code compatibility boundary is created — `PASS`;
- focused P5.05/R15 executable regression evidence is committed — `PASS`;
- hosted accumulated full reference CI — `PASS` (`Reference Python CI #262`, 695 tests).

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
- hosted full reference CI — `PASS` (`Reference Python CI #223`, 634 tests, `OK`; accumulated R16 `#262` remains green).

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
- hosted full reference CI — `PASS` (`Reference Python CI #237`, 653 tests, `OK`; accumulated R16 `#262` remains green).

### P5.08 — Workspace/capability integration adapters without private coupling

Status: `Complete` — [`review evidence`](../reviews/P5-08-workspace-capability-integration-adapters.md), refined by [`R15`](../reviews/R15-reuse-developer-experience-refactoring-review.md) and hardened by [`R16`](../reviews/R16-m5-integration-hardening.md).

P5.08 demonstrates integration with the M3/M4 surfaces through an explicit internal/provisional adapter seam, preserving Incubating capability status and product ownership of product semantics. R15 narrows only the shared stored adapter shape from two-consumer evidence; R16 binds the retained capability adapter to the exact P5.02 declaration evidence already validated by the facade. Neither review replaces semantic owners.

Exit evidence:

- CAP-001..CAP-004 and workspace composition are consumed without product-side internal imports/private state — `PASS`;
- capability-specific authority/freshness/rights semantics remain owned by capabilities — `PASS`;
- product-specific task/disposition semantics remain outside shared platform abstractions — `PASS`;
- current governed dependency/version evidence remains required at dependency-backed adapter calls — `PASS`;
- shared `IntegrationAdapters` stored state is limited to facade + capability delegation; workspace is an explicit optional binding — `PASS` after R15-F1;
- capability adapter contract semantics must equal facade declaration evidence for the same exact Product Contract Version — `PASS` after R16-F1;
- hosted full reference CI — `PASS` (`Reference Python CI #262`, 695 tests, `OK`).

### P5.09 — Second materially distinct integration reuse proof

Status: `Complete` — [`review evidence`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md).

P5.09 builds the P5.01 J3 read-only evidence/reconstruction extension as a second bounded integration materially different from the first and uses it to validate reuse rather than self-confirming abstraction.

Exit evidence:

- both integrations use the same declared Product Contract/composition/`IntegrationAdapters` boundary/tooling — `PASS`;
- no copy/paste of implementation-private platform code is required — `PASS`;
- differences remain consumer-owned where appropriate: extension identity/contract and inspection presentation remain outside platform semantics — `PASS`;
- capability-specific reconstruction, access and redaction rules remain with CAP-004/P3.07 — `PASS`;
- P5.09-F1 identifies and removes one abstraction overfit: derived read-only operations need not pretend to have direct canonical access — `PASS`;
- retained direct canonical-read checks, canonical Write/Organizational Authority mutation checks and current provider/version evidence remain fail-closed — `PASS`;
- reuse evidence is sufficient to retain the Product Contract/resolution/composition/adapter seams and reject premature public SDK/plugin/registry/DTO generalization — `PASS`;
- no Product Contract/capability lifecycle promotion or Stable/public boundary is inferred — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #262`, 695 tests, `OK` after R16 hardening).

### P5.10 — Phase 5 conformance + architecture fitness matrix

Status: `Complete` — [`review evidence`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md).

P5.10 accumulates the phase's positive and negative evidence into a machine-checked cross-cutting index. The matrix is intentionally not a new semantic owner and does not restate Product Contract, compatibility, security, Event or lifecycle logic as independent runtime behavior.

Exit evidence:

- all 15 minimum matrix dimensions are represented as `CF-01` through `CF-15` — `PASS`;
- every row has positive and negative/fail-closed executable evidence — `PASS`;
- all evidence anchors resolve to current test classes/methods — `PASS`;
- the evidence index spans P5.02, R13, P5.03, P5.04, P5.05, P5.06, P5.07, P5.08, P5.09, R14 and R15 rather than self-certifying P5.10 — `PASS`;
- no capability/Product Contract lifecycle promotion, authority grant, public/stable boundary, operational-readiness or M5 conformance claim is created — `PASS`;
- no RFC/ADR is required because no new durable mechanism or Accepted architecture contract is selected — `PASS`;
- hosted accumulated full reference CI after R16 — `PASS` (`Reference Python CI #262`, 695 tests, `OK`).

### P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review

Status: `Current`.

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

Create ADR/RFC/policy only if the corresponding threshold is actually crossed. If no threshold is crossed, record an explicit no-ADR/no-public-boundary disposition and preserve the internal/provisional implementation.

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

> **P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review.**

Review the accumulated Phase 5 implementation for actual compatibility and architecture-governance thresholds. Determine whether any language SDK/package, public API/wire contract, registry/distribution mechanism, plugin/extension runtime, version-negotiation/migration/freshness mechanism, generated-code boundary, separately deployable integration service or stable design-system boundary is now materially relied upon. Create an ADR/RFC/policy only where the established threshold is actually crossed; otherwise record an explicit no-ADR/no-public-boundary disposition and preserve the internal/provisional implementation.

After P5.11, proceed to **P5.12 — Phase 5 / M5 closure review**.
