# Arvectum OS Decision Authority Policy

Status: `Proposed`
Version: `0.2.1`
Created: `2026-08-07`
Updated: `2026-08-07`
Category: `governance`
Constitution basis: `1.2.0`
Architecture basis: `RFC-0001 v1.0.0 Accepted`
Policy owner: `ООО «Арвектум»`

## Purpose

This policy defines the initial decision-authority matrix for Arvectum OS.

It prevents three failure modes:

- every material decision escalating to the founder or owner;
- proposers approving their own material risks or shared-platform obligations;
- commercial or operational commitments becoming binding without authority over the affected platform scope.

This policy is `Proposed`. Until it is approved, the owner of Arvectum OS retains residual decision authority.

## Principles

1. Decision authority follows affected scope, consequence and reversibility.
2. Material decisions require an approver with sufficient independence from the proposer.
3. Low-risk reversible decisions should be delegated close to the work.
4. No delegation may weaken the Constitution or an accepted RFC.
5. Every governed decision must have a canonical reference.
6. Authority may be delegated to a person, role or governance body, but delegation scope and limits must be explicit.
7. A customer-facing commitment cannot create authority that the proposer does not already hold.

## Decision Classes

### Class A — Fundamental Governance

Includes:

- constitutional amendments;
- acceptance or supersession of foundational platform RFCs;
- irreversible changes to the fundamental platform model;
- changes to owner authority.

Decision authority: `Owner of Arvectum OS`.

Proposer may not be the sole approver.

### Class B — Shared Platform, Material Risk and External Commitment

Includes:

- promotion of a capability to `Active`;
- approval of operational readiness for an `Active` capability where material customer or shared-platform obligations exist;
- backward-incompatible stable public-contract changes;
- material shared-platform exceptions;
- production exceptions affecting multiple products or tenants;
- commercial commitments that create new stable platform obligations, conformance claims, portability promises, support guarantees or material customer-facing operational commitments;
- cross-organization data access or knowledge reuse;
- acceptance of material security, privacy, legal, financial, safety or reputational gaps.

Decision authority: `Owner` or explicitly delegated `Platform Decision Authority` with authority over the affected scope.

Required consultation where applicable:

- architecture;
- technology and operations;
- security or privacy;
- legal or commercial owner;
- finance or risk owner;
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
- accurately scoped pilot commitments that do not represent the subject as an Active capability or create undeclared stable platform obligations;
- low-risk reversible exceptions that do not alter shared contracts, cross tenant boundaries or create material external commitments.

Decision authority: delegated `Product Decision Authority` within approved budget, data, risk, commercial and time limits.

Self-approval may be allowed only when delegation explicitly permits it and the decision remains low-risk, reversible and product-local.

### Class E — Operational Changes

Includes routine operational, deployment and maintenance decisions within approved contracts, operational-readiness boundaries and policies.

Decision authority: delegated operational owner.

Material incidents, customer-impacting commitments, exceptions or changes outside approved boundaries escalate to the applicable higher class.

## Initial Authority Matrix

Until named roles or governance bodies are approved, the following temporary matrix applies:

| Decision class | Proposer | Decision authority | Required independence |
|---|---|---|---|
| A | Any authorized proposer | Owner | Owner approval explicit |
| B | Product, platform, commercial, operational or governance owner | Owner | Proposer may not solely approve |
| C | Product or platform owner | Owner | Proposer may not solely approve shared obligation or material risk |
| D | Product owner or delegated operator | Owner or explicit product delegation | Self-approval only if explicitly delegated and low-risk |
| E | Operational owner | Owner or explicit operational delegation | Separation required when material risk, exception or external commitment arises |

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
- affected customer-facing commitments where applicable;
- operational-readiness evidence where applicable;
- effective date;
- expiry, review or supersession condition;
- canonical approval reference.

## Commercial Commitment Approval

A commercial proposal, statement of work, service description or customer commitment that materially changes supported platform obligations, conformance scope, stable compatibility, portability, security or operational commitments must be approved by an authority with responsibility for the affected scope before it becomes binding.

Sales, marketing, product or delivery ownership does not by itself authorize representation of a Product Experiment, Candidate or Incubating capability as Active.

A delegated product authority may approve a bounded pilot commitment only within explicit lifecycle, support, risk, budget and time limits.

## Operational Readiness Approval

Promotion to `Active` requires approved operational-readiness evidence proportionate to scope, consequence and customer commitments.

The approving authority must verify, where applicable:

- accountable support ownership;
- observability and health evidence;
- incident and recovery path;
- continuity and dependency assumptions;
- backup, restoration or reconstruction path;
- customer-facing support and operational commitments;
- migration, deprecation and communication responsibilities.

Operational readiness may rely on manual or bounded controls when proportionate and explicitly approved, but the limitations and review trigger must be recorded.

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
- customer or commercial commitment limits where relevant;
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
- a commercial commitment exceeds approved platform lifecycle, conformance or operational readiness;
- risk exceeds delegated limits;
- legal, contractual or security obligations are uncertain;
- an exception would weaken a constitutional invariant.

Constitutional conflicts must stop the decision until resolved.

## Review

This policy must be approved before:

- the first capability becomes `Active`;
- the first external production conformance claim;
- the first material customer commitment that depends on an Active platform capability;
- material authority is delegated away from the owner.

Review triggers include organizational growth, appointment of CTO or Chief Architect roles, first external production deployment, a material incident, material commercial overcommitment or repeated decision bottlenecks.

## Approval Record

Decision: `Pending`
Decision authority: `ООО «Арвектум»`
Approved by: `Pending`
Decision date: `Pending`
Canonical approval reference: `Pending`
