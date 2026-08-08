# P3.08 Bounded Consumer Product Contract

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Roadmap work item: `P3.08 — Product Contract consumption boundary + bounded consumer proof`
Authority: RFC-0004 `1.0.0` — `Accepted`
Capability baseline: `PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` `1.0.0`

## 1. Purpose

This Product Contract defines the minimum RFC-0004 boundary for one synthetic bounded Product Experiment used only to prove Phase 3 capability consumption.

The experiment is intentionally product-style rather than a real commercial product. It exists to prove that a consumer can rely on CAP-001 through CAP-004 without direct access to platform internals, without importing product-domain semantics into the platform and without treating Incubating capabilities as stable public contracts.

This contract is `Provisional`. It is not a Stable Product Contract, public API/SDK, production-support commitment, capability activation decision, SLA or commercial promise.

## 2. Contract identity and governed scope

- Product Contract subject identity: `product-contract-subject/p3-08-bounded-consumer@org-a`;
- Product Contract version identity: `product-contract-version/p3-08-bounded-consumer-v0.1.0@org-a`;
- Product Experiment identity: `product-experiment/p3-08-bounded-consumer@org-a`;
- Product Experiment version: `0.1.0`;
- accountable architectural owner: `ООО «Арвектум»`;
- Organization scope in executable proof: bounded reference Organization `org-a`;
- lifecycle: `Provisional`;
- operational scope: internal in-memory reference harness only;
- side-effect scope: read-only capability consumption; no product-caused canonical mutation.

The `org-a` identity is a reference-harness fixture, not a tenant identifier or public naming convention.

## 3. Bounded interaction scope

The consumer may perform only the following internal reference operations:

| Capability | Lifecycle | Capability contract | Bounded operation token | Boundary effect |
|---|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Incubating` | Provisional `1.0.0` | `p3.08.resolve-document` | exact governed Document/Artifact read |
| `CAP-002 — Memory & Knowledge Governance` | `Incubating` | Provisional `1.0.0` | `p3.08.retrieve-knowledge` | constrained governed Knowledge retrieval |
| `CAP-003 — Search / Index Projection` | `Incubating` | Provisional `1.0.0` | `p3.08.discover-sources` | derived non-authoritative discovery |
| `CAP-003 — Search / Index Projection` | `Incubating` | Provisional `1.0.0` | `p3.08.resolve-search-source` | exact governed source resolution after discovery |
| `CAP-004 — Audit / Reconstruction Support` | `Incubating` | Provisional `1.0.0` | `p3.08.reconstruct-execution` | derived read-oriented reconstruction |

These operation tokens are internal executable evidence only. They are not stable interface names, protocol methods or cross-product compatibility commitments.

## 4. Provider and consumer responsibilities

For every dependency, the platform-side responsibility is limited to the bounded Incubating semantics already declared by the Phase 3 Provisional capability contracts.

The consumer MUST:

- use this exact Product Contract version for the bounded proof;
- declare the exact capability dependency, provisional contract version and operation;
- remain inside the Product Contract Organization scope;
- carry the current P3.07 access context into protected capability access;
- preserve exact governed source/version attribution where consequential reliance exits a derived projection;
- fail closed on undeclared dependency, version, operation, source read or Organization mismatch;
- never fall back to internal tables, internal imports, undocumented endpoints, private Event streams, direct index/store access or implicit shared state.

The consumer MUST NOT infer permission, Organizational Authority, approval, delegation, lifecycle `Active`, production readiness or stable compatibility from possession of this contract or from successful capability invocation.

## 5. Product-owned semantics at the boundary

No tender, procurement, finance, CRM, legal, marketing or other domain type crosses this bounded Product Contract.

The synthetic consumer owns only its local presentation and orchestration semantics. Query text and rendered consumer views remain product-local/transient unless separately promoted through applicable governance.

Platform capabilities continue to expose domain-neutral governed identities, versions, constraints and reconstruction references only.

## 6. Canonical state and authority

The bounded executable fixture exercises read-only Native authority for the governed source records it directly resolves:

- `platform.document` / `platform.document/state` — canonical read only;
- `platform.knowledge` / `platform.knowledge/state` — canonical read only;
- CAP-003 discovery entries remain derived/non-authoritative and cannot replace their governed source;
- CAP-004 reconstruction views remain derived/read-oriented and cannot replace execution/Event/evidence authority.

The fixture does not authorize canonical writes.

If a later consumer relies on `External Reference` or `Governed Replica` authority, that authority mode, authoritative source, freshness/synchronization and failure behavior MUST be declared explicitly in a revised Product Contract. This contract does not silently generalize the bounded Native fixture to those modes.

## 7. Security, authority and data handling

Every bounded operation preserves RFC-0003 separation among authentication evidence, authorization, Organizational Authority/approval and data governance.

For executable P3.08 evidence:

- Organization context is explicit and must match the Product Contract;
- protected capability access receives the P3.07 `AccessRequest` with explicit purpose, required permitted-use right and allowed classifications;
- operation declarations preserve `Authorization` and `DataGovernance` boundaries;
- cross-Organization access is denied by default;
- discovery visibility does not grant source access;
- current access context does not create approval, delegation or Organizational Authority;
- Product Contract validation does not itself satisfy a security or authority decision.

The concrete fixture values such as purpose `review`, right `read` and classification `internal` are test evidence only, not a stable policy vocabulary.

No IAM provider, PDP/PEP, policy language, entitlement store or authentication protocol is selected.

## 8. Events, artifacts and shared history

The consumer may read governed execution/Event/evidence references only through the bounded CAP-004 reconstruction operation.

This Product Contract does not authorize the consumer to emit new shared platform Events, write shared execution history or create governed Artifacts as part of P3.08.

Consumer-local logs, presentation views and test outputs remain transient/non-authoritative unless separately admitted as governed state.

## 9. Failure behavior

Failure is closed at the Product Contract boundary.

The bounded consumer rejects:

- missing or non-`Provisional` Product Contract reliance;
- product identity/version mismatch;
- Organization mismatch;
- undeclared capability dependency;
- incompatible capability contract version;
- undeclared operation;
- non-read-only operation in this bounded proof;
- omission of required authorization/data-governance boundary declarations;
- undeclared canonical source read;
- hidden internal coupling mechanisms.

A failure MUST NOT fall back to a platform internal table, store, index, import, private stream or undocumented convention.

## 10. Portability, compatibility and migration

The consumer relies only on governed organizational semantics and exact identities/version references. Derived search and reconstruction state remains rebuildable or regenerable from retained governed sources.

Compatibility is intentionally narrow:

- exact Product Contract version `0.1.0`;
- exact Phase 3 Provisional capability-contract baseline `1.0.0`;
- internal in-memory reference implementation only.

Any material capability-contract change requires review and, where necessary, a new immutable Product Contract version. There is no public compatibility promise.

No database, object store, search engine, Event transport, serialization format, SDK, service boundary or deployment topology is part of this contract identity.

## 11. Review and exit path

Review condition: `P3.11` or earlier if a material capability-contract/security/authority boundary changes.

Exit paths:

- revise through a new immutable `Provisional` Product Contract version;
- contain or retire the synthetic Product Experiment after Phase 3 evidence is sufficient;
- stabilize only through a separate RFC-0004 lifecycle decision with the required compatibility, migration, support and conformance evidence.

This contract does not promote CAP-001 through CAP-004. All remain `Incubating` until a separate lifecycle decision.

## 12. ADR gate assessment

No new ADR is crossed by this Product Contract because it selects no durable persistence, object-store/search topology, transaction/concurrency mechanism, Event transport/store, IAM/PDP/PEP, evidence-integrity technology, stable API/serialization or separately deployable service/process topology.

Material reliance on any such mechanism re-opens the Phase 3 ADR gate.
