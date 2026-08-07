# RFC-0006: Event, Provenance and Observability Model

Status: `Draft`
Version: `0.1.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`; `RFC-0005 v1.0.0`
Supersedes: `None`
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS requires meaningful action to be observable, consequential operations to be reconstructable, significant outputs to be explainable, and organizational history to remain governed rather than disappear into transient logs or conversations.

RFC-0001 establishes `Event` as one of the five Platform Kernel primitives. RFC-0002 finalizes Event as a Canonical Record specialization: append-only, normally single-version, immutable after admission to canonical history, and correctable only through additional linked Events. RFC-0003 requires security, privacy, isolation, minimization, auditability and failure-closed handling. RFC-0004 requires Product Contracts to declare shared event and artifact boundaries where products rely on the platform. RFC-0005 requires Governed Execution to preserve sufficient evidence, causation and emitted Event references for consequential reconstruction.

This RFC defines the domain-neutral model that connects those requirements without selecting a message broker, event store, logging stack, metrics system, tracing protocol, SIEM, database, cloud provider or observability vendor.

The model is based on ten rules:

1. **A canonical Event is an append-only governed observation that something meaningful occurred; it is not synonymous with a log line, trace span, queue message or metric sample.**
2. **Meaningful consequential action MUST produce or be linked to observable governed evidence proportionate to consequence.**
3. **Operational telemetry is not canonical state by default.** Logs, metrics, traces and diagnostic records MAY remain transient or retention-bounded unless they are required as governed evidence.
4. **Provenance is traceable origin and lineage, not a sixth Kernel primitive.** It is represented through governed references, Events, Execution Contexts, Typed Relationships and other version-identifiable evidence.
5. **Correlation is not causation, and neither creates authority.** Causation, correlation, authorization and Organizational Authority remain distinct semantics.
6. **No universal global event order or delivery guarantee is assumed.** Ordering, delivery, deduplication and replay requirements MUST be explicit where consequential behavior relies on them.
7. **A required Event for consequential state change MUST NOT be silently lost.** The execution must either establish durable attributable event evidence or expose an explicit incomplete/reconciliation-required state.
8. **Observability MUST preserve security, privacy, tenant isolation, purpose limitation and minimization.** Diagnostic convenience does not justify uncontrolled retention or cross-organization visibility.
9. **Event and provenance semantics remain portable and technology-independent.** Backends, collectors, brokers and dashboards are replaceable infrastructure.
10. **Events and evidence do not automatically become Memory, Knowledge or reusable organizational assets.** Promotion belongs to RFC-0007 and applicable governance.

This RFC defines Event envelope semantics, event-type/schema versioning, significance, time, causation and correlation, authority and external-event representation, emission and consistency, delivery and replay contracts, provenance representation, observability and telemetry boundaries, consequential triggers, privacy/security controls, retention/deletion, integrity, Product Contract boundaries, portability, migration and scoped conformance.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 through RFC-0005 without changing their architectural laws.

The most relevant constitutional requirements are:

- meaningful actions generate observable records proportionate to consequence;
- nothing important happens silently;
- the system preserves enough context to reconstruct consequential operations;
- significant outputs are explainable through actors, workflows, standards, knowledge, automation, artifacts, validation and approvals where applicable;
- organizational memory and assets preserve provenance and evolution;
- security, privacy, confidentiality, isolation, minimization, retention, deletion and auditability are structural properties;
- reproducibility is required to the extent permitted by declared inputs and dependencies;
- significant governed objects are versioned;
- AI is an execution means rather than an authority source;
- architecture and observability remain proportionate to risk, maturity and organizational value;
- technologies may change without loss of organizational semantics or operational history.

RFC-0001 additionally requires:

- Event as a Kernel primitive;
- meaningful operational history through events and evidence;
- Governed Execution to identify emitted events, correlation and causation where applicable;
- enough provenance for Canonical Records, relationships, organizational assets, learning and governed export;
- attributable and observable consequential access and state change;
- technology-independent contracts and portability.

RFC-0002 establishes that:

- Event is a Canonical Record specialization;
- one Event has one stable Event Identity and normally one immutable canonical version;
- correction, reversal, compensation and invalidation use additional linked Events rather than mutation;
- an Event identifies, where applicable, type/schema version, occurrence and recording time, actor/component, Organization scope, related subjects/versions, execution/correlation/causation and provenance/classification;
- Event authority mode follows Canonical Record authority rules;
- Execution Context preserves emitted consequential Event references and reconstruction-relevant history.

RFC-0003 requires:

- explicit Organization scope and tenant isolation;
- deny-by-default authorization and least privilege;
- separation of authentication, authorization, Organizational Authority and data governance;
- purpose-aware minimization, retention and deletion;
- no logging of reusable secrets merely for evidence;
- attributable privileged access and failure behavior that does not silently broaden access.

RFC-0004 requires Product Contracts, where applicable, to declare shared operation, event, artifact, security, authority, data-handling and compatibility boundaries without creating hidden coupling.

RFC-0005 requires:

- consequential execution to remain reconstructable through version-pinned inputs and controls;
- governance-significant execution transitions to be preserved;
- retries, uncertainty and compensation not to duplicate consequential effects silently;
- output/artifact classification not to imply automatic knowledge promotion;
- complete Event taxonomy, delivery semantics, provenance representation and observability infrastructure to be defined by RFC-0006.

Where this RFC conflicts with the Constitution or an earlier Accepted RFC, the higher-authority source prevails.

## 3. Scope

This RFC defines domain-neutral architecture for:

- Event significance and the canonical Event / telemetry boundary;
- Event identity, immutability and envelope semantics;
- event type and schema versioning;
- occurrence time, recording time, ordering and late-arrival semantics;
- correlation and causation;
- Event authority modes and external occurrences;
- required Event evidence for consequential operations;
- delivery, duplication, replay, gap and ordering contracts;
- provenance origin, lineage and transformation references;
- provenance for deterministic and AI-mediated outputs;
- observability signals and diagnostic telemetry;
- governed alerts, incidents and event-driven consequential triggers;
- security, privacy, tenant isolation and classification of observability data;
- retention, deletion, minimization and reconstructability consequences;
- integrity and tamper-evidence requirements proportionate to consequence;
- Product Contract event boundaries;
- semantic portability and governed export;
- migration from product-local logs, event buses and telemetry;
- scoped conformance.

## 4. Non-goals

This RFC does not define:

- a message broker, event store, log collector, metrics database, tracing backend or SIEM;
- Kafka, NATS, RabbitMQ, OpenTelemetry or another specific protocol/product;
- physical event-table or topic layouts;
- one universal event taxonomy for every product domain;
- business-domain event names or payload schemas;
- one global total order across distributed systems;
- universal exactly-once transport delivery;
- a mandatory cryptographic algorithm or signing format;
- concrete retention periods;
- alert thresholds, SLOs, SLIs, RTOs or RPOs;
- incident-management organizational procedure;
- complete Memory, Knowledge, Observation or governed-learning promotion semantics, which belong to RFC-0007;
- domain-specific audit requirements or jurisdiction-specific legal advice;
- automatic promotion of observability infrastructure into an `Active` Platform Capability.

These subjects belong to subordinate ADRs, standards, catalogs, Product Contracts, operational decisions, legal requirements or later RFCs.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Model

### 6.1 Canonical Event

An **Event** is the RFC-0002 Canonical Record specialization representing an append-only governed observation that something meaningful occurred.

An Event is part of canonical operational history within its declared scope.

An Event MUST NOT be equated with every emitted technical message, log line, trace span, metric sample or diagnostic record.

### 6.2 Operational Telemetry

**Operational Telemetry** is diagnostic or operational data used to understand runtime behavior, health, performance, security or failures.

Telemetry MAY include:

- logs;
- metrics;
- traces/spans;
- health signals;
- diagnostic snapshots;
- delivery metadata;
- runtime counters.

Telemetry is not Canonical Record state by default.

Telemetry MAY remain mutable, aggregated, sampled, compacted or retention-bounded when doing so does not destroy evidence required by Accepted architecture or applicable governance.

### 6.3 Provenance

**Provenance** is traceable origin and lineage information that allows governed records, relationships, Events, artifacts and executions to be attributed to relevant sources, actors, versions and transformations.

Provenance is not an additional Kernel primitive.

It MAY be represented through:

- direct immutable references;
- version-pinned references in Execution Context;
- Event references;
- Typed Relationships;
- governed artifact manifests;
- external-authority retrieval evidence;
- other version-identifiable governed records.

### 6.4 Observability

**Observability** is the ability to determine and explain the relevant operational state, behavior and history of Arvectum OS from governed events, execution history and proportionate telemetry.

Observability serves at least:

- reconstruction;
- operational diagnosis;
- security and privacy review;
- incident investigation;
- explainability;
- policy and contract verification;
- performance and reliability analysis;
- controlled learning inputs where later governance permits.

Observability does not itself create authority or validate knowledge.

### 6.5 Evidence and Reconstruction

A consequential operation is reconstructable when retained governed evidence is sufficient, within the declared scope, to explain materially:

- who or what initiated it;
- which Organization scope applied;
- which Workflow/Product Contract/policies/standards and material input versions governed it;
- what consequential operations and external effects were attempted;
- what validations and approvals applied;
- what Events were emitted or observed;
- what outputs/artifacts resulted;
- what failed, remained uncertain, was retried or was compensated;
- what material deterministic or AI components influenced the result.

Reconstructability does not require indefinite retention of every runtime byte.

## 7. Event Significance

### 7.1 Significance Threshold

An occurrence SHOULD be represented as a canonical Event when failure to preserve it would materially impair understanding of:

- a consequential canonical mutation;
- a consequential external mutation or organizational commitment;
- authorization, Organizational Authority, approval or validation relevant to a consequential result;
- material security, privacy, tenant-isolation or privileged-access state;
- material workflow/execution lifecycle or recovery state;
- external-authority synchronization or conflict relevant to a consequential result;
- creation, change, supersession, invalidation or deletion of a significant governed object;
- material failure, uncertainty, compensation or reconciliation;
- promotion/designation of a governed organizational asset;
- another occurrence required by contract, policy, law or accepted architecture.

The significance threshold MUST remain proportionate to consequence and risk.

### 7.2 Non-significant Technical Activity

High-frequency technical activity MAY remain telemetry when it is not needed for authority, canonical meaning, contractual/legal evidence, security/privacy evidence, reconstruction or another consequential purpose.

Persisting technical data does not by itself make it a canonical Event.

### 7.3 Promotion of Telemetry to Governed Evidence

Telemetry that becomes necessary to support a dispute, incident, security investigation, reconciliation or other consequential purpose MAY be designated or captured as governed evidence through a governed operation.

Such promotion MUST preserve origin, collection time, source and integrity context sufficient for its intended evidentiary use and MUST NOT retroactively pretend that previously mutable telemetry was always canonical history.

## 8. Event Identity and Envelope

### 8.1 Event Identity

Every Event MUST have:

- one stable Event Identity as its Subject Identity;
- one immutable Version Identity;
- normally exactly one canonical Event version.

Event Identity MUST NOT be recycled.

Duplicate transport delivery of the same Event MUST preserve the same Event Identity rather than creating a new Event merely because the delivery was repeated.

### 8.2 Minimum Event Envelope

An Event MUST identify, directly or by governed reference and where applicable:

- Event Identity and Version Identity;
- event type identity/name;
- event type/schema version;
- Organization/tenant scope;
- authority mode and authoritative source where applicable;
- occurrence time;
- recording/admission time when materially different;
- producer component/principal;
- initiating actor/principal when different from producer;
- related Subject and/or Version Identities;
- Execution Identity and relevant Execution Context Version Identity where applicable;
- correlation reference(s) where applicable;
- causation reference(s) where applicable;
- classification/access constraints;
- retention/deletion policy reference where applicable;
- provenance sufficient for declared consequence;
- integrity metadata proportionate to consequence;
- payload or immutable/governed payload reference sufficient to interpret the event.

The exact physical field layout is not normative.

### 8.3 Producer and Initiator

The component that records or emits an Event MAY differ from the actor or governed trigger that initiated the occurrence.

Where that distinction is material, both MUST remain attributable.

A collector, broker, database writer or observability agent MUST NOT silently replace the actual initiating/producing provenance with its own technical identity.

## 9. Event Types and Schemas

### 9.1 Version-identifiable Semantics

Every canonical Event MUST reference an event-type definition whose semantics are version-identifiable.

When payload interpretation materially affects historical meaning, the exact event schema version MUST be preserved.

An admitted Event MUST NOT change meaning because a later schema version redefines the same type name.

### 9.2 Domain-neutral Platform Classes

Platform-level catalogs MAY classify Events into broad domain-neutral classes such as:

- execution/lifecycle;
- canonical-state change;
- authorization/authority/approval;
- security/privacy/isolation;
- external interaction/synchronization;
- artifact/output;
- validation/control evaluation;
- failure/uncertainty/recovery.

These classes do not require one universal physical topic layout and do not replace product-specific event types.

### 9.3 Product-specific Event Semantics

Tender, CRM, finance, legal, marketing and other domain event semantics remain product-owned by default.

A product-specific Event MUST NOT become a platform-wide semantic contract merely because multiple services happen to consume it.

Promotion into shared platform semantics requires the applicable architecture/governance decision.

## 10. Time and Ordering

### 10.1 Occurrence Time and Recording Time

An Event SHOULD distinguish:

- **occurrence time** — when the represented occurrence is understood to have happened;
- **recording/admission time** — when the Event entered the relevant Arvectum OS canonical history.

These times MAY differ because of offline work, external-system delay, batching, clock uncertainty or later discovery.

### 10.2 Clock Claims

A timestamp MUST NOT be treated as stronger evidence of order or simultaneity than its source and assurance support.

Where clock source, uncertainty or precision materially affects a consequential interpretation, the Event SHOULD preserve that context.

This RFC does not require one clock-synchronization technology.

### 10.3 No Universal Global Order

Arvectum OS does not assume one globally total order across all Events.

A consumer that relies on ordering MUST use a declared ordering scope and mechanism appropriate to that event contract, such as:

- per subject;
- per execution;
- per external source stream;
- per governed sequence.

Occurrence time alone MUST NOT be used as a universal distributed ordering guarantee.

### 10.4 Late and Out-of-order Events

A valid Event arriving late or out of expected order MUST remain append-only.

It MUST NOT be inserted by mutating prior Events.

If late arrival materially changes a prior consequential interpretation, the system MUST create explicit follow-up governed evidence, correction, reconciliation or review rather than silently rewriting history.

## 11. Correlation and Causation

### 11.1 Correlation

Correlation groups records that may belong to the same business, technical or investigative context.

Correlation MAY be many-to-many and MAY be supplied by product, workflow, integration or platform infrastructure.

A correlation reference MUST NOT by itself assert that one Event caused another.

### 11.2 Causation

Causation identifies a governed reason or predecessor occurrence for an Event or execution.

Where a causal relation materially affects reconstruction, the Event MUST preserve an explicit causation reference to the applicable Event, Execution, command/operation or other governed object.

### 11.3 Authority Separation

Neither correlation nor causation grants:

- authorization;
- Organizational Authority;
- approval power;
- cross-organization access;
- data-use rights.

Those remain governed by RFC-0003, RFC-0004, RFC-0005 and applicable policies/contracts.

## 12. Event Authority and External Occurrences

### 12.1 Authority Mode

Every Event MUST declare one RFC-0001/RFC-0002 authority mode:

- `Native`;
- `External Reference`;
- `Governed Replica`.

An Event produced as part of Arvectum OS governed operation is normally `Native` for the governed observation that Arvectum OS made.

### 12.2 External Occurrence

Where an external system remains authoritative for the underlying occurrence, Arvectum OS MUST preserve that external authority rather than converting ingestion into competing authority.

A significant external occurrence MAY be represented as:

- `External Reference` when Arvectum OS stores a governed identity/reference and retrieval contract; or
- `Governed Replica` when Arvectum OS stores a synchronized governed representation.

### 12.3 Ingestion Does Not Create Truth

Receiving a webhook, queue message, file, API response or telemetry signal does not by itself prove the underlying external fact.

The Event MUST preserve enough source and authority context to explain what is authoritative, what Arvectum OS observed and what transformations occurred.

## 13. Event Emission and Consistency

### 13.1 Required Event Evidence

When Accepted architecture, a Product Contract, policy or workflow requires an Event as evidence of a consequential operation, successful completion MUST NOT result in a silent canonical/external consequence with no attributable Event evidence.

### 13.2 Consistency Boundary

A conforming implementation MUST use a consistency strategy that ensures one of the following outcomes for a required Event and its consequential effect:

1. both the effect and attributable Event evidence are durably established within the declared consistency boundary; or
2. the execution enters an explicit incomplete, uncertain or reconciliation-required state in which the missing event/effect relationship is visible and recoverable.

This RFC does not require one distributed transaction or outbox technology.

### 13.3 Event-before-effect and Event-after-effect

A workflow MAY record intent before a consequential effect and outcome after it.

An intent Event MUST NOT be represented as proof that the effect succeeded.

An outcome Event MUST distinguish success, failure, uncertainty or partial completion where that distinction is material.

## 14. Delivery, Duplication and Replay

### 14.1 Event and Delivery Are Distinct

An Event is the governed occurrence record.

A **delivery** is transport of an Event representation or reference to a consumer.

Repeated delivery does not create a new Event.

### 14.2 Declared Delivery Contract

A producer/consumer boundary that relies on Events MUST declare, proportionate to consequence:

- delivery guarantee or expectation;
- ordering scope if any;
- duplicate behavior;
- retry behavior;
- gap detection/recovery where required;
- schema compatibility expectations;
- retention/replay window where applicable;
- failure/unavailability behavior.

No universal exactly-once transport guarantee is required.

### 14.3 Consequential Consumers

A consumer that may cause a consequential effect from an Event MUST:

- preserve the triggering Event Identity or immutable event reference in its Execution Context or equivalent governed evidence;
- enforce applicable authorization, Organizational Authority, data-governance and Product Contract gates;
- handle duplicate delivery without silently duplicating consequential effects;
- define behavior for missing, late or out-of-order Events when those conditions could affect correctness.

Event possession MUST NOT itself authorize consequential action.

### 14.4 Replay

Replay of an existing Event for rebuilding projections, recovery or diagnostics MUST preserve the original Event Identity and MUST NOT be treated as a new occurrence.

If replay intentionally causes a new governed operation, that operation MUST have its own Execution Identity and preserve causation to the replayed Event.

### 14.5 Gap Detection

Where a consumer relies on a complete ordered event sequence for consequential correctness, the contract MUST support detection of missing sequence elements or another governed method to prove/restore completeness.

A consumer MUST NOT silently assume completeness when the delivery contract does not provide it.

## 15. Provenance Model

### 15.1 Provenance Purpose

Provenance explains where governed information or output came from and how it was materially produced.

Provenance MUST be sufficient for the declared consequence, reconstruction, explainability, rights evaluation and permitted reuse.

### 15.2 Minimum Provenance Dimensions

Where materially relevant, provenance SHOULD identify or immutably reference:

- originating actor/principal or governed trigger;
- Organization scope;
- authoritative source and authority mode;
- source Subject/Version Identities;
- Workflow Version Identity;
- Product Contract Version Identity where applicable;
- applicable policy/standard/schema/validator versions;
- material deterministic or AI component identity/configuration;
- material transformations;
- Execution Identity and relevant Execution Context version;
- generated Event and artifact references;
- validation and approval evidence;
- occurrence/processing times sufficient for reconstruction;
- known gaps, uncertainty or unavailable dependencies.

### 15.3 Provenance by Reference

Provenance MAY be represented by reference rather than duplicated payload.

A provenance reference MUST be stable and version-identifiable enough for the intended reconstruction scope.

A mutable URL, current-head reference or vendor-internal identifier alone is insufficient when historical meaning depends on the exact version.

### 15.4 Derived Artifacts

A significant generated artifact SHOULD remain attributable to the material inputs, governing execution and transformations that produced it.

Derived-from relationships MUST NOT imply legal reuse rights, ownership or authorization.

### 15.5 Provenance Gaps

If required provenance is unavailable, incomplete, deleted, legally inaccessible or impossible to reproduce, the system MUST NOT claim a stronger level of reconstructability or explainability than the retained evidence supports.

Known material gaps SHOULD be explicit.

## 16. AI-mediated Provenance

### 16.1 AI Is a Component, Not Authority

AI-generated or AI-mediated output MUST preserve the same authority separation required by RFC-0003 and RFC-0005.

Model execution does not create Organizational Authority, approval or validated knowledge.

### 16.2 Material AI Inputs and Configuration

Where AI materially influences a consequential result, provenance SHOULD preserve, subject to minimization, rights and retention constraints:

- model/provider or model artifact identity sufficient to identify the execution dependency;
- material model version/configuration where available;
- prompt/template/configuration version where materially relevant;
- governed input references;
- retrieval/source references materially used;
- tool/operation calls that created consequential effects;
- validation/approval evidence;
- known non-determinism or reproducibility limitations.

This requirement does not mandate retention of raw prompts, chain-of-thought, model internals, secrets or sensitive payload when a governed reference or minimized representation is sufficient.

### 16.3 Equivalent Reproduction

Where non-determinism prevents byte-identical reproduction, provenance MUST support an equivalent-result reconstruction claim only to the extent actually supported by retained inputs, versions, configurations and dependencies.

## 17. Observability Signals

### 17.1 Signal Classes

A conforming implementation MAY use any combination of:

- canonical Events;
- Execution Context history;
- logs;
- metrics;
- traces;
- profiles;
- security telemetry;
- infrastructure telemetry;
- external monitoring signals.

No one backend or signal class is mandatory for every deployment.

### 17.2 Telemetry Is Not Authority

Dashboards, indexes, metrics stores, log stores and trace backends are projections or operational evidence stores unless separately governed as authoritative for a declared fact scope.

They MUST NOT silently become the source of truth for canonical organizational state.

### 17.3 Linking Telemetry to Governed History

Where practical and proportionate, telemetry used to diagnose governed execution SHOULD carry references such as Organization scope, Execution Identity, Event Identity, correlation reference or stable operation identity sufficient to connect diagnostics to canonical history without embedding sensitive payload unnecessarily.

### 17.4 Sampling and Aggregation

Telemetry MAY be sampled, aggregated, compacted or dropped according to operational policy when doing so does not violate required security evidence, contractual/legal obligations or accepted reconstruction requirements.

Required canonical Event evidence MUST NOT be lost merely because a telemetry sampler or log-retention policy discards diagnostic data.

## 18. Alerts, Incidents and Consequential Triggers

### 18.1 Alerts

An alert is an operational signal indicating that a condition may require attention.

An alert is not automatically a canonical Event or authoritative organizational fact.

If an alert materially initiates a consequential workflow, the trigger path MUST become attributable through the resulting Execution Context/Event evidence.

### 18.2 Incident Evidence

Security, privacy, reliability or operational incidents MAY require selected telemetry to be preserved as governed evidence.

Promotion/preservation MUST follow applicable classification, access, retention, legal and privacy controls.

### 18.3 Event-driven Automation

An Event MAY trigger Governed Execution.

The trigger MUST NOT bypass:

- authentication/actor attribution where applicable;
- authorization;
- Organizational Authority;
- data-governance permission;
- Product Contract limits;
- validation/approval gates.

## 19. Security, Privacy and Tenant Isolation

### 19.1 Organization Scope

Canonical Events and governed provenance MUST carry or resolve to an Organization scope unless explicitly governed as platform-global or cross-organization shared state.

Telemetry SHOULD preserve enough scope for isolation enforcement without unnecessarily duplicating customer data.

### 19.2 No Ambient Cross-Organization Observability

A shared observability backend MUST NOT create ambient visibility across Organizations.

Cross-organization event or telemetry access requires explicit authorization, applicable rights/purpose and classification-aware controls.

Shared correlation identifiers MUST NOT be treated as permission to join or disclose cross-organization data.

### 19.3 Sensitive Data Minimization

Events, logs, metrics, traces and provenance MUST NOT contain reusable secrets, authentication tokens, private keys, passwords or equivalent credentials merely for diagnostic convenience.

Sensitive payload SHOULD be referenced, redacted, tokenized, minimized or omitted when the required semantics can be preserved without retaining it.

### 19.4 Privileged Observability Access

Privileged access to sensitive observability data MUST be attributable and governed under RFC-0003, including break-glass requirements where applicable.

## 20. Retention, Deletion and Minimization

### 20.1 Different Retention Classes

Canonical Events, governed provenance and operational telemetry MAY have different retention periods and storage policies.

Retention MUST follow applicable legal, contractual, privacy, security and organizational requirements.

### 20.2 Immutability and Deletion

Event immutability prohibits in-place semantic rewriting of admitted canonical history.

It does not require unlawful or contractually prohibited indefinite retention.

Deletion or payload minimization required by applicable governance MUST occur through an attributable governed process and MUST NOT be disguised as an ordinary Event edit.

### 20.3 Reduced Reconstruction

If lawful deletion, minimization or external dependency loss reduces the retained evidence, Arvectum OS MUST reduce or qualify reconstructability, explainability or reproducibility claims accordingly.

### 20.4 Telemetry Retention

High-volume telemetry SHOULD use shorter or more selective retention than canonical consequential Event history unless risk, security, contract or law justifies longer retention.

## 21. Integrity and Tamper Evidence

### 21.1 Integrity Metadata

Canonical Events and high-consequence provenance MUST include integrity metadata proportionate to their consequence and threat model.

Possible implementation mechanisms include content hashes, signatures, append-only storage controls, immutable object versions or external attestations, but this RFC does not mandate a specific mechanism.

### 21.2 Integrity Is Not Authority

A valid signature, checksum or immutable storage property proves only the claim supported by that mechanism.

It does not automatically prove organizational authority, legal validity, truth of an external fact or permission to use the data.

## 22. Product Contract Boundary

### 22.1 Shared Event Contract

Where a product relies on platform Events or exposes product Events through the platform, the applicable Product Contract MUST declare, proportionate to consequence:

- event type identities and schema versions or compatibility ranges;
- direction of production/consumption;
- Organization scope;
- authority/source semantics;
- delivery and ordering expectations where relied upon;
- retry/duplicate/gap behavior where relevant;
- classification and data-handling constraints;
- retention/replay expectations where relevant;
- failure behavior;
- compatibility/migration expectations.

### 22.2 No Hidden Event Coupling

Products MUST NOT create governed dependence on private platform topics, undocumented streams, internal log formats or incidental database change feeds outside the Product Contract.

### 22.3 Lifecycle Independence

A Stable Product Contract does not make the underlying event infrastructure an `Active` Platform Capability, and a successful product event integration does not automatically promote product event semantics into the platform.

## 23. External Systems and Authority

### 23.1 External Event Streams

External event feeds, webhooks, audit logs and CDC streams MAY be integrated, but their authoritative scope, freshness, ordering, duplicate, retention and failure semantics MUST be explicit where consequential behavior relies on them.

### 23.2 Change Data Capture

A database or external-system change feed MAY be used as transport or evidence, but it MUST NOT automatically become the semantic organizational Event model.

If CDC semantics are insufficient to explain organizational meaning, a governed Event or execution interpretation layer is required before consequential reliance.

### 23.3 External Observability Vendors

External telemetry and observability vendors MAY be used when applicable security, privacy, contract, retention, sovereignty and portability controls are satisfied.

Vendor-specific representation MUST NOT become the only inaccessible form of required organizational operational history.

## 24. Portability and Export

### 24.1 Semantic Portability

A governed export of relevant operational history SHOULD preserve, subject to applicable rights and deletion restrictions:

- Event identities and immutable versions;
- event type/schema identities;
- Organization scope;
- authority/source declarations;
- occurrence/recording time;
- subject/version references;
- execution/correlation/causation references;
- provenance links;
- classification and retention metadata where exportable;
- integrity metadata necessary to interpret exported evidence.

### 24.2 Replaceable Backends

Changing event broker, log store, tracing backend or monitoring vendor MUST NOT require loss of the semantic Event/Provenance model for retained governed history.

### 24.3 Export Scope

Portability does not require export of secrets, non-exportable credentials, vendor-owned internal telemetry, legally prohibited data or information outside the organization’s rights.

## 25. Migration and Compatibility

### 25.1 No Big-bang Migration

Existing product-local logs, audit tables, event buses and telemetry MAY migrate incrementally.

This RFC does not require historic low-value telemetry to be retroactively converted into canonical Events.

### 25.2 Event Admission During Migration

A migration MAY initially admit only high-consequence event classes needed for current governed workflows and expand later based on evidence and value.

### 25.3 Legacy History

When legacy evidence cannot meet current provenance or schema requirements, it MAY remain accessible as legacy evidence with explicit limitations rather than being rewritten to appear natively conformant.

### 25.4 Compatibility

Event schema evolution MUST preserve historical interpretability.

Breaking consumer changes MUST follow Product Contract or platform contract compatibility/migration rules applicable to the boundary.

## 26. Scoped Conformance

Conformance to this RFC is scoped to the subject, Organization, workflow/product boundary and operational environment being assessed.

A conforming implementation within its declared scope MUST demonstrate that:

1. canonical Events conform to RFC-0002 identity, immutability and authority rules;
2. meaningful consequential actions have attributable governed Event/evidence coverage proportionate to consequence;
3. telemetry is not silently treated as canonical authority;
4. event type/schema semantics are version-identifiable;
5. occurrence and recording time are distinguishable where materially different;
6. correlation and causation are distinguishable and do not imply authority;
7. required Event evidence cannot be silently lost during consequential state change;
8. delivery contracts define duplicates, ordering, gaps/replay and failure where consequential correctness relies on them;
9. event-driven consequential consumers preserve triggering Event identity and pass applicable RFC-0003/RFC-0005 gates;
10. provenance is sufficient for declared reconstruction/explainability scope without mandatory unnecessary sensitive-data retention;
11. cross-organization observability does not bypass tenant isolation or purpose/rights controls;
12. secrets and reusable credentials are not retained in ordinary observability data merely for convenience;
13. retention/deletion behavior does not falsify canonical history or reconstructability claims;
14. Product Contract event boundaries are explicit where RFC-0004 applies;
15. required governed history remains semantically portable without dependence on one observability vendor.

## 27. Normative Fitness Scenarios

### Scenario A — Canonical mutation and missing Event

A workflow commits a consequential canonical change, but the event broker is unavailable.

Conforming behavior:

- the system does not silently report a fully complete governed result with no required event evidence;
- it either establishes durable Event evidence through its declared consistency strategy or records an explicit incomplete/reconciliation-required condition;
- later recovery preserves the original execution and causation.

### Scenario B — Duplicate delivery

A consequential consumer receives the same Event three times.

Conforming behavior:

- the Event Identity is the same;
- transport duplicates do not create three canonical Events;
- downstream consequential effects are deduplicated/idempotent or reconciled explicitly.

### Scenario C — Late external Event

An external authoritative system reports an occurrence after a dependent execution already completed.

Conforming behavior:

- the new Event is appended with external authority context and correct occurrence/recording times;
- prior Event history is not rewritten;
- if the late fact materially affects prior outcome, a governed reconciliation/review is created.

### Scenario D — Sensitive log

An integration error includes an access token in a raw exception object.

Conforming behavior:

- the reusable secret is not persisted in ordinary logs/events for convenience;
- the diagnostic record is redacted/minimized;
- required failure evidence is preserved without the secret.

### Scenario E — AI-generated consequential artifact

An AI component drafts a document later approved and issued externally.

Conforming behavior:

- provenance identifies the governing execution, material source/version references and materially relevant model/configuration information to the extent lawfully retained;
- AI is not recorded as final Organizational Authority merely because it generated the draft;
- approval evidence remains attributable to the authorized governance mechanism.

### Scenario F — Cross-tenant correlation

Two Organizations use the same external correlation string.

Conforming behavior:

- the shared string does not join or expose their data automatically;
- each Event remains Organization-scoped;
- cross-organization visibility requires explicit governed authorization and rights.

### Scenario G — Replay for projection rebuild

An operator replays six months of Events into a new search projection.

Conforming behavior:

- replay preserves original Event identities;
- projection rebuild does not create new historical occurrences;
- any new consequential operation caused intentionally by replay obtains a new Execution Identity and explicit causation.

## 28. Deferred Implementation Decisions

The following should be decided through ADRs, standards or operational decisions only when implementation evidence requires them:

- event persistence technology;
- broker/queue selection;
- physical Event envelope encoding;
- schema registry technology;
- outbox/inbox pattern implementation;
- trace propagation protocol;
- log/metric/trace backend;
- integrity/signature mechanism;
- telemetry sampling defaults;
- retention profiles;
- event partitioning/ordering mechanism;
- incident alerting stack.

This RFC intentionally preserves reversibility across those choices.

## 29. Risks and Consequences

### 29.1 Event Explosion

Risk: interpreting “nothing important happens silently” as “store everything forever.”

Mitigation: preserve the canonical Event significance threshold and keep high-volume telemetry non-canonical by default.

### 29.2 False Exactly-once Assumptions

Risk: consumers assume message delivery equals unique occurrence.

Mitigation: distinguish Event from delivery, require stable Event Identity and explicit duplicate/idempotency behavior.

### 29.3 Privacy Leakage Through Observability

Risk: logs and traces become an uncontrolled shadow dataset.

Mitigation: Organization scope, classification, minimization, restricted privileged access, retention control and prohibition on casual secret logging.

### 29.4 Provenance Overcollection

Risk: explainability is used to justify retaining raw prompts, payloads and sensitive intermediate data indefinitely.

Mitigation: provenance by governed reference, minimization and qualified reconstruction claims.

### 29.5 Vendor Lock-in

Risk: required operational history exists only in one proprietary backend.

Mitigation: technology-independent Event/Provenance semantics and governed export.

### 29.6 Event Bus as Authority

Risk: whichever message arrived first becomes treated as truth.

Mitigation: preserve authority mode/source and separate transport from organizational authority.

## 30. Acceptance Criteria

RFC-0006 MAY be accepted only when:

1. it remains compatible with Constitution `1.2.0`;
2. it remains compatible with Accepted RFC-0001 through RFC-0005;
3. Event remains an RFC-0002 Canonical Record specialization with append-only single-version semantics;
4. provenance is not introduced as a competing sixth Kernel primitive;
5. telemetry is clearly separated from canonical operational history;
6. required consequential Event evidence cannot be silently lost;
7. delivery/replay semantics do not assume universal exactly-once or global ordering;
8. security/privacy/isolation/minimization rules are at least as strong as RFC-0003;
9. Product Contract event boundaries remain explicit and product-domain semantics do not leak into the platform;
10. AI provenance does not create AI authority or require unjustified sensitive-data retention;
11. RFC-0007 Memory/Knowledge/Governed Learning scope is not pre-empted;
12. no irreversible observability technology commitment is introduced;
13. functional cross-review finds no unresolved material objection for the current lifecycle stage;
14. explicit owner approval exists independently before acceptance publication;
15. RFC Index and canonical roadmap are synchronized during acceptance publication and verified through read-after-write refresh.

## 31. Current Decision State

Current status: `Draft`.

This working proposal has no normative force until functional cross-review is completed, the proposal is published as `Proposed`, explicit owner approval exists independently, and a valid acceptance publication is completed under the RFC State Transition Procedure.
