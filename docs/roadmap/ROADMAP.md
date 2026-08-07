# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `1.1.9`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS.

It answers:

> What should Arvectum OS work on next, in what order, and what constitutes completion of the current foundation stage?

This roadmap coordinates work. It does **not** override architectural or governance authority.

Authority remains, in descending order:

1. the Constitution;
2. Accepted RFCs;
3. Accepted ADRs;
4. approved policies, standards and catalogs;
5. Product Contracts and approved product-specific decisions;
6. implementation and tests;
7. this roadmap as a planning artifact;
8. task materials, chats and model memory.

If this roadmap conflicts with a higher-authority source, the higher-authority source prevails and this roadmap must be corrected.

## 2. Versioning and update rules

This roadmap is versioned in Git and uses semantic versioning:

- `PATCH` — progress, status, links, wording clarifications and other non-structural updates;
- `MINOR` — sequencing, milestone scope, exit-criteria or roadmap-maintenance process changes that do not alter an Accepted architectural contract;
- `MAJOR` — restructuring of the roadmap lifecycle or planning model.

A roadmap update must never silently redefine the scope of an Accepted RFC. If an Accepted RFC must change, use the applicable architecture-governance process first, then update the roadmap to reflect the accepted decision.

Git history is the canonical history of roadmap revisions.

## 3. Status and progress legend

| Marker | Meaning |
|---|---|
| 🟩 | Complete / accepted / published |
| 🟨 | In progress |
| 🟦 | Ready / next planned work |
| ⬜ | Planned, not started |
| 🟥 | Blocked or conflicted |
| ⚫ | Deferred / not currently scheduled |

Progress bars are planning indicators, not conformance claims.

`██████████ 100%` — complete  
`█████░░░░░ 50%` — partially complete  
`░░░░░░░░░░ 0%` — not started

## 4. Current phase

**Phase 0 — Foundation / Architecture Bootstrap — Complete**

The goal of Phase 0 is to establish enough shared language, architecture, governance and contracts to permit reversible implementation without premature platform lock-in.

The phase does **not** require the entire future platform to be fully specified before useful product experiments or reversible reference implementation work can begin.

### Phase 0 overview

| Block | Scope | Status | Progress |
|---|---|---:|---:|
| 🟪 0A | Governance baseline | 🟩 | `██████████ 100%` |
| 🟦 0B | Architecture language baseline | 🟩 | `██████████ 100%` |
| 🟪 0C | RFC-0002 — Kernel metamodel | 🟩 | `██████████ 100%` |
| 🟢 0D | RFC-0003 — Identity, security, privacy, sovereignty | 🟩 | `██████████ 100%` |
| 🟠 0E | RFC-0004 — Product Contract and extension model | 🟩 | `██████████ 100%` |
| 🔵 0F | RFC-0005/0006 — Governed execution, events and provenance | 🟩 | `██████████ 100%` |
| 🟣 0G | RFC-0007 — Memory, knowledge and learning lifecycle | 🟩 | `██████████ 100%` |
| 🟨 0H | Reference implementation readiness | 🟩 | `██████████ 100%` |

## 5. Block 0A — Governance baseline

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Completed

- 🟩 Constitution `1.2.0` — `Ratified`;
- 🟩 RFC Index established;
- 🟩 RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- 🟩 canonical roadmap established in this file;
- 🟩 repository agent rules identify governance work as a first-class task classification.

### Known governance debt

The RFC Index records a provenance gap for the transition to Constitution `1.2.0`. This debt must be repaired only from confirmed owner-approved evidence and must not be reconstructed by assumption.

### Exit criterion

There is one canonical architecture baseline and one canonical planning source in the repository.

## 6. Block 0B — Architecture language baseline

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Objective

Create a shared vocabulary before further detailed architecture work so that contributors, products and AI agents use the same terms consistently.

### Deliverable

Published and synchronized:

- 🟩 [`docs/architecture/GLOSSARY.md`](../architecture/GLOSSARY.md) — Arvectum OS Architecture Glossary `1.2.0`, aligned through Accepted RFC-0007.

The glossary provides current navigation for architectural terms established by the Constitution and Accepted RFCs, including at minimum:

- Organization / Tenant;
- Organizational Intelligence;
- Executable Organizational Model;
- Identity;
- Canonical Record;
- Canonical Lineage;
- Canonical Head;
- Effective Version;
- Governed Organizational Asset;
- Transient Output;
- Typed Relationship;
- Event;
- Execution Context;
- Governed Execution;
- Principal / Actor;
- Authentication / Authorization / Organizational Authority;
- Product;
- Product Experiment;
- Product Contract;
- Platform Capability;
- Platform Service;
- Kernel;
- Workflow;
- Memory;
- Knowledge;
- Provenance;
- Authority Mode;
- Conformance.

### Constraint

The glossary is a language and navigation artifact. It summarizes terms from higher-authority sources and does not create new architectural obligations or silently redefine Accepted RFC terminology.

### Exit criterion

🟩 Achieved: a contributor can resolve the meaning and canonical source of core Arvectum OS terms without relying on chat history or model memory.

## 7. Block 0C — RFC-0002: Kernel metamodel

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### Canonical scope

RFC-0001 explicitly reserved the precise Kernel metamodel for RFC-0002.

RFC-0002 is:

`Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model`

It defines the items required by RFC-0001, including:

- identity and version semantics for every Kernel primitive;
- Event as a Canonical Record specialization;
- Execution Context as a Canonical Record specialization with governed lifecycle and preservation semantics;
- independent identity and versioning for Typed Relationship assertion instances;
- Canonical Lineage, Canonical Head and Effective Version semantics;
- version-pinned consequential resolution;
- authority declarations, external-authority contracts and cutover semantics;
- Governed Organizational Asset designation and legal-rights neutrality;
- compatibility and staged migration rules for provisional implementations;
- scoped Kernel metamodel conformance.

### Completed

- 🟩 RFC-0002 `1.0.0` — `Accepted`;
- 🟩 owner approval recorded independently in [`DECISION-2026-08-07-RFC-0002-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0002-ACCEPTANCE.md);
- 🟩 structured draft review completed;
- 🟩 domain-neutral scenario validation completed;
- 🟩 architecture cross-section consistency validation completed;
- 🟩 role-based top-management cross-review across CEO, COO, CFO/Risk, CISO/Privacy, Legal/Rights, Product/Commercial and CTO/Architecture completed;
- 🟩 management review corrected accountable architectural ownership and mandatory external-authority contract fidelity to RFC-0001;
- 🟩 Architecture Glossary synchronized to Accepted RFC-0002 and later foundational RFCs;
- 🟩 RFC Index synchronized to `Accepted 1.0.0`.

### Accepted boundary

Within RFC-0002 scope, the precise Kernel metamodel is no longer provisional.

Implementation details intentionally left to later RFCs, ADRs, standards, Product Contracts and product decisions remain unresolved where RFC-0002 says so. Acceptance does not select a physical database model, authentication/authorization mechanism, workflow engine, observability backend or product-specific schema.

Acceptance also does not make a capability `Active`, establish production readiness or an SLA/support commitment, grant legal reuse rights, or require immediate wholesale migration of product-local legacy data.

### Exit criterion

🟩 Achieved: RFC-0002 is `Accepted` with prior owner approval evidence and synchronized RFC Index and glossary.

## 8. Block 0D — RFC-0003: Identity, security, privacy, tenant sovereignty and portability

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### RFC

`RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability`

### Dependency baseline

RFC-0003 builds on the Accepted Kernel semantics in RFC-0001 and RFC-0002 without redefining Identity as mutable canonical state, turning Typed Relationships into implicit permissions, or creating competing authority across organizations.

### Completed

- 🟩 first complete working draft `0.1.0` prepared;
- 🟩 functional role-based cross-review completed across CEO/strategy, COO/operations, CTO/architecture, CISO/security, Privacy, Legal/rights, Product and Engineering perspectives;
- 🟩 review corrections incorporated into RFC-0003 `0.2.0` reviewed proposal;
- 🟩 detailed review evidence published in [`docs/reviews/RFC-0003-functional-cross-review.md`](../reviews/RFC-0003-functional-cross-review.md);
- 🟩 owner approval recorded independently in [`DECISION-2026-08-07-RFC-0003-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0003-ACCEPTANCE.md);
- 🟩 [`RFC-0003`](../rfc/RFC-0003-identity-security-privacy-tenant-sovereignty-portability.md) published as `Accepted 1.0.0`;
- 🟩 RFC Index synchronized with acceptance evidence.

### Accepted boundary

RFC-0003 `1.0.0` is binding architecture within its declared scope for identity administration, authentication, authorization, organizational authority separation, tenant isolation, privacy/data governance, cross-organization sharing constraints, privileged/break-glass access and portability.

It does not select IAM, cryptographic, database or cloud technologies and does not pre-empt RFC-0004 Product Contracts, RFC-0005 Governed Execution, RFC-0006 Event/Provenance or RFC-0007 Memory/Knowledge semantics.

### Exit criterion

🟩 Achieved: the shared platform has accepted domain-neutral rules for identity administration, isolation, authority boundaries, portability and applicable security/privacy invariants without prematurely fixing commodity implementation technology.

## 9. Block 0E — RFC-0004: Product Contract, Product Experiment and Extension Model

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### RFC

[`RFC-0004 — Product Contract, Product Experiment and Extension Model`](../rfc/RFC-0004-product-contract-product-experiment-extension-model-v1.0.0.md) — `Accepted 1.0.0`.

### Completed

- 🟩 complete working draft prepared and iteratively refined;
- 🟩 functional role-based cross-review completed across CEO/strategy, COO/operations, CTO/architecture, CISO/security, Privacy, Legal/rights, Product and Engineering perspectives;
- 🟩 reviewed proposal `0.3.0` preserved with immutable proposal blob `5a413a240588677211ad56f3a23b30a65d1c4334`;
- 🟩 owner approval recovered through current canonical repair decision [`DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR`](../governance/decisions/DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR.md) — `Approved`;
- 🟩 additional compatibility re-check performed against Accepted RFC-0003 `1.0.0` as review iteration 4;
- 🟩 no material conflict found; stale RFC-0003 lifecycle wording reconciled for acceptance publication;
- 🟩 RFC-0004 published as `Accepted 1.0.0` in commit `3b3f72a01bd76d9cfb6a1ef78e7ec6a627173ee2`;
- 🟩 RFC Index synchronized with acceptance evidence;
- 🟩 read-after-write transition verification completed against RFC publication, Index, owner approval and roadmap state.

### Accepted boundary

RFC-0004 `1.0.0` is binding architecture for Product Contract identity/version/lifecycle semantics, minimal provisional contracts for platform-interacting Product Experiments, explicit capability/canonical-state/operation/event/artifact boundaries, extension registration, compatibility/migration/deprecation rules, and evidence-based promotion from product-local experiments into platform incubation.

Product Contract lifecycle remains independent from Platform Capability lifecycle. Product-domain logic remains product-owned by default. Extension registration remains distinct from authorization and Organizational Authority. Undocumented direct database/internal-import coupling across the product/platform boundary is non-conforming.

RFC-0004 is subordinate to Accepted RFC-0003 security, privacy, isolation, authority and portability requirements.

### Exit criterion

🟩 Achieved: products can interact with Arvectum OS through an explicit, versioned and governed boundary without leaking product business logic into the platform.

## 10. Block 0F — Governed execution, events and provenance

**Status:** 🟩 Complete — RFC-0005 and RFC-0006 `Accepted 1.0.0`  
**Progress:** `██████████ 100%`

### Planned RFCs

1. `RFC-0005 — Governed Execution and Workflow Model`;
2. `RFC-0006 — Event, Provenance and Observability Model`.

### RFC-0005 completed

- 🟩 RFC-0005 `0.1.0` initial complete proposal prepared;
- 🟩 first functional cross-review completed with 3 iterations;
- 🟩 reviewed proposal `0.2.0` published;
- 🟩 RFC-0004 `1.0.0` accepted and its state transition fully closed;
- 🟩 review iteration 4 completed against Accepted RFC-0004 and Roadmap `1.1.2`;
- 🟩 result `Pass with bounded reconciliation`;
- 🟩 RFC-0005 reviewed proposal `0.3.0` published with normative dependency on Accepted RFC-0004;
- 🟩 explicit owner approval recorded in [`DECISION-2026-08-07-RFC-0005-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0005-ACCEPTANCE.md);
- 🟩 [`RFC-0005`](../rfc/RFC-0005-governed-execution-workflow-model-v1.0.0.md) published as `Accepted 1.0.0`;
- 🟩 RFC Index synchronized with approval and publication evidence.

### RFC-0006 completed

- 🟩 RFC-0006 `0.1.0` working draft prepared;
- 🟩 functional cross-review completed across architecture, operations, engineering/SRE, security, privacy, legal, product and AI-governance perspectives;
- 🟩 review completed after 4 of maximum 7 iterations with result `Pass after bounded reconciliation`;
- 🟩 review evidence published in [`docs/reviews/RFC-0006-functional-cross-review.md`](../reviews/RFC-0006-functional-cross-review.md);
- 🟩 reviewed proposal `0.2.0` published with immutable blob SHA `5468001d2a0ff13fb16b7f88f7a3bc26f6bc6225`;
- 🟩 explicit owner approval recorded in [`DECISION-2026-08-07-RFC-0006-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0006-ACCEPTANCE.md), approval commit `26a92a6663083cc2923bc25e5ccf920b61c17387`;
- 🟩 [`RFC-0006`](../rfc/RFC-0006-event-provenance-observability-model-v1.0.0.md) published as `Accepted 1.0.0`, publication commit `49f88d04f6440dcbeedb860ccbf7b5f43a2b7b2a`;
- 🟩 RFC Index synchronized with approval, proposal, review and publication evidence.

### Accepted Block 0F boundary

RFC-0005 `1.0.0` is binding architecture for Governed Execution and Workflow semantics. RFC-0006 `1.0.0` is binding architecture for Event, Provenance and Observability semantics.

Together they establish the domain-neutral model for consequential execution, observable operational history, Event admission/immutability, causation/correlation, required evidence, delivery/replay semantics, provenance, telemetry boundaries, reconstruction, security/privacy of observability data and semantic portability.

They preserve RFC-0004 Product Contract boundaries and RFC-0003 authority/security/privacy invariants. Their acceptance does not make an implementation capability `Active`, establish operational readiness, or select a broker/workflow/observability technology.

### Exit criterion

🟩 Achieved: consequential execution and operational history have accepted domain-neutral models sufficient for explainability, reconstruction and controlled state change.

## 11. Block 0G — Memory, knowledge and governed learning

**Status:** 🟩 Complete — RFC-0007 `Accepted 1.0.0`  
**Progress:** `██████████ 100%`

### RFC

[`RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`](../rfc/RFC-0007-memory-knowledge-governed-learning-lifecycle-v1.0.0.md) — `Accepted 1.0.0`.

### Completed

- 🟩 RFC-0007 `0.1.0` working draft published;
- 🟩 functional cross-review completed across organizational-value, operations, architecture, security, privacy, legal/rights, product, engineering and AI-governance perspectives;
- 🟩 4 of maximum 7 review iterations completed;
- 🟩 review result: `Pass after bounded reconciliation`;
- 🟩 review evidence published in [`docs/reviews/RFC-0007-functional-cross-review.md`](../reviews/RFC-0007-functional-cross-review.md);
- 🟩 reviewed RFC-0007 `0.2.0` published as `Proposed` with immutable blob SHA `06dc706c3f717a159c0d9495a3c9ae3f29fbdf11`;
- 🟩 explicit owner approval recorded independently in [`DECISION-2026-08-07-RFC-0007-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0007-ACCEPTANCE.md), approval commit `0de3fc2a85f5b567e28cae2eed95f67838b66b4e`;
- 🟩 RFC-0007 published as `Accepted 1.0.0`, publication commit `45eb9f08f3d039b6642379e5dd7bc762b9289927`;
- 🟩 RFC Index synchronized with approval, proposal, review and publication evidence.

### Accepted boundary

RFC-0007 `1.0.0` is binding architecture for Observation, Organizational Memory, Knowledge Candidate, Improvement Proposal, validated Knowledge, explicit governed promotion, freshness/contradiction/supersession/retraction, AI authority boundaries, RAG/index/embedding non-authority, product and cross-organization learning boundaries, and portability/migration semantics.

It does not create a new Kernel primitive, make any implementation capability `Active`, establish operational readiness, select persistence/retrieval/model technology, authorize cross-organization reuse, or approve product-specific domain knowledge.

### Exit criterion

🟩 Achieved: the platform has an accepted model for distinguishing observations, memory, validated knowledge, proposals and approved reusable organizational assets without allowing silent AI-driven mutation of governed state.

## 12. Block 0H — Reference implementation readiness

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Objective

Make the smallest useful reference implementation startable now that the planned foundational semantic RFC sequence through RFC-0007 is Accepted, without introducing speculative technology or cross-cutting architecture in code.

### Completed

- 🟩 Constitution `1.2.0` and RFC-0001 through RFC-0007 `1.0.0` re-verified from the canonical repository;
- 🟩 [`Reference Implementation Readiness Baseline`](../implementation/REFERENCE-IMPLEMENTATION-READINESS.md) `1.0.0` published;
- 🟩 logical modular-monolith implementation structure defined without fixing permanent service topology;
- 🟩 first domain-neutral executable slice and failure cases defined;
- 🟩 minimum architecture fitness matrix mapped to RFC-0001 through RFC-0007;
- 🟩 security/privacy/Organization-scope bootstrap constraints defined;
- 🟩 Product Contract entry condition for real product interaction defined;
- 🟩 ADR trigger criteria defined;
- 🟩 minimum ADR set before the first in-memory/in-process slice assessed as `zero` because no constraining technology/public-contract choice is yet required;
- 🟩 functional cross-review completed after 3 of maximum 7 iterations with result `Pass after bounded reconciliation`;
- 🟩 review evidence published in [`docs/reviews/REFERENCE-IMPLEMENTATION-READINESS-functional-cross-review.md`](../reviews/REFERENCE-IMPLEMENTATION-READINESS-functional-cross-review.md);
- 🟩 Architecture Glossary synchronized to `1.2.0` through Accepted RFC-0007;
- 🟩 RFC-0008 numbering/scope collision prevented: readiness remains Roadmap Block 0H; RFC-0008 remains reserved by RFC-0001 for Document and Artifact Architecture.

### Readiness boundary

The first reference implementation may begin with domain-neutral semantic modules, in-memory persistence ports, in-process application calls and executable fitness fixtures.

No programming language, database, API protocol, event broker, workflow engine, IAM provider, policy engine, vector store, LLM/model provider, cloud topology or permanent package structure is canonically selected by Block 0H.

An ADR becomes necessary only when an implementation choice becomes sufficiently constraining, such as a durable cross-module dependency, material migration commitment, stable public boundary, security/isolation mechanism or vendor/technology dependency with meaningful portability consequences.

Reference implementation readiness is not operational readiness. This block does not make any capability `Active`, authorize a production conformance claim, create an SLA/support promise or make the Proposed Decision Authority Policy effective.

### Exit criterion for Phase 0

🟩 **Achieved. Phase 0 is complete.**

1. core architectural language is discoverable and aligned through Accepted RFC-0007 in Architecture Glossary `1.2.0`;
2. the foundational RFCs required for the first reference implementation are Accepted;
3. unresolved technology choices are explicitly deferred, provisional and migration-safe;
4. the first executable slice is defined tightly enough to start without inventing cross-cutting architecture in code;
5. product experiments have an explicit Product Contract entry boundary when platform interaction begins.

## 13. Default work sequence

The current default sequence is:

```text
Constitution 1.2.0                      ✅
        ↓
RFC-0001 Architecture                   ✅ ACCEPTED 1.0.0
        ↓
Canonical Roadmap                       ✅
        ↓
Architecture Glossary                   ✅ 1.2.0
        ↓
RFC-0002 Kernel Metamodel               ✅ ACCEPTED 1.0.0
        ↓
RFC-0003 Identity / Security / Privacy  ✅ ACCEPTED 1.0.0
        ↓
RFC-0004 Product Contract / Extensions  ✅ ACCEPTED 1.0.0
        ↓
RFC-0005 Governed Execution / Workflow  ✅ ACCEPTED 1.0.0
        ↓
RFC-0006 Event / Provenance / Observability  ✅ ACCEPTED 1.0.0
        ↓
RFC-0007 Memory / Knowledge / Learning  ✅ ACCEPTED 1.0.0
        ↓
Reference Implementation Readiness      ✅ BLOCK 0H COMPLETE
        ↓
First bounded executable slice          🟦 NEXT
        ↓
Product-driven validation and capability incubation
```

This is a **default dependency-aware sequence**, not a ban on parallel work.

Parallel work is permitted when the work is bounded and reversible and does not prejudge unresolved higher-level architecture.

RFC-0008 Document and Artifact Architecture may proceed when its scope becomes the highest-value unresolved architectural dependency; it is not a prerequisite for the already bounded first executable slice unless that slice begins to rely on unresolved shared Document/Artifact semantics.

## 14. Next canonical action

The current architecture/delivery work item is:

> **Implement the first bounded reference implementation executable slice defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`: prove stable identities, immutable canonical versions, explicit Organization/authority gates, Governed Execution mutation, canonical Event evidence, provenance and Observation non-promotion with executable tests before adding infrastructure.**

For the first code slice:

- prefer the simplest reversible implementation;
- keep product-domain semantics out of shared modules;
- use an ADR before a concrete choice crosses the readiness document's ADR gate;
- do not treat working code as an `Active` Platform Capability or production-readiness evidence by itself.

## 15. Roadmap maintenance rule

Every roadmap update **MUST begin with repository synchronization**, not chat-memory reconstruction.

Before changing roadmap status or progress:

1. fetch the current canonical `docs/constitution/CONSTITUTION.md`;
2. fetch `docs/rfc/README.md` and determine the actual status/version of every relevant RFC;
3. inspect relevant Accepted RFC/ADR/decision records for the milestone being updated;
4. fetch the current `docs/roadmap/ROADMAP.md` from the canonical repository;
5. reconcile repository state with any project-chat context; repository state remains authoritative unless a current governance repair is explicitly being recorded.

After every accepted RFC, material planning decision, or meaningful implementation milestone:

1. update status and progress in this file;
2. update links and dependencies;
3. increment the roadmap version according to Section 2;
4. commit the update to the canonical repository;
5. do not maintain a competing roadmap in chat, local notes or another repository.

The approved [`RFC State Transition Procedure`](../governance/RFC-STATE-TRANSITION-PROCEDURE.md) additionally requires each owner-approved RFC transition to be fully closed through canonical publication, RFC Index synchronization, roadmap synchronization and read-after-write consistency verification before substantive work advances to the next RFC.

Chats may discuss future roadmap changes, but only the version committed here is canonical.