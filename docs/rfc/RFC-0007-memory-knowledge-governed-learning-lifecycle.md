# RFC-0007: Memory, Knowledge and Governed Learning Lifecycle

Status: `Proposed`
Version: `0.2.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`; `RFC-0005 v1.0.0`; `RFC-0006 v1.0.0`
Supersedes: `RFC-0007 v0.1.0` working draft
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Cross-review: `docs/reviews/RFC-0007-functional-cross-review.md`

## 1. Executive Summary

Arvectum OS exists to preserve and compound organizational intelligence without allowing transient outputs, remembered context, operational evidence or AI-generated interpretations to silently become organizational truth.

Accepted RFC-0001 establishes the Governed Learning Loop. RFC-0002 defines the Canonical Record and Governed Organizational Asset model. RFC-0003 constrains learning by identity, authorization, organizational authority, privacy, tenant sovereignty, minimization, retention and portability. RFC-0004 keeps product-domain knowledge and experiments behind explicit product/platform boundaries. RFC-0005 requires consequential use and mutation of governed state to occur through Governed Execution. RFC-0006 distinguishes canonical Events and provenance from telemetry and reserves promotion into Memory and Knowledge for this RFC.

This RFC defines the domain-neutral lifecycle by which observations and retained organizational memory may contribute to validated organizational understanding and approved improvements while preserving source authority, provenance, rights, organization boundaries, reviewability and human/governance control proportionate to consequence.

The model is based on fourteen rules:

1. **Observation, Memory, Knowledge and Proposal are distinct semantic roles.** Storage or retrieval does not collapse them into one another.
2. **Observation is not a sixth Kernel primitive and is not automatically truth.** It is an input to evaluation whose representation depends on significance and retention needs.
3. **Organizational Memory preserves governed context and experience; it does not automatically validate what it remembers.**
4. **Knowledge is validated organizational understanding.** Unvalidated material is a Knowledge Candidate or other proposal, not Knowledge.
5. **Significant Memory, Knowledge and learning-state objects use the RFC-0002 Canonical Record model.** This RFC introduces no new Kernel primitive.
6. **Promotion is explicit and reconstructable.** Observation or Memory becomes Knowledge only through declared validation, rights/classification review and approval appropriate to scope and consequence.
7. **AI may propose, summarize, cluster, retrieve, compare and perform bounded validation where authorized, but it does not obtain Organizational Authority or silently promote governed state.**
8. **Knowledge authority is scoped.** A Knowledge Record may be authoritative for an organization's adopted understanding without pretending to become authoritative for an external underlying fact.
9. **Contradiction creates review, supersession, retraction or a competing candidate—not silent overwrite.** Historical versions remain interpretable subject to lawful retention.
10. **Freshness, applicability and uncertainty are first-class.** Confidence, popularity, embedding similarity or repeated observation do not create authority.
11. **Cross-organization learning is denied by default.** Customer data, memory, evidence and knowledge do not become shared platform assets merely because Arvectum OS processed them.
12. **Product-domain learning remains product-owned by default.** Reuse does not automatically promote domain knowledge into the platform.
13. **Retrieval and indexing are projections, not canonical truth.** Vector stores, search indexes, caches, model context and embeddings may be rebuilt from governed sources.
14. **Governed learning closes the loop only through a new approved version or governed decision.** Production behavior never changes merely because a model, analyst or metric detected a pattern.

## 2. Constitutional and Architectural Basis

This RFC implements Constitution `1.2.0` and refines Accepted RFC-0001 through RFC-0006 without changing their architectural laws.

The most relevant constitutional requirements are:

- organizational intelligence is a compounding strategic asset;
- Memory consists of structured, versioned organizational records together with relationships, provenance and evolution;
- Knowledge is validated, versioned, reusable, explainable and technology-independent;
- authoritative organizational knowledge has exactly one canonical source within its declared scope;
- chats, model memory, local copies and generated artifacts are not independent sources of truth unless explicitly promoted and governed;
- governed organizational assets are explicitly designated rather than created by persistence alone;
- transient outputs do not automatically become permanent organizational assets;
- learning mechanisms may identify patterns and propose improvements but do not silently modify approved standards, policies, workflows or production behavior;
- organizational control, portability, security, privacy, isolation, minimization, retention, deletion and auditability are structural requirements;
- validated improvements should become reusable where doing so creates organizational value;
- evolution is deliberate, governed and traceable.

RFC-0001 establishes the learning sequence:

```text
Governed Execution
        ↓
Events and Outcomes
        ↓
Observations
        ↓
Organizational Memory
        ↓
Knowledge or Improvement Proposal
        ↓
Validation, Rights Review and Approval
        ↓
Approved Knowledge / Standard / Policy / Workflow Version
        ↓
Future Governed Execution
```

RFC-0002 establishes that significant governed objects use Canonical Records; Governed Organizational Asset designation is explicit; transient outputs do not automatically become Memory or validated Knowledge; and memory/knowledge promotion semantics belong to RFC-0007.

RFC-0003 requires deny-by-default access, least privilege, Organization scope, purpose limitation, minimization, retention/deletion, cross-organization isolation and explicit Organizational Authority. Learning cannot weaken those rules.

RFC-0004 requires product/platform dependencies involving shared platform history, canonical state, Events, artifacts or capabilities to be declared through Product Contracts where applicable. Product-domain knowledge remains product-owned by default.

RFC-0005 requires exact version attribution of material governed inputs in consequential execution and prohibits automatic promotion of outputs into authoritative Knowledge or organizational assets.

RFC-0006 establishes canonical Events, provenance and observability semantics and explicitly states that Events, telemetry and provenance do not automatically become Memory, validated Knowledge or Governed Organizational Assets.

Where this RFC conflicts with the Constitution or an earlier Accepted RFC, the higher-authority source prevails.

## 3. Scope

This RFC defines domain-neutral architecture for:

- Observation semantics in the learning lifecycle;
- Organizational Memory semantics and retention boundaries;
- Knowledge Candidate and Improvement Proposal semantics;
- validated Knowledge representation and lifecycle;
- promotion gates from observation/memory into governed Knowledge;
- validation, review, approval, rejection and withdrawal;
- provenance and evidence chains for learning;
- confidence, freshness, applicability, uncertainty and contradiction;
- supersession, retraction, retirement and historical interpretation;
- AI participation and authority boundaries;
- retrieval, search, RAG, embeddings and derived-index boundaries;
- product/platform and cross-organization learning boundaries;
- security, privacy, rights, classification, minimization, retention and deletion;
- portability and migration of Memory and Knowledge;
- learning-driven proposals for standards, policies, workflows and capabilities;
- scoped conformance and fitness criteria.

## 4. Non-goals

This RFC does not define:

- one vector database, graph database, document store, search engine or memory product;
- one embedding model, reranker, RAG framework, LLM, agent framework or model provider;
- physical table, index, chunk or storage schema;
- a universal ontology for every product/domain;
- product-specific knowledge taxonomies or business rules;
- a mandatory knowledge-validation methodology for every risk class;
- concrete retention periods or legal bases;
- a universal confidence-scoring formula;
- automatic model fine-tuning or training-data pipelines;
- autonomous production self-modification;
- Platform Capability activation, operational readiness, SLA or support commitments;
- legal title, copyright, database rights or contractual reuse rights beyond requiring those rights to be respected and governed.

These belong to subordinate ADRs, standards, catalogs, Product Contracts, legal agreements, product decisions or later architecture where necessary.

## 5. Normative Language

The capitalized terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** have the meaning defined by RFC-0001.

## 6. Core Semantic Model

### 6.1 Observation

An **Observation** is an observed operational result, pattern, assertion, signal or fact carried forward for evaluation in the Governed Learning Loop.

Observation is a semantic role, not a new Kernel primitive.

An Observation MAY originate from:

- one or more canonical Events;
- a Governed Execution outcome;
- a document or external authoritative source;
- user or expert input;
- product analytics;
- an investigation or review;
- an AI-generated inference;
- retained telemetry that is explicitly captured for learning or evidence;
- another governed source permitted by applicable rights and policy.

An Observation MUST preserve enough source/provenance context for its intended evaluation. It MUST NOT be treated as validated Knowledge merely because it is repeated, statistically common, generated confidently or stored durably.

A low-consequence Observation MAY remain a transient or product-local object. If the Observation is significant, reusable, evidentiary, relied upon for consequential learning or required for reconstruction, its governed representation MUST use the RFC-0002 Canonical Record model or a version-identifiable governed reference to an already canonical source.

### 6.2 Organizational Memory

**Organizational Memory** is the structured, versioned body of organizational records, relationships, provenance and evolution retained so that relevant organizational experience and context remain available beyond transient conversations, individual employees, model context windows or implementation technologies.

Memory answers primarily:

> What did the organization preserve about what was observed, decided, experienced or used?

Memory does not by itself answer:

> What has the organization validated as true or adopted as current understanding?

A Memory representation MUST preserve the epistemic and authority status of what it remembers. Remembering an assertion MUST NOT silently upgrade the assertion into validated Knowledge.

Memory MAY reference Events, Execution Contexts, documents, decisions, prior Knowledge versions, product records and external sources rather than duplicate their full content. Physical duplication SHOULD be minimized where governed references preserve meaning and availability.

### 6.3 Knowledge Candidate

A **Knowledge Candidate** is a governed proposal that a claim, model, rule, interpretation, pattern or reusable understanding should become Knowledge.

A Knowledge Candidate is explicitly **not Knowledge** until its applicable validation and approval gates succeed.

A material Knowledge Candidate SHOULD identify:

- candidate subject and scope;
- proposer/producer;
- Organization scope;
- supporting and contradicting Observations/evidence;
- provenance and source authority;
- proposed applicability conditions;
- uncertainty or confidence where useful;
- rights, classification and permitted-use constraints;
- proposed validation method;
- accountable owner;
- review/expiry condition where applicable.

### 6.4 Improvement Proposal

An **Improvement Proposal** proposes a change to an approved organizational asset or behavior such as a Standard, Policy, Workflow, Product Contract, validator, template, Platform Capability contract or product-specific operating rule.

An Improvement Proposal MAY be informed by Memory or Knowledge but MUST remain distinct from the Knowledge itself.

Approval of Knowledge does not automatically approve an operational change. A change to a governed Standard, Policy, Workflow, Product Contract or other consequential state MUST follow that artifact's applicable governance and Governed Execution rules.

### 6.5 Knowledge

**Knowledge** is validated organizational understanding within a declared scope.

A significant Knowledge item MUST be represented as a Canonical Record or Canonical Record lineage under RFC-0002.

A Knowledge Record MUST identify, directly or by governed reference and where applicable:

- stable Subject Identity;
- immutable Version Identity;
- semantic knowledge type/schema version;
- Organization scope;
- authority mode and authority scope;
- accountable architectural owner;
- proposition/understanding or governed content reference;
- applicability scope and known limitations;
- provenance and material evidence references;
- validation method and result;
- approval/decision reference where required;
- effective period or freshness/review conditions where applicable;
- classification, access, purpose and reuse constraints;
- supersession/retraction history;
- retention/deletion policy references where applicable.

Knowledge MUST be explainable to the extent required by its declared consequence and retained evidence.

### 6.6 Approved Reusable Knowledge and Governed Organizational Assets

A Knowledge Record does not become organization-wide or platform-wide reusable merely because it is validated.

When the organization designates Knowledge as authoritative, reusable, evidentiary or operationally significant, the applicable governed subject MUST receive explicit Governed Organizational Asset designation under RFC-0002.

Asset designation MUST NOT create legal rights, cross-organization rights or broader purpose permission that did not already exist.

## 7. Representation and Authority

### 7.1 No New Kernel Primitive

Observation, Memory, Knowledge Candidate, Improvement Proposal and Knowledge are semantic roles implemented above the existing RFC-0002 Kernel metamodel.

This RFC MUST NOT be interpreted as adding a sixth Kernel primitive or requiring one physical inheritance hierarchy.

### 7.2 Canonical Authority Scope

Every significant Knowledge Record MUST have exactly one canonical source within its declared knowledge scope.

A Knowledge Record MAY be `Native` when Arvectum OS is authoritative for the organization's adopted understanding, even when material evidence comes from an external authoritative system.

Such a `Native` Knowledge Record is authoritative for the organizational interpretation or adopted understanding only. It MUST NOT falsely claim that Arvectum OS has become authoritative for the underlying external fact where RFC-0001/RFC-0002 designate an external authority.

Where the Knowledge subject itself is externally authoritative, `External Reference` or `Governed Replica` MUST preserve the external authority contract.

### 7.3 Canonical Lineage

A change to current Knowledge MUST create a new immutable Knowledge version in one unambiguous RFC-0002 Canonical Lineage.

Draft candidates, simulations and competing hypotheses MAY exist outside the canonical Knowledge lineage. They MUST NOT create competing canonical heads.

### 7.4 Version-pinned Reliance

When Knowledge materially affects a consequential Governed Execution, the exact effective Knowledge Version Identity MUST be preserved in the Execution Context or equivalent governed evidence.

A search query, retrieval timestamp, embedding nearest-neighbor result or mutable alias MUST NOT substitute for the version identity materially relied upon.

## 8. Governed Learning Lifecycle

### 8.1 Lifecycle Overview

The normative learning lifecycle is:

```text
Events / Outcomes / Sources
           ↓
       Observation
           ↓
  Retained Organizational Memory
           ↓
 Knowledge Candidate or Improvement Proposal
           ↓
 Validation + Authority/Source Review
           ↓
 Rights + Classification + Purpose Review
           ↓
 Approval required for declared scope/consequence
           ↓
 ┌───────────────────────┬───────────────────────────┐
 ↓                       ↓
Knowledge Record     Approved change proposal path
 ↓                       ↓
Optional GOA         Standard/Policy/Workflow/etc.
designation          governed change process
           ↓
 Future Governed Execution
           ↓
 New Events / Outcomes / Observations
```

Not every Observation MUST be retained. Not every retained Memory item MUST become a candidate. Not every candidate MUST become Knowledge. Not every Knowledge item MUST become a Governed Organizational Asset or shared platform capability.

### 8.2 Promotion Preconditions

Before a Knowledge Candidate becomes Knowledge, the promotion process MUST evaluate, proportionate to consequence:

1. **identity and scope** — what claim or understanding is being validated, for which Organization/domain/use;
2. **provenance** — where it came from and what material transformations occurred;
3. **source authority** — what sources are authoritative for which underlying facts;
4. **evidence sufficiency** — what supporting and contradicting evidence exists;
5. **validation** — which declared method was applied and with what result;
6. **rights and permitted reuse** — whether the organization may retain, transform, rely on and reuse the material for the proposed purpose;
7. **classification and privacy** — whether access, minimization, retention, deletion and disclosure constraints are satisfied;
8. **Organization boundary** — whether any cross-organization use is separately authorized;
9. **conflict check** — whether current Knowledge or authoritative sources conflict with the candidate;
10. **applicability and freshness** — where, when and under what assumptions the candidate is valid;
11. **accountability** — who owns the resulting Knowledge;
12. **approval** — which Organizational Authority or approved governance mechanism authorizes admission for the declared scope where approval is required.

Failure of a required gate MUST produce rejection, withdrawal, quarantine, unresolved/review-required state or another explicit governed outcome. It MUST NOT silently promote the candidate.

### 8.3 Proportional Validation

Validation rigor MUST be proportionate to consequence, reversibility, uncertainty, source quality, data sensitivity, external impact and expected reuse.

Low-risk product-local knowledge MAY use bounded automated or reviewer validation.

High-consequence or broadly reusable Knowledge SHOULD require stronger independent evidence, explicit review and applicable decision authority.

This RFC does not mandate one validation checklist for every knowledge class.

### 8.4 Approval Is Not Validation

Validation evaluates whether evidence supports a candidate under a declared method.

Approval authorizes the organization to adopt, publish or rely on the resulting governed Knowledge within a declared scope.

The two MUST remain distinguishable when consequence requires Organizational Authority.

A technically successful validator MUST NOT be treated as an organizational approver merely because it returned a positive result.

### 8.5 Rejection and Withdrawal

A rejected or withdrawn candidate MUST NOT enter the Knowledge canonical lineage as though it had been accepted.

Material rejection rationale and evidence SHOULD be preserved when useful for avoiding repeated invalid proposals, subject to minimization and retention rules.

## 9. Knowledge Lifecycle After Promotion

### 9.1 Current

A Knowledge version is **Current** when it is the applicable effective version under its declared scope and has no triggered review, supersession or retraction condition.

### 9.2 Review Required

Knowledge MUST enter or resolve to **Review Required** when a declared review trigger occurs, such as:

- freshness deadline;
- material contradictory evidence;
- authoritative-source change;
- scope or assumption change;
- legal/contractual or classification change;
- validation-method invalidation;
- material incident or failed outcome suggesting the Knowledge may no longer be reliable.

`Review Required` does not automatically prove the Knowledge false. Consequential use MUST follow the declared fallback rule: continue with warning, require revalidation, use an earlier/alternative source, pause, or fail closed as appropriate.

### 9.3 Superseded

A new approved Knowledge version MAY supersede an earlier version.

Supersession MUST preserve the relationship between versions and their effective periods. Historical executions MUST remain attributable to the exact version they used.

### 9.4 Retracted

Knowledge MAY be **Retracted** when later evidence shows that continued reliance would materially misrepresent validated understanding or create unacceptable risk.

Retraction MUST create a new governed state/version or linked governed decision; it MUST NOT rewrite historical versions as if the earlier validation never occurred.

Where continuing use is unsafe or impermissible, retrieval and execution paths MUST enforce the retraction status according to applicable policy.

### 9.5 Retired

Knowledge MAY be **Retired** when it is no longer operationally relevant and no longer intended for active reuse.

Retirement does not require unlawful or unnecessary indefinite retention. Historical metadata and evidence are retained only to the extent permitted and required by applicable governance, privacy, legal, contractual and reconstruction needs.

## 10. Contradiction, Uncertainty and Confidence

### 10.1 Contradiction

Conflicting Observations or candidates MUST NOT silently overwrite one another.

When contradiction is material, the system MUST preserve enough provenance to identify the competing claims and trigger the applicable review, validation or reconciliation path.

### 10.2 Confidence

A confidence score or label MAY be stored when useful, but it MUST identify what produced the confidence and what the score means within the applicable schema/method.

Confidence MUST NOT substitute for:

- source authority;
- validation;
- Organizational Authority;
- applicability;
- rights;
- freshness;
- approval.

LLM probability, model confidence, retrieval similarity, frequency of mention and user popularity MUST NOT independently create Knowledge authority.

### 10.3 Known Gaps and Limitations

Knowledge SHOULD expose known material gaps, limitations, assumptions and uncertainty where omission would mislead consequential use.

The absence of known contradictory evidence MUST NOT automatically be represented as proof of completeness.

## 11. Freshness and Effective Applicability

Knowledge whose validity can materially decay over time MUST declare a freshness/review rule appropriate to its use.

The rule MAY use:

- review-by time;
- external-source freshness;
- effective period;
- event-triggered invalidation/review;
- source-version dependency;
- explicit no-expiry with rationale for stable knowledge.

Retrieval MUST distinguish `Current` from `Review Required`, `Superseded`, `Retracted` and `Retired` states where that distinction affects reliance.

A mutable search index or cache MUST NOT make stale Knowledge appear current merely because it remains retrievable.

## 12. Provenance and Learning Evidence

### 12.1 Learning Provenance Chain

For material Knowledge, provenance SHOULD permit reconstruction of the path:

```text
Source / Event / Execution
          ↓
      Observation
          ↓
   Memory reference
          ↓
 Knowledge Candidate
          ↓
 Validation evidence
          ↓
 Rights/classification review
          ↓
 Approval/decision
          ↓
 Knowledge Version
```

Not every step requires a physically separate object when one governed record can represent multiple bounded steps without losing semantics.

### 12.2 Material Transformations

Material transformations such as extraction, normalization, summarization, aggregation, deduplication, classification, model inference or human editing MUST remain attributable at a level sufficient to understand how the final Knowledge relates to its sources.

### 12.3 AI Provenance

Where AI materially contributes to a candidate or validation, provenance SHOULD preserve, where relevant and lawfully retained:

- model/provider or model-artifact identity;
- model/configuration version;
- prompt/template/configuration version where material;
- governed input/retrieval references;
- material tool calls or transformations;
- validation and approval evidence;
- known reproducibility limits.

Provenance MUST NOT require retention of hidden chain-of-thought, reusable secrets or unnecessary sensitive raw payload.

## 13. AI and Automated Learning Boundary

AI MAY:

- extract candidate assertions from records or documents;
- summarize and organize Memory;
- detect repeated patterns or anomalies;
- cluster Observations;
- propose Knowledge Candidates;
- compare candidates with existing Knowledge;
- retrieve relevant Knowledge;
- identify contradictions or freshness risks;
- draft Improvement Proposals;
- execute bounded validation steps explicitly authorized by the governing workflow.

AI MUST NOT independently:

- declare an unvalidated candidate to be Knowledge;
- make its own output sufficient evidence for final promotion merely because it generated, scored or validated that output;
- grant itself or another actor Organizational Authority;
- bypass authorization, rights, privacy, tenant-isolation or approval gates;
- silently broaden Knowledge scope or cross-organization reuse;
- silently extend retention;
- convert customer or product knowledge into shared platform knowledge;
- silently change approved Standards, Policies, Workflows, Product Contracts or production behavior;
- treat its own prior output or model memory as canonical source merely because it generated or recalled it.

Automated promotion **execution** MAY implement an already approved bounded governance rule when the final promotion predicate is independently defined by that approved governance mechanism and all RFC-0003/RFC-0005 controls remain enforceable. AI-generated judgement by itself MUST NOT constitute Organizational Authority or the final approval predicate for promotion into validated Knowledge. Automation executes delegated governance; it does not create governance authority.

## 14. Memory Retrieval and Use

### 14.1 Retrieval Is Not Authority

Successful retrieval means only that information matched a query or context under the retrieval mechanism. It does not prove truth, current applicability, permission to use, or authority.

### 14.2 Retrieval Controls

Retrieval of Memory or Knowledge MUST apply, where relevant:

- Organization/tenant scope;
- actor authorization;
- purpose limitation;
- classification/access constraints;
- current rights and permitted-use conditions;
- lifecycle/status filters;
- effective-version and freshness rules;
- minimization appropriate to the task.

### 14.3 Retrieval-Augmented Generation

RAG, semantic search and model-context assembly are execution techniques, not authoritative layers.

When RAG materially affects a consequential output, the system MUST preserve version-identifiable references to the material governed sources actually relied upon to the extent required by RFC-0005/RFC-0006 reconstruction rules.

Model context windows, prompt caches and conversational memory MUST NOT become independent canonical authorities.

## 15. Search, Embeddings and Derived Projections

Embeddings, vector indexes, lexical indexes, ranking features, summaries, caches and derived graph projections are non-canonical projections by default.

They MAY be rebuilt, compacted or replaced when:

- canonical governed sources remain preserved according to applicable policy;
- deletion and classification changes propagate correctly;
- stale or unauthorized projections cannot continue to expose deleted/restricted data;
- consequential reliance resolves to governed source versions rather than projection identity alone.

An embedding or model-derived representation MUST NOT be treated as a portable substitute for the underlying governed semantics.

## 16. Product and Platform Boundary

### 16.1 Product-domain Knowledge

Tender, procurement, legal, finance, marketing, manufacturing and other domain knowledge remains product-owned by default.

A product MAY define its own Knowledge types, validation rules, ontologies and domain-specific learning workflows within its architecture and applicable Product Contract.

### 16.2 Platform Interaction

Where a product reads, writes, proposes or relies upon shared platform Memory/Knowledge through Arvectum OS, the applicable Product Contract MUST declare, proportionate to consequence:

- relevant Memory/Knowledge types or capability contracts;
- read/write/propose operations;
- Organization scope;
- authority/source semantics;
- lifecycle/status expectations;
- classification and data-handling constraints;
- version/retrieval compatibility relied upon;
- failure and stale-data behavior;
- portability and migration expectations.

Declaring a read, write or propose operation in a Product Contract defines the permitted integration surface; it MUST NOT itself grant technical authorization, Organizational Authority, final validation authority or approval to promote Knowledge. Those gates remain independently evaluated under RFC-0003, RFC-0005 and applicable governance.

Undocumented direct access to internal knowledge tables, private vector collections, hidden prompts, private indexes or internal memory stores MUST NOT become a governed product/platform dependency.

### 16.3 Promotion to Platform

Repeated successful product-domain Knowledge or learning mechanisms do not automatically become Platform Capabilities or platform-global Knowledge.

Promotion requires the separate evidence-based platform admission/promotion rules of Accepted RFC-0001/RFC-0004 and MUST preserve domain neutrality.

## 17. Cross-Organization Learning and Reuse

### 17.1 Default Isolation

Memory, Knowledge, candidates, observations and learning evidence are Organization-scoped by default.

One organization's data MUST NOT alter another organization's Knowledge, model context, canonical state or learning decisions without explicit authorized cross-organization scope.

### 17.2 Shared Learning

Cross-organization reuse requires explicit rights, classification, purpose and governance appropriate to the material and proposed use.

Aggregation, anonymization, pseudonymization or model training MAY reduce risk but MUST NOT be treated as automatically creating legal or contractual reuse rights.

Platform-global learning MUST be limited to genuinely platform-governed, domain-neutral knowledge for which the platform has explicit authority and permitted reuse.

### 17.3 No Ambient Model Learning

A model provider's or shared model's technical ability to learn from inputs MUST NOT be treated as permission for Arvectum OS to expose organization data for training or cross-customer learning.

Training, fine-tuning or provider retention using organization data requires explicit applicable data-governance and contractual permission.

## 18. Security, Privacy, Retention and Deletion

### 18.1 Structural Controls

Memory and Knowledge are subject to RFC-0003 deny-by-default authorization, least privilege, Organization isolation, purpose limitation, minimization, classification, retention/deletion and privileged-access requirements.

### 18.2 Minimize Memory

The objective of organizational continuity MUST NOT be interpreted as a mandate to retain every conversation, prompt, document copy, telemetry sample or personal detail indefinitely.

Memory SHOULD prefer governed references, structured summaries and minimum sufficient evidence when those preserve required organizational meaning with lower privacy/security cost.

### 18.3 Deletion and Semantic History

When content must be deleted or minimized, the system MUST comply even if reconstructability is reduced.

Where lawful and useful, a tombstone or non-sensitive metadata record MAY preserve that a governed item existed, was deleted/restricted and affected historical outputs. Such metadata MUST NOT retain prohibited content or recreate the deleted information.

The system MUST NOT claim full reconstructability or reproducibility when required source material has been lawfully deleted.

### 18.4 Access Changes

A later classification, permission or rights change MUST propagate to retrieval/indexing/projection layers so that stale derived stores do not continue exposing restricted Memory or Knowledge.

## 19. Standards, Policies, Workflows and Learning

Knowledge may justify an Improvement Proposal, but it does not directly mutate operational rules.

A validated finding such as “this workflow frequently fails under condition X” MAY become Knowledge.

A proposed change such as “change Workflow version Y to retry using rule Z” is an Improvement Proposal and MUST follow the applicable Workflow/governance change process.

Likewise:

- Knowledge about policy performance does not silently amend Policy;
- Knowledge about a product contract does not silently amend the Product Contract;
- Knowledge about a capability does not change its lifecycle;
- Knowledge about an approval pattern does not create delegated Organizational Authority.

## 20. External Sources and Knowledge

When Knowledge depends materially on an external authoritative source, the Knowledge Record SHOULD preserve enough source identity/version/freshness context to determine whether the interpretation remains applicable.

If the external source changes materially, the affected Knowledge SHOULD enter Review Required or another explicit state according to its freshness/dependency rule.

A copied external fact MUST NOT become `Native` organizational authority merely because Arvectum OS stores or validates it. A `Native` Knowledge Record MAY represent the organization's validated interpretation of that fact while preserving the external authority for the underlying source.

## 21. Portability and Migration

A governed export of Memory or Knowledge SHOULD preserve, where applicable and permitted:

- stable subject and version identities or portable mappings;
- semantic type/schema versions;
- Organization scope;
- authority mode/source semantics;
- lifecycle/status;
- provenance and material evidence references;
- validation and approval references;
- relationships and supersession/retraction history;
- classification and rights constraints;
- freshness/effective-period metadata;
- known gaps caused by deletion, unavailable external sources or non-portable dependencies.

Search indexes, embeddings and vendor-specific retrieval structures MAY be omitted or regenerated if organizational meaning and required governed state remain portable.

Migration MUST NOT silently promote transient data, stale model memory, caches or legacy analytics into canonical Memory or Knowledge.

## 22. Failure, Degraded Mode and Reconciliation

When a required learning gate, authoritative source, validation mechanism or approval path is unavailable, the system MUST NOT silently promote Knowledge.

A workflow MAY:

- pause;
- reject;
- remain a candidate;
- use an explicitly governed degraded/manual validation path;
- mark the result unresolved or review-required.

If a Knowledge item used in a consequential execution is later retracted or found materially wrong, the system SHOULD support impact analysis over version-pinned usages and trigger review, correction, compensation or follow-up Governed Execution where proportionate to consequence.

## 23. Domain-Neutral Relationship Semantics

Implementations MAY use Typed Relationships to represent learning lineage such as:

- `derived_from`;
- `supports`;
- `contradicts`;
- `validated_by`;
- `approved_by`;
- `supersedes`;
- `retracts`;
- `applies_to`;
- `used_in`.

This list is informative and does not create a mandatory global relationship-type catalog.

Relationship endpoints MUST preserve RFC-0002 subject-level versus version-pinned semantics where consequential interpretation depends on a specific version.

## 24. Capability and Governance Boundary

This RFC defines platform architecture but does not declare a Memory or Knowledge implementation capability `Active`.

Any platform capability implementing shared Memory, Knowledge retrieval, validation, learning orchestration or promotion remains subject to RFC-0001 capability lifecycle and operational-readiness rules.

Decision-authority delegation remains governed by approved policy. Until such delegation exists, residual decision authority remains with the owner under Accepted governance.

## 25. Semantic Portability and Technology Independence

The meaning of Observation, Memory, Knowledge Candidate, Knowledge, validation, approval, supersession and retraction MUST remain independent of one database, vector engine, LLM, vendor or agent framework.

A conforming implementation SHOULD be able to replace retrieval/indexing/model technology without losing:

- canonical Knowledge identity/version semantics;
- governed Memory references;
- provenance;
- validation and approval history;
- organization scope and authority;
- lifecycle and supersession/retraction semantics;
- material execution attribution.

## 26. Migration from Provisional or Product-local Implementations

Existing chat histories, agent memories, vector stores, product notes, embeddings, analytics and product-local knowledge bases MUST NOT be bulk-promoted into canonical Memory or Knowledge merely to satisfy this RFC.

Migration SHOULD be incremental and evidence-driven:

1. identify material reusable subjects;
2. classify source authority and rights;
3. preserve or reconstruct provenance where supportable;
4. create candidates for material knowledge;
5. validate and approve proportionate to consequence;
6. keep low-value or ungovernable legacy content transient, product-local, archived or deleted as appropriate.

Where provenance cannot be established, the migrated item MUST expose that limitation and MUST NOT be represented as stronger Knowledge than evidence supports.

## 27. Conformance

Conformance to RFC-0007 is scoped.

A conforming subject MUST declare which Memory, Knowledge, candidate, retrieval and learning operations are in scope and which remain product-local, manual, provisional or out of scope.

At minimum, scoped conformance MUST demonstrate that:

1. Observation, Memory, Candidate, Knowledge and Improvement Proposal remain semantically distinguishable;
2. unvalidated material cannot silently become Knowledge;
3. significant governed Memory/Knowledge objects use RFC-0002 identity/version/canonical semantics;
4. consequential Knowledge reliance pins exact effective versions;
5. promotion gates preserve provenance, authority/source, validation, rights/classification, Organization scope and approval where applicable;
6. AI cannot create Organizational Authority or silently promote governed state;
7. contradiction and retraction do not rewrite immutable historical versions;
8. stale/retracted Knowledge is not silently represented as current;
9. retrieval/index projections do not become canonical authority;
10. RFC-0003 privacy, isolation, retention/deletion and cross-organization rules are enforced;
11. product-domain knowledge does not silently become platform-global knowledge;
12. learning-driven operational changes pass the applicable RFC-0005/governance path rather than mutating production behavior directly;
13. export/migration preserves governed semantics proportionate to the declared portability scope.

## 28. Normative Fitness Scenarios

### 28.1 Repeated AI Observation

A model observes the same purchasing pattern across many executions and proposes a rule.

**Required result:** repeated model observation remains Observation/Candidate state until governed validation and approval. Frequency and model confidence alone do not create Knowledge or a production rule.

### 28.2 External Registry Fact

A government registry is authoritative for an external legal status. Arvectum OS creates organizational guidance based on that status.

**Required result:** the external source remains authoritative for the legal-status fact. Arvectum OS MAY hold `Native` Knowledge for its validated organizational interpretation/guidance, with provenance to the external authority. It MUST NOT claim native authority over the registry fact.

### 28.3 Contradictory Evidence

New evidence materially contradicts Current Knowledge used by a workflow.

**Required result:** the existing Knowledge is not silently overwritten. Review Required, supersession or retraction is triggered according to policy, and material prior uses remain attributable to their exact versions.

### 28.4 Deleted Personal Data

A Knowledge provenance chain references personal data that must be deleted.

**Required result:** deletion takes precedence over perfect reconstruction. Permitted non-sensitive metadata MAY preserve the existence/effect of deletion; the system must not claim reconstructability it no longer has.

### 28.5 Cross-customer Pattern

A platform operator sees similar customer behavior in two Organizations and wants to create shared Knowledge.

**Required result:** no cross-organization promotion occurs without explicit rights, classification, purpose and governance. Processing by Arvectum OS does not create reuse rights.

### 28.6 Vector Search Result

A vector index returns an old Knowledge version as the top semantic match.

**Required result:** retrieval resolves lifecycle and effective-version status before consequential reliance. Similarity ranking cannot make a superseded or retracted version current.

### 28.7 Product-local Domain Knowledge

A procurement product validates a domain-specific supplier heuristic successfully in several pilots.

**Required result:** the heuristic remains product-owned Knowledge unless a separate platform-promotion decision demonstrates a domain-neutral reusable mechanism. Success does not automatically create a Platform Capability or platform-global semantic.

### 28.8 Learning-driven Workflow Change

Operational evidence shows that an approved Workflow should change.

**Required result:** the evidence may produce Knowledge and an Improvement Proposal. The Workflow changes only through its governed versioning/approval process; the learning mechanism does not mutate it directly.

## 29. Consequences

### Positive

- Arvectum OS can accumulate organizational intelligence without treating storage as truth.
- AI-assisted learning becomes useful without granting AI silent authority.
- Knowledge remains explainable, versioned, reviewable and portable.
- external source authority and customer sovereignty remain intact.
- retrieval/RAG technology can evolve without redefining canonical organizational meaning.
- product learning can compound locally while shared platform promotion remains evidence-based.
- stale, contradictory and retracted Knowledge has explicit handling rather than hidden overwrite.

### Costs

- material Knowledge requires provenance and lifecycle metadata;
- promotion workflows introduce validation and approval overhead where consequence justifies it;
- deletion and rights constraints can reduce reproducibility or reuse;
- product/platform and cross-organization learning cannot rely on implicit shared memory;
- derived indexes must propagate access/deletion/lifecycle changes correctly.

These costs are intentional and MUST remain proportionate to consequence and organizational value.

## 30. Risks and Mitigations

### Risk: everything becomes canonical Memory

**Mitigation:** significance threshold, transient/product-local options, explicit retention and asset designation.

### Risk: validation becomes bureaucratic

**Mitigation:** proportional validation; low-risk local knowledge may use bounded automated/manual controls.

### Risk: AI confidence is mistaken for truth

**Mitigation:** confidence is explicitly non-authoritative and separate from validation, source authority and approval.

### Risk: stale Knowledge remains operational

**Mitigation:** freshness/review rules, lifecycle-aware retrieval and version-pinned execution evidence.

### Risk: customer data leaks into shared learning

**Mitigation:** organization-local default, explicit rights/governance for cross-organization reuse and no ambient model learning.

### Risk: product domain semantics leak into platform

**Mitigation:** product ownership by default and separate evidence-based platform promotion.

### Risk: deletion destroys historical explainability

**Mitigation:** minimization, governed references and permitted tombstone metadata, while explicitly preferring legal/privacy obligations over false claims of perfect reconstruction.

## 31. Acceptance Criteria

RFC-0007 may be accepted only when:

1. compatibility with Constitution `1.2.0` and Accepted RFC-0001 through RFC-0006 has been reviewed;
2. Observation, Memory, Knowledge Candidate, Knowledge and Improvement Proposal are clearly distinguishable;
3. no new Kernel primitive or competing authority model is introduced;
4. product-domain and cross-organization boundaries preserve RFC-0003/RFC-0004 requirements;
5. AI cannot silently promote Knowledge or operational change;
6. contradiction, freshness, supersession, retraction, deletion and historical interpretation are addressed;
7. retrieval/RAG/indexing are explicitly non-authoritative projections;
8. version-pinned consequential reliance and RFC-0005/RFC-0006 reconstruction requirements remain intact;
9. functional cross-review is complete with no unresolved material contradiction;
10. explicit owner approval exists independently before acceptance publication;
11. RFC Index and canonical roadmap are synchronized during acceptance publication;
12. read-after-write verification closes the transition under the approved RFC State Transition Procedure.

## 32. Open Implementation Decisions

The following are intentionally left to subordinate decisions unless later evidence requires architecture:

- physical Memory/Knowledge persistence model;
- vector/lexical/graph retrieval technology;
- chunking and embedding strategy;
- concrete validation workflow templates by risk class;
- confidence-calibration methods;
- knowledge-type and relationship catalogs;
- automated review scheduling implementation;
- cache/index invalidation technology;
- product-specific ontology and domain validation rules;
- UI for review, contradiction and approval.

## 33. Review Evidence

Functional cross-review:

- `docs/reviews/RFC-0007-functional-cross-review.md` — `Complete`;
- iterations completed: 4 of maximum 7;
- result: `Pass after bounded reconciliation`.

Reviewed working draft:

- RFC-0007 `0.1.0`;
- immutable blob SHA `686e6fc3fe720709773efb3b685f97b45d458b69`.

The bounded reconciliation required by the cross-review is incorporated in this `0.2.0` proposal.

## 34. Decision Requested

Approve RFC-0007 `0.2.0` as the domain-neutral architecture for Memory, Knowledge and Governed Learning Lifecycle.

Acceptance would complete Roadmap Block 0G architecture and permit Phase 0 reference implementation work to proceed without inventing cross-cutting Memory/Knowledge semantics in code.
