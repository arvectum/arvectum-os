# P3.05 — Non-authoritative Search / Index Projection Candidate Slice Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P3.05 — Non-authoritative Search / Index Projection candidate slice`
Capability: `CAP-003 — Search / Index Projection`
Lifecycle: `Incubating`
Contract: `Provisional`
Result: **`PASS — the bounded CAP-003 slice provides rebuildable non-authoritative discovery with exact source/version attribution, explicit projection reconciliation state, fail-closed stale/missing/ambiguous behavior and governed-source resolution before reliance without selecting durable search/index technology or shared ranking semantics.`**

## 1. Scope

P3.05 implements the first executable bounded slice of CAP-003 above the Phase 2 Core Runtime and the governed source semantics already exercised by P3.03/P3.04.

The slice proves only:

- a discovery projection is derived/disposable state rather than Canonical Record authority;
- every projection entry retains exact governed source Subject Identity and Version Identity attribution;
- ordinary discovery is scoped to an explicit Organization and current source eligibility;
- current purpose, permitted-use right and classification constraints are re-evaluated before a projected text match is returned;
- projection reconciliation distinguishes `Current`, `Stale`, `Missing` and `Ambiguous` source state;
- stale, missing and ambiguous entries fail closed for ordinary discovery;
- a search hit does not grant access to its governed source or Organizational Authority;
- source resolution requires an explicit already-evaluated source-access decision and the exact current governed source version;
- a stale projected version cannot silently resolve to or be substituted by a newer source version;
- the complete projection may be rebuilt from current governed sources and the old derived state discarded.

It does not implement a durable search engine, vector database, embedding model, semantic ranking, recommendation system, saved-search behavior, product-domain taxonomy/filtering, public API/SDK, stable query language or serialization, Product Contract for a real product, production IAM/policy enforcement, operational readiness or `Active` capability promotion.

## 2. Canonical authority checked

P3.05 was evaluated against Constitution `1.2.0`, the RFC Index and Accepted RFC-0001 through RFC-0008, with RFC-0002 projection non-authority, RFC-0003 Organization/security/derived-data constraints, RFC-0007 retrieval/indexing boundaries and RFC-0008 search/index/document-source boundaries most directly relevant.

Subordinate boundaries checked:

- `docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md`;
- `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md`;
- `docs/reviews/R5-capability-boundary-review.md`;
- `docs/roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`;
- `docs/roadmap/ROADMAP.md`.

R5 records that no relevant Accepted ADR fixes a durable mechanism in this boundary. No conflict with Constitution `1.2.0` or the Accepted RFC baseline was found.

## 3. Implementation disposition

Implementation: `reference/python/arvectum_os_ref/search_index_projection.py`.

The module is internal, in-memory, Provisional and domain-neutral. It composes existing `CanonicalRecord`, `Identity` and `OrganizationScope` semantics rather than creating a second canonical-state, authority, identity or authorization engine.

`GovernedSearchSource` is a bounded source-owner handoff value: CAP-003 does not decide Canonical Head, Effective Version, Knowledge lifecycle, Document admission or authoritative-source semantics. The owning governed source boundary supplies the exact currently eligible Canonical Record, bounded searchable material and current discovery constraints.

`ProjectionEntry`, `SearchProjection`, `ProjectionDiagnostic` and `SearchHit` remain derived values and intentionally do not expose Canonical Record authority fields.

## 4. Projection and reconciliation semantics

`rebuild_projection()` accepts a unique current governed source per Organization/Subject and creates only derived entries containing:

- source Subject Identity;
- source Version Identity;
- source semantic type;
- Organization scope;
- bounded searchable text.

It rejects an ambiguous current source set rather than choosing one version heuristically.

`assess_projection_entry()` compares an existing derived entry with the current governed source set and returns one explicit state:

- `Current` — the exact projected source/version remains the unique current source supplied by its owner;
- `Stale` — the source subject remains current but at a different exact version;
- `Missing` — the source subject is no longer present in the current governed discovery set;
- `Ambiguous` — more than one current source or inconsistent semantic identity prevents unique resolution.

`inspect_projection()` exposes these reconciliation states without returning projected content. This supports rebuild/reconciliation evidence without upgrading the projection into organizational authority.

## 5. Discovery, rights and exact source resolution

`query_projection()` requires explicit Organization, purpose, right and allowed-classification context. It first resolves each candidate projection entry against the current governed source set and re-evaluates the current source constraints before matching projected text.

This ordering is intentional: stale projection metadata is not trusted merely because it remains physically present. Only `Current` entries may become ordinary `SearchHit` values. Stale, missing and ambiguous entries are suppressed rather than exposed as current discovery results.

The bounded matching algorithm is only case-insensitive substring containment. It is executable fixture behavior, not a platform relevance policy, query-language contract or ranking promise. CAP-003 therefore does not absorb product-owned ranking, recommendation, taxonomy or UX semantics.

`resolve_search_hit_for_reliance()` exits the projection boundary by resolving the exact governed Canonical Record. It requires explicit Organization context and an already-evaluated source-access decision. A search hit alone grants neither source access nor Organizational Authority. If the current governed source version differs from the hit version, resolution fails rather than substituting the newer version.

The bounded boolean source-access input is test-harness evidence only; P3.07 remains responsible for broader cross-capability security/rights/Organization enforcement composition.

## 6. Executable evidence

`reference/python/tests/test_p3_05_search_index_projection.py` adds 9 focused tests for:

1. projection non-authority;
2. exact source/version attribution across distinct governed source semantic types;
3. Organization/purpose/right/classification filtering;
4. re-evaluation of changed current constraints without trusting stale projection metadata;
5. explicit `Current`/`Stale`/`Missing`/`Ambiguous` diagnostics;
6. fail-closed ordinary query for stale/missing/ambiguous state;
7. separate source-access decision and exact source-version resolution before reliance;
8. complete rebuild from current sources replacing disposable stale state;
9. ambiguous rebuild and absent Organization context failing closed.

GitHub Actions `Reference Python CI` PR run `#85` passed the full accumulated reference suite on the executable P3.05 code head: `335 tests`, `OK`.

These tests become continuous P3.10 fitness evidence for CAP-003. They do not claim full RFC-0002, RFC-0003, RFC-0007 or RFC-0008 conformance and do not complete the broader P3.07 cross-capability enforcement scope.

## 7. Product-domain and capability boundary

No procurement/tender semantics, domain filters, taxonomies, recommendation rules, ranking model, saved-search behavior, product UI or business relevance policy is introduced.

The shared responsibility remains limited to non-authoritative discovery, exact source/version attribution, reconciliation state, governed source resolution and rebuildability. Search/vector/index engines remain replaceable infrastructure rather than capability identity.

P3.08 still owns the first bounded RFC-0004 Product Contract consumption proof. This P3.05 module must not be treated as a public/cross-product stable interface before that separate boundary is intentionally established.

## 8. Security, deletion and stale-state boundary

The slice supplies bounded executable evidence that:

- Organization context has no default fallback;
- current purpose/right/classification constraints are evaluated before returning a match;
- stale/missing/ambiguous source state fails closed for ordinary discovery;
- changed current constraints can suppress an existing physical projection entry before rebuild;
- discovery visibility does not itself grant access to underlying governed source state;
- stale exact versions cannot be silently substituted during source resolution.

This is intentionally not a complete IAM/PDP/PEP, deletion executor or cross-capability security implementation. P3.07 must prove the broader RFC-0003 composition across retained capabilities, including propagation of rights/deletion/Organization changes through capability interactions.

## 9. ADR gate assessment

**No new ADR is required for P3.05.**

The slice selects no durable search/vector/index engine, database, persistence model, index topology, embedding/reranking model, transaction/concurrency mechanism, Event transport/store, IAM/PDP/PEP technology, stable API/query language/serialization or separately deployable service/process topology.

The full projection is rebuilt from supplied governed source state and remains disposable. The matching rule exists only as a bounded deterministic test fixture and is explicitly not a shared relevance contract.

The ADR gate must be re-opened before material reliance on durable projection/replay storage, a concrete shared search/vector topology, stable query/wire compatibility, production authorization enforcement technology or separately deployable search service topology.

## 10. Exit assessment

P3.05 exit conditions are satisfied for the declared bounded slice:

- CAP-003 remains `Incubating` with a `Provisional` contract;
- projection state remains derived and non-authoritative;
- exact governed source identities/versions remain attributable;
- stale/missing/ambiguous state is explicit and ordinary discovery fails closed;
- current handling constraints are re-evaluated before match exposure;
- search visibility does not become source access or authority;
- source resolution never substitutes a different version;
- projection state is rebuildable and disposable;
- no product ranking/business semantics leak into the capability;
- no durable ADR boundary is crossed;
- no `Active`, production, SLA/support, stable-public-interface or full-conformance claim is made.

**Final result: `PASS — P3.05 complete for the bounded CAP-003 candidate-slice scope.`**

## 11. Next action

P3.06 remains the last initial bounded Incubating capability slice. P3.10 should continuously index this P3.05 evidence. After P3.06, continue with P3.07 cross-capability security/rights/Organization-scope enforcement, then the existing R6 gate.

CAP-003 must remain `Incubating` until later P3.08/P3.09 consumer/reuse evidence and P3.11 independent lifecycle disposition.
