# P6.03 — First real product/workflow platform integration closure

Status: `Complete / PASS`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `product_specific`, `platform` and `governance`
Product repository: `arutyunoveth/ai-corporation`
Product PR: `#141`, merged
Product merge commit: `2c21a33eec02959aba7d13909f0d0c835294becf`
Real case: `0344100006426000005` — «Поставка кабельной продукции»
Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`
Predecessor: [`P6-03-stage-1-first-real-product-workflow-platform-integration.md`](P6-03-stage-1-first-real-product-workflow-platform-integration.md), `Stage 1 PASS`

## 1. Decision

**PASS — P6.03 is complete for the declared bounded first-real-product integration scope.**

P6.03 produced both required kinds of evidence:

1. Stage 1 synthetic/anonymized/redacted boundary proof with fail-closed negative paths;
2. Stage 2 execution of exactly one real public 44-ФЗ procurement case through the same P6.02 CAP-001/CAP-004 boundary.

The Stage 2 case is notice `0344100006426000005`, «Поставка кабельной продукции». Real procurement facts remain externally authoritative. The product-owned human-review disposition is deliberately:

`NOT_CLIENT_READY_EVIDENCE_INCOMPLETE`

The repository retains an integrity-protected normalized public-fact snapshot and exact source references, but not the exact bytes/digests of all listed tender attachments. Producing a client-ready procurement recommendation from that retained evidence would overstate what was actually reviewed, so the product correctly blocks that designation pending exact source-package retrieval/acceptance.

This is a successful governance outcome and material real-use evidence, not a failed integration result.

## 2. Canonical basis checked

Closure preserves:

- Constitution `1.2.0`, `Ratified`, frozen;
- RFC-0001 through RFC-0008 `1.0.0`, `Accepted`;
- P6.02 Product Contract `Provisional 0.1.0`;
- R17 `PASS`;
- P6.03 Stage 1 `PASS`;
- CAP-001 and CAP-004 `Incubating / Provisional 1.0.0`;
- CAP-002 and CAP-003 omission;
- external authority for procurement facts/documents;
- product ownership of procurement interpretation and review disposition;
- no automated external mutation or organizational commitment.

No higher-priority canonical conflict was identified.

## 3. Real-case evidence

The real validation run used public procurement notice `0344100006426000005` with normalized facts including IKZ `261710706281346320100100070012732244`, customer INN `7107062813`, electronic request-for-quotations method, publication `2026-06-25`, deadline `2026-07-02`, NMCK `328800.00 RUB` and two LAN-cable positions.

The product repository protects only its normalized fact payload with:

`sha256:ae5f68d547fdce8a82cc695396b330b0244ea06892ddbea7155bd86c6e9d8033`

That digest is explicitly not represented as a hash of the remote procurement page or tender attachments.

The public source set identifies seven tender documents. Their exact bytes/digests are not retained by this run, which is the evidence basis for the incomplete/client-ready stop.

## 4. Exact boundary behavior

Stage 2:

1. used one explicit Organization and attributable human operator context;
2. retained the exact P6.02 Product Contract lineage/version `0.1.0`;
3. bound exactly CAP-001 + CAP-004 to explicit current Provisional `1.0.0` provider evidence;
4. represented the real procurement source as `External Reference`, not `Native`;
5. admitted and resolved the exact integrity-protected normalized source snapshot through CAP-001;
6. kept procurement interpretation and the completeness/client-ready judgment product-owned;
7. recorded the product-owned review result as derived evidence rather than platform authority;
8. reconstructed the platform-backed acts through CAP-004;
9. performed no supplier/customer communication, EIS/ETP mutation, application submission, signature, payment or another organizational commitment.

CAP-002/CAP-003 remained absent.

## 5. Hosted validation

Product CI run `#1934` completed successfully before merge. All jobs passed:

- `P6.03 Arvectum OS Stage 2 real case` — `PASS`, `2 passed`;
- P6.03 Stage 1 regression — `PASS`;
- quality `make check` — `PASS`;
- quality full `make test` — `PASS`;
- security — `PASS`;
- migrations — `PASS`;
- R8 PostgreSQL integration/acceptance — `PASS`;
- R8 tenant acceptance — `PASS`;
- Redis integration — `PASS`.

The Stage 2 job was pinned to Arvectum OS Stage 1 implementation merge `8c838edafeb564862b88230cba1b6ea02b7c8e14`.

Product PR `#141` was then squash-merged to `main` as `2c21a33eec02959aba7d13909f0d0c835294becf`.

## 6. Cross-review findings

### Architecture

`PASS`. The real case reused the existing internal/provisional `IntegrationAdapters` seam and created no durable/public/stable technology or compatibility boundary.

### Product/platform boundary

`PASS`. Procurement meaning, completeness judgment and client-ready disposition remain in `ai-corporation`. The platform governs exact identity/version/reference/provenance and reconstruction only.

### Authority integrity

`PASS`. External procurement facts remain externally authoritative. The normalized repository snapshot is a governed transformed reference, not a replacement source of truth.

### Security and external action

`PASS` within scope. One explicit Organization/Actor context was used and no external procurement action was performed or authorized.

### Evidence honesty

`PASS`. Missing exact attachment bytes/digests caused a truthful product stop instead of inference over unseen requirements or a fabricated positive recommendation.

## 7. Evidence-backed friction

P6.03 demonstrates one concrete first-real-use gap:

- the bounded integration can govern and reconstruct an exact real external procurement reference;
- the current product/platform seam does not yet provide the complete end-to-end governed retrieval/admission contour for the full external tender attachment set needed by the intended client-ready workflow;
- without that exact source package, the product correctly cannot finish the client-ready decision-package path.

This finding is now input evidence for P6.04 and, after measurement/disposition, P6.05. It does not justify speculative CAP-002/CAP-003 adoption or platform-domain expansion.

## 8. Stage 3 calibration-cap disposition

**Stage 3 calibration capacity is deliberately not consumed.**

P6.02 authorizes a maximum of three platform-backed calibration cases; it does not require three cases. Stage 2 already produced the material new evidence sought from real use: the declared read-oriented boundary works on a real external procurement reference, while completion of the intended client-ready workflow is blocked by a specific missing full-attachment retrieval/admission contour.

Running additional cases through the unchanged incomplete contour would primarily reproduce the same known limitation rather than test a new hypothesis. Under the Constitution/RFC principles of evidence over intuition, organizational value over ceremony, validated reuse over speculative generality and reversible experimentation, the correct disposition is therefore:

- consume `0` additional Stage 3 calibration cases now;
- preserve the remaining calibration capacity rather than treating it as an obligation;
- close P6.03 on the Stage 1 + Stage 2 evidence already obtained;
- move the measured value/friction/governance analysis to P6.04;
- allow P6.05 to remediate only the gap P6.04 confirms and prioritizes;
- reopen bounded calibration later only if remediation creates a materially new contour or hypothesis worth validating.

This is not a waiver of security/governance evidence and not an automatic capability expansion.

## 9. Lifecycle and commercial integrity

At P6.03 closure:

- CAP-001: `Incubating / Provisional`;
- CAP-004: `Incubating / Provisional`;
- CAP-002/CAP-003: unchanged and omitted;
- P6.02 Product Contract: `Provisional 0.1.0`;
- P6.03: `Complete / PASS` for the declared bounded integration scope;
- no Platform Capability becomes `Active`;
- no Stable/public integration contract is created;
- no production-readiness/SLA/support claim is created;
- no client-ready procurement recommendation is claimed for case `0344100006426000005`.

## 10. Next canonical action

> **P6.04 — Product value, delivery-friction + governance evidence capture.**

P6.04 must use the actual Stage 1/Stage 2 evidence, including the truthful `NOT_CLIENT_READY_EVIDENCE_INCOMPLETE` outcome and the demonstrated full-attachment-contour friction. It must measure both benefit and overhead and may conclude that a platform abstraction creates no net value for part of the workflow.
