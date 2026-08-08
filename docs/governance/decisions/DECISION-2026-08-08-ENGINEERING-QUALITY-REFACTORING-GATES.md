# DECISION-2026-08-08 — Engineering Quality and Refactoring Gates

Status: `Approved`
Date: `2026-08-08`
Decision owner: `ООО «Арвектум»`
Task classification: `governance`
Scope: Arvectum OS engineering and roadmap execution
Constitution: `1.2.0`
Architecture baseline: RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)
Related roadmap: `docs/roadmap/ROADMAP.md`
Related active phase: `docs/roadmap/PHASE-2-CORE-RUNTIME.md`

## 1. Context

Arvectum OS needs explicit points at which the accumulated implementation is reviewed, simplified, refactored and, where evidence warrants it, optimized.

Running a full-codebase refactoring exercise after every roadmap work item would create delivery overhead and encourage premature abstraction. Deferring all cleanup until a large phase boundary would instead allow accidental implementation structure and technical debt to harden into cross-module dependencies.

The adopted model therefore uses evidence-backed engineering gates tied to architectural and delivery milestones rather than a calendar cadence.

This decision is subordinate to the Constitution, Accepted RFCs, Accepted ADRs and other higher-authority canonical artifacts. It does not amend architecture and does not itself select implementation technology.

## 2. Decision

### 2.1 Continuous engineering hygiene

Normal local engineering hygiene remains continuous and does not wait for a milestone gate. Pull requests and bounded work items SHOULD address proportionate issues such as naming, local duplication, typing, tests, dead code, obvious complexity and regressions when doing so does not materially broaden scope.

A full-codebase review is not required after every `PN.xx` work item.

### 2.2 Phase 2 engineering gates

Phase 2 uses four named engineering gates. These identifiers are engineering checkpoints, not roadmap work-item, RFC, ADR or capability identifiers.

#### R1 — Structural Review

Trigger: immediately after `P2.01` and before substantive `P2.02` implementation.

Purpose:

- review the extracted runtime / fixture / test boundaries;
- detect scenario-specific leakage into reusable runtime code;
- review dependency direction, cycles, duplicated orchestration and accidental internal APIs;
- remove obsolete P1-only implementation structure where evidence supports removal;
- keep adapters and physical package topology reversible;
- preserve behavior through tests.

R1 is architecture-oriented refactoring. Performance optimization is not a goal unless a measured or correctness/security-relevant problem is discovered.

Because this decision is being recorded after canonical completion of `P2.01`, R1 becomes the current engineering gate and MUST complete before substantive `P2.02` work proceeds.

#### R2 — Runtime Health Review

Trigger: after `P2.06` and before substantive `P2.07` implementation.

Purpose:

- review the accumulated Core Runtime semantic spine across lineage/version resolution, relationships, Governed Execution, Events/provenance and consistency semantics;
- reconcile duplicated validation, state-transition, error, idempotency and conflict logic;
- review module cohesion and dependency structure;
- assess test quality and cross-cutting invariant coverage;
- identify concrete ADR triggers that have emerged;
- establish profiling or benchmark evidence where runtime performance has become materially relevant.

#### R3 — Reuse Refactoring Review

Trigger: after `P2.09` and before final Phase 2 hardening.

Purpose:

- use evidence from two materially distinct bounded workflows to determine what is genuinely reusable;
- remove speculative abstractions and unused extension hooks;
- eliminate workflow-specific forks or duplicated orchestration from shared runtime code;
- simplify interfaces that were over-generalized from the first scenario;
- generalize only where reuse evidence justifies it.

The governing principle is `validated reuse over speculative generality`.

#### R4 — Milestone Hardening

Trigger: after the final applicable `P2.10` fitness evidence is available and before `P2.11` / `P2.12` close M2.

Purpose:

- perform the final full Phase 2 code-health review;
- remediate material architecture, correctness, security, maintainability and evidence gaps;
- perform evidence-backed performance optimization where measured bottlenecks justify it;
- leave `P2.11` to evaluate the hardened runtime boundaries and ADR gates rather than use the closure review as an uncontrolled refactoring phase;
- leave `P2.12` as a closure decision over an already hardened code head.

### 2.3 Performance optimization rule

Performance optimization SHOULD be evidence-backed.

Where performance matters, the preferred sequence is:

1. establish a benchmark, profile or other reproducible evidence;
2. identify a material bottleneck or resource problem;
3. optimize without weakening architectural invariants;
4. rerun the measurement and regression/fitness tests;
5. retain the optimization only when it produces justified value without disproportionate complexity.

This does not prohibit immediate correction of an obvious algorithmic, denial-of-service, resource-exhaustion, correctness or security problem merely because formal profiling has not yet been run.

### 2.4 Milestone Code Health Gate

Every later roadmap milestone `Mx` MUST include a proportionate Code Health Gate before closure.

The gate scope is determined by the code and contracts materially accumulated or changed by that milestone. It does not require mechanically reviewing unrelated stable code at maximum depth.

The gate SHOULD examine, as applicable:

- architecture and dependency boundaries;
- product/platform leakage;
- correctness and invariant preservation;
- security, privacy, isolation and authority semantics;
- maintainability, duplication, dead code and unnecessary abstraction;
- test and fitness evidence;
- migration/reversibility;
- performance evidence where performance is materially relevant;
- crossed RFC/ADR/Product Contract/policy gates.

### 2.5 Stable-boundary gate

Independently of milestone timing, a focused engineering review is required before an implementation boundary becomes materially expensive to change, including where applicable before reliance on:

- a `Stable` Product Contract boundary;
- a stable public or cross-product API/SDK;
- a durable cross-module serialization or schema contract;
- a materially constraining shared persistence/runtime dependency;
- an `Active` Platform Capability transition;
- material external production reliance.

The review MUST remain scoped and proportionate. It does not itself authorize lifecycle promotion, production readiness, conformance or commercial commitments.

### 2.6 ADR and governance interaction

Engineering gates do not replace the existing ADR gate.

If a review discovers that a concrete implementation choice has become materially constraining under the canonical Roadmap or Accepted RFC rules, the applicable ADR MUST be created and accepted before further material reliance on that choice.

No new RFC or ADR is required merely to establish these engineering-quality checkpoints.

## 3. Consequences

Positive consequences:

- refactoring occurs after meaningful evidence accumulates rather than by arbitrary cadence;
- the runtime is simplified before accidental interfaces harden;
- reuse decisions can be based on more than one workflow;
- performance work is tied to measurable value;
- milestone closure is separated from uncontrolled code restructuring;
- future stable/public boundaries receive scrutiny before change becomes expensive.

Trade-offs:

- engineering gates add bounded delivery work at selected milestones;
- a gate may temporarily delay the next roadmap item when material debt or an ADR trigger is found;
- not every cleanup request is guaranteed to wait for a gate, because local hygiene remains continuous.

## 4. Authority and compatibility

This decision is an approved engineering/planning decision at a subordinate governance level.

It is compatible with Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008 because it reinforces proportionality, reversibility, validated reuse, explicit boundaries, architecture-before-materially-constraining implementation and evidence-based evolution without modifying any normative architectural contract.

It does not:

- amend the Constitution;
- modify an Accepted RFC;
- create or activate a Platform Capability;
- establish production readiness or conformance;
- select a database, broker, IAM provider, workflow engine, public protocol or service topology;
- create SLA, support or commercial commitments.
