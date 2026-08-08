# Bounded Reference Implementation — Phase 1

Status: `Provisional implementation harness`
Scope: `Phase 1 / P1.01–P1.09`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001, RFC-0002, RFC-0003, RFC-0005, RFC-0006 and RFC-0007 `1.0.0`
Roadmap baseline: `2.0.5`

This directory contains the bounded executable reference implementation defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`.

## P1.01 — Organization scope and attributable Actor / Principal

Implemented and merged:

1. one Organization scope is explicit and has no ambient/default fallback;
2. one acting Principal is attributable through a stable Subject Identity;
3. acting-on-behalf-of context preserves both actual and represented Principals;
4. Identity values remain immutable and do not encode roles, permissions or Organizational Authority;
5. authentication evidence is reference-only and is not authorization or Organizational Authority.

## P1.02 — Native subject + first immutable Canonical Record version

This work item adds one domain-neutral `Native` canonical subject with:

- stable Subject Identity;
- distinct first Version Identity;
- semantic record type and schema version;
- explicit Organization scope;
- explicit `Native` authority mode and authority scope;
- accountable architectural owner reference;
- attributable creation Actor and timezone-aware creation time;
- explicit provenance references;
- proportional integrity metadata for this bounded in-memory harness;
- immutable tuple payload representation;
- no predecessor for the initial version.

`External Reference` and `Governed Replica` are intentionally rejected by the P1.02 model. Their required external-authority, synchronization, freshness, ordering, conflict and failure contracts are not part of this work item.

The Python `frozen` value object and immutable tuple payload provide executable evidence of in-process semantic immutability for this bounded harness. They are **not** a claim of durable storage integrity, tamper evidence, database persistence, cryptographic sealing or production canonical-history guarantees.

## P1.03 — Versioned Workflow baseline

This work item adds one domain-neutral governed Workflow definition with:

- stable Workflow Subject Identity;
- distinct immutable Workflow Version Identity;
- a `Native` Canonical Record envelope for the Workflow version;
- explicit Organization scope, owner, lifecycle and provenance;
- one immutable semantic operation declaration targeting the exact reference subject;
- RFC-0005 `CanonicalMutation` side-effect classification;
- explicit separation between Workflow capability declaration and authorization, Organizational Authority or consequential approval;
- fail-closed Organization-scope validation for the Workflow and its target.

The Workflow does **not** execute the mutation in P1.03. It only declares the governed executable intent required for the next steps. No workflow engine, scheduler, queue or orchestration runtime is introduced.

## P1.04 — Execution Context + exact version pinning

This work item starts one bounded domain-neutral governed execution attempt with:

- a stable Execution Subject Identity and distinct immutable initial Execution Version Identity;
- a `Native` `platform.execution-context` Canonical Record envelope;
- explicit Organization scope and attributable initiating Actor;
- initial lifecycle state `AwaitingGate`, making unresolved P1.05 governance gates explicit rather than implicitly passed;
- an exact immutable pin to both the Workflow Subject Identity and the effective Workflow Version Identity supplied to the execution;
- an exact immutable pin to the materially relied-upon P1.02 Canonical Record Subject Identity and Version Identity;
- operation attribution to the single scoped `CanonicalMutation` declaration from the pinned Workflow version;
- provenance references containing the exact Workflow and material input versions;
- fail-closed checks for Organization mismatch, operation mismatch, invalid pin shape and duplicate material input versions.

The reference test proves that a later version under the same Workflow or input Subject Identity does not change the already-started execution's pinned Version Identity. This is exact version reliance rather than a mutable "current" lookup.

P1.04 deliberately does **not** add authorization decisions, Organizational Authority, approval evaluation, a Canonical Head/effective-version resolver, actual canonical mutation, an Event, durable persistence or a workflow engine. Those remain later Phase 1 work items.

Canonical validation through P1.04 remains the previously recorded `31` unit-test baseline, including `10` P1.04 tests.

## P1.05 — Authorization and Organizational Authority gates

This work item adds two deliberately separate, fail-closed governed gate boundaries for the exact P1.04 execution attempt:

- `Authorization` and `OrganizationalAuthority` are distinct gate kinds;
- each gate has an explicit immutable `Allow` or `Deny` decision record rather than an ambient boolean;
- missing required decisions remain unresolved and cannot advance execution;
- authentication/Actor attribution does not satisfy Authorization;
- Authorization `Allow` does not satisfy Organizational Authority;
- Organizational Authority `Allow` does not satisfy Authorization;
- an explicit `Deny` on either required gate blocks the bounded transition;
- each decision is bound to one Organization, initiating Principal, exact `AwaitingGate` Execution Context version, exact pinned Workflow Version Identity, operation, target Subject Identity and target Version Identity;
- each decision preserves an explicit governed basis reference in provenance without defining a production policy engine, role matrix or delegation catalog;
- only two independently valid explicit `Allow` decisions create the next immutable Execution Context version under the same Execution Subject Identity;
- the new version is `Ready`, links to the P1.04 `AwaitingGate` version as predecessor, preserves the exact Workflow/material-input pins and pins both exact gate-decision versions;
- a manually constructed `Ready` context containing a `Deny` gate pin fails validation;
- the original target Canonical Record is not changed by P1.05.

The `Ready` label is scoped to this bounded scenario: it proves the two P1.05 gates applicable to the first reference slice and is not a claim that every possible RFC-0005 approval, data-governance, validation or product-specific gate has been globally satisfied.

`build_p1_05_gate_decision` records fixture decision evidence supplied by the caller; it does **not** grant real permissions, delegation or Organizational Authority. The Proposed Decision Authority Policy is not treated as approved or implemented by this harness. A real IAM provider, policy engine, authorization enforcement technology and organization-specific authority model remain later adapter/ADR/governance concerns when actual product evidence requires them.

Repository evidence: `reference/python/arvectum_os_ref/gates.py`, the P1.05 extensions in `reference/python/arvectum_os_ref/execution.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_05_authorization_authority_gates.py`.

P1.05 adds `12` executable fitness tests covering independent gate semantics, deny-by-default behavior, exact scoped decision evidence, governed basis provenance, immutable gate pins, Ready-version lineage, forged Ready rejection and non-mutation of the target.

## P1.06 — Governed Canonical Mutation + second immutable version

This work item executes the already-declared `CanonicalMutation` only through the exact immutable `Ready` Execution Context admitted by P1.05:

- direct consequential mutation without an explicit Execution Context fails closed;
- an `AwaitingGate` execution cannot mutate canonical state;
- the mutation consumes the exact Workflow Subject/Version pin established by P1.04 rather than re-resolving a mutable current Workflow;
- the mutation consumes the exact P1.05 Authorization and Organizational Authority decision versions already pinned by the `Ready` execution;
- the caller-supplied admitted current target version must still equal the exact material-input Version Identity pinned before consequential reliance;
- a different current target version raises an explicit canonical conflict instead of silently overwriting newer state;
- the resulting target record preserves the original stable Subject Identity and creates a distinct immutable Version Identity;
- the second target version names P1.02 v1 as its exact predecessor while P1.02 v1 remains unchanged and immutable;
- result provenance preserves the exact input, `Ready` execution, Workflow and gate-decision version references used for the mutation;
- the canonical-state change creates a governance-significant terminal `Succeeded` Execution Context version under the same Execution Subject Identity;
- that terminal execution version preserves the exact Workflow/material-input/gate pins and adds one exact canonical-effect Version pin;
- P1.06 does not emit or admit a canonical Event; Event admission remains P1.07.

Repository evidence: `reference/python/arvectum_os_ref/mutation.py`, P1.06 extensions in `reference/python/arvectum_os_ref/execution.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_06_governed_canonical_mutation.py`.

P1.06 adds `13` executable fitness tests covering governed-entry enforcement, immutable-version lineage, exact pinned Workflow/gate evidence, stale-current conflict detection, Organization/version constraints, provenance, terminal execution effect pinning and explicit non-preemption of P1.07 Event admission.

## P1.07 — Canonical Event admission and execution linkage

This work item admits one bounded domain-neutral canonical Event for the completed P1.06 mutation under RFC-0002/RFC-0006 semantics:

- receipt is represented by a transient immutable `EventCandidate` and is explicitly distinct from canonical Event admission;
- only the admission boundary creates the `platform.event` Canonical Record specialization;
- the admitted Event uses stable Event Identity plus one distinct immutable Event Version Identity and has no predecessor, preserving the normal single-version append-only Event model;
- the Event uses `Native` authority for the governed observation produced by Arvectum OS and preserves explicit event type/schema, source, occurrence/admission time, producer/initiation attribution, classification/access scope, provenance and integrity metadata;
- admission consumes the exact P1.06 `CanonicalMutationResult` rather than re-resolving mutable state;
- the Event links to the exact terminal `Succeeded` Execution Subject/Version Identity and to the exact resulting target Subject/Version Identity;
- correlation preserves the stable Execution Subject Identity while causation preserves the exact terminal Execution Context Version Identity used by this bounded scenario;
- the sealed terminal Execution Context is not mutated or extended after success merely to add an Event reference;
- repeated delivery of the same immutable Event representation returns the already-admitted Event and does not create a second occurrence or repeat the canonical mutation;
- reuse of an admitted Event Identity with materially different immutable content raises an explicit `EventIdentityConflictError` without rewriting history;
- reuse of an immutable Event Version Identity for another Event is rejected;
- wrong execution linkage, wrong resulting-version linkage and cross-Organization linkage fail closed;
- broader provenance graph/reconstruction semantics remain P1.08 scope.

The caller-supplied `admitted_events` tuple is bounded immutable history for the in-memory harness. It is not an event store, topic, broker, outbox/inbox mechanism, delivery guarantee or public persistence contract.

Repository evidence: `reference/python/arvectum_os_ref/events.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_07_canonical_event_admission.py`.

P1.07 adds `14` focused executable fitness tests covering receipt/admission separation, immutable single-version Event semantics, exact execution/result linkage, occurrence/admission time, explicit Event envelope semantics, duplicate-delivery idempotency, conflicting Event Identity/Version Identity handling, cross-Organization fail-closed behavior and preservation of the sealed P1.06 execution/result evidence.

## P1.08 — Provenance, causation and reconstruction evidence

This work item adds a read-only reconstruction boundary over the exact immutable P1.02–P1.07 evidence:

- `ReconstructionEvidence` is a frozen derived manifest, not a Canonical Record and not an authority source;
- reconstruction identifies the initiating Principal and Organization, exact Workflow version, exact material input version, both governed gate-decision versions and their basis references, all three governance-significant Execution Context versions, the exact canonical result version and the exact admitted Event version;
- `AwaitingGate → Ready → Succeeded` predecessor lineage is verified without rewriting history;
- exact Workflow/material-input/gate/result/Event version linkage and actor continuity are validated fail closed;
- result, terminal execution and Event provenance are checked for the exact version-identifiable references required by the bounded operation;
- correlation remains the stable Execution Subject Identity while causation remains the exact terminal `Succeeded` Execution Context Version Identity;
- repeated reconstruction is deterministic and observational and does not replay the mutation, emit another Event or mutate sealed canonical/execution/Event history.

Repository evidence: `reference/python/arvectum_os_ref/provenance.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_08_provenance_reconstruction.py`.

P1.08 adds `15` focused architecture-fitness tests. It deliberately does **not** define replay execution semantics, a portable serialization/fixture contract, Observation/Knowledge promotion, a projection/index authority model, durable lineage persistence or a public provenance API.

## P1.09 — Observation creation without Knowledge promotion

This work item creates one significant, domain-neutral RFC-0007 Observation from exact already-governed P1.06–P1.08 evidence:

- Observation is a semantic role represented through the existing RFC-0002 `CanonicalRecord` envelope rather than a new Kernel primitive;
- the Observation has stable Subject Identity, distinct immutable initial Version Identity, explicit Organization scope, `Native` authority limited to the recorded observation, accountable owner, attributable Actor and `Captured` lifecycle state;
- exact source pins identify the admitted P1.07 Event, terminal `Succeeded` P1.06 Execution Context and resulting canonical-effect versions verified by P1.08;
- reconstruction provenance and initiating-Principal attribution are preserved in the Observation evidence rather than replaced with an inferred current-state lookup;
- epistemic status is explicitly `Unvalidated`, and integrity metadata records that Knowledge promotion was not performed;
- `require_explicit_knowledge_promotion` is intentionally a fail-closed negative-path guard, not a promotion API: the P1.09 harness provides no successful path that can reinterpret an Observation as validated Knowledge;
- creating the Observation does not mutate the Workflow, original/result Canonical Record versions, sealed terminal Execution Context or admitted Event and does not change an approved standard, policy, Workflow or production behavior;
- wrong Event, terminal Execution or effect versions, changed Event semantics and incomplete reconstruction provenance fail closed;
- Organizational Memory, Knowledge Candidate/Proposal, Knowledge admission, Improvement Proposal, promotion approval and self-modifying production behavior remain outside P1.09.

Repository evidence: `reference/python/arvectum_os_ref/observation.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_09_observation_non_promotion.py`.

P1.09 adds `14` focused architecture-fitness tests. PR-time `Reference Python CI` passes the complete bounded suite: `99` tests, `OK`.

## Deliberately not decided

This harness does **not** establish a permanent package layout, programming-language contract, database, API, event broker, durable event store, outbox/inbox strategy, delivery protocol, schema registry, IAM provider, policy engine, deployment topology, persistent lineage store, Canonical Head/effective-version resolver, workflow engine, Product Contract, production role matrix or durable authorization-enforcement mechanism.

The P1.06 `current_record` argument is a bounded caller-supplied admitted-current fixture used only to exercise conflict detection against the exact version already pinned by the execution. It is not a canonical-head service, mutable projection authority or public resolution contract.

The P1.07 `admitted_events` argument is a bounded caller-supplied immutable Event-history fixture used only to exercise admission, duplicate and conflict semantics. It is not a durable Event repository or transport contract.

The P1.08 reconstruction manifest is an immutable derived view of already-governed references. It does not create canonical state, grant authority, provide a mutable projection, establish durable evidence storage, or pre-empt P1.09/P1.10 semantics.

The P1.09 Observation is bounded significant governed learning evidence with explicit `Unvalidated` epistemic status. It is authoritative only for the fact that the Observation was captured in its declared scope; it is not validated Knowledge, Organizational Memory, an approved standard, a production rule or an implementation of the RFC-0007 promotion lifecycle. Its negative guard does not pre-empt P1.10 fixture semantics or a later governed Knowledge implementation.

Python and `unittest` are used only as a reversible, zero-dependency vehicle for executable architecture fitness evidence. No Platform Capability becomes `Active`, and no production-readiness or full-platform conformance claim is created by these tests.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next roadmap work item

After P1.09 is completed and roadmap evidence is synchronized, the next dependency-ordered item is `P1.10 — Portable semantic fixture export`.