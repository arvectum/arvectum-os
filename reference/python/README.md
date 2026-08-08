# Bounded Reference Implementation — Phase 1 + Core Runtime extraction

Status: `Provisional implementation harness — Phase 1 complete; P2.01 complete; R1 complete`
Executable scope: `P1.01–P1.11; P2.01; R1 structural fitness`
Closure: `P1.12 complete; M1 achieved`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001 through RFC-0008 `1.0.0`
Roadmap baseline: `2.3.1`
Phase 1 closure review: `docs/reviews/P1-12-phase-1-bounded-slice-closure-review.md`
R1 review: `docs/reviews/R1-structural-review.md`
Phase 2 plan: `docs/roadmap/PHASE-2-CORE-RUNTIME.md` `1.1.1`

This directory contains the bounded executable reference implementation used to prove Roadmap milestone `M1` and the provisional Phase 2 extraction work that begins turning those semantics into reusable Core Runtime boundaries.

It is deliberately an in-memory, domain-neutral, reversible implementation harness. It is **not** a supported production runtime, stable public API, persistence contract, Product Contract, `Active` Platform Capability, SLA/support commitment or full-platform conformance claim.

## Executable Phase 1 spine

### P1.01 — Organization scope and attributable Actor / Principal

Implemented:

- explicit Organization scope with no ambient/default fallback;
- stable immutable Identity value semantics;
- attributable actual Principal and acting-on-behalf-of representation;
- authentication evidence as reference-only context rather than permission or Organizational Authority.

Evidence: `arvectum_os_ref/identity.py`, `arvectum_os_ref/security.py`, `tests/test_identity_organization_actor.py`.

### P1.02 — Native subject + first immutable Canonical Record version

Implemented one bounded domain-neutral `Native` canonical subject with stable Subject Identity, distinct immutable Version Identity, explicit Organization/authority/owner/actor/provenance/integrity semantics, immutable payload and no predecessor for v1.

External authority modes intentionally fail closed because their complete external-authority contracts are outside this bounded scenario.

Evidence: `arvectum_os_ref/canonical.py`, `tests/test_p1_02_native_canonical_record.py`.

### P1.03 — Versioned Workflow baseline

Implemented one immutable domain-neutral Workflow version with a `Native` Canonical Record envelope and one scoped `CanonicalMutation` operation declaration.

Declaring the operation grants neither Authorization nor Organizational Authority and introduces no workflow engine.

Evidence: `arvectum_os_ref/workflow.py`, `tests/test_p1_03_versioned_workflow.py`.

### P1.04 — Execution Context + exact version pinning

Implemented one initial immutable `AwaitingGate` Execution Context with exact pins to the supplied effective Workflow version and material input version. Later versions under the same Subject Identities do not change the already-started execution's governed reliance.

No Canonical Head/effective-version resolver is introduced.

Evidence: `arvectum_os_ref/execution.py`, `tests/test_p1_04_execution_context.py`.

### P1.05 — Authorization and Organizational Authority gates

Implemented two separate fail-closed governed gate boundaries:

- `Authorization`;
- `OrganizationalAuthority`.

Neither implies the other. Two exact explicit `Allow` decision versions are required to create the immutable `Ready` Execution Context version.

The fixture records caller-supplied governed decision evidence. It does not grant real permissions or implement the Proposed Decision Authority Policy as normative governance.

Evidence: `arvectum_os_ref/gates.py`, `arvectum_os_ref/execution.py`, `tests/test_p1_05_authorization_authority_gates.py`.

### P1.06 — Governed Canonical Mutation + second immutable version

Implemented one bounded canonical mutation that:

- requires the exact immutable `Ready` execution;
- consumes exact Workflow/input/gate pins;
- rejects stale-current conflict;
- preserves v1 unchanged;
- creates a distinct immutable v2 with exact predecessor lineage;
- creates a terminal immutable `Succeeded` Execution Context version with the exact canonical effect pin.

Evidence: `arvectum_os_ref/mutation.py`, `tests/test_p1_06_governed_canonical_mutation.py`.

### P1.07 — Canonical Event admission and execution linkage

Implemented bounded Event receipt/admission separation and one immutable canonical Event linked to the exact terminal execution and resulting target version.

Duplicate delivery is idempotent and does not repeat the canonical mutation. Conflicting immutable Event identity/version reuse fails closed.

Evidence: `arvectum_os_ref/events.py`, `tests/test_p1_07_canonical_event_admission.py`.

### P1.08 — Provenance, causation and reconstruction evidence

Implemented a frozen derived non-canonical reconstruction manifest that verifies exact actor, Workflow/input/gate/execution/result/Event references and predecessor lineage.

Reconstruction is observational and cannot replay the mutation or create another Event.

Evidence: `arvectum_os_ref/provenance.py`, `tests/test_p1_08_provenance_reconstruction.py`.

### P1.09 — Observation creation without Knowledge promotion

Implemented one significant Observation through the existing Canonical Record envelope with explicit `Unvalidated` epistemic status and exact Event/execution/effect evidence pins.

The harness exposes no successful Knowledge-promotion path; validated-Knowledge reliance fails without the RFC-0007 governed promotion lifecycle.

Evidence: `arvectum_os_ref/observation.py`, `tests/test_p1_09_observation_non_promotion.py`.

### P1.10 — Portable semantic fixture export

Implemented deterministic documented UTF-8 JSON export through explicit semantic mapping rather than Python object layout.

The fixture preserves Organization, Actor attribution, Subject/Version identity roles, Canonical Record envelopes, exact Workflow/input/gate/effect pins, Event/provenance semantics and Observation non-promotion.

The fixture explicitly declares:

- `canonical_authority = false`;
- `public_compatibility_contract = false`;
- `production_export_endpoint = false`.

Derived `semantic_links` preserve reference meaning while declaring `canonical_typed_relationship = false`; they do not fabricate RFC-0002 Typed Relationship Canonical Records.

Evidence: `arvectum_os_ref/portability.py`, `PORTABLE-SEMANTIC-FIXTURE.md`, `tests/test_p1_10_portable_semantic_fixture.py`.

### P1.11 — Negative-path and architecture fitness tests

Implemented the final replay/projection matrix:

- historical fixture replay creates only an immutable non-authoritative `ProjectionSnapshot`;
- replay has no Governed Execution, canonical mutation, Event-admission callback or external-effect path;
- replay preserves exact source Version Identity attribution and rejects manifest drift;
- derived links cannot be reinterpreted as canonical Typed Relationships;
- projection lookup exposes all matching source versions without resolving canonical/effective authority;
- a projection cannot mint or substitute for a governed exact-version pin;
- consequential version reliance requires an independently supplied exact `CanonicalRecord`;
- stale or mismatched source versions fail closed.

Evidence: `arvectum_os_ref/fitness.py`, `tests/test_p1_11_architecture_fitness.py`.

Phase 1 final executable evidence:

- GitHub Actions workflow: `Reference Python CI`;
- run: `#13`;
- final Phase 1 executable code head: `ac96593478d132e88be5807afa5b3af82adce6ec`;
- command: `python -m unittest discover -s tests -v`;
- result: `Ran 128 tests` / `OK`;
- workflow conclusion: `success`.

## P1.12 — Phase 1 bounded-slice closure review

P1.12 is a review/roadmap milestone rather than additional executable reference code.

Canonical closure review:

- `../../docs/reviews/P1-12-phase-1-bounded-slice-closure-review.md`.

Result: **`PASS — M1 achieved for the declared bounded reference scope.`**

The review confirms:

1. P1.01–P1.10 complete within the declared scope;
2. P1.11 matrix passes;
3. no product-domain leakage;
4. no missed ADR gate;
5. implementation remains reversible/migration-friendly;
6. no `Active`/production implication;
7. canonical roadmap synchronized.

## P2.01 — Runtime boundary extraction and reusable composition baseline

P2.01 extracts runtime orchestration ownership from the deterministic P1 scenario without changing the proven semantic steps.

Implemented:

- `arvectum_os_ref/runtime.py` — provisional internal `RuntimeComposition` plus explicit `RuntimeExecutionRequest`, `RuntimeExecutionResult` and replaceable `RuntimeOperations` adapters;
- `arvectum_os_ref/reference_scenario.py` — deterministic fixture setup that supplies Organization/actors, the exact Workflow/material input, governed basis references and successor content, then delegates once through the runtime composition boundary;
- runtime orchestration preserves exact Workflow/material-input pins, separate Authorization and Organizational Authority evidence, immutable Execution Context lineage, governed canonical mutation, canonical Event admission, reconstruction evidence and Observation non-promotion;
- existing P1.10 semantic export consumes the runtime result unchanged and remains bounded, derived, non-authoritative and non-public;
- adapters remain replaceable and no product-domain semantics are introduced into the shared runtime boundary;
- no database, broker, IAM/policy provider, workflow engine, service topology, public API/SDK or durable serialization contract is selected.

Evidence: `arvectum_os_ref/runtime.py`, `arvectum_os_ref/reference_scenario.py`, `tests/test_p2_01_runtime_composition.py`.

P2.01 executable checkpoint:

- GitHub Actions workflow: `Reference Python CI`;
- run: `#18`;
- executable code head: `5f56f0bf36e58efe5249b93e9df6ca4437d5621e`;
- command: `python -m unittest discover -s tests -v`;
- result: `Ran 138 tests` / `OK`;
- workflow conclusion: `success`.

P2.01 established the first composition seam but still selected the bounded P1 adapter set by default. R1 subsequently hardened that boundary without changing P2.01 semantics.

## R1 — Structural Review

R1 reviewed the P2.01 runtime / fixture / test split, dependency direction, scenario leakage, duplicated orchestration, accidental APIs and reversibility before substantive P2.02 work.

Canonical review:

- `../../docs/reviews/R1-structural-review.md`.

Structural remediation:

- `arvectum_os_ref/reference_runtime_adapters.py` now explicitly owns the bounded P1 operation binding;
- `RuntimeComposition` requires explicit `RuntimeOperations` and no longer imports or selects historical `*_p1_*` operation functions by default;
- the deterministic reference scenario explicitly selects `reference_runtime_operations()` when using the reference fixture;
- no duplicated P1.04–P1.09 orchestration was introduced;
- P1-specific deterministic IDs/timestamps remain contained inside reference adapters rather than being prematurely generalized ahead of P2.04/P2.05;
- package-root P1 re-exports remain provisional/non-public and are not treated as a stable SDK/cross-product contract;
- no ADR gate was crossed.

R1 executable checkpoint:

- GitHub Actions workflow: `Reference Python CI`;
- run: `#23`;
- executable code head: `e0c71c1c80b658711a7420ffb7d59248ce741fb8`;
- command: `python -m unittest discover -s tests -v`;
- result: `Ran 140 tests` / `OK`;
- workflow conclusion: `success`.

Result: **`PASS — R1 completed for the P2.01 structural scope.`**

## Deliberately not decided or claimed

This harness does **not** establish:

- a permanent package layout or Python platform contract;
- a database, transaction or concurrency technology;
- a public API or SDK;
- an event broker/store, outbox/inbox or delivery protocol;
- a durable workflow engine, scheduler, queue or permanent orchestration/service runtime technology;
- an IAM provider, durable authorization/policy engine or production authority model;
- a tenant-isolation technology;
- a persistent lineage/provenance store;
- a Canonical Head / Effective Version resolver;
- a search/index/vector provider or durable projection store;
- a Product Contract instance for a real Product;
- the full RFC-0002 Typed Relationship lifecycle;
- the complete RFC-0007 Organizational Memory / Knowledge Candidate / validated Knowledge lifecycle;
- production portability or service-termination export;
- full RFC conformance, operational readiness or customer commitments.

The P1.06 `current_record` argument is bounded conflict-check evidence, not a Canonical Head resolver.

The P1.07 `admitted_events` tuple is bounded immutable test history, not a durable Event store.

P1.08 reconstruction is derived non-authority.

P1.09 Observation is explicitly unvalidated and not Knowledge.

P1.10 JSON is a bounded semantic fixture, not a stable public wire format.

P1.11 projection is a derived read model and cannot become canonical authority.

P2.01/R1 `RuntimeComposition` is an internal bounded composition root; its Python call surface and the reference adapter set are not stable public/cross-product contracts.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next canonical action

Phase 1 remains complete, `P2.01` is complete within its bounded runtime-extraction scope, and `R1` is complete.

The Canonical Roadmap current action is **`P2.02 — Canonical Record lineage, Head and Effective Version runtime`**. P2.02 must preserve exact Version Identity reliance and distinguish Canonical Head from Effective Version resolution without selecting a database/index technology merely for implementation convenience, and must not turn the R1-hardened provisional Python composition boundary into a stable public contract.
