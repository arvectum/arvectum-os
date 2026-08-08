# Arvectum OS Phase 2 — Core Runtime

Status: `Active`
Version: `1.1.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M2 — Reusable governed runtime baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Engineering quality decision: [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md)
Predecessor: `Phase 1 — Reference Implementation`, `M1` achieved

## 1. Purpose

Phase 2 turns the bounded Phase 1 reference proof into a reusable, domain-neutral Core Runtime without allowing the P1 harness or any provisional technology choice to become accidental platform architecture.

The phase is successful only if multiple bounded workflows can reuse the same governed runtime semantics through explicit runtime boundaries rather than copying P1 implementation logic.

Phase 2 is not a production-readiness phase, does not make a Platform Capability `Active`, and does not establish a public SDK/API, persistence technology, broker, IAM provider, workflow engine, service topology, SLA or full-platform conformance claim.

## 2. Evidence carried forward from Phase 1

Phase 1 established executable evidence for:

- explicit Organization scope and attributable Actor/Principal semantics;
- stable Subject Identity and immutable Canonical Record Version Identity;
- versioned Workflow attribution;
- Execution Context exact-version pinning;
- separate Authorization and Organizational Authority gates;
- governed canonical mutation with immutable successor version and stale-current conflict rejection;
- canonical Event admission with duplicate/conflicting admission behavior;
- provenance/reconstruction evidence;
- Observation non-promotion to Knowledge;
- semantic fixture export and derived non-authoritative projection/replay behavior;
- a passing architecture fitness matrix and closure review.

The canonical P1 closure review also carried forward these intentionally unproven areas as Phase 2 inputs:

- reusable Typed Relationship lifecycle and endpoint operations;
- reusable Canonical Head / Effective Version resolution;
- Product Contract representation/validation at a real product/platform boundary;
- reusable runtime composition rather than a one-scenario harness;
- decisions around durable persistence, transaction/concurrency, IAM enforcement, Event storage/delivery, evidence integrity, replay/projection storage and public interfaces if and only if concrete choices cross the ADR gate;
- full Memory/Knowledge lifecycle remains outside M1 and is not automatically part of Core Runtime unless runtime evidence requires it.

## 3. Phase 2 design principles

Phase 2 MUST:

1. preserve the Accepted Kernel and governance semantics rather than derive architecture from P1 code structure;
2. extract reusable runtime behavior only where Phase 1 evidence or the M2 reuse proof justifies it;
3. keep product-domain logic outside shared runtime modules;
4. keep runtime contracts explicit and testable;
5. preserve exact version reliance, immutable governed history and explicit authority boundaries;
6. keep derived projections, caches and indexes non-authoritative;
7. remain migration-friendly until concrete technology choices are justified;
8. trigger ADR work before a materially constraining implementation choice is relied upon;
9. use RFC-0004 Product Contract semantics before a real Product relies on platform capabilities, canonical platform state or shared platform history;
10. avoid representing working runtime code as an `Active` Platform Capability or production readiness;
11. use evidence-backed engineering review and refactoring gates so implementation structure is hardened at meaningful boundaries rather than by arbitrary cadence.

## 4. Status and progress legend

| Marker | Meaning |
|---|---|
| 🟩 | Complete |
| 🟨 | In progress |
| 🟦 | Ready / next |
| ⬜ | Planned |
| 🟥 | Blocked / conflicted |
| ⚫ | Deferred after evidence review |

Progress bars are planning indicators only.

## 5. Phase 2 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P2.01` | Runtime boundary extraction and reusable composition baseline | 🟩 | `██████████ 100%` |
| `P2.02` | Canonical Record lineage, Head and Effective Version runtime | 🟦 | `░░░░░░░░░░ 0%` |
| `P2.03` | Typed Relationship runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.04` | Governed Execution lifecycle and gate orchestration runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.05` | Event admission, provenance and reconstruction runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.06` | Runtime consistency, idempotency and conflict semantics | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.07` | Product Contract runtime validation boundary | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.08` | Portability, replay and non-authoritative projection runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.09` | Second bounded workflow reuse proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.10` | Core Runtime architecture fitness matrix | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.11` | ADR-gate and runtime-boundary hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.12` | Phase 2 / M2 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Engineering gates `R1`–`R4` are cross-cutting checkpoints and intentionally do not consume `P2.xx` work-item identifiers.

## 6. Detailed work items

### P2.01 — Runtime boundary extraction and reusable composition baseline

**Objective:** separate reusable runtime semantics from the one-scenario P1 reference harness while preserving behavior and keeping the physical package/service topology reversible.

Minimum evidence:

- identify semantic runtime responsibilities versus reference-scenario fixtures;
- expose reusable domain-neutral runtime interfaces/composition for existing P1 capabilities;
- preserve Organization, Identity, version, authority and Governed Execution semantics;
- keep adapters replaceable and keep product semantics outside the runtime;
- migrate or wrap P1 tests so behavior remains demonstrably unchanged;
- no durable technology selection merely to create a cleaner package structure.

**Exit:** at least the P1 scenario can execute through reusable runtime composition without directly depending on scenario-specific orchestration internals.

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/runtime.py` introduces a provisional internal `RuntimeComposition`, explicit `RuntimeExecutionRequest` / `RuntimeExecutionResult` boundaries and replaceable `RuntimeOperations` adapters;
- `reference/python/arvectum_os_ref/reference_scenario.py` owns only deterministic P1 fixture setup and delegates the governed execution spine through one runtime composition call;
- the composition preserves exact Workflow/material-input pins, separate Authorization and Organizational Authority evidence, immutable Execution Context lineage, governed canonical mutation, canonical Event admission, reconstruction evidence and Observation non-promotion;
- existing P1.10 portability evidence consumes the runtime result without changing its bounded, non-authoritative, non-public semantics;
- `reference/python/tests/test_p2_01_runtime_composition.py` adds 10 focused boundary/negative-path tests;
- GitHub Actions `Reference Python CI` run `#18` on executable code head `5f56f0bf36e58efe5249b93e9df6ca4437d5621e` completed successfully: `Ran 138 tests` / `OK`;
- no database, broker, IAM/policy provider, workflow engine, public API/SDK, service topology or durable serialization contract was selected;
- no new RFC or ADR is required for this bounded, replaceable, non-public composition baseline.

P2.01 completion does not make the composition seam a stable public platform contract, does not generalize the P1 execution/Event implementations beyond their proven scope, and does not make any Platform Capability `Active` or production-ready. P2.04 and P2.05 remain responsible for broader reusable Governed Execution/gate and Event/provenance runtime semantics.

### P2.02 — Canonical Record lineage, Head and Effective Version runtime

**Objective:** implement reusable resolution operations that P1 intentionally left bounded to explicit current-version arguments.

Minimum evidence:

- stable Subject Identity with immutable version lineage;
- Canonical Head resolution distinguished from Effective Version resolution;
- declared evaluation context for effective-version selection where applicable;
- exact Version Identity can still be pinned for consequential reliance;
- ambiguous/missing resolution fails explicitly rather than silently selecting a version;
- runtime resolver remains independent of a particular database/index technology.

**Exit:** two or more record lineages can be resolved correctly for head and effective-version cases with deterministic tests including future-effective and stale/conflict cases.

### P2.03 — Typed Relationship runtime

**Objective:** exercise the RFC-0002 relationship model as reusable governed runtime behavior rather than derived fixture links.

Minimum evidence:

- independent Relationship Identity and immutable relationship versions;
- source/target endpoint roles explicitly distinguish Subject Identity and Version Identity references;
- attributable relationship type/schema/version and Organization scope;
- relationship existence does not grant authorization or Organizational Authority;
- supersession/history behavior is preserved without mutating prior relationship versions;
- no graph database assumption.

**Exit:** the runtime can create, version, resolve and traverse a bounded set of canonical Typed Relationships while preserving exact endpoint semantics.

### P2.04 — Governed Execution lifecycle and gate orchestration runtime

**Objective:** turn the P1 execution/gate proof into reusable runtime operations.

Minimum evidence:

- reusable Execution Context lifecycle transitions;
- exact Workflow, material input and applicable Product Contract version attribution;
- separate authorization, Organizational Authority, validation/approval and data-governance gate concepts where applicable;
- fail-closed unresolved required gates;
- terminal state sealing and immutable governance-significant execution versions;
- direct consequential canonical mutation outside admitted Governed Execution remains rejected.

**Exit:** more than one workflow shape can use the same execution/gate runtime without copying P1-specific gate orchestration.

### P2.05 — Event admission, provenance and reconstruction runtime

**Objective:** make canonical Event admission and reconstructable evidence reusable across executions.

Minimum evidence:

- receipt/admission distinction remains explicit;
- duplicate delivery is idempotent for the same immutable Event occurrence;
- conflicting immutable content for one Event Identity is rejected/quarantined by the bounded runtime contract;
- correlation/causation and exact governed version references are preserved;
- reconstruction can identify actor, workflow, material input, gates, execution, result and Event versions for the exercised scope;
- Event semantics remain distinct from telemetry and no broker/event-store technology is assumed.

**Exit:** multiple executions can share the same Event/provenance runtime and reconstruct their exact bounded histories.

### P2.06 — Runtime consistency, idempotency and conflict semantics

**Objective:** define reusable logical consistency rules before selecting a durable transaction/concurrency technology.

Minimum evidence:

- stale-head/current-version conflicts are detected explicitly;
- repeat invocation semantics are deterministic for operations requiring idempotency;
- duplicate admission/retry does not repeat consequential effects;
- uncertainty/failure states do not silently claim success;
- logical atomicity boundaries are documented for the bounded runtime;
- identify whether durable persistence/transaction/concurrency requirements now cross an ADR gate.

**Exit:** concurrency/conflict/idempotency fitness scenarios are executable at the semantic/runtime-contract level, with any technology decision either still demonstrably reversible or governed by an ADR before reliance.

### P2.07 — Product Contract runtime validation boundary

**Objective:** make RFC-0004 enforceable at the first reusable runtime entry boundary without inventing product-domain semantics.

Minimum evidence:

- represent and validate Product Contract identity, version and lifecycle required by the exercised runtime interaction;
- validate declared platform dependencies and allowed canonical read/write operations;
- validate required Organization/authority/security/portability/failure declarations proportionately to the interaction;
- reject hidden internal coupling in the reference scenarios;
- use a domain-neutral synthetic product fixture unless a real product interaction is canonically ready;
- do not treat registration as authorization or organizational approval.

**Exit:** one bounded product-like consumer cannot perform governed platform reliance unless the applicable Product Contract version permits that interaction.

### P2.08 — Portability, replay and non-authoritative projection runtime

**Objective:** generalize the P1 fixture/projection proof into reusable runtime behavior without freezing a public wire format.

Minimum evidence:

- implementation-neutral semantic export preserves identities, immutable versions, authority declarations and governed relationships for the exercised runtime scope;
- import/reconstruction tests preserve meaning rather than Python object layout;
- replay rebuilds derived state without causing consequential side effects;
- projections cannot mint governed pins or become independent authority;
- exact source Version Identity attribution survives projection/reconstruction;
- format remains explicitly internal/bounded unless a later public contract is governed separately.

**Exit:** at least two runtime scenarios can round-trip through the bounded semantic portability fixture and rebuild non-authoritative projections with zero consequential replay effects.

### P2.09 — Second bounded workflow reuse proof

**Objective:** prove the M2 reuse claim with a second domain-neutral workflow that reuses the same runtime rather than cloning the P1 path.

The second workflow MUST differ materially enough to test reuse, for example by exercising different relationship/version-resolution/gate/effect paths while remaining domain-neutral.

Minimum evidence:

- no copied runtime orchestration from P1;
- common runtime boundaries are reused;
- both workflows preserve exact-version reliance and governance invariants;
- differences remain workflow/configuration semantics rather than forks of shared platform behavior;
- reusable runtime code is smaller/clearer than maintaining two independent harnesses.

**Exit:** two bounded workflows execute through the same Core Runtime and pass shared fitness tests.

### P2.10 — Core Runtime architecture fitness matrix

**Objective:** accumulate cross-cutting executable evidence for M2.

Matrix SHOULD cover, where exercised:

- identity and Organization scope isolation;
- immutable Canonical Record and Relationship histories;
- Head versus Effective Version resolution;
- exact consequential version pinning;
- separate authority/gate semantics;
- direct-mutation rejection;
- idempotency/retry/conflict behavior;
- Event duplicate/conflict admission;
- reconstruction completeness;
- Product Contract enforcement;
- projection non-authority and replay safety;
- portability semantic round-trip;
- product-domain leakage checks;
- migration/reversibility constraints.

This work item is cross-cutting and MAY progress in parallel with P2.01–P2.09.

**Exit:** the applicable matrix passes on the final P2 runtime code head in CI or equivalent repository evidence.

### P2.11 — ADR-gate and runtime-boundary hardening review

**Objective:** ensure that reuse has not converted provisional implementation convenience into undeclared durable architecture.

Review MUST explicitly examine whether Phase 2 now requires ADRs for any concrete choice around:

- repository/runtime package structure if it becomes a stable cross-module dependency;
- persistence model/database;
- transaction/concurrency mechanism;
- Event persistence/delivery;
- IAM/policy enforcement;
- evidence-integrity mechanism;
- public/cross-product API or serialization contract;
- replay/projection storage;
- service/process topology.

If a choice crosses the existing ADR gate, the ADR MUST be created and accepted before Phase 2 relies on that choice materially. If it does not cross the gate, the review records why.

**Exit:** all materially constraining runtime choices have either accepted ADR coverage or explicit evidence that they remain bounded and replaceable.

### P2.12 — Phase 2 / M2 closure review

**Objective:** determine whether the Core Runtime milestone is genuinely achieved within scope.

Closure review MUST verify:

1. P2.01–P2.09 complete within declared scope;
2. P2.10 final fitness matrix passes;
3. P2.11 finds no missing ADR gate;
4. R1–R4 engineering gates are complete within their declared scope and material findings are resolved or explicitly dispositioned;
5. at least two materially distinct bounded workflows reuse the same runtime semantics rather than copying the P1 harness;
6. no product-domain logic leaked into shared Core Runtime;
7. exact authority/version/provenance semantics remain aligned with Accepted RFCs;
8. portability/replay/projection remain bounded and non-authoritative as declared;
9. no capability activation, production readiness, SLA or full-conformance claim is implied;
10. strategic Roadmap is revalidated before Phase 3 is activated.

**Exit:** `M2 — Reusable governed runtime baseline` is recorded as achieved, or the review returns a bounded list of blocking reconciliation items.

### Cross-cutting engineering quality and refactoring gates

The canonical gate decision is [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md).

| Gate | Trigger | Primary purpose |
|---|---|---|
| `R1 — Structural Review` | after P2.01, before substantive P2.02 | validate runtime/fixture/test boundaries, dependency direction and remove accidental P1 structure |
| `R2 — Runtime Health Review` | after P2.06, before substantive P2.07 | review the accumulated semantic runtime spine, consistency/error/idempotency patterns and emerging ADR triggers |
| `R3 — Reuse Refactoring Review` | after P2.09, before final Phase 2 hardening | refactor abstractions using evidence from two materially distinct workflows |
| `R4 — Milestone Hardening` | after final applicable P2.10 evidence, before P2.11/P2.12 | full Phase 2 code-health remediation and evidence-backed optimization before closure reviews |

Rules:

- normal local code hygiene remains continuous and does not wait for these gates;
- gates are engineering checkpoints, not capability-lifecycle or conformance claims;
- performance optimization SHOULD follow reproducible benchmark/profile evidence unless an obvious correctness, resource-exhaustion or security problem requires immediate correction;
- a gate does not replace the ADR gate; any materially constraining choice discovered by a gate must be governed before further material reliance;
- because P2.01 was completed before this decision was canonically recorded, `R1` is now the current required gate and precedes substantive P2.02 implementation.

## 7. Dependency-aware sequence

```text
P2.01 Runtime boundary extraction
          ↓
R1 Structural Review
          ↓
P2.02 Canonical Record Head / Effective Version runtime
   ├──────────────┐
   ↓              ↓
P2.03 Relationships     P2.04 Governed Execution runtime
   │              │
   └──────┬───────┘
          ↓
P2.05 Event / provenance runtime
          ↓
P2.06 Consistency / idempotency / conflict semantics
          ↓
R2 Runtime Health Review
          ↓
P2.07 Product Contract runtime boundary
          ↓
P2.08 Portability / replay / projection runtime
          ↓
P2.09 Second workflow reuse proof
          ↓
R3 Reuse Refactoring Review
          ↓
P2.10 final applicable fitness evidence
          ↓
R4 Milestone Hardening
          ↓
P2.11 ADR / boundary review
          ↓
P2.12 Closure review
```

`P2.10` architecture fitness tests run continuously across the phase; the diagram shows only its final applicable evidence point before R4.

The sequence is dependency-aware rather than mechanically serial. P2.02–P2.04 MAY proceed in bounded parallel where interfaces are explicit and no unresolved decision is prejudged, but declared engineering gates remain ordering constraints for the work that follows them.

## 8. Current canonical action

> **`R1 — Structural Review`.**

Review the completed P2.01 extraction before substantive P2.02 implementation. Confirm that reusable runtime semantics are separated from deterministic reference-scenario fixtures and tests, inspect dependency direction/cycles/duplication/accidental internal APIs, remove obsolete P1-only structure where evidence supports it, and preserve behavior through the existing fitness/test suite.

R1 is not a performance-optimization sprint and must not introduce a database, broker, IAM/policy provider, workflow engine, public API/SDK, stable service topology or other materially constraining choice merely to make the package structure appear cleaner.

After R1 completes with material findings resolved or explicitly dispositioned, the next roadmap work item is `P2.02 — Canonical Record lineage, Head and Effective Version runtime`.

## 9. ADR gate

No new ADR is required merely because Phase 2 is Active or because an engineering gate is performed.

An ADR is required before relying on a concrete implementation choice when it becomes materially constraining under the parent Roadmap gate, including cross-module/product coupling, material migration cost, stable public/cross-product interfaces, security/authority enforcement technology, durable data/event/runtime dependencies or materially different portability/reliability consequences.

Phase 2 is expected to be the first phase in which one or more ADR gates may realistically be crossed. This document does not pre-approve any particular ADR or technology.

## 10. Phase 2 exit criterion

Phase 2 is complete when:

1. reusable domain-neutral Core Runtime boundaries exist for the exercised Kernel/governed-execution spine;
2. the previously unexercised relationship and Head/Effective Version semantics needed by the runtime are executable;
3. Governed Execution, gate, Event/provenance and consistency semantics are reusable rather than scenario-specific;
4. Product Contract validation protects the exercised product/platform runtime boundary;
5. two materially distinct bounded workflows reuse the same runtime;
6. portability/replay/projection behavior remains migration-friendly and non-authoritative;
7. architecture fitness evidence passes;
8. R1–R4 engineering quality/refactoring gates have completed proportionately and their material findings are resolved or explicitly dispositioned;
9. all crossed ADR gates are governed;
10. no product-domain leakage or unsupported production/capability claim exists;
11. `P2.12` closure review passes and records `M2` achieved.

Completion of Phase 2 does not automatically make any runtime element an `Active` Platform Capability or production-ready service.

## 11. Roadmap maintenance

Before changing any P2 task or engineering-gate status, synchronize with the canonical repository and inspect implementation/tests that support the claimed progress.

After each meaningful P2 milestone or engineering gate:

- update this file and the parent `ROADMAP.md`;
- increment versions according to the roadmap rules;
- keep task identifiers stable unless scope materially changes;
- keep engineering-gate identifiers distinct from roadmap/RFC/ADR namespaces;
- record any required ADR/RFC/policy/Product Contract dependency explicitly;
- do not maintain a competing Phase 2 plan only in chat.
