# INT-B3 — 1С First-Candidate Design

Status: `Complete / concrete integration design baseline`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform` and `product_specific` boundaries
Roadmap lane: `Lane B — Russian-market integrations`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](../roadmap/ROADMAP.md)
Predecessors:
- [`INT-B1 — Integration Portfolio Baseline`](INT-B1-integration-portfolio-baseline.md) `1.0.0`;
- [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0`.

## 1. Purpose

INT-B3 applies the INT-B2 domain-neutral connector boundary to one concrete first-candidate 1С design.

The selected target is:

> **`1С:ERP Управление предприятием 2`, standard configuration family `2.5`, self-hosted/client-server deployment, web-published standard OData interface, dedicated least-privilege integration identity, read-only procurement projection.**

This is a reference integration design for a concrete configuration/deployment profile. It is **not** evidence that a particular customer installation has already been discovered, tested or certified. Before real reliance, the exact deployed platform/configuration version, enabled modules, published metadata, authentication mechanism and object availability MUST be discovered and pinned.

The first bounded organizational outcome is:

> **Surface selected authoritative procurement order/status information from 1С:ERP into Arvectum Workspace so procurement work can be prioritized and reconciled without moving procurement authority out of 1С or requiring employees to abandon 1С.**

The first candidate is deliberately read-only. INT-B3 does not authorize creating, editing, posting, cancelling or otherwise mutating 1С business objects.

## 2. Canonical basis

INT-B3 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0002 external-identifier, Canonical Record, version and authority semantics;
- RFC-0003 identity/authentication/authorization/Organizational Authority/Data Governance separation, least privilege, secret handling and portability;
- RFC-0004 Product Contract requirements before governed platform reliance;
- RFC-0005 Governed Execution and external-effect semantics;
- RFC-0006 source-occurrence/Event/provenance/replay semantics;
- INT-B1 ranked portfolio baseline;
- INT-B2 Connector Boundary Envelope;
- canonical roadmap `2.90.0` at task start.

No conflict with higher-authority canonical sources was found.

## 3. External product evidence

Official 1С product/platform documentation checked on `2026-08-22` supports the feasibility assumptions used by this design:

1. `1С:ERP Управление предприятием` includes a procurement-management scope with supplier selection, purchase conditions, supplier orders, execution control, delivery/payment schedules and related purchasing processes:
   - <https://v8.1c.ru/erp/purchasing/>
   - <https://v8.1c.ru/erp/funktsionalnost-1s-erp/>
2. `1С:Предприятие 8` can publish an automatic REST interface for an application solution; the interface uses OData `3.0`, supports HTTP access and exposes metadata describing available application objects:
   - <https://v8.1c.ru/platforma/rest-interfeys/>
3. The platform can also expose custom HTTP services where a future concrete integration needs behavior narrower than or unsuitable for automatic OData:
   - <https://v8.1c.ru/platforma/http-servisy/>

These sources prove that supported integration surfaces exist. They do **not** prove that every concrete 1С:ERP deployment publishes OData, exposes identical metadata names, permits the same operations, or has the same authentication/network configuration.

## 4. Selected deployment profile

Canonical design identifier:

`1c_erp25_procurement_read_v1`

Reference profile:

| Property | INT-B3 disposition |
|---|---|
| External system | `1С:ERP Управление предприятием 2` |
| Configuration family | standard `2.5` family |
| Deployment | self-hosted/client-server organization deployment |
| Integration surface | standard OData interface published on an organization-controlled web server |
| Transport | HTTPS required by Arvectum integration policy for real deployment |
| Authentication | dedicated 1С integration identity through an authentication mechanism supported by the actual publication; exact mechanism discovered/pinned before activation |
| Access | read-only for the first admitted scope |
| External authority | 1С remains authoritative |
| Arvectum OS authority mode | `External Reference` by default; bounded `Governed Replica` only if later evidence demonstrates need |
| Organization scope | exactly one Arvectum OS Organization binding per connector endpoint |
| Product dependence | none until a Product Contract explicitly declares governed reliance |

The design does not assume cloud/Fresh deployment, direct database access, COM connection, filesystem coupling, private database schema access or undocumented 1С internals.

## 5. Why this candidate

`1С:ERP Управление предприятием 2` is selected before a narrower accounting-only configuration because the target organizational outcome is cross-functional procurement visibility rather than bookkeeping automation.

The candidate creates useful leverage while respecting the strategy that employees may continue working in familiar systems:

- procurement authority and operational editing remain in 1С;
- Arvectum Workspace can surface attention and organizational context above 1С;
- no forced replacement of the existing ERP user interface is required;
- the initial read-only boundary minimizes consequence while testing real integration value;
- successful evidence can later inform, but does not automatically justify, write-side integration or platform capability promotion.

This selection is a planning/design choice, not a claim about market share or customer prevalence.

## 6. Bounded organizational outcome

### 6.1 Outcome statement

The connector supplies enough authoritative procurement context for Arvectum Workspace to answer:

> **Which supplier orders represented in the bound 1С:ERP deployment currently require organizational attention, and what authoritative 1С record/status should the operator open or reconcile?**

### 6.2 In-scope information classes

The first design may retrieve, when present in the discovered deployment metadata:

- supplier-order identity/reference;
- order number and date;
- supplier/counterparty identity/reference and display label;
- organization/legal-entity reference needed to preserve scope;
- order lifecycle/status/state fields;
- expected delivery or schedule information where exposed;
- currency and total/value information only where needed for the product outcome and permitted by Data Governance;
- relevant 1С references needed to navigate/reconcile back to the authoritative object;
- source/version/freshness evidence sufficient for the declared use.

Exact metadata names and OData entity-set names are **not canonicalized by INT-B3**. They MUST be discovered from the actual deployment metadata and mapped in the system-specific adapter configuration.

### 6.3 Out of scope

INT-B3 excludes:

- editing or creating supplier orders;
- posting/unposting 1С documents;
- supplier selection or procurement approval decisions inside the connector;
- payment creation, treasury actions or accounting postings;
- inventory write-offs, receipt registration or returns;
- customer-specific purchasing policy;
- domain decision rules such as “late”, “high risk”, “critical” or “approve supplier” unless owned by a product/workflow outside the connector;
- universal 1С schema normalization across ERP, УТ, Бухгалтерия, КА or custom configurations.

## 7. INT-B2 Connector Definition application

### 7.1 Connector Definition

Reference logical definition:

```yaml
connector_id: connector.1c.erp25.procurement.read
connector_version: 1.0.0
adapter_kind: 1c_enterprise_8_odata
external_system_class: 1c_erp_2
compatibility_scope:
  configuration_family: 2.5
  deployment_profile: self_hosted_client_server
  interface: published_standard_odata
supported_operations:
  - procurement_orders.list
  - procurement_orders.get
  - counterparties.get
  - metadata.discover
status: design_baseline
```

This YAML is illustrative logical content, not a frozen wire format or SDK contract.

### 7.2 External Endpoint Binding

A real binding MUST identify at minimum:

- owning Arvectum OS Organization;
- external deployment identifier assigned by the organization;
- base HTTPS publication endpoint;
- exact 1С platform version if materially relevant;
- exact configuration name/version;
- publication/interface identity;
- authoritative scope: procurement records exposed through the declared binding;
- retrieval/freshness policy;
- credential binding reference;
- enabled/disabled state;
- date/time of last successful metadata discovery;
- last compatibility verification result.

Endpoint URL and credentials are deployment configuration, not portable public connector semantics.

## 8. Identity mapping

### 8.1 Rule

A 1С GUID/reference/key MUST NOT automatically become an Arvectum OS Subject Identity.

External object identity is represented as a governed alias/reference including at least:

```text
external_system = bound 1С deployment
external_namespace = discovered 1С metadata/entity-set namespace
external_object_type = discovered object/entity type
external_object_id = immutable/stable identifier exposed by the source where available
```

### 8.2 Arvectum identities

Arvectum OS creates its own stable identity only when a governed Arvectum subject is needed, for example an `External Reference` Canonical Record representing reliance on a particular supplier order.

The Arvectum record preserves the external alias and source authority; it does not claim ownership of the procurement fact.

### 8.3 Counterparty equivalence

A 1С counterparty reference MUST NOT be automatically merged with a CRM/customer/supplier identity from another system merely because name, INN or another field matches.

Cross-system entity resolution is a separate governed product/platform concern and requires explicit evidence/semantics. INT-B3 creates no universal master-data identity model.

## 9. Authority and state model

### 9.1 Authority mode

For first scope:

- authoritative source: bound `1С:ERP` deployment;
- Arvectum OS mode: `External Reference`;
- local Workspace projection: non-authoritative mutable projection;
- local adapter cache: non-authoritative technical cache where needed;
- no editable competing replica.

### 9.2 Governed Replica threshold

A future `Governed Replica` MAY be justified only if a concrete outcome requires materially better:

- offline continuity;
- historical reconstruction;
- bounded search/performance;
- stable snapshot comparison;
- product workflow continuity during temporary 1С unavailability.

Before such promotion the concrete contract MUST define synchronization, freshness, conflict behavior, retention, deletion, portability and recovery semantics.

INT-B3 does not make that promotion.

## 10. Operation contracts

### 10.1 `metadata.discover`

Purpose: retrieve OData metadata necessary to prove the actual deployment shape before business-object reliance.

- direction: `read_from_external`;
- effect class: `read_only`;
- output: discovered entity/type/property capabilities and compatibility evidence;
- authority: external deployment metadata is authoritative for what the publication exposes at discovery time;
- result: compatibility pass/fail/unsupported;
- no business data is made authoritative by metadata discovery.

### 10.2 `procurement_orders.list`

Purpose: retrieve a bounded set of supplier-order records for Workspace projection.

- direction: `read_from_external`;
- effect class: `read_only`;
- input: bounded filters/pagination/window permitted by adapter configuration;
- output: normalized adapter DTO with source identifiers and provenance;
- authority: 1С;
- retries: safe only as repeated read, subject to rate/resource controls;
- failure: no stale result may be represented as current without explicit freshness state.

### 10.3 `procurement_orders.get`

Purpose: retrieve one authoritative current supplier-order representation by external identity.

- direction: `read_from_external`;
- effect class: `read_only`;
- output includes source identity and retrieval time;
- missing object MUST be represented as an explicit source result, not silently converted to deletion of historical Arvectum evidence.

### 10.4 `counterparties.get`

Purpose: retrieve the source-side counterparty representation required to label/relate a supplier order.

- direction: `read_from_external`;
- effect class: `read_only`;
- no cross-system master-data merge is performed by this operation.

### 10.5 Write/effect operations

No write/effect operation is admitted by INT-B3 v1.0.0.

The following hypothetical classes remain **prohibited/unimplemented** until a later separately reviewed design:

- `procurement_orders.create`;
- `procurement_orders.update`;
- `procurement_orders.post`;
- `procurement_orders.cancel`;
- `receipts.create`;
- `payments.create`;
- any arbitrary/untyped `execute_1c_method` operation.

Technical OData support for create/update/delete or document posting does not constitute Arvectum authorization to expose those capabilities.

## 11. Credential and security model

A real connector binding requires a dedicated integration principal in 1С with the minimum source-side rights required for the selected read-only objects.

Requirements:

- credentials stored in an approved secret store or runtime secret mechanism, referenced indirectly from governed connector state;
- no password/token/private secret in Canonical Records, Events, logs, prompts, repository files or portable exports;
- one binding MUST NOT reuse credentials across Organizations by ambient convention;
- source-side account rights must be read-only for INT-B3 scope;
- endpoint access limited by network controls appropriate to the deployment;
- HTTPS required for real remote network transport under this Arvectum design;
- credential rotation/revocation must not erase historical attribution;
- authentication success does not imply Arvectum authorization, Organizational Authority or Data Governance permission.

The exact 1С authentication mechanism is deployment-specific and MUST be discovered/pinned before activation rather than guessed by the shared architecture.

## 12. Retrieval, freshness and synchronization

INT-B3 does not assume that every 1С:ERP object has a universally reliable `modified_at` field or source change feed.

Therefore the initial design uses **bounded pull/reconciliation semantics**, not an assumed universal CDC model.

A concrete adapter MUST define one of the following after metadata/deployment discovery:

1. source-supported incremental retrieval with a proven stable cursor/change marker; or
2. bounded time/window/key polling plus deterministic reconciliation; or
3. bounded full-list reconciliation for a small declared scope.

The adapter MUST expose freshness explicitly:

- `retrieved_at`;
- last successful source contact;
- query/snapshot scope;
- known incomplete/pagination state;
- stale/unavailable state where applicable.

Workspace MUST NOT present stale cached data as “current 1С state” without freshness indication.

## 13. Duplicate and reconciliation semantics

Because first scope is read-only, duplicate retrieval is not itself a duplicate external effect.

However duplicate/local projection behavior still requires deterministic identity handling:

- the same external object alias from the same endpoint binding resolves to the same governed external subject/reference;
- repeat retrieval updates a mutable projection or creates a new governed version only when the governed representation actually requires one;
- transport duplicates do not create multiple semantic supplier-order subjects;
- conflicting payloads with the same source identity are compared using source retrieval/version evidence where available;
- unresolved inconsistency is exposed rather than silently choosing a value for consequential use.

Reconciliation cases include:

- source object no longer returned by a list query;
- source object returns not-found;
- pagination interrupted;
- metadata changed incompatibly;
- object mapping fails;
- source unavailable;
- stale projection exceeds declared freshness threshold.

No case permits silently deleting historical canonical evidence merely because the current external object is absent.

## 14. Source occurrence and Event boundary

INT-B3 v1 is pull-oriented and does not require webhooks.

Each OData response is a transport/source result, not automatically a canonical Event.

Canonical Event admission is justified only when an occurrence is organizationally meaningful and passes RFC-0006 admission rules. Examples that MAY later become canonical Events include:

- connector compatibility status materially changed;
- a governed synchronization/reconciliation outcome materially affected a workflow;
- a consequential later write operation produced externally confirmed evidence.

Routine polling logs, request latency, HTTP status metrics and retries remain telemetry by default.

## 15. Product Contract boundary

INT-B3 is a design baseline and does not yet require a Product Contract merely to exist in the repository.

Before a product or Workspace feature **relies** on this connector through shared platform state/history/behavior, the applicable RFC-0004 Product Contract MUST declare at minimum:

- connector definition/version;
- exact endpoint binding scope;
- operations relied upon;
- product-owned interpretation of the retrieved data;
- authority mode and authoritative source;
- input/output schema compatibility relied upon;
- freshness/degraded-mode expectations;
- classification/purpose/retention requirements;
- record/Event dependencies;
- failure and reconciliation behavior;
- migration/termination behavior;
- security and Organization scope.

Tender/Procurement business rules such as supplier risk, tender matching, purchasing recommendations, approval thresholds or “needs attention” criteria remain product-owned and MUST NOT be embedded in the shared 1С connector.

## 16. Workspace composition boundary

The first intended Workspace composition is a non-authoritative procurement projection.

Illustrative operator experience:

```text
Needs Attention
└── Supplier order from 1С
    ├── 1С order number/date
    ├── supplier label
    ├── authoritative status
    ├── freshness/source indicator
    ├── related product/workflow context
    └── open/reconcile source reference
```

The projection MUST distinguish:

- data retrieved from authoritative 1С;
- Arvectum-owned attention/workflow state;
- product-generated interpretation/recommendation;
- AI-generated proposal or explanation.

An Arvectum attention marker may be `Native` Arvectum state while the underlying order remains externally authoritative in 1С. These authorities MUST NOT be conflated.

## 17. Failure and degraded-mode behavior

| Failure | Required behavior |
|---|---|
| 1С endpoint unavailable | preserve last-known projection only with explicit stale state; do not claim current authority |
| Authentication rejected | fail closed; surface connector attention; do not broaden credentials automatically |
| Authorization/source rights insufficient | fail closed for affected operation; record attributable technical evidence without secrets |
| OData metadata incompatible | mark connector binding incompatible and block relied-upon mapping until reviewed |
| Mapping error | quarantine/expose affected source result; do not fabricate normalized value |
| Pagination/interruption | mark snapshot incomplete; do not treat partial list as full authoritative population |
| Source object missing | expose source absence/not-found; preserve historical references/evidence |
| Classification/Data Governance gate fails | do not retrieve/store/propgate disallowed payload |

## 18. Portability and termination

Connector termination MUST allow:

- disabling new retrievals;
- revoking/deleting runtime credentials according to secret-governance rules;
- removing subscriptions if any are later introduced;
- deleting non-authoritative caches/projections subject to retention requirements;
- retaining lawful historical attribution/provenance where necessary;
- exporting governed references without exporting reusable source credentials;
- identifying which product/workflow dependencies must be migrated or retired.

Termination of the connector does not delete or mutate the authoritative 1С system.

## 19. ADR trigger analysis

No new ADR is required for INT-B3 design baseline because this document does not select a cross-product shared runtime/topology.

A future implementation requires ADR consideration if it would standardize any materially constraining shared choice such as:

- a single shared 1С connector process/runtime for multiple products;
- a mandatory secrets-manager technology;
- a shared polling scheduler/outbox/inbox architecture;
- a shared connector persistence schema exposed across products;
- a durable public/internal SDK or wire contract;
- a connector isolation/deployment topology with security/portability consequences.

Using OData for this concrete first adapter is a system-specific implementation decision supported by the external platform and does not itself establish OData as the universal Arvectum connector protocol.

## 20. Implementation admission gates

A real INT-B3 connector implementation MUST NOT become governed shared reliance until all applicable gates are satisfied:

- [ ] actual 1С:ERP deployment selected;
- [ ] exact platform/configuration versions recorded;
- [ ] standard OData publication enabled and reachable through approved network path;
- [ ] `$metadata`/equivalent discovered and mapping compatibility proven;
- [ ] dedicated least-privilege read-only 1С integration principal established;
- [ ] secret binding established outside canonical payloads;
- [ ] exact source objects/fields needed for bounded outcome mapped;
- [ ] classification/purpose/retention disposition recorded;
- [ ] Organization scope proven;
- [ ] retrieval/freshness/reconciliation strategy proven;
- [ ] Product Contract created before product/shared-platform reliance;
- [ ] applicable ADR decision completed if a shared constraining implementation choice is introduced;
- [ ] integration security/reliability review completed before material real reliance under INT-B6;
- [ ] no write/posting/payment/signature operation exposed by accidental OData capability;
- [ ] read-after-write/operational evidence and rollback/disable path validated for connector configuration.

## 21. Exit criteria and result

INT-B3 design exit criteria are satisfied:

- [x] one concrete 1С configuration family selected: `1С:ERP Управление предприятием 2`, standard `2.5` family;
- [x] one concrete reference deployment profile selected: self-hosted/client-server + published OData;
- [x] bounded organizational outcome selected: read-only procurement attention projection;
- [x] external authority remains 1С;
- [x] first authority mode set to `External Reference`;
- [x] identity mapping defined without reusing external IDs as Arvectum identities;
- [x] exact first operations enumerated;
- [x] write/effect operations explicitly excluded;
- [x] credential/least-privilege model defined;
- [x] freshness/retrieval/reconciliation semantics defined without assuming universal CDC;
- [x] Event/provenance boundary defined;
- [x] Product Contract trigger and product-owned business semantics defined;
- [x] failure, termination and portability behavior defined;
- [x] ADR triggers analyzed;
- [x] implementation admission gates recorded.

**Result:** `INT-B3 — Complete / concrete integration design baseline`.

This closure does not prove a live customer 1С deployment, create a real connector implementation, authorize any 1С write/effect, stabilize a Product Contract, activate a Platform Capability or establish public compatibility/support commitments.

The next integration-lane action is `INT-B4 — CRM designs`, keeping Битрикс24 and amoCRM as separate concrete designs until real reuse evidence supports any shared CRM abstraction.
