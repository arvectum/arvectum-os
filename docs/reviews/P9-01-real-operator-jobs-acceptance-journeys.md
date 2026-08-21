# P9.01 — Real Operator Jobs-to-be-Done + Acceptance Journeys

Status: `Complete / PASS — acceptance baseline fixed; downstream journey execution pending`
Version: `1.0.0`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Roadmap item: `P9.01 — Real operator jobs-to-be-done + acceptance journeys`
Phase: `Phase 9 — Productive Workspace & Daily Operations`
Milestone targets: `M9-alpha — Usable Internal Workspace`; `M9 — Daily-use organizational workbench`
Predecessor: `P9.00 — Complete / PASS`

## 1. Purpose and decision level

P9.01 converts the Phase 9 outcome statement into executable owner/operator jobs and acceptance evidence **before** selecting the long-lived frontend/BFF/session/read-model architecture or implementing broad screens.

This artifact fixes:

- the human jobs that the private Workspace must support;
- the real or truthfully representative Arvectum evidence to use for those jobs;
- the ordinary-path acceptance contract;
- negative-path authority/security/uncertainty requirements;
- the evidence record required to call each journey passed;
- which journeys are required for `M9-alpha` versus full `M9`.

P9.01 does **not** claim that these journeys have already been implemented or executed in the new Productive Workspace. It closes the **acceptance-baseline definition** only. Journey execution evidence belongs to P9.03–P9.08, R30/R31 and real dogfooding.

P9.01 does not select a frontend framework, BFF/API topology, session/IAM provider, durable search/read-model technology, design system or product UI composition mechanism. No ADR threshold is crossed by fixing human outcomes and evidence semantics alone.

## 2. Canonical authority checked

Checked before defining the journeys:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral shared platform behavior, explicit Product Contracts, Governed Execution, security/isolation, organizational sovereignty, technology independence and evidence-driven reuse;
4. RFC-0002 — Subject versus immutable exact Version identity, Head/Effective distinctions, relationship and projection non-authority;
5. RFC-0003 — explicit Organization scope, attributable Actor, deny-by-default/fail-closed access, Authorization versus Organizational Authority separation, minimization and Organization isolation;
6. RFC-0004 — Product Contract boundaries, product-owned semantics, no hidden coupling and no automatic platform promotion;
7. RFC-0005 — exact governed execution context, separate gates, consequential change only through Governed Execution, retry/replay authority requirements;
8. RFC-0006 — append-only canonical Events, provenance honesty, non-authoritative telemetry/projections, replay/reconstruction boundaries;
9. RFC-0007 — Observation/Memory/Candidate/Knowledge distinctions, Search/RAG non-authority, validation/approval and freshness/exact-reliance requirements;
10. RFC-0008 — Document/Document Version/Artifact/derived representation distinctions, authority/source/provenance and transient-output defaults;
11. ADR Index — no Accepted ADR selects a permanent frontend/BFF/session/IAM/read-model/search/product-composition topology;
12. P6.02 Tender Operator Product Contract `Provisional 0.1.0`;
13. P6.06 Discount Parser Product Contract `Provisional 0.1.0`;
14. P4.01/P4.10 operator-workspace and accessibility/usability baseline;
15. P7.06-UI4 first real owner interaction evidence;
16. P7.07 persistent Tender Operator selected-Mac closure;
17. P7.08 persistent Discount Parser cross-host closure;
18. P8.05 external uncertainty/reconciliation evidence;
19. P8.08 multi-Organization validation disposition — realistic two-Organization isolation remains `NOT ACTIVATED`;
20. P9.00 Productive Workspace activation baseline and current Phase 9/master roadmaps.

No conflict with Constitution `1.2.0` or Accepted RFC-0001…RFC-0008 was found.

## 3. Operator and activated scope

The primary Phase 9 operator is the attributable owner/operator of `ООО «Арвектум»` using the private `Persistent Internal / owner-operated` Arvectum OS environment.

The currently activated organizational scope contains one governing Organization: `ООО «Арвектум»`. P9.01 therefore must not fabricate a second customer/tenant merely to create UX examples. Existing cross-Organization denial/failure-closed semantics remain mandatory, while realistic two-Organization usability/isolation remains outside the evidence that P9.01 can truthfully claim.

Ordinary Workspace navigation MUST preserve an explicit Organization and attributable Actor context. A technically available page, control, session or button is not evidence of Organizational Authority, consequential approval or permission to mutate canonical/external state.

## 4. Real acceptance fixture registry

P9.01 uses existing retained evidence instead of synthetic UX-only cards wherever current real evidence exists.

### F1 — Real EIS-backed governed Document

Use the retained governed EIS evidence already inspected by the owner in P7.06-UI4:

- authoritative external system: `ЕИС / zakupki.gov.ru`;
- notice: `0344100006426000005`;
- semantic type: `platform.document`;
- authority mode: `External Reference`;
- Document Subject: `document-subject/eis-0344100006426000005-exact-attachment-evidence@aa4e760c379c8952aba6c6c335f3e233`;
- exact Document Version: `document-version/eis-0344100006426000005-74e943d855406b04@aa4e760c379c8952aba6c6c335f3e233`;
- integrity evidence: `sha256:74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- Product Contract boundary: P6.02 Tender Operator `Provisional 0.1.0`.

The ordinary UI MUST NOT require the operator to know or paste these technical identifiers. They are retained here so acceptance evidence can prove that a human-readable journey resolves to exact governed state.

### F2 — Real governed Execution / provenance chain

Use the retained P7.06-UI4 execution/provenance chain for inspection and fail-closed action semantics:

- Execution Subject: `execution-subject/p7-06-ui1-real-state-74e943d855406b04@aa4e760c379c8952aba6c6c335f3e233`;
- exact Execution Version: `execution-version/p7-06-ui1-real-state-74e943d855406b04-v5@aa4e760c379c8952aba6c6c335f3e233`;
- Admission Event Version: `event-version/p7-06-ui1-document-admitted-74e943d855406b04-v1@aa4e760c379c8952aba6c6c335f3e233`;
- authoritative source remains `ЕИС / zakupki.gov.ru`;
- prior real owner preflight result: `WAITING / fail-closed`, with no canonical mutation or external effect.

This fixture proves that the Workspace can explain a real execution and can exercise a bounded governed interaction without manufacturing missing gate evidence.

### F3 — Persistent Tender Operator reliance

Use the persistent P7.07 Tender Operator contour as a real product/platform boundary fixture:

- product repository: `arvectum/tender-agent`;
- Product Contract: P6.02 `Provisional 0.1.0`;
- exact CAP-001 reliance on the F1 Document/Version/Artifact evidence;
- EIS remains externally authoritative;
- no hidden read of platform persistence internals is permitted.

At execution time, acceptance evidence SHOULD bind the exact currently active product/runtime release and exact Product Contract version rather than assuming historical release identifiers are still current.

### F4 — Persistent Discount Parser governed contour

Use the persistent P7.08 Discount Parser contour as the second real product boundary fixture:

- product repository: `arvectum/discount-parser`;
- Product Contract: P6.06 `Provisional 0.1.0`;
- shared platform dependency: exactly `CAP-004` for the currently proven contour;
- product owns Offer/publication/product database/Telegram integration and product UI semantics;
- Arvectum OS owns the admitted governed execution/evidence/reconstruction boundary;
- reconstruction remains read-only and never replays Telegram or another external effect.

At execution time, select a current verified real Discount Parser publication/reconstruction context exposed through the applicable product-owned adapter and bind its exact execution/effect/evidence identifiers in the acceptance record. If no current live item is available, a deliberately prepared truthfully representative fixture MAY be used only if it is clearly marked as scenario-generated, does not claim that an external effect occurred, and preserves the exact P6.06 authority/uncertainty rules.

### F5 — External uncertainty / reconciliation state

Where a journey needs an uncertain external outcome, use real retained uncertainty evidence if available. If no real currently unresolved effect exists, use a controlled acceptance fixture implementing the already-proven P8.05 semantics:

- outcome `Uncertain`, never synthetic `Succeeded`;
- reconciliation required;
- blind retry prohibited;
- `StillUncertain` and `ConfirmedSucceeded` prohibit retry;
- `ConfirmedNotApplied` can permit a **new** governed execution with a new retry token;
- historical reconstruction never repeats the external effect.

The fixture must be visibly identified as acceptance/scenario evidence if it is not a real current external occurrence.

## 5. Global acceptance contract

The following requirements apply to every journey where relevant.

### 5.1 Ordinary-path usability

A journey passes only if the owner can complete the declared ordinary task through the private browser Workspace without:

- terminal commands;
- GitHub navigation;
- database access;
- knowledge or copy/paste of internal Subject/Version/Execution/Event/storage identifiers;
- reverse-engineering platform implementation concepts merely to locate the human work item.

Human-readable names, product/source labels, business context and meaningful status come first. Exact technical identity/version/provenance remains reachable on demand.

No arbitrary time-to-completion SLA or click-count target is declared before P9.02 prototypes exist. Acceptance runs MUST record task completion time, primary interactions, dead ends and escapes so P9.02/R30/dogfooding can compare usability with evidence rather than intuition.

### 5.2 Authority and action safety

- UI visibility or an enabled button is never proof of Authorization, Organizational Authority, Data Governance approval or Consequential Approval.
- Consequential canonical change routes through Governed Execution.
- The authoritative runtime revalidates current gates/preconditions independently of client state.
- Missing, ambiguous, stale or revoked required evidence fails closed.
- AI output or recommendation cannot be the final consequential approver.

### 5.3 Canonical versus derived state

Home queues, `My Work`, search, activity, notification and relationship summaries are projections and remain non-authoritative. They may route the operator to governed state but do not replace it.

If projection freshness or source availability is materially uncertain, the UI must make that limitation understandable and must not silently present stale derived state as current canonical truth.

### 5.4 External authority and uncertainty

External facts retain their declared authority mode/source. `ЕИС / zakupki.gov.ru` does not become Native merely because Arvectum OS admitted evidence about it.

An unknown external-effect result remains visibly uncertain. Timeout, acknowledgement, intent or transport receipt is not presented as success. Retry/reconciliation behavior must preserve P8.05 semantics.

### 5.5 Product boundary

Shared Workspace owns domain-neutral navigation, presentation/composition primitives and governed platform semantics. Tender, Discount and other product-specific schemas, statuses, workflows, templates, business rules and UX remain product-owned and enter Workspace through explicit governed boundaries.

No direct product access to platform internal tables, undocumented imports/endpoints or implicit shared state is accepted.

### 5.6 Organization isolation and minimization

- Organization context is explicit; unresolved scope fails closed.
- The ordinary Workspace must not disclose protected previews/counts/existence details merely to make a denied state more informative.
- No cross-Organization result is accepted by default.
- P9.01 makes no realistic two-Organization conformance claim; P8.08 remains `NOT ACTIVATED` for that evidence class.

### 5.7 Accessibility baseline

For the target real application, critical object/status/authority/action/blocking meaning must be textual and not color-only; semantic native controls/regions should be used where applicable; governed text must be safely rendered; and blocked/error meaning must be understandable programmatically and visually.

Formal keyboard-flow, focus management, contrast, zoom/reflow, screen-reader and localization validation belongs to the selected real frontend implementation and R30/R32; P9.01 does not claim those unexecuted checks already pass.

## 6. Acceptance Journey J1 — Morning overview / “What needs my attention?”

Acceptance stage: **`M9-alpha blocker`**.

### Job-to-be-done

> When I start work, I want to understand what actually needs my attention across current Arvectum OS work so that I can decide where to act first without hunting through raw Executions, Events or repositories.

### Real fixture set

Use F1/F2 and any current real pending/blocked/failed/reconciliation-required governed state available in the persistent environment. Include F4/F5 when a real or truthfully representative Discount Parser attention item is available.

### Starting condition

- owner is authenticated to the private Workspace;
- one explicit Organization and attributable Actor are resolved;
- persistent runtime is available, or an explicit unavailable/degraded state is shown.

### Ordinary journey

1. Open Workspace home.
2. See a human-readable `My Work / Needs Attention` area without navigating through raw platform taxonomy first.
3. Distinguish at minimum:
   - decision/action required;
   - blocked/failed;
   - awaiting reconciliation / uncertain;
   - recent important outcome;
   - informational-only item.
4. For one item, understand **why it appears**, its product/source context and what legitimate next step exists.
5. Open the item into J3 context.
6. Optionally drill to exact technical identity/version/provenance.

### PASS conditions

- ordinary path requires zero terminal/GitHub/internal-ID knowledge;
- each attention item has a human-readable reason and source/product context;
- informational-only and action-required states are not conflated;
- uncertain/reconciliation-required state is never styled or worded as success;
- denied/unavailable data does not leak protected preview/count detail;
- stale/derived projection limitations are surfaced where material;
- opening an item resolves to exact governed state or a truthful unavailable/stale explanation;
- exact IDs/provenance are available only as drill-down evidence, not required navigation input.

### Negative-path acceptance

- unresolved Organization → home fails closed rather than showing ambient work;
- revoked/denied source access → minimized unavailable state;
- uncertain external effect → no blind retry CTA represented as safe;
- projection/source disagreement → canonical/source state wins and discrepancy is visible.

### Required evidence

Capture the acceptance-run record defined in Section 12 plus screenshots or equivalent UI evidence for the overview, one attention reason, one negative/blocked or uncertain state, and exact-state drill-down.

## 7. Acceptance Journey J2 — Find anything / human-readable discovery

Acceptance stage: **`M9-alpha blocker`** for one real governed object; broader product discovery continues into full M9.

### Job-to-be-done

> When I know the human context but not an internal identifier, I want to find the organizational object I mean and open the authoritative context quickly.

### Real fixture set

Primary fixture: F1, searchable/navigable by human context such as EIS notice number `0344100006426000005`, source label, meaningful document/tender description where available, or related product context — not by the Document Subject/Version identifier.

Later full-M9 coverage should include F4 through the product-owned workspace surface.

### Ordinary journey

1. Invoke persistent global search/navigation from the normal Workspace shell.
2. Enter a human-readable term.
3. Receive scoped results that distinguish object kind, source/product context and meaningful state.
4. Narrow/filter when multiple result types are returned.
5. Open the intended real object.
6. Reach exact technical history only when requested.

### PASS conditions

- F1 is findable without typing an internal platform identifier;
- search results do not flatten Document/Record/Knowledge/Execution/product context into an ambiguous generic object;
- externally authoritative source is labeled truthfully;
- search/index status is treated as derived/non-authoritative;
- inaccessible foreign/denied content is not leaked through result snippets/counts;
- an exact governed item can be reached from the result;
- stale/missing index data cannot silently override canonical/source state.

### Negative-path acceptance

- exact human term but denied source → no protected snippet/existence leak beyond the applicable minimized policy;
- stale result target → explicit unavailable/stale explanation, not a fabricated current object;
- ambiguous query → disambiguation by human context instead of requiring internal IDs.

## 8. Acceptance Journey J3 — Understand context / “What is this and what happened?”

Acceptance stage: **`M9-alpha blocker`**.

### Job-to-be-done

> When I open a real organizational object, I want to understand its meaning, authority, provenance, relevant process and required next step before I act.

### Real fixture set

Use F1 + F2 + F3.

### Ordinary journey

From the opened real EIS-backed object, the owner can answer from the human-facing context:

1. What is this?
2. Why is it relevant now?
3. Where did it come from?
4. Which source/state is authoritative?
5. What changed or happened to it?
6. Which product/process/execution is related?
7. Is any action required now?
8. Where can I inspect exact version/provenance if needed?

### PASS conditions

- human meaning precedes technical identifier strings;
- authority mode/source is explicit and truthful (`External Reference`, EIS for F1);
- related Document/Version/Execution/Event/Product Contract context is navigable without forcing internal-ID copy/paste;
- Head/Effective/exact relied-on version distinctions remain available where material;
- relationship/activity summaries do not become authority;
- generated/derived representations are distinguishable from authoritative/source evidence;
- the operator can state the seven human answers above without GitHub/terminal assistance;
- exact F1/F2 identity/provenance can be opened on demand and matches the acceptance-run record.

### Negative-path acceptance

Missing/redacted/deleted evidence is reported as such; the Workspace does not invent reconstruction detail. If source freshness cannot be established, the limitation is visible rather than silently interpreted as current truth.

## 9. Acceptance Journey J4 — Make a governed decision/action

Acceptance stage: **`M9-alpha blocker`**.

### Job-to-be-done

> When an action is appropriate, I want to inspect its consequence and gates, submit it through the governed boundary, and understand the result or reason it is blocked without the UI manufacturing authority.

### Real fixture set

The minimum M9-alpha acceptance fixture reuses F2 and the existing real owner-operated preflight pattern. A downstream implementation MAY provide a stronger bounded real canonical interaction if an already-authorized, reversible, low-consequence action exists, but it must not fabricate authority merely to obtain a successful mutation.

Full-M9 product-bound action evidence may additionally use F4, subject to the P6.06 Product Contract and external-effect rules.

### Ordinary journey

1. Open the action from a human context rather than an Execution ID.
2. See what the requested action would do and which Organization/Actor/product/source it concerns.
3. See distinct gate/readiness semantics for Authorization, Organizational Authority, Data Governance and consequential approval/preconditions where applicable.
4. Submit the governed request/preflight.
5. Backend/runtime revalidates the current context independently of UI state.
6. See one truthful result: completed, blocked/denied/waiting, failed, or uncertain/reconciliation-required as applicable.
7. Inspect resulting exact Execution/Event/effect/provenance evidence on demand.

### PASS conditions

- action is initiated through Governed Execution or the bounded preflight into that boundary;
- UI does not turn technical access, button state or AI suggestion into authority/approval;
- missing gate evidence fails closed and explains the blocking category without exposing protected data;
- no direct alternate mutation path bypasses the governed runtime;
- successful canonical mutation, if exercised, produces attributable version/event evidence;
- unknown external effect remains `Uncertain` and routes to reconciliation rather than success;
- historical replay/reconstruction offers no implicit re-execution of an external effect;
- ordinary action path requires no internal identifier copy/paste.

### M9-alpha exact acceptance

A real fail-closed preflight is an acceptable M9-alpha governed interaction **provided it is initiated by the owner through the new Workspace over real retained state and independently proves that missing authority/gates are not manufactured**. M9-alpha does not require creating a consequential mutation solely for demo value.

## 10. Acceptance Journey J5 — Work across products

Acceptance stage: **`Full M9 target; not an M9-alpha blocker`**.

### Job-to-be-done

> When I move between company work in different products, I want one coherent organizational workspace while each product keeps ownership of its own business semantics and execution boundary.

### Real fixture set

Use both F3 Tender Operator and F4 Discount Parser.

P9.01 deliberately does **not** invent a business relationship between a tender and a discount offer. The shared job is company-level navigation/composition across two real product contexts, not forced semantic merging of unrelated domain objects.

### Ordinary journey

1. Start from company-level `My Work`, search or product navigation.
2. Enter a real Tender Operator context through its explicit Product Contract-backed surface.
3. Return to shared company/work navigation without losing Organization/Actor context.
4. Enter a real Discount Parser context through its explicit Product Contract-backed surface.
5. Inspect exact Product Contract/version/provenance details on demand.
6. Perform product-specific work only through the product-owned surface/governed boundary responsible for it.

### PASS conditions

- at least two real product-owned surfaces are reachable inside/coherently from Workspace;
- Product Contract/context boundary is explicit and inspectable;
- Tender fields/rules do not become generic shared platform schema merely for composition;
- Discount Offer/publication/taxonomy/template/Telegram semantics remain product-owned;
- no direct internal-table/import/undocumented endpoint coupling is introduced;
- shared shell/search/attention semantics remain domain-neutral;
- switching products does not broaden Organization, authorization or authority;
- lifecycle remains truthful: Product Contracts stay `Provisional` unless separately transitioned.

## 11. Acceptance Journey J6 — Ask Arvectum / source-grounded organizational assistance

Acceptance stage: **`Full M9 target; not an M9-alpha blocker`**.

### Job-to-be-done

> When I need an explanation or synthesis, I want to ask Arvectum in natural language and receive a useful answer grounded in inspectable organizational evidence without AI inventing authority, certainty or validated Knowledge.

### Real question fixtures

Use questions tied to F1–F4, for example:

- “What is the current status and authoritative source for EIS notice 0344100006426000005 in our retained context?”
- “Why is this Tender Operator document in the current work context, and what exact evidence supports that?”
- “What happened in the selected Discount Parser publication/reconstruction context, and is any uncertainty or reconciliation still open?”

### Ordinary journey

1. Ask a natural-language organizational question from global Copilot or an object context.
2. Receive an answer/proposal with inspectable source references.
3. Distinguish sourced fact, inference/synthesis, uncertainty and unavailable evidence.
4. Open the cited organizational evidence.
5. If a consequential follow-up is proposed, route it into J4/Governed Execution rather than executing silently.

### PASS conditions

- material factual claims are grounded in inspectable sources/evidence available within the operator’s scope;
- uncertainty and missing/stale evidence are explicit;
- Observation/Memory/Candidate/Knowledge roles are not flattened into “known truth”;
- generated answer/proposal is a transient output by default and is not silently validated into Knowledge;
- AI neither grants authorization/Organizational Authority nor acts as final consequential approver;
- no consequential canonical or external effect occurs merely because the user asked a question;
- cross-Organization retrieval/reuse is denied by default;
- user can inspect the evidence behind the answer without leaving ordinary Workspace for GitHub/terminal.

## 12. Acceptance evidence record

Every executed journey must produce a minimized evidence record sufficient for review without retaining unnecessary sensitive content.

Required fields:

| Field | Requirement |
|---|---|
| `journey_id` | `J1`…`J6` |
| `acceptance_stage` | `M9-alpha` or `M9` |
| `run_at` | attributable run timestamp |
| `organization_ref` | exact explicit Organization reference |
| `actor_ref` | attributable Actor reference; minimized as appropriate in canonical evidence |
| `workspace_release` | exact deployed application/runtime release |
| `product_context` | product + exact Product Contract version when applicable |
| `fixture_refs` | F1…F5 plus exact current governed identifiers bound at run time |
| `human_entry_terms` | human-readable starting term/context; no requirement to expose sensitive content |
| `task_completed` | boolean + truthful outcome |
| `ordinary_path_internal_id_dependency` | MUST be `false` for PASS |
| `terminal_or_github_escape` | MUST be `false` for PASS |
| `primary_interactions` | measured count for usability comparison, not a current SLA |
| `task_duration` | measured duration for usability comparison, not a current SLA |
| `dead_ends_or_recovery` | recorded friction/recovery steps |
| `authority_or_success_misrepresentation` | MUST be `false` for PASS |
| `organization_scope_violation` | MUST be `false` for PASS |
| `canonical_or_external_outcome` | exact known outcome; uncertainty preserved |
| `exact_identity_drilldown_verified` | boolean where applicable |
| `provenance_source_refs` | minimized exact evidence references |
| `negative_path_exercised` | at least the journey-specific declared negative case where required by gate |
| `operator_notes` | concise friction/comprehension notes |

Raw secrets, session cookies, CSRF tokens, private keys, reusable credentials and unnecessary protected payloads must not be copied into canonical journey evidence.

## 13. Stage gates

### 13.1 M9-alpha acceptance script

`M9-alpha` cannot pass until, through the **new normal private Workspace** rather than the P4/P7 diagnostic shell alone:

1. J1 passes over real current/retained state;
2. J2 finds at least one real governed object by human context;
3. J3 explains F1/F2/F3 business/authority/provenance context in human terms;
4. J4 executes one real bounded governed interaction, including a truthful fail-closed preflight when authority is intentionally absent;
5. ordinary J1–J4 paths record `ordinary_path_internal_id_dependency = false`;
6. ordinary J1–J4 paths record `terminal_or_github_escape = false`;
7. no journey records authority/success misrepresentation or Organization-scope violation;
8. exact technical identity/version/provenance is reachable on demand;
9. R29 and R30 have no unresolved material finding.

J5 and J6 are explicitly **not** M9-alpha blockers because the canonical Phase 9 sequence places product composition and Copilot after M9-alpha.

### 13.2 Full M9 acceptance extension

Full M9 additionally requires:

- J5 to pass with at least Tender Operator + Discount Parser real product-owned surfaces;
- J6 to pass with source-grounded, uncertainty-aware, authority-safe AI assistance;
- P9.09/P9.10 company activity/composition to preserve the J1/J5 boundaries;
- real P9.11 owner dogfooding to expose recurring friction, with material findings dispositioned before R32/P9.12 closure.

## 14. P9.02 architecture-spike evaluation inputs

P9.02 should prototype architecture against these journeys, not against generic component demos.

At minimum, each candidate should demonstrate enough of J1–J4 to evaluate:

- persistent private application ergonomics;
- explicit Organization/Actor/session context;
- server-side authorization/gate revalidation;
- projection/search/read-model non-authority;
- human-readable deep context with exact-version/provenance drill-down;
- fail-closed governed action composition;
- accessibility/testability/observability potential;
- product-owned composition path for later J5;
- source-grounded assistant integration path for later J6 without giving AI authority;
- deploy/update/rollback fit with the persistent owner-operated runtime.

The comparison should use the recorded `primary_interactions`, `task_duration`, dead ends, internal-ID escapes and security/authority outcomes. These are evidence for choosing an application architecture, not public UX/SLA commitments.

## 15. Functional cross-review

Five review/revise iterations were performed; no material objection remains for the P9.01 definition scope.

### Iteration 1 — product/platform ownership

Finding: “work across products” could tempt the Workspace to normalize Tender and Discount business concepts into one platform schema.

Revision: J5 is defined as company-level navigation/composition only. Tender and Discount semantics remain product-owned behind explicit Product Contracts; no invented cross-product domain relationship is required.

Disposition: `PASS`.

### Iteration 2 — security / authority-safe UX

Finding: `Needs Attention`, search results and enabled actions can be misread as permission, authority or approval and can leak denied data through counts/previews.

Revision: global and per-journey gates require explicit Organization/Actor scope, minimized denied states, projection non-authority and independent backend revalidation. UI availability is never authority.

Disposition: `PASS`.

### Iteration 3 — external effects / replay / uncertainty

Finding: an acceptance demo might force a “successful” external action or offer a blind retry merely to make the UI look complete.

Revision: J4 accepts the real fail-closed governed preflight as valid M9-alpha evidence; F5/J1/J4 require `Uncertain` + reconciliation semantics and prohibit historical replay from repeating effects.

Disposition: `PASS`.

### Iteration 4 — Knowledge / AI authority

Finding: J6 could collapse search, inference and generated text into validated organizational truth or turn Copilot into an approver.

Revision: J6 is source-grounded, uncertainty-aware, transient by default, preserves RFC-0007 epistemic distinctions and routes every consequential follow-up through J4/Governed Execution.

Disposition: `PASS`.

### Iteration 5 — sequencing / measurability / premature UX commitments

Finding: requiring J5/J6 at M9-alpha would contradict the roadmap sequence, while hard-coded click/time targets before P9.02 could prematurely optimize or constrain architecture.

Revision: J1–J4 are M9-alpha blockers; J5/J6 remain full-M9 targets. Hard acceptance uses zero terminal/GitHub/internal-ID dependency, zero authority/success misrepresentation and zero Organization-scope violation, while interaction count/time are measured comparative signals until real prototype/dogfooding evidence supports thresholds.

Disposition: `PASS`.

Functional review is not formal approval, lifecycle promotion, accessibility certification, Production readiness or public-interface commitment.

## 16. Exit criteria

P9.01 definition exit criteria are satisfied:

- [x] six Phase 9 jobs are expressed as concrete owner outcomes;
- [x] real Tender/EIS and persistent product evidence is bound into the acceptance fixture registry;
- [x] controlled truthfully representative uncertainty fixtures are allowed only where current real evidence is unavailable and are clearly non-production evidence;
- [x] J1–J4 exact M9-alpha acceptance paths and negative paths are fixed;
- [x] J5/J6 full-M9 paths are fixed without blocking M9-alpha prematurely;
- [x] ordinary-path no-terminal/no-GitHub/no-internal-ID requirements are measurable;
- [x] authority, external-source, uncertainty, replay, Knowledge/AI and Organization boundaries are explicit;
- [x] acceptance evidence schema is fixed;
- [x] P9.02 receives architecture-spike evaluation inputs without selecting technology;
- [x] functional cross-review completed in five iterations with no remaining material objection;
- [x] no Constitution/RFC/ADR/Product Contract/capability lifecycle change is required.

## 17. Closure and next action

`P9.01 = Complete / PASS` **for acceptance-baseline definition only**.

This does not claim J1–J6 implementation completion, M9-alpha acceptance, M9 acceptance, customer Production, public/stable interfaces, Stable Product Contracts, Active Platform Capabilities, formal accessibility conformance, multi-Organization proof or AI authority.

After roadmap synchronization, the next canonical action is:

> **`P9.02 — Application architecture spike + frontend/BFF/session decision`.**

P9.02 must compare bounded implementation options against J1–J4 and the evidence contract above before the project materially relies on a long-lived frontend/application topology.