# RFC-0001: Amend the Arvectum OS Constitution to Version 1.2.0

Status: `Accepted`
Date: `2026-08-06`
Owner: `ООО «Арвектум»`
Amends: `The Constitution of Arvectum OS 1.1.0`
Resulting version: `1.2.0`

## Summary

This RFC completes the founder review of the Arvectum OS Constitution before architecture design begins.

The amendment restores security, privacy and isolation as explicit structural requirements; makes decision records proportionate to impact; permits declared and replaceable vendor-specific workflow implementations; and removes the implementation-level term `kernel` from the constitutional domain-boundary rule.

## Motivation

Version `1.1.0` established the mission of Arvectum OS, organizational intelligence, product experimentation, value proportionality, portability and governed organizational assets.

A final review identified four remaining risks:

1. Security and privacy were referenced indirectly but were not protected by a dedicated constitutional article.
2. The decision-recording rule could be interpreted as requiring a full decision dossier for routine or reversible choices.
3. The workflow rule could be interpreted as prohibiting useful vendor-specific implementations even when their dependencies are explicit and replaceable.
4. The term `kernel` fixed an architecture concept before RFC-0002 defines the platform architecture.

## Scope and non-goals

This RFC changes only constitutional governance and related roadmap numbering.

It does not:

- select security technologies or compliance standards;
- define tenancy, identity or permission schemas;
- approve any model provider or vendor dependency;
- define the architecture of Arvectum OS;
- change the mission established in version `1.1.0`.

## Terminology

- **Structural property** — a requirement designed into platform capabilities and workflows rather than added only at deployment time.
- **Material decision** — a decision whose cost, duration, organizational scope or consequences justify a durable record.
- **Durable state** — governed organizational state that must survive replacement of an implementation dependency.
- **Vendor-specific implementation** — an implementation that relies on a named external technology while preserving declared boundaries and replaceability.
- **Shared platform foundations** — domain-neutral platform concepts and contracts whose concrete architecture will be defined by a later RFC.

## Proposed amendments

### 1. Security, privacy and isolation

Add a dedicated article establishing security, privacy, confidentiality and data isolation as structural properties of Arvectum OS.

Require identity, least privilege, authorization, tenant isolation, data minimization, retention, deletion and auditability to be designed into platform capabilities and workflows.

Prohibit experiments, automations and shortcuts from bypassing applicable security, privacy, legal or contractual controls.

Require control rigor to be proportionate to data sensitivity, consequence and threat.

### 2. Proportionate decision records

Replace the requirement to fully document every significant decision with a proportional rule covering material, durable or consequential decisions.

Decision records preserve context, alternatives, rationale, consequences and authority where applicable rather than requiring every field in every case.

### 3. Replaceable workflow dependencies

Replace the absolute prohibition on workflows depending on a specific model, vendor or runtime.

The business meaning, governance and durable state of a workflow may not be inseparably bound to such a dependency.

Vendor-specific implementations are permitted when dependencies are declared, bounded and replaceable without loss of governed organizational state.

### 4. Domain-boundary abstraction

Replace `kernel and shared platform logic` with `shared platform foundations, contracts and governance mechanisms`.

The Constitution therefore protects domain neutrality without deciding that the implementation must contain a component named `kernel`.

### 5. Article numbering

Insert the new security article after Organizational Control and Portability and renumber subsequent articles.

## Invariants

The amendment preserves these invariants:

- organizational intelligence remains the central strategic asset managed by Arvectum OS;
- AI remains a means of execution rather than the purpose of the platform;
- experiments remain bounded, reversible and governed;
- shared platform foundations remain domain-neutral;
- organizational control and portability remain protected;
- consequential automation remains explainable, observable and subject to proportional human governance;
- technologies remain replaceable and constitutional principles remain vendor-independent.

## Lifecycle and versioning

The resulting Constitution version is `1.2.0` and supersedes `1.1.0`.

This is a minor version because the amendment strengthens and clarifies existing principles without reversing the mission or invalidating an implemented platform contract.

Further constitutional amendments should require evidence of a practical conflict, material omission or strategic change rather than stylistic refinement alone.

## Security and privacy considerations

This amendment strengthens security and privacy by making them direct constitutional obligations.

Detailed controls, threat models, tenancy boundaries, identity semantics, retention policies and compliance mappings remain subjects for RFCs, ADRs, standards and product contracts.

## Observability and audit requirements

The amendment does not reduce observability requirements.

Security-relevant and consequential operations must remain reconstructable according to proportionality, applicable policies and data-retention constraints.

Decision records must identify decision authority or approval where applicable.

## Compatibility and migration

No production implementation exists that requires migration.

The architecture roadmap and RFC numbering are updated because `RFC-0001` is now consumed by this constitutional amendment. The system architecture document becomes `RFC-0002`, and subsequent planned RFC identifiers advance by one.

Future architecture documents must conform to Constitution `1.2.0` or later.

## Alternatives considered

### Keep version 1.1.0 unchanged

Rejected because security and privacy would remain only implicit and the workflow language could unnecessarily restrict product and vendor choices.

### Put security only in a later architecture RFC

Rejected because security, privacy and isolation constrain every future architecture and product implementation and therefore require constitutional authority.

### Preserve an absolute vendor-neutral workflow rule

Rejected because technology independence should protect governed state and replaceability, not prohibit pragmatic use of differentiated technologies.

### Keep the word `kernel`

Rejected because the Constitution should establish domain neutrality without predetermining the component model of RFC-0002.

## Unresolved questions

None at the constitutional level.

Concrete security architecture, isolation models, workflow portability contracts and decision-record formats remain intentionally unresolved for later RFCs.

## Acceptance criteria

This RFC is accepted when:

1. Constitution version `1.2.0` is committed as the canonical document;
2. the four amendments above are present without weakening version `1.1.0` principles;
3. RFC and roadmap numbering are internally consistent;
4. the owner explicitly approves the amendment;
5. the changes are merged into `main`.

## Consequences

### Positive

- Enterprise security and privacy expectations receive constitutional authority.
- Product teams can use differentiated vendor capabilities without surrendering governed organizational state.
- Decision governance remains rigorous without imposing unnecessary ceremony.
- Architecture remains free to define or reject a kernel component.
- The Constitution is ready to guide RFC-0002 Architecture without additional speculative refinement.

### Trade-offs

- Security and isolation requirements will add implementation obligations to every platform capability.
- Replaceability must be demonstrated through contracts and migration paths rather than asserted.
- Proportionality requires judgment and governance criteria in later documents.
- Planned RFC numbers after RFC-0001 advance by one.

## Approval

The owner of Arvectum OS explicitly approved applying these amendments on `2026-08-06`.
