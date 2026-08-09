# P6.03 Stage 1 — First real product/workflow platform integration

Status: `Stage 1 Complete / PASS`; `P6.03 overall In Progress`
Date: `2026-08-09`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Product repository: `arutyunoveth/ai-corporation`
Product PR: `#140`, merged
Product merge commit: `5d1c0e5f096188cc1028cc2bf79ace325d0a5167`
Platform branch/PR: `p6-03-stage1-first-real-integration` / `#77`
Product Contract: [`P6-02-FIRST-REAL-PRODUCT-CONTRACT.md`](../contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md), `Provisional 0.1.0`
Predecessor gate: [`R17-first-product-boundary-review.md`](R17-first-product-boundary-review.md), `PASS`

## 1. Decision

**PASS for P6.03 Stage 1 only.**

The first real product boundary is now exercised by the real `ai-corporation` product repository through the existing internal/provisional Arvectum OS integration-adapter seam using synthetic/anonymized/redacted evidence only.

This evidence is sufficient to move P6.03 to its next bounded adoption gate: **Stage 2 — one real 44-ФЗ case** under the same P6.02 Product Contract, subject to the constraints below.

This decision does **not**:

- complete P6.03 as a whole;
- authorize Stage 3 calibration cases;
- promote CAP-001 or CAP-004 beyond `Incubating / Provisional`;
- change Product Contract `0.1.0` or make it `Stable`;
- create a public/stable SDK, API, wire, package or service boundary;
- create production-readiness, SLA, support or commercial platform commitments;
- authorize EIS/ETP mutation, procurement submission, signature/EDS, supplier/client delivery, payment or another external organizational commitment.

## 2. Canonical basis checked

Stage 1 was implemented against the current canonical hierarchy:

1. Constitution `1.2.0`, `Ratified`, frozen;
2. RFC Index with RFC-0001 through RFC-0008 `1.0.0` `Accepted`;
3. RFC-0001 — platform/product boundary, governed organizational state, security/privacy/portability and no accidental authority;
4. RFC-0002 — Canonical Record authority modes and explicit external-authority contracts;
5. RFC-0003 — Organization sovereignty, deny-by-default access, purpose/rights/classification and separation of authentication, authorization and organizational authority;
6. RFC-0004 — explicit Product Contract, exact dependencies and prohibition of hidden product/platform coupling;
7. RFC-0005 — Governed Execution and explicit gates for consequential effects;
8. RFC-0006 — append-only provenance and truthful missing/redacted/deleted/unavailable reconstruction;
9. RFC-0008 — Document/Artifact exact identity/version/provenance/handling semantics;
10. current ADR index — no Accepted ADR is required for the bounded Stage 1 implementation;
11. current CAP-001/CAP-004 capability catalog/contracts — both remain `Incubating / Provisional 1.0.0`;
12. P6.01 evidence baseline, P6.02 Product Contract and R17 `PASS`.

No conflict with a higher-priority canonical source was identified.

## 3. Exact Stage 1 boundary

The executable proof preserves the P6.02 boundary:

- Product Identity: `product/arvectum-tender-operator@<organization>`;
- Product compatibility line: `restricted-paid-pilot/44fz-prebid-v1`;
- Product Contract subject: `product-contract-subject/p6-02-arvectum-tender-operator@<organization>`;
- Product Contract exact version: `product-contract-version/p6-02-arvectum-tender-operator-v0.1.0@<organization>`;
- CAP-001 — `Incubating`, Provisional provider contract `1.0.0`;
- CAP-004 — `Incubating`, Provisional provider contract `1.0.0`;
- CAP-002 and CAP-003 remain intentionally omitted;
- procurement-domain meaning, extraction/risk/RFQ/TKP/economics/recommendation semantics remain product-owned;
- source tender/partner/supplier document facts remain externally authoritative;
- external actions remain product/manual contour only.

The Stage 1 executable projection uses only the current integration-facing operations already supported by `IntegrationAdapters`:

- CAP-001 exact Document/Artifact resolve/reliance;
- CAP-004 read-oriented execution reconstruction.

Current Python operation/module names remain internal/provisional implementation evidence and are not a public compatibility commitment.

## 4. Platform gap discovered and bounded remediation

P6.03 exposed one real platform-reference gap: the current `CanonicalRecord` reference implementation recognized RFC-0002 authority-mode names but admitted only `Native` records. P6.02 correctly requires `External Reference` for the first tender-document sources.

Using `Native` merely to make the integration test green would have created false authority and a competing source of truth. Stage 1 therefore adds the minimum RFC-0002-aligned reference semantics:

- explicit immutable `ExternalAuthorityContract`;
- required authoritative system/object reference and authority scope;
- explicit retrieval/synchronization, freshness, source-version, conflict and failure semantics;
- explicit permitted transformations, retention/deletion and portability semantics;
- `External Reference` and `Governed Replica` fail closed without that contract;
- `Native` fails closed if an external-authority contract is attached;
- Canonical Record and external contract authority scopes must match.

This is a subordinate implementation of already Accepted RFC-0002 semantics. It does not choose an EIS client, synchronization service, persistence topology, credential model, durable transport or public serialization contract; no new RFC or ADR is required by this Stage 1 change.

## 5. Real product integration evidence

The product-owned integration is implemented in `arutyunoveth/ai-corporation`, not moved into shared platform domain code.

The bridge:

- imports only `arvectum_os_ref.integration_adapters` as its platform seam;
- invokes CAP-001 document reliance and CAP-004 reconstruction only;
- does not import platform private stores, capability internals, workspace internals, event-store internals or undocumented endpoints;
- does not catch and relabel platform fail-closed errors as governed success;
- contains no direct HTTP/network, browser automation, process execution or external-action dependency;
- keeps all procurement business semantics in the product repository.

The product CI job checks out an exact immutable Arvectum OS Stage 1 reference commit and executes the cross-repository proof with that exact provider evidence rather than relying on an ambient/latest platform checkout.

## 6. R17 Stage 1 evidence matrix

| R17/P6.03 requirement | Executable evidence | Result |
|---|---|---|
| exact Product Contract/version continuity | `test_exact_p6_02_identity_and_only_cap001_cap004_dependencies_are_preserved`; cross-repository product happy path | `PASS` |
| exact CAP-001/CAP-004 current provider support | explicit `GovernedDependencyVersionEvidence`; product CI pins exact platform commit | `PASS` |
| wrong-Organization denial | `test_wrong_organization_fails_closed` | `PASS` |
| purpose/right/classification denial | `test_purpose_right_and_classification_denials_fail_closed` | `PASS` |
| missing/stale/incompatible dependency evidence | `test_missing_incompatible_and_deprecated_provider_evidence_fail_closed`; current-evidence omission guard | `PASS` |
| external authority preserved | `test_external_reference_document_resolves_without_native_authority_substitution`; missing-contract negative path | `PASS` |
| truthful incomplete reconstruction | platform and product cross-repository REDACTED/incomplete tests | `PASS` |
| no private platform fallback/coupling | hidden coupling negative paths plus product AST import guard | `PASS` |
| no external mutation/organizational commitment | product structural guard and read-only executable projection | `PASS` |
| changed-scope + reference regression | hosted Arvectum OS Reference Python CI | `PASS` |

## 7. Hosted validation

### 7.1 Arvectum OS

Platform PR `#77` hosted `Reference Python CI #274` is green on the roadmap-synchronized Stage 1 branch head before this final evidence-only amendment.

Validated result:

- `713` tests run;
- `713` passed;
- all `9` new P6.03 Stage 1 platform tests passed;
- no existing reference fitness test remained failing.

An earlier run exposed two old M3 closure tests that expected wording superseded by current Phase 6 canonical terminology. All nine new P6.03 tests were already green in that run. The old assertions were updated to the current canonical wording without weakening their lifecycle/conformance guard, after which the full reference suite passed.

### 7.2 ai-corporation

Product PR `#140` CI run `#1922` completed with **all jobs green** before merge:

- dedicated `P6.03 Arvectum OS Stage 1` cross-repository job — `PASS` against pinned platform commit `18e747d3fa099c9aadb946d16055e0a926c723c1`;
- security — `PASS`;
- migrations — `PASS`;
- R8 PostgreSQL integration/acceptance — `PASS`;
- R8 tenant acceptance — `PASS`;
- Redis integration — `PASS`;
- quality `make check` — `PASS`;
- quality full `make test` — `PASS`.

PR `#140` was then squash-merged to product `main` as commit `5d1c0e5f096188cc1028cc2bf79ace325d0a5167`.

## 8. Cross-review findings

### Architecture

`PASS` for Stage 1. Existing `IntegrationAdapters` is sufficient for the read-oriented proof and remains internal/provisional. No technology or compatibility choice crossed the RFC/ADR threshold. The external-authority repair implements RFC-0002 rather than changing it.

### Product/platform boundary

`PASS`. Procurement semantics remain in `ai-corporation`; the platform sees only domain-neutral Product Contract, exact Document/Artifact reliance and reconstruction evidence. CAP-002/CAP-003 were not added speculatively.

### Security and sovereignty

`PASS` within Stage 1 scope. Organization, current Actor/access, purpose, right and classification checks fail closed. Redacted/incomplete reconstruction does not disclose its hidden source pin. No cross-Organization or ambient access path was added.

### Authority integrity

`PASS`. External tender-document authority remains `External Reference`; `Native` substitution is explicitly prohibited by the new reference guard. Product-derived procurement conclusions remain non-platform authority.

### Engineering

`PASS` for the bounded proof. The product uses one integration-facing platform import and exact provider evidence. Hosted regression evidence exists on both repositories. No production dependency, package-distribution promise or service topology is introduced.

## 9. Stage 2 gate and unresolved implementation boundary

One limitation is intentionally not disguised as completion: P6.02's broader CAP-001 semantic envelope also permits governed registration/admission of an exact external Document/Artifact reference where the selected real case needs it. The current `IntegrationAdapters` capability seam used by Stage 1 is read-oriented and does not expose a corresponding canonical admission/mutation operation.

Stage 1 therefore **does not fabricate** such an operation, bypass the seam, mutate canonical state directly or weaken the contract to fit the implementation.

Before or during Stage 2, if the selected real case requires platform-side admission rather than relying on an already admitted exact reference, the implementation must map that need through the existing RFC-0005 Governed Execution/gate semantics or introduce the minimum subordinate implementation change. Any new consequential mutation must retain explicit authorization, organizational authority/data-governance requirements as applicable, exact Product Contract/version attribution and Event/provenance evidence. If that mapping materially selects a new durable/public/cross-cutting boundary, the applicable ADR/RFC gate must be reopened first.

## 10. Stage 2 authorization scope

Stage 1 PASS authorizes only the next P6.02/R17 adoption step:

- exactly **one real 44-ФЗ pre-bid case**;
- exact Product Contract `0.1.0` unless a material boundary change requires a new immutable version first;
- CAP-001/CAP-004 only unless real evidence requires a contract change;
- one explicit Organization scope and attributable Actor context;
- external tender/partner/supplier sources remain externally authoritative;
- platform-backed acts remain reconstructable from exact evidence;
- external actions and organizational commitments remain manual/product-owned;
- any fail-closed integration failure returns explicitly to the product-local/manual contour and must not be represented as Arvectum OS governed success.

Stage 3 remains gated until the real Stage 2 case is completed and reviewed for boundary drift, security/authority behavior and useful product/platform evidence.

## 11. Lifecycle and commercial integrity

After Stage 1:

- CAP-001: `Incubating / Provisional`;
- CAP-004: `Incubating / Provisional`;
- CAP-002/CAP-003: unchanged and not part of this Product Contract;
- P6.02 Product Contract: `Provisional 0.1.0`;
- P6.03: `In Progress`, Stage 1 `PASS`, Stage 2 next;
- no Platform Capability is promoted to `Active`;
- no product/platform conformance claim is broadened;
- no production support/SLA/public compatibility claim is created.

The correct next action is P6.03 Stage 2, not P6.04.
