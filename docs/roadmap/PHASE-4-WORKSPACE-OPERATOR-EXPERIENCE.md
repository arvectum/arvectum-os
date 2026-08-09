# Arvectum OS Phase 4 — Workspace / Operator Experience

Status: `Complete`
Version: `1.16.0`
Created: `2026-08-08`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M4 — Coherent governed workspace baseline` — `Achieved`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 3 — Shared Platform Capabilities`, `M3` achieved

## Version note

Version `1.16.0` records completion of **P4.12 — Phase 4 / M4 closure review** with `PASS`, closes Phase 4 at `12 / 12 = 100%`, and records **M4 — Coherent governed workspace baseline** as `Achieved` for the declared bounded governed-workspace reference scope.

P4.12 re-evaluated all thirteen M4 exit conditions over P4.01–P4.11 plus R9–R12. The complete evidence supports closure without introducing new architecture merely to finish the phase. The final synchronized P4.11 pull-request head passed `Reference Python CI #200` on PR #60 with Ubuntu 24.04.4 / CPython 3.12.13 and **570 tests, OK**.

The closure changes roadmap milestone state only. The P4.08 Product Contract remains `Provisional 0.1.0`; CAP-001 through CAP-004 remain `Incubating / Provisional`; no Workspace capability is promoted to `Active`; no production/operational-readiness, Stable/public interface, formal WCAG/full-platform conformance, SLA/support or commercial commitment is created.

P4.11's ADR disposition remains current: no stable frontend/runtime framework, public route/API/BFF topology, stable wire/serialization contract, IAM/session/PDP/PEP technology, durable workspace/read-model/cache store, shared search/vector/RAG technology, Document/object/OCR/signing topology, stable design-system boundary or separately deployable workspace service topology has crossed an ADR threshold. R12-F1 remains a fixed stale-authorization presentation-continuity regression invariant.

The next canonical action is **Phase 5 boundary revalidation and decomposition — SDK, Contracts and Extension Experience**. Phase 5 remains `Draft` until separately revalidated, decomposed and activated.

Canonical completion evidence:

- [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- [`R9 Workspace Boundary Review`](../reviews/R9-workspace-boundary-review.md) — `PASS`;
- [`P4.03 Canonical Record / Relationship inspection review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`;
- [`P4.04 Version / Event / provenance / reconstruction review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`;
- [`P4.05 Governed Execution / gate / approval-action review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`, four functional cross-review iterations;
- [`P4.06 Document / Artifact workspace review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`, five functional cross-review iterations including one pre-merge security finding and remediation;
- [`P4.07 Memory / Knowledge / Search discovery review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`, five functional cross-review iterations including exact-source, projection-gap, semantic-owner policy and ambiguity remediations;
- [`R10 Operator Safety / Cross-Capability Health Review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`, five functional cross-review iterations with one material stale-source-access action finding remediated before P4.08;
- [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`, six functional cross-review iterations with exact Product Contract/dependency/target continuity hardened;
- [`P4.08 bounded product Product Contract`](../contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md) — remains `Provisional 0.1.0`;
- [`R11 Composition / Usability Refactoring Review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`, five functional cross-review iterations;
- [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- [`P4.10 Hosted CI Validation Evidence`](../reviews/P4-10-ci-validation.md) — `PASS`, Reference Python CI #191, `559 tests`, `OK`, issue #54 closed;
- [`R12 M4 Workspace Hardening`](../reviews/R12-m4-workspace-hardening.md) — `PASS`, material stale-presentation authorization-continuity finding remediated;
- `reference/python/tests/test_r12_m4_workspace_hardening.py` — deterministic R12 hardening regression evidence;
- [`P4.11 Workspace hardening / ADR / refactoring review`](../reviews/P4-11-workspace-hardening-adr-refactoring-review.md) — `PASS`, no material runtime refactor or ADR required;
- `reference/python/tests/test_p4_11_workspace_hardening_adr_refactoring_review.py` — R12-F1, product/platform, semantic-owner, derived-state, ADR and operator-error guards;
- [`P4.12 Phase 4 / M4 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`, M4 achieved for the bounded governed-workspace reference scope;
- `Reference Python CI #200` — final synchronized P4.11 PR head, Ubuntu 24.04.4 / Python 3.12.13, `570 tests`, `OK`.

## 1. Purpose

Phase 4 proves that a human operator can understand, inspect and perform bounded governed work through one coherent workspace over the already established Core Runtime and Incubating shared capabilities.

The phase is intentionally **operator-experience first, UI-technology neutral**. It does not select a frontend framework, browser/mobile architecture, BFF/API topology, design system vendor, notification infrastructure or public API merely because a visible workspace is now required.

The workspace is a projection and interaction surface over governed organizational state. It MUST NOT become an independent source of canonical truth, bypass authorization or Organizational Authority, silently mutate canonical state, infer lifecycle `Active`, or hide provenance/version scope where those are material to consequential work.

Phase 4 is also the first phase where Arvectum OS becomes visibly understandable as a working operating environment rather than only an executable semantic/runtime foundation.

## 2. Boundary revalidation result

M3 evidence justified a bounded Phase 4 because:

1. Core Runtime and four shared capability slices have executable governed semantics;
2. operators need a coherent way to inspect canonical state, history, provenance, documents, knowledge/search projections and governed executions;
3. the workspace validates whether the platform abstractions are understandable and usable without adding product-domain semantics;
4. product entry points can rely on a shared operator shell through Product Contracts rather than each product rebuilding platform inspection/governance UI;
5. the phase remains reversible through internal/adaptor-backed presentation boundaries without premature public API or frontend technology commitments.

M4 closure confirms that this bounded proof succeeded. It does not make a Workspace Platform Capability `Active` under RFC-0001 lifecycle rules.

## 3. Phase 4 work breakdown

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

## 4. Detailed task intent and completion

### P4.01 — Operator journeys, workspace boundary and information architecture

Defined the smallest domain-neutral operator journeys that Phase 4 must support and the information architecture that exposes existing governed semantics without inventing new authority.

Completion evidence: [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`, four functional cross-review iterations.

### P4.02 — Organization context, identity and scoped navigation shell

Implemented the minimal workspace shell with explicit current Organization scope, attributable Actor/Principal context, fail-closed unresolved scope, domain-neutral navigation and non-authoritative presentation state. No SSO/IAM vendor choice is implied.

Completion evidence: [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`, four functional cross-review iterations and green full reference CI.

### P4.03 — Canonical Record / Relationship inspection experience

Provides operator inspection of governed objects and graph context with stable Subject Identity, exact Version Identity, Head versus Effective Version, authority/source, typed relationship direction/endpoint role, owner/scope/lifecycle visibility and fail-closed missing/ambiguous resolution.

Completion evidence: [`P4.03 Canonical Record / Relationship inspection review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`, four functional cross-review iterations and green full reference CI.

### P4.04 — Version, Event, provenance and reconstruction experience

Exposes Event history, causation/correlation, execution linkage, exact relied-upon versions and provenance while keeping reconstruction/replay derived, read-only and non-authoritative and showing uncertainty/deletion gaps honestly.

Completion evidence: [`P4.04 Version / Event / provenance / reconstruction review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`, four functional cross-review iterations and green full reference CI (`Reference Python CI #132`, `456` tests).

### P4.05 — Governed Execution, gate and approval/action experience

Provides bounded consequential-work inspection and action intent through Governed Execution, with exact Workflow/material-input/Product Contract pins, distinct Authorization/Organizational Authority/approval evidence, fail-closed unresolved gates and existing governed runtime mutation paths.

Completion evidence: [`P4.05 Governed Execution / gate / approval-action review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`, four functional cross-review iterations, executable static demo and green full reference CI.

### P4.06 — Document / Artifact workspace experience

Exercises CAP-001/RFC-0008 with logical Document, exact Version, Artifact, integrity/rendition/locator separation, transient candidate non-promotion, derivation provenance and purpose/right/classification handling controls. No DMS, object store, OCR or signing provider is selected.

Completion evidence: [`P4.06 Document / Artifact workspace review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`, five functional cross-review iterations and green `Reference Python CI #154`, `495` tests, `OK`.

### P4.07 — Memory / Knowledge / Search discovery experience

Exercises CAP-002/CAP-003 without conflating retrieval with authority: Observation, Memory, Knowledge Candidate and validated Knowledge remain distinct; exact/fresh Knowledge reliance is explicit; Search remains derived; purpose/classification/rights/minimization controls remain enforced.

Completion evidence: [`P4.07 Memory / Knowledge / Search discovery review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`, five functional cross-review iterations and `Reference Python CI #164`, `521` tests, `OK`.

### P4.08 — Cross-capability task/context composition + bounded product entry point

Proves one Provisional Product Contract-backed product entry point can compose the existing P4.06 Document/Artifact and P4.07 Memory/Knowledge surfaces while preserving exact Product Contract/dependency/Actor/Organization/task-target continuity, product-owned disposition semantics and the R10 consequential-action choke point.

Completion evidence: [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`, six functional cross-review iterations. The Product Contract remains `Provisional 0.1.0`.

### P4.09 — Security, rights, minimization and authority-safe UX

Hardens the presentation boundary so denied, wrong-Organization, missing, ambiguous or stale authorization does not expose governed content, protected counts or stale previews. `authority_safe_ux` consumes authorization evidence but owns no IAM/policy/Organizational Authority semantics.

Completion evidence: [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`.

### P4.10 — Workspace architecture fitness + accessibility/usability baseline

Cross-cutting executable evidence covers Organization isolation, identity attribution, authority separation, canonical/derived distinction, exact-version reliance, provenance honesty, Product Contract integrity, Document/Knowledge semantics, fail-closed actions, domain neutrality, accessibility baseline, deterministic states and presentation reversibility.

Completion evidence: [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`. [`P4.10 Hosted CI Validation Evidence`](../reviews/P4-10-ci-validation.md) confirms Reference Python CI #191 with `559 tests`, `OK`.

### P4.11 — Workspace hardening / ADR / refactoring review

Re-opened presentation-domain, refactoring, authority-bypass, derived-state/read-model, ADR, accessibility/operator-error and performance gates. It found no material product/domain leakage, action bypass, derived-state authority drift, ADR-triggering stable/durable choice, accessibility/operator-error defect or measured performance need. No material runtime refactor is justified; R12-F1 remains fixed.

Completion evidence: [`P4.11 Workspace hardening / ADR / refactoring review`](../reviews/P4-11-workspace-hardening-adr-refactoring-review.md) — `PASS`, four cross-review iterations. Final synchronized PR validation: `Reference Python CI #200`, `570 tests`, `OK`.

### P4.12 — Phase 4 / M4 closure review

Canonical closure review over the complete accumulated Phase 4 evidence.

Completion evidence: [`P4.12 Phase 4 / M4 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — **`PASS — M4 achieved for the declared bounded governed-workspace reference scope.`**

The closure keeps roadmap completion, Platform Capability lifecycle, operational environment/readiness, Product Contract stability, conformance scope and public compatibility/SLA/support claims explicitly distinct.

## 5. Engineering / quality gates

| Gate | Trigger | Purpose |
|---|---|---|
| `R9 — Workspace Boundary Review` | after P4.02 | **Complete / PASS** — shell/navigation does not create authority, product leakage or accidental public boundary; P4.03 source-resolution handoff recorded |
| `R10 — Operator Safety / Cross-Capability Health Review` | after P4.07 | **Complete / PASS** — current source-access freshness is enforced at operator action composition; material stale-source-access finding remediated |
| `R11 — Composition / Usability Refactoring Review` | after P4.08 / meaningful usability evidence | **Complete / PASS** — product-backed composition remains bounded and semantically explicit; no action bypass or ADR trigger found |
| `R12 — M4 Workspace Hardening` | after P4.10 | **Complete / PASS** — one material stale-presentation authorization-continuity defect remediated; dependency, authority-bypass, accessibility, deterministic-state and ADR-gate hardening passed |

Engineering gates are review/hardening gates and do not inflate roadmap completion percentages as separate equal-weight product tasks.

## 6. Dependency-aware sequence

```text
M3 ✅ Shared Capability baseline
        ↓
P4.01 Operator journeys + IA ✅
        ↓
P4.02 Organization/identity navigation shell ✅
        ↓
R9 Workspace Boundary Review ✅
        ↓
 ┌──────────┼───────────────┐
 ↓          ↓               ↓
P4.03 ✅   P4.04 ✅        P4.05 ✅
Records     Provenance      Execution
 └──────────┼───────────────┘
            ↓
 ┌──────────┴─────────┐
 ↓                    ↓
P4.06 ✅              P4.07 ✅
Docs                  Knowledge/Search
 └──────────┬─────────┘
            ↓
R10 Cross-Capability Health ✅
            ↓
P4.08 Product-backed composition proof ✅
            ↓
R11 Composition/Usability Refactoring ✅
            ↓
P4.09 Security / rights / authority-safe UX ✅
            ↓
P4.10 Fitness + accessibility/usability evidence ✅
            ↓
R12 M4 Hardening ✅
            ↓
P4.11 ADR / boundary / refactoring review ✅
            ↓
P4.12 Closure review ✅
            ↓
M4 Coherent governed workspace baseline ✅
```

Phase 4 is complete. The planning transition now moves to Phase 5 boundary revalidation/decomposition without automatically activating Phase 5 or stabilizing any interface.

## 7. M4 exit criteria

M4 is achieved because all of the following hold within the declared bounded reference scope:

1. a coherent domain-neutral workspace exists over governed platform state;
2. Organization scope and operator identity are explicit and preserved;
3. an operator can inspect Canonical Records, immutable versions and Typed Relationships without losing authority/version meaning;
4. Event/provenance/reconstruction history is understandable and derived reconstruction remains non-authoritative;
5. consequential operator actions flow through Governed Execution with distinct Authorization and Organizational Authority gates;
6. Document/Artifact and Memory/Knowledge/Search capability slices are usable without collapsing their Accepted semantic distinctions;
7. at least one Product Contract-backed bounded product entry point composes shared workspace surfaces without private platform coupling;
8. cross-capability security, rights, minimization and Organization isolation pass fitness tests;
9. core operator journeys meet the declared accessibility/usability baseline;
10. presentation/read-model/cache state cannot become independent canonical authority;
11. all crossed ADR gates, if any, have canonical dispositions;
12. R9–R12 are complete and material findings are resolved or explicitly bounded;
13. P4.12 closure review passes and records M4 achieved.

Canonical criterion-by-criterion evidence is recorded in [`P4.12 — Phase 4 / M4 Closure Review`](../reviews/P4-12-phase-4-m4-closure-review.md).

## 8. Explicit non-goals

M4 closure does not require or promise:

- a polished commercial design system or final brand UI;
- complete product UX for Tender, Marketing, Sales or any other domain;
- mobile applications;
- marketplace or extension UI;
- production IAM/SSO;
- notifications infrastructure;
- a stable public REST/GraphQL/gRPC API;
- a stable public frontend SDK;
- a specific frontend framework;
- microfrontends or microservices;
- durable cache/search/index infrastructure;
- production HA/SLA/support;
- lifecycle `Active` promotion of CAP-001 through CAP-004;
- a Stable P4.08 Product Contract;
- formal WCAG certification;
- full RFC-0001–RFC-0008 or full-platform conformance.

## 9. ADR gate

Re-open the ADR gate before material reliance on a concrete choice that becomes durable or externally constraining, including:

- frontend/runtime framework as a stable cross-product boundary;
- BFF/API topology or stable wire/serialization contract;
- authentication/session/IAM enforcement mechanism;
- durable workspace/read-model/cache storage;
- search/index technology relied upon beyond replaceable projection semantics;
- document/object storage topology;
- stable design-system/package compatibility boundary;
- separately deployable UI/API service topology.

A reversible internal reference implementation may proceed without an ADR when these thresholds are not crossed.

## 10. Current canonical action

> **Phase 5 boundary revalidation and decomposition — SDK, Contracts and Extension Experience.**

Phase 5 remains `Draft`. Revalidate its scope against M4 evidence and actual product/extension demand before activation, then create a bounded P5 work breakdown and exit criteria. The transition must preserve the distinction among roadmap phase state, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance scope and public/commercial commitments.
