# P7.06 — Governed Deploy / Update / Rollback / Version / Migration Path

Status: `Complete / PASS`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance`
Operating classification: `Persistent Internal / owner-operated`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor gate: [`R22 — Persistent Runtime Health Review`](../reviews/R22-persistent-runtime-health-review.md) — `Complete / PASS`
Selected-Mac closure: [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md) — `Complete / PASS`

## 1. Purpose

P7.06 introduces the first explicit owner-operated deployment boundary for the persistent Arvectum OS runtime. It governs exact release identity, update preparation, pre-update durable backup, runtime/observer re-pin, post-update health verification, rollback, historical release reconstruction and state-format migration disposition without creating a public deployment API or Production/support promise.

The first successful live P7.06 proof carried the merged R22 hardening to the selected Mac mini through the governed update path.

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

The selected runtime and observer must resolve to the same exact SHA after every successful update and after rollback. Mutable `current` is only a selector; it is not a version identity.

The P7.02 owner-local adapter replaces the `current` symlink object atomically and verifies that it resolves to the exact target SHA before plist generation and launchd activation. This prevents a directory-symlink destination from leaving the selector stale while a target runtime starts independently from its exact plist.

### 4.1 Bounded pre-R22 first-upgrade bridge

R22 deliberately did not deploy its observer hardening to the already-proven selected-Mac P7.05 release, because that deployment belongs to P7.06. Therefore the first governed update had one narrowly admitted historical source condition:

- exact source release MUST be the canonical P7.05 selected-Mac release `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- the observer MUST actually be loaded;
- the installed plist MUST match the exact historical P7.05 ProgramArguments shape: exact source-release Python plus the historically proven mutable `current/source/.../p7_05_operational_visibility.py` script path and exact runtime-root arguments;
- the historical observer implementation MUST still report healthy operational status;
- any different release, different plist shape, missing observer or different mismatch fails closed.

This was a one-release compatibility bridge for the R22 handoff, not a general relaxation of exact-release verification. Attempt 8 successfully crossed the handoff. After the successful target activation and subsequent rollback/re-update proof, observer execution uses the hardened exact-release pin. No arbitrary pre-R22 or unknown mixed-version observer state is admitted.

## 5. Controlled update sequence

P7.06 requires this order:

1. canonical checkout = clean `main` = `origin/main` and contains the merged R22 hardening;
2. verify the source runtime health and source observer state: normal exact-release P7.05 verification is required except for the bounded `cf60e52…` pre-R22 bridge defined above;
3. prepare/verify target immutable release without selecting it;
4. create immutable P7.06 deployment plan and perform state-format compatibility/migration preflight;
5. acquire a single-writer owner-local deployment lock;
6. retain the exact pre-change runtime and observer plists as historical rollback evidence;
7. verify P7.03 live store and create+verify a new minimized pre-update backup with exact archive SHA-256;
8. stop the observer, then stop the runtime;
9. prove deployment-specific runtime-process quiescence at the existing P7.02 single-instance lock;
10. activate the target using the existing P7.02 canonical install primitive;
11. verify target runtime exact-release health;
12. install/re-pin the R22-hardened observer and verify loaded exact-release consistency;
13. record immutable transaction evidence and the bounded latest-transaction pointer.

If activation or post-update verification fails after the update has begun, the adapter restores the prior exact runtime release and then re-installs the observer through the current P7.05 semantic owner so that the rollback observer is pinned to the restored exact source release. The old observer plist is retained as evidence but is not blindly restored when it contains the known pre-R22 mutable-`current` path. A rollback failure is not represented as success.

The bounded live-remediation sequence also added an operational `recover-interrupted-latest` path for an interrupted transition whose source can be established from retained exact pre-update evidence. Recovery does not fabricate a successful deployment transaction or restore a durable backup unless separately required and authorized.

## 6. Rollback

`rollback-last` is allowed only when the active release equals the target of the latest successful P7.06 transaction and the recorded migration disposition is rollback-safe.

For the current P7.03 store schema, rollback restores the exact prior runtime release, re-pins the observer to that exact prior release, and retains the pre-update backup; it does not restore the backup because no state-format migration occurred. This avoids erasing legitimate state created after deployment.

For the first R22-carry-forward proof, rollback to `cf60e52…` intentionally did **not** recreate the historical unsafe observer plist that referenced mutable `/current/`. The source release was restored exactly, while the observer launchd configuration was regenerated as an exact-release pin to the restored source implementation. Attempt 8 proved both historical release recovery and the R22 mixed-release safety invariant.

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

P7.06 required the selected Mac mini to run `p7_06_selected_mac_proof.sh` from canonical `main` and prove:

- real transition from the already-proven P7.05 release to a target containing R22;
- bounded recognition of the exact historically proven pre-R22 observer state on the first transition, with no general mixed-version exception;
- fresh pre-update verified backup;
- target runtime + observer exact-release health;
- exact historical rollback to the prior runtime release with safe exact-release observer re-pin;
- healthy prior runtime + observer after rollback;
- final controlled re-update to the target release;
- no schema-changing migration, canonical mutation or product/external effect replay by the deployment path;
- retained owner-local attestation digest.

### 9.1 Attempt 8 closure evidence

[`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](../reviews/P7-06-selected-mac-governed-deploy-proof-attempt-8.md) completed `PASS` on `2026-08-18`.

Exact live evidence:

- source release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- target release: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- first pre-update backup SHA-256: `904374591e1de92cf9dbd868f285b728ec78e9dcb5e849f39f632daab833c9d6`;
- first update transaction: `a33209268d34b25c1bb8db9c63e835bf6149a404af57f8e77952177f22c5ffb3`;
- exact rollback transaction: `589f282e3e062c1b5aa298f841f044d4d9c6227214c862d45044673a5ce9e951`;
- second pre-update backup SHA-256: `aa3336b8d16937c36f517aaed8202148ed9ce79aace0aab2fa6461ff58be5e92`;
- final update transaction: `34470ac05993465155b8048405d1dbb712ffb9387b90a29666b927fcfb9dfdc4`;
- final active exact release: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- owner-local proof attestation SHA-256: `3dec1d1dd34aff960753105e72aa60739c01fb61c0af091a554e93f344418e69`.

No schema-changing migration or backup restore occurred. The proof wrapper reported final `P7.06 selected-Mac proof PASS` after update, exact rollback, source verification, final update and exact target verification.

The selected-Mac closure contract is therefore satisfied for the declared bounded operating classification.

## 10. Closure result

`P7.06 = Complete / PASS` for `Persistent Internal / owner-operated` scope, subject to canonical publication of this closure state together with the review and roadmap synchronization and successful final repository CI/read-after-write verification.

The next canonical action after publication is `P7.06-UI1 — Live read-only governed workspace`.

## 11. Non-claims

P7.06 does not establish external/customer Production, an `Active` Platform Capability, Stable Product Contract, public/stable installer/updater API, supported macOS matrix, permanent deployment manager, generalized database migration framework, automatic remote rollout, SLA/SLO/support or broader conformance.