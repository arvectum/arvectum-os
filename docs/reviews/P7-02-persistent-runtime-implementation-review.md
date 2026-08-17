# P7.02 — Persistent Runtime Implementation Cross-Review

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed scope: `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle`
Selected-Mac operational proof: `Complete / PASS`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Implementation runbook: [`P7.02 Persistent Mac mini Runtime and Service Lifecycle`](../implementation/P7-02-MAC-MINI-PERSISTENT-RUNTIME.md)
Closure evidence: [`P7.02 Selected Mac mini Proof Attempt 2`](P7-02-selected-mac-proof-attempt-2.md)

## 1. Purpose

This functional cross-review verifies both the repository implementation and the resulting selected owner-operated Mac mini evidence for P7.02.

The review determines whether the bounded persistent runtime satisfies the declared P7.02 scope without silently creating a stable service/deployment architecture, public ingress, product-effect path, lifecycle promotion or stronger production claim.

This review is not `R22`, not a Platform Capability lifecycle transition, not a Product Contract stabilization and not external/customer Production approval.

## 2. Authority baseline checked

Checked at closure:

- Constitution `1.2.0` — `Ratified`, frozen;
- canonical RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
- RFC-0001 — platform/runtime/stable-boundary/operational-readiness constraints;
- RFC-0003 — security, least privilege, secrets, Organization scope and portability constraints;
- RFC-0006 — telemetry non-authority, failure evidence and replay-safety constraints;
- P7.01 baseline `1.0.1`;
- R21 — `Complete / PASS`;
- Accepted ADRs — none currently select service supervision or deployment topology;
- canonical roadmap `2.54.2` immediately before P7.02 closure.

No higher-authority conflict was found.

## 3. Functional review iterations

### Iteration 1 — implementation semantics and evidence specificity

Result: `REVISE`.

Findings:

1. invalid release-SHA negative test could pass for the wrong reason;
2. existing release-directory reuse trusted a SHA-named directory too much;
3. runtime/source separation needed a physical-path check as well as lexical checking.

Disposition:

- test exact invalid-SHA rejection directly;
- reconstruct canonical `git archive` on every install and compare archive SHA-256, deterministic manifest and extracted source;
- fail closed on release mismatch;
- add physical-path source/runtime separation validation.

### Iteration 2 — post-revision repository review

Result: `PASS for repository implementation`.

No material repository-side objection remained before selected-Mac execution.

### Iteration 3 — selected-Mac Attempt 1

Result: `REVISE`.

Attempt 1 installed exact canonical release `2db9d6c178d8e67a593d7ebb716f86e394862eea` successfully but failed during explicit stop. The later status check showed the service already unloaded.

Finding: the adapter used a one-shot `bootout → sleep 0.5 → is_loaded` check and could misclassify an asynchronous unload as failure.

Disposition: bounded polling remediation required before re-proof.

Canonical evidence: [`P7.02 Selected Mac mini Proof Attempt 1`](P7-02-selected-mac-proof-attempt-1.md).

### Iteration 4 — stop-race remediation

Result: `PASS for repository remediation`.

PR `#27` introduced:

- bounded asynchronous unload polling;
- idempotent already-unloaded handling;
- fail-closed timeout behavior;
- final target-state check at timeout boundary;
- one unload helper reused by install/stop/remove;
- executable fake-`launchctl` regression tests.

Reference Python CI run `35`: `920/920 PASS`, including:

- delayed asynchronous unload reproduction;
- bounded timeout fail-closed negative path;
- already-unloaded idempotency path.

PR `#27` was squash-merged at `4a46ad40599287dde92ef87a0459965fb2cb45db`.

### Iteration 5 — selected-Mac Attempt 2 and closure review

Result: `PASS`.

Attempt 2 executed exact canonical release:

`73af746f83271b14670fe22db658dfd55cacb291`

Observed evidence:

- canonical repository `arvectum/arvectum-os` — PASS;
- clean `main`, `HEAD == origin/main` — PASS;
- install — PASS;
- aggregate prove — PASS;
- final status — PASS;
- explicit stop/start — PASS;
- explicit restart — PASS;
- restart changed PID — PASS;
- real `SIGKILL` — YES;
- launchd crash restart — PASS;
- crashed PID `91775`, replacement PID `91885`;
- health generation `3 → 4`;
- network listener exposure — none observed;
- product-effect replay — false;
- canonical-state write by envelope — false;
- reusable P7.02 secrets required — false;
- source checkout dirty — false;
- `RunAtLoad=true`;
- `KeepAlive.SuccessfulExit=false`;
- plist permissions `0600`;
- service left loaded after proof.

No material objection remains for P7.02.

Functional review iterations completed: `5 of maximum 7`.

## 4. Architecture and stable-boundary disposition

Result: `PASS`.

The owner `launchd` LaunchAgent remains a reversible environment adapter. P7.02 creates no:

- public API or wire protocol;
- stable macOS support commitment;
- permanent platform service topology contract;
- database/broker/storage selection;
- Product Contract dependency on `launchd`;
- Platform Capability lifecycle transition;
- external/customer Production claim.

R21's `ADR required now: NO` disposition remains valid. The ADR/stable-boundary trigger must be re-evaluated if this mechanism becomes cross-product, externally relied upon or materially expensive to reverse.

## 5. Source/runtime/release integrity disposition

Result: `PASS`.

The proven path preserves:

- exact canonical repository pin;
- clean canonical branch;
- exact full Git SHA release;
- immutable `git archive` release snapshot;
- release archive/manifest/source verification;
- runtime/source separation;
- isolated version-specific venv;
- clean source checkout after proof.

Raw owner-local paths are not required in canonical closure evidence and are intentionally minimized.

## 6. Service lifecycle disposition

Result: `PASS`.

Selected-Mac evidence proves:

- supervised owner-login service lifecycle;
- explicit stop/start/restart;
- process replacement on restart;
- actual crash recovery through `launchd`;
- bounded unsuccessful-exit restart pressure;
- service remains loaded after proof.

`RunAtLoad=true`, `KeepAlive.SuccessfulExit=false` and plist `0600` were observed on the selected Mac.

## 7. Health and observability boundary

Result: `PASS for P7.02 scope`.

Health remains local operational telemetry, non-canonical by default. It records exact release/process/generation state without becoming organizational authority.

Attempt 2 ended with health generation `4` and PASS state. Crash recovery advanced generation from `3` to `4`.

Broader logs, metrics, alerting and retention/minimization remain P7.05 and R22 scope.

## 8. Network and external-effect boundary

Result: `PASS`.

The selected runtime process owned no observed network listener/socket during proof.

The runtime envelope performs no product/external consequential effect and recorded:

- `product_effect_replay=false`;
- `canonical_state_written_by_runtime_envelope=false`.

Crash/restart supervision is not authorization to replay historical external effects. Persistent Tender Operator and Discount Parser operational reliance remains P7.07/P7.08.

## 9. Secrets and access boundary

Result: `PASS for P7.02 scope`.

P7.02 requires no reusable secret and did not migrate or consume P6 EIS/product secrets.

This does not establish the final persistent service identity/access/secret-rotation model. P7.04 remains responsible for that hardening.

## 10. Failure and recovery disposition

Result: `PASS for process/service lifecycle scope`.

The final proof demonstrates graceful lifecycle control and actual crash replacement. The failed first attempt remains preserved as operational learning evidence and the corresponding repository defect is regression-tested.

Durable governed state recovery, backup/restore and host-loss recovery remain P7.03 and P7.10.

## 11. Known bounded deferrals

The following remain intentionally outside P7.02:

- durable governed/checkpoint state and backup/restore — P7.03;
- persistent service identity/access/secret lifecycle — P7.04;
- broader observability, alerting and telemetry retention — P7.05;
- generalized governed deploy/update/rollback/migration — P7.06;
- repeatable persistent Tender Operator reliance — P7.07;
- repeatable Discount Parser cross-host reliance — P7.08;
- incident/recovery drills — P7.09;
- host-loss portability proof — P7.10;
- lifecycle/conformance/stable-boundary decisions — P7.11;
- M7 closure — P7.12.

These deferrals must not be represented as already proven by P7.02.

## 12. Review result

`P7.02 functional cross-review = Complete / PASS after 5 iterations.`

The repository implementation, remediation and selected-Mac operational proof satisfy the declared P7.02 exit evidence.

The selected Mac mini may enter **regular Persistent Internal / owner-operated** Arvectum OS operation. This is an operational-mode transition only; it does not imply external Production, capability activation, Product Contract stabilization, SLA/support or a stable deployment boundary.

After canonical roadmap synchronization, P7.03 becomes the next canonical action.