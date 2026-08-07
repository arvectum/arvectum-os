# RFC-0006: Event, Provenance and Observability Model

Status: `Accepted`
Version: `1.0.0`
Accepted: `2026-08-07`
Published: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`; `RFC-0005 v1.0.0`
Supersedes: `RFC-0006 v0.2.0` reviewed proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Owner approval: `DECISION-2026-08-07-RFC-0006-ACCEPTANCE`
Cross-review: `docs/reviews/RFC-0006-functional-cross-review.md`

## 1. Acceptance Publication

This document is the canonical Accepted publication of RFC-0006 `1.0.0`.

The owner-approved normative substance is the reviewed RFC-0006 `0.2.0` proposal preserved in repository history and identified by canonical proposal blob SHA:

`5468001d2a0ff13fb16b7f88f7a3bc26f6bc6225`

Historical proposal path:

`docs/rfc/RFC-0006-event-provenance-observability-model.md`

RFC-0006 `0.2.0` is incorporated into this Accepted publication in full by immutable content reference. No normative substance of the owner-approved proposal is changed by this acceptance publication.

## 2. Accepted Architecture Baseline

RFC-0006 `1.0.0` refines, without changing, the architectural laws and contracts of:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0002 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0004 `1.0.0` — Accepted;
- RFC-0005 `1.0.0` — Accepted.

Where this RFC conflicts with a higher-authority source, the higher-authority source prevails.

## 3. Accepted Model

RFC-0006 `1.0.0` establishes binding domain-neutral Event, Provenance and Observability semantics, including:

1. Event remains an append-only RFC-0002 Canonical Record specialization;
2. transport receipt is distinct from canonical Event admission;
3. Event admission validates identity, schema, Organization scope, authority/source, attribution, classification, provenance/integrity and payload interpretability proportionate to consequence;
4. conflicting reuse of one Event Identity with materially different immutable content cannot silently mutate history;
5. correction, reversal, compensation and invalidation create additional linked Events rather than editing admitted Events;
6. event type/schema semantics remain version-identifiable and historical Events cannot be silently reinterpreted by later schema versions;
7. occurrence time, recording time, ordering, late-arrival, correlation and causation remain explicit and do not create authority by implication;
8. external Event representation preserves RFC-0001/RFC-0002 authority modes and does not convert transport into organizational truth;
9. required Event/evidence paths for consequential operations cannot fail silently and must establish evidence, fail/pause, use an explicitly governed degraded mode, or expose incomplete/uncertain/reconciliation-required state;
10. delivery is distinct from Event identity, and duplicate delivery, checkpoints, gaps and replay do not create organizational authority or universal exactly-once semantics;
11. replay of historical Events is side-effect safe unless a new Governed Execution explicitly authorizes a new consequential action;
12. provenance is traceable origin and lineage represented through governed references and records rather than a sixth Kernel primitive;
13. AI-mediated provenance preserves material dependencies without granting AI Organizational Authority or requiring unjustified retention of raw prompts, chain-of-thought, secrets or sensitive payload;
14. operational telemetry, logs, metrics, traces, dashboards and observability projections are non-canonical by default and must not become competing organizational authority;
15. observability remains subject to RFC-0003 security, privacy, tenant isolation, minimization, retention, deletion and attributable privileged-access requirements;
16. changes to observability controls that would remove required evidence are governed consequential configuration changes;
17. Event immutability does not require unlawful indefinite retention, but deletion/minimization must not semantically rewrite retained history or overstate reconstructability;
18. integrity mechanisms prove only the claim supported by the mechanism and do not automatically establish truth, legal validity, Organizational Authority or reuse rights;
19. shared product/platform Event reliance remains explicit through RFC-0004 Product Contracts and may not depend on private topics, undocumented streams, log formats or incidental CDC feeds;
20. Event/Provenance semantics remain portable across brokers, stores, tracing backends and observability vendors;
21. legacy/event/telemetry migration may be incremental and need not retroactively promote low-value historical telemetry into canonical Events;
22. Events, telemetry and provenance do not automatically become Memory, validated Knowledge or Governed Organizational Assets; RFC-0007 remains authoritative for that lifecycle once accepted.

## 4. Scope Boundary

This RFC does not define:

- one mandatory message broker, event store, observability stack, tracing protocol, metrics store, SIEM or cloud vendor;
- physical Event table/topic/service topology;
- universal exactly-once transport delivery or one global total Event order;
- product-specific event taxonomies or domain payload semantics;
- concrete retention periods, SLO/SLI, RTO/RPO or incident procedures;
- Memory, Knowledge, Observation or Governed Learning promotion semantics, which remain RFC-0007 scope;
- Platform Capability activation, operational readiness, SLA, support or commercial commitments.

These matters remain subordinate ADR, standard, catalog, Product Contract, operational, legal or later-RFC decisions as applicable.

## 5. Product Contract Boundary

Accepted RFC-0004 `1.0.0` remains the normative product/platform boundary.

Where a product relies on platform Events or exposes product Events through the platform:

- the applicable Product Contract MUST declare the relevant event types/schema compatibility, direction, Organization scope, authority/source semantics, delivery/ordering expectations where relied upon, duplicate/gap/retry behavior, classification/data-handling, retention/replay, failure and migration expectations proportionate to consequence;
- private topics, undocumented streams, internal log formats, incidental database change feeds or implementation-specific observability channels MUST NOT become hidden governed product/platform dependencies;
- Product Contract possession or Event receipt MUST NOT bypass RFC-0003 authorization, Organizational Authority or data-governance gates;
- successful integration does not automatically promote product-domain Event semantics or observability infrastructure into an `Active` Platform Capability.

## 6. Governed Execution Boundary

Accepted RFC-0005 `1.0.0` remains authoritative for Governed Execution.

RFC-0006 requires that consequential event-driven consumers preserve the triggering Event identity or immutable reference and pass normal authentication/authorization, Organizational Authority, data-governance, validation and approval gates.

A required Event/evidence path is part of the declared reconstruction boundary of the consequential operation. Failure of that path MUST NOT be silently treated as a fully successful governed outcome.

## 7. AI Authority Boundary

AI remains an execution means, not an authority source.

RFC-0006 provenance MAY identify materially relevant model/provider or model artifact identity, model/configuration, prompt/template/configuration version, governed input/retrieval references, consequential tool calls, validation and approval evidence, and reproducibility limitations where applicable and lawfully retained.

AI provenance MUST NOT:

- make the AI component an Organizational Authority;
- substitute for final consequential approval;
- imply that AI output is validated Knowledge;
- require retention of chain-of-thought, reusable secrets or unnecessary sensitive payload;
- broaden Organization scope, rights, retention or cross-organization sharing.

## 8. Review and Approval Evidence

Functional cross-review:

- `docs/reviews/RFC-0006-functional-cross-review.md` — `Complete`;
- iterations completed: 4 of maximum 7;
- result: `Pass after bounded reconciliation`.

Approved reviewed proposal:

- RFC-0006 `0.2.0`;
- immutable proposal blob SHA `5468001d2a0ff13fb16b7f88f7a3bc26f6bc6225`.

Owner approval:

- `docs/governance/decisions/DECISION-2026-08-07-RFC-0006-ACCEPTANCE.md` — `Approved`;
- approval record was canonically created before this acceptance publication.

## 9. Acceptance Result

RFC-0006 `1.0.0` is binding architecture within its declared Event, Provenance and Observability scope from this publication onward.

Its acceptance completes the architecture portion of Roadmap Block 0F together with Accepted RFC-0005.

Acceptance does not itself make any Platform Capability `Active`, establish production readiness, select an implementation technology, create an SLA/support commitment, or authorize product-specific consequential decisions.
