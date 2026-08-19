# P7.06 — Live Operator Workspace Substream

Status: `Active / UI3 Current — runtime consistency recovery required before selected-Mac closure`
Version: `0.1.8`
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

The P7.06 governed deploy/update/rollback prerequisite is complete. UI1 and UI2 are also complete. UI3 is now the current action and must close before UI4 or P7.07/P7.08 operational workload expansion.

```text
P7.06 governed update / rollback proof
        ↓ PASS
P7.06-UI1 live read-only workspace
        ↓ PASS
P7.06-UI2 governed interaction / preflight
        ↓ PASS
P7.06-UI3 persistent private operator access  ← CURRENT
        ↓ selected-Mac operational PASS required
P7.06-UI4 first real owner interaction proof
        ↓ PASS
P7.07 persistent Tender Operator contour
```

UI3 repository implementation and the full functional review/revise loop are complete, but selected-Mac operational closure is not. The bounded current-pointer forensic run has now classified the selected-Mac blocker as `UPDATE_COMMAND_FAILED`: the runtime `current` pointer named release `d5cb521bf2565c42ad8ccf47565dda18cf9106c6` while the live P7.02 runtime health and launchd process remained on exact release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5`. No new rollback/recovery evidence or P7.03/P7.04 mutation accompanied the failed update attempt. The bounded runtime-consistency recovery and hardened proof-runner remediations are merged. The immediate evidence step is therefore recovery of pointer/runtime consistency, followed by the ordinary P7.06 governed update and the complete UI3 proof.

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

Status: `Current — repository implementation/review and bounded remediations complete; selected-Mac recovery/update/proof pending`.

Repository implementation is merged and reviewed. It provides:

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
- hardened reconciliation that keeps the invoking controller while pinning service Python/module/plist to the actual resulting release, avoiding replay of a known historical lifecycle race.

Canonical functional review: [`P7.06-UI3 — Functional cross-review`](../reviews/P7.06-UI3-functional-cross-review.md) — repository implementation review complete, maximum `7/7` review/revise iterations, no remaining material repository-scope objection. This is engineering evidence only; it is not selected-Mac closure or lifecycle/readiness approval.

Selected-Mac progression:

1. Attempt 1 failed closed because the selected human operator lacked the exact UI1+UI2 local grant set; a bounded owner-authorized P7.04 administrative step corrected that without granting Organizational Authority or changing P7.03 governed state.
2. Attempt 2 reached launchd installation but exposed listener-readiness ambiguity; PR `#62` remediated readiness/port-collision handling and later review iterations hardened multi-row listener validation.
3. Historical-release reconciliation was hardened in iteration 7 / PR `#64` so rollback does not replay the pre-remediation lifecycle controller.
4. Attempt 4 failed before closure after the runtime `current` pointer was observed inconsistent with the release still represented by the live runtime process.
5. The merged PR `#65` forensic runner then classified the actual selected-Mac condition as `UPDATE_COMMAND_FAILED`, not background rollback: `origin/main = ec649b8df8b90444162590dbaeed0b2b79aeaae6`, `current = d5cb521bf2565c42ad8ccf47565dda18cf9106c6`, live P7.02 health release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5`, update exit code `7`, no new rollback/recovery evidence, no observed pointer transition during the watch window, P7.03 unchanged and P7.04 unchanged. Owner-local forensic attestation SHA-256: `89d1786f8dff7ebb0b745620701d1d7437f6c6d02e34bba0c37617468b1b365a`.
6. PR `#67`, merged as `fa8e0729974462a44d688f77194d7080d621e2ba`, adds the supported proof entry point that keeps the hardened target UI3 controller across historical rollback while preserving exact-release service pins. `Reference Python CI #138` passed.
7. PR `#66`, merged as `e586084ea1292a3c0e22f888dc8ed5524c748732`, adds bounded P7.06 runtime-consistency recovery. The helper has no arbitrary target-release argument: it requires matching P7.02 launchd pin, live health release/PID, P7.05 observer pin and exact installed release manifest before atomically reconciling only `current` to the already-running proven release. P7.03/P7.04 digests must remain unchanged; failed post-reconciliation verification restores the exact original pointer. The final combined branch head `9b20b5b9b3f9d7da5d35bd8b9156142d7749755d` passed `Reference Python CI #141` after the proof-harness merge was included.

The former Attempt 4 hypothesis of an unexplained background rollback is therefore not the current diagnosis. The proven blocker is an inconsistent runtime pointer/live-release state that prevents P7.06 update from passing its initial P7.02 health gate. The recovery helper restores only internal consistency to the release already executing; it does not advance to canonical main and does not bypass governed deployment.

Diagnostic evidence: [`P7.06-UI3 — Selected-Mac runtime-pointer investigation`](../reviews/P7.06-UI3-selected-mac-runtime-pointer-investigation.md).

Recovery review: [`P7.06 — Runtime consistency recovery review`](../reviews/P7.06-runtime-consistency-recovery-review.md).

Proof-harness review: [`P7.06-UI3 — Proof harness historical-controller review`](../reviews/P7.06-UI3-proof-harness-historical-controller-review.md).

Immediate UI3 closure path:

1. execute `p7_06_runtime_consistency_recovery.py` on the selected Mac and require `PASS`, exact runtime/observer/live-health agreement and unchanged P7.03/P7.04 state;
2. verify P7.02 and P7.05 exact-release status on the recovered running release;
3. stop any stale UI3 launchd job without modifying P7.04 or governed state;
4. execute the ordinary P7.06 governed update from the recovered release to current canonical `main` and require exact target activation;
5. re-check runtime/observer exact-release stability after a bounded observation interval;
6. run the supported `p7_06_ui3_selected_mac_proof_runner.py` against the exact active release, using the selected host's explicit private loopback port configuration;
7. perform read-after-write/runtime verification and record minimized owner-local evidence;
8. only then mark UI3 `Complete / PASS` and advance to UI4.

### P7.06-UI4 — First real owner interaction proof

Status: `Pending`.

The owner performs a real interaction session against the selected Mac mini persistent runtime.

Minimum proof:

- open the live Arvectum OS workspace in a browser;
- visibly confirm Organization/Actor and runtime health context;
- navigate at least Records, Executions, Evidence and one Document or Knowledge surface using real retained governed state;
- inspect one exact-version/provenance/reconstruction chain;
- execute one bounded governed interaction or preflight without bypassing required runtime gates;
- record operator friction and material security/authority/usability defects;
- perform functional cross-review until no material objections remain or the seven-iteration cap is reached.

`P7.06-UI = Complete / PASS` only when the owner can both see live governed state and exercise at least one real bounded interaction through the workspace.

## 5. Relationship to Phase 4

This substream reuses the already-proven M4 semantics rather than redesigning the workspace from scratch: explicit Organization/Actor context, domain-neutral navigation, Canonical Record / Relationship inspection, exact version/Event/provenance/reconstruction, Governed Execution/gate/approval-action experience, Document/Artifact, Memory/Knowledge/Search, cross-capability composition and authority-safe UX.

The new work is operational connection and interaction, not a new semantic workspace model.

## 6. ADR and stable-boundary disposition

No Accepted ADR currently applies to this bounded private reversible UI3 adapter, the pointer diagnostic or the bounded runtime-consistency recovery helper. Re-open the ADR/stable-boundary gate before materially relying on a public/stable HTTP/websocket API, externally relied-upon route/deep-link schema, durable shared frontend package/framework, stable BFF/service topology, public authentication/session protocol, customer-facing browser matrix or externally relied-upon remote administration surface.

## 7. Non-claims

Current progress does not create:

- external/customer Production;
- a public Arvectum OS product UI;
- a Stable/public API or SDK;
- `Active` Platform Capability status;
- Stable Product Contract status;
- SLA/support/browser-compatibility commitments;
- a final frontend or deployment architecture.

## 8. Current canonical action

> **P7.06-UI3 — execute selected-Mac runtime-consistency recovery, perform the ordinary governed update to current canonical main, verify stable exact-release runtime/observer state, then run the supported complete UI3 operational proof.**

UI4 and P7.07 remain pending/downstream. UI3 must not be marked `Complete / PASS` from repository CI, functional review or remediation merge alone.
