# Arvectum OS Capability Catalog

Status: `Informative`
Version: `0.2.0`
Updated: `2026-08-06`
Architecture basis: `RFC-0001 v0.4.0`

## Purpose

This catalog records the current candidate, incubating, active, deprecated and retired capability areas of Arvectum OS.

It is intentionally separate from RFC-0001 because capabilities may be added, split, merged, renamed, returned to a product or retired without changing the foundational architecture, provided the change remains compatible with accepted RFCs.

This document is not an authority above the Constitution or accepted RFCs.

## Lifecycle States

Capabilities use the lifecycle defined by RFC-0001:

```text
Candidate → Incubating → Active → Deprecated → Retired
```

- `Candidate` — documented proposal without an implementation commitment.
- `Incubating` — limited implementation being tested through a real product or organizational need.
- `Active` — approved shared capability with supported contracts and evidence for platform ownership.
- `Deprecated` — available for migration but not recommended for new consumers.
- `Retired` — no longer available except through preserved historical or archival support.

A lifecycle transition must identify the approving decision, owner and effective date.

## Capability Entry Requirements

Each capability entry should identify:

- capability owner;
- organizational outcome;
- sponsoring need or product;
- current and expected consumers;
- lifecycle status;
- public or provisional contracts;
- canonical record ownership;
- dependencies;
- emitted events;
- authority and access rules;
- compatibility policy;
- operational evidence;
- review date where required;
- promotion, deprecation and retirement criteria.

## Incubation Requirements

An `Incubating` capability must declare:

- a sponsoring product or organizational need;
- an accountable owner;
- a bounded implementation scope and budget;
- a reuse hypothesis;
- a review date;
- criteria for promotion to `Active`;
- criteria for returning the capability to a product, replacing it or retiring it;
- provisional contracts and known compatibility limits.

Incubation does not prove that the capability belongs permanently in the platform.

## Promotion to Active

A capability may become `Active` only after passing the Economic Admission Test in RFC-0001.

The supporting decision should show:

- constitutional or cross-product need;
- demonstrated or credible consumers;
- measurable product, cost, quality, control or risk benefit;
- ownership and support capacity;
- compatibility and migration policy;
- why platform ownership is better than product ownership or an external solution.

## Exit and De-platformization

A capability should be returned to a product, replaced, deprecated or retired when evidence no longer supports centralized platform ownership.

Review triggers include:

- no second consumer appears within the incubation period;
- integration remains slower or more expensive than local implementation;
- the capability becomes a recurring product bottleneck;
- support cost exceeds demonstrated value;
- a commodity external solution provides a better outcome;
- the abstraction cannot remain domain-independent.

Exit decisions must preserve required history, compatibility obligations and migration paths.

## Current Capability Areas

All entries below remain `Candidate`. Listing does not authorize implementation or imply that a separate service must exist.

| Capability area | Intended organizational outcome | Status | Owner | Sponsor | Review date |
|---|---|---|---|---|---|
| Identity and Authority | Attribute actions, evaluate permissions and represent delegated authority | Candidate | Unassigned | Unassigned | Not set |
| Canonical Records and Relationships | Preserve significant organizational objects and their graph | Candidate | Unassigned | Unassigned | Not set |
| Product Contracts and Extension Registry | Validate product-platform compatibility and registered extensions | Candidate | Unassigned | Unassigned | Not set |
| Governed Workflow Execution | Execute repeatable processes within explicit Execution Contexts | Candidate | Unassigned | Unassigned | Not set |
| Events, Provenance and Observability | Reconstruct meaningful actions, causes, inputs and outputs | Candidate | Unassigned | Unassigned | Not set |
| Governance and Approvals | Apply proportional human authority to consequential changes and decisions | Candidate | Unassigned | Unassigned | Not set |
| Validation | Execute reusable structural, semantic, quality and policy controls | Candidate | Unassigned | Unassigned | Not set |
| Organizational Memory | Retain structured operational experience with provenance | Candidate | Unassigned | Unassigned | Not set |
| Organizational Knowledge | Preserve validated, reusable organizational understanding | Candidate | Unassigned | Unassigned | Not set |
| Standards and Policies | Version approved production methods and behavioral constraints | Candidate | Unassigned | Unassigned | Not set |
| Decisions | Preserve context, alternatives, rationale, consequences and approval | Candidate | Unassigned | Unassigned | Not set |
| Documents and Artifacts | Manage identity, versions, generation context and lifecycle of deliverables | Candidate | Unassigned | Unassigned | Not set |
| Search and Context Resolution | Resolve relevant records and relationships without creating a second source of truth | Candidate | Unassigned | Unassigned | Not set |
| Integration and Adapter Management | Register and operate replaceable technology and external-system adapters | Candidate | Unassigned | Unassigned | Not set |

## Change Rule

Changing this catalog does not by itself authorize implementation.

A catalog change requires an RFC when it changes a foundational law, Kernel primitive, product boundary, sovereignty rule or another accepted architectural contract.

Other lifecycle and inventory changes may be governed by an ADR or an approved catalog maintenance process, provided the required evidence and ownership are recorded.