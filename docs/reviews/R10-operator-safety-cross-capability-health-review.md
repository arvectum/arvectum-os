# R10 — Operator Safety / Cross-Capability Health Review

Status: `Complete / PASS`
Date: `2026-08-08`
Roadmap gate: `R10`
Scope: accumulated Phase 4 operator experience through `P4.07`
Task classification: `platform` with a bounded `governance` review dimension
Capability lifecycle effect: `None`
ADR effect: `None`

## 1. Review purpose

R10 is the mandatory Phase 4 engineering health gate between P4.07 and P4.08.

The review asks whether the operator experience accumulated across P4.03–P4.07 still preserves one coherent safety model before task/context composition starts joining those surfaces together.

The review is deliberately narrower than a new architecture exercise. It does not create a public frontend/API contract, does not establish a new authorization engine, does not change Product Contract semantics, does not promote an Incubating capability, and does not reopen Accepted architecture without evidence.

The required review dimensions are:

- Organization and Actor scoping;
- current source authorization;
- purpose, rights, classification and minimization;
- exact-version reliance;
- canonical versus derived/presentation authority;
- stale presentation and stale action behavior;
- duplicate or ambiguous sources;
- protected counts/previews and hidden actions;
- repeated presentation/access implementation patterns;
- cross-capability code health and accidental-contract risk.

## 2. Canonical basis checked

R10 was checked against the current canonical repository state before implementation.

Binding sources:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001 `1.0.0` — `Accepted`;
- RFC-0002 `1.0.0` — `Accepted`;
- RFC-0003 `1.0.0` — `Accepted`;
- RFC-0005 `1.0.0` — `Accepted`, including the owner-approved incorporated proposal;
- RFC-0006 `1.0.0` — `Accepted`, including the owner-approved incorporated proposal;
- RFC-0007 `1.0.0` — `Accepted`, including the owner-approved incorporated proposal;
- RFC-0008 `1.0.0` — `Accepted`, including the owner-approved incorporated proposal;
- RFC Index;
- ADR Index;
- Phase 4 roadmap and the P4.03–P4.07 review records.

No Accepted ADR currently constrains this bounded operator-experience implementation further.

The current Decision Authority Policy remains `Proposed`; R10 therefore does not use it as normative authority and creates no new delegated authority.

## 3. Cross-capability inventory reviewed

| Area | Current owner / surface | R10 result |
| --- | --- | --- |
| Canonical Record / relationship inspection | P4.03 / `canonical_inspection.py` | Pass |
| Version / Event / provenance reconstruction | P4.04 / `provenance_inspection.py` | Pass |
| Governed Execution / gate / action experience | P4.05 / `execution_action_experience.py` | Pass after bounded remediation |
| Document / Artifact workspace | P4.06 / `document_artifact_experience.py` | Pass |
| Memory / Knowledge / Search discovery | P4.07 / `memory_knowledge_search_experience.py` | Pass |
| Cross-capability operator action freshness | R10 / `operator_safety.py` | Added as bounded internal guard |

The review also re-read the P4.03–P4.07 implementation reviews rather than inferring safety only from current code shape.

## 4. Findings

### 4.1 Organization and Actor source authorization — PASS after one material correction

P4.03–P4.07 consistently bind protected presentation to the current Workspace Organization and Actor, including represented-principal context where applicable.

The inspection surfaces fail closed on missing, denied, duplicate/ambiguous or wrong-Actor source authorization before protected content or exact-version existence is disclosed.

One material gap was found in the accumulated P4.05 action path:

1. P4.05 inspection correctly consumed one current source-access decision;
2. the successful inspection stored the exact `source_authorization_decision_version_id`;
3. P4.05 action preparation and execution correctly rechecked Workspace Actor/Organization, Governed Execution state, gates, runtime head/conflict state and idempotency;
4. however, a prepared operator action did not itself require the source-access decision used by the inspected presentation to remain the unique current allow decision.

Therefore an internal action intent could survive source-access revocation or replacement between inspection and later operator action invocation.

This did **not** bypass RFC-0005 Governed Execution authorization, Organizational Authority or consequential approval gates. It was nevertheless an operator-safety defect: stale presentation access could leave a hidden/stale action affordance viable after the presentation access assumption had changed.

That conflicts with the R10 stale-presentation/hidden-action purpose and with RFC-0003 revocation/cached-decision rules and RFC-0005 gate re-evaluation semantics.

#### Remediation

R10 adds `reference/python/arvectum_os_ref/operator_safety.py`.

The guard:

- remains internal and non-authoritative;
- binds an operator action to the exact source-authorization decision Version Identity used by the inspected P4.05 view;
- requires that decision to remain the unique current allow decision during action preparation;
- rechecks the same exact decision immediately before delegating the commit request;
- fails closed if access is missing, denied, ambiguous or replaced;
- requires re-inspection after any decision change, including allow → newer allow;
- grants no authorization, Organizational Authority or approval;
- does not implement canonical mutation itself;
- delegates the only consequential action path to the existing P4.05 adapter, which in turn delegates to the existing governed runtime consistency path.

A structural regression test also prevents future package modules from calling the lower-level P4.05 action preparation/execution functions directly outside `execution_action_experience.py` and `operator_safety.py`.

This is intentionally a composition guard, not a new policy engine.

### 4.2 Purpose, rights, classification and minimization — PASS

The reviewed surfaces preserve the separation between source visibility and handling/use constraints.

Important current behavior:

- P4.06 independently applies P3.07 purpose/right/classification constraints to Artifact metadata after Document source authorization;
- P4.07 applies Organization, authorization, purpose, rights, classification, lifecycle/freshness and minimization constraints to Memory/Knowledge retrieval and search;
- exact Document and exact Knowledge reliance paths re-evaluate current access conditions rather than treating earlier rendering as permanent permission;
- derived previews are minimized;
- blocked or omitted protected items do not reveal protected counts;
- content bytes, protected locators and equivalent sensitive implementation details are not exposed merely because metadata is inspectable.

No cross-capability rule was found that treats successful rendering as unrestricted subsequent use.

### 4.3 Exact-version reliance — PASS

The accumulated operator experience preserves the RFC-0002/RFC-0005 distinction between navigation/discovery and consequential reliance.

Observed invariants:

- subject/head navigation remains appropriate for browsing;
- exact historical versions can be inspected where authorized;
- consequential Document reliance requires explicit exact Document Version selection and current access rechecks;
- consequential Knowledge reliance requires explicit exact Knowledge Version selection and current source/freshness/access rechecks;
- derived search hits exit discovery only through current exact governed source resolution;
- P4.05 action intent pins exact governed execution and expected canonical head state;
- stale or conflicting canonical head state is blocked by the existing runtime consistency path.

No mutable search hit, preview, current-head alias or presentation row becomes a substitute for the exact materially relied-upon governed Version Identity.

### 4.4 Canonical versus derived/presentation authority — PASS

All reviewed P4.03–P4.07 workspace surfaces continue to declare `PresentationAuthority.NON_AUTHORITATIVE`.

The following remain derived/non-authoritative:

- rendered workspace inspection;
- provenance reconstruction presentation;
- operator action intent;
- document/artifact presentation;
- search projection, ranking and preview;
- RAG-like discovery state;
- working candidates and transient generated/presentation state.

R10's new operator-safety intent is also explicitly non-authoritative.

No cache, index, preview, renderer, search order, approval label, UI role label or repeated display is promoted into canonical authority.

### 4.5 Duplicate or ambiguous source handling — PASS

Across the reviewed surfaces, multiplicity is treated as an ambiguity to fail closed or omit safely rather than as permission to choose a convenient source.

Examples include:

- current source authorization requires one unambiguous matching decision;
- exact canonical sources/lineages are not silently selected when duplicates exist;
- duplicate exact Memory/Knowledge representations are not accepted as reliable exact reliance;
- document admitted-version and manifest evidence must resolve unambiguously;
- search discovery re-resolves derived hits against current exact governed sources.

R10 extends the same rule to operator action freshness: multiple matching source-access decisions do not create a usable action.

### 4.6 Stale presentation and hidden actions — PASS after remediation

Before R10, stale governed data itself was already handled in the reviewed read/reliance surfaces, but the P4.05 operator action presentation had the freshness gap described in Section 4.1.

After remediation:

- an action prepared from an inspected execution is bound to the exact inspected source-access decision;
- a newer replacement decision invalidates the old prepared action even if the replacement is also an allow;
- revocation, missing access and ambiguous access all block without mutation;
- the operator receives a generic re-inspection requirement rather than protected detail about why the decision changed;
- runtime state remains unchanged when the freshness guard blocks;
- future cross-capability package modules are structurally prevented from bypassing this guard through direct use of the lower-level P4.05 action adapter.

This closes the material R10 hidden-action finding before P4.08 composes real task/context entry points.

### 4.7 Protected counts and previews — PASS

The review found no justified need to expose counts of denied/omitted protected resources.

Current bounded surfaces prefer statements such as omitted/unavailable without disclosing whether the protected set contains zero, one or many resources.

Search previews remain minimized and are derived presentation only.

R10 adds no aggregate count, hidden-card count, authorization diagnostic count, raw retry token, protected locator or hidden source identity disclosure.

### 4.8 Repeated presentation/access patterns — no broad refactor justified yet

P4.03–P4.07 contain repeated local patterns for:

- matching Organization/Actor/represented-principal source authorization;
- fail-closed uniqueness;
- non-authoritative presentation;
- access-context matching;
- generic blocked states.

The repetition is visible.

R10 does **not** extract a general shared authorization/presentation framework yet because:

1. each capability still has materially different semantic owners and downstream handling checks;
2. authorization decision production remains outside these experience adapters;
3. a premature common abstraction could accidentally become a public/internal policy contract;
4. P4.08 is the first point where real cross-capability task/context composition can provide evidence about which part of the pattern is actually stable.

The only refactor admitted by R10 is the bounded operator-action freshness guard because a concrete safety defect justified it.

P4.08 MAY reuse the R10 guard but MUST NOT generalize it into a public authorization API without separate evidence and the appropriate architecture/governance level.

## 5. Security and authority interpretation

R10 does not introduce a new authorization decision.

`CurrentSourceAuthorization` remains consumed evidence supplied to the presentation/composition boundary. The new guard only verifies that the exact decision already relied upon by the inspected operator context is still current and uniquely allowed.

The layers remain distinct:

```text
source visibility / current access
        ↓
non-authoritative operator presentation
        ↓
R10 source-access freshness guard
        ↓
P4.05 Governed Execution action adapter
        ↓
authorization / Organizational Authority / approval gates
        ↓
existing runtime consistency / canonical mutation path
```

The R10 guard MUST NOT be represented as satisfying Governed Execution authorization, Organizational Authority or approval.

## 6. Product/platform boundary

R10 is platform engineering work over existing domain-neutral workspace/capability semantics.

It introduces:

- no product-domain workflow;
- no product role or entitlement;
- no Product Contract;
- no customer-specific behavior;
- no new shared business schema.

P4.08 remains responsible for introducing the first bounded Product Contract-backed product entry point.

R10 merely makes the shared operator action composition safer before that boundary is used.

## 7. Capability lifecycle and commercial interpretation

R10 changes no capability lifecycle status.

In particular, it does not make CAP-001, CAP-002, CAP-003 or CAP-004 `Active`.

R10 is an engineering health gate only. It creates no production-readiness, SLA, support, portability or commercial-conformance claim.

## 8. ADR disposition

No ADR is required by R10.

The remediation:

- selects no framework;
- selects no frontend stack;
- selects no API protocol;
- selects no IAM/policy engine;
- selects no database or persistence model;
- selects no broker/cache/search technology;
- creates no durable external integration contract.

It is a small reversible internal composition adapter and regression boundary.

An ADR should be reopened only if later P4 work introduces a durable/external choice that materially constrains portability, supported public interfaces, tenant isolation, persistence or migration.

## 9. Regression evidence

R10 adds:

- `reference/python/arvectum_os_ref/operator_safety.py`;
- `reference/python/tests/test_r10_operator_safety_cross_capability_health.py`;
- `reference/python/tests/test_r10_operator_action_entrypoint_guard.py`.

The regression suite covers:

1. exact source-access decision binding;
2. normal safe commit delegation;
3. allow-decision replacement before preparation;
4. revocation before execution;
5. missing access before execution;
6. duplicate/ambiguous current access before execution;
7. allow-decision replacement before execution;
8. no mutation while blocked;
9. no direct canonical mutation path in the guard;
10. no frontend/network/storage technology commitment;
11. non-authoritative presentation across accumulated P4 surfaces;
12. exact Document/Knowledge reliance signatures retaining current source and handling rechecks;
13. a package-level structural guard preventing future direct bypass of the R10 operator-safety entry path.

Existing P4.03–P4.07 tests remain the primary detailed conformance evidence for each capability-specific surface.

## 10. Cross-review iterations

The R10 review used role-based functional perspectives as a development method only. These perspectives are not approval evidence and do not imply that named employees or external professionals performed the review.

### Iteration 1 — Architecture / canonical-state review

Question:

> Have P4.03–P4.07 accidentally made presentation, search, reconstruction or action intent authoritative?

Result:

- no canonical/derived collapse found;
- exact-version reliance remains explicit;
- existing canonical mutation path remains single-owner;
- no material correction required.

### Iteration 2 — Security / privacy / operator-safety review

Question:

> Can stale access, duplicate source evidence, hidden state or derived presentation survive in a way that broadens future operator action?

Result:

- one material finding: P4.05 action intent could survive replacement/revocation of the source-access decision used by its inspected presentation;
- correction required.

### Iteration 3 — Remediation architecture review

Question:

> Can the finding be fixed without creating a second authorization engine or mutation path?

Result:

- yes;
- bounded `operator_safety.py` composition guard selected;
- exact source-access decision pin + prepare-time recheck + pre-delegation recheck;
- lower-level P4.05 Governed Execution action ownership preserved.

### Iteration 4 — Product / UX / information-disclosure review

Question:

> Does the correction expose protected decision reasons/counts, convert access into authority, or create product-specific semantics?

Result:

- no protected counts or decision diagnostics added;
- blocked result is generic and requires re-inspection;
- no new product semantics or Product Contract created;
- no material correction required.

### Iteration 5 — Engineering / maintainability / ADR review

Question:

> Does R10 need a broader refactor or ADR before P4.08?

Result:

- repeated local access/presentation patterns are visible, but evidence is insufficient for a broad shared abstraction;
- structural entrypoint regression is sufficient to prevent future action bypass;
- no durable technology choice exists;
- no ADR required;
- no further material correction identified.

The loop stops after iteration 5 of maximum 7 because no unresolved material issue remains within the R10 scope.

## 11. R10 exit criteria

| Exit criterion | Result |
| --- | --- |
| Organization/Actor source authorization reviewed consistently | PASS |
| purpose/rights/classification/minimization reviewed | PASS |
| exact-version reliance reviewed | PASS |
| canonical-vs-derived distinction preserved | PASS |
| stale presentation/action reviewed | PASS after remediation |
| duplicate/ambiguous sources fail closed | PASS |
| protected counts/previews reviewed | PASS |
| hidden operator action after source-access change blocked | PASS after remediation |
| repeated patterns reviewed without premature public abstraction | PASS |
| no new authority created | PASS |
| no capability promotion | PASS |
| ADR gate evaluated | PASS — no ADR required |
| P4.08 safe to start after CI confirms repository regression suite | PASS |

## 12. Result

**R10 result: PASS.**

The accumulated P4.03–P4.07 operator experience is healthy enough to proceed to P4.08 after repository CI confirms the R10 regression suite.

The material stale-source-access action gap found during review has been closed at the cross-capability operator composition boundary without changing Accepted architecture, creating new authority or introducing a second canonical mutation path.

The next roadmap item is:

**P4.08 — Cross-capability task/context composition + bounded Product Contract-backed product entry point.**
