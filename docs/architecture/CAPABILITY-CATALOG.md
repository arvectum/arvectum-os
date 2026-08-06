# Arvectum OS Capability Catalog

Status: `Informative`
Version: `0.3.0`
Updated: `2026-08-06`
Architecture basis: `RFC-0001 v0.5.0`
Constitution basis: `1.2.0`

## Purpose

This catalog records candidate, incubating, active, deprecated and retired platform capability areas of Arvectum OS.

It does not catalog ordinary product features or Product Experiments.

Capabilities may be added, split, merged, renamed, returned to products or retired without changing foundational architecture when the change remains compatible with the Constitution and accepted RFCs.

This document is informative and does not itself authorize implementation.

## Product Experiments Are Not Platform Capabilities

A Product Experiment is owned by a product or operational sponsor while uncertainty is high.

It may contain domain-specific logic and does not enter this catalog merely because it may later prove reusable.

A Product Experiment must have:

- an owner;
- bounded scope;
- risk and data classification;
- a review date;
- applicable security, privacy, legal and contractual controls;
- an explicit path to promotion, containment or retirement.

A reusable pattern enters this catalog only after a decision creates a `Candidate` or `Incubating` Platform Capability with a proposed domain-neutral boundary.

## Capability Lifecycle

```text
Candidate → Incubating → Active → Deprecated → Retired
```

- `Candidate` — documented platform proposal without implementation commitment.
- `Incubating` — limited domain-neutral platform boundary being tested through real consumers.
- `Active` — approved shared capability with supported contracts and evidence for platform ownership.
- `Deprecated` — available for migration but not recommended for new consumers.
- `Retired` — unavailable except through preserved history or explicit archival support.

Lifecycle transitions must identify the decision, owner and effective date.

## Capability Entry Requirements

Each entry should identify:

- owner;
- organizational outcome;
- source Product Experiment or strategic need;
- current and expected consumers;
- lifecycle status;
- public or provisional contracts;
- canonical record and organizational asset ownership;
- dependencies;
- emitted events;
- authority and least-privilege rules;
- tenant scope and data classification;
- retention, deletion, export and portability obligations;
- compatibility and migration policy;
- operational evidence;
- review date;
- promotion, deprecation, de-platformization and retirement criteria.

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

Incubation does not prove permanent platform ownership.

## Promotion to Active

A capability may become `Active` only after satisfying RFC-0001 admission rules.

The supporting decision should demonstrate:

- constitutional, strategic or cross-product need;
- credible consumers;
- measurable product, cost, quality, governance, security, portability or risk benefit;
- domain-neutral contracts;
- ownership and support capacity;
- compatibility, export and migration policy;
- why platform ownership is better than product ownership or an external solution.

## Exit and De-platformization

A capability should be returned to a product, replaced, deprecated or retired when centralized ownership is no longer justified.

Review triggers include:

- no second consumer within the declared period;
- integration slower or more expensive than local implementation;
- recurring product bottlenecks;
- support cost above demonstrated value;
- a superior commodity external solution;
- failure to remain domain-neutral;
- inability to meet security, isolation or portability obligations.

Exit decisions must preserve required history, contractual commitments, governed export and migration paths.

## Current Capability Areas

All entries remain `Candidate`. Listing does not authorize implementation or imply a separate service.

| Capability area | Intended organizational outcome | Status | Owner | Sponsor | Review date |
|---|---|---|---|---|---|
| Identity and Authority | Attribute actions, enforce least privilege and represent delegated authority | Candidate | Unassigned | Unassigned | Not set |
| Canonical Records, Relationships and Assets | Preserve governed objects, versions, organizational assets and their graph | Candidate | Unassigned | Unassigned | Not set |
| Security, Privacy and Tenant Isolation | Enforce classification, minimization, isolation, retention, deletion and auditability | Candidate | Unassigned | Unassigned | Not set |
| Organizational Control and Portability | Provide governed export, migration, handover and deletion capabilities | Candidate | Unassigned | Unassigned | Not set |
| Product Contracts and Extension Registry | Validate product-platform compatibility and registered extensions | Candidate | Unassigned | Unassigned | Not set |
| Governed Workflow Execution | Execute repeatable processes within explicit Execution Contexts | Candidate | Unassigned | Unassigned | Not set |
| Events, Provenance and Observability | Reconstruct meaningful actions, causes, inputs and outputs | Candidate | Unassigned | Unassigned | Not set |
| Governance and Approvals | Apply proportional authority to consequential changes and decisions | Candidate | Unassigned | Unassigned | Not set |
| Validation | Execute reusable structural, semantic, quality, security and policy controls | Candidate | Unassigned | Unassigned | Not set |
| Organizational Memory | Retain structured operational experience with provenance and permitted use | Candidate | Unassigned | Unassigned | Not set |
| Organizational Knowledge | Preserve validated, reusable organizational understanding | Candidate | Unassigned | Unassigned | Not set |
| Standards and Policies | Version approved methods and behavioral constraints | Candidate | Unassigned | Unassigned | Not set |
| Decisions | Preserve context, alternatives, rationale, consequences and authority | Candidate | Unassigned | Unassigned | Not set |
| Documents and Artifacts | Manage versions, generation context, classification and lifecycle of deliverables | Candidate | Unassigned | Unassigned | Not set |
| Search and Context Resolution | Resolve relevant records without creating a second source of truth | Candidate | Unassigned | Unassigned | Not set |
| Integration and Adapter Management | Operate replaceable technology and external-system adapters | Candidate | Unassigned | Unassigned | Not set |

## Change Rule

A catalog change requires an RFC when it changes a foundational law, Kernel primitive, product boundary, security or sovereignty invariant, portability obligation or another accepted architectural contract.

Other inventory and lifecycle changes may be governed by an ADR or approved catalog-maintenance process when evidence, ownership and migration are recorded.
