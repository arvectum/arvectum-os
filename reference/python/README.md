# Bounded Reference Implementation — Phase 1

Status: `Provisional implementation harness`
Scope: `Phase 1 / P1.01–P1.06`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001, RFC-0002, RFC-0003 and RFC-0005 `1.0.0`
Roadmap baseline: `2.0.2`

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

## Deliberately not decided

This harness does **not** establish a permanent package layout, programming-language contract, database, API, event broker, IAM provider, policy engine, deployment topology, persistent lineage store, Canonical Head/effective-version resolver, workflow engine, Product Contract, production role matrix or durable authorization-enforcement mechanism.

The P1.06 `current_record` argument is a bounded caller-supplied admitted-current fixture used only to exercise conflict detection against the exact version already pinned by the execution. It is not a canonical-head service, mutable projection authority or public resolution contract.

Python and `unittest` are used only as a reversible, zero-dependency vehicle for executable architecture fitness evidence. No Platform Capability becomes `Active`, and no production-readiness or full-platform conformance claim is created by these tests.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next roadmap work item

After P1.06 is completed and roadmap evidence is synchronized, the next dependency-ordered item is `P1.07 — Canonical Event admission and execution linkage`.
