# RFC-0000: Amend the Arvectum OS Constitution to Version 1.1.0

Status: `Accepted`
Date: `2026-08-06`
Owner: `ООО «Арвектум»`
Amends: `The Constitution of Arvectum OS 1.0.0`
Resulting version: `1.1.0`

## Summary

This RFC strengthens the Constitution from the perspective of a founder building a commercially viable platform company.

The amendment preserves the architectural principles of Arvectum OS while preventing platform discipline from becoming an obstacle to product discovery, customer value, commercial speed or organizational sovereignty.

## Motivation

Version 1.0.0 established strong safeguards for reuse, explainability, governance, versioning, domain boundaries and technology independence.

A founder review identified several risks:

1. `Platform First` could be interpreted as requiring premature platformization before a product capability has demonstrated value.
2. `Domain Independence` could be interpreted as preventing Arvectum OS from storing and governing domain knowledge at all.
3. The Constitution did not explicitly require architectural effort to be proportionate to business value, maturity and risk.
4. Customer control, portability, migration and deletion were not explicitly protected.
5. Organizational intelligence and organizational assets were not defined precisely enough.
6. The purpose statement was unnecessarily limited to an `AI-native organization`.

## Amendments

### 1. Organizational intelligence

Introduce organizational intelligence as a compounding strategic asset rather than claiming it is universally the primary asset of every organization.

### 2. Purpose

Define Arvectum OS as an operational foundation for organizations in which people, AI systems and software work through shared memory, standards, workflows and governance.

Artificial intelligence is established as a means of execution, not the purpose of the platform.

### 3. Platform and product evolution

Replace a rigid `Platform First` interpretation with the following lifecycle:

1. experiment locally when uncertainty is high;
2. validate value and repeatability;
3. promote successful reusable mechanisms into Arvectum OS;
4. retire or contain unsuccessful experiments;
5. avoid indefinite duplication.

Capabilities may also belong in the platform before repeated product use when required for governance, security, identity, provenance or interoperability.

### 4. Domain boundaries

Require the kernel and shared platform contracts to remain domain-neutral while allowing Arvectum OS to store, govern and serve domain knowledge through product-owned modules, schemas and contracts.

### 5. Organizational control and portability

Protect an organization's governance and control over its data, organizational intelligence, standards, decisions and operational history, subject to applicable law and contract.

Require governed export, migration and deletion capabilities where legally and operationally permitted.

### 6. Organizational assets

An artifact becomes a governed organizational asset only when it is designated as authoritative, reusable, evidentiary or operationally significant.

Transient outputs are not automatically permanent assets.

### 7. Value and proportionality

Require governance, standardization, validation and reuse mechanisms to be proportionate to risk, maturity and expected impact.

Permit simpler reversible solutions when they are sufficient.

### 8. Architecture before irreversible implementation

Preserve architecture-first discipline for cross-cutting and materially constraining decisions while explicitly allowing bounded, reversible experiments.

### 9. Mission and final statement

Clarify that the long-term objective is not merely to build smarter artificial intelligence, but to help organizations become progressively more intelligent through accumulated experience.

## Consequences

### Positive

- Product teams can validate hypotheses without prematurely expanding the platform.
- Proven reusable mechanisms still converge into Arvectum OS.
- Domain knowledge can be governed without contaminating the kernel.
- Enterprise customers receive an explicit portability and control commitment.
- Architectural effort must remain tied to value and risk.
- The Constitution better reflects the founder's commercial and strategic responsibilities.

### Trade-offs

- Product-local prototypes require explicit promotion or retirement criteria.
- The boundary between a transient artifact and a governed organizational asset must be designated rather than assumed.
- Portability requirements may add implementation cost to storage and data models.
- Proportionality requires judgment and cannot be reduced to one universal rule.

## Compatibility and migration

No production implementation exists that requires migration.

Accepted RFCs, ADRs, catalogs and product contracts created after this amendment must reference Constitution version `1.1.0` or later.

Future architecture documents must distinguish:

- domain-neutral kernel and shared contracts;
- product-owned domain knowledge;
- local reversible experiments;
- validated reusable platform capabilities;
- transient artifacts;
- governed organizational assets.

## Alternatives considered

### Keep version 1.0.0 unchanged

Rejected because it could incentivize premature platform construction and create an internal contradiction around domain knowledge.

### Move all founder-oriented principles into a manifesto

Rejected because value proportionality, portability and product experimentation constrain architecture and therefore belong in the Constitution.

### Remove Platform First entirely

Rejected because reuse and convergence into a shared platform remain central to Arvectum OS.

## Approval

The owner of Arvectum OS explicitly approved applying these amendments on `2026-08-06`.
