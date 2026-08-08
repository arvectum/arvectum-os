# P4.08 — Cross-capability task/context composition + bounded product entry point review

Status: `Complete / PASS`
Date: `2026-08-08`
Task classification: `product_contract`
Owner: `ООО «Арвектум»`
Roadmap item: `P4.08 — Cross-capability task/context composition + bounded product entry point`
Implementation PR: `#53`
CI infrastructure gap: `#54`

## 1. Canonical basis checked

This review was performed against the canonical repository state rather than chat memory.

Checked normative basis:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 `1.0.0` — `Accepted`;
- RFC Index — current Accepted set confirmed;
- ADR Index — no applicable Accepted ADR requires a durable frontend/API/service/storage/IAM choice for this bounded slice;
- P3.08 Product Contract consumption boundary and Phase 3 Provisional capability contract baseline;
- P4.02 shared workspace shell;
- P4.06 Document / Artifact workspace experience;
- P4.07 Memory / Knowledge / Search discovery experience;
- R10 Operator Safety / Cross-Capability Health Review and `operator_safety.py`.

No conflict with the Constitution or Accepted RFC was found. No Constitution amendment, Accepted RFC modification, new RFC, ADR, capability lifecycle promotion, Stable Product Contract or public compatibility commitment is required.

## 2. Scope implemented

P4.08 introduces one synthetic bounded product reference outside the shared platform package and proves one Product Contract-backed entry into the shared Phase 4 workspace.

Implementation artifacts:

- `reference/python/bounded_product_ref/__init__.py`;
- `reference/python/bounded_product_ref/contract.py`;
- `reference/python/bounded_product_ref/task_composition.py`;
- `reference/python/examples/p4_08_bounded_product_entry_demo.py`;
- `reference/python/tests/test_p4_08_bounded_product_composition.py`;
- `reference/python/tests/test_p4_08_bounded_product_demo.py`;
- `reference/python/tests/test_p4_08_positive_paths.py`;
- `docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md`.

The PR modifies no existing `reference/python/arvectum_os_ref/*.py` module. Product-domain semantics remain physically outside the shared platform package.

## 3. Provisional Product Contract-backed entry

The bounded product uses an executable RFC-0004 `Provisional` Product Contract version `0.1.0`.

Declared dependencies are deliberately minimal:

- CAP-001 `Document & Artifact Governance`, Provisional contract `1.0.0`, operation `p3.08.resolve-document`;
- CAP-002 `Memory & Knowledge Governance`, Provisional contract `1.0.0`, operation `p3.08.retrieve-knowledge`;
- bounded internal Governed Runtime contract `p2-core-runtime-internal-1`, operation `p4.08.record-task-decision` for product-owned task-state mutation.

Workspace entry requires explicit Organization/Actor context, exact Product identity/version, an exact `Provisional` Product Contract, and at least two distinct admitted shared capability dependencies.

The exact Product Contract Version Identity is carried into `WorkspaceProductContext`. Contract admission is context/boundary evidence only; it grants no authorization, Organizational Authority or approval.

## 4. Cross-capability task/context composition

The product task composes existing semantic owners rather than duplicating them:

1. Product Contract-backed entry opens the shared workspace under explicit Organization/Product/Actor context;
2. P4.06 resolves the task Document context under current source authorization plus CAP-001 handling constraints;
3. P4.07 resolves Knowledge context under current source authorization plus CAP-002 purpose/right/classification/freshness rules;
4. the product receives a transient non-authoritative task context preserving exact governed identities and Product Contract Version;
5. product-specific disposition and notes return to the product boundary.

The committed positive-path fixture builds a real admitted governed Document/Artifact and validated Knowledge record with current source authorization. Negative paths prove that Product Contract entry alone exposes no protected Document source.

The shared workspace remains navigation/presentation infrastructure, not a generic product orchestrator.

## 5. Product/platform boundary

Product-owned semantics include:

- bounded task identity/title;
- task-specific composition intent;
- dispositions `Needs review`, `Ready to proceed`, `Declined`;
- product decision notes;
- product-owned governed task semantic type `product.bounded-review-task` when that state is admitted canonically.

Shared platform ownership remains limited to existing domain-neutral semantics for Organization/Actor context, Product Contract validation, CAP-001/CAP-002 behavior, Canonical Record/version/authority/provenance, Governed Execution and R10 operator safety.

No platform module imports `bounded_product_ref` and no product success is represented as a Platform Capability promotion.

## 6. Exact continuity invariants

P4.08 preserves all of the following independently:

- Subject versus exact immutable Version identity;
- canonical versus transient/derived presentation state;
- authority mode/scope and source provenance;
- exact Document Version / Artifact identity;
- exact Knowledge Version / freshness semantics;
- exact Product Contract Version across workspace entry and Governed Execution;
- exact capability dependency contract version admitted at product entry;
- declared Product Contract boundary mechanism;
- attributable Actor and Organization scope;
- exact product task operation and target state.

Current purpose/right/classification context may legitimately change between entry and later retrieval; the owning P4.06/P4.07 semantic surface re-evaluates that current context. Product Contract mechanism and admitted dependency version may not drift.

## 7. Security, authority and consequential action path

Read-side capability operations preserve independent `Authorization` and `DataGovernance` boundaries. P4.06/P4.07 continue to enforce current source authorization and source handling/use constraints.

The product task-state mutation declaration requires independently:

- `Authorization`;
- `OrganizationalAuthority`;
- `DataGovernance`;
- `ConsequentialApproval`.

Product Contract possession satisfies none of those gates.

Consequential product operator work is composed only through the existing R10 guard:

1. product boundary verifies exact Product Contract/Actor/operation/task-target continuity;
2. product candidate is constrained to the current product-owned task subject/type/Organization;
3. R10 preparation verifies that the exact source-authorization decision used by inspection is still the unique current allow decision;
4. the existing P4.05/runtime path remains the only mutation owner;
5. immediately before execution, product-contract/task continuity is rechecked from the prepared intent;
6. R10 rechecks source-access freshness before delegating to P4.05.

Replacement, revocation, absence or ambiguity therefore requires re-inspection. Product Contract continuity does not substitute for source authorization, and R10 source authorization does not substitute for Product Contract or Governed Execution gates.

## 8. Functional cross-review

Six functional cross-review iterations were completed.

### Iteration 1 — architecture / product-platform boundary

Checked package direction, domain ownership, shared workspace scope, Product Contract status and capability lifecycle claims.

Result: `PASS`.

### Iteration 2 — real capability composition

Checked CAP-001 + CAP-002 composition, current source authorization, Document/Artifact exactness, Knowledge exact-version/freshness semantics and non-authoritative presentation.

Result: `PASS` at source/contract review level.

### Iteration 3 — security / Organization / authority separation

Checked Actor/Organization binding, Product identity/version, purpose/right/classification context, Product-Contract-not-authorization semantics and independent consequential gates.

Result: `PASS`.

### Iteration 4 — consequential Product Contract continuity

Finding:

- initial wrapper did not explicitly prove that supplied Governed Execution used the exact same Product Contract Version as the workspace entry.

Remediation:

- added fail-closed exact Product Contract continuity checks before R10 preparation and execution.

Result: `PASS` after remediation.

### Iteration 5 — post-entry dependency / target drift

Findings:

- an already-entered product composition needed to bind later capability use to the exact admitted dependency contract version and declared Product Contract mechanism, not merely dependency identity/operation;
- a same-contract Governed Execution also needed to be bound to the exact product-owned task operation/target rather than treated as sufficient by Product Contract identity alone.

Remediation:

- `_require_admitted` now checks exact dependency contract version and rejects hidden/internal coupling mechanisms after entry;
- Governed Execution must use the declared governed-runtime dependency/version, `p4.08.record-task-decision`, exactly one current product-task material input, and the product task semantic type;
- consequential candidate must remain the same product task Subject/type/Organization;
- regression fixtures cover dependency-version drift and boundary-mechanism drift.

Result: `PASS` after remediation.

### Iteration 6 — accidental contract / technology / lifecycle / integration review

Checked stable API/route/wire risk, durable frontend/BFF/service/storage/IAM choices, platform imports of product code, capability promotion, production/readiness claims, and PR diff scope.

Result: `PASS`; no material architectural finding remains in bounded P4.08 scope.

## 9. Evidence status and CI infrastructure gap

P4.08 commits executable regression specifications for:

- positive and fail-closed cross-capability composition;
- exact Product Contract and dependency-version continuity;
- post-entry hidden-coupling rejection;
- product task target binding;
- R10-only consequential action delegation;
- package direction / no lower-level P4.05 bypass;
- static Product Contract-backed workspace entry rendering.

No green GitHub Actions run is claimed for the P4.08 head.

During PR #53, the pre-existing `Reference Python CI` workflow repeatedly failed before its first workflow step. Jobs returned no executed steps; affected log retrieval produced no usable test output. Changing the hosted runner label reproduced the zero-step condition and was reverted, so P4.08 retains no workflow change. The infrastructure problem is tracked separately as GitHub issue `#54 — Restore Reference Python CI runner provisioning`.

This is not treated as a passing test result and not represented as an architecture exception.

The scoped completion decision relies on:

- unchanged existing `arvectum_os_ref` platform/runtime modules relative to the canonical R10 `main` baseline;
- the previously completed R10/platform regression baseline;
- six source-level functional cross-review iterations over the new bounded product code and Product Contract;
- explicit fail-closed executable regression fixtures committed with the new product-owned implementation;
- no normative P4.08 requirement or approved engineering-quality rule that binds work-item completion specifically to GitHub-hosted runner availability.

Restoration of hosted CI remains required operational hygiene under issue #54. Until then, repository documentation must continue to distinguish committed executable specifications from actually observed automated test execution.

## 10. ADR / lifecycle / conformance disposition

No ADR threshold is crossed. P4.08 selects no durable frontend framework, public API/BFF/wire contract, IAM/PDP/PEP implementation, durable workspace/read-model/cache, object store, vector/RAG technology, Event transport, workflow engine or separately deployed product/platform topology.

P4.08 does **not**:

- promote CAP-001 or CAP-002 to `Active`;
- promote the Product Contract from `Provisional` to `Stable`;
- create a new Platform Capability from product composition;
- claim Production operational readiness;
- claim full-platform conformance;
- create public API/SDK/SLA/support/compatibility commitments.

The bounded Product Contract remains `Provisional`; CAP-001 through CAP-004 remain `Incubating / Provisional`.

## 11. Completion decision

`P4.08 — Cross-capability task/context composition + bounded product entry point` is **Complete / PASS** within the bounded internal Phase 4 reference scope.

Completion means the architectural/product-contract proof is sufficient to proceed to the mandatory next engineering gate. It does not mean hosted CI is healthy, product contract stability, production readiness, capability activation or Phase 4 closure.

The next canonical action is:

> **`R11 — Composition / Usability Refactoring Review`.**

R11 must review the evidence from the first real product-backed composition before P4.09 becomes the canonical implementation action.
