# Arvectum OS Architecture Glossary

Document status: `Active`
Version: `1.0.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Normative status: `Informative`
Source baseline: Constitution `1.2.0`; RFC-0001 `1.0.0` (`Accepted`)

## 1. Purpose

This glossary provides a shared architectural vocabulary for Arvectum OS.

It summarizes terms already established by the [Constitution](../constitution/CONSTITUTION.md) and [Accepted RFC-0001](../rfc/RFC-0001-arvectum-os-architecture.md) so that contributors, products and AI agents can resolve core meanings without relying on chat history, model memory or implementation conventions.

This document does not create independent architectural requirements. If a glossary definition is incomplete, ambiguous or inconsistent with a higher-authority source, the Constitution and Accepted RFCs prevail.

The precise Kernel metamodel remains provisional until RFC-0002. In particular, this glossary does not decide whether `Event`, `Execution Context` or `Typed Relationship` are Canonical Record subtypes, governed envelopes, independently persisted primitives or another compatible representation.

## 2. Authority and usage

Terms are summarized from the following sources, in descending authority:

1. [The Constitution of Arvectum OS](../constitution/CONSTITUTION.md), version `1.2.0`, `Ratified`;
2. [RFC-0001 — Arvectum OS Architecture](../rfc/RFC-0001-arvectum-os-architecture.md), version `1.0.0`, `Accepted`.

Later Accepted RFCs may refine terms that RFC-0001 explicitly leaves provisional. When that happens, this glossary should be updated to point to the newer accepted definition without silently changing the underlying architecture.

## 3. Core organizational terms

### Organization / Tenant

An **Organization** is the organizational governance, authority, data-isolation and sovereignty scope within which Arvectum OS operates an organization-specific model.

**Tenant** is used by RFC-0001 as the technical scoping term where records, relationships, executions, artifacts and conformance claims are bound to an organization. RFC-0001 does not define Organization and Tenant as separate Kernel primitives.

By default, one organization's data must not alter another organization's canonical model, and cross-organization access is denied unless explicitly authorized by applicable contracts, rights, classification and governance.

Canonical sources: Constitution Articles VII and VIII; RFC-0001 Sections 6.3, 17, 19 and 24.

### Organizational Intelligence

**Organizational Intelligence** is accumulated knowledge, operational experience, standards, workflows, decisions, relationships and institutional memory that strengthen future work.

Arvectum OS preserves and operationalizes the portion that an organization is entitled and chooses to govern through the platform. Processing organizational intelligence does not by itself transfer legal ownership or create rights for cross-organization reuse.

Canonical sources: Constitution Article 0; RFC-0001 Section 6.1.

### Executable Organizational Model

The **Executable Organizational Model** is the durable, governed representation of organizational intelligence through identities, records, relationships, authority, workflows, evidence and operational history.

It includes, among other things, Canonical Records and versions, typed relationships, governed assets, standards and policies, workflows and execution history, decisions and approvals, memory and knowledge, documents and artifacts, events, evidence, provenance, and product or extension contracts.

It is executable because governed workflows can act on the model and produce records, events and artifacts. It is organizational because meaning and authority come from the organization, applicable contracts and governance. It is a model because it represents selected operational reality rather than claiming to be a complete simulation of the organization.

Canonical source: RFC-0001 Sections 1 and 6.2.

### Organization-specific Model Instance / Organizational Twin

An **Organization-specific Model Instance** is the isolated organization-specific instance or view of the Executable Organizational Model.

**Organizational Twin** is an informative descriptive term for that instance. It is not a separate Kernel primitive and does not imply completeness, real-time simulation or autonomous management.

Canonical source: RFC-0001 Section 6.3.

### Organizational Semantics

**Organizational Semantics** are the stable meanings, authority rules and governed operating concepts defined by the organization and preserved across products and technologies.

RFC-0001 summarizes the intended separation as: the organization defines meaning, products specialize meaning, and technologies execute meaning.

Canonical source: RFC-0001 Section 6.4.

### Architectural Responsibility

**Architectural Responsibility** is responsibility within Arvectum OS for canonical state, lifecycle, contracts, validation, change control and operational support.

It is distinct from legal title, intellectual-property ownership, licensing rights, confidentiality obligations, contractual data rights and legal controller/processor roles.

Canonical source: RFC-0001 Section 6.5.

## 4. Kernel and canonical-state terms

### Kernel / Platform Kernel

The **Kernel** is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

RFC-0001 defines five Kernel primitives:

1. Identity;
2. Canonical Record;
3. Typed Relationship;
4. Event;
5. Execution Context.

The precise metamodel relationships among these primitives are provisional until RFC-0002.

Canonical source: RFC-0001 Sections 1 and 10.

### Identity

**Identity** is a stable reference to organizations, actors, products, governed objects, executions, events and extensions.

RFC-0001 establishes Identity semantics as a Kernel primitive but reserves the precise identity and version metamodel for RFC-0002.

Canonical source: RFC-0001 Section 10.2 and provisional constraints in Section 10.3.

### Canonical Record

A **Canonical Record** is the governed representation of an object or immutable observation at a specific version, including its authority mode and authoritative source.

Every significant governed object managed by Arvectum OS has one Canonical Record within its declared scope and type. A Canonical Record is authoritative for how Arvectum OS identifies, scopes, governs and references the object; it does not necessarily make Arvectum OS the originating system of record for every underlying fact.

Every Canonical Record has an immutable version identity. Changeable native or replicated objects use a stable object identity plus a sequence of immutable versions.

Canonical source: RFC-0001 Sections 7.1 and 10.2.

### Significant Governed Object

A **Significant Governed Object** is an object whose state or meaning materially affects organizational meaning, authority, production behavior, external commitments, financial or legal position, security, safety, reputation, canonical state, a reusable asset, or reconstruction of a consequential result.

Significance determines when the Canonical Record rule applies at full strength.

Canonical source: RFC-0001 Section 7.1.

### Canonical State

**Canonical State** is the authoritative governed state managed by Arvectum OS within a declared scope.

Consequential changes to canonical state occur through Governed Execution. Canonical state must not be confused with caches, projections, indexes, transient outputs or duplicated external facts that remain authoritative elsewhere.

Canonical sources: Constitution Article IV; RFC-0001 Sections 7.1 and 7.5.

### Authoritative Source

An **Authoritative Source** is the source designated as authoritative for a governed object or fact within a declared scope.

The authoritative source may be Arvectum OS or an external system. Arvectum OS must not create a competing authoritative source where an external system remains authoritative.

Canonical sources: Constitution Article IV; RFC-0001 Section 7.1.

### Authority Mode

An **Authority Mode** declares the relationship between a Canonical Record and the authoritative source for the governed object.

RFC-0001 defines exactly three modes:

- `Native` — Arvectum OS is the authoritative source for the governed object;
- `External Reference` — an external system remains authoritative and Arvectum OS stores a governed identity, reference and access or retrieval contract;
- `Governed Replica` — an external system remains authoritative while Arvectum OS stores a synchronized governed representation under an explicit synchronization contract.

Canonical source: RFC-0001 Section 7.1.

### Governed Organizational Asset

A **Governed Organizational Asset** is a record or artifact explicitly designated as authoritative, reusable, evidentiary or operationally significant.

Such assets are discoverable, attributable and versioned at a level proportionate to their importance, and they may be reused only under applicable permissions, classifications, rights and policies.

A record or artifact does not become a Governed Organizational Asset merely because Arvectum OS generated, stored or processed it.

Canonical sources: Constitution Article XVI; RFC-0001 Section 7.2.

### Transient Output

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

Transient and experimental outputs may use lighter versioning, observability and retention when their status, scope, owner, risk, retention and promotion or deletion path are explicit. They do not automatically become validated knowledge, organizational memory or permanent organizational assets.

Canonical sources: Constitution Articles XV and XVI; RFC-0001 Section 7.3.

### Typed Relationship

A **Typed Relationship** is a governed connection between identities or record versions with explicit semantics and provenance.

Operationally relevant relationships are explicit, directionally meaningful, attributable and traceable, and version-aware where required. The relationship graph supports context resolution, explainability, impact analysis, governance, search, dependency resolution and reconstruction; it does not require a graph database.

Whether Typed Relationship has independent identity and versioning is provisional until RFC-0002.

Canonical source: RFC-0001 Sections 7.4, 10.2 and 10.3.

### Event

An **Event** is an append-only observation that something meaningful occurred.

Events form part of operational history. Corrections, reversals and compensations create additional linked objects rather than mutating history.

Whether Event is a Canonical Record subtype or is represented by one is provisional until RFC-0002.

Canonical sources: Constitution Article XI; RFC-0001 Sections 7.1, 10.2 and 10.3.

### Execution Context

An **Execution Context** is the governed execution envelope binding an operation to its organization, actor, authority, product, workflow, inputs, controls, components and outputs.

For consequential operations it provides the context needed to identify relevant versions, sources, standards and policies, validation and approvals, emitted events, correlation and causation, classification, retention and reproducibility constraints.

Whether Execution Context is a Canonical Record subtype, a governed envelope or a related record set is provisional until RFC-0002.

Canonical source: RFC-0001 Sections 7.5, 10.2 and 10.3.

### Governed Execution

**Governed Execution** is an authorized operation performed through an explicit Execution Context when consequential canonical state is read or changed in a way covered by RFC-0001.

Governed Execution binds technical execution to organizational authority, declared inputs, applicable rules, validation and approvals, resulting outputs and events, and sufficient evidence for reconstruction and explainability.

Technical ability to perform an action does not itself grant organizational authority to an AI system, product or service.

Canonical source: RFC-0001 Section 7.5.

### Provenance

**Provenance** is the traceable origin and lineage information that allows governed records, relationships, events, artifacts and executions to be attributed to their relevant sources, actors, versions and transformations.

RFC-0001 requires provenance throughout Canonical Records, Typed Relationships, Governed Execution, learning and governed export, but leaves the detailed Event, Provenance and Observability model to a later RFC.

Canonical sources: Constitution Articles V, XII and XVI; RFC-0001 Sections 7, 8, 18 and 29.

### Observation

An **Observation** is evidence or an observed result produced through operational activity that may feed the governed learning loop.

An observation is not automatically validated knowledge. Promotion requires applicable provenance, rights, classification, validation and approval.

Canonical sources: Constitution Article XXI; RFC-0001 Section 8.

## 5. Product and platform terms

### Product

A **Product** is an extension and client of Arvectum OS that owns domain meaning and product-specific behavior while consuming shared platform foundations through explicit contracts where platform interaction exists.

Products are architecturally responsible for domain concepts, schemas, knowledge, workflows, validators, standards, risk rules, templates, agents, integrations, user experience, commercial packaging and Product Experiments before platform promotion.

Canonical sources: Constitution Articles II, III and XX; RFC-0001 Sections 9 and 12.

### Product Experiment

A **Product Experiment** is a bounded and reversible implementation under the architectural responsibility of a product or operational sponsor while uncertainty is high.

It may contain domain-specific logic and use proportionately lighter documentation and versioning, but it is not a shared platform guarantee and does not bypass applicable security, privacy, legal, contractual, data-integrity or governance controls.

A fully product-local experiment that does not consume platform capabilities, emit events into shared platform history, or read or change canonical platform state may operate without a Product Contract. Once it interacts with those platform responsibilities, it uses a minimal `Provisional` Product Contract proportionate to the interaction.

Canonical sources: Constitution Articles II, XVII and XVIII; RFC-0001 Section 11.1.

### Product Contract

A **Product Contract** is the versioned boundary between a product and Arvectum OS.

It declares the relevant product identity and ownership, capability dependencies, record and relationship types, authority modes, schemas and workflows, event and artifact types, permissions and classifications, approval requirements, extensions and adapters, portability, retention, deletion, migration and support status as applicable to the interaction.

Products and experiments do not access platform internals through undocumented conventions, direct database coupling or internal imports that bypass declared contracts.

Canonical source: RFC-0001 Section 13.

### Provisional Product Contract

A **Provisional Product Contract** is a Product Contract used for bounded product/platform interaction before the dependency or contract has matured into a stable supported boundary.

It is intentionally proportionate to the experiment or interaction and must not be represented as a stable platform guarantee merely because it exists.

Canonical sources: RFC-0001 Sections 9, 11.1 and 13.

### Platform Capability

A **Platform Capability** is a reusable, domain-neutral organizational ability exposed by Arvectum OS to products or other capabilities.

Platform Capability is a responsibility and contract concept, not merely a piece of code. Capability maturity is expressed through the lifecycle `Candidate → Incubating → Active → Deprecated → Retired`.

Canonical source: RFC-0001 Sections 11.2–11.4.

### Candidate

A **Candidate** is a proposed Platform Capability whose organizational outcome, owner, sponsor or constitutional rationale, domain-neutral boundary, expected consumers or strategic need, reuse hypothesis, review date and disposition criteria are declared.

Candidate status does not imply an implementation commitment or a supported platform contract.

Canonical source: RFC-0001 Section 11.2.

### Incubating

An **Incubating** capability is a Platform Capability under bounded platform incubation with a `Provisional` domain-neutral contract and declared source need, consumers, scope, Canonical Record responsibilities, dependencies, events, security and data rules, migration requirements and exit criteria.

Incubating does not mean `Active` or externally supported as a stable capability.

Canonical source: RFC-0001 Section 11.2.

### Active

An **Active** capability is a Platform Capability that has passed applicable admission requirements and has a supported stable public contract, declared compatibility and migration policy, accountable operational support, approved operational readiness, appropriate evidence, and maintained security, portability and lifecycle obligations.

`Active` is a capability lifecycle state. It must not be confused with an operational environment such as `Production`.

Canonical source: RFC-0001 Sections 11.2–11.4 and 24.

### Deprecated

A **Deprecated** capability is a previously supported capability that remains in the lifecycle while consumers move away from it under declared migration and deprecation responsibilities.

RFC-0001 requires preservation of required history, contractual obligations, exportability and migration paths during capability exit.

Canonical source: RFC-0001 Section 11.4.

### Retired

A **Retired** capability is a capability whose platform responsibility has ended after the applicable exit, preservation and migration obligations have been addressed.

Canonical source: RFC-0001 Section 11.4.

### Platform Service

A **Platform Service** is an implementation and architectural-responsibility boundary that realizes one or more Platform Capabilities.

A Platform Service is not necessarily a separate process, network service, repository or deployment. Service boundaries therefore must not be inferred directly from deployment topology.

Canonical source: RFC-0001 Section 11.5.

### Extension

An **Extension** is a registered and versioned product, agent, workflow, schema, validator, template, policy, connector, tool, adapter or UI module that extends Arvectum OS through declared contracts and bounded permissions.

Extensions do not weaken Kernel, security, sovereignty or governance invariants.

Canonical source: RFC-0001 Section 20.

### Platform Gravity

**Platform Gravity** is the informative concept that the platform should become easier to reuse than to replace because it creates real value rather than coercive dependency.

Weak Platform Gravity is indicated by repeated contract bypass, slower integration than local implementation, persistent single-product abstractions, platform bottlenecks or duplicate shared foundations.

This term is informative and does not define a conformance requirement by itself.

Canonical source: RFC-0001 Section 22.

## 6. Workflow, memory and knowledge terms

### Workflow

A **Workflow** is the versioned representation of how repeatable and operationally significant work is performed.

Its business meaning, governance and durable state are not inseparably bound to a specific AI model, vendor or runtime. The rigor of workflow formalization is proportionate to risk, frequency and organizational importance.

Canonical source: Constitution Article X.

### Memory / Organizational Memory

**Memory** is not conversation history.

Organizational Memory consists of structured, versioned organizational records together with their relationships, provenance and evolution over time. In the governed learning loop, memory may accumulate observations, but it does not automatically turn them into validated knowledge.

Canonical sources: Constitution Article V; RFC-0001 Section 8.

### Knowledge

**Knowledge** is validated organizational understanding.

It is versioned, reusable, explainable and independent of implementation technologies. Observations, transient outputs and AI-generated material do not become validated knowledge merely by being produced; promotion is governed.

Canonical sources: Constitution Article VI; RFC-0001 Sections 8 and 21.

### Governed Learning Loop

The **Governed Learning Loop** is the controlled path by which operational evidence can contribute to future approved organizational behavior without silent production mutation.

RFC-0001 describes the sequence as Governed Execution → Events and Outcomes → Observations → Organizational Memory → Knowledge or Improvement Proposal → Validation, Rights Review and Approval → Approved Knowledge / Standard / Policy / Workflow Version → Future Governed Execution.

Learning mechanisms may propose changes but do not silently activate them.

Canonical source: RFC-0001 Section 8.

## 7. Governance and authority terms

### Decision Authority

**Decision Authority** is the accountable authority permitted to approve a governed decision within its declared scope.

A governed decision identifies its subject and scope, proposer, decision authority, rationale and evidence, effective date, review/expiry/supersession condition where applicable, and canonical decision reference.

Until authority is explicitly delegated under an approved policy, the owner of Arvectum OS retains residual decision authority.

Canonical source: RFC-0001 Section 16.

### Architectural Exception

An **Architectural Exception** is an approved, scoped deviation from an otherwise applicable architectural requirement.

Exceptions record scope, proposer, decision authority, rationale, review or expiry date and exit plan. An exception does not silently rewrite the underlying architectural rule.

Canonical sources: RFC-0001 Sections 2.1, 15 and 16.

### Operational Readiness

**Operational Readiness** is the evidence and approval, proportionate to scope, consequence and customer commitments, required before a Platform Capability becomes `Active`.

It may include support responsibility, observability and health evidence, incident and recovery paths, continuity assumptions, backup or reconstruction paths, migration and deprecation responsibilities, and customer-facing operational commitments relevant to the capability.

Canonical source: RFC-0001 Sections 11.2 and 11.3.

## 8. Conformance terms

### Conformance

**Conformance** is assessed against a declared scope rather than against every possible future capability of Arvectum OS.

A conformance claim separates three different axes:

1. subject lifecycle;
2. operational environment;
3. conformance maturity.

A limited pilot, experiment or capability must not be described as fully platform-conformant merely because its bounded scope satisfies applicable requirements.

Canonical source: RFC-0001 Section 24.

### Conformance Statement

A **Conformance Statement** is the scoped record of a conformance assessment for an implementation, pilot, deployment or capability claiming Arvectum OS conformance.

It identifies the subject and version, organization/tenant and deployment scope, workflows and capabilities in scope, relevant data and risk, authority modes and external systems, applicable normative sections, exclusions and rationale, manual or provisional controls, exceptions, known gaps, assessment and approval responsibility, operational-readiness evidence where relevant, external commitments, and reassessment conditions.

Canonical source: RFC-0001 Section 24.

### Subject Lifecycle

**Subject Lifecycle** is the lifecycle axis used in a Conformance Statement.

RFC-0001 permits:

- `Product Experiment`;
- `Candidate`;
- `Incubating`;
- `Active`;
- `Deprecated`;
- `Retired`;
- `Not Applicable` when the assessed subject is not a capability or experiment.

Canonical source: RFC-0001 Section 24.

### Operational Environment

**Operational Environment** is the deployment/use-context axis used in a Conformance Statement.

RFC-0001 permits one or more of:

- `Local`;
- `Development`;
- `Test`;
- `Pilot`;
- `Production`.

Operational environment is separate from capability lifecycle. In particular, `Production` does not mean `Active`.

Canonical source: RFC-0001 Section 24.

### Conformance Maturity

**Conformance Maturity** is the assessment-maturity axis used in a Conformance Statement.

RFC-0001 defines:

- `Draft` — assessment incomplete;
- `Provisional` — applicable invariants are addressed through bounded, manual or provisional controls;
- `Scoped` — assessed and conformant within the declared scope;
- `Scoped with Exceptions` — conformant within scope subject to approved exceptions;
- `Not Conformant`.

Canonical source: RFC-0001 Section 24.

### Provisional

**Provisional** is a qualifier indicating that a definition, implementation, contract or conformance control is intentionally not yet final or stable within its relevant context.

In RFC-0001 it is used in several distinct but related contexts, including the unresolved Kernel metamodel, Provisional Product Contracts, provisional capability contracts during incubation, and `Provisional` conformance maturity. The exact meaning must therefore be read from the lifecycle or artifact being qualified rather than treated as a single global status.

Canonical sources: RFC-0001 Sections 10.3, 11, 13 and 24.

## 9. Normative language

RFC-0001 uses capitalized normative keywords as follows:

- **MUST / MUST NOT** — mandatory for conformance unless an approved architectural exception explicitly applies;
- **SHOULD / SHOULD NOT** — default expectation; deviation requires recorded rationale proportionate to impact;
- **MAY** — permitted but not required.

Lower-case uses in explanatory prose do not create additional normative force.

Canonical source: RFC-0001 Section 2.1.

## 10. Terms intentionally not finalized here

The following areas are deliberately not finalized by this glossary because RFC-0001 reserves them for later Accepted RFCs:

- exact identity and version semantics for every Kernel primitive;
- whether Event is a Canonical Record subtype or is represented by one;
- whether Execution Context is a Canonical Record subtype, governed envelope or related record set;
- whether Typed Relationship has independent identity and versioning;
- preservation and lifecycle requirements for completed Execution Contexts;
- detailed identity, security, privacy and tenant-sovereignty mechanisms;
- detailed Product Contract and extension model beyond RFC-0001;
- detailed Governed Execution and Workflow model;
- detailed Event, Provenance and Observability model;
- detailed Memory, Knowledge and Governed Learning lifecycle.

These areas remain subject to the follow-up RFC sequence established by RFC-0001 and coordinated by the [Canonical Roadmap](../roadmap/ROADMAP.md).

## 11. Quick source map

| Term family | Primary canonical source |
|---|---|
| Organizational Intelligence | Constitution Article 0; RFC-0001 §6.1 |
| Executable Organizational Model | RFC-0001 §6.2 |
| Canonical Record and Authority Modes | RFC-0001 §7.1 |
| Governed Organizational Asset | Constitution Article XVI; RFC-0001 §7.2 |
| Transient Output | RFC-0001 §7.3 |
| Typed Relationship | RFC-0001 §§7.4, 10.2 |
| Governed Execution / Execution Context | RFC-0001 §§7.5, 10.2 |
| Kernel primitives | RFC-0001 §10 |
| Product Experiment | RFC-0001 §11.1 |
| Platform Capability lifecycle | RFC-0001 §§11.2–11.4 |
| Platform Service | RFC-0001 §11.5 |
| Product boundary | Constitution Articles II, III, XX; RFC-0001 §12 |
| Product Contract | RFC-0001 §13 |
| Decision Authority / Exceptions | RFC-0001 §16 |
| Security / Privacy / Isolation | Constitution Article VIII; RFC-0001 §17 |
| Sovereignty / cross-organization rules | RFC-0001 §19 |
| Extensions | RFC-0001 §20 |
| AI authority | Constitution Article XIII; RFC-0001 §21 |
| Workflow | Constitution Article X |
| Memory | Constitution Article V; RFC-0001 §8 |
| Knowledge | Constitution Article VI; RFC-0001 §8 |
| Conformance | RFC-0001 §§24–25 |

## 12. Maintenance note

This glossary is a navigation and language artifact, not a substitute for Accepted architecture.

When a later Accepted RFC refines a term that is provisional here, the glossary should be updated to:

1. preserve the established term where still valid;
2. point to the new accepted source;
3. distinguish refinements from superseded meanings;
4. avoid introducing requirements that do not exist in the higher-authority source.
