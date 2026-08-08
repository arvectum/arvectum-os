# P4.01 — Operator Journeys, Workspace Boundary and Information Architecture

Status: `Complete`
Version: `1.0.0`
Created: `2026-08-08`
Updated: `2026-08-08`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Roadmap work item: `P4.01 — Operator journeys, workspace boundary and information architecture`
Phase: `Phase 4 — Workspace / Operator Experience`
Milestone target: `M4 — Coherent governed workspace baseline`
Result: **`PASS — the bounded operator journeys, workspace/product boundary, information architecture and presentation-authority model are sufficient to begin P4.02 without introducing product-domain behavior, a competing canonical-state model or a durable UI/API technology commitment.`**

## 1. Purpose and decision level

P4.01 defines the smallest domain-neutral operator experience that Phase 4 must make coherent before implementation of the workspace shell begins.

This artifact is a subordinate platform design/review record. It does not amend Constitution or an Accepted RFC, create a new Platform Capability, promote an existing capability, create a Product Contract, select a frontend/API/runtime technology, or establish a stable public interface.

The design target is deliberately semantic rather than screen-specific:

> **The workspace is a non-authoritative presentation and interaction surface over governed organizational state. Read paths may use derived views, but consequential reliance exits those views to exact governed source state; write/action paths cross into Governed Execution rather than mutating canonical state from presentation code.**

The workspace exists to make existing Arvectum OS semantics understandable and operable. It does not create a second organizational model.

## 2. Canonical authority checked

P4.01 was evaluated against:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0`;
3. RFC-0001 — Canonical Records, graph context, Governed Execution, product/platform boundary, capability lifecycle and scoped conformance;
4. RFC-0002 — stable Subject Identity, immutable Version Identity, Head versus Effective Version, relationship semantics and projection non-authority;
5. RFC-0003 — Principal/Actor context, explicit Organization scope, deny-by-default authorization, Organizational Authority separation, minimization and failure-closed behavior;
6. RFC-0004 — Product Contract boundary, product-owned UX/domain semantics and prohibition of hidden coupling;
7. RFC-0005 — Governed Execution, gate separation, exact-version reliance, uncertainty/reconciliation and action semantics;
8. RFC-0006 — canonical Event/provenance semantics, reconstruction honesty and telemetry/projection non-authority;
9. RFC-0007 — Observation/Memory/Knowledge distinctions, explicit Knowledge promotion and retrieval/search non-authority;
10. RFC-0008 — Document/Artifact identity/version/rendition semantics, transient output and derived-view boundaries;
11. `docs/adrs/README.md` — no applicable Accepted ADR currently constrains this bounded workspace design;
12. `PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md` and P3.03–P3.10 evidence;
13. `P3.12 — Phase 3 / M3 closure review`;
14. canonical Roadmap `2.10.0` and active Phase 4 roadmap `1.0.0` before this task.

No conflict with Constitution `1.2.0` or the Accepted RFC baseline was identified.

## 3. Workspace boundary invariant

The reference workspace follows this conceptual boundary:

```text
Authenticated / attributable Principal
              ↓
Actor + explicit Organization context
              ↓
       Workspace presentation
       ┌──────────────┴──────────────┐
       ↓                             ↓
Derived/read presentation       Action intent / preflight
       ↓                             ↓
Exact governed source          Governed Execution
resolution when relied on      + applicable gates
       ↓                             ↓
Canonical Records / Events /   Canonical or external
Execution evidence / CAPs      consequential effect
```

The workspace itself does not become authoritative merely because it renders, caches, summarizes, sorts, groups or links governed state.

The following boundaries are mandatory for Phase 4 implementation:

- Organization scope is explicit; no ambient/default Organization may be inferred for governed content;
- identity or UI presence does not grant permission;
- authorization does not create Organizational Authority;
- relationship visibility does not create permission or delegation;
- search/retrieval/reconstruction/preview state remains derived;
- a subject-level navigation reference does not substitute for an exact Version Identity when consequential reliance requires version pinning;
- a visible or enabled action does not itself authorize or approve the operation;
- product context does not transfer product business semantics into the shared workspace;
- external authority remains external when authority mode is `External Reference` or `Governed Replica`;
- transient/generated/working state is not silently promoted into canonical state, Knowledge or a Governed Organizational Asset.

## 4. Bounded operator journey perspectives

The following are **journey-coverage perspectives, not new platform roles, grants, entitlements or job titles**. They describe what Phase 4 must be able to demonstrate under existing RFC-0003 Principal/Actor, authorization and Organizational Authority semantics.

| Perspective | Existing semantics used | What the journey may prove | What it must not imply |
|---|---|---|---|
| `Scoped observer` | attributable Actor + explicit Organization + current read authorization | inspect permitted governed state and derived views | organization membership, identity or UI access grants broad content access |
| `Governed-action initiator` | Actor + authorization to request a declared operation | assemble intent and initiate an allowed Governed Execution | initiation equals approval or Organizational Authority |
| `Decision/approval participant` | Actor + separately established Organizational Authority/delegation for one applicable gate | inspect and satisfy a required governed approval when authorized | a generic `approver` UI role or title creates authority |
| `Evidence reviewer` | Actor + current authorization for retained evidence | inspect provenance/reconstruction within permitted disclosure scope | reviewer access grants approval power or access to redacted/foreign evidence |

An administrator/support identity is intentionally not treated as a universal content persona. RFC-0003 administrative privilege does not automatically imply unrestricted access to Organization content.

One person or service Principal may participate in more than one perspective in different contexts. The workspace must derive actual behavior from current governed identity, Organization, authorization, delegation/authority and data-governance state rather than from these labels.

## 5. Primary operator journeys

### J-00 — Establish governed context

**Goal:** enter the workspace with an attributable Actor and one unambiguous Organization context before protected governed state is shown.

Minimum flow:

1. resolve Principal/Actor context;
2. resolve exactly one governing Organization for the workspace context;
3. expose the current Organization and attributable actor context in the shell;
4. resolve current authorization/data-handling context as required by the requested surface;
5. if Organization scope is unresolved, inconsistent or unavailable, fail closed rather than select a default Organization.

This is a precondition for every other journey.

### J-01 — Discover and inspect a governed subject

**Goal:** find an eligible governed subject and reach its canonical source without treating discovery as authority.

Minimum flow:

1. operator searches/browses within explicit Organization and permitted-purpose context;
2. CAP-003 or another bounded read projection returns only eligible derived hits with exact source attribution;
3. stale, missing or ambiguous projection entries do not become ordinary results;
4. opening a result independently re-checks source access and resolves the governed subject/version;
5. the inspection surface exposes stable Subject Identity, exact Version Identity where material, semantic type, Organization, authority mode/source and lifecycle/validation context where available and authorized.

A search hit, ranking, snippet, count or cached summary never becomes permission or canonical truth.

### J-02 — Inspect lineage and relationship context

**Goal:** understand what version is being viewed and how it is connected to other governed subjects.

Minimum flow:

1. inspect the selected exact version and its canonical lineage;
2. distinguish Canonical Head from Effective Version where they differ;
3. display ambiguity rather than silently choosing an effective version for consequential use;
4. inspect Typed Relationships with direction and subject-versus-version endpoint semantics;
5. follow permitted relationship links without inferring access, authority or delegation from the relationship itself;
6. preserve historical immutable versions as separately inspectable state within retention/access scope.

### J-03 — Trace Event, provenance and reconstruction history

**Goal:** understand why consequential state exists and what retained evidence supports it.

Minimum flow:

1. enter from a governed subject, version, Event or Execution;
2. inspect canonical Events separately from operational telemetry;
3. expose correlation and causation only where retained evidence supports them;
4. traverse version-identifiable provenance/execution references;
5. build CAP-004 reconstruction as a derived read view over exact governed evidence;
6. show `Available`, `Redacted`, `Deleted`, `Unavailable` or `Missing` evidence states honestly;
7. mark reconstruction completeness from retained evidence rather than filling gaps by inference.

Reconstruction may explain canonical history; it cannot repair or replace it.

### J-04 — Inspect a Governed Execution and its gates

**Goal:** understand what operation is/was being performed, under which versions and why it is allowed, blocked, waiting or complete.

Minimum flow:

1. inspect Execution Identity and the relevant immutable Execution Context version;
2. expose exact Workflow version and material input/Product Contract/Knowledge/Document versions where relevant and permitted;
3. distinguish authentication assurance, authorization, Organizational Authority, data-governance permission, validation and consequential approval where applicable;
4. show required versus satisfied/blocked/expired/unknown gates without inferring authority from UI labels;
5. expose waiting, retry, conflict, uncertainty, reconciliation, compensation and terminal state where material;
6. link to retained Events, outputs/artifacts and provenance.

### J-05 — Locate Document / Artifact context

**Goal:** inspect governed content without confusing logical document identity, version, representation or storage.

Minimum flow:

1. navigate to a logical Document Subject;
2. distinguish immutable Document Version from working/draft candidates;
3. inspect material Artifact/rendition identity and Content Manifest relationships where applicable;
4. expose authority mode/external source and availability/freshness where applicable;
5. expose derivation provenance for conversion/extraction/redaction/rendering or other transformations where material;
6. enforce classification, purpose, rights, retention/deletion and Organization scope at presentation and action boundaries;
7. treat preview/OCR/extracted/summarized content as derived representation rather than independent authority.

### J-06 — Locate Memory / Knowledge context through discovery

**Goal:** retrieve organizational context while preserving epistemic status and exact governed reliance.

Minimum flow:

1. search/retrieve only within current Organization/purpose/rights/classification constraints;
2. distinguish Observation, Organizational Memory, Knowledge Candidate and validated Knowledge;
3. show freshness/applicability/provenance/uncertainty where material;
4. label rankings, snippets, summaries, embeddings or retrieval results as derived discovery;
5. when a consequential action relies on Knowledge, resolve and preserve the exact effective Knowledge Version;
6. browsing, AI output or retrieval never performs Knowledge promotion implicitly.

### J-07 — Initiate a permitted governed action

**Goal:** allow the operator to request consequential work without turning presentation state into authority or mutation logic.

Minimum flow:

1. start from an explicit governed subject/execution context rather than a hidden direct-write path;
2. assemble a transient action intent describing semantic operation and target scope;
3. resolve Organization, actor, exact mutable target/input versions and Product Contract where applicable;
4. evaluate applicable authorization, data-governance and Organizational Authority/approval requirements independently;
5. create or enter the applicable Execution Context no later than before the first consequential action;
6. pin material governed versions before consequential reliance;
7. perform canonical/external mutation only through the governed runtime path;
8. render committed, blocked, waiting, conflicted, uncertain, reconciliation-required, failed or compensated outcomes from governed execution/evidence state;
9. never show optimistic success when the consequential outcome is unknown.

A hidden/disabled button is usability behavior, not the security boundary. Runtime enforcement remains authoritative.

### J-08 — Bounded product entry and return boundary

P4.01 reserves an information-architecture boundary for P4.08 but does not stabilize its protocol.

A later Product Contract-backed entry may supply explicit Organization, Product/Product Contract and governed-subject context so a product can open shared platform surfaces. The workspace may render product-owned semantic labels/types declared at the boundary, but domain decisions, business workflows and product actions remain product-owned and return to the product boundary.

No URL shape, deep-link wire format, frontend SDK or public routing contract is established by P4.01.

## 6. Workspace versus product-owned UX

### 6.1 Shared workspace responsibility

The bounded shared workspace may own domain-neutral interaction for:

- current Organization and attributable Actor context;
- generic Canonical Record/version inspection;
- Canonical Head / Effective Version distinction;
- Typed Relationship graph inspection;
- authority mode / authoritative-source presentation;
- Governed Execution status, version context and gate evidence;
- canonical Event, provenance and derived reconstruction inspection;
- Document/Artifact identity/version/rendition/provenance presentation;
- Memory/Knowledge epistemic status and exact-version presentation;
- non-authoritative discovery/search entry into governed sources;
- generic governed action intent/preflight and handoff into existing Governed Execution;
- evidence availability, uncertainty, stale/ambiguous state and failure-closed UX;
- capability/contract lifecycle labels where needed to avoid overstatement.

### 6.2 Product-owned UX responsibility

The shared workspace must not absorb by default:

- tender, procurement, CRM, finance, legal, marketing or other domain concepts/taxonomies;
- domain-specific queues, stages, prioritization, scoring, recommendation or ranking rules;
- business decision logic or domain approval thresholds;
- product-specific forms, validation rules, prompts, agents or domain workflows;
- product-specific document taxonomies, templates or legal/commercial interpretation;
- product-specific compliance narratives or reports;
- business dashboards/metrics whose meaning is product-specific;
- domain-specific search relevance, saved-search behavior or recommendation UX;
- commercial packaging, customer onboarding or final branded product experience.

A Product Contract may declare product-owned domain types at the boundary. Declaration permits interoperable rendering/interaction; it does not transfer their architectural ownership to the platform.

The shared workspace is therefore an **operator surface over platform-governed semantics**, not a generic product orchestration layer.

## 7. Information architecture hypothesis

The smallest coherent Phase 4 IA is:

```text
Workspace shell
├── Persistent context
│   ├── Organization
│   ├── attributable Actor/Principal context
│   ├── optional Product / Product Contract entry context
│   └── current governed reference / breadcrumb
│
├── Discover
│   └── derived cross-source discovery → exact governed source
│
├── Records
│   ├── subject
│   ├── exact versions / Head / Effective
│   └── typed relationships
│
├── Executions
│   ├── execution state
│   ├── material versions
│   └── authorization / authority / validation / approval gates
│
├── Evidence
│   ├── canonical Events
│   ├── provenance
│   └── derived reconstruction
│
├── Documents
│   ├── Document subject / versions
│   ├── Artifact / rendition / manifest
│   └── derivation / authority / handling context
│
└── Knowledge
    ├── Observation / Memory / Candidate / validated Knowledge
    ├── exact versions / freshness / provenance
    └── derived retrieval context
```

### 7.1 IA rationale

- `Discover` is a utility/perspective, not an authoritative object store. It always exits to governed sources before consequential reliance.
- `Records` exposes the generic Kernel object/graph semantics needed by P4.03.
- `Executions` keeps action/gate meaning distinct from static records and avoids inventing a global product task queue.
- `Evidence` separates Event/provenance/reconstruction semantics from mutable diagnostic dashboards.
- `Documents` and `Knowledge` expose materially distinct Accepted semantics rather than collapsing all content into generic files or search results.
- no top-level `Approvals` persona is introduced because approval authority is contextual to a governed decision/execution, not a UI role;
- no generic `Dashboard` is required for M4 because aggregate/product KPI meaning would either be derived operational state or product-specific UX and is not necessary to prove the workspace baseline;
- governed actions originate from the relevant subject/execution context rather than a global command palette that could hide authority and target-version context.

### 7.2 Navigation reference semantics

The IA assumes conceptual governed references such as Organization, Subject, Version, Execution, Event, Document, Artifact and Knowledge references. These are semantic navigation inputs, not a stable URL/API/wire schema.

Rules:

1. an exact Version reference must remain exact and must not silently redirect to the current Head;
2. a Subject reference may resolve for navigation, but consequential reliance must preserve the exact resolved Version where required;
3. search/reconstruction-derived references require current source authorization before source disclosure;
4. Organization scope is preserved across navigation and re-validated at protected boundaries;
5. product entry context is not permission and must not bypass Product Contract validation or runtime authorization;
6. filenames, storage locators, vendor IDs, search document IDs and frontend route IDs do not become organizational identity by convenience.

## 8. Presentation/read-model authority classification

P4.01 uses five presentation classes to prevent UI state from becoming accidental authority:

- `Canonical-source presentation` — renders an exact governed source/version; the rendered view is still not a second canonical source;
- `Derived projection` — rebuildable/derived state such as search, graph layout, timeline, reconstruction or summary;
- `External-authority presentation` — renders governed reference/replica state while explicitly preserving the external authoritative source;
- `Transient interaction state` — uncommitted UI/action/draft state;
- `Governance-result presentation` — renders an authorization/gate/approval outcome from its governed source; the UI representation does not itself create the result.

| Presentation/read model | Source of meaning | Class | Reliance / guardrail |
|---|---|---|---|
| current Organization context | RFC-0003 governed organization/tenant context | governance-result presentation | must resolve explicitly; unresolved scope blocks governed content/actions |
| Actor/Principal display context | Identity/authentication/delegation context | governance-result presentation | attribution only; identity/authentication does not imply authorization or authority |
| governed subject summary | exact Canonical Record | canonical-source presentation | display exact version when material; UI copy/cache is not canonical |
| lineage / Head / Effective view | canonical lineage + resolution rules | derived projection | ambiguity is shown; consequential reliance does not guess |
| relationship graph layout | Typed Relationship records | derived projection | graph edge does not grant permission/authority |
| cross-source search hit/snippet | CAP-003 projection + exact source attribution | derived projection | current constraints are re-checked; ranking/snippet is not truth or permission |
| search counts/facets | eligible derived result set | derived projection | must not leak existence/metadata of inaccessible resources |
| execution state/gate surface | Execution Context + governed gate evidence | canonical/governance-result presentation | gate states are displayed, not minted by UI |
| Event timeline | canonical Events | derived projection over canonical evidence | no universal total order is implied unless source contract provides one |
| provenance graph | version-identifiable governed references | derived projection | only retained provenance may be claimed |
| reconstruction view/package | CAP-004 over governed reconstruction manifest | derived projection | completeness/availability exact; restricted evidence does not leak source pins |
| Document version metadata | admitted Document Canonical Record | canonical-source presentation | logical Document/version remain distinct from file/locator |
| Document preview/OCR/extraction | Artifact/rendition or derived content | derived/external presentation as applicable | preview cannot bypass source access; derived content is not independent authority |
| Working Copy / generated draft | editing/generation state | transient interaction state | non-canonical until governed checkpoint/admission where required |
| Knowledge record | validated Knowledge Canonical Record | canonical-source presentation | exact Knowledge version required for consequential reliance |
| retrieval/RAG-like result | CAP-002/CAP-003 derived retrieval | derived projection | epistemic status and source version remain explicit; retrieval does not validate |
| external-source freshness/sync status | External Reference/Governed Replica contract/evidence | external-authority presentation | local availability/freshness does not convert external facts to Native authority |
| action draft/preflight | operator input + current resolved context | transient interaction state | no canonical mutation or authority created before governed execution/gates |
| authorization/authority/approval result badge | current governed decision/evidence | governance-result presentation | badge is descriptive only; runtime decision remains authoritative |
| filters/sort/layout/preferences | UI-local/session state | transient interaction state | no organizational meaning or canonical status by default |
| product-entry context | Product identity + applicable Product Contract reference | derived navigation context | does not grant access/authority or transfer product semantics to platform |

P4.02–P4.10 may refine internal presentation models. Any durable read-model store, stable public schema or cross-product API commitment re-opens the ADR gate.

## 9. Fail-closed and uncertainty UX states

The workspace must distinguish a **security/governance block** from a **safe uncertainty display**. It must not convert missing evidence into positive authority or optimistic success.

| Condition | Required UX disposition |
|---|---|
| Organization cannot be resolved unambiguously | fail closed; show no governed content/action; never choose a default tenant |
| target/source belongs to another Organization without explicit governed access | deny without content/metadata/existence leakage beyond the permitted error surface |
| authorization is denied or required policy evaluation is unavailable | block protected read/action; collection surfaces filter inaccessible items rather than leak them |
| required Organizational Authority/delegation is absent, expired or unresolved | action remains blocked/awaiting authority; UI role/title cannot substitute |
| required Product Contract is missing/incompatible for product/platform reliance | block the governed product entry/action; no hidden coupling fallback |
| Effective Version or exact materially required version is ambiguous/missing | show ambiguity/insufficient evidence and block consequential reliance |
| search projection is stale, missing or ambiguous | do not return it as an ordinary current hit; resolve/rebuild/reconcile before reliance |
| source access changed after a search/retrieval hit was created | re-check source access; hit visibility never grants later source access |
| external authority is stale, unavailable, conflicting or freshness is insufficient | expose authority/freshness status and block operations that require stronger current evidence |
| evidence is Redacted/Deleted/Unavailable/Missing | show explicit disposition and incomplete reconstruction; do not invent content or leak protected source references |
| authentication/delegation/policy/gate state has expired during a long-running execution | require applicable re-evaluation before consequential continuation |
| consequential external outcome is unknown | show `uncertain / reconciliation required`; do not claim success and do not blindly retry a non-idempotent effect |
| canonical target changed concurrently | expose conflict and require re-resolution/retry under governed semantics; never silently overwrite |
| generated Artifact, Working Copy, Observation or AI output is not admitted/validated | label transient/candidate status; no silent promotion to canonical state, Knowledge or organizational asset |
| capability/contract dependency is `Incubating` / `Provisional` | preserve lifecycle/status language; do not present as `Active`, Stable or supported production guarantee |
| derived preview/summary is prohibited or cannot be generated safely | omit/block the derived representation rather than fall back to unauthorized source content |

Critical states must be understandable through textual/semantic status and not depend only on color, iconography or visual position. P4.10 will establish the broader accessibility/usability baseline.

## 10. Governed action interaction contract

Phase 4 action UX must preserve this semantic sequence:

```text
Select semantic operation
        ↓
Transient action intent
        ↓
Resolve Organization + Actor + exact target/input versions
        ↓
Resolve Product Contract if applicable
        ↓
Evaluate authorization + data governance
        ↓
Evaluate Organizational Authority / approval requirements
        ↓
Create / continue Execution Context
        ↓
Pin material governed versions
        ↓
Perform governed consequential effect
        ↓
Render outcome from governed execution/evidence
```

Presentation code may help collect intent, explain requirements and display gate outcomes. It must not:

- write canonical storage directly;
- bypass Product Contract or capability boundaries through private internals;
- treat front-end feature flags/hidden buttons as authorization;
- approve on behalf of an actor merely because the actor can technically submit a request;
- replace exact target/input versions with the latest version silently at commit time;
- retry unknown consequential external effects blindly;
- rewrite terminal history to make an operation appear successful.

## 11. P4.02 implementation handoff

P4.02 should implement only the smallest reversible workspace shell needed to make the P4.01 boundary executable.

Minimum shell responsibilities:

1. visible explicit current Organization context;
2. attributable Actor/Principal context where relevant and permitted;
3. domain-neutral navigation destinations: `Discover`, `Records`, `Executions`, `Evidence`, `Documents`, `Knowledge`;
4. current governed reference/breadcrumb capable of distinguishing Subject and exact Version references;
5. explicit blocked/unresolved-scope state;
6. internal presentation-state model that is non-authoritative and disposable;
7. no direct canonical mutation path;
8. no product-domain screen or job-title role taxonomy;
9. no stabilized frontend framework, URL/deep-link schema, BFF/API or public serialization contract.

Minimum P4.02 executable evidence should prove, at least:

- unresolved Organization fails closed;
- a wrong-Organization navigation reference cannot expose content or protected metadata;
- actor attribution and Organization context survive navigation;
- Subject and exact Version references remain distinguishable;
- an exact historical Version reference is not silently redirected to Head;
- presentation/navigation state cannot create authorization or Organizational Authority;
- derived counts/navigation affordances do not leak inaccessible objects;
- optional future product context is treated as context only, not permission;
- critical context and blocked-state meaning is available as text/semantics, not color alone.

P4.02 may use an internal reversible presentation adapter over current reference-runtime semantics. A public/cross-product contract is neither required nor authorized by P4.01.

## 12. ADR, Product Contract and capability disposition

### 12.1 ADR

**No new ADR is required for P4.01.**

This task selects no:

- frontend/runtime framework;
- stable route/deep-link or wire schema;
- BFF/API topology;
- IAM/session/PDP/PEP implementation;
- durable workspace/read-model/cache store;
- search/vector engine;
- document/object store;
- design-system package contract;
- stable public frontend SDK/API;
- separately deployable UI/API service topology.

The Phase 4 ADR gate remains armed before material reliance on any such durable or externally constraining choice.

### 12.2 Product Contract

P4.01 creates no Product Contract because it implements no real product/platform reliance. P4.08 remains responsible for the bounded real Product Contract-backed product entry point.

The IA is intentionally capable of carrying Product/Product Contract context later without defining a stable deep-link or routing contract prematurely.

### 12.3 Capability lifecycle

P4.01 does not create `CAP-005 Workspace`, promote a workspace capability, or change CAP-001 through CAP-004.

CAP-001 through CAP-004 remain `Incubating / Provisional`. Phase 4 roadmap activity and successful operator design do not imply lifecycle `Active`, operational readiness, production, Stable Product Contract or SLA/support status.

## 13. Functional role cross-review

Cross-review followed the repository iterative-completion rule. It is an execution-quality mechanism and not formal approval evidence.

### Iteration 1 — Architecture / product / governance

Material finding: early persona wording could be misread as a new shared role/entitlement taxonomy, and a generic `Approvals/Work` area could accidentally absorb product workflow responsibility.

Correction:

- personas were reframed as journey-coverage perspectives grounded in existing Principal/Actor/authorization/authority semantics;
- no generic `approver` platform role was introduced;
- approval remains execution/gate contextual;
- global product task/workflow orchestration was excluded from the shared IA;
- product UX/domain responsibility was made explicit.

### Iteration 2 — Security / privacy / tenant sovereignty

Material finding: content could be protected while search counts, snippets, graph edges, previews or reconstruction references still leaked inaccessible object existence/metadata.

Correction:

- no-existence/metadata-leak guardrails were added to collection/search/navigation views;
- exact source access is re-evaluated after discovery;
- unresolved Organization always fails closed;
- derived previews/summaries inherit source access constraints;
- restricted reconstruction evidence cannot expose protected source pins;
- administrator/support context was explicitly prevented from implying unrestricted content access.

### Iteration 3 — Operations / UX / accessibility

Material finding: technically correct states could still mislead an operator if `blocked`, `awaiting approval`, `stale`, `unknown outcome`, `incomplete evidence` and `failed` were collapsed into generic success/error UI.

Correction:

- explicit uncertainty/failure-closed state inventory was added;
- unknown consequential external outcome now requires reconciliation state rather than optimistic success/blind retry;
- authority/freshness/evidence completeness must remain visible where material;
- critical states must be conveyed semantically/textually rather than through color alone.

### Iteration 4 — Engineering / architecture reversibility

Material finding: conceptual navigation references and read-model names could be implemented as an accidental stable route/API/BFF/public schema contract before evidence exists.

Correction:

- navigation references are explicitly semantic/conceptual only;
- URL, serialization, BFF/API and frontend framework remain unstabilized;
- P4.02 is bounded to an internal reversible shell/adaptor;
- durable read-model/API/frontend decisions remain ADR-gated.

After Iteration 4, no remaining material objection was identified for the P4.01 lifecycle stage. Further UI component taxonomy, visual design, product flows or technology selection would be premature and belongs to later Phase 4 tasks.

## 14. Exit assessment

P4.01 exit conditions are satisfied:

1. bounded operator journey perspectives are defined without inventing platform job-title roles or authority;
2. minimum M4 journeys cover governed context, records/relationships, provenance/reconstruction, executions/gates, documents/artifacts, memory/knowledge/search and governed action initiation;
3. workspace responsibility is explicitly separated from product-owned UX/domain semantics;
4. a bounded domain-neutral IA is defined for `Discover`, `Records`, `Executions`, `Evidence`, `Documents` and `Knowledge` under persistent Organization/Actor context;
5. presentation/read models are inventoried and classified so derived/transient state cannot become canonical authority;
6. fail-closed, insufficient-authority, stale, ambiguous, unavailable and uncertain states are explicit;
7. the action path preserves Governed Execution and exact-version/gate semantics;
8. no product-domain behavior, new Platform Capability, Stable Product Contract/public API or durable UI technology commitment is introduced;
9. no ADR threshold is crossed;
10. four functional cross-review iterations completed with no material objection remaining for this stage.

**Final decision: `PASS — P4.01 complete for the bounded Phase 4 workspace-design scope.`**

## 15. Next canonical action

Proceed to:

> **`P4.02 — Organization context, identity and scoped navigation shell`.**

P4.02 should implement the smallest internal reversible shell satisfying the P4.01 boundary and evidence requirements, then pass `R9 — Workspace Boundary Review` before the record/execution/document/knowledge operator surfaces expand.