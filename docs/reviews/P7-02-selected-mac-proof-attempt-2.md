# P7.02 — Selected Mac mini Proof Attempt 2

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Canonical repository: `arvectum/arvectum-os`
Proven release: `73af746f83271b14670fe22db658dfd55cacb291`
Parent task: `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle`
Predecessor evidence: [`P7.02 Selected Mac mini Proof Attempt 1`](P7-02-selected-mac-proof-attempt-1.md) — `FAIL recorded / remediation PASS / re-proof required`

## 1. Purpose

This artifact records the second selected owner-operated Mac mini execution of the P7.02 persistent-runtime proof after remediation of the asynchronous `launchd bootout` race found in Attempt 1.

It is minimized canonical operational evidence. Raw local filesystem paths, reusable secrets and unnecessary personal identity values are intentionally not published.

This PASS closes the selected-Mac evidence obligation for P7.02. It does not create an external/customer `Production` claim, activate a Platform Capability, stabilize a Product Contract, create an SLA/support commitment or establish `launchd` as a stable platform contract.

## 2. Authority and canonical-state check

Checked before closure:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
- RFC-0001 — platform/runtime, proportionality, stable-boundary and operational-readiness constraints;
- RFC-0003 — identity/security, least privilege, secret handling, Organization scope and portability constraints;
- RFC-0006 — telemetry non-authority, evidence and side-effect-safe replay constraints;
- P7.01 baseline `1.0.1`;
- R21 — `Complete / PASS`;
- canonical roadmap `2.54.2` immediately before closure;
- P7.02 repository remediation merged before this proof.

No Accepted ADR selects service supervision/deployment topology. No higher-authority conflict was found. The owner `launchd` LaunchAgent remains a reversible environment-specific adapter.

The exact canonical `main` SHA immediately before Attempt 2 and at local execution was:

`73af746f83271b14670fe22db658dfd55cacb291`

The selected Mac reported:

- branch `main`;
- `HEAD == origin/main == 73af746f83271b14670fe22db658dfd55cacb291`;
- clean working tree before and after proof.

## 3. Attempt 2 result

Overall result: `PASS`.

Repository and release:

- canonical repository: `arvectum/arvectum-os`;
- exact release SHA: `73af746f83271b14670fe22db658dfd55cacb291`;
- source checkout remained clean;
- runtime/source separation check: PASS;
- installation: PASS;
- aggregate proof: PASS;
- final status: PASS.

Final service state:

- service label: `com.arvectum.os.persistent-internal`;
- state: `loaded`;
- final observed PID: `91885`;
- health generation: `4`;
- health state: PASS.

The service was intentionally left running after proof so the selected Mac mini enters the declared regular persistent internal operating mode.

## 4. Lifecycle evidence

Observed controls:

| Control | Result |
|---|---|
| explicit stop/start | `PASS` |
| explicit restart | `PASS` |
| restart replaced PID | `PASS` |
| actual `SIGKILL` performed | `YES` |
| launchd crash restart | `PASS` |
| crashed PID | `91775` |
| replacement PID | `91885` |
| health generation before crash | `3` |
| health generation after crash | `4` |

The crash proof therefore demonstrated a real unsuccessful process termination followed by supervised replacement with a different PID and advancing runtime generation.

## 5. Boundary evidence

Observed boundary fields:

- network listener exposure: `none observed`;
- product-effect replay: `false`;
- canonical state written by runtime envelope: `false`;
- reusable P7.02 secrets required: `false`;
- source checkout dirty: `false`.

This remains consistent with RFC-0006: health/log evidence is operational telemetry, non-canonical by default, and restart supervision is not authorization to replay a historical consequential external effect.

## 6. LaunchAgent evidence

Observed service configuration:

- `RunAtLoad = true`;
- `KeepAlive.SuccessfulExit = false`;
- plist permissions = `0600`;
- unsuccessful-exit supervision uses the already-declared bounded `ThrottleInterval=5` configuration.

This is the owner-login lifecycle selected by P7.02. No root/system LaunchDaemon or public ingress was introduced.

## 7. Local evidence references

Selected-Mac local evidence basenames:

- `p7-02-summary-20260817T175128Z.txt`;
- `p7-02-crash-20260817T175127Z.json`.

The crash evidence records:

- schema `arvectum.p7_02.crash-restart-proof/1`;
- classification `local operational evidence; non-canonical telemetry`;
- exact release SHA `73af746f83271b14670fe22db658dfd55cacb291`;
- crashed PID `91775`;
- replacement PID `91885`;
- generation `3 → 4`;
- `launchd_restart_observed=true`;
- `network_listener_exposure="none observed"`;
- `product_effect_replay=false`;
- recorded time `2026-08-17T17:51:27.956351Z`.

Raw local path values are deliberately omitted from canonical closure evidence. The proof result records only the required source/runtime separation and clean-checkout outcome.

## 8. Attempt 1 remediation continuity

Attempt 1 failed at the stop path because the original adapter treated asynchronous `launchd` unload as a one-shot synchronous check.

PR `#27` replaced that behavior with bounded polling and added executable regression coverage for:

1. delayed asynchronous unload;
2. bounded timeout with fail-closed behavior;
3. idempotent already-unloaded stop.

Reference Python CI run `35` completed `920/920 PASS` before Attempt 2. Attempt 2 then exercised the remediated path on the selected Mac and passed the full proof.

The failed first attempt remains preserved as evidence rather than rewritten or hidden.

## 9. Functional cross-review iteration 5

Result: `PASS`.

Review checks:

- exact canonical release pin — PASS;
- canonical repository and clean `main` — PASS;
- install/prove/status — PASS;
- explicit stop/start/restart — PASS;
- restart PID replacement — PASS;
- real crash + launchd recovery — PASS;
- health generation advanced `3 → 4` — PASS;
- network listener boundary — PASS;
- no product-effect replay — PASS;
- no canonical-state mutation by the envelope — PASS;
- reusable P7.02 secrets absent — PASS;
- `RunAtLoad=true` — PASS;
- `KeepAlive.SuccessfulExit=false` — PASS;
- plist `0600` — PASS;
- service left running — PASS;
- no new stable/public boundary or lifecycle promotion — PASS.

No material objection remains for the declared P7.02 scope.

Functional review iterations used for P7.02: `5 of maximum 7`.

## 10. Closure disposition

`P7.02 selected-Mac proof = Complete / PASS.`

The selected Mac mini now satisfies the declared P7.02 threshold for **regular Persistent Internal / owner-operated Arvectum OS operation**.

This transition remains deliberately scoped. The following are still unproven and remain assigned to later Phase 7 work:

- durable governed/checkpoint persistence and verified backup/restore — P7.03;
- persistent least-privilege identity/service access and secret lifecycle — P7.04;
- broader observability/alerting/retention — P7.05;
- generalized governed update/rollback/migration — P7.06;
- repeatable persistent Tender Operator operation — P7.07;
- repeatable Discount Parser cross-host operation — P7.08;
- incident/recovery drills — P7.09;
- host-loss/clean-environment portability — P7.10;
- lifecycle/conformance/stable-boundary dispositions — P7.11;
- M7 closure — P7.12.

P7.03 becomes the next canonical action after repository closure synchronization.