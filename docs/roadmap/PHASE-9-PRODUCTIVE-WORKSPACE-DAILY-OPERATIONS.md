# Arvectum OS Phase 9 — Productive Workspace & Daily Operations

Status: `Active`
Version: `1.4.0`
Created: `2026-08-21`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M9 — Daily-use organizational workbench`
Intermediate milestone: `M9-alpha — Usable Internal Workspace`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`); ADR-0001 `Accepted`
Predecessor: `Phase 8 / M8 — Complete / PASS`
Activation decision: [`DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION`](../governance/decisions/DECISION-2026-08-21-PHASE-9-PRODUCTIVE-WORKSPACE-ACTIVATION.md)

## 1. Purpose

Phase 9 converts the proven Arvectum OS semantic/runtime foundation into a genuinely useful daily work environment for the owner/operator of ООО «Арвектум».

M0–M8 proved architecture, governed runtime semantics, capabilities, Product Contracts, real-product validation, persistent owner-operated operation and bounded ecosystem integration. They did **not** prove that ordinary organizational work can be performed efficiently through a human-friendly application.

The current private workspace is valid diagnostic/reference evidence, but its primary UX is organized around platform internals such as Subject Identity, Version Identity, Execution, Event, provenance and retained manifests. Phase 9 does not discard those semantics; it moves them behind a productive application layer that presents human work, decisions, documents, products and organizational context first.

The Phase 9 question is:

> Can the owner use Arvectum OS as the normal daily interface for understanding what needs attention, finding organizational information, inspecting context, making governed decisions and working across products without relying on GitHub, terminal commands or internal identifiers for ordinary work?

## 2. Starting state

Inherited M8 baseline:

- persistent `Local / Persistent Internal / owner-operated` Arvectum OS runtime on the selected Mac mini;
- durable governed state, backup/restore and host-loss recovery;
- least-privilege identity/access/secrets operations;
- health, observability and audit visibility;
- governed update/rollback/version/migration;
- private browser workspace with real-state inspection and fail-closed governed preflight;
- persistent Tender Operator and Discount Parser contours;
- Creative Test Agent bounded external-consumer evidence;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- Product Contracts remain Provisional unless separately transitioned;
- no public/stable frontend/API/session/browser compatibility surface exists;
- no external/customer Production, SLA/support/certification or broad conformance claim exists.

The existing P4/P7 UI remains a diagnostic/reference/recovery surface. It is not the target productive application and MUST NOT be grown by incremental HTML-handler accretion into the long-lived Workspace by default.

## 3. Productive-workspace principles

1. **Human work first; platform internals second.** Technical identities/provenance remain available, but ordinary navigation uses human-readable names, status and context.
2. **Derived presentation is not canonical authority.** Dashboards, queues, notifications and search are projections over governed state.
3. **UI is not authority.** Buttons, visibility, AI suggestions and client-side state do not satisfy Authorization, Organizational Authority, Data Governance or Consequential Approval.
4. **Products own product semantics.** Tender/Discount/Creative schemas, workflows, decisions and product UI projections remain product-owned and enter Workspace only through explicit governed boundaries.
5. **AI proposes; Governed Execution acts.** Copilot/search may explain, summarize and prepare proposals; consequential state/effects remain governed.
6. **Daily usability is evidence.** A feature is not complete merely because semantic tests pass; the owner must be able to perform the declared job through the application.
7. **No speculative public surface.** Phase 9 is internal-first; public API/browser/SDK/support commitments require separate evidence and decisions.

## 4. Work breakdown

| ID | Work item | Status | Exit outcome |
|---|---|---:|---|
| `P9.00` | Productive Workspace activation + outcome baseline | 🟩 Complete / PASS | Phase 9 activated, UX problem and milestone scope fixed |
| `P9.01` | Real operator jobs-to-be-done + acceptance journeys | 🟩 Complete / PASS | six exact owner jobs, real/truthful fixtures, acceptance evidence contract and M9-alpha script fixed |
| `P9.02` | Application architecture spike + frontend/BFF/session decision | 🟩 Complete / PASS | four bounded topology prototypes compared; preferred topology fixed; ADR-0001 proposed |
| `R29` | Productive Workspace Boundary Review | 🟩 Complete / PASS | boundary PASS after 6 iterations; ADR-0001 owner-approved and Accepted |
| `P9.03` | Real application shell + navigation + organization/user context | 🟩 Complete / PASS | real ADR-0001 shell/BFF/session/release boundary implemented and regression-verified |
| **`P9.04`** | **`My Work` / Needs Attention projection** | **🟨 Current** | actionable owner queue without raw execution hunting |
| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | ⬜ | understandable discovery and object context |
| `P9.06` | Executions / Decisions / governed actions UX | ⬜ | owner can inspect and perform one real governed action |
| `R30` | M9-alpha Usability / Information Architecture Review | ⬜ gate | ordinary workflow usable without terminal/internal IDs |
| `M9-alpha` | Usable Internal Workspace | ⬜ milestone | daily core work usable through browser UI |
| `P9.07` | Product-owned workspace surfaces / composition | ⬜ | at least two real product surfaces inside Workspace |
| `P9.08` | Arvectum AI Copilot + source-grounded organizational assistance | ⬜ | useful AI analysis/proposals with provenance and authority-safe execution |
| `P9.09` | Activity, notifications and attention routing | ⬜ | human-readable operational timeline/alerts projection |
| `P9.10` | ООО «Арвектум» organization composition | ⬜ | company-level navigation over products/projects/knowledge/work |
| `R31` | Product Composition / AI Safety Review | ⬜ gate | no product leakage, hidden coupling or AI authority escalation |
| `P9.11` | Real daily-use dogfooding + friction/backlog closure | ⬜ | real working sessions completed primarily through Workspace |
| `R32` | M9 Productive Workspace Hardening + Milestone Code Health Gate | ⬜ gate | security/usability/maintainability/code-health PASS |
| `P9.12` | Phase 9 / M9 closure review | ⬜ | M9 exact-scope closure or explicit non-closure |

## 5. P9.00 activation result

P9.00 is `Complete / PASS` because:

- M8 is closed and no active post-M8 numbered implementation work item existed;
- real owner feedback identifies a material usability gap: the existing UI is useful as a technical/reference shell but not yet as a full productive daily interface;
- the gap is platform-level operator experience, not Tender/Discount/Creative business logic;
- the intended solution is reversible and can preserve existing authority/security semantics;
- no frontend/API/session technology is selected by activation;
- the owner explicitly approved proceeding step-by-step and using the resulting Workspace in real work.

## 6. P9.01 — Real operator jobs-to-be-done + acceptance journeys

Status: `Complete / PASS — acceptance baseline fixed; downstream journey execution pending`.

Canonical evidence: [`P9-01-real-operator-jobs-acceptance-journeys.md`](../reviews/P9-01-real-operator-jobs-acceptance-journeys.md).

P9.01 fixes six executable human outcomes before technology selection:

1. **J1 — Morning overview / what needs attention** — `M9-alpha blocker`;
2. **J2 — Find anything** — `M9-alpha blocker` for at least one real governed object;
3. **J3 — Understand context** — `M9-alpha blocker`;
4. **J4 — Make a governed decision/action** — `M9-alpha blocker`;
5. **J5 — Work across products** — full `M9` target after M9-alpha/P9.07, not an alpha blocker;
6. **J6 — Ask Arvectum** — full `M9` target after M9-alpha/P9.08, not an alpha blocker.

The acceptance fixture registry is anchored in real retained EIS/Tender Operator evidence, the persistent Tender Operator contour and the persistent Discount Parser contour. Truthfully representative controlled uncertainty fixtures are allowed only when no current real unresolved effect exists, must be visibly scenario evidence and must preserve the already-proven uncertainty/reconciliation semantics.

For ordinary paths, hard acceptance requires:

- zero dependency on terminal/GitHub/internal identifier knowledge;
- zero authority/success misrepresentation;
- zero Organization-scope violation;
- truthful external authority and uncertainty handling;
- exact technical identity/version/provenance reachable on demand rather than as primary navigation.

Task duration and primary interactions are measured during prototypes/dogfooding as comparative usability evidence; P9.01 deliberately does not invent a public UX SLA or arbitrary pre-prototype click/time threshold.

P9.01 completed five functional cross-review iterations with no remaining material objection. It does not claim that J1–J6 are already implemented or that M9-alpha/M9 has passed.

## 7. P9.02 — Application architecture spike result

Status: `Complete / PASS — preferred topology fixed and taken through R29`.

Canonical evidence: [`P9-02-application-architecture-spike-frontend-bff-session-decision.md`](../reviews/P9-02-application-architecture-spike-frontend-bff-session-decision.md).

P9.02 compared four bounded topology prototypes against P9.01 J1–J4:

1. accrete existing `http.server` + rendered-string HTML — rejected for Productive Workspace;
2. Python server-rendered HTML + progressive enhancement — valid fallback, not preferred;
3. React + TypeScript SPA + same-origin co-deployed Python BFF — preferred;
4. separately deployed full-stack Node/BFF + Python platform service — rejected for current owner-operated scope.

The preferred topology crossed the ADR threshold and proceeded to R29 rather than becoming implementation authority merely through roadmap text.

## 8. R29 — Productive Workspace Boundary Review result

Status: `Complete / PASS — 6 functional cross-review iterations; ADR-0001 Accepted`.

Canonical review: [`R29-productive-workspace-boundary-review.md`](../reviews/R29-productive-workspace-boundary-review.md).

Accepted ADR: [`ADR-0001 — Productive Workspace Browser Application Topology`](../adrs/ADR-0001-productive-workspace-browser-application-topology.md).

Owner approval: [`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md).

R29 confirmed the P9.02 topology only after revising four material boundaries:

- protected reads/search/projections are server-authorized, Organization-scoped and minimized before returning protected data or metadata;
- server-side session state is bounded/revocable and cannot create ambient Organization/authority scope;
- compile-time product UI gains no hidden platform access and the BFF remains internal/release-scoped rather than an accidental public/stable API;
- exact-release deployment includes safe browser frontend/BFF release-skew handling.

Final R29 result: no material conflict remains with Constitution `1.2.0`, Accepted RFC-0001…RFC-0008, applicable Product Contract boundaries or P7.06 exact-release semantics.

ADR-0001 is therefore binding architecture for the current `Local / Persistent Internal / owner-operated` Phase 9 application scope. Acceptance does not prove implementation conformance, public/customer readiness or lifecycle promotion.

## 9. P9.03 implementation and closure result

Status: `Complete / PASS`.

Canonical evidence: [`P9-03-real-application-shell-navigation-organization-user-context.md`](../reviews/P9-03-real-application-shell-navigation-organization-user-context.md).

P9.03 established the first material implementation of ADR-0001:

1. real React + TypeScript application shell built to release-pinned static assets;
2. same-origin Python BFF with no browser reliance on private platform internals;
3. explicit attributable actor and Organization context resolved server-side;
4. protected read-side Authorization/Data Governance/minimization;
5. opaque bounded/revocable session behavior and security-sensitive identifier rotation;
6. CSRF + configured Host/Origin enforcement;
7. no auth/session bearer material in browser Web Storage;
8. bounded loopback-only HTTP exception for the current private contour, with stronger HTTPS/Secure-cookie requirements outside it;
9. exact application release identity and safe stale-client/reload behavior;
10. domain-neutral navigation/application shell without product business logic leakage;
11. existing P4/P7 diagnostic/reference/recovery surfaces preserved.

Final repository-level functional cross-review completed six iterations. One material deployment gap was found and resolved before closure: P7.06 now installs/verifies the exact release's own Workspace runtime lock into the release-specific venv while preserving pre-P9 rollback compatibility and per-release isolation.

Final implementation evidence before this roadmap/review-only closure edit:

- implementation/reconciliation head `8989730d01ae43419d6b5c927b32c8b0ab82dd83`;
- `Reference Python CI #242` — `SUCCESS`, `1301 tests`, `OK`;
- generated-Python-artifact rejection — `PASS`;
- `Productive Workspace CI #10` — `SUCCESS`;
- frontend typecheck/tests/Web-Storage/reproducibility/release-asset gates — `SUCCESS`;
- BFF security/context tests — `SUCCESS`.

P9.03 creates no public/stable API, Stable Product Contract, Active Platform Capability, customer Production claim or Organizational Authority. Application release `p9.03.1` remains `bounded-internal-provisional`.

## 10. M9-alpha exit criteria

`M9-alpha — Usable Internal Workspace` is achieved only when the owner can, through the normal private Workspace and without terminal/GitHub/internal-ID knowledge for ordinary steps:

1. open a useful home page;
2. see `My Work` / items needing attention;
3. find a real organizational object by human-readable context;
4. open a real Document/Record/Knowledge item and understand its business context;
5. inspect one real Execution/Decision in human terms;
6. perform at least one bounded real governed interaction through the UI;
7. reach technical identity/version/provenance details on demand rather than as the primary UX;
8. pass the exact P9.01 J1–J4 acceptance script;
9. pass R29 and R30 with no unresolved material finding.

M9-alpha is an internal usability milestone, not a public/stable interface, Production/customer readiness or lifecycle transition.

## 11. M9 exit criteria

`M9 — Daily-use organizational workbench` requires the exact activated internal scope to demonstrate:

1. M9-alpha achieved;
2. at least two real product-owned surfaces composed into Workspace without platform business-logic leakage and P9.01 J5 passed;
3. AI Copilot is source-grounded, uncertainty-aware and authority-safe and P9.01 J6 passed;
4. activity/notifications remain non-authoritative projections;
5. company-level composition is useful without turning organization-specific semantics into shared Kernel behavior;
6. real owner working sessions can be completed primarily through Workspace;
7. recurring usability friction discovered by dogfooding is dispositioned;
8. application security/authority boundaries remain fail closed;
9. selected technology/stable-boundary ADR obligations are satisfied;
10. R29–R32 findings are closed or explicitly accepted by appropriate authority;
11. M9 Milestone Code Health Gate passes before closure.

## 12. Explicit non-goals

Phase 9 does not by itself establish:

- public SaaS;
- customer Production;
- universal multi-tenancy;
- public/stable API or SDK;
- Stable Product Contracts or Active Platform Capabilities;
- external browser/platform support matrix;
- SLA/support commitments;
- product business logic inside Arvectum OS;
- AI Organizational Authority or final consequential approval;
- automatic promotion of observations/generated outputs into validated Knowledge.

## 13. Current canonical action

> **P9.04 — `My Work` / Needs Attention projection.**

Build the first useful owner-facing work queue on top of the now-closed P9.03 application boundary. The projection must remain non-authoritative, Organization-scoped, authorization/data-governance filtered and human-readable; it must not require raw execution/internal identifiers for ordinary use or infer permission/authority from visibility.

The intended near-term sequence is `P9.04 → P9.05 → P9.06 → R30 → M9-alpha`. P9.03 shell/session/release boundaries remain the application foundation for these flows; M9-alpha is not achieved until the full declared exit set passes.