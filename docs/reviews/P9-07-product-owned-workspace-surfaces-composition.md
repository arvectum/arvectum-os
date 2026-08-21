# P9.07 — Product-owned workspace surfaces / composition

Status: `Complete / PASS`
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

## Closure evidence

- Final implementation/reconciliation head: `8e947d1631c850a9cda683edd2d425501b2ac6ce`.
- Productive Workspace CI `#82` / run `32523233168`: `SUCCESS`, including BFF security/context, typecheck, frontend tests, Web Storage guard, production build, committed-asset reproducibility and release-pinned asset boundary.
- Reference Python CI `#314` / run `32523233189`: `SUCCESS`.
- Functional cross-review: 2 iterations, with no remaining material objection. This review is functional evidence, not formal governance approval.
- P9.01 J5 — Work across products: `PASS` through the ordinary path `Home/company context -> Products -> Tender Operator -> back/company context -> Discount Parser`.
- Two product-owned surfaces are composed: Tender Operator and Discount Parser.
- Organization and Actor continuity is server-resolved and revalidated; switching products does not widen authorization.
- Internal IDs are not required on the ordinary path; technical references are available only through explicit drill-down.
- No cross-product business relationship is inferred.
- No canonical mutation, external effect or authority grant is available through this surface; unavailable or unverifiable product evidence fails closed.
- P6.02 and P6.06 remain `Provisional 0.1.0`; CAP-001 and CAP-004 lifecycle states remain unchanged.
- Workspace release remains `p9.07.1`, application contract `5`, `bounded-internal-provisional`, `public_api: false`.
- Temporary artifact-capture instrumentation and helper workflow are absent.

## Explicit limitations

- Surfaces are internal read-only product context surfaces, not full product command UIs.
- The composition boundary is not a public plugin API.
- This evidence does not establish Stable Product Contract or Active Platform Capability lifecycle status.
- This is not public/customer Production evidence.
- No SLA, support or conformance expansion is claimed.
