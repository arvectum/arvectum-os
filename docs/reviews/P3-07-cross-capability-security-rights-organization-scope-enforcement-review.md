# P3.07 — Cross-capability Security, Rights and Organization-scope Enforcement Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P3.07 — Cross-capability security, rights and Organization-scope enforcement`
Capabilities: `CAP-001` through `CAP-004`
Lifecycle: `Incubating`
Contracts: `Provisional`
Result: **`PASS — the bounded composition slice applies one explicit current Organization/purpose/right/classification access context across CAP-001..CAP-004, denies cross-Organization access by default, preserves derived/non-authoritative boundaries and creates neither Organizational Authority nor a durable IAM/policy contract.`**

## 1. Scope

P3.07 adds bounded cross-capability enforcement evidence above the four completed Incubating capability slices. It proves composition, not a production IAM system.

The slice proves:

- no ambient/default Organization context exists;
- CAP-001 exact Document/Artifact access re-checks Organization, purpose, permitted-use right and classification;
- CAP-002 retrieval filters current governed Knowledge by the same context plus freshness;
- CAP-003 discovery and exit-to-source use the same request context, and discovery visibility still does not grant source access;
- CAP-004 reconstruction denies foreign Organization context and redacts exact evidence versions whose current purpose/right/classification constraints do not permit disclosure;
- authorization/access context remains distinct from Organizational Authority, approval and delegation;
- cross-Organization access is denied by default;
- current access decisions do not mutate historical identity, provenance or canonical evidence.

It does not define an IAM vendor, authentication protocol, PDP/PEP technology, durable entitlement store, universal role hierarchy, policy language, stable public API/serialization, production security topology or approved delegation model.

## 2. Canonical authority checked

P3.07 was evaluated against Constitution `1.2.0`, the RFC Index and Accepted RFC-0001 through RFC-0008. RFC-0003 is the direct security/rights/Organization authority; RFC-0001, RFC-0002, RFC-0004, RFC-0005, RFC-0006, RFC-0007 and RFC-0008 constrain the composed capability boundaries.

Subordinate boundaries checked:

- `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`;
- `docs/roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`;
- `docs/roadmap/ROADMAP.md`;
- P3.03 through P3.06 implementations and reviews.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was found.

## 3. Implementation disposition

Implementation: `reference/python/arvectum_os_ref/cross_capability_enforcement.py`.

`AccessRequest` is an internal immutable composition value containing attributable `ActorContext`, explicit purpose, one required permitted-use right and allowed classifications. It deliberately does not contain approval, delegation or Organizational Authority semantics.

The module composes existing capability operations rather than creating replacement canonical owners. CAP-003 remains a disposable projection; CAP-004 remains a derived read view; CAP-001/CAP-002 governed source authority remains unchanged.

## 4. Enforcement semantics

The bounded composition is fail-closed where a caller requests exact protected source/reconstruction access. A request must carry explicit Organization scope and current handling context. Organization mismatch, purpose mismatch, absent right or disallowed classification prevents protected source disclosure.

Collection-style discovery/retrieval filters ineligible resources rather than leaking their content or existence through returned result objects. Exact source access is re-evaluated separately.

This reference slice does not claim that string-valued purpose/right/classification fixtures are a stable policy model. They are bounded executable evidence for RFC-0003 semantics only.

## 5. CAP-001 through CAP-004 composition

### CAP-001

`resolve_document_for_access()` resolves only a governed Artifact in the request Organization and checks inherited Document/Artifact handling constraints before returning exact reliance metadata/content reference.

### CAP-002

`retrieve_knowledge_for_access()` returns only Organization-matching, purpose/right/classification-eligible and, by default, current Knowledge projections. Retrieval remains derived and does not validate or promote Knowledge.

### CAP-003

`search_for_access()` delegates bounded discovery to the existing CAP-003 query boundary with the same current context. `resolve_search_hit_for_access()` independently re-checks exact governed source constraints before allowing CAP-003 to exit to source state. A hit never becomes permission.

### CAP-004

`reconstruct_audit_for_access()` requires exact Organization match and converts disallowed evidence disclosure into explicit `Redacted` disposition without exposing the governed source pin. Unknown/duplicate reconstruction evidence still fails closed through CAP-004 validation.

## 6. Security and authority boundary

P3.07 preserves RFC-0003 separation:

`Identity → Authentication evidence → Authorization/access → Organizational Authority/Approval → Data Governance → Enforcement`.

This slice addresses bounded authorization/data-handling composition only. It does not infer permission from Identity, membership or relationship; does not create delegation; does not grant approval authority; and does not treat technical access as legal/contractual rights.

Cross-Organization sharing remains outside this slice unless later governed by an explicit grant/contract. No ambient same-email/same-account/same-credential access path is introduced.

## 7. Executable evidence

`reference/python/tests/test_p3_07_cross_capability_enforcement.py` adds focused tests covering:

1. CAP-001 cross-Organization and right mismatch denial;
2. CAP-001 matching-context exact access;
3. CAP-002 current governance filtering;
4. CAP-003 same-context discovery plus independent exact source access;
5. CAP-004 redaction of disallowed evidence and foreign-Organization denial;
6. absence of approval/authority/delegation surface on the access context.

These tests are P3.10 fitness evidence. They do not claim full RFC-0003 conformance or production security readiness.

## 8. Product and capability boundary

No product-domain roles, procurement semantics, taxonomies, workflows, ranking rules, compliance narratives or UX are introduced. P3.08 remains responsible for proving a bounded real product-style consumer through an RFC-0004 Provisional Product Contract.

Capability contracts remain Provisional and all four capabilities remain `Incubating`.

## 9. ADR gate assessment

**No new ADR is required for this bounded P3.07 reference slice.**

No concrete IAM provider, PDP/PEP, durable authorization store, database RLS mechanism, network isolation technology, policy language, stable API/serialization or deployable security service topology is selected.

The ADR gate must be re-opened before material reliance on any such durable cross-cutting enforcement mechanism, consistent with the Phase 3 roadmap.

## 10. R6 disposition

R6 security/composition gate: **`PASS`** for the bounded P3.07 scope.

The pass means only that current Phase 3 reference composition preserves Organization/rights/purpose/classification boundaries without authority inflation or capability-boundary leakage. It is not an `Active`, production, compliance, SLA/support or stable-interface claim.

## 11. Exit assessment

P3.07 exit conditions are satisfied for the bounded reference scope:

- one explicit access context composes across CAP-001..CAP-004;
- Organization mismatch fails closed for protected exact access;
- purpose/right/classification constraints are re-evaluated at capability boundaries;
- discovery/retrieval do not create source access or authority;
- restricted reconstruction evidence is redacted without source-pin leakage;
- authorization remains distinct from Organizational Authority and approval;
- no product-domain semantics leak into shared behavior;
- no durable IAM/policy ADR boundary is crossed;
- no capability lifecycle promotion or production/public-contract claim is made.

**Final result: `PASS — P3.07 complete for the bounded cross-capability enforcement scope.`**

## 12. Next action

Proceed to `P3.08 — Product Contract consumption boundary + bounded consumer proof`, while continuing P3.10 fitness evidence. P3.08 must use RFC-0004 Product Contract semantics and must not treat these Incubating capability contracts as permission, authority or stable public compatibility guarantees.
