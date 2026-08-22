# INT-B5 — СЭД/ECM/ЭДО Design

Status: `Complete / concrete integration design baseline`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` and `product_specific` boundaries
Roadmap lane: `Lane B — Russian-market integrations`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](../roadmap/ROADMAP.md)
Predecessors:
- [`INT-B1 — Integration Portfolio Baseline`](INT-B1-integration-portfolio-baseline.md) `1.0.0`;
- [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0`;
- [`INT-B3 — 1С First-Candidate Design`](INT-B3-1c-erp-first-candidate-design.md) `1.0.0`;
- [`INT-B4 — CRM Designs`](INT-B4-crm-designs.md) `1.0.0`.

## 1. Purpose

INT-B5 applies the INT-B2 Connector Boundary Envelope to two concrete Russian-market document-system profiles:

1. **СЭД/ECM:** Directum RX — one organization-controlled deployment bound through the official Integration Service REST/OData interface;
2. **ЭДО:** Контур.Диадок — one organization box/account bound through the official HTTP API.

The two profiles remain separate system-specific designs.

INT-B5 does **not** create:

- a universal document-management connector;
- a shared СЭД/ECM/ЭДО business schema;
- a universal document status taxonomy;
- a common approval/signature model;
- a generic archival/retention authority model;
- a legal-validity determination engine;
- an authorization to sign, send, delete, approve, register or otherwise mutate external documents;
- a public/stable connector API or SDK;
- a Stable Product Contract or Active Platform Capability.

The bounded organizational outcome is:

> **Surface authoritative external document/card/version/workflow context from Directum RX and authoritative legally significant electronic-document/signature/docflow evidence from Диадок in Arvectum Workspace while the external systems remain authoritative and employees continue working in their existing systems.**

The first admitted scope is read/projection oriented.

## 2. Canonical basis

INT-B5 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0002 external identifier, Canonical Record and authority-mode semantics;
- RFC-0003 identity/authentication/authorization/Organizational Authority/Data Governance separation, least privilege, secret handling, retention/deletion and portability;
- RFC-0004 Product Contract boundary and hidden-coupling prohibition;
- RFC-0005 Governed Execution, effect classification, idempotency, uncertainty, compensation and external-effect semantics;
- RFC-0006 transport/source occurrence versus canonical Event admission, provenance and replay safety;
- RFC-0008 Document/Artifact identity, version, content, signature/seal evidence, external authority, rendition and retention boundaries;
- INT-B1 ranked portfolio baseline;
- INT-B2 Connector Boundary Envelope;
- canonical roadmap `2.92.0` at task start.

No conflict with higher-authority canonical sources was found.

## 3. External implementation evidence

Official vendor documentation checked on `2026-08-22` supports the bounded feasibility assumptions below.

### 3.1 Directum RX

Official Directum material states that:

- Directum RX exposes an Integration Service REST API;
- data exchange uses JSON over OData v4.0;
- Directum RX is intended to integrate with ERP, MDM, CRM and other open systems;
- authentication can be integrated with organization identity infrastructure and external authentication providers/protocols;
- Directum RX provides document-management and business-process capabilities.

Evidence:

- <https://www.directum.ru/products/directum/architecture>
- <https://www.directum.ru/products/directum>
- <https://www.directum.ru/products/directum/bpm-instruments>

These sources establish supported integration capability, not the exact entity model, permissions, extensions, customizations or enabled API surface of any particular deployment.

### 3.2 Контур.Диадок

Official Диадок API documentation states that:

- Диадок is a system for exchange of legally significant electronic documents between organizations;
- integration is available through an HTTP API;
- an integration solution is registered and obtains an OAuth access token using supported authorization flows;
- the API exposes document retrieval, message retrieval, document status/docflow information, signature information and a chronological event feed for a box;
- `GetNewEvents (V8)` returns the ordered event feed for a box and supports continuation/pagination semantics;
- API methods expose information about signatures and certificates;
- the Диадок API does not create a document signature: the signature is generated independently using the private key and cryptographic facilities and then supplied where a signing/sending operation requires it.

Evidence:

- <https://developer.kontur.ru/doc/diadoc-api/index.html>
- <https://developer.kontur.ru/doc/diadoc-api/howtostart/integration.html>
- <https://developer.kontur.ru/doc/diadoc-api/api-catalog/documents.html>
- <https://developer.kontur.ru/doc/diadoc-api/instructions/events.html>
- <https://developer.kontur.ru/doc/diadoc-api/http/GetNewEvents_V8.html>
- <https://developer.kontur.ru/doc/diadoc-api/instructions/documents/getdocs.html>
- <https://developer.kontur.ru/doc/diadoc-api/glossary/signature.html>

Vendor documentation is implementation evidence only and does not define Arvectum OS authority or governance.

## 4. Selected concrete profiles

### 4.1 Directum RX profile

Canonical design identifier:

`directum_rx_document_read_v1`

Reference profile:

| Property | INT-B5 disposition |
|---|---|
| External system | `Directum RX` |
| Deployment profile | organization-controlled Directum RX deployment |
| Integration surface | official Integration Service REST API / OData v4 |
| Transport | HTTPS required for real deployment |
| Authentication | dedicated organization integration principal using an authentication mechanism supported by the actual deployment |
| Access | read-only for first admitted scope |
| External authority | Directum RX remains authoritative for its document cards, versions and workflow/task state |
| Arvectum OS authority mode | `External Reference` by default |
| Organization scope | exactly one Arvectum OS Organization per endpoint binding |
| Product dependence | none until a Product Contract declares governed reliance |

Exact deployment version, installed solutions/modules, custom entity types, document kinds, route/task types, security model and exposed Integration Service entities MUST be discovered and pinned before real reliance.

### 4.2 Диадок profile

Canonical design identifier:

`kontur_diadoc_box_read_v1`

Reference profile:

| Property | INT-B5 disposition |
|---|---|
| External system | `Контур.Диадок` |
| Binding | one organization box/account accessible to the integration identity |
| Integration surface | official HTTP API |
| Authentication | registered integration + supported OAuth access-token flow |
| Access | read-only for first admitted business scope |
| External authority | Диадок remains authoritative for box/message/document/docflow/signature evidence exposed by the service |
| Arvectum OS authority mode | `External Reference` by default |
| Event retrieval | bounded polling via current supported event-feed API where used |
| Organization scope | one Arvectum OS Organization mapped to explicitly allowed Диадок organization box(es) |
| Product dependence | none until a Product Contract declares governed reliance |

A real binding MUST discover and pin organization/box identifiers, integration identity, exact scopes/rights, API version assumptions, document-type coverage, retention/export requirements and allowed counterparties/use purposes.

## 5. Why these two first candidates

Directum RX and Диадок represent materially different authority domains that commonly coexist rather than substitute for each other:

- Directum RX represents internal document-management, card/version, task and workflow state;
- Диадок represents inter-organizational electronic-document exchange and the externally maintained document/signature/docflow evidence exposed by the service.

They are useful together because Arvectum Workspace can provide a governed cross-system attention layer without replacing either user interface or creating a competing source of truth.

The design deliberately avoids asserting that every organization uses both systems or that one system is authoritative for all document semantics.

## 6. Document and identity boundaries

RFC-0008 requires logical Document identity to remain distinct from files, bytes, storage locators and vendor identifiers.

Accordingly:

1. a Directum RX entity/document-card identifier is an **external identifier/reference**, not automatically an Arvectum OS Document Subject Identity;
2. a Directum RX document version identifier is not automatically an Arvectum OS Document Version Identity;
3. a Диадок `boxId`, `messageId`, `entityId`, `documentId` or event identifier is an external identifier scoped to that service/binding and MUST NOT silently become an Arvectum OS Subject Identity;
4. a cryptographic hash or signature identifier does not establish organizational identity, authority, approval or legal truth by itself;
5. cross-system matching between a Directum RX document and a Диадок document MUST be an explicit governed relationship with evidence, not a match based only on filename, amount, date, counterparty name or similar heuristics.

Where an Arvectum-native governed reference is needed, it stores its own stable identity plus external aliases/references and authority declaration.

## 7. Authority model

### 7.1 Directum RX

For the first scope:

- Directum RX is authoritative for the document card fields, source document/version references and workflow/task state declared by the actual deployment;
- Arvectum OS uses `External Reference`;
- Workspace projections, OCR/search indexes, summaries, embeddings, extracted metadata and attention signals are non-authoritative projections unless separately promoted under RFC-0008/RFC-0007;
- product interpretation such as “overdue”, “high risk”, “requires CEO attention” or “needs legal review” is not Directum-authoritative unless explicitly sourced from Directum state.

### 7.2 Диадок

For the first scope:

- Диадок remains authoritative for the service-side representation of the organization box, messages, document entities, docflow/status information and signature/certificate evidence returned by its API;
- Arvectum OS uses `External Reference`;
- a fetched signature or certificate fact is evidence about the external document state, not independent proof of Organizational Authority, lawful signing authority, enforceability or legal validity;
- local previews, parsed XML, printable forms, OCR, summaries and search projections are non-authoritative derivatives unless separately governed.

### 7.3 No authority laundering

Copying external document data into an Arvectum schema MUST NOT turn Arvectum OS into the authority for the underlying external document state.

If a future use requires a `Governed Replica`, the Product Contract/design MUST explicitly define synchronization, freshness, conflict behavior, lawful content retention, signature preservation, deletion/export and outage semantics before promotion.

## 8. Directum RX operation contracts

The first Directum RX design exposes only explicit read operations.

### 8.1 `directum.metadata.discover`

Purpose: discover actual integration metadata/entity surface for the bound deployment.

- direction: `read_from_external`;
- effect: `read_only`;
- output: compatibility evidence and mapped entity/property capabilities;
- result: supported / unsupported / partial / incompatible;
- no automatic schema generalization across deployments.

### 8.2 `directum.documents.list`

Purpose: retrieve a bounded list of document/card references needed for Workspace projection.

- direction: `read_from_external`;
- effect: `read_only`;
- preserves external identifiers, source type, freshness and pagination state;
- partial pages MUST NOT be represented as a complete document population.

### 8.3 `directum.documents.get`

Purpose: retrieve one current document/card representation by external identity.

- direction: `read_from_external`;
- effect: `read_only`;
- exact fields remain deployment-specific;
- access result is constrained by the integration principal and Directum deployment permissions.

### 8.4 `directum.document_versions.list_or_get`

Purpose: retrieve available version metadata/content references where the actual API/deployment exposes them and Data Governance permits.

- direction: `read_from_external`;
- effect: `read_only`;
- content retrieval MAY be omitted when metadata is sufficient;
- if content is retrieved, classification/retention/minimization rules apply and the exact external version/content provenance is preserved.

### 8.5 `directum.workflow_or_tasks.list_or_get`

Purpose: retrieve bounded task/workflow status needed for attention routing.

- direction: `read_from_external`;
- effect: `read_only`;
- workflow/task semantics remain Directum-deployment/product-owned;
- no task completion, assignment, approval, route transition or document registration is admitted.

### 8.6 Explicitly excluded Directum effects

INT-B5 does not admit:

- create/update/delete document cards;
- upload/replace document content;
- create a new governed external document version;
- start/complete/reassign tasks;
- approve/reject documents;
- start or transition workflows;
- register incoming/outgoing documents;
- change access rights, retention or classification;
- invoke arbitrary server functions/actions merely because the API exposes them.

Any future such operation is a new design/admission decision.

## 9. Диадок operation contracts

### 9.1 `diadoc.organizations_or_boxes.discover`

Purpose: identify organization/box bindings available to the integration identity.

- direction: `read_from_external`;
- effect: `read_only`;
- output is discovery evidence, not permission to bind every returned box to one Arvectum Organization.

### 9.2 `diadoc.documents.list`

Purpose: retrieve a bounded list of documents matching declared filters.

- direction: `read_from_external`;
- effect: `read_only`;
- supports pagination/filter semantics of the selected current API version;
- incomplete pages and filtered results MUST remain explicit.

### 9.3 `diadoc.documents.get`

Purpose: retrieve one document representation by external identity.

- direction: `read_from_external`;
- effect: `read_only`;
- content retrieval SHOULD be minimized where metadata/status evidence is sufficient;
- when content is retrieved, exact external document/message/entity identity and provenance are retained.

### 9.4 `diadoc.messages.get`

Purpose: retrieve message/docflow context necessary to reconstruct the external document state.

- direction: `read_from_external`;
- effect: `read_only`;
- message/entity relationships remain vendor-specific;
- no Arvectum universal message/document hierarchy is created.

### 9.5 `diadoc.signatures.get_info`

Purpose: retrieve signature/certificate information already present in Диадок.

- direction: `read_from_external`;
- effect: `read_only`;
- result is external evidence about the signature/certificate;
- result MUST NOT be treated as an Arvectum approval, Organizational Authority decision or blanket legal-validity conclusion.

### 9.6 `diadoc.events.list_new`

Purpose: retrieve bounded new box events through the supported event-feed API.

- direction: `read_from_external`;
- effect: `read_only`;
- continuation/index state is preserved for gap detection/reconciliation;
- a Диадок box event is initially a **source occurrence**, not automatically an RFC-0006 canonical Event;
- duplicate delivery/re-read MUST NOT create duplicate canonical Events or effects.

### 9.7 Explicitly excluded Диадок effects

INT-B5 does not admit:

- generating or applying a real electronic signature;
- sending a document/message;
- sending a draft;
- preparing a document for signing as a consequential workflow step;
- approving/rejecting/annulling/revoking a document;
- deleting/restoring external documents;
- changing counterparty relationships;
- changing organization/box settings or access;
- any external organizational commitment.

These actions require a separate write/effect design because they may carry legal, contractual, financial or organizational consequences.

## 10. Signature boundary

Signature handling is a hard authority boundary.

Under RFC-0008 and INT-B5:

1. signature/seal evidence is distinct from authorization, Organizational Authority and governed approval;
2. possession of a certificate or ability to call an API does not establish entitlement to sign;
3. Arvectum AI MUST NOT autonomously decide to sign or send a legally significant document;
4. reusable private keys MUST NOT be copied into prompts, ordinary Canonical Records, Events, logs or connector payload history;
5. the first INT-B5 scope retrieves signature information only;
6. any future signing/sending path requires a concrete legal/organizational authority model, human/approved governance gate, cryptographic-key boundary, exact signer context, idempotency/uncertainty semantics, evidence plan and INT-B6 review.

Vendor documentation explicitly states that the Диадок API does not itself create the signature file from the private key. INT-B5 therefore does not introduce a signing-key runtime or secrets technology choice.

## 11. Retention, content and derived artifacts

Document-system integration creates an elevated risk of uncontrolled content duplication.

Rules:

- metadata/reference retrieval is preferred when full content is unnecessary;
- external content MUST NOT be retained merely because it was fetched;
- local cache/projection retention is independently governed from external-system retention;
- OCR, extraction, translation, summarization, redaction, rendering and preview outputs are derived Artifacts and non-authoritative by default;
- derived Artifacts inherit Organization/classification/purpose/rights/retention constraints unless a governed transformation establishes another permitted rule;
- deletion of a local cache does not delete the external authoritative document;
- external deletion does not permit Arvectum to claim the external state never existed when lawful historical evidence must remain, but retained content/evidence remains subject to applicable deletion/minimization rules;
- portability packages preserve references, provenance and explicit omissions rather than silently exporting inaccessible or unlawfully retained content.

## 12. Freshness, completeness and reconciliation

### 12.1 Directum RX

The concrete adapter MUST expose:

- `retrieved_at` or equivalent observation time;
- pagination/completeness state;
- stale/unavailable state;
- last successful compatibility check;
- external version/change marker only where the deployment actually provides one and its semantics are understood.

No universal Directum change feed or modification timestamp is assumed by INT-B5.

### 12.2 Диадок

For event-feed use the adapter MUST preserve:

- bound `boxId`/external box identity;
- current supported API version used;
- continuation/index cursor semantics;
- last successfully processed external occurrence identity/index;
- detected gap/retry state;
- page completeness;
- reconciliation result.

A polling timeout, network error or missing page MUST NOT be interpreted as “no new documents/events”.

### 12.3 Reconciliation outcomes

Where source state is incomplete, contradictory or uncertain, INT-B2 reconciliation states apply:

- `confirmed_effect` where a previously uncertain external effect is later proven;
- `confirmed_no_effect`;
- `superseded`;
- `manual_review_required`;
- `unresolved`;
- `compensated` only when a separately authorized compensating action exists.

The initial read-only scope primarily uses reconciliation for completeness/freshness/source-identity disputes rather than external side effects.

## 13. Event and provenance boundary

Directum API responses, Диадок event-feed items, HTTP receipts, polling results, integration logs and telemetry are not automatically canonical Arvectum Events.

Canonical Event admission requires RFC-0006 validation appropriate to the intended use.

For admitted external-source Events, preserve where applicable:

- Organization;
- connector definition/version;
- endpoint/box binding;
- external source occurrence identity;
- external authoritative system;
- occurrence/recording time distinction;
- source document/message/card/version references;
- classification and permitted payload scope;
- duplicate/gap/replay state;
- provenance and correlation.

Historical replay MUST NOT invoke signing, sending, task transitions or other external effects without a new authorized Governed Execution.

## 14. Product-owned semantics

The connector boundary MUST NOT own organization-specific document business logic.

Examples remaining outside the shared connector envelope:

### Directum RX/product/customer owned

- document kinds and card taxonomies;
- registration rules;
- route/approval semantics;
- task types and deadlines;
- internal records-management classification;
- customer folder/file-plan semantics;
- access and retention rules beyond the platform governance envelope;
- “needs attention” business criteria.

### Диадок/product/customer/legal-governance owned

- which document types the organization is permitted/required to exchange;
- signing-authority matrix;
- powers of attorney and signer eligibility;
- counterparties and exchange policy;
- acceptance/rejection/annulment business rules;
- tax/accounting/legal interpretation of a document;
- statutory retention periods;
- legal-validity conclusions.

Arvectum OS may preserve and execute these only through appropriate product/governance assets; the connector itself does not invent them.

## 15. Product Contract boundary

INT-B5 is an architecture design and does not itself require a Product Contract merely to exist.

Before a product or shared platform behavior relies on these connectors, the applicable Product Contract MUST declare, proportionate to scope:

- connector and operation versions;
- exact external deployment/box binding;
- authoritative source and authority mode;
- document/card/message/version identities relied upon;
- allowed read/write/effect operations;
- classification, purpose, rights, retention and deletion rules;
- content-versus-metadata retrieval rules;
- signature evidence handling;
- event/source-occurrence semantics where relied upon;
- freshness/completeness/reconciliation requirements;
- failure/degraded-mode behavior;
- compatibility/migration/termination behavior;
- any consequential external-effect authority and approval requirements.

Hidden reliance on internal Directum database tables, private Диадок implementation details, undocumented endpoints, logs or incidental data stores is prohibited.

## 16. Failure and degraded modes

### Directum RX

If the deployment is unreachable or incompatible:

- existing Workspace projections become `stale`/`source_unavailable` with last successful retrieval time;
- stale state MUST NOT be presented as current authoritative Directum state;
- local edits MUST NOT be used to “repair” the missing external authority;
- operator navigation back to Directum may be disabled or marked unavailable.

### Диадок

If API/token/box access fails:

- event progression is paused at the last confirmed cursor/index;
- gaps remain explicit;
- cached document/signature status is marked stale;
- lack of new events is not inferred;
- no automatic fallback signs/sends/changes external state.

Security or authority ambiguity fails closed for consequential use.

## 17. Disable, termination and portability

Connector disable/termination MUST support:

- disabling retrieval;
- revoking or deleting local credential bindings;
- removing local non-authoritative caches subject to retention rules;
- preserving lawful historical attribution/evidence;
- retaining external aliases necessary to explain historical records where lawful;
- exporting Arvectum-governed references/provenance under RFC-0003/RFC-0008 portability rules;
- explicit handling of inaccessible external content.

Termination MUST NOT delete or alter authoritative Directum RX or Диадок state by implication.

Rollback means rollback of connector implementation/configuration where reversible. It does not mean reversing external document registration, signature, sending or legal effect.

## 18. Security requirements

A real deployment MUST satisfy at least:

- explicit one-Organization endpoint/box scope;
- dedicated least-privilege integration identity where supported;
- indirect credential references;
- no reusable OAuth token, password, private key or certificate private material in ordinary canonical payloads, prompts, logs or exports;
- TLS/HTTPS;
- deny-by-default operation allowlist;
- purpose-limited data retrieval;
- content minimization;
- classification-aware logging and observability;
- attributable machine/service principal;
- token/credential rotation and revocation path;
- no ambient cross-Organization credential reuse;
- explicit user/organizational authority gate before any future consequential write/effect.

Authentication or technical API permission does not establish Organizational Authority.

## 19. ADR trigger analysis

INT-B5 does not select a new shared runtime/topology and therefore requires no new ADR for this design baseline.

A new ADR is required before a materially constraining shared decision such as:

- one common document-connector runtime for Directum/Диадок/other СЭД/ЭДО;
- mandatory shared OAuth/token/secrets technology;
- shared durable document-event ingestion topology;
- shared binary/content repository specifically for external connector payloads;
- shared schema registry or common document DTO that constrains products;
- universal document-change CDC/event transport;
- signing/key-management runtime;
- cross-connector archival/retention engine;
- deployment/isolation topology materially affecting security or portability.

## 20. Implementation admission gates

INT-B5 is design/evidence only.

Before the first material real connector implementation or governed reliance:

1. identify the real Directum deployment or Диадок organization box;
2. confirm exact vendor/API/deployment versions and enabled modules/features;
3. discover actual accessible entity/document types and rights;
4. declare Organization scope and Data Governance purpose;
5. create least-privilege credential bindings;
6. enumerate exact operations and effect classes;
7. create/approve the required Product Contract where RFC-0004 applies;
8. define retention/deletion/content-minimization obligations;
9. test freshness, pagination, gap, duplicate and recovery semantics;
10. verify failure-closed behavior and credential revocation;
11. complete `INT-B6 — Integration security/reliability review`;
12. run bounded test-environment evidence before consequential real-data reliance.

For any future signature/send/approval/document-mutation path, additional gates are mandatory:

- explicit Organizational Authority and approval model;
- signer/private-key boundary;
- legal/product decision defining admitted effect;
- idempotency and uncertain-outcome reconciliation;
- exact evidence/reconstruction contract;
- no autonomous AI final approval.

## 21. Exit criteria

INT-B5 is `Complete / concrete integration design baseline` when:

- named Directum RX and Контур.Диадок profiles are selected;
- their authority domains remain distinct;
- document/version/external identity boundaries conform to RFC-0008/RFC-0002;
- first operations are explicitly bounded and read-oriented;
- signing/sending/approval/mutation are excluded;
- signature evidence is separated from Organizational Authority and legal validity;
- retention/content/derived-artifact behavior is explicit;
- source occurrences are separated from canonical Events;
- Product Contract and INT-B6 gates are explicit;
- no generic СЭД/ECM/ЭДО schema/runtime is prematurely admitted;
- functional cross-review has no unresolved material objections.

## 22. Next action

After INT-B5 closure, the next integration-lane action is:

> **INT-B6 — Integration security/reliability review.**

INT-B6 reviews INT-B2 through INT-B5 as one candidate portfolio before any first material real connector implementation. It must test secrets/credentials, Organization isolation, least privilege, external authority, duplicate/gap/retry/replay, uncertainty/reconciliation, content/signature handling, failure/degraded modes, termination and operational evidence across the concrete 1С, CRM and document-system designs.
