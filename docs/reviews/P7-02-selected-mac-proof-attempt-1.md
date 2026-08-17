# P7.02 — Selected Mac mini Proof Attempt 1

Status: `FAIL recorded / remediation PASS / re-proof required`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Canonical repository: `arvectum/arvectum-os`
Attempted release: `2db9d6c178d8e67a593d7ebb716f86e394862eea`
Remediation PR: `#27`
Remediation merge: `4a46ad40599287dde92ef87a0459965fb2cb45db`
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
- canonical roadmap `2.54.1` at remediation start.

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
- perform a final target-state check at the timeout boundary rather than failing solely because the last sleep completed;
- reuse the same unload helper for `install`, `stop` and `remove` so the race is not duplicated elsewhere.

Defaults remain bounded: `20` attempts at `0.5s` intervals.

No product effect, canonical mutation, network listener, secret behavior, Product Contract or Platform Capability lifecycle changes are introduced.

## 6. Regression evidence

The original hosted test suite checked shell syntax but could not reproduce asynchronous `launchctl bootout` visibility.

The remediation adds an executable fake-`launchctl` regression harness that proves:

1. delayed asynchronous unload eventually succeeds;
2. a target that remains visible beyond the bounded wait fails closed;
3. stopping an already-unloaded target is idempotent.

The delayed-unload case specifically reproduces the old one-shot-check failure shape and would fail against the attempted P7.02 implementation.

Canonical PR `#27` completed `Reference Python CI` run `35` with:

- all three new launchd lifecycle regression tests PASS;
- full Reference Python suite `920/920` PASS;
- no material higher-authority or stable-boundary conflict identified.

PR `#27` was then squash-merged to canonical `main` at:

`4a46ad40599287dde92ef87a0459965fb2cb45db`

## 7. Review iterations

### Iteration 3 — selected-Mac operational evidence

Result: `REVISE`.

Material finding: the repository stop-path had a timing race not represented by the original hosted tests.

Disposition: implement bounded polling and regression reproduction before another selected-Mac attempt.

### Iteration 4 — remediation review

Result: `PASS for repository remediation`.

Evidence:

- targeted asynchronous unload test — PASS;
- bounded unload timeout fail-closed test — PASS;
- already-unloaded idempotency test — PASS;
- full Reference Python CI — `920/920 PASS`;
- no widening of service/deployment boundary;
- no Product Contract or Platform Capability lifecycle change;
- selected-Mac re-proof remains explicitly required.

Functional review iterations used for P7.02 to date: `4 of maximum 7`.

## 8. Closure impact

P7.02 remains open.

The failed attempt does not advance P7.03 and does not establish regular persistent internal operation.

The repository defect observed in Attempt 1 is remediated and CI-validated. The selected Mac mini must now update to the latest exact canonical `main` SHA after roadmap/evidence synchronization and rerun the full P7.02 `install` + `prove` sequence.

Only a complete real-Mac PASS may close P7.02.
