# P7.06 — Selected-Mac Live Remediation Review

Status: `Repository remediation PASS / selected-Mac proof pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance` and operational recovery
Parent work item: `P7.06 — Governed deploy/update/rollback/version/migration path`
Predecessor review: [`P7.06 Governed Deploy / Update / Rollback Implementation Cross-Review`](P7-06-governed-deploy-implementation-review.md) — repository/live-readiness PASS after the configured maximum 7 iterations

## 1. Why this is a separate review

The original P7.06 implementation cross-review reached the configured maximum seven functional iterations. Materially distinct selected-Mac defects therefore continue in this separate bounded remediation review rather than creating invalid iterations in the predecessor review.

This review does not reopen or amend Accepted RFCs, does not create a new deployment architecture, and does not change Product Contract or Platform Capability lifecycle.

## 2. Authority baseline checked

Checked before and during remediation:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC Index — RFC-0001 through RFC-0008 `Accepted 1.0.0`;
- RFC-0001 — operationally significant behavior, exact versioning, technology independence and no implicit production/stable-boundary claim;
- RFC-0005 — exact material version pinning, explicit failure/rollback semantics, governed consequential execution boundaries and no effect replay by historical recovery;
- RFC-0006 — required operational evidence must not fail silently; telemetry remains non-canonical by default; replay/recovery does not authorize a new external effect;
- R22 — `Complete / PASS`, with first P7.06 update still responsible for carrying the R22 hardening;
- canonical roadmap — P7.06 remains `Current`; P7.07/P7.08 remain blocked until the first controlled update/rollback proof passes;
- Accepted ADRs — none select a permanent deployment manager, service supervisor or macOS topology.

No higher-authority conflict was found in the bounded owner-operated remediation scope.

## 3. Selected-Mac Attempt 4 — observed failure

Canonical checkout at execution:

`deb2bee14e41abff51d44949adcf61c319cdf3a5`

Source release before mutation:

`cf60e52c93bf0ef4158cf2c3e26792850a126c70`

Observed sequence:

1. bounded historical R22 carry-forward observer verification — `PASS`;
2. pre-update P7.03 backup — `PASS`;
3. exact backup SHA-256 — `7bcd70dd9ad1a9c92716d4a5e254693bec19624a7d0446aabc3e3a4e15dc9d93`;
4. P7.05 observer uninstall — `PASS`;
5. P7.02 stop — `PASS`;
6. target P7.02 install — `FAIL: runtime did not become healthy after install`;
7. automatic P7.06 rollback then reached `launchctl bootstrap` and failed with macOS `Bootstrap failed: 5: Input/output error` before recovery could be proven complete.

The run crossed the stop boundary but did not establish a healthy target release or successful rollback transaction. No schema-changing migration, product/external effect, historical effect replay or canonical mutation by the deploy adapter was reported or authorized. The verified P7.03 backup was retained and not restored.

## 4. Review iteration 1 — REVISE

Result: `REVISE`.

Two coupled operational defects were material.

### F1 — deployment stop did not prove process quiescence

P7.02 `stop` proved bounded asynchronous disappearance of the launchd target but did not provide the deployment-specific barrier that the old runtime process had also released the P7.02 single-instance `runtime.lock` before immediate redeploy.

### F2 — rollback bypassed already-hardened lifecycle owners

`restore_plist_and_start()` used direct one-shot launchd bootout calls and immediately attempted bootstrap. That bypassed bounded asynchronous unload handling already owned by P7.02/P7.05 and was consistent with the observed rollback `Bootstrap failed: 5` race.

## 5. First remediation design

Implemented by PR `#45 — P7.06 — Harden interrupted rollback and runtime quiescence`:

1. P7.06 polls the existing `runtime.lock` after P7.02 stop and before target install until the old process releases it or a bounded timeout fails closed;
2. rollback delegates bounded unload to P7.05 `uninstall` and P7.02 `stop`;
3. rollback requires runtime-lock quiescence before source restoration;
4. normal `rollback-last` reuses the same hardened restoration function;
5. `recover-interrupted-latest` restores the exact source release from retained pre-update work evidence;
6. recovery derives and validates the source SHA from the saved runtime plist, including exact runtime root, version-specific Python and runtime script path;
7. recovery verifies exact source runtime health and observer release pin;
8. recovery writes owner-local non-canonical evidence and records no durable backup restore, canonical mutation, product/external effect or historical replay;
9. interrupted recovery does not fabricate a successful deployment transaction.

## 6. Review iteration 2 — PASS repository-side

Result: `PASS / selected-Mac recovery and proof pending`.

Repository evidence for PR #45:

- code/test head `7a4094bd53bc23d15ac3e6401ffa95e8036f19cb`;
- Reference Python CI run `32125129079`;
- job `95673871057 — Full reference test suite`;
- `984/984 PASS`;
- follow-up final review CI run `32125275729` — `success`;
- canonical merge commit `b218251a3885b190795ca431deebd41848fcc1d4`.

No material repository-side objection remained after iteration 2.

## 7. Selected-Mac interrupted recovery after Attempt 4 — PASS

After PR #45 merged, the selected Mac executed `recover-interrupted-latest` before another deployment attempt.

Recovery evidence:

- exact source restored: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- owner-local recovery evidence: `work-20260818T095406Z-17117/interrupted-recovery-20260818T101401Z.json`;
- P7.02 health — `PASS`;
- P7.02 launchd service — loaded and pinned to the exact source release;
- P7.05 observer — loaded and pinned to the same source release;
- P7.05 runtime classification — `HEALTHY`;
- P7.06 status — `current_release=cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- `last_transaction=null`, confirming recovery did not fabricate successful deployment evidence;
- store schema remained `arvectum.p7_03.durable-store/1`.

This closed the uncertain post-Attempt-4 service state but did not close P7.06.

## 8. Selected-Mac Attempt 5 — observed failure

Attempt 5 began from the recovered healthy source and pinned canonical target:

`b218251a3885b190795ca431deebd41848fcc1d4`

Observed sequence:

1. source observer exact-release verification — `PASS`;
2. pre-update backup — `PASS`;
3. exact backup SHA-256 — `1ef57aaf322e4f815b6440670b11430ead986461eec4515b605173e1c507b668`;
4. P7.05 observer uninstall — `PASS`;
5. P7.02 stop — `PASS`;
6. deployment-specific runtime-lock quiescence did not fail, so execution reached target install;
7. target install — `FAIL: runtime did not become healthy after install`;
8. source release restoration completed;
9. failure transaction evidence then failed validation with `release must be a full 40-character Git commit SHA`;
10. P7.06 reported source restored but transaction evidence recording failed.

The quiescence remediation from iteration 1 was therefore necessary for safe handoff but was not sufficient to explain or remove the target activation failure.

## 9. Review iteration 3 — REVISE

Result: `REVISE`.

Read-only owner-local diagnostics after Attempt 5 established two further concrete defects.

### F3 — P7.02 install creates a RunAtLoad self-race

Selected-Mac runtime stderr contained repeated:

`P7.02 runtime already has an active owner process`

The target exact-release Python and target P7.02 runtime code successfully checked the restored source health, ruling out the observed target Python/runtime artifact as the immediate failure source. Repository comparison from `cf60e52c93bf0ef4158cf2c3e26792850a126c70` to `b218251a3885b190795ca431deebd41848fcc1d4` also confirmed that P7.02 runtime/service code itself had not changed between those releases.

The concrete lifecycle defect is in the existing P7.02 install sequence:

1. generated plist declares `RunAtLoad=true` and `KeepAlive.SuccessfulExit=false`;
2. `launchctl bootstrap` therefore admits and starts the runtime;
3. install immediately executes `launchctl kickstart -k` against that newly starting job;
4. the killed/replacement lifecycle can overlap at the P7.02 single-instance `runtime.lock`, producing the exact repeated live diagnostic and preventing stable target health.

The fix must preserve `kickstart -k` for explicit restart/replacement semantics while removing it from initial install after RunAtLoad bootstrap.

### F4 — P7.06 `wait_loaded()` clobbers the Git target SHA

P7.06 used a POSIX-shell function assignment `target=$1` inside `wait_loaded()`. Shell function variables are process-global in this adapter. During rollback, calling `wait_loaded "$RUNTIME_TARGET"` therefore replaced the deployment Git target SHA with `gui/<uid>/com.arvectum.os.persistent-internal`.

Failure transaction recording then passed that launchd target as `target_release`, producing the observed full-SHA validation error and losing required failure transaction evidence.

This is an evidence-integrity defect independent of F3.

## 10. Second remediation design

Branch: `fix/p7-06-target-evidence-clobber`.

Bounded changes:

1. P7.02 `install_runtime()` retains `launchctl bootstrap` and `wait_healthy` but removes immediate `kickstart -k`; RunAtLoad owns the initial start;
2. P7.02 explicit `restart_runtime()` retains `kickstart -k` where process replacement is intentional;
3. P7.06 `wait_loaded()` uses a distinct `wait_target` variable and no longer overwrites the deployment Git `target` SHA;
4. failure payload continues to use the immutable deployment target SHA from the preflight/update context;
5. regression guards cover install-vs-restart lifecycle semantics, target-variable preservation and POSIX shell syntax.

The remediation does not change durable-state schema, migration policy, Product Contract scope, Platform Capability lifecycle, Organizational Authority, canonical state, external effects or replay semantics.

## 11. Review iteration 4 — PASS repository-side

Result: `PASS / selected-Mac proof pending`.

PR `#46 — P7.06 — Remove launchd install self-race and preserve target evidence` was reviewed against the Attempt 5 evidence and the existing P7.02/P7.06 lifecycle boundaries.

Final code/test head before this review-evidence update:

`cba20a541683caf538f78e78a3b7572b67fa8bcc`

GitHub verification:

- Reference Python CI run `32126851553` (`#69`) — `success`;
- job `95679210687 — Full reference test suite` — `success`;
- PR merge-test SHA `66c8763c429c9e6cd4cef99ce9ae3267d7980a42`;
- `988/988 PASS` (`Ran 988 tests in 12.413s — OK`);
- P7.02 existing lifecycle/runtime tests — PASS;
- P7.06 existing governed deploy/rollback/recovery tests — PASS;
- new install RunAtLoad self-race guard — PASS;
- explicit restart replacement guard — PASS;
- P7.06 Git target preservation guard — PASS;
- remediated POSIX shell syntax guards — PASS.

An earlier intermediate PR CI run failed only because the newly written structural test searched for substring `target=$1`, which is also contained inside the correct `wait_target=$1`. The guard was corrected to reject only the exact assignment line `target=$1`. No runtime, deployment or governance semantics changed as part of that test-only correction. The final full suite above is the governing repository-side evidence.

Diff review confirms:

- initial P7.02 install is now `launchctl bootstrap → wait_healthy` with no immediate forced replacement;
- explicit P7.02 restart retains `launchctl kickstart -k`;
- P7.06 `wait_loaded()` uses `wait_target` rather than the deployment Git `target` variable;
- failed-update payload construction continues to preserve the exact preflight Git target SHA;
- backup-before-stop, compatibility/migration gates, exact-release pinning, rollback/recovery and no-effect-replay constraints remain intact.

No material repository-side objection remains after iteration 4. The remaining closure gap is live selected-Mac proof on the merged canonical remediation target.

## 12. Product/platform, authority and ADR disposition

Current disposition remains bounded:

- no product-domain logic is added;
- no Product Contract dependency changes;
- no Platform Capability lifecycle changes;
- no Organizational Authority is created;
- no external/customer Production or SLA/support claim is introduced;
- no permanent service/deployment technology is selected;
- no new ADR trigger is crossed at the current private, reversible owner-local scope.

## 13. Closure state

Until the selected-Mac full proof succeeds and canonical closure is synchronized:

- `P7.06 = Current`;
- `P7.07` and `P7.08` remain blocked;
- source runtime `cf60e52c93bf0ef4158cf2c3e26792850a126c70` is the last live release whose post-Attempt-5 status was explicitly verified healthy;
- no P7.06 successful deployment transaction has yet been established;
- no Production, Active capability, Stable Product Contract, SLA/support or broader conformance claim is created.
