# Arvectum OS Reference Implementation Readiness Baseline

Status: `Active`
Version: `1.0.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Canonical role: `subordinate implementation-readiness guidance`
Normative authority: `None beyond the Accepted sources it references`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0007 `1.0.0` (`Accepted`)
Roadmap block: `0H — Reference implementation readiness`

## 1. Purpose

This document closes the planning gap between the Accepted semantic architecture of Arvectum OS and the first bounded reference implementation.

Its purpose is to make implementation startable without forcing engineers to invent cross-cutting architecture in code and without prematurely selecting technologies that the Accepted RFCs intentionally leave replaceable.

This document is subordinate to the Constitution, Accepted RFCs, Accepted ADRs and approved governance artifacts. It does not create a new platform contract, capability lifecycle state, production-readiness claim or customer commitment.

## 2. Canonical interpretation of the work item

The current canonical roadmap names this work **Block 0H — Reference implementation readiness**.

This block is **not RFC-0008**.

RFC-0001's follow-up sequence reserves the identifier and title:

`RFC-0008 — Document and Artifact Architecture`.

Therefore this readiness work MUST NOT consume RFC-0008, redefine that reserved scope, or create an unnecessary architecture RFC where subordinate implementation guidance is sufficient.

If Document and Artifact Architecture later requires an RFC, it retains the RFC-0008 slot unless canonical governance changes that sequence.

## 3. Readiness conclusion

The first bounded reference implementation **may start** under the following conditions:

1. it implements only semantics already established by Constitution `1.2.0` and Accepted RFC-0001 through RFC-0007;
2. it remains a modular, reversible implementation rather than a claim about permanent service topology;
3. product-domain logic is excluded from shared platform modules;
4. external authority, Organization scope, authorization, Organizational Authority and data-governance boundaries remain explicit;
5. consequential canonical mutation occurs only through Governed Execution;
6. canonical history remains immutable at the semantic level;
7. product/platform interaction uses the applicable Product Contract boundary;
8. Events, telemetry, Memory, Knowledge and transient outputs retain their distinct Accepted semantics;
9. technology-specific choices remain replaceable and are promoted to ADRs only when they become sufficiently constraining;
10. no part of the reference implementation is represented as an `Active` Platform Capability or as production-ready merely because it works.

## 4. Scope of the first reference implementation

The first implementation should prove the architectural spine, not the whole future platform.

The minimum scope is:

- stable Identity semantics;
- immutable Canonical Record version semantics;
- Typed Relationship identity and version-aware endpoints;
- Event admission and append-only history;
- Execution Context identity and governance-significant versions;
- explicit Organization scope;
- explicit authorization and Organizational Authority decision boundaries;
- a minimal Product Contract representation and validation boundary;
- Workflow and Governed Execution version attribution;
- consequential mutation gating and exact material input version pinning;
- provenance references sufficient for a bounded reconstruction scenario;
- separation of canonical Events from operational telemetry;
- Observation / Memory / Knowledge Candidate / Knowledge distinctions;
- explicit non-authority of retrieval/index projections;
- portability of the semantic fixture data in a documented implementation-neutral representation.

The implementation is expected to grow from real product use. It is not required to implement every optional concept, lifecycle state, deployment environment, integration mode or operational control before the first useful slice exists.

## 5. Non-goals

The readiness baseline does not select or require:

- a programming language;
- a web framework;
- an API protocol;
- a database engine;
- a graph database;
- an event broker;
- a workflow engine;
- an IAM provider;
- a policy engine;
- a secrets manager;
- a vector database or search engine;
- an LLM or model provider;
- a cloud or on-premises topology;
- microservices;
- Kubernetes or another orchestrator;
- a universal schema registry;
- a distributed transaction system;
- a permanent repository/package layout;
- product-specific schemas, workflows, ontologies or business rules.

These choices remain implementation decisions, ADR candidates, standards, Product Contracts or product decisions only when evidence makes them necessary.

## 6. Initial logical implementation structure

The reference implementation SHOULD begin as a **modular monolith** or equivalently simple single-runtime composition unless evidence justifies distribution.

This is an implementation shape, not a permanent Platform Service topology.

The implementation should expose the following logical modules or equivalent boundaries. Exact package names and filesystem layout are not fixed by this document.

### 6.1 Kernel model

Responsibilities:

- Identity value semantics;
- Canonical Record common governed envelope;
- immutable version lineage rules;
- Canonical Head versus Effective Version resolution contract;
- Typed Relationship semantics;
- Event and Execution Context specialization contracts;
- authority-mode representation;
- governed references and integrity metadata interfaces.

The module MUST NOT contain product-domain concepts.

### 6.2 Identity, security and sovereignty

Responsibilities:

- Organization / tenant context;
- Principal and Actor context;
- authentication-evidence boundary;
- deny-by-default authorization decision interface;
- distinct Organizational Authority / approval references;
- data-governance and classification hooks;
- fail-closed behavior when required Organization or authorization context is unresolved.

The first implementation MAY use simple local/manual providers behind these interfaces. Simplicity MUST NOT collapse the semantic distinctions accepted by RFC-0003.

### 6.3 Product Contract boundary

Responsibilities:

- Product Contract identity/version/lifecycle representation;
- minimal `Provisional` contract validation;
- declared platform dependencies;
- canonical read/write operation declarations;
- Event/artifact declarations where in scope;
- Organization, authority, security, portability and failure declarations proportionate to the interaction;
- rejection of hidden internal coupling in the declared reference scenarios.

A versioned file plus validation is sufficient for the first reference implementation. A dedicated registry service is not required.

### 6.4 Governed Execution and Workflow

Responsibilities:

- Workflow identity/version representation;
- Execution Context lifecycle and governance-significant versioning;
- exact effective Workflow and Product Contract version attribution where applicable;
- material input/version pinning;
- operation side-effect classification;
- authorization / authority / data-governance / validation / approval gate separation;
- canonical mutation gate;
- idempotency, retry, uncertainty and compensation semantics required by the bounded scenarios.

No workflow engine is required for the first slice.

### 6.5 Event, provenance and observability boundary

Responsibilities:

- canonical Event admission;
- Event identity and immutable admission semantics;
- schema/type version attribution;
- correlation and causation references;
- required evidence linkage to governed execution;
- duplicate/replay-safe semantics in reference scenarios;
- provenance references;
- explicit distinction between canonical Event history and operational telemetry.

No event broker or dedicated observability backend is required for the first slice.

### 6.6 Memory, Knowledge and governed learning boundary

Responsibilities:

- Observation representation where significant;
- Organizational Memory references;
- Knowledge Candidate and Improvement Proposal distinction;
- Knowledge identity/version/lifecycle representation;
- explicit promotion boundary;
- freshness, contradiction, supersession and retraction semantics required by reference scenarios;
- non-authority of search, RAG, embedding and index projections.

No vector database, embedding model or automated promotion system is required for the first slice.

### 6.7 Application composition

Responsibilities:

- compose the domain-neutral modules for reference scenarios;
- supply clocks, identifier issuers and adapters;
- enforce dependency direction;
- expose a thin entry point for tests, local tools or later adapters.

Application composition MUST NOT become a hidden place for product-domain semantics or bypass Governed Execution.

### 6.8 Adapters

Adapters MAY implement:

- persistence;
- serialization;
- external authoritative systems;
- authentication providers;
- policy evaluation;
- clocks and identifiers;
- AI/model execution;
- search/indexing;
- telemetry.

Adapters translate technology/vendor representation into Accepted organizational semantics. They MUST NOT redefine authority, identity, version, Organization scope or governance meaning.

## 7. Dependency rule

The reference implementation SHOULD follow this dependency direction:

```text
Accepted semantic contracts
          ↓
Domain-neutral implementation modules
          ↓
Application composition
          ↓
Technology / vendor / product adapters
```

Technology and product adapters may depend on shared semantic contracts.

Shared semantic modules MUST NOT depend on product business schemas, vendor SDK semantics, database row layouts, broker topics, UI routes or model-provider conventions.

A future physical split into Platform Services may change deployment boundaries without changing these organizational semantics.

## 8. First executable slice

The first implementation slice SHOULD prove one small end-to-end governed scenario entirely within the reference implementation boundary.

### Scenario

1. establish one Organization scope and attributable Actor;
2. create a `Native` canonical subject with stable Subject Identity and first immutable Version Identity;
3. define a versioned Workflow that is permitted to update that subject;
4. start an Execution Context and pin the effective Workflow version and material input version;
5. pass explicit authorization and Organizational Authority test gates;
6. perform a `CanonicalMutation` operation that creates a second immutable Canonical Record version rather than mutating the first;
7. emit/admit a canonical Event linked to the execution and resulting version;
8. preserve causation and provenance references sufficient to reconstruct the operation;
9. create an Observation from the outcome without treating it as validated Knowledge;
10. export the bounded governed state into a documented semantic fixture and prove that the fixture preserves identities, versions, authority and relationships independently of the in-memory representation.

### Failure cases in the same slice

The tests SHOULD also prove that:

- an unresolved Organization scope fails closed;
- authentication alone does not authorize mutation;
- authorization alone does not satisfy required Organizational Authority;
- a direct canonical mutation outside an Execution Context is rejected;
- an existing canonical version cannot be mutated in place;
- a duplicate Event delivery does not create a second Event occurrence;
- an Event Identity with conflicting immutable content is rejected/quarantined by the admission boundary;
- a replay used to rebuild a projection causes no new consequential side effect;
- an Observation cannot be read as validated Knowledge without promotion;
- a projection/index result cannot substitute for the exact governed Version Identity relied upon.

This slice is intentionally domain-neutral.

## 9. Initial persistence strategy

No persistent storage technology is required to start the first executable slice.

The initial implementation MAY use deterministic in-memory repositories behind explicit persistence ports while testing the Accepted semantics.

This is not an architectural endorsement of in-memory storage. It is a reversible bootstrap technique that prevents a database schema from becoming accidental architecture before the object boundaries and fitness tests are executable.

Before durable persistence becomes required, the implementation MUST either:

- select a bounded persistence approach through an ADR if the choice materially constrains migration, integrity, portability, concurrency or future modules; or
- document why the selected local choice remains non-constraining and replaceable within the current scope.

## 10. Initial external interface strategy

No public network API is required to start the first executable slice.

Tests and local composition MAY call application interfaces in-process.

A REST, RPC, event, CLI or other external protocol should be chosen only when a real consumer or Product Contract requires it. A protocol choice that becomes a supported cross-product or public boundary requires the appropriate ADR/contract evidence before accidental reliance grows around it.

## 11. ADR gate

### 11.1 Minimum ADR set at readiness

**No new ADR is required before the first bounded executable slice starts.**

Reason:

- Accepted RFCs already define the semantic constraints required for the slice;
- the slice can use in-memory adapters and in-process invocation without fixing a public protocol or persistence contract;
- no repository/runtime technology has yet been canonically selected;
- creating speculative ADRs now would turn reversible implementation choices into premature commitments.

### 11.2 When an ADR becomes required

Create an ADR before relying on an implementation choice when one or more of the following is true:

1. the choice constrains multiple platform modules or products;
2. changing it later would require a material data migration or public-contract break;
3. it becomes part of a stable cross-product/public interface;
4. it materially determines tenant isolation, authorization enforcement, evidence integrity or external authority behavior;
5. it creates a durable dependency on a database, broker, orchestration runtime, identity provider, schema registry, retrieval engine or vendor-specific format;
6. competing plausible choices have materially different portability, security, reliability or operational consequences;
7. code would otherwise create a de facto cross-cutting architecture that is not already Accepted.

### 11.3 Likely first ADR candidates

Only as implementation evidence requires them:

- reference implementation language/runtime and repository/package structure;
- durable persistence and migration strategy;
- identifier wire encoding if exposed outside the process;
- authorization enforcement mechanism;
- tenant-isolation implementation strategy;
- durable Event/evidence consistency mechanism;
- public Product Contract/API serialization and validation tooling;
- secrets/key-management integration;
- observability backend and trace propagation;
- retrieval/index technology.

The list is predictive, not a requirement to create every ADR.

## 12. Architecture fitness matrix for the first slice

The first executable slice SHOULD carry tests equivalent to the following minimum matrix.

| Source | Minimum executable evidence |
|---|---|
| RFC-0001 | significant governed objects use canonical semantics; consequential canonical mutation cannot bypass Governed Execution; product boundary remains explicit |
| RFC-0002 | stable Subject Identity; distinct immutable Version Identities; single lineage; head/effective distinction represented; version-aware relationships; Event append-only; terminal execution sealing when exercised |
| RFC-0003 | Organization scope explicit; deny-by-default authorization; authz distinct from Organizational Authority; unresolved scope fails closed; no cross-Organization ambient access |
| RFC-0004 | minimal Provisional Product Contract can be represented/validated; no hidden internal platform dependency; contract registration grants no permission |
| RFC-0005 | exact Workflow/material input version pinning; canonical mutation gate; side-effect classification; retry/idempotency/uncertainty behavior where exercised |
| RFC-0006 | receipt/admission distinction; immutable Event identity; duplicate/replay safety; provenance/causation references; telemetry is non-canonical |
| RFC-0007 | Observation/Memory/Candidate/Knowledge roles remain distinct; no silent promotion; exact Knowledge version required when consequential reliance is later exercised; projections remain non-authoritative |

The full conformance suites of RFC-0001 through RFC-0007 remain authoritative. This matrix only defines the minimum first-slice evidence and does not narrow higher-level requirements.

## 13. Security and privacy bootstrap rules

The bounded first slice MUST start with the following structural controls even before a mature IAM or security stack exists:

- explicit Organization scope on governed state and execution;
- no default tenant fallback;
- deny-by-default authorization interface;
- distinct Organizational Authority / approval references;
- attributable human/service/AI actor identity where operationally significant;
- no reusable secrets in canonical records, events, logs, prompts or fixtures;
- data minimization in execution evidence and provenance;
- derived/indexed representations inherit Organization and handling constraints;
- cross-Organization access disabled unless explicitly modeled and authorized;
- fail-closed behavior for unresolved security/governance decisions affecting consequential mutation.

Manual/local implementations are acceptable only when they preserve these semantics and remain bounded and reviewable.

## 14. Product entry point

A product experiment remains entirely product-local when it does not consume Platform Capabilities, shared platform history or canonical platform state.

When a product first interacts with the reference implementation's governed platform boundary, create a minimal `Provisional` Product Contract before governed reliance.

The first real Product Contract SHOULD be driven by an actual product integration rather than invented as a universal example.

The reference implementation MUST NOT import tender, procurement, finance, CRM, legal, marketing or another product-domain model into shared Kernel/platform modules merely to demonstrate functionality.

## 15. Operational and commercial boundary

Reference implementation readiness is not operational readiness.

At this stage:

- no implementation capability is `Active` merely because the reference tests pass;
- no production environment is implied;
- no SLA, support, compatibility or portability promise is created;
- no external full-platform conformance claim is authorized;
- the Proposed Decision Authority Policy is not treated as approved;
- an operational-readiness standard or equivalent approved process remains required before the first capability can become `Active` under RFC-0001.

## 16. Exit evidence for Roadmap Block 0H

Block 0H may be marked complete when all of the following are true:

1. Constitution `1.2.0` and RFC-0001 through RFC-0007 `1.0.0` are verified as current Accepted foundations;
2. the Architecture Glossary is synchronized to those Accepted definitions sufficiently for implementation navigation;
3. the logical reference implementation structure is explicit and does not imply speculative service topology;
4. the first executable slice and minimum architecture fitness evidence are defined;
5. unresolved technology choices are listed as provisional/deferred and have ADR triggers;
6. no speculative ADR is required before bootstrap;
7. Product Contract entry conditions are explicit;
8. security/privacy/authority bootstrap constraints are explicit;
9. functional cross-review finds no remaining material objection for the readiness stage;
10. the canonical roadmap is synchronized after publication.

## 17. Deferred decisions

The following remain intentionally unresolved until implementation or product evidence requires a decision:

- programming language/runtime;
- package/repository layout;
- durable persistence and migration tooling;
- identifier wire syntax;
- public API/transport protocol;
- event broker/outbox/inbox technology;
- authentication provider and authorization implementation;
- tenant isolation physical controls;
- cryptographic integrity/signature mechanism;
- secrets management;
- workflow/orchestration runtime;
- observability stack;
- Memory/Knowledge persistence;
- vector/lexical/graph retrieval;
- model/provider integrations;
- deployment topology;
- concrete operational-readiness controls;
- product-specific Product Contracts and domain schemas.

Deferring these choices is deliberate. It preserves the Accepted technology-independent architecture while allowing the first executable implementation to begin immediately.

## 18. Change rule

If implementation discovers a cross-cutting semantic gap not already covered by an Accepted RFC, implementation MUST stop short of encoding that gap as de facto platform architecture.

Use the lowest sufficient governance artifact:

- implementation/configuration for local reversible detail;
- ADR for a concrete architecture/technology choice;
- standard/catalog for reusable subordinate semantics;
- Product Contract for product/platform interaction;
- RFC only for a material shared architecture/governance/product-contract decision that cannot be resolved at a lower level.

No implementation artifact may silently amend the Constitution or an Accepted RFC.