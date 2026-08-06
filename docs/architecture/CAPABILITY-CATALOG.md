# Arvectum OS Capability Catalog

Status: `Informative`
Version: `0.6.0`
Updated: `2026-08-07`
Architecture basis: `RFC-0001 v0.8.0`
Constitution basis: `1.2.0`

## Purpose

This catalog records platform capabilities that have entered a governed lifecycle and separately lists exploratory areas that may or may not ever become platform work.

It does not catalog ordinary product features or Product Experiments.

Listing an item does not authorize implementation, allocate budget, create a roadmap commitment or prove that platform responsibility is appropriate.

## Architectural Responsibility and Legal Rights

Architectural responsibility means responsibility for capability boundaries, contracts, canonical state, lifecycle, validation, migration and operational support within Arvectum OS.

It does not determine legal title, intellectual-property ownership, licensing, confidentiality or contractual data rights.

## Product Experiments Are Not Platform Capabilities

A Product Experiment remains under product or operational responsibility while uncertainty is high.

A completely product-local experiment does not require a Product Contract. An experiment interacting with platform capabilities, shared event history or canonical platform state requires a proportionate `Provisional` Product Contract under RFC-0001.

A reusable pattern enters the governed capability lifecycle only after a recorded decision creates a `Candidate` or `Incubating` Platform Capability with a proposed domain-neutral boundary.

## Capability Lifecycle

```text
Candidate → Incubating → Active → Deprecated → Retired
```

- `Candidate` — governed platform proposal with an accountable owner, sponsor or constitutional rationale, review date and no implementation commitment unless separately approved.
- `Incubating` — limited domain-neutral platform boundary being tested through real consumers under a Provisional Contract.
- `Active` — approved shared capability with a supported stable contract and evidence for platform responsibility.
- `Deprecated` — available for migration but not recommended for new consumers.
- `Retired` — unavailable except through preserved history or explicit archival support.

Lifecycle transitions must identify the proposal, decision authority, architectural owner, effective date and canonical decision reference.

An item without an accountable owner, sponsor or constitutional rationale, and review date is not a lifecycle `Candidate`; it remains exploratory only.

## Lifecycle-specific Requirements

### Candidate

A Candidate entry must identify:

- proposed organizational outcome;
- architectural owner;
- sponsor or constitutional rationale;
- intended domain-neutral boundary;
- expected consumers or strategic need;
- reuse hypothesis;
- review date;
- criteria for incubation, containment or rejection.

A Candidate does not require an implemented contract or implementation commitment.

### Incubating

An Incubating entry must additionally identify:

- source Product Experiment or organizational need;
- sponsoring consumers;
- bounded scope and budget;
- Provisional domain-neutral contract;
- Canonical Record responsibilities and authority modes;
- provisional Kernel metamodel assumptions where applicable;
- external authoritative systems and synchronization obligations;
- dependencies and emitted events;
- security, authority and data-handling rules;
- retention, deletion, export and portability obligations;
- compatibility and migration requirements;
- promotion, return-to-product, replacement and retirement criteria.

### Active

An Active entry must additionally identify:

- supported stable public contract;
- compatibility and migration policy;
- accountable operational support;
- evidence supporting centralized platform responsibility;
- maintained security, portability and lifecycle obligations;
- approved decision authority and canonical promotion reference;
- deprecation and retirement path.

## Decision Authority

Every lifecycle transition must comply with RFC-0001 and the approved Decision Authority Policy.

A proposer may not solely approve their own transition to `Active`, material exception, stable public-contract change or acceptance of a material known gap.

Until authority is delegated through an approved policy, the owner of Arvectum OS retains residual decision authority.

## Canonical Record Authority Modes

A capability that governs or consumes Canonical Records must identify the applicable authority mode:

- `Native`;
- `External Reference`;
- `Governed Replica`.

A capability must not create a competing source of truth when an external system remains authoritative.

## Kernel Metamodel Status

Until RFC-0002 is accepted, any capability depending on relationships among Identity, Canonical Record, Typed Relationship, Event and Execution Context must declare those assumptions `Provisional`.

No capability may publish an irreversible public contract that fixes a Kernel metamodel interpretation without an approved RFC or ADR.

## Current Horizon

The Current Horizon contains only capabilities relevant to an approved near-term product workflow or mandatory governance requirement and having an owner, sponsor or constitutional rationale, scope and review date.

No Current Horizon platform capability has yet been approved in this catalog.

## Active and Incubating Capabilities

No capability is currently recorded as `Active` or `Incubating`.

## Candidate Capabilities

No capability is currently recorded as a lifecycle `Candidate`.

## Exploratory Inventory

`Exploratory` is not a capability lifecycle state.

| Exploratory area | Possible organizational outcome |
|---|---|
| Identity and Authority | Attribute actions, enforce least privilege and represent delegated authority |
| Canonical Records, Kernel Metamodel, Authority, Relationships and Assets | Preserve governed objects, versions, authority modes and their graph |
| Security, Privacy and Tenant Isolation | Enforce classification, minimization, isolation, retention, deletion and auditability |
| Organizational Control and Portability | Provide governed export, migration, handover and deletion capabilities |
| Product Contracts and Extension Registry | Validate product-platform compatibility and registered extensions |
| Governed Workflow Execution | Execute repeatable processes within explicit Execution Contexts |
| Events, Provenance and Observability | Reconstruct meaningful actions, causes, inputs and outputs |
| Governance and Approvals | Apply proportional decision authority to consequential changes and decisions |
| Validation | Execute reusable structural, semantic, quality, security and policy controls |
| Organizational Memory | Retain structured operational experience with provenance and permitted use |
| Organizational Knowledge | Preserve validated, reusable organizational understanding |
| Standards and Policies | Version approved methods and behavioral constraints |
| Decisions | Preserve context, alternatives, rationale, consequences and authority |
| Documents and Artifacts | Manage versions, generation context, classification and lifecycle of deliverables |
| Search and Context Resolution | Resolve relevant records without creating a second source of truth |
| Integration and Adapter Management | Operate replaceable technology, external systems of record and adapters |

Exploratory areas may be removed, merged or renamed without deprecation because no supported capability contract exists.

## Conformance

A capability claiming RFC-0001 conformance must separately record:

- subject lifecycle;
- operational environment;
- conformance maturity;
- applicable requirements;
- authority modes;
- provisional Kernel assumptions;
- data and tenant scope;
- manual controls;
- exceptions and their decision authorities;
- known gaps;
- review date.

A catalog listing alone is not a conformance claim.

## Exit and De-platformization

A capability should be returned to a product, replaced, deprecated or retired when centralized responsibility is no longer justified.

Exit decisions must preserve required history, contractual commitments, governed export and migration paths.

## Change Rule

A catalog change requires an RFC when it changes a foundational law, Kernel primitive, metamodel constraint, authority mode, decision-authority invariant, product boundary, security invariant, sovereignty rule or portability obligation.

Other lifecycle changes may be governed by an ADR or approved catalog-maintenance process when evidence, authority, responsibility, conformance scope and migration are recorded.
