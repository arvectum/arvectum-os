# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.27.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.27.0` activates **Phase 5 — SDK, Contracts and Extension Experience** after repository-confirmed Phase 4 closure.

Phase 4 is `Complete`: P4.12 records `PASS`, `M4 — Coherent governed workspace baseline` is `Achieved` for the declared bounded reference scope, and final synchronized P4.11 validation recorded `570 tests`, `OK`.

Phase 5 has been boundary-revalidated and decomposed in [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md). It is now `Active`; the current canonical action is `P5.01`.

Activation does not create a public SDK/API, Stable Product Contract, `Active` Platform Capability, production-readiness approval or compatibility/SLA commitment.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete / achieved;
- Phase 1 / `M1` — complete / achieved;
- Phase 2 / `M2` — complete / achieved for the bounded reusable-runtime reference scope;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- Phase 4 / `M4` — complete / achieved for the bounded governed-workspace reference scope;
- [`P4.12 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 Product Contract remains `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3/M4 is achieved;
- no stable/public SDK, API, wire or frontend compatibility boundary has been created by M4.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Active | 🟨 In progress | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Near-term | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 4 — Workspace / Operator Experience

Canonical detailed record:

- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`, M4 `Achieved`;
- [`P4.12 — Phase 4 / M4 Closure Review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`.

P4.01 through P4.12 are complete. R9 through R12 passed. M4 proves a coherent governed workspace baseline over explicit Organization/Actor context, canonical records/versions/relationships, Event/provenance/reconstruction, Governed Execution, Document/Artifact and Memory/Knowledge/Search semantics, bounded Product Contract-backed composition and scoped security/accessibility fitness evidence.

M4 does not imply production readiness, capability lifecycle `Active`, Stable Product Contract/public API status, formal WCAG/full-platform conformance, SLA/support or final commercial UX.

## 6. Active Phase 5 — SDK, Contracts and Extension Experience

Canonical detailed work breakdown:

- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Active 1.0.0`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P5.01` | Integration boundary revalidation + developer journeys | 🟦 Next | `░░░░░░░░░░ 0%` |
| `P5.02` | Product Contract declaration model + machine-checkable validation baseline | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.03` | Governed dependency/version resolution + compatibility semantics | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.04` | Integration composition API/facade boundary | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.05` | Scaffolding/templates + local integration harness | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.06` | Security, authority, rights + Organization-scope integration guards | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.07` | Event/provenance/portability integration support | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.08` | Workspace/capability integration adapters without private coupling | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.09` | Second materially distinct integration reuse proof | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.10` | Phase 5 conformance + architecture fitness matrix | ⬜ Cross-cutting | `░░░░░░░░░░ 0%` |
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.12` | Phase 5 / M5 closure review | ⬜ Planned | `░░░░░░░░░░ 0%` |

Engineering gates: `R13 — Integration Boundary Review`, `R14 — Developer Safety / Contract Health Review`, `R15 — Reuse / Developer Experience Refactoring Review`, `R16 — M5 Integration Hardening`. They do not inflate Phase 5 percentage as separate equal-weight roadmap tasks.

## 7. M5 target

`M5 — Repeatable product/extension integration` requires repository evidence that at least two materially distinct bounded integrations can rely on the same explicit Product Contract/integration boundary and reusable tooling without private platform coupling, while preserving exact dependency/version identity, Organization isolation, Authorization/Organizational Authority separation, governed canonical mutation, Event/provenance attribution, portability and product ownership of product-specific semantics.

M5 does not require a public SDK, Stable Product Contract or production deployment. Any stable/public compatibility boundary must be governed separately when evidence justifies it.

## 8. Current canonical action

> **P5.01 — Integration boundary revalidation + developer journeys.**

Start from M4 evidence and actual integration needs. Do not begin by choosing an SDK language, API protocol, package format, plugin framework or distribution mechanism.

## 9. ADR and Product Contract gate

Re-open the ADR/governance gate before material reliance on a language-specific SDK/package boundary, stable/public API or wire/serialization contract, package registry/distribution topology, plugin loading/sandboxing mechanism, extension registry topology, version-negotiation/migration protocol, generated-code compatibility boundary or separately deployable integration service.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

Extension registration, Product Contract admission or technical tool access does not itself grant Authorization or Organizational Authority.

## 10. Phase transition rule

Before Phase 6 becomes Active, revalidate its strategic scope against M5 evidence and actual product demand, then create a bounded `P6.xx` work breakdown and exit criteria.

A roadmap phase transition does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness or conformance state.

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
Phase 4 / M4 ✓
        ↓
Phase 5 — SDK, Contracts and Extension Experience ACTIVE
        ↓
P5.01 Integration boundary + developer journeys ← current
        ↓
M5 Repeatable product/extension integration
        ↓
Phase 6 — Product-driven Platform Validation DRAFT / Near-term
```
