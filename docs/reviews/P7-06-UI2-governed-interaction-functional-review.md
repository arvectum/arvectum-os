# P7.06-UI2 — Governed Interaction and Preflight Functional Review

Status: `Complete / PASS`
Date: `2026-08-18`
Task classification: `platform`
Scope: repository-side bounded private governed-interaction/preflight boundary
Architecture basis: Constitution `1.2.0`; RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006 (`Accepted`); existing CAP-004 audit/reconstruction support
Implementation PR: `#56`
Implementation head: `305faafb790e1387cac2aaafa348fbc4ac583797`
Merge commit: `a22ba781d32f64b7097aeaf05a90651308533811`
Reference Python CI: run `32159051764` / `#107` = `success`

## Review result

Five functional review/revise iterations were completed. No material objections remain for the declared UI2 repository scope.

The review closed these material findings:

1. malformed-form handling, exact loopback Host / DNS-rebinding boundary and browser-evidence trust boundary were hardened;
2. exact RFC-0006 source reconstruction was added instead of inferring reconstruction from the in-flight action;
3. observed `Uncertain` was preserved separately from `Reconciliation required`, with blind retry blocked;
4. reconstruction disclosure was constrained to the existing CAP-004 `AuditReconstructionView`, preserving `Redacted` / `Deleted` / `Unavailable` / `Missing` semantics;
5. consequential outcome evidence was scoped to the related Governed Execution Subject so unrelated attempts over the same target cannot be projected into the interaction.

## Exit-scope evidence

The implementation proves the six UI2 flows required by the live-workspace substream:

- exact governed Subject / Version opening;
- provenance, authorized reconstruction and related Execution evidence;
- four independent Authorization / Organizational Authority / Data Governance / Consequential Approval states;
- transient action-intent assembly;
- entry only through R10 `operator_safety` into the existing Governed Execution / runtime-consistency path;
- evidence-derived `Blocked` / `Waiting` / observed `Uncertain` / `Reconciliation required` / `Succeeded` presentation.

The private loopback adapter reuses UI1 exact-release, health and read-authorization invariants. A separate P7.04 `workspace.interact` human/local grant permits technical interaction access but explicitly does not satisfy Organizational Authority or consequential approval. POST re-fetches trusted governed evidence, re-runs preflight, requires exact loopback Host, same Origin, process-local CSRF and bounded form input, and accepts only transient `interaction_id` plus CSRF from the browser.

No UI-local direct canonical-write primitive, ambient authority, optimistic-success projection, browser-supplied gate/authority/reconstruction evidence, public/stable route/API/session/frontend contract, lifecycle promotion, Production claim, Stable Product Contract or support/browser commitment is created.

## Closure disposition

`P7.06-UI2 = Complete / PASS` for its repository implementation/review scope.

This does **not** close the overall `P7.06-UI` substream. `P7.06-UI3 — Persistent private operator access` is the next canonical action. `P7.06-UI4` remains responsible for the first real selected-owner interaction proof against the persistent runtime.
