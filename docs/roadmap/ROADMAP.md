# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.4.0`
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

Version `2.4.0` records closure of Phase 2 and milestone `M2`, synchronizes `P2.12`, and moves the active planning horizon to **Phase 3 boundary revalidation and decomposition** without prematurely activating Phase 3.

Historical detailed Phase 2 evidence remains preserved in [`PHASE-2-CORE-RUNTIME.md`](PHASE-2-CORE-RUNTIME.md), canonical reviews, implementation/tests and repository history.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- [`P2.12 closure review`](../reviews/P2-12-phase-2-m2-closure-review.md) — `PASS — M2 achieved for the declared bounded reusable-runtime reference scope`;
- no Platform Capability becomes `Active` merely because M2 is achieved;
- Phase 3 remains non-Active pending boundary revalidation and decomposition.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Near-term | 🟦 Ready for boundary revalidation | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Exploratory | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

`Ready for boundary revalidation` is a planning status, not a capability lifecycle or production status.

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

Engineering gates `R1`–`R4` are also complete.

M2 evidence establishes reusable domain-neutral runtime semantics across two materially distinct bounded workflows, exact identity/version/authority/provenance behavior, Product Contract validation, architecture fitness, portability/projection non-authority and an explicit P2.11 no-ADR disposition for the current bounded runtime.

M2 does not establish production readiness, full RFC conformance, stable public compatibility, a supported SDK/API, durable infrastructure, SLA/support obligations or an `Active` Platform Capability.

## 6. Current canonical action

> **Phase 3 boundary revalidation and decomposition — Shared Platform Capabilities.**

Before Phase 3 is marked `Active`:

1. revalidate the strategic Phase 3 intent against M2 evidence and current product/workflow needs;
2. identify candidate shared responsibilities backed by validated reuse, universal governance/security need or strategic necessity;
3. distinguish true Platform Capability candidates from product-local experiments and commodity infrastructure;
4. check whether any proposed concrete persistence, Event delivery, IAM/enforcement, serialization/public interface, projection storage or service topology choice crosses an ADR gate;
5. identify required Product Contract boundaries for real product reliance;
6. define a bounded Phase 3 work breakdown and exit criterion;
7. preserve lifecycle discipline: exploratory/candidate work is not `Active` merely because implementation exists;
8. update this roadmap only after the decomposition is canonically recorded.

No substantive Phase 3 implementation should be treated as canonical active-phase work until this boundary process is complete.

## 7. Provisional Phase 3 intent

Phase 3 may evaluate shared capability candidates such as:

- governed document/artifact handling;
- memory/knowledge retrieval and promotion support;
- non-authoritative search/index projections;
- reusable workflow support;
- audit/reconstruction/operator tooling;
- shared connector/adaptor patterns.

This inventory is exploratory. It is not a commitment to build all items, does not make them Platform Capabilities, and does not establish lifecycle status.

Candidate admission must follow evidence and the Constitution/RFC baseline rather than roadmap convenience.

## 8. ADR and Product Contract gate

The P2.11 closure remains binding for the current bounded M2 implementation: no present implementation choice has crossed the ADR threshold.

A fresh ADR-gate assessment is required before material reliance on concrete durable or externally depended-upon choices, including persistence/database topology, transactions/concurrency, Event transport/store, IAM/policy enforcement, evidence-integrity technology, stable API/serialization contracts, durable projection/replay storage or deployable service/process topology.

A real Product that relies on platform capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract boundary before governed reliance.

## 9. Roadmap maintenance rule

After every meaningful canonical milestone:

- synchronize this roadmap with the phase roadmap/review;
- record evidence rather than infer completion from code alone;
- keep planning status distinct from capability lifecycle, operational environment and conformance maturity;
- do not represent Draft/Proposed/exploratory items as accepted or active;
- preserve repository history rather than fabricating retrospective approvals.

## 10. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
        ↓
Phase 3 boundary revalidation + decomposition ← current
        ↓
Phase 3 activation only after bounded plan is canonically established
```
