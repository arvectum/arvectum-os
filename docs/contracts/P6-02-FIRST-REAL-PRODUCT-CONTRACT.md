# P6.02 — First Real Product Contract Boundary + Bounded Adoption Plan

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform` and `governance`
Roadmap work item: `P6.02 — First real Product Contract boundary + bounded adoption plan`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone: `M6 — Platform validated through real products and reuse evidence`
Authority: RFC-0004 `1.0.0` — `Accepted`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` — `Accepted`
Selection evidence: [`P6.01`](../reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md)
Product repository: `arutyunoveth/ai-corporation`

## 1. Purpose and contract status

This Product Contract defines the smallest sufficient governed boundary for the first real Phase 6 validation target selected by P6.01:

> **Arvectum procurement/tender AI operator — bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package, with all external actions retained as manual.**

The contract exists before governed Arvectum OS reliance, as required by RFC-0001 and RFC-0004.

This contract is `Provisional 0.1.0`. It is intentionally bounded and reversible. It is not:

- a Stable Product Contract;
- a public API, SDK, wire protocol, manifest schema or package compatibility promise;
- a Platform Capability lifecycle promotion;
- production or operational-readiness approval;
- a customer SLA/support commitment;
- a full-platform conformance claim;
- an authorization grant, Organizational Authority grant or approval delegation;
- a decision to migrate all procurement workflows or all existing pilot data into Arvectum OS.

P6.02 creates the governed declaration and adoption plan only. No real governed platform reliance may begin until `R17 — First Product Boundary Review` passes and P6.03 implements the admitted boundary through the existing Product Contract/integration semantics or another equally explicit governed path.

## 2. Product and Product Contract identity

The first real contract is Organization-scoped. The placeholder `<organization>` MUST resolve to the explicit Organization governing the concrete pilot case; no ambient/default Organization is permitted.

- Product identity: `product/arvectum-tender-operator@<organization>`;
- Product compatibility line: `restricted-paid-pilot/44fz-prebid-v1`;
- Product architectural owner: `ООО «Арвектум»`;
- Product Contract subject: `product-contract-subject/p6-02-arvectum-tender-operator@<organization>`;
- Product Contract version: `product-contract-version/p6-02-arvectum-tender-operator-v0.1.0@<organization>`;
- Product Contract semantic type: `platform.product-contract`;
- Product Contract authority mode: `Native` for the Product Contract record itself;
- Product Contract authority scope: `platform.product-contract/boundary`;
- Product Contract accountable owner: `ООО «Арвектум»`;
- Product Contract lifecycle: `Provisional`.

The Product Contract Subject Identity is stable for this bounded boundary lineage. Any admitted change to the boundary MUST create a new immutable Product Contract Version Identity. P6.03 consequential reliance MUST preserve the exact effective `0.1.0` Product Contract Version Identity or an equivalent immutable reference.

The product compatibility line is deliberately narrower than a product-wide release claim. It identifies only the restricted-paid-pilot 44-ФЗ pre-bid contour evidenced by P6.01 and the current product repository.

## 3. Bounded workflow scope

### 3.1 In scope

For the first bounded adoption, the product may use Arvectum OS only to support the following governed interaction:

1. identify the explicit Organization and Actor context for one selected pilot case;
2. establish the accepted tender-document set under explicit source authority and handling constraints;
3. register or resolve exact governed references/versions for materially relied-upon input Documents/Artifacts through CAP-001;
4. run the existing product-owned tender analysis, requirements/risk extraction, supplier-question/RFQ preparation, optional TKP normalization/comparison and bounded economics/recommendation logic;
5. preserve exact Product Contract, workflow, material input and materially relied-upon configuration/rule references for the governed execution where applicable;
6. require human operator review and any applicable manual escalation before a result is designated client-ready;
7. register or resolve the exact reviewed final report/artifact reference/version and its material derivation provenance through CAP-001 where admitted;
8. preserve required Event/provenance evidence for the governed run;
9. reconstruct the run through CAP-004 from retained governed evidence and expose incomplete/unavailable/redacted/deleted evidence honestly;
10. leave customer delivery and every external procurement/supplier action manual.

### 3.2 Explicit exclusions

This Product Contract does **not** authorize or include:

- autonomous supplier outreach;
- automatic email, messenger or notification sending;
- EIS/ETP login or mutation;
- procurement application submission;
- EDS/signature actions;
- automatic legal approval;
- automatic final bid authorization;
- automatic client delivery;
- cross-customer data, evidence, memory or knowledge reuse;
- 223-ФЗ or commercial-procurement expansion merely to broaden validation;
- product-wide migration to Arvectum OS;
- public self-service SaaS integration;
- a public SDK/API or stable serialization boundary;
- production IAM, durable storage, broker, event-store, object-store, search/vector or service-topology selection.

Any attempt to cross one of these exclusions requires a new Product Contract version and, where applicable, the minimum sufficient ADR/RFC/policy/approval before material reliance.

## 4. Exact platform dependencies

P6.01 identified CAP-001 and CAP-004 as the minimum evidence-backed dependency hypothesis. P6.02 confirms that hypothesis and intentionally omits CAP-002 and CAP-003 from the first real contract.

| Dependency | Capability lifecycle | Capability contract | Product Contract reliance | Required boundary use |
|---|---|---|---|---|
| `CAP-001 — Document & Artifact Governance` | `Incubating` | Provisional `1.0.0` | `Provisional` | exact governed input/output Document/Artifact identity/version, external-authority references, material derivation provenance and handling constraints |
| `CAP-004 — Audit / Reconstruction Support` | `Incubating` | Provisional `1.0.0` | `Provisional` | read-oriented reconstruction from exact governed evidence, explicit evidence completeness/unavailability and canonical-versus-derived distinction |

### 4.1 CAP-001 operation envelope

The Product Contract requires only these domain-neutral CAP-001 semantics:

- register/admit an exact external Document/Artifact reference or version for governed reliance where the selected case requires a platform-governed reference;
- resolve an exact governed Document/Artifact subject/version for reliance;
- preserve or resolve materially relevant Artifact/content identity where applicable;
- record material derivation/source provenance for generated or transformed artifacts;
- resolve exact relied-upon version and handling constraints.

Current Phase 5 operation-token spellings and Python method names remain internal/provisional evidence. P6.03 MUST map this semantic envelope to exact currently supported provider/version evidence before reliance and MUST NOT treat a token spelling as a Stable/public contract.

### 4.2 CAP-004 operation envelope

The Product Contract requires only these domain-neutral CAP-004 semantics:

- reconstruct the bounded pre-bid governed execution;
- resolve exact Actor/authority, Product Contract, Workflow, material input, output and Event references that are lawfully retained;
- expose evidence completeness, missing/unavailable/redacted/deleted state;
- distinguish source canonical evidence from the derived reconstruction view.

The existing internal/provisional `p3.08.reconstruct-execution` operation is valid implementation evidence for the current reference boundary, but its spelling is not elevated into a public compatibility commitment by this contract.

### 4.3 Explicitly omitted dependencies

**CAP-002 — Memory & Knowledge Governance: omitted.**

Procurement profiles, prompts, supplier context, risk methods, extraction rules, taxonomies, prior outcomes and domain learning remain product-owned/local in the first slice. No shared organizational Memory/Knowledge is read or written through this Product Contract.

**CAP-003 — Search / Index Projection: omitted.**

44-ФЗ discovery, EIS search, supplier relevance scoring, procurement-domain ranking, filtering and search UX remain product-owned. The first slice does not need shared governed discovery to prove CAP-001/CAP-004 value.

Omission is deliberate. A later Product Contract version MAY add CAP-002 or CAP-003 only if real-use evidence demonstrates a concrete governed dependency.

## 5. Product-owned semantics

Arvectum OS does not become the owner of procurement meaning through this Product Contract.

The product retains architectural responsibility for:

- tender/case identity and procurement-domain meaning;
- 44-ФЗ business interpretation;
- requirements and material-risk extraction;
- contract-risk methods and thresholds;
- supplier questions;
- RFQ/TKP workflow and templates;
- supplier profile relevance and procurement search ranking;
- quotation normalization and comparison semantics;
- economics, margin and bid-readiness rules;
- participation recommendation semantics;
- product-specific validation and escalation rules;
- prompts, agents, models and domain configurations;
- operator workflow/UX and partner-facing report narrative;
- customer/pilot operating process and commercial packaging;
- product-owned integrations not explicitly declared as platform dependencies.

Product-owned extracted requirements, risk labels, economics and recommendations remain product outputs. They do not become external truth, validated organizational Knowledge or shared Platform Capability semantics merely because they are referenced by governed execution evidence.

## 6. Organization, Actor and sovereignty boundary

Each concrete pilot adoption uses one explicit Organization sovereignty scope.

Requirements:

1. Product, Product Contract, Actor, governed inputs, Execution Context, Events and governed output references MUST resolve to the same Organization unless an independently governed cross-Organization contract explicitly exists.
2. Cross-Organization access is denied by default.
3. The same technical identity, email, customer name or credential in another Organization creates no ambient access.
4. An Arvectum operator acting for a customer/partner Organization requires explicit attributable Actor/delegation/authorization context; Product Contract possession creates none.
5. No data or evidence from one customer Organization may train, enrich, alter or become available to another Organization under this contract.
6. Platform-global state MUST NOT contain customer-specific tender content or hidden shared customer context.

## 7. Canonical state and authority modes

The first adoption preserves existing authoritative sources instead of turning Arvectum OS into a competing system of record.

| Governed object / information | Authority mode in the bounded contract | Authoritative source / scope | Product/platform responsibility |
|---|---|---|---|
| EIS/zakupki.gov.ru procurement registry facts and source documents | `External Reference` by default | ЕИС / zakupki.gov.ru within the retrieved source scope | Arvectum OS governs identity/version/reference/provenance used by the execution; it does not become factual authority for registry content |
| Partner/customer-provided tender files | `External Reference` | accepted partner/customer source package in the approved controlled product runtime | platform may govern exact reference/version/digest/provenance; raw source authority remains external |
| Supplier TKP/quote source documents | `External Reference` | supplier/partner-origin document | quoted commercial facts remain source-authoritative; normalized comparison remains product-derived |
| Product extraction, risk classification, RFQ draft, TKP comparison, economics, recommendation | product-owned transient/derived state by default | product workflow and its exact inputs/rules | not platform authority and not shared Knowledge; may be referenced by provenance where material |
| Governed Execution Context for the platform-backed run | `Native` | Arvectum OS governed execution history | platform records exact execution/governance state; product owns procurement workflow meaning |
| Required shared Event/provenance evidence | `Native` for the admitted Event/evidence act | Arvectum OS governed history of the platform interaction | event proves the admitted act/evidence, not truth of underlying external tender facts |
| Operator review/approval evidence recorded through the governed flow | `Native` for the attributable review act | actual Actor plus applicable authority/approval context | technical access does not create approval authority; review evidence records what occurred |
| Reviewed final client-ready report/artifact | `External Reference` by default for content; governed exact reference/version/provenance | product-controlled reviewed artifact in approved runtime/export package | platform preserves exact artifact reference/version and derivation/review linkage without becoming authority for underlying external facts |
| Product Contract itself | `Native` | ООО «Арвектум» within the Organization-scoped boundary | exact immutable contract version governs platform reliance |

A later decision MAY use `Governed Replica` for a specific external source only if synchronization/freshness/conflict/failure semantics are explicitly added to a new Product Contract version. `Native` MUST NOT be substituted merely for implementation convenience.

## 8. Boundary record, artifact and message types

The contract exposes only the minimum types necessary for interoperability and reconstruction.

### 8.1 Platform-visible governed types

- `platform.product-contract` — the exact Product Contract version;
- RFC-0008 governed Document/Artifact references and versions used by CAP-001;
- RFC-0005 Execution Context versions for the governed platform-backed run;
- RFC-0006 Events/provenance references required for reconstruction;
- CAP-004 derived reconstruction view.

### 8.2 Product-owned boundary semantics

The following may cross the boundary as product-owned payload/reference semantics without becoming platform domain types:

- accepted tender case/document-set reference;
- product analysis-run reference;
- operator-review disposition/reference;
- client-ready report designation/reference.

Full procurement schemas, requirement/risk taxonomies, RFQ/TKP schemas, economic models and recommendation structures remain outside the platform contract unless a later Product Contract version proves a boundary need.

## 9. Operation and side-effect classes

The first real contract admits only the following side-effect classes.

### 9.1 Read-only platform reliance

Examples:

- resolve exact admitted Document/Artifact version through CAP-001;
- resolve handling/provenance references;
- reconstruct a run through CAP-004.

Required gate declarations: `Authorization` + `DataGovernance`, plus underlying capability/source access checks.

### 9.2 Transient product computation

Examples:

- extraction;
- risk classification;
- supplier-question/RFQ draft;
- quotation normalization/comparison;
- economics;
- preliminary recommendation;
- previews and intermediate renderings.

These remain product-local/transient by default and do not become canonical state merely because they exist.

### 9.3 Canonical platform mutation

Only bounded mutations needed to establish or preserve governed evidence are allowed, such as:

- admitting/registering an exact external Document/Artifact reference/version when required;
- creating/advancing the Execution Context;
- admitting required Events/provenance evidence;
- recording attributable operator-review evidence;
- registering the exact reviewed final artifact reference/version where required for the governed result.

A canonical mutation MUST use Governed Execution and declare/evaluate, as applicable, separate `Authorization`, `OrganizationalAuthority`, `DataGovernance` and `ConsequentialApproval` gates. Product Contract possession satisfies none of them.

### 9.4 External mutation and organizational commitment

**Not allowed in this Product Contract version.**

No platform operation may:

- send to suppliers or customers;
- mutate EIS/ETP or another procurement platform;
- submit/sign an application;
- create a binding bid or contract commitment;
- execute a payment or procurement transaction.

Client delivery remains a manual product operating action outside the automated platform boundary.

## 10. Events, provenance and reconstruction boundary

The first real adoption uses RFC-0006 governed evidence only where required for reconstruction. It does not create a universal procurement Event taxonomy.

At minimum, a completed platform-backed result MUST make it possible to identify, directly or by governed reference:

- exact Product Contract Version Identity;
- exact Workflow/version or product workflow definition reference used for the bounded run;
- Organization and initiating/acting Actor;
- exact materially relied-upon input Document/Artifact versions;
- external authoritative source references and applicable handling constraints;
- materially relevant deterministic/AI component or configuration references where required for reconstruction;
- material product analysis-run reference;
- operator review/approval evidence and Actor;
- exact final reviewed artifact reference/version;
- correlation/causation sufficient to connect the above evidence.

Product-local application logs, debug logs, traces, model telemetry and UI analytics remain non-canonical unless separately admitted. They MUST NOT become hidden Product Contract dependencies or substitutes for required governed evidence.

If required evidence is missing, ambiguous, unavailable, redacted or deleted, CAP-004 MUST expose that state. The product MUST NOT silently describe the run as fully reconstructable.

## 11. Security, privacy, rights and data handling

The bounded adoption inherits the strictest evidenced current pilot controls unless a separately governed decision lawfully changes them.

1. Real partner/customer data MUST NOT be committed to `arvectum-os` or `ai-corporation` repositories.
2. Raw real documents remain in approved local/controlled runtime locations.
3. Repository tests/evidence use synthetic, anonymized or safely redacted fixtures only.
4. Partner-facing output still passes the existing product export/redaction guard and human delivery approval.
5. Access is deny-by-default and least privilege applies.
6. Product Contract declaration or successful dependency admission grants neither Authorization nor Organizational Authority.
7. Classification, purpose, rights, minimization, retention/deletion and portability constraints propagate to material derived artifacts unless an explicitly governed transformation establishes otherwise.
8. Secrets, credentials, EIS tokens, private keys and reusable authentication material MUST NOT enter canonical history, ordinary logs, prompts, portable evidence packages or repository fixtures.
9. AI analysis remains attributable, bounded and human-reviewed and cannot be final consequential approver.
10. No customer document, outcome, evidence, memory or knowledge obtains cross-customer reuse rights through processing by Arvectum OS.
11. Reconstruction MUST NOT reveal content that current rights/classification/redaction state denies.
12. Failure MUST NOT broaden access, cross Organization boundaries or silently reduce required evidence.

## 12. Failure, retry and incomplete-evidence behavior

The Product Contract fails closed at the governed platform boundary.

### 12.1 Contract/dependency failure

Fail the platform-backed path when:

- exact Product Contract Version continuity is missing or stale;
- Product/Organization scope drifts;
- CAP-001 or CAP-004 current provider/version evidence is absent, incompatible, deprecated, retired, ambiguous or otherwise unsupported for the declared operation;
- a required operation is undeclared;
- a private table/import/endpoint/Event stream/cache/implicit shared state is used as a substitute boundary.

No hidden platform fallback is permitted.

### 12.2 Source/authority failure

Fail or pause governed reliance when:

- the authoritative source cannot be determined;
- exact source/version identity is ambiguous;
- required content/reference is unavailable;
- freshness or accepted-case status is insufficient for the intended reliance;
- current access/purpose/right/classification checks fail.

The product MAY return to its pre-existing product-local/manual pilot contour, but such a run MUST NOT be represented as having completed the Arvectum OS governed path.

### 12.3 Evidence/reconstruction failure

If required Event/provenance/reconstruction evidence cannot be established:

- do not silently mark the governed result complete;
- expose `incomplete`, `uncertain`, `unavailable`, `redacted/deleted` or `reconciliation-required` state as applicable;
- retain already admitted immutable history lawfully;
- use correction/compensation/additional Events rather than mutating historical evidence.

### 12.4 Retry/idempotency

Retries MUST NOT create duplicate external effects because external effects are outside this contract.

For governed canonical evidence, retry behavior MUST use exact identities/version/content references or an equivalent deterministic idempotency/reconciliation rule. A duplicate attempt MUST resolve to the already admitted semantic result or fail visibly on conflict; it MUST NOT silently create competing canonical truth.

## 13. Portability, retention, deletion and migration

### 13.1 Portability responsibility

Within this contract scope, a governed export/migration MUST preserve where applicable:

- Product and Product Contract identities/versions;
- Organization scope;
- external authority/source references;
- governed Document/Artifact subject/version identities and lawful content references;
- derivation/provenance relationships;
- Execution Context and required Event/evidence references;
- operator review evidence;
- exact final artifact reference/version;
- classification/handling/retention/deletion references;
- explicit omissions caused by legal, contractual, rights, deletion or technical limits.

The contract does not promise export of non-exportable third-party content or reusable secrets.

### 13.2 Retention/deletion responsibility

Existing customer/partner and product-local retention/deletion controls remain applicable. Arvectum OS creates no new retention right merely by recording a governed reference or execution.

Deletion/minimization of source content MUST NOT be represented as if full reconstruction remains possible when required evidence has lawfully disappeared. Historical retained metadata must describe the resulting evidence limitation truthfully.

### 13.3 Migration boundary

There is **no bulk migration** of historical `ai-corporation` pilot cases under P6.02/P6.03.

Adoption is prospective for selected validation cases only. Existing product-local case/workspace data remains product-owned. If the platform path is later abandoned, the product can continue its current local/manual pilot contour without requiring access to private Arvectum OS implementation state.

## 14. Bounded adoption plan

Adoption is deliberately staged and reversible.

### Stage 0 — Contract and R17 gate

Scope: P6.02 only.

- canonically record this Provisional Product Contract and review evidence;
- no real governed platform reliance yet;
- verify exact dependency versions, authority modes, product-owned semantics, failure/rollback and ADR gates at `R17`.

Exit: R17 passes or P6.02 is revised/contained/retired.

### Stage 1 — Synthetic/redacted integration proof

Scope: first P6.03 implementation increment.

- instantiate the exact `0.1.0` Product Contract through the existing internal/provisional Product Contract declaration/validation path;
- bind CAP-001 and CAP-004 to explicit current provider/version evidence;
- map only the declared operations;
- use synthetic/anonymized/redacted fixtures;
- prove wrong-Organization, denied-rights, missing-version and incomplete-evidence paths fail closed;
- prove no product-side private platform import/table/Event fallback is needed.

Exit: focused tests plus existing reference regression suite pass within the changed scope.

### Stage 2 — One real 44-ФЗ pilot case

Scope: one explicit Organization and one owner-approved real validation case.

- keep raw real data in approved controlled runtime locations;
- preserve the product's current human review/export guard;
- use CAP-001/CAP-004 only;
- keep all external actions manual;
- capture integration effort, operator-step overhead, failures and reconstruction evidence separately from product business-quality evidence.

Exit: no stop condition triggered and the case can be reconstructed to the declared evidence standard.

### Stage 3 — Bounded calibration set

Maximum scope: **three real calibration cases**, matching the existing P6.01 measurement baseline instrument unless a new governed decision changes the sample.

- no bulk onboarding or customer-wide migration;
- no new capability dependency merely to increase platform coverage;
- collect evidence required for P6.04 on value, quality, friction, control and platform overhead.

Exit: hand evidence to P6.04/P6.05; do not expand scope automatically.

## 15. Stop conditions and rollback

The platform-backed adoption MUST stop or return to the product-local/manual contour when any of the following is material and unresolved:

- cross-Organization isolation failure or suspected customer-data leakage;
- unclear/competing authority for a materially relied-upon source;
- Product Contract or dependency-version continuity cannot be proven;
- required evidence/reconstruction is incomplete without an explicitly governed degraded state;
- raw real partner/customer data is persisted in a prohibited repository/evidence path;
- any unapproved automated external action occurs or becomes necessary for the slice;
- rights/classification/retention/deletion constraints cannot be enforced;
- platform integration materially blocks the restricted pilot while producing no compensating governance/reconstruction value;
- implementation requires a durable/stable/public architecture choice that has not passed its ADR/RFC/policy gate.

Rollback means:

1. disable the Arvectum OS platform-backed path for new cases;
2. continue the existing `ai-corporation` local/manual restricted-pilot contour where permitted;
3. export/delete/retain Arvectum OS governed state according to applicable policy and rights;
4. preserve lawfully admitted immutable history and record termination/correction/compensation rather than rewriting it;
5. record the evidence as a valid Phase 6 negative result rather than forcing continued adoption.

## 16. Measurement beginning at contract adoption

P6.01 explicitly recorded that empirical real-case KPI values are not yet observed. P6.02 therefore creates measurement fields, not invented outcomes.

Beginning with P6.02/P6.03, record at least:

- active engineering time to define/adapt the real Product Contract;
- product-side integration effort;
- platform-side adapter/capability effort;
- number of platform-induced operator steps;
- new platform-induced failure modes;
- time to identify and recover from a failed platform path;
- reconstruction completeness against the declared evidence set;
- number of hidden-coupling exceptions required (`target = 0`, but report actual evidence);
- rollback/de-platformization effort if exercised;
- defects attributable to the platform boundary;
- P6.04 business/quality measures already defined by the product pilot scorecard, kept separate from target thresholds.

Time reduction, critical-requirement recall, critical-risk recall and usefulness remain unknown until measured. Existing thresholds remain success criteria rather than baseline observations.

## 17. Compatibility assumptions and support status

Compatibility assumptions for `0.1.0`:

1. CAP-001 and CAP-004 remain available under the current Provisional capability-contract baseline `1.0.0` for bounded validation.
2. Exact current provider/version support evidence is checked before relied-upon operations; no automatic fallback version is allowed.
3. Existing P5 Product Contract declaration/resolution/composition/adapter code is internal/provisional implementation evidence and may evolve without public compatibility guarantees.
4. Product Contract lifecycle and Platform Capability lifecycle remain separate.
5. No Stable Product Contract, public API/SDK/wire/package or service boundary is created.
6. Any material boundary change creates a new immutable Product Contract version and reopens R17 or an equivalent architecture review when required.

Support status: **experimental/provisional bounded Phase 6 validation only**.

## 18. Review, expiry and exit path

Mandatory review condition: `R17 — First Product Boundary Review` **before any P6.03 real governed reliance**.

Time backstop: review no later than `2026-09-08`, matching the current Incubating capability lifecycle review date, even if P6.03 has not begun.

Earlier review is required on any material change to:

- Organization/data-rights scope;
- CAP-001/CAP-004 dependency or contract version;
- authority mode;
- canonical mutation or external side-effect class;
- Event/provenance/reconstruction obligations;
- public/stable compatibility surface;
- durable persistence, event delivery, IAM or service topology;
- product-owned versus platform-owned semantics.

Exit paths:

- issue a new immutable Provisional Product Contract version;
- contain scope;
- return the workflow to product-local operation;
- replace the integration mechanism while preserving contract semantics;
- retire the Product Contract after required migration/retention handling;
- consider `Stable` only through a separate RFC-0004 lifecycle decision with compatibility, migration, support and conformance evidence.

## 19. ADR, RFC, capability lifecycle and commercial disposition

P6.02 crosses no ADR threshold.

This contract selects no durable database, object store, Event broker/store, IAM/PDP/PEP provider, workflow engine, search/vector technology, stable serialization, public API/SDK/package, service boundary or deployment topology.

Therefore:

- no new RFC is required;
- no ADR is required by P6.02;
- no policy is activated or amended;
- CAP-001 through CAP-004 lifecycle remains unchanged;
- CAP-001 and CAP-004 remain `Incubating / Provisional` dependencies;
- CAP-002 and CAP-003 remain `Incubating / Provisional` but are not dependencies of this Product Contract version;
- no capability becomes `Active`;
- this Product Contract remains `Provisional 0.1.0`;
- no operational-readiness or Production claim is created;
- no SLA/support/customer compatibility promise is created;
- no commercial claim may describe the Incubating capabilities as Active or this boundary as Stable.

If P6.03 implementation materially relies on a durable or externally constraining choice, the minimum sufficient ADR/RFC/policy gate MUST be reopened before that reliance is normalized.

## 20. Contract fitness statement

Within the declared P6.02 scope, the boundary is fit to proceed to R17 because:

- the product and Organization scope are explicit;
- CAP-001/CAP-004 exact Provisional contract versions are explicit;
- CAP-002/CAP-003 are deliberately omitted rather than force-fit;
- procurement semantics remain product-owned;
- external source authority remains external;
- platform-owned canonical history is limited to its own governed references/execution/evidence acts;
- read, transient, canonical-mutation and prohibited external-effect classes are explicit;
- security/authority/data-handling and cross-Organization rules fail closed;
- evidence incompleteness cannot silently become a complete reconstruction claim;
- portability, migration and rollback are explicit;
- adoption is capped at a bounded calibration set rather than product-wide migration;
- no Stable/public/durable architecture or commercial commitment is created.

This Product Contract is ready for **R17 — First Product Boundary Review**. It is not yet authority to begin unreviewed real governed platform reliance.