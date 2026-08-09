# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.26.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.26.0` records completion of **P4.12 — Phase 4 / M4 closure review** with `PASS`, closes **Phase 4 — Workspace / Operator Experience** and records **M4 — Coherent governed workspace baseline** as `Achieved` for the declared bounded governed-workspace reference scope.

P4.12 evaluated the complete P4.01–P4.11 and R9–R12 evidence against the thirteen declared M4 exit conditions. All conditions pass. The final P4.11 synchronized pull-request head was validated by `Reference Python CI #200` on PR #60 with Ubuntu 24.04.4, CPython 3.12.13 and `570 tests`, `OK`.

M4 proves a coherent domain-neutral operator workspace over governed platform state with explicit Organization/Actor context, exact Canonical Record/version/relationship meaning, Event/provenance/reconstruction honesty, Governed Execution action paths, Document/Artifact and Memory/Knowledge/Search semantic separation, one bounded Product Contract-backed product composition, security/minimization/isolation fitness evidence, the declared semantic/textual accessibility baseline and non-authoritative presentation/read-model semantics.

The closure intentionally changes only roadmap milestone state. CAP-001 through CAP-004 remain `Incubating / Provisional`; the P4.08 Product Contract remains `Provisional 0.1.0`; no Workspace capability becomes `Active`; no production or operational-readiness approval is created; no Stable/public API, SDK, wire, frontend or design-system compatibility boundary is created; no formal WCAG/full-platform conformance, SLA, support or commercial commitment is inferred.

P4.11's ADR disposition remains current: no concrete frontend/API/BFF/serialization/IAM/durable workspace/read-model/cache/search/vector/RAG/Document storage/service topology has crossed an ADR threshold. R12-F1 remains a fixed stale-authorization presentation-continuity invariant, and `authority_safe_ux` remains a narrow presentation decision consumer rather than an IAM/PDP/policy/Organizational Authority owner.

The next canonical action is **Phase 5 boundary revalidation and decomposition — SDK, Contracts and Extension Experience**. Phase 5 remains `Draft` until that revalidation produces a bounded P5 work breakdown and a separate activation decision.

Canonical evidence:

- [`P4.12 Phase 4 / M4 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`, M4 achieved for the bounded governed-workspace reference scope;
- [`P4.11 Workspace hardening / ADR / refactoring review`](../reviews/P4-11-workspace-hardening-adr-refactoring-review.md) — `PASS`, no material runtime refactor or ADR required;
- [`R12 M4 Workspace Hardening`](../reviews/R12-m4-workspace-hardening.md) — R12-F1 remediation and hardening;
- [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- [`P4.10 Hosted CI Validation Evidence`](../reviews/P4-10-ci-validation.md) — hosted CI recovery evidence;
- [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- [`R11 Composition / Usability Refactoring Review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`;
- [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`;
- [`P4.08 bounded Product Contract`](../contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md) — remains `Provisional 0.1.0`;
- [`R10 Operator Safety / Cross-Capability Health Review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — Phase 4 `Complete`, M4 `Achieved`;
- `Reference Python CI #200` — final synchronized P4.11 PR head, `570 tests`, `OK`.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete / achieved;
- Phase 1 / `M1` — complete / achieved;
- Phase 2 / `M2` — complete / achieved for the bounded reusable-runtime reference scope;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- Phase 4 / `M4` — complete / achieved for the bounded governed-workspace reference scope;
- [`P3.12 closure review`](../reviews/P3-12-phase-3-m3-closure-review.md) — `PASS`;
- [`P4.12 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- no Platform Capability is `Active` merely because M3 or M4 is achieved;
- P4.08 Product Contract remains `Provisional 0.1.0`;
- [`P4.01 review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`P4.02 review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- [`R9 review`](../reviews/R9-workspace-boundary-review.md) — `PASS`;
- [`P4.03 review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`;
- [`P4.04 review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`;
- [`P4.05 review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`;
- [`P4.06 review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`;
- [`P4.07 review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`;
- [`R10 review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`;
- [`P4.08 review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`;
- [`R11 review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`;
- [`P4.09 review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- [`P4.10 review`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- [`P4.10 hosted CI validation`](../reviews/P4-10-ci-validation.md) — `PASS`, Reference Python CI #191, `559 tests`, `OK`;
- [`R12 review`](../reviews/R12-m4-workspace-hardening.md) — `PASS`, R12-F1 remediated;
- [`P4.11 review`](../reviews/P4-11-workspace-hardening-adr-refactoring-review.md) — `PASS`;
- final P4.11 synchronized PR validation — Reference Python CI #200, `570 tests`, `OK`;
- no frontend framework, public route/API/BFF, stable wire contract, IAM provider, durable workspace/read-model/cache/search/vector/RAG technology, document/object-store/OCR/signing topology, content-delivery service or independently deployable workspace service topology is selected by M4 closure;
- P4.12 introduces no new RFC, ADR, Product Contract, capability lifecycle change or runtime behavior.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Near-term | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 3 — Shared Platform Capabilities

Phase 3 closed at 100% with `P3.12 = PASS` and `M3 = Achieved` for the declared bounded reference scope.

Retained shared capabilities:

1. `CAP-001 — Document & Artifact Governance` — `Incubating`, Provisional;
2. `CAP-002 — Memory & Knowledge Governance` — `Incubating`, Provisional;
3. `CAP-003 — Search / Index Projection` — `Incubating`, Provisional, non-authoritative;
4. `CAP-004 — Audit / Reconstruction Support` — `Incubating`, Provisional, derived/read-oriented.

M3 does not imply lifecycle `Active`, operational readiness, Stable Product Contracts, public API compatibility, production deployment or customer-facing SLA/support commitments.

## 6. Completed Phase 4 — Workspace / Operator Experience

Canonical detailed record:

- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`, M4 `Achieved`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P4.01` | Operator journeys, workspace boundary and information architecture | 🟩 Complete | `██████████ 100%` |
| `P4.02` | Organization context, identity and scoped navigation shell | 🟩 Complete | `██████████ 100%` |
| `P4.03` | Canonical Record / Relationship inspection experience | 🟩 Complete | `██████████ 100%` |
| `P4.04` | Version, Event, provenance and reconstruction experience | 🟩 Complete | `██████████ 100%` |
| `P4.05` | Governed Execution, gate and approval/action experience | 🟩 Complete | `██████████ 100%` |
| `P4.06` | Document / Artifact workspace experience | 🟩 Complete | `██████████ 100%` |
| `P4.07` | Memory / Knowledge / Search discovery experience | 🟩 Complete | `██████████ 100%` |
| `P4.08` | Cross-capability task/context composition + bounded product entry point | 🟩 Complete | `██████████ 100%` |
| `P4.09` | Security, rights, minimization and authority-safe UX | 🟩 Complete | `██████████ 100%` |
| `P4.10` | Workspace architecture fitness + accessibility/usability baseline | 🟩 Complete | `██████████ 100%` |
| `P4.11` | Workspace hardening / ADR / refactoring review | 🟩 Complete | `██████████ 100%` |
| `P4.12` | Phase 4 / M4 closure review | 🟩 Complete | `██████████ 100%` |

Phase 4 roadmap work-item completion is `12 / 12 = 100%`. Engineering reviews R9/R10/R11/R12 are gates and do not inflate this percentage as separate equal-weight work items.

Engineering gates:

- `R9 — Workspace Boundary Review` — **Complete / PASS**;
- `R10 — Operator Safety / Cross-Capability Health Review` — **Complete / PASS**, material stale-source-access action gap remediated;
- `R11 — Composition / Usability Refactoring Review` — **Complete / PASS**;
- `R12 — M4 Workspace Hardening` — **Complete / PASS**, material stale-presentation authorization-continuity defect remediated and fixed as R12-F1.

`M4 — Coherent governed workspace baseline` is `Achieved` for the declared bounded reference scope. It is not production readiness, full-platform conformance, Stable Product Contract/public API status, capability lifecycle `Active`, formal WCAG certification, SLA/support or final commercial UX.

## 7. M4 closure boundary

M4 establishes that, within the bounded reference scope:

1. an operator can navigate governed organizational state under explicit Organization/identity scope;
2. Canonical Records, immutable versions, relationships, Events and provenance remain semantically understandable;
3. consequential actions pass through Governed Execution with separate Authorization and Organizational Authority gates;
4. Document/Artifact and Memory/Knowledge/Search surfaces preserve Accepted authority/lifecycle distinctions;
5. derived presentation/reconstruction/search state remains non-authoritative;
6. at least one Provisional Product Contract-backed bounded product entry point composes shared workspace surfaces without private platform coupling;
7. cross-capability rights, minimization and isolation pass fitness checks;
8. core operator journeys meet the declared semantic/textual accessibility/usability baseline;
9. all applicable ADR gates are dispositioned and currently uncrossed;
10. R9–R12 and P4.12 pass.

The canonical closure decision is [`P4.12 — Phase 4 / M4 Closure Review`](../reviews/P4-12-phase-4-m4-closure-review.md).

## 8. Current canonical action

> **Phase 5 boundary revalidation and decomposition — SDK, Contracts and Extension Experience.**

Phase 5 remains `Draft`. Before it becomes `Active`, revalidate its strategic scope against M4 evidence and actual product/extension demand, then create a bounded `P5.xx` work breakdown and exit criteria.

The Phase 5 transition must not infer stable/public compatibility merely from its title. Stable Product Contracts, public APIs/SDKs/wire contracts and other externally relied-upon compatibility boundaries require their own evidence and applicable governance before commitment.

## 9. ADR and Product Contract gate

Re-open the ADR gate before material reliance on concrete durable or externally constraining choices including frontend/runtime framework as a stable cross-product boundary, BFF/API topology, stable wire/serialization contracts, IAM/session enforcement, durable workspace/read-model/cache storage, search/index technology beyond replaceable projection semantics, document/object storage topology, stable design-system/package compatibility or separately deployable UI/API service topology.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

The P4.08 bounded Product Contract remains `Provisional 0.1.0`; M4 closure does not make it Stable.

## 10. Phase transition rule

Before Phase 5 becomes Active, revalidate its draft scope against M4 evidence and actual product/extension demand, then create a bounded `P5.xx` work breakdown and exit criteria.

A roadmap phase transition does not by itself change any Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness or conformance state.

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
CAP-001..CAP-004 remain Incubating / Provisional
P4.08 Product Contract remains Provisional 0.1.0
        ↓
Phase 5 — SDK, Contracts and Extension Experience DRAFT
        ↓
Boundary revalidation + bounded P5 decomposition ← current
```
