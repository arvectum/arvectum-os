# Arvectum OS

Arvectum OS is an operating system for organizational intelligence: a domain-neutral platform foundation for organizational memory, knowledge, standards, workflows, decisions, documents, governance and controlled improvement.

## Start here

Every human contributor, AI agent and connected product must begin with:

1. [The Constitution of Arvectum OS](docs/constitution/CONSTITUTION.md)
2. [Agent Rules](AGENTS.md)
3. [RFC Index](docs/rfc/README.md) and relevant Accepted RFCs/ADRs
4. [Architecture Glossary](docs/architecture/GLOSSARY.md) for canonical terminology and source navigation
5. [Canonical Roadmap](docs/roadmap/ROADMAP.md) when determining sequence, next work, milestones or implementation readiness
6. [Reference Implementation Readiness Baseline](docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md) for the implementation-readiness constraints that shaped the first shared reference slice

The Constitution has the highest architectural authority in this repository. The current ratified version is `1.2.0`.

The glossary and implementation-readiness baseline are subordinate navigation/delivery artifacts and do not override the Constitution or Accepted RFCs. The roadmap is the canonical planning source, but it does not override the Constitution, Accepted RFCs or Accepted ADRs.

For ChatGPT projects and long-lived chats, use:

- [ChatGPT Project Bootstrap](docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md)

## Repository role

This repository contains the canonical architecture, governance and reference implementation of Arvectum OS.

Domain products such as procurement, marketing, finance or legal agents live outside this repository and connect to Arvectum OS through explicit Product Contracts when platform interaction exists.

## Current phase

The completed canonical milestone sequence is:

- `Phase 0 — Foundation / Architecture Bootstrap` — `Complete`, `M0` achieved;
- `Phase 1 — Reference Implementation` — `Complete`, `M1 — First executable architectural spine proven` achieved for its declared scope;
- `Phase 2 — Core Runtime` — `Complete`, `M2 — Reusable governed runtime baseline` achieved for the bounded reusable-runtime reference scope;
- `Phase 3 — Shared Platform Capabilities` — `Complete`, `M3 — Validated shared capability baseline` achieved for the bounded shared-capability reference scope;
- `Phase 4 — Workspace / Operator Experience` — `Complete`, `M4 — Coherent governed workspace baseline` achieved for the bounded governed-workspace reference scope.

`Phase 3 — Shared Platform Capabilities` is complete; its M3 closure remains scoped to the bounded shared-capability reference baseline and does not promote any capability to `Active`.

`Phase 5 — SDK, Contracts and Extension Experience` is `Active`. P5.01 through P5.09 are complete, with R13 and R14 passed. P5.08 establishes the internal/provisional workspace/capability adapter seam without product-side private coupling. P5.09 proves reuse through a materially distinct read-only CAP-004 evidence/reconstruction extension with its own `Provisional 0.1.0` Product Contract and the same `arvectum_os_ref.integration_adapters` boundary as the first bounded product.

The P5.09 second-consumer proof also produced one bounded refactoring finding, P5.09-F1: a derived read-only operation does not necessarily expose direct canonical access. The internal P5.02 validator therefore no longer requires a fake canonical Read declaration for such a view. Where direct canonical access is declared, Read semantics remain validated; canonical mutation still requires explicit Write plus Organizational Authority. The change refines internal validation evidence and does not amend RFC-0004 or create a new contract authority.

The current Phase 5 integration baseline includes:

- Product Contract remains the governed product/platform boundary authority and the existing RFC-0004 `ProductContract` remains the single executable declaration model for the bounded reference implementation;
- relied-upon dependency, operation and version semantics are explicit and machine-checkable;
- exact dependency compatibility is determined from explicit governed provider/version evidence rather than package/module shape, inferred SemVer or automatic fallback;
- dependency-backed facade/adapter actions require explicit current governed provider/version evidence and re-run the existing resolution semantics before reliance;
- the first bounded product and the second read-only extension use the same internal/provisional `IntegrationAdapters` boundary rather than private platform implementation imports;
- workspace presentation, capability-specific access/reconstruction semantics, canonical-state decisions and Governed Execution remain delegated to their existing semantic owners;
- wrong-Organization, stale-continuity, missing-current-evidence and rights/classification negative paths remain fail-closed;
- Product Contract/capability admission remains non-authoritative and does not create permission, approval or Organizational Authority;
- Event/provenance/portable evidence remains version-aware and non-authoritative where derived;
- product/extension-specific behavior remains consumer-owned;
- Product Contract lifecycle and capability lifecycle remain distinct;
- no Stable/public SDK/API/wire/package/registry/facade/adapter/plugin-runtime/generated-code compatibility boundary is created by the current reference implementation.

Hosted `Reference Python CI #246` passed on the final P5.09 branch head after code, review and roadmap synchronization. The earlier P5.09 code proof was also covered by `Reference Python CI #242`, which passed the full 675-test reference suite.

The retained capability set remains unchanged:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative governed discovery/projection semantics;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

The P4.08 bounded Product Contract remains `Provisional 0.1.0`. The P5.09 evidence-extension Product Contract is also `Provisional 0.1.0`.

Completion of P5.09 does **not** promote any capability to `Active`, stabilize either Product Contract, establish `Production` or operational readiness, claim M5/full-platform conformance, or create SLA/support/commercial commitments. The second consumer is reuse evidence, not a lifecycle transition.

Canonical current evidence:

- [Canonical Roadmap](docs/roadmap/ROADMAP.md)
- [Active Phase 5 workstream](docs/roadmap/PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md)
- [P5.01 integration boundary revalidation + developer journeys](docs/reviews/P5-01-integration-boundary-revalidation-developer-journeys.md)
- [P5.02 Product Contract declaration/validation review](docs/reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md)
- [R13 Integration Boundary Review](docs/reviews/R13-integration-boundary-review.md)
- [P5.03 governed dependency/version resolution review](docs/reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md)
- [P5.04 integration composition facade review](docs/reviews/P5-04-integration-composition-api-facade-boundary.md)
- [P5.05 scaffolding/templates + local harness review](docs/reviews/P5-05-scaffolding-templates-local-integration-harness.md)
- [P5.06 security/authority/rights Organization-scope integration-guard review](docs/reviews/P5-06-security-authority-rights-organization-scope-integration-guards.md)
- [R14 Developer Safety / Contract Health Review](docs/reviews/R14-developer-safety-contract-health-review.md)
- [P5.07 Event/provenance/portability integration-support review](docs/reviews/P5-07-event-provenance-portability-integration-support.md)
- [P5.08 workspace/capability integration-adapter review](docs/reviews/P5-08-workspace-capability-integration-adapters.md)
- [P5.09 second materially distinct integration reuse proof](docs/reviews/P5-09-second-materially-distinct-integration-reuse-proof.md)
- [P4.12 Phase 4 / M4 closure review](docs/reviews/P4-12-phase-4-m4-closure-review.md)
- [P4.08 bounded Product Contract](docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)

The current canonical action is:

> **R15 — Reuse / Developer Experience Refactoring Review.**

R15 should review the demonstrated two-consumer evidence before further generalization: retain only abstractions supported by both materially distinct integrations, preserve the P5.09-F1 distinction between derived read-only views and direct canonical access, remove or contain consumer-shaped assumptions, and keep Product Contract/capability lifecycle plus public/stable compatibility decisions separate.

After R15, the next roadmap work item is `P5.10 — Phase 5 conformance + architecture fitness matrix`.

The current delivery sequence is maintained in the [Canonical Roadmap](docs/roadmap/ROADMAP.md) and [RFC Index](docs/rfc/README.md).

RFC-0001 through RFC-0008 are `Accepted 1.0.0` and remain binding within their declared scopes.

The reference implementation remains bounded and intentionally avoids establishing a permanent programming-language contract, durable database/object-store/search/vector/RAG topology, public API/SDK/wire format, Event broker/store, IAM provider, workflow engine, evidence-integrity technology or deployable service topology. Such choices must pass the applicable ADR/stable-boundary gates before material reliance.

## Roadmap blocks and RFC identifiers

Roadmap blocks and RFCs use separate identifier namespaces.

- `Block 0H` = `Reference implementation readiness` — completed non-RFC roadmap milestone.
- `RFC-0008` = `Document and Artifact Architecture` — separate architecture RFC, `Accepted 1.0.0`.
- `P1.12` = Phase 1 roadmap work item closing the bounded executable slice; it is not an RFC or ADR.

Do not call Block 0H `RFC-0008 readiness`. A roadmap milestone may occur between RFCs without consuming or renumbering an RFC identifier.

## Authority order

1. Constitution
2. Accepted RFCs
3. Accepted ADRs
4. approved catalogs, standards and policies
5. Product Contracts and approved product-specific decisions
6. implementation and tests
7. canonical roadmap as a planning artifact
8. task materials
9. chat history and model memory
