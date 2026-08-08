# P4.07 — Memory / Knowledge / Search discovery experience review

Status: `Complete / PASS`
Date: `2026-08-08`
Task classification: `platform`
Owner: `ООО «Арвектум»`
Roadmap item: `P4.07 — Memory / Knowledge / Search discovery experience`

## 1. Canonical basis checked

This review was performed against the canonical repository state, not chat memory.

Checked normative basis:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `1.0.0` — `Accepted`;
- RFC-0006 `Event, Provenance and Observability Model` `1.0.0` — `Accepted`;
- RFC-0007 `Memory, Knowledge and Governed Learning Lifecycle` `1.0.0` — `Accepted`;
- RFC Index — current Accepted set confirmed;
- ADR Index — no applicable Accepted ADR requires or authorizes a durable search/vector/RAG/frontend/API technology choice for this bounded slice;
- Phase 3 reviews for CAP-002, CAP-003 and P3.07 current cross-capability enforcement;
- P4.02 workspace shell and P4.03–P4.06 operator-boundary evidence.

No conflict with Constitution or Accepted RFC was found. No Constitution amendment, new RFC, Accepted RFC modification, ADR, Product Contract, capability lifecycle promotion or public compatibility commitment is required for this bounded internal implementation.

## 2. Scope implemented

P4.07 adds a reversible internal presentation/resolution adapter over the existing semantic owners rather than creating another Memory/Knowledge/Search engine.

Implementation:

- `reference/python/arvectum_os_ref/memory_knowledge_search_experience.py`;
- `reference/python/examples/p4_07_memory_knowledge_search_demo.py`;
- `reference/python/tests/test_p4_07_memory_knowledge_search_experience.py`;
- `reference/python/tests/test_p4_07_discovery_hardening.py`;
- `reference/python/tests/test_p4_07_semantic_owner_hardening.py`;
- `reference/python/tests/test_p4_07_demo.py`.

The adapter remains internal and is not exported as a package-root public platform contract.

## 3. Epistemic distinctions preserved

The operator surface keeps four roles materially distinct:

1. `Observation` — evidence/input, non-Knowledge;
2. `Organizational Memory` — governed retained context that preserves the remembered epistemic role without truth upgrade;
3. `Knowledge Candidate` — non-Knowledge even when validation or review evidence is visible;
4. validated `Knowledge` — governed organizational understanding only within its declared scope, exact Version, freshness and provenance.

Presentation exposes no promotion operation. Browsing, search results, AI-like discovery, validation text or an approval reference cannot themselves perform `KnowledgeCandidate → Knowledge` promotion.

## 4. Exact Knowledge reliance

Consequential reliance does not follow a later Head implicitly and does not treat a search result as authoritative.

For validated Knowledge the adapter:

- preserves stable Subject Identity and exact Knowledge Version Identity;
- requires the operator to explicitly select the exact displayed Version;
- rejects stale/review-required Knowledge for consequential reliance;
- rechecks the current Actor/Organization access context and current source authorization;
- rechecks purpose/right/classification/freshness through the existing P3.07/CAP-002 boundary;
- resolves exact lineage and delegates the final exact-reliance proof to the existing CAP-002 semantic owner.

A forged/stale presentation object therefore cannot create consequential reliance on its own.

## 5. Search / discovery authority boundary

CAP-003 remains a disposable, derived, non-authoritative discovery projection.

The surface:

- labels search/index/RAG-like results as `Derived discovery/projection — non-authoritative`;
- carries exact source Subject and Version attribution;
- resolves each hit back to the current exact governed source before presenting protected source metadata;
- rejects stale, missing or ambiguous projection/source state through existing CAP-003/P3.07 semantics;
- distinguishes `projection unavailable` from `source absent` and makes no source-absence inference from a missing projection;
- does not expose ranking/confidence as truth, validation, permission, approval or Organizational Authority;
- displays only a bounded minimized search preview;
- makes consequential Knowledge reliance exit the projection through exact current source resolution and then CAP-002 exact reliance.

Search technology, vector store, embedding model, LLM provider, ranking algorithm and RAG implementation remain deliberately unselected.

## 6. Security, rights and minimization result

Protected learning/search state is presented only after current context checks.

The implementation enforces:

- workspace Actor and Organization equality with the retrieval context;
- Actor/Organization-bound current source authorization before protected source metadata;
- fail-closed behavior for missing, duplicate or denied source-authorization evidence;
- purpose/right/classification enforcement;
- CAP-002 Knowledge freshness on consequential reliance;
- CAP-002 Memory handling constraints in addition to CAP-003 discovery constraints, so a broader search projection cannot widen the semantic owner's access policy;
- exact source ambiguity handling for duplicate Memory or Knowledge representations;
- omission of unauthorized/ambiguous/handling-ineligible items without protected counts;
- HTML escaping of governed text;
- bounded preview minimization.

Identity possession, a search hit, a UI role label or an approval-looking field creates neither Authorization nor Organizational Authority.

## 7. Functional cross-review

Five functional cross-review iterations were completed.

### Iteration 1 — epistemic / lifecycle semantics

Checked Observation, Memory, Candidate and validated Knowledge distinctions; exact Version reliance; non-promotion; stale Knowledge behavior.

Result: `PASS`.

### Iteration 2 — authorization / Organization isolation / minimization

Checked Actor/Organization request binding, current source authorization, duplicate authorization evidence, purpose/right/classification filtering, protected counts and preview minimization.

Result: `PASS`.

### Iteration 3 — derived discovery / exact-source binding

Findings:

- exact Subject/Version IDs alone were not sufficient to prove that a CAP-002 validated object was the same exact Canonical Record resolved from CAP-003;
- an absent projection needed an explicit `projection unavailable` state rather than an ambiguous empty result.

Remediation:

- Knowledge search results now require exact Canonical Record equality with the resolved governed source;
- missing projection now explicitly states that no inference is made about canonical source absence;
- exact search reliance rechecks current workspace/access context.

Result after regression tests: `PASS`.

### Iteration 4 — cross-capability semantic-owner policy / ambiguity

Findings:

- CAP-003 discovery constraints could otherwise be more permissive than CAP-002 Memory constraints;
- duplicate exact Memory/Knowledge objects could otherwise be presented as if exact-source resolution were unambiguous.

Remediation:

- Memory search results must satisfy both CAP-003 discovery constraints and CAP-002 Memory handling constraints;
- duplicate exact Memory/Knowledge sources fail closed and are omitted without protected counts.

Result after regression tests: `PASS`.

### Iteration 5 — technology / governance / accidental contract review

Checked package exports, network/process dependencies, promotion helpers, durable storage, frontend/API/route contracts, vector/RAG/LLM dependencies, product-domain leakage and lifecycle claims.

Result: `PASS`; no material finding remains in the bounded P4.07 scope.

## 8. Executable evidence

Implementation-head CI evidence before canonical roadmap synchronization:

- GitHub Actions `Reference Python CI #164` — `PASS`;
- Python `3.12.13`;
- `521` tests;
- result: `OK`.

The static demo renders the workspace shell plus Memory/Knowledge and Discover states without a server, frontend framework or network dependency. It is presentation evidence only, not a public UI/API contract.

A final synchronized-head CI run is required after this review and roadmap/README synchronization before merge.

## 9. ADR / architecture disposition

No ADR threshold was crossed.

Still unselected:

- durable search/index/vector technology;
- embedding or LLM provider;
- ranking model;
- RAG orchestration/runtime;
- durable workspace/read-model/cache storage;
- public REST/GraphQL/gRPC route or wire contract;
- frontend framework/BFF topology;
- IAM/PDP/PEP vendor/mechanism;
- separately deployable search/UI service topology.

If later implementation materially relies on any such durable or externally constraining choice, the ADR gate must be reopened before that dependency is normalized.

## 10. Capability and conformance disposition

P4.07 completion does **not**:

- promote CAP-002 or CAP-003 to `Active`;
- create a new Platform Capability;
- claim Production operational readiness;
- claim full-platform conformance;
- create a Product Contract;
- create a public support/SLA/compatibility commitment.

The existing shared capability lifecycle remains `Incubating / Provisional` within the already accepted Phase 3 evidence scope.

## 11. Completion decision

`P4.07 — Memory / Knowledge / Search discovery experience` is `Complete / PASS` within the bounded internal Phase 4 reference scope.

The next canonical action is the roadmap-mandated engineering gate:

> `R10 — Operator Safety / Cross-Capability Health Review`

P4.08 must not begin as the canonical current action until R10 has reviewed the accumulated P4.03–P4.07 cross-capability security, rights, derived-state honesty, repeated UX patterns and code health.
