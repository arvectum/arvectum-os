# R17 — First Product Boundary Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Roadmap gate: `R17 — First Product Boundary Review`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone target: `M6 — Platform validated through real products and reuse evidence`
Reviewed Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`
Result: **`PASS — the first real Product Contract boundary remains minimal, externally authority-preserving, product-owned in domain semantics, fail-closed and reversible. P6.03 may begin with the Stage 1 synthetic/redacted proof only; real governed reliance remains staged behind that evidence.`**

## 1. Purpose and decision level

R17 is the independent product-boundary gate after P6.02 and before P6.03 creates implementation reliance on Arvectum OS.

It verifies the current real-product target, exact dependency set, authority model, product/platform responsibility split, Organization/security/rights behavior, failure/rollback semantics and architecture-choice containment. It is a review and planning gate, not a new platform architecture decision.

R17 does not:

- amend the Constitution or an Accepted RFC;
- change the P6.02 Product Contract lifecycle or version;
- promote a Platform Capability;
- create a Stable/public API, SDK, wire, package or service boundary;
- select production persistence, Event delivery, IAM, object-store, search/vector or service topology;
- approve production/operational readiness;
- grant Authorization, Organizational Authority or consequential approval;
- authorize automated external procurement, supplier or customer actions;
- claim full-platform conformance or create SLA/support commitments.

## 2. Canonical authority checked

R17 was evaluated against the current canonical repository state in authority order:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. `docs/rfc/README.md` — RFC-0001 through RFC-0008 remain `Accepted 1.0.0` with canonical acceptance evidence;
3. RFC-0001 — product/platform separation, minimal Provisional Product Contracts, capability lifecycle honesty, external authority, security/isolation, scoped conformance, proportionality and Commercial Commitment Integrity;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, exact consequential reliance, authority-mode preservation and non-authoritative projection semantics;
5. RFC-0003 — Organization sovereignty, deny-by-default Authorization, least privilege, Organizational Authority separation, Data Governance, minimization, retention/deletion, secrets and portability;
6. RFC-0004 — Product Contract lifecycle, exact dependencies/responsibilities, canonical-state and authority declarations, hidden-coupling prohibition, failure/migration requirements and product responsibility;
7. RFC-0005 — exact Product Contract attribution, Governed Execution, side-effect classes, independent authority/approval gates, retry/reconciliation and bounded AI authority;
8. RFC-0006 — append-only Event/provenance evidence, required-evidence failure behavior, reconstruction truthfulness and non-authoritative telemetry;
9. RFC-0007 — product-domain Memory/Knowledge remains product-owned unless explicitly governed through a Product Contract; no CAP-002 dependency is implied by product prompts/profiles/outcomes;
10. RFC-0008 — exact Document/Artifact identity/version reliance, external authority preservation, derivation provenance, handling propagation and non-authoritative derived representations;
11. `docs/adrs/README.md` — no Accepted ADR establishes a conflicting durable/public persistence, Event, IAM, storage, SDK/API or service-topology boundary;
12. `docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` — CAP-001 and CAP-004 Provisional `1.0.0` operation envelopes and ADR gates;
13. `docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md` — CAP-001 through CAP-004 remain `Incubating / Provisional`;
14. `docs/governance/DECISION-AUTHORITY-POLICY.md` — still `Proposed 0.2.1`; residual decision authority therefore remains with the owner under Accepted governance;
15. P6.01 target/evidence baseline, P6.02 boundary review and the P6.02 Product Contract;
16. current `ai-corporation` product evidence described below;
17. Phase 6 roadmap and canonical roadmap sequencing.

No conflict with Constitution `1.2.0`, Accepted RFC-0001 through RFC-0008 or an Accepted ADR was identified.

## 3. Independent real-target continuity check

R17 re-checked the P6.01 product evidence directly in `arutyunoveth/ai-corporation` rather than treating the P6.02 review as sufficient by itself.

The immutable evidence used by P6.01 is unchanged:

| Evidence | Current blob SHA | P6.01 SHA | R17 result |
|---|---|---|---|
| `README.md` | `614854a7ef3cca8448f4b346f12ce712fca24927` | same | `PASS` |
| `docs/demo/pilot_scope.md` | `8082d7d29f561112ca1de61902ab81a5c1550413` | same | `PASS` |
| `docs/demo/pilot_kpi_scorecard.md` | `b8bcab1a96e257b330724e79a293aeab8a5fd010` | same | `PASS` |
| `docs/product/Tender_Operator_RFQ_Workflow.md` | `e0f74644510dcd996bc2271259ceffae4dd6d1e5` | same | `PASS` |
| `docs/product/Restricted_Paid_Pilot_Operations_Runbook.md` | `ea5cae8e1410e2d4a87b099d505de6b3a8576d22` | same | `PASS` |
| `docs/product/Local_Pilot_Data_Handling_Policy.md` | `c3e9756a9e3142cfc3617b9d8e1721ea2b4eef54` | same | `PASS` |

The current product status still states restricted paid-pilot readiness with manual-control boundaries, human-reviewed LLM use, no broad autonomy, no external execution, no procurement-platform submission, no EDS/signature execution and no supplier email automation.

Repository search found no current `arvectum_os` / `arvectum-os` dependency in `ai-corporation`, so there is no pre-existing hidden platform coupling that R17 would be normalizing retroactively.

**Target continuity result:** `PASS`.

The reviewed target therefore remains:

> **Arvectum procurement/tender AI operator — bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package, with all external actions manual.**

## 4. Minimum dependency review

### 4.1 CAP-001 — required

CAP-001 remains the smallest domain-neutral dependency for the first slice because the workflow needs governed, exact, version-identifiable references for materially relied-upon tender inputs and the reviewed final artifact, plus material derivation provenance and handling constraints.

The product already has document intake and export behavior, but R17 does not treat generic file handling as platform value. The platform responsibility under review is the governed Document/Artifact identity/version/provenance/handling envelope defined by RFC-0008 and the Provisional CAP-001 contract.

Result: **`INCLUDE / PASS`** at exact Provisional capability contract `1.0.0`.

### 4.2 CAP-004 — required

CAP-004 remains the smallest reusable dependency for the Phase 6 reconstruction objective: one governed result must be reconstructable from exact Product Contract, Actor/Organization, workflow, materially relied-upon inputs, Event/provenance, review evidence and final-artifact references, while missing/redacted/deleted evidence is exposed honestly.

This is materially different from ordinary product logs or telemetry and matches the current CAP-004 Incubating boundary.

Result: **`INCLUDE / PASS`** at exact Provisional capability contract `1.0.0`.

### 4.3 CAP-002 — correctly omitted

The product has prompts, supplier context, risk methods, profiles, prior outcomes and domain learning concepts, but none creates a demonstrated dependency on shared Arvectum OS Memory/Knowledge for the first slice.

Moving those semantics into CAP-002 now would be speculative platformization and would violate the product-ownership boundary.

Result: **`OMIT / PASS`**.

### 4.4 CAP-003 — correctly omitted

The product has procurement discovery, EIS search, supplier relevance scoring, ranking and filtering. Those are procurement-domain behaviors and remain product-owned.

The first slice does not need shared governed discovery merely to validate CAP-001/CAP-004. Search/index technology or product ranking must not become an incidental platform dependency.

Result: **`OMIT / PASS`**.

### 4.5 RFC-0004 dependency-responsibility completeness

R17 specifically re-checked RFC-0004 Section 10.2 requirements for each dependency: capability identity/version/lifecycle, required operations, provider responsibility, consumer responsibility, failure/unavailability behavior and provisional status.

The P6.02 Product Contract satisfies these requirements semantically across Sections 4, 5, 7 and 12:

- Section 4 defines exact capability/version and operation envelopes;
- Sections 5 and 7 separate platform and product architectural responsibility without moving procurement meaning into the platform;
- Section 12 defines fail-closed contract/dependency/source/evidence behavior and permits only an explicit return to the product-local/manual contour;
- Incubating/Provisional status is explicit and no Active/Stable inference is permitted.

The declarations are distributed rather than repeated in one dependency table, but they are unambiguous for the bounded scope. R17 therefore does not mutate the admitted `0.1.0` Product Contract merely for documentary duplication.

Result: **`PASS — no Product Contract version change required.`**

## 5. External authority and canonical-state review

R17 confirms that P6.02 does not create a competing source of truth.

| Object / information | R17 disposition |
|---|---|
| ЕИС / zakupki.gov.ru registry facts and source documents | `External Reference`; external authority preserved |
| partner/customer tender files | `External Reference`; accepted source package remains authority for source content |
| supplier TKP/quote documents | `External Reference`; supplier/partner-origin document remains authority for quoted facts |
| extraction, risk, RFQ, normalization, economics, recommendation | product-owned transient/derived semantics by default |
| Governed Execution history | `Native` only for Arvectum OS execution/governance state |
| admitted Event/provenance/review evidence | `Native` only for the evidence act and attributable history |
| final reviewed report content | `External Reference` by default; platform governs exact reference/version/provenance, not underlying tender truth |
| Product Contract | `Native` within its declared Organization-scoped contract lineage |

`Governed Replica` remains deliberately unselected. If P6.03 proves synchronized external-source replication is actually necessary, a new Product Contract version must declare synchronization, freshness, conflict and failure semantics before reliance.

Result: **`PASS`**.

## 6. Product ownership review

The Product Contract continues to keep the following outside shared platform semantics:

- tender/case business meaning;
- 44-ФЗ interpretation;
- requirements and risk semantics;
- supplier questions and RFQ/TKP logic;
- supplier relevance and procurement search/ranking;
- quotation normalization/comparison;
- economics, margin and bid-readiness;
- participation recommendation;
- product validation/escalation;
- prompts, agents, models and domain configuration;
- operator UX and partner report narrative;
- customer pilot process and commercial packaging.

The platform boundary remains limited to existing domain-neutral Product Contract continuity, Organization/security/authority semantics, governed Document/Artifact handling, Governed Execution/Event/provenance and reconstruction semantics.

No procurement taxonomy, risk label, supplier ontology, RFQ schema, bid rule or product workflow state is promoted into Kernel/shared capability semantics.

Result: **`PASS`**.

## 7. Organization, security, rights and evidence review

R17 confirms the bounded path fails closed on the concerns that matter before real data enters the platform-backed route:

1. explicit Organization scope is mandatory; no ambient/default Organization is allowed;
2. Product, Product Contract, Actor, inputs, Execution Context, Events and governed outputs must resolve within the same Organization absent a separately governed cross-Organization contract;
3. cross-Organization access/reuse is denied by default;
4. Product Contract admission grants neither Authorization nor Organizational Authority;
5. canonical mutation still requires applicable Authorization, OrganizationalAuthority, DataGovernance and ConsequentialApproval gates through Governed Execution;
6. raw real partner/customer data remains outside both repositories and in approved controlled runtime locations;
7. repository evidence remains synthetic/anonymized/redacted;
8. partner-facing output retains the product export/redaction guard and human delivery approval;
9. purpose/right/classification/minimization/retention/deletion constraints propagate to material derived artifacts unless an explicitly governed transformation changes them;
10. secrets, credentials, EIS tokens and reusable authentication material remain outside canonical history, ordinary logs, prompts, repository fixtures and portable evidence packages;
11. reconstruction may not reveal content denied by current rights/classification/redaction state;
12. missing required evidence cannot silently become a complete reconstruction claim.

The Decision Authority Policy remains Proposed, so R17 does not infer delegated authority from it. Residual authority remains with the owner under the current Accepted governance baseline.

Result: **`PASS`**.

## 8. Side effects and human-control review

The admitted side-effect classes remain correctly bounded:

- `Read-only` — exact Document/Artifact resolution and CAP-004 reconstruction;
- `Transient` — product analysis and decision-support computation;
- `Canonical mutation` — only the bounded platform reference/execution/Event/review/final-artifact evidence needed for the governed path;
- `External mutation` — none;
- `Organizational commitment` — none through this Product Contract.

Client delivery, supplier communication, EIS/ETP submission, signature and final bid commitment remain manual/outside the automated platform contract.

AI remains an execution means and cannot independently grant authorization, create Organizational Authority or act as final consequential approver.

Result: **`PASS`**.

## 9. Reversibility and adoption-scope review

The adoption remains:

1. Stage 0 — P6.02 + R17 contract review;
2. Stage 1 — synthetic/anonymized/redacted integration proof;
3. Stage 2 — one real 44-ФЗ case;
4. Stage 3 — maximum three real calibration cases before P6.04/P6.05 evidence disposition.

R17 explicitly distinguishes this **platform-backed Phase 6 adoption cap** from the broader product pilot described in `ai-corporation`, which may contain up to 15 pilot cases. The Product Contract does not shrink or redefine the product pilot; it caps only the first Arvectum OS governed-reliance sample. Cases outside the Phase 6 cap may continue through the existing product-local/manual contour.

Rollback remains credible because:

- no historical bulk migration is required;
- existing product-local cases remain product-owned;
- the current local/manual restricted-pilot contour already exists independently;
- disabling the platform-backed path does not require private Arvectum OS implementation state to continue product operation;
- admitted immutable history is preserved or lawfully minimized/deleted with truthful reconstruction limits rather than rewritten;
- negative platform-value evidence is permitted as a valid Phase 6 result.

Result: **`PASS`**.

## 10. Hidden-coupling and architecture-choice review

R17 found no durable/public/stable choice smuggled into the Product Contract.

The boundary does not select or stabilize:

- a database or transaction mechanism;
- object/document storage technology;
- Event broker/store or delivery topology;
- IAM/PDP/PEP provider;
- workflow engine;
- search/vector/RAG technology;
- stable serialization or wire schema;
- public API/SDK/package;
- registry/plugin runtime;
- deployable service/process boundary;
- logging/SIEM/observability vendor;
- customer-facing compatibility or support contract.

Current product use of PostgreSQL/Alembic and current Arvectum OS Python/dataclass/token implementation shapes remain local/internal implementation facts. Neither becomes a shared platform obligation through P6.02/R17.

P6.03 must reopen the minimum sufficient ADR/RFC/policy/Product Contract gate before material reliance if implementation crosses one of these boundaries.

Result: **`PASS — no new ADR/RFC/policy required at R17.`**

## 11. R17 review matrix

| Gate | Result | R17 evidence/disposition |
|---|---|---|
| real target still matches P6.01 | `PASS` | all six checked product evidence blobs remain unchanged |
| CAP-001 exact dependency | `PASS` | Incubating / Provisional `1.0.0`; exact document/artifact governance need remains demonstrated |
| CAP-004 exact dependency | `PASS` | Incubating / Provisional `1.0.0`; reconstruction need remains demonstrated |
| CAP-002 omitted without dependency | `PASS` | domain Memory/Knowledge remains product-owned/local |
| CAP-003 omitted without dependency | `PASS` | procurement search/relevance remains product-owned |
| external authority preserved | `PASS` | EIS/partner/supplier source content remains externally authoritative |
| product-owned procurement semantics | `PASS` | no domain schema/workflow/knowledge/ranking/economics/risk promotion |
| Organization/isolation/security | `PASS` | explicit Organization, deny-by-default, fail-closed controls retained |
| rights/minimization/retention/deletion | `PASS` | propagation and truthful evidence-loss behavior explicit |
| contract does not grant permission/authority | `PASS` | Authorization/Organizational Authority remain separate runtime/governance decisions |
| human review / no automated external action | `PASS` | product safety baseline and Product Contract agree |
| reversible bounded adoption | `PASS` | synthetic → one real case → max three platform-backed calibration cases |
| hidden coupling prohibited | `PASS` | no existing `ai-corporation` Arvectum OS dependency found; P6.03 must prove no private fallback is needed |
| no durable/public/stable choice | `PASS` | ADR gate remains closed until actual implementation pressure crosses it |
| lifecycle/commercial integrity | `PASS` | no Active/Stable/Production/SLA/support claim |

## 12. Functional cross-review iterations

### Iteration 1 — architecture + product boundary

Review focus: dependency minimality, RFC-0004 completeness, product ownership and external authority.

Finding: CAP-001/CAP-004 remain sufficient and exact; CAP-002/CAP-003 would be speculative in this slice. RFC-0004 provider/consumer/failure responsibilities are distributed across the contract rather than duplicated in one table but remain unambiguous.

Disposition: **PASS; no Product Contract mutation justified.**

### Iteration 2 — security + privacy + authority

Review focus: Organization isolation, Authorization versus Organizational Authority, rights, minimization, retention/deletion, secrets, evidence disclosure and AI authority.

Finding: controls remain fail-closed and Product Contract admission creates no permission or authority. Proposed Decision Authority Policy is not treated as Accepted governance.

Disposition: **PASS.**

### Iteration 3 — engineering + operations + reversibility

Review focus: implementation-entry sequence, rollback, hidden coupling, evidence completeness and the relationship between the three-case platform sample and the broader product pilot.

Finding: adoption is reversible and prospective. The three-case cap applies to Arvectum OS governed reliance only; it does not redefine the product's broader pilot scope. No existing Arvectum OS dependency is present in the product repository.

Disposition: **PASS.**

### Iteration 4 — compatibility + ADR + governance + commercial integrity

Review focus: accidental stable/public interface, durable infrastructure pressure, capability/Product Contract lifecycle inflation and customer-facing commitments.

Finding: no ADR/RFC/public-boundary threshold is crossed by the contract. Current implementation technologies remain replaceable and internal/provisional. No Active/Stable/Production/SLA/support claim is created.

Disposition: **PASS; no further material R17 change remains.**

R17 stops after four iterations because the materially relevant roles have no unresolved stage-appropriate objection.

## 13. Gate decision and P6.03 entry conditions

**R17 — PASS.**

P6.03 is unblocked only within the existing bounded adoption sequence.

The first P6.03 increment MUST be **Stage 1 synthetic/anonymized/redacted proof**, not immediate real-data adoption. Before Stage 2 one-real-case reliance, Stage 1 must provide focused executable evidence that:

1. exact Product Contract `0.1.0` continuity is preserved;
2. CAP-001 and CAP-004 resolve to explicit current Provisional `1.0.0` provider/version evidence;
3. wrong-Organization access fails closed;
4. denied rights/classification/purpose fail closed;
5. missing/stale/incompatible dependency version evidence fails closed;
6. incomplete required reconstruction evidence is exposed rather than silently accepted;
7. no product-side private platform table/import/endpoint/Event/cache fallback is required;
8. no external mutation or organizational commitment path is introduced;
9. the changed-scope focused tests and applicable reference regression suite pass.

If Stage 1 reveals a durable/public/stable architecture requirement, an undeclared capability dependency, external-authority ambiguity, unenforceable rights/retention rule or hidden coupling, P6.03 must stop and reopen the minimum sufficient Product Contract/ADR/RFC/policy gate before real reliance.

## 14. Final disposition

- Constitution: unchanged;
- Accepted RFCs: unchanged;
- Accepted ADRs: none newly required;
- P6.02 Product Contract: remains `Provisional 0.1.0`;
- CAP-001 through CAP-004: remain `Incubating / Provisional`;
- CAP-001 + CAP-004: remain the only declared first-real-slice dependencies;
- CAP-002 + CAP-003: remain omitted;
- operational readiness / Production: not established;
- Stable/public compatibility: not established;
- commercial support/SLA commitments: not created;
- next canonical action: **`P6.03 — First real product/workflow platform integration`, beginning with Stage 1 synthetic/redacted proof.**
