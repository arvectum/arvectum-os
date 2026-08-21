# R29 — Productive Workspace Boundary Review

Status: `Complete / PASS — 6 iterations; ADR-0001 owner-approved and Accepted`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Roadmap gate: `R29 — Productive Workspace Boundary Review`
Review subject: [`ADR-0001 — Productive Workspace Browser Application Topology`](../adrs/ADR-0001-productive-workspace-browser-application-topology.md)
Approval: [`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md)
Predecessor evidence: [`P9.02 — Application Architecture Spike`](P9-02-application-architecture-spike-frontend-bff-session-decision.md)
Acceptance workload: [`P9.01 — Real Operator Jobs-to-be-Done + Acceptance Journeys`](P9-01-real-operator-jobs-acceptance-journeys.md)

## 1. Purpose

R29 is the architecture/governance gate between the P9.02 topology spike and material implementation of P9.03.

The review determines whether the Productive Workspace topology can become Accepted implementation authority without weakening the Constitution or Accepted RFCs, creating hidden product/platform coupling, turning projections into authority, broadening browser trust, or accidentally creating a public/stable interface commitment.

Maximum functional cross-review iterations: 7. Completed: 6.

## 2. Canonical authority checked

Checked against canonical repository state before review:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `1.0.0` are `Accepted`;
3. RFC-0001 — domain-neutral platform, Canonical Record / Governed Execution laws, security/isolation, technology independence, proportionality and decision authority;
4. RFC-0002 — finalized Kernel metamodel, immutable/version-pinned governed state and non-authoritative projections without physical-schema mandates;
5. RFC-0003 — Identity / Authentication / Authorization / Organizational Authority / Data Governance separation, explicit Organization scope, deny-by-default, bounded sessions/tokens, isolation and minimization;
6. RFC-0004 — explicit Product Contracts before governed platform reliance and prohibition of hidden coupling through internal tables/imports/endpoints/private streams/implicit shared state;
7. RFC-0005 — consequential canonical mutation through Governed Execution and independent current gate revalidation;
8. RFC-0006 — canonical Event/provenance semantics and non-authoritative telemetry/projections;
9. RFC-0007 — search/index/RAG/summary projections remain non-authoritative and Organization/security/freshness controls remain applicable;
10. RFC-0008 — Document/Artifact/search/preview/derived-representation authority and provenance boundaries;
11. Decision Authority Policy `0.2.1` — `Proposed`, non-binding; residual decision authority remains with owner;
12. P7.06 governed deploy/update/rollback evidence — exact-release runtime unit and fail-closed rollback semantics;
13. P9.01 J1–J4 acceptance contract;
14. P9.02 architecture-spike result and Proposed ADR-0001;
15. Phase 9 and canonical master roadmaps.

No higher-authority source requires a different frontend framework, separate BFF process, public API, external IAM provider, dedicated projection database or product UI plugin technology.

## 3. Iteration 1 — PASS: architecture level

The P9.02 selection of React + TypeScript SPA static assets with a same-origin Python BFF co-deployed in the existing exact-release runtime unit is compatible with the Constitution and RFC-0001/RFC-0002.

The decision is concrete enough for an ADR but does not redefine the permanent Kernel, physical persistence, authority model or product lifecycle. React/Vite/Python remain replaceable implementation technologies; the durable boundary is browser → BFF/application → governed services/Product Contracts/Governed Execution.

A separate Node/full-stack production service remains unjustified for the current one-Organization owner-operated contour. Avoiding it is consistent with constitutional proportionality and P7.06 evidence.

Result: `PASS`. No RFC or Constitution amendment required.

## 4. Iteration 2 — REVISE → PASS: read-side trust and minimization

### Material finding

The Proposed ADR correctly required server-side authority revalidation for consequential commands, but it did not state with sufficient normative force that protected browser reads and projections also require current Organization/Authorization/Data Governance enforcement before counts, previews, snippets, existence information or derived summaries are returned.

That gap could leak protected information through search or `My Work` projections despite a correctly protected command path, conflicting with RFC-0003 and P9.01 negative-path acceptance.

### Revision

ADR-0001 now requires every governed/protected BFF read to:

- resolve attributable actor and exactly one Organization scope;
- apply current server-side Authorization and Data Governance constraints;
- fail closed on unresolved/ambiguous/revoked/mismatched scope;
- avoid unauthorized existence/count/preview/summary leakage;
- enforce equivalent Organization/security/minimization constraints in projections and search indexes.

Result: `PASS` after revision.

## 5. Iteration 3 — REVISE → PASS: session lifecycle and Organization binding

### Material finding

Opaque server-side sessions and cookie flags were selected, but the Proposed ADR did not normatively require bounded lifetime, server-side revocation or security-sensitive identifier rotation. RFC-0003 requires bounded session/token scope and lifetime and forbids relying on stale claims beyond issuance guarantees.

### Revision

ADR-0001 now requires:

- bounded server-side session scope/lifetime;
- server-side revocation;
- identifier rotation on security-sensitive binding changes sufficient to prevent fixation/stale-privilege reuse;
- server-side resolution of attributable actor and exactly one Organization context per request;
- explicit validated Organization transition if switching is ever introduced;
- no ambient cross-Organization session authority;
- exact timeout values remain subordinate implementation/security decisions.

Result: `PASS` after revision.

## 6. Iteration 4 — REVISE → PASS: Product Contract and stable-surface boundary

### Material finding

Compile-time product UI composition could still become hidden coupling if product browser code gained private platform imports/routes or if `/bff/*` became a de facto external API used outside the same exact release.

### Revision

ADR-0001 now requires:

- product browser code to use the same governed BFF/application boundary as platform browser code;
- no private platform imports/tables/reusable credentials/ambient authority through compile-time composition;
- server-side product adapters traceable to applicable Product Contracts where RFC-0004 requires one;
- `/bff/*` to remain internal and release-scoped for the current owner-operated environment;
- no public API, third-party client, arbitrary cross-release compatibility or support-matrix promise;
- any externally relied-upon or independently versioned BFF/API to require new/superseding ADR and applicable Product Contract/security/lifecycle governance.

Result: `PASS` after revision.

## 7. Iteration 5 — REVISE → PASS: exact-release deploy and browser cache skew

### Material finding

P7.06 proves exact-release runtime update/rollback and ADR-0001 co-deploys frontend+BFF, but a browser can retain previously cached frontend assets after update/rollback. Without an explicit boundary, an exact server release could still receive requests from an incompatible historical browser shell.

### Revision

ADR-0001 now requires:

- runtime serving the SPA entrypoint/assets from its own exact release;
- hashed immutable assets may be long-cached while entrypoint/release metadata is revalidated;
- exact application release identity available sufficiently to detect material frontend/BFF skew;
- material mismatch fails safely for consequential actions and directs controlled reload/recovery;
- browser/client version never substitutes for server-side current gate/version resolution.

Result: `PASS` after revision.

## 8. Iteration 6 — final functional cross-review

### Architecture / governance

`PASS`. The revised ADR is a concrete subordinate architecture choice and does not amend the Constitution or Accepted RFCs. It preserves technology independence and reversal paths.

### Security / privacy / Organization isolation

`PASS` for the declared internal architecture scope. Reads and commands are server-controlled; Organization scope is explicit; session state is bounded/revocable and not authority; CSRF/origin/host controls are distinct from authorization; loopback HTTP remains an explicit local-only exception and cannot be represented as LAN/remote readiness.

This is architecture acceptance, not proof that P9.03 implementation already satisfies the controls.

### Authority / Governed Execution

`PASS`. UI, session, read model and BFF are not sources of Authorization or Organizational Authority. Consequential commands revalidate current gates and remain routed through Governed Execution. Stale client/projection state is insufficient for consequential reliance.

### Canonical state / search / provenance

`PASS`. Read models/search remain rebuildable and non-authoritative; source/version/provenance/freshness remain attributable; discrepancies cannot silently redefine canonical or external authority.

### Product / platform

`PASS`. Workspace shell/security/navigation remain domain-neutral. Product semantics stay product-owned; compile-time composition grants no hidden platform access; platform reliance remains Product Contract governed where applicable. P9.07 still owns any reusable product UI composition contract.

### Operations / recovery

`PASS` for architecture fit. One exact-release P7.06 deployable unit is preserved; no second production service lifecycle is introduced; browser caching/release skew is an explicit implementation gate.

### Public/stable/commercial scope

`PASS`. ADR acceptance creates no customer Production, public/stable API, browser support matrix, SLA/support, Stable Product Contract, Active Platform Capability or multi-Organization conformance claim.

Final review result: **`PASS after 6 iterations`** with no remaining material objection.

## 9. Decision-authority disposition

Decision Authority Policy `0.2.1` remains `Proposed`, so residual decision authority remains with the owner under Accepted governance.

The owner instructed execution of R29 after the immediately preceding canonical step stated that R29 includes formal ADR-0001 disposition before P9.03. The resulting approval is now preserved canonically in:

[`DECISION-2026-08-21 — ADR-0001 Acceptance`](../governance/decisions/DECISION-2026-08-21-ADR-0001-ACCEPTANCE.md) — `Approved`.

Approved reviewed proposal blob: `47963cc4c9ca62e986dffbe09ac67b5c6345a111`.

ADR-0001 is published as `Accepted` only after that independent canonical approval record.

## 10. Required P9.03 implementation gates

ADR acceptance authorizes the topology, not an unreviewed implementation. P9.03 must prove at minimum:

1. real React + TypeScript application shell built to release-pinned static assets;
2. same-origin Python BFF boundary with no direct browser access to platform internals;
3. explicit attributable actor and Organization resolution on protected requests;
4. read-side Authorization/Data Governance/minimization checks;
5. opaque bounded/revocable session implementation with tested security-sensitive rotation;
6. CSRF + configured Host/Origin enforcement for unsafe requests;
7. no auth/session bearer material in Web Storage;
8. loopback-only HTTP exception mechanically prevented from becoming non-loopback remote exposure without HTTPS + Secure cookie profile;
9. release identity and stale-client/reload behavior sufficient to prevent incompatible frontend/BFF consequential actions;
10. product UI contribution remains bounded and does not create hidden Product Contract coupling;
11. no public/stable API/browser compatibility claim;
12. diagnostic P4/P7 shell remains recoverable/reference evidence or has an explicit governed replacement/retirement path rather than being silently mutated beyond recognition.

P9.04–P9.06 and R30 remain responsible for downstream projections/search/action usability and real J1–J4 execution evidence.

## 11. Closure disposition

R29 closure publication contains all required canonical artifacts:

- R29 functional cross-review evidence;
- immutable approved reviewed ADR proposal identity;
- independent owner approval record;
- ADR-0001 Accepted publication and ADR index synchronization;
- master and Phase 9 roadmap synchronization advancing to P9.03.

Repository merge history plus mandatory read-after-write verification of resulting `main` are the external publication evidence and are not embedded as self-referential hashes inside this review.

Closure result: `Complete / PASS` for the declared architecture/governance gate. This is not P9.03 implementation PASS, M9-alpha, Production readiness, lifecycle promotion or public/stable interface approval.