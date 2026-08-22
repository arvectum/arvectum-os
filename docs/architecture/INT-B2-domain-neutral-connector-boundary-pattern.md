# INT-B2 — Domain-Neutral Connector Boundary Pattern

Status: `Complete / architecture baseline`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` boundaries
Roadmap lane: `Lane B — Russian-market integrations`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](../roadmap/ROADMAP.md)
Predecessor: [`INT-B1 — Integration Portfolio Baseline`](INT-B1-integration-portfolio-baseline.md) `1.0.0`

## 1. Purpose

INT-B2 defines the smallest domain-neutral boundary pattern that concrete Arvectum OS integrations may use without creating a speculative universal connector framework.

The pattern exists to make integrations governable, attributable, replaceable and safe across external systems while preserving system-specific and product-specific semantics outside the shared platform boundary.

It is an architecture baseline, not a public API or activated Platform Capability.

INT-B2 does **not**:

- create a generic connector marketplace, universal adapter runtime or plugin ecosystem;
- standardize one transport, protocol, SDK, deployment topology or persistence model;
- create a universal business-object schema across 1С, CRM, СЭД, ЭДО or other systems;
- make any external system subordinate to Arvectum OS authority;
- authorize a real external write/effect;
- create a Stable Product Contract;
- activate a Platform Capability;
- establish customer Production, SLA/support, certification or compatibility promises.

## 2. Canonical basis

INT-B2 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- RFC-0002 identity, Canonical Record, external identifier and authority semantics;
- RFC-0003 identity/authentication/authorization/Organizational Authority/Data Governance separation, least privilege, secret handling and portability;
- RFC-0004 Product Contract boundary and prohibition of hidden product/platform coupling;
- RFC-0005 Governed Execution, effect classification, idempotency, uncertainty, reconciliation and historical-effect rules;
- RFC-0006 Event/provenance/observability semantics, including transport receipt ≠ canonical Event and replay safety;
- `INT-B1 — Integration Portfolio Baseline` `1.0.0`;
- canonical roadmap `2.89.0` at task start.

No conflict with higher-authority canonical sources was found.

## 3. Architectural decision

Arvectum OS may standardize a **Connector Boundary Envelope** for concrete integrations.

The envelope standardizes governance semantics around an integration, not the business semantics inside the connected system.

A concrete adapter is therefore modeled as:

```text
Product / Governed Workflow
          │
          │ Product Contract where RFC-0004 requires it
          ▼
Connector Boundary Envelope
  identity + authority + operation contract
  credential reference + security context
  idempotency + uncertainty + reconciliation
  provenance + lifecycle/termination
          │
          ▼
System-specific Adapter
  1С / Битрикс24 / amoCRM / СЭД / ЭДО / ...
  system-specific API, mapping and transport
          │
          ▼
External Authoritative System
```

The envelope MUST remain domain-neutral. A concrete adapter MAY implement system-specific translation, protocol handling and object mapping behind that boundary.

## 4. Boundary object model

The pattern defines six logical boundary concepts. They are semantic concepts and do not require six physical tables, services or classes.

### 4.1 Connector Definition

A **Connector Definition** identifies one versioned adapter contract for one concrete external-system family or deployment class.

Minimum fields/semantics:

- `connector_id` — stable connector identity;
- `connector_version` — immutable version identity/reference;
- `adapter_kind` — system-specific implementation kind, e.g. `1c_enterprise_8`, `bitrix24`, `amocrm`;
- `organization_scope` — governing Organization scope;
- `external_system_class` — external system family;
- `supported_operations` — exact declared operation identifiers;
- `credential_requirement_ref` — reference to required credential class/secret binding;
- `compatibility_scope` — exact supported deployment/configuration/API assumptions where known;
- `owner` — accountable architectural/operational owner;
- `status` — lifecycle status of this concrete connector definition, without implying Platform Capability lifecycle.

`connector_id` and `connector_version` are Arvectum OS governed identities. External identifiers MUST NOT silently become those identities.

### 4.2 External Endpoint Binding

An **External Endpoint Binding** identifies the actual external account, portal, database publication endpoint, tenant, configuration or deployment reached by one connector instance.

It MUST declare:

- external system identity and namespace;
- endpoint/deployment identity sufficient to avoid accidental cross-environment use;
- Organization scope;
- declared external authority scope;
- Arvectum OS authority mode for relied-upon data: `External Reference` or `Governed Replica` unless a separately justified native object exists;
- environment/deployment label where relevant;
- freshness/retrieval/synchronization contract where relied upon;
- failure/unavailability behavior;
- termination/revocation state.

A binding MUST NOT imply that all objects exposed by the external system are permitted or authoritative for all uses.

### 4.3 Credential Binding Reference

A **Credential Binding Reference** identifies how the connector obtains authentication material without placing reusable secrets in ordinary canonical payload/history.

It MUST preserve, directly or by governed reference:

- credential binding identity;
- owning Organization and accountable operator/service;
- credential mechanism class;
- intended external endpoint binding;
- allowed operation/scope constraints where available;
- rotation/revocation path;
- expiry/freshness metadata where applicable;
- secret-store/provider reference.

Reusable secrets, private keys, passwords, refresh tokens and equivalent sensitive material MUST NOT be copied into Canonical Records, Events, prompts, logs or portability packages merely for convenience.

Possession of a valid credential proves neither authorization nor Organizational Authority.

### 4.4 Connector Operation Contract

Every supported action MUST be an explicit **Connector Operation Contract** rather than an untyped generic `execute` call.

Each operation declares:

- stable operation identifier and version;
- direction: `read_from_external`, `write_to_external`, `invoke_external_effect`, or `manage_subscription`;
- effect class aligned with RFC-0005: `read_only`, `transient`, `canonical_mutation`, `external_mutation`, `organizational_commitment` as applicable;
- input/output schema references at the connector boundary;
- external object identity rules;
- authority source and authority mode;
- authentication requirement;
- authorization requirement;
- Organizational Authority / approval requirement where consequential;
- Data Governance purpose/scope requirement;
- idempotency semantics;
- retry policy category;
- timeout/uncertainty semantics;
- reconciliation procedure/reference;
- provenance/evidence requirement;
- cancellation/compensation statement;
- Product Contract dependency where a product relies on the operation.

A concrete integration MUST NOT expose a write/effect merely because the external API technically supports it.

### 4.5 Connector Invocation

A **Connector Invocation** is one attributable attempt to perform a declared operation.

For a consequential operation it MUST execute within Governed Execution and preserve enough evidence to reconstruct:

- Organization;
- initiating Actor and actual technical integration Principal;
- effective Product Contract version where applicable;
- connector definition/version;
- endpoint binding;
- operation contract/version;
- material input record/version references;
- applicable authorization, Organizational Authority and Data Governance decisions;
- idempotency/correlation identity;
- attempt number;
- external request/reference identity where available;
- result classification;
- uncertainty/reconciliation state;
- admitted Events and provenance references where applicable.

A low-consequence read MAY use lighter operational representation where it does not create significant governed state, but it remains attributable and subject to security/data-governance controls.

### 4.6 Reconciliation Record

A **Reconciliation Record** represents the governed result of resolving an uncertain, duplicated, late, conflicting or partially completed connector operation.

It declares:

- original invocation/execution reference;
- external endpoint/object/effect reference;
- reason reconciliation was required;
- evidence consulted;
- resulting state: `confirmed_effect`, `confirmed_no_effect`, `compensated`, `superseded`, `manual_review_required`, or `unresolved`;
- actor/automation performing reconciliation;
- approval where the reconciliation itself is consequential;
- linked correction/compensation Events or new Governed Execution where applicable.

Reconciliation MUST NOT rewrite historical invocation/Event evidence.

## 5. External authority model

Every connector binding and every relied-upon external object class MUST declare its authoritative source and scope.

Default rules:

1. **External system remains authoritative.** 1С, Битрикс24, amoCRM, СЭД, ЭДО, bank, register or another external system is not displaced merely by integration.
2. **External Reference first.** Use `External Reference` where live retrieval/reference is sufficient.
3. **Governed Replica only with an explicit need.** Replication requires declared synchronization, freshness, conflict, failure, retention and portability semantics.
4. **No authority laundering.** Mapping external data into an Arvectum OS schema does not make Arvectum OS authoritative for the underlying fact.
5. **No competing writes.** If the external system owns a business fact, local editable replicas MUST NOT silently create a second authority.

External object identifiers are governed aliases/references, not automatically Arvectum OS Subject Identities.

## 6. Operation and effect classes

The connector boundary distinguishes operations before transport-specific implementation.

| Boundary class | Typical example | Governed rule |
|---|---|---|
| `read_from_external` | read 1С counterparty status | external authority preserved; provenance/freshness explicit where relied upon |
| `manage_subscription` | register or renew a webhook/subscription | administrative effect; explicit scope, revocation and duplicate handling required |
| `write_to_external` | update CRM field | explicit authorization + declared external mutation semantics; idempotency/reconciliation required |
| `invoke_external_effect` | post 1С document, send ЭДО document, trigger workflow transition | Governed Execution; Organizational Authority/approval and uncertainty handling proportionate to consequence |
| `organizational_commitment` | legally/financially consequential send/sign/payment-like action | never admitted implicitly; requires explicit workflow/authority/security/legal boundary and may remain prohibited |

A transport method such as HTTP `POST` does not determine the organizational effect class.

## 7. Idempotency, duplicates and retry

The boundary MUST NOT promise universal exactly-once execution.

For every non-read-only operation the concrete design MUST state one of:

- external system supports a stable idempotency key;
- operation is naturally idempotent under declared semantics;
- duplicate detection uses an explicit external/business key plus reconciliation;
- retry after uncertain outcome is prohibited until reconciliation;
- operation is non-repeatable and requires manual/governed resolution after uncertainty.

Rules:

- the same idempotency identity MUST NOT be reused for materially different intended effects;
- retry does not create new Organizational Authority;
- duplicate delivery of a webhook/transport occurrence does not create duplicate canonical Events or duplicate external effects by implication;
- a historical invocation or Event replay MUST NOT repeat an external effect without a new authorized Governed Execution.

## 8. Uncertainty and reconciliation state machine

A connector MUST distinguish transport failure from known business outcome.

Minimum result semantics:

```text
requested
   │
   ├──> confirmed_success
   ├──> confirmed_failure
   └──> outcome_uncertain
            │
            └──> reconciliation_required
                     │
                     ├──> confirmed_effect
                     ├──> confirmed_no_effect
                     ├──> compensated
                     ├──> manual_review_required
                     └──> unresolved
```

Timeout, connection reset or missing response MUST NOT automatically be interpreted as “no external effect”.

Where consequence is material, the system MUST pause or expose uncertainty until reconciliation is completed or an explicitly governed degraded path applies.

## 9. Source occurrences, webhooks and Events

Incoming webhook, message, callback, polling result, API response, file arrival or change-feed occurrence is initially a **source occurrence/transport receipt**, not automatically a canonical Arvectum OS Event.

Canonical Event admission requires RFC-0006-compatible validation proportionate to consequence, including where applicable:

- external source identity;
- Organization scope;
- event/occurrence schema and version;
- external object/effect identity;
- occurrence and receipt time;
- duplicate identity/detection semantics;
- provenance/integrity evidence;
- classification and data-governance checks;
- authority/source semantics;
- payload interpretability.

Late, duplicate or out-of-order delivery MUST NOT silently rewrite prior canonical history.

Operational logs, metrics and traces remain non-canonical telemetry by default.

## 10. Security and authority boundary

A connector invocation MUST keep these decisions distinct:

```text
Identity
→ Authentication
→ Authorization
→ Organizational Authority / Approval
→ Data Governance
→ Governed Execution / External Effect
```

Connector registration, possession of credentials, endpoint reachability, API permission or technical administrator status MUST NOT skip later gates.

Minimum controls:

- deny by default;
- least-privilege credential and operation scopes;
- explicit Organization scoping;
- no ambient cross-Organization credential reuse;
- secret minimization and redaction;
- attributable machine/service identities for material operations;
- failure closed where an authorization/authority/data-governance decision cannot be safely established;
- governed revocation and historical attribution preservation.

## 11. Product Contract boundary

A concrete adapter may be product-local while isolated and reversible.

A Product Contract is required before a product relies on shared Arvectum OS connector behavior, canonical platform state/history, platform Events or other governed platform capability as defined by RFC-0004.

The Product Contract MUST declare, proportionate to reliance:

- connector/operation versions relied upon;
- direction and operation/effect scope;
- canonical/external authority boundary;
- record/event/artifact dependencies;
- Organization and security scope;
- data classification/purpose/retention requirements;
- duplicate/retry/gap/ordering assumptions;
- uncertainty/reconciliation behavior;
- failure/degraded-mode behavior;
- compatibility/migration/termination expectations.

A Product Contract MUST NOT depend on private adapter tables, undocumented endpoints, internal imports, private topics, incidental logs or unversioned mappings.

## 12. System-specific and product-specific ownership

INT-B2 deliberately does **not** standardize the following:

- 1С configuration objects, registers, document posting semantics or business rules;
- Битрикс24/amoCRM pipeline stages, sales rules, automation or field mappings;
- СЭД document/card taxonomies, routing, registration and approval semantics;
- ЭДО provider legal/signature workflow and signing authority;
- ЕИС procurement-domain interpretation;
- customer-specific field mapping, transformation, normalization and validation rules;
- system-specific API pagination, rate limits, protocol quirks or transport details unless needed in the concrete adapter contract.

These remain adapter-, product- or customer-owned.

Shared abstraction between two concrete integrations requires real evidence of materially identical semantics, not just similarly named fields or HTTP mechanisms.

## 13. Connector lifecycle and termination

Connector lifecycle is implementation/governance state and MUST NOT be confused with Platform Capability lifecycle or Product Contract lifecycle.

A concrete connector definition MUST support:

- identifiable version upgrade;
- compatibility declaration;
- disable/suspend;
- credential revocation;
- endpoint rebinding under governed change;
- migration where retained references depend on the old version;
- termination;
- preservation of historical attribution after disable/termination.

Rollback means returning Arvectum OS connector implementation/configuration to a prior compatible version. It MUST NOT be described as rolling back an already committed external business effect unless the external system provides a valid compensation/reversal mechanism and a new authorized action performs it.

Termination MUST define what happens to:

- External References;
- Governed Replicas;
- retained canonical Events/evidence;
- credentials/secrets;
- subscriptions/webhooks;
- projections/caches;
- portability/export obligations.

## 14. Compatibility and versioning

Versioning is required for semantics materially relied upon by products/workflows.

A connector change is materially breaking when it changes, for example:

- operation meaning or effect class;
- external authority assumptions;
- identity mapping semantics;
- input/output schema incompatibly;
- idempotency/retry behavior;
- uncertainty/reconciliation behavior;
- security/authorization scope;
- event admission or provenance semantics;
- termination/portability obligations.

Transport/library upgrades that preserve the declared boundary semantics need not create a new public architectural contract, but still require normal engineering validation.

## 15. ADR trigger analysis

INT-B2 does not require a new ADR because it selects no durable shared implementation technology or topology.

A new or updated ADR becomes necessary before a concrete implementation makes a materially constraining shared decision such as:

- one shared connector runtime/process topology;
- a mandatory secrets manager technology;
- a mandatory integration queue/broker or CDC mechanism;
- a durable shared wire protocol/SDK surface;
- a cross-product retry/outbox/inbox persistence topology;
- a shared schema-registry technology;
- a connector deployment/isolation model that materially affects security or portability.

System-specific API choice alone normally belongs to the concrete adapter design unless it creates a durable shared architectural constraint.

## 16. Conformance checklist for INT-B3–INT-B5

Every concrete Lane-B connector design MUST answer all items below before real governed reliance:

- [ ] concrete external deployment/configuration/account identified;
- [ ] bounded organizational outcome identified;
- [ ] connector identity/version declared;
- [ ] external endpoint and object identity rules declared;
- [ ] authoritative source and authority mode declared;
- [ ] exact operations enumerated and effect-classified;
- [ ] credential reference, rotation and revocation model declared;
- [ ] Authentication, Authorization, Organizational Authority and Data Governance kept distinct;
- [ ] Organization scope and cross-organization behavior explicit;
- [ ] freshness/synchronization/retrieval semantics explicit where relied upon;
- [ ] duplicates, idempotency, retry and replay semantics explicit;
- [ ] timeout/uncertain-outcome behavior explicit;
- [ ] reconciliation path explicit;
- [ ] source-occurrence vs canonical-Event admission explicit;
- [ ] provenance/evidence requirements explicit;
- [ ] disable/upgrade/rollback/termination behavior explicit;
- [ ] Product Contract need and exact dependency disposition recorded;
- [ ] ADR trigger analysis completed;
- [ ] no product business schema/rule leaked into the domain-neutral boundary;
- [ ] no unsupported Platform Capability/public API/Production/SLA claim inferred.

## 17. Exit criteria and result

INT-B2 exit criteria are satisfied when the domain-neutral pattern covers:

- connector identity/version;
- external system/binding identity;
- authority mode;
- exact operation and effect classification;
- credential reference semantics;
- security/authority/data-governance separation;
- duplicate/idempotency/retry/replay behavior;
- uncertain outcome and reconciliation;
- source occurrence vs canonical Event admission;
- provenance/evidence;
- disable/upgrade/rollback/termination;
- Product Contract dependency boundary;
- ADR trigger conditions;
- explicit exclusion of system/product business semantics from the shared envelope.

**Result:** `INT-B2 — Complete / architecture baseline`.

No new Platform Capability, Stable Product Contract, public connector API/SDK, implementation runtime or external production commitment is created.

The next Lane-B action is `INT-B3 — 1С first-candidate design`, which must start from one concrete 1С configuration/deployment and one bounded organizational outcome rather than a universal 1С model.
