# Arvectum OS

Arvectum OS is a domain-neutral operating system for organizational intelligence: governed organizational state, execution, provenance, knowledge, documents, security, portability and product/platform interoperability.

## Start here

Every human contributor, AI agent and connected product should begin with:

1. [Constitution](docs/constitution/CONSTITUTION.md) — highest authority; current ratified/frozen version `1.2.0`.
2. [Agent Rules](AGENTS.md).
3. [RFC Index](docs/rfc/README.md) and the relevant Accepted RFCs.
4. [ADR Index](docs/adrs/README.md) and any relevant Accepted ADRs.
5. [Architecture Glossary](docs/architecture/GLOSSARY.md).
6. [Canonical Roadmap](docs/roadmap/ROADMAP.md).

`docs/roadmap/ROADMAP.md` is the **only canonical source for current action, phase sequencing and milestone status**. This README deliberately does not duplicate the mutable current-action pointer, so repository navigation cannot silently become a competing roadmap.

## Authority order

Use the following precedence when sources disagree:

1. Constitution;
2. Accepted RFC;
3. Accepted ADR;
4. approved policies, procedures, standards and catalogs;
5. Product Contracts and approved product decisions;
6. code and tests;
7. canonical roadmap;
8. task materials;
9. project/chat context;
10. model memory.

Lower-authority artifacts, including this README, never override higher-authority sources.

## Architecture baseline

The current accepted foundation is:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- no Accepted ADR currently selects a permanent public API/serialization, external-consumer registry, connector marketplace, customer-handover format, IAM provider, Event broker or multi-Organization deployment topology.

The platform remains technology-independent at the semantic level. Current Python reference implementation structures are executable evidence, not a permanent programming-language or public SDK contract.

## Current delivery state

Phases 0 through 7 are closed at their scoped milestones. Phase 8 — **Ecosystem and External Integration** — is the active workstream; exact current action and sequencing are maintained only in the [Canonical Roadmap](docs/roadmap/ROADMAP.md) and the [Phase 8 workstream](docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md).

Stable historical milestone continuity remains explicit:

- `Phase 3 — Shared Platform Capabilities` — `Complete`, `M3 — Validated shared capability baseline` achieved for the bounded shared-capability reference scope;
- `Phase 4 — Workspace / Operator Experience` — closed at its scoped milestone;
- those historical milestone records do **not** promote any capability to `Active`;
- The P4.08 bounded Product Contract remains `Provisional 0.1.0`; later implementation and reuse evidence do not silently convert it to `Stable`.

Phase 8 has validated, within the existing owner-operated internal contour:

- a bounded read-only EIS / `zakupki.gov.ru` external-authority revalidation case;
- one separately maintained Creative Test Agent consumer using an exact `Provisional 0.1.0` Product Contract and exact CAP-004 `1.0.0` read-only reconstruction dependency;
- bounded semantic portability/handover mechanics with an isolated same-Organization receiver;
- repeatable external operator/developer integration documentation for that exact external-consumer case.

Phase 8 does **not** establish arbitrary external compatibility, realistic multi-Organization isolation, customer handover, public/stable SDK/API/manifest/registry/export format, external/customer Production readiness, SLA/support/certification commitments, Stable Product Contracts or Active Platform Capabilities.

Canonical Phase 8 architecture disposition:

- [P8.11 — Ecosystem architecture hardening + ADR/refactoring/lifecycle disposition](docs/reviews/P8-11-ecosystem-architecture-hardening-adr-refactoring-lifecycle-disposition.md)
- [R27 — Portability / Ecosystem Reuse Review](docs/reviews/R27-portability-ecosystem-reuse-review.md)
- [P8.10 — Scoped external conformance / commercial / support boundary review](docs/reviews/P8-10-scoped-external-conformance-commercial-support-boundary-review.md)
- [P8.08 — Multi-Organization isolation + cross-organization security validation](docs/reviews/P8-08-multi-organization-isolation-cross-organization-security-validation.md)

## Platform capability lifecycle

The retained Platform Capability set remains:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`.

See the [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md) for the canonical subordinate lifecycle record.

`Incubating` is not `Active`. A successful reference implementation, internal deployment, Product Contract or external reuse case does not itself create Active lifecycle status, Stable compatibility, operational-readiness approval or commercial support obligations.

## Product / platform boundary

Products remain responsible for domain schemas, business workflows, rules, knowledge, prompts, UX, product-owned integrations and Product Experiments by default.

When a product relies on platform capabilities, shared platform history or canonical platform state, it must use the applicable versioned Product Contract under Accepted RFC-0004. Product Contract presence does not grant Authentication, Authorization, Organizational Authority, data-governance rights or capability lifecycle status.

Hidden dependencies through internal tables, private imports, undocumented endpoints, private streams or implicit shared mutable state are not allowed.

## Security, authority and AI boundary

Identity, Authentication, Authorization, Organizational Authority and Data Governance are distinct concerns. Access is deny-by-default and least-privilege. Organization boundaries, purpose limitation, minimization, retention/deletion and provenance are structural requirements.

AI may analyze, propose and execute explicitly governed bounded work. AI is not an Organizational Authority, final consequential approver or autonomous source of canonical truth.

Consequential canonical mutation remains subject to Governed Execution. Historical Event replay does not repeat external effects without fresh authorization.

## Portability and external authority

Arvectum OS does not assume it is always the primary system of record. External systems may remain authoritative through `External Reference` or `Governed Replica` semantics.

Portability must preserve governed organizational meaning — identities, versions, authority, provenance, relationships and handling constraints — without silently exporting secrets, permissions or Organizational Authority.

Current Phase 8 portability evidence is bounded semantic interoperability evidence only. External customer/cross-Organization transfer remains unactivated, and realistic two-Organization isolation remains unproven until the canonical re-entry condition is satisfied.

## Reference implementation

The reference implementation lives under [`reference/python`](reference/python/).

It intentionally avoids turning incidental implementation choices into architecture. Durable database/object-store/search/vector topology, stable API/SDK/wire format, Event broker/store, IAM/PDP/PEP provider, workflow engine, evidence-integrity technology and deployable service topology remain subject to their applicable future ADR/stable-boundary gates when materially relied upon.

See:

- [Reference Python README](reference/python/README.md)
- [Reference Implementation Readiness Baseline](docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md)

## Governance and continuity

For ChatGPT projects and long-lived workstreams use the [ChatGPT Project Bootstrap](docs/governance/CHATGPT_PROJECT_BOOTSTRAP.md).

For architecture changes, use the lowest sufficient governance level: Constitution amendment only for fundamental principles; RFC for major architecture/governance; ADR for concrete cross-cutting choices; policy/standard/catalog for subordinate rules; Product Contract for product/platform boundary; product decision for product-specific behavior; code/configuration only when no higher-level decision is required.

Do not infer acceptance, lifecycle promotion, Production readiness, conformance maturity or commercial promises from implementation success alone.