# P7.01 — Persistent Internal Operating Boundary and Operational Requirements Baseline

Status: `Complete / Baseline`
Version: `1.0.0`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract`
Operating classification: `Persistent Internal / owner-operated`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Review gate: [`R21 — Operational Boundary Review`](../reviews/R21-operational-boundary-review.md)
Architecture baseline: Constitution `1.2.0`; RFC-0001 through RFC-0008 `1.0.0` (`Accepted`)

## 1. Purpose

This document defines the operating boundary and minimum operational requirements that must be preserved while Arvectum OS moves from bounded owner-operated validation into a persistent internal runtime.

It is intentionally a requirements baseline rather than a deployment architecture. It does not select a database, IAM provider, service manager, public API, message broker, storage engine, backup product or permanent deployment topology.

The baseline exists so that `P7.02` and later Phase 7 work can make reversible environment-specific implementation choices without silently creating stronger lifecycle, conformance, customer, support or compatibility commitments.

## 2. Authority and interpretation

This baseline is subordinate to, and must be interpreted consistently with:

1. Constitution `1.2.0` (`Ratified`, frozen);
2. RFC-0001 through RFC-0008 `1.0.0` (`Accepted`);
3. any future Accepted ADR applicable to this operating contour;
4. approved governance decisions and engineering gates;
5. applicable Product Contracts;
6. implementation and test evidence.

No statement in this document amends an Accepted RFC or creates an architectural exception.

The Decision Authority Policy remains `Proposed 0.2.1`. Until an approved delegation replaces the current rule, residual decision authority remains with the owner under Accepted governance.

## 3. Operating classification and scope

### 3.1 Classification

The selected Mac mini operating contour is classified as:

> **Persistent Internal / owner-operated**

This means Arvectum OS may run regularly and persistently for internal ООО «Арвектум» governed work after the `P7.02` runtime gate passes.

The Mac mini is an operating environment, not an architectural platform commitment.

### 3.2 Organization scope

The initial sovereignty and operating scope is exactly:

- Organization: `ООО «Арвектум»`;
- tenant/organization boundary: one owner-operated internal Organization context;
- cross-Organization access: prohibited unless separately governed under Accepted RFC-0003 and an applicable contract/decision;
- external customer tenant operation: outside P7.01 scope.

No shared undifferentiated multi-Organization authority context is permitted.

### 3.3 Accountable owner and operator

Operational owner:

- `ООО «Арвектум»`.

Named operating role:

- `Arvectum OS Owner-Operator`.

The operating role MUST resolve at runtime to an attributable human RFC-0003 Principal/Actor identity in the applicable Organization context. Exact raw personal identity values, reusable credentials and authentication material are owner-local operational data and MUST NOT be published in this public canonical repository merely to name the role.

Machine/service execution that becomes operationally significant MUST use an attributable workload/service identity rather than an anonymous shared account.

The operating role does not receive Organizational Authority merely from technical access. Consequential approvals continue to require the applicable owner/delegated authority under Accepted governance.

## 4. Initial workloads allowed to rely on the persistent runtime

After `P7.02 PASS`, the following bounded workloads MAY rely on the persistent internal runtime, subject to their existing contracts and later Phase 7 hardening requirements.

### 4.1 Tender Operator

Allowed reliance:

- the existing real Tender Operator platform interaction defined by the applicable P6.02 Provisional Product Contract;
- governed exact-document/evidence admission and reconstruction through the already validated platform boundary;
- persistent internal execution only within declared Product Contract operations and Organization scope.

Constraints:

- procurement/domain semantics remain product-owned;
- external EIS authority remains external where already declared;
- no new platform capability dependency may be inferred from persistence alone;
- no product-specific approval rule moves into the platform through this baseline.

### 4.2 Arvectum Discount Parser

Allowed reliance:

- the existing P6.06 Provisional Product Contract `0.1.0` boundary;
- CAP-004-only minimized evidence/reconstruction reliance already validated in Phase 6;
- repeatable Windows/product-host to persistent Mac mini evidence/reconstruction work once P7.08 establishes the operational contour.

Constraints:

- Offer/source/normalization/deduplication/classification/scheduler/rules/templates/Telegram/publication-ledger semantics remain product-owned;
- external Telegram mutation remains product-owned and separately authorized where consequential;
- persistent platform reliance MUST NOT replay a historical external effect;
- no hidden shared database, private stream or implicit cross-host state dependency is permitted.

### 4.3 Platform-owned operational work

The persistent runtime MAY perform internal platform health, diagnostics, reconstruction, validation and administration needed to operate the declared contour.

Such work does not create new customer-facing product behavior or lifecycle promotion.

### 4.4 Workloads not admitted by P7.01

P7.01 does not admit:

- customer production workloads;
- public multi-tenant workloads;
- third-party Organization data without a separately governed boundary;
- product workloads lacking a Product Contract where RFC-0004 requires one;
- consequential external mutation merely because the persistent runtime is technically capable of it;
- new product-specific domain semantics inside shared platform behavior.

## 5. Explicit non-goals and prohibited claims

This baseline MUST NOT be represented as evidence of any of the following:

- external/customer `Production` readiness;
- an SLA, SLO, support or availability commitment to a customer;
- a supported macOS platform promise;
- a stable deployment topology;
- a public API/SDK or compatibility commitment;
- `Active` status for CAP-001 through CAP-004;
- `Stable` status for any Product Contract;
- full-platform conformance;
- a public multi-tenant service;
- a permanent choice of persistence, IAM, service supervision, storage, observability or networking technology.

Internal measurements may be introduced to operate and improve the environment, but they remain internal operating objectives unless separately approved as external commitments.

## 6. Data, classification and minimization boundary

### 6.1 Data classes in the persistent contour

Persistent operation MUST keep at least the following semantic classes distinguishable:

1. **canonical governed state and canonical Events/evidence** required by Accepted RFC semantics;
2. **governance-significant execution/checkpoint state** required to reconstruct or safely continue governed work;
3. **non-canonical telemetry** such as process logs, metrics, traces and health projections;
4. **cache/derived projections/transient outputs** that are not authority;
5. **owner-local configuration and secrets**;
6. **product-owned data** accessed only through declared Product Contract boundaries;
7. **external-authority references/replicas** whose authority remains outside Arvectum OS where declared.

The implementation MUST NOT collapse these classes into one undifferentiated persistence or retention rule merely for convenience.

### 6.2 Classification and purpose

Governed or sensitive data MUST have a classification or resolvable handling rule proportionate to risk where classification affects access, logging, retention, export or external processing.

Collection and retention MUST be purpose-limited and minimized. Persistent operation is not permission to retain every prompt, payload, intermediate file, log line or external response indefinitely.

### 6.3 Telemetry is not authority

Logs, metrics, traces, dashboards and health projections are non-canonical by default.

They MUST NOT silently become a competing source of organizational truth, approval state, authorization, Knowledge or product state.

Where consequential reconstruction requires canonical evidence, loss of ordinary telemetry MUST NOT be treated as equivalent to loss or mutation of canonical history.

### 6.4 Transient outputs

Generated files, temporary reports, caches, indexes, summaries and other intermediate artifacts remain Transient Outputs unless explicitly promoted through the applicable governed process.

Persistence duration alone does not convert an Observation or transient output into validated Knowledge or a Governed Organizational Asset.

## 7. Secret and credential boundary

Reusable secrets, passwords, private keys, API tokens, recovery material and equivalent credentials:

- MUST remain outside Git;
- MUST NOT be written into ordinary canonical record payloads merely for convenience;
- MUST NOT be written into ordinary logs, telemetry or model prompts;
- MUST be scoped and protected proportionately to privilege and threat;
- MUST have a replacement/rotation path;
- MUST have a revocation/disablement path;
- MUST be re-provisionable independently of ordinary portable governed-state restore when export is prohibited or unsafe.

A backup or portability proof MUST NOT copy non-exportable or unnecessary reusable secrets merely to claim completeness.

## 8. Authority, approvals and execution boundary

Persistent operation does not change Accepted authority semantics.

The runtime MUST preserve the separation of:

- Identity;
- Authentication;
- Authorization;
- Organizational Authority;
- Data Governance;
- validation;
- consequential approval;
- technical execution.

Consequential canonical mutation MUST occur through Governed Execution with the exact effective workflow, material inputs and Product Contract version references where applicable.

Technical administrator access MUST NOT be interpreted as Organizational Authority to approve consequential business or governance decisions.

AI MAY analyze, propose, generate and perform bounded execution allowed by the governing workflow. AI MUST NOT independently grant authorization, create Organizational Authority, act as final consequential approver or silently broaden Organization scope, retention or sharing.

## 9. Runtime health and supervision requirements

`P7.02` MUST implement a supervised runtime that satisfies the following requirements without turning the supervision mechanism itself into a platform contract:

- predictable start, stop and restart;
- boot/login lifecycle appropriate to the owner-operated Mac mini contour;
- process supervision rather than reliance on an interactive terminal remaining open;
- clear liveness/health indication;
- observable crash/restart behavior;
- bounded retry behavior that does not duplicate consequential effects;
- failure state visible to the owner-operator rather than silently disappearing;
- clean disablement/removal path;
- runtime files separated from the mutable repository checkout;
- runtime configuration and reusable secrets separated from source;
- immutable/reconstructable source or release pin for the running version.

A runtime that is merely long-lived but unsupervised does not satisfy P7.02.

## 10. Failure, degraded mode and uncertain outcome requirements

Failure MUST NOT silently broaden permissions, Organization scope or authority.

If required governed state/evidence is unavailable, inconsistent or cannot be verified, consequential processing MUST fail, pause, enter an explicitly governed degraded mode, or expose an incomplete/uncertain/reconciliation-required state as applicable.

Automatic restart or retry MUST NOT replay a historical consequential external effect merely because the process restarted.

Where an external effect may have occurred but confirmation is uncertain, the runtime MUST preserve uncertainty and require reconciliation/new authorization as required by the effective workflow rather than assuming success or blindly retrying.

## 11. Backup and restore baseline

`P7.03` MUST establish durable backup/restore for the state required to preserve organizational continuity within the declared contour.

The backup scope MUST identify separately:

- canonical governed state required for continuing/reconstructing the declared operation;
- governance-significant execution/checkpoint state where required;
- exact versions, identities, authority/provenance references and schema information required for interpretation;
- owner-local configuration metadata required to reconstruct the runtime without embedding reusable secrets;
- explicit exclusions such as replaceable caches, ordinary telemetry and non-exportable secrets.

A valid backup path MUST include integrity verification and a tested restore into an isolated location/environment.

The baseline does not establish one retention period, RPO, RTO, backup product or storage medium. Those details must be based on Phase 7 operational evidence and subordinate operational decisions.

If persistence is unavailable or integrity validation fails, the runtime MUST fail closed for operations whose correctness depends on that state.

## 12. Retention and deletion baseline

No fixed universal retention period is selected by P7.01.

Later Phase 7 implementation MUST define retention/deletion handling proportionate to data class, operational purpose, rights and reconstruction needs.

At minimum:

- ordinary telemetry MUST be bounded and rotatable;
- sensitive operational data MUST be minimized;
- canonical history MUST NOT be silently rewritten by log rotation or cache cleanup;
- deletion/minimization MAY legitimately reduce future reconstructability and that limitation MUST be represented truthfully;
- derived artifacts inherit applicable classification, purpose, rights and retention constraints unless a governed transformation establishes another permitted rule.

## 13. Upgrade, rollback and migration requirements

`P7.06` MUST provide a repeatable governed upgrade path with:

- immutable deployment/release/source pin;
- controlled stop/update/start sequence;
- pre-update backup/checkpoint where governed state is at risk;
- compatibility/migration checks when persisted governed state changes;
- health verification after update;
- last-known-good rollback path where semantically safe;
- explicit refusal or forward-recovery procedure where rollback is unsafe after an irreversible state migration;
- preservation of exact historical version references needed to reconstruct prior governed executions.

An update MUST NOT silently reinterpret historical canonical state under a new incompatible schema/version.

## 14. Network, proxy and trust boundary

The initial runtime is private/internal and MUST NOT create accidental public ingress.

Requirements:

- listeners MUST be bound only to the minimum interface/address scope required by the declared internal contour;
- public internet exposure requires a separate reviewed boundary before reliance;
- remote administration, if used, MUST remain owner-controlled, attributable and least-privilege;
- outbound network dependencies MUST be explicit where they are necessary for operation or external-authority retrieval;
- host/system proxy behavior MAY be used as an environment-specific dependency but MUST be documented where it affects operation;
- proxy bypasses, TLS trust roots, certificates and external service trust dependencies MUST NOT be implicit when they materially affect execution;
- failure of proxy/DNS/TLS/external connectivity MUST fail safely and remain distinguishable from successful governed execution;
- local/private network reachability MUST NOT itself create authorization or Organizational Authority.

P7.01 does not establish a public hostname, reverse proxy, VPN product, TLS termination topology or network-service contract.

## 15. Operator access assumptions

The initial contour assumes a small owner-operated environment rather than enterprise workforce IAM.

The implementation MUST nevertheless preserve:

- attributable human operation;
- deny-by-default access;
- least privilege;
- explicit Organization scope;
- no anonymous shared administrative account for consequential operation;
- no ambient access to organization content merely because an operator has host administration rights;
- secret access limited to the operational purpose;
- remote administration that does not create an undocumented authority path;
- revocation/disablement and credential rotation capability.

A concrete authentication or IAM product is deliberately not selected here.

## 16. Portability and host-loss boundary

The persistent Mac mini MUST NOT become the sole inaccessible representation of organizational meaning or governed state.

Phase 7 MUST preserve a path to:

- export/backup the governed state needed for the declared contour;
- reconstruct exact identities, versions, authority/provenance references and material relationships as applicable;
- restore on a clean secondary environment in P7.10;
- identify host-specific adapters/configuration separately from portable organizational semantics;
- re-provision non-exportable secrets rather than pretending they are portable;
- report known restore/portability gaps truthfully.

Passing portability testing does not establish a supported hardware or OS compatibility matrix.

## 17. Product Contract boundary during persistent operation

Persistent use does not weaken RFC-0004.

For every product workload:

- a Product Contract MUST exist before governed platform reliance where RFC-0004 requires one;
- the exact effective Product Contract version MUST remain attributable in consequential execution;
- the product MUST use declared platform surfaces rather than private tables, undocumented endpoints/imports, private streams or incidental telemetry;
- new platform dependency discovered during operation MUST be added through the appropriate Product Contract/version/change process before consequential reliance;
- product-domain schemas, workflows, approval thresholds, templates and integrations remain product-owned unless separately promoted through governed platform admission.

Product Contract lifecycle remains independent of environment maturity and Platform Capability lifecycle.

## 18. ADR and stable-boundary triggers

P7.01 intentionally leaves concrete implementation choices open. Work MUST stop at the minimum applicable architecture/stable-boundary gate before further material reliance when evidence shows that a choice is becoming materially constraining, cross-product, externally relied upon or expensive to reverse.

Explicit triggers include:

1. a persistence/database/object-store choice becomes a durable cross-product dependency or its schema/serialization becomes expensive to migrate;
2. a service-supervision/deployment mechanism becomes a cross-platform or externally relied-upon contract rather than a Mac mini adapter;
3. a wire format, cross-host API, SDK or serialization boundary is proposed as stable/public/cross-product;
4. an IAM/authentication provider or authorization mechanism becomes a shared durable platform dependency rather than a replaceable adapter;
5. a broker/event store/observability transport becomes necessary for canonical Event semantics or product contracts rather than incidental implementation;
6. public ingress, externally reachable control plane or durable network topology is introduced;
7. encryption/key-management topology creates a shared migration or portability constraint;
8. a Product Contract is proposed for `Stable` transition;
9. a Platform Capability is proposed for `Active` transition;
10. material customer/external Production reliance is proposed.

The required gate MAY be an ADR, focused stable-boundary review, Product Contract decision, capability lifecycle decision, policy/standard or other minimum sufficient governed artifact depending on the decision type.

P7.01 itself crosses none of these triggers.

## 19. Rollback and removal path

The persistent internal runtime MUST remain removable without destroying the canonical repository or creating a false requirement that the Mac mini remain online forever.

The rollback/removal path MUST support, as applicable:

1. stop new governed work safely;
2. surface and reconcile in-flight or uncertain consequential executions rather than discard them;
3. stop and disable the supervised runtime;
4. preserve/verify the latest required governed-state backup before destructive removal;
5. remove runtime/service registration and mutable runtime files independently of source history;
6. retain or export required canonical state and provenance under applicable retention rules;
7. remove or revoke runtime credentials separately from retained historical identity references;
8. restore host configuration altered solely for the runtime where applicable;
9. permit later clean reinstallation/restore from canonical source plus governed backup/evidence.

Rollback/removal MUST NOT replay external effects or mutate historical evidence to make shutdown appear clean.

## 20. Phase 7 requirement allocation

This baseline allocates implementation proof to later Phase 7 work rather than pretending P7.01 already proves runtime behavior.

| Requirement area | Primary proof task |
|---|---|
| supervised process and boot/restart lifecycle | `P7.02` |
| durable state, backup and restore | `P7.03` |
| persistent identity/access/secrets | `P7.04` |
| health/observability/logging/alerting | `P7.05` |
| update/rollback/version/migration | `P7.06` |
| persistent Tender Operator reliance | `P7.07` |
| persistent Discount Parser cross-host reliance | `P7.08` |
| runbook and incident/recovery drills | `P7.09` |
| host-loss/clean restore portability | `P7.10` |
| lifecycle/conformance/stable-boundary disposition | `P7.11` |
| final milestone closure | `P7.12` |

This allocation is sequencing, not permission to defer structural security or authority invariants. Each task must preserve applicable Accepted requirements from its first implementation step.

## 21. P7.02 admission checklist

P7.02 may begin only when R21 records no material unresolved objection to this baseline.

Before P7.02 may be marked PASS, evidence must show at minimum:

- exact canonical source/release pin;
- runtime/source separation;
- secrets outside Git;
- supervised start/stop/restart;
- appropriate boot/login lifecycle;
- health indication;
- crash/restart proof;
- bounded listener exposure with no accidental public ingress;
- safe failure behavior;
- clean disablement/removal path;
- no lifecycle, SLA/support or stable-topology claim created by the implementation.

## 22. Baseline result

`P7.01 operating boundary = DEFINED.`

The allowed next implementation step is `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle`, subject to `R21 PASS`.

This baseline creates no Constitution amendment, RFC change, ADR, lifecycle promotion, Product Contract stabilization, Production claim, public compatibility promise or commercial commitment.