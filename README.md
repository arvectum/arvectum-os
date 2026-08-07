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

RFC-0001 through RFC-0008 are now `Accepted 1.0.0`. [`RFC-0008 — Document and Artifact Architecture`](docs/rfc/RFC-0008-document-artifact-architecture-v1.0.0.md) is binding architecture within its declared scope following explicit owner approval and canonical acceptance publication.

RFC-0008 establishes domain-neutral Document and Artifact semantics without adding a Kernel primitive or selecting a DMS, object store, database, file format, OCR engine, signing provider, search technology or service topology. Acceptance does not itself make a document/artifact Platform Capability `Active` or establish production, operational, SLA, support, archival, legal-signature or product-specific commitments.

The reference implementation delivery track remains independently ready: the first bounded executable reference implementation slice is defined in [Reference Implementation Readiness Baseline](docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md).

That first slice is intentionally reversible and does not yet canonically select a programming language, database, public API protocol, event broker, workflow engine, IAM provider, retrieval engine, model provider or permanent service topology. Concrete choices should use an ADR only when they become sufficiently constraining under the readiness baseline.

Working reference code does not by itself make a Platform Capability `Active`, establish operational readiness, create an SLA/support commitment or authorize a full-platform production conformance claim.

## Roadmap blocks and RFC identifiers

Roadmap blocks and RFCs use separate identifier namespaces.

- `Block 0H` = `Reference implementation readiness` — completed non-RFC roadmap milestone.
- `RFC-0008` = `Document and Artifact Architecture` — separate architecture RFC, now `Accepted 1.0.0`.

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
