# P7.03 — Selected Mac mini Proof Attempt 1

Status: `Rejected as closure evidence / proof-contract inconsistency`
Date: `2026-08-17`
Owner: `ООО «Арвектум»`
Task classification: `platform`
Operating classification: `Persistent Internal / owner-operated`
P7.03 implementation release tested: `e2440b6f8afc7e0f21b20d370047bfa3ac803017`
Observed P7.02 runtime release: `73af746f83271b14670fe22db658dfd55cacb291`

## 1. Purpose

This artifact preserves the first selected-Mac P7.03 operational proof output exactly at the level needed for governance and engineering review. It is retained because the reported result contained an internal contradiction and therefore must not be silently discarded or represented as successful P7.03 closure evidence.

The attempt demonstrated working backup/restore and integrity mechanics, but it did **not** satisfy the selected-Mac runtime-health closure condition.

## 2. Reported operational result

The operator reported:

- final shell result: `RESULT: PASS`;
- canonical checkout release: `e2440b6f8afc7e0f21b20d370047bfa3ac803017`;
- working tree clean: `YES`;
- P7.03 proof summary `status=PASS`;
- persistent runtime observed: `true`;
- persistent runtime release: `73af746f83271b14670fe22db658dfd55cacb291`;
- persistent runtime state reported by the proof summary: **`stopped`**;
- live store integrity before backup: `PASS`;
- live governed items: `0`;
- live checkpoints: `0`;
- live restore integrity: `PASS`;
- live state digest matched restored state: `true`;
- fixture backup integrity: `PASS`;
- fixture restore integrity: `PASS`;
- deliberate tamper detection: fail-closed `true`;
- explicit excluded paths absent: `true`;
- reusable secrets in backup: `false`;
- telemetry in backup: `false`;
- cache in backup: `false`;
- checkpoint canonical authority: `false`;
- historical/external effect replay authorized: `false`;
- proof fixture canonical authority: `false`.

The live backup was reported as:

- basename: `p7-03-backup-20260817T184717Z-abc6e2894a44c9db.tar.gz`;
- SHA-256: `da98133b26d9e2ba25f48bf73ecb3e191428315724d08eb4bbfa862d525477d0`.

The local proof summary basename was reported as:

- `p7-03-summary-20260817T184717Z-ded97a96.json`.

The separate live `verify` command reported durable-store integrity `PASS`, zero governed items/checkpoints, tool release `e2440b6f...`, and observed persistent-runtime release `73af746f...`.

The separate `verify-backup` command reported:

- archive SHA-256 equal to the reported live backup SHA-256;
- `integrity=PASS`;
- exactly one included file in the empty-live-store backup;
- explicit exclusions `run/`, `logs/`, `cache/`, `secrets/`;
- reusable secrets included: `false`.

## 3. Blocking inconsistency

The canonical P7.03 implementation at release `e2440b6f8afc7e0f21b20d370047bfa3ac803017` defines the selected-Mac proof condition as follows:

- `--require-persistent-runtime` requires an observable P7.02 runtime health record;
- the observed runtime state must equal exactly `healthy`;
- any other state, including `stopped`, raises `IntegrityError` and the CLI exits non-zero.

The canonical implementation document likewise states that a successful selected-Mac proof must show the persistent runtime observed with `state=healthy`.

Therefore a result combining:

```text
status = PASS
persistent_runtime_state = stopped
```

cannot be accepted as evidence that the required selected-Mac proof contract was actually satisfied.

This is an evidence/proof-contract problem, not evidence that backup/restore itself failed.

## 4. Disposition

Attempt 1 is classified:

`REJECTED AS P7.03 CLOSURE EVIDENCE`.

The useful engineering observations remain valid only within their demonstrated scope:

- the reported live backup verified;
- isolated restore verified;
- state digest equality verified;
- fixture checkpoint/backup/restore mechanics verified;
- deliberate corruption failed closed;
- excluded telemetry/cache/secrets were absent;
- no authority or replay promotion was reported.

The attempt does **not** prove that P7.03 ran while the required persistent runtime was healthy.

No roadmap advancement to P7.04 is permitted from Attempt 1.

## 5. Remediation

PR `#31` hardens the selected-Mac proof contract by adding a dedicated wrapper that:

1. requires observed P7.02 state `healthy` before the core proof;
2. calls the core proof with `require_persistent_runtime=True` internally rather than relying on an operator-provided flag;
3. requires observed P7.02 state `healthy` again after the core proof;
4. rejects a core `PASS` summary if its runtime state is not `healthy`;
5. requires the observed P7.02 release to remain unchanged across the proof;
6. emits explicit local non-canonical attestation field `required_runtime_enforced=true`.

Regression coverage explicitly includes rejection of both a stopped runtime and a fabricated/inconsistent `PASS + stopped` core summary.

PR `#31` passed the full Reference Python CI suite: `935/935 PASS` and was merged to canonical `main` as `5d33f874beb38f773ecf816ecd6d35e5fcb26c97`.

## 6. Required next evidence

P7.03 remains current and open.

A new selected-Mac proof must execute the dedicated hardened wrapper from exact canonical `main` release `5d33f874beb38f773ecf816ecd6d35e5fcb26c97` or a later explicitly reviewed canonical release if `main` advances before execution.

Closure requires a resulting attestation with at least:

- `status=PASS`;
- `required_runtime_enforced=true`;
- persistent runtime state before = `healthy`;
- persistent runtime state after = `healthy`;
- identical exact persistent-runtime release before/after;
- live restore integrity `PASS`;
- live state digest equality `true`;
- fixture backup/restore integrity `PASS`;
- tamper detection fail-closed `true`;
- explicit exclusions absent;
- no reusable secrets/telemetry/cache in backup;
- checkpoint and proof fixture non-authoritative;
- external-effect replay not authorized.

Until that evidence is obtained and canonically recorded, `P7.03` is not `Complete / PASS`.