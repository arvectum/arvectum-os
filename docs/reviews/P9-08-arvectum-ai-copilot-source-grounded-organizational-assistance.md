# P9.08 — Arvectum AI Copilot + source-grounded organizational assistance

Status: `Complete / PASS`
Date: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `product_contract` and `governance`
Predecessor: `P9.07 — Complete / PASS`
Target journey: `P9.01 J6 — Ask Arvectum / source-grounded organizational assistance`

## Scope

P9.08 adds a bounded, source-grounded `Ask Arvectum` surface to the internal Productive Workspace through the topology accepted by ADR-0001. The shared platform behavior remains domain-neutral: it retrieves only through already-authorized Workspace discovery/product-composition boundaries and does not load product internals or absorb product schemas, workflows, approvals, knowledge, templates or detailed UX.

Canonical baseline checked before implementation: Constitution `1.2.0` (`Ratified`, frozen); RFC-0001 through RFC-0008 (`Accepted 1.0.0`) with direct focus on RFC-0003, RFC-0005, RFC-0006, RFC-0007 and RFC-0008; Accepted ADR-0001; P9.01 J6; P9.07 composition boundary; canonical roadmap `2.82.0`.

## Implementation under review

- protected same-origin `POST /api/app/v1/copilot/ask` using current server-resolved Organization/Actor access context;
- browser request contract accepts only a bounded natural-language `question`; browser-supplied Organization, authority, approval or hidden retrieval context is rejected;
- explicit response roles: `sourced-fact`, `synthesis`, `uncertainty`, `unavailable-evidence`;
- source cards expose human-readable source/authority/freshness/Knowledge-role context and open inspectable evidence in ordinary Workspace;
- generated answers are `Transient Output` by default: no silent Memory/Knowledge promotion, canonical mutation, external effect, authorization, Organizational Authority or consequential approval;
- consequential follow-up routes to the existing Governed Execution review surface rather than executing silently;
- model boundary is optional and technology-independent at the platform level; the current owner-operated P9.08 contour permits only an explicitly configured loopback OpenAI-compatible endpoint;
- model input is a minimized grounding packet and omits opaque Workspace source identities/open paths, credentials, raw product stores and Organization/Actor technical identifiers;
- evidence is treated as untrusted data for prompt-injection resistance; model output can only be represented as synthesis, never as sourced fact or validated Knowledge;
- missing evidence, stale/degraded evidence or model failure produces explicit limitation/uncertainty rather than fabricated certainty;
- Workspace release `p9.08.1`, internal application contract `6`, remains `bounded-internal-provisional` and `public_api: false`.

## Closure evidence

- Final implementation/test head before canonical closure docs: `e5bedffa778cd2487929f826f10359071c1f0b76`.
- Productive Workspace CI `#90` / run `32553258369`: `SUCCESS`; backend security/context tests, TypeScript typecheck, frontend tests, Web Storage guard, production build, committed-asset reproducibility and release-pinned asset boundary all passed.
- Reference Python CI `#322` / run `32553258317`: `SUCCESS`.
- Functional cross-review: 3 iterations. Material findings repaired: product-specific shared ranking/prompt coupling, ordinary-path opaque IDs, actual request-size enforcement, prompt-injection treatment, and opaque source identity in the model packet. No material objection remains. This is functional evidence, not formal governance approval.
- The temporary CI asset-reconciliation helper was removed after the generated production assets were reconciled; the final Productive Workspace CI runs under the normal read-only workflow.
- P6.02 and P6.06 Product Contracts remain `Provisional 0.1.0`; no Platform Capability lifecycle state changed.

## P9.01 J6 acceptance evidence

| Field | Evidence |
|---|---|
| `journey_id` | `J6` |
| `acceptance_stage` | `M9` implementation acceptance; does not replace P9.11 real daily-use dogfooding |
| `run_at` | `2026-08-22T05:01:34Z`–`2026-08-22T05:02:02Z` for Productive Workspace CI #90 |
| `organization_ref` | Server-resolved current Workspace scope; automated BFF acceptance uses minimized fixture `org-a` and does not retain a reusable production credential or protected Organization payload |
| `actor_ref` | Attributable current Workspace actor boundary; automated BFF fixture `actor-a`, CI actor attributable through GitHub run evidence |
| `workspace_release` | `p9.08.1`; internal application contract `6` |
| `product_context` | Product-neutral composition over Tender Operator P6.02 and Discount Parser P6.06, both `Provisional 0.1.0`; no product semantics promoted into the shared Copilot schema |
| `fixture_refs` | F1 retained EIS notice `0344100006426000005`; Tender Operator retained context; Discount Parser reconstruction/reconciliation context |
| `human_entry_terms` | current status + authoritative source for EIS notice; evidence supporting a current work/product context; remaining uncertainty/reconciliation |
| `task_completed` | `true` for automated J6 implementation acceptance |
| `ordinary_path_internal_id_dependency` | `false`; opaque IDs are not needed to ask/read/open evidence |
| `terminal_or_github_escape` | `false` for the browser-facing ordinary path; canonical review evidence itself remains in the repository |
| `primary_interactions` | ask question → inspect classified answer; optional open-evidence and governed-follow-up interactions; not an SLA |
| `task_duration` | automated acceptance only; human task-duration measurement is deferred to P9.11 dogfooding and is not inferred from CI duration |
| `dead_ends_or_recovery` | final path has no known dead end; CI exposed one stale P9.07 release-header test fixture, repaired to use the current release contract |
| `authority_or_success_misrepresentation` | `false` |
| `organization_scope_violation` | `false`; cross-Organization retrieval is denied by contract/default |
| `canonical_or_external_outcome` | none; asking Copilot is read-only/transient and performs no canonical or external effect |
| `exact_identity_drilldown_verified` | `true` through the existing object-context/provenance boundary; exact identifiers remain on-demand rather than ordinary-path input |
| `provenance_source_refs` | F1 subject/version drill-down plus CI #90 / run `32553258369` and implementation head `e5bedffa778cd2487929f826f10359071c1f0b76` |
| `negative_path_exercised` | model unavailable; no sufficient evidence; access revoked; browser scope/authority injection; unavailable product evidence; external/non-loopback model endpoint rejected |
| `operator_notes` | answer is explicitly transient; source facts and free-form synthesis remain distinguishable; P9.11 still owns real daily-use friction/timing evidence |

Exact F1 drill-down identity retained by the existing P9.05 acceptance fixture:

- `document-subject/eis-0344100006426000005-exact-attachment-evidence@aa4e760c379c8952aba6c6c335f3e233`
- `document-version/eis-0344100006426000005-74e943d855406b04@aa4e760c379c8952aba6c6c335f3e233`

## Explicit limitations

- P9.08 does not make AI an authority source, approver or autonomous consequential executor.
- P9.08 does not validate generated answers into Knowledge and does not create a memory/learning write path.
- External/cloud AI providers are intentionally outside the current P9.08 owner-operated contour. Enabling one requires a separate proportionate data-governance/privacy/contract decision rather than a configuration shortcut.
- Retrieval quality is bounded by currently authorized Workspace projections; the assistant reports unavailable/stale evidence rather than bypassing those boundaries.
- This is internal implementation/acceptance evidence, not public/customer Production evidence and not an SLA, support, conformance, Stable Product Contract or Active Platform Capability claim.
- Full M9 remains open: P9.09–P9.12 and R31/R32 still govern activity/notifications, company composition, real dogfooding, hardening and final acceptance.
