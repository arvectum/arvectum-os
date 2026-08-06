# Arvectum OS

Arvectum OS is an operating system for organizational intelligence: a domain-neutral platform foundation for organizational memory, knowledge, standards, workflows, decisions, documents, governance and controlled improvement.

## Start here

Every human contributor, AI agent and connected product must begin with:

1. [The Constitution of Arvectum OS](docs/constitution/CONSTITUTION.md)
2. [Agent Rules](AGENTS.md)
3. relevant accepted RFCs and ADRs

The Constitution has the highest architectural authority in this repository. The current ratified version is `1.2.0`.

For ChatGPT projects and long-lived chats, use:

- [ChatGPT Project Bootstrap](docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md)

## Repository role

This repository contains the canonical architecture, governance and future reference implementation of Arvectum OS.

Domain products such as procurement, marketing, finance or legal agents live outside this repository and connect to Arvectum OS through explicit product contracts.

## Current phase

`Foundation / Architecture Bootstrap`

Production implementation is intentionally deferred until the foundational RFCs define the platform architecture, language, core models, security boundaries and contracts.

The next architecture document is `RFC-0002 Architecture`. RFC identifiers `0000` and `0001` record the constitutional amendments that produced versions `1.1.0` and `1.2.0`.

## Authority order

1. Constitution
2. accepted RFCs
3. accepted ADRs
4. approved catalogs, standards and policies
5. implementation and tests
6. task materials
7. chat history and model memory
