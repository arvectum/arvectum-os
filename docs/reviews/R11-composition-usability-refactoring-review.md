# R11 — Composition / Usability Refactoring Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` boundary review
Engineering gate: `R11 — Composition / Usability Refactoring Review`
Phase: `Phase 4 — Workspace / Operator Experience`
Result: **`PASS — P4.02–P4.08 composition remains domain-neutral on the platform side, product-owned on the product side, fail-closed across Product Contract/dependency/Actor/task-target continuity, non-authoritative in presentation, and unable to bypass R10/Governed Execution. Repeated source-authorization matching is real but remains bounded local duplication until P4.09/P4.10 provide evidence for a safe shared security abstraction; no ADR threshold is crossed.`**

## 1. Purpose

R11 is the mandatory engineering refactoring/usability gate after the first real Product Contract-backed cross-capability composition proof in P4.08 and before substantive P4.09 security/right/authority-safe UX work.

The review asks whether the accumulated P4.02–P4.08 operator experience has now produced enough evidence to simplify repeated internal patterns without accidentally stabilizing a public API, frontend architecture, Product Contract substitute, IAM/policy layer or product-domain platform abstraction.

R11 reviews:

- repeated Organization/Actor/source-access/presentation composition patterns;
- product-domain leakage into shared workspace code;
- exact Product Contract, dependency contract, Actor, Organization and task-target continuity;
- bypass risk around current source authorization, R10 operator safety and Governed Execution;
- composed usability around exact Version, authority, provenance, validation and approval distinctions;
- the P4.08 Provisional Product Contract review condition;
- ADR threshold pressure from any concrete frontend/API/serialization/IAM/storage choice;
- deterministic-testability implications of the separately tracked hosted CI issue #54.

R11 is not a capability-admission decision, Product Contract stabilization, public API/SDK decision, production-readiness approval, conformance claim or commercial commitment.

## 2. Canonical authority checked

R11 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral shared platform behavior, product/platform separation, Governed Execution, authority modes, security/isolation, portability and no accidental public interfaces;
4. RFC-0002 — stable Subject Identity, immutable exact Version Identity, fail-closed ambiguity handling, non-authoritative projections and exact-version consequential reliance;
5. RFC-0003 — explicit Organization scope, deny-by-default access, separation of identity/authentication/authorization/Organizational Authority/data governance, and fail-closed unresolved scope;
6. RFC-0004 — explicit Product Contract boundary, exact contract/dependency declarations, hidden-coupling prohibition and product-owned domain semantics;
7. RFC-0005 — exact governed input/Product Contract pinning, separate authorization/authority/approval gates and consequential mutation only through Governed Execution;
8. RFC-0006 — provenance/evidence semantics, non-authoritative telemetry/projections and no silent evidence loss;
9. RFC-0007 — Memory/Knowledge lifecycle distinctions, retrieval non-authority, freshness/exact-version reliance and product-owned domain knowledge;
10. RFC-0008 — Document/Artifact/version/authority/provenance distinctions, non-authoritative derived projections and explicit Product Contract artifact surfaces;
11. `docs/adrs/README.md` — no applicable Accepted ADR constrains the bounded internal Phase 4 composition;
12. approved `DECISION-2026-08-08 — Engineering Quality and Refactoring Gates`;
13. P4.02 through P4.08 implementation/review evidence, including R9 and R10;
14. `P4.08 Bounded Product Entry Product Contract` — `Provisional 0.1.0`, with R11 as its explicit review condition;
15. canonical Roadmap `2.20.0` and Phase 4 roadmap `1.10.0` at R11 start;
16. main commit `9f1c080e9279d510337214d28816769327b8dbe0`, which completed P4.08 and advanced the canonical action to R11;
17. GitHub issue #54, which remains an external hosted-runner provisioning gap rather than an architectural exception.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

The Decision Authority Policy remains non-normative while `Proposed`; R11 does not depend on unapproved delegated authority.

## 3. Composition boundary under review

The first real composition currently has this bounded dependency direction:

```text
bounded_product_ref (product-owned)
        |
        | exact Provisional Product Contract
        | exact capability admissions
        v
WorkspaceProductContext / WorkspaceShellState
        |
        +--> P4.06 Document / Artifact surface (CAP-001)
        |
        +--> P4.07 Memory / Knowledge surface (CAP-002)
        |
        +--> product-owned transient task disposition
        |
        `--> Product Contract-backed Governed Execution
                 |
                 v
              R10 operator_safety
                 |
                 v
              P4.05 action adapter
                 |
                 v
              existing runtime consistency commit path
```

The product owns task identity, task title, task disposition and task-state semantics. The platform owns only the already established domain-neutral workspace, Canonical Record/version, capability, Product Contract, Governed Execution and operator-safety semantics.

## 4. Review findings

### R11-F1 — Product-domain meaning remains product-owned

Severity: `No material finding`
Result: `PASS`

`bounded_product_ref` remains outside `arvectum_os_ref`. Product tokens and behaviors such as:

- `product.bounded-review-task`;
- `p4.08.record-task-decision`;
- `Needs review`;
- `Ready to proceed`;
- `Declined`;

remain in the bounded product reference and are not imported or reproduced inside the shared platform package.

The platform package does not import `bounded_product_ref`.

R11 therefore finds no evidence that P4.08 has turned the workspace into a generic product orchestrator or promoted product workflow meaning into shared platform semantics.

### R11-F2 — Composition preserves semantic owners instead of flattening them

Severity: `No material finding`
Result: `PASS`

`ProductTaskContextView` composes the existing shared result types:

- `DocumentWorkspaceResult`;
- `KnowledgeWorkspaceResult`.

It does not copy their authority, provenance, lifecycle, freshness, approval or exact-version semantics into a new product-owned read model.

This is important both architecturally and for usability. The operator-facing meaning remains traceable to the shared semantic owner instead of being reduced to ambiguous fields such as a generic `approved`, `current`, `trusted` or `allowed` boolean.

The composed Document surface still distinguishes, where applicable:

- Subject versus exact displayed Version;
- Canonical Head versus exact Version reference basis;
- authority mode, authority scope and authoritative-source meaning;
- Artifact identity and derivation/source-artifact provenance;
- exact governed reliance availability.

The composed Knowledge surface still distinguishes:

- Observation/Memory/Candidate/Knowledge role;
- exact Version where applicable;
- provenance references;
- freshness and lifecycle state;
- authority mode/scope;
- validation result;
- approval reference;
- exact consequential reliance state.

The execution/action surface still exposes gate kind, outcome, exact decision evidence, Workflow/material-input/Product Contract pins, unresolved gates and denied gates separately.

R11 therefore finds no usability regression in which composition collapses exact Version, authority, provenance, validation and approval into one ambiguous status.

### R11-F3 — Product Contract/dependency/Actor/Organization continuity remains fail-closed

Severity: `No material finding`
Result: `PASS`

P4.08 preserves the exact entry boundary after workspace creation rather than treating successful entry as a permanent capability grant.

A composed capability request is rejected if any of the following drift:

- current Actor;
- current Organization;
- Product identity;
- Product version;
- declared Product Contract boundary mechanism;
- dependency identity;
- dependency operation;
- dependency contract version;
- exact Product Contract Version under which the capability was admitted.

A consequential product execution is separately rejected if it does not preserve:

- workspace Organization;
- workspace Actor;
- exact Product Contract Version;
- declared `record-task-decision` operation;
- exactly the current product-owned task Subject/type as its material target.

The candidate canonical state is independently checked against the same product task Subject/type/Organization.

Successful Product Contract validation therefore remains context/admission evidence only; it does not become authorization, Organizational Authority, approval or an unlimited capability token.

### R11-F4 — No consequential bypass of R10 or Governed Execution was found

Severity: `No material finding`
Result: `PASS`

The product composition imports and invokes only:

- `prepare_operator_canonical_mutation_action`;
- `execute_operator_canonical_mutation_action`.

It does not import the lower-level P4.05 `execution_action_experience` adapter directly and does not invoke its lower-level canonical mutation preparation/execution functions.

Product action preparation first revalidates exact Product Contract/Actor/task-target continuity. R10 then pins and rechecks the exact current source-authorization decision used for inspection. The existing P4.05/runtime path remains the only exercised consequential canonical mutation path.

No alternate product-side database, internal table, direct canonical mutation helper, hidden route, private Event stream or presentation-state commit path was found.

### R11-F5 — Repeated source-authorization matching is real, but extraction is not yet justified

Severity: `Refactoring watch item — bounded, not blocking`
Disposition: **`retain explicit local matching through P4.09/P4.10; do not create a new shared authorization framework at R11`**

R11 confirms the repetition anticipated by R10. P4.03, P4.04, P4.05, P4.06, P4.07 and R10 each consume the same internal `CurrentSourceAuthorization` evidence shape and match, in their local boundary, the current:

- Organization;
- actual Principal;
- represented Principal when present;
- protected resource Subject;
- unique allow decision.

This is genuine repeated implementation structure. It is therefore a valid refactoring candidate, not speculative resemblance.

However, R11 does **not** extract it into a new common `authorization service`, `workspace authorization framework`, `policy engine` or product-composition abstraction for four reasons:

1. `CurrentSourceAuthorization` is still an internal reference/test evidence shape, not an Accepted IAM/PDP public contract;
2. each consuming surface has distinct surrounding semantics for source resolution, handling constraints, freshness, exact reliance or stale-presentation action safety;
3. centralizing the match now could make a presentation helper look like the owner of authorization policy, contrary to RFC-0003 separation of concerns;
4. P4.09 and P4.10 are the next tasks that deliberately stress cross-capability rights, minimization, stale/revoked authority and operator usability, and therefore provide the right evidence for whether a shared *decision-consumption* helper is safe and useful.

The duplication is consequently accepted as **bounded duplication with an explicit review trigger**, not as an endorsed permanent architecture.

A later refactor may extract a narrow internal helper only if it remains a consumer of already-produced authorization decisions, preserves each semantic owner's independent data-governance/freshness/exact-reliance checks, and does not become a new authorization-policy source.

### R11-F6 — No stable/durable implementation choice crosses the ADR threshold

Severity: `No material finding`
Result: `PASS — no new ADR required at R11`

The reviewed composition still selects no materially relied-upon:

- frontend/runtime framework;
- public route/deep-link schema;
- REST/GraphQL/gRPC/BFF boundary;
- stable wire/serialization format;
- authentication/session/IAM provider or policy engine;
- durable workspace/read-model/cache store;
- durable search/vector/RAG technology;
- document/object-store topology;
- stable design-system/package compatibility contract;
- separately deployable workspace service topology.

The current Python reference modules remain internal, reversible executable evidence. R11 does not turn module names, dataclass shapes or operation tokens into Stable/public compatibility commitments.

The ADR gate remains armed for later durable choices.

### R11-F7 — P4.08 Product Contract review condition is satisfied without stabilization

Severity: `No material finding`
Result: `PASS — remain Provisional 0.1.0`

R11 fulfills the explicit review condition in `P4.08 Bounded Product Entry Product Contract`.

The review found no material contract defect requiring a new Product Contract version and no evidence supporting promotion to `Stable`.

The existing `Provisional 0.1.0` contract is therefore left unchanged. This is intentional: an admitted/versioned Product Contract is not edited merely to record that a review occurred. Any material later change must create the appropriate new immutable Provisional version or follow the RFC-0004 stabilization path.

No CAP-001/CAP-002 lifecycle state changes.

### R11-F8 — Hosted CI issue #54 remains a tooling gap, not architecture authority

Severity: `Engineering tooling gap — externally tracked`
Disposition: `does not block the scoped R11 architecture/refactoring decision; remains relevant to P4.10 deterministic-testability evidence`

Issue #54 remains open because GitHub-hosted `Reference Python CI` fails during runner/account provisioning before the first workflow step.

R11 does not reinterpret runner availability as architectural evidence. It also does not claim a green R11 hosted CI run.

Because R11 changes no runtime implementation module and adds only structural regression evidence plus canonical review/roadmap state, the scoped architecture/refactoring result can be decided independently. P4.10 must still treat deterministic execution of critical operator-state tests as a real quality requirement and must not close that requirement by documentation alone.

## 5. Executable R11 hardening evidence

R11 adds:

- `reference/python/tests/test_r11_composition_usability_refactoring_review.py`.

The guard verifies that:

1. bounded product-domain task/disposition/operation semantics remain outside the shared platform package;
2. `ProductTaskContextView` composes the existing Document and Knowledge shared result types rather than flattening their semantic state;
3. Document, Knowledge and Execution shared surfaces retain explicit exact-Version, authority, provenance, freshness/validation/approval and gate distinctions;
4. post-entry Product Contract/dependency/Actor/Organization/product/task-target continuity remains represented by explicit fail-closed guards;
5. consequential product actions route only through R10 operator-safety wrappers and not directly into the lower-level P4.05 action adapter;
6. the repeated source-access matching remains visible as local consumption of `CurrentSourceAuthorization` rather than being silently replaced by a speculative new authorization framework;
7. the reviewed composition imports no concrete durable frontend/API/IAM/storage framework that would silently cross the ADR gate.

The new test file was syntax-validated while preparing R11. Hosted execution remains subject to issue #54; no green hosted run is claimed by this review.

## 6. Refactoring disposition

Result: **`PASS — bounded duplication retained; no runtime refactor required at R11.`**

R11 considered three possible refactoring directions:

1. **Create a generic cross-capability task/context composer** — rejected. The first real task semantics are product-owned and one bounded product is insufficient evidence for a shared orchestrator.
2. **Create a shared authorization/presentation framework** — rejected at this gate. The repeated decision-matching structure is real, but ownership and interaction with data-governance/freshness/exact-reliance semantics are not yet sufficiently validated.
3. **Flatten shared capability views into one ergonomic product read model** — rejected. That would obscure exact Version/authority/provenance/approval semantics and create a second semantic owner.

The preferred current design is therefore deliberately small:

- reuse shared capability views as composed values;
- keep product task meaning product-owned;
- preserve exact Contract/dependency continuity explicitly;
- preserve R10 as the action-composition safety choke point;
- let P4.09/P4.10 generate the next evidence before extracting any security-critical common helper.

This follows validated reuse over speculative generality.

## 7. Usability disposition

Result: `PASS for semantic usability; visual/accessibility refinement remains P4.09/P4.10 scope`.

The first composition is understandable at the semantic boundary because it does not manufacture ambiguous convenience state. An operator or adapter can still determine, from the owning shared surfaces:

- which logical object and exact Version are being viewed;
- whether the reference is Head/current context or an exact historical Version;
- where authority comes from;
- which provenance/source links are carried;
- whether Knowledge is current/stale/review-required for exact reliance;
- whether validation exists separately from approval;
- which Governed Execution gates are unresolved, allowed or denied;
- whether a product decision is merely transient product-owned state;
- why a consequential action is blocked when Contract/access/gate continuity no longer holds.

R11 does not claim polished visual usability or accessibility. P4.09 must harden authority-safe labels/omissions/stale-state behavior, and P4.10 must provide executable accessibility/usability evidence over core operator journeys.

## 8. Security, privacy and authority disposition

Result: `PASS for the reviewed composition boundary`.

R11 confirms that:

- Product Contract possession is not permission;
- current source authorization remains separately evaluated by each source/capability surface;
- purpose/right/classification handling remains separate from source visibility;
- Product Contract, source authorization, Organizational Authority and approval remain distinct;
- protected omission does not become a product-side count/preview reconstruction path;
- source-access replacement/revocation/ambiguity invalidates prepared action continuity through R10;
- no cross-Organization fallback is introduced;
- presentation remains non-authoritative;
- product-domain decisions do not become canonical merely because they were made from governed context.

R11 introduces no weaker security or privacy shortcut.

## 9. Product / platform disposition

Result: `PASS`.

The bounded reference product remains evidence of product/platform composition, not part of the shared platform domain model.

R11 creates no new Platform Capability and does not promote CAP-001 through CAP-004. It does not create `CAP-005 Workspace` or a generic task/orchestration capability.

The P4.08 Product Contract remains `Provisional 0.1.0`. R11 does not create Stable/public API, SDK, route or support obligations.

## 10. Functional cross-review

Cross-review is engineering-quality evidence, not a substitute for formal authority or Product Contract lifecycle governance.

### Iteration 1 — Architecture / product-platform boundary

Question: has the first real product-backed composition created a generic product orchestrator or leaked task semantics into shared platform code?

Finding: no. Product tokens, task types, dispositions and task-state operation remain under `bounded_product_ref`; shared platform code has no reverse dependency.

Disposition: retain product ownership; do not extract a generic composition framework.

### Iteration 2 — Security / source-authorization repetition

Question: is the repeated current source-authorization matcher now proven enough to centralize?

Finding: the matching structure is genuinely repeated across P4.03–P4.07 and R10, but the surrounding semantics differ and the current evidence shape is not a public IAM/policy contract.

Disposition: record bounded duplication and a P4.09/P4.10 review trigger; do not create a new authorization owner.

### Iteration 3 — Governed Execution / bypass analysis

Question: can product composition bypass exact Product Contract continuity, R10 source-access freshness or the existing Governed Execution mutation path?

Finding: no viable path found. Product wrappers recheck Contract/Actor/task-target continuity and delegate consequential preparation/execution only through R10.

Disposition: add structural regression evidence around the R10-only action path and continuity guards.

### Iteration 4 — Usability / semantic ambiguity

Question: does composing Document and Knowledge context hide exact Version, authority, provenance, freshness, validation or approval meaning behind simplified product state?

Finding: no. The product view carries the owning shared result objects directly; it does not flatten those distinctions into convenience booleans or duplicate semantic state.

Disposition: preserve semantic-owner composition. Defer visual/accessibility refinement to P4.09/P4.10 rather than introducing a new read-model contract.

### Iteration 5 — ADR / portability / deterministic testability

Question: has composition selected a durable frontend/API/IAM/storage technology or does CI issue #54 require an architectural workaround?

Finding: no durable technology choice is selected. Issue #54 is a hosted execution/tooling problem before workflow steps begin and should not be converted into application architecture.

Disposition: no ADR; add deterministic structural regression evidence; keep #54 explicitly open for execution infrastructure and P4.10 quality evidence.

No material objection remained after iteration 5.

## 11. Validation

Validation evidence for R11 consists of:

- canonical Constitution/RFC/ADR/Product Contract/roadmap review;
- direct source review of P4.02–P4.08 composition and action paths;
- review of the P4.08 negative-path tests and R10 hardening evidence already present on main;
- new R11 structural regression test covering product leakage, semantic-owner preservation, continuity, action bypass and ADR-pressure boundaries;
- syntax validation of the new test module during review preparation.

A green GitHub-hosted R11 test run is **not** claimed because issue #54 remains unresolved at runner provisioning.

R11 does not modify runtime implementation behavior. Its code change is a regression guard over the already reviewed composition.

## 12. R11 completion decision

**R11 passes.**

The accumulated P4.02–P4.08 implementation is healthy enough to proceed to P4.09 without a runtime refactor or new ADR.

Completion means only that, within the current bounded reference scope:

- first product-backed composition preserves product/platform boundaries;
- exact Contract/dependency/Actor/task-target continuity remains fail-closed;
- source authorization, data-governance handling, Organizational Authority and approval remain distinct;
- product consequential action cannot bypass R10/Governed Execution through the reviewed path;
- exact Version, authority, provenance and approval semantics remain available through composed shared surfaces;
- repeated source-authorization matching is consciously retained as bounded duplication pending stronger P4.09/P4.10 evidence;
- the P4.08 Product Contract has satisfied its R11 review condition and remains `Provisional 0.1.0`;
- no stable/durable choice requires an ADR;
- no capability lifecycle, conformance, operational-readiness or commercial status changes.

The next canonical action is **`P4.09 — Security, rights, minimization and authority-safe UX`**.
