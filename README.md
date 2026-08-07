# Arvectum OS

Arvectum OS is an operating system for organizational intelligence: a domain-neutral platform foundation for organizational memory, knowledge, standards, workflows, decisions, documents, governance and controlled improvement.

## Start here

Every human contributor, AI agent and connected product must begin with:

1. [The Constitution of Arvectum OS](docs/constitution/CONSTITUTION.md)
2. [Agent Rules](AGENTS.md)
3. [RFC Index](docs/rfc/README.md) and relevant Accepted RFCs/ADRs
4. [Architecture Glossary](docs/architecture/GLOSSARY.md) for canonical terminology and source navigation
5. [Canonical Roadmap](docs/roadmap/ROADMAP.md) when determining sequence, next work, milestones or implementation readiness

The Constitution has the highest architectural authority in this repository. The current ratified version is `1.2.0`.

The glossary is informative and does not override the Constitution or Accepted RFCs. The roadmap is the canonical planning source, but it does not override the Constitution, Accepted RFCs or Accepted ADRs.

For ChatGPT projects and long-lived chats, use:

- [ChatGPT Project Bootstrap](docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md)

## Repository role

This repository contains the canonical architecture, governance and future reference implementation of Arvectum OS.

Domain products such as procurement, marketing, finance or legal agents live outside this repository and connect to Arvectum OS through explicit product contracts.

## Current phase

`Phase 0 — Foundation / Architecture Bootstrap`

The current sequence is maintained only in the [Canonical Roadmap](docs/roadmap/ROADMAP.md).

The Architecture Glossary (`docs/architecture/GLOSSARY.md`) is published as the shared language baseline. RFC-0002 `Canonical Record, Kernel Metamodel, Authority, Relationship and Organizational Asset Model` is `Accepted 1.0.0`.

The current major architecture proposal is RFC-0003 `Identity, Security, Privacy, Tenant Sovereignty and Portability` `0.2.0` — `Proposed`, with functional role cross-review complete. It remains non-normative until explicit owner approval and valid acceptance publication.

Production implementation is not allowed to prejudge unresolved cross-cutting architecture. Bounded, reversible and migration-friendly reference implementation work may proceed in parallel when permitted by the Accepted architecture.

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
