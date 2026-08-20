# P8.00-A2 — Candidate Triage and Value Test

Status: `Complete / PASS`
Version: `1.0.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform` and `product_contract`
Roadmap work item: `P8.00-A2 — Candidate triage and value test`
Parent: [`P8.00 — Phase 8 Activation / External-Ecosystem Boundary Revalidation`](../roadmap/P8-00-PHASE-8-ACTIVATION-BOUNDARY-REVALIDATION.md)
Predecessor evidence: [`P8.00-A1 — External-Demand Evidence Inventory`](P8-00-A1-external-demand-evidence-inventory.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Result

**PASS — the three evidence-backed A1 candidates were qualitatively triaged and one candidate remains on the P8.00-A3 shortlist.**

Shortlist:

1. `A1-C01 — ЕИС / zakupki.gov.ru authoritative tender-document boundary` — `SHORTLIST_FOR_A3`.

Contained/deferred:

- `A1-C02 — Telegram controlled publication effect boundary` — `CONTAIN_PRODUCT_LOCAL / NOT_SHORTLISTED` because the strongest reusable external-effect evidence is already materially covered by M6/M7 and no current evidence shows that a broader Telegram/notification boundary should become Phase 8 platform work;
- `A1-C03 — Discount Parser public discount/promo source set` — `DEFER_RIGHTS_GAP / NOT_SHORTLISTED` because source-specific permitted-use, redistribution and retention scope is not canonically established and the implemented adapter/normalization behavior remains product-owned.

These labels are A2 triage dispositions only. They are not Platform Capability lifecycle states, Product Contract lifecycle states, architecture approvals or permanent rejection decisions.

A2 does **not**:

- select the final Phase 8 activation outcome;
- decide platform responsibility under A5;
- move the EIS connector into Arvectum OS;
- treat technical EIS access, token possession or successful retrieval as legal/contractual permission beyond the currently evidenced operating contour;
- authorize EIS mutation, customer-facing service, redistribution or cross-Organization use;
- create a generic Telegram/notification capability;
- centralize Discount Parser source adapters, crawling, normalization, deduplication or classification;
- activate Phase 8;
- create a Stable Product Contract, public/stable API or wire format, Active Platform Capability, external/customer Production scope, SLA/support commitment, certification or broader conformance claim.

## 2. Canonical authority checked

P8.00-A2 was checked against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. `docs/rfc/README.md` — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with recorded approval evidence;
3. RFC-0001 — organizational-value/proportionality rules, external authority modes, platform admission discipline, Product Experiment/Product Capability boundaries, lifecycle/commercial integrity and the requirement to prefer validated reuse over speculative generality;
4. RFC-0002 — external identifiers remain aliases/references, exact-version reliance, external authority preservation and technology-independent Canonical Record semantics;
5. RFC-0003 — Identity/Authentication/Authorization/Organizational Authority/Data Governance separation, deny-by-default behavior, least privilege, secrets handling and cross-Organization rights boundaries;
6. RFC-0004 — Product Contract before governed platform reliance, product-local bounded behavior may remain product-local, hidden coupling is prohibited and platform promotion requires a separate evidence-based decision;
7. RFC-0005 — external side-effect classification, explicit authority/approval, idempotency, uncertainty/reconciliation and product-owned workflow semantics;
8. RFC-0006 — external Event/provenance authority, duplicate/replay safety, evidence completeness and failure-closed behavior;
9. `docs/adrs/README.md` and current `docs/adrs/` contents — no Accepted ADR currently selects a permanent external connector, public API/wire format, external trust protocol, broker, connector/plugin protocol or external deployment topology;
10. the canonical master roadmap, P8.00 activation plan and Phase 8 draft roadmap;
11. `P8.00-A1` candidate inventory;
12. P6.02 Tender Operator and P6.06 Discount Parser Provisional Product Contracts and the real-use evidence summarized by A1.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was identified. No RFC or ADR is required merely to record the A2 triage result.

## 3. Triage method

A2 evaluates only the three named A1 candidates. A1 evidence leads that do not name an external party/recipient/consumer are not promoted into candidates by inference.

Each candidate is assessed qualitatively against the eight dimensions required by the P8.00 plan:

1. **real organizational value now** — whether the external boundary currently supports a real Arvectum outcome rather than a hypothetical future use;
2. **consequence and reversibility** — whether the validation can remain bounded and recoverable without creating unnecessary consequential external effects;
3. **external dependency maturity/readiness** — whether the current external integration path has enough exercised behavior to support a bounded next validation without pretending the dependency is controlled by Arvectum OS;
4. **authority/data-rights clarity** — whether current evidence identifies the authoritative source and enough rights information to determine what remains unresolved and must fail closed before broader use;
5. **distinctness from M6/M7 internal validation** — whether Phase 8 can add materially new external-ecosystem evidence rather than rerun an already proven owner-operated case;
6. **ability to generate reusable platform evidence** — whether the boundary can test domain-neutral platform semantics such as authority preservation, exact-version reliance, provenance, failure behavior, governed external effects or interoperability without importing product business logic;
7. **cost of keeping the mechanism product-local** — whether the current product-local implementation already satisfies the real need cheaply enough that platform generalization would be speculative;
8. **risk of premature stable/public commitment** — whether pursuing the candidate is likely to harden a public/stable API, protocol, connector surface, rights commitment or support obligation before evidence justifies it.

A2 deliberately does not assign synthetic numeric weights or fabricated business-value estimates. Terms such as `strong`, `moderate`, `weak`, `clear`, `partial` and `blocking` summarize only the evidence currently available.

## 4. Comparative triage

| Candidate | Value now | Consequence / reversibility | External readiness | Authority / rights clarity | Distinctness from M6/M7 | Reusable platform evidence | Cost of staying product-local | Premature-stability risk | A2 disposition |
|---|---|---|---|---|---|---|---|---|---|
| `A1-C01` ЕИС / `zakupki.gov.ru` | Strong | Favorable for a bounded read-only case; no mutation required | Moderate; real retrieval works, but trust/availability remain external | Authority is clear; rights are incomplete. Current evidence supports only a bounded candidate under deny-by-default, not a broader legal/contractual permission claim | Moderate; prior M6 retrieval exists, so A3 must define a new bounded outcome rather than repeat it | Strong for external-authority, exact-version/provenance and fail-closed integration evidence | Low today; connector can remain product-owned | Low if kept read-only/provisional; higher if generalized into a stable connector/API | `SHORTLIST_FOR_A3` |
| `A1-C02` Telegram effect boundary | Real but bounded | Consequential external publication; replay/duplicate risk requires controls | Strong for the current controlled test path | Partial; owner-controlled test target and secret boundary are known, broader customer/cross-Organization rights are not | Weak; M6/M7 already proved controlled publication plus reconstruction without replay | Moderate, but largely duplicates already proven RFC-0005/RFC-0006 pressure | Low; product publisher/ledger already owns the behavior | Moderate if reframed as generic notification/Telegram infrastructure | `CONTAIN_PRODUCT_LOCAL / NOT_SHORTLISTED` |
| `A1-C03` public discount/promo sources | Real for Discount Parser | Read-oriented collection is bounded, but downstream use/redistribution may create rights exposure | Moderate; multiple adapters already implement retry/backoff and failure isolation | Blocking for broader Phase 8 use because source-specific permitted-use/redistribution/retention scope is not canonical | Weak-to-moderate; the source set already exists inside the M6 product contour | Weak-to-moderate; generic external-source provenance is reusable, but parsing/dedup/classification remain product-specific | Low; Source SDK/adapters already exist product-locally | High if volatile source adapters or uncertain rights are generalized into platform commitments | `DEFER_RIGHTS_GAP / NOT_SHORTLISTED` |

The table expresses comparative evidence, not a lifecycle decision, legal opinion or formal risk rating.

## 5. Candidate analysis

### 5.1 A1-C01 — ЕИС / zakupki.gov.ru

#### Real organizational value now

The Tender Operator already depends on exact tender-source documentation for a real procurement workflow. The value is not hypothetical: exact source-document identity, version and provenance affect what the product is allowed to rely on and what a later reviewer can reconstruct.

This is stronger Phase 8 material than simply adding another connector because ЕИС is an external authoritative system whose availability, certificate/trust behavior and source state are outside Arvectum OS control.

#### Consequence and reversibility

The evidenced path is read-only. A bounded read-only validation can preserve the real external authority while avoiding EIS/ETP mutation, application submission, signature, supplier communication or another organizational commitment.

That makes the candidate comparatively suitable for pre-activation work: it can generate external-boundary evidence without requiring a high-consequence external mutation.

#### External dependency maturity/readiness

The current path has exercised real retrieval evidence, including one fail-closed TLS trust problem and a later successful exact-document retrieval with certificate verification preserved.

This is enough to show that the dependency is real and operationally imperfect. It is not evidence that EIS is under Arvectum control, that availability is guaranteed or that any customer-facing SLA is supportable.

#### Authority and rights clarity

The authority boundary is clear enough for A2: EIS remains authoritative for the registry/source-document scope and the current default authority mode is `External Reference`.

The rights boundary is not equivalently complete. Canonical evidence proves that a bounded read-only retrieval path has been exercised inside the current Tender Operator contour and that handling/export restrictions exist; it does **not** by itself establish a comprehensive legal or contractual permission basis for Phase 8 use. Technical access, possession of an individual-person token or successful retrieval does not create such rights.

A3 may therefore keep EIS on the shortlist only as a bounded candidate under deny-by-default assumptions. A4 must explicitly map purpose, legal/contractual rights, credential use, classification, disclosure, retention, deletion and export constraints before any selected outcome is treated as authorized beyond the already evidenced operational contour.

Broader mutation, redistribution, customer-facing service and cross-Organization reuse remain unresolved and must not be inferred.

#### Distinctness from M6/M7

Distinctness is not automatic. M6 already proved one real exact EIS retrieval path as part of the owner-operated Tender Operator validation.

Therefore A3 must not define the Phase 8 outcome as merely “retrieve another tender from ЕИС” or “repeat P6.05-L7.” A valid A3 outcome must identify what materially new external-ecosystem property is being validated beyond the prior internal product proof.

If A3 cannot identify such a bounded new outcome without inventing demand, widening rights or creating a premature stable connector commitment, the correct disposition is `DEFER`, even though C01 is the A2 shortlist leader.

#### Reusable platform evidence potential

The strongest reusable evidence is domain-neutral and sits around the connector rather than inside procurement logic:

- preservation of an external authoritative source instead of creating competing local truth;
- exact source/reference/version/freshness evidence when materially relied upon;
- fail-closed handling when external trust or retrieval evidence is insufficient;
- provenance from external source reference into a governed execution;
- explicit separation between product-owned tender discovery/parsing and platform-owned governed reliance/reconstruction semantics.

A2 does not conclude that these pressures require new platform ownership. That is A5.

#### Cost of keeping the mechanism product-local

Current evidence shows low pressure to move the EIS connector itself into the platform. Tender Operator already owns procurement discovery/intake behavior, and the Product Contract explicitly keeps procurement search and product-owned integrations outside the platform unless later evidence proves otherwise.

This is compatible with shortlisting the **external-authority boundary** while keeping the **connector implementation** product-owned.

#### Premature stable/public commitment risk

Risk is containable if the next validation remains read-only, bounded, provisional and explicit that no stable/public EIS connector contract exists.

Risk rises materially if the work is reframed as a universal government-system connector, public API, externally supported compatibility promise or customer Production dependency before A6 and later governance gates.

**A2 disposition:** `SHORTLIST_FOR_A3`.

### 5.2 A1-C02 — Telegram controlled publication effect boundary

#### Real organizational value now

The Discount Parser publication path has real operational value and exercises a consequential external effect. The prior controlled run demonstrated explicit authorization, durable pre-send intent/idempotency state, one Telegram send, confirmed external message identity and later reconstruction with zero effect replay.

#### Distinctness and reusable evidence

That same success is why C02 is not currently the strongest Phase 8 activation candidate. M6/M7 already used this boundary specifically to validate a materially distinct real external-effect workflow and reconstruction path.

A new Phase 8 Telegram case would need a genuinely new external relationship, authority scope, external consumer or other ecosystem property to avoid merely repeating the existing proof. A1 found no such evidence.

The reusable side-effect semantics — authorization, idempotency, uncertain outcome, reconciliation, replay safety and provenance — are already part of Accepted RFC-0005/RFC-0006 and have real product evidence.

#### Product-local sufficiency

The Telegram publisher, rendering, channel semantics, publication ledger and duplicate-prevention implementation are product-owned and already fit the bounded product need. No evidence shows that a generic Telegram/notification capability would remove meaningful duplicated responsibility across products.

**A2 disposition:** `CONTAIN_PRODUCT_LOCAL / NOT_SHORTLISTED`.

Containment means:

- retain the current Telegram integration as product-owned;
- keep using it as regression/operational evidence where relevant;
- do not use it as the P8.00-A3 activation candidate on present evidence;
- reconsider only if new evidence introduces a materially distinct external consumer/Organization/effect boundary or repeated cross-product need.

### 5.3 A1-C03 — Discount Parser public discount/promo source set

#### Real organizational value now

The source set is real and central to Discount Parser operation. The product already owns collection, retry/backoff, source/row failure isolation, normalization, deduplication, classification and offer lifecycle semantics.

#### Rights boundary

The decisive A2 weakness is not technical immaturity. It is the unresolved source-specific rights basis.

Current canonical evidence does not establish exact terms of use, redistribution rights, retention limits or a Phase 8 contractual basis for broader use. Technical accessibility of a public page does not create legal/contractual permission to generalize its use into a shared external platform boundary.

Under RFC-0003 and the P8.00 plan, unresolved rights remain deny-by-default for broader use.

#### Product-local sufficiency and platform evidence

Most implemented complexity is product-specific:

- source parsing;
- normalization;
- source-specific extraction;
- deduplication;
- classification;
- Offer lifecycle and publication eligibility.

Generic external-source provenance/failure semantics may be reusable, but current evidence does not show enough duplicated cross-product responsibility to justify platformizing these adapters or their domain semantics.

#### Premature commitment risk

Generalizing volatile public-source adapters before rights and repeated-use evidence exist would create an unnecessary maintenance/compatibility surface and may accidentally imply supported data access or redistribution rights that have not been established.

**A2 disposition:** `DEFER_RIGHTS_GAP / NOT_SHORTLISTED`.

Re-entry into A2/A3 consideration requires new evidence sufficient to resolve the blocking rights scope and show a concrete Phase 8 outcome beyond the existing Discount Parser product-local contour.

## 6. Shortlist and A3 guardrails

The A2 shortlist contains exactly one candidate:

1. **ЕИС / `zakupki.gov.ru` authoritative tender-document boundary.**

This is a shortlist, not an activation selection or platform-responsibility approval.

P8.00-A3 must now either:

- define one bounded EIS-related external outcome that is materially new relative to the M6/M7 evidence and remains deny-by-default for unresolved rights until A4 maps them explicitly; or
- record `DEFER` rather than recycling the prior P6 retrieval proof or inventing a broader external demand.

A3 must not select:

- “build a generic EIS connector” as a technology goal;
- EIS/ETP mutation, bid submission or digital-signature action without separate authority/rights/governance evidence;
- a public/stable API or universal government-system integration surface;
- customer-facing Production/SLA/support scope;
- a second Organization, portability recipient or external consumer that has not been named by evidence.

## 7. Cross-review

A functional cross-review was applied to the A2 triage before closure.

### Iteration 1 — platform / product boundary

**Finding:** ranking EIS above the other candidates could be misread as a decision to migrate the EIS connector into Arvectum OS.

**Revision:** the artifact now distinguishes the shortlisted **external-authority boundary** from the product-owned **connector implementation** and explicitly reserves platform-responsibility judgment for A5.

**Result:** no material product/domain leakage remains.

### Iteration 2 — value / novelty / roadmap integrity

**Finding:** Telegram has strong real evidence, so a simple maturity-based comparison would incorrectly favor it despite Phase 6 already proving the same external-effect pressure.

**Revision:** distinctness from M6/M7 is treated as a material triage dimension; Telegram is contained because a new Phase 8 case would currently duplicate prior evidence rather than create a materially new ecosystem relationship.

**Result:** the shortlist now reflects incremental organizational/evidence value rather than implementation maturity alone.

### Iteration 3 — security / rights / data governance

**Finding:** technical accessibility could be mistaken for sufficient rights both for EIS retrieval and for the public discount-source set. In particular, successful EIS access or token possession must not be presented as a comprehensive legal/contractual rights basis.

**Revision:** EIS authority is now separated explicitly from incomplete rights evidence; A4 must map purpose/legal/contractual/credential/data-governance scope before broader reliance. The public-source permitted-use, redistribution and retention gap remains a blocking A2 condition for broader Phase 8 use.

**Result:** no material authority or rights overclaim remains.

### Iteration 4 — operations / evidence integrity

**Finding:** EIS was also exercised in M6, so shortlisting it could still result in a cosmetic replay of old evidence.

**Revision:** A3 is explicitly required to identify a materially new bounded external outcome; repeating the existing P6 retrieval is not enough, and `DEFER` is the required result if no new bounded outcome can be justified.

**Result:** `PASS`; no remaining material objections were identified. Further changes would be editorial rather than substantive.

This functional cross-review is not formal owner approval, A5 platform-responsibility approval, Phase 8 activation, lifecycle promotion or operational-readiness approval.

## 8. A2 closure and handoff

P8.00-A2 exit criteria are satisfied:

- all three evidence-backed A1 candidates were qualitatively triaged against the eight required dimensions;
- no synthetic demand, business-value metric, SLA or rights claim was invented;
- the shortlist contains no more than three candidates and in fact contains one;
- Telegram is explicitly contained product-locally on current evidence;
- the public discount/promo source set is explicitly deferred because of the unresolved rights gap and product-local sufficiency;
- EIS remains the sole A3 candidate without implying connector platformization or broader legal/contractual rights;
- Phase 8 remains `Draft / Exploratory`.

The correct next canonical action is:

> **P8.00-A3 — Select one bounded external outcome.**

A3 must either identify a materially new bounded EIS-related external outcome under deny-by-default unresolved-rights assumptions or record `DEFER`. P8.01 remains unauthorized until the remaining P8.00 gates and fresh owner activation decision are complete.