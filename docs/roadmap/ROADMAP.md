# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.75.0`
Created: `2026-08-07`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.75.0` closes **`P9.02 — Application architecture spike + frontend/BFF/session decision`** as `Complete / PASS` for architecture-spike scope and advances Phase 9 to **`R29 — Productive Workspace Boundary Review`**.

P9.02 compared four bounded application topologies against the P9.01 `J1`–`J4` M9-alpha blocker workload and selected the preferred gate-ready shape: a React + TypeScript SPA built to static assets, a same-origin Python BFF co-deployed in the existing exact-release runtime unit, opaque server-side sessions, explicit CSRF/origin controls, rebuildable Organization-scoped non-authoritative read models, and compile-time product-owned UI composition without freezing a public/stable plugin contract.

The selected topology is materially constraining/long-lived, so the ADR threshold was crossed. [`ADR-0001 — Productive Workspace Browser Application Topology`](../adrs/ADR-0001-productive-workspace-browser-application-topology.md) now exists as `Proposed`; it has **not** been represented as Accepted or owner-approved. Broad P9.03 material reliance is therefore gated by R29, which must verify the product/platform, authority/security and stable-surface boundaries and disposition ADR-0001 through valid decision authority.

P9.02 explicitly rejects growing the P4/P7 `http.server` + rendered-string HTML diagnostic shell into the durable Productive Workspace and rejects a separately deployed Node/full-stack BFF service for the current owner-operated contour because J1–J4 provide no evidence that the added service/authentication/deployment boundary is necessary. Six functional cross-review iterations ended with no material objection for architecture-spike scope.

Canonical P9.02 evidence: [`P9-02-application-architecture-spike-frontend-bff-session-decision.md`](../reviews/P9-02-application-architecture-spike-frontend-bff-session-decision.md). Detailed Phase 9 roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) `Active 1.2.0`.

The intermediate milestone remains **`M9-alpha — Usable Internal Workspace`**: the owner can use the normal private browser Workspace for a useful home page, `My Work`, human-readable discovery/context, real Documents/Knowledge/Records, understandable Executions/Decisions and at least one real governed interaction without needing terminal, GitHub or internal identifiers for ordinary steps.

This roadmap update does not create public/customer Production, Stable Product Contracts, Active Platform Capabilities, public/stable API/SDK/browser compatibility, SLA/support/certification, multi-Organization validation, or AI authority. A Proposed ADR does not create an Accepted architectural contract.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `ADR-0001 — Productive Workspace Browser Application Topology` exists as `Proposed`; no Accepted ADR currently selects a permanent frontend, BFF/API/session, IAM, projection/read-model, public browser or product-UI composition topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02, P6.06, P8.03 and P8.06 Product Contracts remain Provisional within their exact scopes;
- the operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- no Platform Capability is `Active` and no Product Contract is `Stable` merely because M0–M8 completed or Phase 9 activated;
- no public/stable SDK/API/wire/browser surface, external/customer Production, SLA/support/certification or broader conformance claim exists.

## 4. Strategic roadmap

| Phase | Strategic scope | Status | Milestone |
|---|---|---|---|
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

## 5. Completed baseline through M8

Arvectum OS has already established, within its exact proven scopes:

- governed Kernel/runtime semantics, exact versions, relationships, provenance and Governed Execution;
- bounded shared capabilities CAP-001 through CAP-004 (`Incubating / Provisional`);
- operator/workspace semantic model;
- Product Contract and extension integration mechanisms;
- real Tender Operator and Discount Parser validation;
- persistent owner-operated Mac mini runtime;
- durable state, backup/restore and host-loss recovery;
- least-privilege identity/access/secrets operations;
- health/observability/audit visibility;
- governed deploy/update/rollback/version/migration;
- private live technical/operator workspace and real owner preflight interaction;
- persistent Tender Operator and Discount Parser operational contours;
- bounded external-authority validation and Creative Test Agent external-consumer evidence;
- Phase 8 hardening and M8 Milestone Code Health Gate.

The current private P4/P7 UI remains useful as diagnostic/reference/recovery evidence, but it is not considered the final productive daily Workspace.

## 6. Active Phase 9 — Productive Workspace & Daily Operations

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.2.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| **`R29`** | **Productive Workspace Boundary Review** | **🟨 Current gate** |
| `P9.03` | Real application shell + navigation + organization/user context | ⬜ blocked by R29 |
| `P9.04` | `My Work` / Needs Attention projection | ⬜ |
| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | ⬜ |
| `P9.06` | Executions / Decisions / governed actions UX | ⬜ |
| `R30` | M9-alpha Usability / Information Architecture Review | ⬜ gate |
| `M9-alpha` | Usable Internal Workspace | ⬜ milestone |
| `P9.07` | Product-owned workspace surfaces / composition | ⬜ |
| `P9.08` | Arvectum AI Copilot + source-grounded organizational assistance | ⬜ |
| `P9.09` | Activity, notifications and attention routing | ⬜ |
| `P9.10` | ООО «Арвектум» organization composition | ⬜ |
| `R31` | Product Composition / AI Safety Review | ⬜ gate |
| `P9.11` | Real daily-use dogfooding + friction/backlog closure | ⬜ |
| `R32` | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ gate |
| `P9.12` | Phase 9 / M9 closure review | ⬜ |

### Critical path to first genuinely useful Workspace

```text
P9.00 activation                                      PASS
        ↓
P9.01 real owner jobs / acceptance journeys           PASS
        ↓
P9.02 application architecture spike + Proposed ADR   PASS
        ↓
R29 Productive Workspace Boundary Review              CURRENT
        ↓
P9.03 real application shell
        ↓
P9.04 My Work / Needs Attention
        ↓
P9.05 human-friendly Records/Documents/Knowledge/search
        ↓
P9.06 Executions/Decisions/governed actions
        ↓
R30 usability / information architecture review
        ↓
M9-alpha — USABLE INTERNAL WORKSPACE
```

After M9-alpha the owner should begin using the new Workspace as the primary validation loop while P9.07–P9.12 add real product composition, AI assistance, activity/notifications, company-level composition and harden the daily-use baseline.

## 7. M9-alpha definition

`M9-alpha — Usable Internal Workspace` requires the owner to complete ordinary core work through the private browser Workspace without terminal/GitHub/internal-ID knowledge for ordinary steps:

1. open a useful home page;
2. see work requiring attention;
3. find a real organizational object using human-readable context;
4. open a real Document/Record/Knowledge item and understand its context;
5. inspect one real Execution/Decision in human terms;
6. perform at least one bounded real governed interaction;
7. reach exact technical identity/version/provenance details on demand rather than as the primary UX;
8. pass P9.01 J1–J4 with ordinary-path internal-ID dependency = false, terminal/GitHub escape = false, authority/success misrepresentation = false and Organization-scope violation = false;
9. R29 and R30 have no unresolved material finding.

M9-alpha is internal usability evidence only; it creates no public/stable surface or readiness/lifecycle promotion.

## 8. M9 definition

`M9 — Daily-use organizational workbench` requires M9-alpha plus:

- at least two real product-owned surfaces composed through explicit boundaries and P9.01 J5 passed;
- source-grounded, uncertainty-aware and authority-safe AI Copilot and P9.01 J6 passed;
- non-authoritative activity/notification projections;
- useful ООО «Арвектум» company-level composition without Kernel product/company leakage;
- real owner working sessions completed primarily through Workspace;
- recurring usability friction dispositioned;
- applicable ADR obligations satisfied;
- R29–R32 material findings closed or explicitly accepted;
- pre-closure M9 Milestone Code Health Gate PASS.

## 9. Current canonical action

> **R29 — Productive Workspace Boundary Review.**

R29 must review the P9.02 preferred topology and Proposed ADR-0001 against the Constitution and Accepted RFCs, with explicit attention to browser/server trust, server-side Authorization/Organizational Authority/Data Governance revalidation, Organization isolation, non-authoritative projections, product-owned UI boundaries, P7.06 exact-release deployment and absence of accidental public/stable API/browser commitments. R29 must disposition ADR-0001 through valid decision authority before P9.03 materially relies on the topology.