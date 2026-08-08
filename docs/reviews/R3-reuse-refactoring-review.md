# R3 — Reuse Refactoring Review

Status: `Complete`
Date: `2026-08-08`
Gate: `R3 — Reuse Refactoring Review`
Task classification: `platform`
Trigger: after `P2.09`, before final Phase 2 hardening
Result: **`PASS — evidence-backed reuse retained; first-scenario over-generalization contained; no new shared abstraction justified.`**

## 1. Scope

R3 reviews the accumulated Phase 2 Core Runtime after the second materially distinct workflow proof. Its purpose is not to maximize abstraction. It is to use actual reuse evidence to decide which boundaries are genuinely shared, which first-scenario structures should remain compatibility-only, which duplication should be removed, and which apparent duplication should remain explicit because it carries different governance meaning.

The review covers:

- the historical P2.01 `RuntimeComposition` / `RuntimeOperations` / reference-scenario seam;
- P2.04 Governed Execution and P2.07 Product Contract as the demonstrated shared product/runtime entry path;
- P2.02–P2.08 semantic-owner boundaries exercised by the two P2.09 workflows;
- fixture/configuration duplication pressure carried forward by the P2.09 cross-review;
- R2 bounded debt relevant to reuse, error specificity and runtime-state integrity;
- package/import direction and accidental extension/public-contract pressure;
- whether any refactoring now crosses an ADR gate.

R3 does not change an Accepted RFC, establish a stable public API/SDK, select durable persistence or execution technology, activate a Platform Capability, or claim production readiness/full conformance.

## 2. Canonical authority checked

The review was performed against the current canonical repository state and the following higher-authority material:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `1.0.0` — `Accepted`;
- RFC-0004 Product Contract / Product Experiment / Extension Model `1.0.0` — `Accepted`;
- RFC-0005 Governed Execution / Workflow Model `1.0.0` — `Accepted`;
- RFC-0006 Event / Provenance / Observability Model `1.0.0` — `Accepted`;
- `DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`;
- R1 Structural Review;
- R2 Runtime Health Review;
- P2.09 second bounded workflow reuse proof and its cross-review;
- current Phase 2 roadmap and implementation/tests.

No conflict with the Constitution or Accepted RFC baseline was found.

## 3. Reuse evidence used

P2.09 supplies two materially different domain-neutral workflows rather than two copies of the original P1 path.

### Workflow A — canonical mutation

The first P2.09 workflow:

- relies on one exact current Canonical Record version;
- uses Authorization, Organizational Authority, Data Governance and Validation gates;
- declares `CanonicalMutation`;
- commits one immutable successor and one canonical Event through P2.06/P2.05 semantics;
- proves keyed retry does not append a second result/Event/effect attempt.

### Workflow B — external consequence with version/relationship context

The second P2.09 workflow:

- resolves an Effective Version that intentionally differs from the future-effective Canonical Head;
- pins a Typed Relationship whose source endpoint is an exact `VersionIdentity`;
- uses multiple material inputs;
- uses Actor Assurance, Authorization, Data Governance and Consequential Approval gates;
- declares `ExternalMutation` and `Commitment` rather than canonical mutation;
- records external-consequence outcome/idempotency evidence without publishing a canonical successor or Event.

Both workflows enter through P2.07 `start_product_governed_execution`, reuse P2.04 Governed Execution lifecycle/gate semantics, preserve exact Product Contract/Workflow/material-input Version Identity attribution, and then compose the domain-neutral semantic owners appropriate to their distinct effects.

That is the reuse evidence R3 treats as authoritative for refactoring decisions.

## 4. Findings and dispositions

### R3-F1 — Historical P2.01 composition is not the demonstrated Core Runtime reuse seam

**Severity:** material design clarification  
**Disposition:** resolved

`RuntimeComposition` was useful in P2.01 to separate the original Phase 1 fixture from its orchestration and R1 correctly prevented it from silently selecting P1 adapters. However, its request/result shape remains specific to the original first scenario:

- one `material_input`;
- exactly Authorization plus Organizational Authority decisions;
- one canonical successor mutation;
- one Event;
- reconstruction evidence;
- one unvalidated Observation.

The materially distinct P2.09 workflow deliberately does not use that composition. Generalizing `RuntimeExecutionRequest` now with variable material inputs, arbitrary gate sets, Product Contract data, relationship/version-resolution configuration and external-effect semantics would turn a historical first-scenario seam into a speculative workflow framework.

**R3 action:** retain `runtime.py` as executable P1/P2.01 reference-compatibility evidence, explicitly document that it is not the reusable Phase 2 Core Runtime entry point, and add fitness tests preventing later semantic owners from depending on it. Do not delete it yet because it preserves already-proven bounded historical behavior; do not expand it merely to fit newer workflows.

### R3-F2 — Genuine reuse is semantic-owner reuse, not one universal orchestrator

**Severity:** architectural confirmation  
**Disposition:** accepted

Actual shared behavior now sits in the domain-neutral semantic owners established by P2.02–P2.08:

- canonical lineage / exact, Head and Effective Version resolution;
- Typed Relationship identity/version/endpoint semantics;
- Governed Execution lifecycle, gates and consequential-operation admission;
- Event admission/provenance/reconstruction;
- runtime consistency, idempotency, stale-head and uncertainty semantics;
- Product Contract validation and product-like governed entry;
- bounded portability/reconstruction/non-authoritative projection.

The two workflows share these owners selectively according to their declared semantics. R3 therefore rejects the assumption that successful reuse requires one monolithic `execute_any_workflow()` abstraction.

### R3-F3 — Do not promote the P2.09 gate-decision helper into runtime authority

**Severity:** governance/security guard  
**Disposition:** no refactor

The P2.09 test fixture contains one shared helper that creates explicit `ALLOW` decisions and advances execution through AwaitingGate → Ready → Running. This is useful test orchestration because the test intentionally supplies the decision evidence.

Promoting that helper into platform runtime would be dangerous over-generalization: the runtime must not fabricate or infer Organizational Authority, Authorization or other consequential approvals. Governed Execution validates and records decision evidence; it does not become the decision authority.

**R3 action:** keep the helper test-local. No `allow_all_gates`, automatic-decision or universal start-and-approve runtime API is introduced.

### R3-F4 — Fixture/configuration repetition does not yet justify a shared runtime factory

**Severity:** maintainability observation  
**Disposition:** explicit duplication retained

P2.07/P2.09 repeat setup for synthetic Organizations, Actors, Workflows, Product Contracts and exact version identities. The repeated syntax is real, but the values are the evidence under test: different gate sets, effect classes, read/write scopes, exact version pins and Product Contract declarations are intentionally visible.

A generic fixture factory would reduce line count while making the material differences less obvious and could prematurely standardize a Python test API as platform structure.

**R3 action:** no shared platform/runtime fixture abstraction is created. A test-support-only builder may be reconsidered after additional independent scenarios demonstrate stable construction semantics and a measurable readability/maintenance benefit.

### R3-F5 — Product Contract requested-vs-declared repetition is intentional

**Severity:** design clarification  
**Disposition:** retained

`validate_product_contract_interaction` / `start_product_governed_execution` repeat requested interaction data against the allowed contract declarations. This is not accidental duplication: it is the fail-closed comparison boundary between what a caller is trying to rely on and what the exact Product Contract version permits.

Deriving the interaction automatically from the contract would erase that distinction and weaken mismatch detection.

**R3 action:** retain the explicit requested interaction parameters.

### R3-F6 — Similar local validators/error families still do not justify speculative unification

**Severity:** bounded maintainability debt  
**Disposition:** retain local ownership

R2 noted repeated validation idioms and multiple resolution/conflict error families. R3 now has two workflow configurations, but still no evidence of one stable shared semantic contract that would improve correctness by collapsing those boundaries.

Canonical-lineage errors, relationship errors, Governed Execution errors, Event identity/admission errors and runtime-consistency/idempotency errors describe materially different failure domains. A shared generic hierarchy/helper would currently optimize Python shape rather than organizational semantics.

**R3 action:** keep validation/error ownership local. Revisit if a stable public/cross-product boundary or repeated caller behavior demonstrates one common contract.

### R3-F7 — Broad Event-conflict test assertion was too weak

**Severity:** small test-quality debt  
**Disposition:** resolved

R2 carried one P2.06 assertion that expected broad `RuntimeError` when Event admission detected conflicting immutable Event identity/content.

**R3 action:** tighten the assertion to the exact semantic owner error: `EventIdentityConflictError`. Runtime behavior is unchanged; the test now protects the intended Event-admission contract rather than any arbitrary runtime failure.

### R3-F8 — Package-root P1 convenience exports remain provisional, not proven public API

**Severity:** low / deferred boundary hygiene  
**Disposition:** deferred to stable-boundary hardening

The package root still exposes convenience symbols inherited from the Phase 1 harness. P2.09 does not rely on that root surface, and the package is explicitly internal/provisional.

Removing exports now would create churn without improving the demonstrated reuse boundary. Treating them as stable would be worse.

**R3 action:** no public-contract claim and no forced pruning in R3. R4/P2.11 must revisit the surface before any stable public/cross-product SDK/API commitment.

### R3-F9 — `RuntimeConsistencyState` remains a bounded in-memory aggregate, not durable admission authority

**Severity:** carried architecture debt  
**Disposition:** explicitly carried forward

R2 correctly noted that arbitrary/deserialized construction of `RuntimeConsistencyState` is not hardened as a durable aggregate-integrity admission boundary. R3 does not introduce persistence/deserialization or a trusted external construction path, so the issue does not block this gate and no speculative durable mechanism should be invented here.

**R3 action:** keep the limitation explicit. Revisit when a concrete persistence/import/transaction boundary is selected; govern any materially constraining choice through the ADR gate before reliance.

### R3-F10 — No evidence-backed performance refactor is justified

**Severity:** none  
**Disposition:** no optimization

The complete reference suite remains sub-second at current scale and no correctness/resource-exhaustion/security profile indicates a hotspot requiring optimization. R3 therefore performs structural reuse refactoring only and does not introduce caches, concurrency primitives, persistence shortcuts or other speculative performance architecture.

## 5. Implemented R3 changes

R3 makes the minimum changes supported by the review evidence:

1. reclassifies `reference/python/arvectum_os_ref/runtime.py` as the historical P1/P2.01 reference-composition compatibility boundary;
2. explicitly states that `RuntimeOperations` is not a plugin/extension contract and `RuntimeComposition` must not be expanded to absorb the second workflow;
3. aligns `reference_runtime_adapters.py` and `reference_scenario.py` with that compatibility-only disposition;
4. simplifies `reference/python/README.md` around the current reusable semantic-owner model instead of presenting the P2.01 seam as the current runtime architecture;
5. adds `tests/test_r3_reuse_refactoring.py` to lock dependency direction and prevent later runtime owners from acquiring a dependency on historical `RuntimeComposition`;
6. tightens the carried P2.06 Event conflict assertion to `EventIdentityConflictError`.

No behavioral platform contract is broadened, no Accepted RFC is edited, and no first-scenario API is promoted to a stable cross-product surface.

## 6. Executable evidence

GitHub Actions `Reference Python CI` run `#63` on executable branch head `72c97b8b24e86369d00c5932a3723743577b0c21` completed successfully.

Command:

```text
python -m unittest discover -s tests -v
```

Result:

```text
Ran 293 tests in 0.312s
OK
```

The suite includes the prior P1/P2.01–P2.09 and R2 evidence plus four R3 reuse-boundary fitness tests. No previously green runtime behavior regressed.

## 7. ADR gate assessment

**Result: no new ADR required for R3.**

R3 does not select or materially rely on:

- durable persistence/database topology;
- transaction, locking or concurrency technology;
- Event storage/delivery or outbox/inbox topology;
- IAM/policy enforcement technology;
- stable public/cross-product API or serialization contract;
- durable projection/replay storage;
- service/process topology;
- extension/plugin technology.

The refactoring is internal, bounded, reversible and primarily constrains accidental interpretation of an existing historical seam. If later work converts any current module/interface into a materially constraining durable/public boundary, P2.11 must apply the existing ADR gate before reliance.

## 8. R3 exit assessment

R3 exit conditions are satisfied:

- two materially distinct workflows provide real reuse evidence;
- the shared semantic owners are identified from that evidence;
- first-scenario over-generalization is contained rather than promoted;
- no duplicated platform orchestration fork exists between the two workflows;
- explicit gate/authority/version boundaries are preserved;
- product-domain semantics remain absent from the shared runtime;
- carried actionable test-specificity debt is resolved;
- speculative validation/error/fixture/public API abstractions are rejected for lack of evidence;
- no missing ADR gate is found;
- the full executable suite is green.

**Final R3 decision: `PASS`.**

## 9. Carried items for final Phase 2 hardening

The following do not block R3 but remain visible for P2.10/R4/P2.11:

1. final cross-cutting architecture fitness coverage over the complete Phase 2 semantic-owner set;
2. stable-boundary review of package-root convenience exports before any public/cross-product API claim;
3. reconsider exact-resolution/error taxonomy only if caller evidence demonstrates a common external contract;
4. harden `RuntimeConsistencyState` aggregate admission only when a real durable/deserialization boundary exists;
5. re-run the ADR gate if final hardening introduces any materially constraining implementation choice.

## 10. Next canonical action

Proceed to **`P2.10 — Core Runtime architecture fitness matrix`**.

P2.10 should consolidate final applicable M2 fitness evidence across the semantic owners proven through P2.09/R3. It should not reopen the rejected idea of generalizing the historical P2.01 compatibility composition merely to obtain one universal orchestration API.
