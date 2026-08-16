# P6.06 — Second Real Product / Workflow Product Contract Boundary

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-16`
Updated: `2026-08-16`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform` and `governance`
Roadmap work item: `P6.06 — Second real target`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone: `M6 — Platform validated through real products and reuse evidence`
Authority: RFC-0004 `1.0.0` — `Accepted`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0007 `1.0.0` — `Accepted`; RFC-0008 remains outside the required dependency surface of this contract
Product repository: `arvectum/discount-parser`

## 1. Result and purpose

P6.06 result: **PASS**.

The second materially distinct real Phase 6 target is:

> **Arvectum Discount Parser — one controlled publication workflow from externally observed discount/promo source data through product-owned normalization, deduplication, classification and publication eligibility to a manual or pre-authorized scheduled Telegram publication attempt, with governed reconstruction of the consequential external effect.**

This is materially distinct from the first Tender Operator Product Contract. P6.02 validates a bounded case/document-analysis workflow that ends in a human-reviewed artifact and keeps external actions manual. P6.06 validates a continuous/scheduled operational workflow with an actual external side effect, idempotency/duplicate-protection requirements, possible uncertain external outcome and reconciliation requirements.

The Product Contract exists before Arvectum OS governed reliance on shared platform execution/history, as required by RFC-0001 and RFC-0004.

This contract is `Provisional 0.1.0`. It is intentionally narrow and reversible. It is not:

- a Stable Product Contract;
- a public SDK/API/wire/package compatibility promise;
- a Platform Capability lifecycle promotion;
- a production-readiness, SLA or support commitment;
- a full-platform conformance claim;
- an authorization, Organizational Authority or approval grant;
- a decision to migrate the full Discount Parser database or all historical runs into Arvectum OS;
- a decision to turn Discount Parser source adapters, scheduler, Offer model, classification, deduplication, rule memory, Telegram integration or UI into Platform Capabilities.

## 2. Selection evidence and material difference

The current real product repository establishes the following implemented/product-owned contour:

- external website/Telegram-source collection;
- normalized Offer state with source observations/provenance;
- deterministic classification and deduplication;
- scheduled collection/lifecycle/publication work;
- manual preview/publish and autopost modes;
- publication eligibility filters;
- a publication ledger;
- duplicate prevention before Telegram submission;
- Telegram message result capture;
- local operational/audit data and tests.

Immutable implementation evidence used for selection:

| Evidence | Blob SHA | Why it matters |
|---|---|---|
| `README.md` | `7580d8112918c0be3381ff0073b7a481fa388434` | current product purpose and end-to-end pipeline |
| `docs/TECHNICAL_SPEC_V1.md` | `1b39e946f48e3eec99d21e225b9384089a120f3a` | scheduler, manual/autopost modes, publication-ledger and idempotency requirements |
| `src/modules/publishing/service.py` | `11a4456d22926de93f69fd8a32f4b2e453c6b06a` | product-owned publication candidate selection and duplicate exclusion |
| `src/telegram/publisher.py` | `e9ad7b90a55c2f1d4a7324f99a171b471f757b48` | durable pre-send reservation, duplicate protection and Telegram outcome/message-id capture |
| `tests/test_publishing.py` | `93de7a08e14463c9b65cd47a063622baca4aa280` | publication behavior has an existing test surface |

Repository-provenance note: current evidence is read from `arvectum/discount-parser`; some older product documentation still names the predecessor `arutyunoveth/discount-parser`. Repository naming is implementation provenance and does not define Product Identity.

The selection is not based on superficial product-domain difference. It creates a different platform pressure:

1. scheduled/machine-initiated execution rather than one bounded human-led analysis case;
2. external mutation to Telegram rather than artifact-only output;
3. duplicate/idempotency protection before an external effect;
4. explicit failure versus uncertain-outcome/reconciliation semantics;
5. source observations that remain externally authoritative rather than admitted platform Documents;
6. a product-local operational ledger that must remain distinguishable from shared governed reconstruction evidence.

## 3. Product and Product Contract identity

The contract is Organization-scoped. `<organization>` MUST resolve to the explicit Organization operating the selected Discount Parser instance; no ambient/default Organization is permitted.

- Product identity: `product/arvectum-discount-parser@<organization>`;
- Product compatibility line: `mvp-v1/controlled-telegram-publication`;
- Product architectural owner: `ООО «Арвектум»`;
- Product Contract subject: `product-contract-subject/p6-06-arvectum-discount-parser@<organization>`;
- Product Contract version: `product-contract-version/p6-06-arvectum-discount-parser-v0.1.0@<organization>`;
- Product Contract semantic type: `platform.product-contract`;
- Product Contract authority mode: `Native` for the Product Contract record itself;
- Product Contract authority scope: `platform.product-contract/boundary`;
- Product Contract accountable owner: `ООО «Арвектум»`;
- Product Contract lifecycle: `Provisional`.

The Product Contract Subject Identity is stable for this boundary lineage. Any material admitted boundary change MUST create a new immutable Product Contract Version Identity. Any consequential governed P6.06 execution MUST preserve the exact effective Product Contract Version Identity or equivalent immutable reference.

## 4. Bounded workflow scope

### 4.1 In scope

One governed P6.06 publication execution may:

1. resolve one explicit Organization and initiating Actor or governed scheduled/service trigger;
2. reference one product-owned eligible publication candidate and the material product/source observations on which eligibility depends;
3. preserve exact product workflow/configuration/rule/template references that materially determine the publication attempt where required for reconstruction;
4. create or advance the RFC-0005 Execution Context before the consequential external effect;
5. classify the publication operation as `ExternalMutation` and, because public channel output may affect reputation/communications, as a bounded external organizational consequence;
6. establish the required intent/evidence path before sending to Telegram;
7. invoke the existing product-owned Telegram publisher for one candidate;
8. record the external outcome as success, failure, duplicate/not-applicable, or explicit uncertainty/reconciliation-required state as supported by the governed adapter;
9. preserve the Telegram external reference, including `telegram_message_id` when success is confirmed;
10. preserve required RFC-0006 Event/provenance/effect references sufficient for reconstruction;
11. reconstruct the execution through CAP-004 without treating the reconstruction view as a new authority.

The first implementation proof SHOULD start with an explicit manual/operator-approved publication because it gives the clearest authority evidence. A later run MAY exercise existing product autopost behavior only when the scheduled/service trigger, current configuration, authorization and pre-authorized operating rule are explicit and reconstructable. Successful manual integration does not silently authorize autopost.

### 4.2 Explicit exclusions

This Product Contract does **not** include or authorize:

- migration of the full Discount Parser SQLite database into the Platform Kernel;
- platform ownership of `Offer`, source-adapter, taxonomy, classification, deduplication, stale/expiry, queue or publication-template semantics;
- generic scheduler promotion into a Platform Capability;
- generic notification/Telegram capability admission;
- source crawling or adapter execution as a shared Platform Capability;
- CAP-001 admission of every source page, image or generated Telegram post as a governed Document/Artifact;
- CAP-002 promotion of manual overrides or learned classification rules into shared Organizational Memory/Knowledge;
- CAP-003 replacement of product-local filtering/browsing/search;
- cross-Organization sharing or learning;
- automatic change to approved product rules, filters, templates or autopost settings by AI;
- bot-token, channel credential or other reusable-secret storage in canonical history;
- public/stable API or serialization commitment;
- bulk historical reconstruction of prior publications;
- an assumption that Telegram or source websites are always available or transactionally coupled to Arvectum OS.

Crossing any exclusion requires a new Product Contract version and the minimum sufficient RFC/ADR/policy/approval gate if triggered.

## 5. Exact platform dependency

P6.06 intentionally has one minimum shared capability dependency.

| Dependency | Capability lifecycle | Capability contract | Product Contract reliance | Required boundary use |
|---|---|---|---|---|
| `CAP-004 — Audit / Reconstruction Support` | `Incubating` | `Provisional` | `Provisional` | reconstruct the controlled publication execution from exact governed execution/event/effect references and expose incomplete/uncertain/unavailable evidence honestly |

### 5.1 CAP-004 operation envelope

The contract requires only these domain-neutral CAP-004 semantics:

- reconstruct one governed publication execution;
- resolve the exact Actor or governed trigger, Organization, Product Contract and Workflow/config references materially used;
- resolve material product-owned source/candidate/publication references without importing their domain schemas into the platform;
- resolve attempted external effect and confirmed/failed/uncertain outcome evidence;
- resolve retry/reconciliation causation where applicable;
- expose evidence completeness and known gaps;
- distinguish canonical governed evidence from derived reconstruction output.

Current implementation tokens, method names, persistence layout and service boundaries remain internal/provisional and are not promoted into public compatibility commitments.

### 5.2 Explicitly omitted dependencies

**CAP-001 — Document & Artifact Governance: omitted.** Source pages/images and Telegram posts remain external/product references for this slice. P6.06 does not need shared Document/Artifact governance to validate the external-effect reconstruction boundary.

**CAP-002 — Memory & Knowledge Governance: omitted.** Manual overrides, deterministic classification rules, learned product rules and correction behavior remain product-owned. Product-local rule memory does not become validated platform Knowledge through this contract.

**CAP-003 — Search / Index Projection: omitted.** Offer browsing, source filters, queue filters, ranking and web UI remain product-owned.

Omission is deliberate. A later immutable Product Contract version may add a capability only when real-use evidence establishes a concrete governed need.

## 6. Product-owned semantics

Discount Parser remains responsible for all product-domain meaning and behavior, including:

- source registry and source adapter semantics;
- public-source collection behavior and network policies;
- `Offer`, `Source`, `OfferSourceObservation`, `Publication` and related product schemas;
- normalization and canonical-URL rules;
- exact/fuzzy deduplication and fingerprints;
- category/subcategory taxonomy;
- manual overrides and product-local learned classification rules;
- lifecycle states such as `new`, `needs_review`, `ready`, `published`, `expired`, `rejected`;
- publication filters and eligibility;
- queue ordering and max-post policy;
- scheduler cadence;
- manual versus autopost product behavior;
- Telegram rendering, template/version and keyboard UX;
- publication reservation/duplicate protection implementation;
- product-local SQLite/XLSX representation;
- customer/operator UI and onboarding;
- product-owned logs, ParseRun/run reports and diagnostics.

None of these becomes a Platform Capability, platform-wide Event taxonomy or shared organizational Knowledge merely because a governed execution references it.

## 7. Organization, Actor, authority and sovereignty boundary

Each governed run uses one explicit Organization scope.

Requirements:

1. Product Contract, Execution Context, required Events/evidence and product boundary references MUST resolve to the same Organization unless an independently governed cross-Organization contract exists.
2. Scheduled/background work MUST carry explicit Organization and attributable service/trigger identity; it MUST NOT run under ambient cross-tenant credentials.
3. Manual publication MUST preserve the actual operator Actor and applicable authorization/approval context.
4. Autopost, if later exercised within this version, MUST preserve the attributable service identity plus the governed configuration/authority basis that pre-authorized the bounded operation; Product Contract possession is not authorization.
5. Cross-Organization access/reuse is denied by default.
6. Product/public-source data from one Organization MUST NOT silently become shared platform knowledge or another Organization's product input.
7. Secrets MUST remain outside canonical payload/history.

## 8. Canonical state and authority modes

| Object / information | Authority in this contract | Authoritative source / scope | Boundary responsibility |
|---|---|---|---|
| External discount/promo source page/post observation | `External Reference` for the underlying source occurrence/content | originating public website/channel within the observed retrieval scope | product collects/transforms; governed evidence may retain stable source/time/reference without claiming external truth beyond the evidence |
| Normalized Offer, dedup/classification state and publication eligibility | product-owned local state | Discount Parser product runtime | platform does not become source of truth for product workflow state |
| Product publication reservation/ledger row | product-owned local state | Discount Parser product runtime | may be referenced for reconstruction; it is not platform canonical authority for Telegram message existence |
| Telegram message existence and Telegram message identifier | `External Reference` | Telegram channel/API | Telegram remains authoritative for the external message/result; local success evidence records what was observed |
| P6.06 Execution Context | `Native` | Arvectum OS governed execution history | platform owns its governance/execution envelope, not Discount Parser domain meaning |
| Required admitted Event/provenance/effect evidence | `Native` for the Arvectum OS observation/evidence act | Arvectum OS governed history | evidence records what the governed execution observed/did; it does not convert source or Telegram facts into Native business truth |
| CAP-004 reconstruction view | derived/read-only | exact retained governed evidence | never a competing authority |
| Product Contract | `Native` | ООО «Арвектум» within the declared Organization boundary | exact immutable version governs shared reliance |

No `Governed Replica` is required by `0.1.0`. If later synchronization or replica semantics are needed, a new Product Contract version MUST define freshness, ordering, conflict, failure, retention/deletion and cutover rules before reliance.

## 9. Boundary reference types

The minimum product-owned references that may cross the boundary are:

- `discount-parser.parse-run-ref`;
- `discount-parser.source-observation-ref`;
- `discount-parser.offer-ref`;
- `discount-parser.publication-candidate-ref`;
- `discount-parser.publication-attempt-ref`;
- `discount-parser.rule-config-ref`;
- `discount-parser.template-version-ref`;
- `discount-parser.telegram-message-ref`.

These are product-owned semantic references, not new Kernel primitives or platform-wide schemas. Full product payloads SHOULD NOT cross the boundary when stable references plus minimized evidence are sufficient.

## 10. Operation and side-effect classes

### 10.1 Product-local preparation

Source collection, normalization, deduplication, classification, lifecycle maintenance, queue construction and rendering preview remain product-owned operations. They may be referenced by governed evidence when material, but are not shared platform operations in this contract.

### 10.2 Governed publication attempt

Semantic operation: `controlled external publication attempt`.

Side-effect class:

- `ExternalMutation` — Telegram channel state may change;
- bounded external organizational consequence — public output may affect communications/reputation.

Before the external call, the governed execution MUST establish:

- exact Product Contract version;
- Organization;
- initiating Actor or governed scheduled/service trigger;
- product publication candidate reference;
- materially relied-upon product configuration/filter/template references;
- applicable authorization and Organizational Authority/approved operating rule where required;
- idempotency/duplicate-protection reference;
- required intent/evidence path;
- target Telegram channel external reference;
- failure/uncertainty/reconciliation behavior.

A successful Telegram call MUST NOT be treated as governed completion until required outcome/effect evidence is durably attributable or the execution is explicitly marked incomplete/uncertain/reconciliation-required under RFC-0006.

### 10.3 Reconstruction

CAP-004 reconstruction is `ReadOnly` and derived. It MUST NOT mutate Telegram, product state or prior admitted evidence.

## 11. Event, provenance and reconstruction boundary

P6.06 uses RFC-0006 evidence semantics without creating a generic promotion/marketing Event taxonomy.

For one completed governed publication attempt, reconstruction MUST be able to identify, directly or by governed reference and within lawful retention:

- exact Product Contract Version Identity;
- exact Workflow/config version or immutable product workflow reference governing the operation;
- Organization;
- actual Actor or governed service/trigger;
- candidate Offer/publication reference;
- material source-observation references;
- material filter/rule/template references;
- external target reference;
- pre-effect publication reservation/idempotency evidence;
- external operation intent/attempt reference;
- outcome: `published`, `failed`, `duplicate/not-applicable`, or explicit `uncertain/reconciliation-required` where applicable;
- Telegram message reference/id when success is confirmed;
- retry/reconciliation/compensation causation if any;
- terminal governed execution state;
- known missing/redacted/deleted/unavailable evidence.

Product-local debug logs, source logs, metrics, traces, ParseRun diagnostics and UI analytics remain telemetry/non-canonical by default. They MUST NOT become hidden Product Contract dependencies or substitutes for required governed evidence.

## 12. Idempotency, retry, uncertainty and reconciliation

The existing product implementation establishes a durable reservation before the Telegram network call and uses product-level duplicate protection. This remains product-owned implementation evidence.

The governed boundary adds these requirements:

1. the publication candidate/attempt MUST have a stable correlation or idempotency reference sufficient to connect the product reservation, external call and governed execution;
2. duplicate delivery or execution retry MUST NOT create a second Telegram post silently;
3. a known failed attempt MAY be retried only under the product's explicit safe retry/requeue rule and a new/linked governed attempt where the operation is a new consequential action;
4. if the system cannot determine whether Telegram accepted the operation, the execution MUST enter `uncertain/reconciliation-required` rather than blindly retry;
5. reconciliation SHOULD consult the external Telegram state and product ledger where feasible, while preserving Telegram as authority for the external message fact;
6. correction or compensation creates additional governed history; it MUST NOT rewrite prior admitted Events or sealed terminal execution history;
7. partial completion MUST be exposed rather than reported as unqualified success.

Current product code that maps any caught Telegram exception directly to `failed` is implementation evidence, not proof that every network/API failure is semantically known-failed. Before a P6.06 governed live run, the adapter MUST distinguish safely retryable known-failure from ambiguous external outcome or conservatively map ambiguity to reconciliation-required state.

## 13. Security, privacy, rights and secret handling

1. Access is deny-by-default and least privilege applies.
2. Product Contract existence grants no authorization or Organizational Authority.
3. Telegram bot tokens, cookies, API credentials, private keys and reusable secrets MUST NOT enter canonical history, ordinary governed Events, portable evidence packages or repository fixtures.
4. The contract SHOULD preserve a secret/config handle/version reference when materially required, never the reusable value.
5. Organization scope MUST fail closed if unresolved.
6. Background/scheduled execution MUST not lose Organization/actor attribution.
7. External/public data classification does not automatically create unrestricted cross-Organization reuse rights.
8. Derived product data inherits applicable rights/purpose/retention constraints unless a governed rule establishes otherwise.
9. Required reconstruction MUST use minimized references rather than indiscriminate copies of source HTML, bot payloads or logs.
10. Failure MUST NOT broaden access, target another channel, use a default tenant or silently reduce required evidence.

## 14. Failure and degraded-mode behavior

### 14.1 Contract/context failure

A governed P6.06 publication MUST stop before external mutation when:

- exact Product Contract version cannot be resolved;
- Organization is missing/ambiguous;
- initiating Actor/service/trigger cannot be attributed sufficiently;
- the operation is outside the declared boundary;
- applicable authorization/authority/data-governance gate cannot be evaluated;
- the target channel or product candidate reference is ambiguous;
- required pre-effect evidence cannot be established.

### 14.2 CAP-004/reconstruction path failure

If CAP-004 is unavailable after a completed effect, already established evidence remains authoritative; reconstruction unavailability MUST be exposed and MUST NOT mutate or duplicate the external effect.

If required Event/evidence persistence is unavailable **before** the external mutation, the P6.06 governed path MUST fail/pause unless an explicit bounded degraded mode has been separately governed. Ordinary product-local operation may continue only outside the claimed P6.06 governed path and MUST NOT be counted as governed evidence.

### 14.3 External Telegram failure

Known failure records `failed` with attributable evidence and no success claim. Ambiguous outcome records `uncertain/reconciliation-required`. Retry is permitted only after the duplicate/idempotency/reconciliation rule establishes that it is safe.

### 14.4 Source-data failure

Failure or staleness of one product source remains a product concern until a candidate is selected. The contract does not make Arvectum OS authoritative for unavailable/ambiguous source facts. If a material source reference needed to justify publication cannot be resolved, the governed publication attempt MUST pause/fail rather than invent the missing fact.

## 15. Portability, retention, deletion and migration

Within this contract scope, a governed export/migration SHOULD preserve where applicable:

- Product and Product Contract identities/versions;
- Organization scope;
- Execution Identity/version lineage;
- Actor/service/trigger references;
- product candidate/source/publication references sufficient for reconstruction;
- Workflow/config/template immutable references materially used;
- required Events, causation/correlation and external-effect references;
- Telegram message reference/id where lawfully retained;
- outcome/uncertainty/reconciliation state;
- classification/retention/deletion references;
- explicit evidence gaps.

The export MUST NOT include reusable Telegram credentials or other non-exportable secrets merely for convenience.

There is no bulk migration of historical Discount Parser runs/publications. P6.06 adoption is prospective for a bounded validation slice. Product-local SQLite, XLSX, raw source payloads and historical publication rows remain product responsibility unless a later governed migration decision changes scope.

Deletion/minimization may lawfully reduce reconstruction. The system MUST qualify resulting evidence limitations instead of claiming full reconstruction after required payload/reference removal.

## 16. Bounded adoption and evidence plan

P6.06 completes **selection plus Product Contract boundary definition**, not full second-product integration.

Recommended next bounded execution sequence under this contract:

### Stage 1 — synthetic/offline contract proof

- instantiate exact Product Contract `0.1.0`;
- map CAP-004 and shared execution/event semantics;
- use a fake/stub Telegram adapter;
- prove wrong Organization, missing contract version, duplicate attempt, missing pre-effect evidence and ambiguous external outcome fail safely;
- prove product schemas remain product-owned references rather than platform schemas.

### Stage 2 — one explicit manual real publication

- one Organization;
- one attributable human operator;
- one publication candidate;
- one real Telegram target channel authorized for the validation;
- preserve product reservation and governed intent before send;
- capture confirmed message reference and reconstruct the run through CAP-004.

### Stage 3 — one controlled scheduled/autopost run

Only after Stage 2 passes:

- preserve scheduled/service identity;
- preserve exact enabled autopost/config/filter rule reference;
- prove the pre-authorized operating rule rather than treating scheduler capability as authority;
- prove duplicate/retry/uncertain-outcome behavior;
- reconstruct through the same CAP-004 semantics.

No stage creates an automatic Stable-contract or CAP-004 `Active` promotion.

## 17. Review, exit and lifecycle consequences

Mandatory review: after the first real governed publication execution or no later than `2026-09-08`, matching the current CAP-004 Incubating lifecycle review backstop, whichever occurs first.

Earlier review is required if any material change affects:

- CAP-004 dependency/boundary;
- external side-effect class;
- autopost authority model;
- Organization/cross-Organization scope;
- Event/evidence/reconstruction requirements;
- source/Telegram authority semantics;
- public/stable compatibility surface;
- durable event, storage, IAM, queue or service-topology mechanism;
- product-owned versus platform-owned semantics.

Exit paths:

- issue a new immutable Provisional Product Contract version;
- contain or narrow scope;
- return entirely to product-local operation;
- replace the adapter/integration mechanism while preserving boundary semantics;
- retire the Product Contract with required retention/migration handling;
- consider `Stable` only through a separate RFC-0004 lifecycle decision with compatibility, migration, support and conformance evidence.

P6.06 produces **new real reuse evidence for CAP-004**, but that evidence does not by itself promote CAP-004 from `Incubating` to `Active`. Any lifecycle promotion remains a separate RFC-0001 admission/readiness/decision-authority action.

## 18. ADR, RFC and commercial disposition

P6.06 crosses no current ADR or new-RFC threshold because it selects no durable database, event broker/store, IAM provider, scheduler framework, stable wire format, public API/SDK, service boundary or deployment topology.

Therefore:

- no Constitution change is required;
- no Accepted RFC is changed;
- no new RFC is required;
- no ADR is required by this boundary alone;
- no policy is activated or amended;
- CAP-004 remains `Incubating / Provisional`;
- CAP-001, CAP-002 and CAP-003 remain `Incubating / Provisional` but are not dependencies of this Product Contract version;
- no capability becomes `Active`;
- this Product Contract remains `Provisional 0.1.0`;
- no production/readiness/SLA/support/commercial compatibility claim is created.

If implementation later requires a durable or externally constraining architectural choice, the minimum sufficient ADR/RFC/policy gate MUST reopen before that choice is normalized.

## 19. Contract fitness statement

Within the declared P6.06 scope, this boundary is fit for bounded implementation because:

- Discount Parser is materially different from the first Tender Operator target at the workflow/side-effect level, not merely by business domain;
- the minimum shared dependency is one domain-neutral capability, CAP-004;
- product schemas, source adapters, rules, scheduler and Telegram behavior remain product-owned;
- external-source and Telegram authority remain external;
- Arvectum OS owns only its Product Contract, Execution Context and admitted governed evidence semantics;
- external mutation, idempotency, duplicate, uncertainty and reconciliation responsibilities are explicit;
- product-local telemetry/ledger state is not silently upgraded into platform canonical history;
- security, tenant scope, secret handling and required evidence fail closed;
- portability and rollback are bounded;
- no Stable/public architecture or capability promotion is implied.

**P6.06 selection and Product Contract boundary definition are complete / PASS.**
