# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.5.0`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS.

It coordinates work but does not override architectural or governance authority. Source priority remains:

1. Constitution;
2. Accepted RFCs;
3. Accepted ADRs;
4. approved policies, standards and catalogs;
5. Product Contracts and approved product decisions;
6. code and tests;
7. this roadmap;
8. task materials, chats and model memory.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.5.0` records canonical Phase 3 boundary revalidation and decomposition, activates **Phase 3 — Shared Platform Capabilities**, links its detailed work breakdown, and sets `P3.01` as the current canonical action.

Phase 2 / M2 remains closed and unchanged. Phase 3 activation is a planning/workstream state only: it does not promote any Platform Capability to RFC-0001 `Active` lifecycle status.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- [`P2.12 closure review`](../reviews/P2-12-phase-2-m2-closure-review.md) — `PASS — M2 achieved for the declared bounded reusable-runtime reference scope`;
- Phase 3 boundary revalidation/decomposition — complete;
- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Active 1.0.0`;
- no Platform Capability becomes lifecycle `Active` merely because Phase 3 is active or implementation exists.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Active | 🟨 In progress | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Near-term | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status and Platform Capability lifecycle status are distinct. Phase 3 may be `Active` while individual capability candidates remain `Candidate` or `Incubating`.

## 5. Completed Phase 2 / M2

Phase 2 is closed at 100%.

| ID | Work item | Status |
|---|---|---:|
| `P2.01` | Runtime boundary extraction and reusable composition baseline | 🟩 Complete |
| `P2.02` | Canonical Record lineage, Head and Effective Version runtime | 🟩 Complete |
| `P2.03` | Typed Relationship runtime | 🟩 Complete |
| `P2.04` | Governed Execution lifecycle and gate orchestration runtime | 🟩 Complete |
| `P2.05` | Event admission, provenance and reconstruction runtime | 🟩 Complete |
| `P2.06` | Runtime consistency, idempotency and conflict semantics | 🟩 Complete |
| `P2.07` | Product Contract runtime validation boundary | 🟩 Complete |
| `P2.08` | Portability, replay and non-authoritative projection runtime | 🟩 Complete |
| `P2.09` | Second bounded workflow reuse proof | 🟩 Complete |
| `P2.10` | Core Runtime architecture fitness matrix | 🟩 Complete |
| `P2.11` | ADR-gate and runtime-boundary hardening review | 🟩 Complete |
| `P2.12` | Phase 2 / M2 closure review | 🟩 Complete |

Engineering gates `R1`–`R4` are complete.

M2 evidence establishes reusable domain-neutral runtime semantics across two materially distinct bounded workflows, exact identity/version/authority/provenance behavior, Product Contract validation, architecture fitness, portability/projection non-authority and an explicit P2.11 no-ADR disposition for the current bounded runtime.

M2 does not establish production readiness, full RFC conformance, stable public compatibility, a supported SDK/API, durable infrastructure, SLA/support obligations or an `Active` Platform Capability.

## 6. Active Phase 3 — Shared Platform Capabilities

Detailed canonical plan:

- [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](PHASE-3-SHARED-PLATFORM-CAPABILITIES.md) — `Active 1.0.0`.

Phase 3 evaluates a deliberately small initial candidate set grounded in Accepted architecture and M2 evidence:

1. Document & Artifact Governance;
2. Memory & Knowledge Governance;
3. non-authoritative Search / Index Projection;
4. Audit / Reconstruction Support.

These are **capability candidates**, not automatically lifecycle `Active` capabilities. P3.01/P3.02 must record explicit RFC-0001 Candidate/Incubating metadata, ownership and Provisional contracts before broad implementation proceeds.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P3.01` | Capability boundary revalidation + Candidate catalog | 🟦 Next | `░░░░░░░░░░ 0%` |
| `P3.02` | Capability lifecycle, ownership and Provisional contract baseline | ⬜ | `░░░░░░░░░░ 0%` |
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

Engineering gates for Phase 3 are `R5 — Capability Boundary Review`, `R6 — Cross-Capability Health Review`, `R7 — Reuse Refactoring Review`, and `R8 — M3 Hardening Review` as defined in the detailed Phase 3 roadmap.

### M3 target

A small set of domain-neutral shared capabilities has demonstrated governed reuse above the Core Runtime with explicit lifecycle/ownership/contracts, no product-domain leakage, preserved authority/provenance/portability semantics and no unsupported production/public-contract claims.

M3 does not itself require or imply lifecycle `Active` capability promotion.

## 7. Current canonical action

> **P3.01 — Capability boundary revalidation + Candidate catalog.**

Record the initial candidate set and the RFC-0001-required Candidate metadata: organizational outcome, owner, rationale/sponsor, domain-neutral boundary, expected consumers/strategic need, reuse hypothesis, review date and incubation/containment/rejection criteria.

Do not begin broad capability implementation, promote candidates to lifecycle `Active`, or select durable infrastructure merely because Phase 3 is active.

## 8. ADR and Product Contract gate

The P2.11 closure remains binding for the bounded M2 implementation: no present implementation choice has crossed the ADR threshold.

A fresh ADR-gate assessment is required before material reliance on concrete durable or externally depended-upon choices, including persistence/database/object-store/search topology, transactions/concurrency, Event transport/store, IAM/policy enforcement, evidence-integrity technology, stable API/serialization contracts, durable projection/replay storage or deployable service/process topology.

A real Product that relies on platform capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract boundary before governed reliance.

## 9. Phase transition rule

Before Phase 4 becomes Active:

1. complete P3.12 and record the M3 result;
2. revalidate Phase 4 against actual M3 evidence and current product/operator needs;
3. distinguish operator UX needs from product-specific UX and Kernel/platform semantics;
4. create a detailed Phase 4 work breakdown with stable `P4.xx` identifiers;
5. identify required RFC/ADR/policy/Product Contract work;
6. define scoped exit criteria and engineering/fitness evidence;
7. update this roadmap with the resulting canonical phase plan.

## 10. Roadmap maintenance rule

Every roadmap update MUST begin with repository synchronization rather than chat-memory reconstruction.

After every meaningful canonical milestone:

- synchronize this roadmap with the active phase roadmap/review;
- record evidence rather than infer completion from code alone;
- keep planning status distinct from capability lifecycle, operational environment and conformance maturity;
- do not represent Draft/Proposed/exploratory items as accepted or lifecycle Active;
- preserve repository history rather than fabricating retrospective approvals.

## 11. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
        ↓
Phase 3 — Shared Platform Capabilities ACTIVE
        ↓
P3.01 Candidate catalog / boundary revalidation ← current
        ↓
P3.02 lifecycle + Provisional contracts
        ↓
P3.03–P3.06 bounded capability slices
        ↓
P3.07–P3.09 composition / consumer / reuse proof
        ↓
P3.10–P3.12 fitness / hardening / M3 closure
```
