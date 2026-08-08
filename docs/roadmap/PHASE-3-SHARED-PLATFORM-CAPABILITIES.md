# Arvectum OS Phase 3 — Shared Platform Capabilities

Status: `Active`
Version: `1.1.3`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M3 — Validated shared capability baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 2 — Core Runtime`, `M2` achieved

## 1. Purpose

Phase 3 proves that a small justified set of domain-neutral shared responsibilities can be implemented above the reusable Core Runtime without product-domain leakage, competing canonical authority, premature public contracts or accidental infrastructure lock-in.

The RFC-0001 capability lifecycle is `Candidate → Incubating → Active → Deprecated → Retired`.

P3.01 admitted four Candidates. P3.02 established bounded incubation envelopes and Provisional domain-neutral capability contracts. R5 passed the pre-implementation boundary review. P3.03 through P3.05 now complete bounded executable slices for CAP-001 through CAP-003 while all retained capabilities remain `Incubating`.

## 2. Current bounded capability set

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional contract; P3.03 bounded slice complete;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional contract; P3.04 bounded slice complete;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional contract, strictly non-authoritative; P3.05 bounded slice complete;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional contract, derived/read-oriented.

Canonical lifecycle catalog: [`PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md).
Canonical P3.02 contract baseline: [`PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md).

## 3. Explicitly deferred / outside capability identity

Generic notification/scheduler/connector marketplace, public SDK/API, product-domain workflows/taxonomies/templates/ontologies/prompts/scoring/business rules, production IAM choice, fixed database/object store/search engine/broker/service topology and customer-facing SLA/support/HA/compliance commitments remain outside the initial capability identity.

## 4. Phase 3 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟩 Complete | `██████████ 100%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | 🟩 Complete | `██████████ 100%` |
| `P3.03` | Document & Artifact Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.04` | Memory & Knowledge Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.05` | Non-authoritative Search / Index Projection candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.06` | Audit / Reconstruction Support candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.09` | Shared-capability reuse and composition proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.10` | Phase 3 architecture fitness matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

## 5. Completed boundary work

P3.01 admitted CAP-001 through CAP-004 as bounded domain-neutral responsibilities. P3.02 moved them to `Incubating` for Phase 3 validation and established Provisional capability contracts. R5 confirmed no accidental service-catalog growth, lifecycle inflation, product-domain leakage, stable-interface leakage or already-crossed durable ADR commitment.

## 6. Completed bounded slices

### P3.03 — CAP-001

Canonical review: [`P3-03-document-artifact-governance-candidate-slice-review.md`](../reviews/P3-03-document-artifact-governance-candidate-slice-review.md) — `PASS`.

Implementation/evidence: `reference/python/arvectum_os_ref/document_artifact_governance.py`; `reference/python/tests/test_p3_03_document_artifact_governance.py`.

### P3.04 — CAP-002

Canonical review: [`P3-04-memory-knowledge-governance-candidate-slice-review.md`](../reviews/P3-04-memory-knowledge-governance-candidate-slice-review.md) — `PASS`.

Implementation/evidence: `reference/python/arvectum_os_ref/memory_knowledge_governance.py`; `reference/python/tests/test_p3_04_memory_knowledge_governance.py`.

The bounded CAP-002 slice proves Observation/Memory/Candidate/Knowledge separation, epistemic-status preservation, distinct validation and approval gates, Organization/purpose/rights/freshness retrieval filtering, derived retrieval non-authority and exact Knowledge Version reliance without Head/rank inference. It selects no durable knowledge/vector/search technology or stable interface.

### P3.05 — CAP-003

Canonical review: [`P3-05-non-authoritative-search-index-projection-candidate-slice-review.md`](../reviews/P3-05-non-authoritative-search-index-projection-candidate-slice-review.md) — `PASS`.

Implementation/evidence: `reference/python/arvectum_os_ref/search_index_projection.py`; `reference/python/tests/test_p3_05_search_index_projection.py`.

The bounded CAP-003 slice proves disposable derived discovery, exact governed source/version attribution, explicit `Current`/`Stale`/`Missing`/`Ambiguous` reconciliation state, fail-closed ordinary discovery for unresolved projection state, current Organization/purpose/right/classification filtering, separate source-access resolution and complete rebuildability. It deliberately defines no shared relevance/ranking contract and selects no durable search/vector/index technology or stable interface.

## 7. Remaining bounded slice

P3.06 proves read-oriented Audit / Reconstruction Support over governed evidence.

P3.10 fitness evidence continues to accumulate from completed bounded slices.

## 8. Later Phase 3 work

P3.07 proves cross-capability security/rights/Organization enforcement. P3.08 proves consumption through an RFC-0004 Provisional Product Contract. P3.09 proves reuse across materially distinct bounded consumers/workflows. P3.10 consolidates fitness evidence. P3.11 independently dispositions each Incubating capability and re-checks ADR/refactoring boundaries. P3.12 decides M3 closure.

## 9. Engineering review gates

R5 is PASS. R6 follows P3.07, R7 follows P3.09, and R8 follows P3.10. Each gate must preserve capability boundaries, dependency direction, security/rights semantics and ADR triggers.

## 10. ADR and Product Contract gates

Re-open the ADR gate before material reliance on concrete durable database/object-store/search/vector topology, transactions/concurrency, Event delivery/store, IAM/PDP/PEP, evidence-integrity technology, stable public/cross-product API/SDK/serialization, durable projection/replay storage or separately deployable service/process topology.

A real Product or Product Experiment relying on P3 capabilities, canonical platform state or shared history must use an RFC-0004 Product Contract. Incubating capability contracts do not grant permissions or authority.

## 11. M3 exit criteria

M3 may be declared achieved only when retained capabilities have explicit lifecycle/ownership/bounded contracts, a small set is executable above M2, composition preserves scope/authority/rights/provenance, RFC-0007/RFC-0008 semantics pass in scope, derived capabilities remain non-authoritative, reuse and Product Contract consumption are proven, P3.10 fitness passes, R5–R8 are complete, crossed ADR gates are governed, and P3.12 passes without unsupported `Active`/production/SLA/public-compatibility claims.

## 12. Current canonical action

> **P3.06 — final initial bounded capability slice; P3.10 evidence continuous.**

P3.03 through P3.05 are complete. Continue CAP-004 without expanding capability identity, stabilizing public/cross-product interfaces, importing product-domain semantics or selecting durable cross-cutting mechanisms without re-opening the ADR gate.
