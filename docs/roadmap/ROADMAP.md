# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.94.0`
Created: `2026-08-07`
Updated: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing and concurrency. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.94.0` preserves `P9.11 — Real daily-use dogfooding + friction/backlog closure` as the current **critical-path** action while closing `INT-B6 — Integration security/reliability review` and advancing Lane B to `INT-B7 — First real connector pilot admission package`.

M9-alpha is already achieved and P9.07–P9.10 plus R31 are `Complete / PASS`. P9.11 depends materially on real owner working sessions, so bounded work that does not falsify or bypass P9.11 evidence may proceed concurrently.

Canonical parallel-workstream plan: [`PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md`](PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md) `1.0.0`.

`INT-B1` through `INT-B5` remain closed at their previously recorded scopes.

`INT-B6` is closed by [`INT-B6 — Integration Security / Reliability Review`](../reviews/INT-B6-integration-security-reliability-review.md) `1.0.0` — `PASS for bounded read-only pilot admission after reconciliation`, 4 of maximum 7 iterations. The review confirms Organization isolation, external authority, least-privilege credential boundaries, secret/private-key handling, explicit operation allowlists, freshness/completeness semantics, duplicate/gap/replay safety, uncertainty/reconciliation, source-occurrence/Event admission, data minimization/retention, fail-closed behavior and termination requirements across INT-B2–INT-B5.

The PASS is deliberately scoped. It does not activate a connector or authorize any external write/effect. Endpoint-specific discovery, credentials, data-purpose/classification, Product Contract where required, compatibility evidence, failure/reconciliation tests and ADR disposition remain mandatory before governed reliance.

`1С:ERP` remains the preferred first real pilot candidate because INT-B1 ranked 1С first and INT-B3 already defines the narrow read-only procurement projection. The next Lane-B artifact MUST use an exact real endpoint/deployment if one is available. Synthetic customer/deployment evidence is not accepted.

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
| **B — Russian-market integrations** | INT-B1–INT-B6 baseline/gate; first real bounded pilot admission | 🟨 INT-B1–INT-B6 complete; INT-B7 ready / real-endpoint dependent | **yes** |
| **C — Product ↔ Workspace composition** | Tender/Discount/Creative/Proxy product-owned projections and governed entry points | 🟦 Available | yes, within Product Contract/product-local boundaries |
| **D — Reliability / DX / technical debt** | CI, dependencies, observability, recovery regressions, evidence-backed cleanup | 🟦 Continuous | yes |
| **E — Future external/customer readiness** | second-Organization/customer/deployment/regulatory discovery only | ⬜ Discovery | yes, no customer-Production implementation |

### 6.1 Lane A — current UI branch

Current action remains:

> **P9.11 — Real daily-use dogfooding + friction/backlog closure.**

The owner uses the Productive Workspace for real work, records friction, and validates whether ordinary work can remain inside the Workspace rather than escaping to terminal/GitHub/internal identifiers. Material defects are fixed as they appear. R32 remains locked until real-session evidence and backlog disposition satisfy P9.11.

### 6.2 Lane B — integration sequence

Canonical integration sequence:

1. `INT-B1 — Integration portfolio baseline` — **Complete / PASS**;
2. `INT-B2 — Domain-neutral connector boundary pattern` — **Complete / PASS**;
3. `INT-B3 — 1С first-candidate design` — **Complete / PASS**;
4. `INT-B4 — CRM designs` — **Complete / PASS**;
5. `INT-B5 — СЭД/ECM/ЭДО design` — **Complete / PASS**;
6. `INT-B6 — Integration security/reliability review` — **Complete / scoped PASS** for bounded read-only pilot admission;
7. **`INT-B7 — First real connector pilot admission package` — Ready / real-endpoint dependent**.

INT-B6 gate disposition:

- all current candidates preserve external authority and begin from `External Reference`;
- one endpoint binding resolves to one governing Organization scope for admitted data;
- external IDs remain external aliases/references;
- dedicated least-privilege integration credentials are required; secrets/private keys remain outside ordinary canonical state, prompts, logs and repository files;
- authentication/API permission does not create Organizational Authority;
- operation allowlists remain explicit and read-only for the admitted first scopes;
- partial, stale, unavailable and schema-incompatible states must be explicit;
- webhook/event-feed/callback data is a source occurrence before canonical Event admission;
- duplicate/gap/retry/replay behavior must be deterministic and replay must not repeat external effects;
- document/content collection is minimized; derived artifacts remain non-authoritative by default;
- signing/sending/posting/payment/approval/stage-transition and other business writes remain prohibited;
- connector disable/termination preserves lawful history and external authority while revoking credentials/subscriptions and disposing non-authoritative caches according to retention;
- materially shared runtime/topology choices remain ADR triggers rather than implicit implementation decisions.

INT-B7 admission package MUST contain endpoint-specific evidence for:

- exact real system/account/portal/box/deployment;
- Organization mapping and external authority scope;
- one bounded outcome;
- exact read-only operation allowlist;
- dedicated least-privilege credential binding and revocation;
- purpose/classification/minimization/retention/deletion/portability;
- API/configuration/version compatibility;
- freshness/completeness and stale-state semantics;
- authentication, authorization, timeout, source-unavailable, partial-pagination/cursor-gap, schema-drift and credential-revocation failure tests;
- reconciliation and deterministic duplicate handling;
- source-occurrence/Event boundary where webhooks or feeds are used;
- connector disable/termination test;
- applicable Product Contract before governed product/shared-platform reliance;
- ADR disposition for any materially shared implementation constraint.

Preferred candidate is the INT-B3 `1С:ERP 2.5` read-only procurement projection. However, INT-B7 MUST NOT fabricate an endpoint. If no exact real 1С deployment is available, Lane B remains ready/blocked on real endpoint or may select another already-designed candidate only when an exact real binding and concrete organizational outcome exist.

## 7. Concurrency map

```text
                         ┌─ Lane A: P9.11 real UI dogfooding ──→ R32 ─→ P9.12/M9
                         │
current canonical main ──┼─ Lane B: INT-B7 first real connector admission
                         │             └─ exact endpoint required; no synthetic evidence
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

**Parallel integration:**

> **INT-B7 — First real connector pilot admission package — Ready / real-endpoint dependent.**

INT-B7 may proceed concurrently only when an exact real endpoint and bounded outcome exist. Until then, the integration lane must not fabricate operational evidence or treat a reference profile as a live deployment. No first material governed connector reliance is admitted without the endpoint-specific evidence, applicable Product Contract/governance gates and INT-B6 conditions recorded above.
