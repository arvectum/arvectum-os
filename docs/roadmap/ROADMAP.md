# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.54.0`
Created: `2026-08-07`
Updated: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

Future roadmap content is a planning hypothesis until its phase is activated. Roadmap status does not by itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.54.0` closes `P7.01 — Persistent internal operating boundary + operational requirements baseline` and records `R21 — Operational Boundary Review = PASS` after two review iterations.

Canonical P7.01 evidence:

- [`P7.01 Persistent Internal Operating Boundary and Operational Requirements Baseline`](P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) — `Complete / Baseline 1.0.1`;
- [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) — `Complete / PASS`.

The P7.01 baseline fixes the initial operating classification as `Persistent Internal / owner-operated`, Organization scope as ООО «Арвектум», admitted bounded workload classes, data/secret/retention/authority/recovery/network/upgrade boundaries, explicit ADR/stable-boundary triggers and a rollback/removal path without choosing a permanent persistence, IAM, service, storage, API or deployment topology.

`P7.02` is now the current canonical action. After `P7.02 PASS`, the selected Mac mini enters regular persistent internal operation; dedicated repeatable product operational proof still remains `P7.07` for Tender Operator and `P7.08` for Discount Parser.

The Phase 7/8 strategic restoration remains governed by [`DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION.md`](../governance/decisions/DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION.md).

This persistent internal classification is not automatically an external/customer `Production` claim, supported macOS platform promise, `Active` capability transition, Stable Product Contract, SLA/support commitment or final deployment topology.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a persistence, IAM, service, deployment, public API, broker or storage topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 real Product Contracts remain `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because later phases consume or validate it;
- no Stable/public SDK/API/wire/service/deployment compatibility boundary has been established;
- no external Production/SLA/support/full-platform conformance claim is implied.

## 4. Strategic roadmap

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Executed | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Internal workspace/operator baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Executed | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Executed | 🟩 Complete / PASS | `M6` Real-product validation across two materially distinct workflows |
| `Phase 7` | Operational / Enterprise Readiness | Active | 🟨 Active | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |

Phase status, capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 6 / M6

Detailed roadmap: [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md).

Phase 6 completed with two materially distinct real-product/workflow chains:

1. Tender Operator — exact real tender package `7/7` admitted and governed/reconstructed;
2. Discount Parser — one explicitly authorized real Telegram publication with pre-effect evidence, confirmed external effect and read-only CAP-004 reconstruction without effect replay.

P6.07 Stage 2C recorded `9` targeted tests PASS and `911` full Reference Python tests PASS. P6.06 remained `Provisional 0.1.0`, CAP-004-only; CAP-004 remained `Incubating / Provisional`.

The required M6 Milestone Code Health Gate is [`M6-milestone-code-health-gate-governance-repair.md`](../reviews/M6-milestone-code-health-gate-governance-repair.md) — `Complete / PASS`. It was recorded transparently after the original closure publication when the missing gate artifact was discovered. No material defect required M6 reopening.

`M6 = achieved for the declared bounded scope.`

## 6. Active Phase 7 — Operational / Enterprise Readiness

Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Active 1.1.0`.

Phase 7 converts validated owner-operated use into a persistent, recoverable and observable internal operating baseline before considering stronger production/lifecycle claims.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P7.01` | Persistent internal operating boundary + operational requirements baseline | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.02` | Persistent Mac mini runtime + boot/restart/service lifecycle | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P7.03` | Durable governed state/checkpoint persistence + backup/restore baseline | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.04` | Persistent identity/operator/service access + least-privilege operations | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.05` | Health, observability, audit visibility, alerting + retention/minimization | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.06` | Governed deploy/update/rollback/version/migration path | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.07` | Persistent Tender Operator operational contour | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.08` | Persistent Discount Parser cross-host operational contour | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.09` | Operator runbook + incident/uncertain-outcome/recovery drills | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.10` | Portability, host-loss and restore-on-clean-environment proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.11` | Scoped operational-readiness, lifecycle, conformance + stable-boundary disposition | ⬜ | `░░░░░░░░░░ 0%` |
| `P7.12` | Phase 7 / M7 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Engineering/quality gates:

- [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md) — 🟩 `Complete / PASS` after P7.01;
- `R22 — Persistent Runtime Health Review` — after P7.05;
- `R23 — Recovery / Portability Review` — after P7.10;
- `R24 — M7 Operational Hardening + required Milestone Code Health Gate` — after P7.11 and before P7.12.

### Persistent Mac mini transition

The canonical persistent-use threshold is intentionally early:

```text
P7.01 operational boundary — PASS
        ↓
R21 boundary review — PASS
        ↓
P7.02 persistent Mac mini runtime
        ↓
PASS
        ↓
ARVECTUM OS ENTERS REGULAR PERSISTENT INTERNAL USE
        ↓
P7.03–P7.12 harden the live operating baseline
```

`P7.02 PASS` requires supervised start/stop/restart, boot/login lifecycle appropriate to the owner-operated model, source/runtime separation, secrets outside Git, bounded listener exposure, health evidence, crash/restart proof and rollback/removal path.

## 7. M7 milestone definition

`M7 — Scoped production-grade operating baseline` requires, within the declared scope:

1. persistent supervised owner-operated Arvectum OS runtime on the selected Mac mini;
2. durable required governed state with tested backup/restore;
3. persistent least-privilege identity/access/secrets operations;
4. actionable health/observability without telemetry becoming authority;
5. governed deploy/update/rollback/version/migration path;
6. repeatable persistent Tender Operator reliance through its Product Contract;
7. repeatable Discount Parser cross-host evidence/reconstruction through its Product Contract;
8. executable incident/recovery procedures;
9. host-loss/portability proof on a clean secondary environment;
10. explicit lifecycle/conformance/stable-boundary dispositions;
11. R21–R24 material findings closed or accepted by appropriate authority;
12. pre-closure M7 Milestone Code Health Gate PASS.

M7 does not inherently require an external customer Production deployment, public multi-tenant service, `Active` capability, Stable Product Contract, public SDK/API or SLA/support promise.

## 8. Draft Phase 8 — Ecosystem and External Integration

Detailed draft: [`PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`](PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md) — `Draft / Exploratory 0.1.0`.

Draft work items:

- `P8.01` External ecosystem target + evidence baseline;
- `P8.02` Cross-Organization identity/trust/rights/data-governance boundary;
- `P8.03` External Product Contract/integration-contract + stable-surface decision;
- `P8.04` External authoritative-system connector validation;
- `P8.05` Event/ingress/egress/duplicate/replay/reconciliation semantics;
- `P8.06` External extension/product onboarding + governed dependency resolution;
- `P8.07` Portability/export/migration/customer handover interoperability;
- `P8.08` Multi-Organization isolation + cross-organization security validation;
- `P8.09` External operator/developer integration experience + documentation;
- `P8.10` Scoped external conformance/commercial/support boundary review;
- `P8.11` Ecosystem architecture hardening + ADR/refactoring review;
- `P8.12` Phase 8 / M8 closure review.

Provisional gates R25–R28 are defined in the Phase 8 draft and must be revalidated before activation.

## 9. ADR, lifecycle and stable-boundary rule

Phase 7 may create pressure to choose concrete durable persistence, service-management, IAM, serialization, API, storage or deployment mechanisms.

Use the lowest sufficient decision level. Environment-specific reversible adapters do not automatically require ADRs. If a choice becomes materially constraining, cross-product, externally relied upon or expensive to reverse, stop at the applicable ADR/stable-boundary gate before further reliance.

No capability becomes `Active` and no Product Contract becomes `Stable` through roadmap progress alone.

## 10. Phase transition rule

Phase 8 remains `Draft / Exploratory` until Phase 7 / M7 closes and the external ecosystem boundary is revalidated against actual operational evidence, external demand, rights, Organization isolation, portability and commercial commitments.

A roadmap phase transition does not itself change lifecycle, production readiness, conformance or commercial status.

## 11. Current canonical action

> **P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle.**

P7.01 and R21 are complete. P7.02 is the first local Mac mini implementation step. After `P7.02 PASS`, Arvectum OS becomes a regular `Persistent Internal / owner-operated` runtime for ООО «Арвектум» while the remainder of Phase 7 hardens that live operating baseline. Repeatable persistent product contours are proven separately in P7.07 and P7.08.