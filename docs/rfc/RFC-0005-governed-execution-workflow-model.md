# RFC-0005: Governed Execution and Workflow Model

Status: `Proposed`
Version: `0.1.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`
Forward-compatible with: `RFC-0004 v0.3.0` (`Proposed`, non-normative)
Supersedes: `None`
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS requires consequential changes to canonical organizational state to occur through **Governed Execution**. RFC-0001 establishes this as an architectural law. RFC-0002 defines Execution Context as a Canonical Record specialization with stable execution identity and immutable governance-significant versions. RFC-0003 separates identity, authentication, authorization, organizational authority and data governance so that technical ability to perform an action does not become organizational authority.

This RFC defines the domain-neutral execution and workflow model that makes those requirements operational without selecting a workflow engine, job scheduler, message broker, programming language, AI provider, BPMN runtime or service topology.

The model is built around eight rules:

1. **A Workflow defines governed executable intent; an Execution Context records one governed attempt to carry that intent out.**
2. **Every consequential canonical mutation MUST occur inside an Execution Context through an authorized operation.**
3. **Execution MUST pin the effective versions of changeable governed inputs, policies, standards, contracts and workflow definitions that materially determine the result.**
4. **Authorization, organizational authority, approval and data-governance checks remain distinct and MUST be satisfied at the points where they are materially required.**
5. **AI components MAY execute, analyze, propose and generate, but MUST NOT acquire undeclared organizational authority or silently activate governed changes.**
6. **Retries, resumptions, compensation and replay MUST preserve causation and MUST NOT create duplicate consequential effects silently.**
7. **Failure MUST be explicit, attributable and fail closed where continuing would risk unauthorized, cross-organization, privacy-violating or inconsistent canonical change.**
8. **Workflow semantics remain domain-neutral in the platform; product-specific business process meaning remains product-owned unless separately promoted through governance.**

This RFC defines:

- Workflow identity, versioning and lifecycle;
- Execution Context lifecycle and state transitions;
- execution initiation and actor context;
- operation semantics and side-effect classes;
- input resolution and immutable version pinning;
- authorization, authority, validation and approval gates;
- canonical mutation rules;
- deterministic and AI-mediated execution;
- idempotency, retries, resumption, compensation and cancellation;
- parent/child execution and delegation boundaries;
- time, deadlines and waiting states;
- external-system interaction and authority preservation;
- failure, uncertainty and partial-completion semantics;
- execution outputs and artifact handling;
- workflow evolution and migration;
- proportional evidence and reconstructability requirements;
- scoped conformance criteria.

This RFC intentionally leaves complete Event taxonomy, delivery semantics, provenance representation and observability infrastructure to RFC-0006, and memory/knowledge/learning promotion semantics to RFC-0007.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 `1.0.0`, RFC-0002 `1.0.0` and RFC-0003 `1.0.0` without changing their architectural laws.

The most relevant constitutional requirements are:

- repeatable and operationally significant processes should be represented as versioned workflows;
- significant governed objects are versioned;
- meaningful consequential actions are observable and reconstructable proportionate to consequence;
- approved organizational assets and consequential operations are reproducible to the extent permitted by declared inputs and dependencies;
- only approved governance mechanisms may authorize consequential changes to production behavior, standards or organizational decisions;
- AI is an execution means rather than a source of organizational authority;
- security, privacy, least privilege, isolation, minimization, retention, deletion and auditability are structural requirements;
- temporary and experimental solutions are permitted when bounded, reversible, owned and governed proportionately;
- architecture precedes cross-cutting irreversible implementation;
- technology may change without loss of organizational meaning.

RFC-0001 additionally requires that consequential canonical change occur through Governed Execution and that the applicable Execution Context identify, where relevant, organization, actor, authority, Product Contract, workflow/version, input versions, external authority, standards/policies, knowledge/memory, deterministic and AI components, validation/approval requirements, outputs/artifacts, events, causation, classification, retention and reproducibility constraints.

RFC-0002 additionally establishes that:

- Execution Context is a Canonical Record specialization;
- one governed execution has a stable Execution Identity;
- governance-significant execution state transitions are represented as immutable canonical versions;
- terminal execution state is sealed and preserved according to applicable retention, privacy, legal and contractual requirements;
- consequential reliance on changeable governed state pins exact Version Identities;
- Canonical Record versions are immutable and corrections create additional linked governed state rather than mutation of history.

RFC-0003 additionally requires that:

- identity, authentication, authorization, organizational authority and data governance remain distinct;
- authorization is deny-by-default;
- technical authorization does not automatically satisfy organizational authority;
- organization/tenant boundaries are explicit and cross-organization access requires governed authorization;
- classification, purpose, minimization, retention and deletion constraints apply to execution;
- privileged and break-glass access remains attributable and governed;
- failure must not silently broaden access or cross organization boundaries.

Where this RFC conflicts with the Constitution or an earlier Accepted RFC, the higher-authority source prevails.

### 2.1 RFC-0004 Status Boundary

RFC-0004 `0.3.0` is `Proposed` and therefore has no normative force at the time of this RFC proposal.

This RFC is designed to remain compatible with the RFC-0004 proposal, especially its Product Contract declarations for operations, canonical reads/writes, security/authority requirements, shared events, artifacts and product/platform dependencies. Any reference to RFC-0004 concepts beyond what is already required by Accepted RFC-0001 is informative until RFC-0004 is accepted.

If RFC-0004 is accepted with materially different execution-boundary semantics, this RFC proposal MUST be reviewed before acceptance.

## 3. Scope

This RFC defines the shared domain-neutral architecture for:

- Workflow identity, versions, lifecycle and effective-version resolution;
- Execution Context lifecycle and governance-significant state;
- execution initiation, actor and organization scope;
- operation declaration and invocation;
- input resolution and version pinning;
- authorization, organizational authority, policy, validation and approval gates;
- canonical mutations and commit boundaries;
- deterministic and AI-mediated work;
- orchestration of sub-executions;
- waiting, resumption, timeout and deadline behavior;
- idempotency, retry and duplicate-suppression semantics;
- compensation, cancellation and reversal semantics;
- external-system interactions while preserving authority modes;
- partial completion and uncertainty;
- execution outputs, artifacts and transient results;
- workflow evolution and in-flight migration;
- reconstructability and proportional execution evidence;
- portability of governed execution history at the semantic level;
- scoped conformance.

## 4. Non-goals

This RFC does not define:

- a mandatory workflow language or BPMN profile;
- a mandatory orchestration engine;
- a task scheduler, queue, worker framework or message broker;
- service boundaries or microservice topology;
- a database schema or ORM model;
- a complete Event taxonomy or delivery guarantee model;
- tracing protocol, telemetry backend, log format or metrics stack;
- a complete provenance graph schema;
- Product Contract schemas or extension registration, which remain RFC-0004 scope;
- memory, knowledge, observation or governed-learning promotion semantics, which remain RFC-0007 scope;
- domain-specific workflows, approval thresholds or business rules;
- named organizational roles or company-specific RACI;
- customer-facing SLA, support or performance commitments;
- a universal distributed transaction protocol;
- automatic legal enforceability of technical approvals;
- automatic promotion of workflow implementations into Platform Capabilities.

These subjects belong to RFC-0004, RFC-0006, RFC-0007, subordinate ADRs, standards, policies, Product Contracts, product decisions, legal agreements or implementation choices.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Model

### 6.1 Workflow

A **Workflow** is a versioned governed definition of how a repeatable or operationally significant class of work is performed.

A Workflow defines executable intent. It may declare:

- entry conditions;
- permitted initiating actors or actor classes by reference;
- required inputs and their resolution rules;
- operations or stages;
- decision points;
- validations;
- approval requirements;
- expected outputs;
- failure, timeout, retry and compensation behavior;
- completion criteria;
- applicable policies, standards and contracts;
- permitted deterministic and AI-mediated components;
- execution evidence requirements proportionate to consequence.

A Workflow MUST NOT derive organizational authority merely from its technical ability to invoke an operation.

### 6.2 Execution Context

An **Execution Context** is the governed Canonical Record specialization representing one execution instance under RFC-0002.

One execution has:

- one stable Execution Identity;
- immutable Execution Context versions for governance-significant transitions;
- one declared Organization scope unless explicitly governed as platform-global or cross-organization;
- an initiating actor or governed trigger;
- an effective Workflow version where a Workflow applies;
- the effective governed inputs and controls necessary to explain and reconstruct the execution within its declared scope.

### 6.3 Workflow and Execution Are Different Subjects

A Workflow definition and an Execution Context MUST have distinct Subject Identities.

Changing a Workflow MUST NOT mutate historical Execution Contexts.

A historical Execution Context MUST remain attributable to the exact Workflow version that governed it where workflow semantics materially determined the result.

### 6.4 Governed Execution

**Governed Execution** is the act of performing work within an Execution Context under applicable authorization, organizational authority, policy, validation, approval, data-governance and evidence requirements.

Governed Execution is a semantic architecture requirement. It does not require one physical runtime or centralized orchestrator.

## 7. Workflow Identity and Versioning

### 7.1 Stable Workflow Identity

A governed Workflow MUST have:

- a stable Workflow Subject Identity;
- immutable Workflow Version Identities;
- a semantic workflow type or name;
- an accountable architectural owner;
- organization, platform or product scope;
- lifecycle status;
- creation and version provenance.

### 7.2 Immutable Versions

An admitted Workflow version MUST NOT be mutated.

A change to executable governed behavior MUST create a new Workflow version under the same Workflow Subject Identity when the semantic workflow remains the same lineage.

A change that creates a materially different process subject MAY require a new Workflow Subject Identity.

### 7.3 Effective Workflow Version

A Workflow MUST distinguish canonical lineage head from the version effective for a particular execution when they differ.

An Execution Context MUST pin the exact Workflow Version Identity before consequential behavior relies on that workflow.

### 7.4 Workflow Lifecycle

A Workflow MAY use a lifecycle such as:

```text
Draft → Approved → Deprecated → Retired
```

A product or governance domain MAY define additional states provided they do not weaken Accepted architecture.

A `Draft` workflow MUST NOT be the sole basis for consequential production behavior unless an explicitly governed experiment or exception permits it within bounded scope.

A `Retired` workflow MUST NOT start new governed executions unless an approved recovery, migration or replay procedure explicitly allows it.

## 8. Execution Lifecycle

### 8.1 Minimum Semantic States

A conforming Execution Context MUST be able to represent at least the following semantic conditions, whether or not an implementation uses these exact labels:

```text
Created
  ↓
Ready / Awaiting Required Gate
  ↓
Running
  ├── Waiting
  ├── Suspended
  ├── Compensating
  ↓
Terminal
  ├── Succeeded
  ├── Failed
  ├── Cancelled
  └── Compensated / Partially Compensated where applicable
```

Implementations MAY combine or refine states when no governed meaning is lost.

### 8.2 Governance-significant Transitions

A transition is governance-significant when it materially affects authority, canonical state, external commitments, execution responsibility, replayability, approval state, compensation obligations, legal/financial position, security/privacy posture or reconstruction of a consequential result.

Each governance-significant transition MUST create a new immutable Execution Context version or equivalent RFC-0002-conforming canonical version.

High-frequency technical worker state that has no governed significance MAY remain operational telemetry rather than canonical execution history.

### 8.3 Terminal Sealing

When an execution reaches a terminal governed state, its terminal Execution Context version MUST be sealed against mutation.

Later correction, reversal, compensation, dispute or reinterpretation MUST be represented through additional linked governed records or executions rather than mutation of the sealed history.

## 9. Initiation and Actor Context

### 9.1 Initiating Actor or Trigger

A governed execution MUST identify either:

- an initiating Actor under RFC-0003; or
- a governed trigger whose authority to initiate can be reconstructed.

A scheduled, event-driven or machine-initiated execution MUST remain attributable to the principal, service, policy or previously governed execution that authorized the trigger path.

### 9.2 Organization Scope

Before consequential work begins, the Execution Context MUST resolve one governing Organization scope, except for explicitly governed platform-global or cross-organization execution.

Cross-organization execution MUST preserve each participating Organization scope and MUST NOT collapse them into an undifferentiated authority context.

### 9.3 Acting on Behalf Of

When an actor acts on behalf of another principal or under delegated authority, execution evidence MUST preserve:

- actual acting Principal;
- represented Principal where applicable;
- applicable delegation or authority reference;
- organization scope;
- relevant authorization/assurance context proportionate to consequence.

## 10. Operation Model

### 10.1 Operation

An **Operation** is a stable semantic action that an execution may attempt against governed state, an external system or a controlled side-effect boundary.

An operation declaration SHOULD identify, where relevant:

- stable operation identity or semantic name;
- input and output types;
- target governed subject or resource semantics;
- side-effect class;
- idempotency expectations;
- authorization requirements;
- organizational authority requirements;
- validation or approval gates;
- data-governance constraints;
- timeout and failure semantics;
- compensation or reversal support.

### 10.2 Side-effect Classes

A conforming implementation MUST be able to distinguish at least:

- `ReadOnly` — no intended governed or external mutation;
- `Transient` — temporary effect that does not become canonical or externally consequential by itself;
- `CanonicalMutation` — changes canonical Arvectum OS state;
- `ExternalMutation` — changes state in an external authoritative or consequential system;
- `Commitment` — creates or materially affects a legal, financial, security, contractual, reputational or equivalent organizational commitment.

One operation MAY belong to more than one consequential class.

Controls MUST increase proportionately with consequence, reversibility, sensitivity and external impact.

## 11. Input Resolution and Version Pinning

### 11.1 Resolve Before Reliance

A changeable governed subject referenced by Subject Identity MUST be resolved to an exact effective Version Identity before consequential behavior relies on it.

The Execution Context or linked governed evidence MUST preserve the exact version used.

### 11.2 Material Governing Inputs

Where they materially determine a consequential result, execution MUST pin or immutably reference the effective versions of applicable:

- Workflow;
- Product Contract where applicable under Accepted architecture;
- Canonical Records and relationships;
- policies;
- standards;
- validators;
- schemas;
- knowledge or memory assets when later RFCs define their governed use;
- model configuration or prompt package where material to reproducibility and lawful retention;
- external authoritative source state or retrieval evidence where exact local pinning is not possible.

### 11.3 Dynamic Inputs

A workflow MAY deliberately resolve inputs dynamically during execution.

When dynamic resolution materially affects a consequential result, the resolved version or external-state evidence MUST be captured at the point of reliance.

### 11.4 Missing or Ambiguous Inputs

If a required authoritative version cannot be resolved unambiguously, consequential execution MUST NOT silently choose a candidate.

The execution MUST either:

- stop or wait for resolution;
- use an explicitly governed fallback allowed by policy; or
- continue only in a bounded non-consequential mode that cannot commit the unresolved result as authoritative state.

## 12. Authorization, Authority, Validation and Approval Gates

### 12.1 Distinct Gates

A workflow MUST keep the following conceptually distinct where applicable:

1. authentication/actor assurance;
2. technical authorization;
3. organizational authority;
4. data-governance permission;
5. validation;
6. human or governed approval.

Passing one gate MUST NOT imply that another has passed.

### 12.2 Point of Enforcement

A gate MUST be evaluated at a point where the information needed for that decision is sufficiently known.

A previous allow decision MUST be re-evaluated when a material change occurs in actor, target, organization scope, authority, policy version, classification, purpose, requested effect or other condition that invalidates the earlier decision assumptions.

### 12.3 Approval Evidence

Where an operation requires approval, the execution MUST preserve enough governed evidence to identify:

- what was approved;
- by which authorized decision authority or delegated approver;
- under which scope and constraints;
- which input/result version was approved where material;
- when approval became effective and expired or was superseded where applicable.

### 12.4 Approval Is Not a Mutable Flag

A consequential approval SHOULD be represented as attributable governed evidence rather than an unaudited mutable boolean.

Revocation or supersession of approval MUST NOT erase historical approval evidence required to reconstruct earlier execution.

## 13. Canonical Mutation

### 13.1 Mandatory Execution Context

Every consequential change to canonical state managed by Arvectum OS MUST occur through an Execution Context and an authorized operation.

A direct database write, internal import, administrative script or AI tool call MUST NOT bypass this rule merely because it is technically able to mutate storage.

### 13.2 Mutation Produces New Canonical Versions

Canonical mutation MUST obey RFC-0002 immutability semantics.

Changing governed state MUST create a new canonical version or a new governed record as appropriate. Existing admitted canonical history MUST NOT be overwritten.

### 13.3 Commit Boundary

An execution that performs multiple consequential mutations MUST define a commit boundary appropriate to its consistency requirements.

The architecture does not require a universal ACID transaction across all systems.

Where atomic completion cannot be guaranteed, the execution MUST expose partial completion explicitly and define recovery, compensation or reconciliation behavior proportionate to consequence.

### 13.4 Concurrency and Conflicting Writes

A canonical mutation MUST detect material conflicts between the state relied upon and the state being committed when concurrent change could invalidate the result.

A conflict MUST NOT silently overwrite a newer canonical version.

Resolution MAY use optimistic concurrency, governed merge, re-evaluation, manual review or another mechanism, provided canonical lineage remains unambiguous.

## 14. Deterministic and AI-mediated Execution

### 14.1 Component Identity

Consequential execution SHOULD preserve the identity and version/configuration of deterministic and AI-mediated components when they materially influence the result.

### 14.2 AI Has No Ambient Authority

An AI component MAY:

- analyze;
- classify;
- extract;
- generate;
- recommend;
- propose;
- select among pre-authorized bounded actions where the governing workflow permits it.

An AI component MUST NOT by itself:

- grant authorization;
- create organizational authority;
- approve a consequential action unless an Accepted governance mechanism explicitly delegates that authority in a manner compatible with the Constitution;
- silently alter approved policies, standards or workflow definitions;
- promote transient output into validated knowledge or authoritative canonical state outside Governed Execution;
- broaden organization scope, retention or cross-organization sharing.

### 14.3 AI Output Classification

AI-generated output is transient by default unless and until a governed workflow explicitly validates and promotes it into canonical state or a Governed Organizational Asset.

### 14.4 Non-determinism

A workflow using non-deterministic components MUST NOT claim byte-for-byte reproducibility unless it can actually provide it.

Instead, it MUST preserve enough declared inputs, versions, configuration, evidence and constraints to reproduce an equivalent result where feasible or explain why equivalence cannot be achieved.

## 15. Idempotency, Retry and Duplicate Effects

### 15.1 Idempotency Requirement

A consequential operation that may be retried MUST declare whether it is:

- naturally idempotent;
- idempotent under a governed idempotency key or execution identity;
- non-idempotent and therefore requires duplicate-protection or manual reconciliation.

### 15.2 Retry

Retry MUST NOT create duplicate canonical mutations, external commitments, approvals or payments silently.

Retry behavior MUST preserve causal linkage to the original operation attempt.

### 15.3 Unknown Outcome

When the system cannot determine whether an external consequential operation succeeded, the execution MUST enter an explicit uncertain or reconciliation-required condition rather than blindly retrying a potentially non-idempotent effect.

## 16. Waiting, Suspension, Resumption and Time

### 16.1 Waiting

An execution MAY wait for:

- human approval;
- external-system response;
- scheduled time;
- event or condition;
- missing authoritative input;
- retry window;
- policy-required cooling or review period.

A waiting execution MUST preserve enough state to resume under the correct Organization, Workflow version and authority context.

### 16.2 Revalidation on Resume

Resumption MUST re-evaluate time-sensitive or changeable gates when their previous decision is no longer valid by policy, expiry, changed scope or changed governed state.

### 16.3 Deadlines and Timeouts

Deadlines and timeouts that materially affect organizational outcome MUST be represented as governed workflow or execution semantics rather than hidden only in worker infrastructure.

A timeout MUST have explicit failure, retry, escalation, cancellation or compensation behavior where consequential.

## 17. Parent and Child Executions

### 17.1 Composition

A Workflow MAY invoke child executions.

Each consequential child execution SHOULD have its own Execution Identity when it has independent authority, failure, retry, retention, portability, audit or lifecycle significance.

### 17.2 Causation

A child execution MUST preserve causal linkage to the parent execution.

The parent MUST NOT be treated as automatically conferring all of its authorization or organizational authority to the child.

### 17.3 Delegated Scope

A parent MAY delegate a bounded operation scope to a child only when the applicable authorization and organizational authority model permits that delegation.

The child MUST NOT broaden the delegated organization, operation, resource, purpose, duration or authority scope silently.

## 18. External Systems and Authority Preservation

### 18.1 External Authority

When an external system remains authoritative under `External Reference` or `Governed Replica`, a workflow MUST preserve that authority boundary.

Execution MUST NOT convert external data into `Native` Arvectum OS authority merely because the data was read, transformed or acted upon.

### 18.2 External Mutation

Before a consequential external mutation, the execution MUST determine where applicable:

- target external authority;
- operation identity;
- actor/service authorization;
- organizational authority;
- expected idempotency;
- current relevant external version or state token if available;
- failure and uncertainty behavior;
- reconciliation path.

### 18.3 External Inconsistency

If Arvectum OS canonical state and an external authority disagree, the workflow MUST apply the declared authority and conflict rules rather than choose based on convenience or data recency alone.

## 19. Failure, Partial Completion, Cancellation and Compensation

### 19.1 Explicit Failure

A failure that affects a consequential execution MUST be represented explicitly enough to determine:

- what failed;
- at which governed stage or operation;
- which effects may already have occurred;
- whether retry is safe;
- whether compensation or reconciliation is required;
- who or what owns the next action where applicable.

### 19.2 Fail Closed

Execution MUST fail closed when continuing would risk:

- unauthorized access or mutation;
- invalid organizational authority;
- cross-organization data leakage;
- prohibited data processing;
- ambiguous authoritative input;
- silent canonical lineage conflict;
- duplicate consequential external effect;
- bypass of required approval.

### 19.3 Cancellation

Cancellation MUST NOT erase already committed canonical history or external effects.

Cancellation semantics MUST distinguish stopping future work from reversing completed effects.

### 19.4 Compensation

Compensation is a new governed action intended to counteract or remediate a previous effect. It is not mutation of history.

A compensation execution MUST link to the effect it compensates and preserve its own authorization, authority, inputs, outcome and evidence.

### 19.5 Partial Completion

If only part of a multi-effect workflow succeeds, the terminal or waiting state MUST expose the partial completion rather than report unqualified success.

## 20. Outputs and Artifacts

### 20.1 Output Classification

Execution outputs MUST be classified according to their governed role, including as applicable:

- transient output;
- Canonical Record or candidate canonical mutation;
- Governed Organizational Asset;
- external-system result/reference;
- artifact requiring retention;
- operational telemetry.

### 20.2 No Automatic Promotion

An execution output MUST NOT become authoritative knowledge, organizational memory, approved standard or other governed asset merely because the workflow completed successfully.

Promotion belongs to the applicable governance or later learning lifecycle.

### 20.3 Sensitive Outputs

Sensitive data MUST NOT be copied into execution history merely for convenience when governed references or minimized evidence are sufficient.

## 21. Workflow Evolution and In-flight Executions

### 21.1 No Silent Mid-flight Upgrade

An in-flight execution MUST NOT silently switch to a new Workflow version when doing so could change consequential semantics.

### 21.2 Migration

Migration of an in-flight execution to another Workflow version MUST be explicit when the change is governance-significant.

Migration SHOULD identify:

- source Workflow version;
- target Workflow version;
- reason;
- compatibility or state-mapping rule;
- required revalidation or approval;
- actor/authority responsible for migration;
- resulting execution state.

### 21.3 Security or Policy Emergency

A newly effective security, privacy, legal or governance rule MAY require suspension, revalidation, migration or cancellation of in-flight executions even when they were validly started under an older Workflow version.

Historical evidence MUST remain intact.

## 22. Reconstructability and Proportional Evidence

### 22.1 Reconstruction Objective

For a consequential execution, Arvectum OS MUST preserve enough governed evidence to answer, where applicable:

- who or what initiated it;
- for which Organization;
- which Workflow version applied;
- which exact governed input versions were relied upon;
- which policies, standards, contracts and approvals applied;
- which actor authorization and organizational authority were relied upon;
- which deterministic and AI components materially influenced the result;
- which operations were attempted;
- which canonical or external effects were produced;
- which failures, retries, resumptions or compensations occurred;
- what terminal or current governed state resulted.

### 22.2 Proportionality

Not every technical step becomes canonical history.

Evidence depth MUST be proportionate to consequence, reversibility, sensitivity, threat, external commitment, legal/contractual obligations and organizational value.

Low-risk bounded experiments MAY retain lighter governed evidence when scope, owner, retention and exit path are explicit.

### 22.3 Secret and Sensitive Data Minimization

Reconstructability MUST NOT be implemented by indiscriminately retaining secrets, raw credentials, unnecessary personal data, full model prompts, complete external payloads or other sensitive material.

A reference, digest, immutable artifact identity, policy decision reference or minimized evidence MAY be sufficient when it preserves the required governed meaning.

## 23. Portability and Technology Independence

A portable representation of governed execution history MUST preserve semantic meaning sufficient for the declared portability scope, including where applicable:

- Execution Identity;
- Execution Context versions;
- Workflow identity/version references;
- Organization scope;
- actor and authority references;
- pinned governed input versions;
- canonical effects;
- parent/child and causation relationships;
- terminal state;
- required approval and policy references;
- artifact references that are legally and contractually portable.

Portability does not require exporting runtime internals, reusable secrets, proprietary model weights or vendor-specific credentials when those are not organizational assets or are not legally/technically exportable.

## 24. Product and Platform Boundary

### 24.1 Domain Workflows Remain Product-owned by Default

Tender, CRM, finance, legal, marketing and other domain workflows remain product-specific unless a separate governed decision establishes a domain-neutral platform responsibility.

This RFC defines the execution semantics those workflows may rely upon; it does not move their business meaning into the platform.

### 24.2 Product Contract Interaction

Where a product relies on shared platform execution behavior, the applicable Product Contract requirements are governed by Accepted architecture and, once accepted, RFC-0004.

Until RFC-0004 is Accepted, this RFC MUST NOT use the current proposal to create new binding Product Contract obligations beyond RFC-0001.

### 24.3 No Accidental Platform Capability

A reusable workflow mechanism does not become an `Active` Platform Capability merely because more than one product uses it.

Capability lifecycle remains governed by RFC-0001 and applicable later decisions.

## 25. Minimal Reference Execution Contract

A conforming governed execution representation SHOULD be able to expose, directly or by governed immutable reference, the following conceptual fields where applicable:

```text
execution_subject_id
execution_version_id
organization_scope
execution_state
workflow_subject_id
workflow_version_id
initiating_actor
represented_actor_or_delegation
parent_execution_id / causation
operation_or_stage
pinned_input_versions
external_authority_evidence
policy_and_standard_versions
authorization_decision_refs
organizational_authority_refs
approval_refs
validation_refs
component_versions
canonical_effect_refs
external_effect_refs
artifact_refs
failure_or_uncertainty_state
retention/classification refs
created_at / transitioned_at
```

This is a semantic contract, not a required physical schema.

## 26. Conformance

Conformance to this RFC is scoped.

A system or capability MAY claim conformance only for a declared subject, environment and maturity scope.

### 26.1 Required Fitness Tests

A conforming implementation within its declared scope MUST demonstrate that:

1. consequential canonical mutation cannot occur without an Execution Context and authorized operation;
2. one execution has stable identity and immutable governance-significant Execution Context versions;
3. historical executions remain pinned to the exact Workflow version and material governed input versions relied upon;
4. authorization does not substitute for organizational authority;
5. required approval cannot be bypassed by a technically authorized service or AI component;
6. organization scope does not silently broaden during parent/child execution, retry or resumption;
7. retries do not silently duplicate consequential canonical or external effects;
8. unknown external outcome enters explicit uncertainty/reconciliation behavior rather than unsafe blind retry;
9. canonical conflicts do not overwrite newer state silently;
10. cancellation does not erase committed history;
11. compensation creates linked governed action rather than mutating historical effect;
12. in-flight execution does not silently adopt a materially different Workflow version;
13. sensitive evidence is minimized while retaining required reconstructability;
14. AI output remains transient unless explicitly promoted through governed execution;
15. terminal execution history remains sealed and reconstructable according to applicable retention constraints.

### 26.2 Non-conformance Examples

The following are non-conforming within relevant scope:

- direct canonical database updates outside Governed Execution;
- an AI agent invoking consequential mutation solely because it possesses an API credential;
- retrying an uncertain non-idempotent payment or external commitment without duplicate protection or reconciliation;
- changing an execution's recorded Workflow version after the fact;
- storing only a mutable `approved=true` flag with no attributable approval evidence for consequential action;
- resuming a long-running workflow with expired authority without revalidation where required;
- reporting success after only some required consequential effects completed without exposing partial completion;
- using a relationship or product registration as implicit authorization;
- collapsing multiple organizations into one execution authority scope without explicit governed cross-organization rules.

## 27. Migration and Compatibility

### 27.1 Existing Workflows

Existing product-local or provisional workflows MAY continue during migration when they are bounded, reversible and do not violate Accepted security, privacy, authority, data-integrity or contractual requirements.

Migration SHOULD prioritize flows that perform consequential canonical or external mutations.

### 27.2 No Big-bang Requirement

This RFC does not require every script, task or background job to become a fully modeled Workflow immediately.

Non-significant technical jobs MAY remain implementation-local when they do not carry governed organizational meaning or consequential effects.

### 27.3 Compatibility Principle

A conforming implementation MAY change orchestration engines, queues, worker frameworks, databases, model providers or service boundaries without changing the governed Workflow and Execution semantics visible at the architectural contract level.

## 28. Consequences

### 28.1 Positive

This RFC makes consequential execution explicit and reconstructable while preserving implementation freedom.

It prevents technical permissions, AI capabilities or incidental runtime behavior from becoming undeclared organizational authority.

It supports safe retry, recovery, compensation and evolution without requiring a universal distributed transaction system.

It keeps domain business workflows product-owned while providing shared platform semantics for governed execution.

### 28.2 Costs

Consequential workflows require versioned definitions, execution identity, gate evaluation and evidence retention.

Some current ad-hoc scripts or direct state mutations may require migration.

Long-running workflows require explicit resumption and version-migration behavior.

External systems with weak idempotency or poor versioning may require reconciliation logic.

These costs are accepted only where proportionate to consequence and organizational value.

## 29. Risks and Mitigations

### Risk: workflow governance becomes bureaucratic

Mitigation: only operationally significant or consequential work requires full governed semantics; lightweight product-local experiments remain permitted within Accepted boundaries.

### Risk: execution history becomes an indiscriminate data lake

Mitigation: proportional evidence, minimization, classification, retention and governed references are explicit requirements.

### Risk: workflow engine technology leaks into architecture

Mitigation: the RFC defines semantic contracts and leaves orchestration technology to ADRs and implementation.

### Risk: AI is treated as an approver because it can call tools

Mitigation: organizational authority and approval remain independent governed gates.

### Risk: retries duplicate external commitments

Mitigation: explicit idempotency classification, uncertainty state and reconciliation requirements.

### Risk: workflow updates corrupt in-flight execution meaning

Mitigation: exact Workflow version pinning and explicit migration.

## 30. Follow-up Decisions

This RFC intentionally leaves the following to later work:

1. **RFC-0006 — Event, Provenance and Observability Model**
   - Event taxonomy;
   - causal/provenance representation;
   - event delivery and durability semantics;
   - observability boundaries;
   - operational evidence relationship to canonical Event history.

2. **RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle**
   - observations;
   - organizational memory;
   - validated knowledge;
   - improvement proposals;
   - governed promotion and learning.

3. **Subordinate ADRs and standards**
   - workflow/orchestration implementation technology;
   - persistence mapping;
   - transaction/outbox patterns where needed;
   - idempotency-key implementation;
   - timeout/retry defaults;
   - tracing and telemetry technology after RFC-0006;
   - reference implementation conventions.

## 31. Acceptance Criteria

RFC-0005 MAY be accepted only when:

- it remains compatible with Constitution `1.2.0`;
- it remains compatible with Accepted RFC-0001, RFC-0002 and RFC-0003;
- RFC-0004 status and any accepted changes have been re-checked for compatibility before the owner decision;
- domain-specific workflow semantics have not leaked into shared platform behavior;
- AI authority remains bounded by Accepted governance;
- security, privacy, isolation and data-governance gates cannot be bypassed by execution mechanics;
- workflow and execution versioning preserve reconstructability without requiring indiscriminate sensitive-data retention;
- retry, uncertainty, compensation and in-flight migration semantics are sufficiently defined to prevent silent consequential inconsistency;
- functional cross-review identifies no unresolved material conflict;
- explicit owner approval exists independently of any acceptance publication commit;
- the RFC Index and Acceptance Integrity evidence are synchronized during acceptance publication.

## 32. Approval Record

Current status: `Proposed`.

No owner approval is recorded by this proposal.

Acceptance requires an independent owner-approved decision record that already exists before the acceptance publication commit, consistent with the RFC Index Acceptance Integrity rules.
