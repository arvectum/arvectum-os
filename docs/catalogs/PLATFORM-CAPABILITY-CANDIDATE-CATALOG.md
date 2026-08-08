# Arvectum OS Platform Capability Candidate Catalog

Status: `Active`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Lifecycle authority: RFC-0001 `1.0.0` — `Accepted`
Phase source: [`PHASE-3-SHARED-PLATFORM-CAPABILITIES.md`](../roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md)
Created by work item: `P3.01 — Capability boundary revalidation + Candidate catalog`

## 1. Purpose and authority

This catalog records the bounded initial set of Arvectum OS Platform Capability **Candidates** admitted for Phase 3 evaluation.

It is a subordinate catalog under Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008. It does not amend an Accepted RFC, create a stable public contract, select infrastructure, authorize production use or promote any capability to `Incubating` or `Active`.

RFC-0001 requires every `Candidate` capability to declare:

- proposed organizational outcome;
- accountable architectural owner;
- sponsor or constitutional rationale;
- intended domain-neutral boundary;
- expected consumers or strategic need;
- reuse hypothesis;
- review date;
- criteria for incubation, containment or rejection.

A `Candidate` does not require an implemented contract or implementation commitment.

## 2. Boundary revalidation decision

P3.01 revalidated the Phase 3 inventory against:

- M2 evidence from the bounded reusable Core Runtime;
- Constitution `1.2.0`;
- Accepted RFC-0001 through RFC-0008;
- RFC-0004 product/platform boundary rules;
- RFC-0003 security, authorization, Organization and portability invariants;
- RFC-0006 Event/provenance/observability semantics;
- RFC-0007 Memory/Knowledge semantics;
- RFC-0008 Document/Artifact semantics;
- the P2.11 ADR-gate disposition.

Result:

1. retain four domain-neutral responsibilities as lifecycle `Candidate` entries;
2. do not admit product-domain behavior, generic utility services or commodity infrastructure as Platform Capability candidates merely because they may be useful;
3. keep search/index and audit/reconstruction explicitly derived/non-authoritative;
4. keep storage, retrieval, IAM, observability and deployment technologies replaceable and outside capability identity;
5. require P3.02 before any retained candidate may move to `Incubating` or acquire a Provisional capability contract;
6. require a fresh ADR assessment before material reliance on a concrete durable or externally depended-upon mechanism.

## 3. Candidate summary

| ID | Candidate | Lifecycle | Primary architecture basis | Review date |
|---|---|---|---|---|
| `CAP-001` | Document & Artifact Governance | `Candidate` | RFC-0008 | `2026-09-08` |
| `CAP-002` | Memory & Knowledge Governance | `Candidate` | RFC-0007 | `2026-09-08` |
| `CAP-003` | Search / Index Projection | `Candidate` | RFC-0001; RFC-0007; RFC-0008 | `2026-09-08` |
| `CAP-004` | Audit / Reconstruction Support | `Candidate` | RFC-0006; RFC-0005 | `2026-09-08` |

All entries must also be reviewed at P3.11 if that gate is reached before the stated date.

## 4. Candidate records

### CAP-001 — Document & Artifact Governance

**Lifecycle:** `Candidate`

**Proposed organizational outcome:** provide one reusable domain-neutral way to identify, version, admit, derive, attribute and rely on governed Documents and Artifacts without confusing files, storage locations or transient outputs with organizational authority.

**Accountable architectural owner:** `ООО «Арвектум»` — platform architecture owner.

**Sponsor / constitutional rationale:** Constitution Articles III, XV and XVI require domain-neutral shared foundations, versioning of significant governed objects and governed organizational assets. RFC-0008 already defines the binding domain-neutral Document/Artifact architecture; Phase 3 evaluates whether a bounded reusable implementation should become shared platform responsibility.

**Domain-neutral boundary:**

- logical Document Subject Identity and immutable Document Version Identity;
- governed admission/checkpoint semantics before consequential reliance;
- Artifact/content identity and manifest relationships where applicable;
- derivation provenance and exact-version reliance;
- handling-constraint propagation;
- transient output versus governed asset/canonical-state distinction;
- storage-provider independence.

The capability must not encode tender, procurement, marketing, legal, finance or other product-domain document semantics.

**Expected consumers / strategic need:** P3.03 provides the first bounded shared slice; P3.08/P3.09 must demonstrate governed consumption and reuse across materially distinct bounded consumers before a stronger platform-centralization claim is made. Strategic need exists because Documents and Artifacts are explicitly part of the Executable Organizational Model and are common governed inputs/outputs across products and workflows.

**Reuse hypothesis:** products and workflows can reuse the same identity/version/admission/provenance/derivation semantics while keeping their own document types, taxonomies and business rules.

**Review date:** `2026-09-08`, or earlier at P3.11.

**Incubation criteria:**

- P3.02 records a bounded Provisional capability contract and owner;
- source need and initial sponsoring consumer(s) are explicit;
- scope remains domain-neutral and reversible;
- canonical authority and exact-version responsibilities are explicit;
- RFC-0003 handling constraints and RFC-0006 provenance requirements are preserved;
- no durable storage/API/topology choice is materialized without an ADR-gate assessment.

**Containment criteria:** return document type systems, templates, domain taxonomies, business approvals, legal-signature rules and product UX/workflows to the relevant product; keep any storage/OCR/rendering implementation behind replaceable adapters.

**Rejection criteria:** reject centralized platform responsibility if bounded evidence shows no meaningful reuse beyond one product, if the abstraction requires domain behavior, or if the only shared element is commodity file/storage tooling without shared organizational semantics.

**Explicit product-owned / commodity boundary:** product-specific document schemas, templates, taxonomies, approval rules and workflows remain product-owned. DMS/object store, filesystem, OCR, conversion, rendering, signing provider and similar infrastructure are implementation dependencies, not the capability itself.

---

### CAP-002 — Memory & Knowledge Governance

**Lifecycle:** `Candidate`

**Proposed organizational outcome:** preserve and reuse organizational memory and validated knowledge through explicit lifecycle, provenance, scope, rights and exact-version reliance without allowing observations, AI output, vector indexes or repeated assertions to become truth or authority automatically.

**Accountable architectural owner:** `ООО «Арвектум»` — platform architecture owner.

**Sponsor / constitutional rationale:** Constitution Articles 0, V, VI and XXI make organizational intelligence, memory, validated knowledge and governed learning core purposes of Arvectum OS. RFC-0007 defines binding domain-neutral semantics but explicitly does not activate a capability.

**Domain-neutral boundary:**

- Observation, Organizational Memory, Knowledge Candidate and validated Knowledge remain distinct;
- governed retrieval under Organization, authorization, purpose, classification, rights, lifecycle and freshness constraints where applicable;
- explicit candidate/promotion path;
- exact effective Knowledge Version attribution for consequential reliance;
- validation distinct from approval and Organizational Authority;
- derived retrieval representations remain non-canonical;
- AI cannot silently promote, broaden scope, retention or reuse.

**Expected consumers / strategic need:** P3.04 provides the first bounded shared slice. P3.08/P3.09 must demonstrate governed consumption/reuse before stronger platform responsibility is justified. Strategic need follows directly from the platform purpose: organizational intelligence must compound rather than remain transient product-local output.

**Reuse hypothesis:** products and workflows can reuse the same memory/knowledge lifecycle, retrieval controls, promotion gates and exact-version reliance while retaining domain-specific knowledge, validation rules and business meaning.

**Review date:** `2026-09-08`, or earlier at P3.11.

**Incubation criteria:**

- P3.02 records a bounded Provisional capability contract and owner;
- sponsoring consumer(s) and source need are explicit;
- promotion/retrieval boundaries remain domain-neutral;
- RFC-0003 rights/scope/privacy controls and RFC-0006 provenance are preserved;
- no vector/search/model provider or persistence technology becomes canonical authority;
- portability/migration and rejection paths remain explicit.

**Containment criteria:** keep domain knowledge bases, product prompts, agent behavior, product-specific ontologies, validation/scoring rules and business-specific learning loops inside the product unless separately promoted through evidence-based admission.

**Rejection criteria:** reject centralized platform responsibility if reuse is not demonstrated, if platform semantics would need domain-specific truth/validation rules, or if the proposed capability collapses into a generic AI/vector memory store without governed organizational semantics.

**Explicit product-owned / commodity boundary:** product-domain knowledge, product-specific promotion rules, prompts, agents, ontologies and business workflows remain product-owned. Vector databases, lexical search engines, embedding models, LLM/RAG frameworks and model providers are replaceable implementation technology.

---

### CAP-003 — Search / Index Projection

**Lifecycle:** `Candidate`

**Proposed organizational outcome:** make governed organizational records and assets discoverable across shared platform responsibilities while preserving exact source attribution and ensuring discovery state never becomes a second source of truth or an authority source.

**Accountable architectural owner:** `ООО «Арвектум»` — platform architecture owner.

**Sponsor / constitutional rationale:** Constitution Article XVI requires governed organizational assets to be discoverable. RFC-0001 permits mutable projections, caches and indexes but prohibits them from becoming independent authorities. RFC-0007 and RFC-0008 likewise classify semantic search, embeddings, OCR/extraction indexes, summaries and derived retrieval representations as non-canonical by default.

**Domain-neutral boundary:**

- non-authoritative projection of governed source identities and exact versions;
- explicit stale/missing/ambiguous source state;
- source-resolution before consequential reliance;
- rebuild/replay from governed source state within the declared scope;
- Organization/authorization/purpose/classification/rights filters where relevant;
- search/index technology independence.

The capability does not own canonical records, authority, approvals, product ranking semantics or domain search taxonomies.

**Expected consumers / strategic need:** P3.05 provides the first bounded slice. P3.03/P3.04 and later product consumers may require discovery across governed Documents, Memory and Knowledge without direct internal-store coupling. P3.09 must prove multi-consumer value before promotion beyond Candidate/Incubating status.

**Reuse hypothesis:** a shared non-authoritative projection contract can support discovery across multiple governed source types while every consequential consumer resolves back to the authoritative source/version.

**Review date:** `2026-09-08`, or earlier at P3.11.

**Incubation criteria:**

- P3.02 records a bounded Provisional capability contract and owner;
- exact source/version attribution and non-authority are executable;
- rebuildability and stale/missing-state behavior are explicit;
- RFC-0003 access/rights constraints are enforced at relevant retrieval boundaries;
- technology choice remains replaceable unless separately governed by ADR;
- at least one bounded consumer need is identified without creating a public API promise.

**Containment criteria:** keep product-specific ranking, saved-search UX, domain query semantics, recommendation logic and domain taxonomies product-owned; keep the concrete search/vector/index engine as commodity infrastructure.

**Rejection criteria:** reject centralized platform responsibility if search semantics are predominantly product-specific, if a projection cannot remain reconstructable/non-authoritative, or if the only commonality is a shared vendor/search engine with no stable organizational semantics.

**Explicit product-owned / commodity boundary:** product ranking/relevance policy, domain filters/taxonomies, search UX and recommendations remain product-owned. Elasticsearch/OpenSearch/vector engines/database indexes/caches or equivalent technology are infrastructure, not the capability identity.

---

### CAP-004 — Audit / Reconstruction Support

**Lifecycle:** `Candidate`

**Proposed organizational outcome:** provide reusable, read-oriented reconstruction of consequential operations from governed evidence so operators/reviewers can explain what happened, which exact versions were relied upon and where evidence is missing, redacted or unavailable.

**Accountable architectural owner:** `ООО «Арвектум»` — platform architecture owner.

**Sponsor / constitutional rationale:** Constitution Articles XI and XII require observable meaningful actions and explainability of significant system output. RFC-0006 defines Event/provenance/observability semantics and explicitly keeps telemetry/projections non-canonical by default; RFC-0005 defines Governed Execution context and consequential-operation evidence.

**Domain-neutral boundary:**

- reconstruction over existing governed execution, Event, provenance, authority, Product Contract, workflow/input and output/version evidence;
- clear distinction between canonical evidence and derived reconstruction views;
- explicit unavailable/redacted/deleted/incomplete evidence semantics;
- read-oriented views cannot mutate canonical state or mint authority;
- observability/storage tooling remains replaceable.

The capability does not create a second audit authority, product-specific compliance interpretation or a universal logging taxonomy.

**Expected consumers / strategic need:** P3.06 provides the first bounded operator/reviewer scenario. P3.08/P3.09 must demonstrate governed reuse by materially distinct bounded consumers/workflows. Strategic need is cross-cutting because reconstructability and explainability apply to consequential operations across products.

**Reuse hypothesis:** multiple workflows can reuse the same evidence-resolution and reconstruction semantics while products retain their own domain-specific review screens, compliance interpretations and business narratives.

**Review date:** `2026-09-08`, or earlier at P3.11.

**Incubation criteria:**

- P3.02 records a bounded Provisional capability contract and owner;
- reconstruction is defined as derived/read-oriented and preserves exact version/source attribution;
- unavailable/deleted/redacted evidence is represented honestly;
- RFC-0003 access/minimization/retention rules are preserved;
- no SIEM/log store/dashboard becomes organizational authority;
- no public audit/SLA/compliance guarantee is implied.

**Containment criteria:** keep product-specific audit narratives, compliance mappings, reviewer UX, business-domain event interpretation and reports product-owned; keep SIEM/log/trace/metrics/dashboard technology as replaceable infrastructure.

**Rejection criteria:** reject centralized platform responsibility if reconstruction needs are unique to one product, if the proposed view requires product-domain semantics to be correct, or if the candidate degenerates into generic logging/observability infrastructure without governed evidence semantics.

**Explicit product-owned / commodity boundary:** product compliance/reporting logic and domain-specific review UX remain product-owned. Logging, tracing, SIEM, dashboard and analytical storage technologies remain commodity/operational infrastructure unless separately justified.

## 5. Explicitly not admitted in P3.01

The following items are **not** Platform Capability candidates in this catalog. This is a bounded Phase 3 admission decision, not a claim that they can never be reconsidered.

| Item | P3.01 disposition | Reason / boundary |
|---|---|---|
| Generic notification service | `Deferred / not admitted` | No validated cross-product organizational-semantic need. Treat as product-local or commodity integration until evidence exists. |
| Generic scheduler | `Deferred / not admitted` | Scheduling technology is not by itself a Platform Capability; Governed Workflow semantics remain RFC-0005 scope. |
| Generic connector marketplace / broad adaptor framework | `Deferred / not admitted` | Revisit at P3.09 only if real multi-consumer integration evidence justifies shared semantics. |
| Public SDK/API | `Deferred / not admitted` | Stable external developer surface is a later contract/extension concern and would create compatibility obligations prematurely. |
| Production IAM / policy engine | `Deferred as concrete implementation choice` | RFC-0003 security/authority semantics are mandatory and P3.07 must exercise them, but a specific IAM/PDP/PEP product/topology is infrastructure and requires a fresh ADR-gate assessment when materially relied upon. |
| Fixed database/object store/search engine/broker/service topology | `Not a capability candidate` | Commodity/durable infrastructure selection remains replaceable and subordinate to ADR when a material threshold is crossed. |
| Product-domain workflows, schemas, prompts, taxonomies, templates, ontologies, scoring and business rules | `Product-owned` | Constitution/RFC-0004 require domain expertise to remain in products unless separately promoted through evidence-based admission. |
| Customer-facing SLA/support/HA/archival/compliance commitments | `Not a capability candidate` | Operational/commercial commitments require separate readiness and decision authority; they cannot be created by a catalog entry. |

## 6. Cross-candidate invariants

Every retained Candidate is constrained by the following boundary rules:

1. `Candidate` is a lifecycle state, not a delivery promise, roadmap guarantee or production claim.
2. No candidate becomes `Incubating` until P3.02 records the minimum RFC-0001 incubation envelope and Provisional capability contract.
3. No candidate becomes `Active` without separate RFC-0001 admission, operational-readiness evidence and applicable decision-authority approval.
4. Product-specific domain semantics remain product-owned unless separately promoted through accepted admission rules.
5. Product reliance on shared platform state/history/capabilities must use the applicable RFC-0004 Product Contract boundary.
6. Authorization does not create Organizational Authority; Product Contract possession does not grant permission.
7. Search/index, retrieval representations and reconstruction views remain derived/non-authoritative unless an Accepted decision explicitly establishes a different governed role.
8. Concrete persistence, transaction, Event delivery, IAM enforcement, evidence-integrity, stable API/serialization, durable projection or service-topology choices re-open the ADR gate before material reliance.
9. Cross-Organization access/reuse is denied by default and requires explicit rights, purpose, classification and governance.
10. AI may assist execution and analysis but cannot silently promote Knowledge, mutate canonical authority, broaden rights/retention or approve lifecycle transitions.

## 7. Review and change rule

This catalog may be updated by subordinate governance as Candidate evidence changes, provided the update does not amend Constitution or an Accepted RFC.

Any entry transition to `Incubating`, `Active`, `Deprecated` or `Retired` must be supported by the applicable RFC-0001 lifecycle evidence and canonical decision record proportionate to impact.

The next work item is `P3.02 — Capability lifecycle, ownership and Provisional contract baseline`.
