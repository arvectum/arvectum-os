# Arvectum OS Roadmap

Status: `Active / In Progress`
Version: `2.52.7`
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
| `P6.07` | Second real product/workflow platform integration | 🟨 In Progress — Stage 1 Complete / PASS; Stage 2A Complete / PASS; Stage 2B pending |

## 4. P6.05 Detail

Status: `Complete / PASS`
Plan: [`P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md`](P6-05-LOCAL-INTERNAL-RUNTIME-SUBSTREAM.md)

L1-L9 are complete. Real 7/7 tender attachment evidence for notice `0344100006426000005` is admitted and GOVERNED. L9 captured dogfooding friction and distinguished resolved blockers/defects from non-blocking improvement candidates without automatic architecture, Knowledge, Product Contract or capability promotion.

## 5. P6.06 Detail

Status: `Complete / PASS`
Contract: [`P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md)

The second materially distinct real target is **Arvectum Discount Parser**, bounded to a controlled Telegram publication workflow. The Provisional Product Contract `0.1.0` uses CAP-004 only and preserves Offer/source/dedup/classification/scheduler/rule-memory/Telegram business semantics as product-owned.

P6.06 completion means the target is selected and the Product Contract boundary is canonical before governed reliance. It does **not** promote CAP-004 from `Incubating` or stabilize the Product Contract.

## 6. P6.07 Detail

Status: `In Progress — Stage 1 Complete / PASS; Stage 2A Complete / PASS; Stage 2B pending`

Evidence:

- Stage 1: [`P6-07-stage-1-second-real-product-workflow-integration.md`](../reviews/P6-07-stage-1-second-real-product-workflow-integration.md)
- Stage 2A preparation: [`P6-07-stage-2a-pre-effect-ticket-preparation.md`](../reviews/P6-07-stage-2a-pre-effect-ticket-preparation.md)
- Stage 2A real execution: [`P6-07-stage-2a-real-mac-mini-execution.md`](../reviews/P6-07-stage-2a-real-mac-mini-execution.md)

Stage 1 proved the Discount Parser controlled-publication workflow can reuse the existing CAP-004 integration seam under the exact P6.06 Provisional Product Contract `0.1.0`, while preserving Product Contract, Organization, Actor, product-owned evidence, provenance, correlation, causation and reconstruction semantics. No blocking platform gap was found.

Stage 2 uses a bounded three-part handoff:

1. `Stage 2A` — **Complete / PASS.** Mac mini reused the existing P6.05-L4 Organization/human Actor context, verified the exact P6.06 contract pin, created and independently verified one immutable pre-effect ticket plus SHA-256, and kept evidence outside source control. Targeted tests passed (`8`) and the full Reference Python suite passed (`902`). No external/product effect occurred.
2. `Stage 2B` — **Pending.** Windows Discount Parser must bind the exact Stage 2A handoff, record product-owned candidate/target/reservation/intent plus explicit real-action authorization before the external action, and perform at most one human-operated manual publication. Scheduler/autopost remains disabled.
3. `Stage 2C` — **Pending.** Mac mini must admit the Stage 2B outcome under the same execution/Organization/Actor/Product Contract continuity and reconstruct it through CAP-004 as read-only derived evidence.

Neither the P6.06 Product Contract nor the Stage 2A execution ticket grants authorization for the external mutation. P6.07 remains open until Stage 2C PASS.

## 7. Current Exit State

- [x] First real integration and governed reconstruction completed.
- [x] First-product value/friction and platform-gap work completed.
- [x] Second materially distinct target selected.
- [x] Second Provisional Product Contract boundary defined.
- [x] Second-product synthetic/offline bounded integration evidence executed under the P6.06 contract.
- [x] Stage 2A immutable ticket/hash generator and verification tests prepared.
- [x] Real Stage 2A Mac mini ticket/hash created and independently verified from actual Organization/human Actor context.
- [ ] One explicitly authorized real manual Discount Parser publication executed in Stage 2B.
- [ ] Exact Stage 2B outcome reconstructed through CAP-004 in Stage 2C.

Phase 6 remains active. The next governed action is **P6.07 Stage 2B — one explicit real manual Discount Parser publication on Windows**. No capability promotion or Stable/public commitment is implied by Stage 2A completion.
