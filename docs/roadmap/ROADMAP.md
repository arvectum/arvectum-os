# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.62.0`
Created: `2026-08-07`
Updated: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for Arvectum OS development sequencing. It coordinates work but does not override the Constitution, Accepted RFC/ADR, approved governance, Product Contracts, code/tests or canonical implementation evidence.

Roadmap status does not itself change Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness, conformance maturity, SLA/support or commercial commitments.

Detailed completed-phase history remains in the corresponding phase roadmaps, reviews and repository history rather than being duplicated indefinitely in this master roadmap.

## 2. Version note

Version `2.62.0` completes P8.05 external ingress/egress Event, duplicate, replay, uncertainty and reconciliation semantics with repository `Reference Python CI` at `1235 tests / OK`, synchronizes the detailed Phase 8 roadmap to `1.2.0`, and advances the current canonical action to P8.06. It changes no Platform Capability or Product Contract lifecycle, external/customer readiness, conformance or commercial status.

Version `2.61.1` was a post-merge roadmap synchronization correction aligning the detailed Phase 8 roadmap with the already canonical `P8.04 = Complete / PASS` / `P8.05 = Current` state.

Version `2.61.0` completed the bounded real P8.04 external authoritative-system connector validation (`NO_CHANGE` on the live EIS revalidation with immutable-baseline verification) and advanced the current canonical action to P8.05.

Version `2.60.0` completed the remaining P8.00 activation gates, recorded fresh owner activation of Phase 8, completed P8.01–P8.03 and R25, and advanced the current canonical action to the first real local external-validation step:

> `P8.04 — External authoritative-system connector pattern validation`.

P8.00 selected one bounded Phase 8 outcome:

- real notice `0344100006426000005` in ЕИС / `zakupki.gov.ru`;
- make a later independent read-only source observation;
- compare the fresh exact source/document snapshot with the immutable P6 baseline manifest SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- validate explicit external authority, observation freshness/version drift, provenance and historical non-mutation;
- accept `NO_CHANGE` or `CHANGE_DETECTED` as valid live outcomes when evidenced correctly.

P8.04 executed that bounded case in the owner-operated runtime and returned a verified live `NO_CHANGE`:

- single live read-only run `toa-run-20260820083457-21337c`; fresh observation `2026-08-20T08:34:57.365770+00:00`;
- immutable P6 baseline SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121` verified fail-closed;
- fresh manifest SHA-256 `4113935e43291f820a43fa2efad49663103a86408788b571d7d0e6dac4974a54`; comparison manifest SHA-256 `06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b`;
- aggregate `NO_CHANGE`; all 7 material documents byte-identical;
- independent byte/manifest re-verification and network-free deterministic re-comparison passed;
- governed evidence admission + reconstruction complete without external-effect replay;
- review evidence: [`P8-04-eis-authoritative-system-live-validation.md`](../reviews/P8-04-eis-authoritative-system-live-validation.md).

P8.05 then proved the domain-neutral external-boundary semantics without expanding P8.03 rights:

- transport delivery is distinct from explicit canonical Event admission;
- EIS source authority remains `External Reference`; the Native Event records only Arvectum OS observation/admission;
- duplicate occurrence delivery does not create duplicate canonical truth;
- equal payload bytes do not collapse distinct source occurrences;
- occurrence and recording times remain distinct under late/out-of-order delivery;
- unknown external outcome is explicit `Uncertain` and blocks blind retry;
- reconciliation is append-only, attributable and versioned;
- `ConfirmedSucceeded` permanently blocks duplicate-risk retry for the bounded attempt; `ConfirmedNotApplied` allows only a new Governed Execution with a new retry token;
- historical reconstruction is pure and never repeats live retrieval/external effect automatically;
- executable evidence: `1235 tests / OK`;
- review evidence: [`P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md`](../reviews/P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md).

Activation boundary:

- governing Organization: `ООО «Арвектум»` only;
- authority mode: `External Reference` for EIS source facts/documents;
- EIS connector remains Tender Operator product-owned;
- `PLATFORM_REQUIRED` applies only to the reusable external-authority/freshness/provenance/reconstruction envelope;
- A6 disposition: `NO-GATE` for this bounded internal read-only validation;
- P8.03 contract: `Provisional 0.1.0`, `PROVISIONAL_INTERNAL_ONLY / NO_STABLE_SURFACE`;
- R25: `Complete / PASS`;
- no second Organization, customer Production, Stable Product Contract, Active Platform Capability, public/stable connector/API, SLA/support or redistribution-right claim is created.

Canonical facts preserved from `2.59.0`:

- `Phase 7 = Complete / PASS`;
- `M7 = achieved` for the declared `Persistent Internal / owner-operated` scope;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`;
- M7 conformance remains scoped to its declared owner-operated contour;
- lifecycle, operational environment/readiness, conformance maturity and commercial claims remain distinct.

## 3. Architecture and governance baseline

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a permanent persistence, IAM, service, public API, external Event transport, connector/plugin, broker or deployment topology;
- Decision Authority Policy remains `Proposed 0.2.1`; residual authority remains with the owner under Accepted governance;
- Approved Engineering Quality and Refactoring Gates remain binding;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 real Product Contracts remain `Provisional 0.1.0`;
- P8.03 EIS revalidation integration contract is `Provisional 0.1.0`;
- no Platform Capability is `Active` merely because M3–M7 completed or Phase 8 activated;
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
| `Phase 8` | Ecosystem and External Integration | 🟨 Active | `M8` Governed external ecosystem baseline — not yet achieved |

## 5. Completed platform progression

### Phase 0 / M0 — Architecture Bootstrap

Established the constitutional and RFC architecture baseline and governance hierarchy.

### Phase 1 / M1 — Reference Implementation

Proved the first executable architectural spine without turning reference technology into platform contract.

### Phase 2 / M2 — Core Runtime

Established reusable governed runtime semantics including exact versions, relationships, execution, provenance and consistency behavior.

### Phase 3 / M3 — Shared Platform Capabilities

Validated the bounded shared-capability baseline. CAP-001 through CAP-004 remain `Incubating / Provisional`; M3 did not promote them to `Active`.

### Phase 4 / M4 — Workspace / Operator Experience

Established the domain-neutral operator workspace model for Organization/Actor context, Records, Executions, Evidence, Documents, Knowledge and authority-safe governed actions without selecting a stable frontend/API technology.

### Phase 5 / M5 — SDK, Contracts and Extension Experience

Established repeatable explicit integration through Product Contracts and internal/provisional integration tooling without creating a public Stable SDK/API.

### Phase 6 / M6 — Product-driven Platform Validation

Validated the platform through two materially distinct real product/workflow contexts:

- Tender Operator exact real tender evidence with governed admission/reconstruction;
- Discount Parser controlled real Telegram publication evidence reconstructed through CAP-004 without effect replay.

M6 proved real-product value and reuse while keeping product business semantics product-owned.

### Phase 7 / M7 — Operational / Enterprise Readiness

Detailed roadmap: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md) — `Complete / PASS 1.2.18`.

M7 established the declared `Persistent Internal / owner-operated` baseline:

- persistent supervised runtime on the selected Mac mini;
- durable governed state/checkpoint persistence;
- tested backup/restore and selected-host-loss recovery;
- persistent least-privilege identity/operator/service access;
- health, observability, audit visibility and alerting;
- governed deploy/update/rollback/version/migration;
- private live operator workspace;
- persistent Tender Operator reliance;
- repeatable Discount Parser Windows ↔ Mac mini reconstruction contour;
- incident/recovery drills;
- scoped readiness/lifecycle/conformance/stable-boundary disposition;
- R21–R24 and M7 Milestone Code Health Gate `Complete / PASS`.

Final M7 code-health evidence included `1192 tests / OK`.

M7 did not create external/customer Production, Active Platform Capabilities, Stable Product Contracts, public/stable interfaces, SLA/SLO/RPO/RTO/support commitments or certification.

## 6. Current operating state

For the declared internal scope:

```text
Selected Mac mini
    ↓
Persistent Arvectum OS runtime             PASS
    ↓
Durable governed state + backup/restore   PASS
    ↓
Least-privilege identity/access           PASS
    ↓
Health / observability / audit visibility PASS
    ↓
Governed update / rollback                PASS
    ↓
Private live operator workspace           PASS
    ↓
Tender Operator persistent contour        PASS
    ↓
Discount Parser cross-host contour        PASS
    ↓
Incident / recovery drills                PASS
    ↓
Clean-host portability proof              PASS
    ↓
M7 operational/code-health gates          PASS
```

The owner-operated contour remains the operational baseline. Phase 8 activation adds a bounded external-validation program; it does not broaden the operating environment into external/customer Production.

## 7. Phase 8 activation closure

Detailed pre-activation plan: [`P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md`](P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md) — `Complete / PASS 1.3.0`.

Owner decision: [`DECISION-2026-08-20-PHASE-8-ACTIVATION`](../governance/decisions/DECISION-2026-08-20-PHASE-8-ACTIVATION.md) — `Approved`.

| Substep | Work | Status | Result |
|---|---|---|---|
| `P8.00-A1` | External-demand evidence inventory | 🟩 Complete / PASS | concrete candidate register |
| `P8.00-A2` | Candidate triage + value test | 🟩 Complete / PASS | EIS one-item shortlist |
| `P8.00-A3` | Select one bounded external outcome | 🟩 Complete / PASS | temporal EIS revalidation |
| `P8.00-A4` | Organization / identity / authority / data-rights map | 🟩 Complete / PASS | one-Organization deny-by-default boundary |
| `P8.00-A5` | Platform-responsibility necessity test | 🟩 Complete / PASS | narrow `PLATFORM_REQUIRED` |
| `P8.00-A6` | Stable/readiness/ADR gate scan | 🟩 Complete / PASS | `NO-GATE` for bounded internal read-only scope |
| `P8.00-A7` | Success/failure/rollback/containment envelope | 🟩 Complete / PASS | executable activation envelope |
| `P8.00-A8` | Fresh owner activation decision | 🟩 Approved | Phase 8 `Active` |

Telegram remains product-local on current evidence. The Discount Parser public-source set remains deferred pending source-specific rights clarity and new external value evidence.

## 8. Active Phase 8 — Ecosystem and External Integration

Detailed roadmap: [`PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`](PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md) — `Active 1.2.0`.

| ID | Work item | Status |
|---|---|---:|
| `P8.01` | External ecosystem target execution baseline + evidence package | 🟩 Complete / PASS |
| `P8.02` | Cross-Organization identity, trust, rights + data-governance boundary | 🟩 Complete / PASS |
| `P8.03` | External Product Contract / integration-contract + stable-surface disposition | 🟩 Complete / PASS |
| `R25` | External Boundary Review | 🟩 Complete / PASS |
| `P8.04` | External authoritative-system connector pattern validation | 🟩 Complete / PASS |
| `P8.05` | External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics | 🟩 Complete / PASS |
| `P8.06` | External product/extension onboarding + governed dependency resolution | 🟨 Current |
| `R26` | Cross-Organization Security / Integration Health Review | ⬜ Pending gate |
| `P8.07` | Portability/export/migration/customer-handover interoperability proof | ⬜ Pending |
| `P8.08` | Multi-Organization isolation + cross-organization security validation | ⬜ Pending |
| `P8.09` | External operator/developer integration experience + documentation | ⬜ Pending |
| `R27` | Portability / Ecosystem Reuse Review | ⬜ Pending gate |
| `P8.10` | Scoped external conformance/commercial/support boundary review | ⬜ Pending |
| `P8.11` | Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition | ⬜ Pending |
| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate | ⬜ Pending gate |
| `P8.12` | Phase 8 / M8 closure review | ⬜ Pending |

Completed active-phase preparation/evidence:

- [`P8.01 evidence baseline`](../reviews/P8-01-eis-revalidation-target-evidence-baseline.md);
- [`P8.02 identity/trust/rights boundary`](../reviews/P8-02-identity-trust-rights-data-governance-boundary.md);
- [`P8.03 Provisional integration contract`](../contracts/P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md);
- [`R25 External Boundary Review`](../reviews/R25-external-boundary-review.md);
- [`P8.04 live authoritative-system validation`](../reviews/P8-04-eis-authoritative-system-live-validation.md);
- [`P8.05 external Event/duplicate/replay/uncertainty/reconciliation review`](../reviews/P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md).

### Current critical path

```text
P8.00 PASS + owner activation                DONE
        ↓
P8.01 exact external target/evidence        PASS
        ↓
P8.02 Organization/authority/data-rights    PASS
        ↓
P8.03 explicit integration contract         PASS
        ↓
R25 External Boundary Review                PASS
        ↓
P8.04 real external connector validation    PASS
        ↓
P8.05 duplicate/replay/uncertainty          PASS
        ↓
P8.06 external consumer onboarding          CURRENT
        ↓
R26 Security / Integration Health Review
        ↓
P8.07 portability / handover proof
        ↓
P8.08 cross-Organization isolation validation
        ↓
P8.09 external integration UX/docs
        ↓
R27 Portability / Ecosystem Reuse Review
        ↓
P8.10 external claims boundary
        ↓
P8.11 architecture / ADR / lifecycle hardening
        ↓
R28 M8 hardening + code-health gate
        ↓
P8.12 M8 closure
```

P8.04 was the first current task requiring the real owner-operated Tender Operator/EIS runtime, existing credentials/trust path and owner-only raw artifacts; it completed with a verified live `NO_CHANGE`. P8.05 then completed repository-side semantic/evidence validation without expanding the P8.03 read-only EIS rights boundary.

## 9. M8 milestone definition

`M8 — Governed external ecosystem baseline` may be achieved only for the exact activated scope when:

1. Phase 8 was activated through P8.00 with fresh owner approval;
2. at least one concrete external ecosystem relationship produced real evidence;
3. Organization/identity/authentication/authorization/Organizational Authority/data-governance boundaries are explicit and fail closed;
4. external authoritative-system semantics preserve the actual source of truth;
5. explicit Product Contract/integration-contract boundaries replace hidden coupling;
6. duplicate/replay/uncertain-outcome/reconciliation semantics are proven;
7. external consumer/dependency reliance is explicit and version-governed where actually in scope;
8. governed portability/export/handover is proven where actually in scope;
9. realistic cross-Organization isolation is proven if a second Organization is actually activated;
10. external integration experience is repeatable within declared lifecycle scope;
11. conformance/commercial/support claims are exactly bounded to evidence;
12. reuse versus containment recommendations are evidence-backed;
13. R25–R28 material findings are dispositioned;
14. the M8 Milestone Code Health Gate passes before closure.

If the activated scope does not include a second Organization, public API, customer deployment, external consumer or handover recipient, M8 closure must state those limitations and must not imply validation of those classes.

## 10. Non-goals and invariant guardrails

Neither Phase 8 activation nor current progress automatically establishes:

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

> **P8.06 — External product/extension onboarding + governed dependency resolution.**

P8.05 is `Complete / PASS`: the bounded RFC-0005/RFC-0006 external ingress/egress Event, duplicate, replay, uncertainty and reconciliation semantics passed repository `Reference Python CI` with `1235 tests / OK`; no real EIS mutation, public/stable external Event API, exactly-once guarantee or lifecycle promotion was introduced.

P8.06 is now the current canonical action. It must prove explicit governed onboarding/dependency resolution for a real qualifying separately maintained external consumer if one exists; the roadmap must not fabricate such a consumer merely to satisfy sequencing.
