# Arvectum OS Phase 2 — Core Runtime

Status: `Active`
Version: `1.1.11`
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
| `P2.02` | Canonical Record lineage, Head and Effective Version runtime | 🟩 | `██████████ 100%` |
| `P2.03` | Typed Relationship runtime | 🟩 | `██████████ 100%` |
| `P2.04` | Governed Execution lifecycle and gate orchestration runtime | 🟩 | `██████████ 100%` |
| `P2.05` | Event admission, provenance and reconstruction runtime | 🟩 | `██████████ 100%` |
| `P2.06` | Runtime consistency, idempotency and conflict semantics | 🟩 | `██████████ 100%` |
| `P2.07` | Product Contract runtime validation boundary | 🟩 | `██████████ 100%` |
| `P2.08` | Portability, replay and non-authoritative projection runtime | 🟩 | `██████████ 100%` |
| `P2.09` | Second bounded workflow reuse proof | 🟩 | `██████████ 100%` |
| `P2.10` | Core Runtime architecture fitness matrix | 🟦 | `░░░░░░░░░░ 0%` |
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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/canonical.py` extends the provisional immutable Canonical Record envelope with optional timezone-aware `effective_from` / `effective_until` applicability bounds; prior versions remain immutable and missing bounds remain unbounded on that side;
- `reference/python/arvectum_os_ref/canonical_lineage.py` introduces a domain-neutral in-memory `CanonicalLineage` resolver over already-admitted versions without selecting persistence, database/index, public API or current-state-pointer technology;
- lineage validation preserves one Subject Identity, Organization scope, authority scope/mode and semantic type while requiring distinct Version Identities, exactly one root, known predecessors, one unambiguous successor chain and one Canonical Head;
- Canonical Head is derived from predecessor lineage rather than collection order, creation timestamp or mutable projection state;
- Effective Version resolution requires an explicit timezone-aware evaluation time and uses immutable half-open applicability intervals; zero applicable versions and overlapping applicable versions fail explicitly instead of applying a last-write-wins guess;
- exact immutable Version Identity lookup remains available independently of Head/Effective resolution and is proven compatible with `GovernedVersionPin` consequential pinning;
- `reference/python/tests/test_p2_02_canonical_lineage.py` adds 15 focused tests covering two independent multi-version subjects, future-effective Head/Effective divergence, immediate-effect boundary, historical resolution, exact stale-version pinning, fork/missing-predecessor/mixed-scope conflicts, overlap/gap failures and timezone-aware evaluation;
- GitHub Actions `Reference Python CI` run `#28` for PR `#20` on executable code head `5c86f84628866a5b35a309620190022072ac0261` completed successfully: `Ran 155 tests in 0.303s` / `OK`; the prior 140-test R1 baseline remains green;
- no Accepted RFC is modified; no ADR is required because the implementation remains bounded, in-memory, internal/provisional and reversible, and does not establish a durable datastore, public interface or cross-product compatibility contract.

P2.02 completion makes the exercised RFC-0002 lineage/Head/Effective Version semantics executable within the bounded reference runtime only. It does not create a Governed Execution current-state pointer, solve durable concurrency/branch admission, activate a Platform Capability, establish production readiness or create a full RFC-0002 conformance claim. P2.06 remains responsible for broader runtime consistency/concurrency semantics, while P2.04 remains responsible for reusable Governed Execution lifecycle state.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/relationships.py` introduces a bounded domain-neutral Typed Relationship runtime represented as a Canonical Record specialization through composition, preserving stable Relationship Identity as Subject Identity and immutable relationship Version Identity;
- `RelationshipEndpoint` makes the endpoint reference role explicit as `SubjectIdentity` or `VersionIdentity`; endpoint role is never inferred from Identity syntax and exact traversal does not conflate the two roles;
- `RelationshipTypeReference` preserves governed type identity, exact type-definition Version Identity, semantic relationship name and schema version; a compatible type-definition version may advance under the same Relationship Identity while a semantic relationship-type change is rejected and requires a new Relationship Identity;
- `create_typed_relationship` requires caller-supplied independent Relationship Identity rather than deriving identity from the source/type/target tuple, so distinct assertion instances over the same tuple remain representable;
- `version_typed_relationship` creates immutable predecessor-linked successor versions, preserves identity-defining source/type/target semantics and rejects source identity, endpoint-role, target or semantic relationship-type drift under the same Relationship Identity;
- `TypedRelationshipLineage` reuses the P2.02 Canonical lineage/Head/Effective Version semantics for relationship history while preserving exact relationship Version Identity lookup;
- lifecycle termination is represented by a new immutable relationship version; prior active history remains resolvable and is never deleted or rewritten;
- `traverse_relationships` traverses only exact immutable relationship versions supplied by the caller, with explicit inbound/outbound direction and no silent Head/Effective selection; implementation is a bounded tuple scan and introduces no graph database/index authority assumption;
- relationship existence explicitly carries no intrinsic Authorization or Organizational Authority grant, preserving RFC-0003 policy/enforcement separation;
- the bounded runtime fails closed on cross-Organization endpoints and remains Native-authority-only; cross-organization/shared relationship semantics remain outside this slice and require their applicable security/governance model;
- `reference/python/tests/test_p2_03_typed_relationships.py` adds 25 focused fitness/negative-path tests covering independent identities, exact endpoint roles, type/version attribution, compatible type evolution, identity-defining drift rejection, lineage/history, effective resolution, termination, authority separation, directed traversal, duplicate tuple assertions and absence of graph-database dependencies;
- GitHub Actions `Reference Python CI` run `#31` for PR `#21` on executable code head `4b3420e85fdc0b09ebe9714259d3e837bdfc3b6e` completed successfully: `Ran 180 tests in 0.263s` / `OK`;
- no Accepted RFC is modified and no ADR gate is crossed: the implementation remains bounded, in-memory, internal/provisional and reversible, with no durable datastore, graph engine, public API/SDK, stable serialization contract or capability activation.

P2.03 completion makes the exercised RFC-0002 Typed Relationship semantics executable only within the bounded reference runtime. It does not establish a universal relationship-type catalog, cross-organization relationship sharing, a graph persistence contract, authorization policy semantics, production readiness, full RFC-0002/RFC-0003 conformance or an `Active` Platform Capability.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/governed_execution.py` introduces a bounded domain-neutral in-memory Governed Execution runtime over immutable `platform.execution-context` Canonical Record versions with one stable Execution Identity and explicit `Created`, `AwaitingGate`, `Ready`, `Running`, `Waiting`, `Suspended`, `Compensating` and sealed terminal conditions;
- the runtime pins the exact Approved Workflow Version Identity, every material-input Version Identity and, when supplied, the exact applicable Product Contract Version Identity before consequential reliance; Product Contract presence does not satisfy authorization, Organizational Authority or another gate by itself;
- `ActorAssurance`, `Authorization`, `OrganizationalAuthority`, `DataGovernance`, `Validation` and `ConsequentialApproval` are represented as separate required-gate concepts, and each immutable gate decision is attributed to the exact AwaitingGate execution version, Workflow version, material-input versions and applicable Product Contract version evaluated;
- unresolved or denied required gates fail closed; duplicate gate kinds are rejected; generic lifecycle transitions cannot bypass `AwaitingGate`/`Ready` orchestration;
- Waiting/Suspended resumption requires the caller to state whether prior gate assumptions remain valid; stale assumptions return the execution to a new immutable `AwaitingGate` version and invalidate prior decisions for admission rather than silently reusing them;
- terminal `Succeeded`, `Failed`, `Cancelled`, `Compensated` and `PartiallyCompensated` history is sealed, and `GovernedExecutionLineage` reuses P2.02 canonical-lineage validation for exact immutable history/head resolution;
- `require_consequential_operation_admission` rejects `CanonicalMutation`, `ExternalMutation` and `Commitment` effects outside an admitted `Ready`/`Running` execution, when the exact Workflow operation did not declare the effect, or when required gates are not satisfied; the existing P1 mutation guard remains unchanged and green;
- the same runtime is exercised by two materially different workflow shapes within the P2.04 fitness slice: a canonical-mutation workflow with Authorization/Organizational Authority/Data Governance/Validation/Consequential Approval and an ExternalMutation+Commitment workflow with Actor Assurance/Authorization/Data Governance/Consequential Approval;
- `reference/python/tests/test_p2_04_governed_execution.py` adds 19 focused lifecycle, attribution, fail-closed, stale-gate, sealing, boundary and second-workflow tests;
- GitHub Actions `Reference Python CI` run `#34` for PR `#22` on executable code head `2287a35fe73eb6f849cdd03be2c984a9c9cad476` completed successfully: `Ran 199 tests in 0.341s` / `OK`; the prior 180-test P2.03 baseline remains green;
- no Accepted RFC is modified and no ADR gate is crossed: the implementation remains internal/provisional, bounded, in-memory and reversible, with no workflow engine, durable datastore, IAM/policy provider, Event/provenance backend, broker, transaction/concurrency mechanism, public API/SDK or Product Contract schema/validator selected.

P2.04 completion makes the exercised RFC-0005 lifecycle/gate semantics reusable only within the bounded Core Runtime evidence. It does not establish production readiness, an `Active` Platform Capability, full RFC-0005 conformance, a public orchestration contract, durable execution consistency, generalized Event/provenance behavior or Product Contract validation. P2.05, P2.06 and P2.07 retain those responsibilities respectively.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/event_provenance.py` introduces a bounded domain-neutral in-memory Event/provenance runtime over the reusable P2.04 Governed Execution model without modifying the P1.07/P1.08 scenario-specific evidence modules;
- `EventReceipt` is an immutable transient received representation and remains explicitly distinct from canonical history; only `admit_event` creates an admitted `platform.event` Canonical Record specialization;
- canonical admission preserves exact Event Identity and Version Identity, type/schema version, Organization/Native authority scope, authoritative source, occurrence/recording times, producer/initiation attribution, exact Execution Identity/Version, related governed Subject/Version references, correlation, causation, classification/access metadata, provenance, integrity metadata and immutable payload;
- duplicate delivery of the exact same immutable occurrence returns the previously admitted canonical Event without appending another occurrence; materially different immutable content under the same Event Identity and reuse of one Event Version Identity by another Event are rejected explicitly;
- occurrence and recording/admission timestamps remain independently attributable and are not treated as a universal ordering guarantee, preserving RFC-0006 clock/late-arrival semantics rather than carrying forward the narrower P1 fixture assumption;
- `build_reconstruction_manifest` validates one immutable P2.04 Execution lineage through a sealed terminal head and identifies the initiating actor, exact Workflow version, every material-input version, each terminal gate-decision version, every Execution Context version, governed result versions and admitted Event versions, while preserving correlation/causation and optional Product Contract attribution;
- reconstruction is a frozen derived manifest, not Canonical State; it performs no replay, mutation, Event emission/admission or projection authority resolution;
- the same Event/provenance runtime reconstructs both the canonical-mutation workflow and a materially distinct `ExternalMutation`+`Commitment` workflow with a different gate set;
- `reference/python/tests/test_p2_05_event_provenance.py` adds 21 focused admission, conflict, provenance, reconstruction, negative-path, timestamp and reuse tests;
- GitHub Actions `Reference Python CI` run `#37` for PR `#23` on executable code head `e95bcfa5647fd7d1c73dfee8bc2bb912ee681f9c` completed successfully: `Ran 220 tests in 0.318s` / `OK`; the prior 199-test P2.04 baseline remains green;
- no Accepted RFC is modified and no ADR gate is crossed: the implementation remains bounded, in-memory, internal/provisional and reversible, with no broker, durable Event store, delivery topology, schema registry, telemetry backend, transaction/outbox/inbox mechanism, public API/SDK or Product Contract validator selected.

P2.05 completion makes the exercised RFC-0002/RFC-0006 Event admission and reconstruction semantics reusable only within the bounded Core Runtime evidence. It does not establish a durable Event store, delivery guarantee, universal ordering, exactly-once processing, external-authority Event contract, production observability stack, production readiness, full RFC-0006 conformance or an `Active` Platform Capability. P2.06 retains broader runtime consistency, retry/idempotency, uncertainty and concurrency responsibilities.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/runtime_consistency.py` introduces an immutable, domain-neutral `RuntimeConsistencyState` over one bounded canonical target lineage, admitted Events and consequential invocation-attempt evidence while reusing P2.02 Canonical lineage, P2.04 Governed Execution admission and P2.05 Event admission semantics;
- canonical mutation requires an explicit expected Canonical Head Version Identity and the admitted Governed Execution must pin that exact target version; a stale current head raises an explicit conflict and an execution prepared against a different target version cannot silently commit against newer state;
- the proposed successor must preserve Subject Identity, Organization, authority scope/mode and semantic type, use a new immutable Version Identity and identify the exact expected current head as predecessor before it can extend canonical lineage;
- retry semantics are explicit as `NaturallyIdempotent`, `KeyedIdempotent` or `NonIdempotent`; keyed/non-idempotent attempts require a duplicate-protection token, and reuse of one token for materially different immutable invocation content fails as an idempotency conflict;
- an exact already-committed invocation returns the previously committed record/Event evidence without appending another canonical version, Event or consequential-attempt record; natural idempotency can likewise recognize the already-published exact successor without treating transport delivery as a universal exactly-once guarantee;
- `ExternalMutation`/`Commitment` attempt semantics keep `Succeeded`, `Failed` and `Uncertain` explicit; an uncertain prior outcome blocks blind retry and requires reconciliation, while a definite failure remains a failure and may be retried only under the declared retry semantics;
- the external-consequence boundary records semantic outcome evidence only and does not itself perform an external effect, choose a remote idempotency protocol or imply cross-system atomicity;
- the bounded local logical commit boundary validates expected head, exact execution target pin, successor lineage and required Event admission before returning one immutable next runtime snapshot containing the new record, Event and succeeded attempt; Event-admission failure leaves the caller's prior immutable state unchanged;
- the logical atomicity declaration explicitly excludes durable storage transactions, database locking/CAS implementation, external-system mutation, transport acknowledgement/delivery, outbox/inbox persistence and distributed coordination, so P2.06 does not claim durable ACID or exactly-once processing;
- `reference/python/tests/test_p2_06_runtime_consistency.py` adds 21 focused stale-head/current-version, exact-pin, successor, idempotency-key, natural/keyed retry, duplicate Event, failure, uncertainty/reconciliation, logical-atomicity and second-effect-shape tests;
- GitHub Actions `Reference Python CI` run `#40` for PR `#24` on executable code head `c90b5b0d581e6a4ac9e99c20670c192f59cdcda3` completed successfully: `Ran 241 tests in 0.334s` / `OK`; the prior 220-test P2.05 baseline remains green;
- no Accepted RFC is modified and the durable persistence/transaction/concurrency ADR gate is not crossed: the implementation remains bounded, in-memory, internal/provisional and reversible, with no database transaction model, locking/CAS mechanism, durable idempotency store, outbox/inbox mechanism, broker, distributed coordinator or stable public API/SDK selected.

P2.06 completion makes the exercised RFC-0002/RFC-0005/RFC-0006 conflict, retry/idempotency, uncertainty and local logical-commit semantics reusable only within the bounded Core Runtime evidence. It does not establish durable concurrency control, cross-system atomicity, exactly-once delivery/processing, production readiness, full RFC conformance or an `Active` Platform Capability. Per the approved engineering-quality decision, P2.06 triggered the mandatory `R2 — Runtime Health Review` before substantive P2.07 work.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/product_contract.py` introduces an internal, in-memory and explicitly provisional Product Contract runtime boundary rather than a public manifest, registry or SDK contract;
- the bounded `ProductContract` preserves exact Subject/Version Identity, Product identity/version, accountable owner provenance and RFC-0004 lifecycle, and requires the compatibility, platform-dependency, operation, portability, retention/deletion, review and exit declarations needed by the exercised Provisional interaction;
- `validate_product_contract_interaction` fails closed unless the exact Provisional contract covers the product identity/version, Organization, declared platform dependency/version/operation, Workflow side-effect semantics and required Authorization/Organizational Authority/Data Governance gates;
- canonical material-input reliance requires a declared exact semantic type, authority mode/scope and Read access, while a declared `CanonicalMutation` additionally requires Write access to the exact Workflow target;
- the synthetic boundary rejects modeled hidden coupling through internal tables/imports, undocumented endpoints, private Event streams and implicit shared state instead of treating those paths as valid Product Contract reliance;
- `start_product_governed_execution` is the first product-like reusable entry: it validates RFC-0004 declarations before delegating to the existing P2.04 Governed Execution runtime and passes the exact Product Contract Version Identity pin into execution provenance;
- Product Contract possession/validation creates no Authorization, Organizational Authority, approval or capability lifecycle state; unresolved runtime gates remain unresolved and later gate decisions preserve the exact Product Contract version attribution;
- the fixture is intentionally domain-neutral (`synthetic-product`, `example.subject`) and the implementation contains no procurement/product-domain semantics;
- `reference/python/tests/test_p2_07_product_contract.py` adds 14 focused positive/negative-path Product Contract boundary tests;
- GitHub Actions `Reference Python CI` run `#47` for PR `#26` on executable code head `127d99d44761d2d80c5c6bddc11096fe14fd6f87` completed successfully: `Ran 261 tests in 0.273s` / `OK`;
- no Accepted RFC is modified and no relevant ADR gate is crossed: the boundary remains bounded, internal/provisional and reversible, with no durable contract registry, stable manifest/wire format, public API/SDK, IAM/enforcement technology, persistence topology or capability activation selected.

P2.07 completion makes the exercised RFC-0004 product/platform validation boundary executable for one synthetic product-like consumer only. It does not standardize the Product Contract manifest, claim `Stable` Product Contract support, activate any Platform Capability, create a security credential, establish production readiness or make a full RFC-0004/RFC-0005 conformance claim.

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

**Completion evidence — 2026-08-08:**

- `reference/python/arvectum_os_ref/portability_runtime.py` introduces a bounded domain-neutral semantic portability runtime with an explicitly `bounded-internal-provisional` JSON representation; the representation is derived, non-canonical and explicitly not a stable public/cross-product compatibility contract or production export endpoint;
- export maps documented runtime meaning rather than Python object layout and preserves, within the exercised Native-authority scope, Organization identity, stable Subject Identity, exact immutable Version Identity, semantic/schema type, authority mode/scope, accountable owner and actor attribution, creation/effective time, provenance/integrity metadata, predecessor lineage, lifecycle and payload;
- Typed Relationship export preserves the exact canonical relationship record version, relationship-type identity/version/name/schema and explicit source/target `SubjectIdentity` versus `VersionIdentity` endpoint roles; canonical Event export preserves exact Event record version, type/schema, authoritative source, occurrence/recording times, actor/producer attribution, exact execution Subject/Version, related Subject/Version references, correlation, causation, classification and access scope;
- reconstruction invokes existing bounded Canonical Record / Typed Relationship / Event constructors only as validation machinery and then exposes frozen `Reconstructed*Semantics` values with `canonical_authority = False`, so imported state cannot become an independent canonical authority merely by successful reconstruction;
- package manifests bind exact record/relationship/Event Version Identity sequences and reconstruction fails closed on manifest drift, conflicting immutable Version Identity reuse, relationship endpoint drift, Event execution-version drift, cross-Organization input or invalid semantic envelopes;
- `rebuild_non_authoritative_projection` exposes no consequential-operation executor, external-effect callback, Event-admission adapter, canonical mutation path, database or broker binding; replay only rebuilds immutable derived projection entries and reports `consequential_side_effects_created = 0`;
- projection lookup returns all source versions for a Subject Identity and performs no implicit Canonical Head/Effective Version inference; exact source Version Identity attribution survives both reconstruction and projection;
- projections cannot mint governed pins: `pin_runtime_projection_source` requires an independently supplied exact `CanonicalRecord` whose Subject Identity, Version Identity, semantic type, authority mode/scope and lifecycle attribution match the projection entry; a reconstructed imported record is intentionally not a `CanonicalRecord` and is rejected as an authority substitute;
- `reference/python/tests/test_p2_08_portability_replay_projection.py` adds 20 focused semantic round-trip, replay safety and negative-path tests, including two materially distinct scenarios: multi-version canonical state plus a Typed Relationship, and execution/result state plus a canonical Event;
- [`P2-08-portability-replay-projection-cross-review.md`](../reviews/P2-08-portability-replay-projection-cross-review.md) records two functional review iterations: iteration 1 identified and remediated the imported-state authority-type leak; iteration 2 passed across architecture, engineering, security/privacy and governance perspectives with no unresolved material objection;
- GitHub Actions `Reference Python CI` run `#52` for PR `#27` on executable code head `628005d5baa8abb62284067b808abc84cdf37160` completed successfully: `Ran 281 tests in 0.283s` / `OK`;
- no Accepted RFC is modified and no serialization, replay/projection-storage or public-interface ADR gate is crossed: the implementation remains bounded, in-memory, internal/provisional and reversible, and does not select durable storage, broker, graph engine, schema registry, public API/SDK, production export authorization workflow or stable wire contract.

P2.08 completion makes semantic round-trip and side-effect-safe non-authoritative projection replay reusable only within the bounded Core Runtime evidence and its current Native-authority reference scope. It does not establish production export/disclosure behavior, External Reference or Governed Replica portability support, a stable public/cross-product serialization contract, durable replay/projection infrastructure, production readiness, full RFC conformance or an `Active` Platform Capability.

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

**Completion evidence — 2026-08-08:**

- `reference/python/tests/test_p2_09_second_workflow_reuse.py` adds 8 cross-cutting reuse fitness tests over two complete domain-neutral workflow configurations while deliberately adding no new stable runtime abstraction before the mandatory R3 evidence review;
- both workflows enter through the existing P2.07 `start_product_governed_execution` boundary and reuse one shared fixture-local Governed Execution path (`start → AwaitingGate → exact gate decisions → Ready → Running`) backed by the same P2.04 runtime operations; the fitness test also verifies that the proof imports neither the P1 `reference_scenario`/`reference_runtime_adapters` path nor the historical P2.01 `RuntimeComposition` orchestration;
- workflow A is a direct `CanonicalMutation` against one exact current canonical version with Authorization, Organizational Authority, Data Governance and Validation gates; P2.06 commits one immutable successor plus one canonical Event and an exact keyed retry returns the already-committed evidence without appending another record, Event or consequential attempt;
- workflow B is materially distinct: P2.02 resolves an Effective Version that intentionally differs from a future-effective Canonical Head; P2.03 supplies a Typed Relationship whose source endpoint is explicitly pinned to that exact `VersionIdentity`; the resolved record, context record and exact relationship record version are all pinned as material inputs before consequential reliance;
- workflow B uses Actor Assurance, Authorization, Data Governance and Consequential Approval rather than workflow A's gate set, and declares `ExternalMutation` plus `Commitment` rather than canonical mutation; P2.06 records explicit external-consequence outcome/idempotency evidence without publishing a canonical successor or Event;
- relationship existence remains non-authoritative: the proof explicitly verifies that the Typed Relationship grants neither Authorization nor Organizational Authority and that the required execution gates remain separately satisfied;
- both synthetic consumers cross the same P2.07 Product Contract boundary with exact Provisional Product Contract Version Identity attribution, declared platform dependency/version/operation, exact canonical Read/Write scopes appropriate to each workflow and fail-closed responsibilities;
- [`P2-09-second-bounded-workflow-reuse-proof-cross-review.md`](../reviews/P2-09-second-bounded-workflow-reuse-proof-cross-review.md) records a functional architecture/engineering/security/governance review with result `Pass`; the observed fixture/configuration duplication pressure is explicitly carried into mandatory R3 rather than prematurely standardized into a new platform abstraction;
- GitHub Actions `Reference Python CI` run `#56` for PR `#28` on executable code head `403e6385091fdb94ff0c6ca59df80b311afdd594` completed successfully: `Ran 289 tests in 0.359s` / `OK`;
- no Accepted RFC is modified and no new ADR gate is crossed: the proof remains bounded, internal/provisional and reversible, and does not select durable persistence, transaction/concurrency technology, Event delivery, external connector behavior, IAM/policy enforcement, stable public API/SDK, serialization contract or service topology.

P2.09 completion establishes the second-workflow reuse evidence required before R3, but it does not complete R3, P2.10–P2.12 or milestone M2, does not activate a Platform Capability and does not claim production readiness or full RFC conformance.

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

| Gate | Trigger | Status | Primary purpose |
|---|---|---:|---|
| `R1 — Structural Review` | after P2.01, before substantive P2.02 | 🟩 Complete | validate runtime/fixture/test boundaries, dependency direction and remove accidental P1 structure |
| `R2 — Runtime Health Review` | after P2.06, before substantive P2.07 | 🟩 Complete | review the accumulated semantic runtime spine, consistency/error/idempotency patterns and emerging ADR triggers |
| `R3 — Reuse Refactoring Review` | after P2.09, before final Phase 2 hardening | 🟩 Complete | refactor abstractions using evidence from two materially distinct workflows |
| `R4 — Milestone Hardening` | after final applicable P2.10 evidence, before P2.11/P2.12 | ⬜ Planned | full Phase 2 code-health remediation and evidence-backed optimization before closure reviews |

Rules:

- normal local code hygiene remains continuous and does not wait for these gates;
- gates are engineering checkpoints, not capability-lifecycle or conformance claims;
- performance optimization SHOULD follow reproducible benchmark/profile evidence unless an obvious correctness, resource-exhaustion or security problem requires immediate correction;
- a gate does not replace the ADR gate; any materially constraining choice discovered by a gate must be governed before further material reliance.

**R1 completion evidence — 2026-08-08:**

- canonical review: [`R1-structural-review.md`](../reviews/R1-structural-review.md);
- reusable `runtime.py` no longer selects the historical P1 implementation adapter set by default;
- `reference_runtime_adapters.py` explicitly contains the bounded P1 binding;
- the reference scenario selects that adapter set explicitly and still delegates execution through one runtime call;
- two additional structural fitness tests prevent default adapter binding and historical P1 operation imports from returning to the runtime core;
- GitHub Actions `Reference Python CI` run `#23` on executable code head `e0c71c1c80b658711a7420ffb7d59248ce741fb8` passed `140` tests / `OK`;
- hard-coded P1 reference identifiers/timestamps remain intentionally contained behind the reference adapter boundary and are not generalized ahead of P2.04/P2.05;
- no relevant ADR gate was crossed.

**R2 completion evidence — 2026-08-08:**

- canonical review: [`R2-runtime-health-review.md`](../reviews/R2-runtime-health-review.md) — `Complete`, result `Pass with bounded debt`;
- accumulated semantic ownership remains coherent: Canonical lineage owns Head/exact/effective resolution, Relationships own relationship semantic drift, Governed Execution owns lifecycle/gate admission, Event/provenance owns Event admission/identity conflict/reconstruction, and Runtime Consistency owns stale-head/retry/idempotency/uncertainty/logical-commit conflict semantics;
- no competing lineage, execution-transition, Event-admission or retry/idempotency engine was introduced;
- small repeated validation helpers remain local because their semantic constraints and failure contexts differ; R2 explicitly rejects a speculative shared validation/error abstraction before reuse evidence or a stable public boundary justifies one;
- bounded debt is recorded for exact-resolution error-taxonomy inconsistency, one broad P2.06 Event-conflict assertion and the fact that arbitrary/deserialized `RuntimeConsistencyState` construction is not a durable aggregate-integrity admission boundary;
- `reference/python/tests/test_r2_runtime_health.py` adds 6 cross-cutting semantic-owner, dependency, fail-closed lineage and technology-neutrality checks;
- GitHub Actions `Reference Python CI` run `#43` for PR `#25` on executable head `c519e6fb3fe9d9b333382786740a37c3a477c06b` passed `247` tests in `0.415s` / `OK`;
- no material performance issue justifies profiling/optimization work and no durable persistence, transaction/concurrency, Event-delivery, IAM/enforcement or public-interface ADR gate is crossed.

**R3 completion evidence — 2026-08-08:**

- canonical review: [`R3-reuse-refactoring-review.md`](../reviews/R3-reuse-refactoring-review.md) — `Complete`, result `PASS — evidence-backed reuse retained; first-scenario over-generalization contained; no new shared abstraction justified`;
- P2.09 demonstrates that genuine shared reuse occurs through domain-neutral semantic owners, especially the P2.07 Product Contract entry and P2.04 Governed Execution lifecycle/gate runtime, rather than through the historical P2.01 `RuntimeComposition`;
- `runtime.py`, `reference_runtime_adapters.py` and `reference_scenario.py` are explicitly retained as P1/P2.01 reference-compatibility evidence and are not generalized into a universal workflow/plugin contract;
- `reference/python/tests/test_r3_reuse_refactoring.py` adds 4 fitness checks that prevent Product Contract/Governed Execution from acquiring a dependency on the historical composition seam and prevent widening the historical request merely to fit the second workflow;
- the shared P2.09 fixture helper that fabricates explicit ALLOW decisions remains test-local and is not promoted into platform authority/orchestration behavior;
- P2.07/P2.09 fixture/configuration repetition remains explicit because gate sets, side effects, access scopes and exact-version declarations are the evidence being varied; no speculative generic fixture/runtime builder is introduced;
- the R2 broad Event-conflict assertion is resolved by expecting exact `EventIdentityConflictError`;
- local validation/error families remain semantically scoped; package-root P1 convenience exports and durable `RuntimeConsistencyState` aggregate admission remain explicit bounded items for later stable-boundary hardening rather than R3 blockers;
- GitHub Actions `Reference Python CI` run `#63` on executable branch head `72c97b8b24e86369d00c5932a3723743577b0c21` completed successfully: `Ran 293 tests in 0.312s` / `OK`;
- no new ADR gate was crossed and no Accepted RFC was modified.

## 7. Dependency-aware sequence

```text
P2.01 Runtime boundary extraction
          ↓
R1 Structural Review ✓
          ↓
P2.02 Canonical Record Head / Effective Version runtime ✓
   ├──────────────┐
   ↓              ↓
P2.03 Relationships ✓    P2.04 Governed Execution runtime ✓
   │              │
   └──────┬───────┘
          ↓
P2.05 Event / provenance runtime ✓
          ↓
P2.06 Consistency / idempotency / conflict semantics ✓
          ↓
R2 Runtime Health Review ✓
          ↓
P2.07 Product Contract runtime boundary ✓
          ↓
P2.08 Portability / replay / projection runtime ✓
          ↓
P2.09 Second workflow reuse proof ✓
          ↓
R3 Reuse Refactoring Review ✓
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

The sequence is dependency-aware rather than mechanically serial. P2.03–P2.04 MAY proceed in bounded parallel where interfaces are explicit and no unresolved decision is prejudged, but declared engineering gates remain ordering constraints for the work that follows them.

## 8. Current canonical action

> **`P2.10 — Core Runtime architecture fitness matrix`.**

Consolidate final applicable M2 architecture-fitness evidence over the semantic owners proven through P2.09 and hardened by R3. Cover identity/Organization isolation, immutable canonical/relationship history, Head versus Effective Version resolution, exact consequential version pinning, separate authority/gate semantics, direct consequential-operation rejection, idempotency/retry/conflict behavior, Event duplicate/conflict admission, reconstruction, Product Contract enforcement, projection/replay non-authority, semantic portability, product-domain leakage and migration/reversibility constraints where applicable.

Do not reopen the rejected idea of generalizing the historical P2.01 compatibility composition merely to obtain one universal orchestration API. Any materially constraining implementation choice discovered by P2.10 must still pass the existing ADR gate before further reliance.

## 9. ADR gate

No new ADR is required merely because Phase 2 is Active or because an engineering gate is performed.

An ADR is required before relying on a concrete implementation choice when it becomes materially constraining under the parent Roadmap gate, including cross-module/product coupling, material migration cost, stable public/cross-product interfaces, security/authority enforcement technology, durable data/event/runtime dependencies or materially different portability/reliability consequences.

Phase 2 is expected to be the first phase in which one or more ADR gates may realistically be crossed. This document does not pre-approve any particular ADR or technology. R3 did not cross a new ADR gate.

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
