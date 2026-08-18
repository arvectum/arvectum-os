# P7.06 Selected-Mac Governed Deploy Proof — Attempt 6

Status: `Failed / contained / diagnostic follow-up required`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded operational remediation
Parent: `P7.06 — Governed deploy/update/rollback/version/migration path`

## Authority baseline

Checked against Constitution `1.2.0` (`Ratified`, frozen), Accepted RFC-0001/0005/0006, R22 (`Complete / PASS`) and the current canonical Phase 7 roadmap. P7.06 core remains the current gate. The new Live Operator Workspace substream is explicitly gated by P7.06 core PASS; P7.06-UI1 follows core PASS before P7.07/P7.08 workload expansion.

No higher-authority conflict was identified. No Production, Active capability, Stable Product Contract, SLA/support or permanent deployment topology claim is created.

## Attempt identity

- canonical target at proof start: `77701d3ffbb67d226bc674337218b37591ba8de7`;
- exact live source: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- decision/proof ref: `P7.06-selected-mac-owner-operated-proof`.

## Observed sequence

1. source observer exact-release status — `PASS`;
2. pre-update durable backup — `PASS`;
3. backup SHA-256 — `cdea36edd91cd38b181a3e30d622018f169449009015376848e4cce95a362ecd`;
4. P7.05 observer uninstall — `PASS`;
5. P7.02 runtime stop — `PASS`;
6. target activation — `FAIL: runtime did not become healthy after install`;
7. automatic rollback restored the exact source release;
8. failure/rollback transaction evidence — `PASS`;
9. transaction id — `7ec98de5d0c3b1741610cb8c849022097082c1659b1d0f8fc87d0c63e9b533f7`.

The rollback payload records `result=ROLLED_BACK`, exact source/target SHA identities, exact backup path/SHA-256, runtime/observer verification true, and false for deploy canonical mutation, product/external effect and historical effect replay.

## Post-rollback state

Read-only verification established:

- current release restored to `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- P7.02 health `PASS` and launchd service loaded on the exact source release;
- P7.05 observer loaded/exact-source pinned and `HEALTHY`;
- store schema unchanged: `arvectum.p7_03.durable-store/1`;
- P7.06 last transaction points to the successful `ROLLED_BACK` transaction above.

## Artifact/runtime compatibility diagnostics

Source and failed-target copies of `p7_02_persistent_runtime.py` have identical SHA-256:

`22d28215f255b1fa4de17599f4cd51f1ad30d60abff7da27a617668c38a1c0ae`

Target venv Python is `Python 3.14.7`. Target semantic import self-check passed for canonical lineage, governed execution, event provenance, product contract and portability runtime modules.

This excludes the observed runtime bytes, interpreter availability and semantic importability as the directly demonstrated cause of Attempt 6 failure.

## launchd / stderr evidence limitation

Owner-local launchd diagnostics show source removal, target enablement and later removal during rollback. The cumulative runtime stderr contains repeated `P7.02 runtime already has an active owner process`, but that file is timestampless and cumulative across attempts. Those lines cannot be attributed exclusively to Attempt 6.

Therefore Attempt 6 does not yet prove which exact process, if any, held `runtime.lock` during target startup. Any stronger lock-race conclusion would be speculative.

## Review disposition

Result: `REVISE — cause not yet sufficiently localized`.

Attempt 6 proves that target-SHA evidence clobbering is fixed, automatic rollback is now contained and transaction-recorded, source health is restored after failure, and the remaining defect is within the live activation/handoff boundary.

## Bounded next diagnostic

`reference/python/p7_06_activation_probe.sh` delegates mutation only to the existing governed P7.06 `update`, `rollback-last` and `status` commands while sampling:

- launchd service PID/state;
- runtime health release/PID/generation/state;
- PIDs actually holding P7.02 `runtime.lock`;
- exact command lines only for those lock-holder PIDs.

It does not take a broad process dump. If the diagnostic update succeeds, it immediately invokes governed `rollback-last` to preserve diagnostic source-state intent. Raw samples remain owner-local non-canonical diagnostics.

## Closure state

P7.06 core remains `Current` and incomplete. P7.06-UI1 remains gated by core PASS; P7.07/P7.08 remain downstream.
