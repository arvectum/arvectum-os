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

`Phase 3 — Shared Platform Capabilities` is complete. `P3.12 — Phase 3 / M3 closure review` passed, and milestone `M3 — Validated shared capability baseline` is achieved for the declared bounded shared-capability reference scope.

The retained capability set remains:

- `CAP-001 — Document & Artifact Governance` — `Incubating / Provisional`;
- `CAP-002 — Memory & Knowledge Governance` — `Incubating / Provisional`;
- `CAP-003 — Search / Index Projection` — `Incubating / Provisional`, non-authoritative governed discovery/projection semantics;
- `CAP-004 — Audit / Reconstruction Support` — `Incubating / Provisional`, derived/read-oriented.

M3 closure does not promote any capability to `Active`, create a Stable Product Contract/public API, select durable infrastructure, establish operational or production readiness, or create SLA/support/full-conformance commitments. P3.11 remains the lifecycle/ADR/refactoring disposition: exactly four retained capabilities, no fifth admission, no new ADR required and no material shared refactor justified on the current evidence.

Canonical Phase 3 closure evidence:

- [Completed Phase 3 workstream and M3 state](docs/roadmap/PHASE-3-SHARED-PLATFORM-CAPABILITIES.md)
- [P3.12 Phase 3 / M3 closure review](docs/reviews/P3-12-phase-3-m3-closure-review.md)
- [Platform Capability Catalog](docs/catalogs/PLATFORM-CAPABILITY-CANDIDATE-CATALOG.md)
- [P3.10 architecture fitness matrix](docs/reviews/P3-10-phase-3-architecture-fitness-matrix.md)
- [R8 milestone hardening review](docs/reviews/R8-phase-3-milestone-hardening.md)
- [P3.11 capability admission / ADR / refactoring hardening review](docs/reviews/P3-11-capability-admission-adr-refactoring-hardening-review.md)

`Phase 4 — Workspace / Operator Experience` is **Active**. `P4.01 — Operator journeys, workspace boundary and information architecture`, `P4.02 — Organization context, identity and scoped navigation shell`, the mandatory `R9 — Workspace Boundary Review` gate, `P4.03 — Canonical Record / Relationship inspection experience`, `P4.04 — Version, Event, provenance and reconstruction experience`, `P4.05 — Governed Execution, gate and approval/action experience` and `P4.06 — Document / Artifact workspace experience` are complete with `PASS`. The current canonical action is `P4.07 — Memory / Knowledge / Search discovery experience`.

P4.02 provides the first bounded visible workspace shell: explicit Organization and attributable Actor context, `Discover / Records / Executions / Evidence / Documents / Knowledge` navigation, distinct Subject and exact-Version references, fail-closed unresolved/mismatched Organization state and non-authoritative presentation semantics. A zero-dependency static HTML demo makes the shell inspectable without selecting a frontend framework, route schema, public API/BFF, IAM/session provider or durable read-model topology.

R9 revalidated that boundary before richer record/provenance/execution surfaces expanded. It found no material blocker, no accidental stable public/frontend/IAM boundary and no reason for a new RFC, ADR, Product Contract or Platform Capability. Its source-resolution handoff requires actual governed source dereference to enforce current Organization/access semantics rather than trust presentation state or identifier syntax.

P4.03 makes Canonical Record and Typed Relationship inspection executable through an internal read-only boundary. It keeps stable Subject, exact immutable Version, Canonical Head and Effective Version distinct; preserves exact historical inspection; exposes typed Relationship direction and SubjectIdentity/VersionIdentity endpoint roles; shows authority/source, owner, Organization and lifecycle meaning; and surfaces missing/ambiguous Effective Version without silent fallback.

The P4.03 dereference path checks one current Actor/Organization/Subject authorization decision before source existence/multiplicity or exact-Version disclosure, then independently checks source-owned `OrganizationScope` instead of treating `Identity.scope` or presentation wrappers as proof of canonical membership. Relationship edges require separate current authorization and omitted edges expose no protected relationship metadata/count. The presentation remains non-authoritative, escaped and action-free.

P4.04 adds the bounded history/provenance inspection experience over existing RFC-0006 Event/provenance semantics, CAP-004 Audit/Reconstruction Support and P3.07 evidence access enforcement. Canonical Event history remains separate from raw logs/metrics/traces; Event and exact Event Version identity, type/schema, occurrence and recording/admission time, producer/initiating actor, authority/source, exact Execution linkage, related exact Version references, correlation/causation and provenance remain visible only where the governed authorized evidence carries them.

P4.04 reconstruction is explicitly derived, read-only and non-authoritative. Replay is described only as side-effect-free rebuilding of a derived projection and is not executed by the inspection surface. `Redacted / Deleted / Missing / Unavailable` evidence reduces the reconstruction claim rather than being inferred or fabricated. Source authorization plus P3.07 purpose/right/classification enforcement occur before protected exact Execution-Version existence is disclosed, preventing the inspection path from becoming a metadata oracle.

P4.04 creates no Event store, telemetry backend, replay executor, IAM/PDP/PEP, durable read model, public API/route/wire contract, Product Contract, new Platform Capability or lifecycle promotion. `Reference Python CI #132` passed all `456` tests on Python `3.12.13` on the executable P4.04 implementation branch before roadmap synchronization.

P4.05 adds the bounded Governed Execution / gate / approval-action experience over the existing RFC-0005 and P2.06 runtime semantics. The operator can inspect one stable Execution Identity at its Head or an exact historical Version, see exact Workflow/material-input/Product Contract pins where present, and inspect Authorization, Organizational Authority and Consequential Approval as separate gate decisions with exact evidence rather than one synthetic `approved` flag.

P4.05 keeps source-read access distinct from consequential authority. Unresolved or denied required gates and historical Execution Versions fail closed for action; a different read-authorized Actor cannot invoke the bounded existing Execution action merely because the Execution is visible. Action intent is immutable, transient and non-authoritative, and consequential canonical mutation is delegated only to the existing `runtime_consistency.commit_canonical_mutation` path. Keyed retry/duplicate suppression, stale/conflict state and uncertain/reconciliation meaning are exposed without publishing retry-token values or creating a second canonical-state owner.

P4.05 selects no workflow engine, decision-authority policy, IAM/PDP/PEP, durable runtime/Event store, external-effect executor, frontend framework, public route/API/wire contract or Product Contract. It creates no new Platform Capability and promotes none to `Active`. Initial implementation CI `#137` passed `472` tests on Python `3.12.13`; CI `#139` also passed after the executable static demo and smoke test were added.

P4.06 adds the bounded Document / Artifact workspace experience over existing CAP-001, RFC-0008 and P3.07 cross-capability enforcement. It keeps logical Document Subject, exact immutable Document Version, Canonical Head, Artifact, content-integrity reference, rendition role and storage locator as separate concepts. Exact historical Versions remain inspectable, while consequential Artifact reliance is available only after explicit exact Version selection and current access re-evaluation; structural exact reliance is delegated to the existing CAP-001 resolver.

Current Actor/Organization-bound Document source authorization is evaluated before protected source/version resolution. Governed Artifact metadata is then independently filtered through the existing P3.07 `AccessRequest` purpose/right/classification context. Restricted Artifact metadata is omitted without protected counts. Exact reliance rechecks both source authorization and P3.07 handling access rather than trusting stale presentation state.

Working/draft candidates are shown separately as non-canonical. Their generated/transient Artifacts are not silently promoted, and unadmitted candidate Artifact identities, handling metadata, content references and storage locators are withheld from the P4.06 surface. P4.06 exposes no admission/promotion control and does not call CAP-001 admission from the presentation layer. For permitted governed renditions, source-Artifact provenance, transformation, classification, purpose, rights and retention remain visible, while storage-locator values, content references and bytes are withheld.

The current reference Canonical Record harness implements only Native authority mode. P4.06 therefore renders the Native governed Document source when applicable and fails closed rather than fabricating external authority/source metadata from a file path, import source or storage locator. It selects no DMS, object store, OCR/signing provider, content-delivery service, frontend framework, public route/API/wire contract or durable read model. It creates no Product Contract, new Platform Capability or lifecycle promotion.

The P4.06 cross-review ran five functional iterations. One material pre-merge finding identified that Document source authorization alone was insufficient for Artifact handling constraints; the implementation was hardened to reuse P3.07 enforcement and covered with additional negative-path tests. `Reference Python CI #154` then passed all `495` tests on Python `3.12.13`.

Canonical Phase 4 planning/current evidence:

- [Canonical roadmap](docs/roadmap/ROADMAP.md)
- [Active Phase 4 workstream](docs/roadmap/PHASE-4-WORKSPACE-OPERATOR-EXPERIENCE.md)
- [P4.01 operator journeys / workspace boundary / IA review](docs/reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md)
- [P4.02 Organization context / identity / scoped navigation shell review](docs/reviews/P4-02-organization-context-identity-scoped-navigation-shell.md)
- [R9 Workspace Boundary Review](docs/reviews/R9-workspace-boundary-review.md)
- [P4.03 Canonical Record / Relationship inspection review](docs/reviews/P4-03-canonical-record-relationship-inspection-experience.md)
- [P4.04 Version / Event / provenance / reconstruction review](docs/reviews/P4-04-version-event-provenance-reconstruction-experience.md)
- [P4.05 Governed Execution / gate / approval-action review](docs/reviews/P4-05-governed-execution-gate-approval-action-experience.md)
- [P4.06 Document / Artifact workspace review](docs/reviews/P4-06-document-artifact-workspace-experience.md)

P4.01 through P4.06 and R9 establish, harden and exercise a domain-neutral workspace boundary only. They do not create a new Platform Capability, change CAP-001 through CAP-004 lifecycle, create a Stable Product Contract/public interface or establish production readiness.

RFC-0001 through RFC-0008 are `Accepted 1.0.0` and remain binding within their declared scopes.

The reference implementation remains bounded and intentionally avoids establishing a permanent programming-language contract, durable database/object-store/search topology, public API/SDK/wire format, Event broker/store, IAM provider, workflow engine, evidence-integrity technology or deployable service topology. Such choices must pass the applicable ADR/stable-boundary gates before material reliance.

Phase status, capability lifecycle, operational environment and conformance maturity remain distinct. `M3 Achieved` and Phase 4 progress do not mean any Platform Capability is lifecycle `Active` or production-ready.

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
