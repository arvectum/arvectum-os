# P6.01 — Real Product/Workflow Validation Target Selection + Evidence Baseline

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Roadmap work item: `P6.01 — Real product/workflow validation target selection + evidence baseline`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone: `M6 — Platform validated through real products and reuse evidence`
Result: **`PASS — first real Phase 6 validation target selected with a bounded evidence baseline and reversible handoff to P6.02.`**

## 1. Purpose and decision level

P6.01 selects the first real product/workflow context through which Arvectum OS will be validated after M5. The task does not create a Product Contract, does not change platform behavior, does not promote a Platform Capability, and does not establish operational, production, public-compatibility or commercial commitments.

The selection must be based on actual organizational value, product readiness, measurable real-use evidence, owner/sponsor backing and suitability for bounded platform validation. It must not force a product-local experiment to depend on Arvectum OS merely because the product is strategically important.

## 2. Canonical authority checked

P6.01 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. `docs/rfc/README.md` — RFC-0001 through RFC-0008 remain `Accepted 1.0.0` with recorded approval evidence;
3. RFC-0001 — product/platform separation, validated reuse, authority modes, Product Contract boundary, lifecycle honesty, scoped conformance, proportionality and reversible experimentation;
4. RFC-0002 — stable subject identity, immutable version identity, exact consequential reliance, authority preservation and non-authoritative projections;
5. RFC-0003 — deny-by-default authorization, least privilege, Organization isolation, separation of Authorization and Organizational Authority, purpose/minimization, retention/deletion and portability;
6. RFC-0004 — explicit versioned Product Contract before governed platform reliance, hidden-coupling prohibition and separation of Product Contract and Platform Capability lifecycle;
7. RFC-0005 — product-owned domain workflows, exact Product Contract attribution, Governed Execution for consequential canonical mutation and explicit side-effect semantics;
8. RFC-0006 — append-only Event/provenance semantics, reconstruction evidence, failure-closed required evidence paths and non-authoritative telemetry/projections;
9. RFC-0007 — product-owned domain Memory/Knowledge, explicit promotion and exact relied-upon Knowledge versions where applicable;
10. RFC-0008 — exact Document/Artifact identity/version reliance, derivation provenance, handling propagation and product-owned document taxonomies/workflows;
11. `docs/adrs/README.md` — no applicable Accepted ADR establishes a conflicting durable technology, public SDK/API, persistence, event, IAM, document-storage or service-topology boundary for this selection task;
12. `docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md` — CAP-001 through CAP-004 remain `Incubating / Provisional` and may be used only for bounded validation without implying `Active` lifecycle status;
13. `docs/roadmap/PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md` — P6.01 evidence requirements and M6 boundary.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was identified.

## 3. Product evidence checked

The selected target is grounded in the real product repository `arutyunoveth/ai-corporation` rather than in Phase 6 roadmap history or a preferred product name.

Current evidence used:

| Evidence | Repository path | Immutable blob SHA | What it establishes |
|---|---|---|---|
| Product repository current state | `README.md` | `614854a7ef3cca8448f4b346f12ce712fca24927` | commercial MVP/pilot tooling exists; the product is in restricted paid-pilot readiness with manual-control boundaries; no broad autonomy or external execution is open |
| Pilot scope and success criteria | `docs/demo/pilot_scope.md` | `8082d7d29f561112ca1de61902ab81a5c1550413` | real-case pilot scope, customer/operator roles, manual baseline capture, safety gates, KPI thresholds and client-ready immutable report flow |
| KPI scorecard | `docs/demo/pilot_kpi_scorecard.md` | `b8bcab1a96e257b330724e79a293aeab8a5fd010` | definitions and formulas for manual baseline minutes, pilot minutes, requirement/risk recall, false critical findings, usefulness and safety evidence |
| RFQ-first workflow | `docs/product/Tender_Operator_RFQ_Workflow.md` | `e0f74644510dcd996bc2271259ceffae4dd6d1e5` | bounded tender-analysis → requirements → RFQ/TKP → economics → bid-decision workflow and retained manual external actions |
| Restricted pilot operations | `docs/product/Restricted_Paid_Pilot_Operations_Runbook.md` | `ea5cae8e1410e2d4a87b099d505de6b3a8576d22` | real partner-data handling, manual review/export/delivery, partner feedback/outcome loop and reversibility of the current operating contour |
| Local pilot data policy | `docs/product/Local_Pilot_Data_Handling_Policy.md` | `c3e9756a9e3142cfc3617b9d8e1721ea2b4eef54` | real partner data remains local/ignored, export guard is mandatory, only redacted/synthetic evidence may enter repositories |

The current `ai-corporation` README is used as product-status evidence, not as architecture authority for Arvectum OS. The product evidence above is sufficient to establish the selected workflow boundary and measurement/control baseline.

## 4. Selection result

### 4.1 Selected real validation target

**Product:** Arvectum procurement / tender AI operator (`arutyunoveth/ai-corporation`).

**First Phase 6 workflow:** **real 44-ФЗ tender/operator pre-bid decision package**, bounded from accepted tender documentation through a human-reviewed client-ready result.

The validation slice is:

1. receive or retrieve tender documentation in read-only/manual-intake mode;
2. establish the accepted case/document set;
3. extract requirements and material risks;
4. prepare supplier questions and an RFQ draft;
5. when supported TKP inputs are present, normalize and compare supplier quotations;
6. calculate bounded bid economics and prepare a preliminary participation recommendation;
7. require operator review and applicable manual escalation;
8. produce a version-identifiable, reviewed final report/artifact and record the result as client-ready for manual delivery;
9. retain sufficient evidence to reconstruct which inputs, versions, rules, analysis run and human review produced the delivered result.

### 4.2 Explicit exclusions

The Phase 6 first slice does **not** include:

- autonomous supplier outreach;
- automatic email or messenger sending;
- ETP/EIS login, application submission or procurement-platform mutation;
- EDS/signature actions;
- automatic legal approval;
- automatic final bid authorization;
- cross-customer learning or data reuse;
- 223-ФЗ or commercial-platform expansion merely to broaden the test;
- public self-service SaaS, public SDK/API or Stable Product Contract claims;
- forced migration of every `ai-corporation` workflow into Arvectum OS.

These exclusions preserve the current product safety boundary and keep P6.01/P6.02 reversible.

## 5. Owner, sponsor and organizational outcome

| Field | P6.01 baseline |
|---|---|
| Product/workflow owner | `ООО «Арвектум»` — owner of the procurement product and its pilot workflow |
| Phase validation sponsor | `ООО «Арвектум»` — owner of Arvectum OS and sponsor of Phase 6 validation |
| Organizational/business outcome | determine whether Arvectum OS reduces the cost and friction of operating a real tender-analysis workflow while improving governed document handling, reconstruction and control quality without pushing procurement semantics into the platform |
| Product outcome | preserve or improve the existing pilot's useful pre-bid decision package while retaining human review, manual external actions and current customer-data restrictions |
| Evidence outcome | collect comparable pre/post evidence for active operator time, critical requirement/risk recall, usefulness, reconstruction quality, integration effort and platform overhead |

The selection does not assert that this workflow is the only or highest-priority product initiative of the company. P6.01 selects it because it combines real product readiness, measurable value evidence and genuine platform-semantic pressure. Product-local initiatives that do not need shared platform capabilities, shared platform history or canonical platform state should remain product-local rather than being forced into Phase 6 integration.

## 6. Current evidence baseline before Arvectum OS integration

### 6.1 Product/runtime baseline

The product already has a bounded real-pilot operating contour with:

- real tender/document intake;
- human-controlled analysis;
- product-local case/workspace state;
- requirements/risk extraction;
- RFQ/TKP workflow support;
- deterministic economics/bid-readiness logic;
- operator review;
- guarded partner-facing export;
- manual delivery;
- feedback/outcome capture;
- no broad autonomy or procurement-platform submission.

This means Phase 6 is not allowed to claim value merely by reproducing an existing product feature. The validation question is whether shared governed foundations create measurable leverage or risk reduction compared with this existing product-local baseline.

### 6.2 Measurement baseline

No repository evidence provides completed empirical real-customer values for manual active time, requirement recall, risk recall or usefulness at P6.01 entry. P6.01 therefore records **unknown/not-yet-observed values explicitly rather than fabricating them** and preserves the existing pilot measurement method as the baseline instrument.

| Measure | Current baseline state | P6.01 evidence rule |
|---|---|---|
| Manual active operator time | `T0 = not yet observed in a completed real calibration set` | capture manual minutes for at least the existing 3-case calibration sample before comparing platform-assisted runs |
| Platform-assisted active time | `not applicable before P6.03` | measured separately from waiting time using the existing scorecard definition |
| Critical-requirement quality | empirical baseline `not yet observed` | manual gold-standard cases remain authority for comparison; do not substitute target thresholds for observed baseline |
| Critical-risk quality | empirical baseline `not yet observed` | compare against manually confirmed critical risks; record false critical findings separately |
| Report usefulness | empirical baseline `not yet observed` | use the existing 1–5 operator usefulness scale |
| Safety: human review | current required control = `100%` of delivered results | must not regress |
| Safety: automated external actions | current required control = `0` | must not regress |
| Safety: cross-client leakage | current required control = `0 confirmed` | must not regress |
| Artifact binding | current required control = `100%` of delivered reports bound to the current reviewed run/artifact | must not regress |
| Critical unresolved defects | current required control = `0 Sev-1` at completion | must not regress |

Existing pilot success thresholds such as `≥30%` median active-time reduction, `≥90%` critical-requirement recall, `≥85%` critical-risk recall and `≥4.0/5` usefulness are **target criteria, not baseline measurements**. P6.04 must keep that distinction explicit.

### 6.3 Integration-effort/platform-overhead baseline

Before P6.02/P6.03, the product has no Phase 6 real Product Contract and no declared governed reliance on Arvectum OS shared capability state/history for this workflow.

Therefore the platform-integration baseline is:

- Product Contract creation/adoption effort: `0` historical Phase 6 real-product effort; measurement begins in P6.02;
- platform adapter/composition effort: `0` historical Phase 6 real-product effort; measurement begins in P6.03;
- platform-induced operator steps: `0` before integration;
- platform-induced failure modes: none yet attributable to real-product reliance;
- product-local duplicate governance/reconstruction mechanisms: present and available as comparison evidence, but not automatically treated as platform debt until real-use analysis proves value in consolidation.

## 7. Required and candidate platform interactions

P6.01 records only the minimum evidence-backed dependency hypothesis. Exact dependencies and operations belong to the P6.02 Provisional Product Contract.

### 7.1 Required for the first bounded adoption plan

**CAP-001 — Document & Artifact Governance (`Incubating / Provisional`)**

Expected real-use pressure:

- identity/version handling for accepted tender-document inputs;
- exact relied-upon document/artifact versions;
- derivation provenance for extraction/redaction/rendering where materially relied upon;
- reviewed final report/artifact identity and handling constraints;
- governed export/portability semantics without binding the product to one storage technology.

**CAP-004 — Audit / Reconstruction Support (`Incubating / Provisional`)**

Expected real-use pressure:

- reconstruct the analysis run from exact input versions;
- preserve applicable workflow/Product Contract/dependency versions;
- connect operator review and final artifact to the run that produced it;
- distinguish canonical governed evidence from ordinary logs/telemetry;
- expose incomplete evidence or reconstruction failure instead of silently claiming a complete governed result.

Shared Kernel, RFC-0003 security/Organization semantics, RFC-0005 Governed Execution and RFC-0006 Event/provenance semantics are foundational dependencies behind these interactions where applicable; they are not new product-domain capabilities.

### 7.2 Conditional / not required for the minimum first slice

**CAP-003 — Search / Index Projection** is a candidate only if P6.02 demonstrates that governed discovery over accepted document/result identities materially reduces product duplication. Existing procurement search relevance, 44-ФЗ discovery and supplier relevance remain product-owned domain behavior and must not be moved into CAP-003.

**CAP-002 — Memory & Knowledge Governance** is not required merely because the product has profiles, extraction rules, supplier context or prior outcomes. Procurement taxonomies, prompts, scoring, supplier logic, risk methods and domain learning remain product-owned. CAP-002 becomes relevant only if the real slice intentionally reads/writes shared organizational Memory/Knowledge under an explicit Product Contract and rights/freshness/promotion controls.

This containment is deliberate: P6.01 validates platform reuse rather than maximizing the number of capabilities touched.

## 8. External authorities and source-of-truth baseline

The first real integration must preserve external authority instead of turning Arvectum OS into a competing source of truth.

| Information/object | Baseline authority disposition |
|---|---|
| 44-ФЗ procurement registry/document source retrieved from ЕИС / zakupki.gov.ru | external authoritative source remains external; P6.02 must choose `External Reference` or `Governed Replica` semantics proportionate to the exact reliance and available source contract |
| Partner/customer-provided tender files | source content is authoritative as received from the partner/source channel for the accepted case package; Arvectum OS may govern identity/version/provenance without inventing new factual authority |
| Supplier TKP / quote documents | supplier/partner-origin document remains the source for quoted commercial facts; normalized comparison is derived product output unless separately governed |
| Product-specific extracted requirements, risk classification, economics and participation recommendation | product-owned semantics and outputs; any canonical admission must preserve provenance and must not convert AI/deterministic extraction into external truth |
| Operator review/approval evidence | governed organizational evidence attributable to the actual actor and applicable authority; technical authorization must not be treated as final Organizational Authority automatically |
| Final delivered report | governed product artifact with exact run/input/version association when admitted; delivery itself does not create truth for underlying external facts |

P6.02 must make the exact authority modes and failure behavior contractually explicit before governed reliance.

## 9. Data, security, rights and privacy constraints

The first real validation slice inherits the strictest currently evidenced product controls unless a separately governed decision narrows them lawfully:

1. real partner data must not be committed to either repository;
2. raw real documents remain in approved local/controlled runtime locations;
3. repository evidence uses synthetic, anonymized or safely redacted fixtures only;
4. partner-facing output must pass the product export/redaction guard and human delivery approval;
5. cross-Organization access is deny-by-default;
6. the Product Contract must not grant Authorization or Organizational Authority merely by declaring a dependency;
7. classification, purpose, minimization, retention/deletion and portability obligations must propagate through derived artifacts where applicable;
8. external system credentials/tokens/secrets must not enter canonical history, prompts or repository evidence;
9. AI analysis remains bounded, attributable and human-reviewed and cannot independently approve a final consequential bid decision;
10. no P6.01/P6.02 artifact creates rights to reuse one customer's documents, memory, outcomes or knowledge for another organization.

## 10. Why this target is suitable for Phase 6

The selected procurement workflow satisfies the P6.01 suitability test because it has all of the following at the same time:

- **real organizational value** — it is a commercial tender-operator workflow aimed at reducing operator effort and improving decision quality;
- **existing product readiness** — the product repository already contains restricted-pilot operation, data-handling, reporting and measurement machinery;
- **bounded scope** — the validation stops at a reviewed client-ready decision package and preserves manual external actions;
- **measurability** — active time, recall, usefulness, safety and commercial signals already have defined measurement semantics;
- **platform-semantic pressure** — exact document versions, governed artifacts, reconstruction, Organization isolation, authority and provenance are materially relevant rather than decorative;
- **product/platform separability** — procurement-specific relevance, risk, RFQ/TKP, economics and bid-decision semantics can remain product-owned;
- **reversibility** — the current product-local pilot contour already works independently enough to provide a rollback target;
- **negative-evidence value** — if CAP-001/CAP-004 reuse adds more friction than value, the result can support containment or return-to-product recommendations rather than being forced into platform success.

## 11. Exit and rollback path

The first real integration must remain removable without loss of product ownership or customer data control.

Rollback baseline:

1. the existing `ai-corporation` product remains the owner of procurement workflow/domain semantics;
2. P6.02 uses a `Provisional` Product Contract rather than a Stable/public contract;
3. integration occurs through the existing explicit product/platform boundary rather than direct platform tables, private imports or hidden state;
4. real customer data is not migrated irreversibly merely to validate the platform;
5. if the platform path fails value, security, rights, operability or delivery-friction checks, the product may return to its current local/manual pilot mechanisms;
6. any Arvectum OS records created for validation remain exportable/deletable under applicable policy and do not become the only inaccessible representation of required product/customer state;
7. no public API/SDK, SLA, compatibility or customer-support promise is created by the experiment;
8. rollback does not rewrite historical governed evidence already lawfully admitted; compensating/termination records are used where applicable.

## 12. P6.02 handoff

P6.02 must create the smallest sufficient `Provisional` Product Contract and bounded adoption plan for this exact target before any governed platform reliance.

The handoff must explicitly decide:

- product/consumer identity and Organization scope;
- exact required CAP-001/CAP-004 contract/dependency versions;
- whether CAP-003 is actually required or remains product-local/omitted;
- whether CAP-002 is omitted from the first slice unless real shared Memory/Knowledge reliance is demonstrated;
- Canonical Record interactions and exact authority modes for external tender documents and product outputs;
- allowed read, transient, canonical-mutation and external-side-effect classes;
- Event/provenance obligations and reconstruction boundary;
- document/artifact inputs, outputs, derivations, classifications and retention/deletion handling;
- Authorization versus Organizational Authority/approval responsibilities;
- failure, retry, incomplete-evidence and rollback behavior;
- portability and migration responsibilities;
- which procurement semantics remain product-owned;
- what integration/value/friction measurements begin at contract-adoption time.

No architecture change is required merely to write that Provisional Product Contract. If real adoption crosses a durable technology, Stable/public compatibility, persistence, event-delivery, IAM or service-topology threshold, the minimum sufficient ADR/RFC/policy gate must be reopened before material reliance.

## 13. P6.01 exit-criteria check

| Required evidence | Result | P6.01 disposition |
|---|---|---|
| named product/workflow owner and sponsor | `PASS` | `ООО «Арвектум»` recorded for both product ownership and Phase 6 sponsorship |
| concrete organizational/business outcome | `PASS` | measure platform leverage/control value against the existing tender-pilot product-local baseline |
| bounded workflow scope | `PASS` | real 44-ФЗ tender intake through reviewed client-ready pre-bid decision package; external actions excluded |
| current baseline for time/cost/quality/risk/manual effort where measurable | `PASS with explicit evidence gap` | measurement schema and required controls exist; empirical real-case values are marked not-yet-observed and must be captured, not guessed |
| platform capabilities/state/history actually required | `PASS` | CAP-001 and CAP-004 are the minimum evidence-backed dependency hypothesis; CAP-002/CAP-003 remain conditional rather than forced |
| authoritative external systems | `PASS` | ЕИС/zakupki.gov.ru and partner/supplier source documents remain external authorities within their scopes |
| data/security/rights constraints | `PASS` | real-data repository prohibition, export guard, Organization isolation, purpose/minimization and no cross-customer reuse preserved |
| explicit suitability reason | `PASS` | real readiness + measurable outcome + genuine document/reconstruction pressure + reversibility |
| exit/rollback path | `PASS` | retain product-local contour, Provisional contract only, no irreversible migration or public commitment |

**P6.01 result: PASS.** The first real validation target is sufficiently defined to proceed to P6.02 without changing platform behavior or inventing empirical baseline values.

## 14. Lifecycle, ADR, conformance and commercial disposition

P6.01 changes no lifecycle state.

- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- P4.08 and P5.09 reference Product Contracts remain `Provisional 0.1.0`;
- no real procurement Product Contract exists yet for the selected Phase 6 target until P6.02;
- no capability becomes `Active`;
- no Product Contract becomes `Stable`;
- no production-readiness approval is created;
- no public SDK/API/wire/package boundary is created;
- no SLA/support/customer compatibility promise is created;
- no full-platform conformance claim is made.

No ADR is required by P6.01 because the work item selects and bounds a real validation context without choosing a durable technology or compatibility boundary. P6.02/R17 must reopen the gate if the adoption plan crosses one.

## 15. Final state and next action

**P6.01 — Complete / PASS.**

Selected first real Phase 6 validation target:

> **Arvectum procurement/tender AI operator — bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package, with manual external actions retained.**

The next canonical action is:

> **P6.02 — First real Product Contract boundary + bounded adoption plan.**
