# DECISION-2026-08-18 — Tender Agent Repository Relocation

Status: `Approved`
Date: `2026-08-18`
Decision owner: `ООО «Арвектум»`
Task classification: `product_specific` with `product_contract` and `governance`
Constitution: `1.2.0` — `Ratified`
RFC baseline: RFC-0001 and RFC-0004 `1.0.0` — `Accepted`
Affected Product Contract: P6.02 `Provisional 0.1.0`

## 1. Decision

The current canonical repository locator for the product identified by P6.02 as `product/arvectum-tender-operator@<organization>` is:

`arvectum/tender-agent`

The following repository locators are historical only:

- `arvectum/ai-corporation` — immediate pre-relocation GitHub locator;
- `arutyunoveth/ai-corporation` — older blocked-account historical locator retained only as provenance.

The historical `arvectum/ai-corporation` repository name MUST NOT be reused for another repository while redirect/history compatibility is relied upon.

## 2. Continuity evidence

The GitHub rename preserved repository identity:

- GitHub repository ID before and after relocation: `1333401651`;
- pre-relocation canonical `main` SHA: `4558880d43455ca9ed482b5bbdefe6b9c137277a`;
- post-relocation repository: `arvectum/tender-agent`;
- GitVerse mirror repository: `arvectum/tender-agent`.

This is a repository relocation, not a product replacement, code copy, new lineage, or new Product Contract subject.

## 3. Product Contract treatment

This decision is a repository-locator reconciliation only. It does not change the P6.02 semantic boundary and therefore does not itself create a new Product Contract version.

P6.02 remains:

- lifecycle: `Provisional`;
- effective exact Product Contract version for the implemented P6.03 bridge: `0.1.0`;
- Product Contract subject: unchanged;
- product identity: unchanged;
- platform dependencies: unchanged;
- authority/data-handling/external-action boundaries: unchanged.

Existing P6.03 product-side regression evidence explicitly pins `p6-02-arvectum-tender-operator-v0.1.0`. A Product Contract version transition merely to update a repository locator would create an unnecessary compatibility migration and is not admitted by this decision.

The `Product repository: arutyunoveth/ai-corporation` line in the historical P6.02 `0.1.0` publication is retained as immutable historical content. For current repository discovery, integration maintenance and active lookup, this Approved decision is the canonical locator reconciliation and `arvectum/tender-agent` MUST be used.

Any future Product Contract version that republishes repository metadata MUST use `arvectum/tender-agent` or its then-current explicitly governed successor.

## 4. Data-handling reconciliation

Historical P6.02 text prohibiting real partner/customer data from being committed to `arvectum-os` or `ai-corporation` repositories continues to apply to the same product repository lineage after rename. The current repository name for that prohibition is `tender-agent`.

No real partner/customer data becomes admissible in source control because of this relocation.

## 5. Internal namespace boundary

Repository relocation does not authorize an internal namespace refactor. Existing compatibility names such as `AI_CORP_*`, Python package/module identifiers, database/Alembic history and runtime paths may remain until a separate bounded refactoring change is reviewed and implemented.

## 6. Roadmap and lifecycle impact

This decision does not:

- change the canonical Arvectum OS next action (`P7.06-UI2 — Governed interaction and preflight`);
- promote any Platform Capability;
- promote P6.02 beyond `Provisional`;
- establish Production, SLA/support, conformance or public-interface claims;
- alter any authorization or Organizational Authority grant.

## 7. Closure conditions

The repository relocation is closed only after:

1. renamed-repository GitHub CI passes;
2. GitHub-to-GitVerse mirror passes with the renamed destination;
3. repository identity/read-after-write verification confirms GitHub repository ID `1333401651` and preserved history;
4. this decision is merged canonically after functional cross-review.
