# Arvectum OS Roadmap

Status: `Active / In Progress`
Version: `2.52.5`
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
| Phase 6 | Product validation | 🟨 Active / In Progress |

### Milestone continuity

Later-phase progress does not widen earlier milestone claims or collapse lifecycle dimensions.

| Phase | Scope | Execution | Status | Bounded milestone |
| :--- | :--- | :--- | :--- | :--- |
| `Phase 3` | Shared Platform Capabilities | Executed | 🟩 Complete | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Executed | 🟩 Complete | `M4` Internal workspace/operator baseline |
| `Phase 5` | SDK / Contracts / Integration | Executed | 🟩 Complete | `M5` Internal integration baseline |
| `Phase 6` | Product-Driven Platform Validation | In progress | 🟨 Active / In Progress | Real-product evidence accumulation |

`M3` remains bounded to its validated shared-capability reference scope. CAP-001 through CAP-004 remain `Incubating / Provisional`; no Platform Capability is `Active` merely because later phases consume or validate it.

Phase status, Platform Capability lifecycle, Product Contract lifecycle, operational environment/readiness and conformance maturity remain distinct.

## 3. Phase 6 Breakdown

| Task | Description | Status |
| :--- | :--- | :--- |
| `P6.01` | Validation target selection | 🟩 Complete |
| `P6.02` | First Product Contract | 🟩 Complete |
| `P6.03` | First real integration | 🟩 Complete / PASS |
| `P6.04` | Value/friction capture | 🟩 Complete / PASS |
| `P6.05` | Platform-gap remediation | 🟩 Complete / PASS — L1-L9 complete; real 7/7 GOVERNED |
| `P6.06` | Second materially distinct real target + Product Contract boundary | 🟩 Complete / PASS — Discount Parser / controlled Telegram publication |
| `P6.07` | Second real product/workflow platform integration | 🟨 In Progress — Stage 1 Complete / PASS; Stage 2 real publication pending |

## 4. P6.05 Detail

Status: `Complete / PASS`
Plan: [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md)

L1-L9 are complete. Real 7/7 tender attachment evidence for notice `0344100006426000005` is admitted and GOVERNED. L9 captured dogfooding friction and distinguished resolved blockers/defects from non-blocking improvement candidates without automatic architecture, Knowledge, Product Contract or capability promotion.

## 5. P6.06 Detail

Status: `Complete / PASS`
Contract: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md)

The second materially distinct real target is **Arvectum Discount Parser**, bounded to a controlled Telegram publication workflow. The Provisional Product Contract `0.1.0` uses CAP-004 only and preserves all Offer/source/dedup/classification/scheduler/rule-memory/Telegram business semantics as product-owned.

P6.06 completion means the target is selected and the Product Contract boundary is canonical before governed reliance. It does **not** promote CAP-004 from `Incubating` or stabilize the Product Contract.

## 6. P6.07 Detail

Status: `In Progress — Stage 1 Complete / PASS; Stage 2 pending`
Review: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)

Stage 1 proves the Discount Parser controlled-publication workflow can reuse the existing CAP-004 integration seam under the exact P6.06 Provisional Product Contract `0.1.0`. The proof uses a product-owned fake Telegram adapter and no live network/secret, while preserving exact Product Contract, Organization, Actor, product-owned input/effect references, provenance, correlation, causation and reconstruction semantics.

All 10 P6.07 Stage 1 tests pass as part of the full Reference Python CI suite (`894` tests / `OK`). No blocking platform gap was found, so no new RFC/ADR, Platform Capability, CAP-004 promotion or product-domain transfer is justified by Stage 1.

P6.07 is not complete overall until one explicitly authorized real manual publication is executed and reconstructed through CAP-004. Scheduler/autopost activation is not part of that Stage 2 proof.

## 7. Current Exit State

- [x] First real integration and governed reconstruction completed.
- [x] First-product value/friction and platform-gap work completed.
- [x] Second materially distinct target selected.
- [x] Second Provisional Product Contract boundary defined.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [ ] One explicitly authorized real manual Discount Parser publication executed under P6.06 and reconstructed through CAP-004.

Phase 6 remains active. The next governed action is P6.07 Stage 2 under the existing P6.06 Product Contract; no capability promotion or Stable/public commitment is implied.
