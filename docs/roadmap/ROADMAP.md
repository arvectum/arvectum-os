# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.59.0`
Created: `2026-08-07`
Updated: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.59.0` closes `P8.00-A2 — Candidate triage and value test` as `Complete / PASS` and advances the current pre-activation action to `P8.00-A3 — Select one bounded external outcome`.

A2 qualitatively triaged only the three evidence-backed A1 candidates and produced one-item shortlist:

- ЕИС / `zakupki.gov.ru` authoritative tender-document boundary — `SHORTLIST_FOR_A3`.

A2 explicitly contains/defer the remaining candidates on current evidence:

- Telegram controlled external publication effect boundary — `CONTAIN_PRODUCT_LOCAL / NOT_SHORTLISTED` because M6/M7 already materially validated the same external-effect/reconstruction pressure and no broader generic Telegram/notification platform need is evidenced;
- Discount Parser public discount/promo source set — `DEFER_RIGHTS_GAP / NOT_SHORTLISTED` because source-specific permitted-use/redistribution/retention scope is not canonically established and the current adapter/normalization behavior remains product-owned.

The A2 shortlist does not platformize the EIS connector. A3 must define a materially new bounded EIS-related external outcome beyond the existing M6 retrieval proof or record `DEFER` rather than recycle old evidence.

Canonical facts preserved from `2.58.0`:

- `Phase 7 = Complete / PASS`;
- `M7 = achieved` for the declared `Persistent Internal / owner-operated` scope;
- all P7.01–P7.12 work, R21–R24 and the M7 Milestone Code Health Gate are complete;
- the selected Mac mini remains a persistent owner-operated Arvectum OS environment;
- the live private operator workspace is proven through real owner inspection and fail-closed governed interaction;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`;
- conformance remains `Scoped` for the local persistent-internal contour;
- no external/customer Production, Stable Product Contract, Active Platform Capability, public/stable API/wire/deployment surface, SLA/support or certification claim exists;
- Phase 8 remains `Draft / Exploratory` and has not been activated.

Phase 8 activation still requires completion of P8.00-A3 through A8, including one bounded outcome, explicit Organization/authority/data-rights scope, justified platform responsibility, stable/readiness/ADR gate disposition and fresh owner activation approval.

This planning update does not itself activate Phase 8 or create any external commitment.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a permanent persistence, IAM, service, public API, external Event transport, connector/plugin, broker or deployment topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 real Product Contracts remain `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3–M7 completed;
- no Product Contract becomes `Stable` through roadmap progress alone;
- phase status, capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity and commercial claims remain distinct.

## 4. Strategic roadmap

| Phase | Strategic scope | Status | Milestone |
|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | 🟩 Complete | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | 🟩 Complete | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | 🟩 Complete | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | 🟩 Complete / PASS | `M6` Real-product validation across materially distinct workflows |
| `Phase 7` | Operational / Enterprise Readiness | 🟩 Complete / PASS | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | ⬜ Draft / Exploratory | `M8` Governed external ecosystem baseline |

## 5. Completed platform progression

### Phase 0 / M0 — Architecture Bootstrap

Established the constitutional and RFC architecture baseline and the governance hierarchy used by all later phases.

### Phase 1 / M1 — Reference Implementation

Proved the first executable architectural spine without turning the reference technology into the platform contract.

### Phase 2 / M2 — Core Runtime

Established reusable governed runtime semantics including exact versions, relationships, execution, provenance and consistency behavior.

### Phase 3 / M3 — Shared Platform Capabilities

Validated the bounded shared-capability baseline. CAP-001 through CAP-004 remain `Incubating / Provisional`; M3 did not promote them to `Active`.

### Phase 4 / M4 — Workspace / Operator Experience

Established the domain-neutral operator workspace model covering Organization/Actor context, Records, Executions, Evidence, Documents, Knowledge and authority-safe governed actions without selecting a stable frontend/API technology.

### Phase 5 / M5 — SDK, Contracts and Extension Experience

Established repeatable explicit integration through Product Contracts and internal/provisional integration tooling without creating a public Stable SDK/API.

### Phase 6 / M6 — Product-driven Platform Validation

Validated the platform through two materially distinct real product/workflow contexts:

- Tender Operator exact real tender evidence with governed admission/reconstruction;
- Discount Parser controlled real Telegram publication evidence reconstructed through CAP-004 without effect replay.

M6 proved real-product value and reuse while keeping product business semantics product-owned.

### Phase 7 / M7 — Operational / Enterprise Readiness

Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Complete / PASS 1.2.18`.

M7 established the declared `Persistent Internal / owner-operated` operating baseline:

- persistent supervised Arvectum OS runtime on the selected Mac mini;
- durable governed state/checkpoint persistence;
- tested backup/restore and real selected-host-loss recovery;
- persistent least-privilege identity/operator/service access;
- health, observability, audit visibility and alerting;
- governed deploy/update/rollback/version/migration;
- live private operator workspace with real owner interaction;
- persistent Tender Operator reliance;
- repeatable Discount Parser Windows ↔ Mac mini reconstruction contour;
- executable incident/uncertain-outcome/recovery drills;
- scoped readiness/lifecycle/conformance/stable-boundary disposition;
- R21 through R24 and M7 Milestone Code Health Gate `Complete / PASS`.

Final M7 code-health evidence included `1192 tests / OK` on the hardening baseline.

M7 did **not** create external/customer Production, Active Platform Capabilities, Stable Product Contracts, public/stable interfaces, SLA/SLO/RPO/RTO/support commitments or certification.

## 6. Current operating state

Arvectum OS is no longer only a reference or proof runtime.

For the declared internal scope it currently has:

```text
Selected Mac mini
    ↓
Persistent Arvectum OS runtime            PASS
    ↓
Durable governed state + backup/restore  PASS
    ↓
Least-privilege identity/access          PASS
    ↓
Health / observability / audit visibility PASS
    ↓
Governed update / rollback               PASS
    ↓
Private live operator workspace          PASS
    ↓
Tender Operator persistent contour       PASS
    ↓
Discount Parser cross-host contour       PASS
    ↓
Incident / recovery drills               PASS
    ↓
Clean-host portability proof             PASS
    ↓
M7 operational/code-health gates         PASS
```

The internal operating contour is fit for ongoing governed use within its declared scope. It must not be described as broader external/customer Production or general platform availability.

## 7. Phase 8 pre-activation — current work

Detailed plan: [`P8.00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md`](P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md).

### P8.00 — Phase 8 activation / external-ecosystem boundary revalidation

Status: `Current / Pre-activation`.

P8.00 is deliberately outside active P8 execution. It decides whether the external ecosystem work is justified and what exact boundary may be activated.

| Substep | Work | Status | Exit |
|---|---|---|---|
| `P8.00-A1` | External-demand evidence inventory | 🟩 Complete / PASS | concrete candidate register |
| `P8.00-A2` | Candidate triage + value/platform-need test | 🟩 Complete / PASS | shortlist ≤ 3 candidates |
| `P8.00-A3` | Select one bounded external outcome | 🟨 Current / next | named activation outcome or explicit `DEFER` |
| `P8.00-A4` | Organization / identity / authority / data-rights map | ⬜ Pending | explicit deny-by-default boundary |
| `P8.00-A5` | Platform-responsibility necessity test | ⬜ Pending | `PLATFORM_REQUIRED`, `PRODUCT_LOCAL` or `DEFER` |
| `P8.00-A6` | Stable/readiness/ADR gate scan | ⬜ Pending | explicit required governance or `NO-GATE` |
| `P8.00-A7` | Activation success/failure/rollback/containment envelope | ⬜ Pending | executable validation scope |
| `P8.00-A8` | Fresh owner activation decision | ⬜ Pending | Phase 8 `Active` or explicit `DEFER` |

A1 evidence: [`P8-00-A1-external-demand-evidence-inventory.md`](../reviews/P8-00-A1-external-demand-evidence-inventory.md).

A2 evidence: [`P8-00-A2-candidate-triage-and-value-test.md`](../reviews/P8-00-A2-candidate-triage-and-value-test.md).

Current A2 shortlist:

1. ЕИС / `zakupki.gov.ru` authoritative tender-document boundary.

Contained/deferred on current evidence:

- Telegram controlled external publication effect boundary — product-local containment;
- Discount Parser public discount/promo source set — deferred pending source-specific rights clarity and new external value evidence.

Candidate classes include:

1. external authoritative system such as ERP/CRM/1С/government system;
2. separately maintained external product/extension;
3. real partner/customer Organization;
4. governed external portability/migration/handover recipient.

Existing product-local connectors are evidence candidates, not automatic reasons to move business integration logic into Arvectum OS.

## 8. Draft Phase 8 — Ecosystem and External Integration

Detailed roadmap: [`PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`](PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md) — `Draft / Exploratory 0.2.0`.

P8.01–P8.12 remain planning hypotheses until P8.00 PASS and fresh owner activation approval.

| ID | Work item | Status |
|---|---|---:|
| `P8.01` | External ecosystem target execution baseline + evidence package | ⬜ Draft |
| `P8.02` | Cross-Organization identity, trust, rights + data-governance boundary | ⬜ Draft |
| `P8.03` | External Product Contract / integration-contract + stable-surface disposition | ⬜ Draft |
| `R25` | External Boundary Review | ⬜ Draft gate |
| `P8.04` | External authoritative-system connector pattern validation | ⬜ Draft |
| `P8.05` | External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics | ⬜ Draft |
| `P8.06` | External product/extension onboarding + governed dependency resolution | ⬜ Draft |
| `R26` | Cross-Organization Security / Integration Health Review | ⬜ Draft gate |
| `P8.07` | Portability/export/migration/customer-handover interoperability proof | ⬜ Draft |
| `P8.08` | Multi-Organization isolation + cross-organization security validation | ⬜ Draft |
| `P8.09` | External operator/developer integration experience + documentation | ⬜ Draft |
| `R27` | Portability / Ecosystem Reuse Review | ⬜ Draft gate |
| `P8.10` | Scoped external conformance/commercial/support boundary review | ⬜ Draft |
| `P8.11` | Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition | ⬜ Draft |
| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate | ⬜ Draft gate |
| `P8.12` | Phase 8 / M8 closure review | ⬜ Draft |

### Draft critical path after activation

```text
P8.00 PASS + owner activation
        ↓
P8.01 exact external target/evidence baseline
        ↓
P8.02 Organization/authority/data-rights boundary
        ↓
P8.03 explicit integration contract
        ↓
R25 External Boundary Review
        ↓
P8.04 real external connector validation
        ↓
P8.05 duplicate/replay/uncertainty/reconciliation
        ↓
P8.06 external consumer onboarding
        ↓
R26 Security / Integration Health Review
        ↓
P8.07 portability / handover proof
        ↓
P8.08 cross-Organization isolation validation
        ↓
P8.09 external integration UX/docs
        ↓
R27 Ecosystem Reuse Review
        ↓
P8.10 external claims boundary
        ↓
P8.11 architecture / ADR / lifecycle hardening
        ↓
R28 M8 hardening + code-health gate
        ↓
P8.12 M8 closure
```

## 9. M8 milestone definition

`M8 — Governed external ecosystem baseline` may be achieved only for the exact activated scope when:

1. Phase 8 was activated through P8.00 with fresh owner approval;
2. at least one concrete external ecosystem relationship produced real evidence;
3. Organization/identity/authentication/authorization/Organizational Authority/data-governance boundaries are explicit and fail closed;
4. external authoritative-system semantics preserve the actual source of truth;
5. explicit Product Contract/integration-contract boundaries replace hidden coupling;
6. duplicate/replay/uncertain-outcome/reconciliation semantics are proven;
7. external consumer/dependency reliance is explicit and version-governed where in scope;
8. governed portability/export/handover is proven where in scope;
9. realistic cross-Organization isolation is proven if the activated scope includes more than one Organization;
10. external integration experience is repeatable within declared lifecycle scope;
11. conformance/commercial/support claims are exactly bounded to evidence;
12. reuse versus containment recommendations are evidence-backed;
13. R25–R28 material findings are dispositioned;
14. the M8 Milestone Code Health Gate passes before closure.

If the activated scope does not include a second Organization, public API, customer deployment or other relationship class, M8 closure must state that limitation and must not imply validation of that class.

## 10. Non-goals and invariant guardrails

Neither P8.00 nor Phase 8 automatically establishes:

- public SaaS or general availability;
- universal multi-tenancy;
- public marketplace/plugin store;
- a universal API/SDK;
- Stable Product Contracts;
- Active Platform Capabilities;
- external/customer Production;
- universal ERP/CRM/1С/government connectors;
- SLA/SLO/RPO/RTO/support commitments;
- certification or full-platform conformance;
- cross-customer Knowledge/data sharing;
- AI authority over external access, contractual rights, Organizational Authority, policy or consequential approvals.

Authentication remains distinct from Authorization; Authorization remains distinct from Organizational Authority; technical access does not create legal/contractual rights.

External systems may remain authoritative. Arvectum OS must not create competing sources of truth merely to simplify integration.

## 11. ADR, lifecycle and stable-boundary rule

Use the lowest sufficient decision level.

Before material reliance, reopen the applicable governance gate if Phase 8 pressure selects a long-lived or externally constraining:

- public/stable API or wire format;
- external authentication/trust protocol;
- multi-Organization persistence/isolation topology;
- external Event transport/broker;
- connector/plugin packaging/discovery protocol;
- durable customer-facing export/migration format;
- external Production deployment or compatibility/support commitment.

Successful integration is evidence, not automatic lifecycle promotion.

## 12. Current canonical action

> **P8.00-A3 — Select one bounded external outcome.**

A1 and A2 are `Complete / PASS`. The immediate next action is to work from the one-item A2 shortlist and either define a materially new bounded EIS-related external outcome beyond the existing M6 retrieval proof or record `DEFER`. No P8.01 implementation may begin until one selected outcome passes the remaining P8.00 gates and fresh owner activation approval is recorded.