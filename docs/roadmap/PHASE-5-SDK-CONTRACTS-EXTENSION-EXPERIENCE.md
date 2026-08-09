# Phase 5 — SDK, Contracts and Extension Experience

Status: `Complete`
Version: `1.15.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M5 — Repeatable product/extension integration`
Milestone state: `Achieved` for the declared bounded reference scope

## 1. Purpose

Phase 5 turns the governed runtime, shared-capability and workspace evidence from M1–M4 into a repeatable integration experience for products and extensions without prematurely declaring public/stable compatibility boundaries.

The phase proves that a materially distinct integration can be created through explicit Product Contracts, reusable integration tooling and conformance evidence rather than private imports, copied internals or accidental platform coupling.

Phase 5 is not a commitment to publish a public SDK, public API, marketplace, plugin runtime, stable wire protocol or final developer platform. Those boundaries become stable/public only through their applicable evidence and governance.

## 2. Canonical basis

Phase 5 closed against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
3. RFC-0004 — explicit Product Contract boundary, lifecycle separation and hidden-coupling prohibition;
4. M2 — reusable governed Core Runtime baseline;
5. M3 — CAP-001 through CAP-004 retained as `Incubating / Provisional` shared capabilities;
6. M4 — coherent governed workspace baseline and one bounded Product Contract-backed composition proof;
7. P4.08 Product Contract remains `Provisional 0.1.0` and is evidence, not a Stable compatibility promise;
8. P4.12 — `PASS`, M4 achieved for the bounded governed-workspace reference scope;
9. [`P5.01 integration boundary revalidation`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`;
10. [`P5.02 Product Contract declaration/validation review`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`;
11. [`R13 Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation;
12. [`P5.03 governed dependency/version resolution review`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`;
13. [`P5.04 integration composition facade review`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`;
14. [`P5.05 scaffolding/templates + local harness review`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`;
15. [`P5.06 security/authority/rights Organization-scope integration-guard review`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`;
16. [`R14 Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation;
17. [`P5.07 Event/provenance/portability integration-support review`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`;
18. [`P5.08 workspace/capability integration-adapter review`](../reviews/P5-08-workspace-capability-integration-adapters.md) — `PASS`;
19. [`P5.09 second materially distinct integration reuse proof`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md) — `PASS`;
20. [`R15 Reuse / Developer Experience Refactoring Review`](../reviews/R15-reuse-developer-experience-refactoring-review.md) — `PASS` after R15-F1/R15-F2 remediation;
21. [`P5.10 Phase 5 conformance + architecture fitness matrix`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`;
22. [`R16 M5 Integration Hardening Review`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation;
23. [`P5.11 Compatibility / ADR / Refactoring / Public-Boundary Hardening Review`](../reviews/P5-11-compatibility-adr-refactoring-public-boundary-hardening-review.md) — `PASS`, explicit no-ADR/no-public-boundary disposition;
24. [`P5.12 Phase 5 / M5 Closure Review`](../reviews/P5-12-phase-5-m5-closure-review.md) — `PASS`, M5 achieved for the bounded repeatable product/extension integration reference scope;
25. final synchronized pre-closure executable baseline — `Reference Python CI #269`, Ubuntu 24.04.4, CPython 3.12.13, `704 tests`, `OK`.

No conflict with Constitution or Accepted RFC/ADR was identified by the closure review.

## 3. Phase boundary

### Delivered in scope

- integration boundary revalidated from actual M4 evidence;
- internal/provisional developer integration experience built around Product Contracts and governed platform reliance;
- Product Contract declarations and exact dependency/version semantics made machine-checkable where useful;
- bounded scaffolding/templates/helpers and local integration harness retained as replaceable reference tooling;
- security, Organization, authorization, Organizational Authority, rights and current-support continuity guarded fail-closed;
- Event/provenance and semantic portability preserved through existing owners;
- workspace/capability adapters provided without product-side private coupling;
- materially distinct second integration proved against the same reusable boundary;
- cross-phase conformance/architecture-fitness evidence indexed in P5.10;
- R13–R16 hardening/refactoring findings resolved;
- ADR/public-boundary pressure re-opened in P5.11 and explicitly dispositioned;
- M5 closed only after P5.12 repository-evidence review.

### Explicitly not created by Phase 5

- public or Stable SDK/package/API compatibility;
- Stable Product Contract lifecycle;
- Active Platform Capability lifecycle;
- generic plugin/marketplace runtime;
- cross-organization extension distribution rights;
- production package registry/support/SLA commitments;
- fixed REST/GraphQL/gRPC/BFF or serialization/wire topology;
- fixed language-specific SDK as permanent architecture;
- extension registration as Authorization or Organizational Authority;
- consumer-domain semantics hidden inside shared integration helpers;
- Production environment or operational-readiness approval;
- full-platform conformance or commercial compatibility guarantees.

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
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | 🟩 Complete | `██████████ 100%` |
| `P5.12` | Phase 5 / M5 closure review | 🟩 Complete | `██████████ 100%` |

Engineering gates are separate review gates and do not inflate the phase percentage:

- `R13 — Integration Boundary Review` — **Complete / PASS after R13-F1 remediation**;
- `R14 — Developer Safety / Contract Health Review` — **Complete / PASS after R14-F1/R14-F2 remediation**;
- `R15 — Reuse / Developer Experience Refactoring Review` — **Complete / PASS after R15-F1/R15-F2 remediation**;
- `R16 — M5 Integration Hardening` — **Complete / PASS after R16-F1 remediation**.

## 5. Validated integration baseline

The bounded reference integration method is:

```text
Product / Extension-owned Product Contract
        ↓
P5.02 declaration validation
        ↓
P5.03 exact governed dependency/version resolution
        ↓
P5.04 composition facade
        ↓
P5.08 IntegrationAdapters
        ↓
existing capability / workspace / runtime semantic owners
```

The boundary retains these rules:

- RFC-0004 `ProductContract` remains the product/platform semantic owner; no competing manifest/schema source was introduced;
- exact dependency versions are resolved only from explicit governed provider/version evidence;
- compatibility does not infer package/module/dataclass/SemVer compatibility or automatic fallback;
- R14 requires explicit current support evidence at dependency-backed reliance;
- R16 binds capability-adapter Product Contract semantics to the exact declaration evidence already validated by the facade;
- capability-specific rights/freshness/reconstruction semantics remain with their existing semantic owners;
- Governed Execution remains the consequential canonical-mutation path;
- Product Contract/admission/composition evidence grants no permission, Organizational Authority or approval.

## 6. Reuse evidence

P5.09 proves two materially distinct consumers over the same integration-facing adapter seam:

1. the first bounded product integration, with workspace/capability composition and declared consequential behavior;
2. a read-only evidence/reconstruction extension using CAP-004 only, with its own `Provisional 0.1.0` Product Contract, no workspace assumption and no canonical mutation.

The second consumer exposed P5.09-F1: derived read-only capability consumption does not necessarily mean direct canonical read access. The P5.02 validator was narrowed accordingly rather than forcing a fake canonical-read declaration.

R15 then reduced shared adapter state to the demonstrated cross-consumer core (`facade + capabilities`) and left workspace as explicit optional consumer binding. This is validated reuse, not speculative generalization.

## 7. Security, authority, evidence and portability

The closed M5 scope preserves:

- explicit Organization context and fail-closed cross-Organization isolation;
- independent Authentication/Actor attribution, Authorization, Organizational Authority and Data Governance semantics;
- explicit purpose/right/classification/freshness handling under existing semantic owners;
- no authority gain from Product Contract validation, extension registration, adapter composition or capability admission;
- exact Product Contract/Workflow/material-input/Execution/Event attribution where materially relied upon;
- Event/provenance admission through existing RFC-0006/P2 semantic owners;
- derived telemetry, search/projection and reconstruction as non-authoritative;
- semantic portability without selecting one durable vendor transport/serialization/store.

## 8. Conformance, hardening and closure evidence

P5.10 records a 15-row cross-phase evidence index, `CF-01` through `CF-15`. Every row carries positive and negative/fail-closed executable evidence and remains subordinate to the relevant Accepted RFC/Product Contract/capability/runtime semantic owner.

R16 re-opened the accumulated integration surface and fixed R16-F1: same Product Contract Version identity can no longer carry alternate declaration semantics through the capability adapter.

P5.11 then reviewed all nine explicit compatibility/public-boundary gates and found none crossed. It records the explicit **no-ADR / no-public-boundary** disposition and no material runtime refactor before closure.

P5.12 re-checked all 14 M5 exit criteria and closed one subordinate documentation synchronization finding, P5.12-F1: root README lagged the canonical roadmap after P5.11. The closure synchronizes that summary without changing runtime behavior.

## 9. M5 exit criteria — final disposition

| # | Criterion | Final result |
|---|---|---|
| 1 | bounded integration boundary above private internals | `PASS` |
| 2 | explicit/machine-checkable Product Contract declaration evidence | `PASS` |
| 3 | exact dependency/version identity continuity | `PASS` |
| 4 | hidden coupling rejected | `PASS` |
| 5 | security/Organization/Authz/Organizational Authority fail-closed | `PASS` |
| 6 | governed canonical mutation + Event/provenance continuity | `PASS` |
| 7 | vendor-neutral portability evidence | `PASS` |
| 8 | second materially distinct integration reuse | `PASS` |
| 9 | consumer-specific semantics remain consumer-owned | `PASS` |
| 10 | CAP-001..CAP-004 lifecycle not inflated | `PASS` |
| 11 | P5.10 fitness matrix | `PASS` |
| 12 | R13–R16 findings resolved/bounded | `PASS` |
| 13 | P5.11 ADR/public-boundary disposition | `PASS` |
| 14 | P5.12 closure review | `PASS` |

**M5 result:** `Achieved` for the declared bounded repeatable product/extension integration reference scope.

## 10. Lifecycle and readiness state after closure

Phase 5 completion changes roadmap state only.

| Dimension | State after P5.12 |
|---|---|
| Phase 5 | `Complete` |
| M5 | `Achieved` for bounded reference scope |
| P4.08 Product Contract | `Provisional 0.1.0` |
| P5.09 Product Contract | `Provisional 0.1.0` |
| CAP-001..CAP-004 | `Incubating / Provisional` |
| Integration facade/adapters/scaffolding/harness | internal / provisional reference implementation |
| Public SDK/API/wire/package boundary | not established |
| Operational readiness / `Production` | not established |
| Full-platform conformance | not claimed |
| SLA/support/commercial compatibility commitment | not created |

## 11. ADR and public-boundary gate

P5.11 remains the controlling Phase 5 disposition: **no ADR / no public boundary** for the current implementation.

Re-open the ADR/governance gate before material reliance on:

- a supported language-specific SDK/package boundary;
- a Stable/public API or wire/serialization contract;
- package registry/distribution topology;
- plugin loading/sandboxing/isolation;
- extension registry/discovery topology;
- automated version-negotiation/fallback or durable freshness protocol;
- supported generated-code/client compatibility;
- separately deployable integration service;
- stable design-system/component integration contract.

The internal P5.11 watch items `IntegrationAdapters.workspace` and `LocalIntegrationHarnessResult.facade` remain implementation conveniences, not compatibility promises.

## 12. Hosted verification

The final synchronized P5.11 pre-closure baseline is:

- `Reference Python CI #269` — `PASS`;
- Ubuntu 24.04.4;
- CPython 3.12.13;
- `python -m unittest discover -s tests -v`;
- `704 tests`, `OK`.

P5.12 changes closure/review/planning documentation only. The P5.12 pull-request head must remain green before merge; that validation is closure hygiene over the unchanged executable baseline.

## 13. Dependency-aware sequence

```text
M4 ✓
 ↓
P5.01 ✓
 ↓
P5.02 ✓
 ↓
R13 ✓
 ↓
P5.03 ✓
 ↓
P5.04 ✓
 ↓
P5.05 ✓
 ↓
P5.06 ✓
 ↓
R14 ✓
 ↓
P5.07 ✓
 ↓
P5.08 ✓
 ↓
P5.09 ✓
 ↓
R15 ✓
 ↓
P5.10 ✓
 ↓
R16 ✓
 ↓
P5.11 ✓
 ↓
P5.12 ✓
 ↓
M5 ✓
```

## 14. Closure and handoff

Canonical closure record:

- [`P5.12 — Phase 5 / M5 Closure Review`](../reviews/P5-12-phase-5-m5-closure-review.md) — **PASS**.

Phase 5 is **Complete**. M5 is **Achieved** for the bounded repeatable product/extension integration reference scope.

Phase 6 remains `Draft`; M5 closure does not activate it automatically. The next planning action is **Phase 6 boundary revalidation and decomposition** against real product-driven validation needs before Phase 6 implementation becomes active canonical work.
