# P8.00-A1 — External-Demand Evidence Inventory

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A1 — External-demand evidence inventory`
Parent: [`P8.00 — Phase 8 Activation / External-Ecosystem Boundary Revalidation`](../roadmap/P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — a concrete evidence-backed external-demand candidate register exists and is sufficient to proceed to P8.00-A2.**

P8.00-A1 inventories current external ecosystem pressure only. It does **not**:

- shortlist or rank candidates;
- select the Phase 8 activation outcome;
- decide that any product-local connector belongs in Arvectum OS;
- activate Phase 8;
- create or stabilize a public API, protocol, connector contract or Product Contract;
- promote any Platform Capability or Product Contract lifecycle;
- establish external/customer Production, SLA/support, compatibility, certification or commercial commitments;
- invent demand, customer identities, legal rights or value metrics that are not evidenced.

Those decisions remain later P8.00 work, especially A2–A8.

## 2. Canonical authority checked

P8.00-A1 was checked against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. `docs/rfc/README.md` — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with recorded approval evidence;
3. RFC-0001 — external authority modes, no competing source of truth, product/platform boundary, Product Contract rules, proportionality, cross-Organization controls and lifecycle/commercial integrity;
4. RFC-0002 — stable identities, immutable versions, external identifiers as aliases/references and technology-independent metamodel semantics;
5. RFC-0003 — separation of Identity, Authentication, Authorization, Organizational Authority and Data Governance; deny-by-default cross-Organization behavior; minimization, secret handling, portability and rights boundaries;
6. RFC-0004 — explicit Product Contract before governed platform reliance and prohibition of hidden product/platform coupling;
7. RFC-0005 — governed side-effect, authority, idempotency, uncertainty and reconciliation semantics;
8. RFC-0006 — external Event/provenance authority, duplicate/replay safety and failure-closed evidence semantics;
9. RFC-0008 — external Document/Artifact authority, exact-version reliance and provenance/handling constraints;
10. `docs/adrs/README.md` and current `docs/adrs/` contents — no Accepted ADR currently selects a permanent external connector, public API/wire format, external trust protocol, broker or external deployment topology;
11. the canonical master roadmap and the P8.00/Phase 8 detailed plans;
12. the P6.02 Tender Operator and P6.06 Discount Parser Provisional Product Contracts and their real-use evidence.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was identified. No new RFC or ADR is required merely to record this inventory.

## 3. Evidence rules used for A1

Only evidence already present in canonical Arvectum OS records or the current product repositories was admitted.

For each candidate, A1 records only:

- the external system/source currently evidenced by name;
- the real business or operational outcome currently exercised;
- the existing manual or product-local integration path;
- observed or already exercised risk/pressure without fabricated severity or cost;
- rights, legal, contractual, classification and secret constraints actually known at this stage;
- the authoritative-source disposition supported by existing contracts/evidence.

Unknown rights, value, maturity or external-Organization identity remain explicitly unknown. A1 does not convert a design risk into an observed incident and does not convert an existing product-local integration into platform responsibility.

## 4. Candidate register

### A1-C01 — ЕИС / zakupki.gov.ru authoritative tender-document source

**Candidate class:** external authoritative system / government procurement system.

**Named external system:** ЕИС / `zakupki.gov.ru`.

**Current real outcome:** Tender Operator can retrieve the exact documentation package for a real 44-ФЗ notice in read-only mode and use exact source documents as inputs to the bounded governed tender workflow.

**Current integration path:** product-owned Tender Operator discovery/intake path, including read-only EIS search and `getDocsIP` / `getDocsByReestrNumber` retrieval. The real P6.05-L7 attempt #2 retrieved notice `0344100006426000005`, downloaded the archive and independently verified all `7/7` required documents. No EIS/ETP mutation, platform submission, email or digital-signature action occurred.

**Observed pain/risk/duplication evidence:**

- the first real evidence attempt failed closed on EIS TLS trust;
- attempt #2 required owner-operated trust remediation while preserving certificate verification and read-only behavior;
- exact attachment identity/version/provenance matters to later governed reliance;
- the external system remains outside Arvectum OS availability and control.

No A1 evidence establishes a quantified reliability cost, SLA requirement or need to centralize the EIS connector in the platform.

**Known rights/data constraints:**

- the retrieval path may involve an individual-person token and external credentials, which remain secret and outside canonical evidence;
- real partner/customer tender data remains subject to the existing product-local handling/export restrictions;
- no canonical Phase 8 record currently establishes broader contractual/legal rights for external mutation, redistribution, cross-Organization reuse or customer-facing service commitments.

**Authority disposition:** `External Reference` is the current default for EIS procurement registry facts and source documents. ЕИС remains authoritative for the retrieved registry/document source scope. Arvectum OS may govern exact identity/version/reference/provenance used by an execution but must not become a competing factual authority.

**Evidence references:**

- `docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`;
- `docs/reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md`;
- `docs/reviews/P6-05-L7-attempt-2-real-exact-attachment-live-run.md`;
- current product repository `arvectum/tender-agent` (`README.md`).

**A1 disposition:** `ELIGIBLE_FOR_A2` — concrete current external-system evidence exists. No platform-responsibility conclusion is made here.

### A1-C02 — Telegram controlled publication effect boundary

**Candidate class:** external system / consequential external effect target.

**Named external system:** Telegram.

**Current real outcome:** Discount Parser can execute one explicitly authorized controlled publication and later reconstruct the confirmed external effect without replaying it.

**Current integration path:** product-owned Discount Parser Telegram publisher and publication ledger. In the real P6.07 Stage 2B execution, one eligible text-only Offer was published to `@arvectumtest` under separate one-time human authorization; the product created a durable pre-send `pending` publication record, performed exactly one `send_message`, received Telegram message id `27`, and the operator visually confirmed the message. Stage 2C later reconstructed the outcome through CAP-004 with zero Telegram/effect replay.

**Observed pain/risk/duplication evidence:**

- duplicate/idempotency protection is materially required before the external effect;
- external-effect uncertainty and reconciliation are explicit governed concerns;
- public-channel publication is a bounded communications/reputation consequence;
- the real run itself completed with no retry and `reconciliation required = NO`, so A1 does not claim an observed Telegram failure.

No A1 evidence establishes a need for a generic platform Telegram/notification capability.

**Known rights/data constraints:**

- Telegram bot/channel credentials are reusable secrets and remain outside canonical history;
- Product Contract possession is not authorization; the real effect used separate explicit human authorization;
- the evidenced target is a controlled test channel, not a customer Production commitment;
- no canonical evidence grants broader cross-Organization publication rights or support/SLA obligations.

**Authority disposition:** Telegram remains authoritative for external message existence and the Telegram message identifier. The Arvectum OS evidence records what the governed execution attempted/observed; it does not convert Telegram state into `Native` business truth.

**Evidence references:**

- `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`;
- `docs/roadmap/PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md`;
- current product repository `arvectum/discount-parser`, `README.md` blob `7580d8112918c0be3381ff0073b7a481fa388434`.

**A1 disposition:** `ELIGIBLE_FOR_A2` — concrete real external-effect evidence exists. Product-owned Telegram behavior remains product-local unless a later platform-necessity decision proves otherwise.

### A1-C03 — Discount Parser public discount/promo source set

**Candidate class:** external authoritative source set.

**Named current source adapters:** `promokood`, `promokodik`, `berikod`, `promokodi_net_ru`, `promko`.

These names are recorded as current product source/adapter identities. A1 does not infer a legal entity, contract party or broader platform identity from an adapter token alone.

**Current real outcome:** Discount Parser collects externally observed discount/promo source data, then performs product-owned normalization, cross-source deduplication, classification, lifecycle handling and publication eligibility processing.

**Current integration path:** product-local Source SDK/adapters with HTTP retries/backoff and source/row failure isolation. Normalization, deduplication, classification and source semantics remain entirely product-owned.

**Observed pain/risk/duplication evidence:**

- the product already carries explicit retry/backoff and source/row failure-isolation behavior for external source availability/failure;
- cross-source duplicate observations are handled by product-owned deduplication;
- external source occurrence/content must remain distinguishable from product-derived normalized Offer state.

A1 found no canonical evidence quantifying source drift cost, outage rate or duplicate engineering cost, and no evidence that these adapters should become a shared Platform Capability.

**Known rights/data constraints:**

- P6.06 treats the underlying inputs as externally observed public-source data;
- exact source-specific terms of use, redistribution rights, retention limits and a Phase 8 contractual basis are not canonically recorded in the A1 evidence reviewed;
- unresolved rights must therefore remain unresolved and deny broader Phase 8 use by default until later mapping establishes a permitted purpose/scope.

**Authority disposition:** the originating public website/channel remains the external authority for the underlying observed occurrence/content within the retrieval scope. Product normalization, deduplication, classification and publication eligibility remain product-owned local state and do not become platform authority.

**Evidence references:**

- `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`;
- current `arvectum/discount-parser` `README.md` blob `7580d8112918c0be3381ff0073b7a481fa388434`.

**A1 disposition:** `ELIGIBLE_FOR_A2_WITH_RIGHTS_GAP` — concrete current external-source evidence exists, but source-specific rights/contract details are not yet canonically established.

## 5. Evidence leads that are not yet named A1 candidates

### A1-L01 — Real Tender Operator partner/customer Organization

Canonical P6 evidence proves that the Tender Operator operating contour handles real partner data under local controlled-runtime, export/redaction and manual-delivery constraints. However, the A1 evidence reviewed does not name the external partner/customer Organization or establish a Phase 8 cross-Organization trust/data-rights contract.

Therefore A1 records this as an **evidence lead**, not as a named activation candidate. A2 must not pretend that a second Organization is available for scoring until the actual Organization identity and usable rights/constraints are established.

### A1-L02 — Supplier-origin TKP/quote source

P6.02 establishes supplier/partner-origin quote documents as external-authoritative source material, but no specific supplier external party is named in the A1 evidence reviewed. This remains a source class/evidence lead rather than a named Phase 8 candidate.

## 6. Candidate classes with no current named evidence

### Partner/customer Organization

No named second Organization with an explicit Phase 8 reliance and cross-Organization rights basis was found in the canonical P6/P7/P8 evidence reviewed for A1. Existing partner-data handling is real evidence but is identity-opaque at the Arvectum OS canonical level.

### Portability/handover recipient

No concrete external portability, migration or handover recipient is named in the current canonical evidence reviewed for A1. M7 portability/recovery proofs are owner-operated/internal and do not create an external recipient by implication.

### Separately maintained external product/extension

Tender Operator and Discount Parser are real separately maintained products and useful evidence providers, but their existing M6/M7 Arvectum OS reliance is already part of the owner-operated internal validation baseline. A1 found no separate external product/extension consumer beyond that baseline that should be presented as new Phase 8 demand.

These absence findings are important evidence. Phase 8 must not manufacture a customer, recipient or external consumer merely to exercise every candidate class.

## 7. Cross-review

A functional cross-review was applied to the A1 register before closure.

### Iteration 1 — platform / architecture

**Finding:** the initial evidence could be misread as justification to move the EIS, Telegram or discount-source connectors into Arvectum OS.

**Revision:** every candidate now explicitly separates the current product-local connector path from the external authority/effect boundary and states that platform responsibility remains undecided until A5.

**Result:** no material platform/domain leakage remains.

### Iteration 2 — security / authority / data governance

**Finding:** real external use must not imply rights that are only technically possible, especially for Telegram credentials, public-source data and partner/customer data.

**Revision:** unknown rights remain explicit; secrets are excluded; Product Contract possession is not authorization; partner/customer Organization identity remains unresolved rather than inferred; broader use stays deny-by-default.

**Result:** no material authority or rights overclaim remains.

### Iteration 3 — product / operations / evidence integrity

**Finding:** design pressure must not be reported as an observed failure or quantified business pain without evidence.

**Revision:** EIS TLS is the only specifically recorded failed attempt; the real Telegram run is recorded as successful with no retry/reconciliation; source failure/duplicate concerns are tied only to implemented retry/failure-isolation/dedup controls; no invented cost, demand, SLA or value metric is included.

**Result:** `PASS`; further changes would be editorial rather than material.

This functional cross-review is not formal owner approval, lifecycle promotion, Phase 8 activation or operational-readiness approval.

## 8. A1 closure and handoff

P8.00-A1 exit criteria are satisfied:

- a concrete candidate register exists;
- every admitted candidate has evidence references;
- external authority is preserved;
- known versus unknown rights are explicit;
- product-local integration paths are not silently platformized;
- no demand, customer, SLA or value metric is invented.

The register contains three evidence-backed candidates for A2 evaluation:

1. `A1-C01` — ЕИС / `zakupki.gov.ru` authoritative tender-document boundary;
2. `A1-C02` — Telegram controlled external publication effect boundary;
3. `A1-C03` — Discount Parser public discount/promo source set, with an unresolved rights gap.

No ranking or shortlist decision is made by A1. The correct next canonical action is:

> **P8.00-A2 — Candidate triage and value test.**

Phase 8 remains `Draft / Exploratory`; P8.01 is not authorized; no Product Contract, Platform Capability, ADR, Production or commercial status changes through this A1 closure.