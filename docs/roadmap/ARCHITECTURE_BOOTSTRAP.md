# Arvectum OS Architecture Bootstrap

Status: `Active`
Version: `0.1`

## Goal

Define and approve the minimum stable architecture of Arvectum OS before production implementation.

## Phase A0 — Constitution and governance

Deliverables:

- Constitution;
- RFC process;
- ADR process;
- repository agent rules.

Exit criteria:

- owner approves Constitution v0.1;
- no external product or vendor is named as a constitutional dependency;
- precedence between Constitution, RFCs, ADRs and code is explicit.

## Phase A1 — System architecture

Document: `RFC-0001 Architecture`

Must define:

- platform boundary;
- domain-neutral kernel;
- platform services;
- product clients;
- event-driven interaction model;
- identity, permissions and provenance boundaries;
- deployment-neutral component view.

## Phase A2 — Entity and relation model

Document: `RFC-0002 Entity Model`

Must define:

- entity envelope;
- stable identity;
- type and schema version;
- state and lifecycle;
- relations;
- provenance;
- ownership and access classification;
- immutable history and derived representations.

## Phase A3 — Service model

Document: `RFC-0003 Service Model`

Initial service candidates:

- Entity Service;
- Identity and Permission Service;
- Memory Service;
- Knowledge Service;
- Workflow Service;
- Decision Service;
- Learning Service;
- Document Service;
- Brand and Standards Service;
- Event Service.

The RFC must validate boundaries rather than assume that every candidate becomes a separately deployed service.

## Phase A4 — Event model and catalog

Documents:

- `RFC-0004 Event Model`;
- `docs/catalogs/events/`.

Must define:

- event envelope;
- causation and correlation;
- initiator;
- entity and workflow references;
- versioning;
- immutability;
- privacy and retention;
- replay and idempotency expectations.

## Phase A5 — Workflow and decision model

Documents:

- `RFC-0005 Workflow Model`;
- `RFC-0006 Decision and Approval Model`.

Must define reproducibility, checkpoints, human approvals, validation, failure handling and observable outcomes.

## Phase A6 — Memory, knowledge and controlled learning

Documents:

- `RFC-0007 Memory and Knowledge Model`;
- `RFC-0008 Controlled Learning Model`.

The learning model must remain implementation-neutral. Existing external systems may later be evaluated as adapters, references or migration sources, but none is a constitutional dependency.

## Phase A7 — Product interface

Document: `RFC-0009 Product Integration Contract`

Must define how Tender Agent, Marketing Agent and future products:

- declare product identity and capabilities;
- consume company standards and memory;
- register domain entity extensions;
- emit platform events;
- request workflows and documents;
- enforce permissions;
- avoid duplicating platform responsibilities.

## Phase A8 — Document platform

Documents:

- `RFC-0010 Document Generation Contract`;
- `RFC-0011 Validation Contract`.

First acceptance scenario:

> Generate three materially different Arvectum presentations from the same approved brand, company and product standards, while preserving a stable visual and textual identity and producing complete provenance and validation reports.

## Phase A9 — Reference implementation

Only after A0–A8 are accepted:

- implement the smallest modular kernel;
- implement schemas and conformance tests;
- support one end-to-end document workflow;
- integrate one product as the first client;
- record all state changes as events;
- demonstrate reproducibility from recorded inputs and versions.

## Not in the bootstrap scope

- autonomous modification of approved rules;
- production microservice decomposition;
- premature selection of databases, brokers or model providers;
- migration of all existing product code;
- general-purpose low-code workflow UI;
- promises of self-managing organizational autonomy.
