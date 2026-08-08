# P2.08 Functional Cross-Review — Portability, Replay and Non-Authoritative Projection Runtime

Status: `Complete`
Date: `2026-08-08`
Task classification: `platform`
Constitution: `1.2.0`
Relevant Accepted RFCs: `RFC-0001`, `RFC-0002`, `RFC-0003`, `RFC-0005`, `RFC-0006`
Roadmap item: `P2.08`
Pull request: `#27`

## Scope

Review the bounded `P2.08` runtime implementation for architectural alignment, authority/security safety, semantic portability, replay safety, engineering maintainability and roadmap-stage proportionality.

This review is an execution-quality artifact. It is not formal RFC/ADR acceptance, capability activation, production-readiness approval or conformance certification.

## Iteration 1

Perspectives: architecture, engineering, security/privacy, governance.

### Material finding

The initial reconstruction path validated portable data by rebuilding actual `CanonicalRecord` objects and returned those same authority-capable runtime objects from `reconstruct_runtime_semantics`.

That shape created an authority-boundary risk: imported portability data could potentially be supplied to `pin_runtime_projection_source` as if it were an independently resolved canonical source. Even though the package and projection declared themselves non-authoritative, the returned object type could collapse the distinction in code.

### Remediation

The reconstruction path now uses existing Canonical Record / Typed Relationship / Event constructors only as private validation machinery, then converts validated meaning into frozen derived types:

- `ReconstructedCanonicalRecordSemantics`;
- `ReconstructedRelationshipSemantics`;
- `ReconstructedEventSemantics`;
- `ReconstructedRuntimeSemantics`.

Every reconstructed type is explicitly non-authoritative. `pin_runtime_projection_source` continues to require an independently supplied actual `CanonicalRecord` whose Subject Identity, exact Version Identity, semantic type, authority mode/scope and lifecycle attribution match the projection entry.

A regression test proves that a reconstructed record cannot substitute for an independent canonical source.

Result after remediation: material finding resolved.

## Iteration 2

Perspectives: architecture, engineering, security/privacy, governance.

### Architecture

Pass. The implementation preserves exact Subject/Version identity roles, immutable-version attribution, authority scope/mode, Typed Relationship endpoint-role semantics and Event correlation/causation semantics for the exercised bounded runtime scope. It does not introduce a second Canonical Head/Effective Version resolver, Event admission engine or Governed Execution path.

### Replay and authority safety

Pass. Replay has one input (`SemanticPortabilityPackage`) and only builds an immutable derived projection. No consequential-operation executor, external-effect callback, Event-admission adapter or canonical mutation path is exposed by replay. Projection entries and snapshots cannot claim canonical authority or mint governed pins.

### Security/privacy/isolation

Pass for the declared bounded scope. Export is restricted to one explicit Organization and the current reference runtime's Native authority mode. The format explicitly does not claim production export authorization, credentials/secrets export, cross-organization sharing, External Reference or Governed Replica portability contracts.

### Engineering and reversibility

Pass. The representation is explicitly `bounded-internal-provisional`; no database, broker, graph engine, schema registry, public API/SDK, durable projection store or stable cross-product wire contract is selected. The implementation remains reversible and migration-friendly, so the serialization/projection-storage/public-interface ADR gates remain uncrossed.

### Product/platform boundary

Pass. Runtime/test fixtures are domain-neutral and contain no procurement or other product-domain semantics.

### Validation

GitHub Actions `Reference Python CI` run `#52` on executable code head `628005d5baa8abb62284067b808abc84cdf37160` completed successfully: `Ran 281 tests in 0.283s` / `OK`.

The P2.08 focused suite includes two materially distinct round-trip scenarios plus negative paths for manifest drift, relationship/Event semantic drift, cross-Organization export, conflicting immutable Version Identity reuse, stale/mismatched canonical attribution, non-authority of reconstructed state and absence of replay effect/storage dependencies.

## Result

`Pass` for the declared bounded P2.08 scope.

No unresolved material objection remains after iteration 2. Further refinement before P2.09 would be disproportionate or would prematurely select durable/public portability infrastructure that the current roadmap intentionally defers.

## Explicit non-claims

P2.08 completion does not establish:

- a production export endpoint or disclosure authorization workflow;
- a stable public/cross-product serialization contract;
- External Reference or Governed Replica portability support in the bounded reference runtime;
- durable replay/projection storage;
- an `Active` Platform Capability;
- production readiness, SLA/support commitments or full RFC conformance.
