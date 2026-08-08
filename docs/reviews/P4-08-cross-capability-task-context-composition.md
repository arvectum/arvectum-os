# P4.08 — Cross-capability task/context composition + bounded product entry point review

Status: `Implementation PASS / canonical completion blocked by CI infrastructure`
Date: `2026-08-08`
Task classification: `product_contract`
Owner: `ООО «Арвектум»`
Roadmap item: `P4.08 — Cross-capability task/context composition + bounded product entry point`
PR: `#53`

## 1. Canonical basis checked

This review was performed against the canonical repository state rather than chat memory.

Checked normative basis:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `1.0.0` — `Accepted`;
- RFC-0004 `Product Contract, Product Experiment and Extension Model` `1.0.0` — `Accepted`;
- RFC-0005 `Governed Execution and Workflow Model` `1.0.0` — `Accepted`;
- RFC-0006 `Event, Provenance and Observability Model` `1.0.0` — `Accepted`;
- RFC-0007 `Memory, Knowledge and Governed Learning Lifecycle` `1.0.0` — `Accepted`;
- RFC-0008 `Document and Artifact Architecture` `1.0.0` — `Accepted`;
- RFC Index — current Accepted set confirmed;
- ADR Index — no applicable Accepted ADR requires or authorizes a durable frontend/API/service/storage/IAM technology choice for this bounded slice;
- P3.08 Product Contract consumption boundary and its Provisional capability-consumption baseline;
- P4.02 shared workspace shell;
- P4.06 Document / Artifact workspace experience;
- P4.07 Memory / Knowledge / Search discovery experience;
- R10 Operator Safety / Cross-Capability Health Review and `operator_safety.py` guard.

No conflict with the Constitution or Accepted RFC was found. No Constitution amendment, Accepted RFC modification, new RFC, ADR, capability lifecycle promotion, Stable Product Contract or public compatibility commitment is required for this bounded internal implementation.

## 2. Scope implemented

P4.08 introduces one synthetic bounded product reference outside the shared platform package and uses it to prove a Product Contract-backed product entry into the existing workspace.

Implementation artifacts:

- `reference/python/bounded_product_ref/__init__.py`;
- `reference/python/bounded_product_ref/contract.py`;
- `reference/python/bounded_product_ref/task_composition.py`;
- `reference/python/examples/p4_08_bounded_product_entry_demo.py`;
- `reference/python/tests/test_p4_08_bounded_product_composition.py`;
- `reference/python/tests/test_p4_08_bounded_product_demo.py`;
- `reference/python/tests/test_p4_08_positive_paths.py`;
- `docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md`.

The product reference deliberately lives outside `arvectum_os_ref`. Shared platform code does not import it.

## 3. Provisional Product Contract-backed entry

The bounded product uses an executable RFC-0004 `Provisional` Product Contract, version `0.1.0`.

The contract declares exactly the dependencies needed by this proof:

- CAP-001 `Document & Artifact Governance`, Provisional contract baseline `1.0.0`, operation `p3.08.resolve-document`;
- CAP-002 `Memory & Knowledge Governance`, Provisional contract baseline `1.0.0`, operation `p3.08.retrieve-knowledge`;
- the bounded internal Governed Runtime contract for product-owned task-state mutation, operation `p4.08.record-task-decision`.

Workspace entry requires:

1. explicit current Organization and attributable Actor context;
2. exact Product identity and Product version equality with the Product Contract;
3. an exact `Provisional` Product Contract;
4. at least two distinct admitted shared capability dependencies;
5. explicit capability-consumption requests carrying the current Actor/Organization/purpose/right/classification access context.

The exact Product Contract Version Identity is carried into `WorkspaceProductContext`. Contract admission is context and boundary evidence only; it is not authorization, Organizational Authority or approval.

## 4. Cross-capability task/context composition

The product-owned task composes the existing shared semantic owners rather than reimplementing them.

The bounded flow:

1. enters the shared workspace with exact Organization/Product/Product Contract context;
2. navigates to the P4.06 Documents surface for the task's governed Document subject;
3. invokes the existing P4.06 inspection boundary with current source authorization and CAP-001 handling constraints;
4. navigates to the P4.07 Knowledge surface;
5. invokes the existing P4.07 retrieval/presentation boundary with current source authorization and CAP-002 constraints;
6. returns one product-owned transient task context containing those two non-authoritative shared views plus the exact Product Contract Version Identity;
7. returns product-specific task disposition/notes to the product boundary rather than adding them to the shared platform model.

The positive-path fitness fixture constructs a real admitted governed Document/Artifact and validated Knowledge object and supplies current source authorization for each. Expected product context therefore contains actual P4.06 `DocumentWorkspaceInspection` and P4.07 `KnowledgeWorkspaceView` results with exact governed Version identities.

A separate negative path proves that Product Contract entry by itself exposes no protected Document source when current source authorization is absent.

## 5. Product/platform boundary result

Product-owned semantics include:

- bounded task identity and title;
- task-specific composition intent;
- dispositions `Needs review`, `Ready to proceed` and `Declined`;
- product decision notes;
- product-owned task Canonical Record semantic type `product.bounded-review-task` when the product elects to govern that state.

These semantics are not imported into the shared platform package and are not declared as a Platform Capability.

Shared platform ownership remains limited to the existing domain-neutral boundaries for:

- Organization / Actor workspace context;
- Product Contract validation;
- CAP-001 and CAP-002 semantics;
- Canonical Record / exact-version / authority / provenance semantics;
- Governed Execution;
- R10 operator safety.

The shared workspace therefore remains navigation/presentation infrastructure rather than a generic product orchestrator.

## 6. Exact version, authority and provenance continuity

The composition preserves:

- logical Subject identity versus exact immutable Version identity;
- canonical versus transient/derived presentation state;
- authority mode and authority scope;
- governed source provenance;
- Document Version and Artifact identity where material;
- exact Knowledge Version and freshness semantics where material;
- exact Product Contract Version identity across product entry and governed execution.

A material cross-review finding was identified during implementation: the initial product action wrapper delegated to R10 without first proving that the supplied `GovernedExecutionContext` was pinned to the same exact Product Contract Version used by the product workspace entry.

That gap was remediated before review completion. P4.08 now adds a product-boundary continuity check before R10 action preparation and execution. A mismatched or absent execution Product Contract pin fails closed before the R10 guard is invoked.

This check does not replace R10. Product Contract continuity and current source-authorization freshness remain separate invariants.

## 7. Security, rights, minimization and authority result

The Product Contract declares bounded canonical access but grants none by itself.

Read-side capability operations preserve independent `Authorization` and `DataGovernance` boundaries. Actual P4.06/P4.07 surfaces continue to enforce current source authorization and purpose/right/classification constraints before protected source material is presented or relied upon.

The product task-state mutation declaration requires all of:

- `Authorization`;
- `OrganizationalAuthority`;
- `DataGovernance`;
- `ConsequentialApproval`.

Successful Product Contract validation satisfies none of those gates.

The implementation also rejects Actor/Organization/Product scope drift across the composed requests. Product context remains non-authoritative presentation state, and product decisions are transient unless separately admitted through governed state-transition semantics.

## 8. Consequential operator action boundary

P4.08 does not create a new mutation path.

Consequential product operator work is composed in this order:

1. exact Product Contract continuity between Product workspace entry and Governed Execution is checked at the product boundary;
2. R10 `prepare_operator_canonical_mutation_action` validates that the exact source-authorization decision used for inspection is still the unique current allow decision;
3. the existing P4.05/runtime path prepares the action only through R10 delegation;
4. immediately before execution, Product Contract continuity is checked again from the prepared action intent;
5. R10 rechecks current source-authorization freshness before delegating to the existing P4.05 commit path.

Replacement, revocation, absence or ambiguity of the source-access decision therefore requires re-inspection. Product Contract presence cannot substitute for this R10 check, and R10 cannot substitute for Product Contract or Governed Execution gates.

Structural fitness tests also assert that the product package does not import the lower-level P4.05 action adapter directly.

## 9. Functional cross-review

Five functional cross-review iterations were completed against the branch implementation.

### Iteration 1 — architecture / product-platform boundary

Checked package direction, domain ownership, shared-workspace scope, Product Contract status and capability lifecycle claims.

Result: `PASS`.

### Iteration 2 — capability composition / exact source semantics

Checked real CAP-001 + CAP-002 composition, source authorization, Document/Artifact exactness, Knowledge exact-version semantics, non-authoritative presentation and exact Product Contract attribution.

Result: `PASS` at implementation-review level; executable tests are committed but the repository CI runner has not executed them due the infrastructure condition recorded in section 10.

### Iteration 3 — security / Organization / authority separation

Checked current Actor/Organization binding, Product identity/version binding, purpose/right/classification context, Contract-not-authorization semantics and independent mutation gates.

Result: `PASS`.

### Iteration 4 — consequential action composition

Finding:

- the initial wrapper did not explicitly prove exact Product Contract Version continuity between the workspace entry and the supplied Governed Execution before delegating to R10.

Remediation:

- added exact Product Contract continuity checks for both preparation and execution paths;
- preserved R10 as the sole product-facing bridge to the existing P4.05 consequential action adapter;
- kept Product Contract continuity and source-access freshness as separate fail-closed invariants.

Result after code and fitness-test update: `PASS` at implementation-review level.

### Iteration 5 — accidental contract / technology / commercial / lifecycle review

Checked for stable API/route/wire contracts, durable frontend/BFF/service topology, storage/search/IAM technology choice, platform imports of product code, capability promotion, Production/readiness claims and support/SLA promises.

Result: `PASS`; no material architectural finding remains in the bounded P4.08 implementation.

## 10. Executable evidence and CI infrastructure condition

Executable evidence is committed on PR `#53`:

- cross-capability positive/negative fitness tests;
- Product Contract boundary tests;
- Product Contract exact-version continuity checks;
- R10-only consequential action delegation checks;
- package-direction / no-private-P4.05-bypass checks;
- a static Product Contract-backed workspace-entry demo.

However, no green GitHub Actions execution is claimed.

`Reference Python CI` runs created for this PR repeatedly failed before executing the first workflow step. The GitHub Actions API returned jobs with an empty step list, and job-log retrieval returned no usable test log (`BlobNotFound`). A manual rerun of the latest unchanged implementation head reproduced the same zero-step failure.

Observed affected PR runs include `#171`, `#173`, `#174` and `#176`. Because no `checkout`, Python setup or `unittest` step executed, these runs provide neither a test failure signal nor a passing test signal.

The workflow definition itself remains the existing bounded reference workflow (`ubuntu-latest`, Python `3.12`, `python -m unittest discover -s tests -v`). No workflow change is included in P4.08.

Therefore:

- implementation cross-review result: `PASS`;
- automated test execution result: `NOT ESTABLISHED`;
- canonical completion/merge gate: `BLOCKED` until the full reference suite actually executes successfully on the P4.08 head or an equivalent owner-approved execution environment produces trustworthy full-suite evidence.

The repository roadmap MUST NOT be advanced to R11 on the basis of these zero-step workflow failures.

## 11. ADR / architecture disposition

No ADR threshold was crossed.

Still deliberately unselected:

- frontend framework or durable design-system package boundary;
- public REST/GraphQL/gRPC/BFF/wire contract;
- durable workspace/read-model/cache storage;
- document/object-store topology;
- search/vector/RAG technology;
- IAM/PDP/PEP implementation;
- Event transport/store;
- workflow engine;
- separately deployable product/platform service topology.

Material reliance on any such durable or externally constraining choice reopens the applicable ADR gate.

## 12. Capability, contract and conformance disposition

P4.08 implementation does **not**:

- promote CAP-001 or CAP-002 to `Active`;
- promote the Product Contract from `Provisional` to `Stable`;
- create a new Platform Capability from the product task/composition mechanism;
- claim Production operational readiness;
- claim full-platform conformance;
- create a public API/SDK/support/SLA/compatibility commitment.

The bounded Product Contract remains `Provisional`; the shared capabilities remain `Incubating / Provisional`.

## 13. Completion decision

The bounded P4.08 implementation is architecturally complete and passes the documented functional cross-review.

Canonical work-item completion is **not yet recorded** because trustworthy full reference test execution is currently absent for the implementation head. PR `#53` remains the bounded implementation vehicle, and the canonical roadmap remains on P4.08 until that execution evidence is obtained.

Once the full reference suite executes successfully on the current implementation (or a later reviewed P4.08 head), the remaining closure actions are mechanical:

1. update this review with exact CI run / Python version / test count / result;
2. mark `P4.08` complete in the Phase 4 roadmap;
3. advance the canonical current action to `R11 — Composition / Usability Refactoring Review`;
4. synchronize root roadmap/README evidence;
5. obtain final synchronized-head CI before merge.
