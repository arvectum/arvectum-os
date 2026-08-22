# INT-B4 — CRM Designs: Битрикс24 and amoCRM

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
- [`INT-B3 — 1С First-Candidate Design`](INT-B3-1c-erp-first-candidate-design.md) `1.0.0`.

## 1. Purpose

INT-B4 applies the INT-B2 Connector Boundary Envelope to two concrete CRM families that are strategically relevant to Russian-market organizations:

1. **Битрикс24 — one concrete organization portal/account binding**;
2. **amoCRM — one concrete organization account binding**.

They remain separate system-specific designs. INT-B4 does not create a generic CRM connector, a universal CRM schema, a shared pipeline model or an assumption that similarly named CRM concepts have identical semantics.

The bounded organizational outcome for both designs is deliberately similar but not normalized into one business contract:

> **Surface selected authoritative CRM entities, tasks and change/attention signals in Arvectum Workspace while sales/relationship staff continue normal work in their existing CRM.**

The first admitted scope is read/projection oriented. External CRM mutation is not authorized by INT-B4 merely because the vendor API supports it.

## 2. Canonical basis

INT-B4 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0002 external-identifier, Canonical Record, version and authority semantics;
- RFC-0003 identity/authentication/authorization/Organizational Authority/Data Governance separation, least privilege, secret handling and portability;
- RFC-0004 Product Contract requirements before governed platform reliance;
- RFC-0005 Governed Execution, effect classification, idempotency, uncertainty and reconciliation semantics;
- RFC-0006 source-occurrence/Event/provenance/replay semantics;
- INT-B1 ranked portfolio baseline;
- INT-B2 Connector Boundary Envelope;
- canonical roadmap `2.91.0` at task start.

No conflict with higher-authority canonical sources was found.

## 3. External product evidence

Official vendor documentation checked on `2026-08-22` supports these feasibility assumptions.

### 3.1 Битрикс24

Official REST documentation establishes that:

- REST API calls are ordinary HTTP requests to methods in a concrete Bitrix24 portal;
- authorization may use a local incoming webhook or OAuth 2.0 token;
- REST calls execute in the context of a concrete portal user and are limited by that user's permissions and selected scopes;
- CRM list methods such as `crm.deal.list` expose deal identifiers, title, category/pipeline identifier, stage, amount, responsible user and creation date.

Evidence:

- <https://apidocs.bitrix24.ru/settings/how-to-call-rest-api/general-principles.html>
- <https://apidocs.bitrix24.ru/settings/how-to-call-rest-api/authorization.html>
- <https://apidocs.bitrix24.ru/api-reference/crm/deals/crm-deal-list.html>

### 3.2 amoCRM

Official developer documentation establishes that:

- API v4 provides methods for deals, contacts, companies, tasks and other CRM entities;
- integrations use OAuth 2.0 rather than the retired legacy API-key mechanism;
- available API access is constrained by integration scopes and user/account rights;
- webhooks can be listed, created and deleted through API v4, with subscriptions to declared event types;
- tasks can be read through `GET /api/v4/tasks` and concrete task retrieval, while write methods also exist separately.

Evidence:

- <https://www.amocrm.ru/developers/content/crm_platform/api-reference>
- <https://www.amocrm.ru/developers/content/oauth/oauth>
- <https://www.amocrm.ru/developers/content/oauth/scopes>
- <https://www.amocrm.ru/developers/content/crm_platform/webhooks-api>
- <https://www.amocrm.ru/developers/content/crm_platform/tasks-api>

Vendor documentation is implementation evidence, not Arvectum OS normative authority. Exact account tariff, enabled features, field schemas, pipelines, permissions, limits and webhook availability MUST be discovered before real reliance.

## 4. Shared INT-B2 boundary and non-shared CRM semantics

Both designs use the same **governance envelope** from INT-B2:

- connector identity/version;
- external endpoint/account identity;
- external authority declaration;
- explicit operation/effect contracts;
- indirect credential references;
- Organization scope;
- authentication/authorization/Organizational Authority/Data Governance separation;
- duplicates/retry/replay/uncertainty/reconciliation;
- source occurrence vs canonical Event admission;
- provenance;
- disable/upgrade/termination.

The following are **not shared by INT-B4**:

- pipeline/category/stage semantics;
- custom field taxonomies;
- lead/deal/contact/company equivalence rules;
- task meanings and completion semantics;
- responsible-user semantics beyond source attribution;
- sales automation, robots, digital-pipeline rules or CRM-specific workflows;
- customer-specific mappings;
- write-side behavior.

## 5. Design A — Битрикс24

### 5.1 Reference profile

Design identifier:

`bitrix24_crm_attention_read_v1`

| Property | INT-B4 disposition |
|---|---|
| External system | one concrete Битрикс24 portal |
| Integration surface | official REST API |
| Authentication | dedicated integration context using OAuth 2.0 or an incoming webhook bound to a dedicated least-privilege user; exact mechanism selected per deployment |
| Initial access | read-only CRM/task projection |
| External authority | bound Битрикс24 portal remains authoritative for declared CRM/task data |
| Arvectum authority mode | `External Reference` first |
| Organization scope | exactly one Arvectum OS Organization per endpoint binding |
| Change signals | polling and/or supported event/webhook mechanisms after concrete discovery |

The design does not assume direct database access, Bitrix internal tables, PHP/internal module imports or undocumented endpoints.

### 5.2 Bounded outcome

Workspace may surface, where enabled and permitted:

- selected deal identity/reference;
- deal title;
- pipeline/category identity;
- stage identity;
- responsible-user reference;
- amount/currency only where needed and permitted;
- selected contact/company references needed for context;
- task identity/status/deadline where used for attention;
- source update/freshness evidence;
- navigable reference back to the authoritative portal object where supported.

Workspace attention labels are Arvectum/product interpretation unless the label is a direct authoritative source field. They MUST NOT be represented as native Bitrix24 truth merely because they were derived from Bitrix24 data.

### 5.3 Initial operation contracts

First allowed operation identifiers:

- `portal.identity.get` — establish the bound portal/user context;
- `crm.deals.list` — bounded deal list retrieval;
- `crm.deals.get` — one deal retrieval;
- `crm.contacts.get` — one contact retrieval where required;
- `crm.companies.get` — one company retrieval where required;
- `tasks.list` / deployment-mapped task read operation where applicable;
- `events.subscription.inspect` — inspect configured event/subscription state where supported by the selected integration mechanism.

All first-scope business operations are `read_from_external` / `read_only`.

Explicitly excluded:

- deal/contact/company create/update/delete;
- stage transition;
- task creation/completion/modification;
- automation/robot modification;
- arbitrary generic REST method passthrough;
- acting with administrator rights merely for integration convenience.

### 5.4 Identity and security

Bitrix24 deal/contact/company/task IDs are external identifiers within the bound portal namespace. They MUST NOT automatically become Arvectum Subject Identities.

The concrete binding MUST preserve:

```text
external_system = bound Bitrix24 portal
external_namespace = portal identity/domain binding
external_object_type = vendor entity type
external_object_id = vendor entity ID
```

Because REST calls execute in a concrete user context, the dedicated integration user/account is security-significant. Its technical API permission does not establish Organizational Authority for consequential business actions.

Incoming webhook secrets or OAuth tokens MUST be held through a secret reference, not canonical payload/history or logs.

### 5.5 Freshness and events

The adapter MUST expose:

- retrieval timestamp;
- source update timestamp where supplied and reliable for the relevant entity;
- pagination/incomplete state;
- last successful synchronization/check state;
- stale/unavailable state.

Webhook/event notification is a source occurrence, not automatically a canonical Arvectum Event. Duplicate/late/out-of-order signals are handled through INT-B2/RFC-0006 rules.

## 6. Design B — amoCRM

### 6.1 Reference profile

Design identifier:

`amocrm_attention_read_v1`

| Property | INT-B4 disposition |
|---|---|
| External system | one concrete amoCRM account/subdomain |
| Integration surface | official API v4 |
| Authentication | registered OAuth 2.0 integration with bounded scopes/rights |
| Initial access | read-only deals/contacts/companies/tasks projection |
| External authority | bound amoCRM account remains authoritative |
| Arvectum authority mode | `External Reference` first |
| Organization scope | exactly one Arvectum OS Organization per endpoint binding |
| Change signals | API v4 webhooks for explicitly selected event types where operationally justified |

Legacy API-key authentication is not part of the design.

### 6.2 Bounded outcome

Workspace may surface, where permitted:

- deal/lead identity/reference;
- pipeline identity;
- status/stage identity;
- responsible user reference;
- selected contact/company references;
- task identity, completion state and deadline;
- source timestamps/freshness evidence;
- selected commercial value only where needed and permitted;
- navigable source reference where available.

Custom fields remain account-specific. INT-B4 does not create canonical cross-customer names or meanings for them.

### 6.3 Initial operation contracts

First allowed operation identifiers:

- `account.identity.get`;
- `crm.leads.list`;
- `crm.leads.get`;
- `crm.contacts.get`;
- `crm.companies.get`;
- `crm.tasks.list`;
- `crm.tasks.get`;
- `webhooks.list`;
- `webhooks.subscribe` / `webhooks.unsubscribe` only as explicit `manage_subscription` administrative operations when the concrete deployment approves them.

Business-object operations are initially `read_from_external` / `read_only`.

Webhook subscription changes are not ordinary reads: they are administrative external mutations and MUST be separately authorized, attributable and reversible through explicit unsubscribe/disable behavior.

Explicitly excluded:

- lead/contact/company/task creation or editing;
- pipeline/status changes;
- task completion;
- digital-pipeline automation mutation;
- arbitrary API passthrough;
- file scopes unless a later concrete outcome requires them.

### 6.4 Identity and OAuth security

amoCRM entity IDs are external identifiers within the bound account/subdomain namespace. They MUST NOT automatically become Arvectum Subject Identities.

The binding MUST preserve:

```text
external_system = bound amoCRM account
external_namespace = account/subdomain identity
external_object_type = vendor entity type
external_object_id = API v4 entity ID
```

OAuth client secrets, access tokens and refresh tokens are reusable secrets and MUST remain outside ordinary canonical payload/history, prompts and logs.

OAuth scope availability does not itself create Organizational Authority or permission to perform every technically reachable business effect.

### 6.5 Webhook semantics

A configured amoCRM webhook MUST record:

- destination binding;
- subscribed event types;
- account scope;
- connector version;
- authorization/administrative actor for subscription change;
- enable/disable state;
- termination/unsubscribe behavior.

Incoming webhook deliveries are transport/source occurrences. They MAY trigger bounded refresh/reconciliation, but do not become canonical Events solely on receipt.

## 7. Comparison without premature unification

| Concern | Битрикс24 | amoCRM | INT-B4 shared? |
|---|---|---|---|
| External authority | portal/account | account | yes, only authority-envelope semantics |
| Authentication | incoming webhook or OAuth; calls in user context | OAuth 2.0 integration | no shared credential mechanism |
| CRM read API | REST methods | API v4 resources | no shared wire/API surface |
| Change notification | deployment-supported event/webhook mechanisms | API v4 webhooks | only source-occurrence governance is shared |
| Pipeline/stage semantics | Bitrix24-specific category/stage model | amoCRM-specific pipeline/status model | **no** |
| Custom fields | portal-specific | account-specific | **no** |
| Tasks | Bitrix24-specific task model | amoCRM task API/model | **no** |
| Write operations | technically available, excluded initially | technically available, excluded initially | only effect-governance pattern shared |

A future shared CRM semantic abstraction requires evidence from real product use demonstrating materially equivalent organizational semantics and a governed promotion decision. INT-B4 provides no such evidence yet.

## 8. Product Contract boundary

No Product Contract is required merely to retain these design artifacts.

Before a product relies on shared Arvectum connector behavior, canonical platform state/history or platform Event/execution semantics through either CRM connector, the Product Contract MUST declare at minimum:

- exact connector/version and endpoint binding;
- exact operations relied upon;
- authority/source scope;
- source object classes and mappings;
- Organization scope;
- data-purpose/classification/retention constraints;
- freshness and incomplete/stale behavior;
- event/webhook duplicate/gap/replay assumptions where relevant;
- failure/degraded mode;
- termination/migration behavior;
- prohibition or governed admission of external writes/effects.

Product-specific lead scoring, supplier/customer qualification, sales policy, approval thresholds and attention prioritization remain product-owned.

## 9. Write-side admission rule

A later CRM write operation is not automatically admitted because it appears low-risk.

Before any write-side operation is implemented for governed reliance, the concrete design MUST add:

1. exact operation identifier/version;
2. external mutation/effect classification;
3. authorization and Organizational Authority requirement;
4. Data Governance purpose;
5. idempotency/duplicate strategy;
6. uncertain-outcome and reconciliation behavior;
7. compensation/reversal semantics where actually supported;
8. evidence/provenance requirements;
9. applicable Product Contract declaration;
10. INT-B6 security/reliability review disposition.

Historical replay MUST NOT repeat a CRM mutation without a new authorized Governed Execution.

## 10. Failure, disable and termination

For both connectors:

- authentication failure → connector unavailable; no silent privilege escalation or alternate broad credential;
- authorization failure → operation refused;
- portal/account unavailable → stale/unavailable state exposed explicitly;
- incomplete pagination → partial state MUST NOT be represented as a complete authoritative population;
- webhook gap/uncertainty → reconcile from authoritative REST/API source where feasible;
- connector disable → stop retrieval/subscriptions as declared while preserving lawful historical attribution;
- credential revocation → disable access without deleting historical identity/provenance references;
- termination → revoke secrets/tokens, unsubscribe callbacks where applicable, remove non-authoritative caches/projections under retention rules, preserve lawful canonical evidence, leave authoritative CRM data untouched.

## 11. ADR trigger analysis

INT-B4 does not require a new ADR because it selects only vendor-specific APIs for vendor-specific adapters and creates no durable cross-product runtime/topology.

An ADR becomes necessary before choosing a materially shared constraint such as:

- one common connector worker/runtime;
- one mandatory OAuth/token persistence technology;
- one common webhook ingress topology;
- one shared queue/outbox/inbox mechanism;
- one common CRM DTO/wire contract across products;
- a generic CRM connector SDK or public extension surface.

## 12. Implementation admission gates

INT-B4 authorizes design, not real connector rollout.

Before a material real connector implementation enters governed use for either CRM:

1. exact portal/account is selected;
2. exact account capabilities/tariff/permissions and API surface are discovered;
3. bounded organizational outcome is confirmed;
4. data rights/purpose/classification are established;
5. dedicated least-privilege integration identity/integration is configured;
6. Product Contract exists where RFC-0004 requires it;
7. real operations and event/subscription scope are pinned;
8. failure/reconciliation/termination are tested;
9. any materially constraining shared technology has an ADR if required;
10. `INT-B6 — Integration security/reliability review` passes before material real connector effects/reliance.

## 13. Exit criteria and result

INT-B4 exit criteria are satisfied:

- [x] one concrete Bitrix24 portal design defined;
- [x] one concrete amoCRM account design defined;
- [x] each preserves external authority;
- [x] vendor-specific authentication differences preserved;
- [x] external identity mapping defined;
- [x] initial operations enumerated and bounded;
- [x] first business-object scope is read-only;
- [x] webhook/source-occurrence semantics defined;
- [x] credentials/secrets handled by reference;
- [x] Product Contract boundary defined;
- [x] write-side admission rule defined;
- [x] failure/termination behavior defined;
- [x] ADR triggers defined;
- [x] no universal CRM schema/connector/platform capability inferred.

**Result:** `INT-B4 — Complete / concrete integration design baseline`.

No generic CRM capability, Stable Product Contract, public connector API/SDK, customer Production scope or write-side authorization is created.

The next Lane-B action is `INT-B5 — СЭД/ECM/ЭДО design`, which must begin from actual named deployment/provider profiles and preserve document/signature/retention authority.
