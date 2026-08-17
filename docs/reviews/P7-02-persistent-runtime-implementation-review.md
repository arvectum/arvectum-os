# P7.02 — Persistent Runtime Implementation Cross-Review

Status: `Complete / PASS for repository implementation`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed scope: repository implementation for `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle`
Selected-Mac operational proof: `Pending`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Implementation runbook: [`P7.02 Persistent Mac mini Runtime and Service Lifecycle`](../implementation/P7-02-MAC-MINI-PERSISTENT-RUNTIME.md)

## 1. Purpose

This functional cross-review verifies that the repository-side P7.02 implementation is sufficiently bounded, reversible and testable to proceed to the selected owner-operated Mac mini proof without silently creating a stable service/deployment architecture, public ingress, product effect path, lifecycle promotion or stronger operational claim.

This review is not `R22`, not operational-readiness approval, not a Platform Capability lifecycle transition and not P7.02 closure. Actual `launchd`/Mac lifecycle evidence remains mandatory before P7.02 can become `Complete / PASS`.

## 2. Authority baseline checked

Checked:

- Constitution `1.2.0` — `Ratified`, frozen;
- canonical RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
- RFC-0001 — platform/runtime/stable-boundary/operational-readiness constraints;
- RFC-0003 — security, least privilege, secrets, Organization scope and portability constraints;
- RFC-0006 — telemetry non-authority, failure evidence and replay-safety constraints;
- P7.01 baseline `1.0.1`;
- R21 — `Complete / PASS`;
- Accepted ADRs — none currently select service supervision or deployment topology.

No higher-authority conflict was found.

## 3. Review iterations

### Iteration 1 — implementation semantics and evidence specificity

Result: `REVISE`.

Two issues were identified.

#### Finding 1 — release-pin negative test was not specific enough

The first test for rejecting a short release SHA invoked the health-check path against an empty runtime root. It therefore could pass because `health.json` was absent rather than because the invalid SHA was rejected.

Disposition:

- changed the test to invoke `run` directly with a short SHA;
- require the exact release-SHA validation error;
- require that no health telemetry is created.

#### Finding 2 — existing release-directory reuse needed stronger integrity verification

The first installer version created a canonical Git archive for a new release but, when `releases/<SHA>` already existed, trusted the directory based primarily on its path identity.

That was insufficient for the P7.02 exact deployable-source pin: owner-local corruption or unintended modification could leave a directory named by the correct SHA while its contents no longer matched canonical Git.

Disposition:

- every install now rebuilds the expected canonical `git archive` for the exact SHA in a temporary verification location;
- compares SHA-256 of the stored release archive with the newly generated canonical archive;
- compares the deterministic release manifest;
- recursively compares the extracted runtime source with the canonical archive source;
- fails closed on mismatch rather than silently reusing the release;
- reapplies read-only permissions to the verified source/archive/manifest.

The same revision also added a physical-path check after creating the runtime root so an owner-supplied symlink path cannot bypass the source/runtime separation rule and resolve inside the Git checkout.

### Iteration 2 — post-revision architecture/security/operability review

Result: `PASS for repository implementation`.

No material repository-side objection remains before selected-Mac proof.

Review iterations completed: `2 of maximum 7`.

## 4. Architecture and stable-boundary review

Result: `PASS`.

The implementation deliberately uses an owner `launchd` LaunchAgent as a replaceable environment adapter. It does not create:

- a public API or wire protocol;
- a stable macOS support commitment;
- a persistent platform service topology contract;
- a database/broker/storage selection;
- a Product Contract dependency on `launchd`;
- a Platform Capability lifecycle transition.

The runtime envelope only loads existing bounded domain-neutral semantic modules and publishes local health telemetry. This is consistent with R21's explicit `ADR required now: NO` disposition.

If later evidence turns this supervision/deployment mechanism into a cross-product, externally relied-upon or materially expensive-to-reverse boundary, the P7.01 ADR/stable-boundary trigger must be re-evaluated.

## 5. Source/runtime/release integrity review

Result: `PASS`.

The implementation requires:

- canonical repository `arvectum/arvectum-os`;
- clean branch `main`;
- fast-forward-only synchronization;
- exact `HEAD == origin/main`;
- full 40-character Git release SHA;
- runtime root outside the source checkout by lexical and physical-path checks;
- exact canonical `git archive` release snapshot;
- archive SHA-256 verification on reuse;
- manifest and extracted source comparison on reuse;
- isolated version-specific venv;
- no Python bytecode writes by the supervised runtime into the release snapshot;
- source checkout cleanliness after proof.

The runtime release is therefore reconstructable from canonical Git and is not the mutable Git checkout itself.

## 6. Service lifecycle review

Result: `PASS subject to selected-Mac execution`.

Repository logic provides:

- install;
- start;
- stop;
- restart;
- status;
- crash/restart proof;
- aggregate local proof;
- reversible service removal.

The selected lifecycle is owner-login scoped rather than root/system-wide boot execution. That is consistent with the declared `Persistent Internal / owner-operated` model and the P7.01/P7.02 requirement for a boot/login lifecycle appropriate to that model.

The plist uses `RunAtLoad`, crash supervision and bounded restart throttling. Repository review can inspect this configuration, but actual `launchctl` behavior remains a selected-Mac evidence obligation.

## 7. Health and observability boundary

Result: `PASS`.

Health is local owner-only JSON telemetry that explicitly declares:

- `non-canonical operational telemetry`;
- exact release SHA;
- process instance and generation;
- fresh heartbeat;
- local PID;
- semantic import self-check;
- no network listener mode;
- no product effects;
- no canonical-state writes by the envelope.

The health checker fails when telemetry is missing/stopped/stale, the exact release differs or the recorded PID is no longer alive.

This health document is not canonical Event/evidence, organizational authority or Knowledge.

P7.05 remains responsible for broader logs/metrics/alerting/retention/minimization hardening.

## 8. Network and external-effect boundary

Result: `PASS subject to selected-Mac socket proof`.

The runtime module creates no HTTP/TCP/UDP server and no product/external action adapter.

The Mac proof additionally inspects process-owned network sockets with `lsof` and fails if any are observed.

Crash/restart supervision is explicitly not authorization to replay a consequential product effect. Persistent Tender Operator and Discount Parser operational contours remain P7.07 and P7.08.

## 9. Secrets and local configuration review

Result: `PASS`.

P7.02 itself requires no reusable secret. The runtime root separates `config/` and reserved `secrets/` from source and applies owner-only permissions to the security-sensitive local directories.

The implementation does not read, copy, migrate, print or back up the P6 EIS/product secret material.

This does not establish the final persistent identity/service-access/secret-rotation model; P7.04 remains authoritative for that hardening step.

## 10. Failure and recovery review

Result: `PASS subject to selected-Mac crash proof`.

The runtime:

- prevents two owner processes from using one runtime root simultaneously;
- produces new process-instance/generation evidence after restart;
- marks graceful termination as stopped;
- fails health checks closed for stopped/stale/dead-process state;
- uses unsuccessful-exit supervision for crash replacement;
- keeps service removal separate from destructive state/evidence deletion.

The selected-Mac proof must demonstrate an actual `SIGKILL` followed by a different PID, increased generation and fresh health.

## 11. Testing and CI disposition

Repository tests cover:

- non-canonical/effect-free health semantics;
- exact release pin;
- owner-only health-file permission;
- single-instance lock;
- process-generation continuity after restart;
- stopped-health failure;
- exact invalid-SHA rejection;
- POSIX shell syntax;
- absence of a network-service implementation in the Python runtime envelope.

The canonical `Reference Python CI` full suite is required on the PR because the new tests live under `reference/python/**`.

Hosted CI cannot substitute for the owner-operated Mac `launchd` proof.

## 12. Known bounded deferrals

The following are intentionally not defects in P7.02 and remain assigned to later Phase 7 work:

- durable governed/checkpoint state and backup/restore — P7.03;
- final persistent service identity/access/secret lifecycle — P7.04;
- broader observability, alerting and telemetry retention/rotation — P7.05;
- generalized governed deploy/update/rollback/migration path — P7.06;
- repeatable persistent Tender Operator reliance — P7.07;
- repeatable Discount Parser cross-host reliance — P7.08;
- operator incident/recovery drills — P7.09;
- host-loss portability proof — P7.10.

These deferrals must not be represented as already proven by P7.02.

## 13. Review result

`P7.02 repository implementation cross-review = PASS after 2 iterations.`

The implementation is fit to merge after CI PASS and proceed to selected-Mac execution.

P7.02 itself remains `Current / selected-Mac proof pending` until the canonical merged SHA is installed and the required lifecycle/crash/listener evidence is produced and recorded.
