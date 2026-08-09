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

The completed canonical milestone sequence is now:

- `Phase 0 — Foundation / Architecture Bootstrap` — `Complete`, `M0` achieved;
- `Phase 1 — Reference Implementation` — `Complete`, `M1 — First executable architectural spine proven` achieved for its declared scope;
- `Phase 2 — Core Runtime` — `Complete`, `M2 — Reusable governed runtime baseline` achieved for the bounded reusable-runtime reference scope;
- `Phase 3 — Shared Platform Capabilities` — `Complete`, `M3 — Validated shared capability baseline` achieved for the bounded shared-capability reference scope;
- `Phase 4 — Workspace / Operator Experience` — `Complete`, `M4 — Coherent governed workspace baseline` achieved for the bounded governed-workspace reference scope.

[P4.12 — Phase 4 / M4 Closure Review](docs/reviews/P4-12-phase-4-m4-closure-review.md) records the current closure decision: **`PASS — M4 achieved for the declared bounded governed-workspace reference scope.`** The completed [Phase 4 workstream](docs/roadmap/PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md) records P4.01–P4.12 at `100%` and R9–R12 complete.

The retained capability set remains unchanged by M4 closure:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative governed discovery/projection semantics;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

The P4.08 bounded Product Contract remains `Provisional 0.1.0`.

M4 closure does **not** promote any capability to `Active`, create a Stable Product Contract, create a Stable/public API/SDK/wire/frontend compatibility boundary, select durable frontend/IAM/read-model/search/document/service infrastructure, establish `Production` or operational readiness, claim formal WCAG or full-platform conformance, or create SLA/support/commercial commitments.

The final synchronized P4.11 pull-request head was validated by `Reference Python CI #200` on PR #60 with Ubuntu 24.04.4, CPython 3.12.13 and `570 tests`, `OK`. P4.12 itself introduces no runtime behavior change; it closes the already implemented and hardened bounded milestone.

Canonical M4 evidence:

- [P4.12 Phase 4 / M4 closure review](docs/reviews/P4-12-phase-4-m4-closure-review.md)
- [Completed Phase 4 workstream](docs/roadmap/PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md)
- [P4.11 workspace hardening / ADR / refactoring review](docs/reviews/P4-11-workspace-hardening-adr-refactoring-review.md)
- [R12 M4 Workspace Hardening](docs/reviews/R12-m4-workspace-hardening.md)
- [P4.10 workspace architecture fitness + accessibility/usability baseline](docs/reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md)
- [P4.10 hosted CI validation](docs/reviews/P4-10-ci-validation.md)
- [P4.09 security, rights, minimization and authority-safe UX review](docs/reviews/P4-09-security-rights-minimization-authority-safe-ux.md)
- [R11 Composition / Usability Refactoring Review](docs/reviews/R11-composition-usability-refactoring-review.md)
- [P4.08 cross-capability task/context composition review](docs/reviews/P4-08-cross-capability-task-context-composition.md)
- [P4.08 bounded Product Contract](docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md)
- [R10 Operator Safety / Cross-Capability Health Review](docs/reviews/R10-operator-safety-cross-capability-health-review.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)

The next canonical action is:

> **Phase 5 boundary revalidation and decomposition — SDK, Contracts and Extension Experience.**

`Phase 5` remains `Draft`. Before it becomes `Active`, its draft strategic scope must be revalidated against M4 evidence and actual product/extension demand, then decomposed into a bounded P5 work breakdown with explicit exit criteria. A planning transition does not itself stabilize Product Contracts/interfaces or change capability lifecycle, operational environment/readiness or conformance maturity.

The current delivery sequence is maintained only in the [Canonical Roadmap](docs/roadmap/ROADMAP.md) and [RFC Index](docs/rfc/README.md).

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
