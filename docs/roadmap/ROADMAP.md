# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.49.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.49.0` records **P6.03 — First real product/workflow platform integration** as `Complete / PASS` and advances the current canonical action to **P6.04 — Product value, delivery-friction + governance evidence capture**.

P6.03 now contains both synthetic/redacted boundary proof and real-use evidence. Stage 1 validated the exact P6.02 Product Contract boundary, fail-closed Organization/rights/version/evidence behavior, truthful incomplete reconstruction, no hidden coupling and RFC-0002 `External Reference` semantics. Stage 2 then executed exactly one real public 44-ФЗ case, notice `0344100006426000005`, through the same CAP-001/CAP-004 integration contour.

The real product did not fabricate a client-ready positive recommendation. Its evidence-bounded disposition is `NOT_CLIENT_READY_EVIDENCE_INCOMPLETE`: the normalized public procurement facts and exact external references are retained and governed, but the exact bytes/digests of the complete listed tender attachment set are not. That gap prevents truthful completion of the intended client-ready decision-package path and is now explicit P6.04/P6.05 input evidence.

Product `ai-corporation` CI `#1934` passed all jobs, including the dedicated Stage 2 real-case proof (`2 passed`), the Stage 1 regression, full `make test`, `make check`, security, migrations, PostgreSQL/R8 acceptance and Redis integration. Product PR `#141` was squash-merged to `main` as `2c21a33eec02959aba7d13909f0d0c835294becf`.

The P6.02 Stage 3 allowance remains a **maximum**, not a quota. `0` additional calibration cases are consumed now because Stage 2 already produced the material new finding: the current read-oriented contour works for a real external reference but cannot complete the intended client-ready workflow without full governed external-attachment retrieval/admission. Repeating unchanged cases would duplicate known evidence. Remaining calibration capacity is preserved for a materially new hypothesis after P6.04/P6.05 or another bounded decision.

The first real Product Contract remains [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`, with exactly CAP-001 + CAP-004 at Provisional capability contract `1.0.0`; CAP-002/CAP-003 remain omitted, external authority remains external, procurement semantics remain product-owned, and automated external mutation/organizational commitment remains outside scope.

No Platform Capability is promoted, no Stable/public integration compatibility boundary is created, and no production/SLA/support commitment follows from P6.03 completion.

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
- [`P6.03 Stage 1 integration review`](../reviews/P6-03-stage-1-first-real-product-workflow-platform-integration.md) — `PASS`;
- [`P6.03 first real integration closure`](../reviews/P6-03-stage-2-one-real-44fz-case-review.md) — `PASS`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 Product Contracts remain `Provisional 0.1.0` reference evidence;
- P6.02 procurement Product Contract remains `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3–M5 or P6.01–P6.03 are complete;
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

- [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md) — `Active 1.5.0`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P6.01` | Real product/workflow validation target selection + evidence baseline | 🟩 Complete | `██████████ 100%` |
| `P6.02` | First real Product Contract boundary + bounded adoption plan | 🟩 Complete | `██████████ 100%` |
| `P6.03` | First real product/workflow platform integration | 🟩 Complete / PASS | `██████████ 100%` |
| `P6.04` | Product value, delivery-friction + governance evidence capture | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P6.05` | Platform-gap remediation from first real use | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.06` | Second materially distinct real product/workflow target + Product Contract | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.07` | Second real product/workflow platform integration | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.08` | Cross-product reuse and Platform Gravity evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.09` | Capability lifecycle / return-to-product / containment recommendations | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.10` | Product-driven architecture fitness + value evidence matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P6.11` | Product/platform hardening, ADR + refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.12` | Phase 6 / M6 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Engineering/product-validation gates:

- `R17 — First Product Boundary Review` — **Complete / PASS**;
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

> **P6.04 — Product value, delivery-friction + governance evidence capture.**

Use the actual P6.03 Stage 1 + Stage 2 evidence rather than assuming the first real integration was uniformly positive.

P6.04 must capture and, where feasible, quantify:

- value from exact external authority, Product Contract/version continuity and reconstructability;
- implementation/integration effort introduced by the governed boundary;
- operator clarity from fail-closed and evidence-completeness behavior;
- the concrete friction that the current contour does not provide the exact complete external tender attachment package needed to finish the intended client-ready path;
- any time/cost/quality/security/governance overhead or benefit that can actually be evidenced;
- evidence gaps that cannot yet be measured without inventing customer KPI values.

Do not pre-decide the P6.05 remediation. P6.05 must resolve only gaps demonstrated and prioritized by P6.04 evidence.

The remaining Stage 3 calibration capacity is preserved rather than consumed as ceremony. Reopen it only for a materially new hypothesis after evidence-backed remediation or another bounded decision.

## 9. ADR, lifecycle and Product Contract gates

Real-product pressure may cross architecture decisions that bounded reference phases intentionally left open. Re-open the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance on a concrete durable or externally constraining mechanism.

P6.02 satisfies the RFC-0004 declaration prerequisite for its exact real-product scope. R17 and P6.03 confirm that the current read-oriented boundary can be exercised without hidden coupling while preserving external authority and product ownership.

No Platform Capability becomes `Active` without separate RFC-0001 lifecycle admission and applicable stable-contract, compatibility/migration, operational-readiness and decision-authority evidence.

Product Experiment success remains evidence, not automatic platform promotion.

P6.03 selected no durable persistence, Event delivery, IAM/PDP/PEP provider, stable serialization/API, public SDK/package, object-store, search/vector or service topology. The demonstrated attachment-contour friction must be measured in P6.04 before P6.05 selects a remedy. If a later remedy crosses a materially constraining boundary, reopen the minimum sufficient governance gate first.

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
P6.03 First real product/workflow platform integration ✓ PASS
        ↓
Stage 1 synthetic/redacted proof ✓
        ↓
Stage 2 one real 44-ФЗ case ✓
        ↓
Stage 3 calibration cap: 0 additional cases consumed
        ↓
P6.04 Product value / friction / governance evidence ← current
        ↓
P6.05 evidence-backed remediation
        ↓
Second real product/workflow validation + reuse evidence
        ↓
M6
```
