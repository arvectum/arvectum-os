# P5.04 — Integration Composition API/Facade Boundary Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` integration-boundary implementation
Constitution: `1.2.0` — `Ratified`
Architecture basis: RFC-0001 `1.0.0`; RFC-0002 `1.0.0`; RFC-0003 `1.0.0`; RFC-0004 `1.0.0`; RFC-0005 `1.0.0` — `Accepted`
Product Contract under composition: P4.08 `Provisional 0.1.0`
Preceding engineering baseline: P5.01/P5.02/R13/P5.03 — `PASS`
ADR disposition: no threshold crossed by the bounded internal/provisional facade
Implementation PR: `#64`
Result: `PASS`

## 1. Purpose

P5.04 extracts the smallest reusable integration-facing composition boundary justified by the proved Phase 5 J1/J2 developer journeys.

The implementation reduces product dependence on implementation-private platform modules while preserving the existing semantic owners for Product Contract declaration validation, dependency/version compatibility, capability admission, workspace presentation and Governed Execution.

P5.04 deliberately does **not** create:

- a second Product Contract or independently editable integration manifest;
- a new authorization, Organizational Authority, approval or data-governance engine;
- a second canonical-state or mutation path;
- capability-specific Document/Knowledge/Search/Audit adapters ahead of P5.08;
- a public or Stable Python SDK/package/module contract;
- a REST, GraphQL, gRPC, RPC or other network API;
- a wire/serialization schema;
- a plugin runtime, registry or distribution protocol;
- a separately deployed integration service;
- a Platform Capability lifecycle transition.

## 2. Canonical constraints revalidated

The work was checked against Constitution `1.2.0`, the RFC Index, Accepted RFC-0001 through RFC-0005 where directly relevant, the ADR index, P5.01, P5.02, R13, P5.03, the P4.08 Provisional Product Contract and the current Phase 5 roadmap.

The implementation preserves these binding semantics:

- Product Contract remains the explicit versioned product/platform boundary;
- P5.02 validation remains derived evidence over the RFC-0004 `ProductContract` semantic owner;
- P5.03 compatibility resolution must succeed for the exact effective Product Contract before facade composition;
- exact Product Contract, Product, dependency, dependency-contract-version and operation continuity remain fail-closed;
- possessing a Product Contract or composed facade grants no Authentication, Authorization, permission, Organizational Authority, Data Governance permission or approval;
- workspace state remains non-authoritative presentation state;
- consequential product execution remains Product Contract-backed Governed Execution under RFC-0005;
- canonical-state, security and authority decisions remain with their existing semantic owners;
- product-domain semantics remain product-owned;
- the current Python facade shape remains internal/provisional implementation evidence.

## 3. Implemented boundary

`reference/python/arvectum_os_ref/integration_composition.py` introduces the bounded P5.04 integration facade.

The facade has one responsibility: compose already-governed integration semantics while preserving exact continuity between them.

It does not duplicate those semantics.

### 3.1 Composition input

`compose_integration_facade()` requires:

- the exact RFC-0004 `ProductContract` object;
- an attributable `ActorContext` in the same Organization;
- the explicit effective Product Contract `GovernedVersionPin`;
- explicit governed dependency/version support evidence used by P5.03.

Construction first invokes the existing P5.02 declaration validator and then the existing P5.03 exact dependency/version resolver.

A facade is not created when either boundary fails closed.

### 3.2 Immutable integration context

`IntegrationCompositionContext` preserves only:

- Organization;
- attributable Actor;
- Product Identity;
- Product version;
- exact Product Contract Version pin.

The context intentionally contains no authorization, authority, approval or capability-lifecycle fields.

It is integration-continuity evidence, not a permission object.

### 3.3 J1 capability admission

`IntegrationCompositionFacade.admit_capability()` verifies that the request preserves the composed Organization, Actor, Product identity/version, dependency identity, dependency contract version and operation.

The facade then delegates actual Product Contract capability admission to the existing `validate_capability_consumption()` semantic owner.

The facade does not implement source authorization, purpose/right/classification handling, canonical read admission or capability-specific behavior. Those remain owned by the existing capability/security surfaces and later P5.08 adapters.

### 3.4 Workspace entry

`IntegrationCompositionFacade.open_workspace()` delegates to the existing `open_workspace_shell()` semantic owner and supplies the exact Product Contract Version in `WorkspaceProductContext`.

The returned workspace remains `PresentationAuthority.NON_AUTHORITATIVE`.

The facade verifies that Product Contract Version continuity was not lost during composition, but it does not turn workspace state into authorization or canonical organizational state.

### 3.5 J2 Governed Execution entry

`IntegrationCompositionFacade.start_governed_execution()` checks only the exact composed Product/dependency/version/operation continuity and delegates consequential execution entry to the existing RFC-0004/RFC-0005 `start_product_governed_execution()` boundary.

The resulting execution preserves the exact Product Contract Version and retains its required gates as unsatisfied until their existing RFC-0003/RFC-0005 semantic owners evaluate them.

P5.04 therefore adds no second canonical-mutation path and no implicit allow/approval path.

## 4. Product-side private-coupling reduction

`reference/python/bounded_product_ref/integration_journeys.py` provides product-owned executable evidence for the proved J1/J2 journeys.

Its only `arvectum_os_ref` import is:

- `arvectum_os_ref.integration_composition`.

The module does not directly import Product Contract runtime internals, capability-consumption internals, workspace internals, Canonical Record internals, Governed Execution internals or operator-action implementation modules.

The product-side helper intentionally treats platform values other than the facade type as opaque values. Product code therefore does not reproduce platform semantic-owner rules to enter the proved journeys.

This does not claim that every future product capability operation is already private-coupling-free. Capability/workspace adapters remain explicit P5.08 scope.

## 5. Semantic-owner preservation

P5.04 is composition, not semantic consolidation.

| Concern | Existing semantic owner retained |
|---|---|
| Product Contract declaration semantics | RFC-0004 `ProductContract` + P5.02 validator |
| dependency/version compatibility | P5.03 resolver over exact RFC-0004 declarations |
| capability admission | existing Product Contract capability-consumption boundary |
| current authorization/data handling | RFC-0003 and existing capability/security owners |
| workspace presentation authority | existing workspace shell |
| consequential execution | RFC-0005 Product Contract-backed Governed Execution |
| canonical state and exact version semantics | RFC-0002 / existing canonical owners |
| product task/business meaning | product-owned code |

The facade owns only continuity between these boundaries.

It does not become a policy decision point, canonical store, authorization layer, capability lifecycle catalog or domain model.

## 6. Security and authority separation

Successful facade construction means only:

- the Product Contract declaration is structurally valid under P5.02;
- the exact dependency/version reliance is compatible under P5.03;
- the Actor and Product Contract share the required Organization scope.

It does **not** mean that an Actor:

- is authenticated to a required assurance level;
- is authorized to access a governed source;
- has Organizational Authority;
- satisfies Data Governance constraints;
- has consequential approval;
- may mutate canonical state;
- activates or promotes a Platform Capability.

J1 continues through existing current-access/capability checks. J2 starts with required gates unsatisfied and must proceed through Governed Execution.

Cross-Organization or post-composition Product/dependency/version/operation drift fails closed.

## 7. Product/platform ownership

No product-specific disposition, task title, business workflow meaning or domain rule is added to `arvectum_os_ref` by P5.04.

The facade is domain-neutral and works from the Product Contract's declared identities, versions and operations.

The bounded product journey module remains under `bounded_product_ref` and cannot redefine the shared platform semantics.

The shared platform module does not import the bounded product package.

## 8. Stable/public boundary and ADR review

Result: `PASS — no ADR threshold crossed`.

P5.04 does not select or stabilize:

- a public Python import path;
- a language-specific SDK compatibility commitment;
- package distribution/versioning policy;
- REST/GraphQL/gRPC/RPC endpoints;
- request/response or wire schema;
- JSON/YAML/protobuf/OpenAPI as the Product Contract/facade representation;
- network/service topology;
- plugin loading or registry behavior;
- production support or compatibility guarantees.

The current `IntegrationCompositionFacade` class and module name are internal/provisional reference implementation evidence.

A later decision to make any facade/API/package/network/wire surface externally supported or Stable must re-open the applicable architecture/governance/ADR gate with compatibility, migration and support evidence.

## 9. Executable evidence

P5.04 adds:

- `reference/python/arvectum_os_ref/integration_composition.py`;
- `reference/python/bounded_product_ref/integration_journeys.py`;
- `reference/python/tests/test_p5_04_integration_composition_facade.py`.

The focused suite contains 12 regression/fitness cases covering:

1. exact P5.02 declaration and P5.03 compatibility evidence is composed;
2. missing governed dependency evidence fails before facade construction;
3. effective Product Contract Version drift fails before facade construction;
4. J1 capability admission preserves exact Product Contract/dependency/version/operation continuity;
5. dependency-version drift after facade construction fails closed;
6. workspace entry remains non-authoritative and preserves exact Product Contract Version;
7. the product J1 helper enters only through the facade and preserves admission evidence;
8. J2 Governed Execution preserves the exact Product Contract and begins with required gates unsatisfied;
9. the product J2 helper reaches Governed Execution only through the facade;
10. facade context/declaration/compatibility evidence is not an authority or capability-lifecycle source;
11. the product journey module has exactly one Arvectum OS import boundary: the integration facade;
12. the facade remains internal/provisional and selects no public transport/serialization stack.

PR `#64` was opened for the P5.04 branch.

Hosted `Reference Python CI` run **#218** completed successfully for implementation/test head `cfb666cf73b883e05cbb9b502c4f3fcca6a148aa` / PR merge ref `1194aabb8522889e58bdbb9af5d09ddff95f42dc`.

Observed environment and result:

- CPython `3.12.13`;
- Ubuntu `24.04.4`;
- full reference suite: **615 tests**;
- result: **OK**.

This includes the new P5.04 tests and the existing R10/R11/R12/R13 regression guards.

## 10. Functional cross-review iterations

### Iteration 1 — boundary-size review

Finding: moving capability-specific Document/Knowledge/Search/Audit composition into P5.04 would pre-empt P5.08 and enlarge the facade beyond current evidence.

Disposition: keep P5.04 limited to declaration/resolution continuity, capability admission, workspace entry and Governed Execution entry. Capability-specific adapters remain P5.08.

### Iteration 2 — semantic-owner review

Finding: a facade that reimplemented Product Contract validation, compatibility, source authorization or canonical-state rules would become a competing semantic owner.

Disposition: delegate each operation to the existing owner and keep facade-specific logic limited to exact composition continuity.

### Iteration 3 — product coupling review

Finding: reusing `bounded_product_ref.task_composition` as the reusable facade would preserve its many direct implementation imports and product-specific task semantics.

Disposition: do not promote that historical product composition module. Add a separate domain-neutral platform facade and a product-owned journey proof that imports only that facade.

### Iteration 4 — authority review

Finding: a convenient facade could accidentally be interpreted as integration admission or permission.

Disposition: facade construction/admission evidence contains no authority grants. J1 delegates current access checks; J2 starts with gates unresolved. Product Contract/facade possession satisfies none of them.

### Iteration 5 — public API / ADR review

Finding: naming the work item `API/facade` could accidentally stabilize the current Python class/module shape.

Disposition: explicitly classify all P5.04 surfaces as internal/provisional and avoid network, package, wire, serialization or externally supported compatibility choices. No ADR threshold is crossed.

No remaining material objection was identified after iteration 5 and the full hosted suite passed.

## 11. Exit evidence

- product-owned P5.04 J1/J2 journey code imports no private runtime/capability/workspace implementation modules — `PASS`;
- the product journey sees Arvectum OS through one integration facade module — `PASS`;
- facade construction consumes exact P5.02/P5.03 Product Contract semantics — `PASS`;
- exact Product Contract/Product/dependency/version/operation continuity remains fail-closed — `PASS`;
- capability admission delegates to its existing semantic owner — `PASS`;
- workspace presentation authority remains non-authoritative — `PASS`;
- consequential execution delegates to Product Contract-backed Governed Execution — `PASS`;
- facade grants no Authorization or Organizational Authority — `PASS`;
- product-domain semantics remain product-owned — `PASS`;
- no Stable/public language/network/wire/package boundary is created — `PASS`;
- no new RFC or ADR threshold is crossed — `PASS`;
- focused executable regression evidence is committed — `PASS`;
- hosted full reference CI — `PASS` (`Reference Python CI #218`, 615 tests, OK).

## 12. Final disposition

**PASS — P5.04 is complete for the declared internal/provisional integration composition facade boundary.**

The implementation satisfies the current Phase 5 exit evidence without stabilizing the P4.08 Product Contract, promoting a Platform Capability, establishing production readiness, expanding conformance, or creating public/SLA/support/commercial commitments.

The facade is now sufficient as the integration-facing composition seam for the proved J1/J2 journeys. P5.08 remains responsible for capability/workspace-specific adapters, so P5.04 does not claim complete private-coupling elimination for all future capability operations.

Next canonical work item after roadmap synchronization:

> **P5.05 — Scaffolding/templates + local integration harness.**
