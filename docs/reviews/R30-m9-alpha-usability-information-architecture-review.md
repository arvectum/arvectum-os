# R30 — M9-alpha Usability / Information Architecture Review

Status: `Complete / PASS`
Date: `2026-08-21`
Owner: `ООО «Арвектум»`
Task classification: `platform` with governance implications
Gate: `R30 — M9-alpha Usability / Information Architecture Review`
Milestone result: `M9-alpha — Usable Internal Workspace — Achieved / PASS` within the exact internal Phase 9 scope
Predecessor: `P9.06 — Complete / PASS`
Successor: `P9.07 — Product-owned workspace surfaces / composition`
Workspace release: `p9.06.2`
Internal application contract: `4`

## 1. Purpose and scope

R30 reviews the integrated Productive Workspace ordinary path established by P9.03–P9.06 against the exact P9.01 J1–J4 acceptance script. The gate asks whether an attributable owner/operator can use the normal private Workspace to understand attention, find and understand a real organizational object, inspect the related governed Execution/Decision and initiate one bounded real governed interaction without terminal/GitHub/internal-identifier knowledge for ordinary steps.

R30 is an internal usability and information-architecture gate. It does **not** establish public/customer Production, a public or stable browser/API/SDK surface, an SLA/support promise, a Stable Product Contract, an Active Platform Capability, broad browser/screen-reader certification, full M9 closure or Organizational/AI Authority.

P9.11 remains the later gate for real daily-use dogfooding and recurring-friction disposition. Therefore R30 evidence is deliberately described as deterministic browser-component acceptance plus real retained platform adapter/security evidence; it is not represented as a completed manual owner working session or a human task-time benchmark.

## 2. Canonical authority checked

Checked before and during review:

1. Constitution `1.2.0` — `Ratified`, frozen;
2. RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
3. RFC-0001 — domain-neutral platform boundary, canonical-state discipline and evidence-driven reuse;
4. RFC-0003 — Identity / Authentication / Authorization / Organizational Authority / Data Governance separation, least privilege, Organization scope and fail-closed access;
5. RFC-0005 — Governed Execution, independent governance gates, consequential-action boundary, uncertainty/retry/replay requirements;
6. RFC-0006 — append-only canonical Events, provenance honesty and non-authoritative projections;
7. RFC-0008 — Document/version/source/authority/provenance distinctions relevant to the retained EIS-backed F1 source;
8. ADR-0001 — Accepted Productive Workspace SPA/BFF/session/release topology;
9. P9.01 — exact J1–J4 acceptance journeys, F1/F2/F3 fixture registry and M9-alpha hard acceptance fields;
10. P9.03–P9.06 implementation/closure evidence;
11. canonical Phase 9 and master roadmaps.

No higher-authority conflict remains after the R30 revisions. No Constitution, RFC, ADR, Product Contract or lifecycle amendment is required.

## 3. Functional cross-review

R30 completed three functional cross-review iterations, below the maximum of seven.

### Iteration 1 — ordinary-path information architecture

Material findings:

1. the P9.04 `My Work` attention item opened only an opaque queue focus view and did not continue into the J3 human execution/context path;
2. the P9.05 object context exposed related Execution/Event only inside technical evidence and did not offer an ordinary governed continuation;
3. discovery supported server-side kind filtering but the global browser UX did not expose the J2 narrowing control.

Revisions:

- the **real live retained P7.06-UI4 waiting-preflight** attention item gains `Open execution context` to `/governed`;
- controlled scenario/uncertainty items do **not** gain an action shortcut merely because they are visible;
- the real F1 object context gains `Open related execution and governed action`;
- global discovery exposes a human `Result type` filter for Records, Documents, Knowledge and Executions, reusing the existing authorized server-side query contract.

Result: IA continuity repaired without changing authority/runtime semantics.

### Iteration 2 — accessibility and technical-detail discipline

Material findings:

1. SPA route transitions changed the visible view without explicitly moving keyboard focus into the newly selected main content;
2. exact technical identifiers were visually collapsed inside `<details>` but still pre-rendered into the DOM, which was weaker than the declared “on demand rather than primary UX” requirement.

Revisions:

- SPA route transitions focus the persistent semantic `<main id="workspace-main" tabindex="-1">` region after navigation;
- exact Subject/Version/Execution/Event/checkpoint/provenance values are not rendered until the user explicitly opens the technical drill-down.

Result: keyboard focus continuity and technical-evidence separation strengthened.

### Iteration 3 — final authority/security/release review

Reviewed the resulting diff, integrated J1–J4 interaction test, negative-path tests, BFF security regressions, production-build reproducibility and exact-release pinning.

Result: **no remaining material objection**. The final implementation diff changes only Productive Workspace frontend/release/tests and deterministic built assets; no platform authority engine, Product Contract, product business logic or canonical-runtime owner is modified.

## 4. P9.01 integrated acceptance record

Acceptance mode: deterministic browser-component journey over the real Productive Workspace components and contracts, combined with the already-proven real retained P7.06-UI4 F2 adapter/BFF security boundary.

| Field | R30 result |
|---|---|
| Organization | ООО «Арвектум» |
| Actor context | attributable owner/operator context, resolved server-side |
| Workspace release | `p9.06.2` |
| Application contract | `4` |
| Primary real fixtures | F1 real EIS-backed Document notice `0344100006426000005`; F2 real retained P7.06-UI4 Execution/provenance/preflight contour |
| Human entry terms | `0344100006426000005`, human labels/source/context |
| Ordinary internal-ID dependency | `false` |
| Terminal/GitHub escape | `false` |
| Authority/success misrepresentation | `false` |
| Organization-scope violation | `false` |
| Technical identity/provenance reachable on demand | `true` |
| Governed interaction outcome | real `WAITING / fail-closed` preflight; no missing decision manufactured |
| Canonical mutation performed | `false` |
| External effect performed | `false` |
| Human performance/SLA claim | none; automated timing is not represented as human task time |

The deterministic integrated journey exercises seven primary interactions: open real execution context from attention; submit global search; narrow result type; submit narrowed discovery; open object context; open related governed action; run governed preflight. This interaction count is comparative acceptance instrumentation, not a public UX SLA.

## 5. J1–J4 result

### J1 — Morning overview / what needs attention — PASS

- Home exposes `Needs attention` directly;
- categories, source, reason and legitimate next step are text-first;
- controlled scenario evidence remains visibly scenario evidence;
- the real retained waiting-preflight item continues into human Execution/Decision context;
- stale/degraded queue behavior remains fail-closed and does not disclose protected denied-source counts.

### J2 — Find anything — PASS

- the real F1 EIS-backed object is found using notice number `0344100006426000005` rather than Subject/Version identifiers;
- source/type/context are human-readable;
- global discovery now supports result-type narrowing;
- opening uses an opaque browser reference and revalidates current source/access server-side;
- degraded discovery withholds protected result detail and does not create a denied-result cardinality oracle.

### J3 — Understand context — PASS

- opened F1 context presents what the item is, authoritative source, `External Reference` authority mode, lifecycle/validation context, process meaning and legitimate next step before technical identity;
- related governed continuation is navigable without copying an Execution/Version identifier;
- exact technical Subject/Version/Execution/Event/provenance values are absent from the DOM until explicit technical drill-down;
- Observation/Memory/Knowledge distinctions from P9.05 remain unchanged.

### J4 — Make a governed decision/action — PASS within the declared real fail-closed slice

- the user enters from human context rather than an internal execution identifier;
- Authorization, Organizational Authority, Data Governance and Consequential Approval remain separate and visibly independent;
- `Run governed preflight` reuses the real P7.06-UI4 command boundary;
- server-side access/preflight reconstruction, CSRF/Host/Origin/session/release gates remain in force;
- the browser sends no governance decision payload, candidate mutation, retry instruction or external-effect data;
- the real result remains `WAITING / fail-closed` and writes only minimized owner-local non-canonical proof evidence;
- no canonical mutation or external effect is manufactured for usability evidence.

## 6. Accessibility / information architecture baseline

R30 confirms the bounded internal baseline required at this gate:

- critical state and authority meaning is textual rather than color-only;
- navigation, search, selects, buttons, links, headings, main region and technical disclosure use native semantic controls/regions;
- SPA navigation places focus into the selected main content region;
- technical IDs are explicitly disclosed on demand rather than pre-rendered as ordinary-path content;
- blocked/degraded/error states are described in text and fail closed;
- existing responsive source rules retain a 320px minimum layout baseline and narrow-screen reflow;
- static key-text contrast inspection for the current stylesheet remains at or above the 4.5:1 normal-text baseline for the reviewed primary foreground/background pairs.

This is **not** a claim of exhaustive assistive-technology certification, public browser compatibility, every-state visual QA or external accessibility conformance. Those broader obligations remain subject to later hardening/operational evidence.

## 7. CI and exact-release evidence

Clean implementation/reconciliation head:

`441106e65f7a69c54ff3ff89885ef1596b03e0a7`

Normal CI on that head:

- `Productive Workspace CI #60` / run `32487968433` — `SUCCESS`;
- frontend typecheck — PASS;
- frontend interaction suite — PASS, including the integrated R30 J1→J4 journey;
- Web Storage bearer-material guard — PASS;
- production build — PASS;
- BFF security/context tests — PASS;
- clean second-build reproducibility — PASS;
- committed production assets exactly match the deterministic build — PASS;
- release-pinned asset verification — PASS;
- `Reference Python CI #292` / run `32487968464` — `SUCCESS`;
- reference architecture suite — `1301 tests`, `OK`;
- generated-Python-artifact rejection — PASS.

After canonical review/roadmap synchronization, the final closure branch head also passes the normal Productive Workspace and Reference Python CI gates. Temporary write-capable synchronization helpers are absent from the final PR diff and closure state.

## 8. M9-alpha exit evaluation

All declared M9-alpha exit criteria are satisfied within the exact private internal scope:

1. useful Home — PASS;
2. My Work / attention — PASS;
3. human-readable real object discovery — PASS;
4. real Document/Record/Knowledge context — PASS;
5. real Execution/Decision in human terms — PASS;
6. one bounded real governed interaction — PASS (`WAITING / fail-closed`, truthful);
7. exact technical identity/version/provenance on demand — PASS;
8. exact P9.01 J1–J4 integrated acceptance — PASS;
9. R29 and R30 with no unresolved material finding — PASS.

Therefore:

> **`M9-alpha — Usable Internal Workspace` = Achieved / PASS**, scoped to the current `Local / Persistent Internal / owner-operated` environment and the exact Phase 9 acceptance evidence.

This milestone does not promote any Platform Capability or Product Contract, does not create a public/stable interface, and does not close M9.

## 9. Final disposition

`R30 — Complete / PASS`.

No unresolved material finding remains. The next canonical implementation action is:

> **`P9.07 — Product-owned workspace surfaces / composition`.**

P9.07 must preserve the R30 boundary: product semantics remain product-owned and may enter Workspace only through explicit governed Product Contract/extension boundaries; successful composition does not itself promote a Product Contract or Platform Capability lifecycle state.
