# P6.07 — Stage 2B Windows manual publication — preparation review

Status: `Prepared / Windows execution pending`  
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

This preparation does not amend Constitution, an Accepted RFC/ADR, the P6.06 Product Contract, Platform Capability lifecycle, conformance, operational-readiness or commercial commitments.

## 2. Required Stage 2A continuity

Stage 2B MUST bind the exact real Stage 2A handoff recorded in `P6-07-stage-2a-real-mac-mini-execution.md`:

- execution id: `p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`;
- Stage 2A ticket SHA-256: `d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`;
- Product Contract: `0.1.0`;
- Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- same Organization and attributable human Actor continuity, without copying raw opaque identity values into repository evidence.

Possession of these values is continuity evidence only. It does not grant authorization for the real Telegram mutation.

## 3. Product implementation basis

Stage 2B uses the existing product-owned publication path in `arvectum/discount-parser`; no new platform publication mechanism is introduced.

Preparation verified current product `main` at repository commit:

`10e0213d89ae14307155939e07b62c06667f6459`

Relevant immutable product blobs:

- `src/modules/publishing/service.py`: `49fef9c75538edba8efd6efa1b6f5484a16db8c4`;
- `src/telegram/publisher.py`: `800c3b7492dc1f5710cd8a85e0cfa33260b79a8c`;
- `src/modules/offers/models.py`: `bda6965b3ab1ef9d73440a3ceb31f78043de2157`;
- `tests/test_publishing.py`: `93de7a08e14463c9b65cd47a063622baca4aa280`.

The existing `publish_offer()` path already:

1. resolves one product-owned Offer;
2. creates/commits a durable `Publication(status="pending")` reservation before a Telegram network call;
3. rejects or returns duplicate for an existing reservation according to current product rules;
4. performs one Telegram send attempt;
5. records `published` plus `telegram_message_id` on confirmed success, or `failed` plus bounded error evidence on explicit failure.

Existing tests establish one-send/duplicate behavior and refusal of non-ready offers without reservation. Stage 2B therefore does not justify changing the publisher merely to create a second proof-specific publication mechanism.

## 4. Bounded Windows execution design

Stage 2B is one owner-operated native Windows proof. WSL, Wine, CI, GitHub Actions, mocks, fake Telegram adapters and dry-runs do not satisfy the real-action gate.

Before the send, the Windows operator MUST verify and preserve:

- native Windows host/runtime evidence;
- exact Discount Parser repository/installed-runtime provenance used for the send;
- exact Stage 2A execution id and ticket digest above;
- exact P6.06 Product Contract pin above;
- one explicit eligible product candidate reference;
- material source-observation/config/filter/template references needed for reconstruction;
- exact Telegram target external reference;
- scheduler/autopost disabled;
- no prior `pending`/`published` reservation for the selected candidate+target;
- explicit one-time human real-action authorization scoped to this execution, candidate, target and maximum one external send;
- an immutable local pre-effect evidence record outside source control.

The final invocation MUST call the existing product-owned `publish_offer()` path at most once.

## 5. Pre-effect reservation evidence without publisher redesign

A proof-local wrapper MAY wrap the real aiogram `Bot` object passed to `publish_offer()` without changing product source.

The wrapper's `send_message()` / `send_photo()` delegate MUST, immediately before delegating to the real Telegram bot:

1. query the product `Publication` row for the selected candidate+target;
2. require exactly one row with `status="pending"`;
3. preserve its `publication_id`, `created_at`, candidate/target refs and template version into the immutable pre-effect evidence record;
4. require the exact Stage 2A continuity values and explicit human authorization already present in that record;
5. fail closed without delegating to Telegram if any condition is missing or mismatched.

This observes the existing durable reservation after `publish_offer()` commits it and before the network effect, preserving the required product-owned reservation evidence while avoiding a competing publication implementation.

The wrapper MUST NOT retry the Telegram call, loop over candidates, enable scheduler/autopost, alter product selection rules or print/store the reusable Telegram bot token.

## 6. Human authorization boundary

The real-action authorization MUST be contemporaneous and explicit. The local execution helper SHOULD require the human operator to type an exact one-time confirmation phrase immediately before the allowed invocation, and MUST record only a minimized authorization record such as:

- authorization type: `explicit-human-one-time`;
- authorized operation: `discount-parser.controlled-telegram-publication`;
- execution id;
- candidate reference;
- target reference;
- maximum external sends: `1`;
- authorization timestamp;
- attributable human Actor continuity reference without raw opaque identity disclosure.

A chat instruction, Product Contract, Stage 2A ticket, technical credential, successful authentication or possession of the bot token MUST NOT be treated as the authorization record by itself.

## 7. Required local evidence

Use an owner-only local evidence directory outside both repositories, for example under the current Windows user's local application-data area.

At minimum preserve:

1. `pre-effect.json` — exact continuity pins, product commit/runtime, candidate/target/material references, disabled autopost/scheduler evidence, one-time authorization, pending reservation id/time/template and `max_external_sends=1`;
2. `outcome.json` — exact `publish_offer()` result, publication id, terminal product status, Telegram message id when confirmed, observed target/message reference, timestamps and explicit uncertainty/reconciliation state when confirmation is not possible;
3. SHA-256 digest files for both JSON records;
4. a sanitized execution report containing commands/actions and exit/result states but no reusable secret.

Existing files MUST NOT be overwritten. A failed preparation attempt gets a new directory and remains distinguishable from the accepted attempt.

## 8. Outcome rules

### PASS

Stage 2B may be reported `Complete / PASS` only when all are true:

- exact Stage 2A continuity is verified;
- explicit one-time human authorization exists before send;
- one eligible candidate and one target are fixed before send;
- scheduler/autopost remains disabled;
- one durable `pending` product reservation is observed before the Telegram network call;
- `publish_offer()` is invoked no more than once;
- confirmed success returns `status="published"`, one publication id and a Telegram message id;
- external confirmation of the exact message on the intended target succeeds;
- local pre-effect/outcome evidence and digests are preserved without secrets.

### FAIL

Use `FAIL` when a bounded attempted execution definitively fails and there is no uncertainty about whether Telegram was mutated. Preserve the failed product outcome and do not perform a second send under this execution.

### RECONCILIATION_REQUIRED

If the external call has an uncertain outcome, local state and Telegram cannot be reconciled confidently, the process crashes after the possible send, or confirmation cannot establish whether the effect occurred, record `RECONCILIATION_REQUIRED`. Do not retry under this execution.

### BLOCKED

Use `BLOCKED` before any external call when a prerequisite is missing or mismatched: Stage 2A continuity, Product Contract pin, candidate, target, authorization, disabled autopost/scheduler, credentials, bot/channel permissions, product readiness or native Windows execution environment.

## 9. Containment

Stage 2B MUST NOT:

- perform more than one external Telegram send;
- use scheduler/autopost as the proof;
- activate or modify autopost configuration except to ensure it is disabled;
- change the P6.06 Product Contract;
- admit CAP-001/002/003 reliance;
- promote CAP-004 or any product mechanism into a Platform Capability;
- migrate product schemas/state into Arvectum OS;
- store reusable Telegram credentials, raw opaque Organization identity or raw opaque human identity in Git;
- mark P6.07 complete overall.

Stage 2C remains a separate Mac mini action and is blocked until Stage 2B evidence exists.

## 10. Preparation result

`P6.07 Stage 2B preparation = PASS`.

`P6.07 Stage 2B real Windows execution = PENDING`.

The next action is the owner-operated native Windows execution described above. Only after its evidence is reviewed may Stage 2B be canonically recorded `Complete / PASS` and Stage 2C become the next governed action.
