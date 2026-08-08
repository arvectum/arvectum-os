# P3.11 — Capability Admission / ADR / Refactoring Hardening Review

Status: `Complete`
Version: `1.0.0`
Date: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Phase: `Phase 3 — Shared Platform Capabilities`
Result: **`PASS — CAP-001 through CAP-004 are retained as bounded Incubating Platform Capabilities for the M3 baseline; no Active promotion, new ADR or material refactor is justified by the current evidence.`**

## 1. Purpose

P3.11 is the required decision gate after P3.10 architecture fitness and R8 milestone hardening and before P3.12/M3 closure.

It independently evaluates each retained Phase 3 capability against the RFC-0001 capability lifecycle and asks three separate questions:

1. **Capability admission:** does accumulated evidence still justify shared platform responsibility, or should the capability be contained, returned to product scope, replaced or retired?
2. **ADR gate:** has any concrete implementation mechanism become materially relied upon strongly enough to require an ADR before further reliance?
3. **Refactoring gate:** has reuse evidence or implementation pressure justified a material shared refactor, new abstraction or stable boundary?

P3.11 is not an operational-readiness review, Stable Product Contract decision, public API/SDK approval, production-readiness decision, SLA/support commitment or full-platform conformance claim.

## 2. Canonical authority checked

P3.11 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
3. RFC-0001 — Platform Capability lifecycle, domain-neutral admission, operational-readiness and commercial/conformance restraints;
4. RFC-0002 — Canonical Record, exact identity/version, authority and projection semantics;
5. RFC-0003 — deny-by-default security, Organization isolation, purpose/rights/classification, authority separation and failure-closed behavior;
6. RFC-0004 — Product Contract / Product Experiment boundaries and hidden-coupling prohibition;
7. RFC-0005 — Governed Execution and separation of authorization, Organizational Authority, validation and approval;
8. RFC-0006 — Event/provenance/reconstruction evidence and non-canonical observability semantics;
9. RFC-0007 — Memory/Knowledge lifecycle, governed retrieval and non-authoritative retrieval/index projections;
10. RFC-0008 — Document/Artifact identity, admission, exact reliance and derivation/handling constraints;
11. `docs/adrs/README.md` — no applicable Accepted ADR currently selects a concrete Phase 3 mechanism;
12. approved `DECISION-2026-08-08 — Engineering Quality and Refactoring Gates`;
13. Platform Capability Catalog and Phase 3 Provisional Capability Contracts;
14. P3.03 through P3.09 semantic-owner/reuse evidence;
15. P3.10 architecture fitness matrix — `PASS`;
16. R8 milestone hardening/code-health gate — `PASS` after the recorded CAP-004 fail-closed remediation.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was found.

The Decision Authority Policy remains `Proposed 0.2.1` and is not treated as approved delegation. Residual authority remains with the owner under the Accepted baseline.

## 3. Lifecycle standard applied

RFC-0001 requires an `Incubating` capability to retain an explicit source need, sponsoring consumers, bounded scope/budget, Provisional domain-neutral contract, Canonical Record/authority responsibilities, dependencies/events, security/data-handling rules, portability/migration behavior and exit criteria.

An `Active` capability additionally requires, among other applicable obligations:

- a supported stable public contract;
- declared compatibility and migration policy;
- accountable operational support;
- approved operational readiness proportionate to scope, consequence and customer commitments;
- measurable evidence appropriate to platform responsibility;
- maintained security, portability and lifecycle obligations.

Successful reference code, two synthetic bounded consumers, passing architecture fitness, or M3 closure cannot substitute for those `Active` requirements.

P3.11 therefore distinguishes two questions deliberately:

- **is the capability identity justified as shared platform responsibility?**
- **is the capability ready to become `Active`?**

The first is answered `yes` for the four retained Phase 3 capabilities within the bounded M3 baseline. The second is answered `no` on the current evidence.

## 4. Capability-by-capability disposition

| Capability | Shared-platform evidence | P3.11 disposition | Why not `Active` |
|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | RFC-0008 creates a universal governance need; P3.03 proves bounded domain-neutral identity/admission/derivation/exact-reliance semantics; P3.08 and P3.09 reuse the same capability contract across materially distinct consumer compositions without product-domain leakage; P3.10/R8 preserve portability and internal/provisional boundaries. | **Retain `Incubating / Provisional`.** Capability identity is admitted to the bounded M3 baseline; keep product document schemas, templates, business approvals, DMS/OCR/rendering/signing and storage technology outside the shared semantic owner. | No supported stable public contract, operational support/readiness, production storage/availability model, public compatibility policy or external reliance evidence. |
| `CAP-002 — Memory & Knowledge Governance` | Constitution/RFC-0007 establish a universal need for governed Memory/Knowledge semantics; P3.04 proves epistemic separation, promotion gates, governed retrieval and exact-version reliance; P3.08/P3.09 reuse the same contract across distinct consumer compositions; derived retrieval remains non-authoritative. | **Retain `Incubating / Provisional`.** Capability identity is admitted to the bounded M3 baseline; domain truth, ontologies, prompts, agents, scoring and business learning loops remain product-owned. | No stable supported public contract, operational readiness/support, durable retrieval/persistence design, customer workload evidence or production compatibility commitment. |
| `CAP-003 — Search / Index Projection` | RFC-0001/RFC-0002/RFC-0007/RFC-0008 require governed assets to remain discoverable without making projections authoritative; P3.05 proves source-version attribution, stale/missing/ambiguous handling, current constraint re-check and source resolution; P3.09 demonstrates reuse over both Knowledge and Document sources without changing capability semantics. | **Retain `Incubating / Provisional`.** The admitted capability is the governed discovery/projection responsibility, not a search/vector vendor, ranking policy or generic search product. | No stable query/ranking/public interface, durable projection topology, operational freshness/support model, production search technology decision or public compatibility obligation. |
| `CAP-004 — Audit / Reconstruction Support` | Constitution/RFC-0005/RFC-0006 establish cross-cutting reconstructability need; P3.06 proves read-oriented reconstruction and explicit evidence-status semantics; P3.08/P3.09 reuse the same reconstruction responsibility; R8 found and remediated a material fail-open evidence-constraint handoff and added negative-path evidence. | **Retain `Incubating / Provisional`.** Capability identity is admitted to the bounded M3 baseline; product compliance interpretation, reports, narratives and review UX remain product-owned. | No stable reconstruction/public schema, operational evidence-retention/support model, evidence-integrity technology decision, production observability topology or operational-readiness approval. |

**Capability admission decision:** retain exactly `CAP-001` through `CAP-004` as the validated bounded Phase 3 shared capability set. No capability is returned to product scope, replaced or retired at P3.11, and no new capability is admitted from the P3.08/P3.09 composition evidence.

## 5. Why CAP-003 remains a Platform Capability rather than commodity search infrastructure

P3.11 explicitly re-checks the strongest containment risk in the current set: generic search/index technology is commodity infrastructure and must not be mislabeled as platform organizational semantics.

CAP-003 remains justified only because its retained responsibility is narrower and semantic:

- project governed source identities and exact versions into disposable discovery state;
- preserve source attribution and freshness/staleness diagnostics;
- enforce Organization/security constraints at discovery;
- require separate exact governed-source resolution before consequential reliance;
- keep projection state rebuildable and non-authoritative.

Elasticsearch, OpenSearch, vector databases, lexical engines, caches, ranking algorithms and product query UX remain replaceable infrastructure or product behavior. If future implementation collapses CAP-003 into merely operating a shared search vendor, the capability must be re-reviewed for containment/retirement rather than preserved by name.

## 6. Product Contract and composition disposition

P3.08 and P3.09 provide the required bounded multi-consumer reuse evidence, but they do not create a stable shared product interface.

P3.11 therefore preserves the following boundaries:

- both bounded Product Contracts remain historical/validation evidence at `Provisional 0.1.0`;
- neither Product Contract becomes `Stable`;
- operation tokens remain internal evidence rather than stable method names;
- P3.08/P3.09 composition order remains consumer-owned;
- no generic composition/orchestration framework is admitted;
- no product-domain source schema, workflow, taxonomy or approval behavior is promoted into the platform;
- possession of a Product Contract or capability contract grants neither authorization nor Organizational Authority.

Any real Product relying on these capabilities, canonical platform state or shared history must create or update its own applicable RFC-0004 Product Contract before governed reliance.

## 7. ADR re-assessment

P3.11 re-opens the ADR gate over the concrete mechanism categories carried by P3.02, P3.10 and R8.

| Boundary | Current Phase 3 evidence | P3.11 ADR disposition | Future trigger |
|---|---|---|---|
| Durable persistence / database / object store / search-vector topology | Capability slices remain bounded in-memory semantic owners; no durable vendor or topology is required by capability correctness. | **No ADR now.** | First materially relied-upon durable repository/object/search topology or cross-capability persistence contract. |
| Transaction / concurrency | Phase 3 adds no new physical transaction, lock, CAS, distributed coordination or outbox/inbox mechanism above the bounded Core Runtime semantics. | **No ADR now.** | Concrete physical consistency/concurrency mechanism required for capability correctness. |
| Event transport / store | Capability semantics use governed evidence references without selecting broker, Event store, delivery checkpoint or consumer topology. | **No ADR now.** | Material reliance on a concrete Event delivery/store topology. |
| IAM / PDP / PEP | P3.07 models explicit access context and fail-closed boundaries but selects no IAM provider, policy language, entitlement store or enforcement topology. | **No ADR now.** | Concrete IAM/policy provider or enforcement topology shared across products/capabilities. |
| Evidence-integrity technology | Identity/provenance/integrity semantics are represented without claiming signing, hash-chain, WORM, ledger or external attestation as the governed integrity boundary. | **No ADR now.** | A concrete integrity mechanism becomes relied upon as organizational evidence. |
| Stable API / SDK / serialization | Package-root exposure remains provisional; operation names, dataclasses and Product Contract tokens are internal; no stable wire framework exists. | **No ADR now.** | First stable public/cross-product API, SDK, wire schema, serialization or compatibility boundary. |
| Durable projection / replay storage | CAP-003 projection is disposable/rebuildable and CAP-004 reconstruction is derived/read-oriented; neither has a durable operational store contract. | **No ADR now.** | Operational reliance on durable projection/reconstruction/checkpoint storage or freshness guarantees. |
| Deployable service / process topology | Phase 3 remains module-level reference code with no separate network/process lifecycle or failure contract. | **No ADR now.** | Separately deployable capability service/worker, RPC boundary, independent scaling or topology-specific failure semantics. |

**ADR decision:** no new ADR proposal is justified by the current Phase 3 head. Creating one now would standardize an implementation mechanism that the architecture and evidence still intentionally leave replaceable.

The ADR gate remains armed. A future material commitment in any row above must be governed before further reliance.

## 8. Refactoring hardening disposition

Result: **`No material refactor justified.`**

R8 already hardened code health and found no large refactor requirement after one targeted security remediation. P3.11 independently confirms that lifecycle/admission evidence does not create a reason to restructure the implementation.

Specifically, P3.11 rejects the following premature refactors:

- merging CAP-001 through CAP-004 semantic-owner modules merely because they are often consumed together;
- extracting P3.08/P3.09 composition into a generic platform workflow/composition framework;
- creating repository/provider/service abstractions before a durable mechanism is selected;
- stabilizing internal operation tokens, dataclasses, package-root exports or fixture shapes as public contracts;
- centralizing product-owned ranking, narrative, workflow or domain semantics into shared capability code;
- replacing local bounded validation duplication with a broad abstraction where no stable semantic contract has been demonstrated;
- optimizing or caching the bounded in-memory reference implementation without measured performance evidence.

The current module boundaries remain intentionally migration-friendly and preserve one semantic owner per retained responsibility.

## 9. P3.11 executable hardening evidence

P3.11 adds:

- `reference/python/tests/test_p3_11_capability_admission_hardening.py`.

The guard verifies the current P3.11 decision remains explicit until a later governed change:

1. the catalog retains exactly CAP-001 through CAP-004 as `Incubating / Provisional` after P3.11;
2. the two bounded consumer Product Contracts remain `Provisional 0.1.0` evidence rather than Stable/public contracts;
3. Phase 3 capability/reuse modules still select no concrete durable/transport/search/IAM/public-framework mechanism that would silently cross the reviewed ADR gate;
4. semantic-owner modules remain independent of consumer/reuse harnesses;
5. the package root remains explicitly provisional and not a public platform contract;
6. the canonical P3.11 review records no `Active` promotion, no new ADR and no material refactor.

These guards are not intended to forbid future governed architecture changes. When a later decision legitimately changes lifecycle or crosses an ADR/stable-boundary gate, the corresponding guard must change together with that canonical decision.

## 10. Documentation hardening finding

### P3.11-F1 — root README current-phase drift

Severity: `Minor — repository navigation / planning clarity`
Disposition: `Remediated in P3.11`

The canonical roadmap already records Phase 3 as Active and P3.11 as current, while the root README still described Phase 2 as not Active. The README is lower authority and therefore did not change canonical state, but the repository entry point could mislead contributors.

P3.11 synchronizes the README to the current Phase 3 state and preserves the explicit distinction between Phase status, capability lifecycle, operational readiness and conformance.

This is documentation hardening only. It does not change an Accepted RFC, capability contract or lifecycle decision.

## 11. Capability lifecycle and commercial disposition

After P3.11:

- `CAP-001 — Document & Artifact Governance`: `Incubating`, capability contract `Provisional`;
- `CAP-002 — Memory & Knowledge Governance`: `Incubating`, capability contract `Provisional`;
- `CAP-003 — Search / Index Projection`: `Incubating`, capability contract `Provisional`;
- `CAP-004 — Audit / Reconstruction Support`: `Incubating`, capability contract `Provisional`.

The retained set is sufficient to proceed to M3 closure review, but none is `Active`.

P3.11 creates no:

- Stable Product Contract;
- stable public/cross-product API or SDK;
- operational-readiness approval;
- production environment claim;
- support/SLA/HA commitment;
- customer-facing compatibility guarantee;
- full-platform or full-RFC conformance claim.

## 12. Exit assessment

P3.11 exit conditions are satisfied:

1. each Incubating capability has an explicit independent disposition;
2. all four retained capability identities remain justified by domain-neutral architecture plus materially distinct reuse evidence;
3. product-domain semantics and commodity infrastructure remain outside shared capability identity;
4. none of the RFC-0001 `Active` requirements is inferred from reference implementation success;
5. all declared ADR categories were re-assessed and none is currently crossed;
6. no material refactor or new abstraction is justified after R8 hardening;
7. the P3.08/P3.09 evidence remains Provisional and consumer-owned;
8. the root repository entry point is synchronized with the canonical Phase 3 state;
9. the remaining next slice is a closure decision rather than implementation expansion.

**Final P3.11 decision: `PASS — retain CAP-001 through CAP-004 as Incubating / Provisional; no Active promotion, ADR or material refactor required.`**

## 13. Next action

Proceed to **`P3.12 — Phase 3 / M3 closure review`**.

P3.12 must decide whether the accumulated bounded evidence is sufficient to declare `M3 — Validated shared capability baseline` achieved. It must not use closure as an uncontrolled implementation/refactoring phase and must not infer `Active` capability status, Stable Product Contracts, public API compatibility, production readiness or SLA/support obligations from M3 completion.
