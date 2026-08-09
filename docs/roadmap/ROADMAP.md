# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.46.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.46.0` records completion of **P6.02 — First real Product Contract boundary + bounded adoption plan** with `PASS` and advances the current canonical action to **R17 — First Product Boundary Review**.

The first real Product Contract is [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`, for the selected Arvectum procurement/tender AI operator bounded 44-ФЗ pre-bid workflow. It declares exactly CAP-001 + CAP-004 at Provisional capability contract `1.0.0`, deliberately omits CAP-002/CAP-003, preserves external authority for ЕИС/partner/supplier source documents, keeps procurement-domain semantics product-owned and admits no automated external mutation or organizational commitment. Completion evidence is [`P6.02`](../reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md).

The bounded adoption sequence is synthetic/redacted proof → one real case → maximum three-case calibration set, with explicit stop/rollback criteria and no bulk migration. R17 must pass before P6.03 creates real governed implementation reliance.

P6.01 remains complete under [`P6.01`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md). Empirical real-customer KPI values not yet observed remain evidence gaps rather than fabricated baselines.

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
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 Product Contracts remain `Provisional 0.1.0` reference evidence;
- P6.02 real procurement Product Contract is `Provisional 0.1.0` and does not stabilize the integration boundary;
- no Platform Capability is `Active` merely because M3–M5 or P6.01/P6.02 are complete;
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

- [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md) — `Active 1.2.0`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P6.01` | Real product/workflow validation target selection + evidence baseline | 🟩 Complete | `██████████ 100%` |
| `P6.02` | First real Product Contract boundary + bounded adoption plan | 🟩 Complete | `██████████ 100%` |
| `P6.03` | First real product/workflow platform integration | ⬜ | `░░░░░░░░░░ 0%` |
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

- `R17 — First Product Boundary Review` — **current**, after P6.02 and before P6.03;
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

> **R17 — First Product Boundary Review.**

Review the completed P6.02 `Provisional 0.1.0` Product Contract before P6.03 creates real implementation reliance.

R17 must verify that:

- the real target still matches P6.01 evidence;
- CAP-001 + CAP-004 at exact Provisional contract `1.0.0` are the smallest sufficient dependency set;
- CAP-002/CAP-003 remain omitted unless a concrete dependency is demonstrated;
- ЕИС/partner/supplier source authority remains external and no competing source of truth is created;
- procurement-domain schemas, knowledge, workflow, search/relevance, economics and decision semantics remain product-owned;
- Organization/security/rights/retention/evidence behavior fails closed;
- Product Contract validation creates no permission or Organizational Authority;
- adoption remains synthetic/redacted → one real case → maximum three-case calibration set with explicit rollback;
- no durable persistence/Event/IAM/service/public/stable compatibility choice has been smuggled into the boundary.

P6.03 remains blocked on this review gate, not on capability promotion or platform-wide production readiness.

## 9. ADR, lifecycle and Product Contract gates

Real-product pressure may cross architecture decisions that bounded reference phases intentionally left open. Re-open the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance on a concrete durable or externally constraining mechanism.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance. P6.02 now satisfies that declaration prerequisite for its exact bounded scope, subject to R17 before implementation reliance.

No Platform Capability becomes `Active` without separate RFC-0001 lifecycle admission and applicable stable-contract, compatibility/migration, operational-readiness and decision-authority evidence.

Product Experiment success remains evidence, not automatic platform promotion.

P6.02 selects no durable persistence, Event delivery, IAM/PDP/PEP provider, stable serialization/API, public SDK/package, object-store, search/vector or service topology; therefore it creates no new ADR. R17/P6.03 must reopen the minimum sufficient gate if implementation crosses one.

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
R17 First Product Boundary Review ← current
        ↓
P6.03 First real product/workflow platform integration
        ↓
Two real product/workflow validations + reuse/value evidence
        ↓
M6
```
