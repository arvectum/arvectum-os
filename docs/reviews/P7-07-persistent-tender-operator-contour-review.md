# P7.07 — Persistent Tender Operator operational contour — functional cross-review

Date: `2026-08-19`
Review type: functional cross-review; not formal RFC/ADR acceptance or lifecycle promotion
Task classification: `product_contract` with `platform` and `product_specific`
Constitution: `1.2.0 Ratified`
Product Contract: P6.02 `Provisional 0.1.0`

## Authority checked

Checked before and during review:

- Constitution `1.2.0`;
- RFC Index;
- RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0008 — all `Accepted 1.0.0`;
- no task-relevant Accepted ADR exists;
- P6.02 Product Contract `0.1.0`;
- P7.02 persistent runtime/restart semantics;
- P7.03 durable governed state boundary;
- P7.04 persistent least-privilege access;
- P7.06-UI1 real governed item bridge;
- product-owned `arvectum/tender-agent` `ArvectumOSBridge` and its P6.03 tests;
- canonical Phase 7 roadmap and detailed P7.07 closure criteria.

No higher-authority conflict was found.

## Iteration 1

### Product Contract / product-platform boundary

Result: `PASS`

The design keeps exact P6.02 `0.1.0`. CAP-001 admission/read and CAP-004 reconstruction are already declared by the Product Contract. P7.07 operationalizes that reliance rather than inventing a new platform dependency.

Tender Operator does not directly depend on P7.03 filesystem state. Rehydration is platform-internal; the product crosses the declared seam through its own `ArvectumOSBridge` and CAP-001.

### External authority

Result: `PASS`

The admitted operational Document remains `External Reference`; `ЕИС / zakupki.gov.ru` remains authoritative. No new EIS/SOAP retrieval or mutation is part of setup/consume/restart.

### Governed Execution / authority separation

Result: `PASS`

The one-time admission uses four distinct RFC-0005 decisions: Authorization, Organizational Authority, Data Governance and Consequential Approval. P7.04 access is explicitly treated only as technical Authorization and never as Organizational Authority or Consequential Approval.

### Persisted semantics / restart rehydration

Result: `PASS WITH HARDENING`

A distinct P7.07 exact Version is justified because the earlier UI1 item was intentionally minimized for UI inspection and its Artifact purpose was `prebid-evidence-admission`, while Tender Operator CAP-001 consumption requires `prebid-review`. Silent repurposing would fail exact handling enforcement and blur provenance.

The new representation retains only the domain-neutral CAP-001 state needed to rehydrate the exact admitted Document Version. It does not store raw tender bytes, credentials or product decision state.

### Finding F1 — temporary setup-grant cleanup

Severity: `Material`

The first low-level implementation attempted to revoke its temporary setup grant in `finally`, but a revoke failure occurring while another exception was already propagating could leave the consequential setup privilege active while surfacing only the original failure path.

Disposition: `FIXED`

A supported guarded operator entrypoint now snapshots exact setup/read privileges, refuses ambiguous stale setup privilege, and performs a second security-first cleanup layer. On failed setup it revokes any newly-created exact setup grant and any newly-created P7.07 item-scoped read grant. Cleanup failure itself fails closed.

The low-level semantic module remains private implementation; operator procedures use the guarded entrypoint.

### Finding F2 — dynamic product bridge execution

Severity: `Material`

The first low-level implementation loaded `ArvectumOSBridge` from the supplied product repository after only path/symlink checks. Although the selected-Mac proof also requires canonical clean `arvectum/tender-agent`, a future modified bridge could execute top-level behavior before CAP-001 delegation and make the contour's no-external-effect claim too broad.

Disposition: `FIXED`

The guarded entrypoint parses the bridge source before import and permits only the bounded current module/import/class shape. `resolve_document` must remain one pure keyword-for-keyword return to `self.adapters.capabilities.resolve_document(...)`. Executable top-level behavior, imports outside the bounded seam, extra statements or argument rewriting fail closed.

The selected-Mac closure launcher applies this validation immediately before each product bridge load.

This is intentionally private operational validation, not a Stable source-code ABI.

## Iteration 2

### Least privilege after hardening

Result: `PASS`

The supported setup path has no standing setup grant after success. Failed setup rolls back newly-created P7.07 privileges. Ordinary operation retains only an exact item-scoped local `p3.08.resolve-document` read grant.

### Product execution safety after hardening

Result: `PASS`

The supported consume path validates the actual product-owned bridge before execution and then relies on the existing IntegrationAdapters/CAP-001 enforcement. Procurement-domain logic remains product-owned.

### Restart semantics

Result: `PASS AT REPOSITORY LEVEL / RUNTIME PROOF PENDING`

The selected-Mac proof is designed against existing P7.02 supervised restart semantics and requires instance replacement, generation advance, `previous_instance_id` continuity, byte-stable P7.03 state and the same exact product reliance after restart.

This cannot be considered runtime evidence until executed on the selected Mac against the merged exact release and real product checkout.

### Public/stable boundary / ADR gate

Result: `PASS`

No ADR is required for the current bounded shape because persistence, rehydration, AST guard and operator CLI are private, owner-local, reversible and non-public. The ADR gate must be reopened if any of them becomes cross-product, external or stable contractual surface.

## Remaining objections

Repository design/code review: `No material objection remaining after Iteration 2`.

Operational closure objection: `OPEN` — selected-Mac guarded before/after-restart proof has not yet produced evidence for the merged exact release.

## Review conclusion

`P7.07 repository implementation: PASS subject to CI.`

`P7.07 milestone completion: NOT YET — selected-Mac operational evidence required.`

This review is functional evidence only. It is not Product Contract promotion, capability promotion, ADR acceptance, operational-production approval or broader Arvectum OS conformance approval.