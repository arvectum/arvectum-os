# P8.05 — External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics

Status: `In review — implementation complete; executable CI evidence pending`
Date: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract`
Constitution: `1.2.0` — `Ratified`
Roadmap item: `P8.05`
Predecessor: `P8.04 — Complete / PASS`

## 1. Authority and architecture check

Checked before implementation:

- Constitution `1.2.0`;
- RFC Index;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0004 `1.0.0` — Accepted;
- RFC-0005 `1.0.0` — Accepted;
- RFC-0006 `1.0.0` — Accepted;
- ADR index — no Accepted ADR selects a permanent external Event transport, broker, persistence, inbox/outbox, reconciliation service or public integration API;
- P8.03 EIS revalidation integration contract — `Provisional 0.1.0`, read-only, internal-only;
- P8.04 real EIS validation evidence and current Phase 8 roadmap.

No conflict with higher-authority material was found. No Constitution amendment, RFC amendment, new RFC or ADR is required for this bounded proof because it does not select a permanent transport/persistence topology or create a public/stable contract.

## 2. Real external anchor

P8.05 reuses, without repeating, the real external evidence established by P8.04:

- external authority: ЕИС / `zakupki.gov.ru`;
- notice: `0344100006426000005`;
- live run: `toa-run-20260820083457-21337c`;
- fresh observation: `2026-08-20T08:34:57.365770+00:00`;
- immutable P6 baseline manifest SHA-256: `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- fresh manifest SHA-256: `4113935e43291f820a43fa2efad49663103a86408788b571d7d0e6dac4974a54`;
- comparison manifest SHA-256: `06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b`;
- live outcome: `NO_CHANGE`, 7/7 material documents byte-identical.

No additional live EIS call is required by P8.05. The P8.03 contract does not authorize EIS mutation, submission, signature, messaging or another consequential external write, so P8.05 does not fabricate or perform one merely to exercise egress semantics.

## 3. Implementation boundary

Implemented as a bounded Phase 8 reference/evidence harness:

- `reference/python/p8_05_external_boundary_evidence.py`;
- `reference/python/tests/test_p8_05_external_boundary_evidence.py`;
- `reference/python/tests/test_p8_05_reconciliation_monotonic.py`.

The harness composes existing P2.05 Event/provenance semantics and P2.06 runtime consistency/idempotency/uncertainty primitives rather than duplicating them or turning a task-specific implementation into a platform capability.

It does **not** define or select:

- an external Event transport or wire protocol;
- a broker/topic model;
- a durable inbox/outbox;
- a distributed transaction or exactly-once transport guarantee;
- a reconciliation service topology;
- a public/stable external Event API;
- a Stable Product Contract;
- an Active Platform Capability.

## 4. Ingress Event and delivery semantics

### 4.1 Receipt is not admission

`ExternalDelivery` is transient transport evidence. Constructing or receiving it does not create canonical history.

Canonical Event admission is a separate explicit governed operation through the existing P2.05 `EventReceipt` / `admit_event` boundary.

### 4.2 External authority remains external

The admitted ingress Event is `Native` evidence of the statement:

> Arvectum OS observed and admitted this external occurrence under the governed execution.

It does not convert the underlying EIS fact to Native authority. The linked source record remains `External Reference`, and the admitted Event preserves source system, source object, source occurrence identity, source authority mode/scope, exact external-reference Version Identity and integrity evidence.

### 4.3 Duplicate is defined by occurrence identity, not by payload equality

The bounded occurrence key is contract-scoped external identity:

`source_system + source_object_ref + source_occurrence_id`.

Consequences:

- repeated delivery of the exact same occurrence adds no second canonical Event;
- a later transport delivery may have a different delivery identity/receipt time without rewriting the first admitted Event;
- reuse of one delivery identity for different transport evidence fails closed;
- reuse of one external occurrence identity with materially different immutable evidence fails closed;
- a genuinely new source occurrence creates a new Event even if its payload digest is byte-identical to an earlier occurrence.

This avoids the unsafe assumption that equal bytes imply the same historical occurrence.

### 4.4 Time and ordering

The harness keeps distinct:

- `occurred_at` — source occurrence time;
- `received_at` / canonical `recorded_at` — first governed admission time.

Late/out-of-order delivery remains append-only. Historical Events are not resequenced or rewritten to create a fictitious global order.

## 5. Egress idempotency, uncertainty and reconciliation

P8.05 deliberately does not perform a real external mutation. It exercises the domain-neutral governed semantics over controlled external-effect evidence while preserving the P8.03 read-only rights boundary.

The existing P2.06 retry contract remains authoritative:

- retry semantics are explicit: naturally idempotent, keyed idempotent, or non-idempotent;
- keyed/non-idempotent attempts require explicit duplicate-protection identity;
- materially conflicting retry-token reuse fails closed;
- an unknown external outcome is `Uncertain`, not `Succeeded`;
- an uncertain attempt blocks blind retry.

P8.05 adds the boundary-specific reconciliation proof:

- reconciliation is append-only evidence;
- it pins the exact uncertain attempt fingerprint and retry token;
- it records its own Subject/Version Identities;
- it uses a distinct attributable Governed Execution Identity and exact Execution version;
- it preserves an explicit governed evidence reference;
- resolutions are `ConfirmedSucceeded`, `ConfirmedNotApplied`, or `StillUncertain`.

Retry behavior is fail-closed:

- no reconciliation → retry prohibited;
- `StillUncertain` → retry prohibited;
- `ConfirmedSucceeded` → retry prohibited as a duplicate risk;
- `ConfirmedNotApplied` → retry may proceed only as a **new Governed Execution** with a **new retry token**;
- once any attributable reconciliation confirms success for the original attempt, later contradictory evidence cannot silently reopen retry.

The original `Uncertain` attempt is never rewritten. A later retry is a new attempt with explicit causation through the reconciliation record.

## 6. Outcome Event semantics

An external-effect outcome Event reports exactly what is known:

- `Succeeded` only when success is the recorded outcome;
- `Failed` only when failure is the recorded outcome;
- `Uncertain` when the external result cannot be established.

An intent, timeout or acknowledgement is never upgraded to proof of successful external effect.

## 7. Replay and reconstruction

Historical reconstruction is a pure operation over retained governed evidence.

The P8.05 replay manifest preserves:

- admitted ingress Event identities;
- delivery-evidence identities;
- external-effect attempt fingerprints and outcomes;
- reconciliation identities;
- post-reconciliation retry lineage.

The reconstruction API has no live-retrieval or external-effect callback, and its result explicitly records:

- `live_retrievals_executed = False`;
- `external_effects_executed = False`.

Therefore projection/history replay cannot silently repeat the P8.04 live EIS retrieval or create a new external consequence. An intentionally new consequential operation would remain subject to a new Governed Execution and normal gates under RFC-0005/RFC-0006.

## 8. Partial, incomplete and unverifiable evidence

P8.05 does not create a synthetic success state for incomplete evidence.

At the external boundary:

- identity/evidence conflicts fail closed;
- an unknown effect outcome remains `Uncertain`;
- unresolved reconciliation remains `StillUncertain`;
- no exactly-once claim is made;
- the retained reconstruction cannot claim stronger evidence than it contains.

P8.04 already established that missing/incomplete source evidence cannot be represented as `NO_CHANGE`; P8.05 preserves that fail-closed posture.

## 9. Product/platform boundary

The Tender Operator EIS connector, SOAP/archive handling and procurement-specific semantics remain product-owned under the P8.03 Provisional integration contract.

P8.05 validates only the reusable domain-neutral semantic envelope around:

- Event admission versus delivery;
- duplicate identity;
- timing/resequencing;
- idempotency declaration;
- uncertainty;
- reconciliation;
- replay safety;
- provenance/reconstruction.

No successful mechanism is promoted to a Platform Capability by this review.

## 10. Security, Organization and data handling

The activated scope remains one Organization: `ООО «Арвектум»`.

The proof does not create a second tenant or cross-Organization relationship. Organization-scoped Event, delivery, execution, reconciliation and evidence identities are required to remain in the same Organization scope.

Only minimized identifiers, exact governed references and integrity digests are needed. No reusable secret, credential, raw tender payload, private key or external mutation capability is introduced by P8.05.

## 11. Functional cross-review

### Iteration 1 — architecture / reuse

Finding: do not expand P2.05 into a speculative public external-Event API and do not duplicate P2.06 retry/uncertainty semantics.

Resolution: contained P8.05 harness composes the existing P2.05/P2.06 primitives. No ADR/public surface/lifecycle transition.

### Iteration 2 — authority / source of truth

Finding: an ingress Event must not make the externally authoritative EIS fact Native.

Resolution: the Event is Native evidence of Arvectum OS observation/admission; the underlying source record stays `External Reference` and is linked by exact governed references.

### Iteration 3 — rights / external-effect scope

Finding: a real mutating egress test would exceed P8.03, whose validated EIS boundary is read-only.

Resolution: retain the real P8.04 ingress anchor; exercise egress uncertainty/reconciliation with controlled reference semantics only. No new EIS mutation or unsupported rights claim.

### Iteration 4 — execution contract

Finding: initial synthetic ingress/reconciliation test workflows omitted an explicit side-effect class, violating the existing Workflow contract.

Resolution: both were corrected to explicit `ReadOnly`; egress/retry workflows remain explicit `ExternalMutation`.

### Iteration 5 — reconciliation monotonicity

Finding: selecting only the latest reconciliation could allow a later contradictory `ConfirmedNotApplied` observation to reopen retry after a prior `ConfirmedSucceeded` proof.

Resolution: any retained `ConfirmedSucceeded` for the exact uncertain attempt permanently blocks retry in the bounded ledger; focused regression coverage was added.

### Iteration 6 — executable verification

Pending: full Reference Python CI on the final PR head.

No material architecture, authority, security, product-boundary or replay objection remains before executable verification.

## 12. P8.05 Definition of Done mapping

| Requirement | Evidence | Disposition |
|---|---|---|
| transport receipt is not automatically canonical Event | `ExternalDelivery` separate from explicit admission | PASS |
| canonical admission explicit and attributable | P2.05 admission under Governed Execution | PASS |
| duplicate delivery does not duplicate canonical truth | exact occurrence duplicate tests | PASS |
| idempotency scope explicit | P2.06 `RetrySemantics` + explicit token | PASS |
| replay does not replay live retrieval/external effect | pure reconstruction manifest, no effect hook | PASS |
| timeout/unknown becomes uncertain/reconciliation-required | `ConsequentialOutcome.UNCERTAIN` + retry block | PASS |
| reconciliation attributable and versioned | `ExternalReconciliation` + distinct governed Execution | PASS |
| partial/unverifiable evidence fails closed/remains incomplete | conflict + uncertainty paths | PASS |
| contradictory reconciliation cannot reopen duplicate-risk retry | monotonic confirmed-success guard | PASS |
| full executable regression | Reference Python CI | PENDING |

## 13. Closure boundary

P8.05 may be marked `Complete / PASS` only after the final PR head passes the repository Reference Python CI and read-after-write verification confirms the review, implementation and roadmap state.

Completion of P8.05 will not imply:

- customer/external Production;
- Stable Product Contract;
- Active Platform Capability;
- public/stable Event API or connector surface;
- universal exactly-once delivery;
- selected broker/inbox/outbox/reconciliation infrastructure;
- multi-Organization validation;
- SLA/support/certification/redistribution commitments.
