# Phase 5 — SDK, Contracts and Extension Experience

Status: `Active`
Version: `1.14.0`
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
22. [`R16 M5 Integration Hardening Review`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation; hosted `Reference Python CI #262` passes 695 tests with `OK`;
23. [`P5.11 Compatibility / ADR / Refactoring / Public-Boundary Hardening Review`](../reviews/P5-11-compatibility-adr-refactoring-public-boundary-hardening-review.md) — `PASS`; all nine explicit architecture/public-boundary gates remain un-crossed, no ADR or Stable/public boundary is justified, no material runtime refactor is required before P5.12, and hosted `Reference Python CI #266` passes 704 tests with `OK`.

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
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | 🟩 Complete | `██████████ 100%` |
| `P5.12` | Phase 5 / M5 closure review | 🟨 Current | `░░░░░░░░░░ 0%` |

The detailed implementation/review evidence for completed work remains in the linked review artifacts and git history. This roadmap records planning state and the minimum evidence needed for the next decision; it does not replace those semantic owners or review records.

## 5. Accumulated Phase 5 evidence

### Product Contract and compatibility

- RFC-0004 `ProductContract` remains the single executable product/platform boundary owner for the bounded reference implementation.
- P5.02 machine-checks the existing declaration model rather than creating a competing manifest/schema source.
- R13 preserves provider/consumer/failure responsibilities and operation failure semantics in derived declaration evidence.
- P5.03 resolves only exact declared dependency versions from explicit governed provider/version evidence; no SemVer/package/module/dataclass inference or automatic fallback is used.
- Deprecated, Retired, Unsupported, VersionMismatch and Ambiguous paths remain explicit and fail closed; changed reliance exposes migration obligations.
- R14 requires explicit current governed provider/version evidence for dependency-backed reliance and prevents composition-time compatibility evidence from becoming current support authority.
- R16 binds capability-adapter semantics to the exact P5.02 declaration evidence validated by the facade, so alternate same-version Product Contract semantics fail closed.

### Composition, scaffolding and reuse

- P5.04 establishes a bounded internal/provisional integration composition seam over existing semantic owners.
- P5.05 provides readable, replaceable provisional scaffolding and an in-process local harness without production infrastructure assumptions.
- P5.08 adds the internal/provisional integration adapter seam over workspace/capability consumption.
- P5.09 proves materially distinct reuse with a read-only CAP-004 evidence/reconstruction extension using its own `Provisional 0.1.0` Product Contract.
- R15 narrows demonstrated shared adapter state to `facade + capabilities`; workspace remains an explicit optional binding.
- Product/extension-specific business semantics remain consumer-owned.

### Security, authority, evidence and portability

- Wrong-Organization, missing/denied Authorization/Organizational Authority, purpose/right/classification and stale-continuity paths remain fail closed through existing semantic owners.
- Product Contract/capability admission grants no Authentication, Authorization, permission, Organizational Authority or approval.
- Governed Execution remains the only consequential mutation path for the exercised boundary.
- P5.07 preserves exact Actor/Product/Product Contract/Execution/Event attribution while retaining P2.05 as Event/provenance semantic owner.
- Derived telemetry and CAP-004 reconstruction remain non-authoritative.
- Portable integration fixtures preserve semantic identity/relationship meaning without selecting a durable vendor serialization or transport mechanism.

### Conformance and hardening

- P5.10 indexes `CF-01` through `CF-15` across positive and negative executable evidence without becoming a second semantic owner.
- R16 re-opens the matrix and resolves the only material same-version Product Contract continuity defect found in that hardening pass.
- P5.11 adds nine executable architecture/public-boundary guards and explicitly reviews every listed ADR/public-compatibility threshold.
- Hosted `Reference Python CI #266` passes the full accumulated 704-test suite with `OK`.

## 6. Engineering gates

Engineering reviews are gates, not equal-weight roadmap work items.

- `R13 — Integration Boundary Review` — **Complete / PASS after R13-F1 remediation**.
- `R14 — Developer Safety / Contract Health Review` — **Complete / PASS after R14-F1/R14-F2 remediation**.
- `R15 — Reuse / Developer Experience Refactoring Review` — **Complete / PASS after R15-F1/R15-F2 remediation**.
- `R16 — M5 Integration Hardening` — **Complete / PASS after R16-F1 remediation**.

Performance optimization remains evidence-backed; do not optimize package/API/runtime mechanics without benchmark/profile evidence except correctness, security or resource-exhaustion defects.

## 7. Dependency-aware sequence

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
P5.11 Compatibility / ADR / public-boundary review ✓
 ↓
P5.12 M5 closure ← current
 ↓
M5
```

## 8. P5.11 disposition

P5.11 is `Complete` — [`review evidence`](../reviews/P5-11-compatibility-adr-refactoring-public-boundary-hardening-review.md).

All explicit gates were reviewed:

| Gate | P5.11 result |
|---|---|
| language-specific SDK/package boundary | Not crossed — no ADR / no public boundary |
| stable/public API or wire/serialization contract | Not crossed — no ADR / no public boundary |
| package registry/distribution topology | Not crossed — no ADR |
| plugin loading/sandboxing/isolation mechanism | Not crossed — no ADR |
| extension registry/discovery topology | Not crossed — no ADR |
| version negotiation/migration/freshness protocol | Not crossed — no ADR |
| generated-code compatibility boundary | Not crossed — no ADR / no public boundary |
| separately deployable integration service | Not crossed — no ADR |
| stable design-system/component integration contract | Not crossed — no ADR / no public boundary |

Refactoring disposition:

- no material runtime refactor is justified before P5.12;
- retain Product Contract declaration/validation + exact governed compatibility + composition + adapters as internal/provisional reference architecture;
- retain `IntegrationAdapters.workspace` and `LocalIntegrationHarnessResult.facade` only as bounded internal compatibility conveniences/watch items rather than public contracts;
- do not extract a generic SDK/package, plugin system, registry, wire DTO layer, generated-client boundary or deployable integration service without new evidence and the applicable governed decision.

Hosted `Reference Python CI #266` passes 704 tests with `OK`, including all nine P5.11 guards.

## 9. M5 exit criteria

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

Items 1–13 now have accumulated evidence. **M5 is not yet achieved:** P5.12 remains the explicit closure decision.

M5 does not require a public SDK, Stable Product Contract or production deployment. If later evidence justifies such a boundary, it must be governed separately before that claim is made.

## 10. Current canonical action

> **P5.12 — Phase 5 / M5 closure review.**

Close Phase 5 only on repository evidence. Re-check all M5 exit criteria, current hosted test evidence, unresolved findings and canonical-state consistency. The closure result must distinguish roadmap completion from Product Contract stability, capability lifecycle, operational readiness, conformance maturity and public/commercial commitments.

Do not infer from P5.11 that any Product Contract is `Stable`, any capability is `Active`, any public SDK/API/wire/package boundary exists, or M5 is already achieved.

## 11. ADR and Product Contract gate

P5.11 records an explicit **no-ADR / no-public-boundary** disposition for the current implementation.

Re-open the ADR/governance gate before material reliance on a language-specific SDK/package boundary, stable/public API or wire/serialization contract, package registry/distribution topology, plugin loading/sandboxing mechanism, extension registry topology, version-negotiation/migration/freshness protocol, generated-code compatibility boundary, separately deployable integration service or stable design-system/component contract.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.
