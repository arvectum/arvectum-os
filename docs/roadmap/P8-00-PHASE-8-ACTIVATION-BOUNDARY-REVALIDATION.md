# P8.00 — Phase 8 Activation / External-Ecosystem Boundary Revalidation

Status: `Current / Pre-activation`
Version: `1.1.0`
Created: `2026-08-20`
Updated: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Parent: [`PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`](PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md)
Predecessor: `Phase 7 / M7 — Complete / PASS`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Purpose

P8.00 is the explicit pre-activation gate between the completed internal operating baseline and any external ecosystem reliance.

Its job is not to build an integration. Its job is to determine whether there is a concrete external outcome worth validating, whether Arvectum OS should own any part of that boundary, what Organization/authority/data-rights constraints apply, and what stronger stable/readiness commitments would be crossed if the work proceeds.

P8.00 exists so that Phase 8 is activated by real external value and bounded evidence rather than by roadmap momentum.

## 2. Starting evidence

P8.00 inherits, but does not widen, the M7 baseline:

- persistent `Persistent Internal / owner-operated` Arvectum OS runtime on the selected Mac mini;
- durable governed state with tested backup/restore and host-loss recovery;
- persistent least-privilege identity/access/secrets operations;
- operational health/observability and incident/recovery procedures;
- governed deploy/update/rollback/version/migration path;
- live private operator workspace with a real owner interaction proof;
- persistent Tender Operator and Discount Parser product reliance through Provisional Product Contracts;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`;
- no external/customer Production, Stable Product Contract, Active Platform Capability, public/stable interface, SLA/support or broad conformance claim.

## 3. Candidate classes

P8.00 may evaluate one or more candidate classes, but MUST select only an outcome with real organizational value and actual rights/constraints:

1. **External authoritative system** — ERP, CRM, 1С, government registry/system or other external system of record;
2. **External product/extension** — a separately maintained product or extension that must consume governed platform behavior through an explicit boundary;
3. **Partner/customer Organization** — a real second Organization relying on an Arvectum OS integration with explicit sovereignty, trust and data-rights constraints;
4. **Portability/handover recipient** — a real external recipient requiring governed export, migration or handover without transferring hidden authority or non-exportable secrets.

Existing product-local connectors are evidence candidates, not automatic platform responsibilities. In particular, an integration MUST remain product-local when platform ownership is not justified by reuse, governance, security, identity, provenance, interoperability or strategic necessity.

## 4. Work breakdown

### P8.00-A1 — External-demand evidence inventory

Status: `Complete / PASS`.

Evidence: [`P8-00-A1-external-demand-evidence-inventory.md`](../reviews/P8-00-A1-external-demand-evidence-inventory.md).

A1 established three current evidence-backed candidates without ranking or selecting them:

1. ЕИС / `zakupki.gov.ru` authoritative tender-document boundary;
2. Telegram controlled external publication effect boundary;
3. Discount Parser public discount/promo source set, with unresolved source-specific rights details.

A1 also records that no named second partner/customer Organization, external portability/handover recipient or new external product/extension consumer beyond the existing owner-operated M6/M7 baseline is currently evidenced. Those absences must not be filled by assumption.

The candidate register preserves external authority, distinguishes known from unresolved rights, leaves product-local connectors product-owned, and contains no invented demand/SLA/value metrics.

**Exit:** satisfied — candidate register with evidence references and no invented demand/SLA/value metrics.

### P8.00-A2 — Candidate triage and value test

Status: `Current / next`.

For each candidate, score qualitatively:

- real organizational value now;
- consequence and reversibility;
- external dependency maturity/readiness;
- authority/data-rights clarity;
- distinctness from M6/M7 internal validation;
- ability to generate reusable platform evidence;
- cost of keeping the mechanism product-local;
- risk of premature stable/public commitment.

**Exit:** shortlist of no more than three candidates, with rejected/contained candidates explicitly dispositioned.

### P8.00-A3 — Select one bounded activation outcome

Select one concrete outcome, not a generic technology goal.

The selected outcome MUST identify:

- external system/organization/product/recipient;
- exact organizational result to validate;
- why the outcome is materially external to the current owner-operated internal contour;
- what success looks like;
- what failure must do;
- explicit non-goals.

**Exit:** one selected Phase 8 validation outcome.

### P8.00-A4 — Organization / identity / authority / data-rights map

Define the minimum cross-boundary control model before any external data or authority crosses it:

- governing Organization(s);
- external identities/aliases and trust source;
- Authentication evidence required;
- Authorization owner/rules;
- Organizational Authority and approval owner;
- Data Governance purpose, classification, disclosure, retention, deletion and export constraints;
- legal/contractual rights known at this stage;
- secrets/credentials and non-exportable material;
- external authoritative source and Authority Mode (`External Reference`, `Governed Replica`, or `Native` only where justified).

**Exit:** explicit boundary map with deny-by-default unresolved cases.

### P8.00-A5 — Platform-responsibility necessity test

Answer whether the selected outcome actually belongs in Phase 8 platform work.

Platform responsibility is justified only if one or more are materially true:

- reuse across products/integrations is evidenced or strategically required;
- shared identity/security/Organization isolation is required;
- shared provenance/reconstruction/replay safety is required;
- governed portability/interoperability is required;
- hidden coupling would otherwise be created;
- constitutional/Accepted RFC invariants require platform ownership.

If a bounded product-local adapter is sufficient, Phase 8 MUST NOT absorb the business integration merely to create roadmap work.

**Exit:** `PLATFORM_REQUIRED`, `PRODUCT_LOCAL`, or `DEFER` disposition with rationale.

### P8.00-A6 — Stable/readiness/ADR gate scan

Check whether the selected outcome would materially rely on any concrete long-lived boundary:

- public/stable API or wire format;
- external authentication/trust protocol;
- multi-Organization persistence/isolation topology;
- external Event transport/broker;
- connector/plugin packaging/discovery protocol;
- durable customer-facing export/migration format;
- external Production environment;
- support/SLA/compatibility commitment.

Use the lowest sufficient decision level. A crossed threshold MUST stop at the applicable ADR/RFC/policy/Product Contract/governance decision before implementation relies on it.

**Exit:** explicit `NO-GATE` or named required governance artifacts.

### P8.00-A7 — Activation evidence and success/failure envelope

Define Phase 8 activation evidence:

- selected outcome and accountable owner;
- exact external boundary;
- initial Product Contract/integration-contract need;
- permitted data/effects;
- prohibited data/effects;
- failure-closed behavior;
- required provenance/reconstruction evidence;
- rollout/rollback/containment path;
- review cadence/trigger;
- activation success criteria;
- conditions that return the work to product-local containment or defer it.

### P8.00-A8 — Owner activation decision

A separate canonical owner decision activates Phase 8 only after A1–A7 are complete.

The decision MUST state:

- selected outcome;
- Organization/authority/data-rights scope;
- platform-responsibility rationale;
- required governance artifacts before implementation;
- Phase 8 status transition `Draft / Exploratory → Active`;
- current action `P8.01`;
- explicit non-claims.

## 5. Exit criteria

P8.00 is `Complete / PASS` only when:

1. at least one concrete external candidate has evidence;
2. one bounded activation outcome is selected;
3. Organization/identity/authority/data-rights scope is explicit;
4. platform responsibility is justified rather than assumed;
5. stable/readiness/ADR gates are dispositioned;
6. success/failure/rollback/containment criteria are explicit;
7. fresh owner activation approval is recorded canonically.

If no candidate satisfies these criteria, the correct result is `DEFER / Phase 8 remains Draft`, not artificial activation.

## 6. Current action

> **P8.00-A2 — Candidate triage and value test.**

A1 is complete. A2 must compare only the evidence-backed A1 candidates, keep unresolved rights explicit, disposition contained/rejected candidates honestly and produce a shortlist of no more than three. It must not activate Phase 8, select P8.01 implementation or promote a product-local connector merely because it already works.