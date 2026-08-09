# R12 — M4 Workspace Hardening

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Engineering gate: `R12 — M4 Workspace Hardening`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — one material stale-presentation authorization-continuity defect was identified and remediated; the bounded Phase 4 workspace remains fit to proceed to P4.11 with no remaining material architecture, product/platform, authority-bypass, accessibility-baseline or ADR finding.`**

## 1. Purpose

R12 is the final engineering hardening gate after P4.10 and before P4.11/P4.12. It re-checks the accumulated bounded Phase 4 workspace for defects that could invalidate the M4 baseline even though the P4.10 fitness matrix already passes.

R12 reviews:

- dependency direction and product/platform boundaries;
- Organization/source isolation and source-dereference continuity;
- Authorization versus Organizational Authority separation;
- exact-version/provenance semantics;
- derived presentation/reconstruction/search non-authority;
- fail-closed consequential action paths;
- accessibility-critical blocked/current-state meaning;
- deterministic negative-path coverage;
- the bounded P4.09 decision-consumption helper;
- every still-armed ADR trigger;
- current engineering evidence, including the recovered hosted-CI state after issue #54.

R12 is an engineering hardening checkpoint. It is not a capability-lifecycle promotion, Product Contract stabilization, public API approval, production-readiness approval, formal accessibility certification, full-platform conformance statement or commercial commitment.

## 2. Canonical authority checked

R12 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral product/platform separation, dependency rules, Governed Execution, structural security/isolation, internal-interface containment, proportionality and scoped conformance;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, explicit Head/Effective semantics, fail-closed ambiguity and non-authoritative projections;
5. RFC-0003 — deny-by-default authorization, explicit Organization scope, actual/represented Actor attribution, Authorization/Organizational-Authority separation, purpose/minimization, tenant isolation and fail-closed enforcement;
6. RFC-0004 — explicit Product Contract boundary, no hidden coupling, exact dependency declarations and no permission/authority by contract possession;
7. RFC-0005 — exact governed input/Workflow/Product Contract pinning, separate gates and consequential canonical mutation only through Governed Execution;
8. RFC-0006 — provenance/evidence honesty, side-effect-safe derived reconstruction/replay and non-authoritative telemetry/projections;
9. RFC-0007 — Memory/Knowledge lifecycle distinctions, freshness/exact reliance and Search/RAG non-authority;
10. RFC-0008 — Document/Artifact/version/authority/provenance distinctions, handling-constraint propagation and non-authoritative derived representations;
11. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains the bounded internal Phase 4 implementation;
12. P4.01 through P4.10 reviews plus R9, R10 and R11;
13. `P4.08 Bounded Product Entry Product Contract` — remains `Provisional 0.1.0`;
14. canonical Roadmap `2.23.0` and Phase 4 roadmap `1.13.0` at R12 start;
15. `P4.10 — Hosted CI Validation Evidence` — `Complete`, pre-R12 baseline validated by Reference Python CI #191 with `559 tests`, `OK`;
16. GitHub issue #54 — closed `completed` after hosted runner provisioning recovered.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 is introduced by the R12 remediation.

## 3. Baseline under review

The bounded Phase 4 interaction path remains:

```text
Product-owned bounded entry
        |
        | exact Provisional Product Contract + dependency admissions
        v
Shared Workspace / capability presentation
        |
        +--> Canonical Record / Relationship inspection
        +--> Event / provenance / reconstruction
        +--> Document / Artifact
        +--> Memory / Knowledge / Search
        |
        `--> consequential request
                 |
                 v
           R10 operator_safety
                 |
                 v
           P4.05 action adapter
                 |
                 v
           Governed Execution / runtime canonical commit
```

Presentation, search and reconstruction remain non-authoritative. Product-domain task/disposition semantics remain outside `arvectum_os_ref`. The P4.09 `authority_safe_ux` helper remains an internal consumer of already-produced source-authorization evidence rather than a policy decision point or IAM owner.

## 4. Material finding and remediation

### R12-F1 — Re-inspection state exposed the replacement authorization Version Identity

Severity: `Material — security/correctness / stale-presentation boundary`
Disposition: `Remediated`

Before R12, `consume_current_source_authorization()` correctly detected when a previously inspected source-authorization decision Version Identity had been replaced. It returned `REINSPECTION_REQUIRED`, hid governed content/count/preview and used the safe `Re-inspect current access` label.

However, that blocked result carried the **new current authorization decision Version Identity**. A presentation caller could therefore treat the returned replacement identifier as a continuity token on its next call and advance stale presentation state without preserving the old inspected authorization pin. The helper did not itself re-dereference the governed source, so exposing the replacement token weakened the intended meaning of `re-inspection required`.

This did not bypass R10's consequential-action protection: R10 independently pins and rechecks the exact source-authorization decision immediately before the P4.05/Governed Execution path. The defect was nevertheless material because governed presentation and derived previews must remain fail closed after authorization replacement rather than becoming refreshable from stale presentation continuity alone.

R12 hardens the helper so that:

- `AVAILABLE` requires the safe request-action label, an exact current allow-decision Version Identity and explicit source visibility;
- `REINSPECTION_REQUIRED` carries only the **previously inspected/stale** decision Version Identity supplied by the caller, never the replacement decision identity;
- reusing that blocked continuity token against the replacement decision remains `REINSPECTION_REQUIRED`;
- `NOT_AVAILABLE` exposes no authorization decision identity;
- every blocked state exposes no governed content, protected count or derived preview;
- inconsistent state/label/identity/visibility combinations fail at DTO construction.

The behavior intentionally does not make the helper an authorization policy engine. A true new inspection cycle must still re-dereference the governed source and re-run the applicable capability-specific purpose/right/classification/freshness/exact-reliance checks.

The remediation is bounded, internal and reversible. It changes no Accepted architecture, Product Contract, capability contract or public compatibility surface.

## 5. Dependency and product/platform hardening

Result: `PASS`.

R12 re-checks the product-backed composition and confirms:

- `bounded_product_ref` remains outside `arvectum_os_ref`;
- product task/disposition/operation semantics are not imported into the platform package;
- product capability use remains tied to the exact Product Contract Version and admitted dependency contract versions;
- current Actor and Organization remain explicit composition inputs;
- product consequential action preparation/execution imports and uses the R10 `operator_safety` wrappers rather than the lower P4.05 action adapter directly;
- the platform package does not depend on the bounded product package.

No cross-layer dependency inversion, generic product orchestrator or accidental shared product-domain semantic owner is justified.

## 6. Authorization, Organizational Authority and action hardening

Result: `PASS after R12-F1 remediation`.

The workspace continues to preserve separate meanings for source-read authorization, purpose/right/classification handling controls, authentication/Actor context, Organizational Authority, consequential approval and Governed Execution admission.

P4.09 remains presentation-only. It does not grant permission, Organizational Authority or approval. P4.04/P4.06/P4.07 retain independent evidence/artifact/knowledge handling and exact-reliance checks. R10 retains stricter action-freshness semantics and remains the cross-capability action choke point.

No reviewed presentation state, search hit, reconstruction, Product Contract admission, Actor identity or UI label can substitute for the applicable authority/gate evidence.

## 7. Exact-version, provenance and derived-state hardening

Result: `PASS`.

R12 found no regression in the P4.10 semantic baseline:

- Subject Identity remains distinct from exact immutable Version Identity;
- Head/Effective/exact historical references remain distinguishable;
- consequential Document/Knowledge/Execution reliance remains exact-version pinned where required;
- Event/provenance/correlation/causation and evidence limitations remain explicit;
- reconstruction, replay and Search remain derived/non-authoritative;
- working/transient/generated artifacts do not become canonical or validated organizational assets through presentation;
- presentation/read-model state has no reviewed canonical mutation path.

R12-F1 strengthens this result by ensuring a replaced source-authorization decision cannot be turned into a fresh presentation continuity token by the blocked helper response itself.

## 8. Accessibility and operator-error hardening

Result: `PASS — bounded semantic/textual baseline only`.

The remediation preserves the P4.10 operator meaning:

- `Available` can request a governed action but does not imply approval or Organizational Authority;
- `Re-inspection required` explicitly means the previously inspected access evidence is stale;
- `Not available` remains minimized and does not disclose protected content/count/preview;
- blocked re-inspection state does not disclose the replacement authorization decision identity;
- critical meaning remains textual rather than color-only in the existing reference renderers.

R12 does not claim formal WCAG conformance, production focus/keyboard/contrast/screen-reader validation, localization validation or final end-user UX certification. Those remain future real-frontend concerns when the applicable implementation boundary is selected.

## 9. Refactoring and code-health disposition

Result: `PASS — targeted remediation only`.

R12 does **not** broaden `authority_safe_ux` into a shared authorization framework. That would save little code while risking collapse of capability-specific security ownership.

The current evidence supports only the narrow shared decision-consumption primitive established by P4.09. P4.03–P4.07 and R10 keep their distinct source resolution, data-governance, freshness, exact-reliance and action-safety responsibilities.

No measured performance problem exists in the bounded reference implementation that justifies caching, prefetching, durable read-model selection or other optimization architecture.

## 10. ADR / Product Contract / lifecycle disposition

Result: `PASS — no new ADR required at R12`.

No reviewed implementation materially relies on a durable or externally constraining choice for frontend/runtime framework, public route/deep-link/BFF/API topology, stable wire/serialization contract, IAM/session provider or policy engine, durable workspace/read-model/cache store, durable search/vector/RAG technology, Document/object-store/OCR/signing topology, stable design-system/package compatibility boundary or separately deployable UI/API service topology.

The ADR gate therefore remains armed for P4.11 and later work but is not crossed by R12.

The P4.08 Product Contract remains `Provisional 0.1.0`. CAP-001 through CAP-004 remain `Incubating / Provisional`. R12 creates no lifecycle promotion, Stable/public interface, operational-readiness claim, production claim, SLA/support promise or broader conformance statement.

## 11. Engineering evidence synchronization

R12 re-checked the P4.10 CI evidence state.

The P4.10 completion-time statement that hosted execution was unavailable was accurate when written, but it is no longer the current engineering state. `docs/reviews/P4-10-ci-validation.md` explicitly supersedes those CI-availability statements and records Reference Python CI #191 passing the full pre-R12 baseline with `559 tests`, `OK`; issue #54 is closed `completed`.

Current planning/navigation documents are synchronized to that recovered evidence while preserving the historical P4.10 review rather than rewriting its contemporaneous statement.

## 12. Executable R12 hardening evidence

R12 adds:

- `reference/python/tests/test_r12_m4_workspace_hardening.py`.

The guard verifies that:

1. authorization replacement preserves the stale inspected decision pin and never returns the replacement decision identity in `REINSPECTION_REQUIRED`;
2. reusing a blocked continuity token remains blocked and cannot self-advance stale presentation;
3. inconsistent authority-safe state/label/decision-identity/visibility combinations fail closed;
4. the P4.09 helper remains narrow and does not replace P4.04/P4.06/P4.07/R10 semantic-owner controls;
5. product consequential action continues through R10 and not directly through the lower-level P4.05 adapter;
6. product-domain semantics remain outside the shared platform package.

Hosted validation on PR #58 pre-synchronization head `77e07f9279b48c5eca6d64a7179b0f947ea65bb5`:

```text
Reference Python CI #192
Runner: Ubuntu 24.04.4
Python: CPython 3.12.13
Command: python -m unittest discover -s tests -v
Result: Ran 563 tests — OK
```

This run validates the runtime remediation and all four newly added R12 test methods together with the complete existing reference suite. Documentation/roadmap synchronization follows it; the PR merge remains subject to the normal final synchronized-head CI check.

## 13. Functional cross-review iterations

### Iteration 1 — architecture / dependency direction

Finding: the accumulated workspace still preserves the intended platform/product dependency direction, but the P4.09 helper deserves close inspection because it is the only new shared cross-capability presentation primitive added after R11.

Disposition: no broad refactor; inspect stale authorization transitions directly.

### Iteration 2 — security / privacy / authority

Finding: R12-F1. `REINSPECTION_REQUIRED` concealed content but exposed the replacement authorization decision Version Identity, allowing stale presentation continuity to advance too easily.

Disposition: retain only the prior inspected authorization pin in re-inspection state, forbid replacement decision disclosure there, add state invariants and deterministic regression tests.

### Iteration 3 — engineering / usability / accessibility

Finding: hiding the replacement identity entirely would be weaker than retaining the stale pin because a caller could accidentally discard continuity state. Preserving the old known pin causes naive DTO reuse to remain blocked while keeping the operator-facing instruction explicit.

Disposition: use the stale pin, preserve textual `Re-inspect current access`, keep all content/count/preview hidden, and avoid introducing a session/state machine or framework merely to enforce presentation refresh.

### Iteration 4 — governance / ADR / delivery evidence

Finding: no durable implementation choice crosses an ADR threshold and no Product Contract/capability change is justified. Separately, issue #54 is resolved and current hosted-CI evidence is stronger than the stale planning text carried forward from P4.10 completion time.

Disposition: keep architecture/lifecycle unchanged; synchronize current planning/navigation documents; preserve the historical P4.10 review and rely on its dedicated later CI-validation record for current execution evidence.

No remaining material objection exists after iteration 4.

## 14. Exit criteria

- [x] dependency direction and product/platform boundary re-checked;
- [x] Organization/source isolation and stale authorization continuity re-checked;
- [x] Authorization/Organizational-Authority separation re-checked;
- [x] exact-version/provenance and derived-state non-authority re-checked;
- [x] consequential action choke point re-checked;
- [x] accessibility-critical blocked/current-state meaning re-checked;
- [x] deterministic R12 negative-path regression added;
- [x] all still-armed ADR triggers reviewed;
- [x] one material stale-presentation defect remediated;
- [x] full Reference Python CI passes on the R12 implementation/review head (`#192`, `563 tests`, `OK`);
- [x] canonical roadmap, Phase 4 roadmap and README synchronized to R12 completion and P4.11 handoff.

## 15. Handoff

R12 closes with `PASS`.

The next canonical roadmap work item is:

> **`P4.11 — Workspace hardening / ADR / refactoring review`.**

P4.11 must consume R12-F1 as a fixed regression invariant, keep the P4.09 helper narrow unless stronger reuse evidence appears, inspect presentation-domain/refactoring/ADR triggers explicitly and avoid performance architecture without reproducible evidence before P4.12/M4 closure.
