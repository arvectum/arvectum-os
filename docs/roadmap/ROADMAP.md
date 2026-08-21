# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.77.0`
Created: `2026-08-07`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.77.0` closes **`P9.03 — Real application shell + navigation + organization/user context`** as `Complete / PASS` after six repository-level functional cross-review iterations and advances Phase 9 to **`P9.04 — My Work / Needs Attention projection`**.

P9.03 implements Accepted ADR-0001 with:

1. a real React + TypeScript SPA compiled into committed release-pinned content-hashed static assets;
2. a same-origin co-deployed Python BFF with server-resolved Organization and attributable human actor context;
3. current protected-read Authorization/Data Governance/minimization, opaque bounded/revocable server-side sessions and explicit Host/Origin/CSRF controls;
4. no bearer/session material in browser Web Storage and a strict loopback-only HTTP exception for the current owner-operated contour;
5. exact application release identity with stale-client/reload failure semantics;
6. domain-neutral navigation with P9.04–P9.07 destinations truthfully marked planned rather than implemented;
7. exact P7.06 release coupling for the BFF runtime lock through the release-specific venv while preserving pre-P9 rollback compatibility and existing P4/P7 diagnostic/recovery surfaces.

One material P9.03 finding was resolved before closure: P7.06 already archived the exact Workspace runtime lock but did not install it into a newly prepared release-specific venv. Commit `c4520513e58a813858a53fb807e01473b9146c26` adds exact-release dependency installation, SHA-256 stamp idempotence and fail-closed FastAPI/Uvicorn verification without creating a second independent service lifecycle.

Final implementation/reconciliation head `8989730d01ae43419d6b5c927b32c8b0ab82dd83` passed `Reference Python CI #242` (`1301 tests`, `OK`, generated-artifact guard PASS) and `Productive Workspace CI #10` (BFF security/context and SPA typecheck/test/Web-Storage/reproducibility/release-asset gates PASS) against the then-current canonical `main`, including the independent approved P6.02 repository-locator reconciliation.

Canonical P9.03 evidence: [`P9-03-real-application-shell-navigation-organization-user-context.md`](../reviews/P9-03-real-application-shell-navigation-organization-user-context.md). Detailed Phase 9 roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) `Active 1.4.0`.

The intermediate milestone remains **`M9-alpha — Usable Internal Workspace`** and is **not yet achieved**. P9.04–P9.06 and R30 remain necessary before that milestone can pass.

P9.03 closure does not create public/customer Production, Stable Product Contracts, Active Platform Capabilities, public/stable API/SDK/browser compatibility, SLA/support/certification, multi-Organization validation or Organizational/AI authority.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `ADR-0001 — Productive Workspace Browser Application Topology` — `Accepted 2026-08-21` for the exact internal Phase 9 application topology;
- ADR-0001 acceptance evidence: R29 `Complete / PASS` after 6 iterations + `DECISION-2026-08-21-ADR-0001-ACCEPTANCE` `Approved`;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02, P6.06, P8.03 and P8.06 Product Contracts remain Provisional within their exact scopes;
- the operating environment remains `Local / Persistent Internal / owner-operated` with scoped conformance;
- no Platform Capability is `Active` and no Product Contract is `Stable` merely because M0–M8 completed, Phase 9 activated, ADR-0001 was accepted or P9.03 completed;
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

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.4.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| `R29` | Productive Workspace Boundary Review | 🟩 Complete / PASS |
| `P9.03` | Real application shell + navigation + organization/user context | 🟩 Complete / PASS |
| **`P9.04`** | **`My Work` / Needs Attention projection** | **🟨 Current** |
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
P9.02 application architecture spike                  PASS
        ↓
R29 boundary review + ADR-0001 acceptance              PASS
        ↓
P9.03 real application shell                          PASS
        ↓
P9.04 My Work / Needs Attention                        CURRENT
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

> **P9.04 — `My Work` / Needs Attention projection.**

Build the first useful owner-facing work queue through the closed P9.03 browser/BFF/session boundary. It must be a non-authoritative Organization-scoped projection; current Authorization/Data Governance/minimization must be enforced before returning protected item existence/counts/previews; visibility must not imply permission, Organizational Authority or consequential approval; ordinary owner use must not require raw execution/internal identifiers.

P9.04 does not itself achieve M9-alpha. The remaining critical sequence is `P9.04 → P9.05 → P9.06 → R30 → M9-alpha`.