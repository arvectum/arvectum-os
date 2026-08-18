# P7.06 — Governed Deploy / Update / Rollback Implementation Cross-Review

Status: `Complete / PASS — repository/live-readiness review closed; selected-Mac closure recorded separately`
Date: `2026-08-18`
Owner: `ООО «Арвектум»`
Task classification: `platform` with bounded `governance`

## 1. Scope

Functional review covers the repository-side P7.06 deployment/version/migration boundary and the defects surfaced while attempting the selected-Mac proof. Roles considered materially relevant: architecture/governance, engineering, operations/recovery, security/data governance and product/platform boundary.

The configured maximum seven iterations applied to this review artifact. Material defects discovered after iteration 7 were intentionally handled in the separate [`P7.06 Selected-Mac Live Remediation Review`](P7-06-live-remediation-review.md), preserving the review cap rather than creating an invalid iteration 8 here.

## 2. Iteration 1 — REVISE

Material finding: an initial failure path could restore the prior runtime/observer release but terminate without a P7.06 transaction record. That would leave a consequential operational transition observable only through process exit/raw diagnostics.

Remediation: failed activation or post-update health/re-pin verification now restores the exact source release and attempts an immutable `ROLLED_BACK` transaction record carrying the plan, backup identity and rollback disposition. Evidence-recording failure remains explicitly visible as an operator-investigation condition rather than a false PASS.

## 3. Iteration 2 — REVISE

Material security/recovery finding: transaction evidence originally trusted an arbitrary backup path/SHA supplied by the adapter.

Remediation: the Python evidence boundary now requires the retained backup to exist directly under the owner-local P7.03 `backups/` directory, validates a full SHA-256 and recomputes the archive digest before accepting a transaction record.

## 4. Iteration 3 — PASS for initial repository stage

Architecture/governance: PASS. Exact Git release identity and source/target schema identity are explicit; no Accepted contract is changed; deployment evidence does not claim authority; no public/stable boundary is introduced.

Engineering: PASS for repository stage. One deployment lock prevents concurrent owner-local transitions; target release is prepared/verified before activation; runtime and observer remain one exact-release unit after successful activation; rollback preserves historical release identity.

Operations/recovery: PASS for unchanged P7.03 schema. Every update requires a fresh verified backup; rollback does not restore data unnecessarily; failed updates are fail-closed and recorded. Live behavior still required selected-Mac proof.

Security/data governance: PASS. No reusable secrets enter deployment evidence/backup; migration cannot use arbitrary executable hooks; schema-changing migration is blocked until a separately bounded executor and authority/rollback proof exist; external-effect replay remains false.

Product/platform: PASS. The adapter is domain-neutral and imports no Tender Operator/Discount Parser logic, databases or private product streams. Product Contract and capability lifecycle remain unchanged.

This PASS was explicitly provisional on live selected-Mac execution; subsequent live attempts legitimately reopened the review when real operational defects were observed.

## 5. Iteration 4 — REVISE after selected-Mac attempt 1

Observed live failure:

`p7_06_macos_deploy.sh: ... p7_02_macos_service.sh: Permission denied`

Material engineering/portability finding: the outer selected-Mac proof correctly invoked the P7.06 adapter through `sh`, but the adapter itself directly executed sibling P7.02/P7.05 shell files. Repository files created through the GitHub contents path had mode `0644`, so the update path depended on an executable Git mode that was neither required by the semantic contract nor reliably preserved.

Disposition:

- all P7.02/P7.05 sibling adapter calls inside P7.06 now execute explicitly through `sh`;
- no operator-side `chmod` workaround is required;
- a regression guard rejects reintroduction of direct sibling shell execution;
- backup-before-stop, R22, migration, rollback and replay-safety ordering remain unchanged.

Evidence:

- PR `#42 — P7.06 — Fix non-executable sibling shell adapters`;
- merged canonical main after remediation: `23fd438ad3c16ccb5fe3eb50de347edb82932daa`;
- GitHub `Reference Python CI` run `32121769448`, job `95663550077`: `978/978 PASS`.

The failure occurred before backup/stop/target activation, so it did not constitute a successful deployment transition or P7.06 closure.

## 6. Iteration 5 — REVISE after selected-Mac attempt 2

Observed live failure on the already-proven P7.05 source release `cf60e52c93bf0ef4158cf2c3e26792850a126c70`:

`observer release pin mismatch ... script=.../current/source/reference/python/p7_05_operational_visibility.py`

Material architecture/operations finding: P7.06 pre-update verification required the live source observer to already satisfy the R22 exact-release observer invariant. Canonical R22, however, explicitly did **not** deploy that remediation ad hoc and required the first controlled P7.06 update itself to carry the R22 hardening. The implementation therefore created an impossible handoff: P7.06 required the R22 postcondition before it could execute the update that establishes that postcondition.

Disposition:

- introduce one bounded first-upgrade compatibility bridge for the exact historically proven P7.05 source release `cf60e52c93bf0ef4158cf2c3e26792850a126c70` only;
- require the observer to be loaded;
- require the installed plist `ProgramArguments` to match the exact historical P7.05 shape: exact source-release Python, the known historical mutable-`current` script path, exact runtime root and observer command arguments;
- require the historical observer implementation to report healthy operational status;
- every different source release, missing observer, different plist shape or other mismatch remains fail-closed;
- after successful target activation, the R22 exact-release observer invariant is mandatory;
- rollback restores the exact source runtime but does not blindly restore the known unsafe legacy observer plist; the observer is regenerated through the current P7.05 semantic owner and must pass exact-release verification on the restored source release.

This is a one-release R22 handoff bridge, not a general mixed-version exception or downgrade of exact-version semantics. No schema migration, canonical mutation, external effect or Product Contract/capability lifecycle change is admitted by it.

The failure occurred during pre-update source verification, before backup/stop/target activation, so the selected Mac remained on the prior P7.05 runtime state.

## 7. Iteration 6 — PASS for repository/live-readiness stage

Architecture/governance: PASS. The bounded bridge follows the explicit R22 handoff rather than overriding it, preserves a single exact historical source identity, and requires the R22 invariant after transition and rollback. It creates no new authority or stable/public deployment boundary.

Engineering: PASS. The bridge is exact-release and exact-plist-shape constrained; arbitrary legacy/mixed-version states remain rejected. Rollback no longer reintroduces the known unsafe mutable-`current` observer configuration.

Operations/recovery: PASS for live readiness. Source health is verified before mutation, backup still occurs before stop, rollback retains the exact source runtime and safe exact observer re-pin, and the selected-Mac proof still requires update, rollback, final re-update and final health.

Security/data governance: PASS. No broadened execution surface, secret handling, schema-changing migration or effect replay was introduced. Known historical behavior is only recognized sufficiently to enter the governed remediation transition.

Product/platform: PASS. The change remains owner-local, domain-neutral and independent of product business logic or hidden product state.

The remaining evidence gap after iteration 6 was execution of the complete selected-Mac proof against the merged remediation.

## 8. Iteration 7 — REVISE → PASS after selected-Mac attempt 3

Observed live sequence on canonical `main` `1a6fd740ab3398aedbbe8f30c9a56d04467cf33b`:

- bounded legacy R22 carry-forward verification passed for source `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- the adapter then failed in `backup_preupdate()` with:

`.../p7_06_macos_deploy.sh: line 175: /Users/master/Library/Application: No such file or directory`

Material engineering/portability finding: the P7.03 backup command used `output=$($py ...)`. The selected-Mac runtime Python path is under the default owner-local root `$HOME/Library/Application Support/ArvectumOS/persistent-internal`, so unquoted command-position expansion split the executable path at the space in `Application Support`. The immediately preceding P7.03 verify command already quoted the same executable correctly; the defect was isolated to the backup command substitution.

Disposition:

- execute the release Python inside command substitution as `output=$("$py" "$durable" backup ...)`;
- retain the exact source release and P7.03 release-owned backup implementation;
- add a regression guard that rejects the unquoted `output=$($py ...)` form and requires the quoted form while preserving the real default runtime root containing `Application Support`;
- no path relocation, symlink workaround, operator-side escaping, alternate Python or weakening of the owner-local runtime-root contract is introduced.

Failure position and safety disposition:

- source runtime health had already passed;
- bounded legacy observer verification had passed;
- target preparation and compatibility/migration preflight had completed;
- deployment lock and work evidence directory had been created;
- the P7.03 live-store verification command passed far enough to reach the subsequent backup invocation;
- the backup executable itself was never started because shell command resolution failed first;
- observer uninstall, runtime stop, target activation and canonical/product/external effects had not begun;
- the EXIT trap remains responsible for releasing the P7.06 single-writer lock; retained work-directory material is owner-local non-canonical operational evidence.

Post-remediation review result: PASS for repository/live-readiness scope. The quoting correction changes no authority, schema, migration, replay, product/platform or lifecycle semantics; it makes the existing governed backup-before-stop sequence executable on the actual selected-Mac default path.

Iteration 7 reaches the configured maximum functional-review iteration count. Any materially new defect discovered after this point must be recorded in a new bounded remediation/live-proof review artifact rather than extending this cross-review beyond seven iterations.

## 9. Validation

Repository validation accumulated across the review:

- Python P7.06 focused unit tests: PASS;
- macOS deploy adapter `sh -n`: PASS;
- selected-Mac proof adapter `sh -n`: PASS;
- static guard: no curl/wget/ssh/scp/nc remote transport introduced by the P7.06 macOS adapter;
- initial implementation PR `#40`: full CI `975/975 PASS`;
- executable-bit remediation PR `#42`: `Reference Python CI` run `32121769448`, job `95663550077`, `978/978 PASS`;
- bounded R22 first-upgrade bridge PR `#43`: `Reference Python CI` run `32122402442`, job `95665496605`, `980/980 PASS` on the PR merge ref before its review-note update;
- path-with-spaces remediation PR `#44`: `Reference Python CI` run `32123420416`, job `95668636686`, `981/981 PASS`; the new `test_release_python_command_substitution_is_space_safe` regression is green against the real `Application Support` default-root form.

Functional cross-review result: `PASS` after 7 iterations for repository/live-readiness scope. This is not formal Production/lifecycle approval.

## 10. Post-review live-remediation and closure evidence

Material defects discovered after the configured iteration-7 maximum were handled in the separate [`P7.06 Selected-Mac Live Remediation Review`](P7-06-live-remediation-review.md). That review preserves the original review cap and records the subsequent runtime-quiescence/rollback hardening, target-evidence preservation, bounded activation diagnostics and exact `current` symlink replacement remediation.

Repository remediation culminated in PR `#49 — P7.06 — Fix stale current release pointer after activation`, merged as canonical `main` commit `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`. The final pre-merge Reference Python CI on the reviewed PR merge ref passed `998/998` tests.

The selected Mac then completed [`P7.06 Selected-Mac Governed Deploy Proof — Attempt 8`](P7-06-selected-mac-governed-deploy-proof-attempt-8.md) with exact sequence `update → rollback → final update` and final `PASS` on target `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`.

Live closure identities:

- source release: `cf60e52c93bf0ef4158cf2c3e26792850a126c70`;
- first update transaction: `a33209268d34b25c1bb8db9c63e835bf6149a404af57f8e77952177f22c5ffb3`;
- exact rollback transaction: `589f282e3e062c1b5aa298f841f044d4d9c6227214c862d45044673a5ce9e951`;
- final update transaction: `34470ac05993465155b8048405d1dbb712ffb9387b90a29666b927fcfb9dfdc4`;
- final active target: `4df99c4c66a1b7b93a4b05d7768018b03aa4041b`;
- selected-Mac proof attestation SHA-256: `3dec1d1dd34aff960753105e72aa60739c01fb61c0af091a554e93f344418e69`.

No schema-changing migration, canonical mutation by deployment, product/external effect replay or durable backup restore occurred.

Closure disposition: repository/live-readiness review `PASS`; live selected-Mac closure `PASS`; no material objection remains for the declared `Persistent Internal / owner-operated` P7.06 scope.

No Production, `Active` capability, Stable Product Contract, SLA/support, public/stable deployment interface or broader conformance claim follows from this review.