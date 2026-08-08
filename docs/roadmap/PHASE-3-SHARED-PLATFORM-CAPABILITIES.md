# Arvectum OS Phase 3 — Shared Platform Capabilities

Status: `Active`
Version: `1.1.0`
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

The RFC-0001 capability lifecycle is:

`Candidate → Incubating → Active → Deprecated → Retired`

P3.01 admitted four Candidates. P3.02 has now established bounded incubation envelopes and Provisional domain-neutral capability contracts for all four. `Incubating` remains sufficient for Phase 3 validation; `Active` requires separate admission and operational readiness and is not an automatic M3 outcome.

## 2. Current bounded capability set

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional contract;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional contract;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional contract, strictly non-authoritative;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional contract, derived/read-oriented.

Canonical lifecycle catalog: [`PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md).

Canonical P3.02 contract baseline: [`PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`](../contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md).

P3.02 review: [`P3-02-capability-lifecycle-ownership-provisional-contract-review.md`](../reviews/P3-02-capability-lifecycle-ownership-provisional-contract-review.md) — `PASS`.

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
| `P3.03` | Document & Artifact Governance candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.04` | Memory & Knowledge Governance candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.05` | Non-authoritative Search / Index Projection candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.06` | Audit / Reconstruction Support candidate slice | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.07` | Cross-capability security, rights and Organization-scope enforcement | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.08` | Product Contract consumption boundary + bounded consumer proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.09` | Shared-capability reuse and composition proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.10` | Phase 3 architecture fitness matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P3.11` | Capability admission / ADR / refactoring hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P3.12` | Phase 3 / M3 closure review | ⬜ | `░░░░░░░░░░ 0%` |

## 5. P3.01 completion evidence

P3.01 admitted the four bounded domain-neutral responsibilities as RFC-0001 Candidates and explicitly kept product-domain behavior, generic utilities and commodity infrastructure outside capability identity. No lifecycle inflation, infrastructure selection, stable public contract or production claim occurred.

Canonical review: [`P3-01-capability-boundary-revalidation-review.md`](../reviews/P3-01-capability-boundary-revalidation-review.md).

## 6. P3.02 completion evidence

P3.02 records for CAP-001 through CAP-004:

- lifecycle transition `Candidate → Incubating` for bounded Phase 3 validation;
- accountable architectural owner `ООО «Арвектум»`;
- source organizational need and sponsoring validation consumers;
- bounded scope/budget;
- Provisional domain-neutral capability contract;
- Canonical Record and authority responsibilities;
- dependencies and Event/evidence interactions;
- security, authority and data-handling constraints;
- portability, compatibility and migration requirements;
- promotion/return/replacement/retirement criteria.

P3.02 creates no RFC-0004 Product Contract for a real product. P3.08 remains responsible for the bounded product-style consumer and its Provisional Product Contract.

No concrete durable persistence/search/Event/IAM/API/serialization/service-topology choice is selected, so no new ADR is justified by P3.02 itself.

## 7. Detailed remaining tasks

### P3.03 — Document & Artifact Governance candidate slice

Implement a bounded RFC-0008 shared slice using Core Runtime semantics: logical Document identity, immutable versions, governed admission/checkpoint, Artifact/content identity where applicable, derivation provenance, exact-version reliance, transient/canonical distinction and replaceable storage.

### P3.04 — Memory & Knowledge Governance candidate slice

Implement a bounded RFC-0007 shared slice preserving Observation ≠ Memory ≠ Knowledge Candidate ≠ validated Knowledge, governed retrieval, explicit promotion, exact-version attribution, validation/authority separation, AI non-authority and non-canonical derived retrieval state.

### P3.05 — Non-authoritative Search / Index Projection candidate slice

Prove reusable discovery/index behavior with exact source/version attribution, visible stale/missing state, source resolution before consequential reliance, rebuild/replay and replaceable search technology.

### P3.06 — Audit / Reconstruction Support candidate slice

Expose bounded read-oriented reconstruction of execution, actor/authority, Product Contract, workflow/material inputs, Event causation/correlation and output versions while preserving missing/redacted/deleted evidence semantics.

### P3.07 — Cross-capability security, rights and Organization-scope enforcement

Prove fail-closed composition across Organization isolation, authorization/authority separation, classification/purpose/rights, derivation constraints and Product Contract non-authority.

### P3.08 — Product Contract consumption boundary + bounded consumer proof

Demonstrate a bounded product-style consumer using one or more Incubating capability contracts through an RFC-0004 Provisional Product Contract rather than implementation internals.

### P3.09 — Shared-capability reuse and composition proof

Demonstrate reuse by at least two materially distinct bounded consumers/workflows and decide from evidence whether any connector/adaptor pattern is genuinely shared.

### P3.10 — Phase 3 architecture fitness matrix

Accumulate executable evidence continuously for domain neutrality, lifecycle integrity, Organization isolation, authority separation, exact provenance/versioning, Product Contract boundaries, rights propagation, AI non-authority, portability/rebuildability, no hidden product coupling, no accidental stable public interface and no undeclared ADR dependency.

### P3.11 — Capability admission / ADR / refactoring hardening review

Independently disposition each Incubating capability based on evidence; review ADR triggers, Product Contract boundaries, dependency direction, duplicate semantics and migration/reversibility. `Active` promotion requires a separate complete RFC-0001 admission/readiness decision.

### P3.12 — Phase 3 / M3 closure review

Decide whether M3 is achieved within an explicitly bounded scope and synchronize the parent roadmap.

## 8. Dependency-aware sequence

```text
M2 ✅
 │
 ▼
P3.01 Candidate catalog / boundary revalidation ✅
 │
 ▼
P3.02 Lifecycle + Provisional contracts ✅
 │
 ▼
R5 Capability Boundary Review ← current
 │
 ├──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼              ▼
P3.03          P3.04          P3.05          P3.06
Documents      Knowledge      Search          Audit
 └──────────────┴───────┬──────┴──────────────┘
                        ▼
                     P3.07
                        │
                        ▼
                     P3.08
                        │
                        ▼
                     P3.09
                        │
                        ▼
                     P3.11
                        │
                        ▼
                     P3.12
```

`P3.10` is cross-cutting throughout the phase.

## 9. Engineering review gates

| Gate | Trigger | Purpose |
|---|---|---|
| `R5 — Capability Boundary Review` | after P3.02 | detect accidental service-catalog growth, lifecycle inflation and contract leakage before implementation expands |
| `R6 — Cross-Capability Health Review` | after P3.07 | review duplicate semantics, security/rights propagation, dependency direction and ADR triggers |
| `R7 — Reuse Refactoring Review` | after P3.09 | refactor only abstractions justified by actual reuse |
| `R8 — M3 Hardening Review` | after P3.10 | final code health, fitness, unsafe dependency, capability-status and evidence-backed optimization pass |

## 10. ADR and Product Contract gates

Re-open the ADR gate before material reliance on concrete durable database/object-store/search topology, transactions/concurrency, Event delivery/store, IAM/PDP/PEP, evidence-integrity technology, stable public/cross-product API/SDK/serialization, durable projection/replay storage or separately deployable service/process topology.

A real Product or Product Experiment relying on P3 capabilities, canonical platform state or shared history must use an RFC-0004 Product Contract. Incubating capability contracts do not themselves grant permissions or authority.

## 11. M3 exit criteria

M3 may be declared achieved only when:

1. retained capabilities have explicit lifecycle/ownership/bounded contracts;
2. a small set is executable above M2 Core Runtime;
3. composition preserves Organization scope, authorization/authority separation, rights and provenance;
4. RFC-0007/RFC-0008 semantics pass in scope;
5. search/index and reconstruction remain derived/non-authoritative;
6. at least two materially distinct bounded consumers/workflows demonstrate reuse;
7. Product Contract consumption avoids hidden coupling;
8. P3.10 fitness evidence passes;
9. R5–R8 complete and findings are dispositioned;
10. crossed ADR gates are governed;
11. no product-domain leakage or unsupported `Active`/production/SLA/public-compatibility claim exists;
12. P3.12 passes and parent roadmap is synchronized.

## 12. Current canonical action

> **R5 — Capability Boundary Review.**

Review the P3.02 Incubating/Provisional boundaries for service-catalog growth, lifecycle inflation, product-domain leakage, accidental stable interfaces, hidden implementation coupling and ADR-triggering commitments before P3.03–P3.06 implementation expands.
