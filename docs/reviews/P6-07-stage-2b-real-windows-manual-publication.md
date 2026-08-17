# P6.07 — Stage 2B real Windows manual publication

Status: `Complete / PASS`  
P6.07 overall status: `In Progress`  
Date: `2026-08-17`  
Owner: ООО «Арвектум»

## 1. Governance basis

- Constitution: `1.2.0`, `Ratified`;
- task classification: `product_contract`, with secondary `product_specific`, `platform` validation and `governance` evidence;
- Accepted RFC checked: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006;
- relevant Accepted ADR: none;
- canonical Product Contract: `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`, `Provisional 0.1.0`;
- exact Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- shared dependency remains CAP-004 Audit/Reconstruction Support only.

This review records one real product-owned Telegram mutation under the previously prepared bounded Stage 2B procedure. It does not amend the Constitution, any Accepted RFC/ADR, the Product Contract, Platform Capability lifecycle, conformance, operational-readiness or commercial commitments.

## 2. Stage 2A continuity

The Windows execution preserved the exact Stage 2A handoff:

- execution id: `p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`;
- Stage 2A ticket SHA-256: `d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`;
- Product Contract version: `0.1.0`;
- Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- continuity result: `PASS`.

The Product Contract, ticket and credentials were treated only as continuity/technical prerequisites. A separate explicit one-time human authorization was obtained before the external effect.

## 3. Native Windows execution environment

The real action ran on native Windows:

- Windows version: `10.0.26200`;
- PowerShell: `7.6.5`;
- Python: `3.14.7`;
- Discount Parser operational runtime: `C:\Users\GN\AppData\Local\DiscountParser`;
- scheduler disabled: `YES`;
- default Telegram autopost filter disabled: `YES`;
- other publishers running: `NO`;
- Telegram route resolved through the product-owned `system` route;
- read-only Telegram preflight established the configured bot, intended target and posting permission before the real action.

## 4. Product provenance

The Windows checkout used for the real execution was:

- repository: `arvectum/discount-parser`;
- local repository SHA: `b6ba4e0808d640e938bdd53eb1cf87b2416cca10`;
- locally observed remote-main SHA at execution time: `ff8efb4186ebccca2c30cc78b8fefb5ec7cd0cf5`;
- tracked worktree before: clean;
- tracked worktree after: clean;
- repository mutations: none.

Canonical review subsequently confirmed that `b6ba4e0808d640e938bdd53eb1cf87b2416cca10` is preserved in repository history and is an ancestor of the later canonical `main` line. The exact critical Stage 2B implementation blobs used by the proof match the preparation review:

- `src/telegram/publisher.py`: `800c3b7492dc1f5710cd8a85e0cfa33260b79a8c`;
- `src/modules/publishing/service.py`: `49fef9c75538edba8efd6efa1b6f5484a16db8c4`;
- `src/modules/offers/models.py`: `bda6965b3ab1ef9d73440a3ceb31f78043de2157`;
- `tests/test_publishing.py`: `93de7a08e14463c9b65cd47a063622baca4aa280`.

Later canonical repository movement does not change the exact implementation identity used for this historical execution.

## 5. Candidate and authorization

Exactly one eligible text-only product candidate was fixed before the real mutation:

- candidate: `Offer 148`;
- product Offer id: `148`;
- status before execution: `ready`;
- text-only candidate: `YES`;
- target: `@arvectumtest`;
- template version: `v2-configurable`;
- prior Publication row for candidate+target: none;
- prior `pending` or `published` reservation: none.

The human operator provided an explicit one-time authorization bound to this candidate, target, execution and maximum one external send:

- authorization type: `explicit-human-one-time`;
- authorization received: `YES`;
- authorized at: `2026-08-17T11:07:09Z`;
- scope matched candidate and target: `YES`;
- maximum external sends: `1`.

## 6. Pre-effect reservation and immutable local evidence

The existing product-owned publisher created and committed the durable reservation before the Telegram network call. The proof-local guarded bot observed:

- reservation observed before Telegram: `YES`;
- Publication id: `14`;
- reservation status: `pending`;
- reservation created at: `2026-08-17T11:07:09.082579`;
- template version: `v2-configurable`.

Before delegating to Telegram, the wrapper preserved and read-back verified owner-local `pre-effect.json` outside source control.

Local evidence directory:

`%LOCALAPPDATA%\Arvectum\discount-parser\p6-07-stage2b\20260817-1406-p6-07-stage2`

Evidence digests independently reconciled from disk after execution:

- `pre-effect.json` size: `1073` bytes;
- actual and stored `pre-effect.json` SHA-256: `d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4`;
- `outcome.json` size: `577` bytes;
- actual and stored `outcome.json` SHA-256: `6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a`;
- actual hashes differ as expected;
- both sidecars match their corresponding files;
- evidence files were not modified during reconciliation;
- reusable secrets in evidence: `NO`;
- raw opaque identities in Git: `NO`.

The raw local JSON evidence remains owner-local and is not copied into canonical source control; this review records only minimized non-secret references and integrity evidence needed for Stage 2C reconstruction.

## 7. Real external action

The controlled execution performed exactly one product-owned publication invocation:

- `publish_offer()` invocations: `1`;
- Telegram send delegations: `1`;
- `send_message` calls: `1`;
- `send_photo` calls: `0`;
- maximum external sends: `1`;
- product result: `published`.

No retry, fallback candidate, scheduler or autopost publication occurred.

## 8. Confirmed outcome

The product and external outcome are jointly confirmed:

- Publication id: `14`;
- Publication status: `published`;
- Offer status: `published`;
- Telegram target: `@arvectumtest`;
- Telegram message id: `27`;
- external human confirmation: `PASS`;
- reconciliation required: `NO`.

The human operator visually verified that Telegram message `27` was visible in the intended target and provided the required explicit confirmation after the send.

## 9. Stage 2B result

All prepared PASS gates are satisfied:

- exact Stage 2A and Product Contract continuity — PASS;
- explicit human one-time authorization — PASS;
- one fixed eligible text-only candidate and one target — PASS;
- scheduler/autopost containment — PASS;
- durable `pending` reservation observed before network effect — PASS;
- one and only one `publish_offer()` invocation — PASS;
- one and only one Telegram `send_message` delegation — PASS;
- confirmed product state `published` with Telegram message id — PASS;
- external human confirmation — PASS;
- local evidence and independent digest reconciliation — PASS;
- no secrets or repository mutation — PASS.

`P6.07 Stage 2B = Complete / PASS`.

## 10. Architectural interpretation

This result is evidence that the existing P6.06 Provisional Product Contract and CAP-004-only boundary can carry one materially distinct real external product effect with bounded authorization, exact continuity, durable pre-effect reservation, attributable outcome and reconstructable evidence.

It does **not**:

- promote CAP-004 from `Incubating / Provisional`;
- stabilize the P6.06 Product Contract;
- move Discount Parser Offer, filtering, scheduler, Telegram or publication semantics into Arvectum OS;
- establish a production/SLA/support/conformance claim;
- close P6.07 overall.

Stage 2C remains required.

## 11. Next governed action

`P6.07 Stage 2C — Mac mini / CAP-004 reconstruction`.

Stage 2C must admit the minimized Stage 2B outcome under the same execution, Organization, attributable human Actor and exact Product Contract continuity, then reconstruct it through CAP-004 as read-only derived evidence. No replay of the Telegram mutation is permitted.
