# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.8.1`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.8.1` records completion of **P3.03 — Document & Artifact Governance candidate slice**.

P3.03 adds the first bounded executable CAP-001 slice above the Core Runtime and scoped fitness evidence for logical Document identity, immutable versions, explicit Artifact/content identity, governed admission, derivation provenance, handling propagation, exact-version reliance and storage/hash non-authority. CAP-001 remains `Incubating` with a Provisional contract; no durable ADR boundary, production readiness, stable public interface or `Active` promotion is created.

P3.04–P3.06 remain available in bounded parallel and P3.10 fitness evidence continues to accumulate.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- Phase 3 — `Active` planning/workstream state;
- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Active 1.1.1`;
- [`Platform Capability Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) — `Active 1.1.0`, four entries lifecycle `Incubating`;
- [`Phase 3 Provisional Capability Contracts`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md) — `Active 1.0.0`;
- [`P3.01 review`](../reviews/P3-01-capability-boundary-revalidation-review.md) — `PASS`;
- [`P3.02 review`](../reviews/P3-02-capability-lifecycle-ownership-provisional-contract-review.md) — `PASS`;
- [`R5 Capability Boundary Review`](../reviews/R5-capability-boundary-review.md) — `PASS`;
- [`P3.03 review`](../reviews/P3-03-document-artifact-governance-candidate-slice-review.md) — `PASS`;
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

## 5. Completed Phase 2 / M2

Phase 2 is closed at 100%. M2 proves the bounded reusable Core Runtime semantics but does not establish production readiness, full RFC conformance, stable public compatibility, a supported SDK/API, durable infrastructure, SLA/support obligations or an `Active` Platform Capability.

## 6. Active Phase 3 — Shared Platform Capabilities

Current bounded capability set:

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional; P3.03 bounded slice complete;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional, non-authoritative;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional, derived/read-oriented.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟩 Complete | `██████████ 100%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | 🟩 Complete | `██████████ 100%` |
| `R5` | Capability Boundary Review | 🟩 PASS | `██████████ 100%` |
| `P3.03` | Document & Artifact Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.04` | Memory & Knowledge Governance candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.05` | Non-authoritative Search / Index Projection candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.06` | Audit / Reconstruction Support candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.09` | Shared-capability reuse and composition proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.10` | Phase 3 architecture fitness matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### M3 target

A small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims.

M3 does not itself require or imply lifecycle `Active` capability promotion.

## 7. Current canonical action

> **P3.04–P3.06 — remaining bounded capability slices; P3.10 evidence continuous.**

P3.03 is complete. Continue the remaining Incubating capability slices without expanding capability identity, stabilizing public/cross-product interfaces, importing product-domain semantics or selecting durable cross-cutting mechanisms without re-opening the ADR gate.

## 8. ADR and Product Contract gate

P2.11's bounded no-ADR disposition remains in force only while no material durable/external dependency has crossed the threshold.

Re-open the ADR gate before material reliance on concrete persistence/database/object-store/search topology, transactions/concurrency, Event transport/store, IAM/policy enforcement, evidence-integrity technology, stable API/serialization contracts, durable projection/replay storage or deployable service/process topology.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance. P3.02 capability contracts are not substitutes for Product Contracts and do not grant permission or authority.

## 9. Phase transition rule

Before Phase 4 becomes Active, complete P3.12/M3 closure, revalidate Phase 4 against actual M3 evidence and product/operator needs, create a detailed P4 work breakdown, identify required governance artifacts and synchronize this roadmap.

## 10. Roadmap maintenance rule

Every roadmap update begins with repository synchronization rather than chat-memory reconstruction. After every meaningful canonical milestone, synchronize the roadmap, record evidence, keep lifecycle/environment/conformance distinct, do not inflate Draft/Proposed/exploratory status, and preserve repository history rather than fabricating approvals.

## 11. Current state summary

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
        ↓
P3.02 Incubating lifecycle + Provisional capability contracts ✓
        ↓
R5 Capability Boundary Review ✓ PASS
        ↓
P3.03 Document & Artifact Governance ✓
        ↓
P3.04–P3.06 remaining bounded slices ← current
        ↓
P3.07–P3.09 composition / consumer / reuse proof
        ↓
P3.10–P3.12 fitness / hardening / M3 closure
```
