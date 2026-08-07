# RFC-0005: Governed Execution and Workflow Model

Status: `Proposed`
Version: `0.3.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Authors: `ООО «Арвектум»`
Category: `platform`
Constitution: `1.2.0`
Depends on: `RFC-0001 v1.0.0`; `RFC-0002 v1.0.0`; `RFC-0003 v1.0.0`; `RFC-0004 v1.0.0`
Supersedes: `RFC-0005 v0.2.0` reviewed proposal
Superseded by: `None`
Decision owner: `ООО «Арвектум»`
Cross-review: `docs/reviews/RFC-0005-cross-review-iteration-4.md`

## 1. Proposal Publication

This document is the current reviewed proposal publication of RFC-0005 `0.3.0`.

It incorporates the reviewed RFC-0005 `0.2.0` proposal by immutable content reference and applies the bounded reconciliation defined below.

Incorporated proposal path:

`docs/rfc/RFC-0005-governed-execution-workflow-model.md`

Incorporated proposal blob SHA:

`67e739ceacdbd308618f4fdfffd914dc65e99f09`

The incorporated proposal remains the complete baseline semantic model for Governed Execution and Workflow. Sections below supersede only stale RFC-0004 lifecycle/dependency wording and add the boundary consequences required by Accepted RFC-0004 `1.0.0`.

## 2. Accepted Architecture Baseline

RFC-0005 `0.3.0` refines, without changing, the architectural laws and contracts of:

- Constitution `1.2.0`;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0002 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0004 `1.0.0` — Accepted.

Where this proposal conflicts with any higher-authority source, the higher-authority source prevails.

## 3. RFC-0004 Reconciliation

Historical RFC-0005 `0.2.0` statements describing RFC-0004 `0.3.0` as `Proposed`, `non-normative` or merely forward-compatible are superseded by this section.

RFC-0004 `1.0.0` is now a binding normative dependency for product/platform execution boundaries.

Consequences:

1. when a product or Product Experiment relies on shared platform execution behavior, canonical platform state, shared execution history or another RFC-0004 contract trigger, the applicable Product Contract MUST exist before that governed reliance;
2. an Execution Context that materially relies on a changeable Product Contract MUST preserve the exact effective Product Contract Version Identity or equivalent immutable version reference;
3. Product Contract possession, registration or resolvability MUST NOT substitute for RFC-0003 authentication, authorization, Organizational Authority, data-governance or approval evaluation;
4. RFC-0005 execution semantics MUST enforce applicable operation, canonical-state, authority, security, data-handling, failure and compatibility declarations from the effective Product Contract;
5. Product Contract lifecycle and Platform Capability lifecycle remain independent;
6. product-owned workflow/business semantics remain product-owned unless separately promoted through Accepted capability lifecycle governance;
7. extensions invoked during execution receive no ambient permission or Organizational Authority merely because the Product Contract registers them.

These requirements clarify the interaction between Accepted RFC-0004 and the incorporated RFC-0005 execution model; they do not transfer product business logic into the platform.

## 4. Required Version Pinning

The incorporated RFC-0005 Section 11 list of material governing inputs is strengthened as follows.

Where a Product Contract materially governs a consequential execution, the execution MUST pin or immutably reference:

- the Product Contract Subject Identity;
- the exact effective Product Contract Version Identity or equivalent immutable version reference;
- any material compatibility or dependency state required to explain why the boundary was considered valid for that execution.

If the applicable Product Contract version cannot be resolved unambiguously, consequential product/platform execution MUST stop, wait, follow an explicitly governed fallback, or remain non-consequential. It MUST NOT silently select another contract version.

## 5. Product and Platform Boundary

The incorporated RFC-0005 Product and Platform Boundary section is superseded where it says RFC-0004 applies only "once accepted".

The binding rule is now:

> Where a product relies on shared platform execution behavior, Product Contract requirements are governed by Accepted RFC-0004 `1.0.0`.

RFC-0005 remains responsible only for domain-neutral Governed Execution and Workflow semantics. Tender, CRM, finance, legal, marketing and other domain workflows remain product-owned by default.

## 6. Conformance Addition

In addition to the incorporated RFC-0005 conformance criteria, a conforming product/platform execution boundary MUST demonstrate, where RFC-0004 applies, that:

1. the effective Product Contract is identifiable and version-pinned for consequential execution;
2. execution does not rely on undocumented platform internals outside the Product Contract;
3. contract registration does not bypass authorization or Organizational Authority gates;
4. Product Contract organization/tenant, authority-mode, security, data-handling and failure declarations are enforced at the applicable execution points;
5. a Provisional Product Contract is not treated as a Stable platform guarantee merely because the execution succeeded.

## 7. Scope Preservation

This reconciliation does not expand RFC-0005 into RFC-0006 or RFC-0007 scope.

RFC-0005 may require attributable event/evidence references sufficient for execution reconstruction, but complete Event taxonomy, delivery semantics, provenance representation and observability infrastructure remain RFC-0006 scope.

Memory, validated knowledge, observations and governed-learning promotion remain RFC-0007 scope.

## 8. Cross-Review Iteration 4

Functional cross-review iteration 4 was performed after RFC-0004 acceptance and Roadmap `1.1.2` synchronization.

Evidence:

- `docs/reviews/RFC-0005-cross-review-iteration-4.md` — `Complete`;
- result: `Pass with bounded reconciliation`;
- no material architectural conflict found;
- required corrections are limited to RFC-0004 dependency/status reconciliation and Product Contract version attribution/enforcement.

The review loop has now completed 4 of maximum 7 iterations.

## 9. Updated Acceptance Criteria

RFC-0005 MAY be accepted only when:

1. it remains compatible with Constitution `1.2.0`;
2. it remains compatible with Accepted RFC-0001 `1.0.0`, RFC-0002 `1.0.0`, RFC-0003 `1.0.0` and RFC-0004 `1.0.0`;
3. domain-specific workflow semantics have not leaked into shared platform behavior;
4. applicable Product Contract versions are attributable and version-pinned for consequential product/platform execution;
5. Product Contract registration or possession cannot bypass authorization, Organizational Authority or data-governance gates;
6. AI authority remains bounded by Accepted governance and AI cannot act as independent final consequential approver;
7. security, privacy, isolation and data-governance gates cannot be bypassed by execution mechanics;
8. retry, uncertainty, compensation and in-flight migration semantics remain sufficient to prevent silent consequential inconsistency;
9. RFC-0006 and RFC-0007 reserved scope is not pre-empted;
10. no unresolved material cross-review conflict remains;
11. explicit owner approval exists independently before acceptance publication;
12. RFC Index, canonical roadmap and Acceptance Integrity evidence are synchronized during acceptance publication and verified through read-after-write refresh.

## 10. Current Decision State

Current status: `Proposed`.

RFC-0005 `0.3.0` is a reviewed proposal ready for owner decision. Cross-review does not constitute owner approval and gives this proposal no normative force until an independent owner-approved decision and complete acceptance publication occur.
