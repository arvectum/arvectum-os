# Arvectum OS Phase 1 — Reference Implementation

Status: `Active`
Version: `1.0.1`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](ROADMAP.md)
Readiness baseline: [`docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`](../implementation/REFERENCE-IMPLEMENTATION-READINESS.md)

## 1. Purpose

This document is the canonical work-breakdown view for **Phase 1 — Reference Implementation** of Arvectum OS.

It decomposes the parent roadmap work item `First bounded executable slice` into stable roadmap-level task identifiers so that implementation work, project chats, commits and status updates can refer to the same ordered items without inventing local names.

This document is subordinate to the Constitution, Accepted RFCs, Accepted ADRs, approved governance artifacts and the parent Canonical Roadmap. It does not create new architecture or change Accepted RFC semantics.

## 2. Identifier rule

Phase 1 work items use the namespace `P1.<number>`.

Examples:

- `P1.01` — Organization scope and attributable Actor;
- `P1.02` — first Native Canonical Record version;
- `P1.03` — versioned Workflow baseline.

These identifiers are roadmap/work identifiers only. They are not RFC, ADR, issue, capability or conformance identifiers.

A task keeps its identifier even if its implementation wording is refined. A materially different task receives a new identifier rather than reusing an old one.

## 3. Phase 1 objective

Prove the smallest domain-neutral executable architectural spine of Arvectum OS using reversible implementation techniques before adding infrastructure.

The slice must demonstrate stable identity, immutable canonical versions, explicit Organization and authority gates, Governed Execution, canonical Event evidence, provenance, Observation non-promotion and implementation-neutral export semantics with executable fitness tests.

## 4. Phase 1 overview

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P1.01` | Organization scope and attributable Actor / Principal | 🟩 | `██████████ 100%` |
| `P1.02` | Native subject + first immutable Canonical Record version | 🟩 | `██████████ 100%` |
| `P1.03` | Versioned Workflow baseline | 🟦 | `░░░░░░░░░░ 0%` |
| `P1.04` | Execution Context + exact version pinning | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.05` | Authorization and Organizational Authority gates | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.06` | Governed Canonical Mutation + second immutable version | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.07` | Canonical Event admission and execution linkage | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.08` | Provenance, causation and reconstruction evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.09` | Observation creation without Knowledge promotion | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.10` | Portable semantic fixture export | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `██░░░░░░░░ 20%` |
| `P1.12` | Phase 1 bounded-slice closure review | ⬜ | `░░░░░░░░░░ 0%` |

Progress bars are planning indicators, not conformance or capability-lifecycle claims.

## 5. Work items

### P1.01 — Organization scope and attributable Actor / Principal

**Status:** 🟩 Complete

Prove explicit Organization scope and attributable Actor/Principal semantics without ambient tenant context or anonymous consequential execution.

Current repository evidence: implemented in `reference/python` with executable fitness tests.

### P1.02 — Native subject + first immutable Canonical Record version

**Status:** 🟩 Complete

Implemented one bounded domain-neutral `Native` canonical subject with:

- stable Subject Identity;
- first distinct immutable Version Identity;
- explicit Organization scope;
- explicit `Native` authority mode and authority scope;
- accountable architectural owner reference;
- attributable creation Actor and timezone-aware creation time;
- bounded provenance references;
- proportional integrity metadata for the in-memory reference representation;
- immutable in-memory payload and lifecycle state;
- no predecessor for the first admitted version.

The implementation intentionally rejects `External Reference` and `Governed Replica` in P1.02 because their required external-authority contracts are outside this work item. It does not introduce a database, durable persistence, Canonical Head resolver, public wire format or cryptographic integrity mechanism.

Repository evidence: `reference/python/arvectum_os_ref/canonical.py` and `reference/python/tests/test_p1_02_native_canonical_record.py`.

Executable validation for P1.01 + P1.02: `14` unit tests passed.

### P1.03 — Versioned Workflow baseline

**Status:** 🟦 Next

Represent one versioned domain-neutral Workflow that is permitted to update the reference subject while preserving stable identity and exact Workflow version semantics.

### P1.04 — Execution Context + exact version pinning

**Status:** ⬜ Planned

Start one Execution Context and pin the effective Workflow version and materially relied-upon input Version Identity.

### P1.05 — Authorization and Organizational Authority gates

**Status:** ⬜ Planned

Prove separately that:

- authentication/actor attribution does not imply authorization;
- authorization does not imply Organizational Authority;
- required unresolved gates fail closed.

### P1.06 — Governed Canonical Mutation + second immutable version

**Status:** ⬜ Planned

Perform one `CanonicalMutation` through Governed Execution and create a second immutable Canonical Record version without mutating the first.

Direct consequential canonical mutation outside the required Execution Context must be rejected.

### P1.07 — Canonical Event admission and execution linkage

**Status:** ⬜ Planned

Admit a canonical Event linked to the execution and resulting version while preserving append-only Event semantics and duplicate/conflict handling required by the readiness baseline.

### P1.08 — Provenance, causation and reconstruction evidence

**Status:** ⬜ Planned

Preserve causation, correlation and provenance references sufficient to reconstruct the bounded operation and identify the actor, workflow, inputs, execution, result and Event evidence.

### P1.09 — Observation creation without Knowledge promotion

**Status:** ⬜ Planned

Create an Observation from the execution outcome while proving that it does not become validated Knowledge, an approved standard or production behavior automatically.

### P1.10 — Portable semantic fixture export

**Status:** ⬜ Planned

Export the bounded governed state into a documented implementation-neutral semantic fixture that preserves relevant identities, versions, Organization scope, authority and relationships independently of the in-memory representation.

### P1.11 — Negative-path and architecture fitness tests

**Status:** 🟨 In progress

This is a cross-cutting task and progresses alongside `P1.01`–`P1.10`.

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

`P1.01` and `P1.02` now contribute executable negative-path and architecture-fitness coverage, including unresolved Organization scope, authentication non-authority, immutable identity/record values, Organization-consistent attribution, required Canonical Record envelope validation and fail-closed rejection of unsupported authority modes. The full matrix remains incomplete.

### P1.12 — Phase 1 bounded-slice closure review

**Status:** ⬜ Planned

Close the first bounded executable slice only after:

1. `P1.01`–`P1.10` are complete within the declared slice scope;
2. the applicable `P1.11` fitness matrix passes;
3. no product-domain semantics have leaked into shared reference modules;
4. no technology choice has crossed an ADR gate without the required ADR;
5. the implementation remains reversible and migration-friendly;
6. no capability is represented as `Active` or production-ready merely because the slice works;
7. the Canonical Roadmap is synchronized to the completed milestone.

## 6. Default order and parallelism

Default dependency-aware order:

```text
P1.01 ✅ Organization / Actor
   ↓
P1.02 ✅ Native subject + Canonical Record v1
   ↓
P1.03 🟦 Versioned Workflow
   ↓
P1.04 Execution Context + version pinning
   ↓
P1.05 Authorization + Organizational Authority gates
   ↓
P1.06 Canonical Mutation → immutable v2
   ↓
P1.07 Canonical Event
   ↓
P1.08 Provenance / reconstruction
   ↓
P1.09 Observation ≠ Knowledge
   ↓
P1.10 Portable semantic fixture
   ↓
P1.12 Closure review
```

`P1.11` fitness tests run continuously across the sequence rather than waiting until the end.

Bounded parallel work is permitted when dependencies remain explicit and the work does not prejudge unresolved architecture or technology choices.

## 7. ADR boundary

No new ADR is required merely because Phase 1 has begun.

An ADR becomes required before relying on a choice that crosses the ADR triggers established in `REFERENCE-IMPLEMENTATION-READINESS.md`, including material cross-module constraints, durable migration cost, stable public/cross-product interfaces, security/isolation enforcement choices or durable vendor/infrastructure dependencies.

## 8. Maintenance rule

Before updating Phase 1 status:

1. synchronize with the canonical repository;
2. verify the Constitution and RFC Index;
3. inspect the actual implementation/tests for the affected `P1.*` work item;
4. update this work breakdown and the parent Roadmap when the milestone materially changes overall delivery state.

Project chats and implementation commits SHOULD refer to the stable `P1.*` identifier together with the task name, for example:

> `P1.02 — Native subject + first immutable Canonical Record version`

This prevents neighboring chats from inventing competing task names or ambiguous ordering.
