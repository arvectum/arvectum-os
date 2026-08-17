# Phase 6: Product-driven platform validation

Status: `Complete / PASS`
Version: `1.2.10`

## 1. Goal

Validate platform fitness through real product use and materially distinct reuse evidence without turning product-local behavior into platform responsibility prematurely.

`Goal result: achieved for the declared bounded Phase 6 scope.`

Phase 6 completion does not imply full-platform conformance, production readiness, Stable Product Contracts, `Active` Platform Capabilities, SLA/support readiness or a new commercial commitment.

## 2. P6.05: Real evidence admission

Status: `Complete / PASS`
Evidence: [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md)

L1 through L9 are complete. L7 produced truthful real 7/7 evidence. L8 admitted and reconstructed that evidence under governed execution. L9 captured the observed dogfooding friction without silently promoting observations into architecture, Knowledge, Product Contract changes or capability lifecycle decisions.

## 3. P6.06: Second materially distinct real target

Status: `Complete / PASS`
Evidence: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md)
Post-first-real-publication review: [`P6-06-post-first-real-publication-contract-review.md`](../reviews/P6-06-post-first-real-publication-contract-review.md)

P6.06 selects **Arvectum Discount Parser** and the controlled Telegram publication workflow as the second real validation target. The selection is materially distinct from the first Tender Operator workflow because it introduces scheduled/machine initiation, an actual consequential external mutation, duplicate/idempotency pressure, possible uncertain external outcome and reconciliation requirements.

The canonical Provisional Product Contract `0.1.0` defines a deliberately narrow **CAP-004-only** shared dependency. Offer/source schemas, normalization, deduplication, classification, scheduler, rule memory, publication filters, Telegram integration, product ledger and UX remain product-owned. CAP-001, CAP-002 and CAP-003 are deliberately omitted from this contract version.

Stage 2B triggered the contract's post-first-real-publication review condition. The review found no material boundary defect or dependency gap and therefore requires no new Product Contract Version: P6.06 remains `Provisional 0.1.0`, CAP-004-only. This does not stabilize the contract or promote CAP-004.

## 4. P6.07: Second real product/workflow platform integration

Status: `Complete / PASS`
Stage 1 review: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)
Stage 2A preparation: [`P6-07-stage-2a-pre-effect-ticket-preparation.md`](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md)
Stage 2A real execution: [`P6-07-stage-2a-real-mac-mini-execution.md`](../reviews/P6-07-stage-2a-real-mac-mini-execution.md)
Stage 2B preparation: [`P6-07-stage-2b-windows-manual-publication-preparation.md`](../reviews/P6-07-stage-2b-windows-manual-publication-preparation.md)
Stage 2B real execution: [`P6-07-stage-2b-real-windows-manual-publication.md`](../reviews/P6-07-stage-2b-real-windows-manual-publication.md)
Stage 2C preparation: [`P6-07-stage-2c-mac-mini-cap004-reconstruction-preparation.md`](../reviews/P6-07-stage-2c-mac-mini-cap004-reconstruction-preparation.md)
Stage 2C real execution: [`P6-07-stage-2c-real-mac-mini-cap004-reconstruction.md`](../reviews/P6-07-stage-2c-real-mac-mini-cap004-reconstruction.md)

P6.07 validates the P6.06 boundary against executable Discount Parser controlled-publication evidence.

### Stage 1 — synthetic/offline proof

Stage 1 completed with PASS:

- exact P6.06 Product Contract `0.1.0` continuity preserved;
- only CAP-004 consumed;
- shared integration adapter seam used instead of platform internals;
- synthetic/offline evidence preserved Organization, Actor, contract, product-owned inputs, pre-effect reservation/intent, outcome, correlation, causation and provenance;
- duplicate, missing evidence, wrong Organization, missing current provider evidence and uncertain outcome paths remained fail-closed/reconciliation-safe;
- no live Telegram call, credential, scheduler/autopost activation or product database migration occurred;
- then-current full Reference Python CI suite: `894` tests / `OK`.

No blocking platform gap was found and no new RFC/ADR, Platform Capability, CAP-004 promotion or product-domain transfer was justified.

### Stage 2A — real Mac mini pre-effect ticket

`Complete / PASS.`

The real Mac mini run reused the existing P6.05-L4 Organization/human Actor context, verified the exact P6.06 contract pin, created one immutable execution ticket and SHA-256 before any real external effect and independently verified the digest.

- execution id: `p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`;
- ticket SHA-256: `d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`;
- targeted Stage 2A tests: `8 PASS`;
- full Reference Python suite: `902 PASS`;
- product/Telegram/external effect: zero.

### Stage 2B — real Windows Discount Parser publication

`Complete / PASS.`

One eligible text-only product Offer (`148`) was fixed for `@arvectumtest`, scheduler/autopost and competing publishers were disabled, and a separate explicit one-time human authorization was obtained.

The existing product-owned `publish_offer()` created durable Publication `14` in `pending` before the external call and delegated exactly one `send_message` and zero `send_photo` calls. Product state finished `published`, Telegram returned message id `27`, and the human operator visually confirmed that exact message in the intended target.

Independent post-run digest reconciliation verified:

- pre-effect SHA-256: `d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4`;
- outcome SHA-256: `6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a`;
- retry: none;
- reconciliation required: `NO`;
- repository mutation: none.

### Stage 2C — real Mac mini CAP-004 reconstruction

`Complete / PASS.`

The Windows evidence-owner host created the prepared minimized handoff from the retained Stage 2B evidence. It contained all nine required material reference groups and no raw Windows evidence payload, reusable secret or raw Organization/Actor identity.

The handoff was transferred Windows → Mac mini through owner-controlled SCP. Exact transfer digest:

`b7a8ae4b263cec8f7498d482634c35b9df4356283e23133aeb73d8041c9c4cc5`

Windows source, Mac transferred bytes and Mac sidecar all independently matched this SHA-256.

The Mac mini then verified:

- canonical repository SHA: `791b63efa997b5de8120858bb64b2abe34051598`;
- Stage 2C implementation blob: `5566b5e3e2e643d9afba40b644d1306b7cd898db`;
- Product Contract blob: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- Stage 2B review blob: `4b2cfa04ce92d3a8978cfd41f790358936925014`;
- exact Stage 2A ticket SHA;
- exact Stage 2B handoff SHA;
- exact Product Contract, Organization and attributable human Actor continuity.

Pre-reconstruction tests:

- Stage 2C targeted suite: `9 PASS`;
- full Reference Python suite: `911 PASS`.

CAP-004 result:

- dependency: CAP-004 only;
- read-only: `YES`;
- reconstruction complete: `YES`;
- evidence item count: `18`;
- material reference count: `9`;
- fabricated retroactive platform gate decision: `NO`;
- retroactive Windows Native Event claimed: `NO`.

Containment:

```text
network calls = 0
Telegram calls = 0
publish_offer calls = 0
product DB mutations = 0
canonical state mutations = 0
external mutations = 0
Telegram effect replayed = NO
```

Owner-local immutable Stage 2C report SHA-256:

`370a245601b88766c77bbac05a226d0e9fb680fa52fda3c2f946d062603199a1`

The report passed independent digest and structural validation. Raw Organization/Actor identity values and reusable secrets were not written or exposed.

Neither the Product Contract nor the Stage 2A ticket granted authorization for the Stage 2B external mutation; authorization was separately obtained from the human operator. Stage 2C reconstructed the already confirmed effect and did not authorize or replay it.

P6.07 therefore closes `Complete / PASS` without widening the P6.06 Product Contract. P6.06 remains `Provisional 0.1.0`; CAP-004 remains `Incubating / Provisional`.

## 5. Subtasks / completed evidence

| Task | Outcome | Evidence |
| :--- | :--- | :--- |
| `P6.05-L7` | Real exact-attachment live run | 🟩 Complete / PASS — [review](../reviews/P6-05-L7-attempt-2-real-exact-attachment-live-run.md) |
| `P6.05-L8` | Governed evidence admission | 🟩 Complete / PASS — [review](../reviews/P6-05-L8-attempt-2-governed-evidence-admission-and-closure.md) |
| `P6.05-L9` | Dogfooding friction capture | 🟩 Complete / PASS — [review](../reviews/P6-05-L9-dogfooding-friction-capture.md) |
| `P6.06` | Second materially distinct target selected and Product Contract boundary defined | 🟩 Complete / PASS — [contract](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md) |
| `P6.06 review` | Post-first-real-publication review condition | 🟩 Complete / PASS — no contract revision required |
| `P6.07 Stage 1` | Synthetic/offline second-product integration proof under P6.06 | 🟩 Complete / PASS — [review](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md) |
| `P6.07 Stage 2A` | Immutable pre-effect execution ticket + SHA-256 | 🟩 Complete / PASS — [real execution review](../reviews/P6-07-stage-2a-real-mac-mini-execution.md) |
| `P6.07 Stage 2B` | One explicit real manual Discount Parser publication | 🟩 Complete / PASS — [real execution review](../reviews/P6-07-stage-2b-real-windows-manual-publication.md) |
| `P6.07 Stage 2C` | Outcome admission + CAP-004 reconstruction | 🟩 Complete / PASS — [real execution review](../reviews/P6-07-stage-2c-real-mac-mini-cap004-reconstruction.md) |

## 6. Phase 6 exit state

- [x] First real Tender Operator integration evidence admitted and reconstructed.
- [x] P6.05 dogfooding friction captured without accidental architectural promotion.
- [x] Second materially distinct product/workflow selected.
- [x] Second Product Contract boundary canonically defined before governed reliance.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [x] Stage 2A generator, immutable handoff and verification tests prepared.
- [x] Real Stage 2A Mac mini ticket/hash created and independently verified from actual Organization/human Actor context.
- [x] Stage 2B native-Windows one-send execution procedure and evidence boundary prepared without changing product publication semantics.
- [x] One explicitly authorized real manual publication executed under P6.06 in Stage 2B, with confirmed Telegram effect and reconciled local evidence digests.
- [x] P6.06 post-first-real-publication review completed; Provisional 0.1.0 CAP-004-only boundary retained.
- [x] Stage 2C minimized evidence handoff prepared and transferred with independently verified integrity.
- [x] Exact real Stage 2B outcome reconstructed through CAP-004 on Mac mini in Stage 2C with complete read-only derived evidence and zero effect replay.

`Phase 6 = Complete / PASS`.

The declared Phase 6 goal is satisfied through two materially distinct real-product/workflow validation chains while preserving product/platform boundaries and capability/Product Contract lifecycle separation.

## 7. M6 disposition and next governed action

`M6 — Product-driven platform validation = achieved for the bounded Phase 6 scope.`

M6 does not imply:

- full-platform conformance;
- production readiness;
- Stable Product Contracts;
- `Active` Platform Capabilities;
- SLA/support readiness;
- automatic commercialization commitments;
- automatic admission of product-owned workflows/schemas/rules into the platform.

The current canonical roadmap contains no Phase 6 task after P6.07 and no subsequent phase. Therefore no further development sequence may be inferred from chat context alone.

The next governed action is **canonical roadmap extension / next-phase definition**. Any subsequent phase, milestone or work item must be introduced explicitly in the canonical roadmap with scope and sequencing before it is treated as the next Arvectum OS action.