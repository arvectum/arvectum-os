# RFC-0001: Arvectum OS Architecture

Status: `Accepted`
Version: `1.0.0`
Created: `2026-08-06`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Supersedes: `RFC-0001 v0.9.0`
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS is an operating system for organizational intelligence and a shared operational foundation through which people, AI systems and software work together.

Artificial intelligence is a means of execution, not the purpose or authority source of the platform.

Arvectum OS exists to preserve, structure, govern, operationalize and continuously improve organizational knowledge, experience, standards, workflows, decisions, relationships and institutional memory.

Its business purpose is to create organizational leverage: each validated product, workflow and improvement should make future work faster, safer, more explainable and less expensive without forcing premature platform complexity.

The core architectural asset maintained by Arvectum OS is an **Executable Organizational Model**: a durable and governed representation of organizational intelligence through identities, records, relationships, authority, workflows, evidence and operational history.

Arvectum OS is governed by three architectural laws:

1. **Every significant governed object managed by Arvectum OS has a Canonical Record.**
2. **Arvectum OS represents operationally relevant organizational context as a Graph of Records and Relationships.**
3. **Consequential changes to canonical state managed by Arvectum OS occur through Governed Execution.**

The permanent Platform Kernel is deliberately small. It defines five semantic primitives:

- Identity;
- Canonical Record;
- Typed Relationship;
- Event;
- Execution Context.

The precise metamodel relationships among these primitives are intentionally provisional until RFC-0002. No implementation may make an irreversible cross-cutting schema commitment that prejudges RFC-0002 without an approved architectural decision.

Everything else is a capability implemented above the Kernel and allowed to evolve independently.

This RFC defines the enduring system model. It does not freeze a service list, deployment topology, technology stack, commercial delivery model or product portfolio.

## 2. Constitutional Basis

This RFC implements the Constitution of Arvectum OS version `1.2.0`.

The most relevant constitutional requirements are:

- organizational intelligence is a compounding strategic asset;
- AI is an execution means rather than the purpose of the platform;
- shared capabilities enter the platform through validated reuse, strategic necessity or universal governance requirements;
- bounded and reversible product experiments may precede platform generalization;
- shared platform foundations and contracts remain domain-neutral;
- authoritative organizational knowledge has one canonical source;
- organizational data, intelligence and history remain governed, portable and accessible to the organization;
- security, privacy, least privilege, isolation, minimization, retention, deletion and auditability are structural properties;
- decisions, workflows, events and outputs use controls proportionate to consequence and maturity;
- governed organizational assets are versioned, discoverable, attributable and reusable;
- transient outputs do not automatically become permanent organizational assets;
- architecture precedes irreversible or cross-cutting implementation, not every bounded experiment;
- technologies may change while contracts and organizational assets remain understandable and portable;
- validated improvements become reusable when doing so creates organizational value.

Where this RFC is ambiguous, the Constitution prevails.

### 2.1 Normative Status

This RFC contains normative architectural requirements and informative strategic guidance.

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** mean:

- **MUST** or **MUST NOT** — mandatory for conformance unless an approved architectural exception explicitly applies;
- **SHOULD** or **SHOULD NOT** — the default expectation; deviation requires recorded rationale proportionate to impact;
- **MAY** — permitted but not required.

Lower-case uses of “must”, “should” and “may” in explanatory prose do not create additional normative force.

The following parts are normative:

- the three architectural laws;
- the Platform Kernel, provisional metamodel constraint and admission rules;
- authority modes for Canonical Records;
- Product Experiment, Platform Capability and Platform Service boundaries;
- Product Contract and dependency rules;
- commercial-commitment integrity rules;
- security, privacy, isolation, sovereignty and portability invariants;
- decision-authority and architectural-exception rules;
- operational-readiness requirements for `Active` capabilities;
- extension and AI authority constraints;
- the scoped conformance model and fitness tests;
- acceptance and approval requirements.

The following parts are informative unless a statement explicitly uses a capitalized normative keyword:

- Founder Thesis and Business Outcomes;
- examples and diagrams;
- Platform Gravity indicators;
- delivery and technology recommendations;
- Platform Evidence examples;
- risks, mitigations and consequences;
- the sequence of follow-up documents.

Informative content explains intent and supports decision-making. It does not by itself create a stable public contract.

## 3. Founder Thesis

Arvectum OS is justified only if it creates compounding organizational and commercial advantage.

The intended compounding loop is:

```text
Valuable Products and Workflows
             ↓
Governed Executions and Outcomes
             ↓
Lawfully Retained Operational Evidence
             ↓
Validated Knowledge, Standards and Patterns
             ↓
Reusable Contracts and Platform Capabilities
             ↓
Faster, Safer and Cheaper Future Work
             ↓
Valuable Products and Workflows
```

Compounding may occur through reusable mechanisms, contracts, schemas, controls, methods and knowledge for which reuse is legally and contractually permitted.

Customer data, evidence, memory and organizational intelligence do not become shared platform assets merely because they were processed by Arvectum OS. Cross-organization reuse requires explicit rights, classification, policy and governance.

The architecture should optimize for:

- organizational value over ceremony;
- validated reuse over speculative generality;
- controlled accumulation of organizational intelligence;
- lower marginal cost of launching products and workflows;
- lower operational, security and governance risk;
- faster integration of people, software and AI systems;
- explainability of consequential results;
- portability across technologies and vendors;
- customer control over organizational assets;
- bounded experimentation and rapid learning;
- removal of platform responsibilities that fail to create value.

No component belongs in the platform merely because it is technically elegant.

## 4. Business Outcomes

Arvectum OS should enable ООО «Арвектум» and organizations using the platform to:

1. build multiple products on one shared operational foundation where reuse is validated;
2. preserve organizational intelligence independently of individual employees, chats, models and vendors;
3. reconstruct how and why consequential results were produced;
4. introduce automation without granting undeclared authority;
5. improve standards and workflows through evidence and controlled approval;
6. maintain clear architectural responsibility and permitted use of platform, product and customer knowledge;
7. detect incompatible contracts and dependencies before consequential execution;
8. export, migrate and delete organizational data and assets under governed rules;
9. integrate with external systems of record without creating competing sources of truth;
10. replace technologies without losing organizational meaning or history;
11. prove that platform investment creates measurable leverage rather than architecture overhead.

## 5. Non-goals

This RFC does not define:

- tender, marketing, legal, financial or other domain-specific behavior;
- the complete list of platform capabilities or services;
- detailed schemas for individual record types;
- the final metamodel inheritance or composition relations among Kernel primitives;
- a final microservice topology;
- a programming language, framework, database or message broker;
- a particular AI model or inference runtime;
- detailed identity, cryptography, retention or privacy mechanisms;
- user interface design;
- pricing, packaging or go-to-market strategy;
- the internal architecture of a specific product;
- legal title, intellectual-property ownership, licensing terms or contractual data rights;
- a claim that the organization-specific model is a complete simulation of reality;
- whether Arvectum OS will remain internal, be embedded in products, be deployed for customers or become a standalone offering;
- the complete organizational RACI or employment-role structure of ООО «Арвектум».

These subjects belong to later RFCs, ADRs, product contracts, policies, catalogs, legal agreements or commercial decisions.

## 6. Organizational Intelligence and the Executable Organizational Model

### 6.1 Organizational Intelligence

Organizational intelligence is accumulated knowledge, operational experience, standards, workflows, decisions, relationships and institutional memory that strengthen future work.

Arvectum OS does not acquire legal ownership of organizational intelligence merely by processing or governing it. It preserves and operationalizes the portion that an organization is entitled and chooses to govern through the platform.

### 6.2 Executable Organizational Model

The Executable Organizational Model is the governed representation of organizational intelligence through:

- organizational identities and authority;
- Canonical Records and immutable versions;
- typed relationships;
- governed organizational assets;
- standards and policies;
- workflows and execution history;
- decisions and approvals;
- memory and validated knowledge;
- documents and artifacts;
- events, evidence and provenance;
- product and extension contracts.

It is **executable** because governed workflows can act on the model and produce records, events and artifacts.

It is **organizational** because meaning and authority come from the organization, applicable contracts and governance—not from a database, model provider or framework.

It is a **model** because it represents selected operational reality. It must expose scope, freshness, uncertainty, provenance and known gaps where relevant.

### 6.3 Organization-specific Model Instance

Each organization has an isolated organization-specific instance or view of the Executable Organizational Model.

The descriptive term **Organizational Twin** may be used for this instance, but it is informative rather than a separate Kernel primitive or promise of completeness, real-time simulation or autonomous management.

Normative requirements in this RFC apply to the organization-specific model instance regardless of commercial terminology.

### 6.4 Organizational Semantics

Arvectum OS follows this rule:

> **The organization defines meaning. Products specialize meaning. Technologies execute meaning.**

Consequences:

- the organization governs canonical definitions, authority and approved operating rules;
- products add domain interpretation and commercial behavior;
- platform capabilities preserve and execute shared organizational semantics;
- technology implementations do not become independent sources of organizational truth;
- AI systems may interpret and generate, but do not determine authority or canonical meaning.

### 6.5 Architectural Responsibility and Legal Rights

**Architectural responsibility** means responsibility for canonical state, lifecycle, contracts, validation, change control and operational support within Arvectum OS.

Architectural responsibility does not determine:

- legal title;
- intellectual-property ownership;
- licensing rights;
- confidentiality obligations;
- contractual data rights;
- controller, processor or similar legal roles.

Those rights and obligations are determined by applicable law and contract.

## 7. Canonical Records, Authority Modes, Organizational Assets and Transient Outputs

### 7.1 Law One: Every Significant Governed Object Has a Canonical Record

Every significant governed object managed by Arvectum OS **MUST** have one Canonical Record within its declared scope and type.

A Canonical Record is authoritative about how Arvectum OS identifies, scopes, governs and references the object. It does not necessarily make Arvectum OS the originating system of record for every underlying fact.

Every Canonical Record **MUST** declare one authority mode:

- `Native` — Arvectum OS is the authoritative source for the governed object;
- `External Reference` — an external system remains authoritative and Arvectum OS stores a governed identity, reference and access or retrieval contract;
- `Governed Replica` — an external system remains authoritative while Arvectum OS stores a synchronized governed representation under an explicit synchronization contract.

When an external system remains authoritative, Arvectum OS **MUST** identify the external authority and **MUST NOT** create a competing authoritative source for the same scope.

An `External Reference` or `Governed Replica` **MUST** declare, where applicable:

- external system and object identity;
- authority scope;
- synchronization or retrieval mechanism;
- freshness and latency expectations;
- conflict-resolution rule;
- failure and unavailability behavior;
- provenance;
- permitted local transformations;
- retention, deletion and portability obligations.

Every Canonical Record **MUST** have an immutable version identity.

A changeable native or replicated object **MUST** use a stable object identity and a sequence of immutable versions within Arvectum OS.

An event or another immutable observation is normally a single-version governed object. Corrections, reversals and compensations **MUST** create additional linked objects rather than mutate history.

A record is significant when it materially affects organizational meaning, authority, production behavior, external commitments, financial or legal position, security, safety, reputation, canonical state, a reusable asset or reconstruction of a consequential result.

A significant Canonical Record **MUST** expose, directly or by reference:

- stable object identity where applicable;
- immutable version identity;
- authority mode and authoritative source;
- semantic type and schema version;
- accountable architectural owner;
- organization or tenant scope;
- lifecycle and validation status;
- creation actor and time;
- effective period where applicable;
- provenance;
- typed relationships;
- supersession history where applicable;
- classification and access constraints;
- retention and deletion policy references where applicable;
- integrity metadata.

Mutable projections, caches and indexes **MAY** exist for convenience. They **MUST NOT** become independent authorities.

### 7.2 Governed Organizational Asset

A record or artifact becomes a **Governed Organizational Asset** only when it is explicitly designated as authoritative, reusable, evidentiary or operationally significant.

Governed Organizational Assets **MUST** be discoverable, attributable, versioned at a level proportionate to their importance, and reusable only under applicable permissions, classifications, rights and policies.

### 7.3 Transient and Experimental Outputs

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

Transient and experimental objects **MAY** use lighter versioning, observability and retention when their status, scope, owner, risk, retention and promotion or deletion path are explicit.

A transient output **MUST NOT** become validated knowledge, organizational memory or a permanent asset automatically.

### 7.4 Law Two: Operational Context Is a Graph

Arvectum OS **MUST** represent operationally relevant organizational context as Canonical Records connected through explicit, typed relationships.

Relationships **MUST** be typed, directionally meaningful, attributable and traceable, and **MUST** be version-aware where required.

The graph supports context resolution, explainability, impact analysis, governance, search, dependency resolution and reconstruction.

The graph model does not require a graph database.

### 7.5 Law Three: Consequential Canonical Change Requires Governed Execution

Consequential changes to canonical state managed by Arvectum OS **MUST** occur through an explicit Execution Context and an authorized operation.

Governed Execution **MUST** identify, where applicable:

- organization or tenant;
- initiating actor;
- authority and delegated authority;
- product and Product Contract;
- workflow and version;
- input records and versions;
- external authoritative sources and synchronization state;
- standards and policies;
- knowledge and memory used;
- deterministic and AI components;
- validation and approval requirements;
- outputs and artifacts;
- emitted events;
- correlation and causation;
- classification, retention and reproducibility constraints.

Controls **MUST** be proportionate to consequence, reversibility, data sensitivity, threat and external impact.

No AI system, product or technical service obtains organizational authority merely because it can technically perform an action.

## 8. Governed Learning Loop

Arvectum OS enables organizations to learn without allowing production behavior to mutate silently.

```text
Governed Execution
        ↓
Events and Outcomes
        ↓
Observations
        ↓
Organizational Memory
        ↓
Knowledge or Improvement Proposal
        ↓
Validation, Rights Review and Approval
        ↓
Approved Knowledge / Standard / Policy / Workflow Version
        ↓
Future Governed Execution
```

Promotion **MUST** verify provenance, architectural responsibility, rights, classification and permitted reuse. Learning mechanisms **MAY** propose changes but **MUST NOT** silently activate them.

## 9. System Model

```text
Organizational Actors
People · External Systems · Services · AI Systems
                ↓
Product Layer
Domain meaning · Workflows · Knowledge · UX · Integrations
                │
                ├── Product-local Experiment
                │   No platform contract required
                │
                └── Platform interaction or canonical-state access
                    Minimal Provisional Product Contract required
                                ↓
                    Platform Capability Contracts
                                ↓
                         Platform Kernel
Identity · Canonical Record · Relationship · Event · Execution Context
                                ↓
                    Technology Adapter Contracts
                                ↓
                     Technologies and External Systems
```

External systems of record may remain authoritative through `External Reference` or `Governed Replica` authority modes.

Security, privacy, isolation, portability and governance constrain every layer.

The diagram is informative. Normative experiment, authority and contract rules are defined in Sections 7, 11 and 13.

## 10. Platform Kernel

### 10.1 Purpose

The Kernel is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

### 10.2 Kernel Primitives

#### Identity

Stable reference to organizations, actors, products, governed objects, executions, events and extensions.

#### Canonical Record

The governed representation of an object or immutable observation at a specific version, including its authority mode and authoritative source.

#### Typed Relationship

A governed connection between identities or record versions with explicit semantics and provenance.

#### Event

An append-only observation that something meaningful occurred.

#### Execution Context

The governed execution envelope binding an operation to organization, actor, authority, product, workflow, inputs, controls, components and outputs.

### 10.3 Provisional Kernel Metamodel

This RFC defines the semantics of the five Kernel primitives but does not finalize whether each primitive is:

- a specialization of Canonical Record;
- a governed envelope represented by a Canonical Record;
- an independently persisted primitive linked to Canonical Records;
- or a combination of these patterns.

RFC-0002 **MUST** define:

- identity and version semantics for every primitive;
- whether Event is a Canonical Record subtype or is represented by one;
- whether Execution Context is a Canonical Record subtype, governed envelope or related record set;
- whether Typed Relationship has independent identity and versioning;
- preservation and lifecycle requirements for completed Execution Contexts;
- compatibility and migration rules for provisional implementations.

Before RFC-0002 is accepted:

- implementations **MUST** mark these metamodel relations `Provisional`;
- implementations **MUST** preserve enough separation to migrate between plausible models;
- implementations **MUST NOT** publish an irreversible public contract that fixes one metamodel interpretation without an approved RFC or ADR;
- reversible internal representations **MAY** proceed in parallel with RFC-0002.

### 10.4 Kernel Admission Test

A concept **MAY** enter the Kernel only when all are true:

1. every product or platform capability depends on it directly or indirectly;
2. inconsistent implementations would break platform integrity;
3. its semantics are domain-neutral;
4. it must remain stable across technology changes;
5. it cannot safely remain an optional capability or extension.

A failed criterion means the concept belongs above the Kernel.

### 10.5 Kernel Exclusions

The Kernel **MUST NOT** contain domain rules, prompts, ontologies, scoring, business workflows, templates, user interfaces, model-specific behavior, database-specific behavior, approval policy, knowledge validation logic or document-generation logic.

A backward-incompatible Kernel change **MUST** be approved through an RFC.

## 11. Product Experiments, Capabilities and Services

### 11.1 Product Experiment

A **Product Experiment** is a bounded and reversible implementation under the architectural responsibility of a product or operational sponsor while uncertainty is high.

A Product Experiment:

- **MAY** contain domain-specific logic;
- **MUST NOT** be represented as a shared platform guarantee;
- **MAY** use lighter documentation and versioning proportionate to risk;
- **MUST NOT** bypass security, privacy, legal, contractual, data-integrity or governance controls;
- **MUST** have an owner, scope, effort or budget bound, review date and explicit path to promotion, containment or retirement.

A Product Experiment that remains entirely product-local and neither consumes platform capabilities nor reads or changes canonical platform state **MAY** operate without a Product Contract.

A Product Experiment that consumes a platform capability, emits events into shared platform history, or reads or changes canonical platform state **MUST** use a minimal `Provisional` Product Contract proportionate to the interaction.

A Product Experiment remains product-responsible until a separate decision promotes a reusable pattern into platform incubation.

### 11.2 Platform Capability

A **Platform Capability** is a reusable, domain-neutral organizational ability exposed by Arvectum OS to products or other capabilities.

#### Candidate

A `Candidate` capability **MUST** declare:

- proposed organizational outcome;
- accountable architectural owner;
- sponsor or constitutional rationale;
- intended domain-neutral boundary;
- expected consumers or strategic need;
- reuse hypothesis;
- review date;
- criteria for incubation, containment or rejection.

A `Candidate` does not require an implemented contract or implementation commitment.

#### Incubating

An `Incubating` capability **MUST** additionally declare:

- source Product Experiment or organizational need;
- sponsoring consumers;
- bounded scope and budget;
- a `Provisional` domain-neutral contract;
- Canonical Record and authority-mode responsibilities;
- dependencies and emitted events;
- security, authority and data-handling rules;
- portability, compatibility and migration requirements;
- promotion, return-to-product, replacement and retirement criteria.

#### Active

An `Active` capability **MUST** have:

- a supported stable public contract;
- declared compatibility and migration policy;
- accountable operational support;
- approved operational readiness proportionate to scope, consequence and customer commitments;
- measurable evidence appropriate to platform responsibility;
- maintained security, portability and lifecycle obligations.

Operational readiness **MUST** identify, where applicable:

- support responsibility and escalation path;
- observability and health evidence;
- incident and recovery path;
- continuity and dependency assumptions;
- backup, reconstruction or restoration path proportionate to governed state;
- migration and deprecation communication responsibilities;
- customer-facing operational commitments that the capability is expected to satisfy.

### 11.3 Active Capability Admission

A capability **MAY** become `Active` only when at least one strategic condition is met:

1. two or more real consumers require it;
2. it implements a constitutional or Kernel-level invariant;
3. an approved decision shows a credible near-term second consumer and lower total cost than later duplication and migration;
4. it is strategically required for governance, security, identity, provenance, portability or interoperability.

It **MUST** also materially improve product speed, cost, quality, risk, explainability, governance, portability or integration.

A capability **MUST NOT** become `Active` until the applicable operational-readiness evidence has been reviewed and approved by the decision authority responsible for the affected operational and customer scope.

### 11.4 Capability Lifecycle and Exit

```text
Candidate → Incubating → Active → Deprecated → Retired
```

Platform responsibility is reversible.

A capability **MUST** be simplified, returned to a product, replaced, deprecated or retired when evidence no longer supports centralized platform responsibility.

Required history, contractual obligations, exportability and migration paths **MUST** be preserved.

### 11.5 Platform Service

A Platform Service is an implementation and architectural-responsibility boundary that realizes one or more capabilities.

It is not necessarily a separate process, network service, repository or deployment.

## 12. Product Boundary

Products are architecturally responsible for domain concepts, schemas, knowledge, workflows, validators, standards, risk rules, templates, agents, integrations, user experience, commercial packaging and Product Experiments before platform promotion.

The platform is architecturally responsible for domain-neutral shared foundations, contracts and validated capabilities.

A product **MUST NOT** indefinitely duplicate an `Active` platform capability without an approved exception.

The platform **MUST NOT** absorb product logic merely to appear comprehensive.

## 13. Product Contracts

A Product Contract is the versioned boundary between a product and Arvectum OS.

A stable or provisional Product Contract **MUST** declare, where applicable:

- product or experiment identity, version and architectural owner;
- required capabilities and compatible versions;
- domain record and relationship types;
- Canonical Record authority modes and authoritative systems;
- schemas and workflows;
- validators, standards and policies;
- event and artifact types;
- permissions, classifications and authority requirements;
- approval gates;
- extensions and adapters;
- portability and export obligations;
- retention and deletion responsibilities;
- migration and support status;
- `Provisional` or `Incubating` dependencies.

Products and experiments **MUST NOT** access platform internals through undocumented conventions, direct database coupling or internal imports that bypass declared contracts.

## 14. Commercial Commitment Integrity

Commercial language and external commitments **MUST** reflect the approved architectural and conformance state of Arvectum OS.

Commercial proposals, customer contracts, statements of work, service descriptions, sales commitments, marketing claims and other externally relied-upon representations **MUST NOT**:

- represent a Product Experiment, `Candidate` or `Incubating` capability as an `Active` supported platform capability;
- claim a conformance scope or maturity broader than an approved Conformance Statement;
- create a stable platform obligation, compatibility promise, portability promise, support commitment or customer-facing operational guarantee that has not been approved by the applicable decision authority;
- imply legal rights to customer data, organizational intelligence or shared reuse beyond applicable law and contract;
- describe an informative concept, exploratory inventory item or roadmap hypothesis as a delivered contractual capability.

A commercial commitment that materially changes platform obligations, supported contracts, conformance scope, security or portability expectations, or operational commitments **MUST** be reviewed by the decision authority responsible for the affected scope before it becomes binding.

Commercial commitments **MAY** describe bounded pilots and Product Experiments when their lifecycle, limitations, support expectations and non-production or provisional status are represented accurately.

## 15. Dependency Rules

Mandatory rules:

1. Kernel **MUST NOT** depend on capabilities, services or products.
2. Shared capabilities **MUST NOT** contain product-domain behavior.
3. Products **MUST** depend on platform behavior only through declared contracts.
4. Products **MUST NOT** access each other's internals.
5. Cross-product interaction **MUST** use records, events or explicit contracts.
6. Technologies **MUST NOT** define organizational semantics.
7. External systems of record **MUST** be represented through declared authority modes and contracts.
8. Internal implementation details **MUST NOT** become accidental public interfaces.
9. Circular architectural-responsibility dependencies are prohibited.
10. Security and tenant boundaries **MUST** apply across all dependency paths.
11. Exceptions **MUST** record scope, proposer, decision authority, rationale, review or expiry date and exit plan.

## 16. Decision Authority and Architectural Exceptions

Every governed decision **MUST** identify:

- decision subject and scope;
- proposer;
- accountable decision authority;
- rationale and evidence proportionate to impact;
- effective date;
- review, expiry or supersession condition where applicable;
- canonical decision reference.

The decision authority **MUST** have authority over the affected scope and sufficient independence to evaluate the proposal.

A proposer **MUST NOT** solely approve their own decision when it creates one or more of the following:

- material security, privacy, legal, financial, safety or reputational risk;
- a shared-platform obligation;
- a new `Active` capability;
- a backward-incompatible public contract or Kernel change;
- a material customer-facing commercial or operational commitment;
- cross-organization data access or knowledge reuse;
- acceptance of a material known gap;
- a production architectural exception with external impact.

Self-approval **MAY** be permitted for low-risk, reversible, product-local decisions only when an approved governance policy explicitly delegates that authority and defines its limits.

At minimum:

- the owner of Arvectum OS approves this RFC, constitutional changes and irreversible changes to the fundamental platform model;
- an authorized platform decision authority approves promotion to `Active`, material shared-platform exceptions and stable public-contract changes;
- an authorized product decision authority may approve bounded product-local experiments within delegated risk and budget limits;
- a conformance approver **MUST NOT** approve a material exception they proposed unless a higher authority explicitly reviews and approves it.

A separate governance policy **MUST** define the current authority matrix, delegation limits, escalation paths and substitute approvers before the first `Active` capability or external production conformance claim.

The absence of a named employee or role-holder does not suspend governance. The owner retains residual decision authority until authority is explicitly delegated.

## 17. Structural Security, Privacy and Isolation

The following invariants apply to platform capabilities, products, experiments, workflows, extensions and adapters:

1. Access **MUST** be denied by default and require explicit authorization.
2. Actors and components **MUST** receive least privilege.
3. Governed records, relationships, executions and artifacts **MUST** have an organization scope unless explicitly classified and authorized as shared.
4. Collection, retrieval and propagation **MUST** be limited to data required for the declared purpose.
5. Storage, retrieval, logging, generation and export **MUST** respect classification, rights and permitted use.
6. Governed data **MUST** have an applicable retention or deletion rule where required.
7. Consequential access and change to sensitive or canonical state **MUST** be attributable and observable.
8. Rigor **MUST** reflect sensitivity, consequence, reversibility and threat.
9. Product Experiments **MUST NOT** bypass applicable security, privacy, legal or contractual controls.
10. Failure behavior **MUST NOT** silently broaden access, cross tenant boundaries or lose required evidence.

## 18. Organizational Control, Portability and Lifecycle

Arvectum OS **MUST** support governed export, migration, retention, deletion, service termination and handover within the applicable conformance scope.

A governed export **MUST** preserve, where applicable, identities, versions, authority modes, external-source references, schemas, relationships, provenance, classifications, workflow history, decision history, event history and lawful artifact content or references.

A manual, documented and tested process **MAY** satisfy an early-stage portability or deletion requirement when proportionate to scope and risk.

Organizational continuity **MUST NOT** depend on an inaccessible proprietary representation or a specific employee, AI system, vendor or runtime.

## 19. Organizational and Tenant Sovereignty

Unless an explicit contract and policy state otherwise:

- records and relationships **MUST** be scoped to and governed within one organization;
- authority **MUST** be evaluated within that organization;
- one organization's data **MUST NOT** alter another organization's canonical model;
- cross-organization access **MUST** be denied by default;
- customer evidence, memory and knowledge **MUST NOT** be promoted into shared platform knowledge automatically;
- cross-organization learning **MUST** require explicit rights, classification and governance;
- shared knowledge **MUST** identify architectural owner, source rights and permitted use.

## 20. Extension Model

Arvectum OS **MAY** be extended through registered and versioned products, agents, workflows, schemas, validators, templates, policies, connectors, tools, adapters and UI modules.

Every extension **MUST** declare identity, version, architectural owner, required contracts, compatibility, tenant scope, permissions, data handling, inputs, outputs, events, failure behavior, portability and deprecation rules proportionate to lifecycle and conformance scope.

Extensions **MUST NOT** weaken Kernel, security, sovereignty or governance invariants.

## 21. AI Components

AI is an execution capability, not an authority source or canonical source by default.

AI systems **MAY** analyze, retrieve, classify, recommend, draft, transform, generate and propose improvements.

They **MUST NOT** silently change approved standards, grant permissions, approve consequential decisions, replace Canonical Records, promote observations to validated knowledge, share data across organizations, extend retention or bypass validation, security or approval gates.

For consequential operations the platform **MUST** identify relevant model or component reference, instructions, retrieval sources, tool access, settings, validation and approval state within the declared conformance scope.

## 22. Platform Gravity

The platform should be easier to reuse than to replace.

Weak Platform Gravity appears when products repeatedly bypass contracts, integration is slower than local implementation, abstractions remain single-product beyond incubation, the platform becomes a bottleneck or duplicate shared foundations emerge.

Weak Platform Gravity may justify redesign or de-platformization. It is not grounds for coercive adoption.

## 23. Delivery and Technology Strategy

Arvectum OS should be built through real organizational and product demand.

The first vertical spine should include only what one real consequential workflow requires to demonstrate Canonical Records, Execution Context, provenance, proportionate controls, a reproducible artifact and a credible path to reuse.

The initial implementation should prefer a modular monolith unless evidence requires distribution.

Commodity infrastructure should normally be adopted, integrated or purchased rather than recreated.

RFCs, ADRs, Product Experiments and MVP implementation may proceed in parallel when implementation is bounded and reversible, provisional boundaries are documented, security and governance remain intact, and the work has an owner, review date and exit path.

Before an irreversible cross-cutting commitment becomes binding, the relevant RFC or ADR must be approved.

## 24. Scoped Conformance Model

Conformance is evaluated against a declared scope, not every possible future capability of Arvectum OS.

Any implementation, pilot, deployment or capability claiming conformance **MUST** maintain a Conformance Statement that separately identifies:

### Subject lifecycle

One of:

- `Product Experiment`;
- `Candidate`;
- `Incubating`;
- `Active`;
- `Deprecated`;
- `Retired`;
- `Not Applicable` for a subject that is not a capability or experiment.

### Operational environment

One or more of:

- `Local`;
- `Development`;
- `Test`;
- `Pilot`;
- `Production`.

### Conformance maturity

One of:

- `Draft` — assessment incomplete;
- `Provisional` — applicable invariants are addressed through bounded, manual or provisional controls;
- `Scoped` — assessed and conformant within the declared scope;
- `Scoped with Exceptions` — conformant within scope subject to approved exceptions;
- `Not Conformant`.

The Conformance Statement **MUST** also identify:

- subject and version being assessed;
- organization, tenant and deployment scope;
- workflows and capabilities in scope;
- data classes, sensitivity and risk level;
- Canonical Record authority modes and external systems involved;
- applicable normative sections;
- requirements declared not applicable, with rationale;
- manual or provisional controls;
- architectural exceptions and their decision authorities;
- known gaps and remediation owner;
- assessment owner and independent approver where required;
- operational-readiness evidence where lifecycle is `Active`;
- applicable customer-facing commitments and their canonical references where external commitments exist;
- review date and reassessment triggers.

A requirement **MAY** be declared not applicable only when the subject does not perform, store, govern or expose the addressed behavior or data.

An implementation **MUST NOT** claim full-platform conformance when only a limited scope has been assessed.

## 25. Architectural Fitness Tests

The fitness tests are normative within the scope declared by a Conformance Statement.

A conforming subject **MUST** be able to answer positively, where applicable:

1. Does every significant governed object have one Canonical Record within scope?
2. Is the authority mode explicit?
3. Are competing sources of truth prevented?
4. Are versions immutable and events append-only?
5. Are governed assets and transient outputs distinguishable?
6. Are relationships explicit, typed and traceable?
7. Does consequential canonical change have an Execution Context?
8. Can a consequential output be reconstructed?
9. Does the platform avoid product-domain behavior?
10. Can a product-local experiment avoid unnecessary platform ceremony?
11. Does platform interaction use a proportionate Product Contract?
12. Do capability requirements match lifecycle?
13. Are decision authority and proposer separation adequate for material decisions?
14. Do commercial commitments match approved capability lifecycle, conformance scope and supported contracts?
15. Is operational readiness approved before an `Active` capability is represented as supported?
16. Are security, tenant, classification, retention and deletion rules identifiable?
17. Can prohibited cross-organization use be prevented and audited?
18. Can the organization obtain a usable governed export within scope?
19. Are provisional Kernel metamodel assumptions explicit and migratable?
20. Are lifecycle, environment and conformance maturity recorded separately?
21. Is platform complexity proportionate to maturity, risk and value?
22. Is architectural responsibility distinguishable from legal ownership?
23. Is the platform reducing total cost or risk rather than relocating complexity?

A negative answer indicates non-conformance, an approved exception, a declared gap or an incorrectly scoped claim. The Conformance Statement **MUST** identify which applies.

## 26. Platform Evidence

Platform value should be evaluated through measurable evidence of delivery speed, validated reuse, operating cost, reliability, quality, risk reduction, governance, security, portability, integration effort and de-platformization effort.

Detailed metrics remain informative operating artifacts.

## 27. Risks and Mitigations

### Premature Platformization

Mitigated by Product Experiments, incubation, review dates and admission rules.

### Founder or Executive Bottleneck

Mitigated by explicit delegation and a governance authority matrix while preserving residual owner authority.

### Self-approved Material Risk

Mitigated by proposer/approver separation for material exceptions and decisions.

### Premature Kernel Lock-in

Mitigated by the provisional metamodel constraint and RFC-0002 migration requirements.

### Lifecycle and Environment Confusion

Mitigated by separate lifecycle, operational-environment and conformance-maturity axes.

### Commercial Overcommitment

Mitigated by binding external claims to approved capability lifecycle, supported contracts, Conformance Statements and decision authority.

### Active Without Operational Readiness

Mitigated by requiring operational-readiness approval before promotion to or representation as an `Active` supported capability.

### Contract Ceremony Slowing Experiments

Mitigated by allowing completely product-local experiments without platform contracts.

### Competing Sources of Truth

Mitigated by explicit authority modes and synchronization contracts.

### Security or Privacy Added Too Late

Mitigated by structural invariants applying to every layer.

### Architecture Before Revenue

Mitigated by product pull, bounded experiments, provisional contracts and parallel delivery.

## 28. Consequences

### Positive

- platform and product boundaries remain explicit;
- governance authority is clear enough to prevent both founder bottlenecks and uncontrolled self-approval;
- Kernel semantics are stable without prematurely freezing the persistence metamodel;
- experiments can move quickly without accidental platform commitments;
- commercial claims cannot silently outrun approved platform maturity;
- `Active` means both architecturally admitted and operationally ready for its declared scope;
- capability obligations grow with lifecycle maturity;
- conformance claims distinguish lifecycle from deployment environment;
- external systems may remain authoritative;
- security, portability and customer knowledge governance are structural properties.

### Costs

- decisions and exceptions require explicit authority and evidence;
- externally binding commitments require alignment with approved platform state;
- promotion to `Active` requires operational-readiness evidence;
- provisional Kernel representations require migration discipline;
- Conformance Statements require separate lifecycle and environment tracking;
- Canonical Records, authority modes and provenance create engineering overhead.

These costs are accepted only where they purchase value, control, continuity, evidence or validated reuse.

## 29. Follow-up Documents

Recommended sequence:

1. `RFC-0002 — Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model`;
2. `RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability`;
3. `RFC-0004 — Product Contract, Product Experiment and Extension Model`;
4. `RFC-0005 — Governed Execution and Workflow Model`;
5. `RFC-0006 — Event, Provenance and Observability Model`;
6. `RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`;
7. `RFC-0008 — Document and Artifact Architecture`.

A governance authority policy must be approved before the first `Active` capability or external production conformance claim.

An operational-readiness standard or equivalent approved process must exist before the first `Active` capability.

Implementation ADRs and reversible experiments may proceed in parallel but may not contradict the Constitution or accepted RFCs.

## 30. Acceptance Criteria

This RFC may be accepted only when the owner explicitly approves the following normative decisions:

1. alignment with Constitution `1.2.0`;
2. normative-status model and keyword meanings;
3. the three architectural laws;
4. the five Kernel primitives and provisional metamodel constraint;
5. Canonical Record authority modes;
6. distinction between Canonical Record, Governed Organizational Asset and Transient Output;
7. distinction between Product Experiment and Platform Capability;
8. product-local experiment and Provisional Product Contract rules;
9. lifecycle-specific capability obligations and exit rules;
10. operational-readiness requirement before `Active`;
11. Product Contract and domain boundary;
12. commercial-commitment integrity rules;
13. decision-authority, proposer-separation and exception rules;
14. structural security, privacy, least privilege and tenant-isolation invariants;
15. organizational control, portability and deletion principles;
16. cross-organization rights and reuse constraints;
17. architectural responsibility versus legal ownership;
18. scoped conformance with separate lifecycle, environment and maturity axes;
19. normative fitness tests;
20. formal Approval Record process.

The owner acknowledges, but does not make normative through acceptance, the informative guidance on Founder Thesis, Business Outcomes, Platform Gravity, Build vs Buy, delivery strategy, risks, consequences and follow-up sequence.

## 31. Decision

RFC-0001 is `Accepted` as version `1.0.0`.

The owner approval is recorded in `docs/governance/decisions/DECISION-2026-08-07-RFC-0001-ACCEPTANCE.md`.

No substantive architectural change was introduced between approved proposal `0.9.0` and accepted version `1.0.0`.

## 32. Approval Record

Decision: `Approved`
Decision authority: `ООО «Арвектум»`
Approved by: `Owner of Arvectum OS`
Decision date: `2026-08-07`
Canonical approval reference: `docs/governance/decisions/DECISION-2026-08-07-RFC-0001-ACCEPTANCE.md`

The canonical approval reference identifies an owner-approved record that existed before the repository commit marking this RFC `Accepted`.

The resulting repository commit or release tag is preserved as external repository evidence and is intentionally not embedded as a self-reference inside this document.
