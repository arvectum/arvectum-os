# Phase 6: Product-driven platform validation

Status: `Active / In Progress`
Version: `1.2.5`

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

Status: `In Progress — Stage 1 Complete / PASS; Stage 2A prepared / local execution pending`
Stage 1 review: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)
Stage 2A preparation: [`P6-07-stage-2a-pre-effect-ticket-preparation.md`](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md)

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

- **Stage 2A — Mac mini / Arvectum OS pre-effect ticket.** Create one immutable execution ticket and SHA-256 before any real external effect. The generator and fail-closed verification tests are prepared; the real local ticket/hash is still pending.
- **Stage 2B — Windows / Discount Parser manual publication.** Bind the exact Stage 2A ticket hash and execution id, preserve product-owned candidate/target/reservation/intent plus explicit real-action authorization before send, and perform at most one human-operated `publish_offer()` send. Scheduler/autopost remains disabled.
- **Stage 2C — Mac mini / CAP-004 reconstruction.** Admit the Stage 2B outcome under the same execution, Organization, human Actor and P6.06 Product Contract continuity, then reconstruct it through CAP-004 as read-only derived evidence.

Neither the Product Contract nor the Stage 2A ticket grants authorization for the Stage 2B external mutation. Until real Stage 2A evidence exists, Stage 2B must not send. Until Stage 2C reconstruction succeeds, P6.07 is not closed overall.

## 5. Subtasks / completed evidence

| Task | Outcome | Evidence |
| :--- | :--- | :--- |
| `P6.05-L7` | Real exact-attachment live run | 🟩 Complete / PASS — [review](../reviews/P6-05-L7-attempt-2-real-exact-attachment-live-run.md) |
| `P6.05-L8` | Governed evidence admission | 🟩 Complete / PASS — [review](../reviews/P6-05-L8-attempt-2-governed-evidence-admission-and-closure.md) |
| `P6.05-L9` | Dogfooding friction capture | 🟩 Complete / PASS — [review](../reviews/P6-05-L9-dogfooding-friction-capture.md) |
| `P6.06` | Second materially distinct target selected and Product Contract boundary defined | 🟩 Complete / PASS — [contract](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md) |
| `P6.07 Stage 1` | Synthetic/offline second-product integration proof under P6.06 | 🟩 Complete / PASS — [review](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md) |
| `P6.07 Stage 2A` | Immutable pre-effect execution ticket + SHA-256 | 🟨 Implementation prepared; real Mac mini evidence pending — [review](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md) |
| `P6.07 Stage 2B` | One explicit real manual Discount Parser publication | 🟨 Pending — requires verified Stage 2A handoff + explicit real-action authorization |
| `P6.07 Stage 2C` | Outcome admission + CAP-004 reconstruction | 🟨 Pending — requires Stage 2B evidence |

## 6. Current Phase 6 state

- [x] First real Tender Operator integration evidence admitted and reconstructed.
- [x] P6.05 dogfooding friction captured without accidental architectural promotion.
- [x] Second materially distinct product/workflow selected.
- [x] Second Product Contract boundary canonically defined before governed reliance.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [x] Stage 2A generator, immutable handoff and verification tests prepared.
- [ ] Real Stage 2A Mac mini ticket/hash created and independently verified from actual Organization/human Actor context.
- [ ] One explicitly authorized real manual publication executed under P6.06 in Stage 2B.
- [ ] Exact Stage 2B outcome reconstructed through CAP-004 in Stage 2C.

Phase 6 remains `Active / In Progress`. The next governed action is P6.07 Stage 2A local execution on Mac mini. Scheduled/autopost operation remains outside the proof.
