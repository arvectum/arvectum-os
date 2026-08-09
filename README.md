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
- `Phase 4 — Workspace / Operator Experience` — `Complete`, `M4 — Coherent governed workspace baseline` achieved for the bounded governed-workspace reference scope;
- `Phase 5 — SDK, Contracts and Extension Experience` — `Complete`, `M5 — Repeatable product/extension integration` achieved for the bounded repeatable product/extension integration reference scope.

[P5.12 — Phase 5 / M5 Closure Review](docs/reviews/P5-12-phase-5-m5-closure-review.md) records the explicit closure decision: **PASS**.

M5 proves that two materially distinct bounded consumers can rely on the same explicit Product Contract/dependency/composition/adapter method without private platform coupling while preserving exact dependency/version identity, Organization isolation, Authorization/Organizational Authority separation, governed canonical mutation, Event/provenance attribution, rights/minimization, portability and consumer ownership of consumer-specific semantics.

The Phase 5 integration method remains bounded and internal/provisional:

`Product/Extension-owned Product Contract → declaration validation → exact governed dependency/version resolution → composition facade → IntegrationAdapters → existing semantic owners`

The first consumer is the bounded product integration. The second is the P5.09 read-only CAP-004 evidence/reconstruction extension with its own `Provisional 0.1.0` Product Contract, no workspace assumption and no canonical mutation. P5.09-F1 and R15 refined the shared abstraction from this materially distinct evidence instead of forcing consumer-specific assumptions into the platform.

P5.10 records the accumulated 15-row Phase 5 architecture-fitness index (`CF-01` through `CF-15`) with positive and negative/fail-closed executable evidence. R16 then hardened same-version Product Contract declaration continuity at the capability-adapter seam. P5.11 reviewed all nine explicit compatibility/public-boundary gates and retained an explicit **no-ADR / no-public-boundary** disposition.

P5.12 found one subordinate documentation synchronization defect, P5.12-F1: this README still reflected the earlier P5.10/R16 planning state while the canonical roadmap had already advanced to P5.12. The closure synchronizes the summary; no runtime or architectural change was required.

The final synchronized pre-closure hosted executable baseline is `Reference Python CI #269`: Ubuntu 24.04.4, CPython 3.12.13, `704 tests`, `OK`.

The retained capability set remains unchanged:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative governed discovery/projection semantics;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

The P4.08 bounded Product Contract remains `Provisional 0.1.0`. The P5.09 evidence-extension Product Contract also remains `Provisional 0.1.0`.

M5 closure does **not**:

- promote any capability to `Active`;
- stabilize either Product Contract;
- establish `Production` or operational readiness;
- claim full-platform conformance;
- create a Stable/public SDK, API, wire, package, registry, plugin-runtime, generated-code, service or component compatibility boundary;
- create SLA/support/customer compatibility or other commercial commitments.

Canonical Phase 5 closure evidence:

- [Canonical Roadmap](docs/roadmap/ROADMAP.md)
- [Completed Phase 5 workstream](docs/roadmap/PHASE-5-SDK-CONTRACTS-EXTENSION-EXPERIENCE.md)
- [P5.12 Phase 5 / M5 closure review](docs/reviews/P5-12-phase-5-m5-closure-review.md)
- [P5.10 Phase 5 conformance + architecture fitness matrix](docs/reviews/P5-10-phase-5-conformance-architecture-fitness-matrix.md)
- [R16 M5 Integration Hardening](docs/reviews/R16-m5-integration-hardening.md)
- [P5.11 compatibility / ADR / public-boundary hardening](docs/reviews/P5-11-compatibility-adr-refactoring-public-boundary-hardening-review.md)
- [P5.09 second materially distinct integration reuse proof](docs/reviews/P5-09-second-materially-distinct-integration-reuse-proof.md)
- [P4.08 bounded Product Contract](docs/contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)

Phase 6 is `Active`.

[P6.01 — Real product/workflow validation target selection + evidence baseline](docs/reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md) is `Complete / PASS`. The selected first real validation target is the Arvectum procurement/tender AI operator in a bounded real 44-ФЗ pre-bid workflow from accepted tender documentation to a human-reviewed client-ready decision package while external actions remain manual.

[P6.02 — First real Product Contract boundary + bounded adoption plan](docs/reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md) is `Complete / PASS`.

The first real Product Contract is [P6-02-FIRST-REAL-PRODUCT-CONTRACT.md](docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`. It declares exactly CAP-001 Document & Artifact Governance + CAP-004 Audit / Reconstruction Support at the current Provisional capability-contract baseline `1.0.0`. CAP-002 and CAP-003 are deliberately omitted from the first real slice. Procurement-specific schemas, workflow, knowledge, search/relevance, economics, risk and decision semantics remain product-owned.

External ЕИС/zakupki.gov.ru, partner tender files and supplier TKP/quote content remain externally authoritative within their scopes. Arvectum OS governs only its declared exact references/versions/provenance plus Native Product Contract/Execution/Event/review evidence. No automated external mutation or organizational commitment is admitted by the Product Contract.

[R17 — First Product Boundary Review](docs/reviews/R17-first-product-boundary-review.md) is `Complete / PASS`. The independent review confirmed that the P6.01 product evidence is unchanged; CAP-001 + CAP-004 remain the smallest sufficient exact dependency set; CAP-002/CAP-003 remain omitted; external authority and product-owned procurement semantics remain intact; Organization/security/rights/evidence behavior remains fail-closed; and the boundary introduces no durable/public/stable infrastructure or compatibility commitment.

R17 also confirms that the P6.02 adoption cap of maximum three platform-backed calibration cases is a bounded Arvectum OS validation sample, not a redefinition of the broader product-local pilot. No Product Contract version change, capability lifecycle change or new ADR/RFC/policy is required by R17.

The current canonical action is **P6.03 — First real product/workflow platform integration**. P6.03 must begin with **Stage 1 synthetic/anonymized/redacted proof** under the exact `Provisional 0.1.0` Product Contract and exact CAP-001/CAP-004 Provisional `1.0.0` provider/version evidence. Stage 1 must prove fail-closed wrong-Organization, rights/classification/purpose, dependency-version and incomplete-evidence paths plus absence of hidden private platform coupling before Stage 2 may use one real 44-ФЗ case. Stage 3 remains capped at maximum three platform-backed calibration cases before P6.04/P6.05 disposition.

P6.02/R17 do **not** promote any capability to `Active`, make the real Product Contract `Stable`, establish production/operational readiness, create a public SDK/API/wire/package/service boundary or create SLA/support/customer compatibility commitments.

Canonical Phase 6 evidence now includes:

- [Canonical Roadmap](docs/roadmap/ROADMAP.md)
- [Active Phase 6 workstream](docs/roadmap/PHASE-6-PRODUCT-DRIVEN-PLATFORM-VALIDATION.md)
- [P6.01 target + evidence baseline](docs/reviews/P6-01-real-product-workflow-validation-target-evidence-baseline.md)
- [P6.02 boundary + adoption review](docs/reviews/P6-02-first-real-product-contract-boundary-bounded-adoption-plan.md)
- [P6.02 first real Product Contract](docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md)
- [R17 First Product Boundary Review](docs/reviews/R17-first-product-boundary-review.md)

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
