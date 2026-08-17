# P6.07 — Stage 2C real Mac mini CAP-004 reconstruction

Status: `Complete / PASS`  
P6.07 overall status: `Complete / PASS`  
Phase 6 exit assessment: `Complete / PASS`  
Date: `2026-08-17`  
Owner: ООО «Арвектум»

## 1. Governance basis

- Constitution: `1.2.0`, `Ratified`;
- task classification: `product_contract`, with secondary `platform`, `product_specific` and `governance` evidence;
- Accepted RFC checked: RFC-0001, RFC-0002, RFC-0003, RFC-0004, RFC-0005, RFC-0006;
- relevant Accepted ADR: none;
- canonical P6.06 Product Contract: `Provisional 0.1.0`;
- exact Product Contract blob SHA: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- shared dependency: CAP-004 Audit / Reconstruction Support only;
- CAP-004 lifecycle remains `Incubating`, contract remains `Provisional`;
- Stage 2A: `Complete / PASS`;
- Stage 2B: `Complete / PASS`;
- Stage 2C preparation: `PASS / CI verified`.

This review records the completed real reconstruction evidence. It does not amend Constitution or an Accepted RFC/ADR, create a new Product Contract Version, stabilize the P6.06 Product Contract, promote CAP-004, create operational-readiness/SLA/support claims, or create a public/conformance commitment.

## 2. Canonical implementation baseline

The real Mac mini run used canonical repository `arvectum/arvectum-os`, branch `main`, at exact SHA:

`791b63efa997b5de8120858bb64b2abe34051598`

Verified immutable pins:

- Stage 2C preparation commit is an ancestor: `YES`;
- Stage 2C implementation blob: `5566b5e3e2e643d9afba40b644d1306b7cd898db`;
- P6.06 Product Contract blob: `23bbe792b81ddc5da736333d8a92580a718f920e`;
- Stage 2B canonical review blob: `4b2cfa04ce92d3a8978cfd41f790358936925014`;
- Stage 2B closure commit: `725aeef0bb13376c9045da26a30401947e12d0ed` remains in history.

The tracked working tree was clean before and after local execution.

## 3. Exact Stage 2 continuity

The reconstruction preserved the exact Stage 2 execution identity:

`p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126`

Stage 2A owner-local ticket:

`~/.arvectum-os/p6-07-stage2a/20260817T085109Z-bc495068ab8e/p6-07-stage2-execution-ticket.json`

Exact Stage 2A ticket SHA-256:

`d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7`

Independent ticket verification: `PASS`.

The reconstruction loaded the raw Organization and attributable human Actor only from the owner-local Stage 2A ticket and used those identities in-memory. The Stage 2C report did not write or expose either raw opaque identity.

Continuity results:

- Product Contract `0.1.0`: `PASS`;
- Organization continuity: `PASS`;
- Actor continuity: `PASS`;
- pre-effect SHA continuity: `PASS`;
- outcome SHA continuity: `PASS`.

## 4. Windows-to-Mac minimized evidence handoff

The Stage 2B minimized handoff created on the Windows evidence-owner host was transferred to the Mac mini through owner-controlled SCP.

Mac mini inbound path:

`~/.arvectum-os/p6-07-stage2c/inbound/p6-07-stage2b-minimized-handoff.json`

Exact handoff SHA-256:

`b7a8ae4b263cec8f7498d482634c35b9df4356283e23133aeb73d8041c9c4cc5`

Transfer integrity was independently verified on both hosts:

- Windows source SHA verification: `PASS`;
- Mac calculated JSON SHA: exact match;
- Mac sidecar SHA: exact match;
- raw Stage 2B `pre-effect.json` / `outcome.json` transferred: `NO`;
- Stage 2A raw ticket transferred from Windows: `NO`.

The minimized handoff therefore remained bound to the retained Windows evidence without migrating the raw product evidence payloads.

## 5. Stage 2B evidence reconstructed

The handoff retained the already canonically reviewed real Stage 2B facts:

- Discount Parser execution repository SHA: `b6ba4e0808d640e938bdd53eb1cf87b2416cca10`;
- Offer: `148`;
- Publication: `14`;
- target: `@arvectumtest`;
- template: `v2-configurable`;
- Telegram message id: `27`;
- result: `published`;
- external confirmation: `PASS`;
- reconciliation required: `NO`;
- pre-effect SHA-256: `d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4`;
- outcome SHA-256: `6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a`.

All nine required material reference groups were present in the minimized handoff. Optional parse-run/source references were not required for completeness of this fixed execution.

## 6. Regression evidence

Before reconstruction the real Mac mini run executed:

- Stage 2C targeted suite: `9 PASS`;
- full Reference Python suite: `911 PASS`.

No fail-closed condition was bypassed.

## 7. CAP-004 reconstruction result

The existing CAP-004 integration seam reconstructed the already completed Stage 2B effect as read-only derived evidence.

Result:

- dependency: `CAP-004` only;
- operation: read-only reconstruction;
- reconstruction complete: `YES`;
- CAP-004 evidence item count: `18`;
- material reference count: `9`;
- fabricated retroactive platform gate decision: `NO`;
- retroactive Windows Native platform Event claimed: `NO`.

The Stage 2C admission reference is explicitly a reconstruction-time derived admission reference. It does not rewrite Stage 2B history or claim that a Native Arvectum OS Event existed on the Windows host before or during the Telegram effect.

The real one-time human authorization remains product/local retained evidence. Stage 2C does not transform that evidence into a fabricated retroactive `GovernedGateDecision`.

## 8. Containment and replay safety

Observed/reported containment for the Stage 2C reconstruction:

```text
network calls = 0
Telegram calls = 0
publish_offer calls = 0
product DB mutations = 0
canonical state mutations = 0
external mutations = 0
Telegram effect replayed = NO
```

This satisfies the RFC-0006 replay-safety boundary: historical evidence was reconstructed without repeating the external effect and without a new authorization for a new consequential action.

## 9. Immutable owner-local Stage 2C evidence

Owner-local report:

`~/.arvectum-os/p6-07-stage2c/20260817T130440Z-791b63efa997/p6-07-stage2c-reconstruction.json`

Exact Stage 2C report SHA-256:

`370a245601b88766c77bbac05a226d0e9fb680fa52fda3c2f946d062603199a1`

Verification:

- report SHA sidecar independent verification: `PASS`;
- structural report validation: `PASS`;
- raw Organization identity written/exposed: `NO`;
- raw Actor identity written/exposed: `NO`;
- reusable secrets written/exposed: `NO`.

The raw local report remains owner-local and is not committed to Git. Canonical repository evidence records only minimized safe facts and immutable digests.

## 10. Product / Platform boundary review

The real Stage 2C result does not reveal a need to widen the P6.06 Product Contract.

- CAP-004 remains the only shared dependency required for this proof;
- Discount Parser Offer/source/rule/template/publication/Telegram semantics remain product-owned;
- reconstruction remains derived and non-authoritative;
- no product-local schema or workflow is promoted into shared platform behavior;
- no hidden platform dependency was introduced;
- no new Product Contract version is justified by this run.

Therefore P6.06 remains `Provisional 0.1.0` with exact blob `23bbe792b81ddc5da736333d8a92580a718f920e`.

## 11. Capability lifecycle review

P6.07 establishes materially distinct real-product reuse evidence for CAP-004, but materially distinct reuse is not sufficient on its own for `Active` admission.

CAP-004 therefore remains:

- lifecycle: `Incubating`;
- capability contract: `Provisional`;
- public/stable support commitment: none.

The existing capability catalog requires a separate RFC-0001 admission decision plus stable supported contract, compatibility/migration and operational-readiness evidence before `Active` promotion. P6.07 does not substitute for that gate.

## 12. Functional cross-review

A bounded functional cross-review was performed against the real Stage 2C evidence.

### Product Contract

No material dependency gap, boundary widening, hidden coupling, lifecycle mismatch or Product Contract revision requirement was found.

### Governed Execution / authority

The exact Product Contract, Organization and human Actor continuity were preserved. Stage 2C created no authorization, Organizational Authority or retrospective approval.

### Event / provenance / replay

The reconstruction remained read-only, preserved exact evidence references and did not replay the historical Telegram effect. No retroactive Native Windows Event was fabricated.

### Security / minimization

Raw opaque identities, reusable secrets and raw Windows evidence were not admitted into repository evidence. Cross-host transfer contained only the minimized handoff and its digest sidecar.

### Platform lifecycle

No evidence justifies CAP-004 `Active` promotion, Product Contract stabilization, a new Platform Capability or a new ADR.

`Cross-review result: PASS — no material objections remaining.`

This functional cross-review is evidence review only. It is not formal RFC/ADR acceptance, lifecycle promotion, operational-readiness approval or commercial approval.

## 13. P6.07 result

`P6.07 = Complete / PASS`.

The full bounded second-product integration chain is now complete:

1. Stage 1 — synthetic/offline Product Contract integration proof: PASS;
2. Stage 2A — real Mac mini immutable pre-effect execution ticket: PASS;
3. Stage 2B — one explicitly authorized real Windows Discount Parser publication: PASS;
4. Stage 2C — real Mac mini CAP-004 read-only reconstruction: PASS.

The second materially distinct real product/workflow has therefore been exercised through the declared CAP-004-only platform boundary with exact Product Contract, Organization, Actor, evidence and effect continuity.

## 14. Phase 6 exit assessment

The canonical Phase 6 task set currently contains P6.01 through P6.07. With this Stage 2C result, every listed Phase 6 task is complete.

The Phase 6 goal — validate platform fitness through real product use and materially distinct reuse evidence without prematurely transferring product-local behavior into platform responsibility — is satisfied for the declared bounded scope.

`Phase 6 = Complete / PASS.`

This milestone does not imply full-platform conformance, production readiness, Stable Product Contracts, `Active` Platform Capabilities, SLA/support readiness or a new commercial commitment.

The current canonical roadmap contains no task after P6.07. A subsequent development phase must therefore be introduced explicitly through a future canonical roadmap update rather than inferred from chat context or from completion of Phase 6.