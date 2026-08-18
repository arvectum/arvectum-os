# P7.06 Selected-Mac Governed Deploy Proof — Attempt 6

Status: `Failed / contained / diagnostic follow-up required`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded operational remediation
Parent: `P7.06 — Governed deploy/update/rollback/version/migration path`

## Authority baseline

Checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0005 `1.0.0` — Accepted;
- RFC-0006 `1.0.0` — Accepted;
- R22 Persistent Runtime Health Review — `Complete / PASS`;
- canonical roadmap — P7.06 remains `Current`; P7.07/P7.08 remain blocked pending successful controlled update/rollback proof.

No higher-authority conflict was identified. This attempt does not create Production, Active capability, Stable Product Contract, SLA/support or a permanent deployment topology.

## Attempt identity

Canonical target at proof start:

`77701d3ffbb67d226bc674337218b37591ba8de7`

Exact live source release:

`cf60e52c93bf0ef4158cf2c3e26792850a126c70`

Decision/proof reference:

`P7.06-selected-mac-owner-operated-proof`

## Observed sequence

1. source observer exact-release status — `PASS`;
2. pre-update durable backup — `PASS`;
3. backup SHA-256 — `cdea36edd91cd38b181a3e30d622018f169449009015376848e4cce95a362ecd`;
4. P7.05 observer uninstall — `PASS`;
5. P7.02 runtime stop — `PASS`;
6. target P7.02 activation — `FAIL: runtime did not become healthy after install`;
7. automatic rollback restored the exact source release;
8. failure/rollback transaction evidence — `PASS`;
9. transaction id — `7ec98de5d0c3b1741610cb8c849022097082c1659b1d0f8fc87d0c63e9b533f7`.

The rollback payload records:

- `result=ROLLED_BACK`;
- exact source and target SHA identities;
- exact backup path and SHA-256;
- runtime and observer release verification `true`;
- `canonical_mutation_performed_by_deploy=false`;
- `product_external_effect_invoked=false`;
- `historical_effect_replay_invoked=false`.

## Post-rollback state

Read-only verification after Attempt 6 established:

- current release restored to `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- P7.02 health — `PASS`;
- P7.02 launchd service — loaded on the exact source release;
- P7.05 observer — loaded and exact-source pinned;
- P7.05 classification — `HEALTHY`;
- store schema unchanged: `arvectum.p7_03.durable-store/1`;
- P7.06 last transaction points to the successful `ROLLED_BACK` transaction above.

## Artifact/runtime compatibility diagnostics

The live source and failed target copies of `p7_02_persistent_runtime.py` have the same SHA-256:

`22d28215f255b1fa4de17599f4cd51f1ad30d60abff7da27a617668c38a1c0ae`

The target venv Python is:

`Python 3.14.7`

The target semantic import self-check passed for:

- `arvectum_os_ref.canonical_lineage`;
- `arvectum_os_ref.governed_execution`;
- `arvectum_os_ref.event_provenance`;
- `arvectum_os_ref.product_contract`;
- `arvectum_os_ref.portability_runtime`.

This rules out the observed target runtime artifact, interpreter availability and semantic importability as the directly demonstrated cause of Attempt 6 failure.

## launchd / stderr evidence and limitation

Owner-local launchd diagnostics around Attempt 6 show the service removed during source stop, enabled for the target activation window, and later removed during rollback. The service was reported inactive at removal.

The cumulative runtime stderr contains repeated:

`P7.02 runtime already has an active owner process`

However, this stderr file is cumulative and does not timestamp individual lines. The existing lines cannot be attributed exclusively to Attempt 6. Therefore this evidence is insufficient to declare a new lock-race root cause by itself.

This review explicitly retracts any stronger inference that Attempt 6 alone proved which exact process held `runtime.lock` during failed target activation.

## Review disposition

Result: `REVISE — cause not yet sufficiently localized`.

What Attempt 6 proves:

- previous target-SHA evidence clobbering is fixed;
- automatic failed-update rollback is now operationally contained and transaction-recorded;
- source state returns healthy after the failed target activation;
- target runtime bytes/Python/import surface are not the demonstrated failure source;
- the remaining defect is inside the live activation/handoff boundary and requires time-scoped process/lock evidence.

What Attempt 6 does **not** prove:

- which process, if any, owned `runtime.lock` during each target startup;
- whether a late source process, transient target process, launchd state transition or another lifecycle condition caused target health failure;
- successful P7.06 update/rollback/update closure.

## Bounded next diagnostic

A separate owner-local activation probe is introduced on branch `fix/p7-06-attempt6-diagnostics`.

The probe does not implement deployment itself. It delegates mutation exclusively to the existing governed P7.06 `update` and `rollback-last` commands while sampling only:

- launchd service PID/state;
- runtime `health.json` release/PID/generation/state;
- PIDs that actually hold the P7.02 `runtime.lock`;
- exact command lines only for those lock-holder PIDs.

It does not take a broad process dump. If the diagnostic update unexpectedly succeeds, the probe immediately invokes the governed `rollback-last` path so the diagnostic session returns to the source state rather than silently becoming a closure proof.

Raw probe samples remain owner-local non-canonical operational diagnostics. Canonical history will retain only the reviewed conclusions and sufficient digests/identities.

## Closure state

`P7.06` remains `Current` and incomplete.

`P7.07` and `P7.08` remain blocked.
