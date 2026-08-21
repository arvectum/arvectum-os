# P9.05 — Human-friendly Records / Documents / Knowledge + global search — implementation review and closure evidence

Status: `PASS`
Date: `2026-08-21`
Scope: Phase 9 implementation/closure evidence only. This record is not RFC/ADR acceptance, Product Contract stabilization, Platform Capability promotion, public-API approval, operational-readiness approval, or Organizational Authority delegation.

## Authority checked

The implementation was checked against:

- Constitution `1.2.0` — `Ratified`;
- RFC-0001…RFC-0008 — `Accepted`, with direct focus on RFC-0002, RFC-0003, RFC-0007 and RFC-0008;
- ADR-0001 — `Accepted` Productive Workspace browser application topology;
- `P9.01` operator acceptance journeys, especially J2/J3 and the real F1 EIS fixture;
- the canonical Phase 9 and master roadmaps.

No higher-authority conflict was found. The change remains inside the existing Productive Workspace application boundary and does not create a new canonical store, decision authority, product/platform contract, or platform lifecycle transition.

## Delivered

### Authorized discovery read model

`reference/python/workspace_app/discovery.py` introduces a bounded, rebuildable, read-only discovery projection over already-proven P7.06/P7.04 governed read sources:

- `record`, `document`, `knowledge`, and `execution` discovery kinds;
- human semantic role, title, summary, source, authority mode and governed-state labels in the ordinary result path;
- opaque browser object references derived from exact subject/version identity, with collision detection;
- exact Subject/Version/provenance retained for traceability but omitted from ordinary search-result payloads;
- query/result bounds and fail-closed degraded behavior;
- no durable search database and therefore no second source of truth in this first implementation;
- each search/inspection rebuilds from the current authorized exact-release source snapshot.

### Workspace BFF

The Productive Workspace BFF now exposes:

- `GET /api/app/v1/discovery?q=&kind=`;
- `GET /api/app/v1/objects/{opaque_id}`.

Both routes use the server-resolved current `AccessContext`. Browser-supplied Organization/actor values do not choose scope. Object inspection revalidates current access/source state before protected context is disclosed. Unknown/malformed opaque references remain generic and do not become an existence oracle.

### Human-first browser surfaces

The SPA now provides:

- persistent global search in the application shell;
- dedicated `Search`, `Records`, `Documents`, and `Knowledge` routes;
- human-readable result cards with source/authority/state context;
- object context with meaning, authoritative source/mode/scope, lifecycle/validation state, relevant process and next step;
- exact technical Subject/Version/provenance only in an explicit technical drill-down;
- explicit messaging that read visibility/search results provide no Authorization, Organizational Authority, consequential approval, or canonical authority.

Knowledge-related presentation preserves `Observation`, `Organizational Memory`, `Knowledge Candidate`, validated `Knowledge`, and governed-learning distinctions. Document presentation preserves declared authoritative source and `External Reference` semantics where applicable.

## Real acceptance evidence

The P9.01 F1 EIS fixture is exercised directly:

- a user can search the real notice context `0344100006426000005` without knowing an Arvectum Subject/Version identifier;
- the returned document is presented as a human-readable governed Document with `ЕИС / zakupki.gov.ru` as source and `External Reference` authority mode;
- the search-result projection does not expose the exact internal Subject identity, Version identity, or storage identifier;
- opening the opaque result exposes human context first and exact technical/provenance evidence on demand;
- when the retained UI4 exact F1 preflight is available, related execution/event/checkpoint continuity and waiting governance gates are presented without creating a mutation/action path.

This satisfies the J2/J3 ordinary-path requirement without replacing retained exact-identity evidence.

## Security, privacy, authority and semantics review

Regression coverage confirms:

- Organization and actor scope are server resolved;
- current access is revalidated for protected reads;
- denied-result counts are not exposed;
- protected snippets are minimized;
- search/result projections are explicitly derived and non-authoritative;
- degraded source state withholds protected results instead of serving stale protected details as current;
- malformed/unknown object references return a generic unavailable result;
- exact identifiers remain available only after an authorized object open;
- browser Web Storage remains rejected;
- no consequential write/effect path is introduced;
- Knowledge semantics are not flattened (`Observation ≠ validated Knowledge`);
- Documents preserve authority-source semantics (`External Reference` is not promoted to Native authority).

## Cross-review evidence

### Iteration 1

Functional source review and CI passed for backend behavior, frontend typecheck/interactions, Web Storage guard and production build. The only failing gate was the expected reproducibility mismatch because committed SPA assets still represented the preceding `p9.04.1` release.

A bounded one-shot reconciliation job, restricted to PR `#116`, its exact head branch and repository actor, rebuilt the production SPA and committed only `reference/python/workspace_frontend/dist/**`. The helper was then removed before closure; the canonical workflow returned to read-only permissions.

### Iteration 2

No material functional objections remained.

Evidence on implementation head `5ae5670e1a09530d7946df047046da969f7a3df2`:

- Productive Workspace CI run `32477614572` — `PASS`:
  - BFF security/context tests — `PASS`;
  - frontend typecheck — `PASS`;
  - frontend interaction tests — `PASS`;
  - Web Storage guard — `PASS`;
  - production SPA build — `PASS`;
  - committed `package-lock.json` / `dist` reproducibility gate — `PASS`;
  - release-pinned production asset verification — `PASS`.
- Reference Python CI run `32477614687` — `PASS`, including architecture-fitness coverage.

The final source bundle is reproducible and release-pinned; the temporary reconciliation helper is absent from the closure state.

## Release evidence

Productive Workspace application release:

- release: `p9.05.1`;
- internal application API contract: `3`;
- classification: `bounded-internal-provisional`;
- public API: `false`.

The committed production SPA manifest/index/assets are mutually consistent with that release and pass the release-pin verifier.

## Closure judgement

`P9.05` implementation acceptance: **PASS**.

The operator can discover, distinguish and open real governed objects through human-readable context; exact identity/version/provenance remains reachable on demand; search remains derivative/rebuildable/non-authoritative; protected existence/content is disclosed only through current authorized reads; Records/Documents/Knowledge semantics and authority boundaries remain intact.

This closure does **not** promote search or discovery to an `Active` Platform Capability, does not establish a Stable Product Contract, does not make the Workspace a public API or customer-Production commitment, and does not grant Organizational Authority.

Canonical next Phase 9 implementation item after roadmap synchronization: `P9.06 — Governed action UX`.
