# Arvectum OS Phase 4 — Workspace / Operator Experience

Status: `Active`
Version: `1.13.0`
Created: `2026-08-08`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Milestone: `M4 — Coherent governed workspace baseline`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Predecessor: `Phase 3 — Shared Platform Capabilities`, `M3` achieved

## Version note

Version `1.13.0` records completion of **P4.10 — Workspace architecture fitness + accessibility/usability baseline** with `PASS` and advances the current canonical action to **R12 — M4 Workspace Hardening**.

P4.10 evaluates the accumulated P4.02–P4.09 workspace against the complete 14-dimension M4 fitness matrix. Organization isolation, identity attribution, Authorization-versus-Organizational-Authority separation, canonical-versus-derived state, exact-version visibility/reliance, provenance honesty, Product Contract integrity, Document/Artifact authority, Knowledge/Search non-authority, fail-closed actions, product-domain neutrality, bounded accessibility, deterministic critical states and presentation reversibility all pass for the declared internal reference scope.

The bounded accessibility/usability baseline requires textual Organization/Actor/reference/status meaning, explicit blocked-state reasons, programmatic current-navigation/alert semantics, escaped governed text, exact Version/authority/gate visibility and authority-safe action labels. It is not represented as formal WCAG conformance, production UX certification or completed end-user validation.

P4.10 adds `reference/python/tests/test_p4_10_workspace_architecture_fitness_accessibility_usability.py` as cross-cutting executable regression evidence. Missing, denied, ambiguous and wrong-Organization source-access evidence remain minimized/fail-closed; replaced authorization evidence requires re-inspection; product composition keeps the R10/P4.05/Governed Execution choke point; and reviewed presentation modules still select no durable frontend/API/IAM/storage boundary.

R11/P4.09's source-authorization refactoring watch item is resolved for this gate as **narrow reuse only**. `authority_safe_ux.consume_current_source_authorization()` remains an internal presentation decision consumer; P4.03–P4.07/R10 are not broadly migrated because their purpose/right/classification/freshness/exact-reliance/action-safety responsibilities remain distinct semantic-owner checks. P4.11 may reconsider a lower-level utility only if it preserves those ownership boundaries and materially reduces inconsistency.

No Product Contract change, capability lifecycle promotion, Stable/public interface, production/conformance claim or ADR-triggering durable technology choice is created. The P4.08 Product Contract remains `Provisional 0.1.0`; CAP-001 through CAP-004 remain `Incubating / Provisional`.

GitHub issue #54 remains the separately tracked hosted runner/account provisioning gap. P4.10 records deterministic executable coverage and syntax-validated test source without claiming a green hosted run that does not exist.

Canonical completion evidence:

- [`P4.01 operator journeys / workspace boundary / IA review`](../reviews/P4-01-operator-journeys-workspace-boundary-information-architecture.md) — `PASS`;
- [`P4.02 Organization context / identity / scoped navigation shell review`](../reviews/P4-02-organization-context-identity-scoped-navigation-shell.md) — `PASS`;
- [`R9 Workspace Boundary Review`](../reviews/R9-workspace-boundary-review.md) — `PASS`;
- [`P4.03 Canonical Record / Relationship inspection review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`;
- [`P4.04 Version / Event / provenance / reconstruction review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`;
- [`P4.05 Governed Execution / gate / approval-action review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`, four functional cross-review iterations;
- [`P4.06 Document / Artifact workspace review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`, five functional cross-review iterations including one pre-merge security finding and remediation;
- [`P4.07 Memory / Knowledge / Search discovery review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`, five functional cross-review iterations including exact-source, projection-gap, semantic-owner policy and ambiguity remediations;
- [`R10 Operator Safety / Cross-Capability Health Review`](../reviews/R10-operator-safety-cross-capability-health-review.md) — `PASS`, five functional cross-review iterations with one material stale-source-access action finding remediated before P4.08;
- [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`, six functional cross-review iterations with exact Product Contract/dependency/target continuity hardened;
- [`P4.08 bounded product Product Contract`](../contracts/P4-08-BOUNDED-PRODUCT-ENTRY-PRODUCT-CONTRACT.md) — reviewed at R11, remains `Provisional 0.1.0`;
- [`R11 Composition / Usability Refactoring Review`](../reviews/R11-composition-usability-refactoring-review.md) — `PASS`, five functional cross-review iterations;
- [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`;
- [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`;
- `reference/python/tests/test_p4_10_workspace_architecture_fitness_accessibility_usability.py` — deterministic cross-cutting regression evidence;
- GitHub issue `#54` — tracked hosted-CI provisioning gap; not an architecture exception or green-test claim.

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
| `P4.03` | Canonical Record / Relationship inspection experience | 🟩 Complete | `██████████ 100%` |
| `P4.04` | Version, Event, provenance and reconstruction experience | 🟩 Complete | `██████████ 100%` |
| `P4.05` | Governed Execution, gate and approval/action experience | 🟩 Complete | `██████████ 100%` |
| `P4.06` | Document / Artifact workspace experience | 🟩 Complete | `██████████ 100%` |
| `P4.07` | Memory / Knowledge / Search discovery experience | 🟩 Complete | `██████████ 100%` |
| `P4.08` | Cross-capability task/context composition + bounded product entry point | 🟩 Complete | `██████████ 100%` |
| `P4.09` | Security, rights, minimization and authority-safe UX | 🟩 Complete | `██████████ 100%` |
| `P4.10` | Workspace architecture fitness + accessibility/usability baseline | 🟩 Complete | `██████████ 100%` |
| `P4.11` | Workspace hardening / ADR / refactoring review | ⬜ | `░░░░░░░░░░ 0%` |
| `P4.12` | Phase 4 / M4 closure review | ⬜ | `░░░░░░░░░░ 0%` |

Phase 4 roadmap work-item completion is `10 / 12 = 83.3%`. Engineering reviews such as R9/R10/R11/R12 are gates and do not inflate this percentage as separate equal-weight work items.

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
- ambiguity or missing effective version is surfaced rather than silently resolved;
- actual source dereference independently enforces governed Organization/platform scope and current authorization rather than trusting presentation wrapper or identifier syntax.

Completion evidence: [`P4.03 Canonical Record / Relationship inspection review`](../reviews/P4-03-canonical-record-relationship-inspection-experience.md) — `PASS`, four functional cross-review iterations and green full reference CI.

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

Completion evidence: [`P4.04 Version / Event / provenance / reconstruction review`](../reviews/P4-04-version-event-provenance-reconstruction-experience.md) — `PASS`, four functional cross-review iterations and green full reference CI (`Reference Python CI #132`, `456` tests).

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

Completion evidence: [`P4.05 Governed Execution / gate / approval-action review`](../reviews/P4-05-governed-execution-gate-approval-action-experience.md) — `PASS`, four functional cross-review iterations, executable static demo and green full reference CI.

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

Completion evidence: [`P4.06 Document / Artifact workspace review`](../reviews/P4-06-document-artifact-workspace-experience.md) — `PASS`, five functional cross-review iterations, executable static demo and green full reference CI (`Reference Python CI #154`, Python `3.12.13`, `495` tests, `OK`). The final surface reuses P3.07 purpose/right/classification enforcement before governed Artifact metadata presentation and exact reliance, omits restricted Artifact metadata without protected counts, and withholds unadmitted candidate Artifact metadata.

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

Completion evidence: [`P4.07 Memory / Knowledge / Search discovery review`](../reviews/P4-07-memory-knowledge-search-discovery-experience.md) — `PASS`, five functional cross-review iterations and green full reference CI (`Reference Python CI #164`, Python `3.12.13`, `521` tests, `OK`) on the implementation head. Exact Knowledge reliance is explicitly version-selected and rechecked through current source authorization plus CAP-002/P3.07 constraints; search remains derived and must resolve current exact governed sources; CAP-003 cannot widen CAP-002 Memory handling constraints; duplicate exact semantic-owner sources fail closed; missing projections do not imply source absence.

### P4.08 — Cross-capability task/context composition + bounded product entry point

Prove that one operator flow can compose multiple platform capabilities coherently while preserving product/platform boundaries.

Reference proof should include at least one bounded Product Contract-backed product entry point that:

- enters the shared workspace with explicit Organization/product context;
- consumes at least two relevant shared capability surfaces;
- does not reach into private platform implementation state;
- preserves exact version/authority/provenance semantics;
- returns product-domain decisions/behavior to the product boundary;
- demonstrates that shared workspace navigation does not become a generic product orchestrator;
- composes consequential operator actions through the R10 `operator_safety.py` guard rather than directly through the lower-level P4.05 action adapter;
- treats any source-access decision replacement, revocation, absence or ambiguity as requiring current re-inspection before consequential action can continue.

The Product Contract remains Provisional unless separately promoted through RFC-0004 governance.

Completion evidence: [`P4.08 cross-capability task/context composition review`](../reviews/P4-08-cross-capability-task-context-composition.md) — `PASS`, six functional cross-review iterations. The bounded Product Contract-backed entry composes CAP-001/P4.06 and CAP-002/P4.07 surfaces, keeps task/disposition semantics product-owned, pins exact Product Contract and admitted dependency versions/mechanism, binds Governed Execution to the exact product task operation/target, and routes consequential actions only through R10. No existing platform runtime module is changed. Hosted CI provisioning is tracked separately in issue #54; no green P4.08 Actions run is claimed.

### P4.09 — Security, rights, minimization and authority-safe UX

Harden the human interaction surface so governance semantics are not technically correct but operationally misleading.

Required checks:

- unauthorized or wrong-Organization content is not exposed through navigation, search, counts, previews or metadata leakage;
- hidden actions cannot be invoked through alternate client state;
- UI labels do not imply approval/authority that the runtime has not established;
- sensitive content follows classification/purpose/minimization rules;
- derived previews/summaries cannot bypass source access rules;
- expired/revoked/stale authority or knowledge is represented correctly;
- audit-sensitive operator actions remain attributable;
- revisit R11's bounded source-authorization matching duplication only if P4.09/P4.10 evidence supports a narrow shared decision-consumption helper without creating a new policy/IAM owner.

Completion evidence: [`P4.09 Security, rights, minimization and authority-safe UX review`](../reviews/P4-09-security-rights-minimization-authority-safe-ux.md) — `PASS`. The bounded internal helper consumes exact current source-authorization evidence without deciding policy, fails closed for unauthorized/wrong-Organization/ambiguous state, suppresses protected counts and stale derived previews, requires re-inspection after authorization-decision replacement, and uses authority-safe action labels. Existing semantic owners retain purpose/right/classification/freshness/exact-reliance and Governed Execution authority. `Reference Python CI #188` failed at separately tracked hosted-runner provisioning issue #54; no green run or test-suite failure is claimed from that run.

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

Completion evidence: [`P4.10 Workspace architecture fitness + accessibility/usability baseline`](../reviews/P4-10-workspace-architecture-fitness-accessibility-usability-baseline.md) — `PASS`, four cross-review iterations and executable deterministic regression guards. The baseline is intentionally scoped to semantic/textual accessibility and does not claim formal WCAG or production visual-UX certification. Broad reuse of the P4.09 source-authorization helper is deferred because current capability/action surfaces still own distinct purpose/right/classification/freshness/exact-reliance safety checks.

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
| `R9 — Workspace Boundary Review` | after P4.02 | **Complete / PASS** — shell/navigation does not create authority, product leakage or accidental public boundary; P4.03 source-resolution handoff recorded |
| `R10 — Operator Safety / Cross-Capability Health Review` | after P4.07 | **Complete / PASS** — current source-access freshness is enforced at operator action composition; cross-capability presentation/reliance health reviewed before P4.08 |
| `R11 — Composition / Usability Refactoring Review` | after P4.08 / meaningful usability evidence | **Complete / PASS** — product-backed composition remains bounded and semantically explicit; no action bypass or ADR trigger found; source-access matcher duplication retained as bounded watch item for P4.09/P4.10 |
| `R12 — M4 Workspace Hardening` | after P4.10 | **Current** — final dependency, authority-bypass, accessibility, deterministic-state and ADR-gate hardening |

Engineering gates are review/hardening gates and do not inflate roadmap completion percentages as separate equal-weight product tasks.

## 6. Dependency-aware sequence

```text
M3 ✅ Shared Capability baseline
        ↓
P4.01 Operator journeys + IA ✅
        ↓
P4.02 Organization/identity navigation shell ✅
        ↓
R9 Workspace Boundary Review ✅
        ↓
 ┌──────────┼───────────────┐
 ↓          ↓               ↓
P4.03 ✅   P4.04 ✅        P4.05 ✅
Records     Provenance      Execution
 └──────────┼───────────────┘
            ↓
 ┌──────────┴─────────┐
 ↓                    ↓
P4.06 ✅              P4.07 ✅
Docs                  Knowledge/Search
 └──────────┬─────────┘
            ↓
R10 Cross-Capability Health ✅
            ↓
P4.08 Product-backed composition proof ✅
            ↓
R11 Composition/Usability Refactoring ✅
            ↓
P4.09 Security / rights / authority-safe UX ✅
            ↓
P4.10 Fitness + accessibility/usability evidence ✅
            ↓
R12 M4 Hardening ← current
            ↓
P4.11 ADR / boundary / refactoring review
            ↓
P4.12 Closure review
            ↓
M4
```

P4.10 is now complete; R12 consumes its matrix/baseline as hardening regression evidence.

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

> **`R12 — M4 Workspace Hardening`.**

Use the completed P4.10 fitness matrix and accessibility/usability baseline as regression evidence. Re-check dependency direction, product/platform boundaries, source-authorization/Organizational-Authority separation, fail-closed action paths, exact-version/provenance semantics, derived-state non-authority, accessibility-critical blocked/current-state meaning, deterministic critical-state coverage and every still-armed ADR trigger.

R12 must not turn the P4.10 bounded accessibility baseline into an unsupported formal WCAG/production-certification claim, and it must not treat issue #54 as proof of test success or as grounds to waive deterministic negative-path coverage.

The P4.09 helper remains a narrow presentation decision-consumption primitive through R12. Any wider refactor must preserve capability-specific purpose/right/classification/freshness/exact-reliance checks and R10 action-freshness semantics rather than centralizing them into an accidental IAM/policy owner.
