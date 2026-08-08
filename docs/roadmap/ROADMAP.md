# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.18.0`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.18.0` records completion of **P4.07 — Memory / Knowledge / Search discovery experience** with `PASS` and advances the current canonical action to **R10 — Operator Safety / Cross-Capability Health Review**.

P4.07 adds a bounded internal operator discovery adapter over existing CAP-002 / RFC-0007 semantics, CAP-003 derived search/index semantics, P3.07 current cross-capability access enforcement and the P4.02 workspace shell. Observation, Organizational Memory, Knowledge Candidate and validated Knowledge remain epistemically distinct, and no browsing/search/AI-like output performs Knowledge promotion.

Validated Knowledge retains exact Subject/Version identity. Consequential reliance requires explicit exact Version selection, current freshness, current Actor/Organization-bound source authorization, matching purpose/right/classification context and final CAP-002 exact-reliance resolution. Stale/review-required Knowledge can be inspected as stale but cannot be relied upon consequentially.

Search/index/RAG-like results remain derived and non-authoritative. Current exact governed source resolution is rechecked before protected metadata is shown; a synchronized projection cannot make stale Knowledge current; CAP-003 discovery constraints cannot broaden CAP-002 Memory handling constraints; duplicate exact Memory/Knowledge representations fail closed; and a missing projection is surfaced as a projection gap rather than evidence of source absence. Unauthorized, ambiguous or handling-ineligible items are omitted without protected counts and previews are minimized.

P4.07 selects no durable search/index/vector technology, embedding/LLM provider, ranking model, RAG runtime, durable workspace/read-model/cache store, frontend framework, public route/API/wire contract, IAM/PDP/PEP mechanism, Product Contract, new Platform Capability or lifecycle promotion.

Canonical evidence:

- [`P4.07 Memory / Knowledge / Search discovery review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`, five functional cross-review iterations with remediated exact-source, projection-gap, semantic-owner-policy and ambiguity findings;
- [`P4.06 Document / Artifact workspace review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`;
- [`P4.05 Governed Execution / gate / approval-action review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`;
- [`P4.04 Version / Event / provenance / reconstruction review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`;
- [`P4.03 Canonical Record / Relationship inspection review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`;
- [`R9 Workspace Boundary Review`](../reviews/R9-workspace-boundary-review.md) — `PASS`;
- [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — Phase 4 remains `Active`;
- GitHub Actions `Reference Python CI #164` — `PASS`, Python `3.12.13`, `521` tests, `OK` on the implementation head before canonical roadmap synchronization.

Phase 3 remains closed with `M3 — Validated shared capability baseline` achieved. CAP-001 through CAP-004 remain lifecycle `Incubating / Provisional`; P4.07 creates no new Platform Capability and promotes none to `Active`.

Phase 4 remains operator-experience first and UI-technology neutral. It proves coherent human interaction with governed organizational state and shared capability slices without turning presentation/search state into canonical authority or prematurely selecting a frontend/API/search/service topology.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete;
- Phase 1 / `M1` — complete;
- Phase 2 / `M2` — complete;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- [`P3.12 closure review`](../reviews/P3-12-phase-3-m3-closure-review.md) — `PASS`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- no Platform Capability is `Active` merely because Phase 3 closed or Phase 4 is in progress;
- Phase 4 detailed roadmap remains `Active`;
- [`P4.01 review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`P4.02 review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- [`R9 review`](../reviews/R9-workspace-boundary-review.md) — `PASS`;
- [`P4.03 review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`;
- [`P4.04 review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`;
- [`P4.05 review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`;
- [`P4.06 review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`;
- [`P4.07 review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`;
- no frontend framework, public route/API/BFF, stable wire contract, IAM provider, durable workspace/runtime/Event store, durable search/vector/RAG technology, embedding/LLM provider, document/object-store topology, OCR/signing provider, content-delivery service or service topology is selected by P4.07;
- P4.07 introduces no new RFC, ADR, Product Contract or capability lifecycle change.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Active | 🟨 In progress | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Near-term | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, operational environment and conformance maturity remain distinct.

## 5. Completed Phase 3 — Shared Platform Capabilities

Phase 3 closed at 100% with `P3.12 = PASS` and `M3 = Achieved` for the declared bounded reference scope.

Retained shared capabilities:

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional, non-authoritative;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional, derived/read-oriented.

M3 does not imply lifecycle `Active`, operational readiness, Stable Product Contracts, public API compatibility, production deployment or customer-facing SLA/support commitments.

## 6. Active Phase 4 — Workspace / Operator Experience

Canonical detailed plan:

- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Active`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P4.01` | Operator journeys, workspace boundary and information architecture | 🟩 Complete | `██████████ 100%` |
| `P4.02` | Organization context, identity and scoped navigation shell | 🟩 Complete | `██████████ 100%` |
| `P4.03` | Canonical Record / Relationship inspection experience | 🟩 Complete | `██████████ 100%` |
| `P4.04` | Version, Event, provenance and reconstruction experience | 🟩 Complete | `██████████ 100%` |
| `P4.05` | Governed Execution, gate and approval/action experience | 🟩 Complete | `██████████ 100%` |
| `P4.06` | Document / Artifact workspace experience | 🟩 Complete | `██████████ 100%` |
| `P4.07` | Memory / Knowledge / Search discovery experience | 🟩 Complete | `██████████ 100%` |
| `P4.08` | Cross-capability task/context composition + bounded product entry point | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.09` | Security, rights, minimization and authority-safe UX | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.10` | Workspace architecture fitness + accessibility/usability baseline | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P4.11` | Workspace hardening / ADR / refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.12` | Phase 4 / M4 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Phase 4 roadmap work-item completion is `7 / 12 = 58.3%`. Engineering reviews such as R9/R10 are gates and do not inflate this percentage as separate equal-weight work items.

Engineering gates:

- `R9 — Workspace Boundary Review` after P4.02 — **Complete / PASS**;
- `R10 — Operator Safety / Cross-Capability Health Review` after P4.07 — **Current**;
- `R11 — Composition / Usability Refactoring Review` after P4.08 / meaningful usability evidence;
- `R12 — M4 Workspace Hardening` after P4.10.

## 7. M4 target

`M4 — Coherent governed workspace baseline` requires evidence that, within the bounded reference scope:

1. an operator can navigate governed organizational state under explicit Organization/identity scope;
2. Canonical Records, immutable versions, relationships, Events and provenance remain semantically understandable;
3. consequential actions pass through Governed Execution with separate Authorization and Organizational Authority gates;
4. Document/Artifact and Memory/Knowledge/Search surfaces preserve their Accepted authority and lifecycle distinctions;
5. derived presentation/reconstruction/search state remains non-authoritative;
6. at least one Product Contract-backed bounded product entry point composes shared workspace surfaces without private platform coupling;
7. cross-capability rights, minimization and isolation pass fitness checks;
8. core operator journeys meet the declared accessibility/usability baseline;
9. any crossed ADR gates have canonical dispositions;
10. R9–R12 and P4.12 pass.

M4 is a bounded workspace milestone. It is not production readiness, full-platform conformance, Stable Product Contract/public API status, capability lifecycle `Active`, SLA/support or final commercial UX.

## 8. Current canonical action

> **`R10 — Operator Safety / Cross-Capability Health Review`.**

Review the accumulated P4.03–P4.07 workspace surfaces before P4.08 composes them with a bounded Product Contract-backed product entry point.

R10 must verify that Organization/Actor-bound source authorization, purpose/rights/classification/minimization, exact-version reliance and canonical-versus-derived distinctions are consistently enforced across records, provenance, governed actions, documents/artifacts and Memory/Knowledge/Search. It must inspect stale presentation, duplicate/ambiguous sources, protected counts/previews, hidden actions and repeated presentation/access patterns without granting new authority or prematurely normalizing a public frontend/API abstraction.

R10 may recommend bounded refactoring only where repeated evidence justifies it. It does not promote CAP-001 through CAP-004 and must reopen an ADR gate only if a durable or externally constraining technology/interface decision is actually required.

## 9. ADR and Product Contract gate

Re-open the ADR gate before material reliance on concrete durable or externally constraining choices including frontend/runtime framework as a stable cross-product boundary, BFF/API topology, stable wire/serialization contracts, IAM/session enforcement, durable workspace/read-model/cache storage, search/index technology beyond replaceable projection semantics, document/object storage topology, stable design-system/package compatibility or separately deployable UI/API service topology.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

## 10. Phase transition rule

Before Phase 5 becomes Active, revalidate its draft scope against M4 evidence and actual product/extension demand, then create a bounded `P5.xx` work breakdown and exit criteria.

A roadmap phase transition does not by itself change any Platform Capability lifecycle, operational environment, Product Contract stability or conformance state.

## 11. Roadmap maintenance rule

Every roadmap update begins with repository synchronization rather than chat-memory reconstruction. After every meaningful canonical milestone, synchronize the roadmap, record evidence, keep lifecycle/environment/conformance distinct, do not inflate Draft/Proposed/exploratory status, and preserve repository history rather than fabricating approvals.

## 12. Current state summary

```text
Constitution 1.2.0 ✓
RFC-0001 … RFC-0008 Accepted ✓
Phase 0 / M0 ✓
Phase 1 / M1 ✓
Phase 2 / M2 ✓
Phase 3 / M3 ✓
        ↓
CAP-001..CAP-004 remain Incubating / Provisional
        ↓
Phase 4 — Workspace / Operator Experience ACTIVE
        ↓
P4.01 Operator journeys + workspace boundary + IA ✓
        ↓
P4.02 Organization context + identity + scoped navigation shell ✓
        ↓
R9 Workspace Boundary Review ✓
        ↓
P4.03 Canonical Record / Relationship inspection ✓
        ↓
P4.04 Version / Event / provenance / reconstruction ✓
        ↓
P4.05 Governed Execution / gates / approval-actions ✓
        ↓
P4.06 Document / Artifact workspace experience ✓
        ↓
P4.07 Memory / Knowledge / Search discovery experience ✓
        ↓
R10 Operator Safety / Cross-Capability Health Review ← current
        ↓
M4 Coherent governed workspace baseline
```
