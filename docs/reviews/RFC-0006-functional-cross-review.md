# RFC-0006 Functional Cross-Review

Status: `Complete`
RFC reviewed: `RFC-0006 — Event, Provenance and Observability Model`
Reviewed proposal baseline: `0.1.0`
Review date: `2026-08-07`
Maximum planned iterations: `7`
Iterations completed: `4`
Owner: `ООО «Арвектум»`

## 1. Purpose

This review evaluates RFC-0006 as a proposal against the current canonical authority baseline:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`;
- RFC-0004 `1.0.0` — `Accepted`;
- RFC-0005 `1.0.0` — `Accepted`;
- Canonical Roadmap `1.1.4` — Block 0F identifies RFC-0006 as the next architectural work item.

The review is an execution-quality mechanism. It is not owner approval and does not make RFC-0006 normative.

## 2. Review Method

The proposal was reviewed from the following materially relevant perspectives:

1. CTO / architecture and Kernel compatibility;
2. COO / operational reconstruction and recoverability;
3. Engineering / event delivery, idempotency, migration and implementability;
4. SRE / observability, failure detection and operational evidence;
5. CISO / security, privileged access and tamper resistance;
6. Privacy / minimization, retention and telemetry shadow-data risk;
7. Legal / evidentiary scope, external authority and deletion constraints;
8. Product / Product Contract and domain-boundary integrity;
9. AI governance / provenance, explainability and authority boundaries.

Each iteration evaluated the proposal for conflicts with higher-authority sources, accidental creation of a sixth Kernel primitive, product-domain leakage, irreversible technology commitment, silent consequential action, ambiguous event authority, unsafe observability-data retention, delivery assumptions that could duplicate effects, and overstatement of reconstructability or evidentiary strength.

## 3. Iteration 1 — Kernel, Event Identity and Semantic Integrity

### Findings

The core distinction among canonical Event, Operational Telemetry, Provenance and Observability is compatible with Constitution Article XI and Accepted RFC-0001/RFC-0002.

The proposal correctly preserves:

- Event as an RFC-0002 Canonical Record specialization;
- stable Event Identity and normally one immutable canonical Event version;
- no mutation of prior Event history;
- provenance as traceable lineage rather than a sixth Kernel primitive;
- telemetry as non-canonical by default;
- technology independence from brokers, event stores, tracing protocols and monitoring vendors.

The Event significance threshold is proportionate and avoids turning every log line or metric sample into canonical history.

### Material corrections identified

Four semantic edge cases require explicit treatment before `Proposed` publication:

1. **Event admission must be distinguished from transport receipt.** A queue message or webhook is not yet a canonical Event merely because bytes arrived. Admission should validate enough identity, schema, Organization scope, authority/source, classification and integrity/provenance context for the declared consequence.
2. **Conflicting reuse of Event Identity must fail explicitly.** If the same Event Identity appears with materially different canonical content, the implementation must reject/quarantine/escalate rather than choose one silently.
3. **Correction/reversal/compensation/invalidation must be restated explicitly.** RFC-0002 already requires additional linked Events; RFC-0006 should make the operational consequences visible in its own Event semantics.
4. **An Event records a governed observation/assertion, not metaphysical proof that the underlying occurrence is true.** External authority must remain explicit.

### Result

`Correction required`, no higher-authority conflict.

## 4. Iteration 2 — Security, Privacy, Legal and Evidentiary Boundaries

### Findings

The proposal is correctly stricter than ordinary observability practice where Arvectum OS governance requires it:

- reusable secrets and credentials are excluded from ordinary logs/events;
- cross-organization observability has no ambient visibility;
- correlation identifiers do not create permission to join tenant data;
- high-volume telemetry can use shorter/selective retention;
- lawful deletion/minimization can reduce reconstruction claims without falsifying history;
- provenance may use governed references instead of retaining raw sensitive payload.

The AI provenance section correctly avoids requiring chain-of-thought and does not let model execution create Organizational Authority.

### Material corrections identified

The reviewed proposal should additionally require:

1. **attributable access to sensitive governed observability evidence** where such access is materially security/privacy-relevant, rather than auditing only the underlying business operation;
2. **governed changes to observability controls** when disabling, sampling, rerouting or shortening retention could remove evidence required by Accepted architecture, contract, law or policy;
3. **no in-place semantic redaction of canonical Event history.** Where data must later be deleted/minimized, implementations should delete the Event/payload under governed retention semantics, use separately governed payload references, cryptographic erasure or another mechanism that does not rewrite the admitted Event to say something different;
4. **qualified evidentiary claims.** Integrity metadata, signatures or immutable storage must not be represented as proof of truth, authority or legal validity beyond what the mechanism establishes.

### Result

`Pass with corrections`.

## 5. Iteration 3 — Operations, Delivery, Failure and Recovery

### Findings

The proposal correctly rejects universal exactly-once transport and global total ordering.

The distinction between Event and delivery, stable Event Identity, duplicate handling, gap detection for completeness-dependent consumers, replay semantics and Event-triggered Governed Execution is operationally sound.

The required-event consistency section is aligned with RFC-0005 because it permits technology-specific strategies while preventing a consequential effect from being represented as silently complete when required event evidence is missing.

### Material corrections identified

The reviewed proposal should strengthen operational failure semantics:

1. **Required observability degradation must be explicit.** If a required Event/evidence path is unavailable, the execution must fail, pause, continue only under an explicitly governed degraded mode, or enter reconciliation-required state according to consequence; silent dropping is non-conforming.
2. **Delivery acknowledgements and checkpoints are not Event authority.** Consumer offsets/checkpoints may prove transport progress but do not replace Event identity, authority or execution evidence.
3. **Late/out-of-order handling must preserve earlier decision provenance.** A later Event can trigger reconciliation, but must not make the earlier execution appear to have known information it did not possess.
4. **Replay for projection rebuild must be side-effect safe by design.** Replayed delivery alone must not re-run consequential actions unless a new Governed Execution explicitly authorizes them.

### Result

`Pass with corrections`.

## 6. Iteration 4 — Product Boundary, AI Governance, Portability and Future-RFC Separation

### Findings

The proposal correctly keeps product-domain event semantics product-owned and requires Product Contract declarations only for governed product/platform event reliance.

It does not promote event infrastructure into an `Active` Platform Capability merely because a product integration works.

Portability is semantic rather than vendor-specific and does not require export of secrets, non-exportable credentials or data outside organizational rights.

The RFC-0007 boundary is preserved: Events and provenance can become inputs to observations or learning, but are not automatically Memory, validated Knowledge or Governed Organizational Assets.

### Final refinements identified

Before publication as `Proposed 0.2.0`, the RFC should explicitly add:

- Event schema compatibility must not silently reinterpret historical Events;
- Product Contract boundaries must treat shared private topics/log formats/CDC feeds as undocumented coupling when relied upon without declaration;
- AI provenance retention remains proportionate and may preserve references/configuration rather than raw prompts or sensitive retrieved payload;
- observability projections/dashboards are rebuildable views and must not become competing canonical authority;
- no Accepted architecture requires one event broker or centralized observability service.

### Result

`Pass after bounded reconciliation`.

The review loop stopped after 4 iterations because the remaining changes are bounded clarifications rather than unresolved architectural disagreements. Further iterations would be disproportionate at the proposal stage.

## 7. Required Proposal Reconciliation

RFC-0006 should be republished as `Proposed 0.2.0` incorporating the following material corrections:

1. explicit Event admission semantics separate from transport receipt;
2. conflicting duplicate Event Identity handling;
3. explicit correction/reversal/compensation/invalidation by additional linked Events;
4. external observation versus truth/authority clarification;
5. attributable access to sensitive observability evidence;
6. governed changes to observability controls that affect required evidence;
7. deletion/minimization without semantic rewriting of admitted Event history;
8. explicit degraded/reconciliation behavior when required Event/evidence paths fail;
9. transport checkpoints do not become Event or organizational authority;
10. late information does not retroactively change what a prior execution knew;
11. replay is side-effect safe unless a new Governed Execution explicitly acts;
12. qualified evidentiary/integrity claims;
13. RFC-0007 boundary restatement.

No new Kernel primitive, product-domain semantic, technology commitment or constitutional amendment is required.

## 8. Compatibility Assessment

| Source | Result |
|---|---|
| Constitution `1.2.0` | Compatible after bounded reconciliation |
| RFC-0001 `1.0.0` | Compatible |
| RFC-0002 `1.0.0` | Compatible; Event specialization preserved |
| RFC-0003 `1.0.0` | Compatible after observability-access/control clarifications |
| RFC-0004 `1.0.0` | Compatible; Product Contract boundary preserved |
| RFC-0005 `1.0.0` | Compatible after required-event degradation/recovery clarification |
| RFC-0007 reserved scope | Not pre-empted |

## 9. Review Conclusion

RFC-0006 is architecturally coherent and sufficiently detailed for publication as a reviewed proposal after the bounded reconciliation listed above.

Recommended lifecycle state after incorporating corrections: `Proposed 0.2.0`.

This review does not constitute owner approval. RFC-0006 remains non-normative until an independent owner-approved decision exists and the RFC State Transition Procedure completes canonical acceptance publication, RFC Index synchronization, roadmap synchronization and read-after-write verification.
