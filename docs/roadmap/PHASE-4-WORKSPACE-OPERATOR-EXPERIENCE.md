# Arvectum OS Phase 4 — Workspace / Operator Experience

Status: `Active`
Version: `1.2.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M4 — Coherent governed workspace baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 3 — Shared Platform Capabilities`, `M3` achieved

## Version note

Version `1.2.0` completes `P4.02 — Organization context, identity and scoped navigation shell` and advances the current canonical action to the mandatory `R9 — Workspace Boundary Review` engineering gate.

P4.02 makes the P4.01 workspace boundary executable through a bounded zero-dependency internal shell with explicit Organization and attributable Actor context, domain-neutral navigation, Subject-versus-exact-Version reference semantics, fail-closed unresolved/mismatched scope, non-authoritative presentation state and an inert standalone HTML demo. It selects no frontend/API/IAM/durable-read-model technology, creates no new Platform Capability and changes no capability lifecycle.

Canonical completion evidence:

- [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- GitHub Actions `Reference Python CI #109` — `PASS` on the P4.02 implementation branch before roadmap synchronization.

## 1. Purpose

Phase 4 proves that a human operator can understand, inspect and perform bounded governed work through one coherent workspace over the already established Core Runtime and Incubating shared capabilities.

The phase is intentionally **operator-experience first, UI-technology neutral**. It does not select a frontend framework, browser/mobile architecture, BFF/API topology, design system vendor, notification infrastructure or public API merely because a visible workspace is now required.

The workspace is a projection and interaction surface over governed organizational state. It MUST NOT become an independent source of canonical truth, bypass authorization or Organizational Authority, silently mutate canonical state, infer lifecycle `Active`, or hide provenance/version scope where those are material to consequential work.

Phase 4 is also the first phase where Arvectum OS should become visibly understandable as a working operating environment rather than only an executable semantic/runtime foundation.

## 2. Boundary revalidation result

M3 evidence justifies a bounded Phase 4 because:

1. Core Runtime and four shared capability slices have executable governed semantics;
2. operators now need a coherent way to inspect canonical state, history, provenance, documents, knowledge/search projections and governed executions;
3. the workspace can validate whether the platform abstractions are understandable and usable without adding product-domain semantics;
4. real product entry points can later rely on a shared operator shell through Product Contracts rather than each product rebuilding platform inspection/governance UI;
5. the phase can remain reversible by using internal/adaptor-backed presentation boundaries and avoiding premature public API or frontend technology commitments.

The workspace remains a platform interaction capability under development. Activation of this roadmap phase does not make a Workspace Platform Capability `Active` under RFC-0001 lifecycle rules.

## 3. Phase 4 work breakdown

| ID | Work item | Status | Progress |
|---|---|---:|---:|
| `P4.01` | Operator journeys, workspace boundary and information architecture | 🟩 Complete | `██████████ 100%` |
| `P4.02` | Organization context, identity and scoped navigation shell | 🟩 Complete | `██████████ 100%` |
| `P4.03` | Canonical Record / Relationship inspection experience | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.04` | Version, Event, provenance and reconstruction experience | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.05` | Governed Execution, gate and approval/action experience | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.06` | Document / Artifact workspace experience | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.07` | Memory / Knowledge / Search discovery experience | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.08` | Cross-capability task/context composition + bounded product entry point | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.09` | Security, rights, minimization and authority-safe UX | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.10` | Workspace architecture fitness + accessibility/usability baseline | ⬜ cross-cutting | `░░░░░░░░░░ 0%` |
| `P4.11` | Workspace hardening / ADR / refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.12` | Phase 4 / M4 closure review | ⬜ | `░░░░░░░░░░ 0%` |

## 4. Detailed task intent

### P4.01 — Operator journeys, workspace boundary and information architecture

Define the smallest domain-neutral operator journeys that Phase 4 must support and the information architecture that exposes existing governed semantics without inventing new authority.

Required outputs:

- bounded operator personas/roles for the reference scope, expressed through existing identity/authorization semantics rather than product job titles;
- primary journeys such as inspect governed object, trace history/provenance, inspect execution/gates, locate document/knowledge context, and initiate a permitted governed action;
- explicit workspace boundary versus product-owned UX;
- navigation/information architecture hypothesis;
- presentation/read-model inventory and authority classification;
- explicit list of UX states that must fail closed or show uncertainty/insufficient authority.

Exit criterion: the operator journeys cover the minimum M4 proof and do not introduce product-domain business behavior or a competing canonical state model.

Completion evidence: [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`, four functional cross-review iterations.

### P4.02 — Organization context, identity and scoped navigation shell

Implement the minimal workspace shell that always makes Organization scope and attributable operator identity visible and preserved across navigation.

Required behavior:

- explicit current Organization scope;
- attributable Actor/Principal context where relevant;
- no cross-Organization context leakage;
- fail-closed handling of unresolved scope;
- domain-neutral navigation to the exercised governed surfaces;
- presentation state remains non-authoritative.

No SSO/IAM vendor choice is implied.

Completion evidence: [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`, four functional cross-review iterations and green full reference CI.

### P4.03 — Canonical Record / Relationship inspection experience

Provide operator inspection of governed objects and their graph context.

Required behavior:

- stable Subject Identity and exact Version Identity visibility where material;
- Head versus Effective Version distinction;
- authority mode / authoritative source visibility;
- typed relationship direction and endpoint-role visibility;
- lifecycle/validation state and owner/scope visibility;
- immutable historical versions remain inspectable;
- ambiguity or missing effective version is surfaced rather than silently resolved.

### P4.04 — Version, Event, provenance and reconstruction experience

Expose why and how consequential state exists.

Required behavior:

- Event history separated from raw telemetry;
- causation/correlation where available;
- execution linkage and exact relied-upon versions;
- provenance chain inspection;
- reconstruction/replay explicitly labeled derived/non-authoritative;
- uncertainty, missing evidence or lawful deletion gaps shown honestly;
- no UI reconstruction becomes a source of truth.

### P4.05 — Governed Execution, gate and approval/action experience

Provide a bounded operator surface for consequential work through Governed Execution.

Required behavior:

- action intent is distinct from committed canonical mutation;
- exact Workflow/material input/Product Contract versions visible where material;
- Authorization and Organizational Authority shown as distinct gates;
- approval requirements shown without inferring authority from UI role/title;
- unresolved required gates fail closed;
- retry/idempotency/conflict/uncertainty states are understandable;
- consequential mutation occurs only through existing governed runtime paths.

### P4.06 — Document / Artifact workspace experience

Exercise CAP-001 and RFC-0008 through operator interaction.

Required behavior:

- logical Document identity separated from rendition/file/storage locator;
- exact Document Version and material Artifact identity visible when relied upon;
- working/draft candidates distinguished from canonical admitted versions;
- authority mode and external source where applicable;
- derivation provenance for transformed artifacts;
- classification/rights/retention constraints respected in presentation/actions;
- generated/transient artifacts are not silently promoted.

This task does not select a DMS, object store, OCR or signing provider.

### P4.07 — Memory / Knowledge / Search discovery experience

Exercise CAP-002 and CAP-003 without conflating retrieval with authority.

Required behavior:

- Observation, Memory, Knowledge Candidate and validated Knowledge remain distinguishable;
- exact Knowledge version shown for consequential reliance;
- search/index/RAG-like results labeled as derived discovery/projection where applicable;
- freshness, scope, provenance and known uncertainty visible where material;
- purpose/classification/rights/minimization controls enforced at retrieval/presentation boundaries;
- search ranking does not imply truth or authority;
- no automatic Knowledge promotion from operator browsing or AI output.

### P4.08 — Cross-capability task/context composition + bounded product entry point

Prove that one operator flow can compose multiple platform capabilities coherently while preserving product/platform boundaries.

Reference proof should include at least one bounded Product Contract-backed product entry point that:

- enters the shared workspace with explicit Organization/product context;
- consumes at least two relevant shared capability surfaces;
- does not reach into private platform implementation state;
- preserves exact version/authority/provenance semantics;
- returns product-domain decisions/behavior to the product boundary;
- demonstrates that shared workspace navigation does not become a generic product orchestrator.

The Product Contract remains Provisional unless separately promoted through RFC-0004 governance.

### P4.09 — Security, rights, minimization and authority-safe UX

Harden the human interaction surface so governance semantics are not technically correct but operationally misleading.

Required checks:

- unauthorized or wrong-Organization content is not exposed through navigation, search, counts, previews or metadata leakage;
- hidden actions cannot be invoked through alternate client state;
- UI labels do not imply approval/authority that the runtime has not established;
- sensitive content follows classification/purpose/minimization rules;
- derived previews/summaries cannot bypass source access rules;
- expired/revoked/stale authority or knowledge is represented correctly;
- audit-sensitive operator actions remain attributable.

### P4.10 — Workspace architecture fitness + accessibility/usability baseline

Cross-cutting executable and review evidence accumulated through the phase.

Minimum matrix dimensions:

1. Organization isolation;
2. identity attribution;
3. authorization versus Organizational Authority separation;
4. canonical-versus-derived state distinction;
5. exact-version visibility/reliance;
6. provenance/reconstruction honesty;
7. Product Contract boundary integrity;
8. document/artifact authority semantics;
9. knowledge/search non-authority;
10. fail-closed action paths;
11. product-domain neutrality of shared workspace;
12. accessibility baseline for core operator journeys;
13. deterministic testability of critical operator states;
14. portability/reversibility of presentation boundaries.

Usability evidence SHOULD verify that an operator can identify what object/version they are viewing, where its authority comes from, what action is being requested, and why an action is allowed, blocked or awaiting approval.

### P4.11 — Workspace hardening / ADR / refactoring review

Before M4 closure:

- review presentation-domain boundaries and remove accidental product/domain leakage;
- refactor only where repeated workspace evidence supports a shared abstraction;
- inspect authorization/authority bypass surfaces;
- inspect derived-state caching/read-model authority risks;
- inspect API/serialization/frontend/BFF choices for ADR triggers;
- inspect accessibility/usability failures that could create material operator error;
- record any durable infrastructure or stable-interface decision that now crosses an ADR gate;
- avoid performance optimization without reproducible evidence.

### P4.12 — Phase 4 / M4 closure review

Canonical closure review proving or rejecting M4 within the bounded declared scope.

The closure review MUST distinguish:

- roadmap completion;
- any capability lifecycle state;
- operational environment/readiness;
- Product Contract stability;
- conformance scope;
- public compatibility/SLA/support claims.

## 5. Engineering / quality gates

| Gate | Trigger | Purpose |
|---|---|---|
| `R9 — Workspace Boundary Review` | after P4.02 | confirm shell/navigation does not create authority, product leakage or accidental public boundary |
| `R10 — Operator Safety / Cross-Capability Health Review` | after P4.07 | review security, rights, derived-state honesty, repeated UX patterns and code health |
| `R11 — Composition / Usability Refactoring Review` | after P4.08 / meaningful usability evidence | allow evidence-backed shared UX refactoring only after real composition is demonstrated |
| `R12 — M4 Workspace Hardening` | after P4.10 | final dependency, authority-bypass, accessibility, deterministic-state and ADR-gate hardening |

Engineering gates are review/hardening gates and do not inflate roadmap completion percentages as separate equal-weight product tasks.

## 6. Dependency-aware sequence

```text
M3 ✅ Shared Capability baseline
        ↓
P4.01 Operator journeys + IA ✅
        ↓
P4.02 Organization/identity navigation shell ✅
        ↓
R9 Workspace Boundary Review ← current
        ↓
 ┌──────┼───────────────┐
 ↓      ↓               ↓
P4.03  P4.04           P4.05
Records Provenance     Execution
 └──────┼───────────────┘
        ↓
 ┌──────┴──────┐
 ↓             ↓
P4.06         P4.07
Docs          Knowledge/Search
 └──────┬──────┘
        ↓
R10 Cross-Capability Health
        ↓
P4.08 Product-backed composition proof
        ↓
R11 Composition/Usability Refactoring
        ↓
P4.09 Security / rights / authority-safe UX
        ↓
P4.10 Fitness + accessibility/usability evidence
        ↓
R12 M4 Hardening
        ↓
P4.11 ADR / boundary / refactoring review
        ↓
P4.12 Closure review
        ↓
M4
```

P4.10 accumulates evidence throughout the phase rather than beginning only near closure.

## 7. M4 exit criteria

M4 is achieved only when all of the following hold within the declared bounded reference scope:

1. a coherent domain-neutral workspace exists over governed platform state;
2. Organization scope and operator identity are explicit and preserved;
3. an operator can inspect Canonical Records, immutable versions and Typed Relationships without losing authority/version meaning;
4. Event/provenance/reconstruction history is understandable and derived reconstruction remains non-authoritative;
5. consequential operator actions flow through Governed Execution with distinct Authorization and Organizational Authority gates;
6. Document/Artifact and Memory/Knowledge/Search capability slices are usable without collapsing their Accepted semantic distinctions;
7. at least one Product Contract-backed bounded product entry point composes shared workspace surfaces without private platform coupling;
8. cross-capability security, rights, minimization and Organization isolation pass fitness tests;
9. core operator journeys meet the declared accessibility/usability baseline;
10. presentation/read-model/cache state cannot become independent canonical authority;
11. all crossed ADR gates, if any, have canonical dispositions;
12. R9–R12 are complete and material findings are resolved or explicitly bounded;
13. P4.12 closure review passes and records M4 achieved.

## 8. Explicit non-goals

Phase 4 does not require or promise:

- a polished commercial design system or final brand UI;
- complete product UX for Tender, Marketing, Sales or any other domain;
- mobile applications;
- marketplace or extension UI;
- production IAM/SSO;
- notifications infrastructure;
- a stable public REST/GraphQL/gRPC API;
- a stable public frontend SDK;
- a specific frontend framework;
- microfrontends or microservices;
- durable cache/search/index infrastructure;
- production HA/SLA/support;
- lifecycle `Active` promotion of CAP-001 through CAP-004;
- full RFC-0001–RFC-0008 conformance.

## 9. ADR gate

Re-open the ADR gate before material reliance on a concrete choice that becomes durable or externally constraining, including:

- frontend/runtime framework as a stable cross-product boundary;
- BFF/API topology or stable wire/serialization contract;
- authentication/session/IAM enforcement mechanism;
- durable workspace/read-model/cache storage;
- search/index technology relied upon beyond replaceable projection semantics;
- document/object storage topology;
- stable design-system/package compatibility boundary;
- separately deployable UI/API service topology.

A reversible internal reference implementation may proceed without an ADR when these thresholds are not crossed.

## 10. Current canonical action

> **`R9 — Workspace Boundary Review`.**

Review the combined P4.01 + P4.02 workspace boundary before expanding into P4.03–P4.05. Confirm that Organization/Actor scope remains explicit and fail-closed, navigation/presentation state cannot create authority, Subject/exact-Version semantics remain intact, product-entry context has not become hidden product/platform coupling, and the zero-dependency reference adapter has not accidentally stabilized a frontend/API/route/IAM boundary. Resolve material findings before beginning the next workspace surface work.