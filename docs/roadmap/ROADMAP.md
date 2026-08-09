# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.48.1`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.48.1` records **P6.03 Stage 1 — synthetic/anonymized/redacted first real product integration proof** with `PASS` and advances the current canonical action to **P6.03 Stage 2 — one real 44-ФЗ pre-bid case**.

Stage 1 is recorded in [`P6-03-stage-1-first-real-product-workflow-platform-integration.md`](../reviews/P6-03-stage-1-first-real-product-workflow-platform-integration.md). The real `arutyunoveth/ai-corporation` product repository now crosses the explicit Arvectum OS Product Contract boundary through the existing internal/provisional `IntegrationAdapters` seam for CAP-001 exact Document/Artifact reliance and CAP-004 read-oriented reconstruction. The product keeps procurement semantics, RFQ/TKP/economics/recommendation logic and all external actions outside the platform.

Stage 1 preserves exact P6.02 `Provisional 0.1.0`, exact CAP-001/CAP-004 Provisional `1.0.0` provider evidence, wrong-Organization and purpose/right/classification denial, fail-closed missing/incompatible/deprecated provider evidence, truthful incomplete/redacted reconstruction and rejection of hidden platform coupling. It also exposed a real reference-runtime gap: RFC-0002 `External Reference` authority could not previously be represented without falling back to `Native`. The bounded remediation requires an explicit external-authority contract and prohibits Native authority substitution rather than creating a new source of truth.

Hosted Arvectum OS `Reference Python CI #274` is green at `713 tests`, `OK`, including all nine new P6.03 Stage 1 platform tests. Product `ai-corporation` CI `#1922` completed with all jobs green, including the dedicated cross-repository P6.03 proof and the full `make test` regression; product PR `#140` was then squash-merged to `main` as `5d1c0e5f096188cc1028cc2bf79ace325d0a5167`. Platform PR `#77` was squash-merged as `8c838edafeb564862b88230cba1b6ea02b7c8e14`.

R17 remains `PASS`. P6.03 itself remains **In Progress**. Stage 2 is authorized only for exactly one real 44-ФЗ case under the same Product Contract unless real evidence first requires a new immutable Product Contract version. Stage 3 remains blocked until Stage 2 evidence is reviewed. P6.04 remains downstream of completed P6.03 adoption evidence.

The first real Product Contract remains [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`, for the selected Arvectum procurement/tender AI operator bounded 44-ФЗ pre-bid workflow. It declares exactly CAP-001 + CAP-004 at Provisional capability contract `1.0.0`, deliberately omits CAP-002/CAP-003, preserves external authority for ЕИС/partner/supplier source documents, keeps procurement-domain semantics product-owned and admits no automated external mutation or organizational commitment.

P6.01 and P6.02 remain complete under [`P6.01`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md) and [`P6.02`](../reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md). Empirical real-customer KPI values not yet observed remain evidence gaps rather than fabricated baselines.

Phase 5 closure remains based on [`P5.12`](../reviews/P5-12-phase-5-m5-closure-review.md): `PASS — M5 achieved for the declared bounded repeatable product/extension integration reference scope.` The final synchronized pre-closure hosted baseline remains `Reference Python CI #269`, CPython 3.12.13, `704 tests`, `OK`.

## 3. Verified architecture and milestone baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete / achieved;
- Phase 1 / `M1` — complete / achieved;
- Phase 2 / `M2` — complete / achieved for the bounded reusable-runtime reference scope;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- Phase 4 / `M4` — complete / achieved for the bounded governed-workspace reference scope;
- Phase 5 / `M5` — complete / achieved for the bounded repeatable integration reference scope;
- [`P5.12 closure review`](../reviews/P5-12-phase-5-m5-closure-review.md) — `PASS`;
- [`P6.01 real target + evidence baseline`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md) — `PASS`;
- [`P6.02 first real Product Contract review`](../reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md) — `PASS`;
- [`P6.02 first real Product Contract`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`;
- [`R17 First Product Boundary Review`](../reviews/R17-first-product-boundary-review.md) — `PASS`;
- [`P6.03 Stage 1 first real product integration`](../reviews/P6-03-stage-1-first-real-product-workflow-platform-integration.md) — `PASS`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 Product Contracts remain `Provisional 0.1.0` reference evidence;
- P6.02 real procurement Product Contract remains `Provisional 0.1.0` and does not stabilize the integration boundary;
- no Platform Capability is `Active` merely because M3–M5, P6.01/P6.02, R17 or P6.03 Stage 1 are complete;
- no Stable/public SDK, API, wire, package or service compatibility boundary has been created;
- no production/operational-readiness or SLA/support commitment is implied.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Executed | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Active | 🟨 Active | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Near-term | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 5 — SDK, Contracts and Extension Experience

Canonical detailed evidence:

- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Complete`, M5 `Achieved`;
- [`P5.12 — Phase 5 / M5 Closure Review`](../reviews/P5-12-phase-5-m5-closure-review.md) — `PASS`.

All `P5.01` through `P5.12` work items and R13–R16 engineering gates are complete.

M5 proves repeatable governed integration through explicit Product Contracts and reusable internal/provisional tooling. It does not establish a public SDK, Stable Product Contract, Active capability, production deployment or customer-facing support/compatibility promise.

## 6. Active Phase 6 — Product-driven Platform Validation

Canonical detailed roadmap:

- [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md) — `Active 1.4.0`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P6.01` | Real product/workflow validation target selection + evidence baseline | 🟩 Complete | `██████████ 100%` |
| `P6.02` | First real Product Contract boundary + bounded adoption plan | 🟩 Complete | `██████████ 100%` |
| `P6.03` | First real product/workflow platform integration | 🟨 In Progress — Stage 1 PASS / Stage 2 current | `Stage 1/3 PASS` |
| `P6.04` | Product value, delivery-friction + governance evidence capture | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.05` | Platform-gap remediation from first real use | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.06` | Second materially distinct real product/workflow target + Product Contract | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.07` | Second real product/workflow platform integration | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.08` | Cross-product reuse and Platform Gravity evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.09` | Capability lifecycle / return-to-product / containment recommendations | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.10` | Product-driven architecture fitness + value evidence matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P6.11` | Product/platform hardening, ADR + refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.12` | Phase 6 / M6 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Engineering/product-validation gates:

- `R17 — First Product Boundary Review` — **Complete / PASS**, after P6.02 and before P6.03;
- `R18 — First Real-use Health Review` — after P6.05;
- `R19 — Cross-product Reuse Review` — after P6.08;
- `R20 — M6 Product-validation Hardening` — after P6.10.

These gates do not inflate Phase 6 completion percentage as separate equal-weight roadmap tasks.

## 7. M6 milestone definition

`M6 — Platform validated through real products and reuse evidence` requires, within the declared bounded scope:

1. at least two materially distinct real product/workflow contexts with owner-backed validation evidence;
2. explicit Product Contracts wherever real products rely on platform capabilities, shared platform history or canonical state;
3. reuse of shared Arvectum OS foundations without hidden coupling;
4. product-domain semantics remaining product-owned;
5. measurable evidence of at least one material shared reuse benefit;
6. explicit measurement/disposition of platform friction and overhead;
7. preserved Governed Execution, exact-version, authority, security and provenance semantics;
8. evidence-backed Platform Gravity and capability-lifecycle recommendations;
9. product-driven architecture fitness/value evidence passing;
10. all R17–R20 material findings and crossed governance/ADR gates dispositioned;
11. P6.12 closure review passing.

M6 does not require an `Active` Platform Capability, Stable Product Contract, production deployment, public SDK/API, SLA or support commitment.

## 8. Current canonical action

> **P6.03 Stage 2 — execute exactly one real 44-ФЗ pre-bid case through the bounded P6.02 Product Contract.**

Stage 1 has passed under exact Product Contract `0.1.0` and exact CAP-001/CAP-004 Provisional `1.0.0` provider evidence. Stage 2 is the next bounded adoption step and must use one explicit real case, one Organization scope and attributable Actor context.

Stage 2 must:

- preserve external ЕИС/partner/supplier authority instead of substituting Native platform authority;
- preserve procurement-domain semantics in `ai-corporation`;
- keep CAP-002/CAP-003 absent unless a concrete governed dependency requires a new immutable Product Contract version;
- retain exact Product Contract/provider/version evidence at each platform reliance point;
- keep wrong-Organization, rights/classification/purpose and incomplete-evidence paths fail closed;
- keep external actions and organizational commitments manual/product-owned;
- distinguish a failed platform path from an explicit return to the product-local/manual contour;
- record enough exact evidence for CAP-004 reconstruction of the platform-backed acts.

If the real case requires CAP-001 canonical admission/mutation rather than reliance on an already admitted exact reference, map it through existing Governed Execution/gate semantics or introduce only the minimum subordinate implementation change. Do not bypass the integration seam or invent a public/stable interface. If a durable persistence, Event delivery, IAM, service, public/stable compatibility or another materially constraining choice becomes necessary, reopen the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance.

Stage 3 remains blocked until Stage 2 evidence is reviewed. No bulk migration or automatic expansion is authorized.

## 9. ADR, lifecycle and Product Contract gates

Real-product pressure may cross architecture decisions that bounded reference phases intentionally left open. Re-open the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance on a concrete durable or externally constraining mechanism.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance. P6.02 satisfies that declaration prerequisite for its exact bounded scope, and R17/P6.03 Stage 1 have passed the bounded boundary/fitness gates.

No Platform Capability becomes `Active` without separate RFC-0001 lifecycle admission and applicable stable-contract, compatibility/migration, operational-readiness and decision-authority evidence.

Product Experiment success remains evidence, not automatic platform promotion.

P6.02/R17/P6.03 Stage 1 select no durable persistence, Event delivery, IAM/PDP/PEP provider, stable serialization/API, public SDK/package, object-store, search/vector or service topology; therefore they create no new ADR. P6.03 must reopen the minimum sufficient gate if Stage 2 implementation crosses one.

## 10. Phase transition rule

Phase 7 remains `Draft` until Phase 6 closes and its boundary is revalidated against real-product evidence, actual customer/operational requirements and unresolved production-readiness risks.

A roadmap phase transition does not itself change capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity or commercial commitments.

## 11. Roadmap maintenance rule

Every roadmap update begins with repository synchronization rather than chat-memory reconstruction. After every meaningful canonical milestone, synchronize this roadmap and the active phase roadmap, record evidence, keep lifecycle/environment/conformance distinct, do not inflate Draft/Proposed/exploratory status, and preserve repository history rather than fabricating approvals.

## 12. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
Phase 3 / M3 ✓
Phase 4 / M4 ✓
Phase 5 / M5 ✓
        ↓
Phase 6 — Product-driven Platform Validation ACTIVE
        ↓
P6.01 Real product/workflow target + evidence baseline ✓
        ↓
P6.02 First real Product Contract + bounded adoption plan ✓
        ↓
R17 First Product Boundary Review ✓
        ↓
P6.03 First real product/workflow platform integration ← in progress
        ↓
Stage 1 synthetic/redacted proof ✓ PASS
        ↓
Stage 2 one real 44-ФЗ case ← current gate
        ↓
Stage 3 max three platform-backed calibration cases
        ↓
Two real product/workflow validations + reuse/value evidence
        ↓
M6
```
