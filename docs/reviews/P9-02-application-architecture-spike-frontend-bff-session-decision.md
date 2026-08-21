# P9.02 — Application Architecture Spike + Frontend/BFF/Session Decision

Status: `Complete / PASS — preferred topology fixed for R29; ADR-0001 remains Proposed pending decision authority`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`
Parent roadmap: [`PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md`](../roadmap/PHASE-9-PRODUCTIVE-WORKSPACE-DAILY-OPERATIONS.md)
Acceptance baseline: [`P9-01-real-operator-jobs-acceptance-journeys.md`](P9-01-real-operator-jobs-acceptance-journeys.md)
Proposed ADR: [`ADR-0001-productive-workspace-browser-application-topology.md`](../adrs/ADR-0001-productive-workspace-browser-application-topology.md)

## 1. Purpose

P9.02 selects a bounded application topology for the Phase 9 Productive Workspace before implementation grows around the P4/P7 diagnostic shell.

The selection is evaluated against the P9.01 M9-alpha blocker journeys:

- `J1 — Morning overview / what needs attention`;
- `J2 — Find anything`;
- `J3 — Understand context`;
- `J4 — Make a governed decision/action`.

The existing P4/P7 `http.server` + rendered-string HTML implementation remains valid diagnostic/reference/recovery evidence only. It is not promoted into the long-lived Productive Workspace.

P9.02 does not change Kernel semantics, Product Contract lifecycle, Platform Capability lifecycle, public API commitments, organizational authority or canonical-state rules.

## 2. Authority and constraints checked

Checked before selection:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- ADR index — no Accepted ADR previously selected a permanent frontend/BFF/session topology;
- P9.01 real operator acceptance journeys;
- P7.06 governed deploy/update/rollback evidence;
- current `workspace_shell.py` diagnostic/reference boundary.

Material constraints inherited from higher authority:

1. UI and AI are not sources of Authorization or Organizational Authority.
2. Consequential canonical change goes through Governed Execution.
3. Authentication, Authorization, Organizational Authority and Data Governance remain distinct.
4. Organization scope is explicit and fail-closed.
5. Projections/search/read models remain derived and non-authoritative.
6. Product business semantics remain product-owned and may not enter the platform through hidden coupling.
7. Product/platform reliance must use declared Product Contract boundaries.
8. Generated browser/application state must not create a competing source of truth.
9. The implementation should remain reversible and operationally proportionate to the current `Local / Persistent Internal / owner-operated` contour.

No conflict with Constitution or Accepted RFC was found.

## 3. Spike workload

The architecture must support the following ordinary browser workload without requiring terminal, GitHub or internal identifiers:

### J1 — Morning overview

The application must hold a persistent shell, show useful `My Work` / `Needs Attention` categories, expose freshness/source truthfully and refresh bounded derived state without treating the projection as canonical authority.

### J2 — Find anything

The application must support human-readable search, scoped result lists, direct object navigation and provenance drill-down. Search indexes and result ranking are derived presentation only.

### J3 — Understand context

The application must compose human-oriented views from canonical/platform/product evidence while preserving source, authority, uncertainty and product ownership. Technical identity/version/provenance must remain reachable on demand rather than dominate the default view.

### J4 — Make a governed decision/action

The application must present an understandable action flow but must not authorize the action merely because a button is visible or enabled. The server-side action boundary must revalidate identity/session context, Authorization, Organization scope, Organizational Authority, Data Governance, validation and applicable approval gates before invoking Governed Execution. Results must remain truthfully `Completed`, `Blocked`, `Failed` or `Uncertain` as applicable.

## 4. Candidate architecture prototypes

The spike compares four bounded topology prototypes. These are architecture prototypes, not production implementations.

### Option A — Accrete the existing `http.server` + rendered-string HTML shell

Topology:

```text
Browser
  -> Python http.server handlers
      -> rendered HTML strings
      -> current reference/runtime adapters
```

Advantages:

- lowest immediate implementation cost;
- no new frontend toolchain;
- already useful for diagnostic/reference/recovery evidence.

Material defects for P9.01:

- poor component/state ergonomics for J1–J4;
- encourages route/HTML/business-shaping accretion inside the diagnostic shell;
- weak long-term accessibility and component testing ergonomics;
- likely to entangle presentation, browser security and runtime adapter concerns;
- contradicts the explicit P9.00/P9.01/P9.02 boundary that the existing shell is not the final productive application.

Disposition: **REJECT for Productive Workspace**. Retain as diagnostic/reference/recovery evidence.

### Option B — Server-rendered Python application + progressive enhancement/HTMX-style interactions

Topology:

```text
Browser
  -> Python application server
      -> HTML templates / partial responses
      -> application/query/command services
```

Advantages:

- one runtime language/process;
- naturally same-origin;
- simpler initial session/CSRF handling;
- low client-state complexity.

Material limitations for the intended workload:

- J1 live attention state, J2 search/filter/navigation, J3 context transitions and J4 multi-stage governed action UX would increasingly require client-side interaction conventions anyway;
- richer product-owned surface composition would tend to become template/server coupling;
- testable reusable interaction primitives are less direct for the planned persistent workbench;
- future P9.07/P9.08 composition and source-grounded assistance would likely force a second frontend architecture migration.

Disposition: **VALID fallback, not preferred**. Revisit only if the SPA implementation proves materially disproportionate during R29/P9.03.

### Option C — React + TypeScript SPA + same-origin Python BFF, co-deployed as one runtime unit

Topology:

```text
Browser
  -> same-origin Productive Workspace
       React + TypeScript SPA
       static production assets
  -> /bff/*
       Python BFF/application boundary
         -> query/read-model services
         -> canonical/application services
         -> Governed Execution command boundary
         -> Product Contract adapters
```

Production packaging:

```text
Vite build (build-time only)
  -> hashed static frontend assets
  -> packaged with exact Arvectum OS release
  -> served by the same Python application/deployable unit
```

Advantages:

- strong fit for persistent application shell and J1–J4 interaction state;
- explicit browser/server trust boundary;
- browser never needs direct access to internal platform APIs or reusable platform credentials;
- same-origin deployment simplifies cookies, CSRF/origin policy and CORS posture;
- frontend assets and Python server roll forward/back as one exact release under P7.06;
- no second production application server or Node runtime is required;
- React/TypeScript component model supports accessibility, reusable interaction primitives and browser-level testing;
- Vite supports a backend-integrated static build with a production manifest, keeping the Node toolchain build-time only;
- read and command paths can be separated cleanly without changing canonical semantics.

Costs:

- adds Node-based build tooling to development/CI;
- introduces a real frontend codebase and frontend dependency lifecycle;
- requires explicit BFF/session/CSRF contracts and end-to-end tests;
- requires discipline so frontend view models do not become a hidden product/platform contract.

Disposition: **PREFERRED**.

### Option D — Full-stack Node/Next-style application + separately deployed Python platform/API service

Topology:

```text
Browser
  -> Node full-stack frontend/BFF service
      -> Python platform/API service
          -> runtime/canonical state
```

Advantages:

- rich full-stack web ecosystem;
- SSR/server-components options;
- clean physical frontend/backend deployment separation.

Material defects for current scope:

- creates a second long-lived application server/runtime without P9.01 evidence requiring it;
- complicates P7.06 exact-release deploy/update/rollback and local owner-operated operations;
- creates an additional service-to-service authentication/authorization/session boundary;
- increases failure modes and operational evidence burden before external scale or public API needs exist;
- risks turning an internal Workspace implementation concern into a premature distributed architecture.

Disposition: **REJECT for current Phase 9**. A later externally deployed/public product may justify a separate decision.

## 5. Decision matrix

Scale: `1 = poor`, `3 = acceptable`, `5 = strong`. Scores are comparative engineering evidence, not governance authority.

| Criterion | A: string HTML | B: server HTML | C: React SPA + co-deployed BFF | D: split Node + Python |
|---|---:|---:|---:|---:|
| Persistent browser ergonomics / J1–J4 | 1 | 3 | **5** | 5 |
| Explicit server/authz revalidation boundary | 2 | 4 | **5** | 4 |
| Session/CSRF/origin simplicity | 2 | **5** | **5** | 3 |
| Derived read-model fit | 2 | 4 | **5** | 5 |
| Product-owned UI evolution | 1 | 3 | **5** | 5 |
| P7.06 deploy/update/rollback fit | **5** | **5** | **5** | 2 |
| Accessibility/component/E2E testing | 2 | 4 | **5** | 5 |
| Reversibility / operational complexity | 3 | **5** | **4** | 2 |
| Avoids premature public/distributed surface | 3 | **5** | **5** | 2 |
| Total | 21 | 38 | **44** | 33 |

Option C wins without requiring a new semantic RFC or a second production service.

## 6. Selected frontend boundary

The preferred Productive Workspace frontend is a **React + TypeScript single-page application** built into static production assets with **Vite-class build tooling**.

The ADR constrains the architectural shape, not exact package versions. Exact React/Vite/TypeScript versions remain implementation/dependency decisions subject to the normal dependency/security gates.

Rules:

1. The SPA is a presentation/application client, not canonical state.
2. The SPA may cache ephemeral UI/query state but may not persist authority-bearing credentials or canonical truth in browser storage.
3. No bearer access token, refresh token, session identifier or reusable platform credential may be stored in `localStorage` or `sessionStorage`.
4. The browser uses only the same-origin BFF surface for governed application interaction.
5. Internal platform tables, private streams and internal runtime imports are never browser interfaces.
6. Accessibility starts at the component boundary: semantic HTML, keyboard operation, visible focus, labels/names and sensible live-region behavior where asynchronous state changes require it.
7. Frontend errors/telemetry are non-canonical observability and must not contain secrets, raw session identifiers or cross-Organization data.

## 7. Selected BFF boundary

The preferred BFF is a **logical Python module/application boundary co-deployed in the existing Arvectum OS runtime unit**, not a separately deployed service at this stage.

Responsibilities:

- terminate the browser-facing same-origin application protocol;
- resolve the server-side session and explicit Organization context;
- enforce method/content/origin/CSRF requirements;
- construct human-oriented response/view models;
- call governed query/application services;
- invoke command/application services that lead to Governed Execution where consequential change is required;
- translate outcomes into truthful browser-visible states;
- attach bounded request correlation and provenance handles.

Explicit non-responsibilities:

- BFF does not become a second canonical system of record;
- BFF does not grant Organizational Authority;
- BFF does not replace Authorization or Data Governance policy evaluation;
- BFF does not directly mutate canonical tables/state for consequential actions;
- BFF does not embed Tender/Discount/Creative business logic into platform code;
- BFF does not expose private platform APIs as an undocumented product integration surface.

The same BFF process may serve the built SPA assets. Physical separation into another service requires a later ADR backed by operational/scale/security evidence.

## 8. Selected session and browser security model

### 8.1 Session shape

Use a **server-side opaque session**. The browser receives only an unpredictable opaque session identifier in an HTTP cookie. Identity, Organization binding, authentication metadata, expiry and CSRF state remain server-side.

Session data is **security/application state, not canonical organizational authority**. A session may carry bounded context needed to evaluate a request, but it may not turn cached roles/claims into permanent authorization truth.

Minimum server-side session fields/semantics:

- opaque random session identifier;
- authenticated Principal/Actor reference where authentication exists;
- explicit current Organization scope;
- authentication time/strength/source metadata sufficient for policy evaluation;
- creation time, last activity, idle expiry and absolute expiry;
- CSRF secret/token state;
- revocation/rotation state;
- optional non-sensitive UI preferences separated from security authority.

### 8.2 Cookie rules

For HTTPS-capable deployment profiles, the session cookie must be host-only and use `Secure`, `HttpOnly`, `SameSite=Strict` unless an explicitly reviewed interoperability need requires `Lax`; no `Domain` attribute; narrowest practicable path, normally `/` for a single-origin application.

The current selected-Mac contour may temporarily use an explicitly bounded loopback-only HTTP profile during P9.03 if and only if:

- listener binding is strictly loopback (`127.0.0.1`/equivalent), not LAN/all-interfaces;
- session cookie remains `HttpOnly` and `SameSite=Strict`;
- origin/host validation and CSRF controls remain enforced;
- no remote/browser exposure is claimed;
- the insecure transport exception is explicit in configuration and tests, not silently inferred;
- any LAN/remote/customer exposure is blocked until HTTPS allows a `Secure` session cookie.

This is a proportional internal-profile exception, not a public/stable browser-security promise.

### 8.3 Session lifecycle

- strict session management: reject unknown session identifiers rather than adopting them;
- rotate/regenerate on authentication and material privilege/authentication-context change;
- idle and absolute expiry are mandatory and configurable by the security profile;
- logout/revocation invalidates server-side state;
- session identifiers are never logged; use a non-reversible/salted correlation representation if session correlation is required;
- failure to resolve required Principal/Organization/security context is fail-closed.

### 8.4 CSRF/origin rules

State-changing BFF endpoints:

- use non-safe HTTP methods (`POST`/`PUT`/`PATCH`/`DELETE` as appropriate); `GET` is side-effect free;
- require a server-generated CSRF token returned to the SPA and echoed in a custom request header;
- validate the CSRF token against server-side session state;
- validate `Origin` and, where needed, `Referer`/Fetch Metadata as defense in depth;
- reject cross-origin requests by default;
- do not enable broad CORS for the private Workspace.

SameSite cookies are defense in depth and do not replace explicit CSRF validation.

## 9. Authorization, Organizational Authority and Governed Execution

The request path for a consequential action is:

```text
SPA intent
  -> BFF: session + org + CSRF/origin validation
  -> application command boundary
  -> current Authorization check
  -> current Organizational Authority check
  -> current Data Governance check
  -> validation / approval requirements
  -> Governed Execution
  -> canonical evidence / effect handling
  -> truthful outcome back to BFF/SPA
```

Rules:

- button visibility/disabled state is convenience only;
- the BFF/application backend revalidates the required authority controls at the action boundary regardless of client state;
- session-cached permissions may at most optimize presentation and must never be the sole consequential authorization decision;
- action requests carry explicit Organization scope and sufficient target/action context;
- uncertainty after external-effect dispatch is never rendered as success merely because the HTTP request returned;
- historical replay does not reissue an external effect without a new governed authorization/execution context.

## 10. Read-model / projection decision

Use **rebuildable, Organization-scoped application read models** behind query services/BFF response shaping.

For P9.03–P9.06, default to the simplest local implementation compatible with current persistent runtime rather than selecting a new database/search service prematurely.

Required properties:

- non-authoritative by construction;
- rebuildable from governed/canonical/product-contract-declared sources where applicable;
- explicit source/version/provenance handles;
- freshness/staleness metadata when material to user interpretation;
- Organization scope applied during projection creation and retrieval;
- derived data inherits applicable classification/access/retention constraints;
- stale/missing projection cannot silently grant authority or manufacture canonical truth;
- search ranking/index contents are presentation aids only;
- consequential actions resolve/revalidate current canonical/application state rather than trusting a previously rendered projection.

No durable projection technology is standardized by P9.02. A separate ADR is required if a later database/search topology becomes materially constraining.

## 11. Product-owned UI composition decision

P9.02 fixes a boundary, not a public/stable plugin API.

- Workspace shell/navigation/application security remain platform-owned and domain-neutral.
- Product-specific labels, schemas, workflow semantics, decision rules, knowledge and detailed product views remain product-owned.
- A product UI surface may enter Workspace only through an explicit registered boundary traceable to the applicable Product Contract/product decision.
- The initial implementation may use **compile-time composition inside the same frontend build** to minimize operational complexity.
- The exact contribution manifest/registry schema is deliberately deferred to P9.07 and must not become an accidental stable contract during P9.03–P9.06.
- No remote microfrontend, dynamic third-party code loading or hidden direct product-database access is selected.

This preserves a migration path to a stronger extension mechanism only after real multi-product evidence exists.

## 12. Deployment/update/rollback decision

For the current owner-operated contour:

```text
exact Arvectum OS release
  = Python application/BFF code
  + built SPA assets
  + compatible projection/schema metadata
  + tests/evidence
```

The Node toolchain is build-time/CI tooling only; production operation does not require a separate Node server.

P7.06 consequences:

- frontend and BFF roll forward/back as one release identity;
- static asset hashes/manifests are part of release evidence;
- rollback restores a compatible frontend+BFF pair rather than mixing versions;
- schema-changing projection migration remains governed by the existing migration/rollback discipline;
- browser cache behavior must not keep a rolled-back incompatible asset graph; hashed assets plus a non-long-lived app entry document are preferred;
- no second service lifecycle/port/health/credential boundary is introduced.

## 13. Testing, accessibility and observability baseline

P9.03 implementation must establish at least:

1. frontend unit/component tests for core navigation/state/error primitives;
2. BFF request-contract tests, including Organization scope and fail-closed session behavior;
3. CSRF/origin/session lifecycle negative tests;
4. end-to-end browser tests for the P9.01 J1–J4 ordinary path as each journey becomes available;
5. keyboard/focus/name/role accessibility checks on core flows;
6. truthful error/outcome tests for `Blocked`, `Failed` and `Uncertain` states;
7. projection freshness/provenance tests;
8. deploy artifact test proving frontend build output is packaged with the exact Python release;
9. structured request correlation without logging secrets/raw session IDs;
10. browser telemetry treated as non-canonical and Organization-safe.

Exact test libraries are implementation choices. A modern browser E2E runner such as Playwright is suitable but not made a stable platform contract by this decision.

## 14. Explicitly deferred decisions

P9.02 deliberately does **not** select:

- public/customer browser support matrix;
- public API or SDK;
- external IdP vendor or OIDC provider;
- multi-Organization production tenancy model;
- remote microfrontend/plugin runtime;
- CDN/edge deployment;
- WebSocket/event-stream transport;
- SSR/React Server Components/full-stack Node runtime;
- dedicated search engine/vector database;
- independent BFF service deployment;
- Stable Product Contract or Active Platform Capability transition.

These require evidence at the point they become necessary.

## 15. External implementation references checked

The architecture spike used current external implementation/security guidance only at the subordinate implementation level; these sources do not override Arvectum OS governance:

- React installation/current project guidance: <https://react.dev/learn/installation>
- Vite backend integration / production manifest: <https://vite.dev/guide/backend-integration.html>
- OWASP Session Management Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- OWASP Cross-Site Request Forgery Prevention Cheat Sheet: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>

## 16. Functional cross-review

Maximum configured review iterations: `7`.

### Iteration 1 — REVISE: operational topology

Finding: a split full-stack Node service would produce an additional runtime/deploy/authentication boundary without J1–J4 evidence requiring it.

Revision: prefer a logical Python BFF co-deployed with static SPA assets in the existing exact-release unit. Keep physical service separation as a future ADR-backed option.

### Iteration 2 — REVISE: browser credential/session risk

Finding: an SPA design is unsafe if bearer/session credentials become browser-readable persistent storage or if SameSite alone is treated as CSRF protection.

Revision: server-side opaque session, HttpOnly cookie, no auth/session credentials in Web Storage, explicit CSRF token + origin validation, strict session lifecycle and fail-closed context resolution.

### Iteration 3 — REVISE: authority leakage through presentation state

Finding: cached roles, visible actions or projection state could accidentally become authorization/authority evidence.

Revision: distinguish presentation hints from authority; revalidate Authorization, Organizational Authority, Data Governance, validation and approval at the server-side command boundary before Governed Execution.

### Iteration 4 — REVISE: product/platform hidden coupling

Finding: freezing a cross-product frontend plugin API in P9.02 would pre-empt P9.07 and could create a hidden stable surface before Product Contract evidence exists.

Revision: select only compile-time product-owned composition plus an explicit registered boundary; defer the concrete contribution schema/publicness to P9.07 and applicable Product Contract decisions.

### Iteration 5 — REVISE: loopback transport profile

Finding: requiring a `Secure` cookie without defining the current selected-Mac loopback transport would create either an unimplementable requirement or a silent security downgrade.

Revision: make HTTPS + `Secure` mandatory for any non-loopback exposure; permit only an explicit, tested loopback-only HTTP exception for the current internal contour with HttpOnly/SameSite=Strict, CSRF/origin/host enforcement and no remote-exposure claim.

### Iteration 6 — PASS

Architecture/governance: PASS. The topology changes no Accepted semantic contract and is captured at ADR level because it is long-lived/materially constraining.

Security/authority: PASS. Browser/session convenience cannot grant authority; cross-origin/session risks have explicit controls; Organization scope remains server-enforced and fail-closed.

Product/platform: PASS. Product semantics remain product-owned; no remote microfrontend or hidden product database/API dependency is created; concrete composition schema remains deferred until evidence exists.

Engineering/operations: PASS. One co-deployed runtime unit fits P7.06, avoids a second production server and has a clear reversal path to server-rendered UI or later service separation.

Usability/accessibility/testing: PASS for architecture-spike scope. The selected componentized SPA topology supports J1–J4 persistent UX and an explicit automated browser-testing/accessibility baseline.

No material objection remains within P9.02 scope.

## 17. Governance disposition

The selected topology is materially constraining/long-lived, so the ADR threshold is crossed.

`ADR-0001 — Productive Workspace Browser Application Topology` is therefore created as **`Proposed`**. P9.02 does not fabricate Acceptance or owner approval. Until a valid decision authority accepts the ADR:

- the architecture is the **preferred gate-ready decision**, not an Accepted normative contract;
- broad P9.03 material reliance is blocked by `R29`;
- bounded reversible proof code may be used only if clearly disposable and non-authoritative;
- R29 must verify the product/platform, authority/security and stable-surface boundaries and disposition ADR-0001 before long-lived implementation proceeds.

No RFC or Constitution change is required.

## 18. P9.02 closure

P9.02 is `Complete / PASS` for architecture-spike scope because:

- P9.01 J1–J4 were used as the concrete workload;
- four bounded topology prototypes were compared;
- frontend, BFF, session, CSRF/origin, read-model, product composition and deploy/rollback direction are explicit;
- the current diagnostic HTML shell was not promoted;
- the long-lived decision is captured in Proposed ADR-0001 rather than smuggled into implementation;
- six functional cross-review iterations leave no material objection;
- no higher-authority conflict was found.

Canonical next action: **`R29 — Productive Workspace Boundary Review`**. R29 must include disposition of Proposed ADR-0001 before P9.03 materially relies on the selected topology.