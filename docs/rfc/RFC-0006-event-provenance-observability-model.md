# RFC-0006: Event, Provenance and Observability Model

Status: `Proposed`
Version: `0.2.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`; `RFC-0005 v1.0.0`
Supersedes: `RFC-0006 v0.1.0` working draft
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Cross-review: `docs/reviews/RFC-0006-functional-cross-review.md`

## 1. Executive Summary

Arvectum OS requires meaningful action to be observable, consequential operations to be reconstructable, significant outputs to be explainable, and operational history to remain governed rather than disappear into transient logs, dashboards or conversations.

RFC-0001 establishes `Event` as a Platform Kernel primitive. RFC-0002 finalizes Event as a Canonical Record specialization: append-only, normally single-version, immutable after admission to canonical history, and correctable only through additional linked Events. RFC-0003 requires security, privacy, tenant isolation, minimization, auditability and failure-closed handling. RFC-0004 requires explicit Product Contract boundaries for shared events and artifacts. RFC-0005 requires Governed Execution to preserve sufficient evidence, causation and emitted Event references for consequential reconstruction.

This RFC defines the domain-neutral Event, Provenance and Observability model needed to make those requirements interoperable without selecting a message broker, event store, logging stack, metrics system, tracing protocol, SIEM, database, cloud provider or observability vendor.

The model is based on twelve rules:

1. **A canonical Event is an append-only governed observation/assertion that something meaningful occurred.** It is not synonymous with a queue message, log line, trace span or metric sample.
2. **Transport receipt is not canonical Event admission.** Admission validates enough identity, schema, Organization scope, authority/source, classification, provenance and integrity context for the declared consequence.
3. **Meaningful consequential action MUST produce or be linked to observable governed evidence proportionate to consequence.** Nothing important happens silently.
4. **Operational telemetry is not canonical state by default.** Logs, metrics, traces and diagnostics MAY remain mutable, sampled, aggregated or retention-bounded unless required as governed evidence.
5. **Provenance is traceable origin and lineage, not a sixth Kernel primitive.** It is represented through governed references, Events, Execution Contexts, Typed Relationships and other version-identifiable evidence.
6. **Correlation is not causation, and neither creates authority.** Correlation, causation, authorization, Organizational Authority and data-use permission remain distinct.
7. **No universal global Event order or exactly-once transport guarantee is assumed.** Ordering, delivery, duplicate, gap and replay semantics MUST be explicit where consequential behavior relies on them.
8. **A required Event/evidence path MUST NOT fail silently.** The operation must establish durable attributable evidence, fail/pause, use an explicitly governed degraded mode, or enter an explicit incomplete/uncertain/reconciliation-required condition.
9. **Replay and duplicate delivery MUST be side-effect safe.** Replayed transport is not a new occurrence, and event possession does not authorize a consequential action.
10. **Observability is subject to the same security, privacy, tenant-isolation, purpose, minimization, retention and deletion constraints as other platform data.** Diagnostic convenience creates no exception.
11. **Event and provenance semantics are portable and technology-independent.** Brokers, collectors, indexes and dashboards are replaceable infrastructure and projections, not organizational authority.
12. **Events, telemetry and provenance do not automatically become Memory, validated Knowledge or reusable Governed Organizational Assets.** Promotion belongs to RFC-0007 and applicable governance.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 through RFC-0005 without changing their architectural laws.

The most relevant constitutional requirements are:

- meaningful actions generate observable records proportionate to consequence;
- nothing important happens silently;
- consequential operations preserve enough context for reconstruction;
- significant outputs are explainable through actors, workflows, standards, sources, automation, artifacts, validation and approvals where applicable;
- organizational memory and assets preserve provenance and evolution;
- security, privacy, confidentiality, isolation, minimization, retention, deletion and auditability are structural properties;
- reproducibility is required only to the extent supported by declared inputs and dependencies;
- AI is an execution means, not an authority source;
- observability and governance remain proportionate to risk, maturity and organizational value;
- technology may change without loss of organizational meaning or operational history.

RFC-0002 establishes the minimum Event semantics this RFC MUST preserve:

- Event is a Canonical Record specialization;
- one Event has one stable Event Identity and normally one immutable canonical Event version;
- correction, reversal, compensation and invalidation use additional linked Events rather than mutation;
- an Event identifies, where applicable, event type/schema version, occurrence and recording time, actor/component, Organization scope, related subjects/versions, execution/correlation/causation and provenance/classification;
- every Event declares one authority mode;
- Execution Context preserves emitted consequential Event references and reconstruction-relevant history.

RFC-0003 additionally requires explicit Organization scope, deny-by-default authorization, least privilege, separation of authentication/authorization/Organizational Authority/data governance, minimization, retention/deletion, attributable privileged access and failure behavior that does not silently broaden access.

RFC-0004 requires shared product/platform event reliance to be declared through the applicable Product Contract rather than through private topics, log formats, internal tables, undocumented streams or accidental shared state.

RFC-0005 requires consequential execution to remain reconstructable through version-pinned material inputs and controls, explicit failure/uncertainty/compensation, and attributable event/evidence references.

Where this RFC conflicts with the Constitution or an earlier Accepted RFC, the higher-authority source prevails.

## 3. Scope

This RFC defines domain-neutral architecture for:

- canonical Event significance and Event admission;
- Event identity, immutability, envelope and schema versioning;
- correction, reversal, compensation and invalidation;
- occurrence time, recording time, ordering and late arrival;
- correlation and causation;
- Event authority and external occurrences;
- consistency between consequential effects and required Event evidence;
- delivery, duplication, acknowledgement/checkpoint, gap and replay semantics;
- provenance origin, lineage, transformation and reconstruction;
- AI-mediated provenance without AI authority;
- operational telemetry and observability projections;
- alert/incident/consequential-trigger evidence;
- security, privacy, tenant isolation, sensitive-data access and observability-control changes;
- retention, deletion, minimization, integrity and evidentiary limits;
- Product Contract event boundaries;
- portability, migration and scoped conformance.

## 4. Non-goals

This RFC does not select or define:

- a message broker, event store, log collector, metrics database, tracing backend or SIEM;
- Kafka, NATS, RabbitMQ, OpenTelemetry or another specific protocol/product;
- physical table/topic layouts or service topology;
- one universal domain event taxonomy;
- one global total order across distributed systems;
- universal exactly-once transport delivery;
- a mandatory cryptographic algorithm or signing format;
- concrete retention periods, alert thresholds, SLO/SLI, RTO/RPO or incident procedure;
- Memory, Knowledge, Observation or governed-learning promotion semantics, which belong to RFC-0007;
- jurisdiction-specific legal advice;
- automatic promotion of observability infrastructure into an `Active` Platform Capability.

Those choices belong to subordinate ADRs, standards, catalogs, Product Contracts, operational decisions, legal requirements or later RFCs.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Model

### 6.1 Canonical Event

An **Event** is the RFC-0002 Canonical Record specialization representing an append-only governed observation or assertion that something meaningful occurred.

An Event is canonical operational history within its declared scope. It records what Arvectum OS or an identified external authority/source observed or asserted; it is not metaphysical proof that an underlying real-world fact is true beyond the declared authority/evidence.

### 6.2 Operational Telemetry

**Operational Telemetry** is diagnostic or operational data used to understand runtime behavior, health, security, performance or failures, including logs, metrics, traces/spans, health signals, delivery metadata and diagnostic snapshots.

Telemetry is not Canonical Record state by default. It MAY be mutable, sampled, compacted, aggregated or retention-bounded when doing so does not destroy evidence required by Accepted architecture, contract, policy or law.

Persisting telemetry does not automatically promote it into canonical history.

### 6.3 Provenance

**Provenance** is traceable origin and lineage information that allows governed records, relationships, Events, artifacts and executions to be attributed to relevant sources, actors, versions and transformations.

Provenance is not a new Kernel primitive. It MAY be represented through direct immutable references, version-pinned Execution Context references, Events, Typed Relationships, governed manifests, external-authority retrieval evidence and other version-identifiable governed records.

### 6.4 Observability

**Observability** is the ability to determine and explain relevant operational state, behavior and history from canonical Events, execution history and proportionate telemetry.

Dashboards, indexes, search projections and monitoring backends are operational views. They MUST NOT silently become competing canonical authorities.

### 6.5 Reconstruction

A consequential operation is reconstructable when retained governed evidence is sufficient, within the declared scope, to explain materially:

- initiating actor or governed trigger;
- Organization scope;
- Workflow, Product Contract and material policy/standard/input versions;
- consequential operations and external effects attempted;
- validation/approval evidence;
- relevant Events, outputs and artifacts;
- failure, uncertainty, retry, compensation and reconciliation;
- material deterministic or AI components and transformations.

Reconstructability does not require indefinite retention of every runtime byte. Arvectum OS MUST NOT claim stronger reconstructability, explainability or reproducibility than retained evidence actually supports.

## 7. Event Significance and Admission

### 7.1 Significance Threshold

An occurrence SHOULD be represented as a canonical Event when failure to preserve it would materially impair understanding of:

- a consequential canonical mutation;
- a consequential external mutation or organizational commitment;
- authorization, Organizational Authority, approval or validation relevant to consequential action;
- material security, privacy, tenant-isolation or privileged-access behavior;
- material workflow/execution lifecycle or recovery state;
- external-authority synchronization/conflict relevant to a consequential result;
- creation, supersession, invalidation or deletion of significant governed state;
- material failure, uncertainty, compensation or reconciliation;
- another occurrence required by Accepted architecture, Product Contract, policy or law.

High-frequency technical activity MAY remain telemetry when it is not needed for authority, canonical meaning, evidentiary duty, security/privacy review or reconstruction.

### 7.2 Admission Is Not Receipt

Receiving bytes from a webhook, queue, CDC feed, file, API or telemetry collector does not by itself create a canonical Event.

Before admission to canonical Event history, a conforming implementation MUST validate or resolve, proportionate to consequence:

- Event Identity or issuance of one under the applicable namespace;
- event type and schema version;
- Organization/tenant scope;
- authority mode/source;
- minimum required actor/producer attribution;
- classification/access constraints;
- required provenance/integrity context;
- payload interpretability.

Invalid, ambiguous or insufficiently governed input MAY remain quarantined/transient evidence, be rejected, or trigger reconciliation. It MUST NOT silently become trusted canonical history.

### 7.3 Conflicting Event Identity

Repeated transport of the same canonical Event MUST preserve the same Event Identity.

If the same Event Identity is presented with materially different canonical content or incompatible immutable metadata, the system MUST reject, quarantine or escalate the conflict. It MUST NOT silently choose one version or mutate the admitted Event.

### 7.4 Promotion of Telemetry to Evidence

Telemetry needed later for an incident, dispute, security investigation or reconciliation MAY be designated/captured as governed evidence through a governed operation.

The promotion MUST preserve origin, source, collection time and integrity context sufficient for its intended use and MUST NOT pretend that previously mutable telemetry was always canonical Event history.

## 8. Event Identity, Envelope and Correction

### 8.1 Event Identity

Every Event MUST have one stable Event Identity as Subject Identity and one immutable Version Identity. The normal Event model has exactly one canonical version.

Event Identity MUST be non-recycled.

### 8.2 Minimum Event Envelope

An Event MUST identify, directly or by governed reference and where applicable:

- Event Identity and Version Identity;
- event type identity/name and version-identifiable schema;
- Organization/tenant scope;
- authority mode and authoritative source;
- occurrence time;
- recording/admission time when materially different;
- producing component/principal;
- initiating actor/principal when different;
- related Subject and/or Version Identities;
- Execution Identity and relevant Execution Context version;
- correlation reference(s);
- causation reference(s);
- classification/access constraints;
- retention/deletion policy reference where applicable;
- provenance sufficient for declared consequence;
- integrity metadata proportionate to consequence;
- payload or governed immutable/version-identifiable payload reference sufficient to interpret the Event.

The exact physical field layout is not normative.

### 8.3 Producer and Initiator

The component that records/emits an Event MAY differ from the actor or governed trigger that initiated the occurrence. Where material, both MUST remain attributable.

A collector, broker or observability agent MUST NOT erase actual initiating/producing provenance by replacing it only with its own transport identity.

### 8.4 Correction, Reversal, Compensation and Invalidation

An admitted Event MUST NOT be edited in place.

Correction, reversal, compensation or invalidation MUST create one or more additional Events and explicit version-identifiable relationships or causation references to the prior Event as required by RFC-0002.

A corrective Event describes a later governed assertion about prior history; it does not mutate what the earlier Event recorded at admission time.

## 9. Event Types and Schema Evolution

Every canonical Event MUST reference an event-type definition whose semantics are version-identifiable.

When payload interpretation materially determines historical meaning, the exact schema version MUST be preserved.

A later schema/type version MUST NOT silently reinterpret an already admitted Event.

Platform-level catalogs MAY define broad domain-neutral classes such as execution/lifecycle, canonical-state change, authority/approval, security/privacy, external synchronization, artifact/output, validation/control and failure/recovery.

Tender, CRM, finance, legal, marketing and other business event semantics remain product-owned by default. Reuse by several implementations does not automatically promote a product event type into a shared Platform Capability or platform-wide semantic contract.

## 10. Time, Ordering, Correlation and Causation

### 10.1 Occurrence and Recording Time

An Event SHOULD distinguish:

- **occurrence time** — when the represented occurrence is understood to have happened;
- **recording/admission time** — when the Event entered Arvectum OS canonical history.

They MAY differ because of offline work, external delay, batching, clock uncertainty or later discovery.

A timestamp MUST NOT be treated as stronger proof of order/simultaneity than its source and assurance support. Clock source/precision/uncertainty SHOULD be retained when material.

### 10.2 Ordering

Arvectum OS assumes no universal global total Event order.

A consumer that relies on ordering MUST use a declared ordering scope/mechanism appropriate to the contract, such as per subject, execution, external stream or governed sequence.

Occurrence time alone MUST NOT be used as a universal distributed ordering guarantee.

### 10.3 Late and Out-of-order Events

A valid late/out-of-order Event remains append-only. It MUST NOT cause prior Event history or prior Execution evidence to be rewritten as if the later information had been known earlier.

If late information materially changes a prior consequential interpretation, an explicit follow-up reconciliation, correction, review or Governed Execution MUST be created.

### 10.4 Correlation

Correlation groups records that may share a business, technical or investigative context. It MAY be many-to-many.

A correlation reference MUST NOT assert causation, authorization, Organizational Authority, data-use permission or cross-organization visibility.

### 10.5 Causation

Where a causal relation materially affects reconstruction, the Event MUST preserve an explicit causation reference to the applicable Event, Execution, operation/command or other governed object.

Causation does not itself grant authority.

## 11. Authority and External Events

Every Event MUST declare one RFC-0001/RFC-0002 authority mode: `Native`, `External Reference` or `Governed Replica`.

An Event produced as part of Arvectum OS governed operation is normally `Native` for the observation that Arvectum OS made.

Where an external system remains authoritative for the underlying occurrence, Arvectum OS MUST preserve that authority rather than converting ingestion into competing authority.

A significant external occurrence MAY be represented as:

- `External Reference` when Arvectum OS stores a governed identity/reference and retrieval contract; or
- `Governed Replica` when Arvectum OS stores a synchronized governed representation.

Receiving a webhook, API response, file, queue message, external audit entry or CDC record does not by itself prove the underlying external fact. The Event MUST preserve enough source/authority/transformation context to explain what Arvectum OS observed and what remains externally authoritative.

## 12. Consequential Effects and Required Event Evidence

### 12.1 No Silent Consequence

When Accepted architecture, a Product Contract, workflow, policy or law requires Event/evidence coverage for a consequential operation, successful completion MUST NOT leave a consequential canonical/external effect with no attributable required evidence.

### 12.2 Consistency Strategy

A conforming implementation MUST use a consistency strategy that results in one of:

1. the consequential effect and required attributable Event evidence are durably established within the declared consistency boundary; or
2. the execution is explicitly failed/paused; or
3. an explicitly governed degraded mode permits continuation with bounded consequence; or
4. the execution enters an explicit incomplete, uncertain or reconciliation-required state in which the missing evidence/effect relationship is visible and recoverable.

Silent dropping of required Event evidence is non-conforming.

This RFC does not require a universal distributed transaction, event broker or outbox implementation.

### 12.3 Intent and Outcome

A workflow MAY record intent before a consequential effect and outcome after it.

An intent Event MUST NOT be represented as proof that the effect succeeded.

Outcome evidence MUST distinguish success, failure, uncertainty or partial completion where material.

### 12.4 Observability Degradation

If disabling, sampling, rerouting, misconfiguring or shortening retention of observability controls would remove evidence required by Accepted architecture, contract, policy or law, that control change is itself a governed consequential configuration change and MUST be attributable.

A deployment MUST NOT silently disable required evidence collection merely as an operational shortcut.

## 13. Delivery, Duplication, Checkpoints and Replay

### 13.1 Event and Delivery Are Distinct

An Event is the governed occurrence record. A **delivery** is transport of an Event representation/reference to a consumer.

Repeated delivery does not create a new Event.

### 13.2 Declared Delivery Contract

A producer/consumer boundary that relies on Events MUST declare, proportionate to consequence:

- delivery guarantee/expectation;
- ordering scope if any;
- duplicate behavior;
- retry behavior;
- gap detection/recovery where required;
- schema compatibility expectations;
- retention/replay window where applicable;
- failure/unavailability behavior.

No universal exactly-once transport guarantee is required.

### 13.3 Acknowledgements and Checkpoints

Transport acknowledgements, offsets, cursors and consumer checkpoints MAY prove delivery progress within their declared transport semantics.

They MUST NOT replace Event identity, Event authority, authorization, Organizational Authority, canonical state or execution evidence.

### 13.4 Consequential Consumers

A consumer that may cause a consequential effect from an Event MUST:

- preserve the triggering Event Identity/immutable reference in its Execution Context or equivalent governed evidence;
- enforce RFC-0003/RFC-0005 authorization, Organizational Authority, data-governance, validation and approval gates;
- handle duplicate delivery without silently duplicating consequential effects;
- define behavior for missing, late or out-of-order Events when correctness depends on them.

Event possession is not permission.

### 13.5 Replay

Replay of an existing Event for rebuilding projections, recovery or diagnostics MUST preserve the original Event Identity and MUST NOT be treated as a new historical occurrence.

Replay for projection rebuild MUST be side-effect safe by design.

If replay intentionally causes a new consequential operation, that operation MUST use a new Execution Identity, pass normal Governed Execution gates, and preserve causation to the replayed Event.

### 13.6 Gap Detection

Where a consumer relies on a complete ordered sequence for consequential correctness, the contract MUST provide a method to detect/restore missing sequence elements or otherwise prove completeness.

A consumer MUST NOT silently assume completeness when the delivery contract cannot support that claim.

## 14. Provenance Model

### 14.1 Purpose

Provenance explains where governed information/output came from and how it was materially produced.

It MUST be sufficient for the declared consequence, reconstruction, explainability, rights evaluation and permitted reuse.

### 14.2 Material Provenance Dimensions

Where relevant, provenance SHOULD identify or immutably reference:

- originating actor/principal or governed trigger;
- Organization scope;
- authoritative source and authority mode;
- source Subject/Version Identities;
- Workflow Version Identity;
- Product Contract Version Identity where applicable;
- policy/standard/schema/validator versions materially used;
- material deterministic or AI component identity/configuration;
- material transformations;
- Execution Identity and relevant Execution Context version;
- Event and artifact references;
- validation/approval evidence;
- relevant occurrence/processing times;
- known gaps, uncertainty or unavailable dependencies.

### 14.3 Provenance by Reference

Provenance MAY use governed references instead of duplicated payload. A reference MUST be stable and version-identifiable enough for the intended reconstruction scope.

A mutable URL, current-head reference or vendor-internal identifier alone is insufficient when exact historical version materially affects meaning.

### 14.4 Derived Artifacts

A significant generated artifact SHOULD remain attributable to material input versions, governing execution and transformations.

`derived from`, `generated by`, causation or similar lineage does not imply legal ownership, reuse rights, access rights or Organizational Authority.

### 14.5 Provenance Gaps

If required provenance is unavailable, incomplete, deleted, legally inaccessible or impossible to reproduce, the system MUST expose or account for the limitation and MUST NOT claim a stronger evidentiary/reconstruction level than supported.

## 15. AI-mediated Provenance

AI-generated or AI-mediated output remains subject to RFC-0003 and RFC-0005 authority boundaries. Model execution does not create Organizational Authority, final approval or validated Knowledge.

Where AI materially influences a consequential result, provenance SHOULD preserve, subject to minimization, rights and retention constraints:

- model/provider or model artifact identity sufficient to identify the dependency;
- material model version/configuration where available;
- prompt/template/configuration version when materially relevant;
- governed input/retrieval source references materially used;
- consequential tool/operation calls;
- validation/approval evidence;
- known non-determinism or reproducibility limits.

This RFC does not require retention of raw prompts, chain-of-thought, model internals, secrets or sensitive retrieved payload where a governed reference or minimized representation is sufficient.

Where non-determinism prevents byte-identical reproduction, Arvectum OS MUST qualify reproduction as equivalent-result reconstruction only to the extent supported by retained evidence.

## 16. Observability, Alerts and Incidents

### 16.1 Signals

A conforming implementation MAY use canonical Events, Execution Context history, logs, metrics, traces, profiles, security telemetry, infrastructure telemetry and external monitoring signals.

No single backend or signal class is mandatory for every deployment.

### 16.2 Telemetry Is Not Authority

Dashboards, log/metric/trace stores, search documents and derived observability projections MUST NOT silently become authoritative organizational state.

When practical and proportionate, telemetry used to diagnose governed execution SHOULD carry non-sensitive references such as Organization scope, Execution Identity, Event Identity, correlation reference or stable operation identity sufficient to connect diagnostics to canonical history.

### 16.3 Sampling and Aggregation

Telemetry MAY be sampled, aggregated, compacted or dropped according to operational policy when this does not violate required security evidence, contractual/legal obligations or accepted reconstruction requirements.

Required canonical Event evidence MUST NOT be lost merely because a telemetry sampler discards diagnostics.

### 16.4 Alerts

An alert is an operational signal that a condition may require attention. It is not automatically a canonical Event or authoritative organizational fact.

If an alert materially initiates a consequential workflow, the trigger path MUST become attributable through the resulting Execution Context/Event evidence.

### 16.5 Incidents

Security, privacy, reliability or operational incidents MAY require selected telemetry to be preserved as governed evidence. Preservation/promotion MUST follow applicable classification, access, retention, legal and privacy controls.

## 17. Security, Privacy and Tenant Isolation

### 17.1 Organization Scope

Canonical Events and governed provenance MUST carry or resolve to an Organization scope unless explicitly governed as platform-global or cross-organization shared state.

A shared observability backend MUST NOT create ambient visibility across Organizations.

### 17.2 Correlation Is Not Cross-tenant Permission

Shared correlation strings, external identifiers, trace identifiers or technical infrastructure MUST NOT be used as implicit permission to join or expose data from multiple Organizations.

Cross-organization access requires explicit authorization, applicable purpose/rights and classification-aware controls.

### 17.3 Sensitive-data Minimization

Events, logs, metrics, traces and provenance MUST NOT contain reusable secrets, authentication tokens, private keys, passwords or equivalent credentials merely for diagnostic convenience.

Sensitive payload SHOULD be referenced, redacted before admission, tokenized, minimized or omitted when required semantics can be preserved without retaining it.

### 17.4 Sensitive Observability Access

Privileged access to sensitive governed Events, provenance or telemetry MUST be attributable and governed under RFC-0003.

Where access itself is materially security/privacy-relevant, it SHOULD produce or link to appropriate governed evidence. Break-glass access remains subject to RFC-0003 rules.

## 18. Retention, Deletion, Integrity and Evidentiary Claims

### 18.1 Different Retention Classes

Canonical Events, governed provenance and operational telemetry MAY use different retention profiles. Retention MUST follow applicable legal, contractual, privacy, security and organizational requirements.

High-volume telemetry SHOULD normally use shorter/selective retention than consequential canonical Event history unless justified by risk or obligation.

### 18.2 Immutability and Deletion

Event immutability prohibits in-place semantic rewriting of admitted canonical history. It does not require unlawful or contractually prohibited indefinite retention.

Required deletion/minimization MUST occur through an attributable governed process and MAY use deletion of the Event/payload under applicable retention semantics, separately governed payload references, cryptographic erasure or another mechanism that does not rewrite the retained Event to assert a different historical fact.

If deletion/minimization reduces retained evidence, reconstructability/explainability/reproducibility claims MUST be reduced accordingly.

### 18.3 Integrity Metadata

Canonical Events and high-consequence provenance MUST include integrity metadata proportionate to consequence and threat model.

Possible mechanisms include hashes, signatures, append-only storage controls, immutable object versions or external attestations. This RFC mandates no specific cryptographic mechanism.

### 18.4 Integrity Is Not Truth or Authority

A valid signature, checksum, append-only store or transport acknowledgement proves only the claim supported by that mechanism.

It does not automatically prove truth of an external fact, Organizational Authority, legal validity, ownership, reuse rights or permission to access/use the data.

## 19. Product Contract Boundary

Where a product relies on platform Events or exposes product Events through the platform, the applicable Product Contract MUST declare, proportionate to consequence:

- event type identities and schema versions/compatibility ranges;
- production/consumption direction;
- Organization scope;
- authority/source semantics;
- delivery and ordering expectations where relied upon;
- retry/duplicate/gap behavior;
- classification/data-handling constraints;
- retention/replay expectations where relevant;
- failure behavior;
- compatibility/migration expectations.

Products MUST NOT create governed dependence on private platform topics, undocumented streams, internal log formats, incidental CDC feeds, database tables or implementation-specific observability channels outside the Product Contract.

A Stable Product Contract does not make the underlying event infrastructure an `Active` Platform Capability, and a successful product event integration does not automatically promote product-domain event semantics into the platform.

## 20. External Systems, Portability and Migration

### 20.1 External Streams

External event feeds, webhooks, audit logs and CDC streams MAY be integrated, but authority scope, freshness, ordering, duplicate, retention and failure semantics MUST be explicit where consequential behavior relies on them.

A change-data feed MAY be transport/evidence, but it MUST NOT automatically become the semantic organizational Event model when it lacks organizational meaning.

### 20.2 External Observability Vendors

External telemetry/observability vendors MAY be used when applicable security, privacy, contract, retention, sovereignty and portability controls are satisfied.

Vendor representation MUST NOT become the only inaccessible representation of required governed operational history.

### 20.3 Semantic Portability

Governed export of relevant operational history SHOULD preserve, subject to applicable rights/deletion restrictions:

- Event identities/immutable versions;
- event type/schema identities;
- Organization scope;
- authority/source declarations;
- occurrence/recording time;
- subject/version, execution, correlation and causation references;
- provenance links;
- classification/retention metadata where exportable;
- integrity metadata necessary to interpret exported evidence.

Changing broker, log store, tracing backend or monitoring vendor MUST NOT require loss of retained semantic Event/Provenance meaning.

### 20.4 Incremental Migration

Existing product-local logs, audit tables, event buses and telemetry MAY migrate incrementally.

This RFC does not require historic low-value telemetry to be retroactively converted into canonical Events.

Migration MAY start with the highest-consequence event classes required for current Governed Execution and expand only when evidence/value justifies it.

Legacy evidence that cannot meet current provenance/schema requirements MAY remain accessible with explicit limitations rather than being rewritten to appear natively conformant.

## 21. Relationship to RFC-0007

Events, telemetry and provenance MAY provide inputs for later observations, learning or knowledge-validation workflows.

They MUST NOT automatically become:

- Organizational Memory;
- validated Knowledge;
- approved standards/policies/workflows;
- Governed Organizational Assets;
- reusable cross-organization intelligence.

RFC-0007 will define the Memory, Knowledge and Governed Learning lifecycle. This RFC intentionally does not pre-empt that decision.

## 22. Scoped Conformance

Conformance is scoped to the subject, Organization, product/workflow boundary and operational environment being assessed.

A conforming implementation within its declared scope MUST demonstrate that:

1. canonical Events conform to RFC-0002 identity, immutability and authority rules;
2. transport receipt is distinguished from canonical Event admission;
3. conflicting reuse of Event Identity cannot silently mutate history;
4. corrections/reversals/compensations/invalidations create additional linked Events;
5. meaningful consequential actions have attributable Event/evidence coverage proportionate to consequence;
6. telemetry and observability projections are not silently treated as canonical authority;
7. event type/schema semantics are version-identifiable and historical Events are not silently reinterpreted;
8. occurrence/recording time are distinguishable where materially different;
9. correlation and causation are distinguishable and neither implies authority;
10. required Event/evidence paths cannot fail silently during consequential action;
11. delivery contracts define duplicates, ordering, gaps/replay and failure where consequential correctness relies on them;
12. transport checkpoints do not replace Event/authority/execution evidence;
13. replay is side-effect safe unless a new Governed Execution explicitly authorizes action;
14. event-driven consequential consumers preserve triggering Event identity and pass RFC-0003/RFC-0005 gates;
15. provenance is sufficient for declared reconstruction without mandatory unnecessary sensitive-data retention;
16. cross-organization observability does not bypass tenant isolation, purpose or rights controls;
17. reusable secrets are not retained in ordinary observability data merely for convenience;
18. sensitive observability access and material evidence-control changes are attributable where consequence requires it;
19. retention/deletion does not falsify Event history or overstate reconstructability;
20. Product Contract event boundaries are explicit where RFC-0004 applies;
21. governed operational history remains semantically portable without dependence on one observability vendor;
22. Events/telemetry/provenance are not automatically promoted into RFC-0007 governed knowledge/memory.

## 23. Normative Fitness Scenarios

### Scenario A — Consequential mutation while event transport is unavailable

A workflow performs a consequential canonical mutation but the normal event transport is unavailable.

Conforming behavior: the system either durably establishes required Event evidence through another declared consistency path, fails/pauses, continues only under an explicitly governed bounded degraded mode, or enters an explicit reconciliation-required state. It does not silently report a fully complete governed result with no required evidence.

### Scenario B — Duplicate delivery

A consequential consumer receives the same Event three times.

Conforming behavior: the Event Identity remains the same; transport duplicates do not create three canonical Events; downstream consequential effects are deduplicated/idempotent or reconciled explicitly.

### Scenario C — Same Event Identity, different payload

A producer submits an Event Identity already admitted to history but with materially different payload.

Conforming behavior: the conflict is rejected/quarantined/escalated. The original Event is not overwritten and the second payload is not silently treated as the same immutable Event.

### Scenario D — Late external Event

An external authoritative system reports an occurrence after a dependent execution already completed.

Conforming behavior: the Event is appended with correct external authority and occurrence/recording context; prior execution remains evidence of what was known then; any material consequence is handled by a later governed reconciliation/review.

### Scenario E — Sensitive log

An exception contains an access token.

Conforming behavior: the reusable secret is not persisted for convenience; diagnostic evidence is redacted/minimized while sufficient failure attribution is preserved.

### Scenario F — AI-generated consequential artifact

An AI component drafts a document later approved and issued externally.

Conforming behavior: provenance identifies governing execution, material source/version references and materially relevant model/configuration information to the extent lawfully retained; AI is not represented as final Organizational Authority; approval remains attributable to the authorized mechanism.

### Scenario G — Cross-tenant correlation

Two Organizations use the same external correlation string.

Conforming behavior: the string does not join/expose their data automatically; each Event remains Organization-scoped; cross-organization access requires explicit governed rights and authorization.

### Scenario H — Replay for projection rebuild

An operator replays six months of Events into a new search projection.

Conforming behavior: replay preserves original Event identities and creates no new historical occurrences or consequential actions. If a new action is intentionally required, it receives a new Execution Identity and passes normal gates.

### Scenario I — Observability retention changed below required evidence window

An operator attempts to reduce retention for evidence required by a Product Contract or security policy.

Conforming behavior: the change is governed and attributable; it is rejected or approved only under applicable authority/policy. Required evidence is not silently removed by ordinary telemetry configuration.

## 24. Deferred Implementation Decisions

The following belong to later ADRs, standards or operational decisions when implementation evidence requires them:

- event persistence technology;
- broker/queue selection;
- physical Event envelope encoding;
- schema-registry technology;
- outbox/inbox implementation;
- trace propagation protocol;
- log/metric/trace backend;
- integrity/signature mechanism;
- telemetry sampling defaults;
- retention profiles;
- event partitioning/ordering mechanism;
- alerting/incident tooling.

No Accepted architecture currently requires one event broker, centralized observability service or specific telemetry vendor.

## 25. Risks and Consequences

### Event explosion

Risk: “nothing important happens silently” is misread as “store everything forever.”

Mitigation: canonical Event significance threshold; telemetry remains non-canonical by default; proportional retention/minimization.

### False exactly-once assumptions

Risk: transport delivery is mistaken for a unique organizational occurrence.

Mitigation: Event/delivery separation, stable Event Identity, explicit duplicate/idempotency semantics.

### Privacy shadow dataset

Risk: logs/traces become an uncontrolled duplicate of tenant data.

Mitigation: scope, classification, minimization, restricted access, governed evidence controls and retention limits.

### Provenance overcollection

Risk: explainability is used to justify indefinite retention of prompts, raw payloads or sensitive intermediate data.

Mitigation: provenance by reference, data minimization and qualified reconstruction claims.

### Event bus as authority

Risk: whichever message arrives first is treated as truth.

Mitigation: authority mode/source preserved independently from transport.

### Vendor lock-in

Risk: required operational history exists only in one proprietary observability backend.

Mitigation: technology-independent Event/Provenance semantics and governed export.

## 26. Review Evidence

Functional cross-review:

- `docs/reviews/RFC-0006-functional-cross-review.md` — `Complete`;
- iterations completed: `4` of maximum `7`;
- result: `Pass after bounded reconciliation`;
- no unresolved material architectural conflict identified for the proposal stage.

The review does not constitute owner approval.

## 27. Acceptance Criteria

RFC-0006 MAY be accepted only when:

1. it remains compatible with Constitution `1.2.0`;
2. it remains compatible with Accepted RFC-0001 through RFC-0005;
3. Event remains an RFC-0002 Canonical Record specialization with append-only single-version semantics;
4. provenance is not introduced as a competing Kernel primitive;
5. canonical Event history is clearly separated from operational telemetry/projections;
6. required consequential Event/evidence paths cannot fail silently;
7. delivery/replay semantics do not assume universal exactly-once transport or global ordering;
8. security/privacy/isolation/minimization rules remain at least as strong as RFC-0003;
9. Product Contract event boundaries remain explicit and product-domain semantics do not leak into the platform;
10. AI provenance does not create AI authority or require unjustified sensitive-data retention;
11. RFC-0007 Memory/Knowledge/Governed Learning scope is not pre-empted;
12. no irreversible observability technology commitment is introduced;
13. no unresolved material cross-review objection remains;
14. explicit owner approval exists independently before acceptance publication;
15. RFC Index and canonical roadmap are synchronized during acceptance publication and verified through read-after-write refresh under the approved RFC State Transition Procedure.

## 28. Current Decision State

Current status: `Proposed`.

RFC-0006 `0.2.0` is a reviewed proposal ready for owner decision. Functional cross-review does not constitute approval and gives this proposal no normative force until an independent owner-approved decision and complete acceptance publication occur.
