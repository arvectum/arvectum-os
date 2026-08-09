# P6.04 — Product value, delivery-friction + governance evidence capture

Status: `Complete / PASS`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`, `product_specific` and `governance`
Phase: `Phase 6 — Product-driven Platform Validation`
Milestone: `M6 — Platform validated through real products and reuse evidence`
Predecessor: [`P6-03-stage-2-one-real-44fz-case-review.md`](P6-03-stage-2-one-real-44fz-case-review.md), `PASS`
Real product: `arutyunoveth/ai-corporation`
Real case: `0344100006426000005` — «Поставка кабельной продукции»
Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`

## 1. Decision

**PASS — P6.04 is complete for the first-real-use evidence-capture scope.**

The first real integration produced a mixed result that is more useful than an automatically positive platform score:

1. **Governance/control value is directly evidenced.** The real case preserved external authority, exact Product Contract lineage, exact capability-provider evidence and reconstructability, and it failed closed rather than fabricating a client-ready result when required source evidence was incomplete.
2. **The intended end-to-end product outcome was not completed.** The current contour retained normalized public facts and exact external references but not the exact bytes/digests of the complete seven-document tender attachment set. The product therefore correctly returned `NOT_CLIENT_READY_EVIDENCE_INCOMPLETE`.
3. **The integration is not cost-free.** Repository change evidence shows a material implementation/testing footprint on both product and platform sides. That footprint is measurable as code/change surface, but there is no reliable active-engineering-time capture, so it MUST NOT be converted into invented hours or cost.
4. **Economic and operator-speed value remain unproven.** P6.01 deliberately recorded manual-time, recall and usefulness baselines as not-yet-observed. One Stage 2 case blocked before a client-ready result cannot establish time reduction, operating-cost reduction, recall improvement or customer usefulness.

The evidence therefore supports **positive governance value, material delivery friction, and insufficient evidence for a net economic/productivity claim**.

P6.05 may remediate the demonstrated attachment-evidence blocker, but P6.04 does not pre-select the architecture or ownership of that remedy.

## 2. Canonical basis checked

P6.04 was checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0` with recorded acceptance evidence;
- RFC-0001 — organizational value, evidence over intuition, Product/Platform separation, external authority, scoped conformance, proportionality and no automatic capability promotion;
- RFC-0002 — exact immutable version reliance, external authority preservation, canonical-state honesty and no silent substitution of authority;
- RFC-0003 — Organization isolation, deny-by-default access and no authority by technical capability;
- RFC-0004 — explicit versioned Product Contract, exact dependencies and hidden-coupling prohibition;
- RFC-0005 — Governed Execution boundary for consequential canonical mutation and side effects;
- RFC-0006 — required evidence paths fail/pause or expose incomplete state rather than silently claiming complete success;
- RFC-0008 — exact Document/Artifact identity/version/provenance requirements and truthful incomplete source-package handling;
- `docs/adrs/README.md` — no Accepted ADR establishes a conflicting durable technology or public/stable compatibility choice for this evidence-capture task;
- P6.01 baseline, P6.02 Product Contract, R17, P6.03 Stage 1 and P6.03 Stage 2 closure evidence.

No higher-priority canonical conflict was identified.

## 3. Measurement rules

P6.04 distinguishes four evidence classes:

- **Observed** — directly demonstrated in executable or repository evidence;
- **Measured proxy** — objective repository/runtime evidence that measures change surface or control behavior but is not itself a business KPI;
- **Not yet observed** — a defined metric for which no defensible empirical value exists yet;
- **Not applicable in this slice** — a metric outside the bounded Stage 1/Stage 2 contour.

Target thresholds from the product pilot scorecard are not substituted for measurements. PR timestamps, lines changed and commit counts are not treated as active engineering time. Test counts are not treated as customer value by themselves.

## 4. Product-value evidence matrix

| Outcome | P6.01 baseline | P6.03/P6.04 evidence | Measurement state | P6.04 disposition |
|---|---|---|---|---|
| Exact external authority | no Phase 6 real-platform case yet | real notice represented as `External Reference`; no `Native` substitution | **Observed: 1/1 real case preserved external authority** | positive platform value |
| Exact Product Contract continuity | no real Product Contract before P6.02 | exact `0.1.0` lineage retained through Stage 1 and Stage 2 | **Observed: 1/1 real case** | positive governance value |
| Exact capability dependency evidence | no real dependency evidence before P6.02 | exactly CAP-001 + CAP-004, each with Provisional provider contract `1.0.0`; CAP-002/CAP-003 omitted | **Observed: 2/2 declared capability dependencies exact** | positive control/minimality value |
| Reconstruction/explainability | product-local baseline existed but no comparable Arvectum OS real-case measure | CAP-004 reconstructed the platform-backed real-case acts; incomplete evidence remained explicit | **Observed: 1/1 real case reconstructable within retained evidence** | positive explainability value |
| Evidence honesty / fail-closed behavior | safety requirement existed | missing complete source package produced `NOT_CLIENT_READY_EVIDENCE_INCOMPLETE`, not a fabricated recommendation | **Observed: 1/1 real case stopped truthfully** | strong governance/risk value |
| External action safety | required baseline = `0` automated external actions | no supplier/customer communication, EIS/ETP mutation, submission, signature or payment | **Observed: 0 external actions** | no regression |
| Human-review boundary | required baseline = human review for delivered result | no client-ready delivery was claimed; disposition remained product/human-review owned | **Observed within bounded case** | no regression |
| Complete tender source package | no Phase 6 platform-backed real case yet | public source listed seven tender documents; exact bytes/digests of those attachments were not retained by the run | **Observed blocker: 0/7 exact attachment bytes/digests retained by this run** | material negative delivery friction |
| Client-ready end-state completion | intended workflow target ends at reviewed client-ready package | real Stage 2 disposition was incomplete | **Observed: 0/1 real case reached client-ready state** | blocker; do not generalize beyond one case |
| Manual active operator time | `T0 = not yet observed` | Stage 2 does not provide a comparable completed manual/platform pair | **Not yet observed** | no speed claim permitted |
| Critical-requirement recall | empirical baseline not yet observed | source package incomplete; no defensible completed-case comparison | **Not yet observed** | no quality-uplift claim permitted |
| Critical-risk recall / false criticals | empirical baseline not yet observed | source package incomplete; no completed gold-standard comparison | **Not yet observed** | no quality-uplift claim permitted |
| Operator usefulness | empirical baseline not yet observed | no completed client-ready report from Stage 2 | **Not yet observed** | no usefulness claim permitted |
| Operating cost | no empirical baseline | no active-time/cost capture | **Not yet observed** | no cost-reduction claim permitted |
| Portability benefit | architecture remains technology-independent and source references are explicit | no migration exercise performed in this real slice | **Not yet observed as business outcome** | architecture property retained, benefit not quantified |

## 5. Integration-effort and platform-overhead evidence

### 5.1 Objective repository change footprint

The first-real-use contour required material implementation and proof work.

| Change set | Repository | PR | Commits | Changed files | Additions | Deletions | Evidence meaning |
|---|---|---:|---:|---:|---:|---:|---|
| P6.03 Stage 1 product bridge | `ai-corporation` | `#140` | `6` | `5` | `202` | `0` | product-side bridge, structural guards and cross-repository proof |
| P6.03 Stage 2 real case | `ai-corporation` | `#141` | `9` | `9` | `687` | `0` | one-real-case evidence, tests and dedicated CI proof |
| P6.03 Stage 1 platform repair/proof | `arvectum-os` | `#77` | `10` | `9` | `1223` | `45` | RFC-0002 External Reference/Replica reference semantics plus Stage 1 proof |
| **PR metadata aggregate** | both | three PRs | **25** | **23 file-touches** | **2112** | **45** | objective change-surface proxy; not unique-file count and not engineering hours |

Interpretation:

- product-side P6.03 additions total `889` across `14` PR file-touches;
- platform-side Stage 1 additions/deletions total `1223/45` across `9` PR file-touches;
- the platform repair was not speculative feature growth: it closed a real mismatch where the reference implementation could name RFC-0002 external authority modes but could not admit them truthfully;
- nevertheless, the footprint is evidence that governed integration has non-trivial delivery overhead and must earn its keep through reusable value.

These figures MUST NOT be read as:

- active engineering hours;
- monetary cost;
- unique lines permanently attributable to platform overhead;
- net productivity loss or gain;
- customer-facing feature volume.

### 5.2 Test and validation overhead

Stage 1 platform validation ran `713/713` reference tests, including all `9` new P6.03 Stage 1 tests. Product Stage 1 and Stage 2 each added dedicated hosted cross-repository jobs, while full product quality, security, migration, PostgreSQL/R8 and Redis jobs remained green.

This creates two simultaneous findings:

- **benefit:** exact boundary regressions, authority substitution, hidden coupling, Organization/rights failures and incomplete-evidence behavior are executable rather than informal;
- **overhead:** cross-repository compatibility proof and pinned provider evidence add maintenance surface compared with a purely product-local path.

No current evidence quantifies the recurring CI time/cost attributable only to Arvectum OS, so P6.04 records the overhead qualitatively and structurally rather than inventing a monetary value.

## 6. Concrete delivery friction

The first demonstrated blocker is narrowly defined:

> The current CAP-001/CAP-004 read-oriented integration contour can govern and reconstruct an exact external procurement reference, but the end-to-end path used in P6.03 does not retain/admit the exact complete external tender attachment package required by the product to truthfully complete its client-ready decision package.

For the real case:

- public source set: `7` listed tender documents;
- exact attachment bytes/digests retained by the Stage 2 run: `0/7`;
- normalized public-fact payload: integrity-protected by one explicit SHA-256 digest;
- exact source references: retained;
- client-ready disposition: blocked;
- automated external action: none.

This is not evidence that CAP-001 or CAP-004 are intrinsically wrong abstractions. It is evidence that the **current bounded contour is insufficient for the declared product outcome**.

P6.05 must therefore address the demonstrated source-package completeness problem at the minimum sufficient level. It must not infer from this one case that all external document retrieval belongs in the platform, that CAP-002/CAP-003 are needed, or that a durable storage/service topology has been selected.

## 7. Governance and risk value

The strongest positive P6.04 evidence is risk/control value rather than speed.

### 7.1 False-authority prevention

Stage 1 discovered that the reference runtime could not truthfully represent RFC-0002 `External Reference`/`Governed Replica` admission. The implementation was repaired instead of substituting `Native` merely to make integration pass.

Measured consequence:

- false `Native` substitution in the exercised contour: `0`;
- external-authority real case preserved: `1/1`.

### 7.2 Incomplete-evidence prevention

Stage 2 had enough normalized public facts to produce a plausible-looking procurement analysis, but not enough retained source evidence to support the intended client-ready designation.

Measured consequence:

- fabricated client-ready positive dispositions: `0`;
- explicit incomplete disposition: `1/1` real case;
- unsupported external commitments: `0`.

This is direct evidence for the Constitution/RFC rule that required evidence paths must not fail silently.

### 7.3 Domain-boundary preservation

No procurement semantics were moved into shared platform behavior. CAP-002/CAP-003 remained omitted. Procurement interpretation, completeness judgment and recommendation ownership remained in `ai-corporation`.

Measured consequence:

- platform capabilities used: `2` (`CAP-001`, `CAP-004`);
- speculative additional capabilities added to the Product Contract: `0`;
- product-domain capability promotions: `0`;
- Platform Capability promotions to `Active`: `0`.

## 8. What P6.04 cannot honestly conclude

P6.04 does **not** establish that Arvectum OS currently:

- reduces tender-processing active time by the product target of `≥30%`;
- improves critical-requirement recall to `≥90%`;
- improves critical-risk recall to `≥85%`;
- achieves operator usefulness `≥4.0/5`;
- lowers monetary operating cost;
- completes the first declared real workflow end-to-end;
- has proven cross-product reuse;
- should promote CAP-001 or CAP-004 to `Active`;
- should stabilize the P6.02 Product Contract;
- should expose a public SDK/API or create production/SLA/support commitments.

Those conclusions would exceed the available evidence.

## 9. Evidence gaps carried forward

The following gaps remain explicit:

1. **Manual baseline gap** — no completed three-case manual calibration set with active-time evidence exists in the canonical evidence used by P6.04.
2. **Completed-case comparison gap** — Stage 2 stopped before client-ready completion, so no paired completed manual/platform run exists for speed, recall or usefulness comparison.
3. **Cost gap** — engineering and recurring CI cost were not time-tracked in a way that can be defensibly converted into currency or active hours.
4. **Portability gap** — portability semantics are preserved architecturally, but no migration/export exercise in this real product slice quantifies operational benefit.
5. **Cross-product gap** — only the first real product context exists; cross-product reuse remains P6.06–P6.08 scope.

These are measurement gaps, not permission to invent estimates.

## 10. P6.05 handoff — evidence-backed problem statement only

P6.05 receives one **P0 product-outcome blocker** from P6.04:

> Enable the first real workflow to obtain and govern sufficient exact external tender attachment evidence to support a truthful client-ready completeness decision, while preserving external authority, exact version/provenance, Organization/rights controls, product ownership of procurement semantics and current no-external-action boundary.

P6.05 must first decide the minimum sufficient responsibility boundary. Permissible dispositions remain open, including product-local retrieval with governed platform admission, bounded CAP-001 functionality, Product Contract clarification, or another subordinate implementation choice.

P6.04 explicitly does **not** select:

- an EIS/Fabrikant client implementation;
- a storage backend;
- a document service topology;
- a public API/SDK;
- CAP-002/CAP-003 adoption;
- automatic external mutation;
- a Stable Product Contract;
- an `Active` capability lifecycle transition.

If the selected remediation becomes durable, cross-cutting, externally constraining or public/stable, the minimum sufficient ADR/RFC/Product Contract/policy gate must be reopened before material reliance.

## 11. Stage 3 calibration-cap disposition

The remaining P6.02 Stage 3 capacity stays unconsumed at P6.04 closure.

Reason:

- the current contour's blocker is already known;
- more unchanged cases would mostly re-demonstrate missing complete attachment evidence;
- the next useful calibration case should test a materially changed evidence contour after P6.05, not increase case count ceremonially.

Current consumption remains `0` additional Stage 3 cases.

## 12. Lifecycle, conformance and commercial integrity

At P6.04 closure:

- P6.04: `Complete / PASS` for evidence capture;
- CAP-001: `Incubating / Provisional`;
- CAP-004: `Incubating / Provisional`;
- CAP-002/CAP-003: unchanged and omitted from the real Product Contract;
- P6.02 Product Contract: `Provisional 0.1.0`;
- first real Stage 2 case: not client-ready due incomplete retained source package;
- no Platform Capability is `Active`;
- no Stable/public compatibility boundary exists;
- no production-readiness/SLA/support claim exists;
- no net productivity, cost-reduction or customer-quality claim is made from insufficient evidence.

## 13. P6.04 result summary

| Dimension | Result |
|---|---|
| Governance/control quality | **Positive, directly evidenced** |
| External-authority integrity | **Positive, 1/1 real case** |
| Exact dependency/contract continuity | **Positive, directly evidenced** |
| Reconstruction/explainability | **Positive within retained evidence** |
| Operator/product outcome completeness | **Negative: 0/1 client-ready completion** |
| Exact attachment evidence completeness | **Negative: 0/7 retained exact attachment bytes/digests** |
| Integration/change footprint | **Material and measurable as repository surface** |
| Delivery speed | **Unknown / not yet observed** |
| Recall/usefulness | **Unknown / not yet observed** |
| Operating cost | **Unknown / not yet observed** |
| Net platform value | **Not yet reducible to one scalar; positive governance value + material delivery blocker** |

## 14. Next canonical action

> **P6.05 — Platform-gap remediation from first real use.**

P6.05 must remediate only the evidence-backed first-real-use gap and preserve the successful authority, exact-version, Product Contract, reconstruction, Organization/security and product-boundary behavior demonstrated by P6.03/P6.04.

R18 remains after P6.05, where the measured value/friction findings and the actual remediation can be reviewed together.
