# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.36.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.36.0` records completion of **P5.07 — Event/provenance/portability integration support** with `PASS` and advances the current canonical action to **P5.08 — Workspace/capability integration adapters without private coupling**.

P5.07 adds the smallest bounded internal/provisional integration-evidence helper above the R14-hardened composition path. Canonical Event admission, duplicate-delivery behavior and Event identity-conflict semantics remain owned by the existing P2.05 Event/provenance runtime rather than being reimplemented by integration tooling.

The new integration evidence preserves exact actual/represented Actor, Product, Product Contract Subject/Version, Execution Subject/Version and Event identity/version context. Derived telemetry is explicitly non-authoritative; the portable semantic fixture is explicitly non-canonical and preserves identity roles and semantic links without fabricating RFC-0002 Canonical Typed Relationships.

P5.07 intentionally selects no broker, Event store, tracing backend, schema registry, export endpoint, freshness registry, stable serialization/wire format or public SDK/API boundary. Hosted `Reference Python CI #237` passed the full 653-test reference suite with result `OK`, including all 9 focused P5.07 regression/fitness cases.

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
- [`P5.02 Product Contract declaration/validation review`](../reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md) — `PASS`;
- [`R13 Integration Boundary Review`](../reviews/R13-integration-boundary-review.md) — `PASS` after R13-F1 remediation;
- [`P5.03 governed dependency/version resolution review`](../reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) — `PASS`;
- [`P5.04 integration composition facade review`](../reviews/P5-04-integration-composition-api-facade-boundary.md) — `PASS`;
- [`P5.05 scaffolding/templates + local harness review`](../reviews/P5-05-scaffolding-templates-local-integration-harness.md) — `PASS`;
- [`P5.06 security/authority/rights Organization-scope integration-guard review`](../reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md) — `PASS`;
- [`R14 Developer Safety / Contract Health Review`](../reviews/R14-developer-safety-contract-health-review.md) — `PASS` after R14-F1/R14-F2 remediation;
- [`P5.07 Event/provenance/portability integration-support review`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`;
- hosted `Reference Python CI #237` — `PASS`, 653 tests, including all 9 focused P5.07 regressions and the accumulated reference architecture-fitness suite;
- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`;
- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Active`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 Product Contract remains `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3/M4/P5.02/R13/P5.03/P5.04/P5.05/P5.06/R14/P5.07 is achieved;
- no stable/public SDK, API, wire, manifest, package, registry, facade, scaffolding, event-transport, portability-serialization, IAM/policy, freshness or generated-code compatibility boundary has been created by M4 or P5.01 through P5.07.

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
- [`P5.07 — Event/Provenance/Portability Integration Support`](../reviews/P5-07-event-provenance-portability-integration-support.md) — `PASS`.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P5.01` | Integration boundary revalidation + developer journeys | 🟩 Complete | `██████████ 100%` |
| `P5.02` | Product Contract declaration model + machine-checkable validation baseline | 🟩 Complete | `██████████ 100%` |
| `P5.03` | Governed dependency/version resolution + compatibility semantics | 🟩 Complete | `██████████ 100%` |
| `P5.04` | Integration composition API/facade boundary | 🟩 Complete | `██████████ 100%` |
| `P5.05` | Scaffolding/templates + local integration harness | 🟩 Complete | `██████████ 100%` |
| `P5.06` | Security, authority, rights + Organization-scope integration guards | 🟩 Complete | `██████████ 100%` |
| `P5.07` | Event/provenance/portability integration support | 🟩 Complete | `██████████ 100%` |
| `P5.08` | Workspace/capability integration adapters without private coupling | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.09` | Second materially distinct integration reuse proof | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.10` | Phase 5 conformance + architecture fitness matrix | ⬜ Cross-cutting | `░░░░░░░░░░ 0%` |
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | ⬜ Planned | `░░░░░░░░░░ 0%` |
| `P5.12` | Phase 5 / M5 closure review | ⬜ Planned | `░░░░░░░░░░ 0%` |

P5.01/P5.02/R13/P5.03/P5.04/P5.05/P5.06/R14/P5.07 establish these minimum integration-boundary invariants:

- Product Contract is the governed boundary authority; tooling must not create a second contract system;
- relied-upon dependencies, operations and versions remain exact and inspectable;
- exact dependency compatibility is determined from explicit governed evidence rather than implementation/package shape or inferred SemVer ranges;
- dependency provider/consumer responsibilities and dependency/operation failure semantics remain available from the exact effective Product Contract boundary;
- derived declaration-validation and compatibility evidence remain evidence tied to the exact Product Contract Version rather than independently evolving contract sources;
- ambiguous, unsupported, deprecated and retired reliance fails closed deterministically and changed reliance exposes migration obligations;
- integration facade construction must pass through the governed P5.02/P5.03 factory path rather than accepting caller-fabricated derived evidence as a normal developer path;
- dependency-backed J1/J2 facade actions require explicit current governed dependency/version evidence and re-run P5.03 resolution instead of self-advancing composition-time compatibility snapshots;
- composition-time compatibility remains immutable inspection/history evidence, not current provider-support authority;
- product-owned proved J1/J2 entry passes through one internal/provisional composition facade instead of importing the private platform module graph;
- capability admission, workspace presentation authority and Governed Execution remain delegated to existing semantic owners rather than being reimplemented by the facade;
- P5.05 scaffolding imports Arvectum OS through the P5.04 facade, remains readable/replaceable and does not copy bounded-product implementation or contract/resolution logic;
- the local harness requires explicit Product Contract/version/dependency evidence and preserves a non-authoritative workspace without production infrastructure;
- wrong-Organization actor/request/Event-reference paths fail closed at composition/admission boundaries;
- Product Contract/capability admission grants no Authorization, permission, Organizational Authority or approval;
- P3.07 purpose/right/classification constraints remain effective after contract/capability admission;
- RFC-0005 Authorization, Organizational Authority, Data Governance and approval remain independently required execution-time gates;
- stale gate decisions, stale Product Contract continuity and stale composition-time dependency-support evidence cannot silently self-advance;
- integration-originated canonical Events preserve exact Actor/Product/Product Contract/Execution attribution and retain P2.05 as their semantic owner;
- Event correlation and causation remain explicit and version-aware rather than inferred from telemetry;
- derived telemetry remains non-authoritative and cannot mint permission, authority, approval or canonical state;
- portable integration fixtures preserve identity roles and semantic links while remaining derived/non-canonical and vendor/serialization neutral;
- direct implementation-private imports/tables/stores/routes/Event streams cannot become the integration contract;
- product-specific semantics remain product-owned;
- Product Contract lifecycle and capability lifecycle remain distinct;
- current declaration/validation/resolution/facade/scaffolding/harness/guard/event-evidence surfaces remain internal/provisional until evidence and governance justify otherwise;
- no representation, packaging, version-resolution, facade, scaffolding, event-transport, portability-serialization, IAM/policy, freshness-registry or generated-code mechanism is stable/public merely because the reference implementation exists.

Engineering gates: `R13 — Integration Boundary Review` — `Complete / PASS`; `R14 — Developer Safety / Contract Health Review` — `Complete / PASS after R14-F1/R14-F2 remediation`; `R15 — Reuse / Developer Experience Refactoring Review` and `R16 — M5 Integration Hardening` remain future gates. They do not inflate Phase 5 percentage as separate equal-weight roadmap tasks.

## 7. M5 target

`M5 — Repeatable product/extension integration` requires repository evidence that at least two materially distinct bounded integrations can rely on the same explicit Product Contract/integration boundary and reusable tooling without private platform coupling, while preserving exact dependency/version identity, Organization isolation, Authorization/Organizational Authority separation, governed canonical mutation, Event/provenance attribution, portability and product ownership of product-specific semantics.

M5 does not require a public SDK, Stable Product Contract or production deployment. Any stable/public compatibility boundary must be governed separately when evidence justifies it.

## 8. Current canonical action

> **P5.08 — Workspace/capability integration adapters without private coupling.**

Demonstrate consumption of M3/M4 workspace/capability surfaces through explicit integration boundaries without private imports or shared-state shortcuts. Keep capability-specific authority, freshness, rights and data-governance semantics with their existing owners, keep product-specific semantics product-owned, and do not infer capability promotion or a Stable/public adapter contract from the reference implementation.

## 9. ADR and Product Contract gate

Re-open the ADR/governance gate before material reliance on a language-specific SDK/package boundary, stable/public API or wire/serialization contract, package registry/distribution topology, plugin loading/sandboxing mechanism, extension registry topology, version-negotiation/migration/freshness protocol, generated-code compatibility boundary or separately deployable integration service.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

Extension registration, Product Contract admission, validation, dependency resolution, facade composition, scaffolding/harness convenience, Event/telemetry/portable evidence or technical tool access does not itself grant Authorization or Organizational Authority.

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
P5.08 Workspace/capability adapters ← current
        ↓
M5 Repeatable product/extension integration
        ↓
Phase 6 — Product-driven Platform Validation DRAFT / Near-term
```
