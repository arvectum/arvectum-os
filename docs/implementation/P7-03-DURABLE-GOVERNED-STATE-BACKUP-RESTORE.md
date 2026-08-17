# P7.03 — Durable Governed State / Checkpoint Persistence and Backup / Restore Baseline

Status: `Repository implementation ready / selected-Mac proof pending`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Predecessor: [`P7.02 Persistent Mac mini Runtime`](P7-02-MAC-MINI-PERSISTENT-RUNTIME.md) — `Complete / PASS`
Cross-review: [`P7.03 Durable State Implementation Cross-Review`](../reviews/P7-03-durable-state-implementation-review.md)

## 1. Purpose

P7.03 provides the minimum durable governed-state/checkpoint and backup/restore mechanism required by the current persistent internal contour without selecting a permanent database, object store, backup product or stable serialization/storage contract.

The implementation is intentionally a bounded owner-local filesystem adapter. It preserves the semantic distinctions required by the Accepted architecture while remaining reversible and replaceable.

It does **not** authorize canonical mutation. A caller may persist bytes as canonical governed state only after the applicable Governed Execution/admission path has already authorized and produced that state. The persistence adapter is a durability mechanism, not a decision authority, validation authority or canonical-admission engine.

## 2. Authority checked

Implementation was checked against:

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

`reference/python/p7_03_durable_state.py`

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

## 10. Executable proof

The repository test suite exercises:

- state-class separation and exclusions;
- canonical metadata boundaries;
- historical source-release attribution;
- secret-declared payload refusal;
- immutable governed item validation;
- non-authoritative/replay-safe checkpoints;
- minimized backup contents;
- backup checksum verification;
- isolated restore;
- restore target protection;
- path traversal rejection;
- tamper detection and fail-closed behavior;
- empty-live-store backup/restore;
- synthetic non-authoritative checkpoint proof without live canonical pollution;
- exact persistent-runtime release observation when present;
- required-runtime failure when health is absent/unhealthy;
- backup output confinement to the owner-local backup directory.

### Selected Mac mini proof

Repository/CI validation is not a substitute for the selected-Mac proof. After this implementation is merged to canonical `main`, run from a clean canonical checkout:

```sh
REPO=/Users/master/workspace/arvectum-os
RUNTIME_ROOT="$HOME/Library/Application Support/ArvectumOS/persistent-internal"

cd "$REPO"
git fetch origin
git switch main
git pull --ff-only origin main
TEST_SHA=$(git rev-parse HEAD)

test "$(git status --porcelain)" = ""

python3 reference/python/p7_03_durable_state.py prove \
  --runtime-root "$RUNTIME_ROOT" \
  --release-sha "$TEST_SHA" \
  --require-persistent-runtime \
  --json
```

The proof intentionally does **not** update the P7.02 running service release. P7.06 owns the generalized governed update/rollback/migration path. P7.03 only observes and records the exact running release exposed by existing P7.02 health.

A successful selected-Mac proof must show at least:

- `status=PASS`;
- persistent runtime observed and `state=healthy`;
- exact persistent-runtime release recorded;
- live backup integrity PASS;
- isolated live restore integrity PASS;
- live state digest equals restored state digest;
- non-authoritative fixture checkpoint backup/restore PASS;
- tamper detection fail-closed PASS;
- explicit exclusions absent from backup;
- reusable secrets / telemetry / cache absent;
- no external effect replay authorization;
- no proof-fixture canonical authority.

The live store may legitimately contain zero governed items before P7.07/P7.08 begin persistent product reliance. The selected proof therefore verifies the actual live state as-is and uses a separate ephemeral non-authoritative fixture store to prove the non-empty checkpoint/backup/restore mechanics without fabricating or promoting canonical state.

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

## 12. Closure rule

P7.03 may be closed as `Complete / PASS` only when all of the following are true:

1. repository implementation and tests are merged to canonical `main`;
2. Reference Python CI is PASS;
3. selected Mac mini runs the exact merged implementation against the existing persistent-internal runtime root;
4. selected-Mac minimized proof evidence is canonically recorded;
5. functional cross-review has no remaining material objection;
6. canonical roadmap and Phase 7 roadmap are synchronized to P7.03 closure.

Until the selected-Mac proof is recorded, P7.03 remains open and P7.04 must not be represented as the current canonical action.
