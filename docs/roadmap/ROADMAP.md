# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.73.0`
Created: `2026-08-07`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.73.0` activates **Phase 9 — Productive Workspace & Daily Operations** after M8 closure and closes `P9.00 — Productive Workspace activation + outcome baseline` as `Complete / PASS`.

The activation is driven by evidence from actual owner use: the current P4/P7 browser workspace correctly proves live governed-state inspection, exact identity/version/provenance, private least-privilege access and fail-closed governed preflight, but remains intentionally a technical/reference interface rather than a productive daily workbench. This is consistent with its canonical implementation boundary and is now treated as a material product/operational gap to solve.

Phase 9 is activated through [`DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION`](../governance/decisions/DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION.md). The detailed roadmap is [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) `Active 1.0.0`. The P9.00 evidence record is [`P9-00-productive-workspace-activation-outcome-baseline.md`](../reviews/P9-00-productive-workspace-activation-outcome-baseline.md).

P9.00 deliberately does **not** select a long-lived frontend framework, BFF/API/session topology or durable read-model technology. P9.01 must first define real owner jobs-to-be-done and acceptance journeys; P9.02 will then evaluate application architecture and trigger an ADR before material reliance if the selected technology becomes materially constraining or long-lived.

The new intermediate milestone is **`M9-alpha — Usable Internal Workspace`**: the owner can use the normal private browser Workspace for a useful home page, `My Work`, human-readable discovery/context, real Documents/Knowledge/Records, understandable Executions/Decisions and at least one real governed interaction without needing terminal, GitHub or internal identifiers for ordinary steps.

This activation does not create public/customer Production, Stable Product Contracts, Active Platform Capabilities, public/stable API/SDK/browser compatibility, SLA/support/certification, multi-Organization validation, or AI authority.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a permanent frontend, BFF/API/session, IAM, projection/read-model, public browser or product-UI composition topology;
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

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.0.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| **`P9.01`** | **Real operator jobs-to-be-done + acceptance journeys** | **🟨 Current** |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | ⬜ |
| `R29` | Productive Workspace Boundary Review | ⬜ gate |
| `P9.03` | Real application shell + navigation + organization/user context | ⬜ |
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
P9.01 real owner jobs / acceptance journeys           CURRENT
        ↓
P9.02 application architecture spike + ADR gate
        ↓
R29 Productive Workspace Boundary Review
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
8. R29 and R30 have no unresolved material finding.

M9-alpha is internal usability evidence only; it creates no public/stable surface or readiness/lifecycle promotion.

## 8. M9 definition

`M9 — Daily-use organizational workbench` requires M9-alpha plus:

- at least two real product-owned surfaces composed through explicit boundaries;
- source-grounded, uncertainty-aware and authority-safe AI Copilot;
- non-authoritative activity/notification projections;
- useful ООО «Арвектум» company-level composition without Kernel product/company leakage;
- real owner working sessions completed primarily through Workspace;
- recurring usability friction dispositioned;
- applicable ADR obligations satisfied;
- R29–R32 material findings closed or explicitly accepted;
- pre-closure M9 Milestone Code Health Gate PASS.

## 9. Current canonical action

> **P9.01 — Real operator jobs-to-be-done + acceptance journeys.**

P9.01 must turn the six initial journeys (`Morning overview`, `Find anything`, `Understand context`, `Make a governed decision/action`, `Work across products`, `Ask Arvectum`) into exact real owner workflows and acceptance evidence. Broad UI implementation or long-lived frontend technology selection should not precede this baseline.
