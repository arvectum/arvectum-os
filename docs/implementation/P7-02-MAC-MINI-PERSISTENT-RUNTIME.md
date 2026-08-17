# P7.02 — Persistent Mac mini Runtime and Service Lifecycle

Status: `Implementation prepared / selected-Mac proof required`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)

## 1. Purpose

P7.02 turns the already validated owner-operated Mac mini contour into a supervised persistent internal runtime without selecting a permanent service/deployment architecture or creating a public service boundary.

This implementation is deliberately an environment-specific reversible adapter:

- the running version is pinned to an exact canonical `arvectum/arvectum-os` Git commit;
- the runtime source snapshot is produced with `git archive` and lives outside the mutable checkout;
- the runtime uses an isolated stdlib-only Python venv;
- an owner `launchd` LaunchAgent starts the process at login and restarts it after unsuccessful exit;
- health is a secret-safe local JSON heartbeat classified as non-canonical telemetry;
- the process opens no network listener and performs no product/external consequential effect;
- service removal does not delete releases, configuration, secrets or evidence.

`launchd`, the filesystem layout, the health JSON schema and this process envelope are not stable platform contracts, public APIs, supported macOS promises or Product Contract surfaces.

## 2. Authority checked

Implementation was designed against:

- Constitution `1.2.0` — `Ratified`, frozen;
- RFC-0001 through RFC-0008 — `Accepted 1.0.0` per the canonical RFC Index;
- RFC-0001 platform/operational-readiness and stable-boundary rules;
- RFC-0003 security, authority, least-privilege, secret and portability invariants;
- RFC-0006 telemetry non-authority, provenance and replay-safety invariants;
- P7.01 baseline `1.0.1`;
- R21 — `PASS`.

No Accepted ADR selects a service/deployment topology. R21 explicitly records that an ADR is not required for a reversible environment-specific `launchd` adapter. If this adapter later becomes a materially constraining cross-product or externally relied-upon deployment/service boundary, the ADR/stable-boundary gate must be revisited before further reliance.

## 3. Implementation components

### 3.1 Persistent runtime envelope

`reference/python/p7_02_persistent_runtime.py`

Responsibilities:

1. require a full 40-character Git release SHA;
2. acquire a single-process owner lock;
3. import the existing domain-neutral reference-runtime semantic modules as a startup self-check;
4. write atomic owner-only `run/health.json` telemetry;
5. maintain heartbeat/generation/process-instance evidence;
6. fail health checks when the process is stopped/stale or the release pin differs;
7. expose no network listener;
8. perform no product effect and no canonical mutation.

The health document explicitly declares itself `non-canonical operational telemetry`. It must not be used as a competing source of organizational truth.

### 3.2 macOS lifecycle adapter

`reference/python/p7_02_macos_service.sh`

Commands:

- `install` — verify canonical clean `main`, fast-forward to `origin/main`, create exact runtime release, create isolated venv, generate/install owner LaunchAgent, start and verify health;
- `start` — load/start the LaunchAgent;
- `stop` — unload/stop it;
- `restart` — replace the supervised process;
- `status` — verify launchd state plus fresh exact-release health;
- `crash-proof` — `SIGKILL` the process and prove launchd replacement, health-generation advance and no process-owned network socket;
- `prove` — exercise stop/start/restart/crash recovery, LaunchAgent controls, listener boundary and source-checkout cleanliness;
- `remove` — unload and remove only the service adapter while retaining runtime releases/config/secrets/evidence.

### 3.3 LaunchAgent behavior

Service label:

`com.arvectum.os.persistent-internal`

Selected lifecycle:

- owner LaunchAgent, not root LaunchDaemon;
- `RunAtLoad=true` — start in the owner login lifecycle;
- `KeepAlive.SuccessfulExit=false` — unsuccessful/crash exit is supervised;
- `ThrottleInterval=5` — bounded rapid restart pressure;
- no TCP/UDP listener;
- stdout/stderr remain local operational telemetry.

This is proportionate to the current owner-operated model. P7.04 may later strengthen service/workload identity and access handling without changing the architectural meaning of P7.02.

## 4. Runtime/source/config separation

Default owner-local runtime root:

`~/Library/Application Support/ArvectumOS/persistent-internal`

The root is outside the repository checkout and contains distinct subtrees:

```text
releases/<exact-git-sha>/   immutable git-archive source snapshot + manifest
venvs/<exact-git-sha>/      isolated stdlib-only interpreter environment
current                     symlink to selected exact release
run/                        lock + non-canonical health telemetry
logs/                       launchd stdout/stderr telemetry
config/                     owner-local non-secret runtime configuration
secrets/                    reserved owner-only secret location; P7.02 requires none
evidence/                   selected-Mac local lifecycle proof
service/                    generated launchd adapter copy
```

The LaunchAgent itself is installed at:

`~/Library/LaunchAgents/com.arvectum.os.persistent-internal.plist`

P7.02 does not read or migrate P6 product/EIS secrets and does not establish a shared secret-store architecture. `reusable_secrets_required_for_p7_02=false` is recorded in local configuration/evidence.

## 5. Selected-Mac execution

P7.02 is not complete merely because the repository implementation exists. The selected owner-operated Mac mini must execute the canonical merged implementation.

From the clean canonical checkout:

```sh
git fetch origin main
git merge --ff-only origin/main
sh reference/python/p7_02_macos_service.sh install
sh reference/python/p7_02_macos_service.sh prove
```

The script fails closed when the checkout is not canonical `arvectum/arvectum-os`, is not clean `main`, cannot fast-forward exactly to `origin/main`, the runtime root falls inside the checkout, required macOS commands are unavailable, health does not become current, restart does not replace the process, or network sockets are observed on the runtime process.

## 6. Required PASS evidence

Selected-Mac proof must demonstrate:

- exact `release_sha` equal to canonical merged `main` at installation;
- runtime release outside the source checkout;
- clean source checkout after lifecycle proof;
- owner LaunchAgent installed with `0600` permissions;
- `RunAtLoad=true`;
- failed/crashed process supervision with bounded launchd throttle;
- predictable explicit stop/start/restart;
- fresh exact-release health indication;
- `SIGKILL` crash followed by a different replacement PID and increased health generation;
- no TCP/UDP listener owned by the runtime process;
- no product/external consequential effect replay;
- no canonical-state mutation by the runtime envelope;
- reusable P7.02 secrets absent and any future secrets/config kept outside Git;
- clean service removal path available.

Local evidence is written under the runtime root, including:

- `evidence/p7-02-crash-<timestamp>.json`;
- `evidence/p7-02-summary-<timestamp>.txt`.

Raw local paths, raw personal identity values and reusable credentials need not be published in the public repository merely to prove the controls. Canonical closure evidence should record the exact release SHA, relevant result fields and minimized attributable execution context.

## 7. Failure and replay boundary

The P7.02 runtime envelope performs no product effect itself.

Supervision or restart must not be interpreted as authorization to replay a historical consequential external action. Future product reliance remains constrained by its exact Product Contract and Governed Execution semantics. Uncertain external outcomes remain reconciliation/new-authorization problems rather than daemon retry problems.

## 8. Removal / rollback

To disable the environment-specific service adapter:

```sh
sh reference/python/p7_02_macos_service.sh remove
```

Removal:

- unloads the LaunchAgent;
- removes the installed plist and generated service copy;
- intentionally retains release snapshots, local configuration, secret directory and evidence.

Destructive cleanup is not automated by P7.02. Later governed persistence/backup work must not be bypassed by a convenience purge command.

Reinstallation from canonical Git reconstructs the service adapter without relying on the mutable source checkout as runtime state.

## 9. Scope and non-claims

P7.02 does not establish:

- external/customer Production;
- SLA/SLO/support commitments;
- a supported macOS platform matrix;
- `Active` status for any Platform Capability;
- `Stable` status for a Product Contract;
- a public API/SDK/service wire contract;
- persistent product operational proof for Tender Operator or Discount Parser;
- durable canonical/checkpoint persistence or backup/restore (P7.03);
- final persistent IAM/service identity model (P7.04);
- full observability/alerting/retention baseline (P7.05);
- a governed general deployment/update/migration contract (P7.06).

## 10. Closure rule

Repository CI and review can prove implementation correctness and portability of the bounded adapter logic, but they cannot substitute for selected-Mac lifecycle evidence.

P7.02 may be marked `Complete / PASS` only after:

1. the implementation is merged to canonical `main`;
2. the selected Mac mini runs `install` and `prove` against that exact merged release;
3. local evidence is reviewed and minimized canonical closure evidence is recorded;
4. no material objection remains after functional cross-review;
5. the canonical roadmap is synchronized.

Until then, P7.02 remains the current canonical action.
