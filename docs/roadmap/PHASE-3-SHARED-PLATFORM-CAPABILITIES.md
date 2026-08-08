# Arvectum OS Phase 3 — Shared Platform Capabilities

Status: `Active`
Version: `1.0.1`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M3 — Validated shared capability baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 2 — Core Runtime`, `M2` achieved
Phase 2 closure: [`P2-12-phase-2-m2-closure-review.md`](../reviews/P2-12-phase-2-m2-closure-review.md)

## 1. Purpose

Phase 3 begins only after the Phase 2 boundary revalidation required by the canonical roadmap.

Its purpose is to prove that a **small, justified set of domain-neutral shared responsibilities** can be implemented above the reusable Core Runtime as governed Platform Capability candidates without product-domain leakage, competing canonical authority, premature public contracts or accidental infrastructure lock-in.

Phase 3 does **not** attempt to build a complete service catalog. It does not make every useful mechanism a Platform Capability and does not make any capability `Active` merely because code exists.

The phase follows the RFC-0001 lifecycle:

`Candidate → Incubating → Active → Deprecated → Retired`

During Phase 3, candidate/incubating status is sufficient for bounded validation. `Active` requires the independent RFC-0001 admission and operational-readiness conditions and is not an automatic M3 outcome.

## 2. Boundary revalidation result

M2 established reusable domain-neutral semantics for Canonical Records, Relationships, Governed Execution, Events/provenance, Product Contract validation, portability/replay and non-authoritative projections across two materially distinct bounded workflows.

M2 explicitly carried forward broader shared-capability work, including:

- complete Memory/Knowledge lifecycle;
- complete Document/Artifact platform capability;
- durable replay/projection/search/index storage;
- capability lifecycle admission/promotion decisions;
- stable public Product Contract/API surfaces;
- operational readiness.

Accepted RFC-0007 and RFC-0008 already define domain-neutral architecture for Memory/Knowledge and Document/Artifact responsibilities. RFC-0001 additionally establishes that search/index projections remain non-authoritative and that platform admission must be evidence-driven.

Therefore Phase 3 will evaluate a bounded capability set around responsibilities already justified by Accepted architecture and M2 reuse seams rather than inventing a broad platform service inventory.

### 2.1 Initial bounded capability candidates

P3.01 has admitted the following entries to the RFC-0001 lifecycle state `Candidate`:

1. `CAP-001 — Document & Artifact Governance` — bounded RFC-0008 semantics above Core Runtime;
2. `CAP-002 — Memory & Knowledge Governance` — bounded RFC-0007 retrieval/promotion lifecycle semantics above Core Runtime;
3. `CAP-003 — Search / Index Projection` — non-authoritative discovery over governed source versions;
4. `CAP-004 — Audit / Reconstruction Support` — reusable operator-facing reconstruction/evidence access over existing Event/provenance semantics.

Canonical Candidate metadata, review dates, incubation/containment/rejection criteria and explicit product/commodity boundaries are recorded in [`PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md).

All four entries remain lifecycle `Candidate`. P3.01 does not promote any entry to `Incubating` or `Active` and creates no implementation commitment.

### 2.2 Explicitly deferred from the initial bounded set

The following remain outside the initial P3 implementation scope unless later evidence changes the plan:

- generic notification service;
- generic scheduler;
- generic connector marketplace or broad adaptor framework;
- public SDK/API;
- product-domain workflows, taxonomies, templates, ontologies or business rules;
- production IAM/policy engine;
- fixed database, object store, search engine, broker or service topology;
- customer-facing SLA/support/HA commitments.

Shared connector/adaptor patterns may be studied at P3.09 only if actual capability integration evidence requires them; they are not pre-admitted as a capability.

## 3. Phase 3 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟩 Complete | `██████████ 100%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | 🟦 Next | `░░░░░░░░░░ 0%` |
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

## 4. Detailed tasks

### P3.01 — Capability boundary revalidation + Candidate catalog

**Goal:** convert the exploratory Phase 3 inventory into explicit RFC-0001 Candidate records and reject/contain anything that lacks a platform justification.

Required output for every retained candidate:

- proposed organizational outcome;
- accountable architectural owner;
- sponsor or constitutional rationale;
- domain-neutral boundary;
- expected consumers or strategic need;
- reuse hypothesis;
- review date;
- incubation/containment/rejection criteria;
- explicit statement of what remains product-owned or commodity infrastructure.

**Exit:** canonical Candidate catalog exists; initial scope is bounded; rejected/deferred items are explicit; no lifecycle inflation occurs.

**Completion evidence — 2026-08-08:**

- [`Platform Capability Candidate Catalog`](../catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) records four retained entries (`CAP-001` through `CAP-004`) at lifecycle `Candidate` with every RFC-0001-required Candidate metadata field;
- [`P3.01 Capability Boundary Revalidation Review`](../reviews/P3-01-capability-boundary-revalidation-review.md) records `PASS — four bounded domain-neutral responsibilities are admitted as RFC-0001 Candidates; product-domain behavior and commodity infrastructure remain outside the capability boundary`;
- product-specific document/knowledge/search/audit semantics remain product-owned and concrete storage/search/IAM/observability/deployment technology remains outside capability identity;
- generic notifications, scheduler, broad connector framework, public SDK/API and operational/commercial commitments are explicitly deferred/not admitted;
- all four retained entries have review date `2026-09-08` with earlier review at P3.11;
- no Candidate is promoted to `Incubating` or `Active`;
- no Accepted RFC is changed and no ADR is fabricated or prematurely created.

### P3.02 — Capability lifecycle, ownership and Provisional contract baseline

**Goal:** define the minimum governed incubation envelope for retained candidates without creating stable public contracts prematurely.

For any candidate moving to `Incubating`, record the RFC-0001-required source need, sponsoring consumers, bounded scope/budget, Provisional domain-neutral contract, Canonical Record/authority responsibilities, dependencies/events, security/data handling, portability/migration and exit criteria.

**Exit:** each implemented capability has explicit lifecycle state, owner and Provisional contract boundary; implementation existence is not confused with `Active` status.

### P3.03 — Document & Artifact Governance candidate slice

**Goal:** implement a bounded RFC-0008 shared slice using Core Runtime semantics.

Minimum exercised semantics:

- logical Document identity distinct from file/storage identity;
- immutable Document Version identity;
- governed admission/checkpoint before consequential reliance;
- Artifact/content identity and content-manifest semantics where applicable;
- derivation provenance;
- exact relied-upon Document/Artifact version pinning;
- transient output does not silently become canonical Document state;
- storage remains replaceable and non-authoritative.

**Exit:** bounded document/artifact workflow passes fitness tests without selecting a permanent DMS/object-store architecture or importing product-specific templates/taxonomies.

### P3.04 — Memory & Knowledge Governance candidate slice

**Goal:** implement a bounded RFC-0007 shared slice while preserving Observation ≠ Memory ≠ Knowledge Candidate ≠ validated Knowledge.

Minimum exercised semantics:

- governed retrieval under Organization/authorization/purpose/classification/rights/freshness constraints where relevant;
- explicit candidate/promotion path;
- provenance and exact Knowledge Version attribution for consequential reliance;
- validation distinct from approval and Organizational Authority;
- AI cannot silently promote or broaden scope/retention/reuse;
- derived retrieval representations remain non-canonical.

**Exit:** bounded learning/retrieval workflow passes positive and negative-path tests without creating a generic AI memory store as authority.

### P3.05 — Non-authoritative Search / Index Projection candidate slice

**Goal:** prove reusable discovery/index behavior over governed sources without creating a second source of truth.

Minimum exercised semantics:

- projection entries attribute exact source identities/versions;
- stale/missing/ambiguous source state is visible and handled explicitly;
- projection cannot authorize consequential mutation or mint authority;
- rebuild/replay from canonical source is possible within the bounded reference scope;
- search/index technology remains replaceable.

**Exit:** search/index projection is useful for discovery while canonical reliance still resolves through governed source state.

### P3.06 — Audit / Reconstruction Support candidate slice

**Goal:** expose reusable reconstruction/evidence access over RFC-0006 and M2 provenance semantics without inventing a competing audit authority.

Minimum exercised semantics:

- reconstruct relevant execution, actor, authority, Product Contract, Workflow/material inputs, Event causation/correlation and output versions;
- distinguish canonical evidence from derived views;
- preserve unavailable/redacted/deleted evidence semantics honestly;
- derived audit views cannot mutate canonical state.

**Exit:** a bounded operator/reviewer reconstruction scenario is explainable from governed evidence and exact versions.

### P3.07 — Cross-capability security, rights and Organization-scope enforcement

**Goal:** prove that composing P3 candidates does not weaken RFC-0003 controls.

Required negative paths include:

- cross-Organization access denied by default;
- authorization does not imply Organizational Authority;
- retrieval/search does not bypass classification/purpose/rights controls;
- document derivation does not silently declassify or expand retention/reuse;
- knowledge/search projections cannot become authority;
- Product Contract declaration does not grant permissions.

**Exit:** cross-capability composition fails closed at relevant boundaries.

### P3.08 — Product Contract consumption boundary + bounded consumer proof

**Goal:** demonstrate a real or bounded product-style consumer using one or more P3 capability contracts through RFC-0004 rather than internal implementation coupling.

The consumer must declare exact capability/contract dependencies and remain product-responsible for domain semantics.

**Exit:** capability consumption works through a Provisional Product Contract surface with no hidden table/store/index coupling and no authority inflation.

### P3.09 — Shared-capability reuse and composition proof

**Goal:** demonstrate that at least two materially distinct bounded consumers/workflows reuse retained shared capability semantics without copying implementation internals or forcing speculative universal abstractions.

This task is also the evidence point for deciding whether any connector/adaptor pattern is genuinely shared or should remain local.

**Exit:** validated reuse evidence exists for the retained capability baseline; unsupported candidates may be contained, returned to product scope or deferred rather than promoted.

### P3.10 — Phase 3 architecture fitness matrix

**Goal:** accumulate executable evidence across the phase.

At minimum cover:

- domain neutrality;
- lifecycle-state integrity;
- Organization isolation;
- authorization/authority separation;
- canonical vs derived/non-authoritative state;
- exact version/provenance attribution;
- Product Contract boundary integrity;
- rights/classification/purpose/retention propagation where applicable;
- AI non-authority;
- portability/rebuildability;
- no hidden product coupling;
- no accidental stable public interface;
- no undeclared ADR-triggering dependency.

P3.10 runs continuously rather than only at phase end.

### P3.11 — Capability admission / ADR / refactoring hardening review

**Goal:** perform the Phase 3 structural and governance hardening pass before M3 closure.

Review:

- whether abstractions are justified by actual reuse;
- whether candidates should remain Candidate, become Incubating, be contained/returned/deferred, or separately qualify for Active admission;
- whether any concrete persistence/search/object-store/Event/IAM/API/serialization/service-topology choice crossed an ADR gate;
- whether Product Contract boundaries are explicit;
- dependency direction, duplicate semantics and bypass paths;
- benchmark/profile evidence before performance optimization;
- migration/reversibility implications.

`Active` capability promotion, if any, requires its own complete RFC-0001 admission/operational-readiness evidence; P3.11 does not grant it automatically.

**Exit:** all material findings resolved or dispositioned; required ADR/governance work completed before material reliance.

### P3.12 — Phase 3 / M3 closure review

**Goal:** decide whether M3 is achieved within an explicitly bounded scope.

**M3 target:** a small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims.

**Exit:** canonical closure review records `PASS` or bounded failure/continuation disposition and synchronizes the parent roadmap.

## 5. Dependency-aware sequence

```text
M2 ✅
 │
 ▼
P3.01 Candidate catalog / boundary revalidation ✅
 │
 ▼
P3.02 Lifecycle + Provisional contracts ← current
 │
 ├──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼              ▼
P3.03          P3.04          P3.05          P3.06
Documents      Knowledge      Search          Audit
 └──────────────┴───────┬──────┴──────────────┘
                        ▼
                     P3.07
              Security / rights composition
                        │
                        ▼
                     P3.08
              Product Contract consumer
                        │
                        ▼
                     P3.09
                 Reuse proof
                        │
                        ▼
                     P3.11
              Admission / ADR / hardening
                        │
                        ▼
                     P3.12
                    M3 review
```

`P3.10` is cross-cutting and accumulates fitness evidence throughout the phase.

P3.03–P3.06 may proceed in bounded parallel only after P3.01/P3.02 establish explicit ownership/lifecycle/contract boundaries.

## 6. Engineering review gates

Phase 3 preserves the approved principle of milestone-driven refactoring rather than continuous speculative cleanup.

| Gate | Trigger | Purpose |
|---|---|---|
| `R5 — Capability Boundary Review` | after P3.02 | detect accidental service catalog growth, lifecycle inflation and contract leakage before capability implementation expands |
| `R6 — Cross-Capability Health Review` | after P3.07 | review duplicated semantics, security/rights propagation, dependency direction and new ADR triggers |
| `R7 — Reuse Refactoring Review` | after P3.09 | refactor only abstractions justified by actual multi-consumer reuse evidence |
| `R8 — M3 Hardening Review` | after P3.10 | final code health, fitness, unsafe dependency, capability-status and evidence-backed optimization pass |

Performance optimization requires reproducible benchmark/profile evidence except for obvious correctness, security or resource-exhaustion defects.

## 7. ADR gate

No technology ADR is created merely because Phase 3 is Active.

Re-open the ADR gate before material reliance on a concrete durable or externally depended-upon choice, especially:

- database/object-store/search-index topology;
- transaction/concurrency mechanism;
- Event delivery/checkpoint mechanism;
- IAM/PDP/PEP enforcement technology;
- evidence-integrity mechanism;
- stable public/cross-product API, SDK or serialization format;
- durable projection/replay storage;
- separately deployable service/process topology.

Prefer reversible in-memory/local reference mechanisms until a material constraint justifies an ADR.

## 8. Product/platform boundary

Phase 3 MUST NOT absorb product-specific schemas, workflows, prompts, taxonomies, templates, scoring, domain Knowledge, integrations or UX merely because a product needs them.

A product-local reversible experiment remains product-owned. A product relying on P3 shared capability semantics, canonical platform state or shared platform history uses the applicable Provisional Product Contract boundary.

Successful implementation or reuse does not automatically promote a capability to `Active`.

## 9. Phase 3 exit criteria

M3 may be declared achieved only when all applicable conditions pass:

1. the retained capability set has explicit RFC-0001 lifecycle state, owner, rationale and bounded contract;
2. at least a small set of domain-neutral shared responsibilities is executable above the M2 Core Runtime;
3. capability composition preserves Organization scope, authorization/authority separation, rights and provenance;
4. Document/Artifact and Memory/Knowledge semantics implemented in scope conform to Accepted RFC-0008/RFC-0007 boundaries;
5. search/index and audit/reconstruction views remain derived/non-authoritative;
6. at least two materially distinct bounded consumers/workflows demonstrate reuse of retained shared capability semantics;
7. Product Contract consumption avoids hidden implementation coupling;
8. P3.10 fitness evidence passes for the declared scope;
9. R5–R8 complete and material findings are resolved/dispositioned;
10. every crossed ADR gate is governed before material reliance;
11. no product-domain leakage or unsupported `Active`/production/SLA/public-compatibility claim exists;
12. P3.12 closure review passes and parent Roadmap is synchronized.

## 10. Current canonical action

> **P3.02 — Capability lifecycle, ownership and Provisional contract baseline.**

For any retained Candidate considered for incubation, record the RFC-0001-required source need, sponsoring consumers, bounded scope/budget, Provisional domain-neutral capability contract, Canonical Record/authority responsibilities, dependencies/events, security/data handling, portability/migration and exit criteria.

Do not begin broad P3.03–P3.06 implementation, create stable public interfaces or select durable infrastructure before the incubation boundary is explicit.
