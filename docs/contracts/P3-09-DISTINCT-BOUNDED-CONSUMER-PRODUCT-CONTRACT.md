# P3.09 Distinct Bounded Consumer Product Contract

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `product_contract`
Roadmap work item: `P3.09 — Shared-capability reuse and composition proof`
Authority: RFC-0004 `1.0.0` — `Accepted`
Capability baseline: `PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` `1.0.0`
Predecessor evidence: `P3-08-BOUNDED-CONSUMER-PRODUCT-CONTRACT.md` `0.1.0`

## 1. Purpose

This Product Contract defines the RFC-0004 boundary for a second synthetic bounded Product Experiment used only to prove materially distinct reuse and composition of the Phase 3 shared capabilities.

The experiment is intentionally different from the P3.08 document-led bounded consumer. Its reference workflow is discovery-led: it begins with non-authoritative discovery, resolves an exact governed source, and then composes exact Document, reconstruction and Knowledge reads under its own access context. The platform does not acquire or interpret that workflow meaning.

This contract exists to prove reuse, not to broaden capability semantics. It is `Provisional` and is not a Stable Product Contract, public API/SDK, production-support commitment, capability activation decision, SLA or commercial promise.

## 2. Contract identity and governed scope

- Product Contract subject identity: `product-contract-subject/p3-09-distinct-consumer@org-a`;
- Product Contract version identity: `product-contract-version/p3-09-distinct-consumer-v0.1.0@org-a`;
- Product Experiment identity: `product-experiment/p3-09-distinct-consumer@org-a`;
- Product Experiment version: `0.1.0`;
- accountable architectural owner: `ООО «Арвектум»`;
- Organization scope in executable proof: bounded reference Organization `org-a`;
- lifecycle: `Provisional`;
- operational scope: internal in-memory reference harness only;
- workflow proof: exact `platform.workflow` version for the discovery-led bounded composition;
- side-effect scope: read-only capability consumption; no product-caused canonical mutation.

The `org-a` identity and reference Workflow identity are test-harness fixtures, not tenant identifiers, public naming conventions or stable workflow types.

## 3. Shared capability dependencies

The second consumer depends on the same four Incubating capability contracts already exercised by P3.08. No second-consumer-specific capability operation is added.

| Capability | Lifecycle | Capability contract | Current internal operation token | Bounded effect |
|---|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Incubating` | Provisional `1.0.0` | `p3.08.resolve-document` | exact governed Document/Artifact read |
| `CAP-002 — Memory & Knowledge Governance` | `Incubating` | Provisional `1.0.0` | `p3.08.retrieve-knowledge` | constrained governed Knowledge retrieval |
| `CAP-003 — Search / Index Projection` | `Incubating` | Provisional `1.0.0` | `p3.08.discover-sources` | derived non-authoritative discovery |
| `CAP-003 — Search / Index Projection` | `Incubating` | Provisional `1.0.0` | `p3.08.resolve-search-source` | exact governed source resolution after discovery |
| `CAP-004 — Audit / Reconstruction Support` | `Incubating` | Provisional `1.0.0` | `p3.08.reconstruct-execution` | derived read-oriented reconstruction |

The `p3.08.*` tokens are reused only as current internal reference-fixture identifiers. Their reuse in P3.09 does not stabilize them, create a public cross-product API or make the token names part of capability identity. Renaming or replacing them remains permitted through a bounded Provisional-contract migration.

## 4. Materially distinct composition

P3.08 demonstrated a document-led bounded consumer composition. This Product Experiment demonstrates a discovery-led composition over the same shared capability semantics:

1. CAP-003 derived discovery;
2. CAP-003 exact governed source resolution;
3. CAP-001 exact Document/Artifact resolution;
4. CAP-004 read-oriented reconstruction;
5. CAP-002 constrained validated-Knowledge retrieval.

The operation order and exact Workflow Version Identity are consumer-owned evidence. Arvectum OS does not introduce a generic composition language, platform workflow template, orchestration DSL or shared business workflow to express this proof.

Each operation remains independently admitted through this Product Contract and the current RFC-0003/P3.07 access context.

## 5. Provider and consumer responsibilities

The platform-side responsibility is unchanged from the Phase 3 Provisional capability contracts.

The consumer MUST:

- use this exact Product Contract version for the bounded P3.09 proof;
- pin its exact bounded Workflow version in reuse evidence;
- declare the exact capability dependency, Provisional contract version and operation for every capability use;
- remain inside the Product Contract Organization scope;
- carry its own current access context into protected capability access;
- preserve exact governed source/version attribution when leaving derived discovery or reconstruction views;
- fail closed on undeclared dependency, version, operation, source read, Organization or product mismatch;
- never borrow the P3.08 consumer's Product Contract, access context or undeclared canonical-read surface;
- never fall back to internal tables, internal imports, undocumented endpoints, private Event streams, direct index/store access or implicit shared state.

The consumer MUST NOT infer permission, Organizational Authority, approval, delegation, lifecycle `Active`, production readiness or stable compatibility from possession of this contract or from successful capability invocation.

## 6. Product-owned semantics and non-broadening rule

No tender, procurement, finance, CRM, legal, marketing or other product-domain type is added to the shared platform boundary.

The synthetic consumer owns its local workflow purpose, query text, sequence, rendered views and other presentation/orchestration choices. The platform proof treats these only as bounded inputs to existing domain-neutral capability contracts.

A second consumer requirement that cannot be represented without adding product-domain meaning to CAP-001 through CAP-004 MUST remain product-owned or trigger a separate governed capability-contract review. P3.09 MUST NOT silently generalize the shared contract merely to make this proof pass.

## 7. Canonical state and authority

The executable fixture remains read-only.

It exercises:

- `platform.document` / `platform.document/state` — canonical read only;
- `platform.knowledge` / `platform.knowledge/state` — canonical read only;
- CAP-003 derived discovery over exact governed source identity/version, including a `platform.document` source in the distinct-consumer proof;
- CAP-004 derived/read-oriented reconstruction without source-authority replacement.

Using a different governed source semantic type under CAP-003 does not broaden CAP-003 authority. The Product Contract must still explicitly declare the exact canonical source read required when the consumer exits discovery for reliance.

The fixture authorizes no canonical writes and creates no new shared authoritative state.

## 8. Security, authority and Organization isolation

Every operation preserves RFC-0003 separation among authentication evidence, authorization, Organizational Authority/approval and data governance.

For P3.09 executable evidence:

- Organization scope is explicit and matches this Product Contract;
- the second consumer uses its own attributable actor and access context;
- protected operations retain `Authorization` and `DataGovernance` boundaries;
- cross-product Product Contract borrowing fails closed;
- one consumer's canonical-read declaration does not expand the other's declaration;
- discovery visibility does not grant underlying source access;
- Product Contract or reuse-proof admission creates no permission, approval, delegation or Organizational Authority.

Reference fixture purposes such as `review` and `triage`, right `read` and classification `internal` are test-only and do not establish a policy vocabulary.

## 9. Events, artifacts and shared history

The consumer may read retained governed execution/Event/evidence references only through the bounded CAP-004 reconstruction operation.

P3.09 does not authorize the second consumer to emit new shared platform Events, mutate shared execution history, create governed Artifacts, promote Memory/Knowledge or cause external effects.

Consumer-local logs, proof objects and rendered views remain transient/non-authoritative unless separately admitted through applicable governance.

## 10. Failure behavior

Failure remains closed at each Product Contract and capability boundary.

The second consumer rejects:

- missing or non-`Provisional` Product Contract reliance;
- borrowed Product Contract identity from the first consumer;
- product identity/version mismatch;
- Organization mismatch;
- undeclared or missing shared capability operation;
- incompatible capability contract version;
- omission of required authorization/data-governance boundaries;
- undeclared canonical source read;
- hidden internal coupling mechanisms;
- a purported reuse witness that merely duplicates the first consumer's exact operation composition.

Failure MUST NOT broaden platform semantics or fall back to platform internals.

## 11. Portability, compatibility and migration

The consumer relies on governed identities, exact immutable versions and the existing domain-neutral capability semantics. Derived search and reconstruction state remains rebuildable or regenerable from retained governed sources.

Compatibility is intentionally narrow:

- exact Product Contract version `0.1.0`;
- exact Phase 3 Provisional capability-contract baseline `1.0.0`;
- internal in-memory reference implementation only.

The current internal operation tokens are not a compatibility promise. A material capability-contract change requires review and, where necessary, a new immutable Product Contract version.

No database, object store, search engine, Event transport, serialization format, SDK, service boundary, workflow engine or deployment topology is part of this contract identity.

## 12. Review and exit path

Review condition: `P3.11` or earlier if a material capability-contract/security/authority boundary changes.

Exit paths:

- revise through a new immutable `Provisional` Product Contract version;
- contain or retire the synthetic Product Experiment after Phase 3 evidence is sufficient;
- keep composition product-owned rather than promoting it into a platform capability;
- stabilize only through a separate RFC-0004 lifecycle decision with required compatibility, migration, support and conformance evidence.

This contract does not promote CAP-001 through CAP-004. All remain `Incubating` until a separate lifecycle decision.

## 13. ADR gate assessment

No new ADR is crossed because this Product Contract selects no durable persistence, object-store/search topology, transaction/concurrency mechanism, Event transport/store, IAM/PDP/PEP, evidence-integrity technology, stable API/serialization, workflow engine or separately deployable service/process topology.

Material reliance on any such mechanism re-opens the Phase 3 ADR gate.
