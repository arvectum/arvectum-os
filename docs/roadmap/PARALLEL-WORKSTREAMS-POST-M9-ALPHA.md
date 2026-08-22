# Arvectum OS — Parallel Workstreams after M9-alpha

Status: `Active planning / bounded parallel execution`
Version: `1.0.0`
Created: `2026-08-22`
Owner: `ООО «Арвектум»`
Task classification: `governance` with `platform`, `product_contract`, and `product_specific`
Parent roadmap: [`ROADMAP.md`](ROADMAP.md)
Current critical-path action: `P9.11 — Real daily-use dogfooding + friction/backlog closure`

## 1. Purpose

M9-alpha is achieved and P9.11 now depends materially on real owner use rather than continuous implementation throughput. This creates legitimate parallel engineering capacity.

This document defines bounded parallel lanes that may progress while P9.11 owner dogfooding is underway, without pretending that all lanes are one serial milestone sequence.

Parallel work MUST NOT:

- weaken or bypass P9.11/R32/P9.12 closure criteria;
- change the current critical path to M9 without a roadmap update;
- infer Stable Product Contracts, Active Platform Capabilities, public/stable APIs, external/customer Production, SLA/support, or broader conformance;
- move product business semantics into Arvectum OS merely because an integration is technically shared;
- create competing sources of truth for 1С, CRM, СЭД/ECM, government systems, or other externally authoritative systems;
- treat Authentication, Authorization, Organizational Authority, Data Governance, and legal/contractual rights as interchangeable.

## 2. Lane A — Productive Workspace / real dogfooding

Status: `ACTIVE / critical path`.

Canonical sequence:

`P9.11 → R32 → P9.12 → M9`.

Current work:

- owner uses the Productive Workspace for real daily sessions;
- friction/bugs/incomplete journeys are captured through the P9.11 Observation/backlog mechanism;
- material blockers are repaired without weakening security, authority, provenance, Product Contract, or product/platform boundaries;
- recurring friction is dispositioned before R32.

This lane owns the M9 closure clock.

## 3. Lane B — Russian-market integration portfolio and connector architecture

Status: `ACTIVE DESIGN / evidence collection`; non-blocking for P9.11.

Goal:

> Design the governed integration layer needed for common Russian enterprise systems while preserving external authority, product ownership, replay safety, credentials isolation, and explicit contracts.

### INT-B1 — Integration portfolio baseline

Inventory concrete target classes and likely early systems:

1. **1С** — accounting/ERP/HR/industry configurations; authority normally remains external unless an explicitly governed replica is justified.
2. **Битрикс24** — CRM/tasks/communications; distinguish CRM authority from collaboration/event projections.
3. **amoCRM** — CRM/sales pipeline; product/customer-specific pipeline semantics remain external/product-owned.
4. **СЭД / ECM / ASUD** — Directum RX, Docsvision, ТЕЗИС and other concrete systems only when a real deployment exists; document authority/signature/retention semantics must be preserved.
5. **ЭДО / electronic signature contours** — e.g. Диадок / СБИС / 1С-ЭДО only when a concrete organizational outcome and rights are selected.
6. **Government/regulated systems** — ЕИС and later other concrete systems only through bounded authority/rights scopes.

Exit: ranked candidate register with real business outcome, authority owner, data/effect boundary, credentials model, reversibility, and Product Contract/platform-need disposition.

### INT-B2 — Domain-neutral connector boundary pattern

Design only the minimum reusable platform envelope evidenced by M8:

- connector identity/version;
- external system identity and authority mode;
- explicit read/write/effect operations;
- exact Product Contract/integration-contract dependencies;
- credential references without secrets in canonical state;
- source occurrence vs canonical Event admission;
- idempotency/duplicate/retry/replay/uncertainty/reconciliation;
- provenance and exact source/version evidence;
- Organization/Actor/Authorization/Data Governance context;
- rate/availability/failure metadata as non-authoritative telemetry unless explicitly governed;
- disable/revoke/upgrade/rollback/termination.

Do not select a universal transport, broker, plugin protocol, stable manifest, or public API unless real reuse crosses the ADR/stability threshold.

### INT-B3 — 1С first-candidate design

Prepare the first bounded 1С integration candidate, without assuming a specific configuration is universal.

Required design questions:

- concrete configuration/version and organizational outcome;
- what remains authoritative in 1С;
- read-only vs consequential write operations;
- supported integration mechanisms actually available for that configuration (HTTP/OData/web services/file exchange/other concrete mechanism);
- identity mapping and service credentials;
- transaction/effect confirmation and uncertain-outcome semantics;
- reconciliation and historical replay behavior;
- data minimization/retention/export/deletion;
- Product Contract boundary and exact platform responsibilities.

Implementation is not admitted until a concrete 1С target and owner-approved bounded outcome exist.

### INT-B4 — CRM integration designs

Treat Битрикс24 and amoCRM as separate product/system integrations, not one generic CRM schema.

Shared questions:

- externally authoritative entities and identifiers;
- webhook/polling occurrence semantics;
- duplicate/out-of-order events;
- human/robot/service identity and permissions;
- write-side effects and unknown outcomes;
- product-local pipeline/business rules;
- governed projections needed by Workspace/My Work/Activity.

Promotion of any shared CRM abstraction requires evidence from at least two materially similar real integrations and a separate admission decision.

### INT-B5 — СЭД/ECM integration design

Start from a real system/deployment rather than a universal СЭД abstraction.

Required boundaries:

- document/card/workflow authority;
- document versions and attachments;
- electronic signatures and signature verification evidence;
- registration numbers and legal/organizational authority;
- retention/archive/deletion rules;
- inbound/outbound document effects;
- reconciliation when external document state changes;
- artifact/document provenance mapping under RFC-0008.

### INT-B6 — Integration security/reliability review

Before the first material real connector implementation, review:

- secret storage/rotation/revocation;
- least privilege;
- Organization isolation;
- transport authenticity/integrity;
- external source authority;
- replay/duplicate/idempotency/uncertainty;
- logging/minimization;
- operational disable/rollback;
- Product Contract and ADR/stable-boundary triggers.

Exit: concrete first connector is ready for a separately admitted implementation action.

## 4. Lane C — Product-to-Workspace operational composition

Status: `AVAILABLE / bounded`.

Purpose: make existing products increasingly useful through the Productive Workspace while product business logic remains product-owned.

Available work:

- Tender Operator product projection improvements driven by real P9.11 friction;
- Discount Parser operational/status/attention projections;
- Creative Test Agent product surface beyond the already proven bounded P9.07 composition;
- Proxy Launcher only through an explicit Product Contract if/when it relies on governed Arvectum OS capabilities/state;
- human-readable product health, recent outcomes, attention items and governed entry points.

This lane may proceed only when work is either:

1. a product-local reversible improvement; or
2. covered by an existing Product Contract; or
3. preceded by a new/updated Product Contract before new governed platform reliance.

## 5. Lane D — Reliability, developer experience and technical debt

Status: `CONTINUOUS / non-feature`.

Available work that does not need to wait for P9.11:

- CI speed/stability and deterministic build hygiene;
- dependency/license/security updates with regression proof;
- removal of bounded proof harnesses only when no canonical evidence/recovery path depends on them;
- internal observability and operator diagnostics;
- backup/restore/update portability regressions;
- documentation drift guards;
- test fixture quality and source/provenance truthfulness;
- performance profiling where real Productive Workspace use provides evidence.

No speculative refactor should replace a proven bounded mechanism merely to make the architecture look cleaner.

## 6. Lane E — Future external/customer readiness discovery

Status: `DISCOVERY ONLY`.

M8 explicitly did not prove realistic two-Organization isolation or customer Production. Discovery may proceed in parallel for:

- concrete second-Organization candidate;
- deployment/hosting models;
- customer-controlled identity/authority/data governance;
- support/update/backup responsibility split;
- Russian regulatory/commercial constraints;
- registry/certification/signing requirements where relevant.

No customer Production, multi-tenant, SLA/support, or general-availability implementation is admitted by this lane.

## 7. Parallelism and merge rule

Parallel branches are encouraged when they modify independent surfaces.

Before merge, each branch must rebase/reconcile against current `main` and recheck:

- Constitution and Accepted RFC/ADR;
- Product Contract boundaries;
- current roadmap action and related lane status;
- current tests/quality gates;
- conflicts with P9.11 dogfooding observations or active fixes.

A branch that changes shared Workspace/BFF/session/security semantics or a common connector contract is not independent merely because it has a different Git branch name; such work must undergo the applicable cross-review/gate before merge.

## 8. Current concurrency map

```text
                         ┌─ Lane A: P9.11 real UI dogfooding ──→ R32 ─→ P9.12/M9
                         │
M9-alpha / current main ─┼─ Lane B: integration portfolio + connector design
                         │          ├─ 1С
                         │          ├─ Битрикс24
                         │          ├─ amoCRM
                         │          └─ СЭД/ECM/ЭДО
                         │
                         ├─ Lane C: product ↔ Workspace composition
                         │
                         ├─ Lane D: reliability / DX / technical debt
                         │
                         └─ Lane E: future external/customer readiness discovery
```

Only Lane A is currently on the critical path to M9. Lanes B–E may advance in parallel within their declared boundaries.

## 9. Immediate actions

- **Lane A:** continue real P9.11 owner sessions and friction capture.
- **Lane B:** start `INT-B1 — Integration portfolio baseline`; then `INT-B2` and concrete `INT-B3` 1С design may proceed while UI testing continues.
- **Lane C:** take only real dogfooding-driven product composition improvements or explicitly contracted product work.
- **Lane D:** continue evidence-backed quality/reliability work.
- **Lane E:** discovery only until a concrete external/customer outcome is selected and governed.
