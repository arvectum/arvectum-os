# Decision: Accept RFC-0002 Canonical Record and Kernel Metamodel

Status: `Approved`
Decision date: `2026-08-07`
Decision class: `A — Fundamental Governance`
Subject: `RFC-0002: Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model`
Proposal version reviewed: `0.10.0`
Decision authority: `ООО «Арвектум» / Owner of Arvectum OS`
Constitution basis: `1.2.0`
Architecture basis: `RFC-0001 v1.0.0 Accepted`

## Decision

The Owner of Arvectum OS explicitly approves RFC-0002 proposal version `0.10.0` for acceptance without further substantive architectural changes.

The proposal may therefore be published as RFC-0002 version `1.0.0` with status `Accepted`, provided the acceptance publication:

1. references this decision as the canonical approval evidence;
2. preserves the approved metamodel semantics from proposal `0.10.0` without introducing new substantive architectural changes;
3. synchronizes the RFC Index and relevant canonical planning/documentation artifacts;
4. preserves repository evidence of the resulting accepted publication.

## Scope of Approval

Approval covers the platform Kernel metamodel defined by RFC-0002, including:

- Identity and Version Identity semantics;
- Canonical Record immutable-version and lineage semantics;
- Typed Relationship identity, versioning and non-authority semantics;
- Event placement and append-only semantics;
- Execution Context placement, lifecycle, version pinning and preservation semantics;
- authority modes, external-authority contracts and authority transition semantics;
- Governed Organizational Asset designation and legal-rights neutrality;
- proportional representation and technology-independent persistence;
- staged, evidence-preserving migration from provisional implementations;
- scoped RFC-0002 conformance boundaries.

This decision does not approve implementation-specific storage, authentication, authorization, workflow, observability, retention-period, legal-rights, Product Contract or product-domain decisions reserved for later RFCs, ADRs, policies, standards, contracts or product decisions.

## Rationale

RFC-0002 `0.10.0` completed architecture review, domain-neutral scenario validation, cross-section consistency validation and role-based top-management cross-review against the current canonical architecture baseline.

The final proposal preserves the five Kernel primitives established by RFC-0001, resolves the provisional metamodel questions reserved to RFC-0002, restores mandatory RFC-0001 governance and external-authority requirements, avoids unnecessary physical coupling and migration obligations, and does not absorb product-domain logic or pre-empt implementation decisions reserved for later artifacts.

No unresolved conflict with Constitution `1.2.0` or Accepted RFC-0001 `1.0.0` was identified at the time of approval.

## Consequences

Upon valid publication as `Accepted 1.0.0`:

- RFC-0002 becomes binding architectural authority subordinate to the Constitution and RFC-0001;
- the precise Kernel metamodel is no longer provisional within RFC-0002 scope;
- future RFCs, ADRs, standards, Product Contracts and implementations must conform to or validly supersede the accepted metamodel;
- acceptance alone does not make any capability `Active`, establish production readiness, create an SLA/support commitment, grant legal rights, or require wholesale migration of product-local legacy data.

## Approval Evidence

The approval was explicitly confirmed by the Owner of Arvectum OS in the Arvectum OS project conversation on `2026-08-07` after review of RFC-0002 proposal version `0.10.0`.

Owner confirmation: `Принято. Подтверждаю обновленную версию`.

This file is the canonical repository record of that owner decision. Its commit must precede the RFC acceptance publication commit so that RFC Index acceptance-integrity requirements are satisfied.
