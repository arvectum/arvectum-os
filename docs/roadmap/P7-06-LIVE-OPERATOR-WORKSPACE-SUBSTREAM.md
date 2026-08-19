# P7.06 — Live Operator Workspace Substream

Status: `Active / UI3 Current — repository implementation/review complete; selected-Mac forensic execution pending`
Version: `0.1.7`
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

UI3 repository implementation and the full functional review/revise loop are complete, but selected-Mac operational closure is not. Selected-Mac Attempt 4 exposed an unresolved runtime `current` pointer transition after a completed governed update. The bounded forensic diagnostic is merged and repository-tested; its selected-Mac execution is now the immediate evidence step.

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

Status: `Current — repository implementation/review complete; selected-Mac operational proof blocked pending pointer classification`.

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
4. Attempt 4 still failed before closure after the runtime `current` pointer was observed returning from canonical update target `d5cb521bf2565c42ad8ccf47565dda18cf9106c6` to historical release `6d4d07aead603841ecce3c469dd46f5e0d58ccd5` before the exact-release proof runner could establish its initial invariant.

The unresolved Attempt 4 fact is treated as an operational evidence gap, not guessed causation. Canonical P7.06 does not define a background rollback watcher, so PR `#65` added a bounded forensic diagnostic that classifies the observed state as one of:

- `STABLE_AFTER_UPDATE`;
- `UPDATE_COMMAND_FAILED`;
- `EXPLICIT_P7_06_ROLLBACK_EVIDENCE`;
- `EXPLICIT_P7_06_RECOVERY_EVIDENCE`;
- `UNATTRIBUTED_CURRENT_MUTATION`.

Diagnostic evidence: [`P7.06-UI3 — Selected-Mac runtime-pointer investigation`](../reviews/P7.06-UI3-selected-mac-runtime-pointer-investigation.md) — repository diagnostic prepared; selected-Mac execution pending.

PR `#65` repository validation:

- focused authoring validation: `14/14 PASS`;
- GitHub `Reference Python CI` run `32187694627` / `#133`: `success`;
- full Reference Python suite: `1092 tests`, `OK` on the PR merge-test head.

Immediate UI3 closure path:

1. execute the merged bounded pointer diagnostic on the selected Mac;
2. classify the transition from actual P7.06 evidence;
3. remediate only if the evidence demonstrates a material defect;
4. rerun the complete selected-Mac UI3 proof against one exact merged release;
5. perform read-after-write/runtime verification and record minimized owner-local evidence;
6. only then mark UI3 `Complete / PASS` and advance to UI4.

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

No Accepted ADR currently applies to this bounded private reversible UI3 adapter or the pointer diagnostic. Re-open the ADR/stable-boundary gate before materially relying on a public/stable HTTP/websocket API, externally relied-upon route/deep-link schema, durable shared frontend package/framework, stable BFF/service topology, public authentication/session protocol, customer-facing browser matrix or externally relied-upon remote administration surface.

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

> **P7.06-UI3 — run the merged selected-Mac current-pointer diagnostic, classify/remediate the observed pointer transition if necessary, then rerun the complete UI3 operational proof.**

UI4 and P7.07 remain pending/downstream. UI3 must not be marked `Complete / PASS` from repository CI or functional review alone.