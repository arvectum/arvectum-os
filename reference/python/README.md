# Bounded Arvectum OS Reference Runtime Harness

Status: `Provisional internal implementation harness — Phase 1 complete; Phase 2 through P2.09 complete; R3 complete on this branch`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001 through RFC-0008 `1.0.0`
Phase 1 closure: `P1.12 complete; M1 achieved`
Phase 2 plan: `docs/roadmap/PHASE-2-CORE-RUNTIME.md`
R3 review: `docs/reviews/R3-reuse-refactoring-review.md`

This directory contains the bounded executable reference implementation used to prove Arvectum OS architecture and the reusable Core Runtime semantics accumulated through Phase 2.

It is deliberately in-memory, domain-neutral, reversible and internal. It is **not** a supported production runtime, stable public API/SDK, durable persistence contract, Product Contract wire schema, `Active` Platform Capability, SLA/support commitment or full-platform conformance claim.

## Current reuse boundary

P2.09 supplied the required evidence from two materially distinct workflows. R3 uses that evidence to distinguish genuine Core Runtime reuse from historical first-scenario structure.

The reusable Phase 2 semantic owners are the modules that implement domain-neutral runtime responsibilities directly, including:

- `canonical_lineage.py` — Canonical lineage plus exact/Head/Effective Version resolution;
- `relationships.py` — Typed Relationship identity/version/endpoint semantics over canonical lineage;
- `governed_execution.py` — Governed Execution lifecycle, exact version attribution, gates and consequential-operation admission;
- `event_provenance.py` — Event receipt/admission, immutable Event conflict semantics and reconstruction;
- `runtime_consistency.py` — stale-head/current-version protection, retry/idempotency, uncertainty and bounded logical commit semantics;
- `product_contract.py` — bounded Product Contract validation and the product-like entry into Governed Execution;
- `portability_runtime.py` — bounded semantic reconstruction and non-authoritative replay/projection behavior.

The two P2.09 workflows both reuse `product_contract.py` + `governed_execution.py` while exercising materially different version-resolution, relationship, gate and consequential-effect paths.

## Historical P1/P2.01 compatibility path

`runtime.py`, `reference_runtime_adapters.py` and `reference_scenario.py` remain executable evidence for the original Phase 1/P2.01 path.

R3 explicitly classifies this path as **reference compatibility infrastructure, not the generalized Phase 2 Core Runtime entry**:

- `RuntimeExecutionRequest` remains intentionally shaped around the original one-input canonical-mutation scenario;
- `RuntimeOperations` remains an explicit P1 adapter bundle established by R1, not a plugin/extension contract;
- `RuntimeComposition` is not extended to absorb the materially different P2.09 workflow;
- new workflows should compose the later semantic owners appropriate to their declared inputs, gates, authority requirements and side effects.

Keeping this historical path bounded preserves executable Phase 1 evidence without turning first-scenario structure into accidental architecture.

## R3 refactoring disposition

R3 deliberately avoids a generic workflow/test factory or an `allow-all-gates` runtime helper.

The remaining fixture/configuration repetition in P2.07/P2.09 is test-evidence setup, not duplicated platform orchestration. Extracting it into a generalized runtime builder would hide exactly the declarations the tests are intended to vary and could incorrectly couple gate decision creation with execution admission.

Likewise, small validation helpers and module-scoped runtime error families remain local until a stable shared semantic contract—not merely similar Python syntax—justifies consolidation.

One carried R2 test-specificity debt is resolved at R3: the P2.06 Event-admission conflict test now asserts `EventIdentityConflictError` rather than broad `RuntimeError`.

Architecture fitness checks for the R3 reuse disposition live in `tests/test_r3_reuse_refactoring.py`.

## Package-root surface

`arvectum_os_ref.__init__` still re-exports Phase 1 convenience symbols. This package remains explicitly provisional/non-public, and the P2.09 reuse proof does not depend on that root surface.

R3 therefore does not create churn solely to prune those exports. They MUST NOT be treated as a stable SDK or cross-product contract; a stable-boundary review must revisit the surface before any public/cross-product interface is established.

## Deliberately not decided or claimed

This harness does **not** establish:

- a permanent Python package/service topology;
- a stable public or cross-product API/SDK;
- a database, durable transaction, locking/CAS or concurrency technology;
- a durable idempotency store or outbox/inbox mechanism;
- an Event broker/store or delivery guarantee;
- an IAM/policy provider or production authority-enforcement technology;
- a durable workflow engine, scheduler or queue;
- a stable Product Contract manifest/wire format;
- durable replay/projection storage;
- production portability/export authorization;
- full RFC conformance, operational readiness, SLA/support commitments or an `Active` Platform Capability.

The in-memory `RuntimeConsistencyState` is not a trusted arbitrary-deserialization/durable aggregate-admission boundary. That carried R2 limitation remains explicit until a concrete durable/public boundary justifies hardening and any required ADR.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next canonical action

After the R3 review and roadmap synchronization merge, the next Phase 2 work item is **`P2.10 — Core Runtime architecture fitness matrix`**.

P2.10 should accumulate final applicable M2 fitness evidence over the semantic owners above without reopening the rejected idea of generalizing the historical P2.01 compatibility composition.
