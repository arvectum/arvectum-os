# P2.11 — ADR-gate and runtime-boundary hardening review

Status: `Complete`
Date: `2026-08-08`
Task classification: `platform`
Result: **`PASS — no current Phase 2 runtime choice has crossed the ADR threshold; the bounded runtime remains internal, reversible and technology-neutral.`**

## 1. Purpose and scope

P2.11 evaluates the R4-hardened Phase 2 code head against the architecture/governance gate for materially constraining runtime decisions. The objective is not to invent an ADR or implementation seam pre-emptively; it is to determine whether existing reuse has already made any provisional choice durable enough that an ADR is required before further reliance.

The review covers exactly the runtime-boundary categories declared by the Phase 2 roadmap:

- repository/runtime package structure;
- persistence model/database;
- transaction/concurrency mechanism;
- Event persistence/delivery;
- IAM/policy enforcement;
- evidence-integrity mechanism;
- public/cross-product API or serialization contract;
- replay/projection storage;
- service/process topology.

The review also checks the carried R2/R3/R4 concern around `RuntimeConsistencyState`: arbitrary durable/deserialized reconstruction is not an admitted integrity boundary and therefore must not become a persistence contract by accident.

## 2. Canonical authority checked

P2.11 was evaluated against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index;
- RFC-0001 through RFC-0008 `1.0.0` — `Accepted`;
- R2 Runtime Health Review;
- R3 Reuse Refactoring Review;
- P2.10 Core Runtime Architecture Fitness Matrix;
- R4 Milestone Hardening;
- the current Phase 2 reference Python semantic-owner modules and tests.

No conflict with the Constitution or Accepted RFC baseline was found.

No relevant Accepted ADR was found that already selects one of the concrete implementation mechanisms examined by this review. This is consistent with the current bounded reference implementation: Accepted RFCs establish semantic obligations while deliberately leaving physical database, broker, workflow runtime, IAM provider, serialization/public interface and service topology to subordinate decisions when a concrete choice is materially relied upon.

## 3. ADR threshold used by this review

A current implementation choice is treated as having crossed the ADR gate when Phase 2 materially relies on a concrete architectural mechanism in a way that is cross-cutting, difficult to reverse, externally depended upon, or likely to constrain later implementations beyond the bounded reference scope.

Examples include:

- a durable database/repository contract relied on by multiple semantic owners;
- a concrete transaction/locking/CAS or outbox mechanism required for correctness;
- a broker/Event-store/delivery checkpoint contract relied on for governed behavior;
- a concrete IAM/policy-engine integration defining enforcement topology;
- cryptographic/ledger/signature machinery relied on as evidence integrity;
- a stable cross-product/public API, SDK or wire/serialization compatibility promise;
- durable projection/replay storage whose state is operationally relied upon;
- a split into separately deployable services/workers or a network/process boundary;
- a package/repository seam promoted from internal organization into a stable cross-module/cross-product compatibility boundary.

Mere Python module organization, internal immutable dataclasses, in-memory tuples, internal provisional JSON, semantic validation functions or test fixtures do not cross that threshold by themselves.

## 4. Explicit boundary assessment

| Boundary | Current evidence | ADR decision | Trigger before future material reliance |
|---|---|---|---|
| Repository/runtime package structure | P2.02–P2.08 semantic owners are internal sibling modules; the package root remains explicitly provisional and does not export the P2 owner surface. Historical P2.01 composition remains compatibility evidence only. | **No ADR now.** Current package shape is implementation organization, not a stable cross-product contract. | Stable root exports, a cross-product package compatibility promise, mandatory repository interfaces shared by multiple owners, or a physical package/service split. |
| Persistence model/database | Canonical histories, events, attempts, contracts and portability fixtures remain in-memory immutable values/tuples. No SQL/ORM/driver/cache/graph-store dependency is selected. | **No ADR now.** No durable store is materially relied upon. | First durable canonical/Event/contract/execution repository or database topology relied upon for correctness or compatibility. |
| Transaction/concurrency | `commit_canonical_mutation` provides only logical all-or-nothing publication of a new immutable `RuntimeConsistencyState`; it explicitly excludes durable transactions, locks, CAS, distributed coordination and outbox/inbox persistence. | **No ADR now.** Logical semantic validation is not a physical transaction decision. | Concrete transaction manager, locking/CAS strategy, durable idempotency store, distributed coordination, or atomic canonical/Event persistence mechanism. |
| Event persistence/delivery | RFC-0006 Event admission semantics are executable, but no broker, Event store, topic, delivery acknowledgement, checkpoint or consumer topology is selected. | **No ADR now.** Canonical Event admission remains distinct from transport/delivery. | Broker/Event-store selection, durable delivery/checkpoint semantics, outbox/inbox, consumer group or cross-process Event path relied upon. |
| IAM/policy enforcement | Actor, Authorization, Organizational Authority and gate evidence are semantic/in-memory reference objects. No IAM provider, PDP/PEP, directory or policy engine is integrated. | **No ADR now.** Enforcement technology/topology remains unselected. | Concrete identity/policy provider or enforcement topology that multiple modules/products materially depend on. |
| Evidence integrity | Provenance/integrity metadata and reconstruction requirements are semantic only. No signing, hash-chain, ledger, WORM store or external attestation mechanism is claimed as the integrity boundary. | **No ADR now.** No concrete integrity technology is relied upon. | Any cryptographic, immutable-storage, ledger, signature or external attestation mechanism used as governed integrity evidence. |
| Public/cross-product API or serialization | Package root is explicitly non-public; P2.08 JSON is marked internal/provisional and reconstructs bounded semantics only. No stable API/SDK/wire framework or schema compatibility commitment exists. | **No ADR now.** Current representation is replaceable internal evidence. | First externally relied-upon API/SDK/wire schema, stable serialization contract, version-negotiation contract or cross-product compatibility surface. |
| Replay/projection storage | Replay only rebuilds derived non-authoritative projections from bounded semantic packages; no projection store, cache, index, checkpoint store or authoritative read model is selected. | **No ADR now.** Projection remains derived/non-authoritative and in-memory. | Durable projection/index/checkpoint storage, operational reliance on projection freshness, or any attempt to make projection state authoritative. |
| Service/process topology | Shared runtime has no process/network dependency and remains compatible with the RFC-0001 modular-monolith baseline. No worker/service deployment boundary is selected. | **No ADR now.** Python module boundaries are not deployable-service boundaries. | Separate deployable service/worker/process, RPC boundary, independent lifecycle/scaling boundary or topology-specific failure contract. |

**Overall decision: no ADR proposal is justified by the current Phase 2 code head.** Creating one now would standardize an unselected implementation mechanism and violate the project preference for reversible implementation and evidence-backed reuse.

## 5. Runtime-boundary hardening added by P2.11

P2.11 adds `reference/python/tests/test_p2_11_adr_runtime_boundary_hardening.py` to prevent the current bounded state from silently drifting across the reviewed threshold before the next architecture assessment.

The executable guards verify that:

1. semantic-owner modules still select no concrete durable database/repository or Event-transport technology;
2. `runtime_consistency.py` may compose Governed Execution plus Event admission for the logical canonical commit, but does not acquire projection, Product Contract or historical composition coupling;
3. `portability_runtime.py` cannot depend on mutation/runtime-consistency or historical composition paths and retains explicit internal/provisional/non-authoritative scope;
4. `product_contract.py` cannot acquire hidden Event persistence, runtime-state, portability or historical runtime dependencies;
5. repository/Event-delivery abstractions are not normalized into the shared semantic-owner runtime before a fresh ADR-gate assessment.

These guards intentionally do not prohibit a future governed architecture change. When an actual mechanism is selected, the appropriate ADR may change the tests together with the accepted decision.

## 6. Carried boundary debt disposition

### 6.1 `RuntimeConsistencyState` aggregate admission

The R2/R3/R4 observation remains valid: arbitrary durable/deserialized reconstruction of `RuntimeConsistencyState` would need an explicit trusted admission/reconstruction boundary. P2.11 does not hide or “solve” this by adding speculative persistence validation.

Current disposition remains **bounded/non-durable** because:

- the state is internal and not package-root exported;
- no persistence/deserialization boundary exists;
- no public schema claims that arbitrary reconstructed state is trusted;
- all current runtime evidence is produced in-process from immutable semantic values.

**Future trigger:** before durable/deserialized `RuntimeConsistencyState` or equivalent aggregate state is materially relied upon, re-open the ADR gate for persistence/repository and transaction/integrity boundaries. The durable design must not infer authority from mere successful deserialization.

### 6.2 Event admission versus delivery

The existing `runtime_consistency` coupling to `event_provenance` is intentional semantic coupling: a successful logical canonical mutation validates the required canonical Event before publishing the next immutable reference snapshot. It is not evidence of broker/store coupling.

Future Event persistence/delivery must remain separately governed and must preserve RFC-0006's distinction between canonical Event admission and delivery/receipt mechanics.

### 6.3 Portability/projection versus canonical mutation

P2.08 reconstruction and projection remain one-way bounded evidence: reconstructed semantic values and derived projections do not receive an implicit consequential mutation path. P2.11 preserves that dependency direction rather than adding a generic runtime/repository abstraction shared by mutation and projection.

## 7. Security, governance and reversibility assessment

The no-ADR decision does not weaken security or governance. It is safe precisely because no concrete external enforcement, persistence or transport boundary is being claimed.

Within the current M2 reference scope:

- missing durable/IAM/broker mechanisms are not represented as production controls;
- internal data structures do not become sources of Organizational Authority by persistence or reuse;
- projections remain non-authoritative;
- Product Contract validation does not become a hidden persistence/Event access path;
- no public compatibility commitment is created;
- no separately deployable service boundary is implied;
- future architecture remains free to choose a mechanism through a subordinate ADR once evidence requires it.

## 8. P2.11 exit assessment

P2.11 exit conditions are satisfied:

1. every runtime-boundary category listed by the roadmap has been explicitly assessed;
2. no materially constraining implementation choice currently lacks ADR coverage because none has crossed the ADR threshold;
3. no cross-cutting implementation treats provisional package, persistence, Event delivery, serialization, projection or topology boundaries as Accepted architecture;
4. targeted executable guards prevent accidental persistence/Event/projection/repository coupling from being normalized before a fresh decision;
5. the carried non-durable `RuntimeConsistencyState` limitation remains explicit rather than being concealed behind speculative infrastructure;
6. the next implementation slice is bounded and reversible.

**Final P2.11 decision: `PASS — ADR not required at the current runtime boundary.`**

## 9. Validation and bounded next slice

GitHub Actions `Reference Python CI` run `#76` completed successfully on executable P2.11 head `82fd2ad9346a9c8b82b01704bdbe47db06311431`.

After canonical roadmap synchronization, `Reference Python CI` run `#78` also completed successfully on synchronized PR head `22235394bf6fb510ff0c3d543c614fb2b7ac05dc`.

Proceed to **`P2.12 — Phase 2 / M2 closure review`**.

P2.12 is deliberately a review/closure slice, not a runtime expansion. Until M2 closure is decided, do not add durable persistence, concrete transaction/concurrency, Event delivery, IAM enforcement, evidence-integrity technology, public serialization/API, durable projection storage or service/process topology merely to prepare for Phase 3.

If P2.12 or subsequent Phase 3 planning produces a concrete need for one of those mechanisms, perform a fresh ADR-gate assessment first and create the minimum sufficient ADR before material implementation reliance.