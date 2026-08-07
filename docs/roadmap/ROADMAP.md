# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `1.0.7`
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
- `MINOR` — sequencing, milestone scope or exit-criteria changes that do not alter an Accepted architectural contract;
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
| 🟢 0D | RFC-0003 — Identity, security, privacy, sovereignty | 🟦 | `░░░░░░░░░░ 0%` |
| 🟠 0E | RFC-0004 — Product Contract and extension model | ⬜ | `░░░░░░░░░░ 0%` |
| 🔵 0F | RFC-0005/0006 — Governed execution, events and provenance | ⬜ | `░░░░░░░░░░ 0%` |
| 🟣 0G | RFC-0007 — Memory, knowledge and learning lifecycle | ⬜ | `░░░░░░░░░░ 0%` |
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

**Status:** 🟦 Ready / next planned work  
**Progress:** `░░░░░░░░░░ 0%`

### Planned RFC

`RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability`

### Dependency baseline

RFC-0003 must build on the Accepted Kernel semantics in RFC-0001 and RFC-0002 without redefining Identity as mutable canonical state, turning Typed Relationships into implicit permissions, or creating competing authority across organizations.

### Exit criterion

The shared platform has accepted domain-neutral rules for identity administration, isolation, authority boundaries, portability and applicable security/privacy invariants without prematurely fixing commodity implementation technology.

## 9. Block 0E — RFC-0004: Product Contract, Product Experiment and Extension Model

**Status:** ⬜ Planned  
**Progress:** `░░░░░░░░░░ 0%`

### Planned RFC

`RFC-0004 — Product Contract, Product Experiment and Extension Model`

### Exit criterion

Products can interact with Arvectum OS through an explicit, versioned and governed boundary without leaking product business logic into the platform.

## 10. Block 0F — Governed execution, events and provenance

**Status:** ⬜ Planned  
**Progress:** `░░░░░░░░░░ 0%`

### Planned RFCs

1. `RFC-0005 — Governed Execution and Workflow Model`;
2. `RFC-0006 — Event, Provenance and Observability Model`.

### Exit criterion

Consequential execution and operational history have accepted domain-neutral models sufficient for explainability, reconstruction and controlled state change.

## 11. Block 0G — Memory, knowledge and governed learning

**Status:** ⬜ Planned  
**Progress:** `░░░░░░░░░░ 0%`

### Planned RFC

`RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`

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
RFC-0001 Architecture                   ✅
        ↓
Canonical Roadmap                       ✅
        ↓
Architecture Glossary                   ✅
        ↓
RFC-0002 Kernel Metamodel               ✅ ACCEPTED 1.0.0
        ↓
RFC-0003 Identity / Security / Privacy  NEXT
        ↓
RFC-0004 Product Contract / Extensions
        ↓
RFC-0005 Governed Execution / Workflow
        ↓
RFC-0006 Event / Provenance / Observability
        ↓
RFC-0007 Memory / Knowledge / Learning
        ↓
Reference Implementation + ADRs
        ↓
Product-driven validation and capability incubation
```

This is a **default dependency-aware sequence**, not a ban on parallel work.

Parallel work is permitted when the work is bounded and reversible and does not prejudge unresolved higher-level architecture.

## 14. Next canonical action

The current architecture work item is:

> **Begin RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability — using Constitution `1.2.0`, Accepted RFC-0001 `1.0.0` and Accepted RFC-0002 `1.0.0` as the canonical architectural baseline.**

RFC-0003 should resolve the identity-administration, authentication, authorization, isolation, sovereignty and portability mechanisms intentionally deferred by the accepted architecture while preserving the RFC-0002 Kernel metamodel.

## 15. Roadmap maintenance rule

After every accepted RFC, material planning decision, or meaningful implementation milestone:

1. update status and progress in this file;
2. update links and dependencies;
3. increment the roadmap version according to Section 2;
4. commit the update to the canonical repository;
5. do not maintain a competing roadmap in chat, local notes or another repository.

Chats may discuss future roadmap changes, but only the version committed here is canonical.
