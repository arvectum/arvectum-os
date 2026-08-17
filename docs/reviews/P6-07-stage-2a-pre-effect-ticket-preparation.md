# P6.07 — Stage 2A pre-effect execution ticket — preparation review

Status: `Prepared / Local execution pending`  
P6.07 overall status: `In Progress`  
Date: `2026-08-17`  
Owner: ООО «Арвектум»

## 1. Governance basis

- Constitution: `1.2.0`, `Ratified`;
- task classification: `product_contract`, with secondary `platform` validation and `product_specific` handoff evidence;
- Accepted RFC checked: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006;
- relevant Accepted ADR: none;
- canonical Product Contract: `docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`, `Provisional 0.1.0`, blob `23bbe792b81ddc5da736333d8a92580a718f920e`;
- shared dependency remains CAP-004 Audit/Reconstruction Support only.

No Constitution, Accepted RFC, Accepted ADR, Product Contract, capability lifecycle or Stable/public contract change is made by Stage 2A preparation.

## 2. Stage 2 decomposition

The bounded P6.07 real-action proof is executed as three explicit sub-stages:

1. **Stage 2A — Mac mini / Arvectum OS pre-effect ticket.** Create immutable execution intent evidence before any real Telegram effect and bind it with SHA-256.
2. **Stage 2B — Windows / Discount Parser one manual publication.** Bind the exact Stage 2A ticket hash, preserve product-owned candidate/target/reservation/intent/authorization evidence before send, execute at most one manual `publish_offer()` send, and return confirmed effect evidence or explicit uncertain outcome. Scheduler/autopost remains disabled.
3. **Stage 2C — Mac mini / CAP-004 reconstruction.** Admit the Stage 2B outcome under the same execution/Organization/Actor/Product Contract continuity and reconstruct it through CAP-004 as read-only derived evidence.

P6.07 is complete only after Stage 2C PASS. The decomposition does not widen P6.06 scope.

## 3. Stage 2A prepared implementation

Reference implementation:

- `reference/python/p6_07_discount_parser_ref/stage2a.py`;
- `reference/python/tests/test_p6_07_stage2a_pre_effect_ticket.py`.

The Stage 2A generator creates exactly two handoff files:

- `p6-07-stage2-execution-ticket.json`;
- `p6-07-stage2-execution-ticket.sha256`.

The ticket pins:

- one unique `execution_id`;
- one explicit Organization;
- one attributable human Actor;
- semantic operation `discount-parser.controlled-telegram-publication`;
- side-effect class `ExternalMutation` and maximum one external send for the downstream bounded proof;
- product identity and compatibility line;
- exact P6.06 Product Contract `0.1.0` and canonical blob SHA;
- CAP-004-only shared dependency;
- exact Arvectum OS repository commit used to create the ticket;
- containment and Stage 2B/2C handoff requirements.

The generated ticket intentionally does **not** contain product candidate, Telegram target, publication reservation/attempt or external outcome payload. Those remain Discount Parser product-owned evidence and must be recorded by Stage 2B before/during the product-side action. The ticket contains no reusable secret.

## 4. Authority boundary

Neither possession of P6.06 Product Contract `0.1.0` nor creation of the Stage 2A execution ticket grants authorization for the real Telegram mutation.

Stage 2B must preserve explicit real-action authorization before its send. A missing authorization, missing/mismatched ticket hash, Organization/Actor mismatch, missing candidate/target, missing pre-effect reservation/intent, or uncertain prior outcome must fail closed or remain reconciliation-required as applicable.

Stage 2A preparation itself performs no Telegram/network call, product database mutation, scheduler/autopost activation or canonical-state mutation.

## 5. Immutability and handoff

Stage 2A evidence is write-once at the selected local evidence path:

- existing ticket or digest files are never overwritten;
- the digest is SHA-256 of the exact UTF-8 ticket bytes;
- immediate read-after-write verification is required;
- any later byte-level change invalidates the digest;
- Stage 2B must receive and bind the exact digest and `execution_id`.

A failed local Stage 2A attempt must not be repaired by editing the existing ticket in place. A new clean attempt requires a fresh output location/execution identity and an explicit explanation of the discarded failed evidence.

## 6. Current result

`Stage 2A implementation preparation = PASS`.

`Stage 2A real local execution = PENDING` until the Mac mini creates and independently verifies the real ticket/hash using the actual local Organization/human Actor context and a clean canonical repository commit.

No real Telegram publication is authorized or performed by this preparation review.
