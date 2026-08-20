# R27 — Portability / Ecosystem Reuse Review

Status: `Complete / PASS — validated reuse retained; speculative generalization deferred`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract` review
Trigger: after `P8.09`, before `P8.10`
Parent phase: [`Phase 8 — Ecosystem and External Integration`](../roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md)
Operating scope: `Persistent Internal / owner-operated`, one governing Organization; external customer transfer not activated

## 1. Purpose and decision

R27 reviews the Phase 8 portability and ecosystem evidence accumulated through P8.06–P8.09 and determines what is genuinely reusable, what remains product/case-owned, and what must stay bounded until stronger evidence exists.

The review result is `PASS` with an explicit **retain / contain / defer** disposition:

- the external Creative Test Agent case reused existing Arvectum OS platform semantics rather than forcing product-specific behavior into the platform;
- the genuinely shared responsibilities are the already governed Product Contract/dependency-resolution boundary and CAP-004 audit/reconstruction semantics, together with the underlying Kernel/security/execution/provenance portability invariants;
- the P8.06 onboarding helper, P8.09 runbook and P8.07 handover harness remain bounded reference evidence and are **not** promoted into a public/stable integration or export surface;
- Creative Test Agent declaration format and business semantics remain product-owned; EIS/procurement connector behavior remains Tender Operator-owned;
- the P8.07 proof demonstrates preservation of organizational meaning across an implementation/receiver boundary, but does not establish a universal customer export format or actual cross-Organization/customer handover;
- one real external consumer is insufficient evidence for a generic platform manifest, plugin/connector registry, marketplace, package manager, automatic compatibility negotiation, public SDK/API or universal onboarding/export protocol;
- a materially distinct second external consumer is required before proposing a shared/stable external-consumer onboarding abstraction, but even such a second consumer would be evidence for a separate admission/stability decision rather than automatic promotion;
- CAP-004 remains `Incubating / Provisional`; the Creative Test Agent case strengthens its external-reuse evidence but does not by itself justify `Active` lifecycle promotion;
- P8.08 realistic two-Organization isolation remains `NOT ACTIVATED / NOT PROVEN` and is not repaired or bypassed by portability/reuse evidence.

R27 creates no Constitution/RFC amendment, ADR, new Platform Capability, Product Contract lifecycle transition, capability lifecycle transition, public/stable compatibility promise, operational-readiness expansion, conformance claim, SLA/support commitment or commercial promise.

## 2. Authority baseline checked

Checked before and during the review:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with acceptance evidence;
- RFC-0001 — validated reuse over speculative generality, Product/Platform separation, Platform Capability lifecycle, portability, technology independence and commercial-commitment integrity;
- RFC-0002 — stable Subject/Version identity, immutable governed versions, explicit Relationships/authority and technology-independent semantic representation;
- RFC-0003 — Organization sovereignty, deny-by-default access, portability/export/migration/handover, handling constraints, secret boundaries and authority separation;
- RFC-0004 — explicit Product Contract boundary, no hidden coupling, Product Contract lifecycle, extension semantics and evidence-based promotion rather than automatic platform admission;
- RFC-0005 — Governed Execution, exact version attribution, side-effect safety and semantic portability independent of workflow technology;
- RFC-0006 — append-only Event/provenance semantics, replay safety and portability independent of broker/observability technology;
- RFC-0007 — product-owned domain Knowledge by default and governed cross-Organization reuse restrictions;
- RFC-0008 — Document/Artifact identity and manifest/export semantics independent of storage technology without creating a stable customer format by architecture alone;
- Accepted ADRs — none exist; `docs/adrs/README.md` defines the ADR process only, so no permanent public API/serialization, external-consumer registry, connector marketplace, export format, IAM, broker or multi-Organization topology is canonically selected;
- `PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md` — CAP-001 through CAP-004 remain `Incubating / Provisional`; a generic connector marketplace/broad adaptor framework and public SDK/API remain explicitly deferred/not admitted;
- `PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` — CAP-004 is the existing bounded shared Audit/Reconstruction Support responsibility and its view/transport schemas are not stable public interfaces;
- P8.06, R26, P8.07, P8.08 and P8.09 canonical reviews and their executable evidence;
- the exact Creative Test Agent consumer declaration at commit `8dd5aab83beb29be10629f06a2c4e3255e51f06c`, blob `67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3`;
- current repository executable baseline: `Reference Python CI #199`, `1264 tests / OK` from P8.09.

No higher-authority conflict was found for the dispositions below.

## 3. Review question 1 — did the external case reuse platform semantics or force product-specific special cases?

**Disposition: `REUSE CONFIRMED / NO PRODUCT-SEMANTIC PLATFORM LEAKAGE FOUND`.**

The Creative Test Agent case relies on existing governed mechanisms:

1. an RFC-0004 `Provisional` Product Contract;
2. the existing Product Contract declaration/validation path;
3. the existing P5.03 exact governed dependency resolver;
4. the existing CAP-004 `1.0.0` Provisional Audit/Reconstruction Support contract;
5. exact Organization/purpose/right/classification context plus Authorization and DataGovernance gates;
6. exact source/Product Contract/provider version evidence;
7. existing governed evidence/reconstruction semantics from RFC-0005/RFC-0006.

The P8.06 onboarding layer composes those existing mechanisms and rejects direct table access, private imports, undocumented endpoints, private streams and implicit shared mutable state. It does not require Creative Test Agent scoring, brand-safety rules, audience simulation, creative schemas, product workflows, reports, UX, prompt or model semantics to enter CAP-004 or another platform capability.

The product-owned declaration is deliberately owned by `arvectum/creative-test-agent` rather than by Arvectum OS. That is evidence that the current integration did not manufacture a platform manifest merely to fit one consumer.

Result: the external case validates the existing product → declared platform contract direction. No product-specific special case is justified for the platform.

## 4. Review question 2 — what duplicated integration responsibility was actually removed?

**Disposition: `BOUNDED DUPLICATION AVOIDED; GENERAL ECOSYSTEM DUPLICATION NOT YET PROVEN REMOVED`.**

The evidence supports two concrete reuse claims:

- Creative Test Agent does not implement its own audit/reconstruction semantics for the consumed operation; it relies on CAP-004 `p3.08.reconstruct-execution` through an exact Product Contract instead of duplicating the platform reconstruction responsibility.
- P8.06 does not create a Creative-Test-specific dependency resolver. It composes the already existing Product Contract validation and governed dependency-resolution machinery and fails closed on incompatible/missing/ambiguous provider evidence.

The evidence does **not** support stronger claims such as:

- one generic onboarding layer has removed integration duplication across several independent external consumers;
- one universal export/handover package has removed migration work across products/customers/vendors;
- a shared connector framework has replaced product-owned adapters;
- a marketplace/registry/package manager is now justified.

Those stronger statements would exceed the evidence because only one real separately maintained external product consumer has exercised the P8.06/P8.09 onboarding contour, and no real external customer portability recipient exists for P8.07.

## 5. Review question 3 — what remains one-off and should not be generalized?

**Disposition: `CONTAIN`.**

The following remain one-off or bounded reference material:

| Surface | R27 disposition | Reason |
|---|---|---|
| `reference/python/arvectum_os_ref/external_consumer_onboarding.py` | `Contain as internal reference evidence` | Generic-looking shape, but exercised by one real external consumer only; receipt is point-in-time evidence, not registry/current authority. |
| P8.09 external integration runbook | `Contain as bounded reference runbook` | Exact Creative Test Agent source/contract/provider path; not arbitrary-product compatibility documentation. |
| Creative Test Agent declaration JSON shape | `Product-owned / provisional` | Format owner is the product; one declaration does not establish a platform manifest schema. |
| P8.07 `arvectum.p8-07-governed-handover.v1` package | `Contain as task-local proof schema` | Proves semantic reconstruction/handling/authority controls, not stable customer export compatibility. |
| P8.07 receiver receipt schema | `Contain as proof receipt` | No real external customer/Organization receiver or supported importer exists. |
| EIS SOAP/archive/retrieval behavior | `Tender Operator product-owned` | Procurement/external-system-specific semantics are not domain-neutral platform responsibility. |
| exact EIS notice/revalidation case | `Evidence only` | Real validation target, not reusable platform business logic. |
| Creative Test Agent schemas/workflows/scoring/reports/prompts/models | `Creative Test Agent product-owned` | Domain/product semantics under RFC-0004 boundary. |

The following proposed generalizations remain explicitly deferred:

- platform-owned universal external-consumer manifest;
- plugin/extension registry or marketplace;
- remote provider-discovery service;
- package manager/install service;
- semantic-version compatibility inference or automatic fallback;
- automatic background compatibility/resumption service based on historical onboarding receipts;
- universal customer export/import/handover schema;
- cross-Organization migration protocol;
- public/stable external SDK/API.

Containment is intentional architectural discipline, not a failure of reuse.

## 6. Review question 4 — is a second external consumer needed before a stable/shared abstraction?

**Disposition: `YES FOR NEW EXTERNAL-ONBOARDING GENERALIZATION; NOT AN AUTOMATIC PROMOTION RULE`.**

Current external-consumer evidence contains exactly one real separately maintained product integration: Creative Test Agent.

A materially distinct second external consumer is the minimum next evidence needed before proposing that the current onboarding/declaration/helper pattern deserves shared platform ownership or a stable/shared external integration abstraction. The second case should differ materially in product semantics and, ideally, in the capability/dependency shape or integration constraints so that it tests whether the abstraction is genuinely domain-neutral rather than copied from the first consumer.

However:

- `two consumers` is not a magic acceptance threshold;
- a second consumer would only reopen the admission/stability question;
- any new Platform Capability still requires a separate RFC-0001 lifecycle decision;
- any stable Product Contract/public integration surface still requires its applicable RFC-0004/stable-boundary decision;
- concrete durable registry/protocol/serialization/service choices may trigger an ADR;
- security, portability, compatibility, migration, operational readiness and support evidence remain separately required where applicable.

This conclusion applies to **new external-onboarding generalization**. It does not demote CAP-004 or imply that CAP-004 lacks multi-consumer evidence: CAP-004 already has prior Phase 3/Phase 6 bounded reuse evidence and remains legitimately `Incubating / Provisional`. The Creative Test Agent case adds external reliance evidence but does not promote it to `Active`.

## 7. Review question 5 — does portability/handover preserve organizational meaning across implementation changes?

**Disposition: `YES, WITHIN THE BOUNDED P8.07 SEMANTIC PROOF; FORMAT/CUSTOMER TRANSFER REMAIN UNPROVEN`.**

P8.07 demonstrates that an isolated receiver can independently interpret the bounded package while preserving the organizational semantics that matter to the proof:

- Subject Identity and immutable Version Identity;
- explicit relationship endpoints;
- authority mode/scope information;
- provenance and historical Event references;
- selected historical reconstruction without external-effect replay;
- classification and purpose limitation;
- rights/redistribution/cross-Organization restrictions;
- retention/deletion constraints;
- explicit omission of non-exportable secrets plus reprovisioning instructions;
- separation of Organizational Authority, technical access and credentials from export/import;
- explicit termination/revocation requirements;
- fail-closed migration authority transition.

The proof also treats ephemeral runtime cache/telemetry as rebuildable/non-canonical rather than as organizational meaning. This is consistent with technology independence: organizational semantics survive without requiring the originating runtime representation.

The claim stops there. P8.07 does not establish:

- a public/stable serialization contract;
- a universal vendor-neutral customer handover format;
- import compatibility across arbitrary Arvectum OS implementations;
- actual cross-Organization/customer transfer;
- receiver Production readiness;
- redistribution rights or Organizational Authority transfer.

Therefore R27 concludes that **semantic portability is evidenced, while stable packaging interoperability remains deferred**.

## 8. Review question 6 — does any extension/onboarding helper have enough evidence for shared platform ownership?

**Disposition: `NO NEW SHARED PLATFORM OWNERSHIP ADMISSION`.**

The current onboarding helper is useful, domain-neutral in shape and correctly composes governed primitives, but the evidence is still insufficient to admit a new generic `External Consumer Onboarding`, `Connector Framework`, `Extension Registry` or similar Platform Capability.

Reasons:

1. one real external consumer only;
2. declaration schema deliberately remains product-owned;
3. source evidence is caller-supplied and pinned, not remotely discovered through a governed service;
4. the onboarding receipt is historical/point-in-time derived evidence rather than current permission, registry or compatibility state;
5. no persistent runtime reliance/automatic resume mechanism exists;
6. no stable public manifest, package protocol, registry, SDK or API exists;
7. capability catalog already defers a generic connector marketplace/broad adaptor framework pending real multi-consumer evidence;
8. current Product Contract/dependency-resolution mechanisms already cover the genuinely shared responsibility without requiring another capability.

R27 therefore retains the helper as bounded implementation/reference evidence. P8.11 may refactor implementation quality if needed, but such refactoring must not be presented as capability admission or stable-surface creation.

## 9. Reuse / containment / defer matrix

| Mechanism or responsibility | Evidence | R27 disposition |
|---|---|---|
| Kernel identity/version/relationship/authority semantics | RFC-0001/0002 + repeated phase evidence | `Retain shared platform semantics` |
| Organization/security/portability constraints | RFC-0003 + P8.02/P8.07/P8.08 | `Retain shared platform semantics` |
| Product Contract product/platform boundary | RFC-0004 + P8.03/P8.06 | `Retain shared platform semantics` |
| exact governed dependency resolution | existing P5.03 + P8.06/P8.09 | `Retain shared platform mechanism` |
| CAP-004 Audit/Reconstruction Support | Phase 3/6 + P8.06/P8.09 external reliance | `Retain Incubating / Provisional`; no promotion |
| external-consumer onboarding helper | one external consumer | `Contain as bounded reference helper` |
| Creative Test Agent declaration format | one product-owned declaration | `Remain product-owned / provisional` |
| external integration runbook | one exact consumer | `Contain as bounded operational/developer evidence` |
| P8.07 handover package/receipt schema | one same-Organization proof receiver | `Contain as task-local interoperability evidence` |
| stable external-consumer manifest | not proven | `Defer pending materially distinct additional consumer + separate decision` |
| public SDK/API | not proven | `Defer / not admitted` |
| connector/plugin registry/marketplace | not proven | `Defer / not admitted` |
| universal export/import/customer handover format | not proven | `Defer` |
| cross-Organization migration/tenant portability protocol | P8.08 not activated | `Defer; realistic isolation/rights scope absent` |
| EIS procurement adapter behavior | real but domain-specific | `Remain Tender Operator-owned` |
| Creative Test Agent business semantics | real but product-specific | `Remain Creative Test Agent-owned` |

## 10. Functional cross-review

Functional review completed in four iterations of the maximum seven.

### Iteration 1 — scope / claim integrity

Result: `REVISE`.

Material objections:

- “portability proven” could be misread as universal customer/vendor interoperability rather than the bounded semantic P8.07 proof;
- “integration duplication removed” could be misread as proof that one generic ecosystem layer now replaces per-product integration work.

Revision:

- distinguish **semantic portability** from a stable package/import compatibility surface;
- state the exact duplicated responsibilities avoided in Creative Test Agent only;
- preserve actual external customer/cross-Organization transfer as `NOT ACTIVATED`;
- keep P8.08 realistic two-Organization isolation `NOT PROVEN`.

Disposition after revision: `PASS`.

### Iteration 2 — product/platform responsibility and reuse classification

Result: `PASS`.

Checks:

- Creative Test Agent uses existing Product Contract/dependency/CAP-004 semantics;
- no Creative Test Agent business schema/workflow/prompt/model/report responsibility moves into the platform;
- EIS procurement behavior remains product-owned;
- Product Contract/dependency resolution is the shared mechanism actually reused;
- P8.07/P8.09 task-local artifacts are not confused with canonical public platform contracts.

No material objection remains for responsibility direction.

### Iteration 3 — lifecycle / generalization pressure

Result: `REVISE`.

Material objection:

> The generic shape of `external_consumer_onboarding.py` could tempt promotion into shared platform ownership merely because the first external integration passed.

Revision:

- require a materially distinct second external consumer before proposing a new stable/shared external-onboarding abstraction;
- state explicitly that a second consumer is evidence, not automatic admission;
- retain the helper as bounded reference evidence;
- retain CAP-004 at `Incubating / Provisional` and distinguish its pre-existing reuse evidence from the evidence threshold for a **new** onboarding capability;
- preserve the capability catalog’s deferred generic connector/marketplace/public SDK dispositions.

Disposition after revision: `PASS`.

### Iteration 4 — portability, security, ADR and sequencing closure

Result: `PASS`.

Checks:

- bounded P8.07 receiver proof preserves organizational identity/version/relationship/provenance/handling/authority semantics without relying on originating runtime cache/telemetry;
- secrets remain omitted/reprovisioned rather than exported for portability convenience;
- export/import creates no authorization, Organizational Authority, current provider compatibility or external-effect replay;
- no second Organization/customer/recipient is fabricated;
- no stable API/serialization/registry/export-format or persistent integration-state decision is made, so R27 itself crosses no ADR threshold;
- no new Platform Capability or lifecycle transition is required;
- P8.10 remains the correct next step because exact external claims must now be bounded to the evidence and non-claims established here.

No material functional objection remains.

Functional cross-review is not formal RFC/ADR acceptance, lifecycle promotion, operational-readiness approval, conformance approval, customer authorization or commercial approval.

## 11. Engineering / evidence impact

R27 introduces no runtime/code behavior and therefore does not add a new executable test baseline.

The latest executable Phase 8 baseline remains P8.09 `Reference Python CI #199`, `1264 tests / OK`. R27 relies on that executable evidence plus canonical P8.06–P8.09 reviews and the exact external Creative Test Agent declaration.

Roadmap/review synchronization is documentation/governance-only. Any CI run created by the R27 PR is supplementary repository-integrity evidence; it does not widen the R27 result or lifecycle/conformance scope.

## 12. ADR / lifecycle / stable-boundary disposition

- Constitution amendment required: `NO`.
- RFC amendment/new RFC required: `NO`.
- ADR required by R27: `NO`.
- New Platform Capability admitted: `NO`.
- Existing capability promotion: `NO`; CAP-001 through CAP-004 remain `Incubating / Provisional`.
- Product Contract lifecycle change: `NO`; P8.03 and P8.06 remain `Provisional 0.1.0`.
- Public/stable SDK/API/manifest/registry/package/export surface: `NO`.
- External customer/cross-Organization transfer activation: `NO`.
- Realistic two-Organization isolation: `NOT PROVEN`; P8.08 re-entry condition remains unchanged.
- Operational environment/readiness change: `NO`.
- Conformance/commercial/support claim change: `NO`; P8.10 must disposition those separately.

## 13. Gate conclusion and next action

`R27 = Complete / PASS — validated reuse retained; speculative generalization deferred`.

Phase 8 may proceed because the review found no material product/platform leakage or portability contradiction and no justified new shared abstraction that must be admitted before the next step.

The exact reusable core is intentionally narrower than the total amount of integration code/documentation produced in Phase 8. Existing shared platform semantics are retained; task-local helpers and product-specific integrations remain contained; stable ecosystem/onboarding/export generalization is deferred until materially stronger evidence exists.

Next canonical roadmap action:

> `P8.10 — Scoped external conformance/commercial/support boundary review`.

P8.10 must preserve at least these R27 non-claims: one real external product consumer only, external customer transfer `NOT ACTIVATED`, realistic two-Organization isolation `NOT PROVEN`, no public/stable integration or export format, no Stable Product Contract, no Active Platform Capability and no general compatibility/support promise.
