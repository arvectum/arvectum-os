# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.41.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.41.0` records completion of **R16 — M5 Integration Hardening** with `PASS after R16-F1 remediation` and advances the current canonical action to **P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review**.

R16 re-opened the accumulated P5.10 `CF-01` through `CF-15` evidence as a correctness/security/compatibility/maintainability review. One material continuity defect was found: `IntegrationCapabilityAdapter` could be paired with an alternate same-version `ProductContract` value whose deeper declaration semantics differed from the declaration already validated by the composed facade.

R16-F1 is remediated by reusing the existing P5.02 declaration validator and requiring exact equality with `facade.declaration_evidence` before capability delegation. Same-version bounded-scope or dependency-responsibility drift now fails closed without creating a second contract model, registry or new semantic owner.

Hosted `Reference Python CI #262` passed 695 tests with `OK` on the R16 implementation head, including all P5.10 matrix evidence and 7 focused R16 regressions. R16 creates no Product Contract or capability lifecycle promotion, Stable/public SDK/API/package boundary, plugin/extension registry/runtime, new authority source, operational-readiness claim, M5 claim or conformance expansion.

## 3. Verified architecture baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete / achieved;
- Phase 1 / `M1` — complete / achieved for its declared scope;
- Phase 2 / `M2` — complete / achieved for the bounded reusable-runtime reference scope;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- Phase 4 / `M4` — complete / achieved for the bounded governed-workspace reference scope;
- [`P4.12 closure review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`;
- [`P5.01 integration boundary revalidation`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`;
- [`P5.02 Product Contract declaration/validation review`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`, with P5.09-F1 internal refinement recorded in the P5.09/R15 evidence;
- [`R13 Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation;
- [`P5.03 governed dependency/version resolution review`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`;
- [`P5.04 integration composition facade review`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`;
- [`P5.05 scaffolding/templates + local harness review`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`;
- [`P5.06 security/authority/rights Organization-scope integration-guard review`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`;
- [`R14 Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation;
- [`P5.07 Event/provenance/portability integration-support review`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`;
- [`P5.08 workspace/capability integration-adapter review`](../reviews/P5-08-workspace-capability-integration-adapters.md) — `PASS`;
- [`P5.09 second materially distinct integration reuse proof`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md) — `PASS`;
- [`R15 Reuse / Developer Experience Refactoring Review`](../reviews/R15-reuse-developer-experience-refactoring-review.md) — `PASS` after R15-F1/R15-F2 remediation;
- [`P5.10 Phase 5 conformance + architecture fitness matrix`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`;
- [`R16 M5 Integration Hardening Review`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation;
- hosted `Reference Python CI #262` — `PASS`, 695 tests on the R16 implementation head;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`;
- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Active`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 bounded Product Contract remains `Provisional 0.1.0`;
- P5.09 evidence-extension Product Contract remains `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3/M4/P5.02/R13/P5.03/P5.04/P5.05/P5.06/R14/P5.07/P5.08/P5.09/R15/P5.10/R16 is achieved;
- no stable/public SDK, API, wire, manifest, package, registry, facade, scaffolding, adapter, event-transport, portability-serialization, IAM/policy, freshness, extension-runtime or generated-code compatibility boundary has been created by M4 or P5.01 through R16.

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

- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Active`;
- [`P5.01 — Integration Boundary Revalidation + Developer Journeys`](../reviews/P5-01-integration-boundary-revalidation-developer-journeys.md) — `PASS`;
- [`P5.02 — Product Contract Declaration Model + Machine-Checkable Validation Baseline`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`;
- [`R13 — Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation;
- [`P5.03 — Governed Dependency/Version Resolution + Compatibility Semantics`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`;
- [`P5.04 — Integration Composition API/Facade Boundary`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`;
- [`P5.05 — Scaffolding/Templates + Local Integration Harness`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`;
- [`P5.06 — Security, Authority, Rights + Organization-Scope Integration Guards`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`;
- [`R14 — Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation;
- [`P5.07 — Event/Provenance/Portability Integration Support`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`;
- [`P5.08 — Workspace/Capability Integration Adapters Without Private Coupling`](../reviews/P5-08-workspace-capability-integration-adapters.md) — `PASS`;
- [`P5.09 — Second Materially Distinct Integration Reuse Proof`](../reviews/P5-09-second-materially-distinct-integration-reuse-proof.md) — `PASS`;
- [`R15 — Reuse / Developer Experience Refactoring Review`](../reviews/R15-reuse-developer-experience-refactoring-review.md) — `PASS` after R15-F1/R15-F2 remediation;
- [`P5.10 — Phase 5 Conformance + Architecture Fitness Matrix`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`;
- [`R16 — M5 Integration Hardening`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P5.01` | Integration boundary revalidation + developer journeys | 🟩 Complete | `██████████ 100%` |
| `P5.02` | Product Contract declaration model + machine-checkable validation baseline | 🟩 Complete | `██████████ 100%` |
| `P5.03` | Governed dependency/version resolution + compatibility semantics | 🟩 Complete | `██████████ 100%` |
| `P5.04` | Integration composition API/facade boundary | 🟩 Complete | `██████████ 100%` |
| `P5.05` | Scaffolding/templates + local integration harness | 🟩 Complete | `██████████ 100%` |
| `P5.06` | Security, authority, rights + Organization-scope integration guards | 🟩 Complete | `██████████ 100%` |
| `P5.07` | Event/provenance/portability integration support | 🟩 Complete | `██████████ 100%` |
| `P5.08` | Workspace/capability integration adapters without private coupling | 🟩 Complete | `██████████ 100%` |
| `P5.09` | Second materially distinct integration reuse proof | 🟩 Complete | `██████████ 100%` |
| `P5.10` | Phase 5 conformance + architecture fitness matrix | 🟩 Complete | `██████████ 100%` |
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.12` | Phase 5 / M5 closure review | ⬜ Planned | `░░░░░░░░░░ 0%` |

P5.01 through P5.10, with R13/R14/R15/R16 gates, establish these minimum integration-boundary invariants:

- Product Contract is the governed boundary authority; tooling must not create a second contract system;
- relied-upon dependencies, operations and versions remain exact and inspectable;
- exact dependency compatibility is determined from explicit governed evidence rather than implementation/package shape or inferred SemVer ranges;
- dependency provider/consumer responsibilities and dependency/operation failure semantics remain available from the exact effective Product Contract boundary;
- derived declaration-validation and compatibility evidence remain evidence tied to the exact Product Contract Version rather than independently evolving contract sources;
- ambiguous, unsupported, deprecated and retired reliance fails closed deterministically and changed reliance exposes migration obligations;
- integration facade construction must pass through the governed P5.02/P5.03 factory path rather than accepting caller-fabricated derived evidence as a normal developer path;
- dependency-backed facade/adapter actions require explicit current governed dependency/version evidence and re-run P5.03 resolution instead of self-advancing composition-time compatibility snapshots;
- composition-time compatibility remains immutable inspection/history evidence, not current provider-support authority;
- capability-adapter construction requires Product Contract declaration semantics to match the exact P5.02 declaration evidence already validated by the composed facade, so same-version semantic drift fails closed;
- the first bounded product and second read-only extension each pass through the same internal/provisional `IntegrationAdapters` boundary rather than importing the private platform module graph;
- the reusable `IntegrationAdapters` stored core is limited to the exact facade plus capability delegation; workspace presentation is an explicit optional consumer binding rather than a universal integration assumption;
- capability admission, workspace presentation authority, CAP-004 reconstruction and Governed Execution remain delegated to existing semantic owners rather than being reimplemented by integration tooling;
- P5.05 scaffolding now imports Arvectum OS through the demonstrated `integration_adapters` seam, remains readable/replaceable and does not copy bounded-product implementation or contract/resolution logic;
- the local harness composes the same adapter core, requires explicit Product Contract/version/dependency evidence and preserves a non-authoritative workspace without production infrastructure;
- wrong-Organization actor/request/Event/evidence paths fail closed at composition/admission/capability boundaries;
- Product Contract/capability admission grants no Authorization, permission, Organizational Authority or approval;
- P3.07 purpose/right/classification constraints remain effective after contract/capability admission;
- RFC-0005 Authorization, Organizational Authority, Data Governance and approval remain independently required execution-time gates;
- stale gate decisions, stale Product Contract continuity and stale composition-time dependency-support evidence cannot silently self-advance;
- integration-originated canonical Events preserve exact Actor/Product/Product Contract/Execution attribution and retain P2.05 as their semantic owner;
- Event correlation and causation remain explicit and version-aware rather than inferred from telemetry;
- derived telemetry and CAP-004 reconstruction remain non-authoritative and cannot mint permission, authority, approval or canonical state;
- P5.09-F1 distinguishes a derived read-only Product Contract operation from direct canonical access: absence of direct canonical access is allowed only when truthful, while declared direct Read and canonical Write/Organizational Authority requirements remain validated;
- portable integration fixtures preserve identity roles and semantic links while remaining derived/non-canonical and vendor/serialization neutral;
- direct implementation-private imports/tables/stores/routes/Event streams cannot become the integration contract;
- product/extension-specific semantics remain consumer-owned;
- Product Contract lifecycle and capability lifecycle remain distinct;
- current declaration/validation/resolution/facade/scaffolding/harness/guard/event-evidence/adapter surfaces remain internal/provisional until evidence and governance justify otherwise;
- no representation, packaging, version-resolution, facade, scaffolding, adapter, event-transport, portability-serialization, IAM/policy, freshness-registry, extension-runtime or generated-code mechanism is stable/public merely because the reference implementation exists;
- the P5.10 matrix is a machine-checked evidence index over these invariants and remains subordinate to their existing semantic owners.

Engineering gates: `R13 — Integration Boundary Review` — `Complete / PASS`; `R14 — Developer Safety / Contract Health Review` — `Complete / PASS after R14-F1/R14-F2 remediation`; `R15 — Reuse / Developer Experience Refactoring Review` — `Complete / PASS after R15-F1/R15-F2 remediation`; `R16 — M5 Integration Hardening` — `Complete / PASS after R16-F1 remediation`. They do not inflate Phase 5 percentage as separate equal-weight roadmap tasks.

## 7. M5 target

`M5 — Repeatable product/extension integration` requires repository evidence that at least two materially distinct bounded integrations can rely on the same explicit Product Contract/integration boundary and reusable tooling without private platform coupling, while preserving exact dependency/version identity, Organization isolation, Authorization/Organizational Authority separation, governed canonical mutation, Event/provenance attribution, portability and consumer ownership of consumer-specific semantics.

P5.09 satisfies the two-materially-distinct-integration reuse condition, R15 refined the shared seam from that evidence, P5.10 passed the accumulated conformance/fitness matrix, and R16 has hardened same-version Product Contract continuity at the adapter seam. M5 is **not yet achieved**: P5.11 and P5.12 remain applicable work items.

M5 does not require a public SDK, Stable Product Contract or production deployment. Any stable/public compatibility boundary must be governed separately when evidence justifies it.

## 8. Current canonical action

> **P5.11 — Compatibility / ADR / refactoring / public-boundary hardening review.**

Review the accumulated Phase 5 implementation for actual compatibility and architecture-governance thresholds. Determine whether any language SDK/package, public API/wire contract, registry/distribution mechanism, plugin/extension runtime, version-negotiation/migration/freshness mechanism, generated-code boundary, separately deployable integration service or stable design-system boundary is now materially relied upon. Create an ADR/RFC/policy only where the established threshold is actually crossed; otherwise record an explicit no-ADR/no-public-boundary disposition and preserve the internal/provisional implementation.

After P5.11, proceed to **P5.12 — Phase 5 / M5 closure review**.

## 9. ADR and Product Contract gate

Re-open the ADR/governance gate before material reliance on a language-specific SDK/package boundary, stable/public API or wire/serialization contract, package registry/distribution topology, plugin loading/sandboxing mechanism, extension registry topology, version-negotiation/migration/freshness protocol, generated-code compatibility boundary or separately deployable integration service.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

Extension registration, Product Contract admission, validation, dependency resolution, facade/adapter composition, scaffolding/harness convenience, Event/telemetry/portable/reconstruction evidence or technical tool access does not itself grant Authorization or Organizational Authority.

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
P5.01 Integration boundary + developer journeys ✓
        ↓
P5.02 Product Contract declaration/validation ✓
        ↓
R13 Integration Boundary Review ✓
        ↓
P5.03 Dependency/version + compatibility semantics ✓
        ↓
P5.04 Composition API/facade boundary ✓
        ↓
P5.05 Scaffolding/templates + local harness ✓
        ↓
P5.06 Security/authority/rights guards ✓
        ↓
R14 Developer Safety / Contract Health ✓
        ↓
P5.07 Event/provenance/portability support ✓
        ↓
P5.08 Workspace/capability adapters ✓
        ↓
P5.09 Second integration reuse proof ✓
        ↓
R15 Reuse / Developer Experience Refactoring ✓
        ↓
P5.10 Conformance + fitness matrix ✓
        ↓
R16 M5 Integration Hardening ✓
        ↓
P5.11 Compatibility / ADR / public-boundary review ← current
        ↓
P5.12 M5 closure
        ↓
M5 Repeatable product/extension integration
        ↓
Phase 6 — Product-driven Platform Validation DRAFT / Near-term
```
