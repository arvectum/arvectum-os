# P4.05 — Governed Execution, gate and approval/action experience review

Status: `Complete`
Date: `2026-08-08`
Result: **`PASS`**
Task classification: `platform`
Owner: `ООО «Арвектум»`

## 1. Scope

P4.05 implements the smallest bounded operator-facing experience for consequential work through the already accepted and implemented Governed Execution semantics.

The completed slice provides:

- authorized inspection of one stable Execution Identity at its Head or one explicitly requested exact historical Execution Version;
- exact Workflow, material-input and Product Contract version visibility where the execution carries those dependencies;
- separate operator-visible Authorization, Organizational Authority and Consequential Approval evidence rather than one synthetic `approved` flag;
- fail-closed unresolved/denied gate states;
- explicit lifecycle/action-readiness meaning;
- a transient, immutable and non-authoritative canonical-mutation action intent distinct from committed canonical state;
- one bounded action adapter that delegates consequential canonical mutation only to the existing P2.06 `commit_canonical_mutation` semantic owner;
- explicit keyed retry, duplicate suppression, stale/conflict, idempotency-conflict and uncertain/reconciliation meaning;
- an inert HTML presentation plus an executable static demonstration.

P4.05 does **not** define a workflow engine, decision-authority policy, IAM/PDP/PEP, approval service, external-effect executor, durable runtime store, Event store, frontend framework, public route/API/BFF, stable wire/serialization contract, Product Contract schema, new Platform Capability or capability lifecycle transition.

## 2. Canonical authority checked

The implementation and review were performed against the current canonical repository state:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 remain `Accepted 1.0.0`;
- RFC-0001 `Arvectum OS Architecture` `1.0.0` — `Accepted`;
- RFC-0002 `Canonical Record Kernel Metamodel` `1.0.0` — `Accepted`;
- RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `1.0.0` — `Accepted`;
- RFC-0004 Product Contract / Product Experiment / Extension Model `1.0.0` — `Accepted`;
- RFC-0005 Governed Execution / Workflow Model `1.0.0` — `Accepted`;
- RFC-0006 Event / Provenance / Observability Model `1.0.0` — `Accepted`;
- R3 reuse review and R4 Core Runtime hardening disposition;
- completed P4.01–P4.04 and R9 workspace-boundary evidence;
- current Phase 4 detailed roadmap and canonical roadmap.

No conflict with the Constitution or Accepted RFC baseline was found.

No applicable Accepted ADR constrains this bounded internal implementation. The existing ADR gate remains open for any future durable/external/stable technology or interface commitment.

## 3. Implementation

Primary implementation:

- `reference/python/arvectum_os_ref/execution_action_experience.py`;
- `reference/python/tests/test_p4_05_governed_execution_gate_approval_action.py`;
- `reference/python/tests/test_p4_05_demo.py`;
- `reference/python/examples/p4_05_governed_execution_demo.py`.

### 3.1 Governed Execution inspection

`inspect_governed_execution` consumes the P4.02 scoped workspace state, one explicit Subject or exact-Version navigation reference, current source-access evidence and existing `GovernedExecutionLineage` runtime evidence.

For a Subject reference the surface resolves the Execution Head. For an exact-Version reference it preserves that exact historical Version and never silently redirects to Head.

Current source authorization is evaluated before protected source/version existence is distinguished. Read authorization is actor-bound and Organization-bound; missing, denied, duplicate or actor-mismatched source decisions fail closed.

This source-access decision is only permission to inspect the governed source. It does not satisfy or imply any Governed Execution gate and is never presented as action authority.

### 3.2 Exact governed reliance

The inspection preserves and renders the exact version pins already carried by the selected `GovernedExecutionContext`:

- Workflow Subject + Version;
- every material input Subject + Version;
- Product Contract Subject + Version where applicable.

The presentation does not resolve those pins to a later Head and does not manufacture Product Contract validity or authority from UI context.

P4.05 therefore preserves the RFC-0002/RFC-0005 exact-reliance rule without creating a second dependency-resolution mechanism.

### 3.3 Gates and approval meaning

Every required gate is rendered as a separate row. Resolved evidence exposes:

- gate kind;
- exact gate-decision Version Identity;
- attributable decision Actor Identity;
- governed basis reference;
- exact Execution Version against which the decision was evaluated;
- explicit `Allow` or `Deny` outcome.

Unresolved gates carry no fabricated decision evidence.

In particular, `Authorization`, `OrganizationalAuthority` and `ConsequentialApproval` remain separate concepts. The renderer states explicitly that a UI role/title, read-access decision or another passed gate cannot substitute for any of them.

The implementation contains no `allow_all`, auto-approval, role-name inference or AI approval shortcut.

### 3.4 Action readiness

The action surface distinguishes:

- ready for a governed canonical-commit request;
- awaiting required gates;
- denied required gate;
- lifecycle state that does not admit the action;
- historical exact Execution Version, which is inspection-only;
- a different current Workspace Actor, which is blocked by the bounded adapter;
- a non-canonical side-effect operation, which remains inspectable but is not executed by this P4.05 canonical-mutation adapter.

The same-Actor check is intentionally a **bounded adapter safety constraint**, not a new general decision-authority rule. P4.05 has no accepted delegation/action-actor model from which it could safely infer that another read-authorized operator may invoke the already-governed execution. A richer invocation/delegation model, if later needed, must be governed by the appropriate runtime/security boundary rather than inferred by the UI.

### 3.5 Intent is not commit

`CanonicalMutationActionIntent` is immutable, transient and explicitly `PresentationAuthority.NON_AUTHORITATIVE`.

Preparation binds:

- current Organization and Actor context;
- the exact admitted Execution Context version;
- exact expected Canonical Head Version;
- immutable successor candidate;
- exact Event receipt linkage;
- retry semantics and optional duplicate-protection token.

Preparing this intent does not mutate `RuntimeConsistencyState`, append an Event or mark the intent committed.

A historical Execution Version, unresolved/denied gates, incompatible actor context or non-admitted lifecycle cannot produce a ready action intent through the bounded preparation path.

### 3.6 Consequential mutation remains runtime-owned

`execute_canonical_mutation_action` does not implement mutation semantics itself. It delegates to the existing P2.06 `runtime_consistency.commit_canonical_mutation` path.

That existing semantic owner remains responsible for:

- admitted Governed Execution / side-effect checks;
- exact material-input target pinning;
- expected-head/stale-state checks;
- immutable successor validation;
- Event admission;
- keyed/natural idempotency behavior;
- logical publication of record + Event + attempt evidence.

P4.05 maps the bounded operator-relevant outcomes without creating a competing canonical-state owner.

### 3.7 Retry, conflict and uncertainty

The inspection summarizes consequential attempt evidence for the stable Execution Identity and keeps exact Execution Version attribution visible.

It shows:

- side-effect class;
- retry semantics;
- only whether a duplicate-protection token exists, not the token value;
- outcome;
- exact result/Event Version references where present;
- explicit reconciliation requirement for an `Uncertain` outcome.

The action adapter presents successful keyed replay as an idempotent duplicate rather than a second effect, stale state as a non-mutating block, and idempotency-token reuse with different immutable invocation content as a conflict.

The HTML explicitly warns that uncertain consequential outcomes require reconciliation and that blind retry is not presented as safe.

P4.05 does not execute external mutations or commitments; it only exposes already-owned runtime attempt semantics for operator understanding.

## 4. Security and authority ordering

For protected Execution inspection the bounded order is:

1. explicit workspace reference;
2. current actor/Organization-bound source-access authorization;
3. governed Execution source resolution;
4. exact requested Version resolution, if any;
5. exact runtime/gate/attempt evidence interpretation;
6. non-authoritative presentation and action-readiness derivation.

Consequential action then requires a separately ready exact Governed Execution context and is delegated to the runtime mutation semantic owner.

This preserves two independent ideas:

- **source visibility** — may the current operator inspect this Execution?;
- **consequential authority/admission** — does the exact Governed Execution, with its independently governed gates and current runtime preconditions, admit this effect?

The first never creates the second.

## 5. Functional cross-review

Per repository engineering policy, P4.05 was reviewed iteratively until no material objection remained.

### Iteration 1 — architecture / semantic ownership

**Question:** did the operator experience create a second workflow, gate or canonical-mutation authority?

**Result:** `PASS`.

The surface reads existing `GovernedExecutionLineage` and exact pins; action preparation is transient; commit delegates to `commit_canonical_mutation`. No duplicate workflow engine, gate evaluator, Event store or canonical repository was introduced.

### Iteration 2 — security / authority / bypass paths

**Question:** can read access, UI identity labels, historical state or another operator bypass Governed Execution?

**Result:** `PASS`.

Source authorization is checked before exact protected Version existence disclosure. Authorization and Organizational Authority remain separate. Unresolved and denied gates fail closed. Historical versions remain inspection-only. A different read-authorized Workspace Actor cannot invoke the bounded existing Execution action. No role/title or AI-based authority inference exists.

### Iteration 3 — operator UX / accessibility / uncertainty

**Question:** can an operator understand exact reliance, gate state, action readiness and retry risk without hidden state assumptions?

**Result:** `PASS`.

The renderer is textual and inert, uses table headers/captions and explicit status text, exposes exact versions, separates required gates, labels non-authoritative presentation, distinguishes intent from commit, suppresses retry-token values and marks uncertain outcomes as reconciliation-required.

### Iteration 4 — engineering / regression / ADR boundary

**Question:** did implementation or demo stabilize an infrastructure/public boundary or regress existing runtime behavior?

**Result:** `PASS`.

No frontend/server/network/database/queue/IAM framework is selected. The module remains internal and package-root exports are unchanged. The static demo starts no server. Reference Python CI remained green after the implementation and demo additions.

No fifth review iteration was necessary because the fourth iteration produced no material finding.

## 6. Executable evidence

Initial implementation evidence:

- GitHub Actions `Reference Python CI #137` — `PASS`;
- Python `3.12.13`;
- `472` tests;
- `OK`.

After adding the executable static demo and its smoke test:

- GitHub Actions `Reference Python CI #139` — `PASS`.

After canonical roadmap and README synchronization:

- GitHub Actions `Reference Python CI #143` — `PASS`;
- Python `3.12.13`;
- `473` tests;
- `OK`.

This synchronized run is completion-integrity evidence; it does not add a new P4.05 semantic requirement.

## 7. ADR / Product Contract / capability disposition

**New RFC required:** no.

**New ADR required:** no.

P4.05 does not materially select or rely on a durable or externally constraining implementation choice. Re-open the ADR gate before selecting a stable frontend/runtime framework boundary, public route/API/BFF or wire schema, IAM/session enforcement technology, durable workspace/runtime store, Event store, message transport, stable cross-product package, or separately deployable UI/API topology.

**New Product Contract required for P4.05 itself:** no. This is an internal platform workspace/reference implementation. Where the inspected Execution already carries a Product Contract pin, P4.05 displays that exact existing pin without treating it as authority. The Phase 4 bounded Product Contract-backed product entry proof remains P4.08.

**Platform Capability lifecycle change:** none. CAP-001 through CAP-004 remain `Incubating / Provisional`; P4.05 creates no fifth capability and promotes none to `Active`.

## 8. Exit assessment

P4.05 exit expectations are satisfied for the bounded reference scope:

- action intent remains distinct from committed canonical mutation;
- exact Workflow/material-input/Product Contract versions remain visible where material;
- Authorization and Organizational Authority remain separate gates;
- Consequential Approval remains independently visible where required;
- no authority is inferred from UI role/title or source-read access;
- unresolved/denied required gates fail closed;
- historical exact Execution Versions cannot become current action authority;
- retry/idempotency/stale/conflict/uncertainty semantics are understandable;
- uncertain outcome is reconciliation-oriented rather than blindly retried;
- consequential canonical mutation occurs only through the existing governed runtime path;
- presentation remains non-authoritative and internal;
- no public/durable/technology-specific boundary is stabilized;
- executable negative-path evidence is green.

**Final P4.05 decision: `PASS`.**

## 9. Carried boundaries

The following remain intentionally outside P4.05 rather than hidden gaps:

1. P4.06 owns Document / Artifact workspace experience.
2. P4.08 owns the bounded Product Contract-backed product entry composition proof.
3. P4.09 must revalidate cross-surface rights, minimization, hidden-action safety and any richer invocation/delegation UX before M4 closure.
4. ExternalMutation / Commitment execution remains owned by existing runtime semantics; P4.05 does not create a UI-side external-effect executor.
5. The bounded same-Actor invocation constraint is not a stable organizational delegation policy.
6. Stable frontend/API/IAM/storage choices remain behind the existing ADR gate.

## 10. Next canonical action

Proceed to **`P4.06 — Document / Artifact workspace experience`**.
