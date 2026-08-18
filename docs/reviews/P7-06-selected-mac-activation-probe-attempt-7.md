# P7.06 Selected-Mac Activation Probe — Attempt 7

Status: `Diagnostic PASS / deployment attempt failed but contained / root cause localized`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded operational remediation
Parent: `P7.06 — Governed deploy/update/rollback/version/migration path`

## Authority baseline

Checked against Constitution `1.2.0` (`Ratified`, frozen), RFC-0001 `1.0.0`, RFC-0005 `1.0.0`, RFC-0006 `1.0.0`, R22 (`Complete / PASS`) and canonical Phase 7 roadmap `2.55.1` / Phase 7 `1.2.6`.

P7.06 core remains `Current`. P7.06-UI remains gated by core PASS. No lifecycle promotion, Production/SLA claim, Stable Product Contract, canonical mutation, product/external effect or historical effect replay is created by this diagnostic.

## Attempt identity

- exact source release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- canonical target at probe start: `ae904fe2f4d670a3c7b54f87d63feb2e607f132e`;
- decision reference: `P7.06-attempt-7-activation-probe`;
- owner-local probe directory: `activation-probe-20260818T104548Z-43479`;
- pre-update backup SHA-256: `cf01c82ba5e0492dbcb5bdcb07a0c9b5b77af2f7d8e3cf48ef388e81fd44972e`;
- contained failed-update rollback transaction: `fe97846428b92fb2d320b0b140e10cefa27e0b16c6517d35a7eb012053c41754`.

## Probe result

The P7.06 update command returned `1` and therefore did not become a successful deployment transaction. Automatic failure rollback succeeded and final P7.06 status returned `0` with the exact source release restored and healthy.

The probe itself remained owner-local non-canonical operational diagnostics and recorded:

- `canonical_mutation_performed_by_probe=false`;
- `product_external_effect_invoked=false`;
- `historical_effect_replay_invoked=false`.

## Time-scoped activation evidence

The probe captured the exact P7.02 lock owner and launchd/health relationship.

Source phase:

- PID `41775` owned `runtime.lock` on source `cf60e52...`;
- launchd state moved from `running` to `SIGTERMed`;
- source health moved to `stopped`;
- lock became unowned before target activation.

Target phase:

- at approximately `10:45:54Z`, launchd started PID `44267` from exact target release `ae904fe2...`;
- PID `44267` acquired `runtime.lock`;
- health changed to exact target release `ae904fe2...`, PID `44267`, generation `31`, state `healthy`;
- target remained continuously observed `running`, lock-owned by PID `44267`, and `healthy` until rollback began around `10:46:16Z`;
- this healthy interval covered essentially the complete P7.02 `wait_healthy()` window.

Rollback phase:

- target PID `44267` received SIGTERM and released the lock;
- source PID `46170` started and acquired the lock;
- health returned to exact source `cf60e52...`, PID `46170`, generation `32`, state `healthy`;
- final P7.02/P7.05 status was healthy and exact-source pinned.

## Diagnostic hashes

Owner-local diagnostic digest identities supplied by the operator:

- `manifest.json`: `ae4c736588e9d7f55b25133871c629cf807d2b66dcfec16792b8b53e490926b3`;
- `samples.tsv`: `d42f5e53774e6cc143125b5265dd3a490a07ccd5d977e4d88b7a8e65d585eaef`;
- `lock-owner-transitions.log`: `6282dff1ac05ca898ce79cb9d3c31cf435886daed66afe40e77c5746689fd204`;
- `update.stdout`: `90f70e513e0cc6bb986942a911e3d8f77cb5405c912957d1776d56e676d016f6`;
- `update.stderr`: `17390463a1d7d726fff860796bdb7b51cb5af97a33ab51128478bfb39af39f92`;
- `final-status.stdout`: `b3f076e4af8628d87e0bfbd679008a087a9ad041e901a805b1787b9f7197db31`;
- `final-status.stderr`: empty-file SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Root-cause localization

Attempt 7 disproves the then-current lock/handoff hypothesis as the reason the target was classified unhealthy:

- source process fully released `runtime.lock` before target lock acquisition;
- target had one exact owner PID;
- target remained healthy for approximately 22 seconds.

The repository P7.02 install path nevertheless returned `runtime did not become healthy after install`.

The remaining discrepancy is explained by the P7.02 `current` pointer replacement implementation:

```sh
rm -f "$RUNTIME_ROOT/current.new"
ln -s "$release" "$RUNTIME_ROOT/current.new"
mv -f "$RUNTIME_ROOT/current.new" "$RUNTIME_ROOT/current"
```

`current` is itself a symbolic link to a release directory. A normal `mv` destination that resolves as a directory can follow that directory symlink and move `current.new` inside the old release directory instead of replacing the `current` symlink itself. In that state:

1. generated launchd `ProgramArguments` correctly pin the new target SHA, so target PID `44267` starts and writes healthy target telemetry;
2. `current` can remain pinned to the old source SHA;
3. P7.02 `wait_healthy()` derives `rel` and the health-check runtime path from `current`;
4. the health checker therefore expects the stale source release while observing a healthy target release;
5. it returns a false negative until the bounded timeout expires;
6. P7.06 correctly interprets the non-zero install result as activation failure and rolls the otherwise healthy target back.

This explanation fits all time-scoped evidence without requiring a target runtime, Python, import, lock or launchd-startup failure.

## Required remediation

The `current` release pointer must be replaced as the symlink object itself, not by directory-following `mv` semantics.

The bounded remediation uses Python `os.replace(prepared, current)` after verifying that the prepared pointer is a symlink and any existing destination is also a symlink. P7.02 then immediately verifies `current_release == HEAD_SHA` before writing the plist or activating launchd.

This preserves the existing exact-release model and does not select a new deployment technology or architecture.

## Closure state

Attempt 7 is a diagnostic success but not a P7.06 deployment proof.

P7.06 remains `Current` until the remediation passes repository review/CI, is merged, and the selected-Mac governed update/rollback/update proof succeeds on the resulting canonical target.
