# P4.10 — Workspace Architecture Fitness + Accessibility / Usability Baseline

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-09`
Updated: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P4.10 — Workspace architecture fitness + accessibility/usability baseline`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — P4.02–P4.09 satisfy the declared 14-dimension M4 workspace fitness matrix for the bounded reference scope; critical operator states remain fail-closed and deterministically specified; core rendered journeys preserve textual object/version/authority/action/blocking meaning; shared workspace code remains domain-neutral and presentation boundaries remain internal, reversible and technology-neutral.`**

## 1. Purpose and decision level

P4.10 is the cross-cutting fitness gate over the accumulated Phase 4 workspace baseline. It does not introduce another workspace semantic owner. It asks whether the existing P4.02–P4.09 slices compose safely and intelligibly enough to proceed to `R12 — M4 Workspace Hardening`.

This review is subordinate implementation/review evidence. It does not amend Constitution or an Accepted RFC, create a new Platform Capability, stabilize the P4.08 Product Contract, select a frontend/API/IAM/storage technology, establish production readiness, or claim full accessibility/WCAG or full-platform conformance.

## 2. Canonical authority checked

P4.10 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral shared platform behavior, explicit authority, security/isolation, Governed Execution, Product Contract boundary, technology independence, proportional architecture and scoped fitness/conformance;
4. RFC-0002 — stable Subject Identity, immutable exact Version Identity, Head/Effective distinction, relationship non-authority, projection non-authority and consequential exact-version pinning;
5. RFC-0003 — explicit Organization scope, attributable Actor, deny-by-default/fail-closed authorization, Authorization versus Organizational Authority separation, purpose/minimization and tenant isolation;
6. RFC-0004 — explicit Product Contract boundary, dependency continuity, no hidden platform coupling and product-owned domain semantics;
7. RFC-0005 — exact governed input/Workflow/Product Contract pins, separate gates and consequential mutation only through Governed Execution;
8. RFC-0006 — Event/provenance/reconstruction honesty and non-authoritative telemetry/projections;
9. RFC-0007 — Observation/Memory/Candidate/Knowledge distinctions, validation/approval separation, freshness/exact reliance and Search/RAG non-authority;
10. RFC-0008 — Document/Version/Artifact/authority/provenance distinctions and non-authoritative derived representations;
11. `docs/adrs/README.md` — no applicable Accepted ADR constrains the current bounded internal workspace implementation;
12. P4.01–P4.09 reviews plus R9, R10 and R11;
13. `P4.08 Bounded Product Entry Product Contract` — remains `Provisional 0.1.0`;
14. canonical Roadmap `2.22.0` and Phase 4 roadmap `1.12.0` at P4.10 start;
15. GitHub issue #54 — hosted-runner/account provisioning gap, treated as tooling evidence only and not as architectural authority.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

## 3. Executable P4.10 evidence

P4.10 adds:

- `reference/python/tests/test_p4_10_workspace_architecture_fitness_accessibility_usability.py`.

The test is deliberately a cross-cutting guard rather than a new runtime abstraction. It combines deterministic behavioral checks for security-critical P4.02/P4.09 states with structural checks across P4.03–P4.08/R10/R11 boundaries.

It verifies:

- the complete 14-dimension fitness inventory is explicit and unique;
- missing, denied, ambiguous and wrong-Organization source-authorization evidence converge on one minimized unavailable state;
- replaced authorization evidence requires re-inspection and cannot retain source/preview visibility;
- unresolved Organization context produces an alerting blocked state without enabled navigation;
- rendered core workspace surfaces escape governed text and expose blocked meaning textually;
- object/Subject/exact Version/Head, authority/source, requested action and blocking/gate reason remain distinguishable rather than flattened into one ambiguous status;
- the bounded product composition keeps exact Product Contract, Actor, Organization and task-target continuity;
- consequential product action still routes through R10 and the P4.05/Governed Execution path;
- product-domain task semantics remain outside the shared platform package;
- no durable frontend/API/IAM/storage dependency is selected by the reviewed presentation boundary;
- P4.09 source-authorization decision consumption remains narrow rather than silently becoming a policy/IAM owner.

The new test source was syntax-compiled before publication. A green hosted execution is **not** claimed: the repository's separately tracked issue #54 remains an account/runner provisioning limitation. P4.10 therefore records deterministic executable coverage without misrepresenting hosted execution evidence.

## 4. M4 workspace fitness matrix

| # | Dimension | Evidence / disposition | Result |
|---:|---|---|---|
| 1 | Organization isolation | P4.02 requires explicit Organization; mismatched/unresolved scope fails closed; P4.03–P4.07 re-check source-owned Organization/context rather than trusting presentation or identifier syntax | PASS |
| 2 | Identity attribution | Workspace preserves actual Principal, represented Principal when applicable and Organization across navigation/action composition | PASS |
| 3 | Authorization vs Organizational Authority separation | P4.03–P4.09 consume authorization evidence but do not manufacture Organizational Authority; P4.05 keeps authorization, authority and approval/gate evidence distinct | PASS |
| 4 | Canonical-versus-derived state distinction | Workspace presentation is non-authoritative; reconstruction/replay and Search are explicitly derived; Document working candidates and transient outputs remain non-canonical | PASS |
| 5 | Exact-version visibility/reliance | Subject vs exact Version, Head vs Effective and exact historical references remain visible; consequential reliance remains exact-version pinned where required | PASS |
| 6 | Provenance/reconstruction honesty | P4.04 keeps Event/evidence/provenance/correlation/causation distinct and exposes redacted/deleted/missing/unavailable limitations without fabrication | PASS |
| 7 | Product Contract boundary integrity | P4.08/R11 preserve exact Provisional Product Contract/dependency/Actor/Organization/task continuity and no hidden platform-internal dependency | PASS |
| 8 | Document/Artifact authority semantics | P4.06 preserves logical Document, immutable Document Version, Artifact, rendition, authority/source, provenance and exact-reliance distinctions | PASS |
| 9 | Knowledge/Search non-authority | P4.07 preserves Observation/Memory/Candidate/Knowledge roles, validation vs approval, freshness, authority and derived Search projection semantics | PASS |
| 10 | Fail-closed action paths | P4.05 + R10 require current source access plus Governed Execution gates; changed/revoked/ambiguous access requires re-inspection and no alternate product mutation path is exposed | PASS |
| 11 | Product-domain neutrality of shared workspace | Product task/disposition/operation meaning remains in `bounded_product_ref`; `arvectum_os_ref` does not import the bounded product package | PASS |
| 12 | Accessibility baseline for core journeys | Core renderers use semantic headings/regions or sections, textual status, alert semantics for blocked states, native button semantics where buttons exist, textual exact-version/authority/gate meaning and escaped governed content; critical meaning is not color-only | PASS — bounded baseline |
| 13 | Deterministic testability of critical states | P4.10 directly encodes deterministic unavailable/reinspection/blocked states and structural choke-point guards; issue #54 is recorded separately and does not waive coverage | PASS for deterministic specification; hosted-run evidence unavailable |
| 14 | Portability/reversibility of presentation boundaries | Phase 4 adapters remain internal/inert and select no stable frontend, route/BFF/API, IAM provider, durable read model, search/vector store or presentation service topology | PASS |

No dimension requires a new RFC, ADR, Product Contract version or capability lifecycle change.

## 5. Accessibility baseline

P4.10 establishes a **bounded reference accessibility baseline**, not a claim of formal WCAG conformance or production UX certification.

For the current static/inert reference surfaces, the baseline is:

1. critical workspace context is textual: Organization, Actor and reference kind are understandable without color;
2. blocked/error states have explicit human-readable reason text and programmatic alert semantics where rendered;
3. current navigation state is programmatically identifiable (`aria-current`) and navigation has a textual accessible label;
4. native interactive elements are used for the bounded shell control semantics rather than inaccessible custom click targets;
5. governed identity/content text is HTML-escaped before rendering;
6. exact Version, authority/source, lifecycle/freshness/provenance and gate meaning are represented in text where material;
7. action labels describe operator intent/state (`Request governed action`, `Re-inspect current access`, `Action unavailable`) and do not claim approval or authority;
8. unavailable protected content does not expose protected counts, hidden previews or sensitive existence details merely to make the UI more informative;
9. presentation state is explicitly identified as non-authoritative;
10. the baseline is technology-neutral and can be reimplemented in a later frontend without treating current HTML or Python DTO shape as a stable public contract.

Formal keyboard-flow, focus-management, contrast, zoom/reflow, screen-reader matrix, localization and production visual-design validation remain appropriate when a real frontend/runtime is selected. P4.10 does not pre-select that technology or overclaim those untested properties.

## 6. Usability baseline for core operator journeys

The minimum semantic usability question is whether an operator can answer four things without reverse-engineering hidden implementation state:

1. **What am I looking at?** — logical object/role and stable Subject identity where applicable;
2. **Which exact state/version is relevant?** — exact displayed Version and Head/Effective/exact-reliance distinctions where material;
3. **Where does authority/evidence come from?** — authority mode/source plus provenance/evidence/freshness semantics where applicable;
4. **What can I request now, and why is it available/blocked/awaiting?** — action label/readiness plus separate gate/access/reinspection reason.

Disposition by core journey:

| Journey | Semantic usability result |
|---|---|
| Scoped workspace/navigation | Organization + Actor + destination + Subject/exact-Version reference are explicit; unresolved scope blocks the workspace |
| Canonical Record / Relationship inspection | object kind, Subject, exact displayed Version, Head, Effective state, authority/source and relationship direction/roles remain distinct |
| Event / provenance / reconstruction | exact evidence versions, provenance, correlation/causation and evidence limitations are explicit; reconstruction/replay remains derived |
| Governed Execution / action | exact Execution Version, Workflow/material-input/Product Contract pins, gate outcomes, action readiness and commit result remain separate |
| Document / Artifact | Document/Version/Artifact/rendition/authority/exact-reliance distinctions remain visible; working candidates stay non-canonical |
| Memory / Knowledge / Search | epistemic role, version, provenance, freshness, validation, approval, authority and derived Search status remain distinct |
| Product Contract-backed composition | product task meaning remains product-owned while shared Document/Knowledge/action semantics retain their owning representations |
| Authority-safe presentation | unavailable/reinspection/available states are textual, minimized and do not manufacture permission, approval or authority |

Result: `PASS` for semantic usability of the bounded reference workspace. This is not a claim that a production visual UI has completed user testing.

## 7. P4.09 reuse decision

R11 identified repeated matching of `CurrentSourceAuthorization` as real bounded duplication. P4.09 then proved that the common visibility decision can be represented safely as a narrow **consumer** of already-produced authorization evidence.

P4.10 finds that a broad migration of P4.03–P4.07/R10 to this helper is **not yet justified**.

Reason:

- P4.04 still owns exact evidence purpose/right/classification enforcement and reconstruction constraints;
- P4.06 still owns Artifact handling/purpose/right/classification and exact Document reliance;
- P4.07 still owns Knowledge freshness, validation/approval and exact Knowledge reliance;
- R10 has a stricter stale-decision action-safety responsibility immediately before consequential execution;
- centralizing these paths now would save small matching code while increasing the risk that a presentation helper is mistaken for the authorization/data-governance owner.

Disposition: keep `authority_safe_ux.consume_current_source_authorization()` as a narrow internal presentation primitive; retain existing callers unchanged through P4.10; allow P4.11 to reconsider a lower-level shared decision-matching utility only if it can preserve semantic-owner checks explicitly and materially reduce inconsistency.

This is validated reuse over speculative generality, not acceptance of duplicate authorization policy.

## 8. ADR / Product Contract / capability disposition

No ADR threshold is crossed by P4.10.

The reviewed workspace still establishes no durable or externally constraining choice for:

- frontend/runtime framework;
- public route/deep-link scheme;
- REST/GraphQL/gRPC/BFF interface;
- stable wire/serialization contract;
- authentication/session/IAM provider or policy engine;
- durable workspace/read-model/cache store;
- search/vector/RAG technology;
- Document/object-store/OCR/signing topology;
- stable design-system compatibility surface;
- separately deployable UI/workspace service topology.

The P4.08 Product Contract remains `Provisional 0.1.0`.

CAP-001 through CAP-004 remain `Incubating / Provisional`. P4.10 does not make them `Active`, establish operational readiness, create SLA/support commitments, or broaden conformance claims.

## 9. Cross-review iterations

### Iteration 1 — architecture / semantic ownership

Finding: adding a new generic workspace-fitness runtime or common authorization framework would duplicate semantic owners rather than prove fitness.

Disposition: P4.10 adds cross-cutting executable/review evidence only; no new runtime abstraction or public contract.

### Iteration 2 — security / privacy / authority

Finding: usability pressure can turn counts, previews, stale access decisions or labels into side channels or implied authority.

Disposition: deterministic tests require unavailable/ambiguous/wrong-Organization states to expose no content/count/preview, and replaced decision evidence requires re-inspection. Existing purpose/right/classification/freshness/exact-reliance owners remain intact.

### Iteration 3 — accessibility / operator comprehension

Finding: technical correctness alone is insufficient if the operator cannot distinguish object/version/authority/action/blocking reason without color or internal state knowledge.

Disposition: the baseline requires textual context/status, blocked alert semantics, current navigation semantics, exact version/authority/gate wording and safe action labels. Formal production accessibility certification remains deferred until a real frontend exists.

### Iteration 4 — engineering / reversibility / ADR pressure

Finding: a cross-cutting UX baseline can accidentally stabilize the current Python/HTML representation.

Disposition: tests protect semantic behavior and absence of durable technology dependencies, not CSS, route shape, component library or DTO compatibility. No ADR trigger is crossed.

No material finding remained after iteration 4 for the declared P4.10 scope.

## 10. Exit criteria

P4.10 exit criteria are satisfied:

- [x] all 14 declared fitness dimensions have explicit disposition and executable guards;
- [x] core operator journeys preserve object/version/authority/action/reason semantics;
- [x] critical unavailable/reinspection states are deterministic and fail closed;
- [x] accessibility baseline is stated without unsupported formal-conformance claims;
- [x] presentation boundaries remain reversible/technology-neutral;
- [x] product-domain meaning remains outside shared workspace code;
- [x] P4.09 helper reuse has an explicit evidence-based disposition;
- [x] no RFC/ADR/Product Contract/capability lifecycle change is required;
- [x] hosted CI limitation is recorded without inventing a green run.

## 11. Handoff

P4.10 is complete with `PASS`.

The next canonical engineering gate is:

> **`R12 — M4 Workspace Hardening`.**

R12 should treat this matrix and baseline as regression evidence, re-check remaining cross-cutting hardening gaps and decide whether any finding must be repaired before P4.11 and final P4.12/M4 closure.
