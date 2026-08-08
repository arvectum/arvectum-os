# Arvectum OS Phase 1 — Reference Implementation

Status: `Active`
Version: `1.0.7`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](ROADMAP.md)
Readiness baseline: [`docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`](../implementation/REFERENCE-IMPLEMENTATION-READINESS.md)

## 1. Purpose

This document is the canonical work-breakdown view for **Phase 1 — Reference Implementation** of Arvectum OS.

It decomposes the first bounded executable slice into stable `P1.*` work identifiers. It is subordinate to the Constitution, Accepted RFCs, Accepted ADRs, approved governance artifacts and the parent Canonical Roadmap; it does not create new architecture or change Accepted RFC semantics.

## 2. Identifier rule

Phase 1 work items use the roadmap namespace `P1.<number>`. These identifiers are not RFC, ADR, issue, capability or conformance identifiers. A task keeps its identifier when wording is refined; a materially different task receives a new identifier.

## 3. Phase 1 objective

Prove the smallest domain-neutral executable architectural spine of Arvectum OS using reversible implementation techniques before adding infrastructure.

The slice must demonstrate stable identity, immutable canonical versions, explicit Organization and authority gates, Governed Execution, canonical Event evidence, provenance/reconstruction, Observation non-promotion and implementation-neutral export semantics with executable fitness tests.

## 4. Phase 1 overview

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P1.01` | Organization scope and attributable Actor / Principal | 🟩 | `██████████ 100%` |
| `P1.02` | Native subject + first immutable Canonical Record version | 🟩 | `██████████ 100%` |
| `P1.03` | Versioned Workflow baseline | 🟩 | `██████████ 100%` |
| `P1.04` | Execution Context + exact version pinning | 🟩 | `██████████ 100%` |
| `P1.05` | Authorization and Organizational Authority gates | 🟩 | `██████████ 100%` |
| `P1.06` | Governed Canonical Mutation + second immutable version | 🟩 | `██████████ 100%` |
| `P1.07` | Canonical Event admission and execution linkage | 🟩 | `██████████ 100%` |
| `P1.08` | Provenance, causation and reconstruction evidence | 🟩 | `██████████ 100%` |
| `P1.09` | Observation creation without Knowledge promotion | 🟦 | `░░░░░░░░░░ 0%` |
| `P1.10` | Portable semantic fixture export | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `███████░░░ 70%` |
| `P1.12` | Phase 1 bounded-slice closure review | ⬜ | `░░░░░░░░░░ 0%` |

Progress bars are planning indicators, not conformance or capability-lifecycle claims.

## 5. Work items

### P1.01 — Organization scope and attributable Actor / Principal

**Status:** 🟩 Complete

Proves explicit Organization scope and attributable Actor/Principal semantics without ambient tenant context or anonymous consequential execution.

Repository evidence: `reference/python` and executable fitness tests.

### P1.02 — Native subject + first immutable Canonical Record version

**Status:** 🟩 Complete

Implements one bounded domain-neutral `Native` subject with stable Subject Identity, distinct immutable Version Identity, explicit Organization/authority scope, accountable owner, attributable creation Actor/time, bounded provenance, proportional in-memory integrity metadata and no predecessor. External authority modes, durable persistence, Canonical Head resolution, public wire format and cryptographic sealing remain outside this work item.

Repository evidence: `reference/python/arvectum_os_ref/canonical.py` and `reference/python/tests/test_p1_02_native_canonical_record.py`.

### P1.03 — Versioned Workflow baseline

**Status:** 🟩 Complete

Implements one immutable domain-neutral Workflow version with stable Workflow Identity, explicit lifecycle/provenance and one scoped `CanonicalMutation` operation. Workflow declaration does not imply authorization, Organizational Authority or approval and introduces no workflow engine, queue, scheduler or durable registry.

Repository evidence: `reference/python/arvectum_os_ref/workflow.py` and `reference/python/tests/test_p1_03_versioned_workflow.py`.

### P1.04 — Execution Context + exact version pinning

**Status:** 🟩 Complete

Implements one immutable initial `AwaitingGate` Execution Context with stable Execution Identity, exact Workflow/material-input version pins and attributable Actor/Organization context. Later versions under the same Subject Identities do not alter already-pinned reliance.

Repository evidence: `reference/python/arvectum_os_ref/execution.py` and `reference/python/tests/test_p1_04_execution_context.py`.

Canonical validation through P1.04 remains the previously recorded `31`-test baseline.

### P1.05 — Authorization and Organizational Authority gates

**Status:** 🟩 Complete

Implements two separate immutable governed decisions for `Authorization` and `OrganizationalAuthority`. Missing/denied evidence fails closed; neither gate implies the other; only two exact scoped `Allow` decisions create the next immutable `Ready` Execution Context version. Decision builders record supplied fixture evidence and do not issue real permission, delegation or organizational authority.

Repository evidence: `reference/python/arvectum_os_ref/gates.py`, `reference/python/arvectum_os_ref/execution.py`, and `reference/python/tests/test_p1_05_authorization_authority_gates.py`.

P1.05 adds `12` focused executable fitness tests.

### P1.06 — Governed Canonical Mutation + second immutable version

**Status:** 🟩 Complete

Executes the bounded `CanonicalMutation` only through the exact immutable `Ready` execution. It consumes exact Workflow/material-input/gate versions, rejects stale-current conflict instead of overwriting newer state, creates immutable target v2 with v1 as predecessor, preserves v1 unchanged, and records the exact canonical effect in a new immutable terminal `Succeeded` Execution Context version.

Repository evidence: `reference/python/arvectum_os_ref/mutation.py`, `reference/python/arvectum_os_ref/execution.py`, and `reference/python/tests/test_p1_06_governed_canonical_mutation.py`.

P1.06 adds `13` focused executable fitness tests.

### P1.07 — Canonical Event admission and execution linkage

**Status:** 🟩 Complete

Distinguishes transient Event receipt from canonical admission; admits one immutable append-only `Native` Event linked to the exact terminal P1.06 execution and result; preserves event type/schema/source/time/actor/classification/provenance/integrity context; handles duplicate delivery idempotently; rejects conflicting Event Identity/Version Identity reuse; and fails closed on wrong execution/result or Organization linkage. Correlation uses the stable Execution Identity and causation the exact terminal Execution Context version.

Repository evidence: `reference/python/arvectum_os_ref/events.py` and `reference/python/tests/test_p1_07_canonical_event_admission.py`.

P1.07 adds `14` focused executable fitness tests.

### P1.08 — Provenance, causation and reconstruction evidence

**Status:** 🟩 Complete

Implemented a bounded read-only reconstruction boundary over the exact immutable P1.02–P1.07 evidence:

- `ReconstructionEvidence` is a frozen derived manifest and is explicitly not Canonical Record state or an authority source;
- reconstruction identifies the initiating Principal and Organization, exact Workflow version, exact material input version, both governed gate-decision versions and governed basis references, all three governance-significant Execution Context versions, exact canonical result version and exact admitted Event version;
- `AwaitingGate → Ready → Succeeded` Execution Context predecessor lineage is verified without rewriting history;
- exact Workflow/material-input pins and the stable semantic operation must remain unchanged across the execution lineage;
- both Authorization and Organizational Authority evidence must be the exact scoped explicit-`Allow` decisions evaluated against the exact `AwaitingGate` version;
- result provenance must preserve input, `Ready` execution, Workflow and both gate-decision versions;
- terminal execution provenance must preserve the exact input, Workflow, gate decisions and result version;
- Event provenance must preserve the initiating actor, exact terminal execution and exact result version;
- correlation remains the stable Execution Subject Identity while causation remains the exact terminal Execution Context Version Identity; one is not treated as the other or as authority;
- wrong Workflow/input/execution/gate/Event versions, broken predecessor lineage, incomplete provenance, actor drift and incorrect Event correlation/causation/result linkage fail closed;
- repeated reconstruction is deterministic and observational: it does not replay the mutation, create a new Event or mutate sealed execution/result/Event history.

Repository evidence: `reference/python/arvectum_os_ref/provenance.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_08_provenance_reconstruction.py`.

P1.08 adds `15` focused architecture-fitness tests. It does not define durable provenance storage, a public provenance API, projection authority, replay-triggered consequential execution, Observation/Knowledge semantics or the P1.10 portable fixture representation.

### P1.09 — Observation creation without Knowledge promotion

**Status:** 🟦 Next

Create an Observation from the execution outcome while proving that it does not become validated Knowledge, an approved standard or production behavior automatically.

### P1.10 — Portable semantic fixture export

**Status:** ⬜ Planned

Export the bounded governed state into a documented implementation-neutral semantic fixture that preserves relevant identities, versions, Organization scope, authority and relationships independently of the in-memory representation.

### P1.11 — Negative-path and architecture fitness tests

**Status:** 🟨 In progress

This cross-cutting task progresses alongside `P1.01`–`P1.10`.

The bounded slice must include applicable executable tests proving at least:

- unresolved Organization scope fails closed;
- authentication alone does not authorize mutation;
- authorization alone does not satisfy Organizational Authority;
- direct consequential canonical mutation outside Governed Execution is rejected;
- existing canonical versions cannot be mutated in place;
- duplicate Event delivery does not create a second occurrence;
- conflicting immutable Event content is rejected or quarantined;
- replay does not create new consequential side effects;
- Observation cannot be consumed as validated Knowledge without promotion;
- projection/index results cannot substitute for exact governed Version Identity reliance.

`P1.01` through `P1.08` now contribute executable negative-path and architecture-fitness coverage. P1.08 adds exact reconstruction checks for actor continuity, Workflow/input/gate/execution/result/Event version linkage, provenance completeness and explicit correlation-versus-causation semantics while proving the reconstruction view itself does not mutate sealed history. Replay, Observation/Knowledge and projection portions remain incomplete.

### P1.12 — Phase 1 bounded-slice closure review

**Status:** ⬜ Planned

Close the bounded slice only after:

1. `P1.01`–`P1.10` are complete within declared scope;
2. the applicable `P1.11` fitness matrix passes;
3. no product-domain semantics have leaked into shared reference modules;
4. no technology choice has crossed an ADR gate without the required ADR;
5. the implementation remains reversible and migration-friendly;
6. no capability is represented as `Active` or production-ready merely because the slice works;
7. the Canonical Roadmap is synchronized to the completed milestone.

## 6. Default order and parallelism

```text
P1.01 ✅ Organization / Actor
   ↓
P1.02 ✅ Native subject + Canonical Record v1
   ↓
P1.03 ✅ Versioned Workflow
   ↓
P1.04 ✅ Execution Context + version pinning
   ↓
P1.05 ✅ Authorization + Organizational Authority gates
   ↓
P1.06 ✅ Canonical Mutation → immutable v2
   ↓
P1.07 ✅ Canonical Event
   ↓
P1.08 ✅ Provenance / reconstruction
   ↓
P1.09 🟦 Observation ≠ Knowledge
   ↓
P1.10 ⬜ Portable semantic fixture
   ↓
P1.12 ⬜ Closure review
```

`P1.11` fitness tests run continuously. Bounded parallel work is permitted when dependencies remain explicit and no unresolved architecture or technology decision is prejudged.

## 7. ADR boundary

No new ADR is required merely because Phase 1 has begun. An ADR becomes required before relying on a materially constraining cross-module, durable, public, security/isolation or vendor/infrastructure choice under `REFERENCE-IMPLEMENTATION-READINESS.md`.

P1.05 remains below the ADR gate because it selects no production IAM/policy/authority-administration mechanism.

P1.06 remains below the ADR gate because it selects no durable persistence, Canonical Head resolver, transaction/concurrency technology, public mutation protocol or durable evidence-integrity mechanism.

P1.07 remains below the ADR gate because it uses caller-supplied immutable in-memory Event history and selects no durable Event store, broker, outbox/inbox, schema registry, delivery protocol or public Event contract.

P1.08 remains below the ADR gate because its reconstruction manifest is derived, immutable, in-memory and non-public. It introduces no durable lineage store, graph database, provenance service, projection technology, public serialization contract or evidence-integrity mechanism and therefore does not create a constraining cross-module dependency.

## 8. Maintenance rule

Before updating Phase 1 status:

1. synchronize with the canonical repository;
2. verify the Constitution and RFC Index;
3. inspect actual implementation/tests for the affected `P1.*` item;
4. update this work breakdown and the parent Roadmap when the milestone materially changes overall delivery state.

Project chats and implementation commits SHOULD use the stable `P1.*` identifier together with the task name. This prevents neighboring chats from inventing competing task names or ambiguous ordering.
