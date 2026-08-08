# Arvectum OS Phase 1 — Reference Implementation

Status: `Active`
Version: `1.0.4`
Created: `2026-08-07`
Updated: `2026-08-08`
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
| `P1.03` | Versioned Workflow baseline | 🟩 | `██████████ 100%` |
| `P1.04` | Execution Context + exact version pinning | 🟩 | `██████████ 100%` |
| `P1.05` | Authorization and Organizational Authority gates | 🟩 | `██████████ 100%` |
| `P1.06` | Governed Canonical Mutation + second immutable version | 🟦 | `░░░░░░░░░░ 0%` |
| `P1.07` | Canonical Event admission and execution linkage | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.08` | Provenance, causation and reconstruction evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.09` | Observation creation without Knowledge promotion | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.10` | Portable semantic fixture export | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `█████░░░░░ 50%` |
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

### P1.03 — Versioned Workflow baseline

**Status:** 🟩 Complete

Implemented one bounded domain-neutral governed Workflow definition with:

- stable Workflow Subject Identity;
- distinct immutable Workflow Version Identity;
- a `Native` Canonical Record envelope for the Workflow version;
- explicit Organization scope, accountable owner, lifecycle and provenance;
- one immutable semantic operation targeting the exact P1.02 reference Subject Identity and semantic type;
- RFC-0005 `CanonicalMutation` side-effect classification;
- fail-closed Organization-scope validation;
- explicit non-equivalence between Workflow operation declaration and authorization, Organizational Authority or consequential approval.

P1.03 does not start an Execution Context and does not mutate canonical state. It introduces no workflow engine, scheduler, queue, public protocol or durable workflow registry.

Repository evidence: `reference/python/arvectum_os_ref/workflow.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_03_versioned_workflow.py`.

### P1.04 — Execution Context + exact version pinning

**Status:** 🟩 Complete

Implemented one bounded domain-neutral initial Execution Context with:

- stable Execution Subject Identity and a distinct immutable initial Execution Version Identity;
- a `Native` `platform.execution-context` Canonical Record envelope, consistent with RFC-0002;
- explicit Organization scope and attributable initiating Actor;
- initial `AwaitingGate` lifecycle state so unresolved P1.05 governance gates remain explicit and fail closed rather than being treated as passed;
- an exact immutable pin to the Workflow Subject Identity and the supplied effective Workflow Version Identity;
- an exact immutable pin to the materially relied-upon P1.02 Canonical Record Subject Identity and Version Identity;
- explicit attribution to the single scoped `CanonicalMutation` operation declared by the pinned Workflow version;
- provenance references containing the exact Workflow and material input versions;
- fail-closed validation for Organization mismatch, operation mismatch, malformed version pins and duplicate material input Version Identities.

Executable evidence proves that a later Workflow or material-input version under the same Subject Identity does not change the Version Identity already pinned by the started execution. P1.04 therefore records exact governed reliance rather than depending on a mutable `current` lookup.

P1.04 does not evaluate authorization, Organizational Authority or consequential approval; does not perform the P1.06 canonical mutation; and does not introduce a Canonical Head/effective-version resolver, Event, workflow engine, durable persistence or public protocol.

Repository evidence: `reference/python/arvectum_os_ref/execution.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_04_execution_context.py`.

Canonical validation through P1.04 remains the previously recorded `31` unit-test baseline, including `10` P1.04 tests.

### P1.05 — Authorization and Organizational Authority gates

**Status:** 🟩 Complete

Implemented two independent domain-neutral governed gate boundaries for the exact P1.04 execution attempt:

- `Authorization` and `OrganizationalAuthority` are separate gate kinds and passing one does not imply passing the other;
- authentication/Actor attribution alone leaves both gates unresolved;
- each gate decision is an immutable `Native` Canonical Record carrying explicit `Allow` or `Deny` outcome rather than ambient permission state;
- absent required gate evidence fails closed;
- explicit `Deny` blocks the bounded transition even when the other gate allows;
- each gate decision is bound to the exact Organization, initiating Principal, `AwaitingGate` Execution Subject/Version Identity, pinned Workflow Version Identity, operation and material target Subject/Version Identity;
- each decision preserves an explicit governed basis reference in provenance without defining a production IAM provider, policy engine, role matrix or delegation catalog;
- only two independently valid explicit `Allow` decisions admit a new immutable `Ready` Execution Context version under the same Execution Subject Identity;
- the `Ready` version preserves predecessor lineage, exact Workflow/material-input pins and exact gate-decision Version Identities;
- gate pins retain the explicit `Allow` state so a forged `Ready` context containing a `Deny` decision pin fails validation;
- no target Canonical Record mutation occurs in P1.05.

`Ready` is scoped to the two gates exercised by this bounded first-slice scenario. It does not collapse RFC-0005 data-governance, validation, consequential-approval or product-specific gates into Authorization/Organizational Authority and does not imply they are globally unnecessary or satisfied.

The fixture builder records already-supplied governed decision evidence. It does not issue real permissions, create delegation or establish Organizational Authority. The Proposed Decision Authority Policy remains non-normative and is not implemented as an approved authority model.

Repository evidence: `reference/python/arvectum_os_ref/gates.py`, the P1.05 extensions in `reference/python/arvectum_os_ref/execution.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_05_authorization_authority_gates.py`.

P1.05 adds `12` executable fitness tests covering gate independence, deny-by-default behavior, explicit deny, exact decision scope, governed basis provenance, immutable explicit-Allow pins, Ready-version lineage, forged Ready rejection and target non-mutation. A bounded current-state smoke validation passes the core P1.05 transition invariants.

### P1.06 — Governed Canonical Mutation + second immutable version

**Status:** 🟦 Next

Perform one `CanonicalMutation` through the `Ready` Governed Execution and create a second immutable Canonical Record version without mutating the first.

Direct consequential canonical mutation outside the required Execution Context must be rejected. P1.06 must consume the exact P1.04 Workflow/material-input pins and the P1.05 gate-decision evidence rather than silently re-resolving or bypassing them.

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

`P1.01` through `P1.05` now contribute executable negative-path and architecture-fitness coverage. P1.05 adds explicit authentication ≠ authorization, authorization ≠ Organizational Authority, authority ≠ authorization, unresolved/denied fail-closed behavior, exact gate scope and version attribution, explicit-Allow pin validation, immutable gate evidence, Execution Context governance-significant versioning and proof that passing P1.05 gates still does not mutate the P1.02 target. The full matrix remains incomplete.

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
P1.03 ✅ Versioned Workflow
   ↓
P1.04 ✅ Execution Context + version pinning
   ↓
P1.05 ✅ Authorization + Organizational Authority gates
   ↓
P1.06 🟦 Canonical Mutation → immutable v2
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

P1.05 remains below that gate: its decision records and evaluator are bounded, reversible, in-memory, domain-neutral and non-public. They do not select an IAM provider, policy engine, durable authorization-enforcement mechanism, tenant-isolation technology or production authority-administration model. A real enforcement choice that materially constrains those concerns will require the applicable ADR/governance evidence before reliance.

## 8. Maintenance rule

Before updating Phase 1 status:

1. synchronize with the canonical repository;
2. verify the Constitution and RFC Index;
3. inspect the actual implementation/tests for the affected `P1.*` work item;
4. update this work breakdown and the parent Roadmap when the milestone materially changes overall delivery state.

Project chats and implementation commits SHOULD refer to the stable `P1.*` identifier together with the task name, for example:

> `P1.02 — Native subject + first immutable Canonical Record version`

This prevents neighboring chats from inventing competing task names or ambiguous ordering.
