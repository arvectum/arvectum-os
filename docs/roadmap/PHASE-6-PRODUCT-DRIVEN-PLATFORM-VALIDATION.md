# Arvectum OS Phase 6 — Product-driven Platform Validation

Status: `Active`
Version: `1.3.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M6 — Platform validated through real products and reuse evidence`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 5 — SDK, Contracts and Extension Experience`, `M5` achieved

## 1. Purpose

Phase 6 validates Arvectum OS through real product/workflow use rather than platform-only reference scenarios.

The phase must produce evidence that the platform creates organizational value and reusable leverage while preserving the Constitution and Accepted RFC boundaries.

Phase 6 is deliberately product-driven:

- product sequencing follows real organizational/business value and evidence;
- product-local reversible experiments remain product-local unless platform interaction requires a Product Contract;
- successful local mechanisms do not become Platform Capabilities automatically;
- platform behavior remains domain-neutral;
- current Incubating capabilities are validated through real reliance before any later lifecycle admission decision;
- no product list is frozen by this roadmap.

The phase does not assume that Tender, Marketing, Sales, Legal, Finance or any other named product must be implemented in a fixed order.

P6.01 is complete. The selected first real validation target is the Arvectum procurement/tender AI operator in a bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package, while external actions remain manual. Canonical completion evidence is [`P6-01-real-product-workflow-validation-target-evidence-baseline.md`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md).

P6.02 is complete. The first real Product Contract is [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`, with exactly CAP-001 + CAP-004 at Provisional contract `1.0.0`. CAP-002/CAP-003 are intentionally omitted from the first slice; procurement semantics remain product-owned; external tender/TKP sources remain externally authoritative; external actions remain manual. Completion evidence is [`P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md`](../reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md).

R17 is complete with **PASS** under [`R17-first-product-boundary-review.md`](../reviews/R17-first-product-boundary-review.md). The independent review confirmed unchanged P6.01 product evidence, CAP-001/CAP-004 minimality, CAP-002/CAP-003 omission, external authority preservation, product ownership, fail-closed Organization/security/rights/evidence behavior, bounded reversibility and absence of a hidden durable/public/stable architecture choice. P6.03 is now the current work item, beginning with Stage 1 synthetic/anonymized/redacted proof only.

## 2. Starting state inherited from M5

M5 established:

- repeatable governed integration through explicit Product Contracts;
- exact dependency/version compatibility;
- reusable internal/provisional integration tooling;
- two materially distinct bounded reference consumers;
- no hidden platform coupling;
- no Stable/public SDK/API/package/wire compatibility boundary;
- no Platform Capability lifecycle promotion;
- no production-readiness claim.

At Phase 6 start:

- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 Product Contracts remain `Provisional 0.1.0` reference evidence;
- no real product is deemed validated merely because bounded reference consumers exist;
- no platform capability is `Active`.

P6.02 adds the first **real** Product Contract boundary without changing that lifecycle baseline. The new procurement Product Contract remains `Provisional 0.1.0`; it does not stabilize the Phase 5 integration mechanism or create production/support claims.

R17 changes only the gate disposition: the P6.02 boundary is independently reviewed and may enter P6.03 Stage 1. It does not change capability lifecycle, Product Contract lifecycle, operational readiness or public compatibility status.

## 3. Phase 6 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P6.01` | Real product/workflow validation target selection + evidence baseline | 🟩 Complete | `██████████ 100%` |
| `P6.02` | First real Product Contract boundary + bounded adoption plan | 🟩 Complete | `██████████ 100%` |
| `P6.03` | First real product/workflow platform integration | 🟨 Current | `░░░░░░░░░░ 0%` |
| `P6.04` | Product value, delivery-friction + governance evidence capture | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.05` | Platform-gap remediation from first real use | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.06` | Second materially distinct real product/workflow target + Product Contract | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.07` | Second real product/workflow platform integration | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.08` | Cross-product reuse and Platform Gravity evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.09` | Capability lifecycle / return-to-product / containment recommendations | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.10` | Product-driven architecture fitness + value evidence matrix | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P6.11` | Product/platform hardening, ADR + refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P6.12` | Phase 6 / M6 closure review | ⬜ | `░░░░░░░░░░ 0%` |

## 4. Work-item intent and exit evidence

### P6.01 — Real product/workflow validation target selection + evidence baseline

Select the first real product or operational workflow based on current organizational value, availability, owner/sponsor commitment and suitability for bounded platform validation.

Required evidence:

- named product/workflow owner and sponsor;
- concrete organizational/business outcome;
- bounded workflow scope;
- current baseline for time/cost/quality/risk/manual effort where measurable;
- platform capabilities/state/history actually required;
- authoritative external systems, if any;
- data/security/rights constraints;
- explicit reason the target is suitable for Phase 6;
- exit/rollback path.

Selection alone creates no Product Contract and no platform commitment.

**Completion:** `PASS` under [`P6.01 evidence baseline`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md). The selected target is the real Arvectum procurement/tender AI operator workflow for a bounded 44-ФЗ pre-bid decision package. CAP-001 and CAP-004 are the minimum evidence-backed platform-dependency hypothesis for P6.02; CAP-002/CAP-003 remain conditional rather than forced. Empirical customer KPI values that do not yet exist are explicitly marked not-yet-observed rather than invented.

### P6.02 — First real Product Contract boundary + bounded adoption plan

Create or adapt a Provisional Product Contract for the selected real product before governed platform reliance.

The contract must declare exact dependencies, canonical-state interactions, events/artifacts, authority modes, security/rights/data handling, portability/migration responsibilities and failure behavior proportionate to the workflow.

The adoption plan must remain reversible and identify what stays product-owned.

**Completion:** `PASS` under [`P6.02 review`](../reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md). The first real Product Contract is [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`. It confirms only CAP-001 + CAP-004 at exact Provisional capability contract `1.0.0`; omits CAP-002/CAP-003; preserves external authority for ЕИС/partner/supplier source documents; keeps procurement-domain semantics in the product; allows no automated external mutation/organizational commitment; and caps adoption at synthetic/redacted proof → one real case → maximum three platform-backed calibration cases.

**R17 disposition:** `PASS`. The boundary is independently verified and no Product Contract version change is required before P6.03 Stage 1.

### P6.03 — First real product/workflow platform integration

Implement the smallest useful real workflow through the governed platform boundary.

The integration must reuse existing runtime/capability/workspace/integration semantics where they fit and must not force product-domain behavior into shared platform code.

P6.03 must proceed in the P6.02/R17 adoption order:

1. **Stage 1 — synthetic/anonymized/redacted proof** under exact Product Contract `0.1.0` and exact CAP-001/CAP-004 Provisional `1.0.0` provider/version evidence;
2. **Stage 2 — one real 44-ФЗ case** only after Stage 1 proves required fail-closed and no-hidden-coupling behavior;
3. **Stage 3 — maximum three platform-backed calibration cases** before P6.04/P6.05 disposition.

Stage 1 must prove at minimum:

- exact Product Contract declaration/version continuity;
- exact current CAP-001/CAP-004 dependency/provider support evidence;
- wrong-Organization denial;
- rights/classification/purpose denial;
- missing/stale/incompatible dependency version failure;
- truthful incomplete reconstruction behavior;
- no private platform table/import/endpoint/Event/cache fallback;
- no external mutation or organizational commitment;
- changed-scope focused tests and applicable reference regressions pass.

The three-case limit is a Phase 6 **platform-backed adoption cap**, not a redefinition of the broader product-local pilot, which may continue through its existing manual contour outside this bounded Arvectum OS sample.

### P6.04 — Product value, delivery-friction + governance evidence capture

Measure whether platform reuse materially improves at least one relevant outcome such as:

- delivery speed;
- integration effort;
- quality/defect rate;
- operator clarity;
- explainability/reconstruction;
- governance/control quality;
- portability;
- security/risk;
- operating cost.

Also record platform overhead and friction. Evidence must be allowed to show that a platform abstraction creates no value.

### P6.05 — Platform-gap remediation from first real use

Resolve only gaps demonstrated by the first real integration.

Possible dispositions:

- fix existing platform behavior;
- clarify Product Contract;
- keep behavior product-local;
- add bounded capability functionality;
- simplify/remove a shared abstraction;
- open RFC/ADR/policy work where the decision level requires it.

No speculative generalization.

### P6.06 — Second materially distinct real product/workflow target + Product Contract

Select a second real context that is materially distinct enough to test reuse rather than duplicate the first case.

It must exercise a meaningfully different workflow, data/authority shape, capability composition or operational context.

A real Product Contract is required where it relies on platform capabilities, shared platform history or canonical state.

### P6.07 — Second real product/workflow platform integration

Implement the second bounded real integration through the same governed platform foundations where reuse is justified.

The purpose is to expose accidental coupling and validate or invalidate reuse hypotheses.

### P6.08 — Cross-product reuse and Platform Gravity evidence

Compare both real integrations and record:

- shared capabilities actually reused;
- duplicated behavior that should remain product-owned;
- recurring domain-neutral mechanisms;
- migration/support burden;
- integration effort saved or added;
- evidence for Platform Gravity candidates;
- evidence against centralized platform responsibility.

A repeated mechanism is not automatically promoted.

### P6.09 — Capability lifecycle / return-to-product / containment recommendations

For CAP-001 through CAP-004 and any newly identified candidate, produce a lifecycle recommendation based on Phase 6 evidence:

- remain `Incubating`;
- prepare separate `Active` admission review;
- contain scope;
- return responsibility to product;
- replace/deprecate;
- continue evidence gathering.

This task does not itself promote any capability to `Active`.

### P6.10 — Product-driven architecture fitness + value evidence matrix

Cross-cutting matrix covering both positive and negative evidence for:

- Product Contract discipline;
- domain-neutral platform boundary;
- canonical-state integrity;
- authority/security/Organization isolation;
- exact version/provenance reliance;
- product ownership of domain semantics;
- portability/migration;
- reuse without hidden coupling;
- measurable organizational value;
- platform overhead;
- lifecycle honesty;
- commercial-integrity boundaries.

### P6.11 — Product/platform hardening, ADR + refactoring review

Re-open architecture, ADR, Product Contract, lifecycle and code-health gates after real-product evidence exists.

Review whether actual use has now made any technology or compatibility choice materially constraining, including durable persistence, event delivery, IAM, public/stable API/SDK, serialization, service topology, search/vector/document storage, supported extension surfaces or operational dependencies.

Refactor only where real two-context evidence justifies it.

### P6.12 — Phase 6 / M6 closure review

Close Phase 6 only when the declared M6 criteria are satisfied and all material findings have a canonical disposition.

## 5. Engineering and product-validation gates

| Gate | Trigger | Purpose | Status |
|---|---|---|---|
| `R17 — First Product Boundary Review` | after P6.02 | verify real target, Product Contract boundary, product ownership and reversibility before implementation reliance | **Complete / PASS** |
| `R18 — First Real-use Health Review` | after P6.05 | review product value, friction, security/governance findings and evidence-backed remediation | Pending |
| `R19 — Cross-product Reuse Review` | after P6.08 | validate reuse against two real contexts and prevent speculative platform generalization | Pending |
| `R20 — M6 Product-validation Hardening` | after P6.10 | final architecture/code/evidence/lifecycle/commercial-integrity hardening before P6.11/P6.12 | Pending |

These gates are engineering/governance checkpoints and do not count as equal-weight P6 work items.

## 6. Dependency-aware sequence

```text
M5 ✓
 ↓
P6.01 Real target + baseline ✓
 ↓
P6.02 Product Contract + adoption plan ✓
 ↓
R17 First Product Boundary Review ✓
 ↓
P6.03 First real integration ← current
   Stage 1 synthetic/redacted proof
   ↓
   Stage 2 one real case
   ↓
   Stage 3 max three platform-backed calibration cases
 ↓
P6.04 Value / friction evidence
 ↓
P6.05 Evidence-backed remediation
 ↓
R18 First Real-use Health Review
 ↓
P6.06 Second real target + Product Contract
 ↓
P6.07 Second real integration
 ↓
P6.08 Cross-product reuse / Platform Gravity evidence
 ↓
R19 Cross-product Reuse Review
 ↓
P6.09 Lifecycle recommendations
 ↓
P6.10 Product-driven fitness + value matrix
 ↓
R20 M6 Product-validation Hardening
 ↓
P6.11 ADR / refactoring / boundary review
 ↓
P6.12 Closure review
 ↓
M6
```

## 7. M6 exit criteria

`M6 — Platform validated through real products and reuse evidence` is achieved only when all applicable criteria pass:

1. at least two materially distinct **real** product/workflow contexts have bounded owner-backed validation evidence;
2. each platform-reliant real context uses an applicable explicit Product Contract;
3. both contexts exercise shared Arvectum OS foundations without private hidden coupling;
4. product-domain semantics remain product-owned;
5. at least one material shared reuse benefit is evidenced across the real contexts;
6. platform friction/overhead is explicitly measured and dispositioned rather than hidden;
7. consequential operations preserve Governed Execution, exact versions, authority and provenance semantics;
8. Organization/security/rights/data-governance controls remain fail-closed;
9. lifecycle recommendations for retained/incubating capabilities are evidence-backed and do not silently promote them;
10. Platform Gravity findings distinguish reusable platform candidates from product-local mechanisms and commodity infrastructure;
11. P6.10 product-driven fitness/value matrix passes within declared scope;
12. R17–R20 material findings are resolved or explicitly bounded;
13. all crossed ADR/RFC/Product Contract/policy gates have canonical dispositions;
14. P6.12 closure review passes.

M6 does not require any capability to become `Active`, any Product Contract to become `Stable`, production deployment, SLA/support commitments or a public SDK/API.

## 8. Scope exclusions

Phase 6 does not automatically include:

- a fixed portfolio of named products;
- migration of all existing products to Arvectum OS;
- production infrastructure hardening;
- enterprise SSO/IAM/HA/backup/SLO work unless real use crosses the applicable gate;
- public marketplace or ecosystem work;
- public SDK/API stabilization;
- automatic capability promotion;
- speculative generic business modules.

## 9. ADR and governance gate

Real-product pressure may cross decisions that reference phases did not. Before material reliance, create the minimum sufficient ADR/RFC/policy/Product Contract decision where actual evidence crosses the relevant threshold.

Do not delay a bounded reversible product validation merely because a future production technology remains undecided, but do not use experimentation to bypass security, authority, data integrity, contractual commitments or governance.

P6.02/R17 select no durable persistence, Event delivery, IAM, public/stable serialization/API or service topology and therefore create no new ADR. P6.03 must reopen the minimum sufficient gate if implementation crosses one.

## 10. Current canonical action

> **P6.03 — First real product/workflow platform integration, beginning with Stage 1 synthetic/anonymized/redacted proof.**

R17 has passed. P6.03 must now instantiate the exact P6.02 `Provisional 0.1.0` Product Contract through an explicit governed integration path, bind only CAP-001 + CAP-004 at exact Provisional capability contract `1.0.0`, and prove fail-closed Organization/rights/dependency/evidence behavior plus no hidden private platform coupling using synthetic/anonymized/redacted fixtures.

Do not begin the one-real-case Stage 2 merely because R17 passed. Stage 1 focused and applicable regression evidence must pass first. If Stage 1 reveals an undeclared capability dependency, authority ambiguity, security/rights failure, hidden coupling or a durable/public/stable implementation commitment, stop and reopen the minimum sufficient Product Contract/ADR/RFC/policy gate before real reliance.