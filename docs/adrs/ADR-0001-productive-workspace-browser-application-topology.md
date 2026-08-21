# ADR-0001 — Productive Workspace Browser Application Topology

Status: `Accepted`
Date: `2026-08-21`
Accepted: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`
Related RFCs: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008
Related work: `P9.02 — Application architecture spike + frontend/BFF/session decision`
Review gate: [`R29 — Productive Workspace Boundary Review`](../reviews/R29-productive-workspace-boundary-review.md) — `Complete / PASS`
Approval: [`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md) — `Approved`
Approved reviewed proposal blob: `47963cc4c9ca62e986dffbe09ac67b5c6345a111`

## Acceptance publication note

The conditional decision text below is retained from the owner-approved R29-reviewed proposal identified by the immutable blob above. Its acceptance condition is satisfied by the canonical owner approval and R29 PASS references in this publication header.

## 1. Context

Phase 9 must replace the diagnostic/reference P4/P7 browser shell with a real internal Productive Workspace capable of the P9.01 J1–J4 workload:

- persistent `My Work` / attention overview;
- human-readable global discovery;
- understandable object/context views with provenance on demand;
- governed decision/action flows that remain authority-safe.

The existing `http.server` + rendered-string HTML shell was intentionally bounded as diagnostic/reference/recovery evidence and is not a durable application architecture.

The selected browser/application topology is materially constraining and expected to shape P9.03–P9.12, so it crosses the ADR threshold. No Accepted RFC requires a particular frontend framework, BFF process topology or session technology.

The P9.02 architecture spike and R29 boundary review are the detailed evidence base.

## 2. Decision

If this ADR is Accepted, the Phase 9 internal Productive Workspace will use the following topology.

### 2.1 Frontend

Use a **React + TypeScript single-page application** as the persistent browser Workspace.

Use a **Vite-class build pipeline** to produce hashed static production assets. The exact dependency versions are implementation decisions and are not frozen by this ADR.

The production runtime does not require a Node application server. Node tooling is build/CI tooling only for the current scope.

### 2.2 BFF and browser/server trust boundary

Use a **same-origin Python Backend-for-Frontend (BFF) as a logical application boundary co-deployed in the existing Arvectum OS runtime unit**.

The BFF owns browser-facing request/session/CSRF/origin/host handling and human-oriented response shaping. It delegates queries and commands to governed application/platform/product-contract boundaries.

The BFF is not canonical state and is not an authority source.

The browser MUST NOT directly consume private platform tables, private streams, internal imports, reusable platform credentials or undocumented internal APIs.

Every browser-facing BFF request that reads governed or protected data MUST resolve an attributable actor and exactly one applicable Organization scope and MUST apply current server-side Authorization and Data Governance constraints before returning protected content, existence information, counts, previews or derived summaries. An unresolved, ambiguous, revoked or mismatched scope MUST fail closed and MUST NOT be made more informative through unauthorized projection data.

A BFF response or browser-visible control MUST NOT be treated as evidence that a later consequential command remains authorized.

### 2.3 Session

Use an **opaque server-side session**. The browser holds only the opaque session identifier in an HTTP cookie; identity/security/session meaning remains server-side.

Auth/session bearer material MUST NOT be stored in browser `localStorage` or `sessionStorage`.

A session MUST have bounded server-side scope and lifetime proportionate to the current internal owner-operated threat model. It MUST be revocable server-side. Session identifiers MUST be rotated when authentication state or other security-sensitive session binding changes in a way that would otherwise permit session fixation or stale privilege reuse.

Each request MUST resolve the current attributable actor and exactly one applicable Organization context server-side. Session state MAY assist that resolution but MUST NOT itself mint Authorization, Organizational Authority or Data Governance permission. Switching Organization context, if later supported, requires an explicit server-side validated transition; ambient cross-Organization session authority is prohibited.

For HTTPS-capable profiles, the session cookie is host-only and uses `Secure`, `HttpOnly` and `SameSite=Strict` by default. A reviewed interoperability case may choose `Lax`; broad cross-site cookies are not the default.

For the existing selected-Mac internal profile, an explicit loopback-only HTTP exception may be used during implementation only when the listener is strictly loopback, `HttpOnly` + `SameSite=Strict` remain set, CSRF/origin/host checks remain enforced, the exception is visible/tested, and no LAN/remote/customer exposure is claimed. Any non-loopback exposure requires HTTPS and a `Secure` session cookie.

Exact inactivity/absolute lifetime values and session-storage technology remain subordinate implementation/security decisions and may change without superseding this ADR provided the bounded-lifetime/revocation requirements above remain satisfied.

### 2.4 CSRF, origin and host

All state-changing browser requests use unsafe HTTP methods and require explicit CSRF validation bound to the server-side session plus same-origin/origin verification. Safe methods, especially `GET`, MUST NOT perform state changes.

The BFF MUST validate the request host/origin against the configured private Workspace origin model rather than accepting arbitrary host or cross-origin browser traffic. Broad CORS is not enabled for the private Workspace by default.

CSRF success does not satisfy Authorization, Organizational Authority, Data Governance or consequential approval.

### 2.5 Authority and command path

UI state, button visibility, cached claims and BFF session state do not constitute Authorization or Organizational Authority.

A consequential command MUST cross the server-side application boundary and revalidate, as applicable:

1. session/identity context;
2. explicit Organization scope;
3. Authorization;
4. Organizational Authority;
5. Data Governance;
6. validation/approval requirements;
7. Governed Execution requirements.

Consequential canonical mutation continues through Governed Execution. Outcomes remain truthfully distinguishable as completed, blocked, failed or uncertain where applicable.

A stale browser page, read model or session-local view MUST NOT be sufficient evidence for a consequential action. The server-side command path resolves and pins the current materially relied-upon governed versions as required by Accepted RFCs and applicable Product Contracts.

### 2.6 Read models and search

Use **rebuildable, Organization-scoped, non-authoritative application read models/projections** for Productive Workspace presentation and search.

P9.02/R29 do not standardize a separate projection database, search engine or vector store. The default implementation is the simplest local mechanism compatible with the existing persistent runtime.

Read models/search results MUST preserve sufficient source/version/provenance and freshness information for consequential or explanatory use. A rendered/search result is never authority for a consequential action; current relevant state is revalidated at the command boundary.

Projection generation and query serving MUST enforce applicable Organization scope, Authorization, Data Governance, classification, purpose/minimization and retention constraints. Derived indexes MUST NOT become a side channel that reveals protected object existence, counts, snippets or relationships denied by the governing source boundary.

When source/projection freshness is materially uncertain or source and projection disagree, the application MUST surface the limitation truthfully and MUST NOT silently prefer the derived representation for consequential behavior.

### 2.7 Product-owned UI composition

The Workspace shell/application security/navigation foundation remains platform-owned and domain-neutral. Product business semantics and detailed product surfaces remain product-owned.

For the current Phase 9 internal scope, product UI may be **compile-time composed into the same frontend build through an explicit registered boundary** traceable to applicable Product Contract/product decisions.

Product-owned browser code MUST use the same governed BFF/application boundary as platform-owned browser code. Compile-time composition does not grant private platform imports, internal-table access, reusable platform credentials, ambient product authority or undocumented server routes. Server-side product adapters relied upon by Workspace MUST remain traceable to the applicable Product Contract where RFC-0004 requires one.

This ADR deliberately does not freeze the schema of the contribution registry and does not establish a public/stable plugin API. The concrete reusable product-composition contract is deferred to P9.07 and applicable Product Contract governance.

Remote microfrontends and dynamic third-party code loading are not selected.

### 2.8 Deploy/update/rollback and browser release skew

The Python BFF/application code and built frontend assets form one exact Arvectum OS release/deployable unit for the existing owner-operated contour.

P7.06 governed deploy/update/rollback MUST move compatible frontend+BFF assets together. A rollback MUST NOT intentionally leave a frontend from one release paired with an incompatible BFF from another.

The runtime MUST serve the SPA entrypoint and hashed assets from its own exact release. Hashed immutable assets MAY use long-lived caching; the application entrypoint/release metadata MUST be revalidated so that deployment or rollback does not deliberately pin the browser to an incompatible historical shell indefinitely.

The browser/BFF exchange MUST make exact application release identity available to the application sufficiently to detect materially incompatible frontend/BFF skew. A detected material release mismatch MUST fail safely for consequential actions and direct the operator toward a controlled reload/recovery path rather than treating stale client state as authority.

No second production service lifecycle is introduced by this ADR.

### 2.9 Surface lifecycle and compatibility

The Phase 9 BFF/browser contract is an **internal, release-scoped application surface** for the current `Local / Persistent Internal / owner-operated` environment.

Acceptance of this ADR does NOT establish:

- a public API;
- a stable external browser/BFF compatibility contract;
- third-party client support;
- backward compatibility across arbitrary releases;
- customer Production or remote/LAN readiness;
- SLA/support/browser support-matrix commitments.

External or independently deployed consumers MUST NOT rely on `/bff/*` merely because the browser can call it. Any transition to an externally relied-upon or independently versioned API/BFF surface requires a new or superseding ADR plus applicable Product Contract, security, lifecycle and commercial-governance decisions.

## 3. Consequences

### Positive

- Strong fit for persistent J1–J4 workbench UX.
- Clear browser/server trust boundary for both reads and commands.
- No reusable platform credentials in browser code/storage.
- Same-origin topology reduces CORS and session complexity.
- Keeps security/authority checks server-side and compatible with RFC-0003/RFC-0005.
- Preserves non-authoritative projection semantics from RFC-0002/RFC-0006/RFC-0007/RFC-0008.
- Co-deployment preserves P7.06 exact-release operational simplicity.
- React/TypeScript provides reusable, testable and accessible interaction primitives without forcing a second production server.
- Product-owned UI can evolve without embedding product business rules into Kernel/platform semantics.
- Explicit internal/release-scoped BFF semantics avoid accidentally creating a public compatibility promise.

### Negative / cost

- Adds a frontend dependency/toolchain lifecycle to development and CI.
- Requires explicit BFF request contracts, session storage/lifecycle and CSRF/origin/host tests.
- Requires release-skew/caching behavior to be tested during deploy/rollback work.
- Creates a new application codebase that must be maintained alongside Python runtime code.
- Compile-time product composition requires rebuild/redeploy for product UI changes in the initial scope.
- A future public/distributed deployment may require revisiting the co-deployed BFF topology.

### Risks to control

- Accidental browser persistence of credentials or authority-relevant state.
- BFF becoming an undocumented public API or second source of truth.
- Unauthorized read-model/search leakage through counts, snippets or existence metadata.
- Stale or unreleased session state surviving security-sensitive context changes.
- View models/projections becoming treated as canonical state.
- Product UI registration becoming an accidental Stable Product Contract before P9.07 evidence.
- Loopback HTTP exception silently expanding to LAN/remote exposure.
- Frontend and BFF release skew after deployment or browser caching.

These are implementation/review gates, not reasons to weaken the higher-level invariants.

## 4. Alternatives considered

### A. Continue the current rendered-string `http.server` shell

Rejected for Productive Workspace. It remains diagnostic/reference/recovery evidence but is a poor durable fit for the J1–J4 persistent application workload and would encourage accidental handler/template accretion.

### B. Python server-rendered HTML with progressive enhancement

Valid fallback, but not preferred. It would keep operations simple yet is less suitable for the planned persistent workbench interaction/component model and likely creates a second migration when product composition/AI interaction becomes richer.

### C. React + TypeScript SPA + co-deployed Python BFF

Selected by this ADR as the best current balance of usability, explicit trust boundary, testability, reversibility and P7.06 operational simplicity.

### D. Full-stack Node application/BFF + separate Python platform service

Rejected for current Phase 9. It introduces a second production runtime/service/authentication boundary without evidence from J1–J4 that the added operational complexity is needed.

## 5. Migration / reversal path

This decision is intentionally reversible.

1. The SPA talks only to a bounded BFF/application surface, not platform internals.
2. The BFF remains logically separated from canonical/query/command services so it can later move to another process if evidence requires it.
3. Static frontend assets are packaged per exact release, allowing whole-release rollback under P7.06.
4. Read models remain rebuildable/non-authoritative and can move to another technology without semantic migration of canonical truth.
5. Product composition starts compile-time; a later governed extension mechanism can replace it without requiring remote microfrontend compatibility with the initial implementation.
6. If P9.03 demonstrates that SPA/toolchain cost is materially disproportionate, a superseding ADR may select the server-rendered fallback before substantial product UI reliance exists.

Any later move to a separately deployed BFF, public browser/API surface, remote microfrontend system, dedicated search service or external IAM topology requires a new or superseding ADR and applicable Product Contract/security governance.

## 6. Acceptance conditions

R29 confirmed the following conditions before this Accepted publication:

- no conflict with Constitution `1.2.0` or Accepted RFC-0001…RFC-0008;
- no browser-side authority or credential persistence shortcut;
- read-side and command-side server enforcement of explicit Organization scope, Authorization and applicable Data Governance;
- bounded, revocable server-side session semantics without ambient cross-Organization authority;
- server-side fail-closed Organizational Authority/approval boundary for consequential commands;
- consequential action path remains Governed Execution;
- read-model/search state remains non-authoritative and cannot leak denied protected metadata;
- product UI boundary does not freeze hidden or public product/platform coupling;
- P7.06-compatible exact-release deployment/rollback plus bounded browser release-skew behavior;
- BFF/browser surface remains internal and release-scoped rather than an accidental public/stable API/browser promise;
- loopback-only transport exception cannot be mistaken for remote-ready security.

These are architecture constraints. P9.03 and later gates still require implementation evidence.

## 7. Evidence

Primary evidence:

- [`P9-02-application-architecture-spike-frontend-bff-session-decision.md`](../reviews/P9-02-application-architecture-spike-frontend-bff-session-decision.md)
- [`P9-01-real-operator-jobs-acceptance-journeys.md`](../reviews/P9-01-real-operator-jobs-acceptance-journeys.md)
- [`P7-06-governed-deploy-implementation-review.md`](../reviews/P7-06-governed-deploy-implementation-review.md)
- [`R29 — Productive Workspace Boundary Review`](../reviews/R29-productive-workspace-boundary-review.md)
- [`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md)

Current subordinate external implementation guidance checked during P9.02:

- React: <https://react.dev/learn/installation>
- Vite backend integration: <https://vite.dev/guide/backend-integration.html>
- OWASP Session Management: <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- OWASP CSRF Prevention: <https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html>

These external references are implementation guidance only and do not override Arvectum OS canonical authority.