# Arvectum OS Architecture Glossary

Document status: `Active`
Version: `1.2.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Normative status: `Informative`
Source baseline: Constitution `1.2.0`; RFC-0001 through RFC-0007 `1.0.0` (`Accepted`)

## 1. Purpose

This glossary provides a shared architectural vocabulary for Arvectum OS.

It summarizes terms already established by the [Constitution](../constitution/CONSTITUTION.md) and Accepted RFCs so contributors, products and AI agents can resolve core meanings without relying on chat history, model memory or implementation conventions.

This document does not create independent architectural requirements. If a definition is incomplete, ambiguous or inconsistent with a higher-authority source, the Constitution and Accepted RFCs prevail.

## 2. Authority and usage

Terms are summarized from the following sources, in descending authority:

1. Constitution `1.2.0` — `Ratified`;
2. RFC-0001 `1.0.0` — `Accepted`;
3. RFC-0002 `1.0.0` — `Accepted`;
4. RFC-0003 `1.0.0` — `Accepted`;
5. RFC-0004 `1.0.0` — `Accepted`;
6. RFC-0005 `1.0.0` — `Accepted`;
7. RFC-0006 `1.0.0` — `Accepted`;
8. RFC-0007 `1.0.0` — `Accepted`.

Draft, Proposed and other non-Accepted artifacts may be useful for discussion but do not change the meanings recorded here.

## 3. Organizational and authority terms

### Organization

An **Organization** is the governance, authority, data-isolation and sovereignty scope within which an organization-specific Executable Organizational Model is operated.

Governed records, relationships, executions and artifacts carry or resolve to an Organization scope unless explicitly governed as platform-global or cross-organization shared state.

One organization's data, authority, memory or knowledge does not alter another organization's governed state without an explicit governed basis.

Canonical sources: Constitution Articles VII and VIII; RFC-0001 Sections 6.3, 17 and 19; RFC-0003 Section 7.

### Tenant

A **Tenant** is the technical isolation context used to enforce an Organization boundary or an explicitly governed subdivision of one Organization.

An Organization may use multiple technical tenant partitions. Each tenant context must resolve unambiguously to one governing Organization for authority and sovereignty evaluation. Multiple Organizations must not share one undifferentiated tenant authority context.

Tenant topology is an implementation/security mechanism; Organization is the governance and sovereignty boundary.

Canonical source: RFC-0003 Section 7.

### Organizational Intelligence

**Organizational Intelligence** is accumulated knowledge, operational experience, standards, workflows, decisions, relationships and institutional memory that strengthen future work.

Arvectum OS preserves and operationalizes only the portion the organization is entitled and chooses to govern. Processing organizational intelligence does not by itself transfer legal ownership or create cross-organization reuse rights.

Canonical sources: Constitution Article 0; RFC-0001 Section 6.1.

### Executable Organizational Model

The **Executable Organizational Model** is the durable governed representation of organizational intelligence through identities, records, relationships, authority, workflows, evidence and operational history.

It is executable because Governed Execution can act on governed state and produce records, Events and artifacts. It is organizational because meaning and authority come from the organization, contracts and governance rather than implementation technology.

Canonical source: RFC-0001 Section 6.2.

### Organization-specific Model Instance / Organizational Twin

An **Organization-specific Model Instance** is the isolated organization-specific instance or governed view of the Executable Organizational Model.

**Organizational Twin** is an informative descriptive term. It is not a separate Kernel primitive and does not imply a complete or real-time simulation of the organization.

Canonical source: RFC-0001 Section 6.3.

### Organizational Semantics

**Organizational Semantics** are stable meanings, authority rules and governed operating concepts that should survive changes in products and technologies.

The organization defines meaning, products specialize meaning, and technologies execute meaning.

Canonical source: RFC-0001 Section 6.4.

### Architectural Responsibility

**Architectural Responsibility** is responsibility for canonical state, lifecycle, contracts, validation, change control and operational support within Arvectum OS.

It is distinct from legal title, intellectual-property ownership, licensing rights, confidentiality obligations, contractual data rights and privacy-law roles.

Canonical sources: RFC-0001 Section 6.5; RFC-0002 Section 8.1.

### Authority Mode

An **Authority Mode** declares the relationship between a Canonical Record and authority for the governed subject.

Exactly three modes exist:

- `Native` — Arvectum OS is authoritative for the governed subject within the declared scope;
- `External Reference` — an external system remains authoritative and Arvectum OS governs a reference/retrieval contract;
- `Governed Replica` — an external system remains authoritative while Arvectum OS stores a synchronized governed representation.

External modes preserve external authority, freshness, conflict, failure and synchronization semantics rather than creating a competing source of truth.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 12.

### Authoritative Source

An **Authoritative Source** is the source designated as authoritative for a governed fact or subject within a declared scope.

Arvectum OS may be authoritative for its own governance envelope or organizational interpretation while another system remains authoritative for an underlying external fact.

Canonical sources: Constitution Article IV; RFC-0001 Section 7.1; RFC-0002 Section 12; RFC-0007 Section 7.2.

## 4. Kernel and canonical-state terms

### Kernel / Platform Kernel

The **Kernel** is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

RFC-0001 defines five primitives:

1. Identity;
2. Canonical Record;
3. Typed Relationship;
4. Event;
5. Execution Context.

RFC-0002 finalizes their metamodel: Identity is a stable non-record reference primitive; Canonical Record is the immutable governed representation at one version; Typed Relationship, Event and Execution Context are semantic specializations of Canonical Record.

Canonical sources: RFC-0001 Section 10; RFC-0002 Section 6.

### Identity

**Identity** is an opaque stable reference to one semantic referent within a declared identity namespace and organization/platform scope.

RFC-0002 distinguishes:

- **Subject Identity** — one logical governed subject across time;
- **Version Identity** — one exact immutable Canonical Record version.

Identity is immutable after issuance, non-recycled and independent of mutable business meaning. Possessing or resolving an Identity grants neither permission nor Organizational Authority.

Canonical source: RFC-0002 Section 7.

### Canonical Record

A **Canonical Record** is the immutable governed representation of one logical subject at one specific version.

A changeable subject has one stable Subject Identity and an unambiguous lineage of immutable versions, each with its own Version Identity.

The common record envelope carries or resolves governance semantics such as Organization scope, authority, accountable ownership, provenance, classification/access and applicable retention/deletion constraints. The model is semantic and does not mandate one physical table or database.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 8.

### Significant Governed Object

A **Significant Governed Object** is an object whose state or meaning materially affects organizational meaning, authority, production behavior, external commitments, security, financial/legal position, canonical state, reusable assets or reconstruction of a consequential result.

Non-significant technical state does not become canonical merely because it is persisted.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 8.8.

### Canonical Lineage

A **Canonical Lineage** is one unambiguous sequence of immutable Canonical Record versions for a governed subject within one declared authority scope.

Drafts, simulations and alternatives may exist outside that lineage but do not silently create parallel canonical heads.

Canonical source: RFC-0002 Section 8.3.

### Canonical Head

The **Canonical Head** is the latest admitted version in a Canonical Lineage.

It is a lineage concept and is not necessarily the version effective for a particular evaluation context.

Canonical source: RFC-0002 Section 8.4.

### Effective Version

The **Effective Version** is the canonical version applicable for a declared evaluation context, such as effective time or authority scope.

Consequential reliance on a mutable Subject Identity resolves and preserves the exact Version Identity materially used.

Canonical sources: RFC-0002 Sections 8.5 and 14.

### Canonical State

**Canonical State** is authoritative governed state managed by Arvectum OS within a declared scope.

Consequential changes to canonical state managed by Arvectum OS occur through Governed Execution. Canonical state must not be confused with caches, projections, indexes, transient outputs or underlying external facts that remain authoritative elsewhere.

Canonical sources: Constitution Article IV; RFC-0001 Sections 7.1 and 7.5; RFC-0005 Section 13.

### Typed Relationship

A **Typed Relationship** is a Canonical Record specialization representing one governed semantic relationship assertion instance from a source reference to a target reference.

It has a stable Relationship Identity and immutable versions. Endpoints distinguish Subject Identity references from exact Version Identity references. Relationship existence does not itself grant access, delegation, approval power or cross-organization visibility.

Canonical sources: RFC-0002 Section 9; RFC-0003 Section 11.4.

### Event

An **Event** is a Canonical Record specialization representing an append-only governed observation/assertion that something meaningful occurred.

One Event has a stable Event Identity and normally one immutable canonical version. Correction, reversal, compensation or invalidation creates additional linked Events rather than mutation.

Receiving a queue message, webhook, log entry or CDC row is not the same as admitting a canonical Event.

Canonical sources: RFC-0002 Section 10; RFC-0006 Sections 6–8.

### Execution Context

An **Execution Context** is a Canonical Record specialization representing one governed execution instance.

One execution has one stable Execution Identity and immutable versions for governance-significant transitions. Exact materially relied-upon versions are preserved for reconstruction. A terminal execution version is sealed.

Canonical sources: RFC-0002 Section 11; RFC-0005 Sections 6 and 8.

### Governed Organizational Asset

A **Governed Organizational Asset** is an explicit governed designation applied to a Canonical Record, lineage, represented artifact or another governed subject designated as authoritative, reusable, evidentiary or operationally significant.

It is not a sixth Kernel primitive. Persistence alone does not create asset status, and asset status does not create legal ownership or cross-organization reuse rights.

Canonical sources: Constitution Article XVI; RFC-0001 Section 7.2; RFC-0002 Section 13.

### Transient Output

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

AI output, generated content, caches and intermediate results are transient by default unless an applicable governed process promotes them.

Canonical sources: RFC-0001 Section 7.3; RFC-0002 Section 13.4; RFC-0005 Section 20.

## 5. Identity, security, privacy and authority terms

### Principal

A **Principal** is an RFC-0002 Subject Identity that may participate in authentication, authorization or authority evaluation.

Principal categories may include human, service, workload, external system, AI agent/mediated actor or integration client. Category is governed state and is not inferred from identifier syntax alone.

Canonical source: RFC-0003 Section 8.1.

### Actor

An **Actor** is the Principal acting in a specific execution context together with relevant representation, delegation and authentication context.

The same Principal may act under different organizations, grants, delegations and assurance levels without changing Identity.

Canonical source: RFC-0003 Section 8.2.

### Authentication

**Authentication** establishes contextual evidence that an actor controls, represents or acts through an asserted Principal Identity.

Authentication is evidence, not authorization or permanent identity state.

Canonical source: RFC-0003 Sections 6.3 and 10.

### Authorization

**Authorization** is the explicit deny-by-default decision whether an actor may perform an operation on a governed resource under applicable Organization scope, policy and context.

An allow decision has an explicit governed basis. Authentication, relationship existence or technical possession of a contract does not imply authorization.

Canonical source: RFC-0003 Section 11.

### Organizational Authority

**Organizational Authority** is entitlement to make or approve a consequential organizational decision or state change.

Technical authorization does not substitute for Organizational Authority. Delegation is explicit governed state and AI does not acquire independent authority merely by receiving tool access.

Canonical sources: RFC-0003 Sections 6.5 and 12; RFC-0005 Section 12.

### Data Governance

**Data Governance** is the set of governed constraints determining whether collection, use, disclosure, retention, export, deletion or cross-organization movement is permitted for a declared purpose.

It remains distinct from authentication, authorization and Organizational Authority.

Canonical source: RFC-0003 Sections 6 and 16–20.

### Tenant Isolation

**Tenant Isolation** is the structural property that prevents one Organization's governed or sensitive state from becoming visible or mutable from another Organization without explicit governed authorization.

Unresolved Organization scope fails closed. Background jobs, caches, indexes, AI context and other asynchronous/derived paths remain Organization-scoped.

Canonical source: RFC-0003 Section 14.

### Break-glass

**Break-glass** is an explicitly governed exceptional emergency-access path.

It is attributable, purpose- and time-bounded, minimal in scope, observable and reviewable, and cannot silently become a permanent grant.

Canonical source: RFC-0003 Section 13.2.

### Organizational Control and Portability

**Organizational Control and Portability** require that an organization retain governance over its data, intelligence, decisions and operational history and can perform governed export, migration, deletion, termination and handover within applicable rights and constraints.

Portability preserves semantic identity, versions, authority, relationships and required history; it is not merely a raw database dump and does not require export of prohibited/non-exportable secrets.

Canonical sources: Constitution Article VII; RFC-0001 Sections 18–19; RFC-0003 Sections 20–21.

### Proportionality

**Proportionality** means governance, standardization, evidence, security and operational rigor match risk, consequence, maturity, reversibility and organizational value.

It permits bounded manual or provisional controls when appropriate but does not waive structural security, isolation, legal, contractual or Accepted RFC requirements.

Canonical sources: Constitution Articles VIII, XIII and XVII; RFC-0001 cross-cutting; RFC-0003 Section 25.

## 6. Product and platform terms

### Product

A **Product** is architecturally responsible by default for domain meaning, domain schemas, workflows, validation, knowledge, integrations, user experience, commercial behavior and bounded Product Experiments.

Products consume shared platform behavior through explicit boundaries where platform interaction exists.

Canonical sources: Constitution Articles II, III and XX; RFC-0001 Section 12; RFC-0004 Section 6.

### Product Experiment

A **Product Experiment** is bounded, reversible work under product or operational responsibility while uncertainty is high.

A fully product-local experiment may operate without a Product Contract when it does not consume Platform Capabilities, canonical platform state or shared platform history. Success does not automatically promote it into the platform.

Canonical sources: RFC-0001 Section 11.1; RFC-0004 Sections 7 and 13.

### Product Contract

A **Product Contract** is the explicit versioned product/platform boundary.

It records only boundary-relevant semantics such as platform dependencies, domain types crossing the boundary, canonical reads/writes, operations, Events/artifacts, security/authority/data handling, portability, compatibility, migration and support status.

It is not a security credential and does not grant authorization or Organizational Authority.

Canonical source: RFC-0004.

### Product Contract lifecycle

The lifecycle is:

`Draft → Provisional → Stable → Deprecated → Retired`.

`Provisional` is the normal bounded early-integration state. `Stable` means the declared product/platform boundary is approved as a durable supported integration contract for its scope. Contract lifecycle does not change Platform Capability lifecycle.

Canonical source: RFC-0004 Section 9.

### Platform Capability

A **Platform Capability** is a reusable domain-neutral organizational ability exposed by Arvectum OS.

It is responsibility plus contract, not merely code.

Lifecycle:

`Candidate → Incubating → Active → Deprecated → Retired`.

Successful implementation or reuse does not automatically advance lifecycle.

Canonical source: RFC-0001 Sections 11.2–11.4.

### Candidate

A **Candidate** is a proposed Platform Capability with declared outcome, responsibility, consumer/reuse hypothesis and disposition criteria.

Candidate status is not an implementation or support commitment.

Canonical source: RFC-0001 Section 11.2.

### Incubating

An **Incubating** capability is undergoing bounded platform incubation under a provisional domain-neutral contract and explicit exit criteria.

It is not `Active` and must not be marketed as a stable supported platform capability.

Canonical source: RFC-0001 Section 11.2.

### Active

An **Active** capability has met applicable admission requirements, stable contract expectations and approved operational readiness for its declared scope.

`Active` is a capability lifecycle state, not a synonym for `Production` environment.

Canonical source: RFC-0001 Sections 11.2–11.4 and 24.

### Deprecated / Retired

A **Deprecated** capability remains in managed exit while consumers migrate under declared responsibilities.

A **Retired** capability has ended platform responsibility after applicable history, migration and commitment obligations are addressed.

Canonical source: RFC-0001 Section 11.4.

### Platform Service

A **Platform Service** is an implementation and architectural-responsibility boundary realizing one or more Platform Capabilities.

It is not necessarily a separate process, repository or deployment unit. Service boundaries must not be inferred from microservice topology.

Canonical source: RFC-0001 Section 11.5.

### Extension

An **Extension** is a registered and versioned component/artifact that extends product or platform behavior through a declared contract without redefining Kernel or shared platform invariants.

Registration makes it governable/discoverable and does not itself grant permission, Organizational Authority, cross-organization visibility or `Active` capability status.

Canonical source: RFC-0004 Section 15.

### Platform Gravity

**Platform Gravity** is the informative idea that the platform should become easier to reuse than to replace because it creates real value rather than coercive dependency.

Canonical source: RFC-0001 Section 22.

### Platform Evidence

**Platform Evidence** is measurable evidence used to determine whether shared platform responsibility creates organizational value through reuse, delivery speed, operating cost, reliability, quality, risk reduction, governance, security, portability and integration effort.

Canonical source: RFC-0001 Section 26.

## 7. Governed Execution, Event and provenance terms

### Workflow

A **Workflow** is a versioned governed definition of how repeatable or operationally significant work is performed.

One admitted Workflow version is immutable. Consequential execution preserves the exact effective Workflow Version Identity.

Product-specific business workflow meaning remains product-owned by default.

Canonical source: RFC-0005 Sections 6–7.

### Governed Execution

**Governed Execution** is performance of work inside an Execution Context under applicable authentication evidence, authorization, Organizational Authority, data-governance, validation, approval and evidence requirements.

Every consequential change to canonical state managed by Arvectum OS occurs through Governed Execution and an authorized operation.

Canonical source: RFC-0005 Sections 6.4 and 13.

### Operation

An **Operation** is a stable semantic action against governed state, an external system or a controlled side-effect boundary.

RFC-0005 distinguishes at least:

- `ReadOnly`;
- `Transient`;
- `CanonicalMutation`;
- `ExternalMutation`;
- `Commitment`.

One operation may belong to more than one side-effect class.

Canonical source: RFC-0005 Section 10.

### Idempotency / Uncertainty / Reconciliation

**Idempotency** describes whether retry can repeat an operation safely without duplicating consequential effects.

When the outcome of a non-idempotent external action is unknown, execution enters an explicit uncertainty/reconciliation path instead of blindly retrying.

Canonical source: RFC-0005 Section 15.

### Provenance

**Provenance** is traceable origin and lineage information linking governed records, Events, artifacts and executions to material sources, actors, versions and transformations.

It is not a sixth Kernel primitive. Provenance may be represented by governed references, Events, Execution Contexts, relationships, manifests and external-source evidence.

Canonical source: RFC-0006 Section 14.

### Operational Telemetry

**Operational Telemetry** is diagnostic data such as logs, metrics, traces, health signals and delivery metadata used to understand runtime behavior.

Telemetry is non-canonical by default and may be sampled, aggregated or retention-bounded when required governed evidence is preserved.

Canonical source: RFC-0006 Sections 6.2 and 16.

### Event admission

**Event admission** is the governed step that accepts an occurrence into canonical Event history after resolving/validating required identity, schema, Organization scope, authority/source, attribution, classification, provenance/integrity and payload interpretability.

Transport receipt is not admission.

Canonical source: RFC-0006 Section 7.

### Correlation and causation

**Correlation** groups records that may share context.

**Causation** records a material causal relation to a triggering Event, Execution, operation/command or other governed object.

Correlation is not causation. Neither creates authorization, Organizational Authority or cross-organization rights.

Canonical source: RFC-0006 Section 10.

### Replay

**Replay** reprocesses an existing Event representation/reference while preserving the original Event Identity.

Projection rebuild replay is side-effect safe. If replay intentionally causes a new consequential action, that action receives a new Execution Identity and normal Governed Execution controls.

Canonical source: RFC-0006 Section 13.5.

## 8. Memory, knowledge and learning terms

### Observation

An **Observation** is an observed operational result, pattern, assertion, signal or fact carried forward for evaluation in the Governed Learning Loop.

Observation is a semantic role, not a new Kernel primitive and not validated Knowledge merely because it is repeated, confident, stored or AI-generated.

Canonical source: RFC-0007 Section 6.1.

### Organizational Memory

**Organizational Memory** is the structured, versioned body of organizational records, relationships, provenance and evolution retained so experience and context survive transient conversations, people, model context windows and technologies.

Memory preserves epistemic and authority status. Remembering an assertion does not validate it.

Canonical source: RFC-0007 Section 6.2.

### Knowledge Candidate

A **Knowledge Candidate** is a governed proposal that a claim, rule, interpretation, model or reusable understanding should become Knowledge.

It is explicitly not Knowledge until applicable validation and approval gates succeed.

Canonical source: RFC-0007 Section 6.3.

### Improvement Proposal

An **Improvement Proposal** proposes a change to an approved organizational asset or behavior such as a Standard, Policy, Workflow, Product Contract, validator or capability contract.

Validated Knowledge may justify an Improvement Proposal, but it does not silently change production behavior.

Canonical sources: RFC-0007 Sections 6.4 and 19.

### Knowledge

**Knowledge** is validated organizational understanding within a declared scope.

Significant Knowledge uses Canonical Record identity/version semantics and carries or resolves applicability, provenance/evidence, validation, authority/source, approval where required, rights/classification, freshness and supersession/retraction information.

A Native Knowledge Record may be authoritative for the organization's adopted interpretation while an external system remains authoritative for an underlying external fact.

Canonical sources: RFC-0007 Sections 6.5 and 7.

### Knowledge lifecycle / applicability state

Knowledge may distinguish states such as `Current`, `Review Required`, `Superseded`, `Retracted` and `Retired` where those distinctions affect reliance.

Contradiction or changed evidence does not rewrite historical versions; it triggers explicit review, supersession, retraction or another governed outcome.

Canonical sources: RFC-0007 Sections 9–11.

### Governed Learning Loop

The **Governed Learning Loop** is the controlled path:

```text
Governed Execution
        ↓
Events / Outcomes / Sources
        ↓
Observation
        ↓
Organizational Memory
        ↓
Knowledge Candidate or Improvement Proposal
        ↓
Validation + authority/source + rights/classification review
        ↓
Approval where required
        ↓
Knowledge or separately governed change path
        ↓
Future Governed Execution
```

Learning can propose changes but does not silently mutate approved Standards, Policies, Workflows, Product Contracts or capability lifecycle.

Canonical sources: RFC-0001 Section 8; RFC-0007 Section 8.

### Retrieval / RAG / derived projections

**Retrieval**, **RAG**, embeddings, vector/lexical indexes, caches, summaries and derived graph projections are execution/retrieval techniques and non-canonical projections by default.

Retrieval does not prove truth, current applicability, authority or permission to use. Consequential reliance resolves to governed exact source versions rather than treating a ranking/index hit as authority.

Canonical sources: RFC-0007 Sections 14–15.

## 9. Governance, AI and conformance terms

### Decision Authority

**Decision Authority** is the accountable authority permitted to approve a governed decision within its declared scope.

Until approved delegation exists, residual authority remains with the Owner under Accepted rules. The current Decision Authority Policy must not be treated as effective while its canonical status remains `Proposed`.

Canonical source: RFC-0001 Section 16.

### Architectural Exception

An **Architectural Exception** is an approved scoped deviation from an otherwise applicable architectural requirement.

It records scope, authority, rationale, risk, review/expiry and exit path and does not silently rewrite the underlying rule.

Canonical source: RFC-0001 Sections 15–16.

### Operational Readiness

**Operational Readiness** is proportionate evidence and approval required before a Platform Capability becomes `Active` for its declared scope.

It may address support ownership, observability/health, incident/recovery, continuity/dependencies, backup/reconstruction, migration/deprecation and customer-facing commitments.

Operational readiness is distinct from reference implementation readiness.

Canonical source: RFC-0001 Sections 11.2–11.3.

### Commercial Commitment Integrity

**Commercial Commitment Integrity** means externally relied-upon language must remain within approved lifecycle, contract, conformance and operational-readiness state.

Product Experiments, Candidates and Incubating capabilities must not be represented as `Active`; a technical implementation does not create an SLA, support guarantee, compatibility promise or full-platform conformance claim.

Canonical sources: RFC-0001 Section 14; RFC-0004 Section 22.

### AI Authority

**AI Authority** is the boundary that AI is an execution, analysis and proposal mechanism rather than an independent organizational authority source.

AI may analyze, retrieve, classify, generate, recommend, propose and execute bounded authorized operations. AI does not independently grant permissions, create Organizational Authority, serve as final consequential approver, silently promote Knowledge, expand data rights or mutate approved governance/production behavior.

Canonical sources: Constitution Article XIII; RFC-0003 Section 23; RFC-0005 Section 14; RFC-0007 Section 13.

### Conformance

**Conformance** is assessed against an explicit scope, not every possible future Arvectum OS capability.

It separates:

1. subject lifecycle;
2. operational environment;
3. conformance maturity.

Canonical source: RFC-0001 Section 24.

### Subject Lifecycle

The conformance lifecycle axis may use:

- `Product Experiment`;
- `Candidate`;
- `Incubating`;
- `Active`;
- `Deprecated`;
- `Retired`;
- `Not Applicable`.

Canonical source: RFC-0001 Section 24.

### Operational Environment

Operational environment may include:

- `Local`;
- `Development`;
- `Test`;
- `Pilot`;
- `Production`.

Environment is separate from lifecycle. `Production` does not mean `Active`.

Canonical source: RFC-0001 Section 24.

### Conformance Maturity

Conformance maturity may be:

- `Draft`;
- `Provisional`;
- `Scoped`;
- `Scoped with Exceptions`;
- `Not Conformant`.

Canonical source: RFC-0001 Section 24.

### Provisional

**Provisional** means intentionally not yet stable/final within the relevant artifact or lifecycle context.

The Kernel metamodel is no longer provisional after RFC-0002 acceptance, but Provisional Product Contracts, provisional implementation choices and Provisional conformance maturity remain valid distinct concepts.

Canonical sources: RFC-0001 Sections 11, 13 and 24; RFC-0002; RFC-0004.

## 10. Terms and implementation choices intentionally not finalized here

The foundational semantic sequence through RFC-0007 is Accepted. The following remain deliberately subordinate or deferred rather than silently finalized by this glossary:

- global identifier wire encoding;
- database/storage topology and physical schemas;
- repository/package layout;
- programming language/runtime;
- API/RPC/message protocol;
- authentication provider and concrete authorization engine;
- cryptographic algorithms and key-management technology;
- event broker, event-store and observability backend;
- workflow/orchestration engine;
- concrete Product Contract serialization/registry technology;
- relationship/event/knowledge catalogs not already standardized;
- Memory/Knowledge persistence and retrieval technology;
- chunking, embedding, vector/lexical/graph indexing technology;
- LLM/model provider and agent framework;
- product-specific schemas, workflows, ontologies, policies and domain knowledge;
- concrete operational-readiness standards, SLOs, RTO/RPO and support procedures;
- detailed Document and Artifact Architecture reserved in the RFC-0001 follow-up sequence for RFC-0008 unless later canonical governance changes that scope.

These choices belong to the lowest sufficient subordinate artifact when implementation or product evidence makes them necessary.

## 11. Quick source map

| Term family | Primary canonical source |
|---|---|
| Organizational Intelligence / Executable Organizational Model | Constitution Article 0; RFC-0001 §6 |
| Organization / Tenant / Principal / Actor | RFC-0003 §§7–8 |
| Authentication / Authorization / Organizational Authority | RFC-0003 §§6, 10–12 |
| Security / privacy / isolation / portability | RFC-0003 §§14–21 |
| Kernel metamodel | RFC-0002 §6 |
| Identity | RFC-0002 §7 |
| Canonical Record / lineage / head / effective version | RFC-0002 §§8, 14 |
| Typed Relationship | RFC-0002 §9 |
| Event | RFC-0002 §10; RFC-0006 §§6–13 |
| Execution Context | RFC-0002 §11; RFC-0005 |
| Authority modes | RFC-0001 §7.1; RFC-0002 §12 |
| Governed Organizational Asset / Transient Output | RFC-0002 §13 |
| Product Experiment / Product Contract / Extension | RFC-0004 |
| Platform Capability lifecycle | RFC-0001 §11 |
| Workflow / Governed Execution / Operation | RFC-0005 |
| Provenance / telemetry / replay | RFC-0006 |
| Observation / Memory / Candidate / Knowledge | RFC-0007 |
| Retrieval / RAG / projections | RFC-0007 §§14–15 |
| Decision Authority / Operational Readiness | RFC-0001 §§11, 16 |
| Commercial Commitment Integrity | RFC-0001 §14; RFC-0004 §22 |
| AI authority | Constitution XIII; RFC-0003/0005/0007 |
| Conformance | RFC-0001 §§24–25 |

## 12. Maintenance note

This glossary is a navigation and language artifact, not a substitute for Accepted architecture.

When a later Accepted source refines a term, update this glossary to:

1. preserve the established term where still valid;
2. point to the newer Accepted source;
3. distinguish refinement from supersession;
4. remove stale statements that describe already-Accepted scope as future/deferred;
5. avoid introducing requirements that do not exist in higher-authority sources.