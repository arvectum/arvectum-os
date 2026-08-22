# INT-B5 — Functional Cross-Review

Status: `Complete`
Reviewed artifact: [`INT-B5 — СЭД/ECM/ЭДО Design`](../architecture/INT-B5-sed-ecm-edo-design.md) `1.0.0`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Iterations: `4 of maximum 7`
Result: `PASS after bounded reconciliation`

## 1. Review scope

The review tested INT-B5 against Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008, INT-B1 through INT-B4 and the canonical roadmap.

Focus:

- concrete named SED/ECM and EDO profiles;
- separation of internal document-management authority from legally significant exchange/signature evidence;
- RFC-0008 document/version/content/rendition/signature boundaries;
- external identity handling;
- least privilege and credential/secret handling;
- read-first operation scope;
- event-feed/source-occurrence semantics;
- freshness, pagination, gap and reconciliation behavior;
- retention/content minimization/derived artifacts;
- signature/private-key/Organizational Authority boundary;
- Product Contract gates;
- termination/portability;
- ADR triggers and avoidance of premature universal document integration.

Functional review is not RFC/ADR acceptance, Product Contract stabilization, Platform Capability promotion, legal opinion, signature-validity certification or operational-readiness approval.

## 2. Iteration 1 — concrete profile and authority separation

### Findings

1. “СЭД/ECM/ЭДО” as one integration target would collapse materially different authority domains.
2. A generic document identifier could hide distinct Directum card/version identifiers and Диадок box/message/entity/document identities.
3. A locally copied document could accidentally become described as authoritative.
4. A reference design could be mistaken for proof of a discovered customer installation.

### Reconciliation

The artifact now fixes two separate concrete profiles:

- Directum RX organization-controlled deployment through the official Integration Service REST/OData surface;
- Контур.Диадок organization box/account through the official HTTP API.

It also:

- preserves Directum authority for document/card/version/workflow state;
- preserves Диадок authority for service-side document/message/docflow/signature evidence;
- starts both as `External Reference`;
- keeps all vendor IDs as scoped external aliases/references;
- states that exact real deployment/box versions, modules, rights and API assumptions must be discovered before reliance.

Result: material objections closed.

## 3. Iteration 2 — RFC-0008 document/content/signature review

### Findings

1. File bytes, vendor document IDs and Arvectum Document identity could be conflated.
2. Signature evidence could be misrepresented as Organizational Authority, approval or blanket legal validity.
3. Fetching full document content by default could create unnecessary retention and data-minimization risk.
4. OCR/search/summary/preview derivatives could become competing document authority.

### Reconciliation

The artifact now explicitly:

- separates logical Document identity from vendor IDs, files, bytes and storage locators;
- treats signature/certificate information only as external evidence;
- states that authentication, API permission, possession of a certificate and signature evidence do not establish Organizational Authority;
- prefers metadata/reference retrieval where content is unnecessary;
- subjects fetched content to classification/purpose/retention/deletion controls;
- keeps OCR, extraction, summaries, previews, embeddings and other derivatives non-authoritative by default under RFC-0008/RFC-0007.

Result: material objections closed.

## 4. Iteration 3 — effects, events and reliability review

### Findings

1. Both vendor APIs expose capabilities beyond read-only retrieval, creating risk of accidental write admission.
2. Диадок signing/sending can create consequential external commitments and cannot be inferred from API availability.
3. Диадок event-feed items could be over-promoted into canonical Arvectum Events.
4. Network failure or pagination gaps could be mistaken for a complete/current external state.
5. Historical replay could accidentally repeat an external document effect in a future implementation.

### Reconciliation

The artifact now:

- enumerates bounded read operations separately for Directum and Диадок;
- explicitly excludes Directum create/update/delete/task/approval/workflow/registration effects;
- explicitly excludes Диадок signing, sending, draft send, approval/rejection/annulment/deletion/settings/counterparty mutations;
- makes future signing/sending subject to a new effect design, Organizational Authority model, key boundary, Governed Execution and INT-B6;
- treats Диадок feed entries and Directum API observations as source occurrences before RFC-0006 Event admission;
- preserves cursor/index, pagination/completeness, stale/gap and reconciliation state;
- reiterates that replay cannot repeat external effects without a new authorized Governed Execution.

Result: material objections closed.

## 5. Iteration 4 — product/platform, lifecycle and legal-boundary review

### Findings

1. Directum taxonomies/routes and Диадок signing/legal rules could leak into the domain-neutral connector envelope.
2. A common document DTO/runtime, shared event ingestion service or signing runtime could be prematurely fixed.
3. Connector termination could be confused with deleting authoritative external documents or reversing signatures/legal effects.
4. Product Contract might be required merely because the architecture document exists rather than before actual governed reliance.
5. Vendor documentation might be mistaken for an Arvectum legal conclusion regarding signature validity or retention.

### Reconciliation

The artifact now:

- keeps Directum document kinds, routes, registration, deadlines and attention rules product/customer-owned;
- keeps Диадок document-type policy, signing authority, powers of attorney, counterparty policy, tax/accounting/legal interpretation and statutory retention outside the connector;
- records shared runtime/content repository/schema registry/event-ingestion/signing/key-management choices as ADR triggers rather than INT-B5 decisions;
- defines termination as stopping retrieval/revoking local credentials/removing governed caches while leaving external authority untouched and preserving lawful history;
- requires Product Contract before governed product/shared-platform reliance, not merely for retaining the design baseline;
- states that vendor documentation is implementation evidence only and does not establish legal validity or Arvectum authority.

Result: no remaining material objection.

## 6. External feasibility evidence review

Official vendor evidence checked on `2026-08-22` supports the bounded design assumptions:

- Directum RX provides Integration Service REST API using JSON/OData v4.0 and supports enterprise identity integration;
- Диадок exposes an HTTP API for documents, messages, signatures/status and a chronological box event feed;
- Диадок integration uses registered OAuth access-token flows;
- Диадок API does not itself create a real electronic signature from a private key.

This evidence does not prove a specific customer's deployment, enabled modules, tariffs, rights, customizations, document types or legal configuration.

## 7. Higher-authority compatibility

- **Constitution 1.2.0:** compatible; external authority, security, portability, domain boundaries and proportionality preserved.
- **RFC-0001:** compatible; no competing source of truth or speculative generic connector capability admitted.
- **RFC-0002:** compatible; external IDs remain aliases/references and authority modes remain explicit.
- **RFC-0003:** compatible; least privilege, secret minimization, Organization scope, purpose limitation, retention/deletion and authority separation preserved.
- **RFC-0004:** compatible; Product Contract is required before governed reliance and hidden coupling is prohibited.
- **RFC-0005:** compatible; consequential external effects are not admitted; future signing/sending/mutation requires explicit Governed Execution semantics.
- **RFC-0006:** compatible; source occurrences/feed items are not automatic canonical Events and replay is side-effect safe.
- **RFC-0007:** compatible; document observations/derivatives are not automatically validated Knowledge.
- **RFC-0008:** compatible; Document identity, version, content, derivatives, signature evidence, external authority and portability boundaries are preserved.

No Accepted ADR conflict was found. No new ADR is required because INT-B5 selects only vendor-specific integration surfaces and no shared runtime/topology.

## 8. Final result

**PASS after bounded reconciliation — 4 of maximum 7 iterations.**

INT-B5 is fit to close as `Complete / concrete integration design baseline`.

Closure does not prove a live/customer Directum RX deployment or Диадок box, create a real connector implementation, authorize a signature/send/approval/document mutation, establish legal validity, stabilize a Product Contract, activate a Platform Capability or establish public compatibility/support commitments.

Next integration-lane action:

> **INT-B6 — Integration security/reliability review.**
