# P7.06 — Governed Deploy / Update / Rollback / Version / Migration Path

Status: `Repository implementation ready / selected-Mac proof pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance`
Operating classification: `Persistent Internal / owner-operated`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor gate: [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) — `Complete / PASS`

## 1. Purpose

P7.06 introduces the first explicit owner-operated deployment boundary for the persistent Arvectum OS runtime. It governs exact release identity, update preparation, pre-update durable backup, runtime/observer re-pin, post-update health verification, rollback, historical release reconstruction and state-format migration disposition without creating a public deployment API or Production/support promise.

The first live P7.06 proof is intentionally the vehicle that carries the merged R22 hardening to the selected Mac mini.

## 2. Authority baseline

Checked against Constitution `1.2.0` and Accepted RFC-0001 through RFC-0008. The directly material constraints are RFC-0003 portability/migration and source-of-truth controls; RFC-0005 exact material version pinning, failure/rollback/workflow-evolution and replay-safe consequential effects; RFC-0006 append-only canonical evidence semantics and replay safety. No Accepted ADR currently selects a deployment manager, persistence engine, migration framework or supported macOS deployment topology.

ADR disposition: `NO` for this private, reversible, owner-local adapter. Re-open the ADR/stable-boundary gate before an externally relied-upon deployment contract, permanent package/update service, generalized migration framework, cross-product shared deployment topology or customer Production reliance.

## 3. Repository implementation

Files:

- `reference/python/p7_06_governed_deploy.py` — immutable deployment plan, exact-release verification, state-schema compatibility/migration gate, transaction evidence and version status;
- `reference/python/p7_06_macos_deploy.sh` — selected-Mac adapter for target preparation, pre-update backup, controlled runtime/observer stop/update/re-pin/start, post-update verification and exact-release rollback;
- `reference/python/p7_06_selected_mac_proof.sh` — live proof sequence `update → rollback → final update` leaving the host on the new exact release;
- corresponding focused tests under `reference/python/tests/`.

The implementation reuses the P7.02 immutable release format/service lifecycle, P7.03 verified minimized backup, and the R22-hardened P7.05 exact-release observer rather than introducing a second runtime stack.

## 4. Version identity

A deployable version is the full canonical Git commit SHA. Every admitted release must have an immutable `releases/<sha>` source snapshot, matching `release-manifest.json`, verified archive SHA-256, exact release Python environment and required P7.02–P7.05 release-coupled files.

The selected runtime and observer must resolve to the same exact SHA. Mutable `current` is only a selector; it is not a version identity.

## 5. Controlled update sequence

P7.06 requires this order:

1. canonical checkout = clean `main` = `origin/main` and contains the merged R22 hardening;
2. prepare/verify target immutable release without selecting it;
3. create immutable P7.06 deployment plan and perform state-format compatibility/migration preflight;
4. acquire a single-writer owner-local deployment lock;
5. retain the exact pre-change runtime and observer plists for rollback;
6. verify P7.03 live store and create+verify a new minimized pre-update backup with exact archive SHA-256;
7. stop the observer, then stop the runtime;
8. activate the target using the existing P7.02 canonical install primitive;
9. verify target runtime exact-release health;
10. install/re-pin the R22-hardened observer and verify loaded exact-release consistency;
11. record immutable transaction evidence and the bounded latest-transaction pointer.

If activation or post-update verification fails after the update has begun, the adapter restores the prior exact release and prior release-pinned launchd configuration and records the failed-update rollback outcome. A rollback failure is not represented as success.

## 6. Rollback

`rollback-last` is allowed only when the active release equals the target of the latest successful P7.06 transaction and the recorded migration disposition is rollback-safe.

For the current P7.03 store schema, rollback re-pins runtime and observer to the exact prior release and retains the pre-update backup; it does not restore the backup because no state-format migration occurred. This avoids erasing legitimate state created after deployment.

Application rollback never means deleting or rewriting canonical Event history. Historical replay, rollback and retry do not authorize re-execution of prior product/external consequential effects.

## 7. Migration boundary

P7.06 reads the live P7.03 `store_schema` and the target release's literal `STORE_SCHEMA` before service activation.

Current admitted migration mode:

- unchanged schema → `mode=none`, rollback by exact release re-pin is safe;
- changed schema without a migration plan → fail closed;
- changed schema with a declared reversible plan → still fail closed until a bounded exact-release migration executor and rollback proof are implemented and reviewed.

This is deliberate. P7.06 establishes a migration gate and governed extension path without creating an arbitrary-script escape hatch that could mutate canonical state outside Governed Execution. A future schema-changing migration must explicitly define source/target schema identities, reversibility, canonical-mutation authority, backup/restore implications and replay safety before admission.

Irreversible migration is not admitted by the current owner-operated baseline.

## 8. Evidence and authority semantics

Deployment plan/transaction files are owner-local operational evidence and explicitly `canonical_authority=false`. They provide exact version, backup, decision reference and outcome evidence; they do not themselves satisfy Organizational Authority or authorize canonical mutation.

A deployment that merely changes runtime code/configuration must not replay external effects. A future migration that materially changes canonical organizational state remains subject to the applicable Governed Execution and authority path independently of technical deployment access.

## 9. Selected-Mac closure contract

P7.06 is not `Complete / PASS` until the selected Mac mini runs `p7_06_selected_mac_proof.sh` from canonical `main` and proves:

- real transition from the already-proven P7.05 release to a target containing R22;
- fresh pre-update verified backup;
- target runtime + observer exact-release health;
- exact historical rollback to the prior release;
- healthy prior runtime + observer after rollback;
- final controlled re-update to the target release;
- no schema-changing migration, canonical mutation or product/external effect replay by the deployment path;
- retained owner-local attestation digest.

Until that proof passes, P7.07/P7.08 workload expansion remains blocked by roadmap sequencing.

## 10. Non-claims

P7.06 does not establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, public/stable installer/updater API, supported macOS matrix, permanent deployment manager, generalized database migration framework, automatic remote rollout, SLA/SLO/support or broader conformance.
