# P9.10 — ООО «Арвектум» organization composition

Status: `Implementation review checkpoint — roadmap closure pending`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Predecessor: `P9.09 — Complete / PASS`

## Canonical baseline checked

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- direct task checks: RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007, RFC-0008;
- ADR-0001 — `Accepted` for the exact Phase 9 Productive Workspace topology;
- canonical roadmap `2.84.0` and Phase 9 roadmap `1.11.0` before closure.

No higher-authority conflict was found. No Constitution amendment, new RFC/ADR, Product Contract lifecycle transition or Platform Capability promotion is required by this bounded read-side composition.

## Implemented scope

P9.10 adds a server-authorized `arvectum.workspace.organization-composition/1` projection and an `Organization` Workspace surface.

The company-level view composes four lanes without creating a new source of truth:

1. **Products** — reuses the P9.07 product-owned composition boundary; product semantics and detailed UI remain product-owned.
2. **Project lenses** — navigation-only views over already-declared product operating contours. They are explicitly `canonical_project_record: false`; no canonical Project model, cross-product business relationship or company-specific Kernel type is inferred.
3. **Knowledge** — reuses P9.05 authorized Discovery and carries an explicit semantic note so Observation / Organizational Memory / Knowledge Candidate / validated Knowledge distinctions are not flattened.
4. **Work** — reuses P9.04/P9.09 attention semantics and routes the user to inspectable context only; visibility grants no Authorization, Organizational Authority or approval and no consequential action is exposed by the composition layer.

The composition is rebuildable and non-authoritative. Organization and Actor are resolved server-side; current access is revalidated by the existing BFF boundary; unavailable protected source lanes are withheld rather than guessed; cross-Organization aggregation and denied-source count disclosure are false.

Workspace release advances to `p9.10.1`, internal application contract `8`, still `bounded-internal-provisional` with `public_api: false`.

## Functional cross-review

Two iterations completed so far, within the maximum of 7.

1. **Architecture / product boundary / security.** Confirmed that company-level composition is a read-side navigation layer over existing authorized projections, not a canonical company database. Project contexts were deliberately represented as non-canonical project lenses rather than inventing a Project source of truth.
2. **RFC-0007 / BFF failure semantics.** Found that the first implementation preserved Knowledge-role distinctions mainly through summary prose and let a structural composition error fall through as a generic server error. Remediation added explicit `semantic_note` presentation and a minimized `ORGANIZATION_COMPOSITION_UNAVAILABLE` 503 boundary. Bounded backend/frontend verification and exact-release rebuild passed after remediation.

A final post-CI implementation review and canonical roadmap synchronization remain before `Complete / PASS`.

## Verification checkpoint

Initial implementation head `381919128c140b7f0eb3d95117714de51ae61469` passed independent PR gates before the cross-review remediation:

- Productive Workspace CI `#107` / run `32557090325` — `SUCCESS`;
- Reference Python CI `#339` / run `32557090431` — `SUCCESS`.

The remediation helper subsequently passed the same bounded backend/frontend suites, Web Storage guard, production build and release-asset verification before removing itself. The helper-removal commit is intentionally not treated as independent CI evidence because GitHub marks runs for commits touching temporary workflow definitions as `action_required`.

A clean ordinary PR head will be used for the independent post-remediation merge gate.

## Explicit limitations

- This is not a canonical organization/company database.
- Project lenses are not canonical Project records and do not define a platform Project metamodel.
- No organization-specific business semantics are promoted into Kernel types or shared platform authority.
- Product-specific schemas, workflows, knowledge and UI remain product-owned.
- Knowledge composition does not promote Observation, Memory or Candidate state into validated Knowledge.
- Work/attention visibility does not grant Authorization, Organizational Authority, Consequential Approval or retry rights.
- No canonical mutation, external effect, public/stable API, Stable Product Contract, Active Platform Capability, SLA/support/certification or broader conformance claim is introduced.
