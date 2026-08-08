# Bounded Reference Implementation — Phase 1

Status: `Provisional implementation harness — Phase 1 complete`
Executable scope: `P1.01–P1.11`
Closure: `P1.12 complete`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001 through RFC-0008 `1.0.0`
Roadmap baseline: `2.1.0`
Closure review: `docs/reviews/P1-12-phase-1-bounded-slice-closure-review.md`

This directory contains the bounded executable reference implementation used to prove Roadmap milestone `M1`.

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

Final executable evidence:

- GitHub Actions workflow: `Reference Python CI`;
- run: `#13`;
- final executable code head: `ac96593478d132e88be5807afa5b3af82adce6ec`;
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

## Deliberately not decided or claimed

This harness does **not** establish:

- a permanent package layout or Python platform contract;
- a database, transaction or concurrency technology;
- a public API or SDK;
- an event broker/store, outbox/inbox or delivery protocol;
- a workflow/orchestration runtime;
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

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next canonical action

Phase 1 is complete. There is no next `P1.*` implementation item.

The Canonical Roadmap now requires **Phase 2 revalidation and decomposition** before `Phase 2 — Core Runtime` can become `Active`. Phase 2 implementation must not begin by treating the Phase 1 harness or the broader readiness inventory as accidental permanent architecture.
