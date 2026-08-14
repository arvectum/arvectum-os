# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.51.4`
Created: `2026-08-07`
Updated: `2026-08-14`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.51.3` records `P6.05-L2` as `Complete / PASS` after the selected owner-operated Mac mini reproduced canonical `main` at `fb61889633b11875dc5e1cf92771a159024a5695`, passed `717/717` reference tests under CPython `3.14.6`, and preserved a clean source checkout with no product, EIS, public-ingress or external action. Canonical evidence is [`P6-05-L2-local-reference-runtime-start.md`](../reviews/P6-05-L2-local-reference-runtime-start.md).

The detailed P6.05 local substream is synchronized to `0.1.4`; `P6.05-L3` is `Complete / PASS` ([evidence](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md)), and `P6.05-L4` is `Complete / PASS` ([evidence](../reviews/P6-05-L4-internal-organization-operator-bootstrap.md)), and `P6.05-L5 — First real product connection through exact P6.02 boundary` is now the current action. The truthful real `7/7` exact-attachment evidence gate remains unobserved, so P6.05 itself remains open.

P6.05 implementation readiness remains separated from the owner-operated runtime work required to execute the real evidence path. The local deployment is treated as a bounded **Internal / local owner-operated runtime** for ООО «Арвектум», not as a Production environment, supported macOS product, Stable/public runtime contract or final deployment topology.

The detailed substream is [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md). It decomposes the remaining work into secure configuration, Organization/operator bootstrap, first real product connection, local smoke, real `7/7` live run, governed admission/closure and dogfooding-friction capture, with L1 and L2 now complete.

Already observed implementation and local-runtime evidence:

- bounded Arvectum OS P6.05 CAP-001 admission implementation merged as `5dbbc7b3af1f0f3896301ef833de2214cb44e6f9`;
- `ai-corporation` PR `#142` merged as `bf9a1c5438426031fce36370344ada969d2493dd`;
- hosted standard product CI and dedicated P6.05 exact-attachment CI passed on the unchanged implementation head;
- P6.05-L1 local host/runtime baseline passed;
- P6.05-L2 reproducible local reference runtime passed on canonical `main` with `717/717` tests and a clean source checkout;
- the real live runner exists but has not yet produced real `7/7` evidence in the authorized owner-operated environment.

The P6.05 P0 problem statement remains unchanged: enable sufficient exact external tender attachment evidence for a truthful client-ready completeness decision while preserving external authority, exact version/provenance, Organization/rights controls, procurement-domain ownership and the no-external-action boundary.

The local-runtime refinement does not select CAP-002/CAP-003, storage/service topology, Stable/public API/SDK, production architecture or capability lifecycle promotion. Any materially constraining dependency discovered during setup must stop at the minimum sufficient ADR/RFC/Product Contract/policy gate before becoming an architectural commitment.

The P6.02 Stage 3 allowance remains a **maximum**, not a quota. `0` additional calibration cases remain consumed. Reopen bounded calibration only after P6.05 creates a materially changed evidence contour and a specific new hypothesis worth testing.

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
- [`P6.04 value/friction/governance evidence`](../reviews/P6-04-product-value-delivery-friction-governance-evidence-capture.md) — `PASS`;
- [`P6.05-L1 local host/runtime baseline`](../reviews/P6-05-L1-local-host-runtime-baseline.md) — `PASS`;
- [`P6.05-L2 local reference runtime start`](../reviews/P6-05-L2-local-reference-runtime-start.md) — `PASS`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 Product Contracts remain `Provisional 0.1.0` reference evidence;
- P6.02 procurement Product Contract remains `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3–M5, P6.01–P6.04, or completed P6.05 local subtasks have passed;
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

- [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md) — `Active 1.7.1`.
- [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md) — `Active 0.1.2`, subordinate execution plan for the current P6.05 owner-operated runtime/evidence path.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P6.01` | Real product/workflow validation target selection + evidence baseline | 🟩 Complete | `██████████ 100%` |
| `P6.02` | First real Product Contract boundary + bounded adoption plan | 🟩 Complete | `██████████ 100%` |
| `P6.03` | First real product/workflow platform integration | 🟩 Complete / PASS | `██████████ 100%` |
| `P6.04` | Product value, delivery-friction + governance evidence capture | 🟩 Complete / PASS | `██████████ 100%` |
| `P6.05` | Platform-gap remediation from first real use | 🟨 Current — L1/L2 PASS; secure configuration next; real evidence pending | `tracked by P6.05 subtasks` |
| `P6.06` | Second materially distinct real product/workflow target + Product Contract | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.07` | Second real product/workflow platform integration | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.08` | Cross-product reuse and Platform Gravity evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.09` | Capability lifecycle / return-to-product / containment recommendations | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.10` | Product-driven architecture fitness + value evidence matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P6.11` | Product/platform hardening, ADR + refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.12` | Phase 6 / M6 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### P6.05 execution breakdown

| ID | Subtask | Status |
|---|---|---|
| `P6.05-I1` | Bounded platform exact-document admission remediation | 🟩 Complete — merged `5dbbc7b3...` |
| `P6.05-I2` | Product exact-attachment evidence capture + governed bridge | 🟩 Complete — product PR `#142` merged `bf9a1c543...` |
| `P6.05-L1` | Local host/runtime baseline | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L1-local-host-runtime-baseline.md) |
| `P6.05-L2` | Reproducible Arvectum OS local checkout + reference runtime start | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L2-local-reference-runtime-start.md) |
| `P6.05-L3` | Secure local configuration + secrets boundary | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md) |
| `P6.05-L4` | Internal Organization + operator bootstrap | 🟩 Complete / PASS — [evidence](../reviews/P6-05-L4-internal-organization-operator-bootstrap.md) |
| `P6.05-L5` | First real product connection through exact P6.02 boundary | 🟨 Current / next |
| `P6.05-L6` | Local synthetic/redacted regression + negative-path smoke | ⬜ Pending |
| `P6.05-L7` | Real P6.05 exact-attachment live run (`7/7` gate) | ⬜ Pending |
| `P6.05-L8` | Governed evidence admission + canonical P6.05 closure package | ⬜ Pending |
| `P6.05-L9` | Dogfooding friction capture | ⬜ Pending / cross-cutting |

Detailed exit evidence and non-goals are defined in [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md).

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

> **P6.05-L5 — First real product connection through exact P6.02 boundary.**

`P6.05-L1`, `P6.05-L2`, and `P6.05-L3` are complete / PASS. The local runtime evidence is recorded in [`P6-05-L1-local-host-runtime-baseline.md`](../reviews/P6-05-L1-local-host-runtime-baseline.md), [`P6-05-L2-local-reference-runtime-start.md`](../reviews/P6-05-L2-local-reference-runtime-start.md), and [`P6-05-L3-secure-local-configuration-secrets-boundary.md`](../reviews/P6-05-L3-secure-local-configuration-secrets-boundary.md). L3 proved the secure local configuration/secrets boundary is established, seven legacy token assignments were scrubbed under explicit owner decision, and the external owner-only secret boundary was established without exposing credential values.

L4 must now establish the internal Organization/operator bootstrap for ООО «Арвектум». Credentials remain outside source control and canonical evidence. The EIS proxy/TLS constraint observed in L1 remains a recorded prerequisite for later L7 work and must be handled fail-closed rather than bypassed implicitly.

The P6.05 code remediation is implementation-ready, but P6.05 remains open until truthful real evidence exists. Continue through the dependency-aware local substream in [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md).

The local runtime exists to make the already-selected P6.05 evidence path executable and to begin real internal use of Arvectum OS. It must preserve:

- exact external authority rather than false `Native` substitution;
- exact Product Contract/version and CAP-001/CAP-004 provider evidence;
- truthful incomplete reconstruction/evidence handling;
- explicit Organization/rights/security boundary;
- product ownership of procurement semantics and completeness judgment;
- no automatic external mutation or organizational commitment.

Do not turn this local setup into a hidden Production architecture decision. The Mac mini is the current operational environment, not the platform contract. Capture setup/operator friction as evidence and stop at the applicable governance gate before introducing any durable cross-cutting dependency.

Manual-time, recall, usefulness, cost and portability KPI values remain unknown; P6.05 must not invent them. The remaining Stage 3 calibration capacity stays preserved and should be reopened only for a materially new hypothesis after remediation.

## 9. ADR, lifecycle and Product Contract gates

Real-product pressure may cross architecture decisions that bounded reference phases intentionally left open. Re-open the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance on a concrete durable or externally constraining mechanism.

P6.02 satisfies the RFC-0004 declaration prerequisite for its exact real-product scope. R17 and P6.03 confirm that the current read-oriented boundary can be exercised without hidden coupling while preserving external authority and product ownership. P6.04 confirms that this boundary creates directly evidenced governance/control value but is insufficient for the intended client-ready source-package completeness outcome.

No Platform Capability becomes `Active` without separate RFC-0001 lifecycle admission and applicable stable-contract, compatibility/migration, operational-readiness and decision-authority evidence.

Product Experiment success remains evidence, not automatic platform promotion.

P6.03/P6.04 selected no durable persistence, Event delivery, IAM/PDP/PEP provider, stable serialization/API, public SDK/package, object-store, search/vector or service topology. The P6.05 local-runtime substream likewise does not select any of those as platform commitments. If local execution reveals a materially constraining dependency, reopen the minimum sufficient governance gate first.

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
P6.04 Product value / friction / governance evidence ✓ PASS
        ↓
P6.05 implementation remediation ✓ merged
        ↓
P6.05-L1 Local host/runtime baseline ✓ PASS
        ↓
P6.05-L2 local checkout + reference runtime start ✓ PASS
        ↓
P6.05-L3 secure local configuration + secrets boundary ✓ PASS
        ↓
P6.05-L4 internal Organization + operator bootstrap ✓ PASS
        ↓
P6.05-L5 first real product connection ← current
        ↓
P6.05-L7 real exact attachment evidence: 7/7 required
        ↓
P6.05-L8 governed admission + P6.05 closure
        ↓
R18 First Real-use Health Review
        ↓
Second real product/workflow validation + reuse evidence
        ↓
M6
```