# R31 — Product Composition / AI Safety Review

Status: `Complete / PASS`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Reviewed integration scope: `P9.07` through `P9.10`
Predecessor: `P9.10 — Complete / PASS`
Next canonical action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Canonical baseline checked

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- direct review authorities: RFC-0003, RFC-0004, RFC-0005, RFC-0006, RFC-0007 and RFC-0008;
- ADR-0001 — `Accepted` for the exact private internal Productive Workspace topology;
- P6.02 — `Provisional 0.1.0`, with approved repository-locator reconciliation to `arvectum/tender-agent`;
- P6.06 — `Provisional 0.1.0` for Discount Parser;
- canonical roadmap `2.85.0` and Phase 9 roadmap `1.12.0` at review start.

No Constitution amendment, new RFC/ADR, Product Contract lifecycle transition or Platform Capability promotion is required by this review. R31 is a review gate, not lifecycle authority.

## 2. Review question

R31 asks whether the integrated P9.07–P9.10 Workspace can continue into real daily-use dogfooding without introducing any of the following through composition rather than through an individually reviewed feature:

1. product/domain semantics leaking into shared Kernel/platform authority;
2. hidden coupling through product databases, private tables, undocumented endpoints/imports/streams, credentials or implicit shared state;
3. Product Contract or Platform Capability lifecycle promotion by UI/composition success;
4. cross-Organization scope expansion or protected metadata leakage;
5. source-authority or provenance flattening;
6. Observation / Organizational Memory / Knowledge Candidate silently presented as validated Knowledge or organizational fact;
7. AI synthesis presented as sourced evidence, permission, approval or Organizational Authority;
8. AI-generated output becoming Memory/Knowledge/canonical state without governed promotion;
9. AI or presentation layers selecting, triggering or shortcutting an unrelated consequential Governed Execution;
10. Activity/notification presentation being mistaken for canonical Event history, audit authority or a new priority/approval system.

## 3. Integrated boundary review

### 3.1 Product composition — P9.07

**Result after review: PASS.**

The shared `arvectum.workspace.product-composition/1` envelope remains domain-neutral and read-only. The current server adapters are explicit, release-scoped adapters over retained evidence for exactly two Product Contract contours; the browser product registry is explicit compile-time composition rather than dynamic/private product access.

P6.02 keeps procurement/tender semantics product-owned and admits only its declared CAP-001/CAP-004 reliance. P6.06 keeps Offer/source/classification/deduplication/scheduler/Telegram/publication semantics product-owned and admits only the declared bounded CAP-004 reliance. The Workspace adapters do not import product databases or domain models and expose no product external-effect command.

The approved P6.02 repository-locator reconciliation resolves the current implementation repository as `arvectum/tender-agent` without changing P6.02 lifecycle or semantic scope. No hidden-coupling finding remains for the current exact composition.

### 3.2 AI Copilot — P9.08

**Initial result: FAIL with two material findings. Post-remediation result: PASS.**

The underlying retrieval boundary was already strong: server-resolved Organization/Actor scope, current authorization reuse, minimized evidence packets, inspectable sources, source authority/freshness/Knowledge-role metadata, untrusted-evidence prompt treatment, synthesis-only model output, transient generation and no canonical mutation/external effect/authority grant.

R31 nevertheless found two integrated presentation/action problems that were not acceptable for the final M9 path:

#### R31-F1 — unvalidated source roles could be visually overstated as `sourced-fact`

The first P9.08 response contract classified retrieved evidence summaries as `sourced-fact`, including evidence whose Knowledge role was Observation, Organizational Memory or Knowledge Candidate. The same payload did preserve the explicit `not validated Knowledge` role, but the top-level `Sourced fact` label could still flatten RFC-0007 semantics for an ordinary user.

**Remediation:** internal Copilot answer schema advanced to `arvectum.workspace.copilot-answer/2`; the claim role is now `source-context`, UI wording is `Source context`, and the contract explicitly declares `unvalidated_knowledge_not_presented_as_fact: true`. A backend regression case covers an Observation and requires the Knowledge role to remain visible without any `sourced-fact` claim.

#### R31-F2 — generic AI → `/governed` continuation was not context-bound

The first P9.08 response always exposed `Review governed actions → /governed`. The existing `/governed` surface is a specific retained EIS execution/preflight, not a generic action router. For a Discount Parser or unrelated Knowledge question, the Copilot link therefore had no proven causal binding to that execution. Although the preflight itself is fail-closed and non-consequential, the generic link was an unsafe contextual AI-to-action shortcut.

**Remediation:** Copilot follow-up is now `inspect-evidence-first`. It links only to the first cited Workspace evidence/product context when one exists, declares `routes_to_governed_execution: false`, `direct_consequential_action: false`, and `context_bound_governed_continuation_required: true`. The UI tells the operator that a governed continuation may appear only from context actually bound to the relevant Execution/Decision; Copilot does not select an unrelated execution.

The response-shape change advances the exact internal Workspace release to `p9.10.2`, application contract `9`, still `bounded-internal-provisional` with `public_api: false`.

### 3.3 Activity / notifications — P9.09

**Result after review: PASS.**

Activity continues to compose current authorized `My Work` attention plus current governed-state observation. It explicitly identifies observation time as presentation time unless a source proves occurrence time, reuses the existing P9.04 attention taxonomy, creates no durable read/unread state and exposes only inspect-context links. It remains neither a canonical RFC-0006 Event store nor audit/notification/approval authority.

### 3.4 Organization composition — P9.10

**Result after review: PASS.**

The company view remains a rebuildable projection over Products, non-canonical project lenses, Knowledge context and Work/attention context. Project lenses remain `canonical_project_record: false`; source projection authority is preserved; unavailable protected lanes are withheld; Organization/Actor scope remains server-resolved; no cross-Organization aggregation, canonical mutation or external effect is introduced.

The Knowledge lane preserves explicit Observation / Memory / Candidate / Knowledge distinctions. The Work lane remains an attention/read context and does not grant permission, Organizational Authority or approval.

## 4. Cross-review iterations

Maximum allowed: `7`.

### Iteration 1 — integrated product/AI/action boundary

Material objections found:

1. `R31-F1`: `sourced-fact` presentation could overstate non-validated Knowledge roles;
2. `R31-F2`: generic Copilot `/governed` follow-up was not bound to cited evidence or a related Execution/Decision.

Both findings were treated as blocking R31 PASS.

### Iteration 2 — post-remediation integrated review

Re-read the remediated Copilot backend contract, frontend presentation, tests, Product Contracts, product server adapters, product UI contributions, Activity surface, Organization composition and governed-action surface.

Results:

- `R31-F1` closed: source context and synthesis are distinct; unvalidated Knowledge roles are not presented as fact;
- `R31-F2` closed: Copilot can only continue to cited evidence/product context; no generic AI-selected execution exists;
- Product Contract boundaries remain explicit and lifecycle states unchanged;
- current product adapters are explicit/release-scoped and do not cross into product DB/domain implementation access;
- no new cross-product business relationship or company-specific Kernel semantic appears;
- Activity remains non-canonical and non-authoritative;
- Organization composition remains non-canonical and scope-preserving;
- the real governed preflight remains separately server-revalidated and fail-closed.

No new material objection was found in iteration 2.

### Iteration 3 — post-independent-CI final net-diff review

Reviewed the complete PR net diff after independent CI, including the versioned Copilot response contract, source-context presentation, evidence-first follow-up, regression tests, exact production assets, Product Contract boundaries, Activity/Organization composition invariants and roadmap closure.

The old release JS asset is absent from the resulting branch asset set; the manifest points to the exact rebuilt `p9.10.2` asset and the reproducibility/release-pin gates passed. Temporary remediation/closure helpers and workflow carriers are absent from the final net diff.

No remaining material architecture, product-boundary, hidden-coupling, security, Organization-scope, authority, provenance, Knowledge-lifecycle, AI-safety, action-routing, reproducibility or maintainability objection was found. Functional cross-review therefore stops at iteration 3 rather than manufacturing further iterations.

Functional cross-review is implementation/review evidence; it is not RFC/ADR acceptance, Product Contract/Capability lifecycle promotion or delegated Organizational Authority.

## 5. Verification evidence

One-shot remediation verification completed successfully before committing the clean implementation head:

- Workspace backend compilation and full `workspace_tests` suite — PASS;
- frontend typecheck — PASS;
- frontend tests — PASS;
- browser Web Storage guard — PASS;
- production frontend build — PASS;
- exact release asset verification — PASS.

Clean remediation implementation head: `078206fce89f0cac417dc576bcbd3b1894afcbc0`.

GitHub marks workflow runs attached directly to helper-removal/workflow-restoration commits as `action_required`; those runs are intentionally not used as independent closure evidence.

Independent clean review head `022db6e18a8e7128c1984e6f46908d48351c54e8` passed:

- Productive Workspace CI `#125` / run `32559626999` — `SUCCESS`;
- Reference Python CI `#356` / run `32559627003` — `SUCCESS`.

Canonical roadmaps are synchronized to master `2.86.0` / Phase 9 `1.13.0`, with `P9.11 — Real daily-use dogfooding + friction/backlog closure` as the next action. Workspace release is `p9.10.2`, internal application contract `9`, still `bounded-internal-provisional` and `public_api: false`.

## 6. Explicit non-effects

R31 `Complete / PASS` does not by itself:

- make P6.02 or P6.06 `Stable`;
- make CAP-001/CAP-004 or any other capability `Active`;
- create a public/stable browser/API/SDK/plugin surface;
- make Arvectum OS the source of truth for EIS, Telegram or product-local state;
- create a platform-wide Project metamodel;
- turn product UI contributions or adapters into Platform Capabilities;
- authorize autonomous external actions;
- grant AI Authorization, Organizational Authority or Consequential Approval;
- promote AI output, Observation, Memory or Candidate state into validated Knowledge;
- establish customer Production, SLA/support/certification or broader conformance.
