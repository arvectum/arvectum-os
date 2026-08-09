# P6.02 — First Real Product Contract Boundary + Bounded Adoption Plan Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform` and `governance`
Roadmap work item: `P6.02 — First real Product Contract boundary + bounded adoption plan`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone: `M6 — Platform validated through real products and reuse evidence`
Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`
Result: **`PASS — the first real Product Contract boundary is explicit, minimal, reversible and ready for R17 before implementation reliance.`**

## 1. Purpose and decision level

P6.02 converts the P6.01 evidence-backed dependency hypothesis into the first real RFC-0004 Product Contract for Arvectum OS.

The work item defines the governed product/platform boundary and adoption envelope. It does not implement P6.03, does not migrate real pilot data, does not authorize external execution, does not promote a capability, does not stabilize a public boundary and does not establish production readiness or a commercial support commitment.

The selected workflow remains exactly the P6.01 target:

> **Arvectum procurement/tender AI operator — bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package, with external actions remaining manual.**

## 2. Canonical authority checked

P6.02 was checked against the current canonical repository state in the following authority order:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. `docs/rfc/README.md` — RFC-0001 through RFC-0008 remain `Accepted 1.0.0` with recorded approval evidence;
3. RFC-0001 — product/platform responsibility, minimal Provisional Product Contract before platform reliance, capability lifecycle honesty, external authority, security/isolation, portability, Commercial Commitment Integrity and Platform Gravity;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, exact consequential version reliance, explicit authority modes and non-authoritative projections;
5. RFC-0003 — Organization sovereignty, deny-by-default authorization, least privilege, separation of Authorization/Organizational Authority/Data Governance, cross-Organization restrictions, minimization, retention/deletion, secrets and portability;
6. RFC-0004 — Product Contract lifecycle, required declarations, exact dependency/operation/authority/security/failure/portability semantics, hidden-coupling prohibition, Provisional experiment proportionality and separate promotion decisions;
7. RFC-0005 — exact Product Contract attribution, Governed Execution, operation side-effect classes, separate approval/authority gates, retry/uncertainty semantics and bounded AI authority;
8. RFC-0006 — append-only Event/provenance evidence, required evidence failure behavior, reconstruction truthfulness and telemetry non-authority;
9. RFC-0007 — product domain Memory/Knowledge remains product-owned unless explicitly governed/promoted; no shared Memory/Knowledge reliance is required here;
10. RFC-0008 — Document/Artifact identity/version, External Reference/Governed Replica preservation, derivation provenance, handling propagation and exact artifact reliance;
11. `docs/adrs/README.md` — no applicable Accepted ADR establishes a conflicting stable/public persistence, Event, IAM, storage or service boundary;
12. `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` — exact capability-contract baseline `1.0.0` and current Provisional operation envelopes;
13. `docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md` — CAP-001 through CAP-004 remain `Incubating / Provisional`;
14. `docs/reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md` and current reference implementation — Product Contract remains the single executable declaration semantic owner and current Python/dataclass/token shapes remain internal/provisional;
15. P6.01 evidence baseline and the current `ai-corporation` restricted-pilot evidence;
16. `docs/roadmap/PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md` — P6.02 intent, R17 gate and M6 boundary.

No conflict with Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008 or an Accepted ADR was identified.

## 3. Product evidence continuity

P6.02 preserves the product state verified by P6.01 rather than inventing a new product architecture.

The `ai-corporation` repository currently supports a restricted paid-pilot contour with:

- manual-control boundaries;
- a real partner tender-folder runner;
- RFQ-first pre-bid analysis;
- controlled schema-validated and human-reviewed LLM use;
- report/export controls;
- no broad autonomy;
- no procurement-platform submission;
- no EDS/signature execution;
- no supplier email automation.

P6.02 does not convert existing product-local mechanisms into platform responsibilities. It establishes only the explicit governed interaction required to test whether CAP-001 and CAP-004 add real value.

## 4. Product Contract result

### 4.1 Identity and lifecycle

The Product Contract is created as:

- lifecycle: `Provisional`;
- version: `0.1.0`;
- Product identity: `product/arvectum-tender-operator@<organization>`;
- Product compatibility line: `restricted-paid-pilot/44fz-prebid-v1`;
- Product Contract subject: `product-contract-subject/p6-02-arvectum-tender-operator@<organization>`;
- Product Contract version identity: `product-contract-version/p6-02-arvectum-tender-operator-v0.1.0@<organization>`;
- accountable owner: `ООО «Арвектум»`.

`<organization>` is an explicit runtime sovereignty scope, not an ambient default or cross-customer product tenant.

The contract itself uses Native Arvectum OS authority for the Product Contract record. A new immutable Product Contract version is required for an admitted boundary change.

### 4.2 Exact dependency decision

P6.02 confirms the P6.01 minimum hypothesis:

| Capability | P6.02 decision | Reason |
|---|---|---|
| CAP-001 Document & Artifact Governance | **include** — exact Provisional contract `1.0.0` | needed for exact governed input/output document/artifact references, versions, provenance and handling constraints |
| CAP-004 Audit / Reconstruction Support | **include** — exact Provisional contract `1.0.0` | needed for honest reconstruction from exact governed evidence and explicit incompleteness |
| CAP-002 Memory & Knowledge Governance | **omit** | no shared organizational Memory/Knowledge reliance is demonstrated; prompts/profiles/risk/domain learning remain product-owned |
| CAP-003 Search / Index Projection | **omit** | EIS/44-ФЗ discovery, relevance ranking and search UX remain product-owned; shared discovery is not needed in the minimum slice |

This is a narrower and more truthful boundary than including all Incubating capabilities for coverage.

## 5. Authority and source-of-truth disposition

P6.02 makes the first real authority modes explicit.

| Object | Authority disposition | Review result |
|---|---|---|
| ЕИС / zakupki.gov.ru registry facts and source documents | `External Reference` by default; ЕИС remains authority | `PASS` |
| partner/customer tender files | `External Reference`; accepted partner/customer source package remains authority | `PASS` |
| supplier TKP/quotes | `External Reference`; supplier/partner-origin document remains authority for quoted facts | `PASS` |
| extraction/risk/RFQ/TKP comparison/economics/recommendation | product-owned transient/derived state by default | `PASS` |
| governed execution history | `Native` for Arvectum OS execution/governance state only | `PASS` |
| admitted Event/provenance/review evidence | `Native` for the evidence act, not for underlying tender truth | `PASS` |
| final reviewed report content | `External Reference` by default; platform governs exact reference/version/provenance | `PASS` |
| Product Contract | `Native` | `PASS` |

`Governed Replica` is deliberately not selected as the default because no P6.02 evidence requires synchronized external-source replication. If real use proves it necessary, freshness/conflict/synchronization semantics require a new Product Contract version.

## 6. Product/platform responsibility review

The boundary passes the product/platform test because procurement meaning remains outside the shared platform.

Product-owned:

- 44-ФЗ interpretation;
- requirements/risk semantics;
- contract-risk method;
- supplier questions/RFQ/TKP logic;
- quotation normalization;
- economics/bid-readiness;
- participation recommendation;
- procurement search/relevance;
- prompts/agents/models/domain configs;
- product validation/escalation;
- operator UX;
- partner report narrative;
- commercial packaging and product integrations.

Platform-owned only within existing domain-neutral responsibility:

- Product Contract version/continuity semantics;
- Organization/security/authority boundaries;
- CAP-001 governed Document/Artifact semantics;
- RFC-0005 governed execution/evidence semantics;
- RFC-0006 Event/provenance semantics;
- CAP-004 reconstruction semantics.

No procurement type, risk label, RFQ schema, supplier ontology, bid rule or workflow state is promoted into Kernel/shared capability semantics.

## 7. Side-effect and human-control review

P6.02 explicitly distinguishes operation classes:

- `Read-only` — CAP-001 exact version/handling resolution and CAP-004 reconstruction;
- `Transient` — product extraction, risk, RFQ, TKP, economics and recommendation computation;
- `Canonical mutation` — only bounded platform reference/execution/Event/review/final-artifact evidence needed for the governed path, through Governed Execution and applicable gates;
- `External mutation` — **none**;
- `Organizational commitment` — **none through this Product Contract**.

Client delivery remains manual. Final bid authorization/submission/signature remain outside scope.

AI remains an execution means. The contract gives AI no Authorization, Organizational Authority or final consequential approval.

## 8. Security, rights and Organization-scope review

The boundary preserves the stricter currently evidenced pilot controls:

- real customer/partner data is prohibited from repository evidence;
- raw real documents remain in approved controlled runtime locations;
- repository fixtures are synthetic/anonymized/redacted;
- product export/redaction guard and human delivery approval remain required;
- cross-Organization access is deny-by-default;
- Product Contract admission grants no access or authority;
- purpose/right/classification/minimization/retention/deletion propagate to material derived artifacts;
- credentials/tokens/secrets stay out of canonical history, ordinary logs, prompts and portable evidence;
- customer evidence creates no cross-customer reuse right;
- reconstruction cannot disclose evidence hidden by current rights/classification/redaction state.

Result: `PASS`.

## 9. Failure and reconstruction review

The contract fails closed for:

- stale/missing exact Product Contract continuity;
- Product/Organization drift;
- missing/incompatible/deprecated/retired/ambiguous CAP-001/CAP-004 provider/version evidence;
- undeclared operations;
- hidden private table/import/endpoint/Event/shared-state reliance;
- ambiguous source authority;
- missing exact source/version identity;
- access/purpose/right/classification denial;
- required reconstruction evidence gaps.

The existing product-local/manual path remains a valid rollback path, but a fallback run cannot be represented as having completed the Arvectum OS governed path.

Required evidence failure must expose incomplete/uncertain/unavailable/redacted/deleted/reconciliation-required state rather than manufacture a complete reconstruction claim.

Result: `PASS`.

## 10. Portability and migration review

The contract avoids irreversible migration:

- no historical bulk migration;
- prospective adoption only for selected Phase 6 cases;
- existing product-local cases remain product-owned;
- governed export preserves identities/versions/authority/source references/provenance/execution/review/final-artifact references and explicit lawful omissions;
- secrets/non-exportable third-party material are not promised as portable payload;
- rollback may return new cases to the current local/manual contour;
- admitted immutable history is preserved or lawfully minimized/deleted with truthful reconstruction limits rather than rewritten.

Result: `PASS`.

## 11. Bounded adoption decision

The plan is capped and staged:

1. **Stage 0 — P6.02 + R17:** contract only; no real governed reliance.
2. **Stage 1 — synthetic/redacted P6.03 proof:** instantiate exact `0.1.0` through the existing Product Contract/integration boundary and prove fail-closed paths.
3. **Stage 2 — one real 44-ФЗ case:** one explicit Organization; CAP-001/CAP-004 only; external actions manual.
4. **Stage 3 — bounded calibration set:** maximum three real calibration cases before P6.04 evidence disposition.

There is no automatic expansion from Stage 3.

Stop conditions include Organization leakage, authority ambiguity, contract/version discontinuity, incomplete required evidence, prohibited real-data persistence, automated external action, unenforceable rights/retention constraints, unacceptable platform delivery blockage without compensating value or an unapproved durable/stable architecture dependency.

Result: `PASS`.

## 12. Measurement baseline opened by P6.02

P6.02 begins measurement of platform adoption cost without inventing outcomes.

Record from this point:

- Product Contract definition/adaptation effort;
- product-side integration effort;
- platform-side adapter/capability effort;
- platform-induced operator steps;
- platform-induced failure modes;
- recovery effort;
- reconstruction completeness;
- hidden-coupling exceptions;
- rollback effort if exercised;
- boundary-attributable defects.

P6.04 will combine these with the existing product scorecard for active time, critical-requirement/risk quality and usefulness. Existing target thresholds are not rewritten as observed baselines.

## 13. Cross-review iterations

### Iteration 1 — product/platform boundary

Finding: P6.01 named CAP-001 + CAP-004 as a hypothesis, but adding CAP-002/CAP-003 would increase ceremony without evidence.

Disposition: CAP-002 and CAP-003 explicitly omitted. Procurement knowledge/search/relevance remain product-owned.

### Iteration 2 — authority / competing source of truth

Finding: treating downloaded ЕИС/partner/TKP documents or the final report as Native platform truth would conflate governance of a reference with factual/source authority.

Disposition: external source content uses `External Reference` by default. Native authority is limited to Arvectum OS Product Contract/execution/Event/review evidence within its actual scope.

### Iteration 3 — reversibility / delivery friction

Finding: a product-wide migration would prevent Phase 6 from distinguishing platform value from migration cost and could create coercive Platform Gravity.

Disposition: no bulk migration; one real case first and maximum three-case calibration set before evidence review. Existing product-local/manual contour remains the rollback path.

### Iteration 4 — security / human authority

Finding: canonical evidence registration must not turn successful Product Contract validation into permission, Organizational Authority or automated bid approval.

Disposition: runtime gates remain separate; canonical mutation uses Governed Execution and applicable Authorization/OrganizationalAuthority/DataGovernance/ConsequentialApproval; no external mutation or organizational commitment is admitted.

### Iteration 5 — compatibility / ADR / commercial integrity

Finding: normalizing current Python modules, operation tokens, storage, Event transport or IAM as stable interfaces would exceed P6.02 evidence.

Disposition: all such shapes remain internal/provisional. No ADR threshold, Stable Product Contract, Active capability, production-readiness or commercial-support claim is created.

No significant unresolved cross-review finding remains for the declared P6.02 scope.

## 14. P6.02 exit-criteria check

| Required evidence | Result | P6.02 disposition |
|---|---|---|
| real Product Contract exists before platform reliance | `PASS` | `P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`, Provisional `0.1.0` |
| explicit product/consumer and Organization scope | `PASS` | Organization-scoped product/contract identities; no ambient tenant |
| exact dependency versions | `PASS` | CAP-001 + CAP-004 Provisional `1.0.0` only |
| unnecessary capability dependencies rejected | `PASS` | CAP-002/CAP-003 omitted |
| canonical-state / authority modes explicit | `PASS` | external source documents remain external authority; platform authority limited to its own governed state/evidence |
| events/artifacts and reconstruction boundary explicit | `PASS` | exact inputs, execution, review and final artifact references required; telemetry remains noncanonical |
| security/rights/data handling explicit | `PASS` | current strict pilot controls retained; cross-Organization denied; secrets excluded |
| portability/migration responsibilities explicit | `PASS` | governed export semantics + no bulk migration + rollback |
| failure/retry behavior explicit | `PASS` | fail closed; no hidden fallback; evidence incompleteness exposed |
| what remains product-owned explicit | `PASS` | procurement semantics/workflow/search/knowledge/UX remain product-owned |
| adoption plan reversible and bounded | `PASS` | synthetic → 1 real case → max 3 cases; stop/rollback criteria |
| integration/value/friction measurements opened | `PASS` | effort/steps/failures/reconstruction/rollback fields begin; no fabricated values |
| ADR/public/stable/lifecycle gate disposition | `PASS` | no threshold crossed; no promotion/stabilization/readiness claim |

**P6.02 result: PASS.**

## 15. Lifecycle, ADR, conformance and commercial disposition

P6.02 changes only the existence of the first real Product Contract boundary.

- P6.02 Product Contract: `Provisional 0.1.0`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- CAP-001/CAP-004 are dependencies of this contract;
- CAP-002/CAP-003 are not dependencies of this contract version;
- P4.08/P5.09 reference Product Contracts remain unchanged;
- no Platform Capability becomes `Active`;
- no Product Contract becomes `Stable`;
- no production/operational-readiness approval is created;
- no public API/SDK/wire/package/service compatibility boundary is created;
- no SLA/support/customer compatibility promise is created;
- no full-platform conformance claim is made.

No new RFC or ADR is required for P6.02 because no durable or externally constraining technology/compatibility boundary is selected.

R17/P6.03 MUST reopen the minimum sufficient ADR/RFC/policy gate if implementation crosses durable persistence, Event delivery, IAM, evidence-integrity, public/stable API/serialization or service-topology reliance.

## 16. Final state and next action

**P6.02 — Complete / PASS.**

The first real Product Contract boundary is now canonically declared as `Provisional 0.1.0`, with CAP-001 + CAP-004 only, explicit external authority, product-owned procurement semantics, bounded evidence mutation, no automated external effects and a reversible maximum-three-case adoption plan.

The next canonical action is:

> **R17 — First Product Boundary Review.**

R17 must independently verify that the real Product Contract remains minimal, truthful about authority/security/rights, product-owned in domain semantics and reversible before P6.03 creates implementation reliance.