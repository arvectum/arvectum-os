# INT-B1 — Functional Cross-Review

Status: `Complete`
Date: `2026-08-22`
Artifact: [`INT-B1 — Integration Portfolio Baseline`](../architecture/INT-B1-integration-portfolio-baseline.md) `1.0.0`
Task classification: `platform` with `product_contract` and `product_specific` boundaries
Maximum iterations: `7`
Iterations completed: `3`
Result: `PASS after bounded reconciliation`

## 1. Review purpose

Review INT-B1 for functional completeness, product/platform boundary integrity, external-authority preservation, security/governance correctness and sequencing usefulness before roadmap closure.

This is functional cross-review evidence. It is **not** RFC/ADR acceptance, Product Contract approval, Platform Capability promotion, operational-readiness approval or commercial approval.

## 2. Review baseline

Checked against:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Platform Capability Catalog `1.2.1`;
- `PARALLEL-WORKSTREAMS-POST-M9-ALPHA.md` `1.0.0`;
- canonical roadmap `2.88.0` at review start.

## 3. Iteration 1 — Architecture / boundary review

### Material questions

1. Does the portfolio accidentally turn common external products into shared platform business schemas?
2. Does ranking a system imply Platform Capability admission or implementation commitment?
3. Does the baseline preserve the existing catalog decision that a generic connector marketplace/framework is not admitted?
4. Is 1С treated as one universal schema rather than a family of concrete configurations?

### Findings

- The first draft risk was primarily semantic: “integration portfolio” could be misread as permission to build a generic adapter framework.
- 1С needed an explicit “one concrete configuration” qualifier.
- CRM systems needed an explicit prohibition on premature shared CRM schema/generalization.
- The connector envelope needed to be separated from system/domain semantics.

### Reconciliation incorporated

- Added explicit non-claims section.
- Ranked `1С:Предприятие 8 — one concrete configuration`, not “1С” as a universal schema.
- Kept Битрикс24 and amoCRM as separate designs.
- Added Platform vs product boundary section.
- Reaffirmed `Generic connector marketplace / broad adaptor framework — Deferred / not admitted`.

**Iteration 1 result:** material boundary objections resolved.

## 4. Iteration 2 — Security / authority / reliability review

### Material questions

1. Does external retrieval silently become Arvectum OS authority?
2. Are webhook/transport receipts being treated as canonical Events?
3. Are credentials or signature keys being proposed as ordinary canonical payloads?
4. Are write effects assumed to be transactionally reversible?
5. Are Authentication, Authorization and Organizational Authority collapsed?

### Findings

- All top candidates required explicit external authority wording.
- Write-side effects required stronger uncertainty/reconciliation language.
- ЭДО and banking needed stronger high-consequence containment.
- Credential text needed explicit “secret by reference” language.

### Reconciliation incorporated

- Every ranked row declares authority and initial authority mode.
- Read and effect boundaries are separate.
- Secrets/private keys are excluded from ordinary canonical payloads.
- External writes use idempotency/uncertainty/reconciliation rather than assumed rollback.
- Historical replay is explicitly side-effect safe absent a new authorized Governed Execution.
- ЭДО signing and banking payment effects are deferred pending dedicated authority/security gates.

**Iteration 2 result:** no remaining material security/authority objection.

## 5. Iteration 3 — Product / sequencing / evidence review

### Material questions

1. Does the ranking produce a useful next action rather than a market survey?
2. Does INT-B1 overstate market-share evidence?
3. Are technical mechanisms being selected too early?
4. Are СЭД/ECM/ЭДО families treated as if all deployments expose the same interface?
5. Is the roadmap sequence preserved?

### Findings

- Ranking criteria needed to be labeled as planning judgment, not market-share statistics.
- Technical feasibility could be confirmed only for the top three without selecting transport.
- СЭД/ECM/ЭДО interface assumptions must wait for a concrete deployment/version.
- INT-B2 remains the immediate next Lane-B action before concrete connector implementation.

### Reconciliation incorporated

- Added ranking-method disclaimer.
- Added official feasibility evidence only for 1С, Битрикс24 and amoCRM.
- Deferred exact СЭД/ECM/ЭДО interface claims to concrete deployments.
- Preserved `INT-B2 → INT-B3 / INT-B4 / INT-B5` sequencing.
- Kept P9.11 unchanged as the overall M9 critical path.

**Iteration 3 result:** `PASS` with no material objections remaining.

## 6. Final review result

`INT-B1 — Integration Portfolio Baseline v1.0.0` satisfies its roadmap exit criterion as a bounded planning baseline.

No review finding requires:

- Constitution amendment;
- new RFC;
- modification of an Accepted RFC;
- new ADR at INT-B1 level;
- Product Contract creation at INT-B1 level;
- Platform Capability lifecycle change.

Future triggers remain explicit:

- `INT-B2` may identify an ADR trigger if a durable shared connector boundary/transport is selected;
- any real product reliance on governed platform integration behavior/state/history requires the applicable RFC-0004 Product Contract;
- consequential external effects require RFC-0005 Governed Execution and RFC-0003 authority/security/data-governance controls;
- the first material real connector must pass `INT-B6` before implementation admission.

**Final result:** `PASS after bounded reconciliation` — 3 of maximum 7 iterations.
