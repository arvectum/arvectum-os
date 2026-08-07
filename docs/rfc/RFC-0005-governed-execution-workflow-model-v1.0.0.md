# RFC-0005: Governed Execution and Workflow Model

Status: `Accepted`
Version: `1.0.0`
Accepted: `2026-08-07`
Published: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`
Supersedes: `RFC-0005 v0.3.0` reviewed proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Owner approval: `DECISION-2026-08-07-RFC-0005-ACCEPTANCE`
Cross-review: `docs/reviews/RFC-0005-functional-cross-review.md`; `docs/reviews/RFC-0005-cross-review-iteration-4.md`

## 1. Acceptance Publication

This document is the canonical Accepted publication of RFC-0005 `1.0.0`.

The approved normative substance is the reviewed RFC-0005 `0.3.0` proposal preserved in repository history and identified by canonical proposal blob SHA:

`5a4b347dc39e88eeacf49a39861e37326beb7234`

Historical proposal path:

`docs/rfc/RFC-0005-governed-execution-workflow-model-v0.3.0.md`

RFC-0005 `0.3.0` itself incorporates the complete reviewed RFC-0005 `0.2.0` semantic baseline by immutable blob SHA:

`67e739ceacdbd308618f4fdfffd914dc65e99f09`

This Accepted publication incorporates RFC-0005 `0.3.0` in full by immutable content reference. No normative substance of the owner-approved proposal is changed by this acceptance publication.

## 2. Accepted Architecture Baseline

RFC-0005 `1.0.0` refines, without changing, the architectural laws and contracts of:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0002 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0004 `1.0.0` — Accepted.

Where this RFC conflicts with a higher-authority source, the higher-authority source prevails.

## 3. Accepted Model

RFC-0005 `1.0.0` establishes binding domain-neutral Governed Execution and Workflow semantics, including:

1. Workflow as a versioned governed definition of repeatable or operationally significant work;
2. Execution Context as the RFC-0002 Canonical Record specialization for one governed execution instance;
3. immutable governance-significant execution transitions and sealed terminal history;
4. exact effective Workflow and material input version pinning before consequential reliance;
5. exact effective Product Contract version attribution where RFC-0004 applies;
6. explicit separation of authentication, authorization, Organizational Authority, data-governance permission, validation and consequential approval;
7. mandatory Governed Execution for consequential canonical mutation;
8. explicit operation side-effect semantics including read-only, transient, canonical mutation, external mutation and organizational commitment;
9. bounded AI participation without independent final consequential approval or Organizational Authority;
10. idempotency, retry, uncertainty and reconciliation rules preventing silent duplicate consequential effects;
11. governed waiting, suspension, resumption, deadlines and re-evaluation of stale gates;
12. parent/child execution causation without ambient transfer of permission or authority;
13. preservation of external authority modes and conflict rules;
14. explicit failure, cancellation, compensation and partial-completion semantics;
15. output and artifact classification without automatic promotion into authoritative knowledge or organizational assets;
16. explicit workflow evolution and in-flight migration rules;
17. proportional reconstructability evidence without indiscriminate sensitive-data retention;
18. semantic portability independent of a specific workflow/orchestration technology;
19. domain-neutral platform execution semantics while product-specific business workflows remain product-owned by default;
20. scoped conformance criteria and fitness expectations contained in the incorporated proposal.

## 4. Product Contract Boundary

Accepted RFC-0004 `1.0.0` is a normative dependency for product/platform execution boundaries.

Where a product or Product Experiment relies on platform behavior for which RFC-0004 requires a Product Contract:

- the applicable Product Contract MUST exist before governed reliance;
- consequential execution MUST preserve the exact effective Product Contract Version Identity or equivalent immutable version reference;
- Product Contract possession, registration or resolvability MUST NOT substitute for authentication, authorization, Organizational Authority, data-governance or approval evaluation;
- execution MUST enforce applicable operation, canonical-state, authority, security, data-handling, failure and compatibility declarations from the effective Product Contract;
- Product Contract lifecycle and Platform Capability lifecycle remain independent;
- registered extensions receive no ambient permission or Organizational Authority.

## 5. AI Authority Boundary

AI is an execution means, not an organizational authority source.

Under RFC-0005 `1.0.0`, AI MAY analyze, classify, extract, generate, recommend, perform bounded validation and execute explicitly pre-authorized bounded operations where the governing workflow permits.

AI MUST NOT independently:

- grant authorization;
- create Organizational Authority;
- act as final consequential approver;
- silently alter approved policies, standards or Workflow definitions;
- promote transient outputs into validated knowledge or authoritative canonical state outside Governed Execution;
- broaden Organization scope, retention or cross-organization sharing.

## 6. Scope Boundary

This RFC does not define:

- complete Event taxonomy, event delivery guarantees, complete provenance representation or observability infrastructure — RFC-0006 scope;
- observations, memory, validated knowledge or governed-learning promotion — RFC-0007 scope;
- product-specific business workflows, domain approval thresholds or product-local rules;
- workflow runtime, scheduler, queue, database, service topology, BPMN engine or other implementation technology;
- Platform Capability activation, operational readiness, SLA, support or commercial commitments.

## 7. Review and Acceptance Evidence

Original functional cross-review:

- `docs/reviews/RFC-0005-functional-cross-review.md` — Complete, iterations 1–3.

Additional compatibility cross-review:

- `docs/reviews/RFC-0005-cross-review-iteration-4.md` — Complete;
- result: `Pass with bounded reconciliation`;
- total review iterations: 4 of maximum 7.

Approved reviewed proposal:

- RFC-0005 `0.3.0`;
- proposal blob SHA `5a4b347dc39e88eeacf49a39861e37326beb7234`.

Owner approval:

- `docs/governance/decisions/DECISION-2026-08-07-RFC-0005-ACCEPTANCE.md` — Approved.

## 8. Acceptance Result

RFC-0005 `1.0.0` is binding architecture within its declared scope from this publication onward.

Its acceptance completes the Governed Execution / Workflow portion of Roadmap Block 0F. RFC-0006 remains the next architectural work item for Event, Provenance and Observability semantics.

Acceptance of RFC-0005 does not by itself make any Platform Capability `Active`, establish production readiness, create an SLA/support commitment, or authorize domain-specific consequential decisions.
