# Arvectum OS

Arvectum OS is an operating system for organizational intelligence: a domain-neutral platform foundation for organizational memory, knowledge, standards, workflows, decisions, documents, governance and controlled improvement.

## Start here

Every human contributor, AI agent and connected product must begin with:

1. [The Constitution of Arvectum OS](docs/constitution/CONSTITUTION.md)
2. [Agent Rules](AGENTS.md)
3. [RFC Index](docs/rfc/README.md) and relevant Accepted RFCs/ADRs
4. [Architecture Glossary](docs/architecture/GLOSSARY.md) for canonical terminology and source navigation
5. [Canonical Roadmap](docs/roadmap/ROADMAP.md) when determining sequence, next work, milestones or implementation readiness
6. [Reference Implementation Readiness Baseline](docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md) before beginning the first shared reference implementation slice

The Constitution has the highest architectural authority in this repository. The current ratified version is `1.2.0`.

The glossary and implementation-readiness baseline are subordinate navigation/delivery artifacts and do not override the Constitution or Accepted RFCs. The roadmap is the canonical planning source, but it does not override the Constitution, Accepted RFCs or Accepted ADRs.

For ChatGPT projects and long-lived chats, use:

- [ChatGPT Project Bootstrap](docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md)

## Repository role

This repository contains the canonical architecture, governance and reference implementation of Arvectum OS.

Domain products such as procurement, marketing, finance or legal agents live outside this repository and connect to Arvectum OS through explicit Product Contracts when platform interaction exists.

## Current phase

`Phase 0 — Foundation / Architecture Bootstrap` is complete.

The foundational semantic sequence RFC-0001 through RFC-0007 is `Accepted 1.0.0`. Architecture Glossary `1.2.0` is synchronized to those Accepted sources, and Roadmap Block 0H `Reference implementation readiness` is complete.

The next canonical delivery step is the first bounded executable reference implementation slice defined in [Reference Implementation Readiness Baseline](docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md).

That first slice is intentionally reversible and does not yet canonically select a programming language, database, public API protocol, event broker, workflow engine, IAM provider, retrieval engine, model provider or permanent service topology. Concrete choices should use an ADR only when they become sufficiently constraining under the readiness baseline.

Working reference code does not by itself make a Platform Capability `Active`, establish operational readiness, create an SLA/support commitment or authorize a full-platform production conformance claim.

RFC-0008 remains reserved by RFC-0001 for `Document and Artifact Architecture`; Reference implementation readiness is Roadmap Block 0H rather than RFC-0008.

The current sequence is maintained only in the [Canonical Roadmap](docs/roadmap/ROADMAP.md).

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
