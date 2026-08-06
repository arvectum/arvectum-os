# Arvectum OS Capability Catalog

Status: `Informative`
Version: `0.1.0`
Updated: `2026-08-06`
Architecture basis: `RFC-0001 v0.3.0`

## Purpose

This catalog records the current candidate and active capability areas of Arvectum OS.

It is intentionally separate from RFC-0001 because capabilities may be added, split, merged, renamed or retired without changing the foundational architecture, provided the change remains compatible with accepted RFCs.

This document is not an authority above the Constitution or accepted RFCs.

## Capability Admission

A capability may be promoted into the platform only after it passes the Economic Admission Test defined by RFC-0001.

Each catalog entry should eventually identify:

- capability owner;
- organizational outcome;
- current consumers;
- public contracts;
- canonical record ownership;
- dependencies;
- emitted events;
- authority and access rules;
- compatibility policy;
- operational evidence;
- lifecycle status.

## Initial Capability Areas

All entries below are `Candidate` until approved by a later RFC, ADR or implementation decision consistent with RFC-0001.

| Capability area | Intended organizational outcome | Status |
|---|---|---|
| Identity and Authority | Attribute actions, evaluate permissions and represent delegated authority | Candidate |
| Canonical Records and Relationships | Preserve significant organizational objects and their graph | Candidate |
| Product Contracts and Extension Registry | Validate product-platform compatibility and registered extensions | Candidate |
| Governed Workflow Execution | Execute repeatable processes within explicit Execution Contexts | Candidate |
| Events, Provenance and Observability | Reconstruct meaningful actions, causes, inputs and outputs | Candidate |
| Governance and Approvals | Apply proportional human authority to consequential changes and decisions | Candidate |
| Validation | Execute reusable structural, semantic, quality and policy controls | Candidate |
| Organizational Memory | Retain structured operational experience with provenance | Candidate |
| Organizational Knowledge | Preserve validated, reusable organizational understanding | Candidate |
| Standards and Policies | Version approved production methods and behavioral constraints | Candidate |
| Decisions | Preserve context, alternatives, rationale, consequences and approval | Candidate |
| Documents and Artifacts | Manage identity, versions, generation context and lifecycle of deliverables | Candidate |
| Search and Context Resolution | Resolve relevant records and relationships without creating a second source of truth | Candidate |
| Integration and Adapter Management | Register and operate replaceable technology and external-system adapters | Candidate |

## Change Rule

Changing this catalog does not by itself authorize implementation.

A catalog change requires an RFC when it changes a foundational law, Kernel primitive, product boundary, sovereignty rule or another accepted architectural contract. Otherwise it may be governed by an ADR or an approved catalog maintenance process.