# R28 — M8 Ecosystem Hardening Review

Status: `Complete / PASS — no unresolved material hardening finding`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract` implications
Constitution: `1.2.0` (`Ratified`, frozen)
Checked Accepted RFC: RFC-0001 through RFC-0008 (`1.0.0`)
Checked ADR: no Accepted ADR exists; `docs/adrs/` contains only the ADR process/index
Roadmap source: `docs/roadmap/PHASE-8-ECOSYSTEM-EXTERNAL-INTEGRATION.md`
Predecessor: `P8.11 — Complete / PASS`
Required successor after PASS: `P8.12 — Phase 8 / M8 closure review`
Engineering gate basis: `DECISION-2026-08-08-ENGINEERING-QUALITY-REFACTORING-GATES.md` (`Approved`)

## 1. Decision

R28 completes the mandatory M8 pre-closure ecosystem hardening review and applies the Approved Milestone Code Health Gate to the material Phase 8 implementation and evidence surfaces.

Verdict:

> **PASS. No unresolved material architecture, dependency-direction, correctness, security/privacy/isolation, maintainability, repository-hygiene, regression-protection, accidental-public-surface, migration/reversibility or documentation/status defect requires remediation before P8.12.**

The review does **not** declare M8 achieved. P8.12 remains responsible for milestone closure against the complete M8 exit criteria and must preserve all stated limitations.

R28 creates no Constitution amendment, RFC/ADR, Product Contract lifecycle transition, Platform Capability lifecycle transition, public/stable SDK/API/manifest/registry/export format, external/customer Production approval, support/SLA commitment, certification or commercial promise.

## 2. Authority and material scope checked

R28 rechecked:

1. Constitution `1.2.0`;
2. RFC Index and Accepted RFC-0001 through RFC-0008 `1.0.0`;
3. current ADR index — no Accepted ADR;
4. Approved Engineering Quality and Refactoring Gates;
5. canonical master and detailed Phase 8 roadmaps;
6. P8.04 EIS governed evidence admission and its tests;
7. P8.05 external ingress/egress, duplicate/replay/uncertainty/reconciliation harness and tests;
8. P8.06 external-consumer onboarding/dependency-resolution helper, Creative Test Agent reference consumer and tests;
9. P8.07 bounded handover/interoperability harness and tests;
10. P8.08 multi-Organization non-activation disposition;
11. P8.09 operator/developer runbook and documentation-behavior tests;
12. R27 reuse/containment disposition;
13. P8.10 external claim boundary;
14. P8.11 architecture/ADR/refactoring/lifecycle disposition and hardening guard;
15. repository Python CI generated-artifact guard and full reference regression suite.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was found.

## 3. Architecture and dependency direction

### 3.1 Product/platform boundary

PASS.

Phase 8 retains the established direction:

- EIS/procurement behavior remains Tender Operator product-owned;
- Creative Test Agent domain semantics and declaration format remain product-owned;
- platform reliance is through exact Product Contract / capability dependency semantics;
- no product obtains platform behavior through internal tables, undocumented endpoints, private event streams, internal imports or implicit shared mutable state;
- P8.06 onboarding remains an internal bounded reference helper, not a new Platform Capability or public integration layer.

There is no evidence-based reason to extract a generic external-consumer framework, manifest/registry, connector marketplace or universal compatibility layer.

### 3.2 External authority and governed state

PASS.

P8.04/P8.05 preserve external source authority rather than creating a competing source of truth. Native platform evidence records admission/reconstruction facts; it does not convert the externally authoritative source fact into Native authority.

Consequential canonical mutation remains RFC-0005 Governed Execution scope. Historical reconstruction/replay does not authorize a fresh external effect.

## 4. Correctness and invariant review

PASS.

Material Phase 8 invariants remain explicit and regression protected:

- Subject/Version identity and Organization scope are pinned where relied upon;
- Product Contract and governed provider dependency versions are exact and fail closed;
- duplicate transport delivery is distinct from canonical Event admission;
- materially different reuse of an occurrence/delivery identity is rejected;
- uncertainty is not silently converted to success or blindly retried;
- reconciliation is append-only evidence and retry after reconciliation requires a fresh governed attempt;
- handover preserves identity/version/relationship/history semantics and explicit omission/reprovisioning rules;
- migration authority cannot be active concurrently in source and receiver without a governed transition;
- generated/exported evidence grants no technical access or Organizational Authority.

No material correctness defect was found that justifies changing the Phase 8 runtime/reference implementation in R28.

## 5. Security, privacy, isolation and authority

PASS for the **actually activated one-Organization scope only**.

The review confirms:

- deny-by-default / least-privilege boundaries remain explicit;
- Authentication, Authorization, Organizational Authority and Data Governance remain distinct;
- onboarding declarations/receipts do not grant permission or authority;
- external transfer remains fail closed;
- secrets/credentials are not embedded in portability evidence;
- cross-Organization transfer/reuse remains denied absent explicit governed rights;
- P8.08 realistic two-Organization isolation remains `NOT ACTIVATED / NOT PROVEN` because no genuine second Organization exists in canonical scope.

R28 intentionally does not fabricate a second Organization merely to make a broader security claim. Storage/query/index/cache/background/observability/admin/AI-context isolation across two real Organizations remains outside the proven scope until the P8.08 re-entry condition is actually satisfied.

## 6. Maintainability, duplication, dead/generated code and abstraction pressure

PASS.

### 6.1 Generated/repository noise

The repository CI already contains an explicit tracked-generated-artifact rejection step for `__pycache__`, `.pyc/.pyo` and `.pytest_cache`; R28 adds a regression assertion that this guard remains present.

No new generated artifact or cache path is introduced by R28.

### 6.2 Dead/obsolete paths

No material `TODO`, `FIXME`, `NotImplementedError`, abandoned compatibility branch or superseded Phase 8 runtime path was identified in the reviewed material Phase 8 surfaces.

Historical evidence files and task-specific proof harnesses are not treated as dead code merely because they are bounded: they remain executable evidence for the milestone and are intentionally not generalized into supported platform surfaces.

### 6.3 Duplication and abstraction

Some Phase 8 evidence intentionally repeats exact immutable evidence pins and boundary assertions across task-local harnesses. That duplication is evidence-local and keeps proofs attributable; it is not sufficient evidence for a shared generic abstraction.

Large test/evidence files are not refactored solely because of size. The gate found no demonstrated responsibility split, coupling defect or repeated behavior whose extraction would reduce risk without prematurely stabilizing a surface.

## 7. Test quality and regression protection

R28 adds `reference/python/tests/test_r28_m8_ecosystem_code_health_gate.py` with seven high-value checks that protect:

1. bounded Phase 8 harnesses from gaining live external transport dependencies;
2. P8.06 onboarding from becoming a public/platform-owned authoritative surface;
3. P8.07 handover from silently activating customer/cross-Organization transfer or external-effect replay;
4. preservation of the P8.08 `NOT ACTIVATED / NOT PROVEN` limitation;
5. the current no-Accepted-ADR / no accidental public-surface disposition;
6. the repository generated-Python-artifact CI guard;
7. mandatory R28-before-P8.12 sequencing without coupling the test to a transient roadmap `Current` status or one Markdown table shape.

The tests protect governed semantics rather than arbitrary line-count, complexity or coverage-percentage thresholds.

Evidence:

- prior P8.11 executable baseline: `1270 tests / OK` recorded canonically;
- R28 introduced seven dedicated semantic code-health regression test methods and reconciled one stale P8.11 roadmap guard;
- initial R28 executable gate: `Reference Python CI #211` / commit `6a11456ed06dbb4f98ba7b6c81128c382c068d86` — `success`;
- final executable/test synchronization head before review-record-only closure edits: commit `ce4479e77123425a11155f3a421ecf80231807ec`;
- final full executable suite on that head: `Reference Python CI #220` — `success`, `Ran 1278 tests in 22.125s`, `OK`;
- the CI generated-artifact rejection step also completed successfully on #220.

The later edits to this review and its companion M8 gate record are documentation-only closure synchronization. They do not alter the reviewed runtime or executable guards; the PR must still have a green required CI on its final merge head.

R28 does not claim that test count alone establishes correctness. The PASS rests on the scoped review plus executable regression evidence.

## 8. Accidental stable/public surface review

PASS.

No material Phase 8 implementation is reclassified as a public/stable compatibility promise.

The following remain deliberately bounded:

- P8.06 `external_consumer_onboarding.py` — internal reference slice;
- Creative Test Agent declaration format — product-owned;
- P8.07 package/receipt schema — task-local interoperability proof;
- P8.09 runbook — exact bounded external-consumer documentation;
- current Python dataclasses, operation names and serialization choices — reference implementation details unless separately governed otherwise.

No Accepted ADR exists because no durable cross-cutting technology/public compatibility choice has crossed the established ADR threshold.

## 9. Performance disposition

`Not a material gate dimension for R28 beyond regression sanity.`

Phase 8 does not introduce a customer-facing latency/throughput/SLO commitment, high-volume transport, selected broker, durable public service boundary or benchmark-backed performance claim. Inventing a threshold here would create unsupported readiness/compatibility expectations.

If a later external Production/service topology creates a material performance commitment, benchmark and operational evidence must be added at that governed boundary.

## 10. Migration, reversibility and portability

PASS for current scope.

- exact Product Contract/provider version reliance remains fail closed;
- onboarding can be disabled/removed and upgrades re-run exact dependency resolution;
- P8.07 demonstrates bounded semantic portability without claiming a universal customer format;
- non-exportable secrets require separate reprovisioning;
- authority transfer is separate and explicit;
- historical replay does not repeat external effects;
- no irreversible shared platform generalization is introduced by R28.

## 11. Documentation and status consistency

PASS after R28 synchronization.

Required canonical state after this review is recorded:

- P8.11 = `Complete / PASS`;
- R28 = `Complete / PASS`;
- M8 is **not yet closed** by R28;
- P8.12 becomes the next canonical action;
- P8.08 realistic two-Organization isolation remains `NOT ACTIVATED / NOT PROVEN`;
- P8.07 external customer/cross-Organization transfer remains `NOT ACTIVATED`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- relevant Product Contracts remain `Provisional`;
- no public/stable ecosystem interface, external/customer Production, support/SLA/certification or commercial promise is created.

## 12. Functional cross-review

Seven iterations were completed, which is the configured maximum. All material objections found during the cycle were resolved before merge; the final iteration ended in PASS.

### Iteration 1 — architecture / dependency direction

Result: `PASS`.

No dependency inversion, product-business-logic leakage or hidden shared-state coupling was found. No new shared abstraction is justified.

### Iteration 2 — security / isolation / authority

Result: `REVISE`.

Material objection: a generic milestone PASS could be misread as realistic multi-Organization validation even though P8.08 is explicitly unproven.

Revision: R28 scope and executable guard explicitly preserve `NOT ACTIVATED / NOT PROVEN` and limit the security PASS to the actually activated one-Organization contour.

Disposition: `resolved`.

### Iteration 3 — maintainability / repository health

Result: `PASS`.

Generated-artifact hygiene is already enforced in CI; reviewed Phase 8 proof-specific duplication is bounded and attributable; no dead compatibility path or justified refactor was identified.

### Iteration 4 — public/stable surface / performance / claims

Result: `REVISE`.

Material objection: a milestone hardening gate could accidentally convert executable helper/package shapes into supported API/export commitments or invent performance readiness requirements.

Revision: explicit non-public/non-stable disposition retained; R28 adds a regression guard and marks performance as non-material absent a measured/contracted performance boundary.

Disposition: `resolved`.

### Iteration 5 — initial executable regression gate

Result: `PASS`.

`Reference Python CI #211` completed successfully with the initial seven-test R28 gate. This established the executable baseline for the hardening review, but roadmap synchronization was still subjected to subsequent cross-review rather than treated as automatically safe.

### Iteration 6 — sequencing guard durability

Result: `REVISE`.

Material objection: the first R28 sequencing assertion encoded the temporary state in which `R28` itself was `Current`. Correctly advancing the roadmap to `R28 Complete / PASS → P8.12 Current` would therefore have made the new regression guard fail after the intended state transition.

Revision: the guard was rewritten to protect the durable historical invariant `P8.11 → R28 → P8.12` and R28 completion, without requiring a transient `Current` marker.

Disposition: `resolved`.

### Iteration 7 — full-suite stale guard and roadmap-shape reconciliation

Result: `REVISE → PASS`.

The final full-suite review exposed two stale/over-specific test assumptions rather than an architecture defect:

1. the P8.11 architecture-fitness guard still pinned exact older roadmap versions/status text, so a legitimate R28 roadmap advance caused failure;
2. the revised R28 roadmap assertion initially assumed the master and detailed Phase 8 roadmaps used the same Markdown table shape, although the detailed roadmap contains an additional dependency column.

Revision:

- P8.11 now protects the durable historical `P8.11 → R28 → P8.12` sequence instead of obsolete roadmap versions/transient status;
- R28 sequencing verification is table-shape independent and checks semantic ordering/completion rather than a brittle literal row shape;
- no runtime behavior, authority boundary, lifecycle, public surface or product/platform responsibility was broadened to make the tests pass.

Final evidence on executable/test head `ce4479e77123425a11155f3a421ecf80231807ec`: `Reference Python CI #220 = success`; generated-artifact guard passed; full suite `1278 tests / OK`.

Disposition: `resolved`; final iteration result `PASS`.

No material objection remains.

Functional cross-review is not formal RFC/ADR acceptance, lifecycle promotion, operational-readiness approval, conformance certification or commercial authority.

## 13. Final R28 verdict

`R28 = Complete / PASS`.

There is no unresolved material R28 finding requiring remediation or owner risk acceptance before P8.12.

The next canonical action is:

> `P8.12 — Phase 8 / M8 closure review`.

P8.12 must decide milestone closure against the complete M8 exit criteria and preserve all bounded/unproven claims above; R28 by itself does not close M8.
