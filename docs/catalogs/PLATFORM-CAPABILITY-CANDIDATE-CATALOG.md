# Arvectum OS Platform Capability Catalog

Status: `Active`
Version: `1.1.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Lifecycle authority: RFC-0001 `1.0.0` — `Accepted`
Phase source: [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](../roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md)

## 1. Purpose and authority

This catalog records the bounded initial Arvectum OS Platform Capability set admitted by P3.01 and its current lifecycle disposition after P3.02.

It is subordinate to Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008. It does not create stable public contracts, select infrastructure, authorize production use or make any capability `Active`.

P3.01 admitted four entries as `Candidate`. P3.02 established the RFC-0001 incubation envelope and Provisional domain-neutral capability contracts, allowing all four to move to bounded lifecycle `Incubating` for Phase 3 validation.

Canonical P3.02 contract baseline: [`PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md).

## 2. Current capability summary

| ID | Capability | Lifecycle | Contract | Primary architecture basis | Review |
|---|---|---|---|---|---|
| `CAP-001` | Document & Artifact Governance | `Incubating` | `Provisional` | RFC-0008 | P3.11 or `2026-09-08` |
| `CAP-002` | Memory & Knowledge Governance | `Incubating` | `Provisional` | RFC-0007 | P3.11 or `2026-09-08` |
| `CAP-003` | Search / Index Projection | `Incubating` | `Provisional` | RFC-0001; RFC-0007; RFC-0008 | P3.11 or `2026-09-08` |
| `CAP-004` | Audit / Reconstruction Support | `Incubating` | `Provisional` | RFC-0006; RFC-0005 | P3.11 or `2026-09-08` |

`Incubating` authorizes bounded validation work only. It is not production, stable public compatibility, SLA/support or commercial status.

## 3. Retained boundaries

### CAP-001 — Document & Artifact Governance

Reusable identity/version/admission/derivation/exact-version reliance semantics for governed Documents and Artifacts. Product document schemas/types, templates, taxonomies, business approvals and workflows/UX remain product-owned. DMS/object store/filesystem/OCR/conversion/rendering/signing remain replaceable infrastructure.

### CAP-002 — Memory & Knowledge Governance

Reusable Memory/Knowledge lifecycle, retrieval controls, promotion gates, provenance and exact-version reliance without turning observations, AI output or vector state into authority. Domain knowledge, prompts, agents, ontologies, validation/scoring and business learning loops remain product-owned. Vector/search/model/RAG technology remains replaceable.

### CAP-003 — Search / Index Projection

Reusable discovery over governed source identities/versions while projection state remains derived and non-authoritative. Ranking/relevance policy, domain filters/taxonomies, recommendations and UX remain product-owned. Search/vector/index engines and caches remain infrastructure.

### CAP-004 — Audit / Reconstruction Support

Reusable read-oriented reconstruction of consequential operations from governed evidence and exact versions. Product compliance interpretation, reports, narratives and review UX remain product-owned. Logging/tracing/SIEM/dashboard/analytical-store technology remains replaceable infrastructure.

## 4. P3.02 incubation disposition

Each capability now satisfies the RFC-0001 minimum `Incubating` declaration through the canonical P3.02 contract baseline:

- source organizational need;
- sponsoring validation consumers;
- bounded scope/budget;
- Provisional domain-neutral capability contract;
- Canonical Record/authority responsibilities;
- dependencies and Event/evidence interactions;
- security, authority and data-handling rules;
- portability, compatibility and migration requirements;
- promotion, return-to-product, replacement and retirement criteria.

Accountable architectural owner for all four bounded incubation contracts is `ООО «Арвектум»` — platform architecture owner.

## 5. Explicit non-admission / containment

The following remain outside the initial capability set unless later evidence produces a separate admission decision:

| Item | Disposition | Boundary |
|---|---|---|
| Generic notification service | `Deferred / not admitted` | Product-local or commodity integration until validated organizational-semantic reuse exists. |
| Generic scheduler | `Deferred / not admitted` | Scheduling technology is not itself a Platform Capability. |
| Generic connector marketplace / broad adaptor framework | `Deferred / not admitted` | Reconsider only from actual P3.09 multi-consumer evidence. |
| Public SDK/API | `Deferred / not admitted` | Stable external developer surface would create compatibility obligations prematurely. |
| Production IAM / policy engine | `Deferred as implementation choice` | RFC-0003 semantics apply; concrete IAM/PDP/PEP technology requires an ADR-gate assessment before material reliance. |
| Fixed database/object-store/search-engine/broker/service topology | `Not a capability` | Durable infrastructure selection remains replaceable and subordinate to ADR when triggered. |
| Product-domain workflows/schemas/prompts/taxonomies/templates/ontologies/scoring/business rules | `Product-owned` | Domain expertise remains in products unless separately promoted through evidence-based admission. |
| Customer-facing SLA/support/HA/archival/compliance commitments | `Not created` | Require separate operational/commercial authority and readiness. |

## 6. Cross-capability invariants

1. `Incubating` is not `Active` and creates no production/support claim.
2. A real Product relying on these capabilities, canonical platform state or shared history must use an RFC-0004 Product Contract.
3. Product Contract possession or capability contract declaration grants neither authorization nor Organizational Authority.
4. Product-specific semantics remain product-owned.
5. Search/index, retrieval representations and reconstruction views remain derived/non-authoritative.
6. External authority is preserved through declared authority modes; no competing source of truth may be created.
7. Cross-Organization access/reuse is denied by default absent explicit rights and governance.
8. Concrete durable persistence, transaction, Event delivery, IAM, evidence-integrity, stable API/serialization, projection storage or service-topology choices re-open the ADR gate.
9. Portability/rebuildability and exit paths must remain explicit throughout incubation.
10. No capability may become `Active` without separate RFC-0001 admission, approved operational readiness and applicable decision authority.

## 7. Lifecycle history

| Date | Work item | Disposition |
|---|---|---|
| `2026-08-08` | P3.01 | CAP-001 through CAP-004 admitted as `Candidate`; no implementation commitment. |
| `2026-08-08` | P3.02 | CAP-001 through CAP-004 moved to bounded `Incubating` with Provisional domain-neutral capability contracts; no `Active` promotion. |

## 8. Next review

R5 must review the P3.02 boundaries before broad capability implementation expands.

P3.11 must independently decide for each capability whether evidence supports continued incubation, containment/return, replacement, retirement or a separate `Active` admission process.
