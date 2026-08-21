# P9.07 — Product-owned workspace surfaces / composition

Status: `In Progress`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Predecessor: `R30 / M9-alpha — Complete / PASS`
Target journey: `P9.01 J5 — Work across products`

## Scope

P9.07 composes the real Tender Operator and Discount Parser contexts into the internal Productive Workspace through the compile-time product-owned UI boundary permitted by Accepted ADR-0001.

The shared composition contract is intentionally internal, release-scoped and provisional. It is not a public plugin API, does not promote a Product Contract or Platform Capability lifecycle state, and does not infer a business relationship between the two products.

Canonical baseline checked before implementation: Constitution `1.2.0`; RFC-0001 through RFC-0008 with direct focus on RFC-0003/RFC-0004; Accepted ADR-0001; P9.01 J5 acceptance; P6.02 and P6.06 Provisional Product Contracts; P7.07/P7.08 retained operational evidence; roadmap `2.81.0`.

## Implementation under review

- platform-owned `/products` navigation and same-origin protected BFF read;
- product-neutral `arvectum.workspace.product-composition/1` envelope;
- exact current Workspace Organization/Actor access revalidated before composition disclosure;
- P7.07 Tender retained context checked through P7.03 governed-item integrity verification;
- P7.08 Discount reconstruction report/receipt checked through immutable SHA-256 sidecars and exact Product Contract/CAP-004/containment invariants;
- compile-time contribution registry containing exactly Tender Operator and Discount Parser;
- product-owned contribution components keep detailed wording/UX outside the shared platform schema;
- no product code loading, product DB/internal-table access, external-effect client, canonical mutation or authority grant;
- technical Product Contract/release/evidence refs available only through explicit drill-down;
- Workspace release target `p9.07.1`, internal app contract `5`, still `bounded-internal-provisional` / non-public.

## Review state

Functional cross-review and CI are pending. This document MUST NOT be treated as closure evidence until status is changed to `Complete / PASS` after clean final-head normal CI and all material findings are resolved.
