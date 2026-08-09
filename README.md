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

`Phase 5 — SDK, Contracts and Extension Experience` is now `Active`. [P5.01 — Integration Boundary Revalidation + Developer Journeys](docs/reviews/P5-01-integration-boundary-revalidation-developer-journeys.md), [P5.02 — Product Contract Declaration Model + Machine-Checkable Validation Baseline](docs/reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md), [R13 — Integration Boundary Review](docs/reviews/R13-integration-boundary-review.md) and [P5.03 — Governed Dependency/Version Resolution + Compatibility Semantics](docs/reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md) record **`PASS`**. The current canonical action is now `P5.04 — Integration composition API/facade boundary`.

P5.01/P5.02/R13/P5.03 establish the current integration baseline:

- Product Contract remains the governed product/platform boundary authority and the existing RFC-0004 `ProductContract` remains the single executable declaration model for the bounded reference implementation;
- relied-upon dependency, operation and version semantics are explicit and machine-checkable;
- J1 = governed read/composition consumer;
- J2 = consequential product action through exact Product Contract continuity and Governed Execution;
- P5.02 validation evidence preserves exact Product Contract/Product/dependency/operation/canonical-access semantics, Organization scope, accountable owner and lifecycle/review/exit responsibilities;
- R13-F1 preserves dependency provider/consumer/failure responsibilities and operation failure semantics in derived evidence;
- P5.03 adds exact Product Contract/dependency version resolution against explicit governed provider/version support evidence, with no SemVer/package/module/dataclass inference and no automatic fallback version;
- compatibility outcomes are explicit (`Compatible`, `VersionMismatch`, `Unsupported`, `Deprecated`, `Retired`, `Ambiguous`) and non-compatible reliance fails closed deterministically;
- changed/deprecated/retired dependency reliance exposes migration obligations rather than silently advancing to another version;
- Product Contract declaration/admission/validation/resolution grants neither Authorization nor Organizational Authority;
- capability lifecycle remains owned by RFC-0001 governance and the canonical capability catalog, not by Product Contract validation/resolution tooling;
- current Python module/import/dataclass shapes remain internal/provisional executable evidence, not a Stable/public SDK contract;
- private tables/stores/imports/routes/Event streams, implicit shared state and lower-level mutation bypasses are not valid integration boundaries;
- no stable/public serialization, SDK/API, wire, package, registry or version-negotiation boundary is created by the Phase 5 declaration/validation/resolution tooling.

The retained capability set remains unchanged:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative governed discovery/projection semantics;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

The P4.08 bounded Product Contract remains `Provisional 0.1.0`.

P5.01/P5.02/R13/P5.03 does **not** promote any capability to `Active`, create a Stable Product Contract, create a Stable/public API/SDK/wire/manifest/module/package/registry/version-negotiation compatibility boundary, select durable package/plugin/network/IAM/Event/storage infrastructure, establish `Production` or operational readiness, claim M5/full-platform conformance, or create SLA/support/commercial commitments.

Canonical current evidence:

- [Canonical Roadmap](docs/roadmap/ROADMAP.md)
- [Active Phase 5 workstream](docs/roadmap/PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md)
- [P5.01 integration boundary revalidation + developer journeys](docs/reviews/P5-01-integration-boundary-revalidation-developer-journeys.md)
- [P5.02 Product Contract declaration/validation review](docs/reviews/P5-02-product-contract-declaration-model-machine-checkable-validation-baseline.md)
- [R13 Integration Boundary Review](docs/reviews/R13-integration-boundary-review.md)
- [P5.03 governed dependency/version resolution review](docs/reviews/P5-03-governed-dependency-version-resolution-compatibility-semantics.md)
- [P4.12 Phase 4 / M4 closure review](docs/reviews/P4-12-phase-4-m4-closure-review.md)
- [P4.08 bounded Product Contract](docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)

The current canonical action is:

> **P5.04 — Integration composition API/facade boundary.**

P5.04 must extract the smallest reusable integration-facing composition boundary from the proved J1/J2 journeys and the Product Contract declaration/validation/resolution semantics now established by P5.02/P5.03. It must avoid private platform coupling, delegate authority/canonical-state decisions to existing semantic owners, preserve exact Product Contract/dependency continuity, and avoid turning the current Python facade/module shape into a Stable/public API without the applicable evidence and governance.

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
