# P8.05 — External ingress/egress Event, duplicate, replay, uncertainty + reconciliation semantics

Status: `Complete / PASS`
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

No additional live EIS call was required. The P8.03 contract does not authorize EIS mutation, submission, signature, messaging or another consequential external write, so P8.05 does not fabricate or perform one merely to exercise egress semantics.

## 3. Implementation boundary

Implemented as a bounded Phase 8 reference/evidence harness:

- `reference/python/p8_05_external_boundary_evidence.py`;
- `reference/python/tests/test_p8_05_external_boundary_evidence.py`;
- `reference/python/tests/test_p8_05_reconciliation_monotonic.py`.

The harness composes existing P2.05 Event/provenance semantics and P2.06 runtime consistency/idempotency/uncertainty primitives. It does not define a permanent transport, broker, durable inbox/outbox, distributed exactly-once guarantee, reconciliation service topology, public/stable external Event API, Stable Product Contract or Active Platform Capability.

## 4. Ingress semantics

`ExternalDelivery` is transient transport evidence. Receipt alone does not create canonical history; canonical admission is a separate explicit governed operation through P2.05.

The admitted Event is `Native` evidence that Arvectum OS observed/admitted an external occurrence. It does not make the underlying EIS fact Native: the source remains `External Reference` and the Event preserves source identity, authority scope/mode, exact governed source references and integrity evidence.

Duplicate identity is contract-scoped external occurrence identity:

`source_system + source_object_ref + source_occurrence_id`.

Therefore:

- repeated delivery of the same occurrence creates no second canonical Event;
- later transport delivery metadata does not rewrite the first Event;
- reuse of one delivery identity for different evidence fails closed;
- reuse of one occurrence identity with different immutable evidence fails closed;
- a genuinely new source occurrence creates a new Event even when payload bytes/hash are identical.

`occurred_at` remains source occurrence time; `recorded_at` is first governed admission time. Late/out-of-order delivery remains append-only and does not rewrite history into a fictitious global order.

## 5. Egress uncertainty and reconciliation

P8.05 preserves the existing P2.06 retry contract:

- retry semantics are explicit;
- keyed/non-idempotent attempts require explicit duplicate-protection identity;
- conflicting token reuse fails closed;
- unknown outcome is `Uncertain`, never synthetic `Succeeded`;
- an uncertain attempt blocks blind retry.

P8.05 adds attributable append-only reconciliation evidence that pins the exact uncertain attempt fingerprint/token, has its own Subject/Version identities, uses a distinct Governed Execution identity/version and retains an explicit evidence reference.

Resolution states are:

- `ConfirmedSucceeded`;
- `ConfirmedNotApplied`;
- `StillUncertain`.

Retry behavior is fail-closed:

- no reconciliation → retry prohibited;
- `StillUncertain` → retry prohibited;
- `ConfirmedSucceeded` → retry prohibited;
- `ConfirmedNotApplied` → retry may proceed only as a new Governed Execution with a new retry token;
- once any attributable reconciliation confirms success for the original attempt, later contradictory evidence cannot silently reopen retry.

The original `Uncertain` attempt is never rewritten. Any allowed retry is a new attempt with explicit reconciliation lineage.

## 6. Event outcome and replay semantics

An external-effect outcome Event reports exactly what is known: `Succeeded`, `Failed`, or `Uncertain`. An intent, timeout or acknowledgement is not upgraded to proof of success.

Historical reconstruction is pure over retained evidence. The replay manifest preserves ingress Event IDs, delivery evidence IDs, external-effect attempt fingerprints/outcomes, reconciliation IDs and retry lineage, and explicitly reports:

- `live_retrievals_executed = False`;
- `external_effects_executed = False`.

The reconstruction API has no transport/effect callback. A new consequential operation after replay would require a new Governed Execution, normal gates and causation under RFC-0005/RFC-0006.

## 7. Partial / unverifiable evidence

The external boundary fails closed:

- identity/evidence conflicts are errors;
- unknown effect outcome remains `Uncertain`;
- unresolved reconciliation remains `StillUncertain`;
- no exactly-once claim is made;
- reconstruction cannot claim stronger evidence than retained history contains.

P8.04 already established that incomplete current source evidence cannot be represented as `NO_CHANGE`; P8.05 preserves that posture.

## 8. Product/platform and security boundary

Tender Operator EIS connector/SOAP/archive/procurement semantics remain product-owned under the P8.03 Provisional contract. P8.05 proves only the domain-neutral envelope around Event admission versus delivery, duplicate identity, timing/resequencing, idempotency declaration, uncertainty, reconciliation, replay safety and provenance/reconstruction.

The activated scope remains one Organization: `ООО «Арвектум»`. Event, delivery, execution, reconciliation and evidence identities remain Organization-scoped. No second tenant, cross-Organization relationship, credential, private key, raw tender payload or external mutation capability is introduced.

## 9. Functional cross-review

### Iteration 1 — architecture / reuse

Finding: do not create a speculative public external-Event API or duplicate P2.06 semantics.

Resolution: bounded harness composes P2.05/P2.06; no ADR/public surface/lifecycle transition.

### Iteration 2 — authority / source of truth

Finding: an ingress Event must not make the externally authoritative EIS fact Native.

Resolution: Native Event records local observation/admission only; linked source remains `External Reference`.

### Iteration 3 — rights / external-effect scope

Finding: a real mutating EIS egress test would exceed P8.03 read-only rights.

Resolution: retain P8.04 as real ingress anchor; exercise egress uncertainty/reconciliation with controlled evidence only.

### Iteration 4 — execution contract

Finding: initial synthetic ingress/reconciliation workflows lacked an explicit side-effect class.

Resolution: both corrected to explicit `ReadOnly`; egress/retry remain explicit `ExternalMutation`.

### Iteration 5 — reconciliation monotonicity

Finding: latest-only reconciliation selection could reopen retry after prior `ConfirmedSucceeded` evidence.

Resolution: any retained `ConfirmedSucceeded` for the exact uncertain attempt blocks retry; focused regression added.

### Iteration 6 — executable verification

Result: repository `Reference Python CI` PASS on the implementation head; `1235 tests / OK`.

No material architecture, authority, security, product-boundary, duplicate, replay or reconciliation objection remains.

## 10. Definition of Done

| Requirement | Evidence | Disposition |
|---|---|---|
| receipt is not automatically canonical Event | delivery/admission separation | PASS |
| canonical admission explicit and attributable | P2.05 admission under Governed Execution | PASS |
| duplicate delivery does not duplicate canonical truth | exact occurrence duplicate tests | PASS |
| idempotency scope explicit | P2.06 `RetrySemantics` + explicit token | PASS |
| replay never repeats live retrieval/external effect automatically | pure reconstruction, no effect hook | PASS |
| unknown/timeout outcome becomes uncertain/reconciliation-required | `Uncertain` + retry block | PASS |
| reconciliation attributable and versioned | exact attempt + distinct Governed Execution + evidence ref | PASS |
| partial/unverifiable evidence fails closed/remains incomplete | conflict + uncertainty paths | PASS |
| contradictory reconciliation cannot reopen duplicate-risk retry | monotonic confirmed-success guard | PASS |
| executable regression | Reference Python CI — `1235 tests / OK` | PASS |

## 11. Closure

**P8.05 = Complete / PASS.**

This closure does not imply customer/external Production, Stable Product Contract, Active Platform Capability, public/stable Event API or connector surface, universal exactly-once delivery, selected broker/inbox/outbox/reconciliation infrastructure, multi-Organization validation, or SLA/support/certification/redistribution commitments.

Next roadmap action: `P8.06 — External product/extension onboarding + governed dependency resolution`.
