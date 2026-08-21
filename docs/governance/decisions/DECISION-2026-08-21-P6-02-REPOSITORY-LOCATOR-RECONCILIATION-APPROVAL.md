# DECISION-2026-08-21 — P6.02 Repository Locator Reconciliation Approval

Status: `Approved`
Decision date: `2026-08-21`
Owner / decision authority: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Decision subject: `P6.02 repository locator / provenance reconciliation`
Approved reviewed proposal blob: `95f32a2625a3df2c18615021aa2ca46f83faa946`
Cross-review evidence: `arvectum/arvectum-company/docs/reviews/AC-305-CROSS-PRODUCT-DEPENDENCY-AND-OS-CONTRACT-CROSS-REVIEW.md`, blob `369c42f8066ac8a10d3b00a0afd2fc034b8c7fe3`
Related Company decision: `arvectum/arvectum-company/docs/governance/decisions/DECISION-2026-08-21-AC-305-APPROVAL.md`
Constitution: `1.2.0` — `Ratified`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Related Product Contract: `docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` — `Provisional 0.1.0`

## 1. Decision

**APPROVED — accept the reviewed P6.02 repository-locator/provenance reconciliation proposal identified by blob `95f32a2625a3df2c18615021aa2ca46f83faa946`.**

The Owner explicitly approved it with the wording:

> `AC-305 и P6.02 repository locator reconciliation в Arvectum OS утверждаю`

The approved reconciliation records:

- current implementation repository locator: `arvectum/tender-agent`;
- predecessor/historical repository locator: `arutyunoveth/ai-corporation`;
- Company portfolio correspondence: `PORT-001 — Arvectum Tender Agent`;
- P6.02 Product identity remains `product/arvectum-tender-operator@<organization>`;
- Product Contract subject/version identities remain unchanged;
- Product Contract lifecycle remains `Provisional 0.1.0`.

## 2. Nature of the change

This is a repository-locator/provenance reconciliation only.

It does **not** change the semantic Product Contract boundary and therefore does not require a new P6.02 Product Contract version.

The original P6.02 artifact remains historical canonical evidence for the exact `0.1.0` contract declaration. It is not silently rewritten to erase its original repository locator. The approved reconciliation publication provides the current resolver overlay while preserving lineage.

## 3. Preserved Product Contract semantics

This decision does not change:

- the bounded 44-ФЗ pre-bid workflow;
- Product identity or Product Contract subject identity;
- compatibility line `restricted-paid-pilot/44fz-prebid-v1`;
- Organization scope;
- CAP-001/CAP-004 reliance;
- CAP-002/CAP-003 omission;
- human review requirement;
- manual external procurement actions;
- authority modes;
- security/privacy/data-governance boundaries;
- portability, reconstruction or failure semantics;
- support, SLA, conformance or customer commitments.

Any later material change to those semantics requires a new immutable Product Contract version through the applicable RFC-0004/governance path.

## 4. P8.03 continuity

`P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md` supplements P6.02 and remains `Provisional 0.1.0` within its exact scope.

Because this locator reconciliation does not alter the P6.02 semantic Product Contract version, no artificial P8.03 version cascade is created.

## 5. Authority and lifecycle non-effects

This approval does not:

- grant Authorization or Organizational Authority;
- widen the procurement workflow;
- authorize autonomous external actions;
- make P6.02 `Stable`;
- make CAP-001 or CAP-004 `Active`;
- create a public/stable API, SDK, wire protocol or package promise;
- merge Tender Agent with Tender Small-Volume Calculator;
- transfer procurement-domain semantics into Arvectum OS;
- create Company portfolio authority inside Arvectum OS.

## 6. Source-of-truth resolution

After this approval:

- Arvectum Company governance is authoritative for Company portfolio identity `PORT-001` and its current canonical product-repository locator;
- `arvectum/tender-agent` is authoritative for product-specific implementation/status;
- P6.02 remains authoritative for the exact Provisional Product Contract semantic boundary;
- the approved reconciliation publication is authoritative for resolving P6.02 implementation provenance from historical locator `arutyunoveth/ai-corporation` to current locator `arvectum/tender-agent`.

No source gains authority outside its declared scope.

## 7. Effective publication

This decision authorizes publication of:

`docs/contracts/P6-02-REPOSITORY-LOCATOR-RECONCILIATION-v1.0.0.md`

as the approved canonical locator/provenance overlay for P6.02.

The Arvectum OS canonical roadmap current implementation action is not changed by this governance-only reconciliation; Phase 9 work remains independently governed by its roadmap.
