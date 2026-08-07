# RFC-0003: Identity, Security, Privacy, Tenant Sovereignty and Portability

Status: `Accepted`
Version: `1.0.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`
Supersedes: `RFC-0003 v0.2.0` approved proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS is an operating system for organizational intelligence. Its value depends on an organization being able to trust that identities are stable, access is explicitly authorized, organization boundaries are preserved, sensitive data is processed proportionately, and governed organizational state can be exported, migrated, deleted or handed over without losing meaning.

RFC-0001 establishes structural security, privacy, isolation, organizational-control and portability invariants. RFC-0002 finalizes the Kernel metamodel and establishes that Identity is a stable, non-versioned reference primitive; possessing or resolving an Identity does not grant permission or authority; Canonical Records carry organization scope, authority, classification and governed metadata; and Typed Relationships do not themselves grant access or delegated authority.

This RFC defines the shared domain-neutral architecture required to turn those invariants into an interoperable platform contract without selecting a specific IAM vendor, protocol, database, cloud, cryptographic suite or policy engine.

The model separates five concerns that must not collapse into one another:

1. **Identity** answers who or what a referent is.
2. **Authentication** establishes confidence that an actor controls or represents an asserted identity in a declared context.
3. **Authorization** determines whether a specific actor may perform a specific operation on a specific governed resource under applicable policy and scope.
4. **Organizational Authority** determines whether the actor is organizationally entitled to make the consequential decision or state change, including any delegation and approval requirements.
5. **Data Governance** determines whether the requested collection, use, disclosure, retention, export, deletion or cross-organization movement is permitted for the declared purpose.

These concerns interact but are not interchangeable. Successful authentication does not grant authorization. Authorization does not create organizational decision authority. A relationship does not create a permission. Technical access does not create legal or contractual rights. An administrator does not automatically become entitled to inspect all tenant content.

This RFC also establishes:

- organization and tenant scope semantics;
- principal and actor semantics built on RFC-0002 Identity;
- identity administration and lifecycle requirements;
- authentication assurance as contextual evidence rather than permanent identity state;
- deny-by-default authorization and least-privilege rules;
- explicit delegation and separation between authorization and consequential authority;
- policy-evaluation and enforcement boundaries;
- cross-organization access and sharing rules;
- isolation requirements and failure-closed behavior;
- data classification, purpose limitation and minimization requirements;
- retention, deletion and legal/contractual restriction semantics;
- auditability and privileged-access safeguards;
- governed portability packages, migration and service-termination requirements;
- key and secret portability boundaries without forcing export of non-exportable credentials;
- break-glass access requirements;
- migration from product-local or provisional IAM implementations;
- scoped conformance criteria.

This RFC does not define detailed workflow semantics, complete event/provenance taxonomy, memory/knowledge promotion, product contracts, concrete authentication protocols, cryptographic algorithms, database row-level security syntax, cloud topology or legal compliance mappings. Those belong to later RFCs, ADRs, standards, policies, Product Contracts, legal agreements or implementation decisions.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 `1.0.0` and RFC-0002 `1.0.0` without changing their architectural laws.

The most relevant constitutional requirements are:

- organizational control and portability are structural requirements;
- security, privacy, confidentiality and data isolation are structural properties;
- identity, least privilege, authorization, tenant isolation, minimization, retention, deletion and auditability must be designed into platform capabilities and workflows;
- every authoritative piece of organizational knowledge has one canonical source;
- AI does not obtain organizational authority merely by executing an operation;
- meaningful consequential actions are observable and reconstructable proportionate to consequence;
- organizational assets remain attributable, governed and portable;
- rigor is proportionate to sensitivity, consequence, reversibility and threat;
- technology choices may change without loss of organizational meaning.

RFC-0001 additionally requires:

- deny-by-default access;
- least privilege;
- organization scoping of governed records, relationships, executions and artifacts unless explicitly shared;
- purpose-limited collection, retrieval and propagation;
- classification-aware storage, retrieval, logging, generation and export;
- applicable retention/deletion rules;
- attributable and observable consequential access and change;
- failure behavior that does not silently broaden access or cross tenant boundaries;
- governed export, migration, deletion, service termination and handover;
- preservation of identities, versions, authority, schemas, relationships, provenance and history where applicable;
- default organization-local authority and isolation;
- explicit rights and governance for cross-organization reuse.

RFC-0002 additionally establishes that:

- Identity is immutable, non-recycled and contains no mutable organizational state;
- Subject Identity and Version Identity are semantic roles;
- Identity resolution is separate from permission;
- external identifiers are aliases or references, not automatically Arvectum OS identities;
- Canonical Records expose organization scope, authority mode, accountable owner, classification/access constraints and policy references where applicable;
- Typed Relationships express governed semantics but do not themselves grant permission or authority;
- consequential reliance on changeable governed state pins exact Version Identities;
- external authority must not be converted into competing Arvectum OS authority.

Where this RFC conflicts with the Constitution, RFC-0001 or RFC-0002, the higher-authority source prevails.

## 3. Scope

This RFC defines the domain-neutral architecture for:

- organization and tenant scope;
- principals, actors and service identities;
- identity administration and lifecycle;
- authentication evidence and assurance context;
- authorization decisions and enforcement;
- least privilege and default denial;
- delegated authority representation boundaries;
- privileged and break-glass access;
- tenant isolation and cross-organization access;
- data classification and purpose-aware processing constraints;
- privacy-oriented minimization, retention and deletion architecture;
- secrets and credential governance boundaries;
- portability, export, migration, deletion, service termination and handover;
- security/privacy evidence required for consequential operations;
- migration and compatibility from provisional implementations;
- scoped conformance.

## 4. Non-goals

This RFC does not define:

- a mandatory IAM provider;
- OAuth, OIDC, SAML, WebAuthn, LDAP, Active Directory or another specific identity protocol;
- password rules or MFA factors;
- a cryptographic algorithm, cipher suite or key-management vendor;
- database tables, ORM classes or row-level security syntax;
- a service-mesh or network segmentation product;
- concrete cloud or on-prem deployment topology;
- jurisdiction-specific legal advice or compliance certification;
- complete controller/processor role mappings;
- specific retention periods;
- a universal enterprise role hierarchy;
- named company positions or financial approval thresholds;
- Product Contract schemas, which belong to RFC-0004;
- full Governed Execution semantics, which belong to RFC-0005;
- complete event, provenance and observability semantics, which belong to RFC-0006;
- memory, knowledge or governed-learning promotion semantics, which belong to RFC-0007;
- domain-specific entitlements or workflows;
- a guarantee that every third-party credential or vendor secret is exportable.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Security and Authority Model

### 6.1 Separation of Concerns

A conforming implementation **MUST** keep the following semantic decisions distinguishable:

```text
Identity
  Who/what is referenced?
        ↓
Authentication
  What evidence supports the actor claim in this context?
        ↓
Authorization
  Is this actor allowed to attempt this operation on this resource?
        ↓
Organizational Authority / Approval
  Is this actor entitled to cause this consequential organizational result?
        ↓
Data Governance
  Is this collection/use/disclosure/retention/export/deletion permitted?
        ↓
Execution / Enforcement
  Perform or refuse the operation and preserve required evidence.
```

An implementation **MUST NOT** treat any earlier layer as automatically satisfying a later layer.

### 6.2 Identity Is Not Permission

An RFC-0002 Identity **MUST NOT** encode mutable permissions, roles, organizational authority or classification in a way that would require issuing a new identity when those properties change.

Possession of an Identity, API key identifier, relationship, tenant membership or resolvable record **MUST NOT** itself grant access.

### 6.3 Authentication Is Contextual Evidence

Authentication establishes evidence that an actor currently controls, represents or acts through an asserted principal identity.

Authentication evidence **MUST** be evaluated in a declared context and **MAY** include factors such as credential type, authentication method, freshness, device posture, external identity-provider assertions or step-up verification.

Authentication assurance **MUST NOT** be stored as permanent truth about the Identity itself.

Where authentication evidence materially affects a consequential authorization or approval, the applicable execution evidence **MUST** preserve enough reference or assurance context to reconstruct why the authentication requirement was considered satisfied, subject to minimization and secret-handling rules.

Raw credentials and reusable secrets **MUST NOT** be placed in canonical history merely to prove authentication.

### 6.4 Authorization Is an Explicit Decision

Authorization answers whether an actor may perform an operation on a governed resource under a declared organization scope, policy set and contextual constraints.

Authorization **MUST** be deny-by-default.

An allow decision **MUST** be attributable to an applicable rule, grant, policy, delegation or explicitly governed exception.

Authorization **MUST** be evaluated at the point where the relevant resource, operation and organization context are known with sufficient certainty.

### 6.5 Organizational Authority Is Distinct

Organizational Authority is entitlement to make or approve a consequential organizational decision or state change.

Technical authorization **MUST NOT** be treated as sufficient evidence of Organizational Authority when a consequential operation requires a decision owner, approver, delegation or other governance authority.

The detailed decision-authority policy may remain subordinate governance, but a conforming system **MUST** be able to represent and enforce the fact that some operations require organizational authority beyond technical permission.

Until approved delegation exists, residual decision authority remains with the applicable owner under Accepted governance rules.

## 7. Organization and Tenant Scope

### 7.1 Organization Is the Sovereignty Boundary

An **Organization** is the governance, authority, data-isolation and sovereignty scope within which an organization-specific Executable Organizational Model is operated.

A **Tenant** is the technical isolation context used to enforce an Organization boundary or an explicitly governed subdivision of one Organization.

This RFC does not require one physical database or deployment per tenant.

### 7.2 Organization–Tenant Mapping

Each tenant context **MUST** resolve unambiguously to exactly one governing Organization for authority and sovereignty evaluation.

One Organization **MAY** use multiple technical tenant partitions for operational reasons.

A technical tenant partition **MUST NOT** become an independent sovereignty boundary unless the governing model explicitly defines it as such.

Multiple Organizations **MUST NOT** share one undifferentiated tenant authority context.

### 7.3 Organization Scope on Governed State

Significant Canonical Records, relationships, executions and governed artifacts **MUST** carry or resolve to an Organization scope unless explicitly classified and governed as platform-global or cross-organization shared state.

Platform-global state **MUST** be limited to genuinely platform-governed semantics and **MUST NOT** become a hidden channel for customer or organization-specific data.

### 7.4 No Ambient Cross-Organization Authority

An actor authenticated in Organization A **MUST NOT** receive access to Organization B merely because the actor has the same email address, external directory identifier, employer, vendor account, product account or technical credential elsewhere.

Cross-organization access requires an explicit governed grant or contract in each relevant scope.

## 8. Principal and Actor Model

### 8.1 Principal

A **Principal** is an RFC-0002 Subject Identity that may participate in authentication, authorization or authority evaluation.

Principal categories **MAY** include:

- human;
- service;
- workload;
- external system;
- AI agent or AI-mediated actor;
- integration client.

Principal category is governed state associated with the identity and **MUST NOT** be inferred solely from identifier syntax.

### 8.2 Actor

An **Actor** is the principal acting in a specific execution context, together with relevant representation, delegation and authentication context.

The same Principal may act under different organization scopes, roles, delegations and authentication assurance levels without changing its Subject Identity.

### 8.3 Human and Machine Accountability

Automated services and AI components **MUST** use attributable principal identities when their actions are operationally significant.

A shared anonymous technical account **MUST NOT** be used where it would prevent attribution of consequential action to the responsible service, workload or initiating human/governed process.

### 8.4 Impersonation and Acting-On-Behalf-Of

Impersonation, support access or acting-on-behalf-of flows **MUST** preserve both:

- the actual acting Principal; and
- the represented or delegated Principal, where applicable.

Such flows **MUST NOT** erase the identity of the real operator.

## 9. Identity Administration and Lifecycle

### 9.1 Identity Administration Is Governed State

Identity creation, binding, membership, disablement, recovery, external alias association and significant credential-administration changes are governed administrative operations.

The Identity primitive itself remains immutable; mutable lifecycle and administration state **MUST** be represented through governed records or equivalent versioned state referencing the Identity.

### 9.2 Identity Issuance

Identity issuance **MUST** establish:

- identity namespace and scope;
- intended principal category or referent type where applicable;
- accountable administrative owner or authority;
- creation provenance sufficient for the declared risk.

An identity **MUST NOT** be recycled after retirement.

### 9.3 External Identity Binding

An external IdP, directory, government identifier, email address or vendor user ID **MAY** be bound as an external alias or authentication reference.

The binding **MUST** preserve the external authority and namespace.

A changed external identifier **MUST NOT** silently create a new Arvectum OS Principal when the semantic principal remains the same, nor silently merge two principals when identity equivalence is uncertain.

### 9.4 Joiner, Mover and Leaver Behavior

A conforming implementation **MUST** support revocation or reduction of access when a principal's relationship, role, contract or organizational status changes.

Revocation of authorization **MUST NOT** require deletion or mutation of historical identity references needed to reconstruct past governed actions.

Historical attribution and current authorization are separate concerns.

### 9.5 Credential Recovery

Credential recovery or identity re-binding **MUST** be treated as a security-sensitive operation with assurance proportionate to account consequence.

Recovery **MUST NOT** silently expand authorization or delegated authority beyond the restored principal's current governed grants.

## 10. Authentication Architecture

### 10.1 Replaceable Authentication Providers

Arvectum OS **MAY** integrate one or more authentication providers.

Authentication provider choice **MUST NOT** redefine principal identity semantics or become the sole inaccessible representation of organization membership, authorization or canonical organizational authority.

### 10.2 Assurance Requirements

A policy **MAY** require stronger or fresher authentication for higher-consequence operations.

Step-up authentication **SHOULD** be possible without issuing a new Principal Identity.

### 10.3 Session and Token Scope

Authentication sessions, tokens and credentials **MUST** have bounded scope and lifetime proportionate to their privilege and threat model.

Session or token claims **MUST NOT** be trusted beyond the scope and freshness guarantees under which they were issued.

### 10.4 Secret Handling

Reusable secrets, private keys, passwords, recovery codes and equivalent credentials **MUST** be stored and transmitted through controls appropriate to their sensitivity.

They **MUST NOT** be logged, embedded in portable canonical exports, placed in model prompts or persisted as ordinary Canonical Record payload merely for convenience.

## 11. Authorization Model

### 11.1 Authorization Inputs

An authorization decision **MAY** consider:

- actor Principal Identity;
- Organization and tenant context;
- requested operation;
- target Subject or Version Identity;
- resource type and classification;
- governed grants, roles or attributes;
- delegation context;
- Product Contract or capability scope where applicable;
- policy versions;
- authentication assurance and freshness;
- environmental or risk context;
- declared purpose where relevant.

The exact authorization language is not defined by this RFC.

### 11.2 Least Privilege

Authorization grants **MUST** be limited to the minimum operation, resource scope, organization scope and duration reasonably required for the declared purpose.

Broad administrative grants **MUST** be exceptional, attributable and reviewable.

### 11.3 Explicit Resource and Operation Semantics

Permissions **SHOULD** be expressed against stable domain-neutral operation and resource semantics rather than incidental UI screens, database tables or code module names when the permission is intended to survive technology changes.

### 11.4 Relationship Is Not Permission

A Typed Relationship such as `member_of`, `owns`, `assigned_to`, `works_for` or similar **MUST NOT** itself be interpreted as an authorization grant unless a governed authorization policy explicitly references that relationship type and version semantics.

### 11.5 Version Awareness

Where a policy, classification, delegation or other governed input materially determines a consequential authorization decision, the evidence for that decision **MUST** preserve the materially relied-upon version or equivalent immutable reference when required for reconstruction.

This requirement does not force every low-risk read to create a Canonical Record.

### 11.6 Enforcement

An authorization architecture **MUST** distinguish, conceptually if not physically:

- **Policy Administration** — how governed rules/grants are created and changed;
- **Policy Decision** — how an allow/deny decision is evaluated;
- **Policy Enforcement** — where the operation is actually blocked or permitted;
- **Policy Information** — governed contextual inputs consulted by evaluation.

These roles **MAY** be implemented in one component for simplicity.

A product or service **MUST NOT** bypass an applicable enforcement point by directly accessing underlying canonical state or shared storage through an undocumented path.

## 12. Delegation and Consequential Authority

### 12.1 Delegation Is Explicit Governed State

Delegated authority **MUST** be explicit, attributable, scoped and revocable.

A delegation **MUST** identify, directly or by governed reference where applicable:

- delegator authority;
- delegate Principal;
- permitted authority scope;
- Organization scope;
- effective period or revocation condition;
- restrictions or approval conditions;
- provenance and governing policy.

### 12.2 No Delegation by Credential Sharing

Sharing a password, token, session or service credential **MUST NOT** constitute valid organizational delegation.

### 12.3 AI and Service Delegation

An AI system or service may execute within delegated technical permission, but **MUST NOT** be presumed to hold independent organizational authority.

Where consequential authority remains human or governance-controlled, the execution must preserve the accountable authority and required approval separately from the technical service identity.

## 13. Privileged Access and Break-Glass

### 13.1 Administrative Privilege

Platform or tenant administration capability **MUST NOT** automatically imply unrestricted access to all organization content.

Operational administration and content access **SHOULD** be separable where feasible and proportionate.

### 13.2 Break-Glass

Emergency access **MAY** bypass ordinary authorization constraints only through an explicitly governed break-glass mechanism.

Break-glass access **MUST** be:

- exceptional and purpose-bounded;
- attributable to an actual Principal;
- time-bounded;
- limited to the minimum required scope;
- observable;
- reviewable after use;
- incapable of silently becoming a permanent grant.

Where prior approval is impossible because of the emergency, post-event review **MUST** be required proportionate to consequence.

## 14. Tenant Isolation

### 14.1 Isolation Invariant

A failure, malformed request, cache key collision, authorization error, search index, model context, logging pipeline, background job, export path or administrative tool **MUST NOT** cause one Organization's governed or sensitive data to become visible or mutable from another Organization without explicit governed authorization.

### 14.2 Isolation Layers

Implementations **SHOULD** apply multiple mutually reinforcing isolation controls proportionate to risk, such as application authorization, storage scoping, process/runtime separation, network controls, encryption boundaries or deployment partitioning.

This RFC does not require every layer for every deployment.

### 14.3 Fail Closed

If Organization scope cannot be determined reliably for an operation involving governed or sensitive state, the operation **MUST** fail closed rather than use a default tenant.

### 14.4 Background and Asynchronous Work

Background jobs, scheduled tasks, queues, caches and asynchronous workers **MUST** carry explicit Organization scope and attributable execution identity sufficient to prevent ambient cross-tenant processing.

### 14.5 AI Context Isolation

Prompts, retrieval context, embeddings, vector indexes, model caches and generated intermediate artifacts **MUST** respect the same organization, classification and permitted-use boundaries as the governed data from which they are derived.

Model-provider configuration **MUST NOT** silently broaden retention, training use or cross-organization exposure beyond applicable policy, contract and rights.

## 15. Cross-Organization Access and Sharing

### 15.1 Default Prohibition

Cross-organization access, replication, reuse and disclosure are denied by default.

### 15.2 Required Basis

A cross-organization flow **MUST** have an explicit governed basis that identifies, where applicable:

- source Organization;
- receiving Organization or platform scope;
- data or asset scope;
- purpose;
- rights or contractual basis;
- classification constraints;
- permitted transformations and reuse;
- retention/deletion behavior;
- revocation or termination behavior;
- accountable authority.

### 15.3 Shared Platform Learning

Operational evidence, customer data or organizational intelligence **MUST NOT** become shared platform knowledge merely because multiple organizations use the same platform.

Cross-organization promotion or reuse requires explicit rights, classification, policy and governance consistent with RFC-0001.

### 15.4 Shared Identity Providers

Two Organizations may rely on the same external identity provider without sharing authorization state, organizational authority or canonical organizational data.

## 16. Data Classification, Purpose and Minimization

### 16.1 Classification

Governed or sensitive data **MUST** have a classification or resolvable handling rule proportionate to its risk when classification affects access, logging, retention, export or external processing.

A later subordinate standard may define the concrete classification taxonomy.

### 16.2 Purpose Limitation

Collection, retrieval, propagation and processing **MUST** be limited to data reasonably required for a declared and permitted purpose.

Possessing technical access to data **MUST NOT** imply permission to use it for an unrelated product, model training, analytics, marketing or cross-organization learning purpose.

### 16.3 Data Minimization

Implementations **MUST NOT** duplicate or retain sensitive data merely because a framework, model provider or physical schema makes duplication convenient.

Where a governed reference preserves required semantics with lower exposure, the reference **SHOULD** be preferred.

### 16.4 Derived Data

Derived artifacts, embeddings, summaries, feature vectors, model outputs and indexes **MUST** inherit applicable organization, classification, purpose, retention and deletion constraints unless a governed transformation explicitly establishes a different lawful classification or scope.

Derived data **MUST NOT** be treated as unrestricted merely because the original text is no longer human-readable.

## 17. Retention and Deletion

### 17.1 Applicable Rule

Governed data **MUST** resolve to an applicable retention or deletion rule where required by classification, contract, law, product commitment or platform policy.

This RFC does not set universal retention durations.

### 17.2 Deletion Versus Historical Integrity

Deletion requirements and historical reconstruction requirements may conflict.

A conforming implementation **MUST** resolve that conflict through applicable law, contract, policy and classification rather than by assuming either indefinite retention or unconditional deletion.

Where lawful deletion removes payload required by an immutable historical reference, the system **MAY** preserve non-sensitive tombstone, lineage or evidence metadata sufficient to explain that content was deleted, provided such metadata is itself permitted to remain.

### 17.3 Cascading Derived Data

Deletion workflows **MUST** account for governed replicas, caches, indexes, embeddings, derived artifacts and other retained representations within the declared scope.

A subordinate implementation standard **MAY** define asynchronous deletion windows and verification methods.

### 17.4 External Authority

For `External Reference` and `Governed Replica` records, Arvectum OS **MUST NOT** claim deletion from the external authority unless it has actually executed and verified an authorized external deletion operation within scope.

Local deletion and external-source deletion are distinct facts.

## 18. Logging, Auditability and Security Evidence

### 18.1 Consequential Access

Consequential access or change involving sensitive or canonical state **MUST** be attributable and observable proportionate to consequence.

### 18.2 Audit Data Minimization

Auditability **MUST NOT** become an excuse to copy unrestricted sensitive payload into logs.

Audit evidence **SHOULD** preserve identities, references, policy/version context, operation, outcome, organization scope and necessary metadata rather than full content when full content is not required.

### 18.3 Tamper Resistance

Security-relevant evidence **SHOULD** have integrity protection proportionate to its evidentiary importance and threat model.

This RFC does not mandate a specific signing or append-only storage technology.

### 18.4 Separation from RFC-0006

This section defines minimum security/privacy evidence obligations only. Complete Event, Provenance and Observability semantics remain the scope of RFC-0006.

## 19. Secrets, Keys and External Credentials

### 19.1 Secret Material

Secret material is not ordinary organizational knowledge and **MUST** receive handling appropriate to credential sensitivity.

### 19.2 Reference over Duplication

Where feasible, Canonical Records and configuration **SHOULD** reference a secret-management identity or handle rather than contain reusable secret values.

### 19.3 Rotation and Revocation

Credential and key-management architecture **MUST** support rotation and revocation without changing stable organizational Subject Identities unnecessarily.

### 19.4 Portability Boundary

Portability **MUST** preserve the organization's ability to reconstruct configuration, ownership, dependency and replacement requirements for secrets and keys.

It **MUST NOT** require export of private keys, hardware-bound credentials, third-party secrets or provider tokens when law, security design or provider constraints prohibit export.

In such cases the portability package **MUST** identify the non-exportable dependency and provide enough governed metadata to support replacement, re-binding or migration without pretending that secret portability was achieved.

## 20. Portability and Organizational Sovereignty

### 20.1 Portability Objective

Portability exists to preserve organizational continuity, governed meaning and control across technology replacement, migration, service termination and handover.

Portability is not merely a database dump.

### 20.2 Governed Portability Package

Within the applicable scope, a governed export or migration package **MUST** preserve or explicitly account for, where applicable:

- Organization and tenant scope;
- Subject and Version Identities;
- Canonical lineage and effective-version semantics;
- schemas and schema versions;
- authority modes and authoritative-source references;
- Canonical Records and permitted payload;
- Typed Relationships and endpoint reference semantics;
- asset designations;
- classifications and handling constraints;
- authorization and delegation records necessary to understand governed state;
- retention/deletion policy references;
- provenance and history required for reconstruction;
- workflow, decision and event references when those later models are in scope;
- artifacts or lawful immutable references;
- external dependencies and non-exportable secret/key dependencies;
- integrity and manifest metadata.

### 20.3 Open and Understandable Representation

A portability package **MUST** use documented representations sufficient for an authorized recipient to understand identities, versions, relationships, authority and governed semantics without access to an inaccessible proprietary runtime.

This does not require every internal optimization or vendor-specific cache to be portable.

### 20.4 Export Is Authorized Disclosure

Export **MUST** be treated as a security- and privacy-sensitive operation.

An export **MUST** enforce applicable authorization, organizational authority, classification, purpose, rights and contractual restrictions.

The ability to administer a tenant technically **MUST NOT** automatically grant the right to export every class of data.

### 20.5 Service Termination and Handover

A conforming operational deployment **MUST** have a documented termination/handover path proportionate to its scope and commitments.

The path **MUST** address:

- export or transfer of permitted organizational state;
- treatment of non-exportable dependencies;
- credential/key replacement or revocation;
- retained copies and deletion obligations;
- external authoritative references;
- verification of completion;
- residual legally required retention.

### 20.6 Manual Early-Stage Portability

A manual, documented and tested portability or deletion process **MAY** satisfy an early-stage requirement when proportionate to scope, risk and customer commitments.

Manual does not mean unspecified or untested.

## 21. Migration Between Deployments or Providers

### 21.1 Preserve Semantic Identity

Migration **SHOULD** preserve Subject and Version Identity semantics whenever possible.

A physical storage key or vendor identifier **MUST NOT** be treated as the portable organizational identity unless it is already the governed identifier by contract.

### 21.2 Re-binding External Systems

When authentication providers, secret stores, external systems or infrastructure change, the migration **MUST** preserve governed mappings and record any necessary re-binding without silently changing organizational authority.

### 21.3 No Competing Canonical Authority

During migration, one authority scope **MUST** have a clear canonical source at each stage.

Dual-running systems **MAY** exist, but the cutover plan **MUST** define source-of-truth, synchronization, freeze/cutover and rollback behavior sufficient to avoid competing authority.

### 21.4 Migration Verification

Migration verification **SHOULD** test at least:

- identity and version integrity;
- organization scope;
- authorization isolation;
- relationship integrity;
- authority-mode fidelity;
- required history/provenance preservation;
- classification and retention metadata;
- export completeness within declared scope.

## 22. Product, Extension and Integration Boundary

### 22.1 No Product Bypass

A product, extension or integration that interacts with platform-governed state **MUST** use the applicable explicit platform boundary rather than bypass authorization or isolation through internal storage access.

The detailed Product Contract model remains RFC-0004 scope.

### 22.2 Product-Specific Entitlements

Product-specific roles, domain permissions and business approval logic belong to the product unless promotion to shared platform semantics is separately justified.

This RFC defines shared authorization architecture; it does not make every product role a platform role.

### 22.3 External Systems of Record

Security controls around an external system **MUST** preserve the RFC-0001/RFC-0002 authority model.

Access to an external system through Arvectum OS **MUST NOT** imply that Arvectum OS becomes authoritative for the external facts.

## 23. AI-Specific Security and Privacy Constraints

### 23.1 AI Is an Actor or Component, Not an Authority Source

AI components **MUST** operate under attributable service/workload identities and bounded authorization where their behavior is operationally significant.

AI output **MUST NOT** grant permissions, create delegation, approve consequential action or broaden data-use rights merely because a model generated the instruction.

### 23.2 Context Assembly

Retrieval and prompt assembly **MUST** enforce authorization, organization scope, classification and purpose before protected content is included in model context.

Filtering model output after unauthorized data was disclosed to the model is not a substitute for pre-retrieval authorization.

### 23.3 External Model Providers

Use of an external model provider **MUST** be consistent with applicable classification, permitted-use, retention, residency/transfer obligations where applicable, and contractual rights.

Provider substitution **SHOULD** remain possible without changing canonical organizational identities or authority semantics.

## 24. Failure and Degraded-Mode Behavior

### 24.1 Security Decision Failure

If an authorization or required policy decision cannot be evaluated reliably, consequential access or change **MUST** fail closed unless an explicitly governed degraded-mode or break-glass rule applies.

### 24.2 Dependency Failure

Failure of an identity provider, policy service, key service, external authority or network dependency **MUST NOT** silently broaden access, cross tenant boundaries or erase required attribution.

### 24.3 Cached Decisions

Cached authentication or authorization results **MAY** be used where their lifetime, revocation behavior and risk are explicit.

A cached allow decision **MUST NOT** outlive the assurance or policy conditions under which relying on it is safe for the operation's declared consequence.

## 25. Proportionality and Maturity

Security and privacy controls **MUST** be proportionate to sensitivity, consequence, reversibility, threat and customer commitments.

A bounded internal experiment may use simpler manual administration, local authentication or manually reviewed export where the scope and risk justify it.

It **MUST NOT** use proportionality to:

- bypass tenant isolation;
- omit authorization entirely for protected data;
- expose secrets in logs or prompts;
- silently share data across organizations;
- invent undeclared organizational authority;
- ignore applicable legal or contractual restrictions;
- make unsupported production or compliance claims.

Operational standards may strengthen requirements by maturity tier without changing this architectural contract.

## 26. Implementation Independence

Conformance to this RFC does not require:

- microservices;
- a separate policy engine;
- a dedicated graph database;
- per-tenant physical databases;
- a particular cloud;
- a specific identity provider;
- a specific cryptographic algorithm;
- a specific secrets manager.

A modular monolith may satisfy this RFC when semantic boundaries, enforcement and isolation are explicit and testable.

Commodity security infrastructure **SHOULD** be integrated rather than rebuilt unless custom implementation creates demonstrated strategic value or is required by constraints.

## 27. Migration from Provisional Implementations

### 27.1 General Rule

Existing product-local or provisional identity/security implementations **MUST NOT** be declared non-conforming solely because their physical representation differs from this RFC.

Migration is required when they interact with shared platform canonical state or make conformance claims within this RFC's scope.

### 27.2 Inventory

Before migration, identify:

- identities and external aliases;
- organization/tenant mappings;
- roles, grants and implicit permissions;
- service and AI identities;
- credentials and secrets;
- data classification assumptions;
- cross-organization flows;
- export/deletion paths;
- external systems of record;
- unresolved authority ambiguities.

### 27.3 Eliminate Ambient Authority

Implicit permissions based only on database access, shared credentials, undocumented role names, tenant-default behavior or relationship existence **SHOULD** be converted into explicit governed authorization semantics before consequential platform reliance.

### 27.4 Staged Migration

Migration **MAY** be staged by product, tenant, resource type or capability.

A big-bang IAM migration is not required when a bounded compatibility layer can preserve security, authority, attribution and migration safety.

### 27.5 Legacy Identity Mapping

Legacy identifiers **MAY** remain external aliases while new stable Arvectum OS Principal Identities are introduced.

Ambiguous person/account merges **MUST** be resolved explicitly rather than guessed.

## 28. Conformance

### 28.1 Scoped Claim

A conformance claim **MUST** state its subject and scope.

Examples:

- `RFC-0003 identity-administration conformance`;
- `RFC-0003 tenant-isolation conformance for service X`;
- `RFC-0003 portability conformance for pilot Y`.

A limited pilot **MUST NOT** claim full-platform security or privacy conformance merely because one boundary is implemented.

### 28.2 Minimum Identity Conformance

Within a claimed identity scope:

1. stable Principal Identity is separate from mutable permissions and lifecycle state;
2. external identifiers are namespaced bindings or aliases rather than accidental global identity;
3. identities are non-recycled;
4. historical attribution survives access revocation;
5. machine/AI actors are attributable where operationally significant.

### 28.3 Minimum Authorization Conformance

Within a claimed authorization scope:

1. access is deny-by-default;
2. allow decisions have an explicit governed basis;
3. least privilege is applied proportionate to scope;
4. organization scope is evaluated explicitly;
5. relationships do not grant permission implicitly;
6. technical authorization is not confused with consequential organizational authority;
7. failure does not silently broaden access.

### 28.4 Minimum Isolation Conformance

Within a claimed isolation scope:

1. tenant/Organization mapping is unambiguous;
2. data access and mutation cannot cross organization boundaries without explicit authorization;
3. background/asynchronous work carries organization scope;
4. caches, indexes, retrieval and AI context respect organization boundaries;
5. unresolved scope fails closed.

### 28.5 Minimum Privacy/Data-Governance Conformance

Within a claimed privacy scope:

1. protected data has applicable classification/handling semantics where required;
2. processing has a permitted purpose;
3. collection and retention are minimized proportionate to purpose;
4. derived data preserves applicable restrictions;
5. deletion addresses relevant retained representations;
6. external authority deletion is not falsely claimed.

### 28.6 Minimum Portability Conformance

Within a claimed portability scope:

1. the export is authorized and scope-declared;
2. identities, versions, relationships, authority and schemas are understandable outside the original runtime where applicable;
3. non-exportable dependencies are explicitly identified;
4. classification and retention/deletion constraints travel with the package or are otherwise preserved;
5. export completeness and integrity are verifiable proportionate to risk;
6. termination/handover behavior is documented when operational commitments require it.

## 29. Normative Fitness Tests

An implementation or design claiming conformance within scope **MUST** pass applicable tests equivalent to the following.

### FT-01 — Authentication does not imply authorization

Given a valid authenticated principal with no grant to resource R, access to R is denied.

### FT-02 — Authorization does not imply consequential authority

Given a technically authorized operator who lacks required decision authority for consequential action A, the action is not approved merely because the API call is permitted.

### FT-03 — Identity is stable across role change

Changing a principal's role or permissions does not require changing the Principal Subject Identity.

### FT-04 — Relationship does not grant access

Creating a semantic relationship to a protected resource does not grant access unless an explicit policy maps that relationship to a permission.

### FT-05 — Tenant scope fails closed

A request without reliably resolved Organization scope cannot access tenant-governed data by falling back to a default tenant.

### FT-06 — Cross-tenant cache isolation

A cache or index hit created under Organization A cannot be returned under Organization B without an explicit governed cross-organization basis.

### FT-07 — Background job isolation

A background job executes with explicit Organization and actor/service context and cannot operate on another Organization through ambient credentials.

### FT-08 — Revocation preserves history

Revoking a principal's access prevents future protected operations while historical governed actions remain attributable to the same principal.

### FT-09 — Break-glass is bounded

Emergency access is attributable, time-bounded, observable and does not become a permanent authorization grant.

### FT-10 — Derived-data restrictions

An embedding, summary or generated artifact derived from restricted Organization A data does not become unrestricted or visible to Organization B merely because its representation differs from the source.

### FT-11 — Deletion distinguishes local and external authority

Deleting an Arvectum OS replica does not produce a claim that the external authoritative source was deleted unless that external deletion was separately authorized and verified.

### FT-12 — Portability preserves meaning

An authorized recipient can identify exported subjects, versions, schemas, authority modes and relationship semantics without access to the original runtime.

### FT-13 — Non-exportable secrets are explicit

A portability package does not copy prohibited private keys or third-party credentials, but identifies the dependency and required replacement/re-binding path.

### FT-14 — AI retrieval respects authorization

Protected content is excluded before prompt assembly when the model-invoking actor is not authorized to retrieve it.

### FT-15 — Failure does not broaden access

Failure of the policy decision mechanism, identity provider or tenant resolver does not silently convert a denied/unknown operation into allowed access.

## 30. Security and Privacy Threat Scenarios

The following scenarios are informative validation cases, not a complete threat model.

### 30.1 Shared Email Across Organizations

A consultant uses the same email address to access two customer organizations. The external account may authenticate the same person, but each Organization maintains separate grants and authority. No ambient cross-tenant access exists.

### 30.2 Support Engineer Investigation

A platform engineer can operate infrastructure but cannot inspect customer content by default. If content access is required, a governed support or break-glass path records actual actor, purpose, scope and review evidence.

### 30.3 AI Retrieval Assistant

A retrieval assistant searches organization documents. Authorization is applied before protected chunks enter the model context. Model output filtering alone is insufficient.

### 30.4 Customer Migration

A customer terminates service. The portability package preserves permitted canonical identities, versions, relationships, authority/source references and required history. Hardware-bound keys and vendor tokens are not copied; replacement requirements are included in the manifest.

### 30.5 External ERP Record

Arvectum OS references an ERP customer record. Permission to read the Arvectum OS reference does not automatically grant permission to call the ERP. If the ERP remains authoritative, migration or deletion does not convert the Arvectum OS copy into a competing source of truth.

## 31. Consequences

### 31.1 Positive Consequences

This RFC:

- gives products and future services one stable security/identity vocabulary;
- prevents accidental coupling of identity to one vendor directory;
- prevents role, relationship and technical access from becoming hidden authority;
- establishes tenant isolation before shared platform state grows;
- makes AI context handling subject to the same boundaries as ordinary data access;
- makes portability an architectural capability rather than an afterthought;
- preserves organization control without requiring per-tenant infrastructure duplication;
- allows simple early implementations while retaining a migration path.

### 31.2 Costs

The architecture requires explicit organization context, attributable machine identities, explicit grants, classification/retention handling where relevant, and portability metadata. These add implementation work compared with informal shared credentials and implicit database access.

The cost is intentional where it prevents authority ambiguity, data leakage, lock-in or loss of reconstruction capability.

### 31.3 Risks

Primary risks include:

- overengineering early-stage IAM;
- treating this RFC as a compliance certification;
- creating a universal enterprise role model too early;
- logging excessive sensitive data for auditability;
- conflating security administration with right to inspect tenant content;
- making portability synonymous with export of secrets;
- using organization boundaries so rigidly that legitimate governed multi-organization collaboration becomes impossible.

The RFC mitigates these through proportionality, domain-neutral semantics, explicit cross-organization grants and implementation independence.

## 32. Required Follow-up Decisions

Acceptance of this RFC does not eliminate the need for subordinate decisions.

Likely follow-up artifacts include, when implementation requires them:

- ADR: initial authentication/identity-provider integration;
- ADR: authorization enforcement architecture for the reference implementation;
- ADR: tenant-isolation implementation strategy;
- ADR: secrets/key-management integration;
- standard: data classification and handling levels;
- standard: retention/deletion execution and verification;
- standard: portability package manifest and serialization format;
- policy: privileged support and break-glass access;
- policy: approved cross-organization data-sharing basis;
- approved Decision Authority Policy or replacement governance artifact.

These artifacts **MUST NOT** weaken this RFC or higher-authority sources.

## 33. Deliberately Deferred Questions

The following remain deferred:

- concrete Product Contract authorization declarations — RFC-0004;
- exact Governed Execution approval-state machine — RFC-0005;
- event taxonomy and audit/event persistence model — RFC-0006;
- memory/knowledge rights propagation and promotion — RFC-0007;
- specific classification labels and retention periods — subordinate standards/policies;
- authentication protocols and cryptographic choices — ADRs/standards;
- jurisdiction-specific compliance mappings — legal/compliance artifacts.

## 34. Alternatives Considered

### 34.1 Identity Equals External IdP Account

Rejected because external providers can change, one person may have multiple providers or organization contexts, and identity semantics must remain portable.

### 34.2 Role-Based Access Control Only

Rejected as the fundamental architecture because fixed roles alone cannot express organization scope, resource classification, delegation, purpose, contextual assurance or product-specific needs. RBAC remains permitted as an implementation technique within scope.

### 34.3 Attribute-Based Access Control Only

Rejected as the fundamental architecture because it would overconstrain implementation and still would not solve organizational decision authority or rights governance by itself. ABAC remains permitted.

### 34.4 One Physical Database per Tenant as a Normative Rule

Rejected because the sovereignty requirement is semantic and security-oriented, not a mandatory deployment topology. Physical separation may still be required by threat, contract or customer needs.

### 34.5 Platform Administrator Can Access Everything

Rejected because operational administration does not automatically establish organizational permission, contractual right or privacy basis to inspect tenant content.

### 34.6 Portability as Raw Database Dump

Rejected because physical rows do not necessarily preserve governed identity, version, authority, schema, relationship and history semantics.

## 35. Cross-Review Development Record

RFC-0003 `0.1.0` was prepared as the initial complete working draft and then subjected to a functional role-based cross-review across:

- CEO / strategy and commercial integrity;
- COO / operational usability and incident handling;
- CTO / architecture and implementation independence;
- CISO / security engineering and threat boundaries;
- Privacy / data minimization, retention and derived-data handling;
- Legal / rights, disclosure and portability boundaries;
- Product / product-platform separation;
- Engineering / migration, enforceability and testability.

The review produced material changes incorporated into the approved `0.2.0` proposal, including:

1. separating authentication, technical authorization, organizational authority and data-governance decisions explicitly;
2. preventing platform/tenant administrators from receiving implicit unrestricted content access;
3. defining Organization as the sovereignty boundary while allowing multiple technical tenant partitions per Organization;
4. adding explicit support, impersonation and acting-on-behalf-of attribution;
5. adding break-glass requirements with bounded post-event review;
6. strengthening AI retrieval rules so authorization occurs before protected context is sent to a model;
7. extending minimization and deletion rules to embeddings, indexes and other derived data;
8. clarifying that portability does not require export of non-exportable secrets or private keys;
9. requiring a portability manifest for non-exportable dependencies and replacement/re-binding paths;
10. strengthening fail-closed behavior for unresolved tenant scope and unavailable policy decisions;
11. adding version-aware authorization evidence only for consequential decisions, avoiding unnecessary canonicalization of ordinary low-risk reads;
12. preserving product-specific entitlements outside the shared platform unless separately justified;
13. adding staged migration and compatibility rules rather than requiring a big-bang IAM migration;
14. adding normative fitness tests for cross-tenant caches, asynchronous jobs, derived data, external deletion claims and AI retrieval.

The detailed review record is maintained in `docs/reviews/RFC-0003-functional-cross-review.md`.

## 36. Acceptance Record

RFC-0003 `0.2.0` was explicitly approved by the owner of Arvectum OS on `2026-08-07` for publication as `Accepted 1.0.0`.

Canonical approval evidence:

- [`DECISION-2026-08-07-RFC-0003-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0003-ACCEPTANCE.md) — `Approved`.

The approval record was committed independently before this acceptance publication, satisfying the repository Acceptance Integrity requirement that owner approval exist independently of the acceptance commit.

This `1.0.0` publication changes status/version metadata and acceptance-record wording only; it does not silently change the owner-approved normative substance of RFC-0003 `0.2.0`.
