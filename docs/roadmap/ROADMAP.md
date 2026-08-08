# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.8.7`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.8.7` records completion of **P3.09 — Shared-capability reuse and composition proof** and engineering gate **R7 PASS**.

P3.09 adds a second RFC-0004 `Provisional` Product Contract and proves that two materially distinct bounded Product Experiments can reuse CAP-001 through CAP-004 through separate Product Contract and exact Workflow Version identities while preserving the same existing Provisional capability contract baseline.

The first proof composition is document-led and the second is discovery-led. Both reuse the same shared capability semantics without changing the platform contract for the second consumer. CAP-003 is additionally exercised over a governed Document source in the second consumer while remaining derived, source-type-neutral and non-authoritative; the Product Contract separately declares the exact canonical source read required for reliance.

The proof rejects Product Contract borrowing, missing or duplicated shared operations, identical composition as insufficient reuse evidence, consumer-specific canonical-read leakage and capability-contract version broadening. Composition remains consumer-owned: no generic platform composition framework, stable public/cross-product API or SDK, product-domain platform semantics, durable implementation decision or capability lifecycle promotion is introduced.

`Reference Python CI #92` passed the complete validation suite with Python `3.12.13`: `366` tests, result `OK`.

P3.10 is now the current canonical action.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- Phase 3 — `Active` planning/workstream state;
- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Active`;
- [`Platform Capability Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) — four entries lifecycle `Incubating`;
- [`Phase 3 Provisional Capability Contracts`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md) — `Active 1.0.0`;
- [`R5 Capability Boundary Review`](../reviews/R5-capability-boundary-review.md) — `PASS`;
- P3.03 through P3.06 capability-slice reviews — `PASS`;
- [`P3.07 review`](../reviews/P3-07-cross-capability-security-rights-organization-scope-enforcement-review.md) / R6 — `PASS`;
- [`P3.08 Product Contract`](../contracts/P3-08-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`;
- [`P3.08 review`](../reviews/P3-08-product-contract-consumption-boundary-bounded-consumer-proof-review.md) — `PASS`;
- [`P3.09 Product Contract`](../contracts/P3-09-DISTINCT-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`;
- [`P3.09 review`](../reviews/P3-09-shared-capability-reuse-composition-proof-review.md) / R7 — `PASS`;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner;
- no Platform Capability is `Active`.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Active | 🟨 In progress | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Near-term | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, operational environment and conformance maturity remain distinct.

## 5. Active Phase 3 — Shared Platform Capabilities

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional; P3.03 complete;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional; P3.04 complete;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional, non-authoritative; P3.05 complete;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional, derived/read-oriented; P3.06 complete.

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
| `P3.10` | Phase 3 architecture fitness matrix | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### M3 target

A small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims. M3 does not itself imply lifecycle `Active` promotion.

## 6. Current canonical action

> **P3.10 — Phase 3 architecture fitness matrix.**

P3.03 through P3.09 are complete and R5–R7 pass. Consolidate the accumulated evidence without promoting any capability, stabilizing public/cross-product interfaces, importing product-domain semantics or selecting durable cross-cutting mechanisms without re-opening the ADR gate.

## 7. ADR and Product Contract gate

Re-open the ADR gate before material reliance on concrete persistence/database/object-store/search/vector topology, transactions/concurrency, Event transport/store, IAM/policy enforcement, evidence-integrity technology, stable API/serialization contracts, durable projection/replay storage or deployable service/process topology.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance. P3.02 capability contracts are not substitutes for Product Contracts and do not grant permission or authority.

## 8. Phase transition rule

Before Phase 4 becomes Active, complete P3.12/M3 closure, revalidate Phase 4 against actual M3 evidence and product/operator needs, create a detailed P4 work breakdown, identify required governance artifacts and synchronize this roadmap.

## 9. Roadmap maintenance rule

Every roadmap update begins with repository synchronization rather than chat-memory reconstruction. After every meaningful canonical milestone, synchronize the roadmap, record evidence, keep lifecycle/environment/conformance distinct, do not inflate Draft/Proposed/exploratory status, and preserve repository history rather than fabricating approvals.

## 10. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
        ↓
Phase 3 — Shared Platform Capabilities ACTIVE
        ↓
P3.01 Candidate admission ✓
P3.02 Incubating lifecycle + Provisional contracts ✓
R5 Capability Boundary Review ✓ PASS
P3.03 Document & Artifact Governance ✓
P3.04 Memory & Knowledge Governance ✓
P3.05 Non-authoritative Search / Index Projection ✓
P3.06 Audit / Reconstruction Support ✓
P3.07 Cross-capability security/rights/Organization enforcement ✓ R6 PASS
P3.08 Product Contract consumption boundary ✓
P3.09 shared-capability reuse/composition proof ✓ R7 PASS
        ↓
P3.10 Phase 3 architecture fitness matrix ← current
        ↓
P3.11–P3.12 hardening / M3 closure
```
