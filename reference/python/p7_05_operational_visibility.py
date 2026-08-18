#!/usr/bin/env python3
"""P7.05 bounded health, observability, audit visibility and retention controls.

This module is an owner-local operational adapter for the Phase-7 persistent
contour. It intentionally keeps operational telemetry separate from canonical
governed state:

* P7.02 ``run/health.json`` remains the liveness source.
* JSONL telemetry and alerts under ``logs/p7-05``/``run`` are non-canonical.
* audit visibility is a metadata-only projection over P7.03 governed manifests;
  payload bytes are never copied into telemetry.
* cleanup is allow-listed to diagnostic/telemetry paths and can never traverse
  ``state/`` or ``evidence/``.
* sensitive/free-form diagnostic fields are rejected rather than logged.

This is not a public observability API, monitoring topology commitment, SIEM,
knowledge store, or source of Organizational Authority.
"""
from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import shutil
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

import p7_03_durable_state as p703
import p7_04_persistent_access as p704

TELEMETRY_SCHEMA = "arvectum.p7_05.telemetry/1"
POLICY_SCHEMA = "arvectum.p7_05.retention-policy/1"
STATUS_SCHEMA = "arvectum.p7_05.operational-status/1"
ALERT_SCHEMA = "arvectum.p7_05.alert/1"
AUDIT_SCHEMA = "arvectum.p7_05.audit-visibility/1"
DEFAULT_RETENTION_HOURS = 168
DEFAULT_MAX_JSONL_BYTES = 2 * 1024 * 1024
DEFAULT_MAX_RECORDS = 5000
DEFAULT_HEALTH_MAX_AGE_SECONDS = 20.0
MAX_ATTRIBUTE_VALUE = 512
SAFE_ATTRIBUTES = frozenset({
    "component", "release_sha", "generation", "duration_ms", "correlation_id",
    "request_id", "operation", "resource", "access_path", "principal_kind",
    "allowed", "reason", "status", "code", "count", "path_class",
})
FORBIDDEN_FIELD_FRAGMENTS = (
    "secret", "token", "password", "passwd", "credential", "authorization",
    "cookie", "payload", "body", "content", "email", "phone", "identity",
    "prompt", "document", "attachment",
)
RAW_DIAGNOSTIC_NAMES = ("stdout.log", "stderr.log", "p7-05-observer.stdout.log", "p7-05-observer.stderr.log")


class P705Error(RuntimeError):
    pass


class IntegrityError(P705Error):
    pass


class BoundaryError(P705Error):
    pass


@dataclass(frozen=True, slots=True)
class HealthStatus:
    state: str
    code: str
    detail: str
    action: str
    release_sha: Optional[str]
    heartbeat_age_seconds: Optional[float]


def _utc_now_dt() -> datetime:
    return datetime.now(timezone.utc)


def _utc_now() -> str:
    return _utc_now_dt().isoformat().replace("+00:00", "Z")


def _parse_ts(value: str) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise IntegrityError("invalid UTC timestamp") from exc
    if result.tzinfo is None:
        raise IntegrityError("timestamp must be timezone-aware")
    return result.astimezone(timezone.utc)


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink() or not path.is_dir():
        raise IntegrityError(f"unsafe P7.05 directory: {path}")
    if os.name != "nt":
        os.chmod(path, 0o700)
        if stat.S_IMODE(path.stat().st_mode) & 0o077:
            raise IntegrityError(f"P7.05 directory is not owner-only: {path}")


def _atomic_json(path: Path, payload: Mapping[str, Any]) -> None:
    _private_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass


def _paths(root: Path) -> dict[str, Path]:
    root = root.expanduser().resolve()
    return {
        "root": root,
        "config": root / "config" / "p7-05-retention.json",
        "telemetry_dir": root / "logs" / "p7-05",
        "telemetry": root / "logs" / "p7-05" / "telemetry.jsonl",
        "raw_logs": root / "logs",
        "alert": root / "run" / "p7-05-alert.json",
        "health": root / "run" / "health.json",
        "governed_items": root / "state" / "governed" / "items",
    }


def initialize(root: Path) -> dict[str, Any]:
    paths = _paths(root)
    for path in (paths["root"], paths["config"].parent, paths["raw_logs"], paths["telemetry_dir"], paths["alert"].parent):
        _private_dir(path)
    if paths["config"].exists():
        return load_policy(root)
    policy = {
        "schema": POLICY_SCHEMA,
        "classification": "owner-local operational retention/minimization configuration; non-canonical",
        "raw_diagnostics_authority": "non-canonical",
        "telemetry_authority": "non-canonical",
        "retention_hours": DEFAULT_RETENTION_HOURS,
        "max_jsonl_bytes": DEFAULT_MAX_JSONL_BYTES,
        "max_records": DEFAULT_MAX_RECORDS,
        "cleanup_allowlist": [
            "logs/p7-05/telemetry.jsonl",
            "logs/stdout.log",
            "logs/stderr.log",
            "logs/p7-05-observer.stdout.log",
            "logs/p7-05-observer.stderr.log",
        ],
        "protected_prefixes": ["state/", "evidence/", "backups/", "secrets/"],
        "payload_logging": False,
        "reusable_secret_logging": False,
        "free_form_business_content_logging": False,
        "canonical_deletion_via_cleanup": False,
    }
    _atomic_json(paths["config"], policy)
    return policy


def load_policy(root: Path) -> dict[str, Any]:
    path = _paths(root)["config"]
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"P7.05 policy unreadable: {exc}") from exc
    required = {
        "schema", "classification", "raw_diagnostics_authority", "telemetry_authority",
        "retention_hours", "max_jsonl_bytes", "max_records", "cleanup_allowlist",
        "protected_prefixes", "payload_logging", "reusable_secret_logging",
        "free_form_business_content_logging", "canonical_deletion_via_cleanup",
    }
    if not isinstance(raw, dict) or set(raw) != required or raw.get("schema") != POLICY_SCHEMA:
        raise IntegrityError("P7.05 policy shape/schema invalid")
    if raw["telemetry_authority"] != "non-canonical" or raw["raw_diagnostics_authority"] != "non-canonical":
        raise IntegrityError("operational diagnostics may not claim canonical authority")
    if raw["payload_logging"] is not False or raw["reusable_secret_logging"] is not False:
        raise IntegrityError("P7.05 minimization boundary weakened")
    if raw["free_form_business_content_logging"] is not False or raw["canonical_deletion_via_cleanup"] is not False:
        raise IntegrityError("P7.05 content/deletion boundary weakened")
    if raw["cleanup_allowlist"] != [
        "logs/p7-05/telemetry.jsonl", "logs/stdout.log", "logs/stderr.log",
        "logs/p7-05-observer.stdout.log", "logs/p7-05-observer.stderr.log",
    ]:
        raise IntegrityError("cleanup allowlist is not the bounded P7.05 set")
    if raw["protected_prefixes"] != ["state/", "evidence/", "backups/", "secrets/"]:
        raise IntegrityError("protected P7.05 prefixes changed")
    for key in ("retention_hours", "max_jsonl_bytes", "max_records"):
        if not isinstance(raw[key], int) or raw[key] <= 0:
            raise IntegrityError(f"{key} must be a positive integer")
    return raw


def _validate_attributes(attributes: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(attributes, Mapping):
        raise BoundaryError("telemetry attributes must be a mapping")
    result: dict[str, Any] = {}
    for key, value in attributes.items():
        if not isinstance(key, str) or key not in SAFE_ATTRIBUTES:
            raise BoundaryError(f"telemetry attribute is not allow-listed: {key!r}")
        lowered = key.lower()
        if any(fragment in lowered for fragment in FORBIDDEN_FIELD_FRAGMENTS):
            raise BoundaryError(f"sensitive telemetry attribute rejected: {key!r}")
        if isinstance(value, bool) or value is None or isinstance(value, (int, float)):
            result[key] = value
        elif isinstance(value, str):
            if len(value) > MAX_ATTRIBUTE_VALUE or "\x00" in value:
                raise BoundaryError(f"telemetry attribute too large/unsafe: {key!r}")
            result[key] = value
        else:
            raise BoundaryError(f"telemetry attribute has unsupported type: {key!r}")
    return result


def emit_telemetry(
    root: Path,
    *,
    event: str,
    level: str = "INFO",
    attributes: Optional[Mapping[str, Any]] = None,
    recorded_at: Optional[str] = None,
) -> dict[str, Any]:
    initialize(root)
    if not isinstance(event, str) or not event or len(event) > 128 or any(ch.isspace() for ch in event):
        raise BoundaryError("event must be a compact structured event identifier")
    level = level.upper()
    if level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        raise BoundaryError("unsupported telemetry level")
    payload = {
        "schema": TELEMETRY_SCHEMA,
        "classification": "raw operational telemetry; non-canonical",
        "canonical_authority": False,
        "recorded_at": recorded_at or _utc_now(),
        "event": event,
        "level": level,
        "attributes": _validate_attributes(attributes or {}),
    }
    _parse_ts(payload["recorded_at"])
    path = _paths(root)["telemetry"]
    _private_dir(path.parent)
    line = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    fd = os.open(path, os.O_CREAT | os.O_APPEND | os.O_WRONLY, 0o600)
    try:
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)
    if os.name != "nt":
        os.chmod(path, 0o600)
    return payload


def classify_health(root: Path, *, max_age_seconds: float = DEFAULT_HEALTH_MAX_AGE_SECONDS) -> HealthStatus:
    path = _paths(root)["health"]
    if not path.exists():
        return HealthStatus("down", "HEALTH_MISSING", "P7.02 health telemetry is missing",
                            "check launchd service state and start/reinstall the persistent runtime", None, None)
    try:
        health = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return HealthStatus("down", "HEALTH_UNREADABLE", "P7.02 health telemetry is unreadable",
                            "inspect owner-local stderr diagnostics and reinstall/restart if corruption persists", None, None)
    if not isinstance(health, dict) or health.get("schema") != "arvectum.p7_02.runtime-health/1":
        return HealthStatus("down", "HEALTH_SCHEMA", "P7.02 health schema is unexpected",
                            "verify the exact installed release and runtime root", None, None)
    release = health.get("release_sha") if isinstance(health.get("release_sha"), str) else None
    if health.get("state") != "healthy":
        return HealthStatus("down", "RUNTIME_NOT_HEALTHY", f"runtime state={health.get('state')!r}",
                            "check launchd service state, then start or restart the persistent runtime", release, None)
    heartbeat_raw = health.get("heartbeat_at")
    try:
        heartbeat = _parse_ts(heartbeat_raw)
    except IntegrityError:
        return HealthStatus("down", "HEARTBEAT_INVALID", "runtime heartbeat timestamp is invalid",
                            "restart the persistent runtime and verify release integrity", release, None)
    age = (_utc_now_dt() - heartbeat).total_seconds()
    if age < -5:
        return HealthStatus("degraded", "CLOCK_SKEW", f"heartbeat is {-age:.1f}s in the future",
                            "verify system clock synchronization", release, age)
    if age > max_age_seconds:
        return HealthStatus("down", "HEARTBEAT_STALE", f"heartbeat age {age:.1f}s exceeds {max_age_seconds:.1f}s",
                            "check launchd process state and restart the persistent runtime", release, age)
    pid = health.get("pid")
    if not isinstance(pid, int) or pid <= 0:
        return HealthStatus("down", "PID_INVALID", "runtime pid is invalid",
                            "restart the persistent runtime", release, age)
    try:
        os.kill(pid, 0)
    except OSError:
        return HealthStatus("down", "PID_DEAD", f"runtime pid {pid} is not alive",
                            "check launchd restart behavior; restart service if needed", release, age)
    try:
        if (_paths(root)["root"] / "config" / "p7-04-access.json").exists():
            p704.verify_store(root)
    except p704.P704Error as exc:
        return HealthStatus("degraded", "ACCESS_REGISTRY", f"P7.04 access registry failed validation: {exc}",
                            "repair/rebootstrap persistent access before remote administration", release, age)
    return HealthStatus("healthy", "OK", "persistent runtime is healthy",
                        "no operator action required", release, age)


def _read_health_record(root: Path) -> dict[str, Any]:
    path = _paths(root)["health"]
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _resource_snapshot(root: Path) -> dict[str, Any]:
    paths = _paths(root)
    usage = shutil.disk_usage(paths["root"])
    diagnostic_bytes = 0
    for name in RAW_DIAGNOSTIC_NAMES:
        path = paths["raw_logs"] / name
        if path.exists() and path.is_file() and not path.is_symlink():
            diagnostic_bytes += path.stat().st_size
    telemetry_bytes = paths["telemetry"].stat().st_size if paths["telemetry"].exists() else 0
    governed_count = 0
    if paths["governed_items"].exists():
        governed_count = sum(1 for item in paths["governed_items"].iterdir() if item.is_dir() and not item.is_symlink())
    checkpoints = paths["root"] / "state" / "checkpoints"
    checkpoint_count = 0
    if checkpoints.exists():
        checkpoint_count = sum(1 for item in checkpoints.iterdir() if item.is_file() and item.suffix == ".json" and not item.is_symlink())
    return {
        "filesystem_total_bytes": usage.total,
        "filesystem_free_bytes": usage.free,
        "telemetry_jsonl_bytes": telemetry_bytes,
        "raw_diagnostic_bytes": diagnostic_bytes,
        "governed_storage_items": governed_count,
        "recovery_checkpoints": checkpoint_count,
        "threshold_claims": "none; visibility only",
    }


def _process_snapshot(root: Path) -> dict[str, Any]:
    health = _read_health_record(root)
    generation = health.get("generation")
    return {
        "pid": health.get("pid") if isinstance(health.get("pid"), int) else None,
        "generation": generation if isinstance(generation, int) else None,
        "started_at": health.get("started_at") if isinstance(health.get("started_at"), str) else None,
        "previous_instance_id_present": isinstance(health.get("previous_instance_id"), str),
        "restart_count_observed_minimum": max(generation - 1, 0) if isinstance(generation, int) and generation >= 1 else None,
        "restart_semantics": "P7.02 generation visibility; not an SLA/reliability claim",
    }


def _alert_payload(status: HealthStatus) -> dict[str, Any]:
    severity = "critical" if status.state == "down" else "warning"
    return {
        "schema": ALERT_SCHEMA,
        "classification": "owner-local actionable operational alert; non-canonical",
        "canonical_authority": False,
        "created_at": _utc_now(),
        "severity": severity,
        "state": status.state,
        "code": status.code,
        "detail": status.detail,
        "operator_action": status.action,
        "release_sha": status.release_sha,
    }


def publish_health_signal(root: Path, status: HealthStatus) -> Optional[dict[str, Any]]:
    initialize(root)
    alert_path = _paths(root)["alert"]
    if status.state == "healthy":
        try:
            alert_path.unlink()
        except FileNotFoundError:
            pass
        emit_telemetry(root, event="health.observed", attributes={"status": "healthy", "code": status.code,
                                                                 "release_sha": status.release_sha})
        return None
    alert = _alert_payload(status)
    _atomic_json(alert_path, alert)
    emit_telemetry(root, event="health.alert", level="CRITICAL" if status.state == "down" else "WARNING",
                   attributes={"status": status.state, "code": status.code, "release_sha": status.release_sha})
    return alert


def operational_status(root: Path, *, max_age_seconds: float = DEFAULT_HEALTH_MAX_AGE_SECONDS,
                       publish: bool = True) -> dict[str, Any]:
    policy = initialize(root)
    status = classify_health(root, max_age_seconds=max_age_seconds)
    alert = publish_health_signal(root, status) if publish else (_alert_payload(status) if status.state != "healthy" else None)
    return {
        "schema": STATUS_SCHEMA,
        "classification": "owner-local operational status projection; non-canonical",
        "canonical_authority": False,
        "state": status.state,
        "code": status.code,
        "detail": status.detail,
        "operator_action": status.action,
        "release_sha": status.release_sha,
        "heartbeat_age_seconds": status.heartbeat_age_seconds,
        "process": _process_snapshot(root),
        "resources": _resource_snapshot(root),
        "active_alert": alert,
        "telemetry_retention_hours": policy["retention_hours"],
    }


def _require_audit_decision(decision: p704.AccessDecision) -> None:
    if not isinstance(decision, p704.AccessDecision):
        raise BoundaryError("audit visibility requires a P7.04 AccessDecision")
    if not decision.allowed or not decision.operational_access_only:
        raise BoundaryError("audit visibility denied by P7.04")
    if decision.operation != "audit.inspect" or decision.resource != "state:governed":
        raise BoundaryError("audit visibility requires exact audit.inspect/state:governed grant")
    if decision.access_path not in {"local", "remote"}:
        raise BoundaryError("unsupported audit access path")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise IntegrityError("operational audit access must not satisfy authority/approval")


def audit_visibility(root: Path, decision: p704.AccessDecision, *, limit: int = 100) -> dict[str, Any]:
    """Return authorized metadata-only views of governed records and recovery checkpoints.

    Filesystem mtimes are exposed only as non-authoritative storage observations;
    canonical event/execution time remains whatever the governed source records say.
    """
    _require_audit_decision(decision)
    if limit <= 0 or limit > 1000:
        raise BoundaryError("audit visibility limit must be 1..1000")
    items_root = _paths(root)["governed_items"]
    entries: list[dict[str, Any]] = []
    candidates: list[tuple[float, Path]] = []
    if items_root.exists():
        for item_dir in items_root.iterdir():
            if item_dir.is_dir() and not item_dir.is_symlink():
                candidates.append((item_dir.stat().st_mtime, item_dir))
    for observed_mtime, item_dir in sorted(candidates, key=lambda value: value[0], reverse=True):
        if len(entries) >= limit:
            break
        manifest = p703.verify_item(item_dir)
        metadata = manifest["metadata"]
        if metadata.get("state_class") != "canonical-governed-state":
            continue
        entries.append({
            "storage_item_id": manifest["storage_item_id"],
            "semantic_type": metadata.get("semantic_type"),
            "schema_version": metadata.get("schema_version"),
            "classification": metadata.get("classification"),
            "authority_mode": metadata.get("authority_mode"),
            "subject_identity": metadata.get("subject_identity"),
            "version_identity": metadata.get("version_identity"),
            "provenance_refs": list(metadata.get("provenance_refs", []))[:20],
            "storage_observed_at": datetime.fromtimestamp(observed_mtime, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            "storage_observed_at_authority": "non-canonical filesystem observation",
            "payload_exposed": False,
        })

    checkpoint_root = _paths(root)["root"] / "state" / "checkpoints"
    checkpoints: list[dict[str, Any]] = []
    checkpoint_candidates: list[tuple[float, Path]] = []
    if checkpoint_root.exists():
        for path in checkpoint_root.iterdir():
            if path.is_file() and path.suffix == ".json" and not path.is_symlink():
                checkpoint_candidates.append((path.stat().st_mtime, path))
    for observed_mtime, path in sorted(checkpoint_candidates, key=lambda value: value[0], reverse=True)[:limit]:
        checkpoint = p703.verify_checkpoint(_paths(root)["root"], path)
        checkpoints.append({
            "checkpoint_id": checkpoint.get("checkpoint_id"),
            "execution_subject_identity": checkpoint.get("execution_subject_identity"),
            "execution_version_identity": checkpoint.get("execution_version_identity"),
            "classification": checkpoint.get("classification"),
            "reason": checkpoint.get("reason"),
            "created_at": checkpoint.get("created_at"),
            "governed_storage_item_count": len(checkpoint.get("governed_storage_item_ids", [])),
            "canonical_authority": checkpoint.get("canonical_authority"),
            "external_effect_replay_authorized": checkpoint.get("external_effect_replay_authorized"),
            "storage_observed_at": datetime.fromtimestamp(observed_mtime, tz=timezone.utc).isoformat().replace("+00:00", "Z"),
            "payload_exposed": False,
        })

    emit_telemetry(root, event="audit.visibility", attributes={
        "operation": decision.operation,
        "resource": decision.resource,
        "access_path": decision.access_path,
        "principal_kind": decision.principal_kind,
        "allowed": True,
        "count": len(entries) + len(checkpoints),
    })
    return {
        "schema": AUDIT_SCHEMA,
        "classification": "authorized audit/reconstruction metadata projection; source records remain authoritative",
        "projection_canonical_authority": False,
        "storage_recency_canonical_authority": False,
        "payload_bytes_exposed": False,
        "count": len(entries),
        "checkpoint_count": len(checkpoints),
        "items": entries,
        "recovery_checkpoints": checkpoints,
    }


def operator_audit_visibility(
    root: Path,
    p6_context_file: Path,
    *,
    access_path: str = "local",
    limit: int = 100,
) -> dict[str, Any]:
    """Authorize an audit projection through the persistent P7.04 boundary."""
    organization, human = p704.load_p6_owner_context(p6_context_file)
    state = p704.load_access_store(root)
    principal_key = p704._principal_key(human)
    active = [
        record for record in state["credentials"].values()
        if record["principal_key"] == principal_key and record["status"] == "active"
    ]
    if len(active) != 1:
        raise BoundaryError("audit visibility requires exactly one active operator credential")
    credential_id = active[0]["credential_id"]
    secret = p704.read_credential_secret(p704._secret_path(root, credential_id))
    decision = p704.authorize(
        root,
        organization=organization,
        principal=human,
        credential_id=credential_id,
        credential_secret=secret,
        operation="audit.inspect",
        resource="state:governed",
        access_path=access_path,
    )
    return audit_visibility(root, decision, limit=limit)


def _rewrite_jsonl(path: Path, records: Sequence[dict[str, Any]]) -> None:
    if not records:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return
    data = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                   for record in records).encode("utf-8")
    _private_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass


def cleanup(root: Path, *, now: Optional[datetime] = None) -> dict[str, Any]:
    policy = initialize(root)
    paths = _paths(root)
    cutoff = (now or _utc_now_dt()) - timedelta(hours=policy["retention_hours"])
    kept: list[dict[str, Any]] = []
    removed_records = 0
    telemetry = paths["telemetry"]
    if telemetry.exists():
        try:
            lines = telemetry.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise IntegrityError(f"telemetry unreadable: {exc}") from exc
        for line in lines:
            try:
                record = json.loads(line)
                if not isinstance(record, dict) or record.get("schema") != TELEMETRY_SCHEMA:
                    raise ValueError
                ts = _parse_ts(record["recorded_at"])
            except (json.JSONDecodeError, KeyError, ValueError, IntegrityError) as exc:
                raise IntegrityError("refusing cleanup of malformed telemetry JSONL") from exc
            if ts < cutoff:
                removed_records += 1
            else:
                kept.append(record)
        if len(kept) > policy["max_records"]:
            removed_records += len(kept) - policy["max_records"]
            kept = kept[-policy["max_records"]:]
        while kept:
            encoded = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                              for r in kept).encode("utf-8")
            if len(encoded) <= policy["max_jsonl_bytes"]:
                break
            kept.pop(0)
            removed_records += 1
        _rewrite_jsonl(telemetry, kept)

    removed_raw_logs: list[str] = []
    for name in RAW_DIAGNOSTIC_NAMES:
        path = paths["raw_logs"] / name
        if not path.exists():
            continue
        # Raw launchd stdout/stderr are non-canonical diagnostic buffers. Remove
        # only when stale; never follow symlinks and never traverse elsewhere.
        if path.is_symlink():
            raise IntegrityError(f"refusing cleanup of symlink diagnostic: {path}")
        metadata = path.stat()
        modified = datetime.fromtimestamp(metadata.st_mtime, tz=timezone.utc)
        if modified < cutoff:
            path.unlink()
            removed_raw_logs.append(name)
        elif metadata.st_size > policy["max_jsonl_bytes"]:
            # Bounded raw diagnostics have no canonical/audit authority. Truncate
            # oversized buffers instead of accumulating arbitrary content.
            path.write_bytes(b"")
            if os.name != "nt":
                os.chmod(path, 0o600)
            removed_raw_logs.append(f"{name}:truncated")

    return {
        "classification": "non-canonical cleanup result",
        "removed_telemetry_records": removed_records,
        "kept_telemetry_records": len(kept),
        "removed_raw_diagnostic_files": removed_raw_logs,
        "protected_prefixes_touched": False,
        "canonical_state_deleted": False,
        "evidence_deleted": False,
    }


def observe_once(root: Path, *, max_age_seconds: float = DEFAULT_HEALTH_MAX_AGE_SECONDS) -> dict[str, Any]:
    """One bounded observer cycle: classify, publish/clear alert, then enforce retention."""
    status = operational_status(root, max_age_seconds=max_age_seconds, publish=True)
    retention = cleanup(root)
    return {"status": status, "retention": retention}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.05 owner-local operational visibility")
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="show actionable health and publish/clear local alert")
    status.add_argument("--runtime-root", required=True)
    status.add_argument("--max-age-seconds", type=float, default=DEFAULT_HEALTH_MAX_AGE_SECONDS)
    status.add_argument("--json", action="store_true")

    observe = sub.add_parser("observe", help="run one observer + retention cycle")
    observe.add_argument("--runtime-root", required=True)
    observe.add_argument("--max-age-seconds", type=float, default=DEFAULT_HEALTH_MAX_AGE_SECONDS)
    observe.add_argument("--json", action="store_true")

    audit = sub.add_parser("audit", help="authorized metadata-only governed audit projection")
    audit.add_argument("--runtime-root", required=True)
    audit.add_argument("--p6-context-file", required=True)
    audit.add_argument("--access-path", choices=("local", "remote"), default="local")
    audit.add_argument("--limit", type=int, default=100)
    audit.add_argument("--json", action="store_true")

    clean = sub.add_parser("cleanup", help="enforce bounded telemetry/diagnostic retention")
    clean.add_argument("--runtime-root", required=True)
    clean.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = Path(args.runtime_root)
        if args.command == "status":
            result = operational_status(root, max_age_seconds=args.max_age_seconds)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            else:
                print(f"P7.05 {result['state'].upper()} [{result['code']}] {result['detail']}")
                print(f"action: {result['operator_action']}")
            return {"healthy": 0, "degraded": 1, "down": 2}[result["state"]]
        if args.command == "observe":
            result = observe_once(root, max_age_seconds=args.max_age_seconds)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            else:
                status = result["status"]
                print(f"P7.05 observer {status['state'].upper()} [{status['code']}] action={status['operator_action']}")
            # The observer process itself succeeded even when it detected a
            # service incident; the non-canonical alert/status carries that signal.
            return 0
        if args.command == "audit":
            result = operator_audit_visibility(
                root, Path(args.p6_context_file),
                access_path=args.access_path, limit=args.limit,
            )
            if args.json:
                print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            else:
                print(f"P7.05 audit PASS canonical-record-metadata={result['count']} payload_bytes_exposed=false")
            return 0
        result = cleanup(root)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        else:
            print("P7.05 cleanup PASS "
                  f"removed_records={result['removed_telemetry_records']} "
                  f"kept_records={result['kept_telemetry_records']}")
        return 0
    except (P705Error, p703.P703Error, p704.P704Error, OSError, ValueError) as exc:
        print(f"P7.05 FAIL: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
