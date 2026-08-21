# Arvectum OS Phase 9 — Productive Workspace & Daily Operations

Status: `Active`
Version: `1.8.0`
Created: `2026-08-21`
Updated: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M9 — Daily-use organizational workbench`
Intermediate milestone: `M9-alpha — Usable Internal Workspace — Achieved / PASS`
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
| `P9.04` | `My Work` / Needs Attention projection | 🟩 Complete / PASS | actionable owner queue without raw execution hunting |
| `P9.05` | Human-friendly Records / Documents / Knowledge + global search | 🟩 Complete / PASS | understandable discovery and object context |
| `P9.06` | Executions / Decisions / governed actions UX | 🟩 Complete / PASS | owner can inspect and perform one real governed action |
| `R30` | M9-alpha Usability / Information Architecture Review | 🟩 Complete / PASS | ordinary workflow usable without terminal/internal IDs |
| `M9-alpha` | Usable Internal Workspace | 🟩 Achieved / PASS | daily core work usable through browser UI |
| **`P9.07`** | **Product-owned workspace surfaces / composition** | **🟨 Current** | at least two real product surfaces inside Workspace |
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

## 10. P9.04 implementation and closure result

Status: `Complete / PASS`.

Canonical evidence: [`P9-04-my-work-needs-attention-projection.md`](../reviews/P9-04-my-work-needs-attention-projection.md).

P9.04 established the first useful owner-facing work queue through the P9.03/ADR-0001 application boundary:

1. internal `arvectum.workspace.my-work/1` read contract with explicit derived/non-authoritative semantics;
2. server-resolved Organization/Actor scope and current P7.04 access revalidation before projection disclosure;
3. no protected denied-source existence/count leakage;
4. opaque projection-local focus links rather than raw governed/execution identifiers;
5. truthful live source adapters limited to already-proven P7.05 runtime health and P7.06 UI4 real owner preflight semantics;
6. controlled scenario evidence clearly marked as scenario rather than current organizational fact;
7. explicit `fresh / stale / degraded` projection health with fail-closed withholding of protected work when current state cannot be revalidated;
8. human-readable title/reason/source/legitimate next step and text-first attention categories;
9. compact `Needs attention` directly on Home plus full `/my-work` filtering/sorting/focus view;
10. no approve/retry/canonical mutation path and no inference of Authorization, Organizational Authority or Consequential Approval from visibility.

Functional cross-review completed four iterations. Material findings repaired test isolation, the P9.01 J1 Home visibility gap and exact CI-built production-asset reconciliation. The fourth iteration found no remaining material objection; the review stopped below the user-approved maximum of 10 rather than manufacturing additional iterations.

Final implementation evidence before this roadmap/review-only closure edit:

- implementation/reconciliation head `04776a93703aa8fd2e7cd9d2fa808fb62d16596b`;
- `Reference Python CI #258` — `SUCCESS`, `1301 tests`, `OK`;
- generated-Python-artifact rejection — `PASS`;
- `Productive Workspace CI #26` — `SUCCESS`;
- BFF security/context tests — `SUCCESS`;
- frontend typecheck/tests/Web-Storage/build/reproducibility/release-asset verification — `SUCCESS`.

Application release `p9.04.1` remains `bounded-internal-provisional`; internal app contract is `2`. P9.04 creates no public/stable API, Product Contract or Platform Capability lifecycle transition, customer Production claim or Organizational Authority.

P9.04 closes the queue/overview portion of J1 but does not claim full end-to-end J1 or `M9-alpha`: P9.05/P9.06 and R30 remain required for human-friendly exact object context, governed-action continuation and full J1–J4 usability evidence.

## 11. P9.05 implementation and closure result

Status: `Complete / PASS`.

Canonical evidence: [`P9-05-human-friendly-records-documents-knowledge-global-search.md`](../reviews/P9-05-human-friendly-records-documents-knowledge-global-search.md).

P9.05 established the first human-friendly discovery and exact-object-context layer through the P9.03/P9.04/ADR-0001 application boundary:

1. internal `arvectum.workspace.discovery/1` derived discovery and `arvectum.workspace.object-context/1` read contracts;
2. persistent global search plus dedicated Records, Documents and Knowledge routes;
3. server-resolved Organization/Actor scope and current protected-read revalidation;
4. human-readable semantic role/title/summary/source/authority/state in the ordinary path;
5. opaque browser object references, with exact Subject/Version/provenance available only through explicit technical drill-down;
6. real P9.01 F1 EIS notice `0344100006426000005` discoverable by human/external context and opened with `ЕИС / zakupki.gov.ru` / `External Reference` semantics intact;
7. `Observation`, Organizational Memory, Knowledge Candidate and validated Knowledge kept semantically distinct;
8. fail-closed degraded search/object behavior with no denied-result cardinality oracle and no stale protected details represented as current;
9. no durable search source of truth in the current implementation and no consequential write/effect path;
10. Workspace release `p9.05.1`, internal application contract `3`, still `bounded-internal-provisional` and non-public.

Functional cross-review completed two iterations. Iteration 1 passed source behavior/typecheck/tests/storage/build gates and found only the expected committed production-asset mismatch; exact CI-built assets were reconciled through a bounded one-shot helper and that helper was removed before closure. Iteration 2 passed Productive Workspace CI run `32477614572` and Reference Python CI run `32477614687` with no remaining material objection.

P9.05 closes the J2/J3 implementation slice for the declared real F1 discovery/context path. It does not claim full M9-alpha: P9.06 must still prove one bounded real governed interaction and R30 must review the complete J1–J4 ordinary path.

P9.05 creates no public/stable API, Product Contract or Platform Capability lifecycle transition, customer Production claim, broader conformance promise or Organizational Authority.

## 12. P9.06 implementation and closure result

Status: `Complete / PASS`.

Canonical evidence: [`P9-06-executions-decisions-governed-actions-ux.md`](../reviews/P9-06-executions-decisions-governed-actions-ux.md).

P9.06 established the first normal Productive Workspace governed-action experience through the Accepted ADR-0001 boundary:

1. human-readable inspection of the real retained P7.06-UI4 EIS-backed Execution/Decision context;
2. truthful `ЕИС / zakupki.gov.ru` / `External Reference` source-authority presentation;
3. four independent governance decision concepts — Authorization, Organizational Authority, Data Governance and Consequential Approval — without collapsing technical access into authority;
4. a real owner-initiated `Run governed preflight` interaction through the React/TypeScript Workspace;
5. current server-side access plus fresh real preflight reconstruction at the POST command boundary;
6. fail-closed rejection of any browser-supplied governance payload before provider execution;
7. real `WAITING / fail-closed` result with minimized owner-local non-canonical proof evidence only;
8. no canonical mutation, external effect, new approval/authority engine, competing source of truth or product-specific business logic moved into the platform;
9. exact Subject/Version/Execution/Event/checkpoint/provenance available through technical drill-down rather than required ordinary navigation;
10. Workspace release `p9.06.1`, internal application contract `4`, still `bounded-internal-provisional` and non-public.

Functional cross-review completed five iterations. Material findings tightened the command-input boundary and reconciled the exact CI-built production assets; the fifth iteration found no remaining material objection.

Final implementation/reconciliation evidence before the closure/roadmap-only edits:

- implementation head `627134709aa5348716b10ae9cac80afceb4bd8ed`;
- `Productive Workspace CI #47` / run `32482850242` — `SUCCESS`;
- `Reference Python CI #279` / run `32482850284` — `SUCCESS`, `1301 tests`, `OK`;
- generated-Python-artifact rejection — `PASS`;
- frontend typecheck/tests/Web-Storage/build/reproducibility/release-pin gates — `PASS`;
- BFF security/context/governed-action tests — `PASS`;
- temporary asset-reconciliation workflow removed before closure.

P9.06 implements the P9.01 J4 real fail-closed governed-interaction slice without manufacturing missing governance decisions or a demo mutation. It does not itself achieve `M9-alpha`: R30 must still execute/review the integrated J1–J4 ordinary path and the remaining milestone evidence.

P9.06 creates no public/stable API, Product Contract or Platform Capability lifecycle transition, external/customer Production claim, broader conformance promise or Organizational Authority.

## 13. M9-alpha exit criteria

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

R30 confirms all nine criteria as `PASS` for the exact private internal scope. M9-alpha is internal usability evidence only; it creates no public/stable surface or readiness/lifecycle promotion and does not substitute for P9.11 real daily-use dogfooding.

## 14. R30 / M9-alpha review result

Status: `R30 Complete / PASS`; `M9-alpha Achieved / PASS` within the exact private internal scope.

Canonical evidence: [`R30-m9-alpha-usability-information-architecture-review.md`](../reviews/R30-m9-alpha-usability-information-architecture-review.md).

R30 completed three functional cross-review iterations. Material findings repaired the ordinary J1→J3 attention/context continuation, J2 result-type narrowing, J3→J4 governed continuation, SPA focus management and technical-evidence-on-demand behavior. The final iteration found no remaining material objection.

The integrated P9.01 J1–J4 acceptance path passes with:

- no ordinary terminal/GitHub/internal-ID dependency;
- real EIS-backed human discovery/context with `External Reference` authority preserved;
- real retained Execution/Decision context in human terms;
- independent Authorization, Organizational Authority, Data Governance and Consequential Approval states;
- real P7.06-UI4 `WAITING / fail-closed` preflight through the normal Productive Workspace;
- no browser-provided authority, canonical mutation or external effect;
- exact technical identity/version/provenance rendered only after explicit drill-down;
- text-first critical state and explicit main-focus continuity on SPA navigation.

Clean implementation/reconciliation head `441106e65f7a69c54ff3ff89885ef1596b03e0a7` passed Productive Workspace CI #60 / run `32487968433` and Reference Python CI #292 / run `32487968464` (`1301 tests`, `OK`).

`M9-alpha` therefore satisfies all declared section 13 exit criteria. This is scoped internal usability evidence, not a public/stable interface, customer Production/readiness claim, lifecycle promotion, full M9 closure or substitute for P9.11 real daily-use dogfooding.

## 15. M9 exit criteria

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

## 16. Explicit non-goals

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

## 17. Current canonical action

> **P9.07 — Product-owned workspace surfaces / composition.**

Compose at least two real product-owned surfaces into Workspace through explicit Product Contract/extension boundaries while keeping product schemas, workflows, approvals, knowledge, templates and UX product-owned. The shared platform application must remain domain-neutral and must not gain hidden access to product internals.

P9.07 is the first post-M9-alpha implementation slice and targets the evidence needed for P9.01 J5. M9 remains open; P9.08–P9.12 and R31/R32 still govern the remaining AI, activity, company composition, dogfooding and hardening work.
