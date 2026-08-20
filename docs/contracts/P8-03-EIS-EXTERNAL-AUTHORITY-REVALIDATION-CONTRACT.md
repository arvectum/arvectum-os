# P8.03 — EIS External-Authority Revalidation Integration Contract

Status: `Provisional`
Version: `0.1.0`
Created: `2026-08-20`
Owner: `ООО «Арвектум»`
Task classification: `product_contract` with `platform`, `product_specific` and `governance`
Phase: `Phase 8 — Active`
Roadmap work item: `P8.03 — External Product Contract / integration-contract boundary + stable-surface disposition`
Product: Tender Operator
Related Product Contract: [`P6.02 — First Real Product Contract`](P6-02-FIRST-REAL-PRODUCT-CONTRACT.md) — `Provisional 0.1.0`
Predecessors: [`P8.01`](../reviews/P8-01-eis-revalidation-target-evidence-baseline.md); [`P8.02`](../reviews/P8-02-identity-trust-rights-data-governance-boundary.md)
Architecture authority: RFC-0004 `1.0.0` — `Accepted`
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Purpose and status

This contract defines the smallest explicit boundary for the Phase 8 EIS authoritative-source revalidation selected by P8.00.

It supplements, but does not supersede or widen generally, the existing P6.02 Tender Operator Product Contract.

This contract is `Provisional 0.1.0` and bounded to one owner-operated validation case. It is not:

- a Stable Product Contract;
- a public API/SDK/wire/package contract;
- a generic EIS/government connector contract;
- a Platform Capability lifecycle transition;
- customer/external Production approval;
- a support/SLA/compatibility promise;
- a cross-Organization grant;
- authorization for EIS/ETP mutation, submission or digital signature;
- a redistribution-rights determination.

## 2. Contract identity and scope

Contract subject: `integration-contract/p8-03-eis-authority-revalidation@<organization>`.

Contract version: `integration-contract-version/p8-03-eis-authority-revalidation-v0.1.0@<organization>`.

`<organization>` MUST resolve to `ООО «Арвектум»` in the local governed runtime; no ambient/default Organization is permitted.

Exact validation target:

- external system: ЕИС / `zakupki.gov.ru`;
- notice: `0344100006426000005`;
- historical comparison baseline: P6.05-L7 attempt #2, manifest SHA-256 `74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121`;
- intended live result: a fresh exact external observation and deterministic comparison yielding `NO_CHANGE`, `CHANGE_DETECTED`, or an explicit non-success state.

Any material widening requires a new immutable contract version or another governed contract as appropriate.

## 3. Responsibility boundary

### Tender Operator owns

- EIS discovery/retrieval implementation;
- SOAP method/endpoint details;
- token/credential integration;
- truststore hookup within approved security controls;
- archive download and safe extraction implementation;
- procurement-specific exact-document expectations;
- source-specific parsing/normalization;
- product-local diagnostics, retry controls and cache behavior;
- procurement workflow/UX/business meaning.

### Arvectum OS owns

- explicit Organization/Actor/contract attribution for governed reliance;
- external authority-mode/source attribution;
- immutable governed reference to the historical P6 observation;
- explicit new observation/freshness reference used by the Phase 8 execution;
- exact materially relied-upon version/integrity references where admitted;
- required Execution Context/Event/provenance evidence;
- explicit incomplete/stale/ambiguous evidence state;
- read-only reconstruction showing which observation/version was relied upon;
- preservation of historical evidence without mutation when the external source changes.

The platform must not import procurement semantics merely to satisfy this contract.

## 4. Platform dependencies

The bounded contract relies on existing Incubating/Provisional platform semantics only.

| Dependency | Lifecycle | Contract reliance | Required use |
|---|---|---|---|
| Kernel / Canonical Record / Execution Context / Event semantics | Accepted RFC architecture | internal/provisional implementation | Organization-scoped governed execution, immutable history, external authority and provenance |
| `CAP-001 — Document & Artifact Governance` | `Incubating / Provisional` | `Provisional` | exact external Document/Artifact reference/version/integrity and provenance where material to comparison/reliance |
| `CAP-004 — Audit / Reconstruction Support` | `Incubating / Provisional` | `Provisional` | reconstruct historical P6 and fresh P8 observation/reliance evidence without external-effect replay |

CAP-002 and CAP-003 are not required by this contract.

No dependency spelling, Python import, internal route, local file layout or persistence representation becomes a stable/public contract through this declaration.

## 5. Permitted operations

### 5.1 Product-local read-only external retrieval

One P8.04 validation attempt may invoke the existing product-owned EIS retrieval path for the exact selected notice.

Side-effect class: external `ReadOnly` retrieval.

Required preconditions:

- explicit Organization;
- attributable Actor/service;
- exact contract version;
- read-only target notice scope;
- required authentication/trust context;
- Data Governance purpose permitted;
- no unresolved rights widening;
- platform evidence path available.

### 5.2 Local deterministic comparison

The product may compare the fresh exact snapshot against the immutable P6 baseline.

Permitted material classifications:

- `UNCHANGED`;
- `ADDED`;
- `REMOVED`;
- `CHANGED`.

Overall result:

- `NO_CHANGE`;
- `CHANGE_DETECTED`;
- `FAIL_CLOSED`;
- `INCOMPLETE`;
- `UNCERTAIN_RECONCILIATION_REQUIRED` where applicable.

Comparison logic remains product-owned unless later evidence proves a genuinely domain-neutral reusable responsibility.

### 5.3 Platform governed evidence

The platform may create/advance the bounded Execution Context and admit the minimum required Canonical Records/Events/references needed for exact attribution and reconstruction.

Any canonical mutation must follow Governed Execution and applicable Authorization, Organizational Authority, Data Governance and approval gates.

### 5.4 Reconstruction

Reconstruction is read-only and must not automatically call EIS, rerun retrieval, replay an external action or mutate historical evidence.

## 6. Prohibited operations

This contract explicitly denies:

- EIS/ETP mutation;
- application/bid submission;
- digital signature/EDS;
- supplier/customer messaging;
- unrelated broad crawling;
- public redistribution of EIS source documents;
- second-Organization/cross-Organization use;
- customer-facing Production;
- stable/public EIS integration exposure;
- generic connector/plugin promotion;
- automatic retry that widens operation scope;
- secret persistence in canonical history;
- weakening TLS verification;
- fallback from failed current retrieval to old P6 state while labelling it fresh.

## 7. External authority, version and freshness semantics

EIS remains authoritative for the external procurement registry/document source scope.

Arvectum OS records what was observed and relied upon; it does not become factual authority for the external content.

The P6 observation and P8 fresh observation are distinct historical observations.

A later observation MUST NOT mutate or replace the prior observation record.

For consequential reliance:

- the effective fresh observation/reference must be explicit;
- observation time/freshness must be attributable;
- exact material document version/integrity evidence must be pinned where needed;
- ambiguous or unavailable current state must be exposed rather than silently resolved to cached state.

No `Governed Replica` synchronization contract is created by `0.1.0`.

## 8. Identity / authorization / authority / data governance

The exact P8.02 boundary is incorporated by reference.

In particular:

- identity resolution is not permission;
- EIS token possession is not authorization or Organizational Authority;
- Authorization is deny-by-default and restricted to the read-only selected notice scope;
- owner authority governs material widening;
- no AI component receives independent authority;
- data purpose is limited to external-authority freshness/version-drift validation;
- raw source data remains owner-local/minimized;
- unresolved redistribution/cross-Organization/customer rights remain denied.

## 9. Secrets and logging

Reusable credentials, private keys, raw auth headers and equivalent secrets MUST NOT appear in:

- Canonical Record payloads;
- canonical Events merely for authentication proof;
- Git commits;
- committed evidence bundles;
- normal logs/traces;
- model prompts.

Logs/telemetry remain non-canonical by default and must not substitute for required governed evidence.

## 10. Failure / retry / uncertainty

- Read-only retrieval failure may be retried only within bounded product-owned policy that does not weaken security, broaden scope or misrepresent the observation time.
- A failed current retrieval must not be reported as `NO_CHANGE`.
- If the external response outcome or completeness is uncertain, the execution must remain explicit `INCOMPLETE` or `UNCERTAIN_RECONCILIATION_REQUIRED` rather than optimistic success.
- Required platform evidence-path failure prevents full PASS.
- Correction/invalidation of admitted evidence creates additional governed history; it does not mutate prior admitted Events/records.

## 11. Provenance and reconstruction obligations

A completed run must make it possible to resolve, directly or by immutable governed reference:

- Organization;
- Actor/service;
- this exact contract version;
- exact workflow/runner/config version materially used;
- EIS source and notice identity;
- authority mode/source;
- fresh observation time;
- P6 baseline reference/hash;
- fresh snapshot identity/integrity evidence;
- deterministic comparison result;
- exact materially relied-upon Document/Artifact references where applicable;
- required Events/Execution Context transitions;
- terminal result and evidence-completeness state.

## 12. Portability / termination

- Contract semantics must remain understandable without the current Python/SOAP/file-layout implementation.
- Reusable EIS credentials are not portable canonical data and must be reprovisioned.
- On termination, product-owned connector use may be removed without erasing historical governed evidence.
- No customer handover/export format is promised by this contract.

## 13. Stable-surface disposition

**Disposition: `PROVISIONAL_INTERNAL_ONLY / NO_STABLE_SURFACE`.**

No stable/public interface is required for the selected validation.

Stop for a separate governance/ADR/stable-boundary decision before an external party materially relies on:

- public/stable API/wire/package syntax;
- connector discovery/packaging protocol;
- platform EIS authentication/trust protocol;
- customer deployment/compatibility surface;
- externally promised export format.

## 14. Lifecycle / conformance non-effects

This contract does not change:

- P6.02 lifecycle (`Provisional 0.1.0`);
- CAP-001 through CAP-004 lifecycle (`Incubating / Provisional`);
- external/customer Production status (none);
- conformance beyond the declared bounded Phase 8 scope;
- support/SLA commitments (none).

## 15. Cross-review

### Iteration 1 — product/platform leakage

Kept EIS/SOAP/archive/procurement semantics product-owned; platform surface is limited to governed reliance semantics.

### Iteration 2 — authority/security

Denied mutation, cross-Organization use and secret persistence; contract possession grants no permission/authority.

### Iteration 3 — stable surface

Explicitly classified the boundary as `PROVISIONAL_INTERNAL_ONLY / NO_STABLE_SURFACE` and added stop triggers.

### Iteration 4 — reconstruction

Made fresh observation and historical baseline independently attributable and prohibited reconstruction from replaying external retrieval automatically.

**Result:** `PASS`; no material objection remains.

## 16. Handoff

P8.03 exit criteria are satisfied.

Next canonical action:

> **R25 — External Boundary Review.**
