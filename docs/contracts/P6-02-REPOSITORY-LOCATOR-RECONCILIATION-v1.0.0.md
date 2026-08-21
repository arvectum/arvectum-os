# P6.02 — Repository Locator Reconciliation

Status: `Approved`
Version: `1.0.0`
Approved: `2026-08-21`
Published: `2026-08-21`
Owner: `ООО «Арвектум»`
Repository: `arvectum/arvectum-os`
Related Product Contract: `docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` — `Provisional 0.1.0`
Approval: `docs/governance/decisions/DECISION-2026-08-21-P6-02-REPOSITORY-LOCATOR-RECONCILIATION-APPROVAL.md`
Approved reviewed proposal: `docs/contracts/P6-02-REPOSITORY-LOCATOR-RECONCILIATION-PROPOSAL.md`, blob `95f32a2625a3df2c18615021aa2ca46f83faa946`
Cross-review evidence: `arvectum/arvectum-company/docs/reviews/AC-305-CROSS-PRODUCT-DEPENDENCY-AND-OS-CONTRACT-CROSS-REVIEW.md`, blob `369c42f8066ac8a10d3b00a0afd2fc034b8c7fe3`

## 1. Publication model

This publication records approval of the exact reviewed proposal without rewriting the historical P6.02 `0.1.0` Product Contract artifact.

Approved proposal:

- file: `docs/contracts/P6-02-REPOSITORY-LOCATOR-RECONCILIATION-PROPOSAL.md`;
- status: `Proposed 0.9.0`;
- immutable git blob SHA: `95f32a2625a3df2c18615021aa2ca46f83faa946`.

Owner approval wording:

> `AC-305 и P6.02 repository locator reconciliation в Arvectum OS утверждаю`

The normative content of the exact proposal blob is incorporated by reference and is approved within its declared scope.

## 2. Approved repository/provenance resolution

For current implementation resolution of the P6.02 product:

- current canonical implementation repository locator: `arvectum/tender-agent`;
- predecessor/historical repository locator preserved in P6.02: `arutyunoveth/ai-corporation`;
- Company portfolio correspondence: `PORT-001 — Arvectum Tender Agent`.

Repository location is implementation provenance/locator metadata. It does not define or replace Product Identity.

## 3. Product Contract continuity

The following remain unchanged:

- Product identity: `product/arvectum-tender-operator@<organization>`;
- Product compatibility line: `restricted-paid-pilot/44fz-prebid-v1`;
- Product Contract subject: `product-contract-subject/p6-02-arvectum-tender-operator@<organization>`;
- Product Contract version identity: `product-contract-version/p6-02-arvectum-tender-operator-v0.1.0@<organization>`;
- lifecycle: `Provisional`;
- exact platform dependencies: `CAP-001 — Document & Artifact Governance` and `CAP-004 — Audit / Reconstruction Support` in the P6.02 bounded scope;
- CAP-002/CAP-003 remain omitted;
- external procurement actions remain manual;
- human-review, Organization, authority, security and data-governance boundaries remain unchanged.

Therefore no new Product Contract semantic version is created by this locator reconciliation.

## 4. Historical evidence rule

`docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` remains unchanged as the historical canonical `Provisional 0.1.0` declaration. Its original repository locator is not erased or silently replaced.

When current implementation provenance is required, readers and governed resolvers must interpret the locator chain as:

`arutyunoveth/ai-corporation` → predecessor/historical implementation locator

`arvectum/tender-agent` → current canonical implementation repository locator

This overlay changes provenance resolution only; it does not rewrite historical evidence.

## 5. P8.03 continuity

`P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md` continues to supplement P6.02 `0.1.0` within its exact scope.

No cascading Product Contract version change is required solely because implementation repository provenance has been reconciled.

## 6. Explicit non-effects

This approved reconciliation does not:

- change Product Identity;
- widen P6.02 workflow scope;
- authorize 223-ФЗ/commercial procurement expansion;
- authorize autonomous supplier/customer/EIS/ETP external actions;
- merge Tender Agent with Tender Small-Volume Calculator;
- transfer procurement-domain semantics into Arvectum OS;
- create a new Platform Capability;
- make CAP-001/CAP-004 `Active`;
- make P6.02 `Stable`;
- create a public/stable API, SDK, manifest, wire or package contract;
- create customer production/SLA/support commitments;
- grant Authorization, Organizational Authority or approval.

## 7. Source-of-truth rule

- Company governance owns Company-level `PORT-001` identity and portfolio locator interpretation;
- `arvectum/tender-agent` owns current product-specific implementation/status/domain semantics;
- P6.02 owns the exact OS Product Contract semantic boundary;
- this publication owns only the current repository-locator/provenance reconciliation for P6.02.

Any later material semantic boundary change must create the appropriate new immutable Product Contract version through Arvectum OS governance.
