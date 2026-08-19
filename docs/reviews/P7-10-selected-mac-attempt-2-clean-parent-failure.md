# P7.10 — Selected-Mac Operational Attempt 2

Status: **FAIL-CLOSED / retry required**  
Date: `2026-08-19`  
Task: `P7.10 — Portability, host-loss and restore-on-clean-environment proof`  
Scope: `Persistent Internal / owner-operated`  
Task classification: `platform`

## 1. Result

Attempt 2 did not close P7.10. The selected-Mac source, P7.03 governed store, handoff creation, off-host transfer and transferred-package verification all passed. The clean-secondary restore stopped before target publication because the chosen restore target was directly under a macOS home directory whose mode was `0750`.

The first failure was preserved and no target, receipt, manifest, checksum, governed item or secret material was modified to obtain a passing result.

This is classified as an **operator-instruction/environment-path defect**, not governed-state loss, archive corruption, host-loss transfer failure or semantic portability failure.

## 2. Source and handoff evidence

Selected source host:

- host marker: `selected-mac-mini-Mac-mini-master.local`;
- canonical checkout: `fbab170ab337c1631b40d0d36ea58a02f6512f6e`;
- persistent root: `/Users/master/Library/Application Support/ArvectumOS/persistent-internal`;
- P7.03 integrity before handoff: `PASS`;
- governed items: `2`;
- checkpoints: `2`;
- P7.03 tool release before prepare: `bf1a3047aadf03384c9525eacd4e186a53092c11`;
- persistent runtime release recorded by P7.03 before prepare: `bf1a3047aadf03384c9525eacd4e186a53092c11`;
- observed P7.02 runtime: healthy, active release `b0c18fba...`, PID `787`, generation `62`;
- P7.05 observer: `HEALTHY`;
- P7.06: consistent, current release `b0c18fba...`, last transaction `PASS` (`bf1a304... → b0c18fba...`).

Handoff:

- prepare: `PASS`;
- verify before transfer: `PASS`;
- member count: exactly `4` regular files;
- owner-controlled off-host medium: encrypted `ArvectumSSD`, `/dev/disk4`, FileVault enabled;
- copy to off-host volume: `PASS`;
- transfer from off-host volume to secondary host: `PASS`;
- verify after transfer: `PASS` at both transferred locations;
- all four file hashes matched byte-for-byte;
- archive SHA-256: `074f2a4e84e222bd26d6ed21a829aa0dcc1c91834479345cfa652405b721bfbd`;
- P7.10 manifest SHA-256: `fe0d2c7d9460f9da4356a3a3f7419b825b8aef3a8d18123ab35fb0281db3ada9`.

The host-loss handoff boundary was therefore crossed successfully in Attempt 2. This does not by itself satisfy P7.10 because clean-secondary reconstruction still has to pass.

## 3. Clean-secondary failure

Secondary environment:

- host: `MacBook-Air-Nikita.local`;
- macOS `26.6.2`;
- architecture: `arm64`;
- Python `3.9.6`;
- canonical checkout: `fbab170ab337c1631b40d0d36ea58a02f6512f6e`;
- target absent before restore: `YES`;
- source/target host markers distinct: `YES`.

Preserved first failure:

```text
{"result": "FAIL", "error": "durable directory is not owner-only: /Users/master mode=0o750"}
```

No restore target or receipt was created.

## 4. Classification

`p7_03_durable_state.restore_backup()` requires an existing immediate `target_root.parent` to satisfy the P7.03 private-path rule. On POSIX, a durable directory with group/other permission bits fails closed. This protects the staging and atomic publication boundary of the isolated restore.

The rule applies to the **immediate restore parent**, not every filesystem ancestor. The failed instruction used a target directly under `$HOME`, making the macOS home directory itself the immediate parent. On this secondary Mac that home directory is intentionally `0750`.

The correct bounded operational response is **not** to weaken the Mac account's home-directory permissions and not to relax P7.03. Instead, create/use a dedicated operator-controlled `0700` restore parent (for example `$HOME/p7-10-proof`) and place the absent restore target underneath it.

## 5. Security and authority disposition

Attempt 2 preserved all required boundaries:

- reusable secrets transferred/restored: `NO`;
- external-effect replay: `NO`;
- Organizational Authority granted by technical recovery: `NO`;
- target overwrite: `NO`;
- synthetic governed state created to make the test pass: `NO`;
- evidence/manifests/checksums rewritten after failure: `NO`.

The owner-only restore-parent requirement remains in force because weakening it would reduce isolation and default-denial properties for the durable restore boundary.

## 6. Corrective action

Before Attempt 3:

1. keep the already transferred four-member handoff immutable and re-verify it;
2. use a dedicated existing non-symlink restore parent with POSIX mode `0700` on the clean secondary host;
3. place a fresh absent target beneath that parent;
4. restore the retained handoff using the **exact release embedded in that handoff**, `fbab170ab337c1631b40d0d36ea58a02f6512f6e`; do not relabel the retained archive with a later documentation/test-only release;
5. preserve Attempt 2 as failed evidence; do not rewrite or delete it to manufacture a single-pass narrative;
6. obtain a new `PASS` receipt only from the separate Attempt 3 restore.

The subsequent correction merge changed only P7.10 documentation, this Attempt 2 review, and regression-test coverage; it did not change `p7_10_portability_proof.py` or `p7_03_durable_state.py`. Therefore retaining the already transferred package and restoring it from an exact checkout of its own canonical release preserves stronger release identity than rebuilding or relabelling evidence solely because operator instructions were corrected later.

P7.10 remains `Current`; M7 criterion 10 remains unsatisfied; R23 remains downstream until clean-secondary restore and final closure review pass.
