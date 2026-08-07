# RFC-0004: Product Contract, Product Experiment and Extension Model

Status: `Accepted`
Version: `1.0.0`
Accepted: `2026-08-07`
Published: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `product_contract`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`
Supersedes: `RFC-0004 v0.3.0` reviewed proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Owner approval: `DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR`
Compatibility review: `docs/reviews/RFC-0004-accepted-rfc0003-compatibility-review.md`

## 1. Acceptance Publication

This document is the canonical Accepted publication of RFC-0004 `1.0.0`.

The owner-approved normative substance is the reviewed RFC-0004 `0.3.0` proposal preserved in repository history and identified by canonical proposal blob SHA:

`5a413a240588677211ad56f3a23b30a65d1c4334`

Historical proposal path:

`docs/rfc/RFC-0004-product-contract-product-experiment-extension-model.md`

The proposal is incorporated into this Accepted publication by immutable content reference, subject only to the status/dependency reconciliation in Section 2 below. This repair publication intentionally avoids rewriting the already reviewed proposal merely to change stale lifecycle wording.

This publication method preserves acceptance integrity: the owner approval exists independently before this acceptance publication, the approved proposal remains content-addressable, the RFC-0003 compatibility re-check is separately recorded, and the RFC Index identifies this file as the current canonical Accepted RFC-0004.

## 2. Normative Status and RFC-0003 Reconciliation

RFC-0003 is now `Accepted` as version `1.0.0` and is a normative dependency of RFC-0004.

The compatibility condition originally stated in RFC-0004 `0.3.0` Section 2.1 and Acceptance Criterion 3 has been satisfied by `docs/reviews/RFC-0004-accepted-rfc0003-compatibility-review.md`.

Accordingly, historical statements in the incorporated proposal that describe RFC-0003 `0.2.0` as `Proposed`, `non-normative`, or merely forward-compatible are superseded by this section and MUST be read as follows:

- RFC-0003 `1.0.0` is binding within its declared scope;
- Product Contracts, extensions, adapters and product/platform interactions MUST conform to RFC-0003 identity, authentication, authorization, Organizational Authority, tenant-isolation, data-governance, privacy, cross-organization and portability requirements;
- registration, contract declaration, tool access or technical permission MUST NOT itself grant Organizational Authority or cross-organization rights;
- no RFC-0004 mechanism may weaken RFC-0003 deny-by-default authorization, least privilege, isolation, purpose limitation, minimization, retention/deletion or failure-closed requirements.

No other normative substance of reviewed RFC-0004 `0.3.0` is changed by this acceptance publication.

## 3. Accepted Model

RFC-0004 `1.0.0` therefore establishes the binding domain-neutral Product Contract, Product Experiment and Extension model defined in the incorporated reviewed proposal, including:

1. Product Contract as the explicit versioned product/platform boundary;
2. no Product Contract requirement for fully product-local bounded experiments that do not use platform capabilities, shared platform history or canonical platform state;
3. mandatory Product Contract before governed platform reliance;
4. Product Contract lifecycle `Draft → Provisional → Stable → Deprecated → Retired`;
5. explicit dependency, canonical-state, operation, event, artifact, security, authority, data-handling, portability, compatibility and migration declarations proportionate to scope;
6. prohibition of hidden product/platform coupling through internal tables, undocumented endpoints, internal imports, private streams or implicit shared state;
7. separation of Product Contract lifecycle from Platform Capability lifecycle;
8. separate evidence-based promotion decision before product-local mechanisms enter platform incubation;
9. extension registration as governance/discovery rather than authorization or authority;
10. preservation of external authority and organization boundaries;
11. scoped conformance and normative fitness tests from the incorporated proposal.

## 4. Scope Boundary

This RFC does not define complete Governed Execution semantics, Event/Provenance/Observability semantics, or Memory/Knowledge/Governed Learning semantics. Those remain RFC-0005, RFC-0006 and RFC-0007 scope respectively.

RFC-0005 may now depend normatively on RFC-0004 `1.0.0` for Product Contract boundary semantics.

## 5. Acceptance Evidence

Owner approval evidence:

- `docs/governance/decisions/DECISION-2026-08-07-RFC-0004-OWNER-APPROVAL-REPAIR.md` — `Approved`.

Compatibility re-check against Accepted RFC-0003:

- `docs/reviews/RFC-0004-accepted-rfc0003-compatibility-review.md` — `Complete`, review iteration 4.

Approved reviewed proposal:

- RFC-0004 `0.3.0`;
- immutable proposal blob SHA `5a413a240588677211ad56f3a23b30a65d1c4334`.

This acceptance publication MUST be followed by RFC Index and canonical roadmap synchronization plus read-after-write verification under the approved RFC State Transition Procedure.

## 6. Authority

RFC-0004 `1.0.0` is binding architecture within its declared product-contract scope from this acceptance publication onward.

Where this RFC conflicts with Constitution `1.2.0`, RFC-0001 `1.0.0`, RFC-0002 `1.0.0` or RFC-0003 `1.0.0`, the higher-authority source prevails.
