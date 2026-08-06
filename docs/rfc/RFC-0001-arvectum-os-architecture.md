# RFC-0001: Arvectum OS Architecture

Status: `Proposed`
Version: `0.7.0`
Created: `2026-08-06`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Supersedes: `RFC-0001 v0.6.0`
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

The permanent Platform Kernel is deliberately small. It defines only:

- Identity;
- Canonical Record;
- Typed Relationship;
- Event;
- Execution Context.

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
- the Platform Kernel and its admission rules;
- authority modes for canonical records;
- Product Experiment, Platform Capability and Platform Service boundaries;
- Product Contract and dependency rules;
- security, privacy, isolation, sovereignty and portability invariants;
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
- a final microservice topology;
- a programming language, framework, database or message broker;
- a particular AI model or inference runtime;
- detailed identity, cryptography, retention or privacy mechanisms;
- user interface design;
- pricing, packaging or go-to-market strategy;
- the internal architecture of a specific product;
- legal title, intellectual-property ownership, licensing terms or contractual data rights;
- a claim that the organization-specific model is a complete simulation of reality;
- whether Arvectum OS will remain internal, be embedded in products, be deployed for customers or become a standalone offering.

These subjects belong to later RFCs, ADRs, product contracts, policies, catalogs, legal agreements or commercial decisions.

## 6. Organizational Intelligence and the Executable Organizational Model

### 6.1 Organizational Intelligence

Organizational intelligence is accumulated knowledge, operational experience, standards, workflows, decisions, relationships and institutional memory that strengthen future work.

Arvectum OS does not acquire legal ownership of organizational intelligence merely by processing or governing it. It preserves and operationalizes the portion that an organization is entitled and chooses to govern through the platform.

### 6.2 Executable Organizational Model

The Executable Organizational Model is the governed representation of organizational intelligence through:

- organizational identities and authority;
- canonical records and immutable versions;
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

Where this RFC says that a product, platform capability, service or organization is architecturally responsible for an object or behavior, it refers only to the architectural meaning above.

## 7. Canonical Records, Authority Modes, Organizational Assets and Transient Outputs

### 7.1 Law One: Every Significant Governed Object Has a Canonical Record

Every significant governed object managed by Arvectum OS **MUST** have one Canonical Record within its declared scope and type.

A Canonical Record is authoritative about how Arvectum OS identifies, scopes, governs and references the object. It does not necessarily make Arvectum OS the originating system of record for every underlying fact.

Every Canonical Record **MUST** declare one authority mode:

- `Native` — Arvectum OS is the authoritative source for the governed object;
- `External Reference` — an external system remains authoritative and Arvectum OS stores a governed identity, reference and access or retrieval contract;
- `Governed Replica` — an external system remains authoritative while Arvectum OS stores a synchronized governed representation under an explicit synchronization contract.

When an external system remains authoritative, Arvectum OS **MUST** preserve a Canonical Record that identifies the external authority and **MUST NOT** create a competing authoritative source for the same scope.

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

An event or another immutable observation is normally a single-version record. Corrections, reversals and compensations **MUST** create additional linked records rather than mutate history.

A record is significant when it materially affects one or more of:

- organizational meaning;
- authority or access;
- production behavior;
- an external commitment;
- financial, legal, security, safety or reputational position;
- canonical state;
- a reusable or evidentiary asset;
- reconstruction of a consequential result.

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

A record or artifact becomes a **Governed Organizational Asset** only when it is explicitly designated as one or more of:

- authoritative;
- reusable;
- evidentiary;
- operationally significant.

Governed Organizational Assets **MUST** be discoverable, attributable, versioned at a level proportionate to their importance, and reusable only under applicable permissions, classifications, rights and policies.

Examples may include validated knowledge, memory records, standards, workflows, decisions, templates, validation rules, product profiles and operational evidence.

### 7.3 Transient and Experimental Outputs

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

Examples may include drafts, intermediate model outputs, temporary files, exploratory analyses and short-lived experiment data.

Transient and experimental objects **MAY** use lighter versioning, observability and retention when their status, scope, owner, risk, retention and promotion or deletion path are explicit.

A transient output **MUST NOT** become validated knowledge, organizational memory or a permanent asset automatically.

### 7.4 Law Two: Operational Context Is a Graph

Arvectum OS **MUST** represent operationally relevant organizational context as Canonical Records connected through explicit, typed relationships.

The graph is a governed representation inside the platform. It is not a claim that all organizational reality is captured or reducible to a graph.

Examples:

```text
Knowledge        --supported_by------> Evidence
Decision         --uses--------------> Knowledge
Policy           --governs-----------> Workflow
Workflow Run     --produces----------> Artifact Version
Memory           --derived_from------> Event
Asset            --classified_as-----> Confidential
Product          --implements--------> Product Contract
Record           --retained_by-------> Retention Policy
External Record  --authoritative_in--> ERP System
Replica          --synchronized_from-> External Record
```

Relationships **MUST** be typed, directionally meaningful, attributable and traceable, and **MUST** be version-aware where required.

The graph supports context resolution, explainability, impact analysis, governance, search, dependency resolution and reconstruction.

The graph model does not require a graph database.

### 7.5 Law Three: Consequential Canonical Change Requires Governed Execution

Consequential changes to canonical state managed by Arvectum OS **MUST** occur through an explicit Execution Context and an authorized operation.

This law governs changes that Arvectum OS records, performs, approves or treats as canonical. It does not claim to govern every real-world organizational action.

A consequential operation is one that can materially affect:

- canonical state;
- permissions or authority;
- active standards, policies or workflows;
- an external party or commitment;
- financial, legal, security, safety or reputational position;
- a production artifact or decision;
- validated knowledge or another governed asset.

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

The states are distinct:

- an **event** records what was observed;
- an **observation** is an interpreted signal;
- a **memory record** is retained organizational experience;
- a **proposal** is a candidate improvement;
- **validated knowledge** is approved organizational understanding;
- a **standard** defines an approved method;
- a **policy** constrains behavior or acceptance;
- a **workflow** defines a repeatable process.

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
                     Technology and Runtime
Storage · Search · Queues · Models · Files · Authentication · APIs
```

External systems of record may remain authoritative through `External Reference` or `Governed Replica` authority modes.

Security, privacy, isolation, portability and governance constrain every layer. They are not a separate outer layer that can be bypassed.

The diagram is informative. Normative experiment, authority and contract rules are defined in Sections 7, 11 and 13.

## 10. Platform Kernel

### 10.1 Purpose

The Kernel is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

### 10.2 Kernel Primitives

#### Identity

Stable reference to organizations, actors, products, records, executions, events and extensions.

#### Canonical Record

The governed representation of an object or immutable observation at a specific version, including its authority mode and authoritative source.

#### Typed Relationship

A connection between identities or record versions with explicit semantics and provenance.

#### Event

An append-only, normally single-version observation that something meaningful occurred. Corrections create additional events.

#### Execution Context

The semantic anchor binding an operation to organization, actor, authority, product, workflow, inputs, controls, components and outputs.

### 10.3 Kernel Admission Test

A concept **MAY** enter the Kernel only when all are true:

1. every product or platform capability depends on it directly or indirectly;
2. inconsistent implementations would break platform integrity;
3. its semantics are domain-neutral;
4. it must remain stable across technology changes;
5. it cannot safely remain an optional capability or extension.

A failed criterion means the concept belongs above the Kernel.

### 10.4 Kernel Exclusions

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

That provisional contract **MUST** declare at least:

- experiment identity and owner;
- platform capabilities or state accessed;
- authority modes and external systems involved;
- tenant and data scope;
- permissions and authority;
- emitted events and outputs;
- security, retention and deletion obligations;
- review date and exit behavior.

A Product Experiment remains product-responsible until a separate decision promotes a reusable pattern into platform incubation.

### 11.2 Platform Capability

A **Platform Capability** is a reusable, domain-neutral organizational ability exposed by Arvectum OS to products or other capabilities.

Requirements depend on lifecycle:

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
- canonical-record and authority-mode responsibilities;
- dependencies and emitted events;
- security, authority and data-handling rules;
- portability, compatibility and migration requirements;
- promotion, return-to-product, replacement and retirement criteria.

#### Active

An `Active` capability **MUST** have:

- a supported stable public contract;
- declared compatibility and migration policy;
- accountable operational support;
- measurable evidence appropriate to platform responsibility;
- maintained security, portability and lifecycle obligations.

The current inventory belongs in the Capability Catalog.

### 11.3 Active Capability Admission

A capability **MAY** become `Active` only when at least one strategic condition is met:

1. two or more real consumers require it;
2. it implements a constitutional or Kernel-level invariant;
3. an approved decision shows a credible near-term second consumer and lower total cost than later duplication and migration;
4. it is strategically required for governance, security, identity, provenance, portability or interoperability.

It **MUST** also materially improve product speed, cost, quality, risk, explainability, governance, portability or integration.

The admission decision **MUST** consider abstraction, responsibility, migration, security and opportunity costs.

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

Capabilities describe what the platform does. Services describe how implementation responsibility is organized.

## 12. Product Boundary

Products are architecturally responsible for:

- domain concepts and terminology;
- domain schemas and relationships;
- domain knowledge;
- domain workflows and validators;
- domain standards, policies and risk rules;
- domain templates, agents and integrations;
- product user experience;
- commercial packaging and customer value proposition;
- Product Experiments before platform promotion.

The platform is architecturally responsible for domain-neutral shared foundations, contracts and validated capabilities.

A product **MUST NOT** indefinitely duplicate an `Active` platform capability without an approved exception.

The platform **MUST NOT** absorb product logic merely to appear comprehensive.

- **Products must reuse validated shared capabilities before rebuilding.**
- **The platform must earn reuse before centralizing.**
- **Experiments remain product-local until promotion is justified.**

The three statements above summarize intent; enforceable requirements are the capitalized rules in this RFC.

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

A completely product-local experiment is outside this requirement until it interacts with platform capabilities or canonical platform state as defined in Section 11.1.

## 14. Dependency Rules

Permitted direction:

```text
Actors
  ↓
Products
  ├── Product-local Experiment
  │   No platform dependency
  │
  └── Contracted Platform Interaction
      ↓
Provisional or Stable Product Contract
      ↓
Platform Capability Contracts
      ↓
Platform Kernel
      ↓
Technology Adapter Contracts
      ↓
Concrete Technologies and External Systems
```

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
11. Exceptions **MUST** record scope, owner, rationale, review or expiry date and exit plan.

## 15. Structural Security, Privacy and Isolation

Security, privacy, confidentiality and isolation are structural properties of Arvectum OS.

The following invariants apply to platform capabilities, products, experiments, workflows, extensions and adapters:

1. **Deny by default.** Access **MUST** require explicit authorization.
2. **Least privilege.** Actors and components **MUST** receive only the minimum authority required for the declared operation and period.
3. **Tenant isolation.** Every governed record, relationship, execution and artifact **MUST** have an organization scope unless explicitly classified and authorized as shared.
4. **Data minimization.** Collection, retrieval and propagation **MUST** be limited to data required for the declared purpose.
5. **Classification-aware handling.** Storage, retrieval, logging, generation and export **MUST** respect classification, rights and permitted use.
6. **Retention and deletion.** Governed data **MUST** have an applicable retention or deletion rule where required.
7. **Auditability.** Consequential access and change to sensitive or canonical state **MUST** be attributable and observable.
8. **Proportional controls.** Rigor **MUST** reflect sensitivity, consequence, reversibility and threat.
9. **No experimental bypass.** Product Experiments and provisional integrations **MUST NOT** bypass applicable security, privacy, legal or contractual controls.
10. **Controlled failure.** Failure behavior **MUST NOT** silently broaden access, cross tenant boundaries or lose required evidence.

Detailed mechanisms require a dedicated RFC and ADRs, but no implementation may violate these invariants.

## 16. Organizational Control, Portability and Lifecycle

An organization retains governance and control over its data, organizational intelligence, standards, decisions and operational history subject to law and contract.

Arvectum OS **MUST** support governed export, migration, retention, deletion, service termination and handover within the applicable conformance scope.

A governed export **MUST** preserve, where applicable:

- record identities and versions;
- authority modes and external authoritative-source references;
- schemas and semantic types;
- typed relationships;
- provenance and evidence references;
- classifications and architectural responsibility;
- workflow, decision and event history;
- artifact content or lawful references;
- machine-readable formats and documentation sufficient for practical use.

Portability does not require exposing another party's confidential implementation, licensed content or rights-restricted data.

Deletion **MUST** distinguish:

- deletion of transient data;
- removal of governed assets where permitted;
- legal or contractual retention;
- irreversible erasure;
- tombstones or minimal evidence needed to preserve integrity;
- removal from indexes, caches, backups and derived stores according to policy.

Organizational continuity **MUST NOT** depend on an inaccessible proprietary representation or a specific employee, AI system, vendor or runtime.

A manual, documented and tested process **MAY** satisfy an early-stage portability or deletion requirement when it is proportionate to the declared conformance scope and risk.

## 17. Organizational and Tenant Sovereignty

Unless an explicit contract and policy state otherwise:

- records and relationships **MUST** be scoped to and governed within one organization;
- authority **MUST** be evaluated within that organization;
- one organization's data **MUST NOT** alter another organization's canonical model;
- cross-organization access **MUST** be denied by default;
- customer evidence, memory and knowledge **MUST NOT** be promoted into shared platform knowledge automatically;
- cross-organization learning **MUST** require explicit rights, classification and governance;
- shared knowledge **MUST** identify architectural owner, source rights and permitted use.

The architecture **MUST** distinguish platform-responsible, product-responsible, organization-governed, licensed, public and generated-but-unvalidated information.

These categories describe architectural scope and governance. They do not determine legal ownership.

## 18. Extension Model

Arvectum OS **MAY** be extended through registered and versioned products, agents, workflows, schemas, validators, templates, policies, connectors, tools, adapters and UI modules.

Every extension **MUST** declare identity, version, architectural owner, required contracts, compatibility, tenant scope, permissions, data handling, inputs, outputs, events, failure behavior, portability and deprecation rules proportionate to its lifecycle and conformance scope.

Extensions **MAY** add domain behavior. They **MUST NOT** weaken Kernel, security, sovereignty or governance invariants.

## 19. AI Components

AI is an execution capability, not an authority source or canonical source by default.

AI systems **MAY** analyze, retrieve, classify, recommend, draft, transform, generate and propose improvements.

They **MUST NOT** silently:

- change approved standards, policies or workflows;
- grant permissions;
- approve consequential decisions;
- replace Canonical Records;
- promote observations to validated knowledge;
- share data across organizations;
- extend retention or permitted use;
- bypass validation, security or approval gates.

For consequential operations the platform **MUST** identify relevant model or component reference, instructions, retrieval sources, tool access, settings, validation and approval state within the declared conformance scope.

Replacing an AI model **SHOULD NOT** require redefining organizational semantics unless the model is explicitly part of a contract.

## 20. Platform Gravity

The platform should be easier to reuse than to replace.

Healthy Platform Gravity appears when integration time, cost and risk decline for later consumers while contracts remain stable and products retain delivery autonomy.

Weak Platform Gravity appears when products repeatedly bypass contracts, platform integration is slower than local implementation, abstractions remain single-product beyond incubation, the platform team becomes a bottleneck or duplicate shared foundations emerge.

Weak Platform Gravity may justify redesign or de-platformization. It is not grounds for coercive adoption.

## 21. Delivery and Technology Strategy

### 21.1 Product Pull Before Platform Push

Arvectum OS should be built through real organizational and product demand.

The company should not attempt to implement a complete operating system before proving valuable workflows.

The first vertical spine should include only what one real consequential workflow requires to demonstrate canonical records, execution context, provenance, proportionate controls, a reproducible artifact and a credible path to reuse.

### 21.2 Modular Monolith by Default

The initial implementation should prefer a modular monolith unless evidence requires distribution for scaling, security, isolation, regulation, availability, release cadence, responsibility boundaries or unacceptable contention.

Distribution is not an architectural objective.

### 21.3 Build vs Buy and Semantic Portability

Arvectum OS should retain architectural responsibility for differentiated organizational semantics, contracts and strategically valuable behavior.

Commodity infrastructure should normally be adopted, integrated or purchased rather than recreated.

Technology independence requires portability of organizational meaning and assets, not speculative abstraction around every vendor.

Custom commodity infrastructure requires material justification such as strategic differentiation, security or sovereignty necessity, unacceptable continuity risk, demonstrated scale economics or absence of an adequate solution.

### 21.4 Architecture and Delivery in Parallel

RFCs, ADRs, Product Experiments and MVP implementation may proceed in parallel when:

- the Constitution and accepted decisions are not violated;
- the implementation is bounded and reversible or explicitly time-limited;
- provisional boundaries are documented;
- contracts are marked `Provisional` where appropriate;
- security, governance, data integrity and contractual controls remain intact;
- the experiment has an owner, review date and exit path.

Before an irreversible cross-cutting commitment becomes binding, the relevant RFC or ADR must be approved.

The follow-up RFC sequence is recommended, not a general delivery gate. Work with real sensitive or customer data requires the minimum security, privacy, isolation and portability decisions applicable to that work.

## 22. Scoped Conformance Model

Conformance is evaluated against a declared scope, not against every possible future capability of Arvectum OS.

Any implementation, pilot, deployment or capability claiming conformance with this RFC **MUST** maintain a Conformance Statement that identifies:

- subject and version being assessed;
- organization, tenant and deployment scope;
- lifecycle stage: `Experiment`, `Candidate`, `Incubating`, `Active` or `Production`;
- workflows and capabilities in scope;
- data classes, sensitivity and risk level;
- Canonical Record authority modes and external systems involved;
- applicable normative sections of this RFC;
- requirements declared not applicable, with rationale;
- manual or provisional controls used;
- approved architectural exceptions;
- known gaps and remediation owner;
- review date and conditions requiring reassessment.

A requirement **MAY** be declared not applicable only when the subject does not perform, store, govern or expose the behavior or data addressed by that requirement.

A requirement **MUST NOT** be declared not applicable merely because implementation is inconvenient or incomplete.

Manual, product-specific or provisional controls **MAY** satisfy a requirement when they preserve the constitutional invariant, are proportionate to risk, are documented in the Conformance Statement and have a review or replacement condition.

An implementation **MUST NOT** claim full-platform conformance when only a limited scope has been assessed.

## 23. Architectural Fitness Tests

The following fitness tests are normative within the scope declared by a Conformance Statement.

A conforming subject **MUST** be able to answer positively, where applicable:

1. Does every significant governed object have one Canonical Record within its scope?
2. Is the authority mode and authoritative source explicit for each Canonical Record?
3. Are competing sources of truth prevented when an external system remains authoritative?
4. Are historical versions immutable and events append-only?
5. Are authoritative knowledge, governed assets and transient outputs distinguishable?
6. Are relationships explicit, typed and traceable?
7. Does every consequential canonical change have an Execution Context?
8. Can a consequential output be reconstructed from inputs, versions, components, controls and approvals?
9. Can the platform operate without embedding product-domain behavior?
10. Can a product-local experiment operate without unnecessary platform ceremony?
11. Does any experiment interacting with platform capabilities or canonical state use a proportionate Provisional Product Contract?
12. Do capability requirements match the declared lifecycle stage?
13. Can an incubating capability be promoted, returned, replaced or retired?
14. Are access, tenant scope, classification, retention and deletion rules identifiable?
15. Can prohibited cross-organization use be prevented and audited?
16. Can the organization obtain a usable governed export within the declared scope?
17. Can technologies or AI models be replaced without losing governed organizational state where replacement is required by contract or risk?
18. Is commodity infrastructure reused unless custom implementation is justified?
19. Is platform complexity proportionate to maturity, risk and value?
20. Is architectural responsibility distinguishable from legal ownership and contractual rights?
21. Is the platform reducing total cost or risk rather than relocating complexity?

A negative answer indicates non-conformance, an approved exception, a declared gap or an incorrectly scoped claim. The Conformance Statement **MUST** identify which applies.

## 24. Platform Evidence

Platform value should be evaluated through measurable evidence of:

- product and workflow delivery speed;
- validated reuse;
- operating and responsibility cost;
- reliability and output quality;
- risk reduction;
- explainability and governance;
- security and isolation outcomes;
- export, migration and deletion capability;
- integration and de-platformization effort.

Detailed metrics remain informative operating artifacts and may evolve without amending this RFC.

## 25. Risks and Mitigations

### Premature Platformization

Mitigated by Product Experiments, incubation, review dates and economic admission.

### Platform Bottleneck

Mitigated by self-service contracts, product responsibility, modular implementation and platform-delay measurement.

### Contract Ceremony Slowing Experiments

Mitigated by allowing completely product-local experiments without platform contracts and requiring only a minimal Provisional Product Contract when platform state is involved.

### Competing Sources of Truth

Mitigated by explicit authority modes, authoritative-source declarations and synchronization contracts.

### Overclaiming Conformance

Mitigated by scoped Conformance Statements, lifecycle-specific requirements and explicit gaps or exceptions.

### Security or Privacy Added Too Late

Mitigated by structural invariants applying to every layer and by requiring minimum controls before real sensitive-data use.

### Cross-organization Knowledge Leakage

Mitigated by isolation, explicit permitted use, classification and governed promotion.

### False Completeness of the Organizational Model

Mitigated by exposing scope, freshness, confidence, provenance and gaps.

### Vendor Lock-in or Inaccessible Organizational State

Mitigated by governed export, semantic portability, documented representations and migration testing.

### Graph and Versioning Complexity

Mitigated by proportional controls, transient-object treatment and evidence-driven schema expansion.

### Architecture Before Revenue

Mitigated by product pull, bounded experiments, provisional contracts and parallel delivery.

### Capability Accumulation

Mitigated by lifecycle states, de-platformization and retirement.

### Commodity Infrastructure Reinvention

Mitigated by Build vs Buy review and explicit justification.

### Legal Ambiguity from Architectural Language

Mitigated by separating architectural responsibility from legal title, IP ownership, licensing and contractual data rights.

## 26. Consequences

### Positive

- organizational intelligence becomes a durable governed capability;
- platform and product boundaries remain explicit;
- external systems may remain authoritative without creating competing truth;
- experiments can move quickly without becoming accidental platform commitments;
- product-local experiments avoid unnecessary platform contracts;
- platform interaction remains governed through proportionate provisional contracts;
- capability obligations grow with lifecycle maturity;
- conformance claims remain scoped and honest;
- security, privacy, isolation and portability are architectural properties;
- customer knowledge governance and permitted reuse are explicit;
- organizational assets remain usable beyond a specific vendor or model;
- architectural responsibility is separated from legal ownership;
- the Kernel remains small;
- failed platform bets can be reversed;
- platform investment is evaluated through evidence.

### Costs

- Canonical Records, authority modes, relationships and provenance create engineering overhead;
- external-system synchronization requires explicit contracts and failure handling;
- security, classification, retention and export require lifecycle discipline;
- capability owners must support compatibility and migration appropriate to lifecycle;
- governance may slow consequential changes;
- provisional contracts and experiments require active review;
- Conformance Statements require disciplined scope management;
- retirement and portability require deliberate implementation work.

These costs are accepted only where they purchase value, control, continuity, evidence or validated reuse.

## 27. Follow-up Documents

The recommended, non-blocking sequence is:

1. `RFC-0002 — Canonical Record, Authority, Relationship and Organizational Asset Model`;
2. `RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability`;
3. `RFC-0004 — Product Contract, Product Experiment and Extension Model`;
4. `RFC-0005 — Governed Execution and Workflow Model`;
5. `RFC-0006 — Event, Provenance and Observability Model`;
6. `RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`;
7. `RFC-0008 — Document and Artifact Architecture`.

Implementation ADRs and reversible experiments may proceed in parallel. They may not contradict the Constitution or accepted RFCs.

Before processing real sensitive or customer data, the applicable minimum decisions from RFC-0002 and RFC-0003 must be accepted or explicitly covered by a bounded product-specific decision that preserves constitutional controls.

The Capability Catalog and Platform Metrics remain informative documents.

## 28. Acceptance Criteria

This RFC may be accepted only when the owner explicitly approves the following normative decisions:

1. alignment with Constitution `1.2.0`;
2. the normative-status model and keyword meanings;
3. the three scoped architectural laws;
4. the five Kernel primitives;
5. Canonical Record authority modes and the rule against competing sources of truth;
6. the distinction between Canonical Record, Governed Organizational Asset and Transient Output;
7. the distinction between Product Experiment and Platform Capability;
8. the rule that product-local experiments need no platform contract while platform interaction requires a proportionate Provisional Product Contract;
9. lifecycle-specific capability obligations, admission, de-platformization and exit rules;
10. the Product Contract and domain boundary;
11. structural security, privacy, least privilege and tenant-isolation invariants;
12. organizational control, export, migration, retention and deletion principles;
13. cross-organization rights and knowledge-reuse constraints;
14. the distinction between architectural responsibility and legal ownership or contractual rights;
15. the scoped conformance model and normative fitness tests;
16. the formal Approval Record process.

The owner acknowledges, but does not make normative through acceptance, the current informative guidance on Founder Thesis, Business Outcomes, Platform Gravity, Build vs Buy, delivery strategy, risks, consequences and follow-up sequence.

Acceptance does not authorize unspecified technologies, approve every cataloged capability, transfer customer rights or commit Arvectum OS to a specific commercial delivery model.

## 29. Decision

RFC-0001 remains `Proposed`.

Acceptance requires explicit approval by the owner of Arvectum OS and completion of the Approval Record below.

## 30. Approval Record

Decision: `Pending`
Decision authority: `ООО «Арвектум»`
Approved by: `Pending`
Decision date: `Pending`
Canonical approval reference: `Pending`

The canonical approval reference **MUST** identify an approval record that exists before or independently of the repository commit that marks this RFC `Accepted`. It may reference an approved governance record, signed decision, issue, pull-request approval or another immutable owner-approved source.

When this RFC is accepted, one repository change **MUST**:

1. set `Status` to `Accepted`;
2. set the accepted version to `1.0.0` unless the owner explicitly approves another stable version;
3. complete this Approval Record using the pre-existing canonical approval reference;
4. update the RFC Index to the accepted version and status;
5. preserve the resulting repository commit or release tag as external repository evidence.

The repository commit **MUST NOT** be embedded inside the same commit as a required self-reference.

A status change without a completed Approval Record and matching RFC Index does not constitute valid acceptance.