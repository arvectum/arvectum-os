# P7.03 — Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor: [`P7.02 Persistent Mac mini Runtime`](P7-02-MAC-MINI-PERSISTENT-RUNTIME.md) — `Complete / PASS`
Cross-review: [`P7.03 Durable State Implementation Cross-Review`](../reviews/P7-03-durable-state-implementation-review.md) — `Complete / PASS`
Selected-Mac closure evidence: [`P7.03 Selected Mac mini Proof Attempt 3`](../reviews/P7-03-selected-mac-proof-attempt-3.md) — `Complete / PASS`

## 1. Purpose

P7.03 provides the minimum durable governed-state/checkpoint and backup/restore mechanism required by the current persistent internal contour without selecting a permanent database, object store, backup product or stable serialization/storage contract.

The implementation is intentionally a bounded owner-local filesystem adapter. It preserves the semantic distinctions required by the Accepted architecture while remaining reversible and replaceable.

It does **not** authorize canonical mutation. A caller may persist bytes as canonical governed state only after the applicable Governed Execution/admission path has already authorized and produced that state. The persistence adapter is a durability mechanism, not a decision authority, validation authority or canonical-admission engine.

## 2. Authority checked

Implementation and closure were checked against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` per the canonical RFC Index;
- RFC-0002 immutable Canonical Record / Execution Context semantics and physical-storage independence;
- RFC-0003 Organization scope, least privilege, minimization, retention/deletion, secret and portability rules;
- RFC-0005 immutable governance-significant execution transitions, exact version attribution, failure/uncertainty and semantic portability;
- RFC-0006 append-only canonical evidence, checkpoint/replay boundaries, non-canonical telemetry and integrity-claim limits;
- RFC-0007 persistence does not promote Observation/derived state into Knowledge;
- RFC-0008 governed checkpoints, content-integrity limits, manifest-based export and reversible simple storage;
- P7.01 baseline `1.0.1`;
- P7.02 persistent runtime closure evidence.

No Accepted ADR selects persistence, database, object-store or backup topology.

### ADR disposition

`ADR required now: NO`.

The selected filesystem/tar adapter is:

- owner-local;
- private to the current persistent internal contour;
- stdlib-only;
- explicitly `bounded-internal-provisional`;
- not a Product Contract surface;
- not a public/stable wire or storage format;
- replaceable without changing RFC identities or governed organizational semantics.

The ADR/stable-boundary gate must be revisited before further reliance if this storage representation becomes materially constraining, cross-product, externally relied upon or expensive to migrate.

## 3. Implementation

Canonical implementation:

- `reference/python/p7_03_durable_state.py` — durable state, checkpoint, backup, verification and isolated restore mechanism;
- `reference/python/p7_03_selected_mac_proof.py` — hardened selected-Mac closure wrapper that enforces healthy P7.02 runtime before and after proof.

Default runtime root inherited from P7.02:

`~/Library/Application Support/ArvectumOS/persistent-internal`

P7.03 adds the following owner-only subtrees:

```text
state/
  governed/items/<storage_item_id>/
    manifest.json
    payload.bin
  checkpoints/<checkpoint_id>.json
config/
  p7-03-recovery.json
backups/
  p7-03-backup-*.tar.gz
  p7-03-backup-*.tar.gz.sha256
evidence/
  p7-03-summary-*.json
  p7-03-selected-mac-attestation-*.json
```

The adapter preserves but does not back up the P7.02/non-governed paths:

```text
run/      non-canonical runtime telemetry
logs/     non-canonical operational logs
cache/    replaceable derived/cache state
secrets/  reusable owner-local secrets
```

## 4. State classes and authority boundary

### 4.1 Canonical governed state

A persisted canonical governed item requires explicit semantic metadata including:

- `state_class=canonical-governed-state`;
- Organization scope;
- semantic type and schema version;
- exact canonical `subject_identity` and `version_identity`;
- authority mode and scope;
- governed admission reference;
- provenance references;
- classification and retention-policy reference;
- exact source/release SHA used to interpret/produce the state;
- `canonical_authority=true`;
- `contains_reusable_secret=false`.

P7.03 does not invent or replace any of those canonical identities. The directory `storage_item_id` is only an internal content-addressed storage locator. It is explicitly **not** an RFC-0002 Subject Identity or Version Identity.

`Native`, `External Reference` and `Governed Replica` authority modes remain the only admitted authority modes. Persistence does not convert external authority into Native authority.

### 4.2 Governance-significant checkpoint state

A checkpoint is immutable recovery metadata that pins:

- exact Execution Subject Identity;
- exact Execution Version Identity;
- exact governed storage-item references required by that recovery position;
- classification and retention-policy reference;
- tool release SHA;
- reason and creation time.

Every checkpoint declares:

- `canonical_authority=false`;
- `external_effect_replay_authorized=false`.

The checkpoint therefore does not compete with canonical Execution Context history and cannot authorize replay of a historical external effect. It is a recovery pointer to exact governed state, not a mutable workflow truth store.

### 4.3 Owner-local recovery configuration

`config/p7-03-recovery.json` is non-secret owner-local recovery metadata. It records:

- exact P7.03 tool release SHA;
- observed exact P7.02 persistent-runtime release SHA when local health is available;
- store schema/status;
- backup scope and explicit exclusions;
- non-canonical telemetry/checkpoint semantics;
- secret re-provisioning rule;
- current retention/deletion boundary.

Reusable credentials are never copied into this file.

## 5. Atomicity and integrity

Within the current single-owner contour:

- durable files are written to same-directory temporary files;
- file contents are flushed and `fsync`ed before publication;
- publication uses atomic `os.replace`;
- containing directories are `fsync`ed where supported;
- state directories are owner-only (`0700`) and state files owner-only (`0600`) on POSIX;
- symlinks are rejected inside governed persistence and backup scope;
- immutable item/checkpoint collisions fail closed;
- live-store verification recursively validates persisted item/checkpoint references and hashes.

This is proportionate to the current owner-operated single-host contour. It is not a distributed transaction or multi-writer consistency claim.

## 6. Backup baseline

A backup contains only:

- `state/governed/**`;
- `state/checkpoints/**`;
- `config/p7-03-recovery.json`.

It explicitly excludes:

- `run/**`;
- `logs/**`;
- `cache/**`;
- `secrets/**`.

The archive is a private internal `.tar.gz` implementation detail, not a stable archival/public interchange format.

Each backup contains an internal manifest with the exact included paths, byte sizes and SHA-256 digests. A separate sidecar SHA-256 covers the archive bytes.

Hash semantics are intentionally limited: these checks prove byte/archive integrity only. They do not establish truth, Organizational Authority, approval, legal validity, provenance rights or canonical admission.

P7.03 writes backup packages only inside the owner-local runtime `backups/` directory. Selection of a second storage medium, remote backup product, replication topology, RPO or RTO is intentionally deferred; P7.10 will later prove host-loss portability on a clean secondary environment.

## 7. Restore baseline

Restore is fail-closed and isolated:

1. verify archive sidecar SHA-256;
2. verify manifest schema, Organization scope, explicit exclusions and per-file hashes;
3. reject duplicate, absolute, traversal, backslash-traversal, symlink, hardlink, device and non-regular archive members;
4. require a target path that does not already exist;
5. restore into a private unique staging directory;
6. reconstruct required empty layout directories where the source backup legitimately contains zero governed items/checkpoints;
7. verify the restored durable store before publication;
8. atomically rename staging to the requested isolated target;
9. preserve the backup manifest as non-canonical restore evidence.

No restore command overwrites live state and no restore action replays a product/external effect.

## 8. Failure behavior

The mechanism fails closed when:

- required state/config is missing;
- a persisted payload/checkpoint hash or reference is inconsistent;
- owner-only permission or symlink boundary is violated;
- backup checksum/manifest/member integrity fails;
- backup contains an excluded or unsafe path;
- restore target already exists;
- selected-Mac proof requires persistent runtime health but P7.02 health is absent or not healthy.

Attempt 2 exercised the last boundary operationally: the hardened wrapper refused closure while P7.02 reported `stopped`. The owner/operator then used the existing P7.02 `start` lifecycle operation, preserving the same exact runtime release, before Attempt 3.

Consequential processing whose correctness depends on invalid/unavailable governed state must not continue as if the state were valid. P7.03 itself performs no consequential product operation; downstream consumers remain responsible for applying the existing Governed Execution failure/pause/reconciliation semantics.

## 9. Retention, deletion and minimization

P7.03 deliberately does not select a universal retention period, RPO or RTO.

Current baseline:

- canonical history is never deleted by telemetry rotation, cache cleanup or backup creation;
- backup rotation/deletion is not automatic;
- ordinary telemetry/cache are excluded from governed backups;
- reusable secrets are excluded and must be re-provisioned separately when required;
- synthetic proof state is ephemeral and removed after proof;
- deletion/minimization that reduces reconstructability must be represented truthfully by later policy/runbook work.

Broader telemetry retention belongs to P7.05. Incident/recovery procedures belong to P7.09. Clean-host portability belongs to P7.10.

## 10. Executable validation and selected-Mac proof

Repository validation included:

- P7.03 focused tests `12/12 PASS` before publication;
- repository implementation PR `#30`, merged at `e2440b6f8afc7e0f21b20d370047bfa3ac803017`;
- full Reference Python CI after repository publication: `932/932 PASS`;
- proof-contract hardening PR `#31`, merged at `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`;
- full Reference Python CI after hardening: `935/935 PASS`, including healthy, stopped and inconsistent-core-summary proof paths.

### 10.1 Attempt 1 — rejected closure evidence

[`P7.03 Selected Mac mini Proof Attempt 1`](../reviews/P7-03-selected-mac-proof-attempt-1.md) preserved useful backup/restore observations but was rejected for closure because the reported combination `status=PASS` and `persistent_runtime_state=stopped` could not satisfy the canonical required-runtime contract.

This triggered the dedicated hardened wrapper in PR `#31`.

### 10.2 Attempt 2 — correct fail-closed lifecycle blocker

[`P7.03 Selected Mac mini Proof Attempt 2`](../reviews/P7-03-selected-mac-proof-attempt-2.md) ran the hardened wrapper on clean canonical SHA `a04f6e6caa90c8f078ab1383be14f83b4f47ad3b` and correctly failed before closure proof because the P7.02 runtime was actually `stopped`.

The existing P7.02 lifecycle `start` operation was then explicitly owner/operator-authorized. It did not perform install, upgrade, migration or runtime release change.

### 10.3 Attempt 3 — Complete / PASS

[`P7.03 Selected Mac mini Proof Attempt 3`](../reviews/P7-03-selected-mac-proof-attempt-3.md) executed from clean exact canonical SHA:

`e20b7801cf389b1afe7f513182d352a566809c55`

with existing P7.02 runtime release:

`73af746f83271b14670fe22db658dfd55cacb291`.

The hardened attestation reported:

- `status=PASS`;
- `required_runtime_enforced=true`;
- runtime state before = `healthy`;
- runtime state after = `healthy`;
- exact runtime release unchanged before/after;
- live restore integrity `PASS`;
- live state digest equals restored state digest `true`;
- fixture backup integrity `PASS`;
- fixture restore integrity `PASS`;
- tamper detection fail-closed `true`;
- explicit exclusions absent `true`;
- reusable secrets in backup `false`;
- telemetry in backup `false`;
- cache in backup `false`;
- checkpoint canonical authority `false`;
- proof fixture canonical authority `false`;
- external-effect replay authorized `false`.

Selected-Mac local evidence:

- attestation: `p7-03-selected-mac-attestation-20260817T192924Z-9fa8f43b.json`;
- core summary: `p7-03-summary-20260817T192924Z-a4d188c7.json`;
- live backup: `p7-03-backup-20260817T192924Z-a8b80b0fe41809da.tar.gz`;
- live backup SHA-256: `6b2661050a2d777c9cae0bada8c584c2e426489156505dc30e6ce5756de97765`;
- source working tree after proof: clean.

The live store may legitimately contain zero governed items before P7.07/P7.08 begin persistent product reliance. Non-empty checkpoint/backup/restore mechanics are separately proven through ephemeral non-authoritative fixture state without fabricating or promoting canonical state.

## 11. Scope and non-claims

P7.03 does not establish:

- an `Active` Platform Capability;
- a Stable Product Contract;
- external/customer Production;
- SLA/SLO/RPO/RTO/support commitments;
- permanent database/object-store/backup technology;
- public/stable persistence or backup format;
- public API/SDK;
- multi-writer/distributed durability guarantees;
- off-host disaster recovery or clean-host portability proof (P7.10);
- persistent product operational proof (P7.07/P7.08);
- generalized update/migration behavior (P7.06);
- final IAM/secret lifecycle (P7.04).

## 12. Closure result

All P7.03 closure conditions are satisfied within the declared scope:

1. repository implementation and tests are merged to canonical `main`;
2. Reference Python CI passed for the implementation and subsequent proof-contract hardening;
3. the selected Mac mini ran the hardened exact merged implementation against the existing persistent-internal runtime root;
4. minimized selected-Mac evidence is canonically recorded in Attempt 3, with Attempts 1 and 2 retained rather than hidden;
5. functional cross-review completes with no remaining material objection after iteration 6;
6. canonical roadmap and Phase 7 roadmap are synchronized as part of the closure change set.

`P7.03 = Complete / PASS` for the declared **Persistent Internal / owner-operated** scope.

The next canonical action is `P7.04 — Persistent identity/operator/service access + least-privilege operations`.
