# P7.03 — Durable State Implementation Cross-Review

Status: `Repository review PASS / selected-Mac proof pending`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed scope: `P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline`
Implementation: [`P7.03 Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline`](../implementation/P7-03-DURABLE-GOVERNED-STATE-BACKUP-RESTORE.md)
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`

## 1. Purpose

This functional cross-review evaluates the P7.03 repository implementation from architecture, engineering, operations, security/privacy and governance perspectives before selected-Mac execution.

It is not R23, not an ADR acceptance, not a Platform Capability lifecycle transition and not a production-readiness approval.

## 2. Authority baseline checked

Checked:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- P7.01 baseline `1.0.1`;
- P7.02 `Complete / PASS`;
- canonical Phase 7 roadmap `1.2.0`;
- canonical roadmap `2.54.3` before P7.03 implementation;
- Accepted ADRs — none select persistence, database, object store or backup topology.

No higher-authority conflict was found.

## 3. Functional review iterations

### Iteration 1 — architecture / identity / authority semantics

Result: `REVISE`.

Material finding:

The first implementation draft used the generic term `item_id` for its content-addressed storage directory. Although the canonical Subject/Version Identities were separately preserved in metadata, the name could be misread as an RFC-0002 identity and become accidental coupling.

Disposition:

- rename the technical locator to `storage_item_id` / `governed_storage_item_ids`;
- explicitly declare that it is content-addressed storage identity only and never an RFC-0002 Subject Identity or Version Identity;
- keep canonical Subject/Version Identities mandatory and independent;
- ensure checkpoints pin exact Execution Subject/Version Identities rather than using the storage hash as execution identity.

Result after revision: identity/authority boundary is materially clear.

### Iteration 2 — engineering / durability / restore safety

Result: `REVISE`.

Material findings from executable proof:

1. restoring a legitimate empty live store initially failed because tar archives contain regular files but do not necessarily preserve empty state directories;
2. missing durable paths should fail as explicit integrity errors rather than leaking a raw filesystem exception;
3. archive member validation should reject backslash traversal as well as POSIX traversal for cross-platform safety;
4. restore must not silently relax/chmod an arbitrary pre-existing parent directory.

Disposition:

- reconstruct required private empty layout directories in restore staging;
- preserve the backup manifest as restore evidence rather than treating it as store content;
- make missing path validation explicit and fail-closed;
- reject backslash-containing member paths;
- require an existing restore parent to already satisfy the private-path boundary, otherwise create a new private parent;
- re-run full mechanism proof and unit tests.

Result after revision: local full-cycle proof PASS; empty and non-empty restore paths PASS.

### Iteration 3 — operations / security / minimization

Result: `REVISE`.

Material findings:

1. selected-Mac evidence must link the backup to the exact already-running P7.02 release without forcing a daemon update that belongs to P7.06;
2. an arbitrary backup output path could create accidental exposure or silently select a backup-medium topology;
3. historical governed state must be able to preserve its originating release SHA even when the persistence utility itself comes from a newer release.

Disposition:

- observe P7.02 `run/health.json` and record its exact release/state as non-secret recovery metadata when present;
- add selected-proof mode that requires observed healthy P7.02 runtime;
- do not update/redeploy the running service as part of P7.03;
- confine P7.03-created backups to the owner-local `backups/` directory;
- treat off-host medium/replication as a later operational/portability decision rather than an accidental storage commitment;
- validate each governed item's `source_release_sha` independently of the current persistence-tool release.

Result after revision: exact-version and minimization boundaries are preserved without prejudging P7.06/P7.10.

### Iteration 4 — final repository-side cross-review

Result: `PASS for repository implementation; selected-Mac proof remains required`.

Architecture:

- no physical schema is presented as RFC metamodel;
- no stable storage API/format is created;
- canonical RFC identities remain independent from storage locators;
- canonical mutation still requires existing Governed Execution/admission semantics;
- checkpoint remains non-authoritative and replay-safe;
- no Product Contract or product-domain behavior is introduced.

Engineering:

- same-directory atomic file publication;
- `fsync` before publication and directory `fsync` where supported;
- immutable item/checkpoint collision detection;
- recursive integrity verification;
- manifest + archive checksum verification;
- safe isolated staged restore;
- empty-state restore handled;
- corruption proof fails closed.

Security/privacy:

- owner-only POSIX permissions;
- secrets excluded/refused when declared reusable;
- logs/telemetry/cache excluded;
- symlink and archive traversal/link/device boundaries fail closed;
- Organization scope fixed to the current ООО «Арвектум» contour;
- no cross-Organization or secret-portability claim.

Operations:

- actual live store can be backed up without adding synthetic canonical state;
- non-empty mechanics are proven in a separate ephemeral non-authoritative fixture store;
- exact running P7.02 release can be observed and included in recovery metadata;
- backups remain local for P7.03; clean-host/off-host portability is deferred to P7.10.

Governance:

- ADR trigger re-evaluated and remains `NO` for this bounded reversible adapter;
- no lifecycle, Production, SLA, support or compatibility promotion;
- P7.03 cannot close until selected-Mac proof and canonical evidence/roadmap synchronization are complete.

No material repository-side objection remains.

Functional review iterations completed: `4 of maximum 7` so far.

## 4. Validation evidence before repository publication

Local executable validation of the candidate implementation:

- P7.03 focused unit tests: `12/12 PASS`;
- standalone `py_compile`: PASS;
- empty live-store backup/verify/isolated restore: PASS;
- non-authoritative fixture persist/checkpoint/backup/restore: PASS;
- post-restore state-tree digest equality: PASS;
- deliberate restored-payload corruption: detected / fail-closed PASS;
- explicit exclusion check (`run/`, `logs/`, `cache/`, `secrets/`): PASS;
- required-persistent-runtime negative path when health absent: PASS.

Repository CI remains required after publication/PR.

## 5. Known bounded deferrals

Intentionally deferred:

- selected-Mac operational proof and canonical evidence record — remaining P7.03 work;
- persistent workload/service identity and secret lifecycle — P7.04;
- broader telemetry/log retention and alerting — P7.05;
- generalized deployment/update/rollback/state migration — P7.06;
- persistent Tender Operator state reliance — P7.07;
- persistent Discount Parser cross-host reliance — P7.08;
- incident/recovery drills — P7.09;
- off-host/clean-environment host-loss restore and portability — P7.10;
- lifecycle/conformance/stable-boundary disposition — P7.11.

These are not defects in the bounded P7.03 repository implementation and must not be represented as already proven.

## 6. Current review result

`P7.03 repository implementation cross-review = PASS after 4 iterations.`

P7.03 itself remains open pending:

1. canonical PR/CI merge;
2. selected Mac mini `prove --require-persistent-runtime` execution against the real persistent-internal root;
3. canonical selected-Mac evidence publication;
4. final read-after-write/cross-review closure and roadmap synchronization.
