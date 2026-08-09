# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.43.0`
Created: `2026-08-07`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

The Strategic Roadmap beyond completed work is a planning hypothesis, not an architecture contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

Detailed completed-phase evidence remains in the corresponding `PHASE-N-...` roadmap and closure-review artifacts rather than being duplicated indefinitely here.

## 2. Version note

Version `2.43.0` records **P5.12 — Phase 5 / M5 closure review** with `PASS`, closes Phase 5 and marks **M5 — Repeatable product/extension integration** as `Achieved` for the declared bounded reference scope.

P5.12 re-checked all 14 M5 exit criteria against P5.01–P5.11, R13–R16, the P5.10 `CF-01` through `CF-15` matrix, P5.11 public-boundary disposition, current Product Contract/capability lifecycle state and hosted executable evidence.

One subordinate closure-hygiene finding, P5.12-F1, was identified: root `README.md` still reflected the earlier P5.10/R16 planning state while this roadmap already pointed to P5.12. The closure synchronizes that summary. No runtime or architectural change was required.

M5 closure does **not** stabilize either Product Contract, promote any capability to `Active`, establish a public SDK/API/wire/package boundary, approve Production/operational readiness, expand conformance to full-platform scope or create SLA/support/commercial commitments.

## 3. Verified architecture and milestone baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Phase 0 / `M0` — complete / achieved;
- Phase 1 / `M1` — complete / achieved for its declared scope;
- Phase 2 / `M2` — complete / achieved for the bounded reusable-runtime reference scope;
- Phase 3 / `M3` — complete / achieved for the bounded shared-capability reference scope;
- Phase 4 / `M4` — complete / achieved for the bounded governed-workspace reference scope;
- Phase 5 / `M5` — complete / achieved for the bounded repeatable product/extension integration reference scope;
- [`P5.12 closure review`](../reviews/P5-12-phase-5-m5-closure-review.md) — `PASS`;
- [`P5.10 conformance + architecture fitness matrix`](../reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md) — `PASS`, CF-01 through CF-15;
- [`R16 M5 Integration Hardening`](../reviews/R16-m5-integration-hardening.md) — `PASS` after R16-F1 remediation;
- [`P5.11 compatibility / ADR / public-boundary hardening`](../reviews/P5-11-compatibility-adr-refactoring-public-boundary-hardening-review.md) — `PASS`, explicit no-ADR/no-public-boundary disposition;
- final synchronized pre-closure hosted baseline: `Reference Python CI #269`, Ubuntu 24.04.4, CPython 3.12.13, `704 tests`, `OK`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 bounded Product Contract remains `Provisional 0.1.0`;
- P5.09 evidence-extension Product Contract remains `Provisional 0.1.0`;
- no Platform Capability becomes `Active` through M5 closure;
- no Stable/public SDK, API, wire, manifest, package, registry, facade, adapter, plugin-runtime, generated-code, service or component-system compatibility boundary is created through M5 closure.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Executed | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Near-term | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 4 — Workspace / Operator Experience

Canonical detailed record:

- [`PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md`](PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) — `Complete`, M4 `Achieved`;
- [`P4.12 — Phase 4 / M4 Closure Review`](../reviews/P4-12-phase-4-m4-closure-review.md) — `PASS`.

M4 proves a coherent governed workspace baseline over explicit Organization/Actor context, canonical records/versions/relationships, Event/provenance/reconstruction, Governed Execution, Document/Artifact and Memory/Knowledge/Search semantics, bounded Product Contract-backed composition and scoped security/accessibility fitness evidence.

M4 does not imply production readiness, capability lifecycle `Active`, Stable Product Contract/public API status, formal WCAG/full-platform conformance, SLA/support or final commercial UX.

## 6. Completed Phase 5 — SDK, Contracts and Extension Experience

Canonical detailed record:

- [`PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md`](PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md) — `Complete`, M5 `Achieved`;
- [`P5.12 — Phase 5 / M5 Closure Review`](../reviews/P5-12-phase-5-m5-closure-review.md) — `PASS`.

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
| `P5.11` | Compatibility / ADR / refactoring / public-boundary hardening review | 🟩 Complete | `██████████ 100%` |
| `P5.12` | Phase 5 / M5 closure review | 🟩 Complete | `██████████ 100%` |

Engineering gates:

- `R13 — Integration Boundary Review` — `PASS after R13-F1 remediation`;
- `R14 — Developer Safety / Contract Health Review` — `PASS after R14-F1/R14-F2 remediation`;
- `R15 — Reuse / Developer Experience Refactoring Review` — `PASS after R15-F1/R15-F2 remediation`;
- `R16 — M5 Integration Hardening` — `PASS after R16-F1 remediation`.

M5 proves that two materially distinct bounded consumers can use the same explicit Product Contract/dependency/composition/adapter method without private platform coupling while preserving exact versions, Organization isolation, Authorization/Organizational Authority separation, governed canonical mutation, Event/provenance, rights/minimization, portability and consumer ownership of consumer-specific semantics.

The two bounded executable Product Contracts remain `Provisional 0.1.0`. CAP-001 through CAP-004 remain `Incubating / Provisional`. M5 is reuse evidence, not a Product Contract stabilization or capability activation decision.

P5.11 remains the controlling public-boundary disposition: current Python modules, scaffolding, facade, adapters and harness are internal/provisional reference implementation, not a supported public SDK/API/package/wire contract.

## 7. M5 closure state

`M5 — Repeatable product/extension integration` is **Achieved** for the declared bounded reference scope.

The closure is based on:

- explicit Product Contract declaration/validation;
- exact governed dependency/version compatibility;
- current dependency-support evidence at reliance time;
- shared internal/provisional composition + adapter tooling;
- first bounded product integration;
- materially distinct CAP-004 read-only evidence/reconstruction extension;
- fail-closed security/authority/rights/Organization behavior;
- Governed Execution and Event/provenance continuity;
- vendor-neutral semantic portability;
- P5.10 CF-01 through CF-15 positive + negative evidence;
- resolved R13–R16 findings;
- P5.11 no-ADR/no-public-boundary decision;
- P5.12 explicit closure review.

M5 does not require and does not imply a public SDK, Stable Product Contract, Active capability or production deployment.

## 8. Current canonical planning action

Phase 5 is closed. **Phase 6 remains `Draft`; it is not automatically activated by M5.**

The next planning action is:

> **Phase 6 — Product-driven Platform Validation: boundary revalidation and decomposition against real product needs.**

Before Phase 6 implementation is marked `Active`, re-check actual product evidence, Product Contract boundaries, current capability lifecycle/review state, security/governance constraints and the smallest reversible work breakdown that advances real product validation.

Do not treat the Strategic Roadmap's Phase 6–8 rows as delivery promises or pre-approved architecture.

## 9. ADR, lifecycle and Product Contract gates carried forward

P5.11 records an explicit **no-ADR / no-public-boundary** disposition for the current integration implementation.

Re-open the ADR/governance gate before material reliance on a language-specific supported SDK/package, Stable/public API or wire/serialization contract, package registry/distribution topology, plugin loader/sandbox, extension registry/discovery topology, automated version-negotiation/freshness protocol, generated-code compatibility boundary, separately deployable integration service or stable design-system/component contract.

A real Product relying on Incubating capabilities, canonical platform state or shared platform history must use the applicable RFC-0004 Product Contract before governed reliance.

No capability may become `Active` without separate RFC-0001 lifecycle admission, applicable Stable contract/compatibility/migration evidence, operational-readiness approval and decision authority.
