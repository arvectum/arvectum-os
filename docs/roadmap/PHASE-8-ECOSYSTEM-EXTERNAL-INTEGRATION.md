# Arvectum OS Phase 8 — Ecosystem and External Integration

Status: `Active`
Version: `1.2.0`
Created: `2026-08-17`
Updated: `2026-08-20`
Activated: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M8 — Governed external ecosystem baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 7 / M7 — Complete / PASS`
Restoration decision: [`DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION`](../governance/decisions/DECISION-2026-08-17-PHASE-7-8-ROADMAP-RESTORATION.md)
Pre-activation plan: [`P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md`](P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md) — `Complete / PASS 1.3.0`
Activation decision: [`DECISION-2026-08-20-PHASE-8-ACTIVATION`](../governance/decisions/DECISION-2026-08-20-PHASE-8-ACTIVATION.md) — `Approved`

Version `1.2.0` completes P8.05 external ingress/egress Event, duplicate, replay, uncertainty and reconciliation semantics with `1235 tests / OK`, and advances the current canonical action to P8.06. No lifecycle, readiness, conformance or commercial status changes.

## 1. Purpose

Phase 8 is the governed continuation after Arvectum OS proved the persistent internal M7 operating baseline.

Its purpose is to validate interaction beyond the prior point-in-time owner-operated product evidence through a concrete external authoritative-system boundary while preserving Organization sovereignty, explicit contracts, external authority, provenance, failure-closed behavior and proportionality.

Phase 8 is now `Active` only for the bounded outcome approved by P8.00/A8:

> **EIS authoritative-source revalidation across time for notice `0344100006426000005`, comparing a fresh exact external observation with the immutable P6 baseline and proving freshness/version-drift semantics without rewriting historical evidence.**

The activation does not assume public SaaS, universal multi-tenancy, a public marketplace, one mandatory API/SDK, customer Production, or migration of product business logic into the platform.

## 2. Starting state inherited from M7

M7 established, within `Persistent Internal / owner-operated` scope:

- supervised persistent Arvectum OS runtime on the selected Mac mini;
- durable governed state with tested backup/restore and selected-host-loss recovery;
- persistent least-privilege identity/operator/service access;
- health, observability, audit visibility and incident/recovery procedures;
- governed deploy/update/rollback/version/migration;
- live private operator workspace with real owner inspection and fail-closed governed preflight;
- persistent Tender Operator operational reliance;
- repeatable Discount Parser Windows ↔ Mac mini reconstruction contour;
- R21 through R24 and the M7 Milestone Code Health Gate `Complete / PASS`;
- final reference baseline of `1192 tests / OK` at M7 hardening.

Lifecycle/readiness boundaries remain unchanged:

- CAP-001 through CAP-004: `Incubating / Provisional`;
- P6.02 and P6.06 Product Contracts: `Provisional 0.1.0`;
- P8.03 EIS revalidation integration contract: `Provisional 0.1.0`;
- conformance remains scoped to evidence actually proven;
- no external/customer Production, Stable Product Contract, Active Platform Capability, public/stable API/wire/deployment boundary, SLA/support or certification claim exists.

## 3. Activation result

P8.00 is `Complete / PASS`.

The activation gate established:

1. one evidence-backed selected external system: ЕИС / `zakupki.gov.ru`;
2. one exact outcome: later source revalidation of real notice `0344100006426000005` against the immutable P6 baseline;
3. one governing Organization: `ООО «Арвектум»`;
4. deny-by-default identity/authority/data-rights scope;
5. `PLATFORM_REQUIRED` only for the domain-neutral external-authority/freshness/provenance/reconstruction envelope;
6. EIS connector/SOAP/archive/procurement semantics remain product-owned;
7. A6 `NO-GATE` for the bounded internal read-only validation;
8. fresh owner activation approval.

No second Organization, customer, portability recipient or external product consumer is implied by activation.

## 4. Roadmap work breakdown

| ID | Work item | Dependency | Status | Intended output |
|---|---|---|---:|---|
| `P8.00` | Phase 8 activation / external-ecosystem boundary revalidation | M7 | 🟩 Complete / PASS | bounded outcome + approved activation |
| `P8.01` | External ecosystem target execution baseline + evidence package | P8.00 PASS | 🟩 Complete / PASS | exact EIS temporal revalidation baseline |
| `P8.02` | Cross-Organization identity, trust, rights + data-governance boundary | P8.01 | 🟩 Complete / PASS | one-Organization deny-by-default boundary |
| `P8.03` | External Product Contract / integration-contract boundary + stable-surface disposition | P8.02 | 🟩 Complete / PASS | Provisional EIS revalidation contract `0.1.0` |
| `R25` | External Boundary Review | P8.03 | 🟩 Complete / PASS | no material boundary blocker |
| `P8.04` | External authoritative-system connector pattern validation | R25 | 🟩 Complete / PASS | real external authority integration evidence |
| `P8.05` | External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics | P8.04 | 🟩 Complete / PASS | fail-closed external effect/evidence semantics |
| `P8.06` | External product/extension onboarding + governed dependency resolution | P8.05 | 🟨 Current | repeatable explicit onboarding/dependency proof |
| `R26` | Cross-Organization Security / Integration Health Review | P8.06 | ⬜ Pending gate | security/isolation/integration-health review |
| `P8.07` | Portability/export/migration/customer-handover interoperability proof | R26 | ⬜ Pending | governed external handover/export evidence |
| `P8.08` | Multi-Organization isolation + cross-organization security validation | P8.07 | ⬜ Pending | realistic isolation/failure-closed evidence when a second Organization is actually in scope |
| `P8.09` | External operator/developer integration experience + documentation | P8.08 | ⬜ Pending | bounded repeatable integration experience |
| `R27` | Portability / Ecosystem Reuse Review | P8.09 | ⬜ Pending gate | reuse/portability/no-speculative-generalization review |
| `P8.10` | Scoped external conformance/commercial/support boundary review | R27 | ⬜ Pending | exact justified external claims and non-claims |
| `P8.11` | Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition | P8.10 | ⬜ Pending | material debt, ADR and lifecycle dispositions |
| `R28` | M8 Ecosystem Hardening + Milestone Code Health Gate | P8.11 | ⬜ Pending gate | pre-closure engineering/code-health PASS |
| `P8.12` | Phase 8 / M8 closure review | R28 | ⬜ Pending | exact M8 closure scope or explicit non-closure |

## 5. Completed active-phase preparation

### P8.01 — External ecosystem target execution baseline + evidence package

Evidence: [`P8-01-eis-revalidation-target-evidence-baseline.md`](../reviews/P8-01-eis-revalidation-target-evidence-baseline.md) — `Complete / PASS`.

Exact case:

- Organization: `ООО «Арвектум»`;
- Product: Tender Operator;
- external authority: ЕИС / `zakupki.gov.ru`;
- notice: `0344100006426000005`;
- immutable P6 baseline manifest SHA-256: `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- live P8 outcome must establish a new observation and deterministic `NO_CHANGE` or `CHANGE_DETECTED` comparison, or an explicit non-success state.

P8.01 does not perform the live EIS request.

### P8.02 — Identity, trust, rights + data-governance boundary

Evidence: [`P8-02-identity-trust-rights-data-governance-boundary.md`](../reviews/P8-02-identity-trust-rights-data-governance-boundary.md) — `Complete / PASS`.

The activated case validates one Organization only.

The boundary keeps separate:

1. Identity;
2. Authentication;
3. Authorization;
4. Organizational Authority;
5. Data Governance.

Verified TLS is mandatory; secrets remain local; technical token access creates no broader rights; cross-Organization access, redistribution, mutation and customer-facing use remain deny-by-default.

### P8.03 — EIS external-authority revalidation integration contract

Contract: [`P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md`](../contracts/P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md) — `Provisional 0.1.0`.

Stable-surface disposition:

`PROVISIONAL_INTERNAL_ONLY / NO_STABLE_SURFACE`.

Platform dependencies are limited to existing Kernel/Execution/Event semantics plus the bounded Provisional CAP-001/CAP-004 reliance required for exact document/provenance/reconstruction semantics.

The EIS adapter and procurement-specific behavior remain product-owned.

### R25 — External Boundary Review

Evidence: [`R25-external-boundary-review.md`](../reviews/R25-external-boundary-review.md) — `Complete / PASS`.

No material blocker remains in:

- product/platform boundary;
- external authority/source of truth;
- identity/authorization/Organizational Authority;
- rights/minimization/secrets;
- stable/public surface;
- lifecycle/readiness claims;
- failure/rollback/termination.

P8.04 may proceed only within the bounded contract and requires real owner-operated local execution.

## 6. Current and future execution intent

### P8.04 — External authoritative-system connector pattern validation

**Status: Complete / PASS.**

Evidence: [`P8-04-eis-authoritative-system-live-validation.md`](../reviews/P8-04-eis-authoritative-system-live-validation.md) — `Complete / PASS`.

The bounded live read-only EIS revalidation for notice `0344100006426000005` completed:

- exactly one top-level live run (`toa-run-20260820083457-21337c`);
- fresh observation `2026-08-20T08:34:57.365770+00:00`;
- immutable P6 baseline SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121` verified fail-closed;
- aggregate result `NO_CHANGE` (all 7 material documents byte-identical);
- independent byte + manifest re-verification passed;
- network-free offline re-comparison byte-identical;
- governed evidence admission + reconstruction complete without external-effect replay.

The live run preserved the external boundary:

- one Organization (`ООО «Арвектум»`), External Reference authority;
- read-only retrieval only; no mutation, submission, signature, messaging, redistribution or cross-Organization action;
- no secrets in canonical history or logs;
- verified TLS required and enforced;
- a failed current retrieval would never be represented as `NO_CHANGE`; missing/incomplete baseline blocks PASS;
- P6 historical evidence preserved immutable.

### P8.05 — External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics

**Status: Complete / PASS.**

Evidence: [`P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md`](../reviews/P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md) — `Complete / PASS`.

P8.05 validated RFC-0005/RFC-0006 behavior at the external boundary while preserving the P8.03 read-only EIS rights boundary:

- transport delivery remains distinct from explicit canonical Event admission;
- the Native ingress Event records Arvectum OS observation/admission while EIS source facts remain External Reference;
- duplicate delivery does not duplicate canonical truth;
- equal payload bytes do not collapse genuinely distinct source occurrences;
- source occurrence time and recording time remain distinct under late/out-of-order delivery;
- idempotency scope and duplicate-protection tokens remain explicit through P2.06;
- unknown external outcomes become `Uncertain` and block blind retry;
- reconciliation is append-only, attributable and versioned;
- `ConfirmedSucceeded` blocks duplicate retry; `StillUncertain` remains blocked; `ConfirmedNotApplied` allows only a new Governed Execution with a new retry token;
- historical reconstruction is pure and never repeats live retrieval or external effect automatically;
- identity/evidence conflicts and incomplete outcomes fail closed.

Executable evidence: repository `Reference Python CI` — `1235 tests / OK`.

P8.05 does not select a transport/broker/inbox/outbox/reconciliation topology, create a public/stable Event API, promote a Platform Capability, stabilize a Product Contract, or perform an unauthorized real EIS mutation.

### P8.06 — External product/extension onboarding + governed dependency resolution

**Status: Current.**

Prove a separately maintained external consumer can enter through explicit governed boundaries without private coupling when a real qualifying consumer is available.

Required evidence:

- product/extension identity and owner;
- Product Contract/integration-contract resolution;
- exact capability/provider compatibility evidence;
- least-privilege access and Organization scope;
- rejection of undeclared dependency/version/operation;
- no direct internal-table/private-module/private-stream reliance;
- no hidden shared mutable state;
- clear install/onboard/disable/remove/upgrade path;
- product-specific schemas/workflows remain product-owned.

If no new external product/extension consumer exists beyond the M6/M7 owner-operated products, P8.06 must not invent one; the roadmap may require explicit defer/re-scope before proceeding.

### R26 — Cross-Organization Security / Integration Health Review

Review P8.01–P8.06 with emphasis on:

- Organization isolation;
- least privilege/default denial;
- secrets and privileged support paths;
- external authority preservation;
- provenance/replay/uncertainty semantics;
- integration dependency direction and hidden coupling;
- incident/recovery impact;
- contract/version drift;
- concrete ADR/stable-boundary triggers.

### P8.07 — Portability/export/migration/customer-handover interoperability proof

Exercise organization control beyond the owner-operated deployment only when a concrete permitted external recipient/scope exists.

Required evidence where activated:

- governed export/handover package preserves identities, versions, authority, provenance, relationships and explicit omissions;
- classification/rights/retention constraints survive handover;
- non-exportable secrets are omitted and reprovisioned separately;
- receiver can validate integrity and interpret scope/version metadata;
- selected historical outcome remains reconstructable to the permitted extent;
- handover does not grant Organizational Authority or technical access implicitly;
- termination/revocation path is explicit;
- migration failure cannot silently create two competing authoritative systems.

No universal customer export format is implied.

### P8.08 — Multi-Organization isolation + cross-organization security validation

This step requires realistic evidence only if a second Organization is actually activated into scope.

When applicable, test at minimum:

- Organization A identity cannot enumerate/read Organization B protected state;
- same external email/directory identifier does not merge authority scopes;
- relationship/contract presence does not grant content access;
- admin/support access is not ambient content access;
- logs/metrics/errors do not leak foreign identifiers/content;
- cache/index/search/projection boundaries do not cross Organization scope;
- export/import/handover cannot widen rights;
- revoked/deleted/grant-expired state fails closed;
- external callback/ingress cannot spoof Organization scope;
- cross-Organization operations require explicit governed grants/contracts.

No second Organization may be fabricated merely to satisfy the roadmap.

### P8.09 — External operator/developer integration experience + documentation

Make the actually validated external integration repeatable without exposing private platform internals.

Required outputs:

- bounded onboarding/integration runbook;
- explicit prerequisites and version pins;
- contract/dependency validation instructions;
- safe credential/configuration handling;
- predictable error/fail-closed states;
- evidence/reconstruction inspection path;
- upgrade/deprecation/termination guidance appropriate to lifecycle;
- examples that do not imply unsupported general compatibility;
- clear separation of platform and product responsibilities.

### R27 — Portability / Ecosystem Reuse Review

Determine what is genuinely reusable and what must remain contained.

Review questions:

- did the external case reuse existing platform semantics or force product-specific special cases;
- what duplicated integration responsibility was actually removed;
- what remains one-off and should not be generalized;
- whether a second external consumer is needed before any stable/shared abstraction;
- whether portability/handover preserves organizational meaning across implementation changes;
- whether any extension/onboarding helper has enough evidence for shared platform ownership.

`contain`, `defer` and `return to product` are valid results.

### P8.10 — Scoped external conformance/commercial/support boundary review

State exactly what external claim is supported by evidence.

Separately disposition:

- operational environment/readiness;
- RFC conformance scope/maturity;
- Product Contract lifecycle;
- Platform Capability lifecycle;
- supported integrations/versions;
- compatibility/migration expectations;
- support responsibility;
- security/isolation scope;
- portability/handover scope;
- commercial promises.

Do not infer Production, SLA/SLO, certification, Stable or Active status from successful integration alone.

### P8.11 — Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition

Review all Phase 8 implementation/evidence before milestone closure.

Must inspect:

- accidental public/stable interfaces;
- product/domain leakage;
- duplicated external-boundary logic;
- authorization/authority/data-governance bypasses;
- Organization isolation defects;
- secret/logging/minimization issues;
- replay/duplicate/uncertain-outcome correctness;
- portability and termination gaps;
- oversized task-specific harnesses that should remain contained;
- concrete ADR triggers;
- whether any capability/Product Contract lifecycle transition is separately justified.

No lifecycle transition occurs merely by recording a recommendation.

### R28 — M8 Ecosystem Hardening + Milestone Code Health Gate

Required before P8.12.

Perform the Approved Engineering Quality and Refactoring Gate for M8 over material Phase 8 surfaces:

- architecture/dependency direction;
- correctness/invariants;
- security/privacy/isolation;
- maintainability and generated/dead code;
- test quality and regression coverage;
- accidental stable/public surface detection;
- performance only where measured or materially relevant;
- documentation/status consistency.

Material findings must be resolved or explicitly accepted by appropriate authority before closure.

### P8.12 — Phase 8 / M8 closure review

Close M8 only when the activated scope is actually proven.

The closure must state:

- exact external outcome(s) validated;
- external Organization/system authority model;
- contracts and lifecycle status;
- isolation/security evidence;
- replay/uncertainty/reconciliation evidence;
- portability/handover evidence where actually in scope;
- reusable versus contained mechanisms;
- external conformance/support/commercial scope;
- all R25–R28 findings;
- exact remaining non-goals and unproven claims.

## 7. Sequencing and local-execution boundary

Current critical path:

```text
P8.00 activation boundary revalidation        PASS
   ↓
OWNER ACTIVATION DECISION                     APPROVED
   ↓
P8.01 target execution baseline               PASS
   ↓
P8.02 authority / rights / data boundary      PASS
   ↓
P8.03 explicit integration contract           PASS
   ↓
R25 External Boundary Review                  PASS
   ↓
P8.04 real external connector validation      PASS
   ↓
P8.05 duplicate / replay / uncertainty        PASS
   ↓
P8.06 external product / extension onboarding CURRENT
   ↓
R26 Integration Health / Cross-Org Security
   ↓
P8.07 portability / handover proof
   ↓
P8.08 multi-Organization isolation validation
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

P8.04 is the first action in this sequence that required the real owner-operated local Tender Operator/EIS runtime, existing credentials/trust path and owner-only raw execution artifacts. P8.05 completed repository-side semantic/evidence validation without expanding the P8.03 read-only rights boundary.

## 8. M8 exit criteria

`M8 — Governed external ecosystem baseline` is achieved only for the declared activated scope when:

1. P8.00 activation requirements were satisfied with fresh owner approval;
2. at least one concrete external ecosystem relationship produced real evidence;
3. Organization/identity/authentication/authorization/Organizational Authority/data-governance boundaries are explicit and fail closed;
4. external authoritative-system semantics preserve the real source of truth;
5. explicit Product Contract/integration-contract boundaries replace hidden coupling;
6. duplicate/replay/uncertain-outcome/reconciliation semantics are proven;
7. external consumer/onboarding reliance is explicit and version-governed where in scope;
8. governed portability/export/handover is demonstrated where in scope;
9. realistic cross-Organization isolation/security evidence passes when cross-Organization scope is actually activated;
10. external operator/developer integration is repeatable within declared lifecycle scope;
11. conformance/commercial/support claims remain exactly bounded to evidence;
12. reuse versus containment recommendations are evidence-backed;
13. R25–R28 material findings are dispositioned;
14. the M8 Milestone Code Health Gate passes before closure.

If the activated case does not exercise a particular external relationship class, closure must state that limitation explicitly and must not claim validation of that class.

## 9. Non-goals

Phase 8 does not inherently establish:

- general availability;
- public SaaS;
- universal multi-tenancy;
- public marketplace/plugin store;
- universal public API/SDK;
- Stable Product Contracts;
- Active Platform Capabilities;
- Production for external customers;
- universal ERP/CRM/1С/government connectors;
- SLA/SLO/RPO/RTO/support commitments;
- certification or full-platform conformance;
- cross-customer data/Knowledge sharing;
- AI authority to approve external access, contracts, policies or consequential effects.

## 10. Current canonical action

> **P8.06 — External product/extension onboarding + governed dependency resolution.**

P8.00, P8.01, P8.02, P8.03, R25, P8.04 and P8.05 are `Complete / PASS`. P8.05 proved the bounded RFC-0005/RFC-0006 external Event/duplicate/replay/uncertainty/reconciliation semantics with `1235 tests / OK`, without a real EIS mutation, public/stable surface or lifecycle promotion. P8.06 is now current and must use a real qualifying external consumer if one exists; it must not fabricate one merely to satisfy sequencing.
