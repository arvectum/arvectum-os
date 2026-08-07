# Arvectum OS Architecture Glossary

Document status: `Active`
Version: `1.1.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Normative status: `Informative`
Source baseline: Constitution `1.2.0`; RFC-0001 `1.0.0` (`Accepted`); RFC-0002 `1.0.0` (`Accepted`)

## 1. Purpose

This glossary provides a shared architectural vocabulary for Arvectum OS.

It summarizes terms already established by the [Constitution](../constitution/CONSTITUTION.md), [Accepted RFC-0001](../rfc/RFC-0001-arvectum-os-architecture.md) and [Accepted RFC-0002](../rfc/RFC-0002-canonical-record-kernel-metamodel.md) so that contributors, products and AI agents can resolve core meanings without relying on chat history, model memory or implementation conventions.

This document does not create independent architectural requirements. If a glossary definition is incomplete, ambiguous or inconsistent with a higher-authority source, the Constitution and Accepted RFCs prevail.

RFC-0002 `1.0.0` finalizes the Kernel metamodel relationships that RFC-0001 left provisional. Identity remains a stable non-record reference primitive; Canonical Record is the immutable governed representation at one version; Typed Relationship, Event and Execution Context are semantic specializations of Canonical Record.

## 2. Authority and usage

Terms are summarized from the following sources, in descending authority:

1. [The Constitution of Arvectum OS](../constitution/CONSTITUTION.md), version `1.2.0`, `Ratified`;
2. [RFC-0001 — Arvectum OS Architecture](../rfc/RFC-0001-arvectum-os-architecture.md), version `1.0.0`, `Accepted`;
3. [RFC-0002 — Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model](../rfc/RFC-0002-canonical-record-kernel-metamodel.md), version `1.0.0`, `Accepted`.

Draft, Proposed and other non-Accepted documents may be useful for design discussion but do not change the meanings recorded here.

Later Accepted RFCs may refine terms further. When that happens, this glossary should be updated to point to the newer accepted definition without silently changing the underlying architecture.

## 3. Core organizational terms

### Organization / Tenant

An **Organization** is the organizational governance, authority, data-isolation and sovereignty scope within which Arvectum OS operates an organization-specific model.

**Tenant** is used by RFC-0001 as a technical scoping term for records, relationships, executions, artifacts, access boundaries and conformance claims associated with an organization.

RFC-0001 does not finalize whether Organization and Tenant are one-to-one, how tenancy is represented, or whether either is modeled as a distinct governed object. That mapping remains subject to a later Accepted identity, security, privacy and sovereignty RFC.

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

RFC-0002 requires significant Canonical Records to expose an accountable architectural owner, directly or through governed reference.

Canonical sources: RFC-0001 Section 6.5; RFC-0002 Section 8.1.

### Organizational Control and Portability

**Organizational Control and Portability** describe the requirement that an organization retain governance and control over its data, organizational intelligence, standards, decisions and operational history, subject to applicable law and contract, and that Arvectum OS support governed export, migration, deletion, service termination and handover within the applicable scope.

Portability protects continuity of organizational meaning and governed history; it does not imply that every item may be exported, retained or transferred regardless of legal, contractual, privacy or classification restrictions.

Canonical sources: Constitution Article VII; RFC-0001 Sections 18 and 19.

### Proportionality

**Proportionality** is the principle that governance, standardization, validation, observability, security controls and architectural rigor should match the risk, maturity, consequence and expected organizational value of the work.

Proportionality permits bounded manual or provisional controls where appropriate. It does not waive mandatory constitutional, security, legal, contractual or Accepted RFC requirements.

RFC-0002 applies this principle to the Kernel metamodel by permitting governed references instead of unnecessary physical duplication and by rejecting automatic wholesale migration of legacy product-local data.

Canonical sources: Constitution Articles VIII, XIII and XVII; RFC-0001 Sections 7.3, 11, 17, 23 and 24; RFC-0002 Sections 8.8 and 17.8.

## 4. Kernel and canonical-state terms

### Kernel / Platform Kernel

The **Kernel** is the smallest stable semantic foundation required for products and platform capabilities to interoperate consistently.

RFC-0001 defines five Kernel primitives:

1. Identity;
2. Canonical Record;
3. Typed Relationship;
4. Event;
5. Execution Context.

RFC-0002 `1.0.0` finalizes their metamodel relationships. Identity is the stable non-versioned reference primitive and is not a Canonical Record. Canonical Record is the immutable governed representation of one logical subject at one specific version. Typed Relationship, Event and Execution Context are semantic specializations of Canonical Record.

Canonical sources: RFC-0001 Sections 1 and 10; RFC-0002 Section 6.

### Identity

**Identity** is an opaque stable reference to one semantic referent within a declared identity namespace and organization or platform scope.

RFC-0002 distinguishes two roles:

- **Subject Identity** identifies one logical governed subject across time;
- **Version Identity** identifies exactly one immutable Canonical Record version.

Identity is immutable after issuance, non-recycled and independent of mutable business meaning. Possession or resolvability of an Identity does not itself grant permission, delegated authority or access.

Canonical source: RFC-0002 Section 7.

### Canonical Record

A **Canonical Record** is the immutable governed representation of one logical subject at one specific version.

A changeable governed subject has one stable Subject Identity and an unambiguous canonical lineage of immutable versions, each with its own Version Identity. The **Canonical Head** is the latest admitted version in that lineage; it is distinct from the **Effective Version**, which is the version applicable for a declared evaluation context.

Canonical Record semantics include authority, accountable architectural ownership, provenance, organization or tenant scope, classification/access constraints and applicable retention/deletion references. The common envelope is semantic and does not require one physical table or duplicated payload.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Sections 8 and 16.

### Significant Governed Object

A **Significant Governed Object** is an object whose state or meaning materially affects organizational meaning, authority, production behavior, external commitments, financial or legal position, security, safety, reputation, canonical state, a reusable asset, or reconstruction of a consequential result.

The Canonical Record requirement applies to every significant governed object managed by Arvectum OS within its declared scope and type. RFC-0002 does not broaden that significance threshold: non-significant technical state and explicit transient outputs do not become Canonical Records merely because they are stored or convenient to persist.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 8.8.

### Canonical State

**Canonical State** is the authoritative governed state managed by Arvectum OS within a declared scope.

Consequential changes to canonical state managed by Arvectum OS occur through Governed Execution. Canonical state must not be confused with caches, projections, indexes, transient outputs or underlying external facts that remain authoritative in another system.

Canonical sources: Constitution Article IV; RFC-0001 Sections 7.1 and 7.5.

### Canonical Lineage

A **Canonical Lineage** is the one unambiguous sequence of immutable Canonical Record versions for a changeable governed subject within one declared authority scope.

Competing draft, simulated or branch representations may exist outside the canonical lineage, but they do not silently create parallel canonical heads.

Canonical source: RFC-0002 Section 8.3.

### Canonical Head

The **Canonical Head** is the latest admitted version in a Canonical Lineage for a governed subject within one declared authority scope.

It is a lineage concept and is not necessarily the version effective at a particular evaluation time.

Canonical source: RFC-0002 Section 8.4.

### Effective Version

The **Effective Version** is the canonical version applicable for a declared evaluation context, such as effective time, authority scope or another version-resolution condition.

A future-effective Canonical Head may therefore coexist with an earlier version that remains currently effective.

Canonical source: RFC-0002 Section 8.5.

### Authoritative Source

An **Authoritative Source** is the source designated as authoritative for a governed object or fact within a declared scope.

The authoritative source may be Arvectum OS or an external system. Arvectum OS must not create a competing authoritative source where an external system remains authoritative.

Canonical sources: Constitution Article IV; RFC-0001 Section 7.1; RFC-0002 Section 12.

### Authority Mode

An **Authority Mode** declares the relationship between a Canonical Record and the authoritative source for the governed object.

Exactly three modes exist:

- `Native` — Arvectum OS is the authoritative source for the governed object;
- `External Reference` — an external system remains authoritative and Arvectum OS stores a governed identity, reference and access or retrieval contract;
- `Governed Replica` — an external system remains authoritative while Arvectum OS stores a synchronized governed representation under an explicit synchronization contract.

For external modes, RFC-0002 requires enough explicit retrieval/synchronization, freshness, ordering, conflict, failure, transformation, retention, deletion and portability semantics to avoid competing authority and ambiguous cutover behavior.

Canonical sources: RFC-0001 Section 7.1; RFC-0002 Section 12.

### Governed Organizational Asset

A **Governed Organizational Asset** is an explicit governed designation applied to a Canonical Record, record lineage, represented artifact or another governed subject that the organization designates as authoritative, reusable, evidentiary or operationally significant.

It is not a sixth Kernel primitive. The designation itself is governed, attributable, version-identifiable and reconstructable. Asset status does not create legal title, intellectual-property ownership, licensing rights or cross-organization reuse rights.

Persistence alone does not imply asset status.

Canonical sources: Constitution Article XVI; RFC-0001 Section 7.2; RFC-0002 Section 13.

### Transient Output

A **Transient Output** is a temporary result that has not been promoted into authoritative state or a Governed Organizational Asset.

Transient and experimental outputs may use lighter versioning, observability and retention when their status, scope, owner, risk, retention and promotion or deletion path are explicit. They do not automatically become validated knowledge, organizational memory or permanent organizational assets.

Canonical sources: Constitution Articles XV and XVI; RFC-0001 Section 7.3; RFC-0002 Section 13.4.

### Typed Relationship

A **Typed Relationship** is a Canonical Record specialization representing one governed semantic relationship assertion instance from a source reference to a target reference.

It has its own stable Relationship Identity and immutable versions. Endpoints explicitly distinguish Subject Identity references from Version Identity references. Relationship Identity represents an assertion instance and is not derived solely from the source/type/target tuple.

A Typed Relationship expresses governed semantics; its existence or resolvability does not itself grant access, delegated authority, approval power or cross-organization visibility.

Canonical source: RFC-0002 Section 9.

### Event

An **Event** is a Canonical Record specialization representing an append-only observation that something meaningful occurred.

An Event has one stable Event Identity and normally exactly one immutable canonical version. Corrections, reversals, compensations and invalidations create additional linked Events rather than mutating prior history.

Canonical sources: Constitution Article XI; RFC-0001 Sections 7.1 and 10.2; RFC-0002 Section 10.

### Execution Context

An **Execution Context** is a Canonical Record specialization representing one governed execution instance.

One governed execution has one stable Execution Identity and immutable versions for governance-significant state transitions. For Arvectum OS Governed Execution, the Execution Context uses `Native` authority mode for its governance envelope even when external systems remain authoritative for underlying inputs.

Consequential reliance on changeable governed inputs pins the exact Version Identities materially used. Terminal execution state is sealed; required history is preserved subject to applicable retention, deletion, privacy, legal and contractual constraints.

Canonical sources: RFC-0001 Section 7.5; RFC-0002 Section 11.

### Governed Execution

**Governed Execution** is an authorized operation carried out through an explicit Execution Context for consequential changes to canonical state managed by Arvectum OS.

It binds technical execution to organizational authority, declared inputs, applicable rules, validation and approvals, resulting outputs and events, and sufficient context for reconstruction and explainability where applicable.

RFC-0001 may require governed context for other consequential behavior through additional controls, but this glossary does not extend Law Three beyond its Accepted requirement for consequential canonical-state change.

Technical ability to perform an action does not itself grant organizational authority to an AI system, product or service.

Canonical sources: RFC-0001 Section 7.5; RFC-0002 Section 11.

### Provenance

**Provenance** is traceable origin and lineage information that allows governed records, relationships, events, artifacts and executions to be attributed to relevant sources, actors, versions and transformations.

RFC-0001 requires provenance throughout Canonical Records, Typed Relationships, Governed Execution, learning and governed export. RFC-0002 requires provenance within the Kernel metamodel but leaves detailed Event, Provenance and Observability mechanics to RFC-0006.

Canonical sources: Constitution Articles V, XII and XVI; RFC-0001 Sections 7, 8, 18 and 29; RFC-0002 Sections 8–12.

### Observation

**Observation** is a term used by the governed learning loop for an observed operational result, pattern or fact carried forward for evaluation.

Observation is not a separate Kernel primitive under RFC-0002. An observation is not automatically validated knowledge; promotion requires applicable provenance, rights, classification, validation and approval.

Canonical sources: Constitution Article XXI; RFC-0001 Section 8; RFC-0002 Section 6.

## 5. Product and platform terms

### Product

A **Product** is an extension and client of Arvectum OS that is architecturally responsible for domain meaning and product-specific behavior while consuming shared platform foundations through explicit contracts where platform interaction exists.

Products are architecturally responsible for domain concepts, schemas, knowledge, workflows, validators, standards, risk rules, templates, agents, integrations, user experience, commercial packaging and Product Experiments before platform promotion.

This architectural responsibility does not determine legal ownership or contractual rights.

Canonical sources: Constitution Articles II, III and XX; RFC-0001 Sections 6.5, 9 and 12.

### Product Experiment

A **Product Experiment** is a bounded and reversible implementation under the architectural responsibility of a product or operational sponsor while uncertainty is high.

It may contain domain-specific logic and use proportionately lighter documentation and versioning, but it is not a shared platform guarantee and does not bypass applicable security, privacy, legal, contractual, data-integrity or governance controls.

RFC-0001 requires a Product Experiment to have an owner, scope, effort or budget bound, review date and explicit path to promotion, containment or retirement.

A fully product-local experiment that does not consume platform capabilities, emit events into shared platform history, or read or change canonical platform state may operate without a Product Contract. Once it interacts with those platform responsibilities, it uses a minimal `Provisional` Product Contract proportionate to the interaction.

RFC-0002 does not require Kernel conformance merely because a fully product-local reversible experiment exists. Success also does not automatically promote an experiment into a Platform Capability; promotion is a separate governed decision.

Canonical sources: Constitution Articles II, XVII and XVIII; RFC-0001 Section 11.1; RFC-0002 Sections 17.8 and 18.

### Product Contract

A **Product Contract** is the versioned boundary between a product and Arvectum OS.

It declares, where applicable, the product or experiment identity, version and architectural owner; capability dependencies; record and relationship types; authority modes and authoritative systems; schemas and workflows; validators, standards and policies; event and artifact types; permissions, classifications and authority requirements; approval gates; extensions and adapters; portability and export obligations; retention and deletion responsibilities; migration and support status; and provisional or incubating dependencies.

Products and experiments do not access platform internals through undocumented conventions, direct database coupling or internal imports that bypass declared contracts.

A Product Contract defines architectural responsibility and interaction boundaries; it does not by itself determine legal title, IP ownership, licensing rights or contractual data rights.

Canonical sources: RFC-0001 Sections 6.5 and 13.

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

RFC-0002 conformance alone does not make a capability `Active` and does not establish production readiness, an SLA or a support guarantee.

Canonical sources: RFC-0001 Sections 11.2–11.4 and 24; RFC-0002 Section 18.2.

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

### Platform Evidence

**Platform Evidence** is the informative body of measurable evidence used to evaluate whether platform responsibility creates organizational value rather than merely relocating complexity.

RFC-0001 suggests evidence across delivery speed, validated reuse, operating cost, reliability, quality, risk reduction, governance, security, portability, integration effort and de-platformization effort.

Platform Evidence informs investment, promotion, redesign and de-platformization decisions but is not itself a fixed universal metric set.

Canonical source: RFC-0001 Section 26.

## 6. Workflow, memory and knowledge terms

### Workflow

A **Workflow** is the versioned representation of how repeatable and operationally significant work is performed.

Its business meaning, governance and durable state are not inseparably bound to a specific AI model, vendor or runtime. The rigor of workflow formalization is proportionate to risk, frequency and organizational importance.

Canonical source: Constitution Article X.

### Memory / Organizational Memory

**Memory** is not conversation history.

Organizational Memory consists of structured, versioned organizational records together with their relationships, provenance and evolution over time. In the governed learning loop, observations may contribute to organizational memory, but memory does not automatically turn them into validated knowledge.

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

## 7. Governance, security and commercial terms

### Decision Authority

**Decision Authority** is the accountable authority permitted to approve a governed decision within its declared scope.

A governed decision identifies its subject and scope, proposer, decision authority, rationale and evidence, effective date, review/expiry/supersession condition where applicable, and canonical decision reference.

The owner of Arvectum OS retains residual decision authority until authority is explicitly delegated. Before the first `Active` capability or external production conformance claim, a separate approved governance policy must define the current authority matrix, delegation limits, escalation paths and substitute approvers.

Canonical source: RFC-0001 Section 16.

### Architectural Exception

An **Architectural Exception** is an approved, scoped deviation from an otherwise applicable architectural requirement.

Exceptions record scope, proposer, decision authority, rationale, review or expiry date and exit plan. An exception does not silently rewrite the underlying architectural rule.

Canonical sources: RFC-0001 Sections 2.1, 15 and 16.

### Operational Readiness

**Operational Readiness** is the evidence and approval, proportionate to scope, consequence and customer commitments, required before a Platform Capability becomes `Active`.

It may include support responsibility, observability and health evidence, incident and recovery paths, continuity assumptions, backup or reconstruction paths, migration and deprecation responsibilities, and customer-facing operational commitments relevant to the capability.

Canonical source: RFC-0001 Sections 11.2 and 11.3.

### Commercial Commitment Integrity

**Commercial Commitment Integrity** is the rule that externally relied-upon commercial language and commitments must stay within the approved architectural, lifecycle, contract, conformance and operational-readiness state of Arvectum OS.

A Product Experiment, `Candidate` or `Incubating` capability must not be represented as an `Active` supported platform capability, and a commercial commitment must not create an unapproved stable platform obligation, compatibility promise, portability promise, support guarantee or broader conformance claim.

Bounded pilots and Product Experiments may be described commercially when their lifecycle, limitations, support expectations and provisional or non-production status are represented accurately.

RFC-0002 conformance is only a scoped metamodel claim and does not itself establish production readiness or an external support commitment.

Canonical sources: RFC-0001 Section 14; RFC-0002 Section 18.2.

### Security, Privacy and Isolation

**Security, Privacy and Isolation** are structural properties that constrain platform capabilities, products, experiments, workflows, extensions and adapters.

Accepted requirements include deny-by-default access, least privilege, organization scoping, data minimization, classification- and rights-aware handling, applicable retention and deletion rules, attributable consequential access and change, and failure behavior that does not silently broaden access or cross tenant boundaries.

RFC-0002 adds metamodel-level guardrails: possession of an Identity or existence of a Typed Relationship does not itself grant access or authority, and physical Canonical Record representation must not require unnecessary sensitive-data duplication.

The exact identity, authorization, cryptography, isolation and privacy mechanisms remain subject to later Accepted architecture and subordinate decisions.

Canonical sources: Constitution Article VIII; RFC-0001 Sections 17 and 19; RFC-0002 Sections 7.5, 8.8 and 9.7.

### AI Authority

**AI Authority** describes the boundary that AI is an execution capability, not an organizational authority source or canonical source by default.

AI systems may analyze, retrieve, classify, recommend, draft, transform, generate and propose improvements. They do not gain authority merely because they can technically perform an action, and they must not silently change approved standards, grant permissions, approve consequential decisions, replace Canonical Records, promote observations to validated knowledge, share data across organizations, extend retention or bypass validation, security or approval gates.

Canonical sources: Constitution Article XIII; RFC-0001 Sections 7.5 and 21.

## 8. Conformance terms

### Conformance

**Conformance** is assessed against a declared scope rather than against every possible future capability of Arvectum OS.

A conformance claim separates three different axes:

1. subject lifecycle;
2. operational environment;
3. conformance maturity.

A limited pilot, experiment or capability must not be described as fully platform-conformant merely because its bounded scope satisfies applicable requirements.

RFC-0002 additionally defines scoped conformance to the Kernel metamodel; that claim is not equivalent to `Active` lifecycle, production readiness, SLA/support or full-platform conformance.

Canonical sources: RFC-0001 Section 24; RFC-0002 Section 18.

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

The Kernel metamodel itself is no longer provisional after acceptance of RFC-0002 `1.0.0`. The qualifier remains valid in other distinct contexts, including Provisional Product Contracts, provisional capability contracts during incubation, provisional implementation choices in unresolved areas, and `Provisional` conformance maturity.

The exact meaning must therefore be read from the lifecycle or artifact being qualified rather than treated as a single global status.

Canonical sources: RFC-0001 Sections 11, 13 and 24; RFC-0002 `1.0.0`.

## 9. Normative language

RFC-0001 uses capitalized normative keywords as follows:

- **MUST / MUST NOT** — mandatory for conformance unless an approved architectural exception explicitly applies;
- **SHOULD / SHOULD NOT** — default expectation; deviation requires recorded rationale proportionate to impact;
- **MAY** — permitted but not required.

Lower-case uses in explanatory prose do not create additional normative force.

Canonical source: RFC-0001 Section 2.1.

## 10. Terms intentionally not finalized here

RFC-0002 finalizes the Kernel metamodel questions previously listed here: Identity and version semantics, Typed Relationship identity/versioning, Event placement, Execution Context placement/lifecycle and product-neutral migration semantics are now governed by Accepted RFC-0002 `1.0.0`.

The following areas remain deliberately not finalized by this glossary because they are reserved for later Accepted RFCs or subordinate decisions:

- exact Organization/Tenant mapping and tenancy metamodel;
- identity administration, authentication, authorization, security, privacy and tenant-sovereignty mechanisms;
- global identifier wire encoding;
- detailed Product Contract and extension model beyond RFC-0001;
- detailed Governed Execution and Workflow model;
- detailed Event, Provenance and Observability taxonomy/mechanics;
- detailed Memory, Knowledge and Governed Learning lifecycle;
- physical persistence topology, database schema and identifier encoding;
- relationship-type catalogs and reusable record schemas beyond the metamodel invariants accepted in RFC-0002.

These areas remain subject to the follow-up RFC sequence coordinated by the [Canonical Roadmap](../roadmap/ROADMAP.md).

## 11. Quick source map

| Term family | Primary canonical source |
|---|---|
| Organizational Intelligence | Constitution Article 0; RFC-0001 §6.1 |
| Executable Organizational Model | RFC-0001 §6.2 |
| Architectural Responsibility | RFC-0001 §6.5; RFC-0002 §8.1 |
| Organizational Control / Portability | Constitution Article VII; RFC-0001 §§18–19 |
| Proportionality | Constitution Articles VIII, XIII, XVII; RFC-0001 cross-cutting; RFC-0002 §§8.8, 17.8 |
| Kernel metamodel | RFC-0002 §6 |
| Identity / Subject Identity / Version Identity | RFC-0002 §7 |
| Canonical Record / Lineage / Head / Effective Version | RFC-0002 §8 |
| Authority Modes / transitions | RFC-0001 §7.1; RFC-0002 §12 |
| Governed Organizational Asset | Constitution Article XVI; RFC-0001 §7.2; RFC-0002 §13 |
| Transient Output | RFC-0001 §7.3; RFC-0002 §13.4 |
| Typed Relationship | RFC-0002 §9 |
| Event | Constitution Article XI; RFC-0002 §10 |
| Governed Execution / Execution Context | RFC-0001 §7.5; RFC-0002 §11 |
| Product Experiment | RFC-0001 §11.1; RFC-0002 §§17.8, 18 |
| Platform Capability lifecycle | RFC-0001 §§11.2–11.4 |
| Platform Service | RFC-0001 §11.5 |
| Product boundary | Constitution Articles II, III, XX; RFC-0001 §12 |
| Product Contract | RFC-0001 §13 |
| Commercial Commitment Integrity | RFC-0001 §14; RFC-0002 §18.2 |
| Decision Authority / Exceptions | RFC-0001 §16 |
| Security / Privacy / Isolation | Constitution Article VIII; RFC-0001 §17; RFC-0002 §§7.5, 8.8, 9.7 |
| Sovereignty / cross-organization rules | RFC-0001 §19 |
| Extensions | RFC-0001 §20 |
| AI authority | Constitution Article XIII; RFC-0001 §21 |
| Platform Gravity | RFC-0001 §22 |
| Platform Evidence | RFC-0001 §26 |
| Workflow | Constitution Article X |
| Memory | Constitution Article V; RFC-0001 §8 |
| Knowledge | Constitution Article VI; RFC-0001 §8 |
| Conformance | RFC-0001 §§24–25; RFC-0002 §18 |

## 12. Maintenance note

This glossary is a navigation and language artifact, not a substitute for Accepted architecture.

When a later Accepted RFC refines a term, the glossary should be updated to:

1. preserve the established term where still valid;
2. point to the new accepted source;
3. distinguish refinements from superseded meanings;
4. avoid introducing requirements that do not exist in the higher-authority source.
