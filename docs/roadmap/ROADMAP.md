# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `2.3.0`
Created: `2026-08-07`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS.

It has two planning horizons:

1. **Strategic Roadmap** — approximate long-range direction across all currently envisioned phases;
2. **Active planning horizon** — detailed, evidence-backed work breakdown for the current execution phase.

The Strategic Roadmap is intentionally provisional beyond the completed/current phase. It is a planning hypothesis, not an architectural contract, delivery promise, capability-lifecycle claim, SLA or commitment to build every listed item.

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

The approved engineering-quality gate decision is [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md).

## 2. Versioning, planning horizons and identifiers

This roadmap uses semantic versioning:

- `PATCH` — progress, status, links and wording clarifications within the current sequencing model;
- `MINOR` — sequencing, milestone scope, work breakdown, phase transition or strategic-horizon changes that do not restructure the planning model;
- `MAJOR` — restructuring of the roadmap lifecycle or planning model.

Version `2.0.0` introduced the two-horizon planning model. Version `2.1.0` recorded Phase 1 / `M1` completion and Phase 2 decomposition as the next action. Version `2.2.0` activates the decomposed Phase 2 Core Runtime plan. Version `2.2.1` records P2.01 completion and advances the active execution sequence to P2.02. Version `2.3.0` establishes evidence-backed engineering quality/refactoring gates, inserts R1 after completed P2.01 before substantive P2.02 work, and defines milestone/stable-boundary Code Health Gate rules.

Roadmap identifiers, engineering-gate identifiers, RFC identifiers and ADR identifiers are independent namespaces.

| Identifier | Namespace | Meaning |
|---|---|---|
| `0H` | Roadmap block | Reference implementation readiness |
| `P1.12` | Phase 1 work item | Phase 1 bounded-slice closure review |
| `P2.01` | Phase 2 work item | Runtime boundary extraction and reusable composition baseline |
| `R1` | Engineering gate | Phase 2 Structural Review checkpoint |
| `M2` | Roadmap milestone | Reusable governed runtime baseline |
| `RFC-0008` | RFC | Document and Artifact Architecture |

Rules:

- roadmap work identifiers never consume RFC or ADR numbers;
- engineering-gate identifiers are checkpoints and do not consume roadmap work-item, RFC, ADR or capability identifiers;
- an RFC number is assigned only through RFC governance and the RFC Index;
- an ADR number is assigned only to an ADR artifact;
- a work item keeps its roadmap identifier when wording is clarified without materially changing the work;
- a materially different work item receives a new identifier;
- project chats, commits and implementation notes SHOULD use the roadmap identifier or engineering-gate identifier together with the task/gate name.

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

## 4. Architecture and delivery baseline

Current verified canonical baseline:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- Architecture Glossary aligned through Accepted RFC-0008;
- Phase 0 reference implementation readiness completed and owner-confirmed;
- Phase 1 bounded executable reference slice completed through `P1.12`;
- Phase 1 final executable evidence: `128` tests passed in GitHub Actions for the final P1 code head;
- [`P1.12 closure review`](../reviews/P1-12-phase-1-bounded-slice-closure-review.md) records `PASS — M1 achieved for the declared bounded reference scope`;
- Phase 2 `P2.01` completed a provisional reusable runtime composition boundary while keeping deterministic reference-scenario fixtures outside runtime orchestration ownership;
- P2.01 executable evidence: GitHub Actions `Reference Python CI` run `#18` passed `138` tests on executable code head `5f56f0bf36e58efe5249b93e9df6ca4437d5621e`;
- [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md) is `Approved` and makes `R1 — Structural Review` the current required engineering gate after P2.01 and before substantive P2.02 implementation;
- no relevant Accepted ADR currently constrains the bounded runtime choices carried from Phase 1 or introduced by P2.01.

The RFC Index remains the canonical source for RFC status and acceptance evidence.

## 5. Strategic Roadmap — current long-range draft

| Phase | Strategic scope | Confidence | Status | Milestone |
|---|---|---|---|---|
| `Phase 0` | Foundation / Architecture Bootstrap | Executed | 🟩 Complete | `M0` Architecture baseline established |
| `Phase 1` | Reference Implementation | Executed | 🟩 Complete | `M1` First executable architectural spine proven |
| `Phase 2` | Core Runtime | Active | 🟨 In progress | `M2` Reusable governed runtime baseline |
| `Phase 3` | Shared Platform Capabilities | Near-term | ⬜ Draft | `M3` Validated shared capability baseline |
| `Phase 4` | Workspace / Operator Experience | Exploratory | ⬜ Draft | `M4` Coherent governed workspace baseline |
| `Phase 5` | SDK, Contracts and Extension Experience | Exploratory | ⬜ Draft | `M5` Repeatable product/extension integration |
| `Phase 6` | Product-driven Platform Validation | Exploratory | ⬜ Draft | `M6` Platform validated through real products and reuse evidence |
| `Phase 7` | Operational / Enterprise Readiness | Exploratory | ⬜ Draft | `M7` Scoped production-grade operating baseline |
| `Phase 8` | Ecosystem and External Integration | Exploratory | ⬜ Draft | `M8` Governed external ecosystem baseline |
| `Phase 9` | Organizational Intelligence Compounding | Exploratory | ⬜ Draft | `M9` Governed learning and organizational-intelligence loop proven at scale |

### Phase 0 — Foundation / Architecture Bootstrap

**Status:** 🟩 Complete — `M0 achieved`.

Established the Constitution/RFC governance baseline, architecture language, Kernel metamodel, identity/security/privacy/sovereignty, Product Contract and extension semantics, Governed Execution, Event/Provenance, Memory/Knowledge, implementation readiness and Accepted RFC-0008 Document/Artifact Architecture.

### Phase 1 — Reference Implementation

**Status:** 🟩 Complete — `M1 achieved`.

The bounded reference slice proved Organization/Actor attribution, immutable Canonical Record versions, Workflow versioning, Execution Context exact-version pinning, separate authorization and Organizational Authority gates, governed mutation, canonical Event admission, provenance/reconstruction, Observation non-promotion, portability fixtures, projection/replay safety and architecture fitness evidence.

Canonical completion records:

- [`PHASE-1-REFERENCE-IMPLEMENTATION.md`](PHASE-1-REFERENCE-IMPLEMENTATION.md);
- [`P1.12 closure review`](../reviews/P1-12-phase-1-bounded-slice-closure-review.md).

M1 intentionally did **not** claim reusable Typed Relationship lifecycle, reusable Canonical Head/Effective Version resolution, Product Contract runtime validation for a real Product, durable persistence/concurrency, full Memory/Knowledge lifecycle, production portability, operational readiness or full RFC conformance. These limits inform Phase 2.

### Phase 2 — Core Runtime

**Status:** 🟨 Active.

**Intent:** turn the proven Phase 1 semantics into a reusable, domain-neutral Core Runtime without allowing the P1 harness or provisional technology choices to become accidental permanent architecture.

Canonical detailed work breakdown:

- [`PHASE-2-CORE-RUNTIME.md`](PHASE-2-CORE-RUNTIME.md) — `Active 1.1.0`.

**Milestone `M2`:** more than one materially distinct bounded workflow reuses the same governed runtime semantics without copying the Phase 1 harness, with architecture fitness evidence, completed Phase 2 engineering quality gates and all crossed ADR gates governed.

**Not assumed:** microservices, PostgreSQL, FastAPI, broker, policy engine, IAM provider, workflow engine, cloud topology or any other specific technology.

### Phase 3 — Shared Platform Capabilities

**Confidence:** Near-term, not decomposed.

Provisional intent: admit shared capabilities only where validated reuse, universal governance or strategic necessity justifies platform admission. Candidate areas may include governed document/artifact handling, memory/knowledge retrieval/promotion support, non-authoritative search/index projections, workflow support, audit/reconstruction/operator tooling and shared connector/adaptor patterns.

Candidate items do not become `Active` merely because code exists.

### Phase 4 — Workspace / Operator Experience

**Confidence:** Exploratory.

Provisional intent: coherent human-facing operating surfaces over governed organizational state, including navigation, record/relationship views, execution/approval surfaces, history/provenance inspection, document/artifact interaction, knowledge/memory navigation and product entry points where evidence requires them.

### Phase 5 — SDK, Contracts and Extension Experience

**Confidence:** Exploratory.

Provisional intent: make product/extension integration repeatable through explicit contracts and evidence-backed tooling rather than unstable internal coupling. Possible scope includes Product Contract tooling, SDK/API surfaces, extension registration, compatibility checks, scaffolding, conformance fixtures, documentation, migration and deprecation workflows.

### Phase 6 — Product-driven Platform Validation

**Confidence:** Exploratory.

Provisional intent: validate platform value and reuse through real products/workflows. Product sequencing follows business value and evidence; the roadmap does not pre-commit Tender/Marketing/Sales/Legal/Finance as a fixed implementation sequence.

### Phase 7 — Operational / Enterprise Readiness

**Confidence:** Exploratory.

Provisional intent: raise explicitly scoped capabilities/environments to the reliability, security and operational maturity actually required. Possible concerns include durable isolation/IAM integration, backup/restore, incident response, retention/deletion/export, secrets, availability/scaling, deployment safety, runbooks and scoped conformance evidence.

`Production` is an environment, not a capability lifecycle state.

### Phase 8 — Ecosystem and External Integration

**Confidence:** Exploratory.

Provisional intent: governed external APIs/integrations/extensions with explicit isolation, provenance, compatibility, rights and portability controls. A marketplace is a possible commercial mechanism, not an architectural requirement.

### Phase 9 — Organizational Intelligence Compounding

**Confidence:** Exploratory.

Provisional intent: demonstrate safe compounding organizational intelligence through richer Executable Organizational Model views, context resolution, governed learning loops, impact analysis, decision support, bounded simulation/planning and AI-assisted optimization without transferring organizational authority to AI.

`Organizational Twin` remains an informative descriptive term, not a promise of complete real-time simulation or autonomous management.

## 6. Active Roadmap — Phase 2 Core Runtime

**Status:** 🟨 In progress  
**Phase progress:** `█░░░░░░░░░ 8%` — P2.01 complete; R1 current; P2.02 follows R1

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P2.01` | Runtime boundary extraction and reusable composition baseline | 🟩 | `██████████ 100%` |
| `P2.02` | Canonical Record lineage, Head and Effective Version runtime | 🟦 | `░░░░░░░░░░ 0%` |
| `P2.03` | Typed Relationship runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.04` | Governed Execution lifecycle and gate orchestration runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.05` | Event admission, provenance and reconstruction runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.06` | Runtime consistency, idempotency and conflict semantics | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.07` | Product Contract runtime validation boundary | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.08` | Portability, replay and non-authoritative projection runtime | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.09` | Second bounded workflow reuse proof | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.10` | Core Runtime architecture fitness matrix | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.11` | ADR-gate and runtime-boundary hardening review | ⬜ | `░░░░░░░░░░ 0%` |
| `P2.12` | Phase 2 / M2 closure review | ⬜ | `░░░░░░░░░░ 0%` |

### Phase 2 engineering gates

| Gate | Trigger | Status |
|---|---|---:|
| `R1 — Structural Review` | after P2.01, before substantive P2.02 | 🟦 Current |
| `R2 — Runtime Health Review` | after P2.06, before substantive P2.07 | ⬜ Planned |
| `R3 — Reuse Refactoring Review` | after P2.09, before final Phase 2 hardening | ⬜ Planned |
| `R4 — Milestone Hardening` | after final applicable P2.10 evidence, before P2.11/P2.12 | ⬜ Planned |

Engineering gates are checkpoints rather than `P2.xx` work items and therefore do not change the numerical Phase progress calculation by themselves.

### Current canonical action

> **`R1 — Structural Review`.**

Review the completed P2.01 extraction before substantive P2.02 implementation. Validate runtime/fixture/test boundaries, dependency direction, duplication and accidental internal APIs; remove obsolete P1-specific structure where justified; preserve behavior through the existing test/fitness suite; do not introduce materially constraining technology merely to clean up package structure.

After R1 completes with material findings resolved or explicitly dispositioned, proceed to `P2.02 — Canonical Record lineage, Head and Effective Version runtime`.

### Dependency-aware sequence

```text
P2.01 Runtime boundary extraction
          ↓
R1 Structural Review
          ↓
P2.02 Canonical Record Head / Effective Version runtime
   ├──────────────┐
   ↓              ↓
P2.03 Relationships     P2.04 Governed Execution runtime
   │              │
   └──────┬───────┘
          ↓
P2.05 Event / provenance runtime
          ↓
P2.06 Consistency / idempotency / conflict semantics
          ↓
R2 Runtime Health Review
          ↓
P2.07 Product Contract runtime boundary
          ↓
P2.08 Portability / replay / projection runtime
          ↓
P2.09 Second workflow reuse proof
          ↓
R3 Reuse Refactoring Review
          ↓
P2.10 final applicable fitness evidence
          ↓
R4 Milestone Hardening
          ↓
P2.11 ADR / boundary review
          ↓
P2.12 Closure review
```

`P2.10` architecture fitness tests run continuously across the phase; the sequence marks only the final applicable fitness evidence used by R4.

## 7. Engineering quality and refactoring rule

Arvectum OS uses evidence-backed engineering review gates rather than a calendar-based full-codebase refactoring cadence.

Canonical decision: [`DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES`](../governance/decisions/DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md).

### Continuous hygiene

Normal local engineering hygiene SHOULD occur continuously in bounded implementation work and pull requests. Naming, local duplication, typing, tests, dead code, obvious complexity and regressions do not need to wait for a milestone gate when they can be corrected proportionately without broadening scope.

A full-codebase review is not required after every roadmap work item.

### Milestone Code Health Gate

Every milestone `Mx` MUST include a proportionate Code Health Gate before closure.

The gate reviews the code and contracts materially accumulated or changed by that milestone. It SHOULD cover architecture/dependency boundaries, product/platform leakage, correctness/invariants, security/privacy/isolation/authority, maintainability, tests/fitness evidence, migration/reversibility, measured performance where relevant, and crossed governance/ADR/Product Contract gates.

This rule does not require maximum-depth review of unrelated stable code merely because a milestone is closing.

### Stable-boundary gate

Independently of milestone timing, a focused engineering review is required before an implementation boundary becomes materially expensive to change, including where applicable before reliance on a `Stable` Product Contract, stable public/cross-product API or SDK, durable cross-module schema/serialization contract, materially constraining shared persistence/runtime dependency, `Active` Platform Capability transition or material external production reliance.

The review itself does not authorize lifecycle promotion, production readiness, conformance or commercial commitments.

### Performance optimization

Performance optimization SHOULD be evidence-backed: establish a benchmark/profile or other reproducible evidence, identify a material bottleneck, optimize while preserving invariants, and rerun measurement plus regression/fitness tests. Obvious algorithmic, resource-exhaustion, correctness or security defects may be corrected immediately without waiting for formal profiling.

Engineering gates do not replace the ADR gate. If a gate discovers a materially constraining implementation choice, the applicable ADR must precede further material reliance.

## 8. Phase transition rule

Before Phase N+1 becomes Active:

1. synchronize with the canonical repository;
2. review evidence and unresolved debt from Phase N;
3. complete the applicable milestone Code Health Gate and resolve or explicitly disposition material findings;
4. revalidate the strategic intent of Phase N+1 against the Constitution and Accepted RFCs;
5. incorporate evidence from real products/workflows where available;
6. split, merge, reorder or remove speculative scope where evidence warrants it;
7. create a detailed `PHASE-N-...` work breakdown with stable `PN.xx` identifiers;
8. identify any RFC/ADR/policy/Product Contract work actually required before implementation;
9. define scoped exit criteria and fitness evidence;
10. update this roadmap and increment its version.

## 9. ADR gate

No ADR is required merely because Phase 2 has begun or because an engineering quality gate is performed.

Create an ADR before relying on an implementation choice when the choice becomes materially constraining, including when it:

1. constrains multiple platform modules or products;
2. creates material migration cost or public-contract breakage;
3. becomes a stable cross-product/public interface;
4. materially determines tenant isolation, authorization enforcement, evidence integrity or external authority behavior;
5. creates a durable dependency on a database, broker, orchestration runtime, identity provider, schema registry, retrieval engine or vendor-specific format;
6. has materially different portability, security, reliability or operational consequences compared with plausible alternatives.

Phase 2 is expected to be the first phase in which one or more ADR gates may realistically be crossed. No technology is pre-approved by this roadmap.

## 10. Roadmap maintenance rule

Every roadmap update **MUST begin with repository synchronization**, not chat-memory reconstruction.

Before changing roadmap status or progress:

1. fetch the current canonical `docs/constitution/CONSTITUTION.md`;
2. fetch `docs/rfc/README.md` and determine the actual status/version of every relevant RFC;
3. inspect relevant Accepted RFC/ADR/decision records for the milestone being updated;
4. fetch the current `docs/roadmap/ROADMAP.md` and applicable phase work-breakdown file;
5. inspect implementation/tests for any work item or engineering gate whose progress/status is changing;
6. reconcile repository state with project-chat context; repository state remains authoritative unless a current governance repair is explicitly being recorded.

After every accepted RFC, material planning decision, meaningful implementation milestone or engineering gate:

1. update status and progress in this file and the applicable phase work breakdown where relevant;
2. update links and dependencies;
3. increment versions according to their versioning rules;
4. commit the update to the canonical repository;
5. do not maintain a competing roadmap in chat, local notes or another repository.

Chats may discuss future roadmap changes, but only committed roadmap artifacts are canonical.
