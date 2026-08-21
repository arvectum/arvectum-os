# R29 — Productive Workspace Boundary Review

Status: `Complete / PASS — ADR-0001 revised; owner disposition required before Accepted publication`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Roadmap gate: `R29 — Productive Workspace Boundary Review`
Review subject: [`ADR-0001 — Productive Workspace Browser Application Topology`](../adrs/ADR-0001-productive-workspace-browser-application-topology.md)
Predecessor evidence: [`P9.02 — Application Architecture Spike`](P9-02-application-architecture-spike-frontend-bff-session-decision.md)
Acceptance workload: [`P9.01 — Real Operator Jobs-to-be-Done + Acceptance Journeys`](P9-01-real-operator-jobs-acceptance-journeys.md)

## 1. Purpose

R29 is the architecture/governance gate between the P9.02 topology spike and material implementation of P9.03.

The review determines whether the proposed Productive Workspace topology can become Accepted implementation authority without weakening the Constitution or Accepted RFCs, creating hidden product/platform coupling, turning projections into authority, broadening browser trust, or accidentally creating a public/stable interface commitment.

The review uses a maximum of seven functional cross-review iterations. Six iterations were sufficient.

## 2. Canonical authority checked

Checked against current canonical `main` before review:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `1.0.0` are `Accepted`;
3. RFC-0001 — domain-neutral platform, Canonical Record / Governed Execution laws, security/isolation, technology independence, proportionate architecture and decision authority;
4. RFC-0002 — finalized Kernel metamodel, immutable/version-pinned governed state and non-authoritative projections without physical-schema mandates;
5. RFC-0003 — Identity / Authentication / Authorization / Organizational Authority / Data Governance separation, explicit Organization scope, deny-by-default, bounded sessions/tokens, isolation and minimization;
6. RFC-0004 — explicit Product Contracts before governed platform reliance and prohibition of hidden coupling through internal tables/imports/endpoints/private streams/implicit shared state;
7. RFC-0005 — consequential canonical mutation through Governed Execution and independent current gate revalidation;
8. RFC-0006 — canonical Event/provenance semantics, non-authoritative telemetry/projections and no hidden private event dependency;
9. RFC-0007 — search/index/RAG/summary projections remain non-authoritative and Organization/security/freshness controls remain applicable;
10. RFC-0008 — Document/Artifact/search/preview/derived-representation authority and provenance boundaries;
11. Decision Authority Policy `0.2.1` — `Proposed`, non-binding; residual decision authority remains with owner;
12. P7.06 governed deploy/update/rollback evidence — exact-release runtime unit and fail-closed rollback semantics;
13. P9.01 J1–J4 acceptance contract;
14. P9.02 architecture-spike result and Proposed ADR-0001;
15. Phase 9 and canonical master roadmaps.

No higher-authority source requires a different frontend framework, separate BFF process, public API, external IAM provider, dedicated projection database or product UI plugin technology.

## 3. Review dimensions

R29 reviewed the proposed topology across these functional views:

- architecture / Constitution / Accepted RFC compatibility;
- security, identity, session, CSRF, host/origin and Organization isolation;
- read/query and command authority boundaries;
- canonical state / projection / search / provenance boundaries;
- product/platform and Product Contract boundaries;
- deploy/update/rollback/version-skew fit with P7.06;
- stable/public surface and lifecycle/commercial non-claims;
- reversibility, proportionality and implementation freedom.

## 4. Iteration 1 — PASS on architecture level

### Review

The P9.02 selection of React + TypeScript SPA static assets with a same-origin Python BFF co-deployed in the existing exact-release runtime unit is compatible with the Constitution and RFC-0001/RFC-0002.

The decision is concrete enough for an ADR but does not redefine the permanent Kernel, physical persistence, authority model or product lifecycle. React/Vite/Python remain replaceable implementation technologies; the meaningful boundary is browser → BFF/application → governed services/Product Contracts/Governed Execution.

The separate Node/full-stack service remains unjustified for the current one-Organization owner-operated contour. Avoiding it is consistent with constitutional proportionality and P7.06 operational evidence.

### Result

`PASS` for architecture level.

No RFC or Constitution amendment is required.

## 5. Iteration 2 — REVISE: read-side trust and minimization

### Material finding

The P9.02 ADR correctly required server-side authority revalidation for consequential commands, but it did not state with sufficient normative force that **browser reads and projections** also require current Organization/Authorization/Data Governance enforcement before protected counts, previews, snippets, existence information or derived summaries are returned.

That gap could permit a conforming implementation to protect commands correctly while leaking protected information through search, `My Work` counts or product-derived projections. This would conflict with RFC-0003 deny-by-default/isolation/minimization and with P9.01 negative-path acceptance.

### Revision

ADR-0001 now requires every governed/protected BFF read to:

- resolve attributable actor and exactly one Organization scope;
- apply current server-side Authorization and Data Governance constraints;
- fail closed on unresolved/ambiguous/revoked/mismatched scope;
- avoid unauthorized existence/count/preview/summary leakage;
- enforce equivalent Organization/security/minimization constraints in projections and search indexes.

### Result

`REVISE → PASS` for read/query trust boundary.

## 6. Iteration 3 — REVISE: session lifecycle and Organization binding

### Material finding

The Proposed ADR selected opaque server-side sessions and safe cookie attributes but did not itself require a bounded session lifetime, server-side revocation or security-sensitive identifier rotation. RFC-0003 explicitly requires bounded session/token scope and lifetime and forbids trusting stale claims beyond their issuance guarantees.

The ADR also needed to make explicit that a session does not create ambient cross-Organization authority.

### Revision

ADR-0001 now requires:

- bounded server-side session scope/lifetime proportionate to the current internal threat model;
- server-side revocation;
- identifier rotation on security-sensitive session-binding changes sufficient to prevent fixation/stale-privilege reuse;
- server-side resolution of attributable actor and exactly one Organization context per request;
- explicit validated Organization transition if switching is ever introduced;
- no ambient cross-Organization session authority;
- implementation-specific exact timeout values remain subordinate and reversible.

### Result

`REVISE → PASS` for session/security boundary.

## 7. Iteration 4 — REVISE: Product Contract and stable-surface boundary

### Material finding

Compile-time product UI composition was correctly product-owned but could still become hidden coupling if product browser code gained private platform imports/routes or if `/bff/*` became an undocumented de facto external API used by products or future consumers outside the same exact release.

That would violate RFC-0004 hidden-coupling prohibitions and prematurely create compatibility expectations not approved by lifecycle or commercial governance.

### Revision

ADR-0001 now requires:

- product browser code to use the same governed BFF/application boundary as platform browser code;
- no private platform imports/tables/reusable credentials/ambient authority from compile-time composition;
- server-side product adapters traceable to applicable Product Contracts where RFC-0004 requires one;
- `/bff/*` to remain internal and release-scoped for the current owner-operated environment;
- no public API, third-party client, arbitrary cross-release compatibility or support-matrix promise;
- any externally relied-upon or independently versioned BFF/API to require new/superseding ADR and applicable Product Contract/security/lifecycle governance.

### Result

`REVISE → PASS` for product/platform and stable-surface boundary.

## 8. Iteration 5 — REVISE: exact-release deploy and browser cache skew

### Material finding

P7.06 proves exact-release runtime update/rollback, and ADR-0001 required frontend+BFF co-deployment, but a browser can retain previously cached frontend assets after an update/rollback. Without an explicit boundary, operationally exact server deployment could still expose an incompatible historical browser shell to a new BFF.

A stale client must not become authority or cause a consequential command to rely on incompatible client assumptions.

### Revision

ADR-0001 now requires:

- runtime serving SPA entrypoint and assets from its own exact release;
- hashed immutable assets may be long-cached, while entrypoint/release metadata is revalidated;
- exact application release identity available sufficiently to detect materially incompatible frontend/BFF skew;
- material release mismatch fails safely for consequential actions and directs controlled reload/recovery;
- browser/client version never substitutes for server-side current gate/version resolution.

### Result

`REVISE → PASS` for P7.06 deployment/version boundary.

## 9. Iteration 6 — final functional cross-review

### Architecture / governance

`PASS`.

The revised ADR is a concrete subordinate architecture choice and does not amend the Constitution or Accepted RFCs. It keeps the durable semantic boundary technology-independent and reversible.

### Security / privacy / Organization isolation

`PASS` for the declared internal architecture scope.

Reads and commands are server-controlled; Organization scope is explicit; session state is bounded/revocable and not authority; CSRF/origin/host controls are distinct from authorization; loopback HTTP remains an explicit local-only exception and cannot be represented as LAN/remote readiness.

This is architecture acceptance, not proof that P9.03 implementation already satisfies those controls.

### Authority / Governed Execution

`PASS`.

UI, session, read model and BFF are not sources of Authorization or Organizational Authority. Consequential commands revalidate current gates and remain routed through Governed Execution. Stale client/projection state is insufficient for consequential reliance.

### Canonical state / search / provenance

`PASS`.

Read models/search remain rebuildable and non-authoritative; source/version/provenance/freshness are preserved proportionately; discrepancies cannot silently redefine canonical or external authority.

### Product / platform

`PASS`.

Workspace shell/security/navigation remain domain-neutral. Product semantics stay product-owned; product browser code gains no hidden platform access through compilation; platform reliance remains Product Contract governed where applicable. P9.07 still owns the reusable product UI composition contract rather than ADR-0001 freezing it prematurely.

### Operations / recovery

`PASS` for architecture fit.

The selected topology preserves one exact-release P7.06 deployable unit and introduces no second production service lifecycle. Browser caching/release skew is now an explicit implementation gate.

### Public/stable/commercial scope

`PASS`.

ADR acceptance does not create customer Production, public/stable API, browser support matrix, SLA/support, Stable Product Contract, Active Platform Capability or multi-Organization conformance claim.

### Final review result

`PASS after 6 iterations`.

No material objection remains to accepting the revised ADR-0001 for the exact declared Phase 9 internal owner-operated scope.

## 10. ADR acceptance recommendation

R29 recommends:

> **ACCEPT ADR-0001 as the binding internal Productive Workspace browser/application topology for the current Phase 9 scope.**

Acceptance is appropriate because:

- architecture precedes material P9.03 reliance;
- no higher-authority conflict remains;
- all material R29 findings were incorporated into the ADR before acceptance;
- the decision remains reversible and proportional;
- the surface remains internal/release-scoped;
- future distributed/public/external topology changes require separate governance.

R29 itself does not manufacture owner approval. Canonical acceptance requires explicit owner decision authority and an approval record.

## 11. Required P9.03 implementation gates

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

## 12. Decision-authority disposition

Decision Authority Policy `0.2.1` is still `Proposed` and therefore does not create binding delegated authority. Accepted governance leaves residual decision authority with the owner of Arvectum OS.

The owner requested execution of the canonical next action R29 after being informed that the gate includes formal ADR-0001 disposition. The canonical approval record must preserve the actual acceptance decision before ADR status is published as `Accepted`.

## 13. Closure criteria

R29 closes only when all of the following are true:

- this review is canonically published;
- the revised ADR content reviewed here is identified immutably;
- owner approval is recorded canonically;
- ADR-0001 status/index are synchronized to the approved disposition;
- master and Phase 9 roadmaps advance to P9.03;
- resulting `main` state is verified after merge.

Until then, the review result is PASS but the gate is not canonically closed.