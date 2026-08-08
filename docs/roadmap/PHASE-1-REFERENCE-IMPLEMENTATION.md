# Arvectum OS Phase 1 — Reference Implementation

Status: `Active`
Version: `1.0.9`
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
| `P1.06` | Governed Canonical Mutation + second immutable version | 🟩 | `██████████ 100%` |
| `P1.07` | Canonical Event admission and execution linkage | 🟩 | `██████████ 100%` |
| `P1.08` | Provenance, causation and reconstruction evidence | 🟩 | `██████████ 100%` |
| `P1.09` | Observation creation without Knowledge promotion | 🟩 | `██████████ 100%` |
| `P1.10` | Portable semantic fixture export | 🟩 | `██████████ 100%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `████████░░ 80%` |
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

P1.05 adds `12` executable fitness tests covering gate independence, deny-by-default behavior, explicit deny, exact decision scope, governed basis provenance, immutable explicit-Allow pins, Ready-version lineage, forged Ready rejection and target non-mutation.

### P1.06 — Governed Canonical Mutation + second immutable version

**Status:** 🟩 Complete

Implemented one bounded domain-neutral `CanonicalMutation` through the exact immutable `Ready` Governed Execution admitted by P1.05:

- direct consequential canonical mutation without an explicit Execution Context fails closed;
- an `AwaitingGate` execution cannot perform the mutation;
- the mutation consumes the exact Workflow Subject/Version pin established by P1.04 and verifies that the pinned Workflow version declares the exact scoped `CanonicalMutation` operation;
- the mutation consumes the exact immutable Authorization and Organizational Authority `Allow` decision versions already pinned by the `Ready` execution rather than re-resolving or replacing them;
- the caller-supplied admitted current target must still equal the exact material-input Version Identity pinned before consequential reliance;
- if another current target version is supplied under the same Subject Identity, the mutation raises an explicit canonical conflict instead of silently overwriting newer state;
- the resulting target version preserves the stable P1.02 Subject Identity, receives a distinct immutable Version Identity and names P1.02 v1 as its exact predecessor;
- P1.02 v1 remains unchanged and immutable;
- result provenance preserves the exact input version, `Ready` execution version, Workflow version and both gate-decision versions relied upon;
- because canonical state change is governance-significant under RFC-0005, successful mutation creates a new immutable terminal `Succeeded` Execution Context version under the same Execution Subject Identity;
- the `Succeeded` execution preserves predecessor lineage, exact Workflow/material-input/gate pins and adds one exact canonical-effect Version pin;
- canonical Event admission is deliberately not performed in P1.06 and remains P1.07 scope.

The bounded `current_record` argument is conflict-check evidence supplied by the in-memory harness. It is not a Canonical Head resolver, projection authority, public API or persistence contract.

Repository evidence: `reference/python/arvectum_os_ref/mutation.py`, the P1.06 extensions in `reference/python/arvectum_os_ref/execution.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_06_governed_canonical_mutation.py`.

P1.06 adds `13` executable fitness tests covering governed-entry enforcement, immutable-version lineage, exact pinned Workflow/gate evidence, conflict detection, Organization/version constraints, provenance, terminal execution effect pinning and explicit non-preemption of P1.07 Event admission.

### P1.07 — Canonical Event admission and execution linkage

**Status:** 🟩 Complete

Implemented one bounded domain-neutral canonical Event admission boundary for the completed P1.06 mutation:

- transient Event receipt is distinct from canonical Event admission;
- the admitted Event is an RFC-0002 Canonical Record specialization with stable Event Identity and one immutable Version Identity;
- the Event has no predecessor and therefore preserves the normal single-version append-only Event model;
- the bounded Event uses `Native` authority for the Arvectum OS governed observation and preserves explicit event type/schema, source, occurrence/admission times, producer/initiation attribution, classification/access, provenance and integrity metadata;
- admission consumes the exact P1.06 `CanonicalMutationResult` and does not re-resolve mutable execution or target state;
- the Event links to the exact terminal `Succeeded` Execution Subject/Version Identity and exact resulting target Subject/Version Identity;
- the terminal P1.06 Execution Context remains sealed and is not mutated after success merely to add Event state;
- duplicate delivery of the same immutable Event representation is idempotent and returns the already-admitted occurrence;
- duplicate delivery does not repeat the canonical mutation or create a second Event occurrence;
- reuse of an admitted Event Identity with materially different immutable content is rejected without rewriting history;
- reuse of an immutable Event Version Identity by another Event is rejected;
- wrong terminal-execution linkage, wrong resulting-version linkage and cross-Organization linkage fail closed;
- broader provenance graph and reconstruction evidence remain P1.08 scope.

The bounded `admitted_events` tuple is caller-supplied immutable history for the reference harness. It is not a broker, event store, outbox/inbox mechanism, schema registry, public Event API or transport guarantee.

Repository evidence: `reference/python/arvectum_os_ref/events.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_07_canonical_event_admission.py`.

P1.07 adds `14` focused architecture-fitness tests for receipt/admission separation, immutable Event semantics, exact execution/result linkage, duplicate/conflict handling, Organization scope and preservation of sealed execution/result evidence.

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

**Status:** 🟩 Complete

Implemented one significant, domain-neutral RFC-0007 Observation over the exact P1.06–P1.08 governed evidence:

- Observation remains an RFC-0007 semantic role represented through the existing RFC-0002 `CanonicalRecord` envelope and does not become a sixth Kernel primitive;
- the bounded Observation has a stable Observation Subject Identity, distinct immutable initial Version Identity, explicit Organization scope, `Native` authority limited to `platform.learning/observation`, accountable owner, attributable Actor and `Captured` lifecycle state;
- the Observation pins the exact admitted P1.07 Event version, terminal `Succeeded` P1.06 Execution Context version and exact resulting canonical-effect version already verified by P1.08;
- reconstruction provenance and initiating-Principal attribution are preserved rather than replaced by an inferred or mutable current-state lookup;
- epistemic status is explicitly `Unvalidated`, and integrity metadata records `knowledge-promotion = not-performed`;
- `require_explicit_knowledge_promotion` is a fail-closed negative-path guard: P1.09 exposes no successful Knowledge-admission path and refuses validated-Knowledge reliance without an explicit RFC-0007 promotion lifecycle;
- Observation creation is deterministic and observational with respect to prior governed evidence: it does not mutate the Workflow, target versions, sealed terminal Execution Context or admitted Event and does not change an approved standard, policy, Workflow or production behavior;
- wrong Event, terminal Execution or canonical-effect versions, changed Event semantics and incomplete reconstruction provenance fail closed;
- P1.09 does not create Organizational Memory, a Knowledge Candidate, validated Knowledge, an Improvement Proposal or a self-modifying production path and does not pre-empt the P1.10 portable-fixture representation.

Repository evidence: `reference/python/arvectum_os_ref/observation.py`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_09_observation_non_promotion.py`.

P1.09 adds `14` focused architecture-fitness tests. PR-time `Reference Python CI` completed successfully with the full reference suite: `99` tests, `OK`.

### P1.10 — Portable semantic fixture export

**Status:** 🟩 Complete

Implemented one bounded implementation-neutral portability representation over the exact P1.02–P1.09 governed state:

- the exporter emits deterministic, human-readable UTF-8 JSON through an explicit semantic mapping rather than Python `repr`, pickle, dataclass field dumping or object-graph layout;
- every Identity preserves `namespace`, `value` and `scope` independently, while materially significant references explicitly distinguish stable `subject`, exact immutable `version` and bounded `governed-identity` roles;
- the fixture preserves the explicit Organization and attributable Actor context plus all ten Canonical Record versions in the bounded slice: material input v1, Workflow v1, two gate decisions, three Execution Context versions, target v2, admitted Event and captured Observation;
- each exported Canonical Record envelope preserves semantic/schema version, Organization, Native authority mode/scope, accountable owner, creation Actor/time, provenance, integrity metadata, payload, lifecycle and predecessor Version Identity where present;
- type-specific sections preserve Workflow operation semantics, separate Authorization/Organizational Authority outcomes and basis references, exact Execution workflow/input/gate/effect pins, Event type/schema/source/times/classification/access plus execution/result/correlation/causation references, and Observation source/effect pins;
- `semantic_links` preserve already-existing relationship/reference meaning such as predecessor lineage, exact version reliance, Event correlation/causation and Observation sources while explicitly declaring `canonical_typed_relationship = false`; P1.10 does not fabricate `platform.relationship` Canonical Records;
- the P1.08 reconstruction manifest remains explicitly `derived-non-canonical` and the fixture itself declares `canonical_authority = false`, `public_compatibility_contract = false` and `production_export_endpoint = false`;
- the P1.09 Observation remains `Unvalidated` with `knowledge_promotion = not-performed`; export creates no `platform.knowledge` record and no promotion path;
- the portability section records explicit omissions, no non-exportable dependencies for the synthetic fixture, and that the reference exporter is not a real-data export authorization mechanism;
- export re-validates the exact P1.08 reconstruction and exact P1.09 Observation before serialization and fails closed on mixed/stale evidence or duplicate exported Version Identities;
- repeated export is deterministic and observational: it does not replay the mutation, create canonical state, issue authority or mutate sealed source objects.

Repository evidence: `reference/python/arvectum_os_ref/portability.py`, `reference/python/PORTABLE-SEMANTIC-FIXTURE.md`, package exports in `reference/python/arvectum_os_ref/__init__.py`, and `reference/python/tests/test_p1_10_portable_semantic_fixture.py`.

P1.10 adds `16` focused portability and negative-path fitness tests. PR-time `Reference Python CI` run `#9` completed successfully; together with the prior `99` tests, the full reference suite now contains `115` passing tests.

P1.10 remains a bounded reference fixture rather than a full RFC-0003 production portability/conformance claim, service-termination package, public wire format, stable organization-wide portability standard or `Active` Platform Capability.

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

`P1.01` through `P1.10` now contribute executable negative-path and architecture-fitness coverage. P1.05 adds explicit authentication ≠ authorization, authorization ≠ Organizational Authority, authority ≠ authorization, unresolved/denied fail-closed behavior, exact gate scope and version attribution, explicit-Allow pin validation and immutable gate evidence. P1.06 adds direct-mutation rejection outside the required `Ready` Execution Context, preservation of the immutable first target version, exact Workflow/gate version consumption, stale-current canonical conflict detection and proof that successful canonical state change is represented by a new immutable target version plus a governance-significant terminal Execution Context version. P1.07 adds receipt/admission separation, duplicate-delivery idempotency, conflicting Event Identity/Version Identity rejection, exact execution/result linkage, cross-Organization fail-closed behavior and proof that Event admission does not mutate the sealed terminal execution or repeat the canonical effect. P1.08 adds exact reconstruction checks for actor continuity, Workflow/input/gate/execution/result/Event version linkage, provenance completeness and explicit correlation-versus-causation semantics while proving the reconstruction view itself does not mutate sealed history. P1.09 adds explicit Observation ≠ Knowledge enforcement, exact source-version pinning, provenance validation, immutability and proof that Observation capture does not alter standards, Workflows or prior governed outcomes. P1.10 adds implementation-neutral JSON parsing, exact exported Version-Identity coverage, explicit subject/version reference roles, non-authoritative derived links/reconstruction, Observation non-promotion preservation, deterministic export and fail-closed rejection of stale reconstruction/Observation state. Replay side-effect-safety and projection/index non-authority portions of the matrix remain incomplete.

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
P1.06 ✅ Canonical Mutation → immutable v2
   ↓
P1.07 ✅ Canonical Event
   ↓
P1.08 ✅ Provenance / reconstruction
   ↓
P1.09 ✅ Observation ≠ Knowledge
   ↓
P1.10 ✅ Portable semantic fixture
   ↓
P1.12 Closure review
```

`P1.11` fitness tests run continuously across the sequence rather than waiting until the end. After P1.10, the remaining P1.11 replay/projection fitness evidence is the next closure dependency before P1.12.

Bounded parallel work is permitted when dependencies remain explicit and the work does not prejudge unresolved architecture or technology choices.

## 7. ADR boundary

No new ADR is required merely because Phase 1 has begun.

An ADR becomes required before relying on a choice that crosses the ADR triggers established in `REFERENCE-IMPLEMENTATION-READINESS.md`, including material cross-module constraints, durable migration cost, stable public/cross-product interfaces, security/isolation enforcement choices or durable vendor/infrastructure dependencies.

P1.05 remains below that gate: its decision records and evaluator are bounded, reversible, in-memory, domain-neutral and non-public. They do not select an IAM provider, policy engine, durable authorization-enforcement mechanism, tenant-isolation technology or production authority-administration model. A real enforcement choice that materially constrains those concerns will require the applicable ADR/governance evidence before reliance.

P1.06 also remains below the ADR gate. Its mutation boundary and conflict check are bounded, deterministic, in-memory, domain-neutral and non-public. It does not select durable persistence, a Canonical Head/effective-version resolver, transaction/concurrency technology, public mutation protocol or evidence-integrity mechanism. A later durable choice that materially constrains those concerns must cross the applicable ADR gate before reliance.

P1.07 remains below the ADR gate for the same reason: Event admission uses only caller-supplied immutable in-memory history and no durable event store, broker, outbox/inbox, schema registry, delivery protocol or public Event contract. Selecting any of those as a durable cross-module dependency remains a later ADR decision if and when the readiness triggers are crossed.

P1.08 remains below the ADR gate because its reconstruction manifest is derived, immutable, in-memory and non-public. It introduces no durable lineage store, graph database, provenance service, projection technology, public serialization contract or evidence-integrity mechanism and therefore does not create a constraining cross-module dependency.

P1.09 remains below the ADR gate because its significant Observation representation reuses the existing in-memory Canonical Record semantics, adds no durable Memory/Knowledge store or promotion engine, introduces no public learning API or serialization contract, and makes no technology/vendor choice. Any later durable Knowledge lifecycle, retrieval/index technology or cross-module/public interface must cross the applicable ADR gate when the readiness triggers are met.

P1.10 remains below the ADR gate because its JSON representation is a documented, deterministic, bounded reference fixture only. It creates no supported public/cross-product wire contract, durable migration commitment, vendor dependency, persistence layout or production export service. If a serialization format later becomes a stable cross-product/public interface, durable portability package standard or customer compatibility commitment, the applicable ADR/standard/governance gate must be crossed before reliance.

## 8. Maintenance rule

Before updating Phase 1 status:

1. synchronize with the canonical repository;
2. verify the Constitution and RFC Index;
3. inspect the actual implementation/tests for the affected `P1.*` work item;
4. update this work breakdown and the parent Roadmap when the milestone materially changes overall delivery state.

Project chats and implementation commits SHOULD refer to the stable `P1.*` identifier together with the task name, for example:

> `P1.02 — Native subject + first immutable Canonical Record version`

This prevents neighboring chats from inventing competing task names or ambiguous ordering.
