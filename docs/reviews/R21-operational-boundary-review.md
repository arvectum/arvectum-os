# R21 — Operational Boundary Review

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform` with `governance` and `product_contract`
Trigger: after `P7.01`, before material persistent-runtime implementation
Reviewed artifact: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)

## 1. Purpose

R21 verifies that the P7.01 persistent-use baseline is sufficiently explicit to permit P7.02 implementation without silently selecting or promising unsupported production, persistence, public API, IAM, service, storage or deployment commitments.

This review is a functional engineering/governance checkpoint. It is not a lifecycle transition, production approval, Product Contract stabilization, capability activation or external conformance decision.

## 2. Authority baseline checked

Checked before review:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 are `Accepted 1.0.0` with acceptance evidence;
- RFC-0001 — platform architecture, lifecycle, operational-readiness, stable-boundary and commercial-commitment constraints;
- RFC-0002 — canonical identities/versions, Event and Execution Context semantics, technology-independent persistence constraint;
- RFC-0003 — identity/authentication/authorization/Organizational Authority/data-governance separation, default denial, least privilege, isolation, minimization, retention/deletion, secrets and portability;
- RFC-0004 — Product Contract boundary, no hidden coupling, Provisional/Stable lifecycle separation;
- RFC-0005 — Governed Execution, exact material version pinning, failure/uncertainty/retry semantics, replay-safe external effects;
- RFC-0006 — append-only canonical Events, provenance, telemetry non-authority, observability minimization and replay safety;
- RFC-0007 — Observation/Memory/Knowledge separation and prohibition on silent promotion;
- RFC-0008 — Document/Artifact roles, Transient Output default, handling/retention propagation and portability;
- Accepted ADRs — none currently exist; `docs/adrs/` contains only the ADR process/index;
- `DECISION-2026-08-08 — Engineering Quality and Refactoring Gates` — `Approved`;
- `DECISION-2026-08-17 — Restore Phase 7/8 strategic roadmap and activate Phase 7` — `Approved`;
- Decision Authority Policy — remains `Proposed 0.2.1`; no approved delegation was inferred;
- P6.02 Product Contract — `Provisional 0.1.0`;
- P6.06 Product Contract — `Provisional 0.1.0`, CAP-004-only;
- CAP-001 through CAP-004 — remain `Incubating / Provisional`.

No higher-authority conflict was found.

## 3. Review method and iterations

### Iteration 1 — boundary and sequencing review

The initial P7.01 baseline correctly separated the operating environment from platform architecture and prohibited Production/SLA/lifecycle claims.

One material wording risk was identified: the phrase allowing product workloads after `P7.02 PASS` could be misread as proof that the dedicated persistent Tender Operator and Discount Parser operational contours were already complete, bypassing `P7.07` and `P7.08`.

Disposition: `REVISE`.

The baseline was revised to `1.0.1` to state explicitly that:

- P7.02 enables the persistent internal runtime and only bounded reliance on previously validated contract surfaces;
- repeatable Tender Operator persistent operation is not proven until `P7.07 PASS`;
- repeatable Discount Parser cross-host persistent operation is not proven until `P7.08 PASS`.

### Iteration 2 — post-revision cross-review

The revised baseline was rechecked across architecture, security/authority, data handling, product/platform boundaries, failure/recovery, stable-boundary triggers and roadmap sequencing.

Result: `PASS`.

No material unresolved objection remains.

Review iterations completed: `2 of maximum 7`.

## 4. Operating classification and commercial boundary

Result: `PASS`.

The baseline defines exactly one operating classification:

- `Persistent Internal / owner-operated`.

It explicitly prevents that classification from being interpreted as:

- external/customer Production;
- SLA/SLO/support commitment;
- supported macOS promise;
- stable deployment topology;
- public API/SDK compatibility commitment;
- full-platform conformance;
- Product Contract `Stable` transition;
- Platform Capability `Active` transition.

This is consistent with the Phase 7 activation decision and Accepted RFC-0001 commercial-commitment integrity.

## 5. Organization, operator and authority boundary

Result: `PASS`.

The baseline fixes the initial Organization scope to `ООО «Арвектум»` and prohibits ambient cross-Organization access.

The operating role is named `Arvectum OS Owner-Operator` and must resolve at runtime to an attributable human RFC-0003 Principal/Actor. Raw personal identifiers and credentials are not published merely to prove attribution, preserving minimization in the public repository.

Technical operator or host-admin access is explicitly separated from Organizational Authority. Machine/service execution that becomes operationally significant requires attributable workload/service identity.

No authentication mechanism, IAM provider or delegation policy is selected by P7.01.

## 6. Product/platform boundary

Result: `PASS`.

The admitted product reliance remains bounded by existing Provisional Product Contracts:

- Tender Operator: P6.02 `Provisional 0.1.0`;
- Discount Parser: P6.06 `Provisional 0.1.0`, CAP-004-only.

The baseline preserves product ownership of procurement semantics and Discount Parser offer/scheduler/Telegram/publication semantics, and prohibits hidden database/stream/state coupling.

It also preserves the dedicated P7.07/P7.08 proof sequence after the iteration-1 revision.

No Product Contract lifecycle change or new shared capability dependency is created.

## 7. Data, secrets, retention and portability boundary

Result: `PASS`.

The baseline distinguishes:

- canonical governed state/evidence;
- governance-significant checkpoint state;
- non-canonical telemetry;
- cache/derived/transient outputs;
- owner-local configuration/secrets;
- product-owned data;
- external-authority references/replicas.

It prohibits raw reusable secrets in Git, canonical payloads used merely for convenience, logs and prompts. Backup/restore explicitly excludes unnecessary/non-exportable secrets and requires independent re-provisioning where appropriate.

No universal retention period, RPO/RTO or backup technology is invented. Telemetry is required to remain bounded and non-authoritative; deletion/minimization effects on reconstructability must be represented truthfully.

The Mac mini is not allowed to become the sole inaccessible representation of governed organizational state.

## 8. Failure, retry, replay and recovery boundary

Result: `PASS`.

The baseline requires failure to remain fail-closed or explicitly uncertain/degraded where required evidence/state cannot be verified.

Automatic restart/retry cannot silently duplicate consequential effects. Uncertain external-effect outcomes remain subject to reconciliation/new authorization rather than blind retry.

Rollback/removal preserves in-flight uncertainty, required governed state and provenance and explicitly prohibits effect replay or historical evidence mutation.

These requirements are compatible with RFC-0005 and RFC-0006.

## 9. Runtime/service/network boundary

Result: `PASS`.

P7.01 requires P7.02 to establish supervision, start/stop/restart, boot/login lifecycle, health indication, runtime/source separation, secrets outside source, bounded listeners and removal/rollback.

It does not select the concrete macOS service manager. An environment-specific mechanism such as `launchd` may still be chosen in P7.02 if it remains a reversible adapter rather than a platform contract.

The baseline prohibits accidental public ingress and keeps proxy/TLS/trust behavior explicit where materially relied upon without selecting a permanent network topology.

## 10. Persistence and backup architecture boundary

Result: `PASS`.

The baseline states what state classes require later durability proof but does not choose a physical database, object store, filesystem layout, backup product or serialization contract.

It includes an explicit stop condition if a persistence or serialization choice becomes a durable cross-product dependency or materially expensive to reverse.

Therefore P7.03 can proceed with a simple reversible implementation where sufficient, but cannot silently harden a materially constraining persistence architecture without the applicable ADR/stable-boundary gate.

## 11. ADR and stable-boundary trigger review

Result: `PASS`.

P7.01 enumerates explicit triggers for:

- durable cross-product persistence/schema reliance;
- stable/public/cross-product wire or SDK boundaries;
- shared materially constraining IAM;
- canonical broker/event-store reliance;
- public ingress/control-plane topology;
- shared key-management constraints;
- Stable Product Contract transition;
- Active Platform Capability transition;
- external/customer Production reliance.

No trigger has been crossed by the requirements baseline itself.

`ADR required now: NO.`

## 12. Security/privacy/authority review

Result: `PASS`.

The baseline carries forward structural requirements from RFC-0003 rather than deferring them as future hardening:

- explicit Organization scope;
- attributable actors;
- deny-by-default;
- least privilege;
- no ambient Organizational Authority;
- purpose/minimization constraints;
- secret separation;
- no accidental cross-Organization sharing;
- revocation/rotation path;
- portability without forced secret export.

Later P7.04/P7.05 tasks must provide concrete operational evidence, but P7.02 implementation is already constrained by these invariants.

## 13. Observability and canonical authority review

Result: `PASS`.

The baseline explicitly states that logs, metrics, traces, dashboards and health projections remain non-canonical by default and cannot substitute for canonical Event/evidence or become Knowledge merely by retention.

This prevents P7.05 observability work from creating a competing source of truth.

## 14. Over-specification review

Result: `PASS`.

The baseline intentionally does not define:

- fixed customer SLO/SLA values;
- RTO/RPO;
- concrete retention periods;
- database/storage technology;
- IAM/authentication vendor;
- service manager as a platform contract;
- broker/event store;
- public hostname or reverse proxy;
- TLS termination topology;
- supported OS matrix.

This preserves proportionality and allows later implementation evidence to drive concrete decisions.

## 15. Exit criteria check

P7.01 required outputs:

- [x] operating classification: `Persistent Internal / owner-operated`;
- [x] named owner/operator and Organization scope;
- [x] initial workloads admitted to the persistent boundary;
- [x] explicit non-goals and prohibited external/customer commitments;
- [x] data/classification/retention/secret boundaries;
- [x] authority and approval expectations;
- [x] health/restart/recovery expectations proportionate to internal use;
- [x] backup/restore scope;
- [x] upgrade/rollback requirements;
- [x] network/proxy/trust dependencies;
- [x] operator-access assumptions;
- [x] explicit ADR/stable-boundary triggers;
- [x] rollback/removal path;
- [x] cross-review and bounded revision completed.

## 16. Gate result

`R21 — Operational Boundary Review = PASS.`

`P7.01 = Complete / PASS for its declared repository/governance scope.`

No Constitution amendment, RFC change, ADR, Product Contract lifecycle transition, Platform Capability lifecycle transition, Production approval, SLA/support commitment or stable public boundary is required or authorized by this gate.

The next governed action is:

> **P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle.**

P7.02 may now begin against the P7.01 `1.0.1` baseline.