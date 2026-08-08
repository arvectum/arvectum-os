# Arvectum OS Platform Capability Catalog

Status: `Active`
Version: `1.2.1`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Lifecycle authority: RFC-0001 `1.0.0` — `Accepted`
Phase source: [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](../roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md)

## 1. Purpose and authority

This catalog records the bounded initial Arvectum OS Platform Capability set admitted by P3.01 and its current lifecycle disposition after the P3.11 capability admission / ADR / refactoring hardening review and P3.12 Phase 3 / M3 closure review.

It is subordinate to Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008. It does not create stable public contracts, select infrastructure, authorize production use or make any capability `Active`.

P3.01 admitted four entries as `Candidate`. P3.02 established the RFC-0001 incubation envelope and Provisional domain-neutral capability contracts, allowing all four to move to bounded lifecycle `Incubating` for Phase 3 validation. P3.11 independently re-reviewed each capability after P3.03–P3.10 and R8 evidence and retained exactly the same four as `Incubating / Provisional` for the bounded M3 baseline. P3.12 then closed Phase 3 and achieved M3 without changing those lifecycle states.

Canonical P3.02 contract baseline: [`PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md).
Canonical P3.11 review: [`P3-11-capability-admission-adr-refactoring-hardening-review.md`](../reviews/P3-11-capability-admission-adr-refactoring-hardening-review.md).
Canonical P3.12 closure: [`P3-12-phase-3-m3-closure-review.md`](../reviews/P3-12-phase-3-m3-closure-review.md).

## 2. Current capability summary

| ID | Capability | Lifecycle | Contract | Primary architecture basis | Review |
|---|---|---|---|---|---|
| `CAP-001` | Document & Artifact Governance | `Incubating` | `Provisional` | RFC-0008 | P3.11 PASS; M3 achieved; lifecycle review by `2026-09-08` |
| `CAP-002` | Memory & Knowledge Governance | `Incubating` | `Provisional` | RFC-0007 | P3.11 PASS; M3 achieved; lifecycle review by `2026-09-08` |
| `CAP-003` | Search / Index Projection | `Incubating` | `Provisional` | RFC-0001; RFC-0007; RFC-0008 | P3.11 PASS; M3 achieved; lifecycle review by `2026-09-08` |
| `CAP-004` | Audit / Reconstruction Support | `Incubating` | `Provisional` | RFC-0006; RFC-0005 | P3.11 PASS; M3 achieved; lifecycle review by `2026-09-08` |

`Incubating` authorizes bounded validation work only. It is not production, stable public compatibility, SLA/support or commercial status.

P3.11 confirms that the four capability identities are justified as the retained bounded shared-capability set for M3 evidence. P3.12 confirms M3 closure over that set. Neither is an RFC-0001 `Active` admission decision.

## 3. Retained boundaries

### CAP-001 — Document & Artifact Governance

Reusable identity/version/admission/derivation/exact-version reliance semantics for governed Documents and Artifacts. Product document schemas/types, templates, taxonomies, business approvals and workflows/UX remain product-owned. DMS/object store/filesystem/OCR/conversion/rendering/signing remain replaceable infrastructure.

### CAP-002 — Memory & Knowledge Governance

Reusable Memory/Knowledge lifecycle, retrieval controls, promotion gates, provenance and exact-version reliance without turning observations, AI output or vector state into authority. Domain knowledge, prompts, agents, ontologies, validation/scoring and business learning loops remain product-owned. Vector/search/model/RAG technology remains replaceable.

### CAP-003 — Search / Index Projection

Reusable discovery over governed source identities/versions while projection state remains derived and non-authoritative. Ranking/relevance policy, domain filters/taxonomies, recommendations and UX remain product-owned. Search/vector/index engines and caches remain infrastructure.

P3.11 explicitly retains CAP-003 because the shared responsibility is governed source/version discovery, attribution, current constraint enforcement and exact source resolution—not operation of a generic search vendor. If the abstraction later collapses into commodity search infrastructure alone, the capability must be re-reviewed for containment or retirement.

### CAP-004 — Audit / Reconstruction Support

Reusable read-oriented reconstruction of consequential operations from governed evidence and exact versions. Product compliance interpretation, reports, narratives and review UX remain product-owned. Logging/tracing/SIEM/dashboard/analytical-store technology remains replaceable infrastructure.

R8's fail-closed CAP-004 evidence-constraint remediation is part of the retained security/correctness evidence. It does not create a new capability responsibility or operational-readiness claim.

## 4. P3.02 incubation disposition

Each capability satisfies the RFC-0001 minimum `Incubating` declaration through the canonical P3.02 contract baseline:

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
| Generic connector marketplace / broad adaptor framework | `Deferred / not admitted` | Reconsider only from actual validated multi-consumer evidence and a separate admission decision. |
| Generic composition/orchestration framework extracted from P3.08/P3.09 | `Not admitted` | Consumer composition remains product-owned evidence; two bounded compositions do not justify a new shared capability or workflow DSL. |
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
11. P3.11 admission to the bounded M3 retained set is not `Active` lifecycle promotion.
12. Materially distinct reuse does not by itself authorize a new generic composition capability, Stable Product Contract or public cross-product interface.
13. P3.12/M3 closure changes roadmap milestone state only; it does not alter capability lifecycle, operational environment or conformance maturity.

## 7. P3.11 capability admission disposition

P3.11 reviewed every capability independently using P3.03–P3.09 semantic/reuse evidence, P3.10 architecture fitness and R8 hardening.

| Capability | P3.11 decision | Retention rationale | Required future gate before `Active` |
|---|---|---|---|
| CAP-001 | `Retain Incubating` | Domain-neutral Document/Artifact governance reused across two bounded consumers without product-schema or storage leakage. | Stable supported contract, compatibility/migration, operational support/readiness and external reliance evidence. |
| CAP-002 | `Retain Incubating` | Domain-neutral Memory/Knowledge lifecycle and retrieval semantics reused without promoting product truth, prompts, ontologies or vector state into authority. | Stable supported contract, operational support/readiness, durable mechanism decisions as needed and external reliance evidence. |
| CAP-003 | `Retain Incubating` | Governed discovery semantics reused over materially distinct Document and Knowledge sources while projection stays non-authoritative and rebuildable. | Stable supported discovery contract, operational freshness/support model, governed durable topology if selected and external reliance evidence. |
| CAP-004 | `Retain Incubating` | Cross-cutting reconstruction semantics reused across bounded consumers; R8 fail-closed defect is remediated with negative-path evidence. | Stable supported reconstruction contract, operational evidence/support/retention readiness, integrity/topology decisions if selected and external reliance evidence. |

The P3.11 disposition table intentionally does not repeat the canonical backticked catalog-row syntax used by the current capability summary; the summary remains the unique machine-readable current-state row set consumed by the Phase 3 fitness evidence.

No capability is returned to product scope, replaced or retired at P3.11. No fifth capability is admitted from the reuse/composition harnesses.

P3.11 also concludes that no current concrete implementation mechanism crosses the ADR threshold and no material shared refactor is justified after R8. Those decisions are recorded in the canonical P3.11 review rather than implied by this catalog.

## 8. Lifecycle history

| Date | Work item | Disposition |
|---|---|---|
| `2026-08-08` | P3.01 | CAP-001 through CAP-004 admitted as `Candidate`; no implementation commitment. |
| `2026-08-08` | P3.02 | CAP-001 through CAP-004 moved to bounded `Incubating` with Provisional domain-neutral capability contracts; no `Active` promotion. |
| `2026-08-08` | P3.11 | CAP-001 through CAP-004 independently retained as `Incubating / Provisional` for the bounded M3 baseline; no Active promotion, new capability admission, ADR or material refactor. |
| `2026-08-08` | P3.12 | Phase 3 closed and M3 achieved for the bounded shared-capability reference scope; capability lifecycle remains unchanged at `Incubating / Provisional`. |

## 9. Next review

P3.12 is complete and M3 is achieved. This milestone does not promote capability lifecycle.

Re-open capability review no later than `2026-09-08` or earlier before any material `Active` admission, Stable/public contract, durable ADR-triggering mechanism, external production reliance or material capability-boundary change.

Any `Active` proposal must independently satisfy RFC-0001 stable-contract, compatibility/migration, accountable support, operational-readiness and applicable decision-authority requirements rather than relying on M3 closure as substitute evidence.
