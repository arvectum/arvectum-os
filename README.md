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

`Phase 0 — Foundation / Architecture Bootstrap` is complete and milestone `M0` is achieved.

`Phase 1 — Reference Implementation` is complete. The bounded executable slice closed through `P1.12 — Phase 1 bounded-slice closure review`, and milestone `M1 — First executable architectural spine proven` is achieved for its declared scope.

`Phase 2 — Core Runtime` is complete. The reusable bounded runtime closed through `P2.12 — Phase 2 / M2 closure review`, and milestone `M2 — Reusable governed runtime baseline` is achieved for its declared scope.

`Phase 3 — Shared Platform Capabilities` is **Active** as a roadmap/workstream phase. P3.01 through P3.11 plus engineering gates R5–R8 are complete. `P3.12 — Phase 3 / M3 closure review` is the current canonical action.

The retained Phase 3 capability set is:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

P3.11 confirmed the four capability identities as the bounded retained set for M3 evidence, but did not promote any capability to `Active`, create a Stable Product Contract/public API, select durable infrastructure, establish operational or production readiness, or create SLA/support/full-conformance commitments. P3.11 also found no current need for a new ADR or material shared refactor.

Canonical Phase 3 evidence:

- [Phase 3 work breakdown and current state](docs/roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)
- [P3.10 architecture fitness matrix](docs/reviews/P3-10-phase-3-architecture-fitness-matrix.md)
- [R8 milestone hardening review](docs/reviews/R8-phase-3-milestone-hardening.md)
- [P3.11 capability admission / ADR / refactoring hardening review](docs/reviews/P3-11-capability-admission-adr-refactoring-hardening-review.md)

RFC-0001 through RFC-0008 are `Accepted 1.0.0` and remain binding within their declared scopes.

The reference implementation remains bounded and intentionally avoids establishing a permanent programming-language contract, durable database/object-store/search topology, public API/SDK/wire format, Event broker/store, IAM provider, workflow engine, evidence-integrity technology or deployable service topology. Such choices must pass the applicable ADR/stable-boundary gates before material reliance.

Phase status, capability lifecycle, operational environment and conformance maturity remain distinct. `Phase 3 Active` does not mean any Platform Capability is lifecycle `Active` or production-ready.

## Roadmap blocks and RFC identifiers

Roadmap blocks and RFCs use separate identifier namespaces.

- `Block 0H` = `Reference implementation readiness` — completed non-RFC roadmap milestone.
- `RFC-0008` = `Document and Artifact Architecture` — separate architecture RFC, `Accepted 1.0.0`.
- `P1.12` = Phase 1 roadmap work item closing the bounded executable slice; it is not an RFC or ADR.

Do not call Block 0H `RFC-0008 readiness`. A roadmap milestone may occur between RFCs without consuming or renumbering an RFC identifier.

The current delivery sequence is maintained only in the [Canonical Roadmap](docs/roadmap/ROADMAP.md) and [RFC Index](docs/rfc/README.md).

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
