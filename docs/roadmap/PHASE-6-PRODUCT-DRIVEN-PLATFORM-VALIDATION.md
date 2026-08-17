# Phase 6: Product-driven platform validation

Status: `Active / In Progress`
Version: `1.2.8`

## 1. Goal

Validate platform fitness through real product use and materially distinct reuse evidence without turning product-local behavior into platform responsibility prematurely.

## 2. P6.05: Real evidence admission

Status: `Complete / PASS`
Evidence: [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md)

L1 through L9 are complete. L7 produced truthful real 7/7 evidence. L8 admitted and reconstructed that evidence under governed execution. L9 captured the observed dogfooding friction without silently promoting observations into architecture, Knowledge, Product Contract changes or capability lifecycle decisions.

## 3. P6.06: Second materially distinct real target

Status: `Complete / PASS`
Evidence: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md)

P6.06 selects **Arvectum Discount Parser** and the controlled Telegram publication workflow as the second real validation target. The selection is materially distinct from the first Tender Operator workflow because it introduces scheduled/machine initiation, an actual consequential external mutation, duplicate/idempotency pressure, possible uncertain external outcome and reconciliation requirements.

The canonical Provisional Product Contract `0.1.0` defines a deliberately narrow **CAP-004-only** shared dependency. Offer/source schemas, normalization, deduplication, classification, scheduler, rule memory, publication filters, Telegram integration, product ledger and UX remain product-owned. CAP-001, CAP-002 and CAP-003 are deliberately omitted from this contract version.

P6.06 records selection plus the Product Contract boundary only. It does not claim that a second real governed integration run has already occurred, does not promote CAP-004, and does not create Stable/public/production/support commitments.

## 4. P6.07: Second real product/workflow platform integration

Status: `In Progress — Stage 1 Complete / PASS; Stage 2A Complete / PASS; Stage 2B Complete / PASS; Stage 2C Pending`
Stage 1 review: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)
Stage 2A preparation: [`P6-07-stage-2a-pre-effect-ticket-preparation.md`](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md)
Stage 2A real execution: [`P6-07-stage-2a-real-mac-mini-execution.md`](../reviews/P6-07-stage-2a-real-mac-mini-execution.md)
Stage 2B preparation: [`P6-07-stage-2b-windows-manual-publication-preparation.md`](../reviews/P6-07-stage-2b-windows-manual-publication-preparation.md)
Stage 2B real execution: [`P6-07-stage-2b-real-windows-manual-publication.md`](../reviews/P6-07-stage-2b-real-windows-manual-publication.md)

P6.07 validates the P6.06 boundary against executable Discount Parser controlled-publication evidence.

Stage 1 is complete and PASS:

- exact P6.06 Product Contract `0.1.0` continuity is preserved;
- only CAP-004 is consumed;
- the product-facing journey uses the shared integration adapter seam rather than platform internals;
- synthetic/offline publication evidence preserves Organization, Actor, contract, product-owned inputs, pre-effect reservation/intent, outcome, correlation, causation and provenance;
- duplicate, missing pre-effect evidence, missing contract pin, wrong Organization, missing current provider evidence and uncertain external outcome are fail-closed or reconciliation-safe;
- no live Telegram call, credential, scheduler/autopost activation or product database migration occurs in Stage 1;
- the full Reference Python CI suite passes: `894` tests / `OK`.

Stage 1 found no blocking platform gap and therefore does not justify a new RFC/ADR, a new Platform Capability, CAP-004 promotion or moving Discount Parser domain semantics into the platform.

Stage 2 is decomposed into three bounded handoffs:

- **Stage 2A — Mac mini / Arvectum OS pre-effect ticket — Complete / PASS.** The real Mac mini run reused the existing P6.05-L4 Organization/human Actor context, verified the exact P6.06 contract pin, created one immutable execution ticket and SHA-256 before any real external effect, and independently verified the digest. Targeted Stage 2A tests passed (`8`); the full Reference Python suite passed (`902`). The local ticket remained owner-only and outside source control. No Discount Parser invocation, Telegram call, scheduler/autopost activation, product database mutation, external effect or CAP-004 Stage 2C reconstruction occurred.
- **Stage 2B — Windows / Discount Parser manual publication — Complete / PASS.** One eligible text-only product Offer (`148`) was fixed for `@arvectumtest`, scheduler/autopost and competing publishers were disabled, and a separate explicit one-time human authorization was obtained. The existing product-owned `publish_offer()` created durable Publication `14` in `pending` before the external call; the proof-local guard captured immutable pre-effect evidence and then delegated exactly one `send_message` and zero `send_photo` calls. Product state finished `published`, Telegram returned message id `27`, and the human operator visually confirmed that exact message in the intended target. Independent post-run digest reconciliation verified distinct `pre-effect.json` and `outcome.json` files plus their stored SHA-256 sidecars. No retry, secret disclosure or repository mutation occurred.
- **Stage 2C — Mac mini / CAP-004 reconstruction — Pending.** Admit the Stage 2B outcome under the same execution, Organization, human Actor and P6.06 Product Contract continuity, then reconstruct it through CAP-004 as read-only derived evidence. The Telegram effect MUST NOT be replayed.

Neither the Product Contract nor the Stage 2A ticket granted authorization for the Stage 2B external mutation; authorization was separately obtained from the human operator. Until Stage 2C reconstruction succeeds, P6.07 is not closed overall.

## 5. Subtasks / completed evidence

| Task | Outcome | Evidence |
| :--- | :--- | :--- |
| `P6.05-L7` | Real exact-attachment live run | 🟩 Complete / PASS — [review](../reviews/P6-05-L7-attempt-2-real-exact-attachment-live-run.md) |
| `P6.05-L8` | Governed evidence admission | 🟩 Complete / PASS — [review](../reviews/P6-05-L8-attempt-2-governed-evidence-admission-and-closure.md) |
| `P6.05-L9` | Dogfooding friction capture | 🟩 Complete / PASS — [review](../reviews/P6-05-L9-dogfooding-friction-capture.md) |
| `P6.06` | Second materially distinct target selected and Product Contract boundary defined | 🟩 Complete / PASS — [contract](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md) |
| `P6.07 Stage 1` | Synthetic/offline second-product integration proof under P6.06 | 🟩 Complete / PASS — [review](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md) |
| `P6.07 Stage 2A` | Immutable pre-effect execution ticket + SHA-256 | 🟩 Complete / PASS — [real execution review](../reviews/P6-07-stage-2a-real-mac-mini-execution.md) |
| `P6.07 Stage 2B` | One explicit real manual Discount Parser publication | 🟩 Complete / PASS — [real execution review](../reviews/P6-07-stage-2b-real-windows-manual-publication.md) |
| `P6.07 Stage 2C` | Outcome admission + CAP-004 reconstruction | 🟨 Pending — Stage 2B evidence is now available |

## 6. Current Phase 6 state

- [x] First real Tender Operator integration evidence admitted and reconstructed.
- [x] P6.05 dogfooding friction captured without accidental architectural promotion.
- [x] Second materially distinct product/workflow selected.
- [x] Second Product Contract boundary canonically defined before governed reliance.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [x] Stage 2A generator, immutable handoff and verification tests prepared.
- [x] Real Stage 2A Mac mini ticket/hash created and independently verified from actual Organization/human Actor context.
- [x] Stage 2B native-Windows one-send execution procedure and evidence boundary prepared without changing product publication semantics.
- [x] One explicitly authorized real manual publication executed under P6.06 in Stage 2B, with confirmed Telegram effect and reconciled local evidence digests.
- [ ] Exact Stage 2B outcome reconstructed through CAP-004 in Stage 2C.

Phase 6 remains `Active / In Progress`. The next governed action is **P6.07 Stage 2C — Mac mini / CAP-004 reconstruction**. Stage 2C is read-only reconstruction of the already confirmed effect; it MUST NOT replay or repeat the Telegram mutation. Scheduled/autopost operation remains outside this proof.
