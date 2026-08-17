# P6.07 — Stage 2C Mac mini / CAP-004 reconstruction — preparation review

Status: `Prepared / local execution pending`  
P6.07 overall status: `In Progress`  
Date: `2026-08-17`  
Owner: ООО «Арвектум»

## 1. Governance basis

- Constitution: `1.2.0`, `Ratified`;
- task classification: `product_contract`, with secondary `platform`, `product_specific` and `governance` evidence;
- Accepted RFC checked: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006;
- relevant Accepted ADR: none;
- canonical P6.06 Product Contract: `Provisional 0.1.0`;
- Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- shared dependency: CAP-004 Audit / Reconstruction Support only;
- Stage 2B: `Complete / PASS`.

This preparation does not amend the Constitution, an Accepted RFC/ADR, the canonical Product Contract, capability lifecycle, conformance, operational readiness or commercial commitments.

## 2. Required post-real-publication Product Contract review

The P6.06 contract requires review after the first real governed publication. Stage 2B triggered that condition.

The canonical review is:

`docs/reviews/P6-06-post-first-real-publication-contract-review.md`

Result:

`Complete / PASS — no contract revision required`.

The real Stage 2B evidence validates the existing CAP-004-only boundary. No evidence justifies CAP-001/002/003 reliance, migration of Discount Parser domain semantics into the platform, Product Contract stabilization or CAP-004 promotion. P6.06 therefore remains `Provisional 0.1.0` under its existing immutable version.

## 3. Exact Stage 2 continuity

Stage 2C MUST preserve:

- execution id: `p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`;
- Stage 2A ticket SHA-256: `d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`;
- Product Contract version: `0.1.0`;
- Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- same Organization and attributable human Actor recovered from the owner-local Stage 2A ticket;
- Stage 2B canonical review blob: `4b2cfa04ce92d3a8978cfd41f790358936925014`;
- Stage 2B closure commit: `725aeef0bb13376c9045da26a30401947e12d0ed`.

Raw Organization/human Actor identity values remain owner-local and MUST NOT be written to repository evidence or the minimized Stage 2C report.

## 4. Stage 2B evidence fixed for reconstruction

Confirmed real evidence:

- Discount Parser execution repository SHA: `b6ba4e0808d640e938bdd53eb1cf87b2416cca10`;
- Offer: `148`;
- Publication: `14`;
- target: `@arvectumtest`;
- template: `v2-configurable`;
- authorization type: `explicit-human-one-time`;
- authorization timestamp: `2026-08-17T11:07:09Z`;
- pre-effect SHA-256: `d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4`;
- outcome SHA-256: `6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a`;
- result: `published`;
- Telegram message id: `27`;
- human external confirmation: `PASS`;
- reconciliation required: `NO`.

The raw `pre-effect.json` and `outcome.json` remain owner-local on the Windows evidence host. They are not copied into Git.

## 5. Why a minimized Windows-to-Mac handoff is required

P6.06 requires reconstruction of material product-owned source/candidate/config/template/reservation/attempt/target references while avoiding migration of full product payloads or private product schemas into Arvectum OS.

The Stage 2B canonical review intentionally records only minimized closure facts, while the owner-local evidence/product runtime retains the exact product-owned references used by the real attempt. Stage 2C therefore uses a task-local minimized handoff generated on the evidence owner host.

The handoff:

- recomputes the exact canonical pre-effect/outcome SHA-256 digests from retained files;
- treats raw JSON as opaque bytes and does not embed it;
- carries only safe `role=reference` values for material product boundary evidence;
- contains no bot token, proxy password, reusable secret, raw Organization identity or raw human Actor identity;
- has its own immutable SHA-256 sidecar;
- is a P6.07-local evidence format, not a public wire/API/Product Contract schema.

Required semantic role groups are:

- source observation;
- Offer;
- publication candidate;
- material filter/rule configuration;
- template version;
- publication reservation;
- publication attempt;
- Telegram target;
- explicit human authorization evidence.

A parse-run/source reference may be included when materially available.

## 6. Prepared Stage 2C implementation

Task-specific module:

`reference/python/p6_07_discount_parser_ref/stage2c.py`

Preparation blob:

`5566b5e3e2e643d9afba40b644d1306b7cd898db`

It provides two local commands:

1. `handoff` — Windows evidence-owner step that verifies retained Stage 2B file digests and creates the minimized handoff;
2. `reconstruct` — Mac mini step that verifies Stage 2A + Stage 2B handoff continuity and invokes the existing product integration adapter / CAP-004 reconstruction path.

The implementation deliberately has no live Telegram client, no Discount Parser publisher call, no product-database write and no external mutation path.

Regression tests:

`reference/python/tests/test_p6_07_stage2c_cap004_reconstruction.py`

Preparation test blob:

`5edb9066efa5b928a9a4534fa7607530518d099f`

The tests cover:

- complete reconstruction of the fixed real Stage 2B evidence shape;
- CAP-004-only/read-only Product Contract projection;
- opaque raw evidence binding without embedding raw content;
- digest, execution and Product Contract mismatch failures;
- unconfirmed/uncertain outcome failure;
- missing source/rule evidence failure;
- zero live-network/external-effect code path;
- exclusion of raw Stage 2A Organization/Actor values from the Stage 2C report;
- absence of fabricated retroactive platform gate decisions.

Repository CI must pass before this preparation is merged to canonical `main`.

## 7. Executable Product Contract projection wording

`reference/python/p6_07_discount_parser_ref/contract.py` is updated only to remove stale “Stage 1 only” wording from the internal executable projection and explicitly cover:

- Stage 1 synthetic/offline validation; and
- Stage 2C read-only reconstruction of the separately authorized, already completed Stage 2B effect.

The canonical Product Contract path, version `0.1.0`, blob SHA, CAP-004-only dependency, read-only reconstruction operation and Provisional lifecycle remain unchanged. This is subordinate implementation clarification, not a Product Contract revision.

## 8. Stage 2C reconstruction semantics

The Mac mini execution MUST:

1. verify the exact owner-local Stage 2A ticket and SHA-256;
2. recover the same Organization and human Actor in-memory from that ticket;
3. verify the exact minimized Stage 2B handoff and SHA-256;
4. verify the exact Product Contract, canonical Stage 2B review, product execution and effect references;
5. compose the existing CAP-004-only Product Contract integration adapters;
6. construct an exact-reference ReconstructionManifest from retained/minimized evidence;
7. invoke existing CAP-004 reconstruction as `ReadOnly`;
8. require complete reconstruction and exact Organization/Actor/Product Contract continuity;
9. create an owner-local immutable Stage 2C report plus SHA-256;
10. preserve zero network calls, zero Telegram calls, zero Discount Parser publication calls, zero product DB mutations and zero external mutations.

The Stage 2C manifest uses an explicit Stage 2C admission-observation reference for the already confirmed Stage 2B outcome. It MUST NOT claim that a Native Arvectum OS Event was retroactively present on Windows before/during the Telegram send.

The real one-time human authorization is retained as exact product/local evidence. Stage 2C MUST NOT fabricate a retroactive platform `GovernedGateDecision` for Stage 2B.

## 9. PASS criteria

Stage 2C may be canonically recorded `Complete / PASS` only when the real Mac mini run establishes all of the following:

- exact Stage 2A ticket digest and execution id verified;
- exact Product Contract `0.1.0` / blob continuity verified;
- same Organization and attributable human Actor continuity verified locally;
- minimized Stage 2B handoff digest verified;
- exact Stage 2B pre-effect/outcome digests verified through the handoff;
- required material product reference groups present;
- CAP-004 current provider evidence present;
- Product Contract dependency remains CAP-004 only;
- reconstruction is complete;
- reconstruction is read-only and derived;
- no fabricated retroactive gate decision;
- no network, Telegram, publication replay, product DB mutation or external mutation;
- immutable Stage 2C report and sidecar pass read-back verification;
- no reusable secrets or raw opaque Organization/Actor identity in the report/repository.

Any mismatch is `BLOCKED` or `FAIL` before canonical closure; no Telegram retry/replay is permitted.

## 10. Preparation result

`P6.07 Stage 2C preparation = PASS, subject to repository CI before merge`.

`P6.07 Stage 2C real Mac mini reconstruction = PENDING`.

The next local action after canonical preparation merge is the bounded Windows handoff generation followed by Mac mini CAP-004 reconstruction. P6.07 remains incomplete until that real Stage 2C evidence is reviewed and canonically recorded.
