# DECISION-2026-08-21 — ADR-0001 Acceptance

Status: `Approved`
Decision date: `2026-08-21`
Owner / decision authority: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Decision subject: `ADR-0001 — Productive Workspace Browser Application Topology`
Approved reviewed proposal blob: `47963cc4c9ca62e986dffbe09ac67b5c6345a111`
Review gate: [`R29 — Productive Workspace Boundary Review`](../../reviews/R29-productive-workspace-boundary-review.md)
Constitution: `1.2.0` — `Ratified`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Decision Authority Policy: `Proposed 0.2.1` — non-binding; residual authority remains with owner
Canonical approval reference: this decision record

## 1. Decision

**APPROVED — accept the R29-reviewed ADR-0001 proposal identified by blob `47963cc4c9ca62e986dffbe09ac67b5c6345a111` as the binding architecture decision for the exact declared Phase 9 internal Productive Workspace scope.**

The approved topology is:

- React + TypeScript SPA built to static production assets;
- same-origin Python BFF as the browser-facing application boundary;
- frontend assets and BFF co-deployed as one exact Arvectum OS release under the existing P7.06 runtime/deployment contour;
- opaque bounded/revocable server-side sessions;
- explicit CSRF/origin/host controls;
- server-side Organization, Authorization and Data Governance enforcement for protected reads;
- separate server-side Organizational Authority/approval/Governed Execution enforcement for consequential commands;
- rebuildable Organization-scoped non-authoritative read models/search projections;
- compile-time product-owned UI composition only through explicit governed boundaries;
- internal release-scoped BFF/browser surface, not a public/stable external API contract.

## 2. Authority basis

Decision Authority Policy `0.2.1` remains `Proposed` and therefore has no binding delegated-authority force. Under the current Accepted governance baseline, residual decision authority remains with the owner of Arvectum OS.

The owner explicitly instructed execution of R29 after the prior canonical step identified R29 as the next action and stated that R29 includes formal ADR-0001 disposition before P9.03. This decision record canonically preserves the resulting approval rather than leaving it only in conversation history.

## 3. Review basis

R29 completed six functional cross-review iterations.

Material findings identified and incorporated before this approval:

1. protected BFF reads/search/projections must enforce current Organization/Authorization/Data Governance/minimization before returning content, counts, previews or existence information;
2. server-side sessions must be bounded in lifetime/scope, revocable and safely rotated on security-sensitive binding changes, without ambient cross-Organization authority;
3. compile-time product UI may not create private platform access or turn `/bff/*` into hidden Product Contract coupling or an accidental external stable API;
4. exact-release deployment must account for browser caching/frontend-BFF release skew and fail safely for consequential actions.

The final R29 iteration found no remaining material objection against Constitution `1.2.0`, Accepted RFC-0001…RFC-0008, current Product Contract boundaries or P7.06 exact-release operational semantics.

## 4. Approved scope

This approval applies only to the current Phase 9 operating contour:

- `Local / Persistent Internal / owner-operated`;
- one currently activated governing Organization: `ООО «Арвектум»`;
- private Productive Workspace browser application;
- no independently deployed browser/BFF consumer contract;
- no new externally relied-upon platform obligation.

The ADR remains technology-specific only at the subordinate implementation topology level. It does not change Kernel semantics or impose a permanent service/database topology.

## 5. Required implementation discipline

Acceptance authorizes P9.03 to materially implement the selected topology. It does not pre-approve implementation conformance.

P9.03 and later gates must prove, as applicable:

- explicit attributable actor and Organization resolution;
- protected read-side authorization/minimization;
- bounded/revocable session implementation and security-sensitive rotation;
- CSRF/origin/host enforcement;
- no auth/session bearer material in browser Web Storage;
- server-side current authority/gate revalidation for consequential commands;
- Governed Execution for consequential canonical mutation;
- non-authoritative projection/search behavior and truthful freshness;
- exact-release frontend/BFF packaging and safe stale-client handling;
- no hidden product/platform coupling;
- bounded loopback-only HTTP exception or a stronger HTTPS profile;
- applicable P9.01 J1–J4 acceptance evidence before M9-alpha.

## 6. Alternatives considered

The owner approves the R29 recommendation after review of the alternatives already recorded in ADR-0001/P9.02:

- continuing the P4/P7 rendered-string diagnostic shell — rejected as durable Productive Workspace architecture;
- Python server-rendered progressive-enhancement application — retained as a reversible fallback but not selected;
- React + TypeScript SPA with co-deployed Python BFF — selected;
- separately deployed Node/full-stack BFF plus Python platform service — rejected for the current contour because its additional operational/authentication/service boundary is not justified by J1–J4 evidence.

## 7. Consequences and accepted risks

Accepted costs include:

- a frontend build/toolchain lifecycle;
- a distinct application codebase alongside Python runtime code;
- explicit session/CSRF/origin/security test obligations;
- browser release-skew handling;
- rebuild/redeploy for initial compile-time product UI changes.

These costs are accepted because the topology remains one exact-release deployable unit, reversible, internal-first and proportionate to the Phase 9 workload.

No material security, privacy, cross-Organization, stable-public-contract or external commercial risk exception is accepted by this decision. Those invariants remain gates, not waived risks.

## 8. Explicit non-claims

This approval does not establish:

- customer/external Production;
- public SaaS;
- a public or Stable BFF/API/SDK/browser compatibility surface;
- third-party client support;
- LAN/remote readiness for the loopback HTTP profile;
- Stable Product Contracts;
- Active Platform Capabilities;
- SLA/support/certification commitments;
- realistic multi-Organization validation beyond existing evidence;
- AI Authorization, Organizational Authority or final consequential approval.

## 9. Effective transition

This approval becomes the canonical decision-authority basis for publishing ADR-0001 as `Accepted` only when:

1. ADR-0001 publication content matches the approved reviewed proposal except for acceptance metadata/status and references to this decision/R29;
2. the ADR index is synchronized;
3. R29 closure evidence and both roadmaps are synchronized;
4. resulting repository state is verified after merge.

The next canonical implementation action after successful R29 closure is `P9.03 — Real application shell + navigation + organization/user context`.