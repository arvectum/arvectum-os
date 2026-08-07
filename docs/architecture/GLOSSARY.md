# Arvectum OS Architecture Glossary

Document status: `Active`
Version: `1.3.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Normative status: `Informative`
Source baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

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
8. RFC-0007 `1.0.0` — `Accepted`;
9. RFC-0008 `1.0.0` — `Accepted`.

Draft, Proposed and other non-Accepted artifacts may be useful for discussion but do not change the meanings recorded here.

## 3. Organizational and authority terms

### Organization

An **Organization** is the governance, authority, data-isolation and sovereignty scope within which an organization-specific Executable Organizational Model is operated.

Governed records, relationships, executions and artifacts carry or resolve to an Organization scope unless explicitly governed as platform-global or cross-organization shared state.

Canonical sources: Constitution Articles VII and VIII; RFC-0001 Sections 6.3, 17 and 19; RFC-0003 Section 7.

### Tenant

A **Tenant** is the technical isolation context used to enforce an Organization boundary or an explicitly governed subdivision of one Organization.

Tenant topology is an implementation/security mechanism; Organization is the governance and sovereignty boundary.

Canonical source: RFC-0003 Section 7.

### Organizational Intelligence

**Organizational Intelligence** is accumulated knowledge, operational experience, standards, workflows, decisions, relationships and institutional memory that strengthen future work.

Canonical sources: Constitution Article 0; RFC-0001 Section 6.1.

### Executable Organizational Model

The **Executable Organizational Model** is the durable governed representation of organizational intelligence through identities, records, relationships, authority, workflows, evidence and operational history.

It is executable because Governed Execution can act on governed state and produce records, Events and artifacts.

Canonical source: RFC-0001 Section 6.2.

### Organization-specific Model Instance / Organizational Twin

An **Organization-specific Model Instance** is the isolated organization-specific instance or governed view of the Executable Organizational Model.

**Organizational Twin** is an informative descriptive term, not a separate Kernel primitive or promise of complete real-time simulation.

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

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 12.

### Authoritative Source

An **Authoritative Source** is the source designated as authoritative for a governed fact or subject within a declared scope.

Arvectum OS may govern its own organizational interpretation while another system remains authoritative for an underlying external fact.

Canonical sources: Constitution Article IV; RFC-0001 Section 7.1; RFC-0002 Section 12; RFC-0007 Section 7.2; RFC-0008 accepted document authority model.

## 4. Kernel and canonical-state terms

### Kernel / Platform Kernel

The **Kernel** is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

The five primitives are:

1. Identity;
2. Canonical Record;
3. Typed Relationship;
4. Event;
5. Execution Context.

Document, Artifact, Observation, Memory, Knowledge and Provenance do not add Kernel primitives.

Canonical sources: RFC-0001 Section 10; RFC-0002 Section 6; RFC-0008 `1.0.0` Section 3.

### Identity

**Identity** is an opaque stable reference to one semantic referent within a declared identity namespace and organization/platform scope.

RFC-0002 distinguishes **Subject Identity** from **Version Identity**. Possessing or resolving Identity grants neither permission nor Organizational Authority.

Canonical source: RFC-0002 Section 7.

### Canonical Record

A **Canonical Record** is the immutable governed representation of one logical subject at one specific version.

A changeable subject has one stable Subject Identity and an unambiguous lineage of immutable versions, each with its own Version Identity.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 8.

### Significant Governed Object

A **Significant Governed Object** is an object whose state or meaning materially affects organizational meaning, authority, production behavior, external commitments, security, financial/legal position, canonical state, reusable assets or reconstruction of a consequential result.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 8.8.

### Canonical Lineage

A **Canonical Lineage** is one unambiguous sequence of immutable Canonical Record versions for a governed subject within one declared authority scope.

Canonical source: RFC-0002 Section 8.3.

### Canonical Head

The **Canonical Head** is the latest admitted version in a Canonical Lineage. It is not necessarily the version effective for a particular evaluation context.

Canonical source: RFC-0002 Section 8.4.

### Effective Version

The **Effective Version** is the canonical version applicable for a declared evaluation context. Consequential reliance preserves the exact Version Identity materially used.

Canonical sources: RFC-0002 Sections 8.5 and 14.

### Canonical State

**Canonical State** is authoritative governed state managed by Arvectum OS within a declared scope.

Consequential changes to canonical state managed by Arvectum OS occur through Governed Execution.

Canonical sources: Constitution Article IV; RFC-0001 Sections 7.1 and 7.5; RFC-0005.

### Typed Relationship

A **Typed Relationship** is a Canonical Record specialization representing one governed semantic relationship assertion instance from a source reference to a target reference.

Canonical sources: RFC-0002 Section 9; RFC-0003 Section 11.4.

### Event

An **Event** is a Canonical Record specialization representing an append-only governed observation/assertion that something meaningful occurred.

Transport receipt is not Event admission.

Canonical sources: RFC-0002 Section 10; RFC-0006.

### Execution Context

An **Execution Context** is a Canonical Record specialization representing one governed execution instance with immutable governance-significant versions.

Canonical sources: RFC-0002 Section 11; RFC-0005.

### Governed Organizational Asset

A **Governed Organizational Asset** is an explicit governed designation applied to a Canonical Record, lineage, represented artifact or another governed subject designated as authoritative, reusable, evidentiary or operationally significant.

Persistence alone does not create asset status.

Canonical sources: Constitution Article XVI; RFC-0001 Section 7.2; RFC-0002 Section 13; RFC-0008 Section 3.

### Transient Output

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

AI-generated documents/artifacts are transient by default unless an applicable governed process promotes them.

Canonical sources: RFC-0001 Section 7.3; RFC-0002 Section 13.4; RFC-0005; RFC-0008 Section 3.

## 5. Identity, security, privacy and authority terms

### Principal

A **Principal** is an RFC-0002 Subject Identity that may participate in authentication, authorization or authority evaluation.

Canonical source: RFC-0003 Section 8.1.

### Actor

An **Actor** is the Principal acting in a specific execution context together with relevant representation, delegation and authentication context.

Canonical source: RFC-0003 Section 8.2.

### Authentication

**Authentication** establishes contextual evidence that an actor controls, represents or acts through an asserted Principal Identity.

Authentication is evidence, not authorization or permanent identity state.

Canonical source: RFC-0003 Sections 6.3 and 10.

### Authorization

**Authorization** is the explicit deny-by-default decision whether an actor may perform an operation on a governed resource under applicable Organization scope, policy and context.

Canonical source: RFC-0003 Section 11.

### Organizational Authority

**Organizational Authority** is entitlement to make or approve a consequential organizational decision or state change.

Technical authorization and signature evidence do not automatically create Organizational Authority.

Canonical sources: RFC-0003 Sections 6.5 and 12; RFC-0005; RFC-0008 Section 3.

### Data Governance

**Data Governance** is the governed constraints determining whether collection, use, disclosure, retention, export, deletion or cross-organization movement is permitted for a declared purpose.

Canonical source: RFC-0003 Sections 6 and 16–20.

### Tenant Isolation

**Tenant Isolation** prevents one Organization's governed or sensitive state from becoming visible or mutable from another Organization without explicit governed authorization.

Canonical source: RFC-0003 Section 14.

### Break-glass

**Break-glass** is an explicitly governed exceptional emergency-access path that is attributable, purpose/time-bounded, minimal, observable and reviewable.

Canonical source: RFC-0003 Section 13.2.

### Organizational Control and Portability

**Organizational Control and Portability** require that an organization retain governance over its data, intelligence, decisions and operational history and can perform governed export, migration, deletion, termination and handover within applicable rights and constraints.

Canonical sources: Constitution Article VII; RFC-0001 Sections 18–19; RFC-0003 Sections 20–21; RFC-0008 Section 3.

### Proportionality

**Proportionality** means governance, standardization, evidence, security and operational rigor match risk, consequence, maturity, reversibility and organizational value.

Canonical sources: Constitution Articles VIII, XIII and XVII; RFC-0001; RFC-0003 Section 25; RFC-0008 Section 3.

## 6. Product and platform terms

### Product

A **Product** is architecturally responsible by default for domain meaning, domain schemas, workflows, validation, knowledge, integrations, user experience, commercial behavior and bounded Product Experiments.

Canonical sources: Constitution Articles II, III and XX; RFC-0001 Section 12; RFC-0004.

### Product Experiment

A **Product Experiment** is bounded, reversible work under product or operational responsibility while uncertainty is high.

A fully product-local experiment may operate without a Product Contract when it does not consume Platform Capabilities, canonical platform state or shared platform history.

Canonical sources: RFC-0001 Section 11.1; RFC-0004.

### Product Contract

A **Product Contract** is the explicit versioned product/platform boundary.

It may declare Event and Artifact surfaces, but does not grant authorization or Organizational Authority and must not expose hidden storage/DMS internals as accidental contracts.

Canonical sources: RFC-0004; RFC-0008 Section 4.

### Product Contract lifecycle

`Draft → Provisional → Stable → Deprecated → Retired`.

Canonical source: RFC-0004.

### Platform Capability

A **Platform Capability** is a reusable domain-neutral organizational ability exposed by Arvectum OS.

Lifecycle:

`Candidate → Incubating → Active → Deprecated → Retired`.

Successful implementation, RFC acceptance or reuse does not automatically advance capability lifecycle.

Canonical source: RFC-0001 Sections 11.2–11.4; RFC-0008 Section 5.

### Candidate

A **Candidate** is a proposed Platform Capability with declared outcome, responsibility, consumer/reuse hypothesis and disposition criteria.

Canonical source: RFC-0001 Section 11.2.

### Incubating

An **Incubating** capability is undergoing bounded platform incubation under a provisional domain-neutral contract and explicit exit criteria.

Canonical source: RFC-0001 Section 11.2.

### Active

An **Active** capability has met applicable admission requirements, stable contract expectations and approved operational readiness for its declared scope.

`Active` is not a synonym for `Production` environment.

Canonical source: RFC-0001 Sections 11.2–11.4 and 24.

### Deprecated / Retired

A **Deprecated** capability remains in managed exit. A **Retired** capability has ended platform responsibility after applicable history, migration and commitment obligations are addressed.

Canonical source: RFC-0001 Section 11.4.

### Platform Service

A **Platform Service** is an implementation and architectural-responsibility boundary realizing one or more Platform Capabilities. It is not necessarily a separate process or deployment unit.

Canonical source: RFC-0001 Section 11.5.

### Extension

An **Extension** is a registered and versioned component/artifact that extends product or platform behavior through a declared contract without redefining Kernel or shared platform invariants.

Canonical source: RFC-0004.

### Platform Gravity

**Platform Gravity** is the informative idea that the platform should become easier to reuse than to replace because it creates real value rather than coercive dependency.

Canonical source: RFC-0001 Section 22.

### Platform Evidence

**Platform Evidence** is measurable evidence used to determine whether shared platform responsibility creates organizational value.

Canonical source: RFC-0001 Section 26.

## 7. Governed Execution, Event and provenance terms

### Workflow

A **Workflow** is a versioned governed definition of how repeatable or operationally significant work is performed.

Canonical source: RFC-0005.

### Governed Execution

**Governed Execution** is performance of work inside an Execution Context under applicable authentication, authorization, Organizational Authority, data-governance, validation, approval and evidence requirements.

Canonical source: RFC-0005.

### Operation

An **Operation** is a stable semantic action against governed state, an external system or a controlled side-effect boundary.

RFC-0005 distinguishes `ReadOnly`, `Transient`, `CanonicalMutation`, `ExternalMutation` and `Commitment` semantics.

Canonical source: RFC-0005.

### Idempotency / Uncertainty / Reconciliation

**Idempotency** describes whether retry can repeat an operation safely without duplicating consequential effects. Unknown outcomes enter an explicit uncertainty/reconciliation path rather than blind retry.

Canonical source: RFC-0005.

### Provenance

**Provenance** is traceable origin and lineage linking governed records, Events, artifacts and executions to material sources, actors, versions and transformations.

It is not a Kernel primitive.

Canonical sources: RFC-0006; RFC-0008 Section 3.

### Operational Telemetry

**Operational Telemetry** is diagnostic data such as logs, metrics, traces, health signals and delivery metadata. It is non-canonical by default.

Canonical source: RFC-0006.

### Event admission

**Event admission** is the governed step that accepts an occurrence into canonical Event history after applicable validation. Transport receipt is not admission.

Canonical source: RFC-0006.

### Correlation and causation

**Correlation** groups records that may share context. **Causation** records a material causal relation. Neither creates authorization or Organizational Authority.

Canonical source: RFC-0006.

### Replay

**Replay** reprocesses an existing Event representation/reference while preserving the original Event Identity. New consequential effects require a new Governed Execution.

Canonical source: RFC-0006.

## 8. Memory, knowledge and learning terms

### Observation

An **Observation** is an observed operational result, pattern, assertion, signal or fact carried forward for evaluation in the Governed Learning Loop.

Observation is not a Kernel primitive and not validated Knowledge merely because it is repeated, stored or AI-generated.

Canonical source: RFC-0007.

### Organizational Memory

**Organizational Memory** is the structured, versioned body of organizational records, relationships, provenance and evolution retained so experience and context survive transient conversations, people and technologies.

Canonical source: RFC-0007.

### Knowledge Candidate

A **Knowledge Candidate** is a governed proposal that a claim, rule, interpretation, model or reusable understanding should become Knowledge.

Canonical source: RFC-0007.

### Improvement Proposal

An **Improvement Proposal** proposes a change to an approved organizational asset or behavior. Validated Knowledge does not silently change production behavior.

Canonical source: RFC-0007.

### Knowledge

**Knowledge** is validated organizational understanding within a declared scope.

Canonical source: RFC-0007.

### Knowledge lifecycle / applicability state

Knowledge may distinguish `Current`, `Review Required`, `Superseded`, `Retracted` and `Retired` states where relevant. Contradiction does not rewrite history.

Canonical source: RFC-0007.

### Governed Learning Loop

The **Governed Learning Loop** is the controlled path from execution/outcomes through Observation and Memory to candidates/proposals, validation/approval and future governed state.

Canonical sources: RFC-0001 Section 8; RFC-0007.

### Retrieval / RAG / derived projections

Retrieval, RAG, embeddings, vector/lexical indexes, caches, summaries and derived graph projections are execution/retrieval techniques and non-canonical projections by default.

Canonical source: RFC-0007.

## 9. Document and artifact terms

### Document

A **Document** is a logical content-bearing governed subject intended to be communicated, reviewed, relied upon, retained, exchanged, approved, evidenced or reused by people or systems.

A Document is a semantic role above the Kernel; a file is only one possible representation.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 6.1.

### Document Version

A **Document Version** is one immutable governed state of a logical Document.

A significant Document has one stable Subject Identity and immutable Version Identities. Material semantic or governance change creates a new version rather than mutating an admitted version.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 6.2.

### Artifact

An **Artifact** is a concrete content-bearing representation, package or captured result produced, received, transformed, attached, signed, exported or otherwise handled by an execution, product, user or external system.

Artifact is not a Kernel primitive and may remain a Transient Output unless significance, evidence, reuse or explicit asset designation requires governed representation.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 6.3.

### Working Copy / Draft Candidate

A **Working Copy** or **Draft Candidate** is mutable content being edited, collaboratively authored, generated or prepared before admission as an immutable governed Document Version.

It is non-canonical by default. Before consequential reliance on a significant state, an immutable governed checkpoint/version is required.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 6.6.

### Governed Content Resolution

**Governed Content Resolution** is the requirement that a significant Document Version resolve to its governed content through payload, immutable content reference, `External Reference`, or `Governed Replica` semantics.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 6.5.

### Content Manifest

A **Content Manifest** is the governed structure describing materially relevant representations, attachments or package relationships for a Document Version or Package.

It is a logical concept and does not require one physical manifest file or storage schema.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Sections 6.5 and 15.

### Rendition

A **Rendition** is an Artifact representing a Document Version for a declared purpose or format, such as authoring, exchange, signed, archival, redacted or machine-readable representation.

Multiple renditions belong to one Document Version only under explicit governed equivalence semantics appropriate to the reliance.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 8.

### Designated Rendition Role

A **Designated Rendition Role** identifies the representation role relied upon for a declared purpose. It does not create a new Canonical Record authority or source of truth.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 8.3.

### Content Availability State

**Content Availability State** distinguishes materially different conditions such as content being available, lawfully deleted, externally unavailable, or intentionally omitted/not permitted for export or disclosure.

These conditions must not be collapsed into an undifferentiated successful/complete state when the distinction matters.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 8.4.

### Derived Artifact

A **Derived Artifact** results from transformation such as conversion, OCR, extraction, summarization, translation, redaction, rendering, signing, packaging or normalization.

Derived representations preserve material source provenance and inherit applicable Organization, classification, purpose, rights, retention and deletion constraints unless a governed transformation establishes a permitted different rule.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 14.

### Attachment

An **Attachment** is an explicit relationship from a parent Document/Record to content. It is version-aware where the attachment materially affects meaning or evidence.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 15.1.

### Bundle / Package

A **Bundle** or **Package** is a governed collection of Documents/Artifacts assembled for a declared purpose such as submission, export, evidence, transfer or archival.

A significant Package pins materially included versions/artifacts and exposes purpose-scoped completeness and material omissions/unavailability.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Sections 15.2–15.3.

### Signature Evidence

**Signature Evidence** is cryptographic/electronic signature, seal, certificate, signed container or external signing evidence supporting specific integrity, identity-assertion, timing or external-process claims.

Signature evidence does not by itself create Authorization, Organizational Authority or canonical approval state.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 16.

### Exact Document Reliance

**Exact Document Reliance** means consequential execution preserves the exact Document Version Identity materially relied upon and, where representation/bytes matter, the exact Artifact/content reference used.

Mutable URLs, `latest` queries or storage paths do not substitute for exact version attribution.

Canonical source: RFC-0008 `1.0.0`, incorporated proposal Section 17.

## 10. Governance, AI and conformance terms

### Decision Authority

**Decision Authority** is the accountable authority permitted to approve a governed decision within its declared scope.

Until approved delegation exists, residual authority remains with the Owner under Accepted rules. The current Decision Authority Policy remains non-effective while its canonical status is `Proposed`.

Canonical source: RFC-0001 Section 16.

### Architectural Exception

An **Architectural Exception** is an approved scoped deviation from an otherwise applicable architectural requirement. It does not silently rewrite the underlying rule.

Canonical source: RFC-0001 Sections 15–16.

### Operational Readiness

**Operational Readiness** is proportionate evidence and approval required before a Platform Capability becomes `Active` for its declared scope.

Operational readiness is distinct from reference implementation readiness and from RFC acceptance.

Canonical source: RFC-0001 Sections 11.2–11.3; RFC-0008 Section 5.

### Commercial Commitment Integrity

**Commercial Commitment Integrity** means externally relied-upon language remains within approved lifecycle, contract, conformance and operational-readiness state.

Canonical sources: RFC-0001 Section 14; RFC-0004; RFC-0008 Section 5.

### AI Authority

AI is an execution, analysis and proposal mechanism rather than an independent organizational authority source.

AI may assist with documents and artifacts, but cannot silently approve, declassify, grant rights, promote Knowledge, broaden Organization scope or turn generated content into authoritative state.

Canonical sources: Constitution Article XIII; RFC-0003; RFC-0005; RFC-0007; RFC-0008 Sections 3–4.

### Conformance

**Conformance** is assessed against an explicit scope and separates subject lifecycle, operational environment and conformance maturity.

Canonical source: RFC-0001 Section 24.

### Subject Lifecycle

The lifecycle axis may use `Product Experiment`, `Candidate`, `Incubating`, `Active`, `Deprecated`, `Retired` and `Not Applicable`.

Canonical source: RFC-0001 Section 24.

### Operational Environment

Operational environment may include `Local`, `Development`, `Test`, `Pilot` and `Production`. Environment is separate from lifecycle.

Canonical source: RFC-0001 Section 24.

### Conformance Maturity

Conformance maturity may be `Draft`, `Provisional`, `Scoped`, `Scoped with Exceptions` or `Not Conformant`.

Canonical source: RFC-0001 Section 24.

### Provisional

**Provisional** means intentionally not yet stable/final within the relevant artifact or lifecycle context. It has different meanings in Product Contract lifecycle and conformance maturity and must not be conflated.

Canonical sources: RFC-0001; RFC-0004.

## 11. Terms and implementation choices intentionally not finalized here

The semantic architecture through RFC-0008 is Accepted. The following remain deliberately subordinate or deferred rather than silently finalized by this glossary:

- global identifier wire encoding;
- database/storage topology and physical schemas;
- repository/package layout;
- programming language/runtime;
- API/RPC/message protocol;
- authentication provider and concrete authorization engine;
- cryptographic algorithms and key-management technology;
- event broker, event-store and observability backend;
- workflow/orchestration engine;
- Product Contract serialization/registry technology;
- relationship/event/knowledge/document-type catalogs not separately standardized;
- Memory/Knowledge persistence and retrieval technology;
- chunking, embedding, vector/lexical/graph indexing technology;
- LLM/model provider and agent framework;
- DMS, object store, document database or content-addressing technology;
- canonical MIME/file-format catalog;
- OCR, parsing, document-understanding and conversion technology;
- signing provider, certificate authority or jurisdiction-specific signature-validity rules;
- malware scanning/content-disarm technology;
- product-specific schemas, workflows, ontologies, document taxonomies, templates, policies and domain knowledge;
- concrete operational-readiness standards, SLOs, RTO/RPO and support procedures.

These choices belong to the lowest sufficient subordinate artifact when implementation or product evidence makes them necessary.

## 12. Quick source map

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
| Event | RFC-0002 §10; RFC-0006 |
| Execution Context | RFC-0002 §11; RFC-0005 |
| Authority modes | RFC-0001 §7.1; RFC-0002 §12 |
| Governed Organizational Asset / Transient Output | RFC-0002 §13 |
| Product Experiment / Product Contract / Extension | RFC-0004 |
| Platform Capability lifecycle | RFC-0001 §11 |
| Workflow / Governed Execution / Operation | RFC-0005 |
| Provenance / telemetry / replay | RFC-0006 |
| Observation / Memory / Candidate / Knowledge | RFC-0007 |
| Retrieval / RAG / projections | RFC-0007 |
| Document / Document Version / Artifact / Working Copy | RFC-0008 |
| Content Manifest / Rendition / Package / Availability | RFC-0008 |
| Signature evidence / exact document reliance | RFC-0008 |
| Decision Authority / Operational Readiness | RFC-0001 §§11, 16 |
| Commercial Commitment Integrity | RFC-0001 §14; RFC-0004; RFC-0008 §5 |
| AI authority | Constitution XIII; RFC-0003/0005/0007/0008 |
| Conformance | RFC-0001 §§24–25; RFC-0008 incorporated fitness tests |

## 13. Maintenance note

This glossary is a navigation and language artifact, not a substitute for Accepted architecture.

When a later Accepted source refines a term, update this glossary to:

1. preserve the established term where still valid;
2. point to the newer Accepted source;
3. distinguish refinement from supersession;
4. remove stale statements that describe already-Accepted scope as future/deferred;
5. avoid introducing requirements that do not exist in higher-authority sources.
