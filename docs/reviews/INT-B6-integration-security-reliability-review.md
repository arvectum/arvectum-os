# INT-B6 — Integration Security / Reliability Review

Status: `Complete`
Version: `1.0.0`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract` consequences
Roadmap lane: `Lane B — Russian-market integrations`
Reviewed artifacts:
- [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](../architecture/INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0`;
- [`INT-B3 — 1С First-Candidate Design`](../architecture/INT-B3-1c-erp-first-candidate-design.md) `1.0.0`;
- [`INT-B4 — CRM Designs`](../architecture/INT-B4-crm-designs.md) `1.0.0`;
- [`INT-B5 — СЭД/ECM/ЭДО Design`](../architecture/INT-B5-sed-ecm-edo-design.md) `1.0.0`.
Iterations: `4 of maximum 7`
Result: `PASS for bounded read-only pilot admission after reconciliation`

## 1. Purpose

INT-B6 is the mandatory cross-portfolio security/reliability gate before the first material real connector implementation.

It determines whether the integration architecture defined by INT-B2 through INT-B5 is safe enough to proceed from design into a **bounded, read-only, explicitly scoped pilot admission package**.

This review does **not**:

- certify any real customer or ООО «Арвектум» external-system deployment;
- approve a Production environment;
- approve customer-facing support, SLA, compatibility or certification commitments;
- make any connector a Platform Capability, let alone an `Active` capability;
- create or stabilize a Product Contract;
- authorize any external business write, posting, workflow transition, signing, sending, payment or organizational commitment;
- approve a generic shared connector runtime, broker, secrets manager, event-ingress topology or public SDK/API;
- establish legal validity of an electronic signature or document;
- substitute for deployment-specific threat modeling, credentials review, operational tests or owner approval where those are required.

## 2. Canonical basis

INT-B6 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` as indexed by the canonical RFC Index;
- RFC-0001 external-system authority, Canonical Record, security, portability and consequential-change principles;
- RFC-0003 Identity / Authentication / Authorization / Organizational Authority / Data Governance separation, deny-by-default, least privilege, Organization isolation, secret handling, revocation and portability;
- RFC-0004 Product Contract boundary and hidden-coupling prohibition;
- RFC-0005 Governed Execution, effect classification, idempotency, retry, uncertainty, reconciliation and external-effect rules;
- RFC-0006 source occurrence versus canonical Event admission, duplicate/gap/replay semantics and evidence requirements;
- RFC-0008 Document/Artifact identity, content, signature/seal evidence, retention, derivative-artifact and external-authority boundaries;
- canonical roadmap `2.93.0` at task start.

No higher-authority conflict was found after the reconciliations recorded in this review.

## 3. Portfolio under review

The reviewed concrete profiles are:

| Candidate | Initial profile | Initial effect scope | External authority |
|---|---|---|---|
| 1С | `1С:ERP Управление предприятием 2`, family 2.5, self-hosted/client-server, published OData | read-only procurement projection | 1С |
| Битрикс24 | one concrete portal/account binding | read-only CRM/task projection | Битрикс24 |
| amoCRM | one concrete account/subdomain, API v4/OAuth 2.0 | read-only CRM/task projection; subscription administration separately governed | amoCRM |
| Directum RX | one organization-controlled deployment, Integration Service REST/OData | read-only document/card/version/task/workflow projection | Directum RX |
| Контур.Диадок | one organization box/account, official HTTP API | read-only document/message/docflow/signature evidence and event-feed retrieval | Диадок |

All reviewed candidates begin with `External Reference` as the default Arvectum OS authority mode. No reviewed design admits business-object mutation merely because the external API technically supports it.

## 4. Security / reliability gate model

A candidate may proceed to a real bounded pilot only if all of the following are satisfied for the exact binding:

```text
exact external endpoint/account/deployment
        ↓
Organization binding and authority scope
        ↓
Data purpose / classification / rights
        ↓
dedicated least-privilege credential binding
        ↓
explicit read-only operation allowlist
        ↓
source identity + freshness + completeness semantics
        ↓
duplicate/gap/retry/replay handling
        ↓
failure / stale / unavailable / reconciliation behavior
        ↓
Product Contract where governed platform reliance begins
        ↓
implementation-specific ADR only if a shared constraining choice is introduced
        ↓
real bounded pilot evidence
```

Failure at any required gate means **no governed reliance**. A connector must fail closed or expose an explicit unavailable/stale/incomplete state rather than silently broadening access or pretending current authoritative state.

## 5. Iteration 1 — Organization isolation, authority and identity

### Findings

1. A technically valid endpoint credential could be accidentally reused across Organizations or environments.
2. External identifiers could be mistaken for Arvectum Subject Identities or used to merge entities across systems without evidence.
3. Local projections could become competing sources of truth if users can edit them independently.
4. A connector may technically expose more source data than the bounded organizational outcome requires.
5. A portal/account/box identity alone does not prove that every exposed object belongs in the same Arvectum Organization scope.

### Reconciliation and gate requirements

The portfolio passes this dimension subject to the following mandatory controls:

- one `External Endpoint Binding` resolves to exactly one governing Arvectum Organization for the admitted scope;
- credentials are bound to the same Organization and endpoint; no ambient credential reuse across Organizations or production/test endpoints;
- vendor IDs remain external aliases/references in their vendor + endpoint namespace;
- cross-system identity equivalence requires separate governed evidence and must not be inferred from name, INN, email, filename or similar convenience fields alone;
- external systems remain authoritative for the declared source facts;
- Workspace projections/caches are non-authoritative and must not expose a competing editable authority;
- each operation is allowlisted to the bounded business outcome rather than granting all technically available API data;
- exact external account/portal/box/configuration and authoritative object scope are discovered before activation.

Result: material objections closed for bounded read-only pilot admission.

## 6. Iteration 2 — authentication, authorization, secrets and private keys

### Findings

1. Integration credentials can be technically broad even when the connector operation contract is read-only.
2. API scopes, source-system user permissions or administrator status can be confused with Arvectum Organizational Authority.
3. OAuth refresh tokens, webhook secrets, 1С credentials and similar material could leak through logs, Canonical Records, prompts, exports or repository configuration.
4. Credential rotation/revocation can break retrieval while leaving Workspace projections apparently current.
5. Диадок signing paths introduce a separate private-key boundary that must not be smuggled into the connector runtime through “future convenience”.

### Reconciliation and gate requirements

Before a real binding is activated:

- a dedicated integration principal/integration registration is used where the external system supports it;
- source-side permissions are the minimum required for the exact admitted operations and object scope;
- authentication success and vendor API permission remain distinct from Arvectum authorization, Organizational Authority and Data Governance;
- reusable secrets are stored only through an approved runtime secret mechanism and referenced indirectly from governed state;
- secrets/private keys/passwords/access or refresh tokens MUST NOT appear in Canonical Record payloads, Events, prompts, normal logs, repository files or portability packages merely for convenience;
- credential metadata records owner, endpoint, allowed scope, rotation/revocation and expiry/freshness where relevant without storing the secret itself;
- credential failure or revocation immediately changes connector health to unavailable/degraded and cannot silently fall back to a broader administrator credential;
- historical attribution is preserved after credential rotation/revocation;
- no signing private key is admitted into the current integration architecture; any future signing path requires a separate design, authority model, cryptographic boundary and review.

Result: material objections closed for bounded read-only pilot admission.

## 7. Iteration 3 — reliability, completeness, duplicates and replay

### Findings

1. Read-only integrations can still produce materially wrong organizational decisions if stale or partial data is presented as complete/current.
2. Pagination interruption, source rate limiting, network timeout or schema drift can create silent gaps.
3. Webhook/event-feed delivery can be duplicated, delayed, reordered or lost.
4. Polling and event-feed reprocessing can create duplicate local records if external identity is not deterministic.
5. Future write/effect code could accidentally retry an uncertain request or replay a historical Event and duplicate an external effect.

### Reconciliation and gate requirements

Every real pilot binding MUST expose, as applicable:

- `retrieved_at` / last successful source contact;
- declared snapshot/query/filter/window scope;
- pagination or continuation state;
- complete versus incomplete state;
- stale/unavailable status;
- connector/adapter version and relevant external schema/API compatibility evidence;
- deterministic external identity namespace;
- reconciliation-required state when metadata/schema mapping, cursor continuity or source result is uncertain.

Additional rules:

- partial retrieval MUST NOT be represented as a complete authoritative population;
- timeout/reset/missing response is not equivalent to “source has no data”;
- webhook, event-feed and callback items are source occurrences before RFC-0006 canonical Event admission;
- duplicate transport occurrence must not create duplicate semantic subjects or canonical Events by implication;
- event-feed cursor/index/checkpoint state must support gap detection where relied upon;
- when a webhook/feed gap can be reconciled against an authoritative read API, reconciliation is preferred before consequential reliance;
- telemetry is non-canonical by default;
- historical replay is side-effect safe; no future external mutation may be repeated without a new authorized Governed Execution;
- future non-read-only operations remain blocked until operation-specific idempotency, uncertain-outcome, compensation/reversal and reconciliation semantics are separately approved.

Result: material objections closed for bounded read-only pilot admission.

## 8. Iteration 4 — data governance, documents, failure, termination and implementation boundary

### Findings

1. A “read-only” connector can still over-collect personal, commercial or document content.
2. Full document bytes may be retrieved where metadata/reference is sufficient.
3. OCR, summaries, previews or embeddings can silently multiply retained sensitive data.
4. Signature/certificate evidence can be misread as proof of Organizational Authority or legal validity.
5. Connector disable/rollback/termination can be misunderstood as deleting external business state or reversing already committed external effects.
6. A successful first adapter could prematurely force a common runtime, secrets manager, broker, event ingress or generic schema across all products.
7. A Product Contract might be skipped because the first pilot appears “read-only”.

### Reconciliation and gate requirements

- collection is purpose-limited and minimized to the exact pilot outcome;
- classification, allowed purpose, retention/deletion and portability obligations are declared before governed reliance;
- document metadata/reference retrieval is preferred over content retrieval when content is not needed;
- when bytes/content are retrieved, exact source version/provenance is preserved and derived artifacts inherit applicable handling constraints unless a governed transformation establishes otherwise;
- OCR, extraction, summary, preview, embedding and search projections remain non-authoritative by default and are not automatically retained as Knowledge/Memory;
- signature/certificate evidence is evidence only and does not establish Organizational Authority, approval, signer entitlement or blanket legal validity;
- disabling a connector stops new retrieval/effects according to its contract but preserves lawful historical attribution;
- rollback means returning Arvectum connector implementation/configuration to a prior compatible version, not undoing external business effects;
- termination revokes credentials/subscriptions, disposes of caches/projections according to retention, preserves required history/evidence and leaves external authoritative state untouched;
- the first implementation MUST NOT introduce a shared connector runtime, queue/broker, secrets-manager mandate, schema registry, webhook ingress or generic DTO/API surface without ADR trigger analysis;
- a Product Contract is mandatory before a product relies on shared Arvectum connector behavior, canonical platform state/history, platform Events or other governed platform capability even when the external operation itself is read-only.

Result: no remaining material objection within the scoped gate.

## 9. Candidate-specific disposition

### 9.1 1С:ERP

Disposition: **eligible as preferred first bounded pilot candidate, subject to exact deployment discovery.**

Why:

- already constrained to read-only procurement projection;
- no external write/effect is admitted;
- bounded pull/reconciliation semantics avoid assuming universal CDC;
- external authority remains 1С;
- source metadata discovery can verify actual deployment shape before reliance.

Pilot blockers that remain deployment-specific:

- exact real 1С deployment/configuration/platform version;
- exact published OData/API surface;
- dedicated read-only source identity and credentials;
- exact procurement entities/fields and data-purpose scope;
- Product Contract before shared governed reliance;
- real stale/incomplete/schema-drift/failure tests.

### 9.2 Битрикс24

Disposition: **eligible for a later bounded read-only pilot after exact portal discovery.**

Additional caution:

- calls execute in source user context, so source-side user rights are security-significant;
- incoming-webhook/OAuth credentials must be dedicated and least-privilege;
- webhook receipt is not trusted as complete authoritative state without reconciliation semantics.

### 9.3 amoCRM

Disposition: **eligible for a later bounded read-only pilot after exact account discovery.**

Additional caution:

- OAuth tokens/scopes are security-sensitive but do not create Organizational Authority;
- webhook subscribe/unsubscribe is an administrative external mutation and remains separately authorized from ordinary reads.

### 9.4 Directum RX

Disposition: **eligible for a later bounded read-only metadata/document projection pilot after exact deployment discovery.**

Additional caution:

- deployment-specific document kinds, routes, permissions and customizations must remain outside domain-neutral platform semantics;
- content retrieval requires stronger classification/retention controls than metadata-only access.

### 9.5 Контур.Диадок

Disposition: **eligible for a later bounded read-only evidence pilot after exact box/account discovery.**

Additional caution:

- signing/sending/annulment and similar actions remain prohibited;
- private keys remain outside the connector scope;
- event feed is source occurrence evidence and requires cursor/gap/reconciliation handling;
- document/signature evidence must not be converted into Arvectum legal conclusions by implication.

## 10. Minimum operational evidence before first real pilot activation

The first real pilot admission package MUST contain evidence for the exact endpoint:

1. **Endpoint identity evidence** — system, environment, account/portal/box/deployment and owner.
2. **Organization mapping** — exactly which Arvectum Organization owns the binding.
3. **Authority declaration** — external source and object scope; initial mode `External Reference` unless separately justified otherwise.
4. **Outcome statement** — one bounded organizational outcome.
5. **Operation allowlist** — exact connector operation IDs and effect classes.
6. **Credential evidence** — dedicated principal/integration, source-side least privilege, secret reference, rotation/revocation procedure.
7. **Data Governance** — purpose, data classes, minimization, content/field scope, retention/deletion and portability constraints.
8. **Compatibility evidence** — exact external API/configuration version/metadata assumptions used by the adapter.
9. **Freshness/completeness evidence** — pagination/window/cursor semantics and stale/unavailable representation.
10. **Failure tests** — authentication failure, authorization denial, network timeout, source unavailability, partial pagination/cursor gap, schema incompatibility and credential revocation.
11. **Reconciliation tests** — deterministic duplicate handling and repair path after incomplete/uncertain reads.
12. **Event/source-occurrence evidence** — where webhooks/feeds are used, prove deduplication, gap handling and Event-admission boundary.
13. **Termination test** — prove disable/revoke/unsubscribe/cache disposal while preserving required history and leaving external authority untouched.
14. **Product Contract** — required before governed product/shared-platform reliance under RFC-0004.
15. **ADR disposition** — explicit statement that no new materially shared runtime/topology is introduced, or an applicable ADR exists before such a constraint is adopted.

Passing INT-B6 without this endpoint-specific evidence does not itself activate a connector.

## 11. Write/effect admission remains closed

INT-B6 does not open a generic write path.

The following categories remain **not admitted** until a later separately reviewed operation-specific design:

- 1С create/update/post/unpost/cancel/receipt/payment operations;
- CRM create/update/delete/stage transitions/task completion/business automation mutation;
- Directum document mutation, version upload, task completion, approval, registration or workflow transition;
- Диадок signing, sending, draft sending, approval/rejection, annulment, deletion, counterparty or settings mutation;
- any payment, signature or legally/financially consequential organizational commitment;
- arbitrary/untyped vendor API passthrough.

A future write/effect proposal must include exact operation semantics, authorization, Organizational Authority, Data Governance, idempotency, retry, uncertainty, reconciliation, compensation/reversal, evidence, Product Contract and Governed Execution requirements before implementation.

## 12. ADR disposition

No new ADR is required to close INT-B6 because this review selects no durable shared implementation topology or technology.

An ADR is required before a first implementation makes a materially shared or cross-product constraining choice such as:

- one connector worker/runtime topology;
- one mandatory secrets-manager technology;
- one shared queue/broker/outbox/inbox/CDC mechanism;
- one shared webhook/event-feed ingress architecture;
- one shared schema registry or generic business-object DTO model;
- one public/stable connector API/SDK;
- one cross-product deployment/isolation model;
- one signing/private-key runtime.

A vendor-specific adapter implementation may remain bounded and reversible without an ADR when it does not establish such a shared constraint and satisfies the applicable Product Contract/governance requirements.

## 13. Higher-authority compatibility

- **Constitution 1.2.0:** PASS — organizational control, domain neutrality, external authority, security/privacy/isolation, proportionality and technology independence preserved.
- **RFC-0001:** PASS — external systems remain authoritative; no competing source of truth or speculative capability promotion is introduced.
- **RFC-0002:** PASS — external identifiers remain aliases/references; no physical schema is mandated.
- **RFC-0003:** PASS — identity/authentication/authorization/Organizational Authority/Data Governance remain distinct; deny-by-default, least privilege, isolation, minimization, secret handling, revocation and portability requirements are preserved.
- **RFC-0004:** PASS — Product Contract remains mandatory before governed platform reliance; hidden coupling is prohibited.
- **RFC-0005:** PASS — current business operations are read-only; external writes/effects remain closed; future effects require Governed Execution, idempotency/uncertainty/reconciliation semantics and authority gates.
- **RFC-0006:** PASS — transport/source occurrences remain distinct from canonical Events; duplicate/gap/replay semantics are explicit and replay is side-effect safe.
- **RFC-0007:** PASS — retrieved/derived integration outputs do not automatically become validated Knowledge/Memory.
- **RFC-0008:** PASS — document identity/content/signature evidence and derivative-artifact boundaries are preserved.

No Accepted ADR conflict was found.

## 14. Final gate result

**PASS for bounded read-only pilot admission after reconciliation — 4 of maximum 7 review iterations.**

This PASS means:

- the INT-B2–INT-B5 architecture is sufficiently bounded to prepare one real read-only connector pilot;
- `1С:ERP` remains the preferred first pilot candidate because INT-B1 ranked it first and INT-B3 already defines the narrowest concrete outcome;
- endpoint-specific discovery/evidence and Product Contract/governance requirements remain mandatory before governed reliance;
- no external business write/effect is admitted;
- no Production, Active capability, Stable Product Contract, SLA/support or public compatibility claim is created.

## 15. Next integration action

The next integration-lane action is:

> **`INT-B7 — First real connector pilot admission package`**

Default candidate: the INT-B3 `1С:ERP 2.5` read-only procurement projection **if and when an exact real deployment is available**.

INT-B7 must not fabricate a deployment. If no real endpoint is available, Lane B is `Ready / blocked on real endpoint` rather than proceeding with synthetic operational evidence.
