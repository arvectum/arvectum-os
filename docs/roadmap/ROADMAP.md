# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `1.1.7`
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

**Phase 0 — Foundation / Architecture Bootstrap**

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
| 🟣 0G | RFC-0007 — Memory, knowledge and learning lifecycle | 🟨 | `████████░░ 80%` |
| 🟨 0H | Reference implementation readiness | ⬜ | `░░░░░░░░░░ 0%` |

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

Published:

- 🟩 [`docs/architecture/GLOSSARY.md`](../architecture/GLOSSARY.md) — Arvectum OS Architecture Glossary `1.1.0`.

The glossary defines the current canonical meaning of architectural terms already established by the Constitution and Accepted RFCs, including at minimum:

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
- 🟩 Architecture Glossary synchronized to Accepted RFC-0002;
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

They preserve RFC-0004 Product Contract boundaries, RFC-0003 authority/security/privacy invariants and the RFC-0007 boundary for Memory, Knowledge and Governed Learning. Their acceptance does not make an implementation capability `Active`, establish operational readiness, or select a broker/workflow/observability technology.

### Exit criterion

🟩 Achieved: consequential execution and operational history have accepted domain-neutral models sufficient for explainability, reconstruction and controlled state change.

## 11. Block 0G — Memory, knowledge and governed learning

**Status:** 🟨 In progress — RFC-0007 `0.2.0` Proposed  
**Progress:** `████████░░ 80%`

### RFC

[`RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`](../rfc/RFC-0007-memory-knowledge-governed-learning-lifecycle.md) — `Proposed 0.2.0`.

### Dependency baseline

RFC-0007 builds on Accepted RFC-0001 through RFC-0006. It preserves the distinction among operational Events/evidence, observations, organizational Memory, validated Knowledge, proposals and approved reusable organizational assets, and does not allow silent AI-driven promotion into governed state.

### Completed

- 🟩 RFC-0007 `0.1.0` working draft published;
- 🟩 functional cross-review completed across organizational-value, operations, architecture, security, privacy, legal/rights, product, engineering and AI-governance perspectives;
- 🟩 4 of maximum 7 review iterations completed;
- 🟩 review result: `Pass after bounded reconciliation`;
- 🟩 review evidence published in [`docs/reviews/RFC-0007-functional-cross-review.md`](../reviews/RFC-0007-functional-cross-review.md);
- 🟩 bounded reconciliation incorporated;
- 🟩 reviewed RFC-0007 `0.2.0` published as `Proposed`;
- 🟩 RFC Index synchronized to show RFC-0007 `Proposed 0.2.0` and review evidence.

### Remaining transition

- 🟨 explicit owner approval of reviewed RFC-0007 `0.2.0`;
- ⬜ canonical approval decision record created independently before acceptance publication;
- ⬜ RFC-0007 acceptance publication as `1.0.0`;
- ⬜ RFC Index acceptance evidence synchronization;
- ⬜ roadmap closure of Block 0G;
- ⬜ read-after-write consistency verification under the approved RFC State Transition Procedure.

### Proposed boundary

RFC-0007 `0.2.0` proposes the domain-neutral lifecycle for Observation, Organizational Memory, Knowledge Candidate, Improvement Proposal and validated Knowledge; explicit promotion gates; freshness/contradiction/supersession/retraction handling; AI authority boundaries; RAG/index/embedding non-authority; product and cross-organization learning boundaries; and portability/migration semantics.

Because RFC-0007 remains `Proposed`, these refinements are not yet binding architecture and do not override Accepted RFC-0001 through RFC-0006.

### Exit criterion

The platform has an accepted model for distinguishing observations, memory, validated knowledge, proposals and approved reusable organizational assets without allowing silent AI-driven mutation of governed state.

## 12. Block 0H — Reference implementation readiness

**Status:** ⬜ Planned  
**Progress:** `░░░░░░░░░░ 0%`

### Objective

Begin the smallest useful reference implementation once the relevant architectural dependencies are sufficiently defined.

Implementation may proceed in parallel with later RFC work when it is:

- bounded;
- reversible;
- explicitly provisional where required;
- migration-friendly;
- owned and reviewable;
- consistent with security, governance, data-integrity and contractual constraints.

### Expected subordinate decisions

Use ADRs for concrete implementation choices only when they become necessary and sufficiently constraining, for example:

- repository/runtime structure;
- persistence technology;
- API style;
- migration tooling;
- test strategy;
- local development environment.

Technology choices are not constitutional or fundamental architectural principles.

### Exit criterion for Phase 0

Phase 0 is complete when:

1. the core architectural language is discoverable and aligned with Accepted sources;
2. RFC-0002 through the minimum set of foundational RFCs required for the first reference implementation are Accepted or explicitly not required for its bounded scope;
3. unresolved areas are clearly marked provisional and migration-safe;
4. the first reference implementation can start without inventing cross-cutting architecture in code;
5. product experiments can connect through explicit boundaries where platform interaction exists.

## 13. Default work sequence

The current default sequence is:

```text
Constitution 1.2.0                      ✅
        ↓
RFC-0001 Architecture                   ✅ ACCEPTED 1.0.0
        ↓
Canonical Roadmap                       ✅
        ↓
Architecture Glossary                   ✅
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
RFC-0007 Memory / Knowledge / Learning  🟨 PROPOSED 0.2.0 — OWNER APPROVAL NEXT
        ↓
Reference Implementation + ADRs
        ↓
Product-driven validation and capability incubation
```

This is a **default dependency-aware sequence**, not a ban on parallel work.

Parallel work is permitted when the work is bounded and reversible and does not prejudge unresolved higher-level architecture.

## 14. Next canonical action

The current architecture action is:

> **Obtain explicit owner approval for reviewed RFC-0007 `0.2.0`. After approval, complete the canonical acceptance publication and transition closure before treating RFC-0007 as binding architecture or closing Block 0G.**

The reviewed proposal and cross-review are already canonical. No additional review iteration is required unless owner review identifies a new material concern.

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
