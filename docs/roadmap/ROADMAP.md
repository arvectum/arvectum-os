# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.0.3`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS.

It has two planning horizons:

1. **Strategic Roadmap** — approximate long-range direction across all currently envisioned phases;
2. **Active Roadmap** — detailed, evidence-backed work breakdown for the current phase.

The Strategic Roadmap is intentionally provisional beyond the active phase. It is a planning hypothesis, not an architectural contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

The roadmap coordinates work. It does **not** override architectural or governance authority.

Authority remains, in descending order:

1. the Constitution;
2. Accepted RFCs;
3. Accepted ADRs;
4. approved policies, standards and catalogs;
5. Product Contracts and approved product-specific decisions;
6. implementation and tests;
7. this roadmap as a planning artifact;
8. task materials, chats and model memory.

If this roadmap conflicts with a higher-authority source, the higher-authority source prevails and this roadmap must be corrected.

Detailed RFC approval/publication evidence is maintained in [`docs/rfc/README.md`](../rfc/README.md).

## 2. Versioning, planning horizons and update rules

This roadmap uses semantic versioning:

- `PATCH` — progress, status, links and wording clarifications;
- `MINOR` — sequencing, milestone scope, work breakdown or strategic-horizon changes that do not restructure the planning model;
- `MAJOR` — restructuring of the roadmap lifecycle or planning model.

Version `2.0.0` introduces the two-horizon planning model: Strategic Roadmap + Active Roadmap.

### 2.1 Planning confidence

Strategic phases have a confidence class:

- **Executed** — completed and evidenced in the repository;
- **Active** — current detailed delivery phase;
- **Near-term** — likely next direction, to be decomposed before execution;
- **Exploratory** — long-range planning hypothesis subject to substantial revision, combination, splitting, resequencing or removal.

A future phase MUST be revalidated against products, evidence, Accepted architecture and organizational priorities before it becomes Active.

At each phase boundary, or earlier after a material product/platform learning milestone, the strategic horizon SHOULD be reviewed and the next phase MUST be decomposed before substantive execution.

### 2.2 Identifier namespaces

Roadmap identifiers, RFC identifiers and ADR identifiers are independent namespaces.

| Identifier | Namespace | Meaning |
|---|---|---|
| `0H` | Roadmap block | Reference implementation readiness |
| `P1.05` | Phase 1 work item | Authorization and Organizational Authority gates |
| `M1` | Roadmap milestone | First executable architectural spine proven |
| `RFC-0008` | RFC | Document and Artifact Architecture |

Rules:

- roadmap work identifiers never consume RFC or ADR numbers;
- an RFC number is assigned only through RFC governance and the RFC Index;
- an ADR number is assigned only to an ADR artifact;
- a work item keeps its roadmap identifier when wording is clarified without materially changing the work;
- a materially different work item receives a new identifier;
- future-phase work item IDs are assigned when that phase is decomposed; the strategic roadmap does not prematurely freeze detailed task numbering;
- project chats, commits and implementation notes SHOULD use the roadmap identifier together with the task name.

Git history is the canonical history of roadmap revisions.

## 3. Status and progress legend

| Marker | Meaning |
|---|---|
| 🟩 | Complete / accepted / published |
| 🟨 | In progress |
| 🟦 | Ready / next planned work |
| ⬜ | Planned, not started |
| 🟥 | Blocked or conflicted |
| ⚫ | Deferred / not currently scheduled |

Progress bars are planning indicators, not conformance or capability-lifecycle claims.

`██████████ 100%` — complete  
`█████░░░░░ 50%` — partially complete  
`░░░░░░░░░░ 0%` — not started

## 4. Architecture baseline

Current verified canonical baseline:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Architecture Glossary aligned through Accepted RFC-0008;
- Phase 0 reference implementation readiness completed and owner-confirmed.

The RFC Index remains the canonical source for RFC status and acceptance evidence.

## 5. Strategic Roadmap — current long-range draft

The strategic horizon estimates the current scale of work without pretending that distant implementation details are already known.

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Active | 🟨 In progress | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Near-term | ⬜ Draft | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Exploratory | ⬜ Draft | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Exploratory | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |
| `Phase 9` | Organizational Intelligence Compounding | Exploratory | ⬜ Draft | `M9` Governed learning and organizational-intelligence loop proven at scale |

### 5.1 Phase 0 — Foundation / Architecture Bootstrap

**Intent:** establish shared semantics, governance and contracts sufficient for bounded implementation without speculative platform lock-in.

Completed scope includes Constitution/RFC governance, architecture language, Kernel metamodel, identity/security/privacy/sovereignty, Product Contract and extension semantics, Governed Execution, Event/Provenance, Memory/Knowledge, implementation readiness, plus Accepted RFC-0008 Document and Artifact Architecture.

**Milestone `M0`:** 🟩 achieved.

### 5.2 Phase 1 — Reference Implementation

**Intent:** prove that the Accepted architecture can execute as one minimal, domain-neutral, reversible slice before infrastructure is selected prematurely.

Current detailed work includes Organization/Actor attribution, Canonical Records and immutable versions, Workflow versioning, Execution Context exact-version pinning, authorization and Organizational Authority gates, governed mutation, canonical Event, provenance, Observation non-promotion, portable fixtures and architecture fitness tests.

**Milestone `M1`:** first bounded executable architectural spine passes its closure review and portability/fitness criteria.

### 5.3 Phase 2 — Core Runtime

**Provisional intent:** turn the proven Phase 1 semantics into a reusable runtime baseline without allowing the current reference harness to become permanent architecture accidentally.

Likely scope to evaluate and decompose after Phase 1:

- stable runtime boundaries for the five Kernel primitives;
- reusable Canonical Record/version and Relationship operations;
- Governed Execution lifecycle and enforcement interfaces;
- Event admission and provenance reconstruction interfaces;
- identity, authorization and Organizational Authority enforcement boundaries;
- persistence/transaction/concurrency requirements only where evidence requires them;
- runtime portability and migration fixtures;
- ADRs for technology choices that actually cross an ADR gate.

**Not assumed yet:** microservices, PostgreSQL, FastAPI, broker, policy engine, cloud topology or any specific implementation technology.

**Milestone `M2`:** more than one bounded workflow can reuse the same governed runtime semantics without copying the Phase 1 harness.

### 5.4 Phase 3 — Shared Platform Capabilities

**Provisional intent:** introduce shared capabilities only where validated reuse, universal governance or strategic necessity justifies platform admission.

Candidate areas, subject to evidence:

- governed document/artifact handling under RFC-0008;
- memory/knowledge retrieval and governed promotion support;
- search/index projections that remain non-authoritative;
- workflow support above Kernel semantics;
- notifications, scheduling or integration support where multiple products genuinely reuse them;
- audit/reconstruction/operator tooling;
- shared connector/adaptor patterns for external authorities.

Candidate items remain `Candidate`/`Incubating` until the applicable lifecycle and operational-readiness criteria are satisfied. This phase does not promise that every candidate becomes a Platform Capability.

**Milestone `M3`:** a small set of shared capabilities has demonstrated reuse and clear ownership/contracts without product-domain leakage.

### 5.5 Phase 4 — Workspace / Operator Experience

**Provisional intent:** provide a coherent human-facing operating surface over governed organizational state without turning UI concepts into Kernel semantics.

Possible scope:

- organization/workspace navigation;
- governed record and relationship views;
- execution/task/approval surfaces;
- event/history/provenance inspection;
- document/artifact interaction where required;
- knowledge/memory navigation;
- product entry points and scoped notifications;
- accessibility, localization and operator safety patterns.

**Milestone `M4`:** an authorized operator can understand and act on a bounded cross-capability workflow through a coherent governed workspace.

### 5.6 Phase 5 — SDK, Contracts and Extension Experience

**Provisional intent:** make product and extension integration repeatable without exposing unstable implementation internals as public contracts.

Possible scope:

- Product Contract tooling and validation;
- SDK/API surfaces justified by real product needs;
- extension registration and compatibility checks;
- templates/scaffolding and local test harnesses;
- contract/fixture conformance tooling;
- developer documentation and examples;
- versioning, migration and deprecation workflows.

A CLI, public SDK or plugin mechanism is not assumed until product evidence demonstrates the useful boundary.

**Milestone `M5`:** a second integration can be built through documented contracts and reusable tooling rather than copying internals.

### 5.7 Phase 6 — Product-driven Platform Validation

**Provisional intent:** validate Arvectum OS through real products, workflows and evidence rather than platform-only demonstrations.

This phase does **not** require building a fixed list of Tender/Marketing/Sales/Legal/Finance modules. Product sequencing follows business value and evidence.

Likely work:

- onboard one or more real product workflows through Provisional/approved Product Contracts;
- keep product-local experiments product-local;
- measure reuse, delivery speed, quality, governance burden and operating cost;
- identify Platform Gravity candidates from repeated product evidence;
- remove or simplify platform mechanisms that do not create value;
- promote capabilities only when lifecycle criteria are met.

**Milestone `M6`:** at least two materially useful product/workflow contexts demonstrate validated shared reuse and expose evidence for the next platform decisions.

### 5.8 Phase 7 — Operational / Enterprise Readiness

**Provisional intent:** raise scoped capabilities and environments to the reliability, security and operational maturity actually required by customers and internal operations.

Potential scope, driven by risk and commitments:

- durable tenant isolation and IAM integration;
- backup/restore and disaster-recovery requirements;
- observability and incident response;
- retention/deletion/export operations;
- secrets/key management;
- availability/scaling/performance requirements;
- deployment and upgrade safety;
- support/runbooks and operational ownership;
- scoped conformance evidence.

`Production` remains an environment designation, not a capability lifecycle state. No SLA, HA or enterprise feature is promised before its requirement and readiness are established.

**Milestone `M7`:** explicitly scoped capabilities can operate in an intended production environment with proportional controls and documented ownership.

### 5.9 Phase 8 — Ecosystem and External Integration

**Provisional intent:** enable governed interaction with external systems, developers and partners without surrendering organizational control or creating accidental public contracts.

Possible scope:

- stable external APIs where justified;
- connector/adaptor ecosystem;
- external developer tooling;
- extension/catalog distribution and trust controls;
- compatibility certification/conformance profiles;
- cross-organization sharing mechanisms under explicit rights and policy;
- portability/import/export tooling across implementations.

A marketplace is only a possible commercial/product mechanism, not an architectural requirement.

**Milestone `M8`:** external integrations/extensions can participate through explicit governed contracts with isolation, provenance, compatibility and portability controls.

### 5.10 Phase 9 — Organizational Intelligence Compounding

**Provisional intent:** demonstrate the long-term purpose of Arvectum OS: organizational intelligence that compounds safely across governed executions and validated reuse.

Possible scope:

- richer organization-specific Executable Organizational Model views;
- knowledge graph and context-resolution capabilities built from canonical Records/Relationships rather than a competing source of truth;
- governed learning loops from outcomes to Observations, Knowledge Candidates and approved improvements;
- cross-workflow impact analysis and decision support;
- simulation/planning where model validity, uncertainty and authority boundaries are explicit;
- AI-assisted optimization that proposes but does not silently acquire organizational authority;
- measurement of organizational leverage and validated reuse.

The descriptive term `Organizational Twin` remains informative as defined by Accepted RFC-0001; this roadmap does not promise a complete real-time simulation or autonomous organization.

**Milestone `M9`:** repeated governed learning demonstrably improves future organizational work while preserving authority, provenance, security, rights and portability.

## 6. Active Roadmap — Phase 1 Reference Implementation

**Status:** 🟨 In progress

Canonical detailed work breakdown:

- [`docs/roadmap/PHASE-1-REFERENCE-IMPLEMENTATION.md`](PHASE-1-REFERENCE-IMPLEMENTATION.md) — current Active Phase 1 plan.

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P1.01` | Organization scope and attributable Actor / Principal | 🟩 | `██████████ 100%` |
| `P1.02` | Native subject + first immutable Canonical Record version | 🟩 | `██████████ 100%` |
| `P1.03` | Versioned Workflow baseline | 🟩 | `██████████ 100%` |
| `P1.04` | Execution Context + exact version pinning | 🟩 | `██████████ 100%` |
| `P1.05` | Authorization and Organizational Authority gates | 🟩 | `██████████ 100%` |
| `P1.06` | Governed Canonical Mutation + second immutable version | 🟩 | `██████████ 100%` |
| `P1.07` | Canonical Event admission and execution linkage | 🟩 | `██████████ 100%` |
| `P1.08` | Provenance, causation and reconstruction evidence | 🟦 | `░░░░░░░░░░ 0%` |
| `P1.09` | Observation creation without Knowledge promotion | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.10` | Portable semantic fixture export | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `███████░░░ 70%` |
| `P1.12` | Phase 1 bounded-slice closure review | ⬜ | `░░░░░░░░░░ 0%` |

### Current implementation evidence

`P1.01` through `P1.04` remain implemented in [`reference/python`](../../reference/python/README.md) with the previously recorded `31`-test validation baseline.

`P1.05` adds separate immutable Authorization and Organizational Authority gate decisions for the exact P1.04 execution attempt. Missing/denied evidence fails closed; neither gate implies the other; two explicit scoped `Allow` decisions are required to create the next immutable `Ready` Execution Context version. The Ready version preserves predecessor lineage, exact Workflow/material-input pins and both explicit-Allow gate decision pins; no target Canonical Record mutation occurs yet. P1.05 adds `12` executable fitness tests.

`P1.06` executes the declared `CanonicalMutation` only through that exact immutable `Ready` execution. It consumes the exact Workflow/material-input and explicit-Allow gate-decision versions, creates a distinct immutable target v2 under the same Subject Identity with P1.02 v1 as predecessor, rejects stale-current conflicts instead of overwriting newer state, preserves v1 unchanged, and records the canonical effect in a new immutable terminal `Succeeded` Execution Context version. P1.06 adds `13` focused executable fitness tests and deliberately leaves canonical Event admission to P1.07.

`P1.07` now distinguishes transient Event receipt from canonical admission, admits one immutable `Native` Event linked to the exact terminal P1.06 Execution Context and resulting target v2, preserves event type/schema/source/time/actor/classification/provenance/integrity context, treats duplicate delivery idempotently, rejects conflicting Event Identity/Version Identity reuse without rewriting history, and fails closed on wrong execution/result or cross-Organization linkage. P1.07 adds `14` focused executable fitness tests and deliberately leaves broader provenance/reconstruction to P1.08.

`P1.11` is cross-cutting and now accumulates negative-path evidence through P1.07, including direct-mutation rejection, immutable-history preservation, canonical conflict detection, receipt/admission separation and duplicate/conflicting Event handling. Replay, Observation/Knowledge and projection portions remain incomplete.

### Current canonical action

> **`P1.08 — Provenance, causation and reconstruction evidence`: preserve enough version-identifiable provenance, causation and correlation to reconstruct the bounded P1.06/P1.07 operation without mutating sealed history or turning projections into authority.**

P1.08 must build on the exact immutable execution, target and Event references already produced by P1.06/P1.07, remain proportionate to the bounded scenario, and avoid pre-empting P1.09 Observation/Knowledge or P1.10 portable-fixture semantics.

## 7. Phase 1 dependency-aware sequence

```text
P1.01 ✅ Organization scope + Actor / Principal
   ↓
P1.02 ✅ Native subject + Canonical Record v1
   ↓
P1.03 ✅ Versioned Workflow
   ↓
P1.04 ✅ Execution Context + version pinning
   ↓
P1.05 ✅ Authorization + Organizational Authority gates
   ↓
P1.06 ✅ Canonical Mutation → immutable v2
   ↓
P1.07 ✅ Canonical Event
   ↓
P1.08 🟦 Provenance / reconstruction
   ↓
P1.09 ⬜ Observation ≠ Knowledge
   ↓
P1.10 ⬜ Portable semantic fixture
   ↓
P1.12 ⬜ Closure review
```

`P1.11` fitness tests run continuously across the sequence.

Bounded parallel work is permitted when dependencies remain explicit and the work does not prejudge unresolved architecture or technology choices.

## 8. Phase transition rule

Before Phase N+1 becomes Active:

1. synchronize with the canonical repository;
2. review evidence and unresolved debt from Phase N;
3. revalidate the strategic intent of Phase N+1 against the Constitution and Accepted RFCs;
4. incorporate evidence from real products/workflows where available;
5. split, merge, reorder or remove speculative scope where evidence warrants it;
6. create a detailed `PHASE-N-...` work breakdown with stable `PN.xx` identifiers;
7. identify any RFC/ADR/policy/Product Contract work actually required before implementation;
8. define scoped exit criteria and fitness evidence;
9. update this roadmap and increment its version.

The strategic phase title and milestone MAY change before activation. Distant roadmap content is deliberately easier to change than Accepted architecture.

## 9. ADR gate

No ADR is required merely because implementation work has begun.

Create an ADR before relying on an implementation choice when the choice becomes materially constraining, including when it:

1. constrains multiple platform modules or products;
2. creates material migration cost or public-contract breakage;
3. becomes a stable cross-product/public interface;
4. materially determines tenant isolation, authorization enforcement, evidence integrity or external authority behavior;
5. creates a durable dependency on a database, broker, orchestration runtime, identity provider, schema registry, retrieval engine or vendor-specific format;
6. has materially different portability, security, reliability or operational consequences compared with plausible alternatives.

P1.05 remains below this ADR gate because it does not select a durable authorization-enforcement mechanism, IAM provider, policy engine, tenant-isolation technology or production Organizational Authority administration model.

P1.06 remains below this ADR gate because its mutation boundary, exact-version checks and conflict detection are bounded, reversible, in-memory and non-public. It does not select durable persistence, a Canonical Head/effective-version resolver, concurrency/transaction technology, a public mutation interface or a durable evidence-integrity mechanism.

P1.07 remains below this ADR gate because its Event admission history is caller-supplied, immutable, in-memory and non-public. It does not select a durable Event store, broker, outbox/inbox mechanism, delivery protocol, schema registry, public Event interface or observability backend.

## 10. Roadmap maintenance rule

Every roadmap update **MUST begin with repository synchronization**, not chat-memory reconstruction.

Before changing roadmap status or progress:

1. fetch the current canonical `docs/constitution/CONSTITUTION.md`;
2. fetch `docs/rfc/README.md` and determine the actual status/version of every relevant RFC;
3. inspect relevant Accepted RFC/ADR/decision records for the milestone being updated;
4. fetch the current `docs/roadmap/ROADMAP.md` and applicable phase work-breakdown file;
5. inspect implementation/tests for any work item whose progress is changing;
6. reconcile repository state with project-chat context; repository state remains authoritative unless a current governance repair is explicitly being recorded.

After every accepted RFC, material planning decision or meaningful implementation milestone:

1. update status and progress in this file and the applicable phase work breakdown;
2. update links and dependencies;
3. increment versions according to their versioning rules;
4. commit the update to the canonical repository;
5. do not maintain a competing roadmap in chat, local notes or another repository.

Chats may discuss future roadmap changes, but only committed roadmap artifacts are canonical.