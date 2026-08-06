# Arvectum OS Capability Catalog

Status: `Informative`
Version: `0.4.0`
Updated: `2026-08-07`
Architecture basis: `RFC-0001 v0.6.0`
Constitution basis: `1.2.0`

## Purpose

This catalog records platform capabilities that have entered a governed lifecycle and separately lists exploratory capability areas that may or may not ever become platform work.

It does not catalog ordinary product features or Product Experiments.

This document is informative. Listing an item does not authorize implementation, allocate budget, create a roadmap commitment or prove that platform responsibility is appropriate.

## Product Experiments Are Not Platform Capabilities

A Product Experiment remains under product or operational responsibility while uncertainty is high.

It may contain domain-specific logic and does not enter this catalog merely because it may later prove reusable.

A Product Experiment must have:

- an owner;
- bounded scope;
- risk and data classification;
- a review date;
- applicable security, privacy, legal and contractual controls;
- an explicit path to promotion, containment or retirement.

A reusable pattern enters the governed capability lifecycle only after a recorded decision creates a `Candidate` or `Incubating` Platform Capability with a proposed domain-neutral boundary.

## Capability Lifecycle

```text
Candidate → Incubating → Active → Deprecated → Retired
```

- `Candidate` — governed platform proposal with an accountable owner, sponsor, review date and no implementation commitment unless separately approved.
- `Incubating` — limited domain-neutral platform boundary being tested through real consumers.
- `Active` — approved shared capability with supported contracts and evidence for platform responsibility.
- `Deprecated` — available for migration but not recommended for new consumers.
- `Retired` — unavailable except through preserved history or explicit archival support.

Lifecycle transitions must identify the decision, architectural owner and effective date.

An item without an accountable owner, sponsor and review date is not a lifecycle `Candidate`; it remains exploratory only.

## Governed Capability Entry Requirements

Each lifecycle entry must identify:

- architectural owner;
- organizational outcome;
- sponsoring product, workflow or governance need;
- current and expected consumers;
- lifecycle status;
- public or provisional contracts;
- canonical record and organizational asset responsibility;
- dependencies;
- emitted events;
- authority and least-privilege rules;
- tenant scope and data classification;
- retention, deletion, export and portability obligations;
- compatibility and migration policy;
- operational evidence;
- review date;
- promotion, deprecation, de-platformization and retirement criteria.

Architectural responsibility does not determine legal title, intellectual-property ownership, licensing or contractual data rights.

## Current Horizon

The Current Horizon contains only capabilities that are relevant to an approved near-term product workflow or mandatory governance requirement and have an owner, sponsor and review date.

No Current Horizon platform capability has yet been approved in this catalog.

An item may enter the Current Horizon only through a recorded decision that identifies:

- the real workflow or governance obligation it serves;
- why product-local implementation is insufficient or why platform incubation is justified;
- owner and sponsor;
- bounded scope and budget;
- lifecycle status;
- review date and exit criteria.

## Active and Incubating Capabilities

No capability is currently recorded as `Active` or `Incubating`.

This section must not be populated without the evidence and ownership required by RFC-0001.

## Candidate Capabilities

No capability is currently recorded as a lifecycle `Candidate`.

Exploratory areas listed below are not automatically candidates.

## Exploratory Inventory

The following areas are hypotheses about possible future platform responsibility. They are included to support discovery and architectural awareness only.

`Exploratory` is not a capability lifecycle state.

| Exploratory area | Possible organizational outcome |
|---|---|
| Identity and Authority | Attribute actions, enforce least privilege and represent delegated authority |
| Canonical Records, Relationships and Assets | Preserve governed objects, versions, organizational assets and their graph |
| Security, Privacy and Tenant Isolation | Enforce classification, minimization, isolation, retention, deletion and auditability |
| Organizational Control and Portability | Provide governed export, migration, handover and deletion capabilities |
| Product Contracts and Extension Registry | Validate product-platform compatibility and registered extensions |
| Governed Workflow Execution | Execute repeatable processes within explicit Execution Contexts |
| Events, Provenance and Observability | Reconstruct meaningful actions, causes, inputs and outputs |
| Governance and Approvals | Apply proportional authority to consequential changes and decisions |
| Validation | Execute reusable structural, semantic, quality, security and policy controls |
| Organizational Memory | Retain structured operational experience with provenance and permitted use |
| Organizational Knowledge | Preserve validated, reusable organizational understanding |
| Standards and Policies | Version approved methods and behavioral constraints |
| Decisions | Preserve context, alternatives, rationale, consequences and authority |
| Documents and Artifacts | Manage versions, generation context, classification and lifecycle of deliverables |
| Search and Context Resolution | Resolve relevant records without creating a second source of truth |
| Integration and Adapter Management | Operate replaceable technology and external-system adapters |

Exploratory areas may be removed, merged or renamed without deprecation because no supported capability contract exists.

## Incubation Requirements

An `Incubating` capability must declare:

- source experiment or organizational need;
- accountable platform owner;
- bounded implementation scope and budget;
- sponsoring and expected consumers;
- reuse hypothesis;
- provisional domain-neutral contract;
- security, privacy, isolation and portability requirements;
- review date;
- promotion criteria;
- criteria for return to a product, replacement or retirement.

Incubation does not prove permanent platform responsibility.

## Promotion to Active

A capability may become `Active` only after satisfying RFC-0001 admission rules.

The supporting decision should demonstrate:

- constitutional, strategic or cross-product need;
- credible consumers;
- measurable product, cost, quality, governance, security, portability or risk benefit;
- domain-neutral contracts;
- ownership and support capacity;
- compatibility, export and migration policy;
- why platform responsibility is better than product responsibility or an external solution.

## Exit and De-platformization

A capability should be returned to a product, replaced, deprecated or retired when centralized responsibility is no longer justified.

Review triggers include:

- no second consumer within the declared period;
- integration slower or more expensive than local implementation;
- recurring product bottlenecks;
- support cost above demonstrated value;
- a superior commodity external solution;
- failure to remain domain-neutral;
- inability to meet security, isolation or portability obligations.

Exit decisions must preserve required history, contractual commitments, governed export and migration paths.

## Change Rule

A catalog change requires an RFC when it changes a foundational law, Kernel primitive, product boundary, security or sovereignty invariant, portability obligation or another accepted architectural contract.

Other inventory and lifecycle changes may be governed by an ADR or approved catalog-maintenance process when evidence, responsibility and migration are recorded.
