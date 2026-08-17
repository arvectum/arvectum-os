# P7.03 — Durable State Implementation Cross-Review

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Reviewed scope: `P7.03 — Durable governed state/checkpoint persistence + backup/restore baseline`
Implementation: [`P7.03 Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline`](../implementation/P7-03-DURABLE-GOVERNED-STATE-BACKUP-RESTORE.md)
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Selected-Mac closure evidence: [`P7.03 Selected Mac mini Proof Attempt 3`](P7-03-selected-mac-proof-attempt-3.md) — `Complete / PASS`

## 1. Purpose

This functional cross-review evaluates the P7.03 repository implementation and selected-Mac closure evidence from architecture, engineering, operations, security/privacy and governance perspectives.

It is not R23, not an ADR acceptance, not a Platform Capability lifecycle transition and not a production-readiness approval.

## 2. Authority baseline checked

Checked:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0`;
- P7.01 baseline `1.0.1`;
- P7.02 `Complete / PASS`;
- canonical Phase 7 roadmap;
- canonical roadmap;
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

### Iteration 4 — repository-side cross-review

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

No material repository-side objection remained.

### Iteration 5 — selected-Mac evidence-contract and lifecycle review

Result: `REVISE`.

Attempt 1 reported an internally inconsistent combination:

```text
status = PASS
persistent_runtime_state = stopped
```

The canonical core proof required `healthy` when persistent runtime enforcement was requested, so Attempt 1 could not be accepted as closure evidence even though its backup/restore observations were useful within their demonstrated scope.

Disposition:

- preserve Attempt 1 as rejected closure evidence rather than discard it;
- add a dedicated selected-Mac wrapper that independently requires `healthy` before and after the core proof;
- force `require_persistent_runtime=True` internally;
- reject inconsistent core `PASS + non-healthy` summaries;
- require unchanged P7.02 runtime release before/after;
- emit explicit `required_runtime_enforced=true` attestation;
- add regression coverage for healthy, stopped and inconsistent-summary paths.

PR `#31` merged the hardening and full Reference Python CI passed `935/935` tests.

The first hardened re-proof, preserved as Attempt 2, then correctly failed closed because P7.02 was actually `stopped`. This was an operational lifecycle blocker, not a persistence-integrity regression. The existing P7.02 lifecycle `start` action was then explicitly human owner/operator-authorized without install, upgrade, migration or release change.

Result after revision: the selected-Mac proof contract now fails closed on an unhealthy lifecycle precondition and does not allow operator wording to substitute for machine-checked runtime health.

### Iteration 6 — final selected-Mac operational evidence review

Result: `PASS`.

Attempt 3 executed the hardened wrapper from clean exact canonical tool release:

`e20b7801cf389b1afe7f513182d352a566809c55`

against the existing P7.02 runtime release:

`73af746f83271b14670fe22db658dfd55cacb291`.

Observed closure evidence:

- `status=PASS`;
- `required_runtime_enforced=true`;
- runtime state before = `healthy`;
- runtime state after = `healthy`;
- P7.02 runtime release unchanged before/after;
- live restore integrity `PASS`;
- live state digest equals restored state digest `true`;
- fixture backup and restore integrity `PASS`;
- deliberate tamper detection fail-closed `true`;
- explicit exclusions absent `true`;
- reusable secrets / telemetry / cache absent;
- checkpoint canonical authority `false`;
- proof fixture canonical authority `false`;
- external-effect replay authorized `false`;
- source checkout clean after proof.

Architecture review:

- successful persistence/backup proof does not promote the filesystem/tar mechanism into stable architecture;
- storage locators remain distinct from RFC identities;
- no permanent database/object-store/backup topology is selected.

Security/privacy review:

- backup minimization boundary remained intact;
- no reusable secrets, telemetry or cache entered the backup;
- proof fixture remained non-authoritative.

Operations review:

- P7.02 service recovery used the existing lifecycle action and preserved exact runtime release;
- hardened runtime-health checks were satisfied both before and after proof;
- restore remained isolated and replay-safe.

Governance review:

- no Product Contract or Platform Capability lifecycle promotion occurs;
- no external/customer Production, SLA/support or compatibility claim occurs;
- no ADR trigger is crossed by the bounded reversible implementation;
- no historical external effect replay is authorized.

No material objection remains.

Functional review iterations completed: `6 of maximum 7`.

## 4. Validation evidence

Repository and CI evidence:

- initial P7.03 focused unit tests: `12/12 PASS`;
- standalone `py_compile`: PASS;
- repository implementation PR `#30` merged at `e2440b6f8afc7e0f21b20d370047bfa3ac803017`;
- full Reference Python CI after implementation: `932/932 PASS`;
- proof-contract hardening PR `#31` merged at `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`;
- full Reference Python CI after hardening: `935/935 PASS`.

Operational evidence:

- [`Attempt 1`](P7-03-selected-mac-proof-attempt-1.md) — rejected as closure evidence; useful scoped backup/restore observations retained;
- [`Attempt 2`](P7-03-selected-mac-proof-attempt-2.md) — correct hardened fail-closed result while P7.02 runtime was stopped;
- [`Attempt 3`](P7-03-selected-mac-proof-attempt-3.md) — `Complete / PASS` after owner-authorized ordinary P7.02 lifecycle recovery.

Attempt 3 selected-Mac local evidence includes:

- attestation `p7-03-selected-mac-attestation-20260817T192924Z-9fa8f43b.json`;
- core summary `p7-03-summary-20260817T192924Z-a4d188c7.json`;
- live backup `p7-03-backup-20260817T192924Z-a8b80b0fe41809da.tar.gz`;
- live backup SHA-256 `6b2661050a2d777c9cae0bada8c584c2e426489156505dc30e6ce5756de97765`.

## 5. Known bounded deferrals

Intentionally deferred:

- persistent workload/service identity and secret lifecycle — P7.04;
- broader telemetry/log retention and alerting — P7.05;
- generalized deployment/update/rollback/state migration — P7.06;
- persistent Tender Operator state reliance — P7.07;
- persistent Discount Parser cross-host reliance — P7.08;
- incident/recovery drills — P7.09;
- off-host/clean-environment host-loss restore and portability — P7.10;
- lifecycle/conformance/stable-boundary disposition — P7.11.

These are not defects in the bounded P7.03 implementation and must not be represented as already proven.

## 6. Final review result

`P7.03 functional cross-review = Complete / PASS after 6 iterations.`

All material objections within the declared P7.03 scope are resolved. Canonical selected-Mac evidence and roadmap synchronization complete the closure package.

This review does not constitute R23, formal production approval, ADR acceptance, Platform Capability promotion or Product Contract stabilization.
