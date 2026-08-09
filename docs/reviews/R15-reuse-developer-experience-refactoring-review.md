# R15 — Reuse / Developer Experience Refactoring Review

Status: `PASS`
Review date: `2026-08-09`
Task classification: `platform` with `product_contract` boundary implications
Scope: accumulated P5.08/P5.09 two-consumer reuse evidence and developer-experience refactoring

## 1. Decision

R15 passes after two bounded reuse/developer-experience findings were remediated without broadening the platform contract.

The second materially distinct P5.09 consumer is strong enough to justify retaining the internal/provisional Product Contract → exact dependency/version resolution → composition facade → capability-adapter path. It is not evidence for a public SDK, plugin runtime, registry, Stable Product Contract or capability lifecycle promotion.

No Constitution amendment, RFC change or ADR is required for R15. The changes are internal/provisional implementation refactoring below the existing Accepted RFC boundaries.

## 2. Canonical basis checked

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` per the RFC Index;
- RFC-0001 — validated reuse over speculative generality, explicit Product Contract boundaries and non-accidental public interfaces;
- RFC-0003 — Organization, identity, Authorization, Organizational Authority and data-governance separation;
- RFC-0004 — Product Contract as the explicit versioned product/platform boundary, with hidden coupling prohibited and Product Contract lifecycle distinct from capability lifecycle;
- RFC-0005 — Product Contract continuity does not grant execution authority and consequential execution remains gated;
- RFC-0006 — reconstruction/provenance evidence remains observational/non-authoritative where derived;
- ADR Index — no applicable Accepted ADR requires or constrains this bounded refactor beyond the Accepted RFC baseline;
- [`P5.08`](P5-08-workspace-capability-integration-adapters.md), [`P5.09`](P5-09-second-materially-distinct-integration-reuse-proof.md) and [`R14`](R14-developer-safety-contract-health-review.md) review evidence.

## 3. Demonstrated two-consumer evidence

The first bounded product needs both capability reliance and workspace presentation. The second P5.09 consumer is materially different: it is a headless read-only CAP-004 evidence/reconstruction extension with its own `Provisional 0.1.0` Product Contract and no workspace, task/disposition or canonical-mutation path.

Both consumers reuse `arvectum_os_ref.integration_adapters` and the same exact Product Contract/dependency-resolution/composition path. This is sufficient to review which implementation abstractions are genuinely shared and which assumptions were shaped by the first consumer.

## 4. Findings and remediation

### R15-F1 — workspace-shaped shared adapter state

**Finding:** `IntegrationAdapters` eagerly stored a workspace adapter even though the materially distinct second consumer does not use workspace presentation. That made first-consumer presentation needs look universal in the shared integration object.

**Remediation:** the shared dataclass state is narrowed to the demonstrated cross-consumer core:

- exact composed facade;
- capability adapter delegation.

Workspace presentation is now an explicit optional binding through `compose_workspace_adapter(...)`. The existing `adapters.workspace` access remains only as a lazy internal compatibility convenience and is no longer part of shared stored adapter state.

**Disposition:** `REFINE`.

### R15-F2 — stale scaffold/developer path

**Finding:** P5.05 scaffolding still taught new integrations to enter through the lower-level `integration_composition` facade even after P5.08/P5.09 demonstrated `integration_adapters` as the reused integration-facing seam.

**Remediation:** the starter template and local integration harness now compose through `IntegrationAdapters` and opt into workspace presentation explicitly when needed. `LocalIntegrationHarnessResult.facade` remains a compatibility accessor over `adapters.facade`; the reusable stored state is the adapter core.

**Disposition:** `REFINE`.

No additional generic DTO, extension base class, registry, plugin API, manifest or package abstraction was introduced.

## 5. Retain / refine / reject disposition

### Retain

- RFC-0004 Product Contract as the single governed product/platform boundary authority;
- P5.02 declaration validation, including P5.09-F1;
- P5.03 exact governed dependency/version resolution;
- R14 requirement for explicit current governed provider/version evidence at dependency-backed reliance;
- P5.04 composition facade as the internal semantic composition path below the adapter seam;
- P5.08 `IntegrationAdapters` as the shared internal/provisional integration-facing module;
- existing capability/workspace/reconstruction semantic owners and fail-closed security/rights behavior.

### Refine

- shared adapter state to `facade + capabilities` only;
- workspace into an explicit optional consumer binding;
- P5.05 scaffold/harness to teach the demonstrated adapter seam rather than the lower-level facade as the default developer entry.

### Reject for R15

- public/Stable SDK or API;
- language/package compatibility promise;
- generic plugin/extension runtime or registry;
- generic cross-consumer DTO/schema layer;
- automatic Product Contract stabilization;
- CAP-001..CAP-004 promotion to `Active`;
- provider-state cache/freshness registry replacing R14 explicit evidence;
- new authorization, Organizational Authority, approval or lifecycle authority in integration tooling.

## 6. P5.09-F1 preservation

R15 preserves the exact distinction established by P5.09-F1:

- a truthful derived read-only Product Contract operation may declare no direct canonical access;
- if direct canonical access is declared for a read operation, `Read` remains required and validated;
- canonical mutation still requires explicit `Write` plus the applicable Organizational Authority declaration;
- the integration adapter/scaffold refactor does not add an implicit canonical read, mutation path or authority grant.

Focused R15 regression coverage re-exercises the derived-read case and fails closed when a direct read declaration is changed to `Write`-only.

## 7. Security, authority and lifecycle review

The refactor does not change semantic ownership:

- Organization scope remains enforced by the existing Product Contract/composition/capability/workspace owners;
- Product Contract/capability admission still grants no Authorization, permission, Organizational Authority or approval;
- R14 current governed provider/version evidence is still required before dependency-backed capability reliance;
- workspace remains `NON_AUTHORITATIVE` presentation;
- CAP-004 reconstruction remains derived/read-oriented;
- Product Contract lifecycle and capability lifecycle remain separate;
- no operational-readiness or conformance claim is introduced by R15.

## 8. Public-boundary / ADR gate

R15 intentionally stays below the public/stable boundary threshold. The current Python modules, dataclasses, template text and compatibility accessors remain internal/provisional reference evidence.

No fixed REST/GraphQL/gRPC/wire/serialization protocol, package registry, generated-code contract, plugin loader, extension registry, IAM mechanism, separately deployable integration service or other ADR-triggering mechanism is selected.

Therefore the correct R15 decision is **no new ADR/RFC**. Re-open the gate at P5.11 or earlier only if a material mechanism boundary is actually crossed.

## 9. Executable evidence

R15 adds `reference/python/tests/test_r15_reuse_developer_experience_refactoring_review.py` covering:

1. shared adapter stored state contains only the two-consumer core;
2. workspace is an explicit optional binding over the same exact facade;
3. both consumers share the adapter module while only the product opts into workspace;
4. scaffolding teaches the demonstrated adapter seam;
5. the local harness preserves adapter/contract continuity without storing a separate facade owner;
6. P5.09-F1 remains fail-closed for direct canonical access;
7. the refactor stays internal/provisional and does not inflate a public boundary.

The accumulated P5.05/P5.06/P5.08/P5.09 suites remain part of the same full reference run. Hosted `Reference Python CI #251` passed the 682-test reference suite on the R15 code/refactoring head before canonical review/roadmap synchronization.

## 10. R15 conclusion

`PASS`.

R15 demonstrates that the correct next step after second-consumer reuse proof is **narrowing**, not generalized SDK construction:

- keep the exact shared capability-oriented integration core;
- make workspace consumer-specific and opt-in;
- align scaffold guidance with the actually reused seam;
- preserve P5.09-F1 and R14 fail-closed semantics;
- keep public/stable, lifecycle and ADR decisions deferred until evidence crosses their thresholds.

With this review recorded and the synchronized full-suite verification passing, the roadmap may advance to **P5.10 — Phase 5 conformance + architecture fitness matrix**.