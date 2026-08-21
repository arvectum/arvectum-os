# P9.06 — Executions / Decisions / Governed Actions UX

Status: `Complete / PASS`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with governance implications
Roadmap item: `P9.06 — Executions / Decisions / governed actions UX`
Phase: `Phase 9 — Productive Workspace & Daily Operations`
Milestone target: `M9-alpha — Usable Internal Workspace`
Predecessor: `P9.05 — Complete / PASS`
Successor gate: `R30 — M9-alpha Usability / Information Architecture Review`

## 1. Purpose and closure scope

P9.06 turns the already-proven Governed Execution / owner-preflight semantics into a normal Productive Workspace experience. The owner can now open a human-readable governed-action surface, understand one real retained Execution/Decision context, see the four action-governance decision concepts independently and initiate one bounded real governed preflight through the React/TypeScript Workspace rather than the historical P4/P7 diagnostic UI.

The implementation deliberately uses the real retained P7.06-UI4 EIS-backed owner-preflight contour. It does **not** create a synthetic successful mutation merely to make the UI demonstrate a positive action. This is consistent with P9.01 J4, which explicitly accepts a real fail-closed preflight for M9-alpha when it is initiated through the new Workspace and proves that absent governance decisions are not manufactured.

P9.06 closes the implementation slice only. It does not by itself achieve `M9-alpha`; R30 must still execute/review the complete P9.01 J1–J4 ordinary-path usability and information-architecture evidence.

## 2. Canonical authority checked

Checked before and during implementation:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral platform behavior, explicit boundaries and evidence-driven reuse;
4. RFC-0003 — Organization scope, attributable Actor, least privilege, fail-closed access and strict separation of technical access, Authorization and Organizational Authority;
5. RFC-0005 — Governed Execution, independent governance gates, consequential action boundary, retry/replay requirements;
6. RFC-0006 — append-only canonical Events, provenance honesty, projection non-authority and no external-effect replay;
7. RFC-0008 — Document/Version/source/authority/provenance distinctions relevant to the retained EIS-backed source;
8. ADR-0001 — Accepted Productive Workspace topology: React/TypeScript SPA → same-origin Python BFF → existing platform query/command boundaries;
9. P9.01 — J4 acceptance journey and real F1/F2 retained EIS/Execution fixtures;
10. P9.03–P9.05 Productive Workspace implementation boundary;
11. canonical Phase 9 and master roadmaps.

No conflict with higher authority was found. No Constitution/RFC/ADR amendment is required.

## 3. Delivered implementation

### 3.1 Real execution / decision projection

`reference/python/workspace_app/governed.py` adds a bounded internal P9.06 adapter over `p7_06_ui4_owner_preflight.py`.

Every protected inspection rebuilds from the current exact-release retained runtime and current server-authorized `AccessContext`. The projection presents:

- a human-readable real EIS document governed-execution context;
- `ЕИС / zakupki.gov.ru` as the authoritative external source;
- authority mode `External Reference` without promoting the EIS fact into Native Arvectum authority;
- understandable current outcome and process meaning;
- four independent governance decision concepts:
  - Authorization;
  - Organizational Authority;
  - Data Governance;
  - Consequential Approval;
- exact Subject/Version/Execution/Event/checkpoint/provenance evidence only as an explicit technical drill-down.

The projection is presentation only. Visibility, session state and the action button provide no authority or permission.

### 3.2 BFF action boundary

The same-origin Productive Workspace BFF now exposes:

- `GET /api/app/v1/governed` — current server-authorized/revalidated governed execution projection;
- `POST /api/app/v1/governed/preflight` — bounded real owner-preflight action.

The POST path preserves the existing P9.03 security boundary:

- exact application release header required;
- configured Host and same Origin required;
- current bounded/revocable session required;
- current access is re-authorized before the command;
- CSRF continuity is required;
- browser-supplied governance payload is rejected fail-closed before provider execution.

The command therefore accepts no browser-supplied candidate record, authorization decision, Organizational Authority, Data Governance decision, consequential approval, retry token or external-effect instruction. Session/CSRF proves only continuity of the bounded technical request; it does not become a governance gate decision.

### 3.3 Bounded real governed interaction

Immediately before action execution, `RuntimeGovernedExperienceProvider.run_preflight` rebuilds the real P7.06-UI4 preflight from retained runtime evidence. The P9.06 action is admitted only for the exact already-proven `Waiting` case in which all four governance decisions remain unresolved.

The action delegates to the existing `ui4.record_browser_preflight` boundary, which revalidates the retained source/execution chain and writes only minimized owner-local **non-canonical proof evidence**.

The result explicitly states:

- outcome `Waiting`;
- canonical mutation requested: `false`;
- canonical mutation performed: `false`;
- external effect requested: `false`;
- external effect performed: `false`;
- Organizational Authority provided: `false`;
- Consequential Approval provided: `false`.

No second mutation path, approval engine, decision-authority policy, canonical store or external-effect adapter was added.

### 3.4 Human-first browser UX

The React/TypeScript Workspace adds `/governed` and activates `Governed actions` in the normal navigation spine.

The ordinary path now presents:

1. `Executions · Decisions · Governed actions` as human work rather than internal taxonomy hunting;
2. current status, authoritative source and authority mode;
3. a plain-language `What happened` explanation;
4. four independent governance decision cards with textual state/basis;
5. an explicit warning that page visibility, technical Workspace access and the button do not grant authority/approval;
6. `Run governed preflight` as the bounded real interaction;
7. a truthful `WAITING / fail-closed` result and non-canonical evidence receipt;
8. exact technical identities/provenance behind a drill-down rather than as required navigation input;
9. minimized fail-closed unavailable state when current protected evidence cannot be revalidated.

The frontend sends no governance body on the POST; it supplies only the existing CSRF header under the same-origin session boundary.

### 3.5 Release boundary

Application release advances to:

- release: `p9.06.1`;
- internal application contract: `4`;
- classification: `bounded-internal-provisional`;
- public API: `false`.

Exact production assets were rebuilt/reconciled from CI and committed. The temporary write-enabled reconciliation workflow used solely to materialize the deterministic CI build was removed before closure.

## 4. P9.01 J4 disposition

P9.06 implements the declared J4 interaction path over the real retained F1/F2 EIS/Execution evidence rather than a synthetic UX-only record.

The important semantic result is intentionally **not** success of a canonical mutation. The real current retained action evidence lacks the four action-specific governance decisions, so the correct outcome is `Waiting / fail-closed`.

This implementation proves the required safety property: initiating the interaction from the new Workspace does not manufacture Authorization, Organizational Authority, Data Governance or Consequential Approval from browser/session/button state.

The ordinary browser path no longer requires terminal, GitHub or prior knowledge/copy-paste of Subject/Version/Execution/Event identifiers to inspect the execution and initiate the bounded preflight. Exact identities remain reachable on demand for audit/reconstruction.

R30 remains responsible for the integrated owner usability/IA review and the complete J1–J4 acceptance record required before `M9-alpha` can be declared achieved.

## 5. Functional cross-review

Five review/revise iterations were completed. No material objection remains for P9.06 implementation scope.

### Iteration 1 — authority / Governed Execution boundary

Finding: a new productive action screen could accidentally become a second authorization/approval/mutation path.

Disposition: the implementation composes the existing real P7.06-UI4 preflight and proof-recorder only. It creates no new authority engine, policy, canonical mutation or external-effect path. The four governance decisions remain independent and unresolved.

Result: `PASS`.

### Iteration 2 — client-input / command-boundary security

Finding: the initial BFF route did not use browser-supplied JSON governance fields, but it still accepted an arbitrary request body. Silent ignoring was weaker than the desired fail-closed contract.

Revision: the governed-preflight POST now requires an empty request body and rejects any browser-supplied governance payload before provider execution. Regression coverage explicitly submits fake `approval` / `authority` fields and verifies rejection.

Result: `PASS`.

### Iteration 3 — source authority / product-platform boundary

Finding: bringing the real EIS-backed execution into a shared Workspace could accidentally imply Native authority or migrate Tender-specific business semantics into the platform.

Disposition: the presentation retains `ЕИС / zakupki.gov.ru` + `External Reference`, consumes only the already-retained domain-neutral governed document/execution/provenance contour, and adds no Tender-specific workflow/business rule to shared platform behavior.

Result: `PASS`.

### Iteration 4 — J4 usability / accessibility / minimization

Finding: a technically correct execution view could still force the owner to understand internal IDs or hide safety meaning in visual styling.

Disposition: the primary path is human-readable and text-first; exact technical identities are drill-down evidence; the four gate meanings and fail-closed status are textual; unavailable protected evidence is withheld rather than partially leaked. Frontend interaction tests cover the ordinary path and protected-unavailable state.

Result: `PASS`.

### Iteration 5 — release reproducibility / closure hygiene

Finding: the first implementation CI passed backend/typecheck/frontend interaction/build checks but correctly failed release-pin verification because committed `dist` still represented P9.05.

Revision: exact CI-built `p9.06.1` assets were reconciled, the temporary reconciliation workflow was removed, and a clean human-origin implementation head re-ran both mandatory CI contours successfully.

Result: `PASS`.

Functional cross-review is implementation review only. It is not formal RFC/ADR acceptance, lifecycle promotion, Production readiness, public API support or the R30 usability gate.

## 6. Verification evidence

Clean implementation/reconciliation head before this closure/roadmap-only documentation edit:

`627134709aa5348716b10ae9cac80afceb4bd8ed`

Mandatory CI on that exact head:

- `Productive Workspace CI #47` / run `32482850242` — `SUCCESS`;
  - BFF security/context/governed-action tests — `PASS`;
  - frontend TypeScript typecheck — `PASS`;
  - frontend interaction tests — `PASS`;
  - Web Storage bearer-material guard — `PASS`;
  - production build — `PASS`;
  - deterministic committed-asset/reproducibility check — `PASS`;
  - release-pinned asset verification — `PASS`;
- `Reference Python CI #279` / run `32482850284` — `SUCCESS`;
  - generated-Python-artifact rejection — `PASS`;
  - full Reference Python suite — `1301 tests`, `OK`.

The temporary P9.06 asset-reconciliation workflow is absent from the clean implementation state.

## 7. Explicit non-claims

P9.06 does **not** establish:

- `M9-alpha` completion before R30;
- a new authorization or Decision Authority model;
- browser/session/button-derived Organizational Authority or consequential approval;
- a new canonical mutation path;
- an external EIS mutation/effect;
- Product Contract stabilization or Platform Capability promotion;
- public/stable API, SDK, browser-support or compatibility commitment;
- external/customer Production, SLA/support/certification or broader conformance;
- a claim that EIS-backed facts became Native Arvectum authority.

## 8. Closure

`P9.06 — Executions / Decisions / governed actions UX` is `Complete / PASS` for its exact internal implementation scope.

The Productive Workspace can now inspect one real retained Execution/Decision in human terms and initiate the real bounded P7.06-UI4 governed preflight through the normal browser application. Missing governance decisions remain missing, the result stays truthfully `WAITING / fail-closed`, and no canonical/external effect is manufactured.

Canonical next action: **`R30 — M9-alpha Usability / Information Architecture Review`**.
