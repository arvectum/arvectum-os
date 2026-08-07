# RFC-0004: Product Contract, Product Experiment and Extension Model

Status: `Proposed`
Version: `0.3.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `product_contract`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`
Forward-compatible with: `RFC-0003 v0.2.0` (`Proposed`, non-normative)
Supersedes: `RFC-0004 v0.2.0` working proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS is a shared platform beneath products, while products remain architecturally responsible for domain meaning, domain workflows, knowledge, validation, integrations, user experience, commercial packaging and bounded Product Experiments until a separate governed decision promotes reusable responsibility into the platform.

RFC-0001 establishes that products which consume platform capabilities, emit events into shared platform history, or read or change canonical platform state must interact through a versioned Product Contract. It also permits entirely product-local bounded experiments to proceed without a Product Contract when they do not depend on platform capabilities, shared platform history or canonical platform state.

This RFC defines the domain-neutral contract and extension model required to make that boundary executable without turning Arvectum OS into a universal product schema, plugin framework or business-process catalog.

The model is built around six rules:

1. **A Product Contract declares the product/platform boundary, not the internal architecture of the product.**
2. **A Product Contract is required when a product or experiment relies on governed platform behavior or shared canonical state.**
3. **Every declared dependency has an accountable provider, consumer, version/compatibility rule and failure boundary proportionate to consequence.**
4. **Extensions are registered, versioned and constrained participants; registration never creates permission, organizational authority or platform status by itself.**
5. **Product Experiments remain product-responsible until a separate governed promotion decision changes architectural responsibility.**
6. **Products may not obtain platform behavior through accidental coupling, undocumented conventions, direct internal database access or internal imports that bypass declared contracts.**

This RFC defines:

- Product Contract identity, lifecycle and version semantics;
- `Provisional` and `Stable` contract states;
- declaration of platform capability dependencies;
- product-owned domain types and schemas at the boundary;
- canonical-state and authority responsibilities;
- operations and governed mutation declarations;
- event and artifact declarations;
- security, authority, privacy and organization-scope constraints at the boundary;
- extension registration and execution boundaries;
- adapter and connector responsibilities;
- compatibility, migration, deprecation and support semantics;
- Product Experiment entry, review and exit semantics;
- promotion from product-local experiment to platform incubation;
- contract discovery and validation requirements;
- conformance and fitness tests.

This RFC does **not** define the detailed identity/security/privacy architecture proposed by RFC-0003, complete Governed Execution semantics reserved for RFC-0005, complete event/provenance semantics reserved for RFC-0006, or memory/knowledge promotion semantics reserved for RFC-0007.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 `1.0.0` and RFC-0002 `1.0.0` without changing their architectural laws.

The most relevant constitutional requirements are:

- shared capabilities belong in Arvectum OS only when reuse is validated, strategically required or necessary for shared governance, security, identity, provenance or interoperability;
- bounded reversible product experiments may precede platform generalization;
- product-local experiments must have an explicit path to promotion, containment or retirement;
- shared platform foundations and contracts remain domain-neutral;
- products specialize meaning while technologies execute meaning;
- significant governed objects are versioned and attributable;
- architecture precedes cross-cutting irreversible implementation, while bounded reversible experimentation may proceed earlier;
- security, privacy, organizational control, portability and human governance are structural requirements;
- organizational value and proportionality take precedence over ceremony and speculative generality.

RFC-0001 additionally requires that:

- a Product Experiment using platform capabilities, shared platform history or canonical platform state use a minimal `Provisional` Product Contract;
- products depend on platform behavior only through declared contracts;
- products do not access platform internals through undocumented conventions, direct database coupling or internal imports;
- Product Contracts declare applicable product identity/version/owner, capability dependencies, domain record and relationship types, authority modes, schemas/workflows, validators/standards/policies, events/artifacts, permissions/classification/authority requirements, approval gates, extensions/adapters, portability/export, retention/deletion, migration/support status and provisional/incubating dependencies;
- extensions are registered, versioned and declare compatibility, permissions, data handling, inputs, outputs, events, failure behavior, portability and deprecation proportionate to scope;
- Product Experiments remain product-responsible until a separate promotion decision;
- commercial claims must not represent provisional product or platform behavior as stable supported platform capability.

RFC-0002 additionally requires that:

- Identity is a stable non-versioned reference primitive and does not itself carry mutable permission or authority;
- Canonical Records use stable Subject Identity plus immutable Version Identity;
- consequential reliance on changeable governed state pins exact versions;
- Typed Relationships do not themselves grant access or authority;
- external-authority semantics remain explicit and do not create competing Arvectum OS authority;
- governance-significant product/platform contract state can be represented through Canonical Records where it is significant.

Where this RFC conflicts with the Constitution, RFC-0001 or RFC-0002, the higher-authority source prevails.

### 2.1 RFC-0003 Status Boundary

RFC-0003 `0.2.0` is `Proposed` and therefore has no normative force at the time of this RFC proposal.

This RFC is designed to remain compatible with RFC-0003 concepts such as deny-by-default authorization, organization scope, actor context, purpose-aware processing and separation of technical permission from organizational authority. Those concepts are used here only where already required by the Constitution or Accepted RFC-0001/RFC-0002, or are explicitly marked as forward-compatibility considerations.

If RFC-0003 is later Accepted with materially different Product Contract implications, this RFC proposal **MUST** be reviewed before acceptance.

## 3. Scope

This RFC defines the shared architecture for:

- when a Product Contract is required;
- Product Contract identity, ownership, status and versions;
- minimal `Provisional` Product Contracts for Product Experiments;
- `Stable` Product Contracts for supported product/platform integration;
- platform capability dependency declarations;
- product-owned domain schema and semantic declarations at the boundary;
- canonical-state reads and writes;
- authority-mode and external-authority declarations relevant to product interaction;
- governed operations exposed across the product/platform boundary;
- declared event and artifact exchange;
- security, authority, classification, organization scope and data-handling requirements at the boundary;
- extension identity, registration, compatibility, permissions, inputs, outputs and failure behavior;
- adapters and external-system connectors used by products through the platform boundary;
- compatibility, migration, deprecation, retirement and support semantics;
- Product Experiment lifecycle and exit paths;
- promotion of reusable product mechanisms into platform capability incubation;
- validation, discovery and conformance of Product Contracts.

## 4. Non-goals

This RFC does not define:

- the internal architecture of any product;
- a universal product domain model;
- tender, finance, CRM, marketing, legal or other business schemas;
- a universal role or entitlement catalog;
- a mandatory API protocol, RPC mechanism, message broker or plugin runtime;
- a specific manifest serialization format;
- repository layout or package-manager conventions;
- detailed IAM, authentication, authorization or cryptographic mechanisms;
- complete Governed Execution semantics or workflow state machines;
- complete Event taxonomy, delivery semantics, provenance schema or observability backend;
- memory, knowledge or governed-learning promotion semantics;
- a mandatory microservice architecture;
- pricing, packaging, SLA, support plan or customer contract terms;
- automatic legal rights for cross-organization data or knowledge reuse;
- automatic promotion of successful product code into the platform;
- automatic activation of capabilities merely because a Product Contract references them.

These subjects belong to later RFCs, ADRs, policies, standards, Product Contracts, product decisions, legal agreements or implementation choices.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Product and Platform Responsibility

### 6.1 Product Responsibility

A Product is architecturally responsible by default for its:

- domain concepts and semantics;
- domain schemas and relationship types;
- domain workflows and validations;
- product-specific standards and risk rules;
- domain knowledge and prompts;
- product-owned integrations;
- user experience;
- commercial behavior and packaging;
- Product Experiments;
- product-local technical choices.

A Product Contract **MUST NOT** transfer those responsibilities to the platform merely by declaring them.

### 6.2 Platform Responsibility

Arvectum OS is architecturally responsible for domain-neutral shared foundations, contracts and capabilities that have been admitted under Accepted platform lifecycle rules.

A Product Contract **MUST NOT** make a product-local mechanism a Platform Capability, change a capability lifecycle state, or create a new shared-platform obligation without the separate decision required by RFC-0001.

### 6.3 Boundary Principle

The Product Contract records the governed interaction surface between the two responsibility domains.

It **MUST** describe only what the platform and product need to know to interoperate, govern access and responsibility, preserve compatibility and reconstruct consequential interaction.

It **SHOULD NOT** duplicate product-internal implementation detail that has no boundary consequence.

## 7. When a Product Contract Is Required

### 7.1 No Contract Required for Fully Product-local Experiment

A Product Experiment **MAY** operate without a Product Contract only when all are true:

1. it does not consume a Platform Capability;
2. it does not read canonical platform state;
3. it does not change canonical platform state;
4. it does not emit Events into shared platform history;
5. it does not depend on a shared platform contract for identity, governed assets, execution or interoperability;
6. it remains within applicable security, privacy, legal, contractual and data-integrity controls.

### 7.2 Contract Required at Platform Boundary

A Product or Product Experiment **MUST** have a Product Contract before it relies on any of the following:

- a Platform Capability contract;
- canonical platform records or relationships;
- shared platform Events or execution history;
- governed platform-side mutation;
- platform-managed extension execution;
- a platform adapter or connector whose behavior forms part of the product/platform boundary;
- another product through a shared platform record, Event or explicit shared contract.

### 7.3 Minimality

The required Product Contract **MUST** be proportionate to the interaction.

A narrow experiment consuming one read-only platform capability does not need the same declaration depth as a stable product that performs consequential canonical mutations, emits shared events and relies on multiple active capabilities.

## 8. Product Contract as a Governed Subject

### 8.1 Identity and Version

A Product Contract **MUST** have:

- a stable Product Contract Subject Identity;
- an immutable Product Contract Version Identity for every admitted governed version;
- a human-readable contract name;
- the Product or Product Experiment identity it governs;
- an accountable architectural owner;
- contract lifecycle status;
- creation and version provenance.

A Product Contract version that is admitted as significant governed state **MUST** use the Canonical Record semantics of RFC-0002.

### 8.2 Contract Version Immutability

An admitted Product Contract version **MUST NOT** be mutated.

Changes **MUST** create a new immutable version under the same Product Contract Subject Identity while the governed boundary remains the same semantic contract lineage.

A materially different boundary that no longer represents the same contract subject **MAY** require a new Product Contract Subject Identity.

### 8.3 Effective Version

A Product Contract **MUST** distinguish current lineage head from the version effective for a specific deployment, execution or compatibility context where they differ.

Consequential execution that relies on a changeable Product Contract **MUST** preserve the exact effective Product Contract Version Identity or an equivalent immutable version reference in the applicable execution evidence.

## 9. Product Contract Lifecycle

A Product Contract has one of the following lifecycle states:

```text
Draft → Provisional → Stable → Deprecated → Retired
```

### 9.1 Draft

`Draft` is incomplete or not yet authorized for governed platform reliance.

A `Draft` contract **MUST NOT** be used as the sole basis for consequential production interaction.

### 9.2 Provisional

`Provisional` is the normal state for bounded Product Experiments and early integrations.

A `Provisional` Product Contract **MUST** declare:

- owner;
- bounded scope;
- required platform interaction;
- known compatibility assumptions;
- security/data/authority constraints relevant to the interaction;
- failure behavior;
- review date;
- exit path: stabilize, revise, contain, replace or retire.

A `Provisional` contract **MAY** use lighter compatibility and support commitments when those limitations are explicit.

### 9.3 Stable

`Stable` means the product/platform boundary is supported as an approved durable integration contract for its declared scope.

A `Stable` Product Contract **MUST** have:

- an approved compatibility policy;
- a migration and deprecation policy;
- declared support responsibility for the boundary;
- validated security/data/authority semantics proportionate to consequence;
- contract-level conformance evidence;
- no unresolved dependency on undocumented platform internals.

`Stable` Product Contract status does not make referenced Platform Capabilities `Active`; capability lifecycle remains governed independently.

### 9.4 Deprecated

A `Deprecated` Product Contract remains supported only within its declared deprecation window or replacement plan.

It **MUST** identify the replacement or retirement path, affected consumers and migration expectations where applicable.

### 9.5 Retired

A `Retired` Product Contract **MUST NOT** be used for new governed interaction.

Required historical identity, versions, execution references and migration evidence **MUST** remain identifiable according to retention, privacy, legal and contractual requirements.

## 10. Required Contract Declaration

A Product Contract **MUST** declare the following where applicable to its actual interaction scope.

### 10.1 Product Identity and Responsibility

- product or experiment Subject Identity;
- product version or compatibility line;
- accountable product architectural owner;
- contract owner;
- contract lifecycle state;
- intended operational environment or pilot scope when relevant.

### 10.2 Capability Dependencies

For each platform capability dependency:

- capability identity;
- compatible capability contract version or version range;
- lifecycle state when relevant to reliance;
- required operations;
- provider responsibility;
- consumer responsibility;
- expected failure or unavailability behavior;
- whether the dependency is `Provisional`, `Incubating` or otherwise not a stable supported dependency.

A Product Contract **MUST NOT** imply that a referenced `Candidate` or `Incubating` capability is `Active`.

### 10.3 Domain Types at the Boundary

The contract **MUST** identify product-owned domain record, relationship, artifact or message types that cross the boundary or materially determine platform behavior.

Their semantics remain product-owned unless separately promoted.

The contract **SHOULD** reference versioned schemas or type definitions rather than duplicating their complete definitions when separate governed artifacts are sufficient.

### 10.4 Canonical State and Authority

For each significant canonical read or write, the contract **MUST** identify where applicable:

- governed subject/type;
- authority mode;
- authoritative source;
- read/write responsibility;
- subject-level or version-pinned reference semantics;
- freshness or synchronization expectation for external authority;
- conflict/failure behavior;
- whether the product may propose, request or cause canonical mutation.

A Product Contract **MUST NOT** silently convert `External Reference` or `Governed Replica` data into `Native` Arvectum OS authority.

### 10.5 Operations

The contract **MUST** identify operations exposed across the boundary when operation semantics materially affect authorization, authority, compatibility or reconstruction.

An operation declaration **SHOULD** identify:

- operation identity or stable semantic name;
- input type/version expectations;
- output type/version expectations;
- side-effect class;
- idempotency or retry expectations where consequential;
- authorization/authority requirements by reference;
- validation/approval gates by reference;
- failure semantics.

Detailed Governed Execution state semantics remain RFC-0005 scope.

### 10.6 Events and Artifacts

The contract **MUST** identify shared Event and artifact types it consumes or produces when they cross the product/platform boundary.

The declaration **MUST** distinguish:

- events entering shared governed platform history;
- product-local telemetry or logs that remain outside shared canonical history;
- governed artifacts;
- transient outputs.

Complete event taxonomy, delivery and provenance semantics remain RFC-0006 scope.

### 10.7 Security, Authority and Data Handling

The contract **MUST** declare or reference applicable:

- organization/tenant scope;
- principal or actor expectations where material;
- required permissions or authorization semantics;
- organizational authority or approval requirements for consequential operations;
- classification constraints;
- purpose/use constraints where applicable;
- cross-organization sharing constraints;
- retention and deletion responsibilities;
- secret-handling boundaries;
- data minimization expectations.

Declaring an identity, relationship, extension or operation **MUST NOT** itself grant access or organizational authority.

### 10.8 Portability and Export

Where product/platform interaction creates or relies on governed organizational state, the contract **MUST** identify portability responsibility sufficient to preserve organizational continuity within its scope.

The contract **MUST NOT** promise export of data, credentials, secrets or third-party material that cannot legally, contractually or technically be exported.

### 10.9 Support and Migration Status

The contract **MUST** state whether its boundary is:

- experimental/provisional;
- supported stable;
- deprecated;
- retired.

Where migration is required, the contract **MUST** identify a migration path or an explicit decision that no automated migration is required within the declared scope.

## 11. Dependency Semantics

### 11.1 Explicit Dependency Graph

Platform dependencies in a Product Contract **MUST** be explicit enough to determine whether the product can operate when a dependency is unavailable, incompatible, deprecated or retired.

### 11.2 No Hidden Internals

A product **MUST NOT** rely on:

- direct reads or writes to platform-internal database tables;
- undocumented internal service endpoints;
- internal implementation imports;
- private event streams;
- undocumented naming conventions;
- internal cache or queue structures;
- implicit shared state

when those mechanisms bypass the Product Contract or applicable public platform contract.

A temporary compatibility bridge **MAY** exist during migration only when it is explicit, bounded, owned, reviewed and has an exit path.

### 11.3 No Circular Responsibility

A Product Contract **MUST NOT** create a circular architectural-responsibility dependency in which the platform depends on product-specific behavior to define a shared platform invariant while the product simultaneously depends on that invariant as a platform guarantee.

### 11.4 Cross-product Interaction

One product **MUST NOT** access another product's internals.

Cross-product interaction **MUST** use one or more of:

- Canonical Records and Typed Relationships under declared authority;
- shared governed Events;
- an explicit shared Product Contract or product-to-product contract boundary;
- an `Active` or appropriately governed shared Platform Capability.

## 12. Compatibility Model

### 12.1 Compatibility Is Semantic

Compatibility is compatibility of declared behavior and organizational meaning, not merely wire-format parsing.

A change that preserves syntax but changes authority, side effects, required approvals, data exposure, canonical meaning or failure behavior **MAY** be backward-incompatible.

### 12.2 Stable Contract Compatibility

A `Stable` Product Contract **MUST** define how compatible versions are recognized.

The mechanism **MAY** use semantic versioning, explicit compatibility matrices, capability negotiation or another technology-independent rule.

### 12.3 Breaking Change

A breaking change to a `Stable` Product Contract **MUST**:

- create a new contract version;
- identify affected consumers/providers;
- provide migration or coexistence behavior proportionate to scope;
- preserve required historical interpretability;
- receive the decision authority required by RFC-0001 when it creates a material shared-platform or external commitment.

### 12.4 Provisional Change

A `Provisional` contract **MAY** change more rapidly, but changes **MUST** preserve its bounded scope, reviewability, migration/exit path and security/data integrity.

A provisional label **MUST NOT** be used to hide irreversible customer dependency.

## 13. Product Experiment Model

### 13.1 Required Experiment Declaration

A Product Experiment **MUST** declare:

- experiment identity;
- accountable product or operational sponsor;
- hypothesis or intended organizational/commercial outcome;
- scope;
- effort or budget bound;
- data and risk boundary;
- review date;
- success/evidence criteria proportionate to the experiment;
- explicit exit path: promote, contain, replace or retire.

### 13.2 Platform-interacting Experiment

When the experiment crosses the platform boundary, its `Provisional` Product Contract **MUST** add only the declarations needed for that interaction.

The platform **MUST NOT** require a complete enterprise integration specification for a low-risk reversible experiment when a smaller contract preserves architecture, security and migration safety.

### 13.3 Experiment Responsibility

The product remains architecturally responsible for the experiment unless and until a separate platform promotion decision is approved.

Platform engineers assisting with implementation do not by themselves transfer architectural responsibility to the platform.

### 13.4 Experiment Review

At the declared review condition, the experiment **MUST** be evaluated for:

- evidence of organizational or commercial value;
- actual consumers;
- reuse evidence;
- security/privacy/governance outcomes;
- operational burden;
- duplication cost;
- portability/migration cost;
- whether it should remain product-local, be contained, be retired or be nominated for platform incubation.

## 14. Promotion into Platform Incubation

### 14.1 Promotion Is a Separate Decision

Success of a Product Experiment **MUST NOT** automatically convert it into a Platform Capability.

Promotion **MUST** be a separate governed decision under RFC-0001 capability lifecycle rules.

### 14.2 Promotion Candidate Evidence

A promotion proposal **SHOULD** include:

- source experiment(s);
- demonstrated consumers or strategic requirement;
- evidence of repeated/domain-neutral mechanism;
- proposed domain-neutral boundary;
- expected organizational benefit;
- migration impact on the source product;
- security/data/authority impact;
- ownership and support implications;
- alternatives, including leaving the mechanism product-local;
- criteria for incubation success or return-to-product.

### 14.3 No Code-equals-Contract Rule

Existing product code **MUST NOT** become the platform contract merely because it is reused.

The promoted contract **MUST** be expressed in domain-neutral semantics and may require a compatibility adapter around product-originated implementation during incubation.

### 14.4 Return to Product

An incubating mechanism that fails to justify shared platform responsibility **MAY** be returned to a product, replaced or retired without treating that outcome as an architectural failure.

Required migration and historical references **MUST** be preserved.

## 15. Extension Model

### 15.1 Definition

An **Extension** is a registered and versioned component or governed extension artifact that extends product or platform behavior through a declared contract without redefining Kernel or shared platform invariants.

Extensions may include products, agents, workflows, schemas, validators, templates, policies, connectors, tools, adapters and UI modules as allowed by RFC-0001.

### 15.2 Extension Identity

An extension **MUST** declare:

- stable extension identity;
- version;
- extension type;
- architectural owner;
- required Product Contract or capability contract;
- compatibility constraints;
- organization/tenant scope where applicable;
- lifecycle/deprecation status.

### 15.3 Registration Is Not Authorization

Extension registration makes an extension discoverable and governable.

Registration **MUST NOT** by itself grant:

- data access;
- platform permissions;
- organizational authority;
- cross-organization visibility;
- approval rights;
- `Active` Platform Capability status.

Runtime access **MUST** be evaluated through applicable authorization, authority and Product Contract rules.

### 15.4 Inputs, Outputs and Side Effects

An extension **MUST** declare inputs, outputs, significant side effects and emitted/consumed governed events proportionate to consequence.

An extension that may cause consequential canonical mutation **MUST** do so only through applicable Governed Execution and authorization/authority boundaries.

Detailed Governed Execution semantics remain RFC-0005 scope.

### 15.5 Data Handling

An extension **MUST** declare or inherit by explicit reference:

- data classes it may access;
- permitted purpose/use where applicable;
- retention behavior;
- whether it sends data to an external processor/service;
- cross-organization restrictions;
- secret-handling requirements;
- portability/deletion implications.

### 15.6 Failure Behavior

An extension **MUST** define failure behavior proportionate to its side effects.

Failure **MUST NOT** silently broaden authorization, cross organization boundaries, create competing authority, lose required evidence or convert a partial operation into an unrecorded consequential mutation.

### 15.7 Deprecation

A versioned extension **MUST** identify deprecation or retirement behavior when consumers may continue to depend on it.

## 16. Adapter and Connector Model

### 16.1 Purpose

Adapters and connectors translate between Arvectum OS contracts and technology/vendor/external-system interfaces.

They **MUST NOT** redefine organizational meaning merely because an external API or vendor representation differs.

### 16.2 External Authority

When an adapter accesses an external system of record, the applicable Product Contract **MUST** preserve RFC-0001/RFC-0002 authority mode semantics.

The adapter **MUST NOT** create competing `Native` authority by caching or transforming external data.

### 16.3 Vendor Replacement

A vendor-specific adapter **MAY** be used directly when it is the simplest solution.

A Product Contract **SHOULD** isolate only the stable organizational semantics and material dependency assumptions needed to replace or migrate the vendor without loss of governed meaning.

This RFC does not require speculative abstraction around every third-party dependency.

## 17. Contract Discovery and Registry

### 17.1 Canonical Discoverability

Current governed Product Contract versions **MUST** be discoverable from a canonical repository or registry controlled by Arvectum OS governance.

Discovery **MUST** identify at least:

- contract identity;
- effective version;
- product/experiment identity;
- owner;
- lifecycle state;
- dependency summary;
- compatibility status;
- canonical reference.

### 17.2 Registry Is Not Runtime Coupling

A canonical contract registry is a governance/discovery concept.

This RFC does not require a dedicated runtime registry service, dynamic plugin loader or network control plane.

A versioned Git-managed manifest and validation tooling **MAY** conform during early stages when proportionate.

## 18. Contract Validation

### 18.1 Validation Timing

A Product Contract **MUST** be validated:

- before first governed platform interaction;
- when a material contract version changes;
- when a stable dependency becomes incompatible or deprecated;
- before a product claims conformance for a scope relying on the contract.

### 18.2 Validation Classes

Validation **SHOULD** cover where applicable:

- structural completeness;
- referenced identity/version existence;
- capability compatibility;
- absence of hidden internal dependencies;
- organization/tenant scope consistency;
- authority-mode consistency;
- permission/authority declarations;
- schema/type compatibility;
- portability/deletion responsibilities;
- migration/deprecation state;
- extension compatibility.

### 18.3 Static and Runtime Validation

Validation **MAY** be performed statically, at deployment, at execution, or through a combination.

This RFC does not require dynamic negotiation when static validation is sufficient.

## 19. Security and Authority Boundary

### 19.1 No Ambient Trust

A Product Contract is not a security credential.

Possessing, loading or referencing a Product Contract **MUST NOT** authorize an actor or extension.

### 19.2 Least Privilege at Boundary

A product or extension **MUST** receive only the platform operations and governed data access required for the declared contract scope.

Broad wildcard access **SHOULD** be exceptional and governed proportionate to risk.

### 19.3 Organizational Authority

Technical permission to invoke an operation **MUST NOT** be treated as sufficient organizational authority for a consequential decision where separate decision authority or approval is required.

### 19.4 AI Extensions

An AI agent registered as an extension **MUST NOT** obtain organizational authority merely from its registration, Product Contract, tool access or ability to generate a result.

AI-mediated consequential operations remain subject to applicable Governed Execution, authorization, approval and evidence rules.

## 20. Data Isolation, Privacy and Cross-organization Use

### 20.1 Organization Scope

Product Contract interactions **MUST** preserve organization/tenant scope on governed state and operations.

A contract **MUST NOT** create an ambient cross-organization data path.

### 20.2 Shared Platform State

Shared platform-global contract metadata **MUST NOT** contain organization-specific customer data unless that data is explicitly classified and governed for shared use.

### 20.3 Derived Data

Indexes, embeddings, summaries, caches and generated artifacts created through a Product Contract **MUST** inherit or resolve applicable organization scope, classification, rights, retention and deletion constraints proportionate to their content and use.

### 20.4 Cross-organization Learning

Product Contract participation **MUST NOT** by itself authorize customer data, evidence, memory or knowledge to be reused across organizations.

Cross-organization reuse requires separate applicable rights, classification and governance.

## 21. Portability, Termination and Handover

A Product Contract that governs organizationally significant state **MUST** identify enough export, migration, deletion and handover responsibility to avoid organizational continuity depending on an inaccessible product/platform integration detail.

On product or contract termination, the applicable boundary **MUST** define where relevant:

- final canonical authority;
- exportable governed state;
- external references preserved;
- remaining retention obligations;
- deletion responsibilities;
- replacement or migration path;
- treatment of extensions and credentials;
- preservation of historical Product Contract Version Identities required to interpret past executions.

Manual documented migration **MAY** satisfy an early-stage requirement when proportionate and tested for the declared scope.

## 22. Commercial Commitment Integrity

A `Provisional` Product Contract **MUST NOT** be represented externally as a stable platform guarantee unless the externally relied-upon commitment explicitly and accurately reflects its provisional scope and limitations.

A `Stable` Product Contract **MUST NOT** imply:

- broader Arvectum OS conformance than approved;
- `Active` status for an `Incubating` capability;
- SLA/support commitments not separately approved;
- unrestricted portability or data rights;
- guaranteed compatibility outside its declared compatibility policy.

Material customer-facing commitments that expand supported platform obligations remain subject to RFC-0001 decision authority.

## 23. Product Contract Changes and Decision Authority

### 23.1 Low-risk Provisional Changes

A low-risk reversible change to a `Provisional` Product Contract **MAY** be approved under delegated product authority if such delegation exists and the change does not create a shared-platform obligation, cross-organization data risk, consequential external commitment or irreversible public dependency.

Until delegated authority is approved, residual authority remains with the owner under RFC-0001.

### 23.2 Material Stable Changes

A material change to a `Stable` Product Contract that creates a backward-incompatible public contract, shared-platform obligation, material security/privacy risk or external commitment **MUST** use the decision authority required by RFC-0001.

### 23.3 Architectural Exception

A temporary exception to Product Contract rules **MUST** identify:

- scope;
- proposer;
- decision authority;
- rationale;
- risk;
- review or expiry condition;
- migration/exit plan.

An exception **MUST NOT** weaken Constitutional or Accepted RFC security, sovereignty, authority or canonical-state invariants.

## 24. Migration from Existing Products

### 24.1 No Mandatory Big Bang

Existing products **MAY** migrate incrementally to Product Contracts.

This RFC does not require immediate redesign of all product-local code or data.

### 24.2 Boundary Inventory

Migration **SHOULD** begin by inventorying actual platform interactions:

- direct database access;
- internal imports;
- shared tables/state;
- implicit identity or authority assumptions;
- platform capability use;
- shared events;
- external-system authority;
- background jobs;
- extension/tool access;
- portability/deletion dependencies.

### 24.3 Compatibility Bridges

A compatibility bridge **MAY** temporarily wrap legacy coupling behind an explicit boundary when:

- scope is bounded;
- security and data integrity are preserved;
- the bridge is owned and observable proportionate to consequence;
- the contract declares the legacy dependency;
- there is a review date and exit path.

### 24.4 Migration Priority

Migration priority **SHOULD** follow consequence and coupling risk rather than code volume.

Consequential canonical writes, cross-organization paths, security-sensitive access and externally committed interfaces should be addressed before low-risk internal reads.

## 25. Reference Representation

This RFC defines semantics, not a mandatory serialization format.

An implementation may represent a Product Contract using YAML, JSON, a database-backed registry, code-generated descriptors or another governed form.

A conceptual representation is:

```text
ProductContract
  identity
  version
  lifecycle
  product
  owner
  scope
  capabilities[]
  domain_types[]
  canonical_state[]
  operations[]
  events[]
  artifacts[]
  security_and_authority
  extensions[]
  portability
  compatibility
  migration
  support_status
  review_or_deprecation
```

The representation **MUST NOT** be mistaken for a fixed physical schema unless separately standardized.

## 26. Conformance

Conformance with this RFC is scoped to a declared product/platform integration boundary.

A conforming subject **MUST** identify:

- product/experiment;
- Product Contract identity and effective version;
- lifecycle state;
- environment or pilot scope where relevant;
- platform dependencies;
- known exceptions;
- applicable conformance maturity.

A product **MUST NOT** claim full-platform conformance merely because one Product Contract passes validation.

Manual or provisional controls **MAY** conform when allowed by the contract lifecycle, proportionate to risk, explicit and reviewable.

## 27. Normative Fitness Tests

A conforming implementation or governed contract process **MUST** be capable of satisfying the following tests within its declared scope.

### FT-01 — Fully Product-local Experiment

Given an experiment with no platform capability use, canonical platform access or shared platform history, the system/process permits it to remain product-local without inventing a Product Contract.

### FT-02 — Minimal Provisional Contract

Given a bounded experiment that consumes one platform capability, a minimal `Provisional` Product Contract can declare only the required interaction, owner, compatibility assumption, constraints, review date and exit path.

### FT-03 — Hidden Database Coupling Rejected

Given a product that reads a platform-internal table not declared by a public/platform contract, contract validation identifies the coupling as non-conforming.

### FT-04 — Capability Status Preserved

Given a Product Contract that depends on an `Incubating` capability, the contract and external representation do not label or imply the capability is `Active`.

### FT-05 — External Authority Preserved

Given a product reading a Governed Replica of an external ERP record, the Product Contract preserves the external authority and does not treat the local replica as `Native` authority.

### FT-06 — Consequential Contract Version Pinning

Given a consequential execution under a changeable Product Contract, the evidence can identify the exact effective Product Contract version materially relied upon.

### FT-07 — Registration Does Not Grant Permission

Given a registered extension with no applicable authorization grant, registration alone does not permit it to read governed organization data or invoke protected operations.

### FT-08 — Organization Isolation

Given identical extension code used by two organizations, the Product Contract and authorization boundary do not create ambient cross-organization access or shared customer state.

### FT-09 — Product-owned Domain Logic Remains Product-owned

Given a domain validator used by one product, declaring it in the Product Contract does not automatically turn the validator into a Platform Capability.

### FT-10 — Explicit Promotion Decision

Given a successful product experiment reused by a second consumer, the system/process still requires a separate governed capability-promotion decision before platform incubation.

### FT-11 — Stable Breaking Change

Given a Stable Product Contract change that alters authority or consequential side effects, the change is treated as potentially breaking even when wire syntax remains parse-compatible.

### FT-12 — Provisional Change Is Bounded

Given a rapidly changing provisional integration, each change retains explicit ownership, scope, security/data constraints and an exit/review path.

### FT-13 — Cross-product Boundary

Given Product A needs data from Product B, Product A cannot access Product B internals; interaction uses declared records/events/contracts or a shared capability.

### FT-14 — Adapter Does Not Redefine Meaning

Given a vendor API field model that differs from Arvectum OS organizational semantics, the adapter translates the vendor representation without making vendor field conventions canonical platform meaning.

### FT-15 — Portability Does Not Leak Secrets

Given a contract termination, the organization can preserve governed meaning and migration references without requiring export of non-exportable private credentials.

### FT-16 — AI Extension Has No Ambient Authority

Given an AI extension with tool access, it cannot approve a consequential decision or mutate canonical state solely because the Product Contract registers the extension.

### FT-17 — Derived Data Retains Scope

Given a product creates an embedding or summary from organization-scoped governed data through a platform capability, the derived representation retains or resolves applicable organization, classification, retention and deletion constraints.

### FT-18 — Retired Contract History Remains Interpretable

Given a retired Product Contract, historical executions can still resolve the contract identity/version necessary to interpret past governed interaction subject to applicable retention/deletion rules.

## 28. Implementation Guidance

The simplest early implementation is expected to be a versioned contract file plus validation in the same repository or modular monolith as the platform.

A dedicated contract-registry service, dynamic plugin marketplace, schema federation system or distributed policy plane is **not** required by this RFC.

Implementation should prefer:

- explicit contract files over implicit conventions;
- static validation before dynamic negotiation when sufficient;
- references to versioned schemas/policies over duplicate declarations;
- product-local experiments over premature platformization;
- compatibility adapters over big-bang migrations;
- modular-monolith boundaries over service proliferation without evidence.

Technology-specific representation, CI validation and runtime integration details should be defined by ADR or implementation decision only when they become materially constraining.

## 29. Risks and Mitigations

### Risk 1 — Contract bureaucracy slows experiments

**Mitigation:** require minimal proportional `Provisional` contracts only when platform interaction exists; fully product-local experiments need no Product Contract.

### Risk 2 — Product Contract becomes a universal product schema

**Mitigation:** contract only boundary-relevant semantics; product internals remain product-owned.

### Risk 3 — Extension registry becomes an authorization system by accident

**Mitigation:** registration explicitly grants no permission or authority.

### Risk 4 — Products bypass contracts because internals are easier

**Mitigation:** validate hidden coupling, improve platform gravity, permit bounded compatibility bridges during migration.

### Risk 5 — Successful product code is prematurely generalized

**Mitigation:** promotion requires separate evidence-based decision and domain-neutral contract design.

### Risk 6 — Stable compatibility promises exceed actual capability maturity

**Mitigation:** Product Contract lifecycle and capability lifecycle remain independent; provisional/incubating dependencies must remain visible.

### Risk 7 — Vendor adapters become sources of organizational meaning

**Mitigation:** adapters translate technology semantics; Product Contracts preserve stable organizational meaning and explicit authority.

### Risk 8 — RFC-0004 prejudges RFC-0003/0005/0006/0007

**Mitigation:** security, execution, event/provenance and knowledge details are declared by reference/boundary only; later RFCs retain their reserved detailed scope.

## 30. Alternatives Considered

### 30.1 No Formal Product Contract

Rejected because products would accumulate accidental platform dependencies, direct internal coupling and ambiguous responsibility.

### 30.2 One Complete Contract Schema Before Any Product Work

Rejected as speculative and contrary to proportionality. The RFC defines semantics and minimum declarations, not a fixed enterprise manifest.

### 30.3 Treat Every Product as a Plugin

Rejected because products may be independent applications, services or organizational workflows; a plugin runtime is an implementation choice, not an architectural principle.

### 30.4 Automatically Promote Reused Code to Platform

Rejected because reuse of code is not evidence that architectural responsibility should move to the platform.

### 30.5 Require Product Contract for Every Experiment

Rejected because RFC-0001 explicitly permits fully product-local experiments without a Product Contract.

## 31. Consequences

If accepted, this RFC establishes a stable product/platform boundary model without fixing a concrete protocol or runtime.

Positive consequences:

- products can experiment quickly while platform interaction remains explicit;
- domain logic remains product-owned by default;
- shared dependencies become discoverable and versionable;
- accidental coupling becomes testable;
- platform promotion remains evidence-based;
- extension registration becomes governable without becoming implicit authorization;
- migration and portability responsibilities become visible;
- future implementation can start with simple versioned files and validation.

Costs:

- products that cross the platform boundary must maintain a contract;
- compatibility and migration must be considered explicitly;
- legacy direct coupling becomes architectural debt requiring staged migration;
- some product/platform changes will require coordinated contract versions.

These costs are intentional and proportionate to the organizational value of an explicit reusable boundary.

## 32. Follow-up Decisions

If accepted, likely subordinate work includes:

1. a Product Contract representation/schema standard when implementation needs it;
2. ADR for repository location and validation tooling when the reference implementation begins;
3. an extension-type catalog only when real extensions require shared classification;
4. concrete Product Contracts for products that begin consuming Arvectum OS;
5. RFC-0005 for Governed Execution and Workflow semantics;
6. RFC-0006 for Event, Provenance and Observability semantics;
7. RFC-0007 for Memory, Knowledge and Governed Learning lifecycle.

No follow-up artifact should be created merely for completeness before there is a concrete decision or implementation need.

## 33. Acceptance Criteria

This RFC may be accepted only when:

1. no conflict exists with Constitution `1.2.0`;
2. no conflict exists with Accepted RFC-0001 `1.0.0` or RFC-0002 `1.0.0`;
3. any then-Accepted RFC-0003 implications have been reconciled;
4. Product Contract requirements remain proportional and do not force contracts on fully product-local experiments;
5. product-domain behavior remains outside shared platform semantics by default;
6. extension registration remains distinct from authorization and organizational authority;
7. promotion to platform incubation remains a separate governed decision;
8. compatibility, migration and portability behavior are sufficiently explicit for durable boundaries;
9. normative fitness tests are objectively satisfiable;
10. functional role cross-review is complete;
11. explicit owner approval exists independently before publication as `Accepted`;
12. RFC Index and related canonical artifacts are synchronized consistently with Acceptance Integrity rules.

## 34. Review History

The proposal was developed through the project functional cross-review loop with a hard maximum of seven iterations.

- `0.1.0` — complete first working draft;
- review iteration 1 — material corrections to contract minimality, independent capability lifecycle, extension authorization, external-authority fidelity, migration and commercial-integrity boundaries;
- `0.2.0` — revised working proposal;
- review iteration 2 — additional corrections to semantic compatibility, derived-data obligations, historical contract version pinning and cross-product interaction;
- `0.3.0` — revised proposal;
- review iteration 3 — no remaining material correction identified for the current lifecycle stage; cycle stopped after 3 of maximum 7 review iterations.

Detailed review evidence is recorded in `docs/reviews/RFC-0004-functional-cross-review.md`.

## 35. Approval

Current state: `Proposed`.

Functional cross-review is evidence of proposal quality only. It is **not** owner approval and does not give this RFC normative force.

Acceptance requires an independent owner-approved decision record followed by publication of `Accepted 1.0.0` and synchronized Acceptance Integrity evidence in the RFC Index.
