# P7.06 — Live Operator Workspace Substream

Status: `Active / UI2 Current — UI1 Complete / PASS`
Version: `0.1.5`
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

The live workspace MUST NOT be attached to the selected Mac mini before the first controlled P7.06 update carries and verifies the merged R22 hardening. That prerequisite is satisfied by [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md), which completed governed update, exact rollback and final re-update on target `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

UI1 selected-Mac Attempt 1 subsequently used the proven P7.06 update path to activate exact release `3a2b561a6935a84749552f016db8d1bd69eabf9a`; deployment, browser, authorization, negative-path and zero-mutation checks passed. The attempt remained `BLOCKED` solely because the persistent P7.03 store contained no real retained `canonical-governed-state` item to inspect. See [`P7.06-UI1 Selected-Mac Live-Browser Proof — Attempt 1`](../reviews/P7-06-UI1-selected-mac-proof-attempt-1.md).

The owner explicitly approved one bounded real-state admission through [`DECISION-2026-08-18-P7-06-UI1-FIRST-REAL-GOVERNED-ITEM-ADMISSION`](../governance/decisions/DECISION-2026-08-18-P7-06-UI1-FIRST-REAL-GOVERNED-ITEM-ADMISSION.md). The repository-side bridge passed three functional review iterations, final `Reference Python CI` run `32144682838`, and merged through PR `#53` at `419d06184e81bbd0dbd292e05a8053ed6bd6f9cc`.

UI1 selected-Mac Attempt 2 then advanced the selected runtime to exact canonical release `b1b78ed9772727dda41b2e509675691f978957ec` through P7.06, verified the approved retained P6.05-L7 manifest, passed four distinct RFC-0005 gate bases, admitted and persisted one real governed item, proved idempotent retry, inspected the real Subject / exact Version / provenance through the browser and proved zero mutation from browsing. See [`P7.06-UI1 Selected-Mac Live-Browser Proof — Attempt 2`](../reviews/P7-06-UI1-selected-mac-proof-attempt-2.md).

Therefore the active sequence is now:

```text
P7.06 governed update / rollback proof
        ↓ PASS
P7.06-UI1 live read-only workspace
        ↓ PASS
P7.06-UI2 governed interaction / preflight  ← CURRENT
        ↓
P7.06-UI3 persistent local operator access
        ↓
P7.06-UI4 owner interaction proof
        ↓ PASS
P7.07 persistent Tender Operator contour
```

UI1 is closed. UI3 MUST NOT start canonically before the bounded UI2 interaction/preflight boundary is implemented and reviewed.

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

An owner-controlled loopback/private access method or reversible tunnel MAY be used for interaction proof. The transport is an environment adapter, not the platform contract.

## 4. Subtasks

### P7.06-UI1 — Live read-only governed workspace

Status: `Complete / PASS`.

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

The implementation remains private, reversible and server-rendered/stdlib based; no frontend-framework or public route contract is established.

Exit evidence:

- browser-visible live state comes from the exact persistent runtime release rather than fixtures: `PASS`;
- at least one real retained non-fixture governed item can be inspected with Subject / exact Version and provenance context: `PASS`;
- wrong/unresolved Organization fails closed: `PASS`;
- unauthorized content/counts do not leak: `PASS`;
- presentation is demonstrably non-authoritative: `PASS`;
- no canonical or external mutation occurs from browsing: `PASS`.

Attempt 1 established the browser/security/read-only conditions on the empty state but could not establish the real-item inspection condition. Attempt 2 closed that sole blocker under the exact existing owner context.

Attempt 2 evidence:

- exact canonical/local/runtime release: `b1b78ed9772727dda41b2e509675691f978957ec`;
- P7.06 update transaction: `dbaec3d61aecd13a608863b9ae1ad78570a5584d`;
- retained real P6.05-L7 manifest SHA-256: `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- Authorization / Organizational Authority / Data Governance / Consequential Approval: four distinct `PASS` outcomes;
- first admission: `PASS_ADMITTED_AND_PERSISTED`;
- second execution: `PASS_IDEMPOTENT_EXISTING`;
- final P7.03 retained set: `1` item / `1` checkpoint;
- retained Subject: `document-subject/eis-0344100006426000005-exact-attachment-evidence`;
- retained exact Version: `document-version/eis-0344100006426000005-74e943d855406b04`;
- semantic type: `platform.document`;
- authority: `External Reference`;
- validation/provenance: `CAP-001 + RFC-0006 + CAP-004`;
- real browser inspection: `PASS`;
- retained `manifest.json` SHA-256 before/after browsing: `d0cd33ac17fcaa91416edcb9526e446b5cbd7c03f75333ecf7055a07ee7f2c38`, unchanged;
- retained `payload.bin` SHA-256 before/after browsing: `5486433cc34296859ccfb6a6690803d2b8c9c7c7a554292c3f1d45613e79b27e`, unchanged;
- network/external effects: `NONE`;
- owner-local bounded evidence SHA-256: `104f64790a36511ca30e14edb864d4b2e650ecf62f39f379685e8d893766a506`.

The UI1 adapter itself was unchanged between Attempt 1 and Attempt 2: `reference/python/p7_06_ui1_live_workspace.py` has the same blob SHA `fbe71502e12d0734f8e9a6242d3253c79a5f79ca` at releases `3a2b561a6935a84749552f016db8d1bd69eabf9a` and `b1b78ed9772727dda41b2e509675691f978957ec`. The Attempt 1 wrong-Organization, revoked-grant, mutation-method and security-header negative-path evidence therefore remains applicable without inferring behavior across a changed implementation.

### P7.06-UI2 — Governed interaction and preflight

Status: `Current`.

Add bounded operator interaction without direct-write shortcuts.

Minimum interactive flows:

1. open a governed Subject and exact Version;
2. inspect provenance/reconstruction and related Execution evidence;
3. inspect an Execution and its independent authorization / Organizational Authority / approval / data-governance gate states;
4. assemble one transient action intent;
5. enter the existing Governed Execution path for an allowed bounded operation;
6. render blocked/waiting/uncertain/reconciliation-required/succeeded outcomes from governed evidence rather than optimistic UI state.

The UI MUST NOT treat button visibility/enabled state as the security boundary.

UI2 MUST preserve the UI1 read-only inspection invariants while adding only a Governed Execution entry/preflight path. No direct canonical write endpoint, ambient authority or optimistic success projection is permitted.

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

No ADR is required merely to create the first private reversible live UI, the one-purpose bounded real-state admission bridge, or a private reversible UI2 preflight adapter that enters existing Governed Execution semantics without becoming an externally relied-upon contract.

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

The bounded concrete P6.05 notice/digest used to prove the first real item remains proof input, not shared platform business logic or a generalized Tender Operator capability.

## 8. Current status

`P7.06 core = Complete / PASS` after selected-Mac Attempt 8.

`P7.06-UI1` repository implementation = `Complete / PASS` through PR `#51`.

`P7.06-UI1` bounded real-state admission bridge = `Complete / PASS` through PR `#53` and final `Reference Python CI` run `32144682838 = success`.

Selected-Mac UI1 Attempt 1 = `BLOCKED` solely because no qualifying real retained governed item existed in the persistent P7.03 store; all exercised empty-state browser/security/read-only paths passed.

Selected-Mac UI1 Attempt 2 = `Complete / PASS` on exact canonical/local/runtime release `b1b78ed9772727dda41b2e509675691f978957ec`. One real retained governed item was validly admitted/persisted under the bounded owner decision, the second execution proved idempotency, the real Subject/exact Version/provenance was visible in the unchanged UI1 browser adapter, and before/after governed-byte digests proved zero mutation from browsing. Network/external effects were `NONE`.

`P7.06-UI1 = Complete / PASS`.

Current canonical action advances to **`P7.06-UI2 — Governed interaction and preflight`**. UI3/UI4 and P7.07 remain pending/downstream. No lifecycle, Product Contract, Production, public/stable interface or support commitment is promoted by UI1 closure.
