# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.23.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

## 2. Version note

Version `2.23.0` records completion of **P4.10 — Workspace architecture fitness + accessibility/usability baseline** with `PASS` and advances the current canonical action to **R12 — M4 Workspace Hardening**.

P4.10 evaluates P4.02–P4.09 against the complete 14-dimension M4 workspace fitness matrix. The bounded reference workspace passes Organization isolation, identity attribution, Authorization-versus-Organizational-Authority separation, canonical-versus-derived state, exact-version visibility/reliance, provenance honesty, Product Contract integrity, Document/Artifact authority semantics, Knowledge/Search non-authority, fail-closed actions, product-domain neutrality, accessibility baseline, deterministic critical-state testability and presentation reversibility.

The accessibility/usability result is deliberately scoped. Core reference renderers expose textual Organization/Actor/reference/status meaning, blocked-state reasons, current-navigation/alert semantics, exact Version/authority/provenance/gate distinctions and authority-safe action labels without relying on color-only meaning. P4.10 does **not** claim formal WCAG conformance, production visual-UX certification or completed end-user validation.

P4.10 adds `reference/python/tests/test_p4_10_workspace_architecture_fitness_accessibility_usability.py` as cross-cutting executable regression evidence. Missing, denied, ambiguous and wrong-Organization source access remains minimized and fail-closed; replaced authorization evidence requires re-inspection; product composition keeps the R10/P4.05/Governed Execution action choke point; and the reviewed presentation boundary selects no durable frontend/API/IAM/storage technology.

The R11/P4.09 refactoring watch item is resolved for this gate as **narrow reuse only**. `authority_safe_ux.consume_current_source_authorization()` remains an internal presentation decision consumer. Existing P4.03–P4.07/R10 paths retain their capability/action-specific purpose/right/classification/freshness/exact-reliance/action-safety checks rather than being broadly migrated into an accidental policy/IAM owner.

No Product Contract changes, capability lifecycle changes, public compatibility commitments or ADR-triggering durable technology choices are created. The P4.08 Product Contract remains `Provisional 0.1.0` and CAP-001 through CAP-004 remain `Incubating / Provisional`.

GitHub issue #54 remains the separately tracked hosted runner/account provisioning gap. The P4.10 test source is deterministic executable evidence and was syntax-validated before publication, but no green hosted P4.10 run is claimed.

Canonical evidence:

- [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- `reference/python/tests/test_p4_10_workspace_architecture_fitness_accessibility_usability.py` — 14-dimension architecture/accessibility/security regression guard;
- [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- `reference/python/arvectum_os_ref/authority_safe_ux.py` — bounded internal decision-consumption helper;
- [`R11 Composition / Usability Refactoring Review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`, source-access matcher refactoring watch item;
- [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`;
- [`P4.08 bounded Product Contract`](../contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md) — remains `Provisional 0.1.0`;
- [`R10 Operator Safety / Cross-Capability Health Review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — Phase 4 remains `Active`, current gate R12;
- GitHub issue `#54` — hosted CI provisioning gap tracked separately from architecture/security completion.

Phase 3 remains closed with `M3 — Validated shared capability baseline` achieved. CAP-001 through CAP-004 remain lifecycle `Incubating / Provisional`; P4.10 creates no new Platform Capability and promotes none to `Active`.

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
- [`R10 review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`;
- [`P4.08 review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`;
- [`R11 review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`;
- [`P4.09 review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- [`P4.10 review`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- P4.08 Product Contract remains `Provisional 0.1.0`;
- no frontend framework, public route/API/BFF, stable wire contract, IAM provider, durable workspace/runtime/Event store, durable search/vector/RAG technology, embedding/LLM provider, document/object-store topology, OCR/signing provider, content-delivery service or service topology is selected by P4.10;
- P4.10 introduces no new RFC, ADR or capability lifecycle change.

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
| `P4.08` | Cross-capability task/context composition + bounded product entry point | 🟩 Complete | `██████████ 100%` |
| `P4.09` | Security, rights, minimization and authority-safe UX | 🟩 Complete | `██████████ 100%` |
| `P4.10` | Workspace architecture fitness + accessibility/usability baseline | 🟩 Complete | `██████████ 100%` |
| `P4.11` | Workspace hardening / ADR / refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.12` | Phase 4 / M4 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Phase 4 roadmap work-item completion is `10 / 12 = 83.3%`. Engineering reviews such as R9/R10/R11/R12 are gates and do not inflate this percentage as separate equal-weight work items.

Engineering gates:

- `R9 — Workspace Boundary Review` after P4.02 — **Complete / PASS**;
- `R10 — Operator Safety / Cross-Capability Health Review` after P4.07 — **Complete / PASS**;
- `R11 — Composition / Usability Refactoring Review` after P4.08 / meaningful usability evidence — **Complete / PASS**;
- `R12 — M4 Workspace Hardening` after P4.10 — **Current**.

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

> **`R12 — M4 Workspace Hardening`.**

R12 now hardens the completed P4.10 matrix/baseline before P4.11. It must re-check dependency direction and product/platform boundaries, Organization/source isolation, Authorization-versus-Organizational-Authority separation, exact-version/provenance semantics, derived-state non-authority, fail-closed consequential action paths, accessibility-critical state meaning, deterministic negative-path coverage and every still-armed ADR trigger.

R12 must preserve the P4.10 scope boundary: the accessibility result is a bounded semantic/textual reference baseline, not formal WCAG/production certification; issue #54 is a tooling limitation, not test-success evidence; and the P4.09 helper remains a narrow decision-consumption primitive unless a later refactor demonstrably preserves capability-specific controls.

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
R10 Operator Safety / Cross-Capability Health Review ✓
        ↓
P4.08 Cross-capability task/context composition + bounded product entry point ✓
        ↓
R11 Composition / Usability Refactoring Review ✓
        ↓
P4.09 Security / rights / minimization / authority-safe UX ✓
        ↓
P4.10 Workspace architecture fitness + accessibility/usability baseline ✓
        ↓
R12 M4 Workspace Hardening ← current
        ↓
P4.11 Workspace hardening / ADR / refactoring review
        ↓
P4.12 Phase 4 / M4 closure review
        ↓
M4 Coherent governed workspace baseline
```
