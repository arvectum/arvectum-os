# P6.07 — Stage 2B real Windows manual publication

Status: `Complete / PASS`  
P6.07 overall status: `In Progress`  
Date: `2026-08-17`  
Owner: ООО «Арвектум»

## Governance basis

Constitution `1.2.0` is Ratified. Relevant Accepted RFC checked: RFC-0001 through RFC-0006. Relevant Accepted ADR: none. Canonical Product Contract remains `P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`, Provisional `0.1.0`, exact blob `23bbe792b81ddc5da736333d8a92580a718f920e`. Shared dependency remains CAP-004 only.

## Exact continuity

- execution id: `p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`;
- Stage 2A ticket SHA-256: `d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`;
- Product Contract version: `0.1.0`;
- Product Contract blob: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- continuity: `PASS`.

## Native Windows execution

- Windows version: `10.0.26200`;
- PowerShell: `7.6.5`;
- Python: `3.14.7`;
- runtime root: `C:\Users\GN\AppData\Local\DiscountParser`;
- scheduler disabled: `YES`;
- autopost disabled: `YES`;
- other publishers: `NO`;
- Telegram product route: `system`;
- read-only bot/target/admin permission preflight: `PASS`.

## Product provenance

Execution checkout: `b6ba4e0808d640e938bdd53eb1cf87b2416cca10`. It is a recovered Windows hotfix commit and an ancestor of current canonical `arvectum/discount-parser` main. The execution-critical blobs matched the preparation baseline exactly:

- publisher: `800c3b7492dc1f5710cd8a85e0cfa33260b79a8c`;
- publishing service: `49fef9c75538edba8efd6efa1b6f5484a16db8c4`;
- models: `bda6965b3ab1ef9d73440a3ceb31f78043de2157`;
- publishing tests: `93de7a08e14463c9b65cd47a063622baca4aa280`.

Tracked worktree was clean before and after; repo mutations: none.

## Candidate and authorization

- candidate: `Offer 148`;
- status before send: `ready`;
- text-only: `YES`;
- target: `@arvectumtest`;
- template: `v2-configurable`;
- prior Publication row: `NO`;
- prior pending/published reservation: `NO`;
- authorization type: `explicit-human-one-time`;
- authorization received: `YES` at `2026-08-17T11:07:09Z`;
- authorization scope matched candidate+target;
- maximum external sends: `1`.

## Pre-effect evidence

A durable product reservation was observed before the Telegram network delegation:

- publication id: `14`;
- status: `pending`;
- created at: `2026-08-17 11:07:09.082579`.

Owner-local evidence directory:
`C:\Users\GN\AppData\Local\Arvectum\discount-parser\p6-07-stage2b\20260817-1406-p6-07-stage2`

`pre-effect.json`:
- size `1073` bytes;
- SHA-256 `d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4`;
- sidecar/readback verification: `PASS`.

## Real action and confirmed outcome

- `publish_offer()` invocations: `1`;
- Telegram send delegations: `1`;
- send_message calls: `1`;
- send_photo calls: `0`;
- publish result: `published`;
- Publication status: `published`;
- Offer status: `published`;
- Telegram message id: `27`;
- target: `@arvectumtest`;
- external human visual confirmation: `PASS`;
- reconciliation required: `NO`.

`outcome.json`:
- size `577` bytes;
- SHA-256 `6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a`;
- sidecar/readback verification: `PASS`.

The initial textual report accidentally repeated the pre-effect digest in the outcome digest field. Final read-only reconciliation recalculated both files independently, confirmed that the two actual hashes differ, both sidecars match their files, and no evidence file was modified. This resolves the reporting defect without rewriting evidence.

No reusable secrets were present in evidence; no raw opaque identities were committed to Git.

## Result

`P6.07 Stage 2B = Complete / PASS`.

This result records one explicitly authorized real native-Windows publication with durable pre-effect reservation, exactly one external Telegram send, confirmed terminal product state, human visual external confirmation and independently verified immutable evidence. It does not promote CAP-004, stabilize the Product Contract, activate scheduler/autopost, or close P6.07 overall.

## Next governed action

`P6.07 Stage 2C — Mac mini / CAP-004 reconstruction`.

Stage 2C must admit the exact Stage 2B outcome under the same execution, Organization, human Actor and Product Contract continuity and reconstruct it through CAP-004 as read-only derived evidence. No Telegram replay or new external mutation is permitted.