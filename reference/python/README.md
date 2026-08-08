# Bounded Reference Implementation — Phase 1

Status: `Provisional implementation harness`
Scope: `Phase 1 / P1.01–P1.08`
Architecture baseline: Constitution `1.2.0`; Accepted RFC-0001, RFC-0002, RFC-0003, RFC-0005 and RFC-0006 `1.0.0`
Roadmap baseline: `2.0.4`

This directory contains the bounded executable reference implementation defined by `docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`.

The harness is intentionally domain-neutral, in-memory, reversible and non-public. It proves Accepted semantics without selecting durable persistence, a broker, workflow engine, IAM provider, public API or deployment topology.

## P1.01 — Organization scope and attributable Actor / Principal

Implemented and merged:

1. one Organization scope is explicit and has no ambient/default fallback;
2. one acting Principal is attributable through stable Identity semantics;
3. acting-on-behalf-of context preserves actual and represented Principals;
4. Identity values do not encode roles, permissions or Organizational Authority;
5. authentication evidence is reference-only and is not authorization or Organizational Authority.

## P1.02 — Native subject + first immutable Canonical Record version

Implemented one domain-neutral `Native` canonical subject with stable Subject Identity, distinct immutable Version Identity, explicit Organization/authority scope, accountable owner, attributable creation Actor/time, bounded provenance, proportional in-memory integrity metadata and no predecessor.

`External Reference` and `Governed Replica` remain outside this bounded item because their external-authority contracts are not exercised here.

## P1.03 — Versioned Workflow baseline

Implemented one immutable domain-neutral Workflow version with stable Workflow Identity, explicit lifecycle/provenance and one `CanonicalMutation` operation targeting the exact P1.02 subject. Declaring the operation grants no authorization, Organizational Authority or approval.

## P1.04 — Execution Context + exact version pinning

Implemented one `AwaitingGate` Execution Context version that pins the exact Workflow and material Canonical Record versions before consequential reliance. A later version under the same Subject Identity does not alter those pins.

## P1.05 — Authorization and Organizational Authority gates

Implemented separate immutable `Authorization` and `OrganizationalAuthority` decision evidence. Missing or denied evidence fails closed; neither gate implies the other; only two exact scoped `Allow` decisions create the next immutable `Ready` Execution Context version. The fixture builders record supplied governed decisions but do not issue real permissions or authority.

## P1.06 — Governed Canonical Mutation + second immutable version

Implemented one `CanonicalMutation` through the exact `Ready` execution. It consumes the exact Workflow/material-input/gate versions, rejects stale-current conflict instead of overwriting newer state, creates immutable target v2 with v1 as predecessor, preserves v1 unchanged and creates a terminal immutable `Succeeded` Execution Context version pinning the exact canonical effect.

## P1.07 — Canonical Event admission and execution linkage

Implemented transient receipt versus canonical Event admission, one append-only `Native` Event linked to the exact terminal execution and result version, explicit event type/schema/source/time/actor/classification/provenance/integrity context, idempotent duplicate delivery, and fail-closed conflicting Event Identity/Version Identity reuse. Correlation preserves the stable Execution Identity; causation preserves the exact terminal Execution Context Version Identity.

## P1.08 — Provenance, causation and reconstruction evidence

Implemented a read-only immutable reconstruction boundary over the exact P1.02–P1.07 evidence:

- `ReconstructionEvidence` is a frozen derived manifest, not a Canonical Record and not an authority source;
- reconstruction identifies the initiating Principal and Organization, exact Workflow version, exact material input version, both governed gate-decision versions and their basis references, all three governance-significant Execution Context versions, the exact canonical result version and the exact admitted Event version;
- the manifest preserves Event type/schema together with explicit correlation and causation references;
- correlation is validated as the stable Execution Subject Identity while causation is validated as the exact terminal `Succeeded` Execution Context Version Identity;
- `AwaitingGate → Ready → Succeeded` predecessor lineage is verified without rewriting any execution version;
- result lineage/provenance must preserve the exact input, Ready execution, Workflow and gate-decision versions;
- terminal execution provenance must preserve the exact material input, Workflow, gate decisions and result version;
- Event provenance must preserve the actor, exact terminal execution and exact result version;
- wrong Workflow/input/execution/gate/Event versions, broken lineage, incomplete provenance, actor drift or incorrect correlation/causation fail closed;
- repeated reconstruction is observational and does not replay the mutation, create another Event or mutate the sealed terminal execution/result/Event history.

Repository evidence: `reference/python/arvectum_os_ref/provenance.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_08_provenance_reconstruction.py`.

P1.08 adds `15` focused architecture-fitness tests. It deliberately does **not** define replay execution semantics, a portable serialization/fixture contract, Observation/Knowledge promotion, a projection/index authority model, durable lineage persistence or a public provenance API.

## Deliberately not decided

This harness does **not** establish a permanent package layout, programming-language contract, database, API, event broker, durable event store, outbox/inbox strategy, delivery protocol, schema registry, IAM provider, policy engine, deployment topology, persistent lineage store, Canonical Head/effective-version resolver, workflow engine, Product Contract, production role matrix or durable authorization-enforcement mechanism.

The P1.06 `current_record` argument remains a bounded caller-supplied admitted-current fixture for exact-version conflict detection. It is not a canonical-head service or projection authority.

The P1.07 `admitted_events` tuple remains bounded caller-supplied immutable Event history. It is not a durable Event repository or transport contract.

The P1.08 reconstruction manifest is an immutable derived view of already-governed references. It does not create canonical state, grant authority, provide a mutable projection, establish durable evidence storage, or pre-empt P1.09/P1.10 semantics.

Python and `unittest` remain only a reversible, zero-dependency vehicle for executable architecture fitness evidence. No Platform Capability becomes `Active`, and no production-readiness or full-platform conformance claim is created by these tests.

## Run

```sh
cd reference/python
python -m unittest discover -s tests -v
```

## Next roadmap work item

After P1.08 completion and roadmap synchronization, the next dependency-ordered item is `P1.09 — Observation creation without Knowledge promotion`.
