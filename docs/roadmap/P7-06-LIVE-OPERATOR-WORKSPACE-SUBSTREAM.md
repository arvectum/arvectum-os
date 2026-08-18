# P7.06 — Live Operator Workspace Substream

Status: `Active / UI1 Current`
Version: `0.1.1`
Created: `2026-08-18`
Updated: `2026-08-18`
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

The live workspace MUST NOT be attached to the selected Mac mini before the first controlled P7.06 update carries and verifies the merged R22 hardening. That prerequisite is now satisfied by [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md), which completed governed update, exact rollback and final re-update on target `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

Therefore the active sequence is:

```text
P7.06 governed update / rollback proof
        ↓ PASS
P7.06-UI1 live read-only workspace  ← CURRENT
        ↓
P7.06-UI2 governed interaction / preflight
        ↓
P7.06-UI3 persistent local operator access
        ↓
P7.06-UI4 owner interaction proof
        ↓ PASS
P7.07 persistent Tender Operator contour
```

## 3. Operating boundary

The initial UI is:

- internal and owner-operated;
- bound to one explicit Organization and attributable human Actor context;
- local/private by default;
- no public ingress;
- no public/stable API, route, SDK or browser compatibility commitment;
- non-authoritative presentation over governed state;
- deny-by-default and fail-closed when identity, Organization, authorization or exact-source continuity is unresolved;
- unable to directly mutate canonical state outside Governed Execution;
- unable to create Organizational Authority or consequential approval merely through UI state.

An owner-controlled loopback/private access method or reversible tunnel MAY be used for the first interaction proof. The transport is an environment adapter, not the platform contract.

## 4. Subtasks

### P7.06-UI1 — Live read-only governed workspace

Status: `Current`.

Connect the M4 workspace presentation semantics to the persistent runtime through a bounded internal adapter.

Minimum visible surfaces:

- current Organization and attributable Actor;
- runtime health summary;
- `Discover`;
- `Records`;
- `Executions`;
- `Evidence`;
- `Documents`;
- `Knowledge`;
- Subject versus exact-Version distinction;
- authority/source and lifecycle/validation context where authorized;
- honest unavailable/redacted/missing evidence states.

The first implementation MAY reuse server-rendered/static HTML patterns or another reversible local approach. A frontend framework is not required merely to make the workspace live.

Exit evidence:

- browser-visible live state comes from the exact persistent runtime release rather than fixtures;
- wrong/unresolved Organization fails closed;
- unauthorized content/counts do not leak;
- presentation is demonstrably non-authoritative;
- no canonical or external mutation occurs.

### P7.06-UI2 — Governed interaction and preflight

Status: `Pending`.

Add bounded operator interaction without direct-write shortcuts.

Minimum interactive flows:

1. open a governed Subject and exact Version;
2. inspect provenance/reconstruction and related Execution evidence;
3. inspect an Execution and its independent authorization / Organizational Authority / approval / data-governance gate states;
4. assemble one transient action intent;
5. enter the existing Governed Execution path for an allowed bounded operation;
6. render blocked/waiting/uncertain/reconciliation-required/succeeded outcomes from governed evidence rather than optimistic UI state.

The UI MUST NOT treat button visibility/enabled state as the security boundary.

### P7.06-UI3 — Persistent private operator access

Status: `Pending`.

Make the workspace reachable during regular owner-operated use while retaining a private/reversible boundary.

Required evidence:

- supervised workspace process or adapter lifecycle tied to an exact release;
- bounded listener exposure;
- no accidental public ingress;
- P7.04 least-privilege access checks applied to operator access;
- secrets remain outside Git and ordinary logs;
- workspace restart does not corrupt governed state;
- UI failure does not stop the core runtime or silently change authority;
- uninstall/rollback path exists.

### P7.06-UI4 — First real owner interaction proof

Status: `Pending`.

The owner performs a real interaction session against the selected Mac mini persistent runtime.

Minimum proof:

- open the live Arvectum OS workspace in a browser;
- visibly confirm Organization/Actor and runtime health context;
- navigate at least Records, Executions, Evidence and one Document or Knowledge surface using real retained governed state;
- inspect one exact-version/provenance/reconstruction chain;
- execute one bounded governed interaction or preflight without bypassing required runtime gates;
- record operator friction and any material security/authority/usability defects;
- perform functional cross-review until no material objections remain or the seven-iteration cap is reached.

`P7.06-UI = Complete / PASS` only when the owner can both see live governed state and exercise at least one real bounded interaction through the workspace.

## 5. Relationship to Phase 4

This substream reuses the already-proven M4 semantics rather than redesigning the workspace from scratch.

Phase 4 already established:

- explicit Organization / Actor context;
- domain-neutral navigation shell;
- Canonical Record / Relationship inspection;
- exact version, Event, provenance and reconstruction experience;
- Governed Execution / gate / approval-action experience;
- Document / Artifact experience;
- Memory / Knowledge / Search discovery;
- cross-capability composition and bounded Product Contract-backed product entry;
- security, rights, minimization and authority-safe UX.

The new work is operational connection and interaction, not a new semantic workspace model.

## 6. ADR and stable-boundary disposition

No ADR is required merely to create the first private reversible live UI.

Re-open the ADR/stable-boundary gate before materially relying on any of the following:

- public/stable HTTP or websocket API;
- externally relied-upon route/deep-link schema;
- durable frontend framework/package contract shared across products;
- stable BFF/service topology;
- public authentication/session protocol;
- customer-facing browser support matrix;
- externally relied-upon remote administration surface.

## 7. Non-claims

Completion does not itself create:

- external/customer Production;
- a public Arvectum OS product UI;
- a Stable/public API or SDK;
- `Active` Platform Capability status;
- Stable Product Contract status;
- SLA/support/browser-compatibility commitments;
- a final frontend or deployment architecture.

## 8. Current status

`P7.06 core = Complete / PASS` after selected-Mac Attempt 8.

`P7.06-UI1 — Live read-only governed workspace` is the current canonical operator-experience action before P7.06-UI2/UI3/UI4 and before P7.07/P7.08 workload expansion.