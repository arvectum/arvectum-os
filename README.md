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

`Phase 0 — Foundation / Architecture Bootstrap` is complete.

`Phase 1 — Reference Implementation` is also complete. The bounded executable slice closed through `P1.12 — Phase 1 bounded-slice closure review`, and milestone `M1 — First executable architectural spine proven` is achieved for its declared scope.

Canonical Phase 1 evidence:

- [Phase 1 work breakdown and completion record](docs/roadmap/PHASE-1-REFERENCE-IMPLEMENTATION.md)
- [P1.12 bounded-slice closure review](docs/reviews/P1-12-phase-1-bounded-slice-closure-review.md)
- [Bounded Python reference harness](reference/python/README.md)

The final executable Phase 1 harness contains `128` passing architecture-fitness tests in the recorded GitHub Actions baseline. That result is scoped reference evidence only: it does not make a Platform Capability `Active`, make the Python harness a production runtime, create a public compatibility contract or establish full-platform conformance.

`Phase 2 — Core Runtime` is **not Active yet**. The current canonical action is to revalidate and decompose Phase 2 against Phase 1 evidence, Accepted architecture and relevant product/workflow evidence before substantive implementation. The detailed `P2.xx` work breakdown and any necessary ADRs must be established through the phase-transition rule in the Canonical Roadmap.

RFC-0001 through RFC-0008 are `Accepted 1.0.0`. Accepted architecture remains binding within the scope of each RFC and is not changed by Phase 1 completion.

The Phase 1 reference harness intentionally avoided selecting a permanent programming language contract, database, public API protocol, event broker, workflow engine, IAM provider, retrieval engine, model provider or service topology. Concrete Phase 2 choices should use an ADR only when they become sufficiently constraining under the existing ADR gate.

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
