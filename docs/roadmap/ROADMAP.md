# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `1.2.2`
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

### 2.1 Identifier namespaces

Roadmap block identifiers and RFC identifiers are **independent namespaces** and MUST NOT be inferred from one another.

| Identifier | Namespace | Canonical meaning |
|---|---|---|
| `0H` | Roadmap block | `Reference implementation readiness` — a non-RFC delivery/readiness milestone |
| `RFC-0008` | RFC | `Document and Artifact Architecture` — Accepted architecture RFC |

Rules:

- a roadmap block such as `0H` is never shorthand for `RFC-0008`;
- an RFC number is assigned only to an RFC artifact listed through the RFC governance process and RFC Index;
- non-RFC implementation, readiness, delivery or validation milestones MAY appear between RFCs in the roadmap without consuming an RFC number;
- the informative follow-up sequence in RFC-0001 does not require every intervening roadmap milestone to become an RFC;
- when referring to the completed readiness work, use `Block 0H — Reference implementation readiness` or `Reference implementation readiness`, not `RFC-0008 readiness`;
- `RFC-0008` refers only to `Document and Artifact Architecture` unless a future properly governed RFC change explicitly changes that assignment.

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
| 🟨 0H | Reference implementation readiness — non-RFC milestone | 🟩 | `██████████ 100%` |

RFC-0008 was intentionally prepared and accepted after Phase 0 readiness as a parallel architecture refinement. It does not retroactively change the Phase 0 completion boundary.

## 5. Block 0A — Governance baseline

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Completed

- 🟩 Constitution `1.2.0` — `Ratified`;
- 🟩 RFC Index established;
- 🟩 RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- 🟩 canonical roadmap established in this file;
- 🟩 repository agent rules identify governance work as a first-class task classification;
- 🟩 Constitution amendment provenance for `1.0.0 → 1.1.0 → 1.2.0` recovered from immutable Git history and indexed;
- 🟩 historical legacy/current `RFC-0001` identifier collision documented without renumbering current Accepted RFCs;
- 🟩 [`Constitution 1.2.0 Provenance Record`](../governance/CONSTITUTION-PROVENANCE.md) closed under [`DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR`](../governance/decisions/DECISION-2026-08-07-CONSTITUTION-1.2-PROVENANCE-REPAIR.md).

### Governance provenance closure

The former Constitution `1.2.0` provenance debt is resolved. Original historical amendment artifacts, resulting Constitution transitions and explicit owner approval were verified from immutable Git history. The RFC Index records the legacy amendment namespace and the historical identifier collision explicitly.

No unresolved Phase 0 governance provenance debt remains.

### Exit criterion

There is one canonical architecture baseline and one canonical planning source in the repository.

## 6. Block 0B — Architecture language baseline

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Objective

Create a shared vocabulary before further detailed architecture work so that contributors, products and AI agents use the same terms consistently.

### Deliverable

Published and synchronized:

- 🟩 [`docs/architecture/GLOSSARY.md`](../architecture/GLOSSARY.md) — Arvectum OS Architecture Glossary `1.3.0`, aligned through Accepted RFC-0008.

The glossary provides current navigation for architectural terms established by the Constitution and Accepted RFCs, including Organization/Tenant, Kernel primitives, Product Contract, Governed Execution, Event/Provenance, Memory/Knowledge and Document/Artifact architecture.

### Constraint

The glossary is a language and navigation artifact. It summarizes terms from higher-authority sources and does not create new architectural obligations or silently redefine Accepted RFC terminology.

### Exit criterion

🟩 Achieved: a contributor can resolve the meaning and canonical source of core Arvectum OS terms without relying on chat history or model memory.

## 7. Block 0C — RFC-0002: Kernel metamodel

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### Canonical scope

RFC-0002 is `Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model` and establishes the stable five-primitive Kernel metamodel, identity/version semantics, Canonical Lineage/Head/Effective Version, authority modes, relationship semantics, organizational-asset designation and migration constraints.

### Completed

- 🟩 RFC-0002 `1.0.0` — `Accepted`;
- 🟩 owner approval recorded independently in [`DECISION-2026-08-07-RFC-0002-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0002-ACCEPTANCE.md);
- 🟩 structured draft review and cross-section validation completed;
- 🟩 RFC Index and glossary synchronized.

### Accepted boundary

Within RFC-0002 scope, the Kernel metamodel is no longer provisional. Acceptance does not select a physical database model or other implementation technology.

### Exit criterion

🟩 Achieved: RFC-0002 is `Accepted` with prior owner approval evidence and synchronized canonical navigation.

## 8. Block 0D — RFC-0003: Identity, security, privacy, tenant sovereignty and portability

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### RFC

`RFC-0003 — Identity, Security, Privacy, Tenant Sovereignty and Portability`

### Completed

- 🟩 working draft and functional cross-review completed;
- 🟩 reviewed proposal published;
- 🟩 owner approval recorded independently in [`DECISION-2026-08-07-RFC-0003-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0003-ACCEPTANCE.md);
- 🟩 [`RFC-0003`](../rfc/RFC-0003-identity-security-privacy-tenant-sovereignty-portability.md) published as `Accepted 1.0.0`;
- 🟩 RFC Index synchronized with acceptance evidence.

### Accepted boundary

RFC-0003 `1.0.0` is binding architecture for identity administration, authentication, authorization, Organizational Authority separation, tenant isolation, privacy/data governance, cross-organization sharing constraints, privileged/break-glass access and portability.

### Exit criterion

🟩 Achieved: the platform has accepted domain-neutral security, privacy, identity, authority and sovereignty semantics.

## 9. Block 0E — RFC-0004: Product Contract, Product Experiment and Extension Model

**Status:** 🟩 Complete — `Accepted`  
**Progress:** `██████████ 100%`

### RFC

[`RFC-0004 — Product Contract, Product Experiment and Extension Model`](../rfc/RFC-0004-product-contract-product-experiment-extension-model-v1.0.0.md) — `Accepted 1.0.0`.

### Completed

- 🟩 complete working draft and functional cross-review completed;
- 🟩 reviewed proposal `0.3.0` preserved with immutable proposal blob `5a413a240588677211ad56f3a23b30a65d1c4334`;
- 🟩 owner approval recorded in [`DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR`](../governance/decisions/DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR.md);
- 🟩 compatibility re-check against Accepted RFC-0003 completed;
- 🟩 RFC-0004 published as `Accepted 1.0.0`;
- 🟩 RFC Index synchronized.

### Accepted boundary

RFC-0004 is binding architecture for Product Contract identity/version/lifecycle semantics, bounded Product Experiments, explicit capability/canonical-state/operation/Event/Artifact boundaries, extension registration and compatibility/migration/deprecation rules.

### Exit criterion

🟩 Achieved: products can interact with Arvectum OS through an explicit, versioned and governed boundary without leaking product business logic into the platform.

## 10. Block 0F — Governed execution, events and provenance

**Status:** 🟩 Complete — RFC-0005 and RFC-0006 `Accepted 1.0.0`  
**Progress:** `██████████ 100%`

### RFCs

1. `RFC-0005 — Governed Execution and Workflow Model`;
2. `RFC-0006 — Event, Provenance and Observability Model`.

### Completed

- 🟩 RFC-0005 review, owner approval and `Accepted 1.0.0` publication completed;
- 🟩 RFC-0006 review, owner approval and `Accepted 1.0.0` publication completed;
- 🟩 RFC Index synchronized with approval and publication evidence.

### Accepted Block 0F boundary

RFC-0005 establishes domain-neutral Governed Execution and Workflow semantics. RFC-0006 establishes Event, Provenance and Observability semantics. Together they support reconstructable consequential state change without selecting workflow, broker or observability technologies.

### Exit criterion

🟩 Achieved: consequential execution and operational history have accepted domain-neutral models sufficient for explainability, reconstruction and controlled state change.

## 11. Block 0G — Memory, knowledge and governed learning

**Status:** 🟩 Complete — RFC-0007 `Accepted 1.0.0`  
**Progress:** `██████████ 100%`

### RFC

[`RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle`](../rfc/RFC-0007-memory-knowledge-governed-learning-lifecycle-v1.0.0.md) — `Accepted 1.0.0`.

### Completed

- 🟩 functional cross-review completed after 4 of maximum 7 iterations with result `Pass after bounded reconciliation`;
- 🟩 reviewed RFC-0007 `0.2.0` published;
- 🟩 explicit owner approval recorded independently in [`DECISION-2026-08-07-RFC-0007-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0007-ACCEPTANCE.md);
- 🟩 RFC-0007 published as `Accepted 1.0.0`;
- 🟩 RFC Index synchronized.

### Accepted boundary

RFC-0007 is binding architecture for Observation, Organizational Memory, Knowledge Candidate, Improvement Proposal, validated Knowledge, governed promotion, AI authority boundaries and non-authoritative retrieval/index projections.

### Exit criterion

🟩 Achieved: the platform distinguishes observations, memory, validated knowledge and proposals without silent AI-driven mutation of governed state.

## 12. Block 0H — Reference implementation readiness — non-RFC milestone

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Objective

Make the smallest useful reference implementation startable after the foundational semantic RFC sequence through RFC-0007, without introducing speculative technology or cross-cutting architecture in code.

### Completed

- 🟩 [`Reference Implementation Readiness Baseline`](../implementation/REFERENCE-IMPLEMENTATION-READINESS.md) `1.0.0` published;
- 🟩 logical modular-monolith implementation structure defined without fixing permanent service topology;
- 🟩 first domain-neutral executable slice and failure cases defined;
- 🟩 minimum architecture fitness matrix mapped to RFC-0001 through RFC-0007;
- 🟩 security/privacy/Organization-scope bootstrap constraints defined;
- 🟩 Product Contract entry condition for real product interaction defined;
- 🟩 ADR trigger criteria defined;
- 🟩 minimum ADR set before the first in-memory/in-process slice assessed as `zero`;
- 🟩 functional cross-review completed after 3 of maximum 7 iterations with result `Pass after bounded reconciliation`;
- 🟩 explicit owner confirmation of completion recorded in [`DECISION-2026-08-07-BLOCK-0H-REFERENCE-IMPLEMENTATION-READINESS-CONFIRMATION`](../governance/decisions/DECISION-2026-08-07-BLOCK-0H-REFERENCE-IMPLEMENTATION-READINESS-CONFIRMATION.md) — `Approved`.

### Readiness boundary

The first reference implementation may begin with domain-neutral semantic modules, in-memory persistence ports, in-process application calls and executable fitness fixtures.

No programming language, database, API protocol, event broker, workflow engine, IAM provider, policy engine, vector store, LLM/model provider, cloud topology or permanent package structure is selected by Block 0H.

Reference implementation readiness is not operational readiness and does not make any capability `Active`.

### Exit criterion for Phase 0

🟩 **Achieved. Phase 0 is complete and explicitly confirmed by the Owner.**

## 13. Post-Phase-0 architecture and delivery state

The reference implementation delivery track remains ready:

```text
Roadmap Block 0H — Reference implementation readiness
(non-RFC milestone)                     ✅ COMPLETE + OWNER CONFIRMED
        ↓
First bounded executable slice          🟦 READY / MAY PROCEED
```

The architecture RFC track is now:

```text
RFC-0007 — Memory, Knowledge and Governed Learning Lifecycle  ✅ ACCEPTED 1.0.0
        ↓
RFC-0008 — Document and Artifact Architecture                ✅ ACCEPTED 1.0.0
```

RFC-0008 acceptance does not retroactively make it a prerequisite for a bounded slice that does not rely on Document/Artifact semantics. Where future implementation does rely on shared Document/Artifact semantics, Accepted RFC-0008 is now binding.

### RFC-0008 completed

- 🟩 Constitution `1.2.0`, RFC Index and Accepted RFC-0001 through RFC-0007 re-verified before substantive work;
- 🟩 RFC-0008 `0.1.0` working draft published;
- 🟩 functional cross-review completed after 4 of maximum 7 iterations;
- 🟩 review result: `Pass after bounded reconciliation`;
- 🟩 review evidence published in [`docs/reviews/RFC-0008-functional-cross-review.md`](../reviews/RFC-0008-functional-cross-review.md);
- 🟩 all bounded reconciliation items incorporated into reviewed proposal `0.2.0`;
- 🟩 reviewed proposal preserved by immutable blob SHA `0de6a1dead4e06605d72d0781505bb44598d752a`;
- 🟩 explicit owner approval recorded independently in [`DECISION-2026-08-07-RFC-0008-ACCEPTANCE`](../governance/decisions/DECISION-2026-08-07-RFC-0008-ACCEPTANCE.md), approval commit `9b104307dc1ee2e04ac65146b6beb73db0d13019`;
- 🟩 [`RFC-0008 — Document and Artifact Architecture`](../rfc/RFC-0008-document-artifact-architecture-v1.0.0.md) published as `Accepted 1.0.0`, publication commit `230fb452f5aa8688950056cf1c4965840803c835`;
- 🟩 RFC Index synchronized with acceptance evidence;
- 🟩 Architecture Glossary synchronized to `1.3.0` through Accepted RFC-0008;
- 🟩 repository README synchronized to Accepted RFC-0008;
- 🟩 roadmap synchronized to this accepted state.

### Accepted RFC-0008 boundary

RFC-0008 `1.0.0` is binding domain-neutral architecture for logical Document identity, immutable Document Versions, Artifact representations, Working Copies, governed content resolution/manifests, renditions, external document authority, generation/admission, transformation/redaction, signature/approval evidence, exact-version reliance, packages, security/privacy propagation, portability/export and migration.

It introduces no new Kernel primitive and selects no DMS, object store, database, file format, OCR engine, signing provider, search engine, workflow engine or service topology.

Acceptance does not make any document/artifact Platform Capability `Active`, establish production/operational readiness, create SLA/support/archival/legal-signature commitments, or approve product-specific document taxonomies, templates or workflows.

## 14. Next canonical action

The current delivery action remains:

> **Implement the first bounded reference implementation executable slice defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`: prove stable identities, immutable canonical versions, explicit Organization/authority gates, Governed Execution mutation, canonical Event evidence, provenance and Observation non-promotion with executable tests before adding infrastructure.**

Accepted RFC-0008 must be applied if that slice or a later slice begins to implement shared Document/Artifact semantics.

For implementation:

- prefer the simplest reversible solution;
- keep product-domain semantics out of shared modules;
- use an ADR before a concrete choice crosses the readiness document's ADR gate;
- do not treat working code or RFC acceptance as an `Active` Platform Capability or production-readiness evidence by itself.

Naming rule:

- completed readiness work = `Block 0H` / `Reference implementation readiness`;
- accepted document/artifact architecture = `RFC-0008` / `RFC-0008 — Document and Artifact Architecture`;
- never use `RFC-0008` as a label for Block 0H.

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
