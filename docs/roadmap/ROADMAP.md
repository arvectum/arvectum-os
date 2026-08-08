# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.8.9`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.8.9` records completion of **R8 — Phase 3 milestone hardening / code-health gate**.

R8 reviewed the accumulated P3.03–P3.10 implementation for dependency direction, semantic ownership, Product Contract isolation, correctness, security/Organization scope/authority behavior, maintainability, reversibility, public-surface pressure, test evidence, performance evidence and ADR-trigger pressure.

The hardening review found one material correctness/security defect in the bounded P3.07/CAP-004 reconstruction access handoff: an evidence Version Identity omitted from current `evidence_constraints` could inherit the lower reconstruction layer's intentional default `Available` disposition. R8 remediates that boundary by requiring exact complete typed constraint coverage for every governed reconstruction evidence Version Identity before disclosure. Missing, unknown, duplicate or malformed constraint sets now fail closed.

R8 also adds seven executable code-health guards preserving Phase 3 dependency direction, provisional package-root exposure, absence of process/network/unsafe-deserialization dependencies, absence of dynamic code execution or implicit authority/gate bypass helpers, and continued non-selection of public framework/stable serialization technology.

`Reference Python CI #100` passed the hardened implementation with Python `3.12.13`: `384` tests, result `OK`.

R8 does not promote CAP-001 through CAP-004 to `Active`, stabilize either bounded Product Contract, create a public API/SDK, select durable infrastructure, establish production readiness or create SLA/support/full-conformance claims. `P3.11 — Capability admission / ADR / refactoring hardening review` is now the current canonical action.

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
- [`P3.10 architecture fitness matrix`](../reviews/P3-10-phase-3-architecture-fitness-matrix.md) — `PASS`;
- [`R8 milestone hardening review`](../reviews/R8-phase-3-milestone-hardening.md) — `PASS`;
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
| `P3.10` | Phase 3 architecture fitness matrix | 🟩 Complete / PASS | `██████████ 100%` |
| `R8` | Phase 3 milestone hardening / code-health gate | 🟩 Complete / PASS | `██████████ 100%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### M3 target

A small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims. M3 does not itself imply lifecycle `Active` promotion.

## 6. Current canonical action

> **P3.11 — Capability admission / ADR / refactoring hardening review.**

R8 is complete and passes after one bounded fail-closed security remediation. Use the accumulated P3.01–R8 evidence to disposition each Incubating capability and re-check ADR/refactoring requirements. Do not infer `Active` lifecycle, Stable Product Contract/public API or production readiness from successful reference implementation alone.

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
P3.10 Phase 3 architecture fitness matrix ✓ PASS
R8 Phase 3 milestone hardening / code-health gate ✓ PASS
        ↓
P3.11 Capability admission / ADR / refactoring hardening review ← current
        ↓
P3.12 Phase 3 / M3 closure review
```
