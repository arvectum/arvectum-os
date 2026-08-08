# Phase 3 Provisional Platform Capability Contracts

Status: `Active`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Lifecycle authority: RFC-0001 `1.0.0` — `Accepted`
Product-boundary authority: RFC-0004 `1.0.0` — `Accepted`
Created by work item: `P3.02 — Capability lifecycle, ownership and Provisional contract baseline`

## 1. Purpose and scope

This document establishes the minimum governed incubation envelope and Provisional domain-neutral capability-contract baseline for the four Phase 3 Platform Capability candidates admitted by P3.01.

It is a subordinate architecture artifact. It does not amend an Accepted RFC, create a Stable Product Contract, create a stable public API/SDK, select durable infrastructure, authorize production use, establish operational readiness, create SLA/support commitments or promote any capability to `Active`.

The lifecycle transition recorded here is bounded to Phase 3 validation:

- `CAP-001 — Document & Artifact Governance`: `Candidate → Incubating`;
- `CAP-002 — Memory & Knowledge Governance`: `Candidate → Incubating`;
- `CAP-003 — Search / Index Projection`: `Candidate → Incubating`;
- `CAP-004 — Audit / Reconstruction Support`: `Candidate → Incubating`.

The transition is justified only for the bounded P3.03–P3.09 validation envelope. Incubation remains reversible and does not imply supported public compatibility or production readiness.

## 2. Shared incubation rules

All four Incubating capabilities use these common constraints:

1. accountable architectural owner: `ООО «Арвектум»` — platform architecture owner;
2. sponsoring consumers: the bounded Phase 3 capability slices and later P3.08/P3.09 bounded consumers; these are validation sponsors, not production customers or commercial commitments;
3. budget boundary: only the implementation/evidence necessary for P3.03–P3.09 and P3.10 fitness evidence; no durable infrastructure, public SDK/API, HA/SLA or generalized service catalog is authorized;
4. capability contracts are `Provisional`, domain-neutral and may change during incubation while preserving security, authority, migration and evidence integrity;
5. concrete persistence, object-store, search, Event delivery, IAM, evidence-integrity, stable serialization/API or deployable service topology remains outside the contract identity and re-opens the ADR gate before material reliance;
6. product-domain schemas, workflows, taxonomies, prompts, scoring, business rules, review narratives and UX remain product-owned;
7. no contract declaration grants authorization or Organizational Authority;
8. cross-Organization access/reuse is denied by default;
9. all consequential reliance resolves to exact governed source/version state rather than derived projections alone;
10. review occurs at P3.11 or no later than `2026-09-08`.

## 3. Contract lifecycle semantics

These are Platform Capability contracts, not RFC-0004 Product Contracts. `Provisional` here describes the unstable incubation contract surface required by RFC-0001 for an `Incubating` capability.

A real Product or Product Experiment consuming these capabilities must separately declare an RFC-0004 Product Contract before governed reliance. During Phase 3 that Product Contract is expected to be `Provisional` unless separately stabilized through the RFC-0004 lifecycle.

No consumer may infer `Active` capability status from a Product Contract or from implementation availability.

## 4. CAP-001 — Document & Artifact Governance

**Lifecycle:** `Incubating`

**Contract status:** `Provisional`

**Source organizational need:** RFC-0008 defines domain-neutral Document/Artifact architecture and P3.01 established a bounded need to test reusable identity, immutable-version, admission, derivation and exact-version reliance semantics above Core Runtime.

**Sponsoring consumers:** P3.03 bounded Document/Artifact slice; P3.08 bounded product-style consumer; P3.09 second materially distinct reuse consumer/workflow.

**Bounded scope / budget:** implement only logical Document identity, immutable Document Version identity, governed admission/checkpoint, Artifact/content identity or manifest where applicable, derivation provenance, exact-version reliance, handling-constraint propagation and transient-versus-governed-state distinction. Excludes DMS breadth, OCR/rendering/signing productization and durable object-store choice.

**Provisional operations:**

- identify or resolve a governed Document subject/version;
- admit a Document Version for governed reliance under applicable validation/authority rules;
- register/resolve Artifact or content identity associated with a governed version;
- record derivation/source relationships and provenance;
- resolve exact relied-upon Document/Artifact version and handling constraints.

Operation names and wire formats are not stable public interfaces.

**Canonical Record / authority responsibilities:** Document subjects and admitted immutable versions use RFC-0002/RFC-0008 canonical semantics. Authority mode and authoritative source must be explicit. Storage location, blob/object identity and transient generated content do not become authority merely by existing. External documents remain `External Reference` or `Governed Replica` where the external source is authoritative.

**Dependencies / events:** depends on Core Runtime Canonical Record, Relationship, Governed Execution and Event/provenance semantics; may emit bounded admission, derivation and reliance evidence Events required for reconstruction. Event taxonomy and transport are not stabilized here.

**Security / authority / data handling:** Organization scope, least privilege, classification, rights, purpose, retention/deletion and derivation constraint propagation apply. Admission or technical write capability does not grant Organizational Authority. Derivation must not silently declassify or broaden permitted reuse.

**Portability / compatibility / migration:** governed export must preserve subject/version identity, authority/source references, derivation/provenance and lawful Artifact content or references within scope. Storage technology must be replaceable. Provisional contract changes may require bounded adapters or test-fixture migration; no stable compatibility promise exists.

**Exit criteria:**

- promote toward stronger platform responsibility only if P3.03/P3.08/P3.09 demonstrate domain-neutral multi-consumer value and P3.11 confirms the abstraction;
- return domain-specific semantics to products whenever correctness depends on product meaning;
- replace implementation technology without changing organizational semantics;
- retire incubation if evidence shows only commodity file/storage commonality or single-product value.

## 5. CAP-002 — Memory & Knowledge Governance

**Lifecycle:** `Incubating`

**Contract status:** `Provisional`

**Source organizational need:** Constitution and RFC-0007 require governed organizational Memory/Knowledge semantics; P3.01 identified a bounded need to test reusable retrieval, candidate/promotion and exact-version reliance without turning AI/vector storage into authority.

**Sponsoring consumers:** P3.04 bounded Memory/Knowledge slice; P3.08 bounded product-style consumer; P3.09 second materially distinct reuse consumer/workflow.

**Bounded scope / budget:** implement only lifecycle distinction among Observation, Organizational Memory, Knowledge Candidate and validated Knowledge; governed retrieval constraints; candidate/promotion path; exact effective Knowledge Version attribution; validation/approval separation; derived retrieval non-authority. Excludes product ontologies, prompts, agents, domain validation/scoring and durable vector/model/persistence selection.

**Provisional operations:**

- record/resolve bounded Memory or Knowledge subjects/versions under declared lifecycle semantics;
- retrieve eligible governed Memory/Knowledge under scope, rights, purpose, classification and freshness constraints;
- create a Knowledge Candidate from attributable source evidence;
- request/record validation or promotion through applicable Governed Execution/authority boundaries;
- resolve exact effective Knowledge Version used by a consequential execution.

Operation names and retrieval representation formats are not stable public interfaces.

**Canonical Record / authority responsibilities:** validated Knowledge and governed Memory use applicable Canonical Record semantics. Observation, candidate state, embeddings, summaries, chunks, rankings and retrieval projections are not automatically validated Knowledge or authority. Exact source/effective versions remain attributable.

**Dependencies / events:** depends on Core Runtime, RFC-0006 provenance and RFC-0007 lifecycle semantics; may emit bounded candidate, validation, promotion, retrieval-reliance and supersession evidence Events. Model/vector/search implementation remains replaceable.

**Security / authority / data handling:** Organization scope, deny-by-default authorization, purpose limitation, classification, rights, minimization, retention/deletion and cross-Organization restrictions apply. AI may propose or retrieve but cannot silently validate, approve, promote, expand retention or broaden reuse.

**Portability / compatibility / migration:** export/migration must preserve governed identities/versions, lifecycle/validation state, provenance, rights/classification references and lawful content or references. Derived indexes may be rebuilt. Provisional contract evolution must preserve historical interpretability of consequential reliance.

**Exit criteria:**

- continue platform incubation only with evidence of reusable lifecycle/retrieval semantics across materially distinct consumers;
- keep domain truth, validation rules, prompts, ontologies and business learning loops product-owned;
- replace commodity AI/vector/search technology freely behind the contract;
- retire/return if the shared abstraction collapses into generic model/vector memory or remains single-product.

## 6. CAP-003 — Search / Index Projection

**Lifecycle:** `Incubating`

**Contract status:** `Provisional`

**Source organizational need:** governed organizational assets must be discoverable, while RFC-0001/RFC-0007/RFC-0008 require projections/indexes to remain derived and non-authoritative. P3.01 admitted a bounded discovery responsibility for validation.

**Sponsoring consumers:** P3.05 bounded search/index slice; P3.03/P3.04 governed sources; P3.08/P3.09 bounded consumers demonstrating discovery without internal-store coupling.

**Bounded scope / budget:** implement only non-authoritative projection of governed source identities/exact versions, stale/missing/ambiguous state, governed source resolution before consequential reliance, rebuild/replay and relevant access/rights filtering. Excludes product ranking/recommendation semantics, saved-search UX and durable search-engine choice.

**Provisional operations:**

- project an eligible governed source identity/version into a derived discovery representation;
- query bounded discovery state under applicable Organization/security constraints;
- return exact source/version attribution plus freshness/staleness status;
- resolve a result back to governed source state before consequential reliance;
- rebuild/replay the bounded projection from governed sources.

Query language, ranking algorithm and wire format are not stable public interfaces.

**Canonical Record / authority responsibilities:** projection entries are derived/non-authoritative. They cannot mint Canonical Records, approve mutations, grant authority or become the relied-upon source for consequential truth. Canonical source identity/version remains the authority reference.

**Dependencies / events:** depends on governed source records/versions and relevant provenance/change Events; may consume source-change evidence and emit bounded projection/rebuild diagnostic evidence. Event transport/index topology is not fixed.

**Security / authority / data handling:** search must not bypass Organization, authorization, purpose, classification, rights or retention constraints. Missing enforcement context fails closed for protected discovery. Result visibility does not grant access to the underlying governed object or Organizational Authority.

**Portability / compatibility / migration:** projection is rebuildable from governed sources within declared scope. Search/index vendor data is disposable derived state unless separately governed. Contract evolution must preserve source attribution and non-authority; no stable ranking compatibility promise exists.

**Exit criteria:**

- retain/incubate further only if shared discovery semantics serve materially distinct governed sources/consumers;
- return product ranking/query semantics and UX to products;
- replace index/search technology without authority migration;
- retire centralized responsibility if commonality is only a shared vendor engine or source-resolution semantics cannot remain trustworthy.

## 7. CAP-004 — Audit / Reconstruction Support

**Lifecycle:** `Incubating`

**Contract status:** `Provisional`

**Source organizational need:** Constitution explainability/observability requirements and RFC-0005/RFC-0006 evidence semantics create a cross-cutting need to reconstruct consequential operations without treating telemetry or derived views as authority.

**Sponsoring consumers:** P3.06 bounded operator/reviewer scenario; P3.08 bounded product-style consumer; P3.09 second materially distinct reconstruction consumer/workflow.

**Bounded scope / budget:** implement only read-oriented resolution/reconstruction of execution, actor/authority, Product Contract, workflow/material inputs, Event causation/correlation and output versions; explicit missing/redacted/deleted/unavailable evidence; canonical-versus-derived distinction. Excludes product compliance narratives, universal logging taxonomy, SIEM/dashboard productization and durable observability topology.

**Provisional operations:**

- reconstruct a bounded consequential execution from governed evidence;
- resolve exact actor/authority, contract/workflow/input/output/event version references where retained;
- expose evidence completeness/unavailability/redaction/deletion status;
- distinguish canonical evidence from derived reconstruction views;
- export a bounded reconstruction package/reference set where permitted.

View schema, UI and transport are not stable public interfaces.

**Canonical Record / authority responsibilities:** reconstruction views are derived/read-oriented. RFC-0005/RFC-0006 governed execution/event/evidence records remain authoritative within their declared scopes. A view cannot mutate canonical state, fill missing evidence by invention or mint Organizational Authority.

**Dependencies / events:** depends on Core Runtime Governed Execution, Product Contract references, Canonical Records/Relationships and RFC-0006 Event/provenance evidence. It primarily consumes evidence; any diagnostic/view-generation Events remain secondary and must not replace source evidence.

**Security / authority / data handling:** access follows Organization, authorization, classification, minimization, purpose, retention/deletion and redaction rules. Reconstruction must not expose unavailable/restricted evidence through derived summaries. Reviewer access does not imply approval authority.

**Portability / compatibility / migration:** reconstruction must rely on portable governed identities/versions and explicit evidence references rather than a proprietary SIEM representation. Derived views may be regenerated when source evidence remains lawfully retained. Provisional schemas may evolve without a public compatibility promise.

**Exit criteria:**

- retain/incubate further only if materially distinct workflows reuse the evidence-resolution semantics;
- keep product compliance interpretation, reports and UX product-owned;
- replace logging/SIEM/trace/dashboard technology without changing governed evidence meaning;
- retire/return if correct reconstruction inherently requires one product's domain semantics or the shared layer degenerates into generic observability tooling.

## 8. Product Contract consumption baseline

P3.02 does not create a Product Contract for a real product. It establishes the minimum capability-side declarations needed so P3.08 can create a bounded RFC-0004 `Provisional` Product Contract without depending on platform internals.

A P3.08 consumer contract must, proportionate to its actual interaction, identify:

- product/experiment identity and owner;
- exact Incubating capability dependencies and Provisional contract versions;
- operations used and failure behavior;
- domain types crossing the boundary while preserving product ownership;
- Canonical Record authority/read-write responsibilities;
- shared Events/artifacts versus product-local telemetry/transient output;
- Organization/security/authority/data-handling constraints;
- portability/export and migration/exit behavior;
- explicit acknowledgement that capability dependencies are Incubating and unsupported as stable public contracts.

Direct table/store/index access, internal imports, private event streams and undocumented conventions remain prohibited boundary mechanisms.

## 9. ADR gate assessment

P3.02 selects no concrete durable implementation mechanism and therefore does not itself cross the ADR threshold.

The ADR gate must be re-opened before material reliance on concrete persistence/object-store/search topology, transaction/concurrency mechanism, Event transport/store, IAM/PDP/PEP technology, evidence-integrity mechanism, stable API/serialization, durable projection/replay store or separately deployable service/process topology.

## 10. Lifecycle review and authority

The four Candidate-to-Incubating transitions are bounded shared-platform lifecycle decisions. Because the Decision Authority Policy remains `Proposed`, residual decision authority remains with the owner of Arvectum OS under Accepted RFC-0001.

This P3.02 artifact records the architecture disposition required to proceed with bounded incubation work; it does not fabricate a separate historical approval or imply delegated authority that has not been canonically approved.

At P3.11, each capability must be dispositioned independently: remain Incubating, return/contain, replace, retire, or separately qualify for an `Active` admission decision. `Active` requires RFC-0001 admission and approved operational-readiness evidence and is not an automatic M3 outcome.

## 11. P3.02 exit statement

The minimum governed incubation envelope now exists for CAP-001 through CAP-004:

- lifecycle state is explicit;
- accountable ownership is explicit;
- source need and sponsoring validation consumers are explicit;
- scope/budget is bounded;
- Provisional domain-neutral capability contracts are declared;
- canonical authority responsibilities, dependencies/events, security/data handling, portability/migration and exit criteria are explicit;
- Product Contract consumption remains a separate RFC-0004 boundary;
- no stable public interface, durable infrastructure, production readiness or `Active` status is implied.

P3.03–P3.06 may therefore begin as bounded Incubating capability slices, subject to R5 and the continuing P3.10 fitness/ADR gates.
