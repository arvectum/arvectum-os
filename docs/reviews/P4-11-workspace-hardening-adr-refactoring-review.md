# P4.11 — Workspace Hardening / ADR / Refactoring Review

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P4.11 — Workspace hardening / ADR / refactoring review`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — no material presentation-domain leakage, authority bypass, derived-state authority drift, accessibility/operator-error defect, ADR-triggering durable choice or evidence-backed performance need was found. No material runtime refactor is justified before P4.12; R12-F1 remains a fixed regression invariant. Canonical roadmaps are synchronized to P4.12 and hosted pre-synchronization validation passes 570 tests.`**

## 1. Purpose and decision level

P4.11 is the final architecture/refactoring work item after R12 and before the Phase 4 / M4 closure decision in P4.12.

It independently re-opens the following gates over the accumulated Phase 4 workspace rather than treating earlier PASS results as permanent assumptions:

1. presentation-domain and product/platform boundary;
2. evidence-based refactoring threshold;
3. Authorization / Organizational Authority / consequential-action bypass surfaces;
4. derived-state, cache and read-model authority risks;
5. API / serialization / frontend / BFF and other ADR triggers;
6. accessibility/usability failures capable of creating material operator error;
7. R12-F1 stale-authorization continuity;
8. performance-architecture pressure.

P4.11 is subordinate engineering/review evidence. It does not amend the Constitution or an Accepted RFC, create a new Platform Capability, stabilize the P4.08 Product Contract, approve production readiness, establish a public API/SDK, certify WCAG conformance, broaden conformance, or create an SLA/support/commercial commitment.

## 2. Canonical authority checked

P4.11 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral platform responsibility, product/platform separation, Governed Execution, security/isolation, proportional architecture, technology independence and scoped conformance;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, Head/Effective semantics, exact consequential reliance and projection/cache non-authority;
5. RFC-0003 — explicit Organization scope, deny-by-default Authorization, attributable Actor, Authorization/Organizational-Authority/Data-Governance separation, minimization and fail-closed behavior;
6. RFC-0004 — explicit Product Contract boundary, hidden-coupling prohibition, Product Contract lifecycle separation and no authority by contract possession;
7. RFC-0005 — exact Workflow/material-input/Product-Contract pinning, separate gates and consequential canonical mutation only through Governed Execution;
8. RFC-0006 — Event/provenance/reconstruction honesty, side-effect-safe replay and non-authoritative observability/projections;
9. RFC-0007 — Memory/Knowledge lifecycle, exact Knowledge reliance, freshness and Search/RAG non-authority;
10. RFC-0008 — Document/Version/Artifact distinctions, exact reliance, handling propagation and derived-representation non-authority;
11. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains the bounded internal Phase 4 implementation;
12. P4.01 through P4.10 reviews and R9/R10/R11/R12 engineering gates;
13. `P4.08 Bounded Product Entry Product Contract` — remains `Provisional 0.1.0`;
14. canonical Phase 4 roadmap synchronized to `1.15.0` and canonical Roadmap synchronized to `2.25.0` by P4.11;
15. R12 final synchronized-head evidence — Reference Python CI #196, `563 tests`, `OK`;
16. P4.11 hosted pre-synchronization evidence — Reference Python CI #197, `570 tests`, `OK`.

No conflict with Constitution `1.2.0` or Accepted RFC-0001 through RFC-0008 was identified by P4.11.

## 3. Presentation-domain and product/platform boundary review

Result: **`PASS — no accidental product/domain leakage.`**

The shared Phase 4 package remains domain-neutral:

- `arvectum_os_ref` owns only Organization/Actor workspace context, governed inspection semantics, presentation non-authority, exact-version/provenance meaning, source-evidence consumption and the R10 consequential-action safety boundary;
- product task identity, disposition values, product operation tokens and product decision notes remain under `bounded_product_ref`;
- platform Phase 4 modules do not import `bounded_product_ref`;
- the bounded product imports shared platform surfaces through its Provisional Product Contract proof, not private platform storage or an accidental product orchestrator;
- consequential product actions continue through R10 `operator_safety` and not directly through the lower-level P4.05 action adapter.

P4.11 found no product schema, taxonomy, business workflow, disposition or product-specific approval semantics that should be removed from the platform because none has crossed that boundary.

## 4. Authorization, Organizational Authority and action-bypass review

Result: **`PASS`**.

The reviewed flow continues to keep separate:

- current source-read Authorization evidence;
- Actor/Organization context;
- purpose/right/classification and other Data Governance controls;
- Organizational Authority;
- consequential approval;
- exact Product Contract and governed input/version pins;
- Governed Execution admission and canonical commit.

The P4.09 `authority_safe_ux` helper remains only a consumer of already-produced source-authorization evidence. It does not grant permission, evaluate purpose/right/classification policy, create Organizational Authority or approve a consequential action.

R10 remains the stricter pre-action freshness boundary: a prepared consequential action is pinned to the exact source-authorization decision used by the inspected view and that exact decision is rechecked before both preparation and execution delegation. Product composition has no reviewed path around R10 to P4.05.

No presentation state, navigation reference, search result, reconstruction, Product Contract admission, identity value or UI label substitutes for required runtime authority/gate evidence.

## 5. R12-F1 fixed regression invariant

Result: **`PASS — preserved and re-specified in P4.11 executable evidence.`**

P4.11 treats R12-F1 as fixed behavior rather than a one-off implementation detail:

- an `AVAILABLE` presentation may carry the exact current allow-decision Version Identity;
- authorization decision replacement produces `REINSPECTION_REQUIRED`;
- that blocked result retains only the previously inspected stale decision pin;
- the replacement decision Version Identity is not exposed as a continuity token;
- reusing the blocked stale token remains blocked;
- blocked state exposes no governed content, protected count or derived preview;
- a real fresh inspection cycle remains necessary before a replacement decision can support newly visible presentation state.

This invariant protects stale presentation continuity. It is additional to, and does not replace, R10 action freshness or capability-specific source/data-governance checks.

## 6. Refactoring gate

Result: **`PASS — no material runtime refactor justified.`**

### 6.1 Evidence reviewed

Exact `CurrentSourceAuthorization` context matching appears in multiple bounded Phase 4 surfaces. The duplication is real, but the surrounding responsibilities remain materially different:

- P4.03 owns governed source resolution, Subject/Version/Head/Effective and relationship semantics;
- P4.04 owns evidence access, provenance/reconstruction limitations and derived replay semantics;
- P4.06 owns Document/Artifact handling, purpose/right/classification and exact Document reliance;
- P4.07 owns Memory/Knowledge lifecycle, freshness, validation/approval, discovery minimization and exact Knowledge reliance;
- R10 owns exact stale-decision continuity immediately before consequential action;
- P4.09 owns minimized presentation consumption only.

### 6.2 Decision

P4.11 does **not** migrate those semantic owners onto `authority_safe_ux` and does not introduce a generic IAM/policy/presentation framework.

A lower-level shared matching utility is also deferred. Current repetition has not produced a demonstrated semantic inconsistency after the P4.10/R12 hardening, while extraction immediately before M4 closure would create a new shared internal abstraction without a stable external boundary or second implementation proving its shape.

The current `CurrentSourceAuthorization` evidence DTO is cross-used from the P4.03 module. That placement is a bounded code-organization watch item, not a material architecture defect: the type is internal, carries no permission semantics by itself and creates no public compatibility obligation. Revisit extraction when one of the following appears:

- a second independent workspace/presentation implementation needs the same evidence contract;
- matcher behavior diverges or produces a real correctness defect;
- a stable cross-module/public interface is being designed;
- a concrete IAM/PDP/PEP integration requires an explicit adapter boundary.

Until then, preserving semantic-owner boundaries is more valuable than reducing a small amount of matching code.

## 7. Derived-state, caching and read-model authority review

Result: **`PASS — no competing authority and no durable read-model commitment.`**

The reviewed workspace still treats:

- shell/navigation state as disposable non-authoritative presentation;
- reconstruction/replay as derived and non-authoritative;
- search/index results as derived discovery/projection;
- previews/summaries as subordinate to source visibility and handling rules;
- working/transient/generated artifacts as non-canonical until governed admission;
- caches/read models, where later introduced, as prohibited from becoming independent authority under Accepted RFC semantics.

The bounded Phase 4 code selects no durable cache, read-model database, projection store or synchronization topology. P4.11 therefore introduces no caching or denormalization abstraction merely to optimize reference code.

## 8. ADR gate re-assessment

P4.11 re-opens every implementation category that could create durable or externally constraining reliance.

| Boundary | Current Phase 4 evidence | P4.11 disposition | Future ADR trigger |
|---|---|---|---|
| Frontend/runtime framework | Static/inert renderers and Python DTOs remain reference evidence; no production frontend is selected. | **No ADR now.** | Material reliance on a concrete frontend/runtime/component framework or independently supported UI architecture. |
| Public route / deep-link / BFF / API topology | No stable route, BFF, REST, GraphQL, gRPC or public service boundary exists. | **No ADR now.** | First supported cross-product/public network boundary or topology-specific failure/compatibility contract. |
| Stable serialization / wire schema / SDK | Dataclasses, enums and operation tokens remain internal/provisional implementation evidence. | **No ADR now.** | First stable wire schema, serialization format, SDK or compatibility commitment. |
| IAM / session / PDP / PEP | Source-authorization evidence is consumed but no identity provider, session technology, policy language, entitlement store or enforcement topology is selected. | **No ADR now.** | Shared materially relied-upon concrete IAM/policy/enforcement mechanism. |
| Durable workspace/read-model/cache store | Presentation state is disposable; no durable workspace state or cache topology is required. | **No ADR now.** | Operational reliance on durable presentation/read-model/cache state, freshness guarantees or invalidation topology. |
| Search/vector/RAG runtime | Search semantics remain derived and technology-neutral. | **No ADR now.** | Concrete shared search/vector/RAG technology becomes required for correctness or supported operation. |
| Document/object/OCR/signing topology | P4.06 preserves semantics only and does not select infrastructure. | **No ADR now.** | Material shared reliance on a concrete DMS/object/OCR/signing topology. |
| Deployable service/process boundary | Phase 4 remains module-level reference code without an independently deployed workspace/API process. | **No ADR now.** | Separate service/worker/process with independent lifecycle, scaling or failure semantics. |
| Design-system/public component compatibility | Accessibility baseline is semantic/textual; no component-library compatibility promise exists. | **No ADR now.** | Supported stable component/design-system boundary or cross-product UI compatibility obligation. |

**ADR decision:** no new ADR proposal is justified by P4.11. Creating one now would standardize a mechanism the Accepted architecture intentionally leaves replaceable.

The ADR gate remains armed for future implementation. A later durable/stable choice must be recorded before it becomes accidental architecture.

## 9. Accessibility / usability / material operator-error review

Result: **`PASS — bounded semantic/textual baseline; no new material operator-error finding.`**

P4.11 rechecks the error classes most likely to convert technically correct governance into unsafe operator behavior:

- blocked states remain explicit text and use alert semantics in current inert renderers;
- current navigation is textually/programmatically identifiable;
- governed values are escaped before HTML rendering;
- exact object/version, authority/source, gate/action state and blocking reason remain distinguishable;
- `Request governed action`, `Re-inspect current access` and `Action unavailable` do not imply approval or Organizational Authority;
- unavailable/reinspection states do not expose protected content merely to improve UX.

No material accessibility/usability defect was found within the declared reference baseline. P4.11 does not claim formal WCAG conformance, production keyboard/focus/contrast/zoom/screen-reader testing, localization validation or end-user usability certification. Those require the later real frontend boundary and appropriate evidence.

## 10. Performance and optimization disposition

Result: **`No performance architecture justified.`**

There is no reproducible performance evidence in the bounded Phase 4 reference implementation requiring:

- durable caching;
- prefetching;
- denormalized workspace read models;
- asynchronous UI projection infrastructure;
- search/vector technology selection;
- independent workspace service scaling;
- speculative batching or concurrency architecture.

P4.11 intentionally adds none of these. Performance work remains evidence-triggered rather than architecture-by-anticipation.

## 11. Product Contract, capability lifecycle and commercial disposition

P4.11 changes none of the following states:

- `P4.08 Bounded Product Entry Product Contract` remains `Provisional 0.1.0`;
- CAP-001 through CAP-004 remain `Incubating / Provisional`;
- no Workspace capability is promoted to `Active`;
- no Stable Product Contract or public interface is created;
- no operational-readiness or production claim is made;
- no formal accessibility/conformance claim is broadened;
- no SLA, support, compatibility or commercial commitment is created.

P4.11 completion is therefore a bounded architecture/refactoring gate only. P4.12 remains responsible for the separate M4 closure decision.

## 12. Executable and hosted P4.11 hardening evidence

P4.11 adds:

- `reference/python/tests/test_p4_11_workspace_hardening_adr_refactoring_review.py`.

The guard verifies:

1. R12-F1 replacement authorization cannot self-advance stale presentation continuity;
2. product-domain task/disposition semantics remain outside the shared Phase 4 package;
3. product consequential action still routes through R10 rather than directly through P4.05;
4. capability-specific semantic-owner checks remain present and are not replaced by `authority_safe_ux`;
5. reconstruction/search/workspace presentation remains explicitly non-authoritative;
6. reviewed Phase 4 modules select no concrete frontend/API/serialization/IAM/persistence/cache/search/service technology that silently crosses the ADR gate;
7. semantic accessibility/operator-error safeguards remain textual and explicit;
8. the P4.08 Product Contract remains `Provisional 0.1.0` with no inferred Stable boundary.

Hosted pre-synchronization validation on PR #60 head `27b663ba643ecc7ca06a0318c47d0fa9f10993c8`:

```text
Reference Python CI #197
Runner: Ubuntu 24.04.4
Python: CPython 3.12.13
Command: python -m unittest discover -s tests -v
Result: Ran 570 tests — OK
```

This validates all seven new P4.11 test methods together with the complete existing reference suite. Canonical roadmap synchronization follows that evidence. PR merge remains conditional on a green final synchronized-head CI run; that merge control does not change the P4.11 architecture/refactoring disposition.

These guards protect the current reviewed decision, not an eternal ban on later governed architecture change. A legitimate future ADR/refactor/stable-boundary decision must update the guard together with the canonical decision.

## 13. Functional cross-review iterations

### Iteration 1 — architecture / product-platform boundary

Finding: no product-domain semantic has leaked into `arvectum_os_ref`; the product composition remains outside the platform package and retains the Provisional Product Contract boundary.

Disposition: no boundary move or generic product orchestrator is justified.

### Iteration 2 — security / authority / stale presentation

Finding: R12-F1 remains the material stale-presentation invariant. No reviewed action-bypass path around R10/Governed Execution is present.

Disposition: preserve R12-F1 as deterministic P4.11 regression evidence; retain independent semantic-owner and action-freshness controls.

### Iteration 3 — refactoring / derived state / performance

Finding: source-authorization matching duplication is real, but its callers own different data-governance/freshness/reliance responsibilities and no post-R12 inconsistency demonstrates a safe broader abstraction. No measured performance issue justifies cache/read-model architecture.

Disposition: no runtime refactor; keep `authority_safe_ux` narrow, record the shared evidence DTO placement as a watch item, and avoid speculative performance infrastructure.

### Iteration 4 — ADR / accessibility / delivery

Finding: no durable frontend/API/serialization/IAM/cache/search/service choice crosses an ADR threshold; the bounded textual accessibility/operator-error baseline remains intact without creating unsupported WCAG claims. Hosted CI #197 passes the full 570-test reference suite.

Disposition: no ADR; synchronize the canonical roadmaps to P4.12 and require final synchronized-head CI before merge. P4.12 remains a closure decision rather than an implementation expansion.

No material objection remains after iteration 4.

## 14. Exit assessment

P4.11 exit conditions are satisfied:

- [x] presentation-domain/product-platform boundary reviewed;
- [x] refactoring threshold reviewed against repeated workspace evidence;
- [x] Authorization/Organizational-Authority/action-bypass surfaces reviewed;
- [x] derived-state/cache/read-model authority risks reviewed;
- [x] frontend/API/serialization/BFF/IAM/storage/search/service ADR triggers reviewed;
- [x] accessibility/usability material operator-error risks reviewed;
- [x] R12-F1 preserved as a fixed executable regression invariant;
- [x] P4.09 helper retained as a narrow decision consumer;
- [x] no performance architecture introduced without reproducible evidence;
- [x] full Reference Python suite green on the P4.11 pre-synchronization implementation/review head (`#197`, `570 tests`, `OK`);
- [x] canonical Roadmap and Phase 4 roadmap synchronized to P4.11 completion / P4.12 current action.

**Final P4.11 decision: `PASS — no material runtime refactor or ADR is required before P4.12; preserve the current bounded workspace architecture and R12-F1 invariant.`**

## 15. Handoff

Proceed to:

> **`P4.12 — Phase 4 / M4 closure review`.**

P4.12 must decide whether the bounded accumulated evidence is sufficient to declare M4 achieved. It must not use closure to infer `Active` capability lifecycle, Stable Product Contract/public API status, production readiness, formal WCAG conformance, full-platform conformance or commercial commitments.
