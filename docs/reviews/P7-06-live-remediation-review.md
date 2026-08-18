# P7.06 — Selected-Mac Live Remediation Review

Status: `Repository remediation under review / selected-Mac recovery and proof pending`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance` and operational recovery
Parent work item: `P7.06 — Governed deploy/update/rollback/version/migration path`
Predecessor review: [`P7.06 Governed Deploy / Update / Rollback Implementation Cross-Review`](P7-06-governed-deploy-implementation-review.md) — repository/live-readiness PASS after the configured maximum 7 iterations

## 1. Why this is a separate review

The original P7.06 implementation cross-review reached the configured maximum seven functional iterations. The next materially distinct selected-Mac defect therefore opens this separate bounded remediation review rather than creating an invalid eighth iteration in the predecessor review.

This review does not reopen or amend Accepted RFCs, does not create a new deployment architecture, and does not change Product Contract or Platform Capability lifecycle.

## 2. Authority baseline checked

Checked before remediation:

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

Canonical checkout at execution was updated to:

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

The run therefore crossed the stop boundary but did not establish a healthy target release and did not establish a successful rollback transaction.

No schema-changing migration, product/external effect, historical effect replay or canonical mutation by the deploy adapter was reported or authorized. The verified P7.03 backup is retained and was not restored.

The post-failure live service state is treated as operationally uncertain until explicit recovery verifies the exact runtime and observer release pins.

## 4. Review iteration 1 — REVISE

Result: `REVISE`.

Two coupled operational defects are material.

### F1 — deployment stop did not prove process quiescence

P7.02 `stop` proves bounded asynchronous disappearance of the launchd target. Its accepted P7.02 scope did not require an immediate redeploy barrier proving that the old runtime process had also released the P7.02 single-instance `runtime.lock`.

P7.06 immediately installed the target after P7.02 returned `stop PASS`. A still-terminating old process can therefore remain inside the deployment race window even though launchd no longer reports the job.

The observed target-health failure is consistent with that missing deployment-specific quiescence barrier. This is recorded as the strongest repository-supported explanation, not as a claim that the owner-local stderr log has independently proven the exact process-level cause.

### F2 — rollback bypassed already-hardened lifecycle owners

`restore_plist_and_start()` used direct one-shot `launchctl bootout ... || true` calls for the runtime and observer, then immediately attempted `bootstrap`.

That path bypassed the bounded asynchronous unload handling already owned by P7.02/P7.05 and reintroduced the class of launchd race discovered during P7.02 closure. The observed `Bootstrap failed: 5` is consistent with this rollback race and makes the previous rollback implementation insufficiently fail-closed/recoverable for P7.06.

## 5. Remediation design

The bounded remediation keeps responsibility at the minimum sufficient layer: P7.02/P7.05 remain the lifecycle semantic owners, while P7.06 adds only deployment-specific quiescence and interrupted-transaction recovery.

Implemented changes on branch `fix/p7-06-interrupted-rollback-recovery`:

1. after P7.02 stop and before target install, P7.06 polls the existing `runtime.lock` with a non-blocking `fcntl.flock` probe until the old process has actually released the single-instance lock or a bounded timeout fails closed;
2. rollback removes direct runtime/observer `bootout` calls and delegates bounded unload to P7.05 `uninstall` and P7.02 `stop`;
3. rollback additionally requires runtime-lock quiescence before source plist bootstrap;
4. normal `rollback-last` reuses the same hardened restoration function rather than pre-running best-effort `|| true` unloads;
5. new `recover-interrupted-latest` restores the exact source release from the newest retained P7.06 work evidence after an interrupted failed-update rollback;
6. recovery derives and validates the source SHA from the saved pre-update runtime plist, including label, runtime root, version-specific Python and version-specific runtime script path;
7. recovery verifies exact source runtime health and exact observer release pin after restoration;
8. recovery writes owner-local non-canonical evidence and explicitly records that it did not restore durable backup, mutate canonical state, invoke product/external effects or replay historical effects;
9. interrupted recovery does not fabricate a successful deployment transaction.

The recovery command is operational recovery only. It does not authorize a new deployment, migration or external action.

## 6. Product/platform, authority and ADR disposition

Result after design review: `PASS with live evidence pending`.

- no product-domain logic is added;
- no Product Contract dependency changes;
- no Platform Capability lifecycle changes;
- no Organizational Authority is created by recovery;
- no external/customer Production or SLA/support claim is introduced;
- no permanent service/deployment technology is selected;
- no new ADR trigger is crossed at the current private, reversible owner-local scope.

## 7. Required closure evidence for this remediation review

Before this remediation review can become `Complete / PASS`:

1. full Reference Python CI must pass on the final remediation head;
2. PR diff must preserve backup-before-stop, compatibility/migration gates and replay-safety constraints;
3. remediation must merge to canonical `main`;
4. selected Mac must run `recover-interrupted-latest` and prove exact source runtime + observer health;
5. complete selected-Mac P7.06 proof must then execute `update → rollback → final update → final status` successfully on the merged canonical target;
6. canonical P7.06 closure documents and both roadmaps must be synchronized only after that live proof.

Until then:

- `P7.06 = Current`;
- `P7.07` and `P7.08` remain blocked;
- the selected-Mac runtime state after Attempt 4 is not claimed healthy until explicit recovery evidence passes.
