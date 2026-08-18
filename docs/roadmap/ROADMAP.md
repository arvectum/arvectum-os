# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.54.6`
Created: `2026-08-07`
Updated: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override Constitution, Accepted RFC/ADR, approved governance, Product Contracts or implementation evidence.

Future roadmap content is a planning hypothesis until its phase is activated. Roadmap status does not by itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

## 2. Version note

Version `2.54.6` synchronizes the master roadmap with active Phase 7 `1.2.2` after the P7.04 repository implementation milestone. No additional implementation or lifecycle claim is introduced by this synchronization.

Version `2.54.5` recorded the repository-side implementation milestone for `P7.04 — Persistent identity/operator/service access + least-privilege operations` after PR `#35` merged at `2b808c658c19056cef65b69e82152ae12d861679`.

The bounded repository implementation now provides exact P6.05-L4 Organization/human identity continuity, one attributable persistent service principal, deny-by-default exact Organization/operation/resource/access-path grants, owner-local credential issuance/rotation/revocation, principal/grant revocation, explicit local/remote access scoping and a hardened selected-Mac proof wrapper. Technical access remains explicitly separate from Organizational Authority and consequential approval. No roles, wildcard grants, superuser or ambient-admin bypass were introduced.

Repository evidence for PR `#35`:

- focused persistent-access tests: `14/14 PASS`;
- selected-Mac proof-contract tests: `2/2 PASS`;
- GitHub `Reference Python CI` on implementation/documentation head `b9c46646324d5d4bccf384196efa3670b828c6af`: `success`, run `32063442269`;
- canonical implementation: [`P7.04 Persistent Identity / Operator / Service Access`](../implementation/P7-04-PERSISTENT-IDENTITY-ACCESS.md) — `Repository implementation PASS / selected-Mac closure pending`;
- repository functional cross-review: `PASS / selected-Mac closure pending`.

`P7.04` is **not** `Complete / PASS` yet. The current canonical action remains the selected-Mac closure proof on clean exact canonical `main`, using the existing healthy P7.02 persistent runtime and the retained P6.05-L4 owner context. Only a passing selected-Mac operational attestation may close P7.04 and advance to P7.05.

Version `2.54.4` closed `P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline` after repository implementation, proof-contract hardening, preserved failed attempts, successful hardened selected-Mac Attempt 3 and final six-iteration functional cross-review.

Repository implementation PR `#30` merged at `e2440b6f8afc7e0f21b20d370047bfa3ac803017` and full Reference Python CI passed `932/932`. After Attempt 1 exposed an evidence-contract inconsistency, PR `#31` added the dedicated hardened selected-Mac wrapper and merged at `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`; full Reference Python CI passed `935/935`.

`P7.03 = Complete / PASS` for the declared `Persistent Internal / owner-operated` scope. The bounded owner-local filesystem/tar adapter remains private, reversible and non-stable. No Accepted ADR is required at this scope, and no external/customer Production, `Active` Platform Capability, Stable Product Contract, SLA/SLO/RPO/RTO/support or permanent persistence technology claim is created.

Version `2.54.3` closed `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle` after remediated selected-Mac Attempt 2 passed. The selected Mac mini entered regular `Persistent Internal / owner-operated` Arvectum OS operation. This is an operational-mode transition only and does not create external/customer Production, an `Active` Platform Capability, a Stable Product Contract, SLA/support, a supported macOS matrix or stable deployment/service topology.

Version `2.54.0` closed `P7.01 — Persistent internal operating boundary + operational requirements baseline` and recorded `R21 — Operational Boundary Review = PASS`.

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

Phase status, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 5. Completed Phase 6 / M6

Detailed roadmap: [`PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`](PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md).

Phase 6 completed with two materially distinct real-product/workflow chains: Tender Operator exact real tender evidence and Discount Parser real Telegram publication evidence reconstructed through CAP-004 without effect replay. The M6 Milestone Code Health Gate is `Complete / PASS`.

`M6 = achieved for the declared bounded scope.`

## 6. Active Phase 7 — Operational / Enterprise Readiness

Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Active 1.2.2`.

Phase 7 converts validated owner-operated use into a persistent, recoverable and observable internal operating baseline before considering stronger production/lifecycle claims.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P7.01` | Persistent internal operating boundary + operational requirements baseline | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.02` | Persistent Mac mini runtime + boot/restart/service lifecycle | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.03` | Durable governed state/checkpoint persistence + backup/restore baseline | 🟩 Complete / PASS | `██████████ 100%` |
| `P7.04` | Persistent identity/operator/service access + least-privilege operations | 🟨 Repository implementation PASS / selected-Mac closure pending | `repository PASS; operational proof pending` |
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

```text
P7.01 operational boundary — PASS
        ↓
R21 boundary review — PASS
        ↓
P7.02 persistent Mac mini runtime — PASS
        ↓
ARVECTUM OS ENTERS REGULAR PERSISTENT INTERNAL USE
        ↓
P7.03 durable-state/backup-restore baseline — PASS
        ↓
P7.04 repository implementation — PASS
        ↓
P7.04 selected-Mac operational proof ← current
        ↓
P7.05–P7.12 continue hardening the live operating baseline
```

P7.02 passed on exact selected-Mac release `73af746f83271b14670fe22db658dfd55cacb291`. P7.03 subsequently established the bounded durable-state/checkpoint and backup/restore baseline. P7.04 repository implementation is merged but has not yet passed the selected-Mac closure proof.

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

Phase 8 remains Draft until M7 closes and its external boundary is revalidated.

## 9. ADR, lifecycle and stable-boundary rule

Phase 7 may create pressure to choose concrete durable persistence, service-management, IAM, serialization, API, storage or deployment mechanisms. Use the lowest sufficient decision level. If a choice becomes materially constraining, cross-product, externally relied upon or expensive to reverse, stop at the applicable ADR/stable-boundary gate before further reliance.

No capability becomes `Active` and no Product Contract becomes `Stable` through roadmap progress alone.

## 10. Phase transition rule

Phase 8 remains `Draft / Exploratory` until Phase 7 / M7 closes and the external ecosystem boundary is revalidated against actual operational evidence, external demand, rights, Organization isolation, portability and commercial commitments.

A roadmap phase transition does not itself change lifecycle, production readiness, conformance or commercial status.

## 11. Current canonical action

> **P7.04 — selected-Mac persistent access closure proof.**

Repository implementation is merged and its CI is green. Execute one clean `p7_04_selected_mac_proof.py` run on the selected ООО «Арвектум» Mac mini from exact canonical `main`, against the existing healthy P7.02 runtime and retained P6.05-L4 owner context. Preserve the produced non-canonical attestation and review it canonically. If the proof passes without material objections, close P7.04 and advance to P7.05; otherwise record the failure and remediate without weakening RFC-0003/RFC-0005 authority boundaries.
