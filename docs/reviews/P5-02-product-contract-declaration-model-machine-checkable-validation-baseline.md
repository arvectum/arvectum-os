# P5.02 — Product Contract Declaration Model + Machine-Checkable Validation Baseline Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Constitution: `1.2.0` — `Ratified`
Architecture basis: RFC-0001 `1.0.0`; RFC-0002 `1.0.0`; RFC-0003 `1.0.0`; RFC-0004 `1.0.0` — `Accepted`
Product Contract under validation: P4.08 `Provisional 0.1.0`
Capability state source: Platform Capability Catalog `1.2.1`
ADR disposition: no threshold crossed by this internal/provisional representation
Result: `PASS`

## 1. Purpose

P5.02 turns the already-existing RFC-0004 Product Contract reference representation into whole-declaration machine-checkable evidence for the P5.01 J1/J2 journeys and the current P4.08 boundary.

This work does **not** define a second Product Contract system. The existing `arvectum_os_ref.product_contract.ProductContract` object remains the executable declaration model and the P4.08 governed Product Contract remains the product/platform boundary source. The P5.02 module validates that declaration as a whole and returns immutable inspection evidence.

## 2. Canonical constraints revalidated

The implementation was checked against Constitution `1.2.0`, the RFC Index, Accepted RFC-0001 through RFC-0004 where directly relevant, the current capability catalog, P5.01, and the P4.08 Product Contract.

The resulting boundary preserves these constraints:

- Product Contract remains a versioned governed product/platform boundary;
- declaration/admission is not Authentication, Authorization, Organizational Authority, approval or permission;
- exact relied-upon dependency identity, contract version and operation remain inspectable;
- canonical read/write and authority-source semantics remain explicit;
- Organization scope, data handling, portability, retention/deletion, review and exit responsibilities remain explicit;
- hidden table/import/endpoint/Event/shared-state coupling fails closed;
- Product Contract lifecycle remains separate from Platform Capability lifecycle;
- Incubating capability lifecycle remains owned by the canonical capability catalog and is not copied into Product Contract validation state;
- current Python dataclasses/module paths remain internal/provisional implementation evidence rather than Stable/public compatibility contracts.

## 3. Implemented baseline

`reference/python/arvectum_os_ref/product_contract_declaration.py` adds:

- immutable dependency evidence preserving exact dependency Identity, contract version, allowed operations and existing Product Contract `provisional` reliance qualifier;
- immutable operation evidence preserving side-effect class and required gate declarations;
- immutable canonical-access evidence preserving semantic type, authority mode/scope, read/write access, authoritative source and failure behavior;
- immutable whole-declaration validation evidence preserving exact Product Contract pin, Product identity/version, Organization, accountable owner, Product Contract lifecycle, bounded scope, compatibility assumptions, portability, retention/deletion, review and exit responsibilities;
- whole-declaration validation over the current RFC-0004 `Provisional` reference scope;
- static hidden-coupling rejection for non-contract boundary mechanisms.

The validator deliberately supports only the current `Provisional` P5.02 reference baseline. It fails closed for Draft/Stable/Deprecated/Retired instead of claiming lifecycle validation for evidence P5.02 does not possess.

## 4. Machine-checkable fail-closed rules

For the current J1/J2 baseline, validation rejects:

1. non-Provisional Product Contract lifecycle;
2. dependency reliance that is no longer explicitly Provisional;
3. dependency operations without an exact Product Contract operation declaration;
4. Product Contract operations not allowed by the exact dependency declaration;
5. governed operations without Authorization and Data Governance gate declarations;
6. canonical mutation without Organizational Authority declaration;
7. read operation without canonical Read access;
8. canonical mutation without canonical Write access;
9. missing/invalid authority source or canonical-access failure behavior;
10. missing portability, retention/deletion, review or exit responsibility;
11. Organization/Product identity scope drift already rejected by the underlying Product Contract model;
12. hidden table/import/undocumented-endpoint/private-Event-stream/implicit-shared-state boundary mechanisms.

These checks validate declarations. They do not satisfy any runtime gate or create a permission/authority decision.

## 5. Cross-review iterations

### Iteration 1 — semantic owner / second-contract-system review

Finding: a new YAML/JSON/SDK manifest or parallel Product Contract dataclass would duplicate the RFC-0004 boundary source and prematurely stabilize representation.

Disposition: rejected. P5.02 validates the existing `ProductContract` semantic owner instead. No serialization or registry was selected.

### Iteration 2 — declaration completeness review

Finding: the first validation evidence shape preserved exact contract/product/dependency/operation/access state but did not copy accountable owner, bounded scope and compatibility assumptions into the immutable validation result.

Remediation: added those fields to the derived validation evidence while keeping them sourced from the existing Product Contract rather than creating parallel state.

### Iteration 3 — security / authority review

Finding: successful static declaration validation must not be reusable as an Authorization or Organizational Authority decision.

Disposition: result objects contain no Authentication, Authorization, permission, Organizational Authority, approval, capability-lifecycle or activation fields. Required gate declarations are inspectable only as declarations. Canonical mutation still requires the existing Governed Execution path for consequential action.

### Iteration 4 — lifecycle / commercial integrity review

Finding: P5.02 has evidence for the current P4.08 Provisional boundary only and must not validate or imply Stable Product Contract or Active capability status.

Disposition: the validator admits only `Provisional`; dependency `provisional` is retained only as Product Contract reliance/support qualification; Incubating capability lifecycle stays canonical in the capability catalog. No lifecycle promotion or operational/commercial claim is created.

### Iteration 5 — technology / ADR review

Finding: choosing YAML, JSON, protobuf, OpenAPI, a package registry, extension registry or public SDK/API here would cross later stable-boundary/ADR gates without evidence.

Disposition: none selected. The implementation is an internal Python reference validator only. No ADR threshold is crossed.

## 6. Executable evidence

`reference/python/tests/test_p5_02_product_contract_declaration_validation.py` covers 16 focused positive and negative cases, including exact P4.08 contract/product/dependency/operation/version validation; immutable evidence; separation from permission/authority/capability activation; fail-closed lifecycle, gate, canonical read/write, Organization, portability/retention/review/exit and hidden-coupling behavior; and internal/reversible/domain-neutral/no-serialization fitness.

Hosted CI observation #1: `Reference Python CI` run `#201` executed 586 tests. All 16 P5.02 tests passed, while two pre-existing P3.12 closure guards failed because they froze obsolete exact wording in current planning documents despite declaring that later phases must remain free to progress.

The historical P3.12 guard was hardened to test the preserved M3 semantics rather than obsolete prose: Phase 3 remains Complete/M3, CAP-001 through CAP-004 remain Incubating/Provisional, M3/M4 do not imply Active, and lifecycle/environment/conformance remain distinct.

Hosted CI observation #2: `Reference Python CI` run `#205` completed successfully on the synchronized implementation head, including the full reference suite and all P5.02 tests.

## 7. Exit evidence

- exact Product Contract identity/version and declared dependency versions/operations are machine-checkable — `PASS`;
- authority/security/data/canonical-access/portability/review/exit declarations fail closed when missing or inconsistent — `PASS`;
- declaration validation grants no permission or Organizational Authority — `PASS`;
- Product Contract lifecycle remains distinct from capability lifecycle — `PASS`;
- Product Contract remains the single governed boundary source rather than a parallel manifest/schema system — `PASS`;
- current implementation creates no Stable/public compatibility surface — `PASS`;
- hosted full reference CI — `PASS` (`#205`).

## 8. Final disposition

**PASS — P5.02 is complete for the declared internal/provisional Product Contract declaration-validation baseline.**

Next gate: **R13 — Integration Boundary Review**. R13 must confirm that the resulting tooling still expresses the RFC-0004 boundary rather than inventing a second contract system before P5.03 begins.

No new RFC, ADR, Stable/public Product Contract schema, API/SDK/wire/package compatibility boundary, capability promotion, production-readiness claim, conformance expansion, SLA/support promise or commercial commitment is created by P5.02.
