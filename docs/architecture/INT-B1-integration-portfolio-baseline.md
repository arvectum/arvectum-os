# INT-B1 — Integration Portfolio Baseline

Status: `Complete / planning baseline`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `product_specific` boundaries
Roadmap lane: `Lane B — Russian-market integrations`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](../roadmap/ROADMAP.md)

## 1. Purpose

INT-B1 establishes the ranked integration portfolio used to sequence design work for common Russian enterprise systems.

It is a planning and architecture-baseline artifact. It does **not**:

- activate a Platform Capability;
- create a generic connector marketplace or broad adapter framework;
- create a public/stable API, SDK, manifest or wire protocol;
- approve a real connector implementation;
- create a Stable Product Contract;
- establish customer Production, SLA/support, certification or commercial compatibility promises;
- make Arvectum OS the primary system of record for external business data.

The exit criterion is a ranked candidate register with a concrete organizational outcome, external authority owner, read/effect boundary, credential model, reversibility and Product Contract/platform-need disposition.

## 2. Canonical basis

This baseline was checked against:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- `PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md` `1.2.1`;
- `PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md` `1.0.0`;
- canonical roadmap `2.88.0` at task start.

The most important constraints are:

1. external systems may remain authoritative through `External Reference` or `Governed Replica`; Arvectum OS must not create a competing source of truth;
2. Authentication, Authorization, Organizational Authority and Data Governance remain distinct;
3. consequential external effects require Governed Execution and explicit uncertainty/reconciliation semantics;
4. product/platform reliance requires an RFC-0004 Product Contract;
5. source occurrences, webhooks and transport receipts do not automatically become canonical Events;
6. product business schemas and workflows stay product-owned by default;
7. the existing Platform Capability Catalog explicitly leaves a generic connector marketplace / broad adapter framework `Deferred / not admitted`.

No conflict with higher-authority canonical sources was found.

## 3. Ranking method

The ranking is a planning judgment, not a market-share claim.

Candidates are ordered using five factors:

- **organizational leverage** — ability to keep employees in familiar operational systems while Arvectum OS provides governed intelligence and coordination above them;
- **Russian-market relevance** — expected frequency in target organizations;
- **near-term product pull** — usefulness to current or plausible Arvectum products/workflows;
- **integration feasibility** — existence of supported external integration mechanisms without database/private-interface coupling;
- **governance/consequence cost** — legal, financial, signature, authority and irreversible-effect risk.

A high rank means “design earlier”, not “platformize earlier”.

## 4. Ranked candidate register

| Rank | Candidate | First bounded organizational outcome | Authority / initial mode | Initial data/effect boundary | Credential model | Reversibility | Product Contract / platform disposition |
|---:|---|---|---|---|---|---|---|
| **1** | **1С:Предприятие 8 — one concrete configuration** | Surface selected authoritative business records/status in Arvectum Workspace and allow a governed workflow to reconcile work against them without replacing 1С | 1С remains authoritative; `External Reference` first, `Governed Replica` only where freshness/offline/reconstruction needs justify it | Start read-oriented: selected master/transaction/status data. Any create/update/posting effect is separately admitted and executed only through explicit governed operation | Dedicated least-privilege service/integration identity; reusable secrets remain outside canonical state and are referenced indirectly | High for read-only/reference; write effects require compensation/reconciliation, not assumed rollback | **INT-B3 first concrete design.** Adapter remains system/configuration-specific. Product Contract required before any product relies on shared platform state/history/capability through it. No universal 1С schema admitted |
| **2** | **Битрикс24 — one concrete portal** | Bring CRM/task attention and selected records into governed Workspace projections while preserving employee work in Битрикс24; later allow explicitly approved bounded actions back into the portal | Битрикс24 remains authoritative for selected CRM/tasks; `External Reference` or bounded `Governed Replica` | Read selected CRM/tasks/users + receive source occurrences; write-side methods only after explicit operation contract and authority check | OAuth/local integration/webhook credential as supported by deployment; scope to minimum modules/operations; secret only by reference | High for projections/subscriptions; consequential CRM mutation requires idempotency/reconciliation | **INT-B4 separate CRM design.** Product-specific pipeline semantics remain external/product-owned. No generic CRM canonical schema admitted |
| **3** | **amoCRM — one concrete account** | Surface deal/customer/task state and attention signals while sales staff continue normal work in amoCRM; later execute narrowly authorized CRM updates | amoCRM remains authoritative; `External Reference` or bounded `Governed Replica` | Read deals/contacts/companies/tasks + source webhook occurrences; writes limited to explicitly declared operations | OAuth integration token flow / account integration credentials; least privilege and revocation path required; secrets outside canonical state | High for read/projection; write uncertainty handled through idempotency/reconciliation rather than assumed transaction rollback | **INT-B4 separate CRM design.** Shared abstraction with Битрикс24 is forbidden until real materially similar reuse evidence exists |
| **4** | **СЭД / ECM / АСУД — actual deployed system (e.g. Directum RX, Docsvision, ТЕЗИС)** | Surface document/card/version/workflow status and governed references in Workspace without moving legal/document authority out of the deployed СЭД | External СЭД remains authoritative for document/card/workflow scope; usually `External Reference`, selectively `Governed Replica` only with explicit need | Read metadata, versions, attachments and workflow status first. Registration, approval, routing or document mutation are separate consequential effects | Deployment-specific integration/service identity; exact method and scopes must be proven from the real deployment | Medium-high for references; low for registration/signature/workflow effects unless compensation exists | **INT-B5 only after a real deployment is selected.** Document types, routing and approval semantics remain product/customer-owned; RFC-0008 governs document/artifact mapping |
| **5** | **ЭДО / electronic-signature contour — actual provider/deployment (Диадок, Saby/СБИС, 1С-ЭДО or other)** | Show authoritative exchange/signature/status evidence alongside governed work, initially without letting Arvectum OS sign or send legally consequential documents | Provider/organization signing contour remains authoritative; `External Reference` first | Read document/status/signature-verification evidence first. Send/sign/reject/cancel effects are high-consequence and deferred to separately governed workflows | Provider-specific service/account credentials plus signature/key contour kept outside Arvectum OS canonical payloads; no secret/private-key copying for convenience | High for read-only evidence; low for legal send/sign effects, which may be irreversible externally | Keep provider-specific. Product Contract required for governed reliance. No “universal e-sign authority” abstraction. Requires security/legal/authority review before effects |
| **6** | **ЕИС / regulated procurement sources — concrete bounded interface** | Let procurement products correlate tender notices/status/evidence with internal governed work while ЕИС remains authoritative | ЕИС remains authoritative; primarily `External Reference` / governed imported observation where lawful | Read/public or authorized retrieval first; no assumption of write capability or legal action authority | Interface-specific credentials if required; purpose/data-right scope explicit | High for read-only retrieval; any future regulated submission/effect would be a separate high-consequence design | Primarily **product-specific** for Tender/Procurement domain. Platform may supply only domain-neutral authority/provenance/execution envelope via Product Contract |
| **7** | **ITSM / service-management deployment (e.g. Naumen-class systems)** | Surface incidents/requests/changes requiring cross-functional attention and correlate them with governed operational work | External ITSM remains authoritative for tickets/change records | Read ticket/change state first; write/transition only if a concrete operational workflow requires it | Deployment-specific service identity / API credential reference | High for projections; medium for workflow transitions | Portfolio watchlist until real customer/product pull exists. Do not admit generic ticket schema as platform responsibility |
| **8** | **Corporate directory / IAM deployment** | Resolve externally managed identities/groups for authentication or governed reference without redefining Organizational Authority | External directory/IdP remains authority for declared identity/authentication assertions; Arvectum OS retains its own governed authorization/authority semantics | Identity resolution/authentication assertions only within RFC-0003 boundaries; no automatic role/authority import | Protocol/provider-specific trust and client credentials; secrets/keys managed outside ordinary canonical payload | Medium; disabling trust/binding must preserve historical attribution | Security-critical integration class, but not first Lane-B connector. Concrete IAM/PDP/PEP technology remains implementation/ADR scope, not new capability by default |
| **9** | **Banking / treasury integration — concrete bank/accounting contour** | Reconcile payment status or prepare a proposed payment action without granting autonomous financial authority | Bank/ERP remains authoritative for account/payment execution | Read balance/status/reference data first. Payment creation/signing/sending is consequential and excluded from baseline implementation | Bank-specific machine credential/signature contour; strong segregation and key handling | High for read-only; low for payment effects | Defer until concrete product/customer outcome and authority policy exist. Requires Product Contract + Governed Execution + dedicated security/authority review |

## 5. Immediate portfolio disposition

### 5.1 Priority A — design now

1. **1С** — first concrete design target (`INT-B3`).
2. **Битрикс24** — separate CRM design (`INT-B4`).
3. **amoCRM** — separate CRM design (`INT-B4`).

These have strong value for the product strategy of placing a governed intelligence layer above existing employee-facing systems rather than forcing replacement of familiar interfaces.

### 5.2 Priority B — design after a real deployment/outcome is selected

4. **СЭД / ECM / АСУД** — one actual system/deployment only (`INT-B5`).
5. **ЭДО / signature contour** — one actual provider/deployment with explicit document/signature authority and rights.
6. **ЕИС / regulated procurement source** — only for a concrete Tender/Procurement product outcome.

### 5.3 Priority C — portfolio watchlist

- ITSM/service management;
- corporate directory/IAM technology integrations;
- banking/treasury;
- later logistics/WMS/TMS, industry MES/SCADA, BI/DWH and other systems only when a concrete organizational outcome creates pull.

Watchlist status is not `Candidate` in the RFC-0001 Platform Capability lifecycle and creates no roadmap promise.

## 6. Platform vs product boundary

INT-B1 deliberately separates the **connector envelope** from **system/domain semantics**.

Potentially reusable, domain-neutral concerns that INT-B2 may design include:

- connector identity/version;
- external-system identity and declared authority mode;
- explicit operation/effect classification;
- credential reference (never secret payload as canonical convenience data);
- Organization/Actor/Authorization/Data Governance context;
- idempotency, duplicate, retry, replay, uncertainty and reconciliation behavior;
- source occurrence vs canonical Event admission;
- provenance;
- disable/revoke/upgrade/rollback/termination semantics.

The following remain system-, product- or customer-owned unless later evidence supports separate admission:

- 1С configuration schemas and posting/business rules;
- Битрикс24/amoCRM pipeline stages, sales rules and CRM-specific automation;
- СЭД document taxonomies, routing, registration and approval rules;
- ЭДО signing authority, legal workflow and provider-specific semantics;
- ЕИС procurement-domain interpretation;
- customer mappings, transformations and field-level business rules.

No new Platform Capability is admitted by INT-B1. The existing catalog’s `Generic connector marketplace / broad adaptor framework — Deferred / not admitted` disposition remains unchanged.

## 7. External authority and effect policy for later designs

Every INT-B3–INT-B5 concrete design must declare at minimum:

1. exact external deployment/configuration/account and object identities;
2. external authority scope and Arvectum OS authority mode;
3. read, write, external-effect and organizational-commitment operations separately;
4. authentication mechanism and credential reference/rotation/revocation model;
5. authorization, Organizational Authority and Data Governance checks separately;
6. freshness, late/out-of-order occurrence, duplicate and gap behavior;
7. idempotency key or equivalent duplicate-effect protection where applicable;
8. uncertain outcome and reconciliation behavior;
9. provenance and exact external source/version evidence where materially relied upon;
10. disable/termination/portability path;
11. Product Contract dependency before governed platform reliance;
12. ADR trigger analysis before selecting a durable shared transport/protocol/runtime boundary.

Historical replay must not repeat an external effect without a new authorized Governed Execution.

## 8. Feasibility evidence captured at baseline

The baseline does not select transports, but confirms that supported integration surfaces exist for the top three systems:

- **1С:Предприятие 8** officially documents web services, HTTP services and OData integration: <https://v8.1c.ru/platforma/integraciya/> and <https://v8.1c.ru/platforma/http-servisy/>.
- **Битрикс24** officially documents REST API, incoming/outgoing webhooks, OAuth and scoped access: <https://apidocs.bitrix24.ru/>, <https://apidocs.bitrix24.ru/local-integrations/local-webhooks.html>, <https://apidocs.bitrix24.ru/settings/how-to-call-rest-api/authorization.html>.
- **amoCRM** officially documents API v4, OAuth and webhooks: <https://www.amocrm.ru/developers/content/crm_platform/api-reference>, <https://www.amocrm.ru/developers/content/crm_platform/webhooks-api>.

For СЭД/ECM/ЭДО and regulated systems, exact API/transport feasibility is intentionally deferred until a concrete deployed product/version/account is selected. INT-B1 does not infer a supported interface from a product family name alone.

## 9. Exit criteria and result

INT-B1 exit criteria are satisfied:

- [x] concrete target classes inventoried;
- [x] 1С, Битрикс24, amoCRM, СЭД/ECM/АСУД, ЭДО and regulated-system candidates represented;
- [x] candidates ranked;
- [x] bounded organizational outcome stated for each ranked candidate;
- [x] authority owner/mode stated;
- [x] initial read/effect boundary stated;
- [x] credential model stated at the correct abstraction level;
- [x] reversibility stated;
- [x] Product Contract/platform-need disposition stated;
- [x] no generic connector capability, public API or Stable contract inferred;
- [x] first design sequence preserved: `INT-B2 → INT-B3 / INT-B4 / INT-B5`.

**Result:** `INT-B1 — Complete / planning baseline`.

The next Lane-B action is **INT-B2 — Domain-neutral connector boundary pattern**. INT-B3 may follow once a concrete 1С configuration and organizational outcome are selected; INT-B4 keeps Битрикс24 and amoCRM separate until reuse evidence exists; INT-B5 starts only from a real СЭД/ECM deployment.
