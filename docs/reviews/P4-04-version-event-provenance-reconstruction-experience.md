# P4.04 — Version, Event, provenance and reconstruction experience review

Status: `PASS`
Date: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Scope: bounded internal Workspace / Operator Experience

## 1. Decision

`P4.04 — Version, Event, provenance and reconstruction experience` passes for the bounded internal reference scope.

The implementation adds a read-only operator inspection boundary over already accepted/runtime-owned Event, provenance and reconstruction semantics. It does not create a second Event model, a telemetry model, an Event store, a replay executor, a public API, a Product Contract, a new Platform Capability or a canonical state owner.

## 2. Canonical baseline checked

The review was performed against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record / Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0005 `Governed Execution / Workflow Model` `1.0.0` — `Accepted`;
- RFC-0006 `Event, Provenance and Observability Model` `1.0.0` — `Accepted`;
- RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
- Accepted ADR index — no Accepted ADR is required by this bounded implementation;
- Phase 4 roadmap `1.4.0` as the task baseline;
- P4.03/R9 source-resolution and presentation-authority boundaries;
- P2.05 Event/provenance runtime, P2.08 non-authoritative projection replay, CAP-004 Audit/Reconstruction Support and P3.07 cross-capability access enforcement.

No conflict with a higher-authority canonical artifact was found.

## 3. Implemented boundary

Primary implementation:

- `reference/python/arvectum_os_ref/provenance_inspection.py`;
- `reference/python/tests/test_p4_04_version_event_provenance_reconstruction.py`;
- `reference/python/examples/p4_04_provenance_inspection_demo.py`.

The operator view exposes only authorized, already-governed evidence and preserves the following distinctions.

### 3.1 Version and execution linkage

- an operator may inspect by Execution Subject or an exact Execution Version;
- exact historical Execution Version selection is preserved without fallback to another version;
- reconstruction evidence keeps exact relied-upon Workflow, material input, gate-decision, Execution, result and Event Version Identities;
- an unknown exact Execution Version is reported only after the governed evidence access boundary has been satisfied.

### 3.2 Canonical Event history versus telemetry

Canonical Event history is rendered separately from raw logs, metrics, traces and other operational telemetry.

For currently visible canonical Event evidence the view preserves:

- Event Identity and exact Event Version Identity;
- Event type and event schema version;
- authority mode, authority scope and authoritative source;
- occurrence time separately from recording/admission time;
- producer and initiating actor;
- Execution Subject and exact causal Execution Version;
- related Subject and exact Version references;
- correlation and causation references;
- classification and access scope.

The presentation does not infer a universal total order from occurrence/recording timestamps.

### 3.3 Provenance and reconstruction

- provenance references remain traceability references, not grants of access, reuse rights, Authorization or Organizational Authority;
- correlation is explicitly not treated as causation;
- reconstruction is labeled `Derived, read-only, non-authoritative`;
- replay is described only as side-effect-free rebuilding of a derived non-authoritative projection;
- the P4.04 surface itself does not execute replay;
- a new consequential action requires a new Governed Execution rather than historical replay.

### 3.4 Evidence gaps and minimization

The view reuses CAP-004 evidence states and preserves honest reconstruction limits:

- `Redacted`;
- `Deleted`;
- `Missing`;
- `Unavailable`;
- `Available`.

A non-available item reduces the reconstruction claim instead of being inferred, repaired or fabricated. Redaction caused by current access constraints dominates a more specific retention/deletion disposition so the UI cannot leak why inaccessible evidence is absent.

## 4. Security and source-resolution order

The final inspection order is security-significant:

1. an explicit Workspace reference is required;
2. the P4.03 current source-authorization handoff must allow the Actor/Organization/Execution Subject;
3. the ReconstructionManifest must belong to that governed Organization and Execution Subject;
4. the P3.07 `AccessRequest` must match the current Actor and Organization;
5. P3.07 re-evaluates purpose, required right and classification for **every exact evidence Version Identity**;
6. retention/availability dispositions are merged without overriding access redaction;
7. only then may the presentation distinguish whether an exact requested Execution Version exists in the authorized reconstruction;
8. the supplied canonical Event set must exactly match the currently visible Event evidence versions and their governed type/schema/execution linkage.

This ordering prevents the exact-Version path from becoming a protected metadata/existence oracle.

## 5. Functional cross-review iterations

### Iteration 1 — architecture / semantic ownership

Result: `PASS`.

The proposed view reuses RFC-0006 and existing runtime/capability semantic owners rather than introducing a second Event/provenance/reconstruction model. No new RFC, ADR, Product Contract or capability lifecycle decision is required.

### Iteration 2 — security / privacy / minimization

Initial finding: the first implementation checked exact Execution Version membership after source authorization but before the P3.07 evidence-level purpose/right/classification enforcement. That could disclose `VERSION_UNAVAILABLE` before the caller had demonstrated access to the reconstruction evidence set.

Remediation: exact-Version existence resolution was moved after P3.07 evidence enforcement and dedicated regression tests were added. Access redaction was also made dominant over more specific deletion/retention details.

Result after remediation: `PASS`.

### Iteration 3 — operator UX / accessibility

Result: `PASS` for the bounded P4.04 baseline.

The static renderer uses textual headings, tables for exact governed evidence and definition-list style Event details. Complete/incomplete reconstruction status, exact versions, provenance, correlation/causation and evidence limitations are understandable without relying on visual color or client-side behavior. Governed text is HTML-escaped.

This is not the final Phase 4 accessibility/usability certification; P4.10 remains the cross-cutting baseline gate.

### Iteration 4 — engineering / coupling / ADR trigger review

Result: `PASS`.

The P4.04 module remains internal and technology-neutral. It selects no frontend framework, HTTP/API/BFF topology, stable wire contract, durable Event/read-model/cache storage, telemetry backend, IAM/PDP/PEP mechanism, message broker, graph database or replay executor. No ADR trigger is crossed by this bounded reference implementation.

## 6. Executable evidence

Focused and full-suite evidence covers, among other cases:

- exact Execution Version selection without fallback;
- source authorization before protected existence disclosure;
- P3.07 evidence enforcement before exact-Version existence disclosure;
- actor-bound access requests and duplicate/denied authorization fail-closed behavior;
- exact per-Version purpose/right/classification constraints;
- classification redaction of Event evidence;
- lawful deletion, missing and unavailable/uncertain evidence;
- redaction dominance over sensitive deletion details;
- exact visible canonical Event-set matching;
- Event type/schema drift rejection;
- Event/telemetry separation and occurrence/recording distinction;
- correlation versus causation;
- explicit non-authoritative reconstruction/replay wording;
- absence of mutation, approval, replay-execution and telemetry authority surfaces;
- absence of selected frontend/network/storage infrastructure dependencies.

GitHub Actions evidence:

- `Reference Python CI #130` — `FAIL`, `455 / 456` tests passed; the sole failure was a case-sensitive test expectation (`canonical Event history` versus renderer text `Canonical Event history`), not an implementation/architecture failure;
- the assertion was corrected without changing production behavior;
- `Reference Python CI #132` — `PASS`, Python `3.12.13`, `456` tests, `OK`.

## 7. P4.04 exit-criterion mapping

| Required behavior | Evidence | Result |
|---|---|---|
| Event history separated from raw telemetry | dedicated canonical Event projection + renderer wording + tests | PASS |
| causation/correlation where available | Event and reconstruction fields rendered independently | PASS |
| execution linkage and exact relied-upon versions | exact Execution/Event/Workflow/input/gate/result Version evidence | PASS |
| provenance chain inspection | exact provenance references rendered as traceability references | PASS |
| reconstruction/replay explicitly derived/non-authoritative | DTO invariants + textual renderer + no replay executor | PASS |
| uncertainty/missing/deletion gaps honest | CAP-004 dispositions + incomplete reconstruction tests/demo | PASS |
| UI reconstruction never source of truth | presentation authority invariant + renderer + no mutation surface | PASS |
| protected evidence dereference independently constrained | P4.03 source authorization + P3.07 exact evidence constraints | PASS |

## 8. Explicitly deferred

P4.04 does **not** pull forward:

- Governed Execution action/gate/approval UX from P4.05;
- Document/Artifact UX from P4.06;
- Memory/Knowledge/Search UX from P4.07;
- Product Contract-backed product composition from P4.08;
- broader cross-surface security/minimization hardening from P4.09;
- final accessibility/usability matrix from P4.10;
- durable UI/API/storage/runtime architecture or an ADR choice;
- public compatibility or Stable Product Contract commitments;
- capability lifecycle promotion or production-readiness claims.

## 9. Governance disposition

- Constitution change: **not required**;
- Accepted RFC change: **not required**;
- new RFC: **not required**;
- ADR: **not required for this bounded reversible implementation**;
- Product Contract: **not required**;
- Platform Capability lifecycle change: **none**;
- CAP-004 remains `Incubating / Provisional`;
- operational environment/readiness claim: **none**;
- public API/SLA/conformance claim: **none**.

## 10. Final result

`P4.04 = PASS / Complete` for the declared internal reference scope.

The next canonical Phase 4 work item is `P4.05 — Governed Execution, gate and approval/action experience` after roadmap synchronization.
