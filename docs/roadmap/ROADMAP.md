# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.8.4`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.8.4` records completion of **P3.06 — Audit / Reconstruction Support candidate slice**.

P3.06 adds bounded executable CAP-004 evidence for derived read-oriented reconstruction over exact governed Workflow/input/Product Contract/gate/execution/result/Event references, explicit `Available`/`Redacted`/`Deleted`/`Unavailable`/`Missing` evidence state, Organization fail-closed behavior, non-leaking restricted evidence and portable reference/status export without replay, mutation, approval or authority creation. CAP-004 remains `Incubating` with a Provisional contract; no durable observability/SIEM/evidence technology, stable view/public interface, production readiness or `Active` promotion is created.

All four initial bounded Incubating capability slices P3.03–P3.06 are now complete. P3.07 is the current canonical action and P3.10 fitness evidence continues to accumulate.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- Phase 3 — `Active` planning/workstream state;
- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Active 1.1.4`;
- [`Platform Capability Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) — `Active 1.1.0`, four entries lifecycle `Incubating`;
- [`Phase 3 Provisional Capability Contracts`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md) — `Active 1.0.0`;
- [`R5 Capability Boundary Review`](../reviews/R5-capability-boundary-review.md) — `PASS`;
- [`P3.03 review`](../reviews/P3-03-document-artifact-governance-candidate-slice-review.md) — `PASS`;
- [`P3.04 review`](../reviews/P3-04-memory-knowledge-governance-candidate-slice-review.md) — `PASS`;
- [`P3.05 review`](../reviews/P3-05-non-authoritative-search-index-projection-candidate-slice-review.md) — `PASS`;
- [`P3.06 review`](../reviews/P3-06-audit-reconstruction-support-candidate-slice-review.md) — `PASS`;
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
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.09` | Shared-capability reuse and composition proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.10` | Phase 3 architecture fitness matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### M3 target

A small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims. M3 does not itself imply lifecycle `Active` promotion.

## 6. Current canonical action

> **P3.07 — cross-capability security, rights and Organization-scope enforcement; P3.10 evidence continuous.**

P3.03 through P3.06 are complete. Continue bounded cross-capability enforcement without expanding capability identity, stabilizing public/cross-product interfaces, importing product-domain semantics or selecting durable cross-cutting mechanisms without re-opening the ADR gate.

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
        ↓
P3.07 Cross-capability security/rights/Organization enforcement ← current
        ↓
P3.08–P3.09 consumer / reuse proof
        ↓
P3.10–P3.12 fitness / hardening / M3 closure
```
