# P6.02 — Repository locator reconciliation proposal

Status: `Proposed`
Version: `0.9.0`
Created: `2026-08-21`
Owner: `ООО «Арвектум»`
Repository: `arvectum/arvectum-os`
Related Product Contract: `docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md` — `Provisional 0.1.0`
Company reconciliation: `AC-305 — Inter-product dependency and Arvectum OS Product Contract reconciliation`
Decision authority: residual Arvectum OS Owner under the current governance baseline

## 1. Purpose

This proposal reconciles one stale implementation-repository locator carried by P6.02 without silently changing the Product Contract's product identity, governed boundary, capability dependencies, authority semantics or lifecycle.

Current evidence establishes:

- P6.02 `0.1.0` names `arutyunoveth/ai-corporation` as the product repository;
- approved Arvectum Company portfolio governance identifies `arvectum/tender-agent` as the current canonical implementation repository for Company portfolio node `PORT-001 — Arvectum Tender Agent`;
- the current `arvectum/tender-agent` repository still carries the procurement/tender operator implementation lineage evidenced by the P6.02 contour, including the `ai-corporation` package name and the same bounded human-reviewed pre-bid product semantics;
- repository location is implementation provenance/locator metadata and does not itself define Product Identity.

The repair therefore preserves the historical locator rather than rewriting history.

## 2. Proposed reconciliation

For current repository resolution of the P6.02 product implementation, record:

- current implementation repository locator: `arvectum/tender-agent`;
- predecessor/historical repository locator: `arutyunoveth/ai-corporation`;
- Company portfolio correspondence: `PORT-001 — Arvectum Tender Agent`;
- P6.02 Product identity remains: `product/arvectum-tender-operator@<organization>`;
- P6.02 Product Contract subject remains: `product-contract-subject/p6-02-arvectum-tender-operator@<organization>`;
- P6.02 Product Contract version remains: `product-contract-version/p6-02-arvectum-tender-operator-v0.1.0@<organization>`;
- Product Contract lifecycle remains: `Provisional`.

This is a repository-locator/provenance reconciliation only. It is not a Product Contract boundary migration.

## 3. Why the Product Contract version is not changed by this proposal

P6.02 requires a new immutable Product Contract Version Identity when the admitted governed boundary materially changes. This proposal does not change that boundary.

It does not change:

- the bounded 44-ФЗ pre-bid workflow;
- Product identity or Product Contract subject identity;
- compatibility line `restricted-paid-pilot/44fz-prebid-v1`;
- Organization scope;
- CAP-001 or CAP-004 reliance;
- CAP-002/CAP-003 omission;
- operation or side-effect classes;
- human-review and external-action restrictions;
- authority modes or external source authority;
- security, privacy, tenant or data-governance rules;
- portability, retention, reconstruction or failure semantics;
- lifecycle, support, conformance or customer commitments.

The original P6.02 `0.1.0` artifact and its historical git evidence remain unchanged. This proposal acts as an explicit governed resolver overlay for the implementation locator.

If any later reconciliation changes the product/platform semantic boundary, dependency set, operation set, authority/data scope or compatibility commitment, that change MUST use a new immutable Product Contract version under RFC-0004 and the existing P6.02 rules.

## 4. P8.03 continuity

`P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md` supplements P6.02 `0.1.0` and does not supersede it.

Because this proposal does not change P6.02's semantic Product Contract version, P8.03 does not require a cascading contract-version change merely to follow the current implementation repository locator.

P8.03 remains bounded to its exact EIS external-authority revalidation scope and retains its existing CAP-001/CAP-004 dependency boundary.

## 5. Authority and non-effects

Approval of this proposal would establish only the canonical interpretation of the repository locator for P6.02 implementation provenance.

It would not:

- grant Authorization, Organizational Authority or approval;
- make CAP-001/CAP-004 `Active`;
- make P6.02 `Stable`;
- create public API/SDK/wire compatibility;
- widen from 44-ФЗ to 223-ФЗ or commercial procurement;
- authorize autonomous external procurement actions;
- merge Tender Agent with Tender Small-Volume Calculator;
- transfer procurement-domain semantics into Arvectum OS;
- create a Company Product Contract or portfolio decision inside the OS repository.

## 6. Source-of-truth rule

After approval, the sources resolve as follows:

- Arvectum Company governance is authoritative for the Company-level portfolio identity `PORT-001` and its current canonical product repository locator;
- the Tender Agent repository is authoritative for product-specific implementation and status;
- P6.02 remains authoritative for its exact Provisional OS Product Contract boundary;
- this reconciliation record is authoritative only for mapping P6.02's historical repository locator to the current implementation locator while preserving lineage.

No source acquires authority outside its declared scope.

## 7. Approval requirement

Status remains `Proposed` until explicit Arvectum OS Owner approval of this exact reviewed proposal.

The approval record must identify the exact proposal git blob SHA and state that the change is a repository-locator/provenance reconciliation only, with no Product Contract semantic-version or lifecycle change.