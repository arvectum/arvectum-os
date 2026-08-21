# P9.04 — My Work / Needs Attention Projection

Status: `Complete / PASS`
Version: `1.0.0`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with governance/security boundary implications
Roadmap item: `P9.04 — My Work / Needs Attention projection`
Phase: `Phase 9 — Productive Workspace & Daily Operations`
Predecessor: `P9.03 — Complete / PASS`
Architecture baseline: `ADR-0001 — Productive Workspace Browser Application Topology` — `Accepted`

## 1. Purpose and closure scope

P9.04 implements the first useful owner-facing `My Work / Needs Attention` projection on top of the closed P9.03 Productive Workspace shell/BFF/session boundary.

The implementation gives the owner a human-readable morning overview without requiring terminal, GitHub or raw Subject/Version/Execution/Event/storage identifiers for ordinary queue use. It remains a **derived, non-authoritative projection** over already-governed/private runtime evidence and does not become a second source of truth.

P9.04 does not create a new RFC/ADR-level architecture decision. The implementation remains within Accepted ADR-0001: React + TypeScript SPA, same-origin co-deployed Python BFF, server-authorized protected reads, bounded/revocable session state, internal/release-scoped application contract and exact-release frontend/BFF compatibility.

## 2. Canonical authority checked

The implementation and closure were checked against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral platform behavior, governed change, security/isolation and evidence-driven reuse;
4. RFC-0002 — exact Subject/Version identity and projection non-authority;
5. RFC-0003 — Organization scope, attributable Actor, deny-by-default access, Authorization versus Organizational Authority and minimization;
6. RFC-0004 — Product Contract boundary and prohibition of hidden product/platform coupling;
7. RFC-0005 — consequential change remains behind Governed Execution and independent gates;
8. RFC-0006 — canonical Event/provenance rules and non-authoritative telemetry/projections;
9. RFC-0007 — Observation/Knowledge/retrieval distinctions and derived search/projection non-authority;
10. RFC-0008 — Document/Artifact authority/provenance boundaries;
11. ADR-0001 — Accepted Productive Workspace browser/BFF topology and protected-read/session/release-skew obligations;
12. P9.01 J1 acceptance baseline;
13. P9.03 shell/session/release implementation closure;
14. P7.05 operational health semantics;
15. P7.06 UI4 real owner-preflight semantics;
16. canonical Phase 9 and master roadmaps.

No material conflict with higher authority was found.

## 3. Implemented projection contract

The BFF exposes an internal/release-scoped `arvectum.workspace.my-work/1` read contract. The contract explicitly declares that the projection is derived and has no canonical or organizational authority.

Each returned work item is bounded to human-facing fields:

- opaque projection-local item identifier;
- normalized attention kind/group and urgency;
- human-readable title and reason;
- human-readable source label;
- legitimate next step;
- live versus controlled-scenario evidence mode;
- source observation time where available;
- inspect-only internal deep link;
- explicit `authority_provided=false`.

The browser does not receive raw governed Subject/Version/Execution/Event/storage identifiers merely to render or navigate the queue. Exact technical identity/provenance remains a downstream context/drill-down responsibility and is not required for ordinary P9.04 navigation.

The projection metadata additionally fixes these boundaries:

- `derived=true`;
- `canonical_authority=false`;
- `organizational_authority_provided=false`;
- `consequential_action_available=false`;
- `visibility_implies_permission=false`;
- denied protected item counts are not exposed.

## 4. Server-side scope, authorization and minimization

`GET /api/app/v1/my-work` reuses the P9.03 protected-read boundary:

1. current server-side Workspace session is resolved;
2. current P7.04 operational access is revalidated;
3. the session's Organization/Actor binding is compared with the current server-authorized context;
4. only that `AccessContext` is passed into the attention provider;
5. browser query/header input cannot select or override Organization/Actor scope;
6. source-level access denial is minimized to no visible item rather than an existence/count oracle;
7. stale/degraded source state withholds protected work until current state can be revalidated.

Visibility in `My Work` is therefore presentation evidence only. It is not Authorization, Organizational Authority, Data Governance approval, Consequential Approval or permission to retry an uncertain effect.

## 5. Truthful live sources and scenario evidence

P9.04 deliberately does **not** infer arbitrary work status from opaque persisted payload fields.

The live adapter uses only already-proven source semantics:

- **P7.05 persistent runtime health** for current/stale/degraded source state;
- **P7.06 UI4 real owner preflight** for a real `Waiting` governed-preflight attention item.

If P7.05 health is stale/degraded, protected queue items are withheld and the owner receives only a generic recoverable system condition. If UI1/UI2 source access is denied, the projection returns no protected source item and no protected count. If source integrity/boundary validation fails, the projection degrades to a generic repair/revalidation condition rather than fabricating business state.

P9.01-required semantic categories that do not currently have a truthful live occurrence are covered by controlled scenario fixtures only. Scenario items are explicitly marked `scenario` in the contract and `Scenario evidence` in the UI; they are not represented as current live organizational facts.

## 6. Owner-facing UX

P9.04 adds two complementary surfaces:

1. **Home morning overview** — a compact live `Needs attention` projection is visible directly on the Workspace home page, satisfying the P9.01 requirement that the owner does not need to hunt through technical navigation before seeing current attention signals;
2. **Full My Work view** — `/my-work` provides work-state filtering, urgency filtering, sorting, refresh and an inspect-only focused item view.

Every visible item explains:

- what needs attention;
- why it appears;
- source/system context;
- legitimate next step;
- whether evidence is live or controlled scenario evidence.

Uncertain/reconciliation-required state is never worded as success and exposes no blind-retry action. No approve/retry/mutate action is introduced by P9.04.

Status and urgency have textual meaning and are not color-only. Mobile/reflow behavior remains supported by the existing responsive Workspace layout.

## 7. Freshness and failure semantics

The projection has explicit `fresh | stale | degraded` health.

- `fresh` means the bounded live sources were evaluated against current healthy runtime state;
- `stale` means the current source heartbeat cannot support presenting protected work as current;
- `degraded` means a required source is unavailable or cannot be safely revalidated.

For stale/degraded states, P9.04 fails closed: protected work items are withheld rather than silently presenting an old derived queue as current canonical truth.

A focused opaque projection item that is no longer present is rendered as unavailable without disclosing whether protected state still exists outside the current authorized projection.

## 8. Functional cross-review

Maximum allowed iterations for this task: **10**.

P9.04 closed after **4 iterations** because no material objection remained.

| Iteration | Finding | Disposition |
|---|---|---|
| 1 | Frontend tests retained DOM between cases, so later assertions could observe duplicated controls. | Added deterministic Testing Library cleanup/test isolation. |
| 2 | The full queue existed at `/my-work`, but P9.01 J1 starts at Home and requires Needs Attention to be immediately visible. | Added compact live My Work projection directly on Home; full `/my-work` remains the filter/detail surface. |
| 3 | First CI artifact export omitted hidden `.vite/manifest.json`, making it unsuitable as exact release artifact evidence. | Refused manual synthesis; rebuilt/reconciled exact `dist` through a temporary branch-only GitHub runner workflow with hidden files included, then removed the temporary workflow and restored normal read-only CI. |
| 4 | Final semantic/security/authority/product-boundary review plus clean CI. | No remaining material objection. |

The review did not continue toward the maximum merely to increase iteration count.

## 9. Verification evidence

Implementation/reconciliation head before closure-only documentation changes:

`04776a93703aa8fd2e7cd9d2fa808fb62d16596b`

Final implementation CI on that head:

- `Reference Python CI #258` — `SUCCESS`;
- generated-Python-artifact rejection — `PASS`;
- full reference suite — `1301 tests`, `OK`;
- `Productive Workspace CI #26` — `SUCCESS`;
- BFF security/context tests — `SUCCESS`;
- frontend TypeScript typecheck — `SUCCESS`;
- frontend interaction tests — `SUCCESS`;
- browser Web Storage guard — `SUCCESS`;
- production build — `SUCCESS`;
- committed `package-lock.json` / `dist` reproducibility gate — `SUCCESS`;
- release-pinned production asset verification — `SUCCESS`.

The final production assets are content-hashed and built for application release `p9.04.1`, internal application API contract `2`, classification `bounded-internal-provisional`.

## 10. Explicit non-claims and remaining acceptance work

P9.04 completion does **not** by itself claim that full P9.01 J1 has passed end-to-end. P9.04 establishes the overview/queue portion, while exact human-friendly object context and governed-action continuation remain P9.05/P9.06 responsibilities and the full J1–J4 usability evidence is evaluated through R30.

P9.04 therefore does not establish:

- `M9-alpha` achievement;
- a public/stable API, SDK, browser support promise or external compatibility contract;
- a Stable Product Contract;
- an Active Platform Capability;
- customer/public Production readiness;
- SLA/support/certification commitments;
- realistic multi-Organization conformance;
- Organizational Authority, Consequential Approval or AI authority;
- product-specific business logic inside the shared Workspace;
- permission to repeat an uncertain external effect;
- promotion of observations/transient outputs into validated Knowledge.

## 11. Closure result

`P9.04 — My Work / Needs Attention projection` is **Complete / PASS** within the exact private `Local / Persistent Internal / owner-operated` Phase 9 scope.

The first owner-facing attention projection is implemented, human-readable, available on Home and `/my-work`, authorization/data-governance filtered, freshness-aware, minimization-safe and explicitly non-authoritative.

The next canonical action is:

> **P9.05 — Human-friendly Records / Documents / Knowledge + global search.**
