# P7.06-UI2 — Governed Interaction / Preflight Functional Cross-Review

Status: `Complete / PASS`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed implementation PR: `#56 — P7.06-UI2 — Governed interaction and preflight`
Implementation head: `305faafb790e1387cac2aaafa348fbc4ac583797`
Implementation merge: `a22ba781d32f64b7097aeaf05a90651308533811`
Final exact-head CI: `Reference Python CI #107 / run 32159051764 = success`
Architecture basis: Constitution `1.2.0`; RFC-0001, RFC-0003, RFC-0004, RFC-0005, RFC-0006 `Accepted 1.0.0`; existing CAP-004 audit/reconstruction support
ADR disposition: `NO` for this private reversible UI2 adapter; stable-boundary gate remains closed

## 1. Review scope

Review the bounded `P7.06-UI2` repository implementation against the live-operator-workspace substream without treating functional review as formal approval, RFC/ADR acceptance, lifecycle promotion, operational-readiness approval or selected-owner live proof.

The review required the implementation to preserve:

- explicit Organization and attributable human Actor context;
- exact governed Subject / Version / provenance continuity;
- source reconstruction through existing RFC-0006 / CAP-004 evidence semantics;
- independent Authorization, Organizational Authority, Data Governance and Consequential Approval states;
- transient intent rather than UI-local authority or approval;
- entry only through the existing Governed Execution / R10 operator-safety path;
- evidence-derived blocked, waiting, uncertain, reconciliation-required and succeeded outcomes;
- deny-by-default / fail-closed behavior when access, evidence or exact-source continuity is unresolved;
- the UI1 private/reversible boundary and absence of a public/stable HTTP/API/browser contract.

## 2. Review iterations

### Iteration 1 — HTTP/browser boundary

Material objection:

- malformed form input was not consistently classified at the UI2 boundary;
- DNS-rebinding / Host continuity needed an explicit regression proof;
- browser fields needed an explicit negative proof that they cannot supply gate evidence.

Revision:

- malformed form encoding now fails as `UI2BoundaryError`;
- exact loopback Host and same-origin POST are enforced;
- process-local CSRF and bounded form size are required;
- browser submission is limited to `interaction_id + csrf`;
- regressions reject forged gate/candidate fields and hostile Host/Origin shapes.

Result: objection closed.

### Iteration 2 — Reconstruction evidence

Material objection:

- provenance alone did not satisfy the UI2 requirement to inspect source reconstruction evidence.

Revision:

- added an explicit source-reconstruction presentation boundary;
- reconstruction is bound to the exact inspected source Version;
- absence of trusted reconstruction evidence renders `Unavailable` rather than inferring a reconstruction from the current action;
- reconstruction remains read-only and never replays a historical side effect.

Result: objection closed.

### Iteration 3 — Uncertainty versus reconciliation

Material objection:

- an observed uncertain consequential attempt could be visually collapsed into the subsequent requirement to reconcile.

Revision:

- added a distinct observed consequential-outcome view;
- `Uncertain` remains an observed governed outcome;
- `Reconciliation required` is displayed separately as the required next safety condition;
- blind retry remains blocked.

Result: objection closed.

### Iteration 4 — CAP-004 redaction / retention preservation

Material objection:

- rendering a raw RFC-0006 `ReconstructionManifest` could bypass existing CAP-004 evidence-availability semantics and disclose evidence that should remain redacted, deleted, unavailable or missing.

Revision:

- UI2 now consumes the existing `AuditReconstructionView` rather than the raw manifest;
- `Available / Redacted / Deleted / Unavailable / Missing` dispositions are preserved;
- unavailable governed source pins are not reconstructed or disclosed;
- exact source binding remains required.

Result: objection closed.

### Iteration 5 — Execution-scoped outcome evidence

Material objection:

- selecting the latest consequential attempt globally could project an attempt belonging to another Governed Execution over the same canonical target lineage into the current interaction.

Revision:

- observed outcome evidence is filtered to the related Governed Execution Subject;
- regression coverage proves that a newer unrelated execution attempt is not projected into the current interaction.

Result: objection closed.

## 3. Final implementation boundary

The reviewed exact implementation head establishes:

1. one typed trusted `GovernedInteractionCase` carrying explicit Organization/Actor, exact source record, exact Governed Execution lineage, runtime state, candidate, Event receipt, source authorization and retry semantics;
2. four independently rendered core preflight gates — Authorization, Organizational Authority, Data Governance and Consequential Approval;
3. authorized CAP-004/RFC-0006 reconstruction presentation bound to the exact source Version, with current evidence-availability restrictions preserved;
4. transient action intent preparation only through `prepare_operator_canonical_mutation_action`;
5. consequential execution only through `execute_operator_canonical_mutation_action` and the existing Governed Execution/runtime-consistency boundary;
6. explicit evidence-derived Ready / Waiting / Blocked / Succeeded / reconciliation presentation and a separate observed Uncertain outcome;
7. fresh POST-side technical-access and governed-evidence re-evaluation instead of trusting prior GET/button state;
8. private loopback Host/Origin, CSRF, no-store/CSP/referrer/nosniff/frame protections and method restrictions;
9. no direct UI-local canonical write primitive, gate-decision constructor, ambient authority, optimistic-success projection or browser-supplied governed evidence;
10. no public/stable route, session, SDK, frontend framework or browser-support commitment.

## 4. Verification

- implementation PR `#56`: merged;
- exact reviewed implementation head: `305faafb790e1387cac2aaafa348fbc4ac583797`;
- exact-head `Reference Python CI` run `32159051764`: `success`;
- merge commit: `a22ba781d32f64b7097aeaf05a90651308533811`;
- read-after-write verification: key UI2 modules are present on canonical `main` after merge;
- no separate status check was attached to the merge commit, so the exact-head PR CI remains the applicable automated implementation evidence.

## 5. Final disposition

`P7.06-UI2 repository implementation = Complete / PASS`.

No material functional-review objections remain on exact head `305faafb790e1387cac2aaafa348fbc4ac583797`.

This result does **not** close the overall `P7.06-UI` substream. `P7.06-UI3 — Persistent private operator access` is the next canonical action, and `P7.06-UI4` remains responsible for the first real selected-owner interaction proof.

No lifecycle, Product Contract, Production, public/stable interface, browser-support, SLA/support or conformance promotion is created by UI2 closure.