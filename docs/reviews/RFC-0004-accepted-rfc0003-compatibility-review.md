# RFC-0004 Compatibility Re-check Against Accepted RFC-0003

Status: `Complete`
Date: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Reviewed RFC: `RFC-0004 — Product Contract, Product Experiment and Extension Model` proposal `0.3.0`
Higher-authority baseline: Constitution `1.2.0`; RFC-0001 `1.0.0` Accepted; RFC-0002 `1.0.0` Accepted; RFC-0003 `1.0.0` Accepted
Owner approval evidence: `DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR`

## Purpose

Close the compatibility condition recorded in the RFC Index and the RFC-0004 owner-approval repair decision before canonical acceptance publication.

RFC-0004 `0.3.0` was functionally reviewed while RFC-0003 was still Proposed. RFC-0003 is now Accepted `1.0.0` and therefore has higher normative authority. This review checks whether the owner-approved RFC-0004 substance conflicts with that Accepted security, privacy, identity, tenant-sovereignty and portability baseline.

## Review result

No material conflict was found.

RFC-0004 already preserves the separations and invariants that RFC-0003 later made binding:

- registration or possession of a Product Contract does not grant authorization or Organizational Authority;
- organization and tenant scope remain explicit at product/platform boundaries;
- cross-organization access and reuse require explicit governed rights and must not arise ambiently;
- external authority modes remain preserved and product integrations must not create competing Native authority;
- security, classification, purpose limitation, minimization, retention, deletion, secret handling and portability responsibilities are declared or referenced at the boundary;
- technical permission remains distinct from consequential Organizational Authority and approval;
- AI extensions do not gain authority merely through registration, Product Contract scope or tool access;
- failure behavior must not broaden access, cross organization boundaries, lose required evidence or create silent consequential mutation.

These requirements are compatible with Accepted RFC-0003 `1.0.0` and do not weaken it.

## Status-language correction required for publication

The proposal text contains historical statements that RFC-0003 `0.2.0` was Proposed and non-normative. Those statements were correct when RFC-0004 `0.3.0` was prepared but are stale for acceptance publication.

For canonical RFC-0004 `1.0.0` publication, those statements must be interpreted and republished as follows:

- RFC-0003 `1.0.0` is an Accepted normative dependency;
- the compatibility re-check required by RFC-0004 Section 2.1 and Acceptance Criterion 3 is complete;
- references to later detailed security architecture remain subordinate to RFC-0003 and may not weaken it;
- no Product Contract, extension registration or product-specific declaration can grant access, delegated authority or cross-organization rights beyond RFC-0003.

This is a status/dependency reconciliation, not a substantive redesign of the owner-approved Product Contract model.

## Functional perspectives — additional iteration

This re-check counts as review iteration 4 for RFC-0004, within the project maximum of seven iterations.

1. CEO / strategy: no new commercial promise or platform scope is introduced.
2. COO / operations: contract failures remain explicit and bounded; no operational deadlock introduced by RFC-0003.
3. CTO / architecture: Product Contract remains domain-neutral and technology-independent.
4. CISO / security: deny-by-default, no ambient trust, least privilege and explicit boundary semantics are preserved.
5. Privacy / data governance: purpose, minimization, retention, deletion and cross-organization restrictions remain compatible.
6. Legal / rights: technical contract declarations do not create legal rights or Organizational Authority.
7. Product / commercial: Provisional versus Stable contract states remain distinct from Platform Capability lifecycle.
8. Engineering / delivery: no new mandatory vendor, protocol, service topology or enterprise-only mechanism is introduced.

No additional material correction was identified beyond status-language reconciliation.

## Acceptance conclusion

The compatibility condition is satisfied. RFC-0004 may be canonically published as Accepted `1.0.0` using the existing owner approval repair decision, provided the acceptance publication:

1. identifies RFC-0003 `1.0.0` as Accepted normative baseline;
2. preserves the normative substance of reviewed RFC-0004 `0.3.0` except for required status/dependency reconciliation;
3. synchronizes the RFC Index and canonical roadmap;
4. performs read-after-write verification under the RFC State Transition Procedure.
