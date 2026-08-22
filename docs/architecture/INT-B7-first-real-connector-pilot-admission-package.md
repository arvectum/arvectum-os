# INT-B7 — First Real Connector Pilot Admission Package

Status: `Prepared / blocked on exact real endpoint`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance` boundaries
Roadmap lane: `Lane B — Russian-market integrations`
Parent roadmap: [`docs/roadmap/ROADMAP.md`](../roadmap/ROADMAP.md)
Predecessors:
- [`INT-B1 — Integration Portfolio Baseline`](INT-B1-integration-portfolio-baseline.md) `1.0.0`;
- [`INT-B2 — Domain-Neutral Connector Boundary Pattern`](INT-B2-domain-neutral-connector-boundary-pattern.md) `1.0.0`;
- [`INT-B3 — 1С First-Candidate Design`](INT-B3-1c-erp-first-candidate-design.md) `1.0.0`;
- [`INT-B4 — CRM Designs`](INT-B4-crm-designs.md) `1.0.0`;
- [`INT-B5 — СЭД/ECM/ЭДО Design`](INT-B5-sed-ecm-edo-design.md) `1.0.0`;
- [`INT-B6 — Integration Security / Reliability Review`](../reviews/INT-B6-integration-security-reliability-review.md) `1.0.0`.

## 1. Purpose

INT-B7 is the endpoint-specific admission package that must exist before the first material real connector enters governed reliance.

The preferred first candidate remains the INT-B3 design:

> `1С:ERP Управление предприятием 2`, family `2.5`, bounded read-only procurement projection.

However, no exact real 1С endpoint/deployment has been supplied to Arvectum OS project context as of `2026-08-22`. Therefore this package is prepared to the maximum truthful extent but **pilot admission is blocked**.

INT-B7 MUST NOT fabricate:

- a customer or ООО «Арвектум» 1С deployment;
- an OData URL;
- a platform/configuration build number;
- published metadata/entity sets;
- credentials or credential scopes;
- real procurement fields;
- network reachability;
- failure-test results;
- Product Contract reliance evidence;
- operational success evidence.

A reference design is not a live endpoint.

## 2. Canonical basis

This package is governed by:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- INT-B2 Connector Boundary Envelope;
- INT-B3 1С reference design;
- INT-B6 scoped security/reliability PASS;
- canonical roadmap `2.94.0` at task start.

No higher-authority source permits synthetic endpoint evidence.

## 3. Candidate and bounded outcome

Preferred candidate design:

`connector.1c.erp25.procurement.read / 1.0.0`

Intended bounded outcome:

> Surface selected authoritative supplier-order/status information from one exact bound 1С:ERP deployment into Arvectum Workspace so procurement work can be prioritized and reconciled while 1С remains authoritative.

Allowed first operations remain:

- `metadata.discover`;
- `procurement_orders.list`;
- `procurement_orders.get`;
- `counterparties.get`.

All are `read_from_external / read_only`.

No create/update/post/unpost/cancel/receipt/payment or arbitrary 1С method execution is admitted.

## 4. Admission evidence register

| Evidence item | Required before activation | Current state | Disposition |
|---|---:|---|---|
| Exact external system/deployment | yes | absent | `BLOCKED` |
| Exact endpoint/publication URL | yes | absent | `BLOCKED` |
| Exact 1С platform version | where material | absent | `BLOCKED` |
| Exact ERP configuration version | yes | absent | `BLOCKED` |
| Published OData metadata | yes | absent | `BLOCKED` |
| Arvectum Organization mapping | yes | can be selected only with real binding | pending |
| External authority scope | yes | design says 1С authoritative; exact object scope absent | pending |
| Bounded organizational outcome | yes | defined at design level | prepared |
| Exact read-only operation allowlist | yes | defined | prepared |
| Dedicated source integration principal | yes | absent | `BLOCKED` |
| Credential secret reference | yes | absent | `BLOCKED` |
| Source-side least-privilege evidence | yes | absent | `BLOCKED` |
| Purpose/classification/minimization | yes | generic design only | pending exact data scope |
| Retention/deletion/portability | yes | generic design only | pending exact data scope |
| API/schema compatibility evidence | yes | absent | `BLOCKED` |
| Freshness/completeness semantics | yes | design prepared | pending endpoint validation |
| Authentication failure test | yes | not executable without endpoint | `BLOCKED` |
| Authorization denial test | yes | not executable without endpoint | `BLOCKED` |
| Network timeout/unavailable test | yes | not executable without endpoint | `BLOCKED` |
| Partial pagination/incomplete-state test | yes | not executable without endpoint | `BLOCKED` |
| Schema drift/incompatibility test | yes | not executable without endpoint | `BLOCKED` |
| Credential revocation test | yes | not executable without credential | `BLOCKED` |
| Duplicate/reconciliation test | yes | design prepared | pending endpoint execution |
| Connector disable/termination test | yes | design prepared | pending endpoint execution |
| Product Contract | before governed shared/platform reliance | not created because endpoint/reliance absent | correctly pending |
| ADR disposition | before materially shared implementation constraint | no shared runtime choice made | `NO ADR CURRENTLY REQUIRED` |

## 5. Endpoint intake record

When a real endpoint becomes available, the following record MUST be completed before activation:

```yaml
external_system: 1C_ERP_2
configuration_family: "2.5"
configuration_version: <real version>
platform_version: <real version if material>
deployment_owner: <organization>
environment: <real environment>
publication_url: <real HTTPS URL or protected locator reference>
publication_identity: <real publication name/id>
organization_scope: <Arvectum Organization identity>
authority_mode: External Reference
authoritative_scope: <exact source object/data scope>
credential_binding_ref: <indirect secret reference>
credential_principal: <dedicated source identity>
allowed_operations:
  - metadata.discover
  - procurement_orders.list
  - procurement_orders.get
  - counterparties.get
```

Secrets themselves MUST NOT be entered into this document.

## 6. Data-governance intake

Before business-data retrieval, record:

- declared purpose of procurement-data use;
- exact source fields needed;
- whether personal data is present;
- whether commercial/financial confidentiality applies;
- which fields are excluded by minimization;
- retention period/policy reference for local projections/evidence;
- deletion behavior;
- portability/export behavior;
- whether any full source payload/content is retained or only selected projection fields;
- access roles/principals allowed to view the resulting Workspace projection.

No field is admitted merely because it is exposed by OData.

## 7. Compatibility discovery procedure

For the exact endpoint, INT-B7 execution MUST:

1. authenticate with the dedicated read-only integration principal;
2. retrieve publication metadata only;
3. record exact metadata/entity capability evidence without secrets;
4. verify the actual supplier-order and required counterparty object mappings;
5. verify the integration identity cannot access prohibited write operations through the admitted connector surface;
6. pin the resulting adapter mapping/configuration version;
7. classify unsupported/incompatible metadata explicitly rather than guessing names from the reference design.

A failure at discovery means `NOT ADMITTED`, not best-effort production mapping.

## 8. Required failure and reliability test matrix

The real pilot MUST produce evidence for:

| Test | Required behavior |
|---|---|
| invalid/expired credential | connector unavailable; no fallback to broad credential |
| source authorization denial | operation refused and attributable |
| network timeout/reset | unavailable/uncertain source contact, not empty authoritative result |
| source unavailable | stale/unavailable state exposed |
| interrupted pagination | result marked incomplete |
| incompatible metadata/schema | connector compatibility failure; no silent field guessing |
| duplicate retrieval | deterministic same external subject/reference |
| object disappears from list | reconciliation required; no automatic deletion of history |
| object direct lookup not-found | explicit source result with historical attribution preserved |
| credential revoked | retrieval stops; prior history remains attributable |
| connector disabled | no new source retrieval; projections marked according to freshness/disable policy |
| termination | credentials revoked, caches/projections disposed per policy, external 1С state untouched |

## 9. Product Contract gate

No Product Contract is created merely to make this package appear complete.

Before a product/Workspace feature relies on shared Arvectum connector behavior, canonical platform state/history or platform Events, the applicable RFC-0004 Product Contract MUST declare the exact:

- connector/version;
- endpoint binding;
- read operations;
- external authority scope;
- mapping/schema reliance;
- Organization scope;
- purpose/classification/retention;
- freshness/incomplete/stale behavior;
- failure/reconciliation semantics;
- migration/termination semantics.

The Product Contract cannot be completed faithfully until the real endpoint and actual reliance are known.

## 10. ADR disposition

Current disposition: `No new ADR required`.

Reason: INT-B7 preparation does not select a shared connector worker/runtime, secrets technology, queue/broker, webhook ingress, schema registry, common DTO, public SDK/API or cross-product retry topology.

If real implementation introduces such a materially constraining shared choice, ADR analysis MUST occur before that choice becomes durable.

## 11. Pilot admission decision

Current decision:

> **NOT ADMITTED — exact real endpoint/deployment and endpoint-specific evidence are absent.**

This is not a failed architecture review. It is the correct outcome of an evidence gate whose external prerequisite does not yet exist in canonical project context.

The package itself is ready for immediate completion when a real endpoint is supplied.

## 12. Lane-B internal completion state

All work that can be completed without fabricating a real external deployment is now complete:

- INT-B1 portfolio baseline — complete;
- INT-B2 connector boundary — complete;
- INT-B3 1С design — complete;
- INT-B4 CRM designs — complete;
- INT-B5 СЭД/ECM/ЭДО design — complete;
- INT-B6 security/reliability gate — complete;
- INT-B7 admission package structure, allowlist, evidence register, intake schema and test matrix — prepared;
- actual pilot activation/evidence — externally blocked on real endpoint.

No further internal design work is required merely to keep Lane B busy. The next valid Lane-B action is to populate and execute this package against an exact real endpoint.
