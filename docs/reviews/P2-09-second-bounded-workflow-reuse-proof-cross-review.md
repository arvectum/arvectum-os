# P2.09 Functional Cross-Review — Second Bounded Workflow Reuse Proof

Status: `Complete`
Date: `2026-08-08`
Task classification: `platform`
Constitution: `1.2.0`
Relevant Accepted RFCs: `RFC-0001`, `RFC-0002`, `RFC-0003`, `RFC-0004`, `RFC-0005`, `RFC-0006`
Roadmap item: `P2.09`
Pull request: `#28`

## Scope

Review the bounded P2.09 reuse proof for architectural validity, material workflow distinctness, exact-version and authority preservation, product/platform-boundary safety, absence of cloned P1 orchestration, engineering proportionality and ADR-gate impact.

This review is an execution-quality artifact. It is not formal RFC/ADR acceptance, capability activation, production-readiness approval or conformance certification.

## Evidence reviewed

- `reference/python/tests/test_p2_09_second_workflow_reuse.py`;
- P2.02 Canonical Head / Effective Version runtime;
- P2.03 Typed Relationship runtime;
- P2.04 Governed Execution and gate runtime;
- P2.05 Event admission/provenance runtime as exercised through P2.06 canonical commit;
- P2.06 consistency/idempotency/external-consequence runtime;
- P2.07 Product Contract runtime boundary;
- existing P1 scenario/composition boundaries for duplicate-orchestration comparison;
- GitHub Actions `Reference Python CI` run `#56` on executable code head `403e6385091fdb94ff0c6ca59df80b311afdd594`: `Ran 289 tests in 0.359s` / `OK`.

## Review

### Architecture and reuse

Pass. Both workflow configurations enter through the same P2.07 Product Contract boundary and the same P2.04 Governed Execution lifecycle/gate operations. The proof contains one shared `_run_interaction` orchestration helper for the two bounded scenarios; it does not import `reference_scenario`, `reference_runtime_adapters` or the historical P2.01 `RuntimeComposition` path.

The first workflow is a direct `CanonicalMutation` over one exact current canonical version and produces an immutable successor plus canonical Event through P2.06/P2.05 semantics. The second workflow resolves an Effective Version that intentionally differs from a future-effective Canonical Head, follows a Typed Relationship whose source endpoint is explicitly `VersionIdentity`, pins the exact resolved record/context/relationship versions into Governed Execution, and exercises `ExternalMutation` plus `Commitment` consistency semantics.

The difference is therefore material across version-resolution, relationship, gate and effect paths rather than a renamed copy of the P1 canonical-mutation route.

### Exact-version and governance invariants

Pass. Both workflows pin exact Product Contract, Workflow and material-input Version Identities. The second workflow proves that consequential reliance remains on the resolved Effective Version rather than silently following the future-effective Head. Relationship existence continues to grant neither Authorization nor Organizational Authority; the external workflow separately requires Actor Assurance, Authorization, Data Governance and Consequential Approval.

The canonical workflow separately requires Authorization, Organizational Authority, Data Governance and Validation. Product Contract validation does not satisfy those runtime gates.

### Consequential effects and consistency

Pass. The canonical path commits one successor and one canonical Event and treats an exact keyed retry as a duplicate rather than repeating publication. The external path records bounded external-consequence outcome evidence without publishing a canonical successor or Event, and an exact keyed retry is likewise suppressed as a duplicate semantic invocation.

No test helper performs an external effect; P2.06 remains an outcome/idempotency semantic boundary rather than an external connector or transaction mechanism.

### Product/platform and security boundaries

Pass for the declared scope. Both synthetic consumers use explicit Provisional Product Contracts with declared dependency version, operation, canonical Read/Write scope and failure behavior. The fixtures remain domain-neutral and single-Organization. No product-domain rule is moved into shared runtime behavior.

No Identity, Product Contract, Workflow or Relationship is treated as a permission/authority grant. Existing Organization-scoping and gate admission remain the enforcement-relevant runtime boundaries exercised by the proof.

### Engineering proportionality and R3 input

Pass with one bounded refactoring input: the P2.09 evidence fixture is intentionally verbose because it constructs two complete workflow configurations and their governed test data. That fixture-local setup is not promoted into a new platform abstraction in P2.09. The mandatory `R3 — Reuse Refactoring Review` is the correct next checkpoint to decide, using this now-observed duplication pressure, which fixture/configuration factories or runtime composition seams should be simplified or extracted.

Refactoring those shapes before the second-workflow evidence existed would have been speculative; leaving the evidence fixture permanently unreviewed would also be inappropriate. P2.09 therefore records this as explicit R3 input rather than either prematurely standardizing it or ignoring it.

### ADR gate

Pass. No durable datastore, transaction/concurrency implementation, Event delivery mechanism, IAM/policy provider, public API/SDK, stable cross-product serialization/interface, external connector implementation, service topology or durable projection/replay mechanism is selected by this proof.

The new code is test/evidence composition over already bounded internal/provisional runtime seams. No current ADR gate is crossed and no Accepted RFC is modified.

## Result

`Pass` for the declared bounded P2.09 scope.

The M2 second-workflow reuse claim is now executable: two materially distinct domain-neutral workflows reuse the same Core Runtime semantic boundaries and pass shared fitness evidence without cloning the P1 orchestration path.

The next mandatory action is `R3 — Reuse Refactoring Review`, using this proof and its fixture/configuration duplication pressure as evidence. P2.09 itself does not claim that R3, P2.10, M2 closure, production readiness or Platform Capability activation is complete.

## Explicit non-claims

P2.09 completion does not establish:

- completion of `R3`, `P2.10`, `P2.11`, `P2.12` or milestone `M2`;
- a stable public runtime composition API or Product Contract schema;
- durable transaction, Event-delivery, external-effect or replay infrastructure;
- production readiness, SLA/support commitments or full RFC conformance;
- an `Active` Platform Capability.
