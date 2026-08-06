# RFC-0001: Arvectum OS Architecture

Status: `Proposed`
Version: `0.2.0`
Created: `2026-08-06`
Updated: `2026-08-06`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.0.0`
Supersedes: `RFC-0001 v0.1.0`
Superseded by: `None`

## 1. Purpose

This RFC defines the foundational system architecture of Arvectum OS.

It establishes:

- what Arvectum OS is as a system;
- where the platform ends and products begin;
- what belongs to the Platform Kernel;
- what a Platform Service means;
- the canonical organizational object model;
- the permitted dependency directions;
- the execution model for consequential operations;
- the supported extension mechanisms;
- the architectural constraints that all later RFCs, ADRs and implementations must preserve.

This RFC is intentionally technology-independent. It defines the logical architecture before implementation choices are made.

## 2. Constitutional Basis

This RFC implements the Constitution of Arvectum OS version `1.0.0`.

The Constitution requires Arvectum OS to be:

- platform-first;
- domain-independent;
- based on canonical, versioned organizational records;
- explainable and reproducible;
- observable by construction;
- governed by explicit human authority;
- extensible through products rather than duplicated implementations;
- independent of particular programming languages, databases, AI models, vendors and runtimes.

Where this RFC is ambiguous, the Constitution prevails.

## 3. Business Objective

Arvectum OS exists to reduce the cost, risk and time required to build and operate AI-native organizational products.

The platform must make it possible to:

1. build multiple products on one shared operational foundation;
2. reuse memory, knowledge, workflows, governance, identity and document capabilities;
3. preserve organizational knowledge independently of employees, chats, models and vendors;
4. reconstruct why a consequential result was produced;
5. introduce automation without surrendering organizational control;
6. improve products through governed evidence rather than undocumented experimentation;
7. avoid rebuilding the same infrastructure for every new product.

An architectural component that does not support these objectives requires explicit justification.

## 4. Non-goals

This RFC does not define:

- any tender, marketing, legal, financial or other domain-specific behavior;
- detailed schemas for individual object types;
- a final microservice topology;
- a programming language, framework or database;
- a specific AI model or inference runtime;
- user interface design;
- pricing, packaging or go-to-market strategy;
- the internal architecture of any product.

These subjects belong to later RFCs, ADRs or product contracts.

## 5. System Model

Arvectum OS is the shared platform beneath domain products.

```text
┌──────────────────────────────────────────────────────────────┐
│                       Organizational Actors                  │
│       People · External Systems · Services · AI Agents      │
└──────────────────────────────┬───────────────────────────────┘
                               │
                               v
┌──────────────────────────────────────────────────────────────┐
│                         Product Layer                        │
│ Domain logic · Domain workflows · Domain knowledge · UX     │
│ Domain agents · Domain integrations · Domain policies       │
└──────────────────────────────┬───────────────────────────────┘
                               │
                    Versioned Product Contracts
                               │
                               v
┌──────────────────────────────────────────────────────────────┐
│                         Arvectum OS                           │
│ Identity · Governance · Records · Memory · Knowledge        │
│ Workflows · Decisions · Artifacts · Events · Validation     │
└──────────────────────────────┬───────────────────────────────┘
                               │
                    Technology Adapter Contracts
                               │
                               v
┌──────────────────────────────────────────────────────────────┐
│                     Technology and Runtime                   │
│ Storage · Search · Queues · Models · Files · Auth · APIs    │
└──────────────────────────────────────────────────────────────┘
```

The platform owns universal organizational capabilities.

Products own domain meaning and commercial behavior.

Technology adapters implement infrastructure without owning organizational meaning.

## 6. Architectural Layers

### 6.1 Platform Kernel

The Platform Kernel is the smallest stable set of concepts and invariants without which no Arvectum product can operate consistently.

A capability belongs in the Kernel only when all of the following are true:

1. every product requires it directly or indirectly;
2. inconsistent implementations would break interoperability, traceability or governance;
3. its semantics are domain-independent;
4. it must remain stable across technology changes;
5. it cannot be safely implemented as an optional extension.

The Kernel owns the contracts for:

- stable object identity;
- object version identity;
- actor identity and actor type;
- lifecycle status;
- ownership;
- timestamps and effective periods;
- provenance;
- relationships;
- execution context;
- authorization context;
- event envelope;
- validation result;
- approval record;
- compatibility metadata;
- outcome and error envelopes.

The Kernel does not contain:

- domain rules;
- domain prompts;
- domain ontologies;
- domain scoring;
- product-specific workflows;
- product-specific user interfaces;
- vendor-specific infrastructure behavior.

Kernel changes are cross-cutting. A backward-incompatible Kernel change requires an RFC.

### 6.2 Platform Services

A Platform Service is a logical responsibility boundary with owned canonical records and versioned interfaces.

A Platform Service is not necessarily:

- a separately deployed process;
- a network service;
- a separate repository;
- a separately scaled component.

The first implementation may be a modular monolith. Logical boundaries must nevertheless be preserved so that services can evolve or be extracted without redefining platform semantics.

The initial platform responsibility areas are:

- Identity and Access;
- Governance;
- Registry;
- Standards and Policies;
- Memory;
- Knowledge;
- Workflow Execution;
- Decisions;
- Documents and Artifacts;
- Events and Provenance;
- Validation;
- Product Contract Registry.

This list defines architectural responsibilities, not the mandatory deployment topology.

### 6.3 Product Layer

A product is an extension and client of Arvectum OS.

Products own:

- domain concepts and terminology;
- domain schemas;
- domain knowledge;
- domain workflows;
- domain validators;
- domain policies and risk rules;
- domain templates;
- domain agents;
- domain integrations;
- product user experience;
- commercial packaging.

A product must not duplicate a platform capability merely to gain local convenience.

### 6.4 Technology Adapter Layer

Technology adapters connect platform contracts to concrete infrastructure.

Adapters may provide:

- database persistence;
- object storage;
- search and indexing;
- event transport;
- authentication;
- AI inference;
- file conversion;
- notifications;
- external API connectivity.

Adapters do not become canonical sources of organizational meaning. Replacing an adapter must not require redefining the object model or product contracts.

## 7. Canonical Organizational Object Model

### 7.1 Everything Significant Is a Record

Every significant organizational object is represented by a canonical, versioned record.

Examples include:

- standards;
- policies;
- workflows;
- workflow executions;
- memory records;
- knowledge objects;
- decisions;
- documents;
- artifacts;
- templates;
- schemas;
- interfaces;
- product contracts;
- agents;
- approvals;
- validation results;
- events.

Raw technical data may exist outside this model, but it does not become authoritative organizational information until it is associated with a canonical record.

### 7.2 Common Record Semantics

Every significant record must support these conceptual properties directly or by reference:

- `object_id` — stable identity across versions;
- `version_id` — identity of one immutable version;
- `object_type` — registered semantic type;
- `schema_version` — schema used to interpret the record;
- `owner` — accountable owner;
- `status` — lifecycle state;
- `created_at` and `created_by`;
- `effective_from` and optional `effective_to`;
- `supersedes` and optional `superseded_by`;
- `provenance` — origin and derivation;
- `relationships` — typed links to other records;
- `classification` and access metadata where required;
- integrity metadata.

The exact storage field names may differ, but these semantics must remain available.

### 7.3 Canonical Ownership

Each record type has exactly one owning platform service or product.

The owner is responsible for:

- authoritative state;
- lifecycle rules;
- validation of changes;
- interface contracts;
- version history;
- migration rules.

Other components reference owned records. They do not create competing authoritative copies.

### 7.4 Relationships Form the Organizational Graph

Records are connected through typed relationships.

Examples:

```text
Knowledge      --supported_by--> Document
Workflow       --uses----------> Standard
Workflow Run   --produces------> Artifact
Decision       --approves------> Policy Version
Product        --implements----> Product Contract
Event          --caused_by-----> Actor
Memory Record  --derived_from--> Event
```

Relationships are first-class, version-aware and traceable.

The resulting graph is the durable organizational context of Arvectum OS.

## 8. Dependency Rules

Permitted dependency direction:

```text
Organizational Actors
        ↓
Products and Agents
        ↓
Product Contracts
        ↓
Platform Service Interfaces
        ↓
Platform Kernel
        ↓
Technology Adapter Interfaces
        ↓
Concrete Technologies
```

The following rules are mandatory:

1. The Kernel must not depend on any product.
2. Platform services must not contain product-domain behavior.
3. A product may depend only on declared platform interfaces and contracts.
4. Product A must not access the internal implementation of Product B.
5. Cross-product interaction must use shared platform records, events or explicit contracts.
6. Platform semantics must not depend on a specific adapter or vendor.
7. A lower layer must not call upward into a higher layer to obtain domain meaning.
8. Internal implementation details must not become accidental public interfaces.
9. Circular dependencies between responsibility boundaries are prohibited.
10. Architectural exceptions require an approved decision record with scope and migration plan.

## 9. Product Contracts

A Product Contract is the versioned boundary between a product and Arvectum OS.

It declares:

- product identity and version;
- required platform capabilities;
- compatible platform versions;
- domain record types and schemas;
- workflows introduced or extended;
- validators;
- standards and policies;
- event types;
- artifact types and templates;
- permissions and authority requirements;
- approval gates;
- extension points used;
- migration requirements;
- ownership and support status.

A product is compatible with Arvectum OS only when its contract can be validated against the active platform version.

Products do not gain platform access through undocumented conventions.

## 10. Execution Model

### 10.1 Execution Context

Every consequential operation runs within an explicit Execution Context.

The context identifies, where applicable:

- organization or tenant;
- initiating actor;
- acting authority and delegated authority;
- product and product version;
- product contract version;
- workflow and workflow version;
- input records and versions;
- applicable standards and versions;
- applicable policies and versions;
- knowledge and memory references;
- validation requirements;
- approval requirements;
- implementation component versions;
- AI model or automated component references;
- correlation and causation identifiers;
- reproducibility constraints.

Outputs, events, validations and approvals are linked to this context.

### 10.2 Standard Operation Lifecycle

A consequential operation follows this logical lifecycle:

1. **Request** — an actor declares an intended operation and inputs.
2. **Resolve identity** — actor, organization, product and contract are identified.
3. **Authorize** — permissions and delegated authority are evaluated.
4. **Resolve versions** — workflow, standards, policies, knowledge and dependencies are fixed.
5. **Plan controls** — required validation and approval gates are established.
6. **Execute** — human, deterministic or AI-assisted work is performed.
7. **Validate** — declared validators assess intermediate or final results.
8. **Approve** — required governance authority is applied.
9. **Commit** — canonical records and artifact versions are created.
10. **Observe** — events and provenance links are recorded.
11. **Publish or deliver** — outputs become available according to policy.
12. **Learn** — outcomes may generate observations or improvement proposals, but never silent production changes.

Not every low-risk operation requires every stage. Any omitted stage must be permitted by policy.

## 11. Events, Provenance and Explainability

Every meaningful action produces an observable event.

Events must identify, where applicable:

- event type and identity;
- time of occurrence and recording;
- actor;
- affected records and versions;
- execution context;
- correlation and causation;
- inputs and outputs;
- standards and policies applied;
- validation results;
- approval state;
- implementation component;
- integrity metadata.

Events are append-only observations. Corrections are represented by additional events, not destructive rewriting.

A significant output is explainable when the platform can reconstruct:

- who initiated it;
- under what authority;
- which product and workflow were used;
- which inputs and versions were used;
- which knowledge, memory, standards and policies were consulted;
- which human and automated components participated;
- which validations were performed;
- which approvals were required and obtained;
- which artifacts and records were produced.

## 12. Extension Model

Arvectum OS may be extended through registered, versioned extensions.

Supported extension classes are:

- products;
- agents;
- workflows;
- record schemas;
- validators;
- templates;
- standards;
- policies;
- connectors;
- tools;
- technology adapters;
- user interface modules.

Every extension must declare:

- identity and version;
- owner;
- extension type;
- required platform contracts;
- compatibility range;
- permissions;
- inputs and outputs;
- emitted events;
- failure behavior;
- migration and deprecation rules.

Extensions may add domain behavior. They may not weaken Kernel invariants, bypass governance or create competing canonical ownership.

## 13. AI Components

AI is an execution capability, not an authority source.

AI components may:

- analyze;
- classify;
- retrieve;
- recommend;
- draft;
- transform;
- generate;
- propose improvements.

AI components may not silently:

- change approved standards or policies;
- change active workflow behavior;
- grant permissions;
- approve consequential decisions;
- replace canonical records;
- promote observations to validated knowledge;
- bypass required validation or approval gates.

Prompts, model references, tool access, retrieval sources and relevant settings must be versioned or otherwise reproducibly identified for consequential operations.

## 14. Deployment and Evolution

The initial implementation should prefer a modular monolith unless operational evidence requires distribution.

This choice is not permanent. Logical service boundaries must be maintained from the beginning.

A component should be extracted into an independently deployed service only when evidence demonstrates a material need, such as:

- independent scaling;
- security isolation;
- regulatory isolation;
- availability requirements;
- independent release cadence;
- ownership boundaries;
- unacceptable coupling in the modular monolith.

Distribution without evidence creates cost and operational risk and is not an architectural objective.

## 15. Initial Delivery Sequence

The first implementation phase should establish a vertical architectural spine rather than implement all services broadly.

Recommended sequence:

1. Kernel contracts and common record semantics;
2. Registry and canonical ownership rules;
3. identity and authorization context;
4. event and provenance capture;
5. product contract registration and compatibility validation;
6. minimal workflow execution with Execution Context;
7. artifact generation and validation;
8. governance approvals;
9. memory and knowledge promotion flow;
10. first product integration proving the platform boundary.

The goal of the first phase is not feature completeness. It is to prove that one real product can execute a consequential workflow through shared platform contracts without embedding domain behavior in the platform.

## 16. Architectural Fitness Tests

An implementation conforms to this RFC only if the following questions can be answered positively:

1. Can a second product reuse the platform capability without copying its implementation?
2. Can the platform operate without knowing the product's domain rules?
3. Is every significant object owned by exactly one canonical authority?
4. Can a past output be traced to exact inputs, versions, policies, workflow and approvals?
5. Can an AI component be replaced without redefining organizational semantics?
6. Can a technology adapter be replaced without changing product contracts?
7. Can incompatible product and platform versions be detected before execution?
8. Can a proposed improvement be prevented from silently changing production behavior?
9. Can the system distinguish an observation, memory record, validated knowledge and approved decision?
10. Can the first implementation remain a modular monolith without violating logical boundaries?

A negative answer indicates architectural debt or non-conformance.

## 17. Acceptance Criteria for This RFC

This RFC may be accepted when the owner confirms that it provides a sufficient basis for subsequent detailed RFCs and ADRs.

Acceptance does not authorize implementation details that this RFC deliberately leaves open.

Before implementation begins, at minimum the following subsequent decisions are required:

- canonical object and relationship schemas;
- execution and workflow contracts;
- product contract schema;
- identity and authorization model;
- event and provenance model;
- governance and approval model;
- initial deployment architecture;
- implementation technology stack.

## 18. Consequences

### Positive

- products share one durable organizational foundation;
- platform and domain responsibilities are explicit;
- vendor and model dependence is reduced;
- governance and explainability are structural rather than optional;
- a modular monolith can be used without sacrificing future evolution;
- future RFCs can refine one concern at a time.

### Costs

- more discipline is required before implementation;
- records, versions, events and provenance create engineering overhead;
- product teams cannot bypass platform contracts for short-term convenience;
- governance may slow high-consequence changes;
- compatibility and migration must be managed explicitly.

These costs are intentional. They purchase organizational memory, control and long-term reuse.

## 19. Follow-up RFCs

The recommended next architecture sequence is:

1. `RFC-0002 — Canonical Object and Relationship Model`;
2. `RFC-0003 — Execution and Workflow Model`;
3. `RFC-0004 — Product Contract Model`;
4. `RFC-0005 — Identity, Authority and Governance Model`;
5. `RFC-0006 — Event, Provenance and Observability Model`;
6. `RFC-0007 — Memory and Knowledge Lifecycle`;
7. `RFC-0008 — Document and Artifact Architecture`.

Implementation technology choices should be recorded in ADRs only after the relevant logical contracts are accepted.

## 20. Decision

RFC-0001 remains `Proposed`.

Acceptance requires explicit approval by the owner of Arvectum OS.
