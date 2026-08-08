# Arvectum OS Phase 3 — Shared Platform Capabilities

Status: `Active`
Version: `1.1.1`
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

P3.01 admitted four Candidates. P3.02 established bounded incubation envelopes and Provisional domain-neutral capability contracts. R5 passed the pre-implementation boundary review. P3.03 now completes the first executable bounded slice for CAP-001 while retaining lifecycle `Incubating`.

## 2. Current bounded capability set

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional contract; P3.03 bounded slice complete;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional contract;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional contract, strictly non-authoritative;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional contract, derived/read-oriented.

Canonical lifecycle catalog: [`PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md).

Canonical P3.02 contract baseline: [`PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md).

## 3. Explicitly deferred / outside capability identity

The following remain outside the initial P3 capability set unless later evidence changes the disposition:

- generic notification service;
- generic scheduler;
- generic connector marketplace/broad adaptor framework;
- public SDK/API;
- product-domain workflows, taxonomies, templates, ontologies, prompts, scoring and business rules;
- production IAM/policy-engine product choice;
- fixed database, object store, search engine, broker or service topology;
- customer-facing SLA/support/HA/compliance commitments.

## 4. Phase 3 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟩 Complete | `██████████ 100%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | 🟩 Complete | `██████████ 100%` |
| `P3.03` | Document & Artifact Governance candidate slice | 🟩 Complete | `██████████ 100%` |
| `P3.04` | Memory & Knowledge Governance candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.05` | Non-authoritative Search / Index Projection candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.06` | Audit / Reconstruction Support candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.09` | Shared-capability reuse and composition proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.10` | Phase 3 architecture fitness matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

## 5. Completed boundary work

P3.01 admitted CAP-001 through CAP-004 as bounded domain-neutral responsibilities. P3.02 moved them to `Incubating` for Phase 3 validation and established Provisional capability contracts. R5 confirmed no accidental service-catalog growth, lifecycle inflation, product-domain leakage, stable-interface leakage or already-crossed durable ADR commitment.

## 6. P3.03 completion evidence

P3.03 implements `CAP-001 — Document & Artifact Governance` in the internal reference Python harness without creating a DMS or stable interface.

Canonical review: [`P3-03-document-artifact-governance-candidate-slice-review.md`](../reviews/P3-03-document-artifact-governance-candidate-slice-review.md) — `PASS`.

Executable implementation/evidence:

- `reference/python/arvectum_os_ref/document_artifact_governance.py`;
- `reference/python/tests/test_p3_03_document_artifact_governance.py`.

The bounded slice proves stable logical Document identity, immutable Document Version identity, explicit Artifact/content identity, transient-versus-governed admission, designated rendition/manifest association, derivation provenance, handling-constraint propagation, exact Document Version + Artifact reliance and storage/hash non-authority. It composes existing `CanonicalRecord`, `CanonicalLineage` and `OrganizationScope` owners rather than creating competing runtime semantics.

P3.03 selects no durable persistence/object store, transaction mechanism, Event transport, IAM provider, evidence-integrity technology, stable serialization/API or service topology. No ADR gate is crossed. CAP-001 remains `Incubating`; P3.03 does not establish operational readiness or `Active` status.

## 7. Remaining bounded slices

### P3.04 — Memory & Knowledge Governance candidate slice

Implement a bounded RFC-0007 shared slice preserving Observation ≠ Memory ≠ Knowledge Candidate ≠ validated Knowledge, governed retrieval, explicit promotion, exact-version attribution, validation/authority separation, AI non-authority and non-canonical derived retrieval state.

### P3.05 — Non-authoritative Search / Index Projection candidate slice

Prove reusable discovery/index behavior with exact source/version attribution, visible stale/missing state, source resolution before consequential reliance, rebuild/replay and replaceable search technology.

### P3.06 — Audit / Reconstruction Support candidate slice

Expose bounded read-oriented reconstruction of execution, actor/authority, Product Contract, workflow/material inputs, Event causation/correlation and output versions while preserving missing/redacted/deleted evidence semantics.

P3.04–P3.06 may proceed in bounded parallel. P3.10 fitness evidence accumulates continuously.

## 8. Later Phase 3 work

P3.07 proves cross-capability security/rights/Organization enforcement. P3.08 proves consumption through an RFC-0004 Provisional Product Contract. P3.09 proves reuse across materially distinct bounded consumers/workflows. P3.10 consolidates fitness evidence. P3.11 independently dispositions each Incubating capability and re-checks ADR/refactoring boundaries. P3.12 decides M3 closure.

## 9. Engineering review gates

| Gate | Trigger | Purpose |
|---|---|---|
| `R5 — Capability Boundary Review` | after P3.02 | 🟩 PASS — boundary checked before implementation expansion |
| `R6 — Cross-Capability Health Review` | after P3.07 | review duplicate semantics, security/rights propagation, dependency direction and ADR triggers |
| `R7 — Reuse Refactoring Review` | after P3.09 | refactor only abstractions justified by actual reuse |
| `R8 — M3 Hardening Review` | after P3.10 | final code health, fitness, unsafe dependency, capability-status and evidence-backed optimization pass |

## 10. ADR and Product Contract gates

Re-open the ADR gate before material reliance on concrete durable database/object-store/search topology, transactions/concurrency, Event delivery/store, IAM/PDP/PEP, evidence-integrity technology, stable public/cross-product API/SDK/serialization, durable projection/replay storage or separately deployable service/process topology.

A real Product or Product Experiment relying on P3 capabilities, canonical platform state or shared history must use an RFC-0004 Product Contract. Incubating capability contracts do not themselves grant permissions or authority.

## 11. M3 exit criteria

M3 may be declared achieved only when retained capabilities have explicit lifecycle/ownership/bounded contracts, a small set is executable above M2, composition preserves scope/authority/rights/provenance, RFC-0007/RFC-0008 semantics pass in scope, derived capabilities remain non-authoritative, reuse and Product Contract consumption are proven, P3.10 fitness passes, R5–R8 are complete, crossed ADR gates are governed, and P3.12 passes without unsupported `Active`/production/SLA/public-compatibility claims.

## 12. Current canonical action

> **P3.04–P3.06 — remaining bounded capability slices; P3.10 evidence continuous.**

P3.03 is complete. Continue the remaining bounded Incubating slices without expanding capability identity, stabilizing public/cross-product interfaces, importing product-domain semantics or selecting durable cross-cutting mechanisms without re-opening the ADR gate.
