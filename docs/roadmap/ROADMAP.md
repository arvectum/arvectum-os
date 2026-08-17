# Arvectum OS Roadmap

Status: `Active`
Version: `2.52.11`
Owner: ООО «Арвектум»

## 1. Overview

Arvectum OS is an operating system for organizational intelligence. This roadmap coordinates its evolution through governed phases.

## 2. Current Status

| Phase | Description | Status |
| :--- | :--- | :--- |
| Phase 1 | Kernel foundations | 🟩 Complete |
| Phase 2 | Core runtime | 🟩 Complete |
| Phase 3 | Capability incubation | 🟩 Complete |
| Phase 4 | Workspace & Experience | 🟩 Complete |
| Phase 5 | SDK & Contracts | 🟩 Complete |
| Phase 6 | Product validation | 🟩 Complete / PASS |

### Milestone continuity

Later-phase progress does not widen earlier milestone claims or collapse lifecycle dimensions.

| Phase | Scope | Execution | Status | Bounded milestone |
| :--- | :--- | :--- | :--- | :--- |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Internal workspace/operator baseline |
| `Phase 5` | SDK / Contracts / Integration | Executed | 🟩 Complete | `M5` Internal integration baseline |
| `Phase 6` | Product-Driven Platform Validation | Executed | 🟩 Complete / PASS | `M6` Real-product validation across two materially distinct workflows |

`M3` remains bounded to its validated shared-capability reference scope. CAP-001 through CAP-004 remain `Incubating / Provisional`; no Platform Capability is `Active` merely because later phases consume or validate it.

Phase status, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct. Phase 6 / M6 completion does not promote CAP-004, stabilize a Product Contract or establish a production/SLA/support commitment.

## 3. Phase 6 Breakdown

| Task | Description | Status |
| :--- | :--- | :--- |
| `P6.01` | Validation target selection | 🟩 Complete |
| `P6.02` | First Product Contract | 🟩 Complete |
| `P6.03` | First real integration | 🟩 Complete / PASS |
| `P6.04` | Value/friction capture | 🟩 Complete / PASS |
| `P6.05` | Platform-gap remediation | 🟩 Complete / PASS — L1-L9 complete; real 7/7 GOVERNED |
| `P6.06` | Second materially distinct real target + Product Contract boundary | 🟩 Complete / PASS — Discount Parser / controlled Telegram publication; post-first-real review PASS, no revision |
| `P6.07` | Second real product/workflow platform integration | 🟩 Complete / PASS — Stage 1, Stage 2A, Stage 2B and real Stage 2C CAP-004 reconstruction complete |

## 4. P6.05 Detail

Status: `Complete / PASS`
Plan: [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md)

L1-L9 are complete. Real 7/7 tender attachment evidence for notice `0344100006426000005` is admitted and GOVERNED. L9 captured dogfooding friction and distinguished resolved blockers/defects from non-blocking improvement candidates without automatic architecture, Knowledge, Product Contract or capability promotion.

## 5. P6.06 Detail

Status: `Complete / PASS`
Contract: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md)
Post-first-real-publication review: [`P6-06-post-first-real-publication-contract-review.md`](../reviews/P6-06-post-first-real-publication-contract-review.md)

The second materially distinct real target is **Arvectum Discount Parser**, bounded to a controlled Telegram publication workflow. The Provisional Product Contract `0.1.0` uses CAP-004 only and preserves all Offer/source/dedup/classification/scheduler/rule-memory/Telegram business semantics as product-owned.

Stage 2B satisfied the Product Contract's first-real-publication review trigger. The canonical review found no material boundary defect or dependency gap: the existing Product Contract remains `Provisional 0.1.0`, CAP-004-only. This is continuity of the existing Provisional boundary, not stabilization, capability promotion or a new public/commercial commitment.

## 6. P6.07 Detail

Status: `Complete / PASS`
Stage 1 review: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)
Stage 2A preparation: [`P6-07-stage-2a-pre-effect-ticket-preparation.md`](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md)
Stage 2A real execution: [`P6-07-stage-2a-real-mac-mini-execution.md`](../reviews/P6-07-stage-2a-real-mac-mini-execution.md)
Stage 2B preparation: [`P6-07-stage-2b-windows-manual-publication-preparation.md`](../reviews/P6-07-stage-2b-windows-manual-publication-preparation.md)
Stage 2B real execution: [`P6-07-stage-2b-real-windows-manual-publication.md`](../reviews/P6-07-stage-2b-real-windows-manual-publication.md)
Stage 2C preparation: [`P6-07-stage-2c-mac-mini-cap004-reconstruction-preparation.md`](../reviews/P6-07-stage-2c-mac-mini-cap004-reconstruction-preparation.md)
Stage 2C real execution: [`P6-07-stage-2c-real-mac-mini-cap004-reconstruction.md`](../reviews/P6-07-stage-2c-real-mac-mini-cap004-reconstruction.md)

Stage 1 proved that the Discount Parser controlled-publication workflow can reuse the existing CAP-004 integration seam under the exact P6.06 Provisional Product Contract `0.1.0`, using a product-owned fake Telegram adapter and no live network/secret. No blocking platform gap was found.

Stage 2 then completed the bounded real-effect chain:

1. `Stage 2A` — **Complete / PASS.** Mac mini reused the existing P6.05-L4 Organization/human Actor context, verified the exact P6.06 contract pin and created one immutable pre-effect execution ticket plus SHA-256 before any real send. No product/Telegram effect occurred.
2. `Stage 2B` — **Complete / PASS.** One explicitly authorized real native-Windows publication executed through the existing product-owned `publish_offer()` path. Offer `148` produced Publication `14`, exactly one Telegram `send_message`, terminal product state `published`, Telegram message id `27`, human external confirmation `PASS`, and independently reconciled pre-effect/outcome evidence. No retry or repository mutation occurred.
3. `Stage 2C` — **Complete / PASS.** The minimized Stage 2B handoff was transferred Windows → Mac mini through owner-controlled SCP and verified at exact SHA-256 `b7a8ae4b263cec8f7498d482634c35b9df4356283e23133aeb73d8041c9c4cc5`. The Mac mini then verified the exact Stage 2A ticket, Product Contract and Stage 2B provenance and completed read-only CAP-004 reconstruction with `18` evidence items and `9` material references. Targeted Stage 2C tests passed (`9`); the full Reference Python suite passed (`911`). Network calls, Telegram calls, publication replay, product DB mutations, canonical state mutations and external mutations were all zero. No retroactive platform gate decision or retroactive Windows-native Event was fabricated.

The immutable owner-local Stage 2C report SHA-256 is `370a245601b88766c77bbac05a226d0e9fb680fa52fda3c2f946d062603199a1`. Raw Organization/Actor identities, reusable secrets and raw Windows evidence remain outside canonical repository evidence.

P6.07 validates the declared CAP-004-only product/platform boundary through a materially distinct real product/workflow. P6.06 remains `Provisional 0.1.0`; CAP-004 remains `Incubating / Provisional`.

## 7. Current Exit State

- [x] First real integration and governed reconstruction completed.
- [x] First-product value/friction and platform-gap work completed.
- [x] Second materially distinct target selected.
- [x] Second Provisional Product Contract boundary defined.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [x] Stage 2A immutable ticket/hash generator and verification tests prepared.
- [x] Real Stage 2A Mac mini ticket/hash created and independently verified from actual Organization/human Actor context.
- [x] Stage 2B native-Windows one-send procedure and evidence boundary prepared without changing Discount Parser publication semantics.
- [x] One explicitly authorized real manual Discount Parser publication executed in Stage 2B with confirmed external effect and reconciled evidence integrity.
- [x] P6.06 post-first-real-publication review completed; Provisional 0.1.0 CAP-004-only boundary retained.
- [x] Stage 2C minimized evidence handoff and CAP-004 reconstruction procedure prepared without external-effect replay.
- [x] Exact real Stage 2B outcome reconstructed through CAP-004 on Mac mini in Stage 2C with read-only derived evidence and zero effect replay.

`Phase 6 = Complete / PASS` for its declared bounded scope. All tasks currently defined by the canonical roadmap through P6.07 are complete.

The current canonical roadmap defines no task or phase after P6.07 / Phase 6. The next governed action is therefore **canonical roadmap extension / next-phase definition** before additional platform-development sequencing is claimed. Completion of M6 does not by itself imply a Phase 7 scope, capability promotion, Stable Product Contract, production readiness or public/commercial commitment.