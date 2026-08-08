# R9 — Workspace Boundary Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Engineering gate: `R9 — Workspace Boundary Review`
Phase: `Phase 4 — Workspace / Operator Experience`
Result: **`PASS — the P4.01 + P4.02 workspace boundary remains explicit, fail-closed, non-authoritative, product-neutral and reversible; no accidental public API/frontend/IAM boundary or Product Contract substitute has been created, and no material finding blocks P4.03–P4.05.`**

## 1. Purpose

R9 is the mandatory focused engineering boundary gate after P4.02 and before the workspace expands into Canonical Record, provenance and Governed Execution surfaces.

The review asks whether the first visible workspace shell has already begun to harden accidental architecture merely because it is now executable and renderable.

R9 therefore reviews the accumulated P4.01 design and P4.02 implementation for:

- explicit Organization and attributable Actor context;
- fail-closed cross-Organization behavior;
- separation of presentation from authorization and Organizational Authority;
- Subject-versus-exact-Version navigation semantics;
- product/platform boundary integrity;
- absence of product-domain behavior in the shared shell;
- accidental public API, route, wire, frontend, IAM/session or durable read-model commitments;
- dependency direction and direct canonical-mutation bypass risk;
- reversibility and ADR-gate pressure;
- executable evidence sufficient to prevent regression while P4.03–P4.05 add richer surfaces.

R9 is an engineering review/hardening gate. It is not a Platform Capability admission, Product Contract promotion, operational-readiness approval, production/conformance statement or public-interface decision.

## 2. Canonical authority checked

R9 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral platform responsibility, non-authoritative projections, product/platform dependency rules, tenant isolation, technology independence and prohibition on accidental public interfaces;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, Subject-versus-Version reference semantics, explicit resolution and projection non-authority;
5. RFC-0003 — explicit Organization/Actor scope, deny-by-default access, no ambient cross-Organization authority, separation of identity/authentication/authorization/Organizational Authority and fail-closed unresolved scope;
6. RFC-0004 — explicit Product Contract boundary, no hidden product/platform coupling and the rule that contract/product context does not itself grant access or authority;
7. RFC-0005 — Governed Execution and gate separation, including the rule that presentation or Product Contract context cannot replace authorization, Organizational Authority or consequential approval;
8. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains the bounded reversible shell;
9. approved `DECISION-2026-08-08 — Engineering Quality and Refactoring Gates`, including the focused stable-boundary and ADR-gate requirements;
10. [`P4.01 — Operator Journeys, Workspace Boundary and Information Architecture`](P4-01-operator-journeys-workspace-boundary-information-architecture.md);
11. [`P4.02 — Organization Context, Identity and Scoped Navigation Shell`](P4-02-organization-context-identity-scoped-navigation-shell.md);
12. canonical Roadmap `2.12.0` and Phase 4 roadmap `1.2.0` at R9 start;
13. current reference implementation and P4.02 executable tests on main commit `7cbebe31bca79daae63aefacbdb35b041ad18f03`.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

The Decision Authority Policy remains non-normative unless and until it is approved. R9 introduces no decision that depends on delegated authority beyond the Accepted baseline.

## 3. Boundary under review

The reviewed boundary is intentionally small:

```text
ActorContext
  ├── actual Principal
  ├── optional represented Principal
  └── explicit Organization
          ↓
open_workspace_shell()
          ↓
┌──────────────────────────────────────────────┐
│ non-authoritative disposable presentation    │
│                                              │
│ Organization + Actor                         │
│ Discover / Records / Executions              │
│ Evidence / Documents / Knowledge             │
│ Subject OR exact Version reference           │
│ optional Product/Product Contract context    │
└──────────────────────────────────────────────┘
          ↓
no source dereference in the shell
no authorization decision in the shell
no Organizational Authority in the shell
no canonical mutation in the shell
no Product Contract validation in the shell
no route/API/session/wire contract in the shell
```

The HTML renderer is evidence that the semantic shell can be seen by a human. It is not a browser application architecture.

## 4. Review findings

### R9-F1 — Organization / Actor boundary remains explicit and fail-closed

Severity: `No material finding`
Result: `PASS`

The shell requires an explicit `ActorContext` carrying one `OrganizationScope` before it exposes navigable workspace state.

If actor/Organization context cannot be resolved, `open_workspace_shell()` returns a blocked state with:

- no governed content;
- no enabled navigation;
- no fallback/default Organization.

An optional product-entry context from a different Organization also blocks the shell rather than switching scope implicitly.

Cross-Organization navigation references are rejected before presentation state changes. The rejection message intentionally omits foreign target and Organization identifiers so the shell does not convert scope validation into an existence/metadata disclosure channel.

This is compatible with RFC-0003 tenant-scope and failure-closed requirements.

### R9-F2 — Presentation cannot create authorization or Organizational Authority

Severity: `No material finding`
Result: `PASS`

`WorkspaceShellState` contains context and navigation state only. It does not carry:

- authorization grants;
- permissions;
- Organizational Authority;
- approvals;
- gate outcomes;
- canonical mutation operations;
- Execution Context state.

`PresentationAuthority.NON_AUTHORITATIVE` is the only admitted presentation-authority classification in the shell.

The workspace module does not import the canonical mutation, execution or gate semantic owners. Navigation therefore cannot become an alternate write/enforcement path merely by adding UI affordances.

This boundary is especially important before P4.05: a visible or enabled control may express operator intent, but only the governed runtime may determine and execute a consequential operation.

### R9-F3 — Subject and exact-Version semantics remain intact

Severity: `No material finding`
Result: `PASS`

P4.02 keeps two different semantic reference types:

- `SubjectNavigationReference` — logical subject, not exact current state;
- `ExactVersionNavigationReference` — one exact immutable Version Identity.

Navigation preserves an exact historical Version Identity without resolving or redirecting it to Canonical Head or Effective Version.

The reference values contain no URL, path, query, endpoint, token, session or serialized payload fields. They remain semantic internal presentation inputs rather than a stabilized routing/wire contract.

P4.03 remains responsible for actual governed source resolution, Head/Effective semantics, authority-mode presentation and relationship inspection.

### R9-F4 — Product entry context has not become a hidden Product Contract

Severity: `No material finding`
Result: `PASS`

`WorkspaceProductContext` carries only:

- Organization scope;
- Product identity;
- optional Product Contract Version Identity reference.

It carries no capability grant, operation list, authorization result, Organizational Authority, contract-validity result or lifecycle promotion.

The context is also not exported as a public package-root surface.

Accordingly, P4.02 has not created a hidden substitute for RFC-0004 contract validation. The first real Product Contract-backed bounded workspace entry point remains P4.08 scope.

### R9-F5 — Shared workspace remains product-domain neutral

Severity: `No material finding`
Result: `PASS`

The shared shell exposes only the P4.01 domain-neutral destinations:

- `Discover`;
- `Records`;
- `Executions`;
- `Evidence`;
- `Documents`;
- `Knowledge`.

No tender, procurement, CRM, finance, marketing, legal or other product-domain screen, workflow stage, queue, role taxonomy, scoring rule or business decision logic appears in the shell.

The current implementation therefore remains an operator surface over shared governed semantics rather than a generic product orchestrator.

### R9-F6 — No accidental public frontend/API/route/IAM boundary has stabilized

Severity: `No material finding`
Result: `PASS`

The review found no selected or materially relied-upon:

- frontend/runtime framework;
- route or deep-link schema;
- REST/GraphQL/gRPC surface;
- public serialization/wire schema;
- BFF/service topology;
- browser session mechanism;
- authentication protocol or IAM provider;
- durable workspace/read-model/cache store;
- stable frontend SDK/package export;
- design-system package contract.

The workspace module imports only the existing internal `identity` and `security` semantics plus Python standard-library facilities. It is not exported from the provisional package root.

The HTML adapter contains inert buttons and textual semantic state only. It defines no links, forms, scripts, endpoint paths or client/server protocol.

No ADR threshold is crossed by the current shell.

### R9-O1 — Organization wrapper and `Identity.scope` must not become competing scope proofs

Severity: `Bounded handoff observation — not a current material defect`
Disposition: `Required P4.03 resolver invariant`

The current navigation references carry an explicit `OrganizationScope` and opaque RFC-0002 `Identity` values. The reference shell checks the explicit Organization wrapper but deliberately does not dereference governed objects or interpret identifier encoding.

This is safe for P4.02 because the shell itself cannot retrieve protected content and RFC-0002 Identity possession is not permission.

However, once P4.03 resolves a Subject or Version to governed source state, the implementation **must not** treat the presentation wrapper, `Identity.scope` string or identifier syntax as sufficient proof of access or canonical Organization membership.

P4.03 source resolution must:

1. resolve the Identity under the applicable governed organization/platform scope;
2. independently enforce current source authorization and RFC-0003 isolation;
3. reject an inconsistent Organization/identity/source combination fail-closed;
4. preserve platform-global scope only where the governed source actually declares it and access is permitted;
5. avoid turning a string-format convention into an authorization or identity-equivalence rule.

This observation does not justify strengthening the P4.02 value object into an IAM/resource resolver or changing RFC-0002 Identity semantics. Doing so now would move source-resolution responsibility into the presentation shell and create the coupling R9 is intended to prevent.

## 5. Executable R9 hardening evidence

R9 adds:

- `reference/python/tests/test_r9_workspace_boundary_review.py`.

The guard verifies that:

1. workspace shell types/functions remain absent from the provisional package-root public surface;
2. `workspace_shell.py` depends only on existing `identity` and `security` semantic owners, not Canonical Record, mutation, execution, gate, capability-consumption or product-composition modules;
3. the shell selects no public web/frontend, transport, serialization or durable-storage framework;
4. Subject and exact-Version navigation references remain semantic values without route/wire/session fields;
5. `WorkspaceProductContext` remains context-only until P4.08 and carries no permission/authority/contract-validity surface;
6. presentation navigation cannot call known governed mutation, execution or gate paths;
7. the HTML adapter remains inert and defines no route/form/script protocol;
8. the critical P4.02 negative boundary tests remain present as semantic-owner evidence.

These guards complement rather than replace the behavioral P4.02 tests.

## 6. Dependency and maintainability disposition

Result: `PASS`.

The shell has one clear responsibility: carry attributable Organization-scoped presentation/navigation context.

R9 found no evidence supporting a broader shared abstraction or refactor. In particular, it does not:

- create a generic UI component framework;
- create a repository/provider abstraction before source inspection exists;
- introduce a route registry or navigation service;
- merge authorization or Product Contract validation into presentation state;
- abstract the six destinations into a dynamic plugin system;
- pull product composition forward from P4.08;
- generalize from one shell into a public workspace SDK.

The current small module is easier to replace than a speculative abstraction and remains proportionate to the evidence available at R9.

## 7. Security, privacy and authority disposition

Result: `PASS for the reviewed shell boundary`.

R9 confirms only the shell-level properties that are currently executable:

- unresolved Organization fails closed;
- explicit Organization and attributable actor survive navigation;
- mismatched Organization context does not fall back to another scope;
- cross-Organization reference rejection does not include foreign identifiers;
- presentation state creates neither authorization nor Organizational Authority;
- no protected-content counts or inventories exist at shell level;
- identity/reference values are HTML-escaped before rendering;
- product context is not permission.

R9 does **not** claim that Phase 4 already has complete runtime authorization, policy, classification, purpose, retention, source-access or derived-view security. Those controls become materially exercised by P4.03–P4.09 and remain subject to later R10/R12 hardening.

## 8. Technology, reversibility and ADR disposition

Result: **`PASS — no new ADR required at R9.`**

The current implementation remains an internal Python reference vehicle and zero-dependency HTML rendering adapter. Neither is treated as a stable public contract.

The Phase 4 ADR gate remains armed. It must reopen before material reliance on a durable or externally constraining choice, including:

- stable frontend/runtime framework boundary;
- stable URL/deep-link or public wire schema;
- BFF/API topology;
- authentication/session/IAM enforcement mechanism;
- durable read-model/cache persistence;
- stable cross-product frontend SDK/package surface;
- durable design-system or extension-module contract;
- separately deployable workspace service topology.

R9 itself selects none of these.

## 9. Product Contract and capability disposition

R9 creates no Product Contract and changes no Product Contract lifecycle state.

`WorkspaceProductContext` remains an internal context-only value and does not validate a contract. P4.08 remains the roadmap point for a real Product Contract-backed bounded product entry proof.

R9 creates no `CAP-005 Workspace`, does not promote any workspace behavior into a Platform Capability, and does not change CAP-001 through CAP-004. The retained capability set remains `Incubating / Provisional`.

A successful R9 means only that the current internal workspace boundary is healthy enough to expand. It does not establish:

- lifecycle `Active`;
- operational or production readiness;
- Stable Product Contract status;
- public API/SDK support;
- SLA/support obligations;
- full-platform conformance.

## 10. Functional cross-review

Cross-review is execution-quality evidence, not formal approval or delegated decision authority.

### Iteration 1 — Architecture / public-boundary pressure

Question: has an internal presentation vocabulary already become a stable cross-product interface?

Finding: no current public export, route, endpoint, wire schema or external consumer was found, but this property was previously documented more strongly than it was structurally guarded.

Disposition:

- added package-root non-export regression evidence;
- added transport/framework/storage dependency guards;
- added semantic reference-shape guards;
- kept the shell internal and reversible.

### Iteration 2 — Security / tenant sovereignty

Question: can shell scope checks be mistaken for full resource authorization, especially once richer record surfaces arrive?

Finding: P4.02 correctly fails closed at the presentation scope boundary, but `OrganizationScope` on a navigation reference must not later become a substitute for governed source resolution and current authorization.

Disposition:

- recorded R9-O1 as a mandatory P4.03 source-resolution invariant;
- did not force identifier-string scope interpretation into the shell;
- retained the existing no-metadata-leak cross-Organization failure behavior;
- kept runtime source authorization outside presentation state.

### Iteration 3 — Product / governance

Question: has optional product-entry context become a de facto Product Contract or product orchestration mechanism?

Finding: no. It carries identity/reference context only and grants nothing.

Disposition:

- added an executable structural guard over the context field surface;
- retained P4.08 as the first real Product Contract-backed workspace-entry proof;
- introduced no product-domain behavior or shared capability promotion.

### Iteration 4 — Engineering / maintainability / ADR

Question: does the first visible adapter justify a framework, API, route abstraction, durable read model or shared UI toolkit now?

Finding: no evidence supports any of those commitments. The standard-library implementation remains small, deterministic and replaceable.

Disposition:

- no refactor beyond boundary regression guards;
- no performance optimization without evidence;
- no new RFC or ADR;
- continue with separate bounded P4.03–P4.05 surfaces rather than expanding `workspace_shell.py` into a generic application layer.

No material objection remained after iteration 4.

## 11. Validation

R9 adds structural regression evidence and retains the complete P4.02 behavioral suite.

Final full `Reference Python CI` evidence for the synchronized R9 branch is recorded in the pull request before merge.

## 12. Gate decision

R9 exit criteria are satisfied for the bounded P4.01 + P4.02 workspace boundary:

1. Organization and Actor context remain explicit and fail-closed;
2. presentation/navigation state cannot create authorization, Organizational Authority, approval or canonical mutation;
3. Subject and exact-Version references remain semantically distinct and exact historical references are preserved;
4. optional product context remains context-only and does not replace RFC-0004 Product Contract validation;
5. shared navigation remains product-domain neutral;
6. no accidental stable public API, frontend, route, serialization, IAM/session or durable-read-model boundary has emerged;
7. the shell remains internal and absent from the package-root public surface;
8. no dependency direction or direct governed-mutation bypass was found;
9. the P4.03 source-resolution handoff is explicit, including the R9-O1 scope-consistency requirement;
10. no new ADR, RFC, Product Contract or capability lifecycle change is justified by current evidence.

**Final result: `PASS — R9 complete.`**

## 13. Next canonical action

Proceed to:

> **`P4.03 — Canonical Record / Relationship inspection experience`.**

P4.03 should add a bounded inspection surface without widening the shell into a resolver, authorization engine or public UI protocol. In particular, source dereference must re-evaluate governed Organization/platform scope and current authorization rather than trusting presentation context or identifier syntax as an authority proof.
