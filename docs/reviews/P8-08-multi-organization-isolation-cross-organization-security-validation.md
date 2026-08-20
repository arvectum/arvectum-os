# P8.08 — Multi-Organization Isolation + Cross-Organization Security Validation

Status: `Complete / NOT ACTIVATED — realistic two-Organization isolation remains unproven`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract` boundary implications
Constitution: `1.2.0` (`Ratified`, frozen)
Checked Accepted RFC: RFC-0001 through RFC-0008 (`1.0.0`), with RFC-0003 as the primary security/isolation authority
Checked ADR: no Accepted ADR exists for a permanent multi-Organization persistence, IAM, cache/index/search, observability, support/admin or deployment-isolation topology
Roadmap source: `docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`
Predecessor: `P8.07 — Complete / PASS — bounded interoperability proof; external customer transfer NOT ACTIVATED`

## 1. Decision

P8.08 is dispositioned as `Complete / NOT ACTIVATED` rather than as a fabricated multi-Organization `PASS`.

The canonical Phase 8 activation still contains exactly one governing Organization: `ООО «Арвектум»`. The separately maintained Creative Test Agent consumer introduced by P8.06 is owned inside the same governing Organization and does not create a second Organization sovereignty boundary. P8.07 likewise preserved customer/cross-Organization transfer as `NOT ACTIVATED`.

No canonical decision, Product Contract, rights record, customer scope, tenant mapping, external-recipient activation or other owner-approved artifact exists after P8.07 that would place a second Organization genuinely in scope. The repository `main` state at the start of this review is the P8.07 merge commit `eec79ea6abfaf2e1ee2092fb5db4b96ad1f4c874`; no later canonical commit activates another Organization.

RFC-0003 requires realistic isolation evidence to be evaluated against actual Organization scopes and explicitly denies ambient cross-Organization authority. The Phase 8 roadmap additionally prohibits inventing Organization B merely to satisfy sequencing. Therefore creating a synthetic second customer/Organization and then calling its unit-test separation a realistic tenant-isolation proof would overstate evidence and violate the approved scope.

This review closes the roadmap step by proving the **activation condition is absent**, preserving existing fail-closed cross-Organization guards, defining the exact re-entry trigger, and carrying the unproven two-Organization claim forward explicitly. It does not claim realistic multi-Organization isolation.

## 2. Canonical compatibility

The disposition is consistent with the authority hierarchy:

- Constitution Article VIII makes security, privacy, confidentiality and data isolation structural properties; proportionality does not permit bypassing tenant isolation.
- RFC-0001 requires Organization scope, deny-by-default cross-organization access, no automatic cross-organization learning/reuse and failure behavior that does not silently cross tenant boundaries.
- RFC-0002 keeps Identity, Canonical Record scope and projections/caches semantically distinct from authorization and authority.
- RFC-0003 is controlling for this task: Organization is the sovereignty boundary; tenant-to-Organization mapping must be unambiguous; unresolved scope fails closed; background work, caches, indexes, AI context and derived data must preserve Organization boundaries; cross-organization access/reuse is denied by default; realistic isolation conformance requires actual cross-boundary prevention evidence.
- RFC-0004 prevents Product Contracts, extensions or registration from becoming ambient authorization/cross-organization rights.
- RFC-0005 prevents execution context, parent/child execution or technical capability from broadening Organization scope or Organizational Authority.
- RFC-0006 subjects logs, telemetry and observability to RFC-0003 tenant isolation and minimization constraints.
- RFC-0007 denies cross-organization Memory/Knowledge reuse by default and keeps caches/vector indexes non-canonical and scoped.
- RFC-0008 propagates Organization/classification/purpose/rights/retention constraints to documents, artifacts and derived representations.

No Constitution amendment, RFC amendment, ADR, lifecycle transition or stable/public surface is required merely to record this non-activation disposition.

## 3. Evidence inspected

The review re-used existing canonical evidence instead of creating duplicate task-local security machinery:

- `P8-02-identity-trust-rights-data-governance-boundary.md` — one-Organization deny-by-default boundary;
- `P8-03-EIS-EXTERNAL-AUTHORITY-REVALIDATION-CONTRACT.md` — explicitly denies second-Organization/customer use in the bounded EIS contour;
- `P8-04-eis-authoritative-system-live-validation.md` — real owner-operated execution bound to the existing Organization;
- `P8-05-external-event-duplicate-replay-uncertainty-reconciliation.md` — no transport/event/replay path creates authority or transfer;
- `P8-06-external-product-extension-onboarding-governed-dependency-resolution.md` — source/contract/request Organization mismatch fails closed and Product Contract presence grants no access;
- `R26-cross-organization-security-integration-health-review.md` — current one-Organization contour has no demonstrated cross-Organization bypass but explicitly leaves realistic two-Organization storage/query/index/cache/log/admin/import validation to P8.08;
- `P8-07-portability-export-migration-customer-handover-interoperability-proof.md` — customer/cross-Organization transfer remains `NOT ACTIVATED` and cannot be synthesized from caller-provided recipient/grant strings;
- repository reference tests and the P8.07 full-CI baseline `1259 tests / OK` remain the current executable regression evidence for the existing bounded contour.

These artifacts establish useful negative/security guard evidence. They do **not** transform one-Organization operation or synthetic mismatch cases into realistic two-Organization isolation proof.

## 4. Scope-preserving security result

Within the actually activated one-Organization Phase 8 contour, the following protections remain evidenced and must remain true:

| Security property | Current evidence status |
|---|---|
| Organization scope is explicit for governed state/execution | `PASS — one Organization only` |
| unknown/unresolved Organization scope fails closed | `PASS semantically / RFC-0003 + existing guard tests` |
| Product Contract or extension presence grants no ambient access | `PASS` |
| foreign Organization mismatch is denied | `PASS semantically` |
| external source/transport/replay creates no cross-Organization authority | `PASS` |
| export/handover package creates no authority/access/credential transfer | `PASS — external transfer NOT ACTIVATED` |
| customer/cross-Organization activation can be synthesized locally | `DENIED` |
| cross-Organization Knowledge/data reuse by platform default | `DENIED` |

The following remain intentionally **not proven** because no second Organization is genuinely activated:

- same-runtime storage/read-model isolation between two Organizations;
- query/search/index/vector/embedding isolation with realistic data in both scopes;
- cache-key collision and stale cache isolation between two Organizations;
- queue/background/scheduled-work routing across two live Organization scopes;
- logs/metrics/traces/error/reporting leakage across two Organizations;
- same external identifier or email collision across two Organizations;
- admin/support/impersonation/break-glass isolation across two Organizations;
- cross-Organization import/handover under an actually authorized recipient relationship;
- revocation/termination on one Organization without effect on another;
- callback/ingress spoofing and Organization-context substitution under realistic external traffic;
- AI retrieval/model-context/derived-artifact isolation using protected data from two Organizations;
- organization-specific deletion/retention behavior when both scopes coexist.

## 5. Why no synthetic Organization B was introduced

A synthetic Organization is legitimate for unit and property tests of a mechanism. It is **not** sufficient evidence for the roadmap phrase `realistic isolation/failure-closed evidence when a second Organization is actually in scope`.

Creating a fake customer, customer rights record, Product Contract, tenancy grant or external recipient solely to close P8.08 would create one or more false implications:

- that another Organization has authorized Arvectum OS processing;
- that cross-Organization/customer rights exist;
- that persistent multi-tenant topology has actually been exercised;
- that support/admin/logging/search/background-worker boundaries were validated under real coexistence;
- that the resulting proof supports Production, external-customer, stable-contract or commercial claims.

P8.08 therefore records non-activation rather than manufacturing governance or evidence.

## 6. Re-entry trigger and minimum future proof

P8.08 realistic validation becomes eligible for a fresh governed execution only when canonical state identifies a genuine second Organization in scope through an applicable owner-approved/product/customer/legal/contractual basis.

Before execution, the future proof must establish at least:

1. unambiguous Organization ↔ tenant mapping for both Organizations;
2. actual permitted data classes/purpose/rights and accountable authority for each scope;
3. explicit Product Contract/integration boundary where platform reliance applies;
4. attributable human/service/AI actors and least-privilege grants per Organization;
5. test data/evidence that may lawfully coexist in the validation environment;
6. storage/read path, search/index/cache, background-work, observability and admin/support boundaries relevant to the selected runtime;
7. deny-by-default behavior for same-identifier collision, Organization substitution, foreign-resource access and missing scope;
8. cross-Organization transfer only when explicitly governed, with revocation/termination behavior;
9. derived-data/AI-context/Document/Knowledge propagation controls where those surfaces are exercised;
10. fail-closed dependency/policy/tenant-resolution failure;
11. regression and evidence sufficient to reconstruct allowed and denied operations without retaining unnecessary sensitive payload;
12. exact non-claims for untested topologies or channels.

A future proof may use synthetic adversarial requests **inside** that genuine two-Organization contour, but the sovereignty scopes themselves must not be fabricated for sequencing.

## 7. Functional cross-review

Functional review completed in three iterations of the maximum seven.

### Iteration 1 — scope and claim integrity

Result: `REVISE`.

Material objection:

> Unit tests can create `Organization A` and `Organization B`, so the task could be marked `PASS` immediately.

Disposition:

Rejected. Such fixtures prove local guard semantics only. They do not satisfy the roadmap's explicit condition that a second Organization be actually in scope and would overstate realistic isolation evidence.

Revision:

- classify the current result as `Complete / NOT ACTIVATED`;
- preserve synthetic/mismatch tests only as bounded semantic evidence;
- keep realistic multi-Organization conformance unclaimed.

### Iteration 2 — security completeness and re-entry

Result: `REVISE`.

Material objection:

> A simple `blocked` status could hide which surfaces remain unvalidated and could allow the issue to disappear from later closure review.

Revision:

- enumerate the unproven two-Organization surfaces explicitly;
- define a concrete re-entry trigger and minimum future proof matrix;
- require M8 closure to carry the limitation forward unless fresh two-Organization evidence exists by then.

### Iteration 3 — architecture/governance proportionality

Result: `PASS`.

Checks:

- no new tenancy topology, IAM provider, datastore partitioning, policy engine, cache/index technology, broker or support-access architecture is selected prematurely;
- no ADR is required merely for non-activation;
- no Product Contract or Platform Capability lifecycle changes;
- no synthetic customer, rights record or governance approval is created;
- no security invariant is weakened;
- no duplicate harness is added solely to repeat already proven one-Organization negative checks;
- next-phase work can proceed while the exact multi-Organization non-claim remains visible.

No material functional objection remains for the `NOT ACTIVATED` disposition.

Functional review is not formal conformance approval, operational-readiness approval, customer authorization or lifecycle promotion.

## 8. Result and non-claims

`P8.08 = Complete / NOT ACTIVATED` means only:

- the canonical activation state was revalidated;
- no genuine second Organization is currently in scope;
- the task did not fabricate one;
- existing cross-Organization denial/failure-closed guards remain the bounded evidence available today;
- realistic two-Organization validation is explicitly deferred until the re-entry trigger is satisfied;
- the unproven claim is preserved for M8 closure and any future conformance/commercial review.

It does **not** mean:

- multi-tenant isolation is proven;
- external customer Production is ready;
- customer data coexistence has been tested;
- cross-Organization sharing is authorized;
- a multi-tenant persistence/IAM/deployment architecture has been selected;
- a Stable Product Contract exists;
- any Platform Capability is `Active`;
- any public/stable API, tenant model or export/import surface exists;
- full RFC-0003 or full-platform conformance is claimed;
- any SLA/support/certification/commercial commitment is created.

## 9. Next canonical action

After canonical review/roadmap synchronization, Phase 8 may proceed to:

> `P8.09 — External operator/developer integration experience + documentation`.

P8.09 must not reinterpret this disposition as multi-Organization security proof. R27/P8.10/P8.12 must preserve the `NOT PROVEN` two-Organization limitation unless a fresh governed re-entry of P8.08 later produces actual evidence.