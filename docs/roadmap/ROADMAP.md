# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.78.0`
Created: `2026-08-07`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.78.0` closes **`P9.04 — My Work / Needs Attention projection`** as `Complete / PASS` after four functional cross-review iterations and advances Phase 9 to **`P9.05 — Human-friendly Records / Documents / Knowledge + global search`**.

P9.04 adds the first useful owner-facing attention projection through the Accepted ADR-0001 / P9.03 application boundary:

1. internal `arvectum.workspace.my-work/1` derived read contract with no canonical or Organizational Authority;
2. current server-side Organization/Actor scope and access revalidation before protected projection disclosure;
3. minimized denial semantics that do not expose protected source existence/counts;
4. truthful live signals from already-proven P7.05 runtime health and P7.06 UI4 preflight semantics, with controlled scenario evidence visibly marked as non-live;
5. explicit `fresh / stale / degraded` health and fail-closed withholding of protected work when source currency cannot be revalidated;
6. human-readable reason/source/next step, opaque projection-local focus links and no ordinary dependency on raw governed/execution identifiers;
7. compact `Needs attention` directly on Home plus full `/my-work` filtering/sorting/focus view;
8. no approval/retry/canonical mutation path and no inference of permission/authority from visibility.

The four review iterations repaired frontend-test isolation, the P9.01 J1 Home-visibility gap and exact CI-built production-asset reconciliation; the final semantic/security review found no remaining material objection. Final implementation/reconciliation head `04776a93703aa8fd2e7cd9d2fa808fb62d16596b` passed `Reference Python CI #258` (`1301 tests`, `OK`, generated-artifact guard PASS) and `Productive Workspace CI #26` (BFF security/context plus SPA typecheck/test/Web-Storage/build/reproducibility/release-asset gates PASS).

Canonical P9.04 evidence: [`P9-04-my-work-needs-attention-projection.md`](../reviews/P9-04-my-work-needs-attention-projection.md). Detailed Phase 9 roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) `Active 1.5.0`.

The intermediate milestone remains **`M9-alpha — Usable Internal Workspace`** and is **not yet achieved**. P9.05, P9.06 and R30 remain necessary for human-friendly exact object context, governed-action continuation and full P9.01 J1–J4 usability evidence.

P9.04 closure does not create public/customer Production, Stable Product Contracts, Active Platform Capabilities, public/stable API/SDK/browser compatibility, SLA/support/certification, realistic multi-Organization validation or Organizational/AI authority.

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
- no Platform Capability is `Active` and no Product Contract is `Stable` merely because M0–M8 completed, Phase 9 activated, ADR-0001 was accepted or P9.03/P9.04 completed;
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

Detailed roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md) — `Active 1.5.0`.

| ID | Work item | Status |
|---|---|---:|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS |
| `R29` | Productive Workspace Boundary Review | 🟩 Complete / PASS |
| `P9.03` | Real application shell + navigation + organization/user context | 🟩 Complete / PASS |
| `P9.04` | `My Work` / Needs Attention projection | 🟩 Complete / PASS |
| **`P9.05`** | **Human-friendly Records / Documents / Knowledge + global search** | **🟨 Current** |
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
P9.04 My Work / Needs Attention                       PASS
        ↓
P9.05 human-friendly Records/Documents/Knowledge/search CURRENT
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

> **P9.05 — Human-friendly Records / Documents / Knowledge + global search.**

Build the next owner-facing discovery/context layer through the P9.03/P9.04 Productive Workspace boundary. The ordinary path must find and open real governed organizational objects by human-readable context without terminal/GitHub/internal identifiers; derived discovery/search must remain non-authoritative; current source Authorization/Data Governance/minimization must be revalidated before protected existence/content is disclosed.

P9.05 does not itself achieve M9-alpha. The remaining critical sequence is `P9.05 → P9.06 → R30 → M9-alpha`.
