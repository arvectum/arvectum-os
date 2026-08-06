# Arvectum OS Decision Authority Policy

Status: `Proposed`
Version: `0.1.0`
Created: `2026-08-07`
Category: `governance`
Constitution basis: `1.2.0`
Architecture basis: `RFC-0001 v0.8.0`
Policy owner: `ООО «Арвектум»`

## Purpose

This policy defines the initial decision-authority matrix for Arvectum OS.

It prevents two failure modes:

- every material decision escalating to the founder or owner;
- proposers approving their own material risks or shared-platform obligations.

This policy is `Proposed`. Until it is approved, the owner of Arvectum OS retains residual decision authority.

## Principles

1. Decision authority follows affected scope, consequence and reversibility.
2. Material decisions require an approver with sufficient independence from the proposer.
3. Low-risk reversible decisions should be delegated close to the work.
4. No delegation may weaken the Constitution or an accepted RFC.
5. Every governed decision must have a canonical reference.
6. Authority may be delegated to a person, role or governance body, but delegation scope and limits must be explicit.

## Decision Classes

### Class A — Fundamental Governance

Includes:

- constitutional amendments;
- acceptance or supersession of foundational platform RFCs;
- irreversible changes to the fundamental platform model;
- changes to owner authority.

Decision authority: `Owner of Arvectum OS`.

Proposer may not be the sole approver.

### Class B — Shared Platform and Material Risk

Includes:

- promotion of a capability to `Active`;
- backward-incompatible stable public-contract changes;
- material shared-platform exceptions;
- production exceptions affecting multiple products or tenants;
- cross-organization data access or knowledge reuse;
- acceptance of material security, privacy, legal, financial, safety or reputational gaps.

Decision authority: `Owner` or explicitly delegated `Platform Decision Authority`.

Required consultation where applicable:

- architecture;
- technology and operations;
- security or privacy;
- legal or commercial owner;
- affected product owners.

Proposer may not be the sole approver.

### Class C — Capability Incubation and Product-Platform Boundary

Includes:

- creation of a lifecycle `Candidate`;
- promotion from `Candidate` to `Incubating`;
- approval of a Provisional domain-neutral contract;
- bounded exception affecting one incubating capability;
- return of an incubating capability to a product.

Decision authority: delegated `Platform Decision Authority` or owner.

The proposer may participate but may not solely approve when the decision creates shared obligations or material risk.

### Class D — Product-local Reversible Decisions

Includes:

- bounded Product Experiments;
- product-local implementation choices;
- manual controls within an approved scope;
- low-risk reversible exceptions that do not alter shared contracts, cross tenant boundaries or create external commitments.

Decision authority: delegated `Product Decision Authority` within approved budget, data, risk and time limits.

Self-approval may be allowed only when delegation explicitly permits it and the decision remains low-risk, reversible and product-local.

### Class E — Operational Changes

Includes routine operational, deployment and maintenance decisions within approved contracts and policies.

Decision authority: delegated operational owner.

Material incidents, exceptions or changes outside approved boundaries escalate to the applicable higher class.

## Initial Authority Matrix

Until named roles or governance bodies are approved, the following temporary matrix applies:

| Decision class | Proposer | Decision authority | Required independence |
|---|---|---|---|
| A | Any authorized proposer | Owner | Approver distinct from proposal record; owner approval explicit |
| B | Product, platform or governance owner | Owner | Proposer may not solely approve |
| C | Product or platform owner | Owner | Proposer may not solely approve shared obligation or material risk |
| D | Product owner or delegated operator | Owner or explicit product delegation | Self-approval only if explicitly delegated and low-risk |
| E | Operational owner | Owner or explicit operational delegation | Separation required only when material risk or exception arises |

This temporary matrix intentionally preserves owner control while the organization is small. It should be replaced by named delegations as soon as qualified accountable roles exist.

## Required Decision Record

Every governed decision must record:

- decision class;
- subject and scope;
- proposer;
- decision authority;
- consulted parties where applicable;
- alternatives considered;
- rationale and evidence;
- consequences and accepted risks;
- effective date;
- expiry, review or supersession condition;
- canonical approval reference.

## Conformance Approval

A Conformance Statement may be approved by a person or body with authority over the assessed scope and accepted risk.

The conformance approver must not approve a material exception they proposed unless a higher authority explicitly approves that exception.

A limited product or pilot approver may not claim full-platform conformance.

## Delegation

A delegation must identify:

- delegating authority;
- delegate;
- decision classes and scope;
- budget or financial limits where relevant;
- data classification and tenant limits;
- maximum risk or consequence;
- duration and review date;
- excluded decisions;
- escalation path;
- canonical delegation reference.

Delegation may be revoked or narrowed at any time by the delegating authority.

## Conflicts and Escalation

A decision must escalate when:

- authority is unclear;
- proposer and approver independence is inadequate;
- the impact crosses products, tenants or organizations;
- a decision changes stable shared contracts;
- risk exceeds delegated limits;
- legal, contractual or security obligations are uncertain;
- an exception would weaken a constitutional invariant.

Constitutional conflicts must stop the decision until resolved.

## Review

This policy must be approved before:

- the first capability becomes `Active`;
- the first external production conformance claim;
- material authority is delegated away from the owner.

Review triggers include organizational growth, appointment of CTO or Chief Architect roles, first external production deployment, a material incident, or repeated decision bottlenecks.

## Approval Record

Decision: `Pending`
Decision authority: `ООО «Арвектум»`
Approved by: `Pending`
Decision date: `Pending`
Canonical approval reference: `Pending`
