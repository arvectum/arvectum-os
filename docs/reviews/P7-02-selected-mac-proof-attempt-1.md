# P7.02 — Selected Mac mini Proof Attempt 1

Status: `FAIL / remediation prepared / re-proof required`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Canonical repository: `arvectum/arvectum-os`
Attempted release: `2db9d6c178d8e67a593d7ebb716f86e394862eea`
Parent task: `P7.02 — Persistent Mac mini runtime + boot/restart/service lifecycle`

## 1. Purpose

This artifact records the first real selected-Mac execution of the P7.02 persistent runtime proof and the repository remediation triggered by that evidence.

It is operational evidence, not an approval, lifecycle transition, Production claim or P7.02 closure.

## 2. Authority checked

The remediation was reviewed against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 `1.0.0` — Accepted;
- RFC-0003 `1.0.0` — Accepted;
- RFC-0006 `1.0.0` — Accepted;
- P7.01 baseline `1.0.1`;
- R21 — `Complete / PASS`;
- canonical roadmap `2.54.1`.

No Accepted ADR currently selects service supervision/deployment topology. The remediation remains inside the already-declared reversible `launchd` environment adapter and creates no new stable/public boundary.

## 3. Attempt 1 evidence

The selected owner-operated Mac mini reported:

```text
RESULT: FAIL

CANONICAL:
repository: arvectum/arvectum-os
branch: main
HEAD: 2db9d6c178d8e67a593d7ebb716f86e394862eea
origin/main: 2db9d6c178d8e67a593d7ebb716f86e394862eea
working_tree_clean: YES

INSTALL:
result: PASS

PROVE:
result: FAIL

STATUS:
result: FAIL
service_label: com.arvectum.os.persistent-internal
service_state: not loaded

ERRORS:
P7.02 FAIL: service remains loaded after stop (during prove)
P7.02 FAIL: service is not loaded (during status)
```

The attempt did not reach `SIGKILL`, crash restart, listener inspection or final evidence generation. No claim is made for those unexecuted controls.

## 4. Root cause

Result: `repository lifecycle polling defect`.

The canonical P7.02 `stop_runtime` implementation at the attempted release performed:

1. `launchctl bootout`;
2. one fixed `sleep 0.5`;
3. one `launchctl print` check;
4. immediate failure if the target was still visible.

The observed sequence is consistent with asynchronous `launchd` target removal:

- the one-shot post-`bootout` check still observed the target and declared failure;
- by the later explicit `status` call the target was no longer loaded.

Therefore the implementation incorrectly treated a bounded in-progress unload as a failed unload.

This is a P7.02 adapter defect, not evidence that `launchd` is architecturally unsuitable.

## 5. Remediation

The repository remediation changes lifecycle control from a fixed one-shot delay to bounded state polling:

- add `wait_unloaded` with explicit finite attempts and interval;
- add `unload_service` as the single bounded unload helper;
- accept the already-unloaded state idempotently;
- tolerate the narrow case where `bootout` returns failure only if a subsequent state check proves the target is already absent;
- otherwise fail closed when the target remains loaded after the bounded wait;
- reuse the same unload helper for `install`, `stop` and `remove` so the race is not duplicated elsewhere.

Defaults remain bounded: `20` attempts at `0.5s` intervals.

No product effect, canonical mutation, network listener, secret behavior, Product Contract or Platform Capability lifecycle changes are introduced.

## 6. Regression evidence requirement

The original hosted test suite checked shell syntax but could not reproduce asynchronous `launchctl bootout` visibility.

The remediation adds an executable fake-`launchctl` regression harness that proves:

1. delayed asynchronous unload eventually succeeds;
2. a target that remains visible beyond the bounded wait fails closed;
3. stopping an already-unloaded target is idempotent.

The delayed-unload case specifically reproduces the old one-shot-check failure shape and would fail against the attempted P7.02 implementation.

## 7. Review iterations

### Iteration 3 — selected-Mac operational evidence

Result: `REVISE`.

Material finding: the repository stop-path had a timing race not represented by the original hosted tests.

Disposition: implement bounded polling and regression reproduction before another selected-Mac attempt.

### Iteration 4 — remediation review

Status: `Pending CI`.

Required before merge:

- new targeted P7.02 tests PASS;
- full Reference Python CI PASS;
- no higher-authority conflict;
- no widening of the service/deployment boundary;
- selected-Mac proof remains explicitly pending.

## 8. Closure impact

P7.02 remains open.

The failed attempt does not advance P7.03 and does not establish regular persistent internal operation.

After the remediation is merged, the selected Mac mini must update to the new exact canonical `main` SHA and rerun the full P7.02 `install` + `prove` sequence. Only a complete real-Mac PASS may close P7.02.
