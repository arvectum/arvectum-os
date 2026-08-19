# P7.06 — Live Operator Workspace Substream

Status: `Complete / PASS — UI4 selected-owner interaction closure PASS`
Version: `0.1.11`
Created: `2026-08-18`
Updated: `2026-08-19`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance`
Parent phase: [`PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor: `P7.06 — Governed deploy/update/rollback/version/migration path` — `Complete / PASS`
Architecture basis: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Workspace basis: Phase 4 / M4 coherent governed workspace baseline

## 1. Purpose

Turn the already-proven Phase 4 workspace semantics into a live owner-operated interaction surface over the persistent Mac mini Arvectum OS runtime.

Phase 4 deliberately remained UI-technology neutral. It proved Organization/Actor context, governed-object inspection, provenance/reconstruction, execution/gate presentation, Document/Artifact and Memory/Knowledge surfaces, bounded product entry and authority-safe UX through internal reference implementations and static HTML evidence. It did not establish a persistent browser application, public API, frontend framework or stable route contract.

This substream closes that operator-experience gap for the current `Persistent Internal / owner-operated` environment without turning a local UI adapter into a public platform contract.

## 2. Sequencing rule

The P7.06 governed deploy/update/rollback prerequisite and UI1 through UI4 are complete. The operator-workspace substream is closed and P7.07 is now the next canonical Phase 7 action.

```text
P7.06 governed update / rollback proof
        ↓ PASS
P7.06-UI1 live read-only workspace
        ↓ PASS
P7.06-UI2 governed interaction / preflight
        ↓ PASS
P7.06-UI3 persistent private operator access
        ↓ PASS
P7.06-UI4 first real owner interaction proof
        ↓ PASS
P7.07 persistent Tender Operator contour  ← NEXT
```

UI3 selected-Mac operational closure passed on exact canonical/runtime release `8451a5cb85c15ceb798438524f46cec87eacc981` after bounded runtime-consistency recovery, canonical-checkout governed update, 20-second exact-release stability verification and the complete supported UI3 proof. P7.03 and P7.04 remained unchanged; no Organizational Authority, consequential approval, real UI4 interaction, product/external effect or historical-effect replay occurred.

UI4 then closed the remaining `P7.06-UI` requirement on exact canonical/runtime release `1da5600963dcba982d3b1969480fd3f725133e12`. The owner successfully entered the real private workspace in Safari, confirmed Organization/Actor/runtime health, navigated Records, Executions, Evidence and Documents over the retained real `platform.document`, inspected exact Subject/Version plus Execution/Event/checkpoint provenance/reconstruction, observed all four action gates independently `Waiting`, and executed one browser preflight with result `WAITING / fail-closed`. The exact-release technical verifier independently passed with `browser_preflight_post_observed = true`, no Organizational Authority or consequential approval, no canonical mutation and no product/external effect. Owner-local minimized preflight evidence SHA-256: `63416f1862168d9a464a30d1824198ad52be4439e9f43fba71360c7ac34a9f91`.

The real owner session also exposed one material Safari unlock interoperability defect. PR `#73` remediated it without accepting missing/`null`/foreign Origin or weakening loopback Host/CSRF/P7.04 boundaries; final Reference Python CI `#150` passed and the selected Mac re-proof succeeded on the merged exact release. The overall `P7.06-UI` substream is therefore `100% / Complete / PASS`.

## 3. Operating boundary

The live workspace remains:

- internal and owner-operated;
- bound to one explicit Organization and attributable human Actor context;
- private/loopback by default, with no public ingress;
- non-authoritative presentation over governed state;
- deny-by-default and fail-closed when identity, Organization, authorization or exact-source continuity is unresolved;
- unable to directly mutate canonical state outside Governed Execution;
- unable to create Organizational Authority or consequential approval through UI state;
- exact-release pinned and reversible;
- free of a public/stable API, route, SDK, browser-compatibility or support commitment.

Environment-specific launchd/loopback mechanics remain private reversible adapters, not platform architecture contracts.

## 4. Subtasks

### P7.06-UI1 — Live read-only governed workspace

Status: `Complete / PASS`.

UI1 connected the M4 workspace presentation semantics to the persistent runtime through a bounded internal adapter and proved browser-visible inspection of real retained governed state.

Closure evidence includes:

- exact selected-Mac release `b1b78ed9772727dda41b2e509675691f978957ec`;
- real retained `platform.document` item from the approved P6.05-L7 exact EIS evidence path;
- explicit Subject / exact Version / `External Reference` authority / CAP-001 + RFC-0006 + CAP-004 provenance visibility;
- wrong/unresolved Organization and revoked grant fail closed;
- no protected counts/content leak;
- no canonical or external mutation from browsing;
- owner-local bounded evidence SHA-256 `104f64790a36511ca30e14edb864d4b2e650ecf62f39f379685e8d893766a506`.

### P7.06-UI2 — Governed interaction and preflight

Status: `Complete / PASS`.

UI2 added bounded governed interaction/preflight over the existing Phase 4 / RFC-0005 path without direct-write shortcuts.

Closure evidence:

- implementation PR `#56`, merged as `a22ba781d32f64b7097aeaf05a90651308533811`;
- exact reviewed head `305faafb790e1387cac2aaafa348fbc4ac583797`;
- [`P7.06-UI2 Governed Interaction and Preflight Functional Review`](../reviews/P7-06-UI2-governed-interaction-functional-review.md) — `Complete / PASS`, five review/revise iterations;
- Reference Python CI run `32159051764` / `#107` — `success`;
- exact Subject/Version, provenance/reconstruction, related Execution and four independent Authorization / Organizational Authority / Data Governance / Consequential Approval states remain distinct;
- transient action intent enters only the existing operator-safety / Governed Execution path;
- blocked/waiting/uncertain/reconciliation-required/succeeded outcomes remain evidence-derived;
- no UI-local direct canonical write, ambient authority or optimistic-success path exists.

### P7.06-UI3 — Persistent private operator access

Status: `Complete / PASS`.

Repository implementation and bounded remediations provide:

- supervised exact-release macOS launchd process;
- strict `127.0.0.1` listener exposure attributed to the exact launchd PID;
- explicit configured-port collision failure before start;
- bounded listener-readiness polling after install/restart/secret rotation;
- existing exact human P7.04 UI1/UI2 grants as a prerequisite; UI3 creates no grant or authority;
- separate owner-only ingress secret exchanged for a bounded process-local browser session;
- restart/rotation invalidates the prior browser session;
- private material/log permission and secret-minimization checks;
- reversible install/start/status/restart/stop/uninstall;
- governed P7.06 update/rollback reconciliation without forking deployment semantics;
- hardened reconciliation that keeps the invoking controller while pinning service Python/module/plist to the actual resulting release, avoiding replay of a known historical lifecycle race;
- canonical-checkout deployment control for UI3 governed update/rollback, so the P7.06 deploy adapter runs only from the real canonical Git checkout while the private service remains exact-current pinned.

Canonical functional review: [`P7.06-UI3 — Functional cross-review`](../reviews/P7.06-UI3-functional-cross-review.md) — repository implementation review complete, maximum `7/7` review/revise iterations, no remaining material repository-scope objection.

Selected-Mac progression:

1. Attempt 1 failed closed because the selected human operator lacked the exact UI1+UI2 local grant set; a bounded owner-authorized P7.04 administrative step corrected that without granting Organizational Authority or changing P7.03 governed state.
2. Attempt 2 reached launchd installation but exposed listener-readiness ambiguity; PR `#62` remediated readiness/port-collision handling and later review iterations hardened multi-row listener validation.
3. Historical-release reconciliation was hardened in iteration 7 / PR `#64` so rollback does not replay the pre-remediation lifecycle controller.
4. Attempt 4 failed before closure after the runtime `current` pointer was observed inconsistent with the release still represented by the live runtime process.
5. PR `#65` forensics classified the actual condition as `UPDATE_COMMAND_FAILED`, not background rollback: `current = d5cb521bf2565c42ad8ccf47565dda18cf9106c6`, live P7.02 health release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5`, update exit code `7`, no new rollback/recovery evidence, P7.03 unchanged and P7.04 unchanged. Owner-local forensic attestation SHA-256: `89d1786f8dff7ebb0b745620701d1d7437f6c6d02e34bba0c37617468b1b365a`.
6. PR `#67`, merged as `fa8e0729974462a44d688f77194d7080d621e2ba`, hardened the selected-Mac proof entry point across historical rollback; `Reference Python CI #138` passed.
7. PR `#66`, merged as `e586084ea1292a3c0e22f888dc8ed5524c748732`, added bounded P7.06 runtime-consistency recovery; the combined head passed `Reference Python CI #141`.
8. PR `#69`, merged as `d4a675aed96a0358d0434a6bf7c50fc0f258b4e9`, added canonical-checkout UI3 governed lifecycle routing. Exact reviewed head `0410bb64674a2f7ba6074bdb37af878631c01f44` passed `Reference Python CI #142` / run `32216759667`.
9. Final selected-Mac closure then passed completely. Recovery reconciled `current` from `d5cb521bf2565c42ad8ccf47565dda18cf9106c6` to the proven live release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5`, with matching runtime/observer release pins and matching launchd/health PID. Recovery evidence SHA-256: `0df255294f8cc17f91aca0fc0ac4eb6eb95eb6085be1a78aeaac85d7c2d39ba3`.
10. The ordinary P7.06 governed update then advanced source `6d4d07aead603841ecce3c469dd46f5e0d58ccd5` to exact canonical target `8451a5cb85c15ceb798438524f46cec87eacc981` under transaction `5de0529aa4c8d478ae13639b12588815c7dfbe9714f6254a6e7dcfd61344ed4c`; 20-second P7.02/P7.05 stability passed.
11. The supported final UI3 proof passed install/readiness/PID attribution/private-material checks, unauthenticated and wrong-secret denial, owner-local unlock, bounded session, restart invalidation, uninstall/reinstall, governed rollback, historical reconciliation and final governed re-update. Final listener: `127.0.0.1:8766`; final active release: `8451a5cb85c15ceb798438524f46cec87eacc981`; P7.03 and P7.04 remained unchanged.
12. Controller evidence passed: `hardened_controller_runner_verified = true`, `historical_ui3_controller_replayed = false`, `canonical_checkout_deploy_controller_verified = true`, `release_snapshot_deploy_controller_invoked = false`. No real UI4 interaction, Organizational Authority, consequential approval, product/external effect or historical external effect replay occurred.

Canonical closure evidence: [`P7.06-UI3 — Selected-Mac Operational Closure`](../reviews/P7.06-UI3-selected-mac-operational-closure.md) — `Complete / PASS`.

Owner-local non-canonical evidence retained canonically only by safe basename/digest:

- recovery attestation SHA-256: `0df255294f8cc17f91aca0fc0ac4eb6eb95eb6085be1a78aeaac85d7c2d39ba3`;
- final UI3 attestation SHA-256: `05a30e20d1d6813ae786620fff8eb00544a04b87dfe5dabc07c2078d19b90f66`.

Historical supporting reviews:

- [`P7.06-UI3 — Selected-Mac runtime-pointer investigation`](../reviews/P7.06-UI3-selected-mac-runtime-pointer-investigation.md);
- [`P7.06 — Runtime consistency recovery review`](../reviews/P7.06-runtime-consistency-recovery-review.md);
- [`P7.06-UI3 — Proof harness historical-controller review`](../reviews/P7.06-UI3-proof-harness-historical-controller-review.md);
- [`P7.06-UI3 — Canonical governed controller review`](../reviews/P7.06-UI3-canonical-governed-controller-review.md) — `Complete / PASS` for repository remediation.

UI3 closure creates no external/customer Production, public/stable UI/API/session contract, lifecycle promotion, Stable Product Contract, SLA/support or broader conformance claim.

### P7.06-UI4 — First real owner interaction proof

Status: `Complete / PASS`.

The owner completed the required real interaction session against the selected Mac mini persistent runtime on exact canonical/runtime release `1da5600963dcba982d3b1969480fd3f725133e12`.

Closure evidence:

- live Safari workspace unlock and session — `PASS` after bounded PR `#73` browser-Origin remediation;
- explicit Organization `aa4e760c379c8952aba6c6c335f3e233`, attributable human Actor `e4fc60984850106dbfc922ba30ec2332` and healthy exact runtime visibly confirmed;
- Records, Executions, Evidence and Documents navigated using real retained governed state;
- retained `platform.document` Subject `document-subject/eis-0344100006426000005-exact-attachment-evidence@aa4e760c379c8952aba6c6c335f3e233` and exact Version `document-version/eis-0344100006426000005-74e943d855406b04@aa4e760c379c8952aba6c6c335f3e233` inspected;
- authority remained `External Reference`, authoritative source remained `ЕИС / zakupki.gov.ru`;
- exact Execution Version `execution-version/p7-06-ui1-real-state-74e943d855406b04-v5@aa4e760c379c8952aba6c6c335f3e233`, admitted Event Version `event-version/p7-06-ui1-document-admitted-74e943d855406b04-v1@aa4e760c379c8952aba6c6c335f3e233`, checkpoint `582ec80686ce5d2bb3b1eb5779c2fdce3b6899379161e9a953c64e4dcf11d5f7` and `CAP-004 reconstruction complete` were visible;
- Authorization, Organizational Authority, Data Governance and Consequential Approval all remained independently `Waiting`;
- the owner clicked `Run governed preflight` once and received `Preflight executed: WAITING / fail-closed. No canonical mutation or external effect was requested.`;
- exact-release technical verifier returned `PASS`, `browser_preflight_post_observed = true`, technical interaction access true, Organizational Authority/approval false, canonical mutation false and product/external effect false;
- owner-local minimized evidence basename `p7-06-ui4-owner-preflight-last.json`, SHA-256 `63416f1862168d9a464a30d1824198ad52be4439e9f43fba71360c7ac34a9f91`;
- [`P7.06-UI4 — First real owner interaction closure`](../reviews/P7.06-UI4-first-real-owner-interaction-closure.md) — `Complete / PASS`, four functional review/revise iterations, no remaining material objection.

The technical verifier intentionally cannot self-attest human visual navigation or operator-friction judgment. The canonical closure review combines its exact machine evidence with the owner's direct visual observations rather than treating automation as authority over the human-proof requirement.

The material operator-friction defect found by the real owner proof was preserved rather than hidden: the original Safari unlock attempt failed before secret validation; a secret-safe direct HTTP diagnostic isolated the browser metadata boundary; PR `#73` changed only `Referrer-Policy: no-referrer` to `same-origin` while preserving exact Host/Origin/CSRF/P7.04 fail-closed checks; final Reference Python CI `#150` passed; selected-Mac governed update and Safari re-proof then succeeded.

`P7.06-UI = Complete / PASS` because the owner can now both inspect live real governed state and exercise a real bounded interaction through the existing runtime authority/security boundary.

## 5. Relationship to Phase 4

This substream reuses the already-proven M4 semantics rather than redesigning the workspace from scratch: explicit Organization/Actor context, domain-neutral navigation, Canonical Record / Relationship inspection, exact version/Event/provenance/reconstruction, Governed Execution/gate/approval-action experience, Document/Artifact, Memory/Knowledge/Search, cross-capability composition and authority-safe UX.

The new work is operational connection and interaction, not a new semantic workspace model.

## 6. ADR and stable-boundary disposition

No Accepted ADR currently applies to this bounded private reversible UI adapter, the pointer diagnostic, bounded runtime-consistency recovery helper or canonical-checkout governed lifecycle controller. Re-open the ADR/stable-boundary gate before materially relying on a public/stable HTTP/websocket API, externally relied-upon route/deep-link schema, durable shared frontend package/framework, stable BFF/service topology, public authentication/session protocol, customer-facing browser matrix or externally relied-upon remote administration surface.

## 7. Non-claims

This closure does not create:

- external/customer Production;
- a public Arvectum OS product UI;
- a Stable/public API or SDK;
- `Active` Platform Capability status;
- Stable Product Contract status;
- SLA/support/browser-compatibility commitments;
- a final frontend or deployment architecture.

Successful Safari proof in the selected owner environment is bounded closure evidence, not a general browser-support promise.

## 8. Current canonical action

> **P7.07 — Persistent Tender Operator operational contour.**

UI1 through UI4 are `Complete / PASS`; the overall `P7.06-UI` substream is `Complete / PASS` at `100%` for the declared `Persistent Internal / owner-operated` scope. The next Phase 7 action is P7.07; P7.08 remains downstream.