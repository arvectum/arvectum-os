# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.90.0`
Created: `2026-08-07`
Updated: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.90.0` preserves `P9.11 — Real daily-use dogfooding + friction/backlog closure` as the current **critical-path** action while closing `INT-B2 — Domain-neutral connector boundary pattern` and advancing the parallel integration lane to `INT-B3 — 1С first-candidate design`.

M9-alpha is already achieved and P9.07–P9.10 plus R31 are `Complete / PASS`. P9.11 now depends materially on real owner working sessions, so bounded work that does not falsify or bypass P9.11 evidence may proceed concurrently.

Canonical parallel-workstream plan: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md) `1.0.0`.

`INT-B1` is closed by [`INT-B1 — Integration Portfolio Baseline`](../architecture/INT-B1-integration-portfolio-baseline.md) `1.0.0` plus [`INT-B1 functional cross-review`](../reviews/INT-B1-functional-cross-review.md) — `PASS after bounded reconciliation`, 3 of maximum 7 iterations. The baseline ranks 1С first, Битрикс24 second, amoCRM third, then deployment-specific СЭД/ECM/АСУД, ЭДО/signature, regulated procurement and bounded watchlist classes. It preserves external authority, product-owned business semantics and the existing non-admission of a generic connector marketplace/broad adapter framework.

`INT-B2` is closed by [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](../architecture/INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0` plus [`INT-B2 functional cross-review`](../reviews/INT-B2-functional-cross-review.md) — `PASS after bounded reconciliation`, 3 of maximum 7 iterations. It standardizes only the domain-neutral connector governance envelope: connector/endpoint identity and versioning, external authority mode, explicit operation/effect contracts, indirect credential references, Organization/security/authority context, duplicate/idempotency/retry/replay rules, uncertainty/reconciliation, source-occurrence versus canonical-Event admission, provenance and disable/upgrade/rollback/termination semantics. It does not create a universal business-object model, generic connector runtime, public API/SDK or new Platform Capability.

The integration lane remains **design/evidence-first**. It may inventory and design governed integration boundaries for 1С, Битрикс24, amoCRM, СЭД/ECM/ЭДО and other concrete external systems while P9.11 dogfooding continues. A real connector implementation is admitted only after a concrete organizational outcome, external authority/data-rights scope, platform-responsibility disposition and required Product Contract/ADR/governance gates exist. This prevents speculative universal connectors and product-business-logic leakage into Arvectum OS.

This update does not create a new numbered phase, public/stable connector/API/SDK, customer Production, Stable Product Contract, Active Platform Capability, SLA/support/certification or broader conformance claim.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `ADR-0001 — Productive Workspace Browser Application Topology` — `Accepted 2026-08-21` for the exact internal Phase 9 application topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02, P6.06, P8.03 and P8.06 Product Contracts remain Provisional within their exact scopes;
- operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- no public/stable SDK/API/wire/browser/connector surface, external/customer Production, SLA/support/certification or broader conformance claim exists.

## 4. Strategic roadmap

| Phase | Strategic scope | Status | Milestone |
|---|---|---:|---|
| `Phase 0` | Foundation / Architecture Bootstrap | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | 🟩 Complete / PASS | `M6` Real-product validation across materially distinct workflows |
| `Phase 7` | Operational / Enterprise Readiness | 🟩 Complete / PASS | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | 🟩 Complete / PASS | `M8` Governed external ecosystem baseline — exact activated one-Organization scope |
| **`Phase 9`** | **Productive Workspace & Daily Operations** | **🟨 Active** | **`M9` Daily-use organizational workbench** |

## 5. Active Phase 9 — Productive Workspace & Daily Operations

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.13.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| `R29` | Productive Workspace Boundary Review | 🟩 Complete / PASS |
| `P9.03` | Real application shell + navigation + organization/user context | 🟩 Complete / PASS |
| `P9.04` | `My Work` / Needs Attention projection | 🟩 Complete / PASS |
| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS |
| `P9.06` | Executions / Decisions / governed actions UX | 🟩 Complete / PASS |
| `R30` | M9-alpha Usability / Information Architecture Review | 🟩 Complete / PASS |
| `M9-alpha` | Usable Internal Workspace | 🟩 Achieved / PASS |
| `P9.07` | Product-owned workspace surfaces / composition | 🟩 Complete / PASS |
| `P9.08` | Arvectum AI Copilot + source-grounded organizational assistance | 🟩 Complete / PASS |
| `P9.09` | Activity, notifications and attention routing | 🟩 Complete / PASS |
| `P9.10` | ООО «Арвектум» organization composition | 🟩 Complete / PASS |
| `R31` | Product Composition / AI Safety Review | 🟩 Complete / PASS |
| **`P9.11`** | **Real daily-use dogfooding + friction/backlog closure** | **🟨 Current — implementation ready / real sessions pending** |
| `R32` | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ gate |
| `P9.12` | Phase 9 / M9 closure review | ⬜ |

P9.11 remains the critical path to M9. The `p9.11.0` internal Workspace release contains the bounded real-session Observation/backlog mechanism; synthetic owner-session evidence is not accepted.

## 6. Parallel development lanes

Detailed concurrency rules and boundaries: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md).

| Lane | Scope | Status | May progress during P9.11? |
|---|---|---:|---:|
| **A — Productive Workspace dogfooding** | real UI use, friction capture/repair, P9.11 → R32 → P9.12 | 🟨 Critical path | yes — primary |
| **B — Russian-market integrations** | integration portfolio, connector boundary design, 1С/CRM/СЭД/ЭДО concrete designs | 🟨 Active design — INT-B1/INT-B2 complete, INT-B3 current | **yes** |
| **C — Product ↔ Workspace composition** | Tender/Discount/Creative/Proxy product-owned projections and governed entry points | 🟦 Available | yes, within Product Contract/product-local boundaries |
| **D — Reliability / DX / technical debt** | CI, dependencies, observability, recovery regressions, evidence-backed cleanup | 🟦 Continuous | yes |
| **E — Future external/customer readiness** | second-Organization/customer/deployment/regulatory discovery only | ⬜ Discovery | yes, no customer-Production implementation |

### 6.1 Lane A — current UI branch

Current action remains:

> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**

The owner uses the Productive Workspace for real work, records friction, and validates whether ordinary work can remain inside the Workspace rather than escaping to terminal/GitHub/internal identifiers. Material defects are fixed as they appear. R32 remains locked until real-session evidence and backlog disposition satisfy P9.11.

### 6.2 Lane B — integration design in parallel

Canonical integration sequence:

1. `INT-B1 — Integration portfolio baseline` — **Complete / PASS**; ranked candidate register in [`INT-B1-integration-portfolio-baseline.md`](../architecture/INT-B1-integration-portfolio-baseline.md);
2. `INT-B2 — Domain-neutral connector boundary pattern` — **Complete / PASS**; governance envelope in [`INT-B2-domain-neutral-connector-boundary-pattern.md`](../architecture/INT-B2-domain-neutral-connector-boundary-pattern.md), with no universal business schema/runtime/public API implied;
3. **`INT-B3 — 1С first-candidate design` — Current**; select one concrete 1С configuration/deployment and bounded organizational outcome, then define exact read/write/effect/identity/reconciliation/Product Contract boundary using INT-B2;
4. `INT-B4 — CRM designs` — Битрикс24 and amoCRM remain separate concrete integrations; shared abstraction only after reuse evidence;
5. `INT-B5 — СЭД/ECM/ЭДО design` — start from an actual deployment and preserve document/signature/retention authority;
6. `INT-B6 — Integration security/reliability review` — prerequisite before first material real connector implementation.

INT-B1 priority disposition:

- Priority A: 1С, Битрикс24, amoCRM;
- Priority B: concrete СЭД/ECM/АСУД deployment, concrete ЭДО/signature contour, bounded ЕИС/regulated procurement source;
- Priority C/watchlist: ITSM, directory/IAM technology integrations, banking/treasury and later logistics/MES/BI classes only when real product/customer pull exists.

INT-B2 boundary disposition:

- shared/domain-neutral: connector and endpoint identity/versioning, external authority declarations, explicit operation/effect classification, credential references, security/authority context, idempotency/duplicate/retry/replay rules, uncertainty/reconciliation, Event admission/provenance and connector termination semantics;
- system/product/customer-owned: 1С configuration schemas and posting rules, CRM pipelines and mappings, СЭД taxonomies/routing, ЭДО signing/legal semantics, ЕИС domain interpretation and customer mappings/transformations;
- no shared runtime, broker, secrets technology, connector marketplace or public API/SDK is selected by INT-B2; materially constraining shared implementation choices require ADR trigger analysis.

The integration lane may design and prototype bounded adapters in isolation, but a real governed reliance/connector implementation requires the applicable Product Contract and governance boundary before use.

## 7. Concurrency map

```text
                         ┌─ Lane A: P9.11 real UI dogfooding ──→ R32 ─→ P9.12/M9
                         │
current canonical main ──┼─ Lane B: INT-B3 concrete 1С design
                         │          ├─ INT-B4: Битрикс24
                         │          ├─ INT-B4: amoCRM
                         │          └─ INT-B5: concrete СЭД/ECM/ЭДО
                         │
                         ├─ Lane C: product ↔ Workspace composition
                         ├─ Lane D: reliability / DX / technical debt
                         └─ Lane E: future external/customer discovery
```

Only Lane A is on the critical path to M9. Parallel lanes must revalidate against current `main` before merge and must not silently change shared Workspace/BFF/session/security or connector-contract boundaries.

## 8. M9 definition

`M9 — Daily-use organizational workbench` requires:

- M9-alpha remains valid;
- at least two real product-owned surfaces composed through explicit boundaries;
- source-grounded, uncertainty-aware and authority-safe AI Copilot;
- non-authoritative activity/notification projections;
- useful ООО «Арвектум» company-level composition without Kernel product/company leakage;
- real owner working sessions completed primarily through Workspace;
- recurring usability friction dispositioned;
- applicable ADR obligations satisfied;
- R29–R32 material findings closed or explicitly accepted;
- pre-closure M9 Milestone Code Health Gate PASS.

Parallel integration progress is not itself an M9 closure criterion and therefore cannot replace P9.11 evidence.

## 9. Current canonical actions

**Critical path:**

> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**

**Parallel integration design:**

> **INT-B3 — 1С first-candidate design.**

These actions may proceed concurrently because INT-B3 is bounded design/evidence work and does not depend on synthetic P9.11 completion or alter the current Productive Workspace authority/security boundary. INT-B3 must begin from one concrete 1С configuration/deployment and bounded organizational outcome; a universal 1С model remains out of scope.
