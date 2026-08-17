# P7.02 — Persistent Mac mini Runtime and Service Lifecycle

Status: `Complete / PASS`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
Parent baseline: [`P7.01 Persistent Internal Operating Boundary`](../roadmap/P7-01-PERSISTENT-INTERNAL-OPERATING-BASELINE.md) `1.0.1`
Parent phase: [`Phase 7 — Operational / Enterprise Readiness`](../roadmap/PHASE-7-OPERATIONAL-ENTERPRISE-READINESS.md)
Selected-Mac closure evidence: [`P7.02 Selected Mac mini Proof Attempt 2`](../reviews/P7-02-selected-mac-proof-attempt-2.md) — `Complete / PASS`

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

Implementation and closure were checked against:

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
- `stop` — unload/stop it using bounded asynchronous unload polling;
- `restart` — replace the supervised process;
- `status` — verify launchd state plus fresh exact-release health;
- `crash-proof` — `SIGKILL` the process and prove launchd replacement, health-generation advance and no process-owned network socket;
- `prove` — exercise stop/start/restart/crash recovery, LaunchAgent controls, listener boundary and source-checkout cleanliness;
- `remove` — unload and remove only the service adapter while retaining runtime releases/config/secrets/evidence.

Attempt 1 exposed an asynchronous `launchd bootout` race in the original one-shot stop check. PR `#27` remediated it with bounded polling, an idempotent already-unloaded path and fail-closed timeout behavior. Reference Python CI run `35` completed `920/920 PASS` before the successful selected-Mac re-proof.

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

P7.02 required the selected owner-operated Mac mini to execute the exact canonical implementation rather than treating repository CI as a substitute for real `launchd` behavior.

Attempt 1 ran exact release `2db9d6c178d8e67a593d7ebb716f86e394862eea`, installed successfully, and then failed during explicit stop because the original adapter used a one-shot post-`bootout` check. The failure is preserved in [`P7.02 Selected Mac mini Proof Attempt 1`](../reviews/P7-02-selected-mac-proof-attempt-1.md).

After PR `#27` remediation and roadmap/evidence synchronization, Attempt 2 ran exact canonical release:

`73af746f83271b14670fe22db658dfd55cacb291`

The selected Mac reported:

- canonical repository `arvectum/arvectum-os`;
- clean branch `main`;
- `HEAD == origin/main == 73af746f83271b14670fe22db658dfd55cacb291`;
- `install = PASS`;
- `prove = PASS`;
- final `status = PASS`;
- service remained loaded after proof.

## 6. Required PASS evidence and result

All P7.02 selected-Mac evidence obligations are satisfied for the declared scope:

- exact release SHA equal to canonical `main` at execution — `PASS`;
- runtime release separated from source checkout — `PASS`;
- clean source checkout after lifecycle proof — `PASS`;
- owner LaunchAgent with `0600` permissions — `PASS`;
- `RunAtLoad=true` — `PASS`;
- `KeepAlive.SuccessfulExit=false` — `PASS`;
- predictable explicit stop/start/restart — `PASS`;
- restart replaced the process PID — `PASS`;
- fresh exact-release health indication — `PASS`;
- actual `SIGKILL` followed by launchd replacement — `PASS`;
- health generation advanced `3 → 4` after crash — `PASS`;
- no TCP/UDP listener owned by the runtime process — `PASS`, none observed;
- product/external consequential effect replay — `false`;
- canonical-state mutation by the runtime envelope — `false`;
- reusable P7.02 secrets required — `false`;
- clean service removal path remains available — `PASS` by implementation/review boundary.

Final observed service state after proof:

- label `com.arvectum.os.persistent-internal`;
- state `loaded`;
- final observed PID `91885`;
- health generation `4`;
- health state PASS.

Local evidence basenames:

- `p7-02-summary-20260817T175128Z.txt`;
- `p7-02-crash-20260817T175127Z.json`.

Raw local paths, raw personal identity values and reusable credentials are intentionally not published in canonical closure evidence.

## 7. Failure and replay boundary

The P7.02 runtime envelope performs no product effect itself.

Supervision or restart must not be interpreted as authorization to replay a historical consequential external action. Future product reliance remains constrained by its exact Product Contract and Governed Execution semantics. Uncertain external outcomes remain reconciliation/new-authorization problems rather than daemon retry problems.

The successful crash proof explicitly recorded `product_effect_replay=false` and `canonical_state_written_by_runtime_envelope=false`.

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

## 10. Closure result

The P7.02 closure rule is satisfied:

1. implementation and remediation are merged to canonical `main`;
2. the selected Mac mini ran `install` and `prove` against exact canonical release `73af746f83271b14670fe22db658dfd55cacb291`;
3. minimized local evidence is canonically recorded in [`P7.02 Selected Mac mini Proof Attempt 2`](../reviews/P7-02-selected-mac-proof-attempt-2.md);
4. functional cross-review completed with no material objection after iteration 5;
5. canonical roadmap synchronization is part of the P7.02 closure change set.

`P7.02 = Complete / PASS` for the declared **Persistent Internal / owner-operated** scope.

The selected Mac mini enters regular persistent internal operation. P7.03 becomes the next canonical action and is responsible for durable governed state/checkpoint persistence plus backup/restore baseline.