# Arvectum OS Canonical Roadmap

Status: `Active`
Version: `1.3.0`
Created: `2026-08-07`
Updated: `2026-08-07`
Owner: `ООО «Арвектум»`
Task classification: `governance`

## 1. Purpose

This document is the canonical planning source for the development sequence of Arvectum OS.

It answers:

> What should Arvectum OS work on next, in what order, and what constitutes completion of the current phase?

This roadmap coordinates work. It does **not** override architectural or governance authority.

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

Detailed RFC approval/publication evidence is maintained in [`docs/rfc/README.md`](../rfc/README.md). This roadmap intentionally summarizes completed architecture milestones rather than duplicating their full governance history.

## 2. Versioning and update rules

This roadmap is versioned in Git and uses semantic versioning:

- `PATCH` — progress, status, links, wording clarifications and other non-structural updates;
- `MINOR` — sequencing, milestone scope, work-breakdown or maintenance-process changes that do not alter an Accepted architectural contract;
- `MAJOR` — restructuring of the roadmap lifecycle or planning model.

A roadmap update must never silently redefine the scope of an Accepted RFC. If an Accepted RFC must change, use the applicable architecture-governance process first, then update the roadmap.

Git history is the canonical history of roadmap revisions.

### 2.1 Identifier namespaces

Roadmap identifiers, RFC identifiers and ADR identifiers are independent namespaces.

Examples:

| Identifier | Namespace | Meaning |
|---|---|---|
| `0H` | Roadmap block | Reference implementation readiness |
| `P1.02` | Phase 1 work item | Native subject + first immutable Canonical Record version |
| `RFC-0008` | RFC | Document and Artifact Architecture |

Rules:

- roadmap work identifiers never consume RFC or ADR numbers;
- an RFC number is assigned only through RFC governance and the RFC Index;
- an ADR number is assigned only to an ADR artifact;
- a work item keeps its roadmap identifier when wording is clarified without materially changing the work;
- a materially different work item receives a new identifier;
- project chats, commits and implementation notes SHOULD use the roadmap identifier together with the task name.

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

## 5. Phase 0 — Foundation / Architecture Bootstrap

**Status:** 🟩 Complete  
**Progress:** `██████████ 100%`

### Phase 0 overview

| Block | Scope | Status | Progress |
|---|---|---:|---:|
| 🟪 `0A` | Governance baseline | 🟩 | `██████████ 100%` |
| 🟦 `0B` | Architecture language baseline | 🟩 | `██████████ 100%` |
| 🟪 `0C` | RFC-0002 — Kernel metamodel | 🟩 | `██████████ 100%` |
| 🟢 `0D` | RFC-0003 — Identity, security, privacy, sovereignty | 🟩 | `██████████ 100%` |
| 🟠 `0E` | RFC-0004 — Product Contract and extension model | 🟩 | `██████████ 100%` |
| 🔵 `0F` | RFC-0005/0006 — Governed execution, events and provenance | 🟩 | `██████████ 100%` |
| 🟣 `0G` | RFC-0007 — Memory, knowledge and learning lifecycle | 🟩 | `██████████ 100%` |
| 🟨 `0H` | Reference implementation readiness — non-RFC milestone | 🟩 | `██████████ 100%` |

Phase 0 established sufficient shared language, architecture, governance and contracts to begin bounded implementation without inventing cross-cutting architecture in code.

The readiness baseline is [`docs/implementation/REFERENCE-IMPLEMENTATION-READINESS.md`](../implementation/REFERENCE-IMPLEMENTATION-READINESS.md).

RFC-0008 — Document and Artifact Architecture — was accepted after Phase 0 readiness as a parallel architecture refinement. It does not retroactively change the Phase 0 completion boundary, but it is binding whenever shared Document/Artifact semantics are implemented.

## 6. Phase 1 — Reference Implementation

**Status:** 🟨 In progress  
**Purpose:** prove the smallest domain-neutral executable architectural spine of Arvectum OS using reversible implementation techniques before adding infrastructure.

Canonical detailed work breakdown:

- [`docs/roadmap/PHASE-1-REFERENCE-IMPLEMENTATION.md`](PHASE-1-REFERENCE-IMPLEMENTATION.md) — `Active 1.0.0`.

### Phase 1 overview

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P1.01` | Organization scope and attributable Actor / Principal | 🟩 | `██████████ 100%` |
| `P1.02` | Native subject + first immutable Canonical Record version | 🟦 | `░░░░░░░░░░ 0%` |
| `P1.03` | Versioned Workflow baseline | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.04` | Execution Context + exact version pinning | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.05` | Authorization and Organizational Authority gates | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.06` | Governed Canonical Mutation + second immutable version | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.07` | Canonical Event admission and execution linkage | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.08` | Provenance, causation and reconstruction evidence | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.09` | Observation creation without Knowledge promotion | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.10` | Portable semantic fixture export | ⬜ | `░░░░░░░░░░ 0%` |
| `P1.11` | Negative-path and architecture fitness tests | 🟨 | `█░░░░░░░░░ 10%` |
| `P1.12` | Phase 1 bounded-slice closure review | ⬜ | `░░░░░░░░░░ 0%` |

### Current implementation evidence

`P1.01` is implemented in [`reference/python`](../../reference/python/README.md) with executable fitness tests proving explicit Organization scope and attributable Actor/Principal semantics.

`P1.11` is cross-cutting and has started because `P1.01` already contributes executable negative-path/fitness coverage. The complete Phase 1 fitness matrix remains unfinished.

### Current canonical action

> **`P1.02 — Native subject + first immutable Canonical Record version`: create one `Native` canonical subject with stable Subject Identity, first immutable Version Identity, explicit Organization scope, authority mode and the minimum governed envelope required by Accepted RFC-0002 and applicable RFC-0003 constraints.**

No database or durable persistence technology is required for `P1.02`.

## 7. Phase 1 dependency-aware sequence

```text
P1.01 ✅ Organization scope + Actor / Principal
   ↓
P1.02 🟦 Native subject + Canonical Record v1
   ↓
P1.03 ⬜ Versioned Workflow
   ↓
P1.04 ⬜ Execution Context + version pinning
   ↓
P1.05 ⬜ Authorization + Organizational Authority gates
   ↓
P1.06 ⬜ Canonical Mutation → immutable v2
   ↓
P1.07 ⬜ Canonical Event
   ↓
P1.08 ⬜ Provenance / reconstruction
   ↓
P1.09 ⬜ Observation ≠ Knowledge
   ↓
P1.10 ⬜ Portable semantic fixture
   ↓
P1.12 ⬜ Closure review
```

`P1.11` fitness tests run continuously across the sequence.

Bounded parallel work is permitted when dependencies remain explicit and the work does not prejudge unresolved architecture or technology choices.

## 8. Phase 1 implementation constraints

Implementation MUST remain within the Accepted architecture and readiness boundary:

- prefer the simplest reversible solution;
- keep product-domain semantics out of shared reference modules;
- begin with in-memory persistence and in-process interfaces where sufficient;
- preserve explicit Organization, authorization, Organizational Authority and data-governance boundaries;
- require Governed Execution for consequential canonical mutation;
- preserve semantic immutability and exact version reliance;
- keep canonical Events distinct from telemetry;
- do not promote Observation to validated Knowledge automatically;
- use Accepted RFC-0008 when Document/Artifact semantics enter scope;
- do not represent working code as an `Active` Platform Capability or production-readiness evidence by itself.

## 9. ADR gate

No new ADR is required merely because Phase 1 has begun.

Create an ADR before relying on an implementation choice when the choice becomes materially constraining, including when it:

1. constrains multiple platform modules or products;
2. creates material migration cost or public-contract breakage;
3. becomes a stable cross-product/public interface;
4. materially determines tenant isolation, authorization enforcement, evidence integrity or external authority behavior;
5. creates a durable dependency on a database, broker, orchestration runtime, identity provider, schema registry, retrieval engine or vendor-specific format;
6. has materially different portability, security, reliability or operational consequences compared with plausible alternatives.

## 10. Phase 1 exit criterion

Phase 1 first bounded executable slice is complete only when:

1. `P1.01` through `P1.10` are complete within the declared slice scope;
2. the applicable `P1.11` fitness matrix passes;
3. `P1.12` closure review confirms no product-domain leakage into shared modules;
4. no technology choice crossed an ADR gate without an ADR;
5. the implementation remains reversible and migration-friendly;
6. implementation-neutral fixture export preserves required organizational semantics;
7. Roadmap status is synchronized with repository evidence.

Completion of Phase 1 does not automatically make any Platform Capability `Active`, establish operational readiness or create SLA/support/conformance claims beyond the explicitly tested scope.

## 11. Roadmap maintenance rule

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
