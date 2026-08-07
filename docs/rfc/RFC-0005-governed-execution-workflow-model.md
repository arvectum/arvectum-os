# RFC-0005: Governed Execution and Workflow Model

Status: `Proposed`
Version: `0.2.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`
Forward-compatible with: `RFC-0004 v0.3.0` (`Proposed`, non-normative)
Supersedes: `RFC-0005 v0.1.0` working proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`

## 1. Executive Summary

Arvectum OS requires consequential changes to canonical organizational state to occur through **Governed Execution**. RFC-0001 establishes that rule. RFC-0002 defines Execution Context as a Canonical Record specialization with stable execution identity and immutable governance-significant versions. RFC-0003 separates identity, authentication, authorization, Organizational Authority and data governance so technical ability never becomes authority by implication.

This RFC defines the domain-neutral execution and workflow model needed to make those requirements operational without choosing a workflow engine, scheduler, queue, database, programming language, AI provider, BPMN runtime or service topology.

The model is based on eight rules:

1. **A Workflow defines governed executable intent; an Execution Context records one governed attempt to carry that intent out.**
2. **Every consequential canonical mutation MUST occur inside an Execution Context through an authorized operation.**
3. **Execution MUST pin the effective versions of changeable governed inputs and controls that materially determine a consequential result.**
4. **Authentication, authorization, Organizational Authority, data-governance permission, validation and approval are distinct gates.**
5. **AI may analyze, generate, recommend, validate and execute explicitly bounded pre-authorized behavior, but it MUST NOT become the independent final consequential approver or source of Organizational Authority.**
6. **Retries, resumptions, compensation and replay MUST preserve causation and MUST NOT silently duplicate consequential effects.**
7. **Failure and uncertainty MUST be explicit and must fail closed where continuing could violate authority, security, privacy, tenant isolation or canonical integrity.**
8. **Platform workflow semantics remain domain-neutral; product-specific business-process meaning remains product-owned unless separately promoted through governance.**

This RFC defines Workflow identity/versioning, Execution Context lifecycle, operation and side-effect semantics, input version pinning, authority and approval gates, canonical mutation rules, deterministic and AI-mediated execution, retries/idempotency, waiting/resumption, parent-child execution, external-system interaction, failure/compensation, workflow evolution, evidence, portability and conformance.

Complete Event taxonomy, delivery semantics, provenance representation and observability infrastructure remain RFC-0006 scope. Memory, knowledge and governed-learning promotion remain RFC-0007 scope.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 `1.0.0`, RFC-0002 `1.0.0` and RFC-0003 `1.0.0` without changing their architectural laws.

The most relevant constitutional requirements are:

- repeatable and operationally significant processes should be versioned workflows;
- significant governed objects are versioned;
- consequential actions are observable and reconstructable proportionate to consequence;
- approved assets and consequential operations are reproducible to the extent permitted by declared inputs and dependencies;
- only approved governance mechanisms authorize consequential changes;
- AI is an execution means, not an authority source;
- security, privacy, least privilege, isolation, minimization, retention, deletion and auditability are structural requirements;
- bounded reversible experiments are permitted;
- technology may change without loss of organizational meaning.

RFC-0001 additionally requires consequential canonical change through Governed Execution and requires the applicable Execution Context to identify, where relevant, organization, actor, authority, Product Contract, workflow/version, input versions, external authority, policies/standards, knowledge/memory, deterministic and AI components, validation/approval requirements, outputs/artifacts, events, causation, classification, retention and reproducibility constraints.

RFC-0002 establishes that Execution Context is a Canonical Record specialization, one execution has a stable Execution Identity, governance-significant transitions are immutable versions, terminal execution is sealed, and consequential reliance on changeable governed state pins exact Version Identities.

RFC-0003 requires deny-by-default authorization, explicit Organization scope, separation of technical authorization from Organizational Authority, purpose-aware data governance, cross-organization isolation and failure behavior that does not silently broaden access.

Where this RFC conflicts with the Constitution or an earlier Accepted RFC, the higher-authority source prevails.

### 2.1 RFC-0004 Status Boundary

RFC-0004 `0.3.0` remains `Proposed` and has no normative force at the time of this proposal.

RFC-0005 is designed to be forward-compatible with RFC-0004 Product Contract concepts, especially operation declarations, canonical reads/writes, security/authority requirements, shared events and artifacts. It MUST NOT use the current RFC-0004 proposal to create binding requirements beyond Accepted RFC-0001.

If RFC-0004 becomes Accepted with materially different execution-boundary semantics, RFC-0005 MUST be re-checked before owner decision.

## 3. Scope

This RFC defines domain-neutral architecture for:

- Workflow identity, immutable versions and effective-version resolution;
- Execution Context lifecycle and governance-significant transitions;
- actor, trigger and Organization scope;
- operations and side-effect classes;
- consequential input resolution and version pinning;
- authentication, authorization, Organizational Authority, data-governance, validation and approval gates;
- canonical mutations and commit boundaries;
- deterministic and AI-mediated execution;
- idempotency, retries and uncertain external outcomes;
- waiting, suspension, resumption, deadlines and timeouts;
- parent and child executions;
- external-system interaction while preserving authority modes;
- partial completion, cancellation and compensation;
- execution outputs and artifact classification;
- workflow evolution and in-flight migration;
- reconstructability and proportional evidence;
- semantic portability;
- scoped conformance.

## 4. Non-goals

This RFC does not define:

- a workflow language, BPMN profile or orchestration engine;
- scheduler, queue, worker framework or message broker;
- physical database schema or service topology;
- complete Event taxonomy, delivery guarantees, tracing protocol or observability backend;
- complete provenance graph schema;
- Product Contract schemas or extension registration;
- memory, knowledge or learning promotion;
- domain-specific workflows, roles, approval thresholds or business rules;
- customer-facing SLA/support commitments;
- universal distributed transactions;
- automatic promotion of workflow implementations into Platform Capabilities.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Model

### 6.1 Workflow

A **Workflow** is a versioned governed definition of how a repeatable or operationally significant class of work is performed.

A Workflow MAY declare:

- entry conditions;
- permitted initiators by governed reference;
- required inputs and resolution rules;
- operations or stages;
- decision points;
- validations and approvals;
- expected outputs;
- retry, timeout and compensation behavior;
- completion criteria;
- policies, standards and contracts;
- permitted deterministic and AI-mediated components;
- proportional evidence requirements.

A Workflow MUST NOT derive Organizational Authority from technical execution capability.

### 6.2 Execution Context

An **Execution Context** is the RFC-0002 Canonical Record specialization representing one execution instance.

One execution has:

- one stable Execution Identity;
- immutable Execution Context versions for governance-significant transitions;
- one declared Organization scope unless explicitly governed otherwise;
- an initiating actor or governed trigger;
- an effective Workflow version where applicable;
- the governed inputs and controls necessary to explain the execution within its declared scope.

### 6.3 Workflow and Execution Are Distinct

Workflow and Execution Context MUST have distinct Subject Identities.

Changing a Workflow MUST NOT mutate historical executions.

Consequential execution MUST remain attributable to the exact Workflow version that governed it.

### 6.4 Governed Execution

**Governed Execution** is performance of work inside an Execution Context under applicable authorization, Organizational Authority, policy, validation, approval, data-governance and evidence requirements.

Governed Execution is a semantic architecture requirement and does not require one centralized runtime.

## 7. Workflow Identity and Versioning

A governed Workflow MUST have:

- stable Workflow Subject Identity;
- immutable Workflow Version Identity for every admitted version;
- semantic type/name;
- accountable architectural owner;
- Organization, platform or product scope;
- lifecycle status;
- creation/version provenance.

An admitted Workflow version MUST NOT be mutated. A behavioral change creates a new immutable version under the same Workflow Subject Identity when the workflow remains the same semantic lineage.

An execution MUST pin the exact effective Workflow Version Identity before consequential behavior relies on it.

A Workflow MAY use a lifecycle such as:

```text
Draft → Approved → Deprecated → Retired
```

Additional states MAY exist in subordinate governance. A `Draft` workflow MUST NOT be the sole basis for consequential production behavior except inside an explicitly bounded governed experiment or exception. A `Retired` workflow MUST NOT start new ordinary executions.

## 8. Execution Lifecycle

A conforming implementation MUST be able to represent at least the following semantic conditions, even if exact labels differ:

```text
Created
  ↓
Ready / Awaiting Gate
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

A transition is governance-significant when it materially affects authority, canonical state, external commitments, approval state, recovery obligations, legal/financial position, security/privacy posture or reconstruction.

Each governance-significant transition MUST create a new immutable Execution Context version or equivalent RFC-0002-conforming canonical version.

High-frequency technical worker state with no governed significance MAY remain operational telemetry rather than canonical history.

A terminal Execution Context version MUST be sealed. Correction, reversal, compensation or dispute MUST create additional linked governed records/executions rather than mutate terminal history.

## 9. Initiation, Actor and Organization Scope

A governed execution MUST identify either an initiating Actor under RFC-0003 or a governed trigger whose authority to initiate can be reconstructed.

Scheduled, event-driven and machine-initiated execution MUST remain attributable to the principal, service, policy or prior governed execution that authorized the trigger path.

Before consequential work begins, the execution MUST resolve its governing Organization scope. Cross-organization execution MUST preserve each Organization's authority and data-governance context and MUST NOT collapse them into one ambient authority scope.

Acting-on-behalf-of or delegated execution MUST preserve the actual actor, represented principal where applicable, delegation/authority reference, Organization scope and relevant assurance context.

## 10. Operation and Side-effect Model

An **Operation** is a stable semantic action performed against governed state, an external system or a controlled side-effect boundary.

An operation SHOULD declare, where relevant:

- stable semantic identity/name;
- input/output types;
- target resource/subject semantics;
- side-effect class;
- idempotency expectations;
- authorization and Organizational Authority requirements;
- validation/approval gates;
- data-governance constraints;
- timeout/failure behavior;
- compensation/reversal support.

A conforming implementation MUST distinguish at least:

- `ReadOnly` — no intended mutation;
- `Transient` — temporary non-authoritative effect;
- `CanonicalMutation` — changes canonical Arvectum OS state;
- `ExternalMutation` — changes state in an external consequential system;
- `Commitment` — creates or materially affects legal, financial, security, contractual, reputational or equivalent organizational commitment.

One operation MAY belong to multiple classes. Controls MUST be proportionate to consequence, sensitivity, reversibility and external impact.

## 11. Input Resolution and Version Pinning

A changeable governed Subject Identity MUST resolve to an exact effective Version Identity before consequential behavior relies on it. The execution MUST preserve the exact version used.

Where they materially determine a consequential result, execution MUST pin or immutably reference effective versions of applicable:

- Workflow;
- Product Contract where applicable under Accepted architecture;
- Canonical Records and relationships;
- policies and standards;
- validators and schemas;
- governed knowledge/memory assets when later RFCs define their use;
- model/prompt configuration where material to reproducibility and lawful retention;
- external authoritative source state or retrieval evidence where exact version pinning is unavailable.

Dynamic resolution is permitted, but material resolved versions or external-state evidence MUST be captured at the point of reliance.

If a required authoritative version cannot be resolved unambiguously, consequential execution MUST NOT silently choose one. It MUST stop/wait, use an explicitly governed fallback, or continue only in a bounded non-consequential mode that cannot commit the unresolved result as authoritative state.

## 12. Authorization, Authority, Validation and Approval

A workflow MUST keep distinct where applicable:

1. authentication/actor assurance;
2. technical authorization;
3. Organizational Authority;
4. data-governance permission;
5. validation;
6. consequential approval.

Passing one gate MUST NOT imply passing another.

A gate MUST be evaluated where the information needed for that decision is sufficiently known and MUST be re-evaluated when a material change invalidates the earlier decision assumptions.

Where consequential approval is required, execution evidence MUST identify what was approved, by which authorized decision authority or governed approval mechanism, under which scope, which material version/result was approved, and applicable effective/expiry/supersession conditions.

Approval SHOULD be attributable governed evidence rather than an unaudited mutable boolean.

**AI MUST NOT serve as the independent final consequential approver or source of Organizational Authority.** AI MAY generate recommendations, perform bounded validation, summarize evidence or execute actions that have already been authorized under an approved workflow and applicable authority. Final consequential approval remains attributable to the authorized governance mechanism and decision authority defined by Accepted rules.

## 13. Canonical Mutation

Every consequential change to canonical state managed by Arvectum OS MUST occur through an Execution Context and authorized operation.

Direct database writes, administrative scripts, internal imports or AI tool calls MUST NOT bypass this rule merely because they can technically mutate storage.

Canonical mutation MUST obey RFC-0002 immutability: changing governed state creates a new canonical version or new governed record as appropriate.

A multi-effect execution MUST define a commit boundary appropriate to its consistency needs. A universal distributed ACID transaction is not required.

If atomic completion cannot be guaranteed, partial completion MUST be exposed explicitly and recovery, compensation or reconciliation behavior MUST be defined proportionate to consequence.

A canonical mutation MUST detect material conflicts when concurrent state change could invalidate the result. A conflict MUST NOT silently overwrite newer canonical state.

## 14. Deterministic and AI-mediated Execution

Consequential execution SHOULD preserve the identity and version/configuration of deterministic and AI components when they materially influence the result.

AI MAY:

- analyze;
- classify;
- extract;
- generate;
- recommend;
- validate within an explicitly bounded rule;
- execute pre-authorized bounded operations when the governing workflow permits.

AI MUST NOT independently:

- grant authorization;
- create Organizational Authority;
- act as final consequential approver;
- alter approved policies, standards or Workflow definitions silently;
- promote transient output into validated knowledge or authoritative canonical state outside Governed Execution;
- broaden Organization scope, retention or cross-organization sharing.

AI output is transient by default until a governed workflow explicitly validates and promotes it to the appropriate governed state.

A workflow using non-deterministic components MUST NOT claim byte-for-byte reproducibility unless it can provide it. It MUST instead retain sufficient declared inputs, versions, configurations and constraints to reproduce an equivalent result where feasible or explain why equivalence cannot be achieved.

## 15. Idempotency, Retry and Uncertain Outcomes

A consequential operation that may be retried MUST declare whether it is:

- naturally idempotent;
- idempotent under an execution/idempotency key;
- non-idempotent and therefore requires duplicate protection or reconciliation.

Retry MUST NOT silently duplicate canonical mutations, external commitments, approvals, payments or equivalent effects.

Retry attempts MUST preserve causation to the original operation attempt.

If the system cannot determine whether a consequential external operation succeeded, it MUST enter an explicit uncertain/reconciliation-required condition rather than blindly retrying a potentially non-idempotent effect.

## 16. Waiting, Suspension, Resumption and Time

Execution MAY wait for human approval, external response, scheduled time, condition/event, missing authoritative input, retry window or other governed dependency.

A waiting execution MUST preserve enough state to resume under the correct Organization, Workflow version and authority context.

Resumption MUST re-evaluate expired or materially changed gates where policy, authority, classification, purpose, target state or other governing conditions have changed.

Deadlines and timeouts that materially affect organizational outcome MUST be governed workflow/execution semantics, not hidden only in worker infrastructure.

## 17. Parent and Child Executions

A Workflow MAY invoke child executions.

A consequential child SHOULD have its own Execution Identity when it has independent authority, failure, retry, retention, portability, audit or lifecycle significance.

A child execution MUST preserve causation to its parent.

Parent execution MUST NOT automatically confer all authorization or Organizational Authority to the child. Delegated scope MUST remain bounded by Organization, operation, resource, purpose, duration and authority.

## 18. External Systems and Authority Preservation

When an external system remains authoritative under `External Reference` or `Governed Replica`, execution MUST preserve that authority boundary.

Reading, transforming or acting on external data MUST NOT silently convert it into `Native` Arvectum OS authority.

Before consequential external mutation, execution MUST determine where applicable:

- target external authority;
- operation identity;
- actor/service authorization;
- Organizational Authority;
- idempotency expectation;
- relevant external version/state token if available;
- failure/uncertainty behavior;
- reconciliation path.

If Arvectum OS state and external authority disagree, the declared authority/conflict rule MUST be applied rather than choosing based on convenience or recency alone.

## 19. Failure, Cancellation, Compensation and Partial Completion

Consequential failure MUST be explicit enough to determine what failed, which effects may already have occurred, whether retry is safe, whether compensation/reconciliation is required, and who/what owns the next action where applicable.

Execution MUST fail closed when continuing would risk:

- unauthorized access/mutation;
- invalid Organizational Authority;
- cross-organization leakage;
- prohibited data processing;
- ambiguous authoritative input;
- silent canonical lineage conflict;
- duplicate consequential external effect;
- bypass of required approval.

Cancellation stops future work but MUST NOT erase committed history or external effects.

Compensation is a new governed action intended to counteract or remediate a previous effect. A compensation execution MUST link to the effect it compensates and preserve its own authorization, authority, inputs and outcome.

If only part of a multi-effect workflow succeeds, the execution MUST expose partial completion rather than report unqualified success.

## 20. Outputs and Artifacts

Execution outputs MUST be classified according to governed role where applicable:

- transient output;
- Canonical Record or candidate mutation;
- Governed Organizational Asset;
- external-system result/reference;
- artifact requiring retention;
- operational telemetry.

Workflow success MUST NOT automatically promote output into authoritative knowledge, organizational memory, approved standards or another governed asset.

Sensitive data MUST NOT be copied into execution history merely for convenience when governed references or minimized evidence are sufficient.

## 21. Workflow Evolution and In-flight Migration

An in-flight execution MUST NOT silently switch to a new Workflow version when doing so could change consequential semantics.

Governance-significant migration to another Workflow version MUST be explicit and SHOULD identify source version, target version, reason, compatibility/state mapping, required revalidation/approval, responsible actor/authority and resulting execution state.

A newly effective security, privacy, legal or governance requirement MAY require suspension, revalidation, migration or cancellation of in-flight work. Historical evidence remains intact.

## 22. Reconstructability and Proportional Evidence

For a consequential execution, Arvectum OS MUST preserve enough governed evidence to answer where applicable:

- who/what initiated it;
- for which Organization;
- which Workflow version applied;
- which exact governed input versions were relied upon;
- which policies, standards, contracts and approvals applied;
- which authorization and Organizational Authority were relied upon;
- which deterministic and AI components materially influenced the result;
- which operations were attempted;
- which canonical/external effects resulted;
- which failures, retries, resumptions or compensations occurred;
- what current/terminal governed state resulted.

Evidence depth MUST remain proportionate to consequence, reversibility, sensitivity, threat, external commitments, legal/contractual obligations and organizational value.

Reconstructability MUST NOT be implemented through indiscriminate retention of secrets, raw credentials, unnecessary personal data, full prompts, complete external payloads or other sensitive material. Governed references, hashes/digests, immutable artifact identities and minimized evidence MAY satisfy the requirement where sufficient.

## 23. Portability and Technology Independence

Portable governed execution history MUST preserve semantic meaning sufficient for the declared scope, including where applicable:

- Execution Identity and versions;
- Workflow identity/version;
- Organization scope;
- actor/authority references;
- pinned governed inputs;
- canonical effects;
- parent/child causation;
- terminal state;
- approval/policy references;
- legally and contractually portable artifact references.

Portability does not require exporting runtime internals, reusable secrets, proprietary model weights or non-exportable vendor credentials.

Workflow/orchestration technology MAY change without changing the governed semantics defined by this RFC.

## 24. Product and Platform Boundary

Tender, CRM, finance, legal, marketing and other domain workflows remain product-owned by default.

RFC-0005 provides shared execution semantics; it does not move domain business meaning into the platform.

A reusable workflow mechanism does not become an `Active` Platform Capability merely because multiple products use it. Capability lifecycle remains governed by RFC-0001.

Where a product relies on shared platform execution behavior, Product Contract requirements are governed by Accepted architecture and, once accepted, RFC-0004.

## 25. Minimal Semantic Execution Contract

A conforming representation SHOULD be able to expose, directly or by governed immutable reference, where applicable:

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

This is a semantic contract, not a physical schema requirement.

## 26. Conformance

Conformance is scoped by subject, environment and maturity.

A conforming implementation within its declared scope MUST demonstrate that:

1. consequential canonical mutation cannot occur without an Execution Context and authorized operation;
2. execution identity is stable and governance-significant versions are immutable;
3. historical executions retain exact Workflow and material input versions;
4. authorization does not substitute for Organizational Authority;
5. required consequential approval cannot be bypassed by a technically authorized service or AI component;
6. AI cannot act as independent final consequential approver;
7. Organization scope does not silently broaden during child execution, retry or resumption;
8. retries do not silently duplicate consequential effects;
9. unknown external outcome enters uncertainty/reconciliation instead of unsafe blind retry;
10. canonical conflicts do not silently overwrite newer state;
11. cancellation does not erase committed history;
12. compensation creates linked governed action rather than mutating history;
13. in-flight execution does not silently adopt a materially different Workflow version;
14. sensitive evidence is minimized while required reconstructability is preserved;
15. AI output remains transient unless explicitly promoted by governed execution;
16. terminal execution history remains sealed according to applicable retention rules.

Examples of non-conformance include direct canonical database writes outside Governed Execution, AI mutation based solely on possession of a credential, blind retry of uncertain non-idempotent commitments, changing historical Workflow references, unaudited mutable approval flags for consequential action, resuming with expired authority without required revalidation, and claiming success while hiding material partial completion.

## 27. Migration and Compatibility

Existing product-local or provisional workflows MAY continue during migration when bounded, reversible and compatible with Accepted security, privacy, authority, data-integrity and contractual requirements.

Migration SHOULD prioritize flows that perform consequential canonical or external mutation.

This RFC does not require every script or background job to become a fully modeled Workflow immediately. Non-significant technical jobs MAY remain implementation-local when they do not carry governed organizational meaning or consequential effects.

No big-bang migration is required.

## 28. Consequences

### 28.1 Positive

- consequential execution becomes explicit and reconstructable;
- technical permission, AI capability and runtime convenience cannot silently become Organizational Authority;
- retries and recovery are safer;
- compensation and partial completion are modeled without rewriting history;
- domain workflows remain product-owned;
- orchestration technology remains replaceable.

### 28.2 Costs

- consequential workflows require versioned definitions, execution identity, gates and evidence;
- ad-hoc direct mutation paths may require migration;
- long-running workflows require explicit resumption/migration rules;
- weakly idempotent external systems may need reconciliation logic.

These costs are required only where proportionate to consequence and organizational value.

## 29. Risks and Mitigations

### Workflow governance becomes bureaucracy

Mitigation: full governed semantics apply to operationally significant or consequential work; bounded reversible product experiments remain possible.

### Execution history becomes a sensitive-data lake

Mitigation: proportional evidence, minimization, classification and governed references are mandatory.

### Runtime technology leaks into architecture

Mitigation: RFC-0005 defines semantic contracts only; concrete engines belong to ADRs/implementation.

### AI is mistaken for approval authority

Mitigation: AI cannot independently grant authority or act as final consequential approver.

### Retry duplicates commitments

Mitigation: explicit idempotency classification, uncertainty state and reconciliation.

### Workflow updates corrupt in-flight meaning

Mitigation: exact version pinning and explicit migration.

## 30. Follow-up Decisions

### RFC-0006 — Event, Provenance and Observability Model

Expected scope:

- Event taxonomy;
- causation/provenance representation;
- event delivery/durability semantics;
- operational telemetry versus canonical Event history;
- observability boundaries.

### RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle

Expected scope:

- observations;
- organizational memory;
- validated knowledge;
- improvement proposals;
- governed promotion and learning.

### Subordinate ADRs and standards

May later define:

- orchestration/runtime technology;
- persistence mapping;
- transaction/outbox patterns;
- idempotency-key implementation;
- retry/timeout defaults;
- tracing/telemetry implementation after RFC-0006;
- reference implementation conventions.

## 31. Functional Cross-Review

Functional role-based cross-review is recorded in:

- [`docs/reviews/RFC-0005-functional-cross-review.md`](../reviews/RFC-0005-functional-cross-review.md).

The review completed 3 iterations of a maximum 7 and stopped when no further material correction was identified for the current proposal lifecycle stage.

The material correction from Iteration 1 was incorporated into this `0.2.0` proposal: AI cannot serve as the independent final consequential approver or source of Organizational Authority.

## 32. Acceptance Criteria

RFC-0005 MAY be accepted only when:

- it remains compatible with Constitution `1.2.0`;
- it remains compatible with Accepted RFC-0001, RFC-0002 and RFC-0003;
- the then-current RFC-0004 state is re-checked before owner decision;
- domain-specific workflow semantics have not leaked into shared platform behavior;
- AI authority remains bounded by Accepted governance;
- security, privacy, isolation and data-governance gates cannot be bypassed by execution mechanics;
- retry, uncertainty, compensation and in-flight migration semantics remain sufficient to prevent silent consequential inconsistency;
- no unresolved material cross-review conflict remains;
- explicit owner approval exists independently of the acceptance publication commit;
- RFC Index and Acceptance Integrity evidence are synchronized during acceptance publication.

## 33. Approval Record

Current status: `Proposed`.

No owner approval is recorded by this proposal or its functional cross-review.

Acceptance requires an independent owner-approved decision record that already exists before the acceptance publication commit, consistent with RFC Index Acceptance Integrity rules.
