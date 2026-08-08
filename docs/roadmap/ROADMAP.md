# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.9.0`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.9.0` records completion of **P3.12 — Phase 3 / M3 closure review** and achievement of **`M3 — Validated shared capability baseline`** for the declared bounded shared-capability reference scope.

P3.12 closes Phase 3 on the accumulated P3.01–P3.11 and R5–R8 evidence. The validated retained set is exactly CAP-001 through CAP-004. All four remain lifecycle `Incubating` with `Provisional` capability contracts; M3 closure is not an RFC-0001 `Active` admission decision.

The closure preserves the P3.11 disposition: no new Platform Capability is admitted, no Stable Product Contract/public API is created, no durable infrastructure mechanism crosses the current ADR threshold, and no material shared refactor is justified. The P3.08 and P3.09 Product Contracts remain `Provisional 0.1.0` validation evidence.

`Reference Python CI #105` validated the final hardened P3.11 head on Python `3.12.13` with `390` tests, result `OK`. P3.12 itself is a closure/governance change over that already hardened code head and does not expand runtime behavior.

Phase 4 is not automatically activated by M3 closure. **Phase 4 boundary revalidation and decomposition — Workspace / Operator Experience** is now the current canonical action.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Complete`;
- [`P3.12 closure review`](../reviews/P3-12-phase-3-m3-closure-review.md) — `PASS`;
- [`Platform Capability Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) — four retained entries lifecycle `Incubating`;
- [`Phase 3 Provisional Capability Contracts`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md) — `Active 1.0.0` subordinate incubation baseline;
- [`R5 Capability Boundary Review`](../reviews/R5-capability-boundary-review.md) — `PASS`;
- P3.03 through P3.06 capability-slice reviews — `PASS`;
- [`P3.07 review`](../reviews/P3-07-cross-capability-security-rights-organization-scope-enforcement-review.md) / R6 — `PASS`;
- [`P3.08 Product Contract`](../contracts/P3-08-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`;
- [`P3.08 review`](../reviews/P3-08-product-contract-consumption-boundary-bounded-consumer-proof-review.md) — `PASS`;
- [`P3.09 Product Contract`](../contracts/P3-09-DISTINCT-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`;
- [`P3.09 review`](../reviews/P3-09-shared-capability-reuse-composition-proof-review.md) / R7 — `PASS`;
- [`P3.10 architecture fitness matrix`](../reviews/P3-10-phase-3-architecture-fitness-matrix.md) — `PASS`;
- [`R8 milestone hardening review`](../reviews/R8-phase-3-milestone-hardening.md) — `PASS` after recorded CAP-004 fail-closed remediation;
- [`P3.11 capability admission / ADR / refactoring hardening review`](../reviews/P3-11-capability-admission-adr-refactoring-hardening-review.md) — `PASS`;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner;
- no Platform Capability is `Active`.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Near-term | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, operational environment and conformance maturity remain distinct.

## 5. Completed Phase 3 — Shared Platform Capabilities

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional; retained by P3.11/M3;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional; retained by P3.11/M3;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional, non-authoritative governed discovery/projection semantics; retained by P3.11/M3;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional, derived/read-oriented; retained by P3.11/M3.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟩 Complete | `██████████ 100%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | 🟩 Complete | `██████████ 100%` |
| `R5` | Capability Boundary Review | 🟩 PASS | `██████████ 100%` |
| `P3.03` | Document & Artifact Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.04` | Memory & Knowledge Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.05` | Non-authoritative Search / Index Projection candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.06` | Audit / Reconstruction Support candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | 🟩 Complete / R6 PASS | `██████████ 100%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | 🟩 Complete | `██████████ 100%` |
| `P3.09` | Shared-capability reuse and composition proof | 🟩 Complete / R7 PASS | `██████████ 100%` |
| `P3.10` | Phase 3 architecture fitness matrix | 🟩 Complete / PASS | `██████████ 100%` |
| `R8` | Phase 3 milestone hardening / code-health gate | 🟩 Complete / PASS | `██████████ 100%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | 🟩 Complete / PASS | `██████████ 100%` |
| `P3.12` | Phase 3 / M3 closure review | 🟩 Complete / PASS | `██████████ 100%` |

### M3 closure

`P3.12` records **`PASS — M3 achieved for the declared bounded shared-capability reference scope.`**

The milestone demonstrates governed shared-capability reuse above Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/security/portability semantics, derived-state non-authority, bounded Product Contract consumption and materially distinct reuse.

M3 does not itself imply lifecycle `Active` promotion, operational readiness, Stable Product Contracts, public API compatibility, production deployment or customer-facing support/SLA commitments.

## 6. Current canonical action

> **Phase 4 boundary revalidation and decomposition — Workspace / Operator Experience.**

Before Phase 4 becomes `Active`, revalidate its draft scope against actual M3 evidence and current product/operator needs. Then create a bounded detailed Phase 4 work breakdown and exit criteria, identify required governance/architecture dependencies, and synchronize this roadmap.

Do not treat Phase 4's current Draft roadmap row as a delivery promise or as already activated work.

## 7. Phase 3 closure disposition carried forward

P3.12 preserves these independent states:

1. **Roadmap phase:** Phase 3 `Complete`; M3 `Achieved`.
2. **Capability lifecycle:** CAP-001 through CAP-004 remain `Incubating / Provisional`; no `Active` promotion.
3. **Product Contracts:** P3.08 and P3.09 remain `Provisional 0.1.0` validation evidence; neither is `Stable`.
4. **ADR gate:** no current durable/cross-cutting implementation mechanism has crossed the threshold; future material reliance re-opens the gate.
5. **Operational environment/readiness:** no production or operational-readiness claim is created.
6. **Conformance/commercial state:** no full-platform conformance, SLA/support/HA or public compatibility commitment is created.

CAP-003 remains a governed discovery/projection responsibility, not a commitment to operate a particular commodity search/vector technology. Consumer composition remains product-owned; no generic orchestration capability is admitted.

## 8. ADR and Product Contract gate

Re-open the ADR gate before material reliance on concrete persistence/database/object-store/search/vector topology, transactions/concurrency, Event transport/store, IAM/policy enforcement, evidence-integrity technology, stable API/serialization contracts, durable projection/replay/reconstruction storage or deployable service/process topology.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance. P3.02 capability contracts are not substitutes for Product Contracts and do not grant permission or authority.

## 9. Phase transition rule

Phase 4 remains `Draft` until its boundary is revalidated and decomposed against M3 evidence and actual product/operator demand.

A later decision to activate Phase 4 must preserve the current architecture hierarchy, identify the bounded work breakdown and exit criteria, and synchronize this roadmap. Activation of a roadmap phase does not itself change any Platform Capability lifecycle.

## 10. Roadmap maintenance rule

Every roadmap update begins with repository synchronization rather than chat-memory reconstruction. After every meaningful canonical milestone, synchronize the roadmap, record evidence, keep lifecycle/environment/conformance distinct, do not inflate Draft/Proposed/exploratory status, and preserve repository history rather than fabricating approvals.

## 11. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
Phase 3 / M3 ✓  COMPLETE / ACHIEVED
        ↓
CAP-001..CAP-004 remain Incubating / Provisional
        ↓
Phase 4 — Workspace / Operator Experience remains DRAFT
        ↓
Boundary revalidation + decomposition ← current canonical action
```
