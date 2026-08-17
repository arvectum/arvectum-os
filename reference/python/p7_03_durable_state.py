#!/usr/bin/env python3
"""P7.03 owner-local durable governed-state/checkpoint backup baseline.

This is a bounded, reversible filesystem adapter for the selected owner-operated
persistent contour.  It is not a public persistence API or stable storage format.
It does not authorize canonical mutation or external effects.  Callers may persist
canonical governed bytes only after the applicable Governed Execution/admission
path has already authorized and produced them.

The adapter keeps these classes physically and semantically separate:

* state/governed     - immutable already-governed payloads + semantic metadata;
* state/checkpoints  - immutable recovery checkpoints, explicitly non-authoritative;
* config/p7-03-recovery.json - owner-local non-secret recovery metadata;
* run/logs/cache     - non-canonical operational/derived state, excluded from backup;
* secrets            - owner-local reusable secrets, always excluded from backup.

Backups are integrity-manifested archives.  Restore is staged, verified, and only
then atomically published to an isolated target root.  No command overwrites live
state or replays an external effect.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shutil
import sys
import tarfile
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterable, Mapping, Optional


STORE_SCHEMA = "arvectum.p7_03.durable-store/1"
ITEM_SCHEMA = "arvectum.p7_03.governed-item/1"
CHECKPOINT_SCHEMA = "arvectum.p7_03.execution-checkpoint/1"
RECOVERY_CONFIG_SCHEMA = "arvectum.p7_03.recovery-config/1"
BACKUP_MANIFEST_SCHEMA = "arvectum.p7_03.backup-manifest/1"
PROOF_SUMMARY_SCHEMA = "arvectum.p7_03.proof-summary/1"
ORGANIZATION_SCOPE = "ООО «Арвектум»"
OPERATING_MODE = "Persistent Internal / owner-operated"
INTERNAL_FORMAT_STATUS = "bounded-internal-provisional"
EXCLUDED_BACKUP_PATHS = ("run/", "logs/", "cache/", "secrets/")
ALLOWED_STATE_CLASSES = {"canonical-governed-state", "governed-test-fixture"}
ALLOWED_AUTHORITY_MODES = {"Native", "External Reference", "Governed Replica"}


class P703Error(RuntimeError):
    """Base P7.03 persistence error."""


class IntegrityError(P703Error):
    """Persisted state or backup failed integrity validation."""


class BoundaryError(P703Error):
    """A P7.03 state/authority/scope boundary would be crossed."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _validate_release_sha(value: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 40 or any(ch not in "0123456789abcdef" for ch in normalized):
        raise BoundaryError("release SHA must be a full 40-character Git commit SHA")
    return normalized


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _fsync_dir(path: Path) -> None:
    if os.name == "nt":
        return
    flags = getattr(os, "O_DIRECTORY", 0) | os.O_RDONLY
    fd = os.open(path, flags)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path, 0o700)
    except OSError:
        if os.name != "nt":
            raise


def _atomic_bytes_write(path: Path, payload: bytes) -> None:
    _ensure_private_dir(path.parent)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.chmod(tmp_name, 0o600)
        except OSError:
            if os.name != "nt":
                raise
        os.replace(tmp_name, path)
        _fsync_dir(path.parent)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def _atomic_json_write(path: Path, payload: Mapping[str, Any]) -> None:
    _atomic_bytes_write(path, json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IntegrityError(f"missing required file: {path}") from exc
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrityError(f"unreadable JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntegrityError(f"expected JSON object: {path}")
    return value


def _assert_private_path(path: Path) -> None:
    if not path.exists():
        raise IntegrityError(f"missing durable path: {path}")
    if path.is_symlink():
        raise IntegrityError(f"symlink not allowed in durable state: {path}")
    if os.name != "nt":
        mode = path.stat().st_mode & 0o777
        if path.is_dir() and mode & 0o077:
            raise IntegrityError(f"durable directory is not owner-only: {path} mode={oct(mode)}")
        if path.is_file() and mode & 0o077:
            raise IntegrityError(f"durable file is not owner-only: {path} mode={oct(mode)}")


def _required_text(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise BoundaryError(f"metadata field {key!r} must be a non-empty string")
    return value.strip()


def _validate_governed_metadata(metadata: Mapping[str, Any], release_sha: str) -> Dict[str, Any]:
    if not isinstance(metadata, Mapping):
        raise BoundaryError("governed metadata must be a JSON object")
    result = dict(metadata)
    state_class = _required_text(result, "state_class")
    if state_class not in ALLOWED_STATE_CLASSES:
        raise BoundaryError(f"unsupported state_class: {state_class}")
    if _required_text(result, "organization_scope") != ORGANIZATION_SCOPE:
        raise BoundaryError("P7.03 initial store is restricted to ООО «Арвектум»")
    _required_text(result, "semantic_type")
    _required_text(result, "schema_version")
    _required_text(result, "classification")
    _required_text(result, "retention_policy_ref")
    _validate_release_sha(_required_text(result, "source_release_sha"))

    if state_class == "canonical-governed-state":
        _required_text(result, "subject_identity")
        _required_text(result, "version_identity")
        authority_mode = _required_text(result, "authority_mode")
        if authority_mode not in ALLOWED_AUTHORITY_MODES:
            raise BoundaryError(f"unsupported authority_mode: {authority_mode}")
        _required_text(result, "authority_scope")
        _required_text(result, "governed_admission_ref")
        provenance = result.get("provenance_refs")
        if not isinstance(provenance, list) or not provenance or not all(isinstance(item, str) and item.strip() for item in provenance):
            raise BoundaryError("canonical governed state requires non-empty provenance_refs")
        if result.get("canonical_authority") is not True:
            raise BoundaryError("canonical governed state metadata must explicitly declare canonical_authority=true")
    else:
        if result.get("canonical_authority") is not False:
            raise BoundaryError("proof fixture must explicitly declare canonical_authority=false")

    if result.get("contains_reusable_secret") is not False:
        raise BoundaryError("P7.03 governed persistence refuses payloads declared to contain reusable secrets")
    return result


def _observe_persistent_runtime(root: Path) -> Dict[str, Any]:
    health_path = root / "run" / "health.json"
    if not health_path.exists():
        return {"observed": False, "release_sha": None, "state": None}
    health = _load_json(health_path)
    release = _validate_release_sha(_required_text(health, "release_sha"))
    state = health.get("state")
    if not isinstance(state, str) or not state:
        raise IntegrityError("persistent runtime health has no valid state")
    if health.get("canonical_state_written") is not False:
        raise IntegrityError("P7.02 runtime health no longer preserves canonical-state-write boundary")
    if health.get("product_effects_enabled") is not False:
        raise IntegrityError("P7.02 runtime health no longer preserves product-effect boundary")
    return {"observed": True, "release_sha": release, "state": state}


def _layout(root: Path) -> Dict[str, Path]:
    return {
        "state": root / "state",
        "governed": root / "state" / "governed",
        "items": root / "state" / "governed" / "items",
        "checkpoints": root / "state" / "checkpoints",
        "config": root / "config",
        "recovery_config": root / "config" / "p7-03-recovery.json",
        "backups": root / "backups",
        "evidence": root / "evidence",
    }


def initialize_store(root: Path, release_sha: str) -> Dict[str, Any]:
    release_sha = _validate_release_sha(release_sha)
    root = root.expanduser().resolve()
    _ensure_private_dir(root)
    paths = _layout(root)
    for key in ("state", "governed", "items", "checkpoints", "config", "backups", "evidence"):
        _ensure_private_dir(paths[key])

    runtime_observation = _observe_persistent_runtime(root)
    recovery_config = {
        "schema": RECOVERY_CONFIG_SCHEMA,
        "format_status": INTERNAL_FORMAT_STATUS,
        "classification": "owner-local non-secret recovery metadata",
        "operating_mode": OPERATING_MODE,
        "organization_scope": ORGANIZATION_SCOPE,
        "tool_release_sha": release_sha,
        "persistent_runtime_release_sha": runtime_observation["release_sha"],
        "persistent_runtime_state_observed": runtime_observation["state"],
        "store_schema": STORE_SCHEMA,
        "backup_scope": ["state/governed/", "state/checkpoints/", "config/p7-03-recovery.json"],
        "explicit_exclusions": list(EXCLUDED_BACKUP_PATHS),
        "telemetry_authority": "non-canonical",
        "checkpoint_authority": "non-canonical recovery state; never substitutes for canonical history",
        "reusable_secrets_in_governed_backup": False,
        "secret_recovery": "re-provision separately when required; P7.03 backup never copies reusable secrets",
        "runtime_reconstruction": "P7.02 service/release is reconstructed from canonical Git and its exact release pin; service adapter is not canonical state",
        "retention_mode": "no universal period selected; backup deletion is explicit owner operation",
        "canonical_deletion_mode": "never implicit through backup rotation or cache/log cleanup",
    }
    _atomic_json_write(paths["recovery_config"], recovery_config)
    return recovery_config


def persist_governed_item(root: Path, release_sha: str, payload: bytes, metadata: Mapping[str, Any]) -> str:
    release_sha = _validate_release_sha(release_sha)
    initialize_store(root, release_sha)
    metadata_value = _validate_governed_metadata(metadata, release_sha)
    payload_sha = _sha256_bytes(payload)
    identity_material = {
        "schema": ITEM_SCHEMA,
        "metadata": metadata_value,
        "payload_sha256": payload_sha,
        "payload_size": len(payload),
    }
    item_id = _sha256_bytes(_canonical_json_bytes(identity_material))
    final_dir = _layout(root)["items"] / item_id
    manifest = {
        **identity_material,
        "storage_item_id": item_id,
        "storage_identity_semantics": "content-addressed storage locator only; not an RFC-0002 Subject Identity or Version Identity",
        "integrity_claim": "byte/content integrity only; does not create truth, authority or approval",
    }

    if final_dir.exists():
        verify_item(final_dir)
        existing = _load_json(final_dir / "manifest.json")
        if existing != manifest or (final_dir / "payload.bin").read_bytes() != payload:
            raise IntegrityError(f"immutable item collision or mismatch: {item_id}")
        return item_id

    parent = final_dir.parent
    _ensure_private_dir(parent)
    staging = parent / f".{item_id}.staging-{uuid.uuid4().hex}"
    _ensure_private_dir(staging)
    try:
        _atomic_bytes_write(staging / "payload.bin", payload)
        _atomic_json_write(staging / "manifest.json", manifest)
        _fsync_dir(staging)
        os.replace(staging, final_dir)
        _fsync_dir(parent)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    verify_item(final_dir)
    return item_id


def verify_item(item_dir: Path) -> Dict[str, Any]:
    _assert_private_path(item_dir)
    manifest_path = item_dir / "manifest.json"
    payload_path = item_dir / "payload.bin"
    _assert_private_path(manifest_path)
    _assert_private_path(payload_path)
    manifest = _load_json(manifest_path)
    if manifest.get("schema") != ITEM_SCHEMA:
        raise IntegrityError(f"unexpected governed item schema: {item_dir}")
    if manifest.get("storage_item_id") != item_dir.name:
        raise IntegrityError(f"governed item directory/id mismatch: {item_dir}")
    payload = payload_path.read_bytes()
    payload_sha = _sha256_bytes(payload)
    if manifest.get("payload_sha256") != payload_sha or manifest.get("payload_size") != len(payload):
        raise IntegrityError(f"governed item payload integrity mismatch: {item_dir.name}")
    metadata = manifest.get("metadata")
    if not isinstance(metadata, dict):
        raise IntegrityError(f"governed item metadata missing: {item_dir.name}")
    release_sha = _validate_release_sha(_required_text(metadata, "source_release_sha"))
    try:
        validated_metadata = _validate_governed_metadata(metadata, release_sha)
    except BoundaryError as exc:
        raise IntegrityError(f"invalid governed item metadata: {item_dir.name}: {exc}") from exc
    identity_material = {
        "schema": ITEM_SCHEMA,
        "metadata": validated_metadata,
        "payload_sha256": payload_sha,
        "payload_size": len(payload),
    }
    expected_id = _sha256_bytes(_canonical_json_bytes(identity_material))
    if expected_id != item_dir.name:
        raise IntegrityError(f"governed item identity hash mismatch: {item_dir.name}")
    return manifest


def create_checkpoint(
    root: Path,
    release_sha: str,
    *,
    execution_subject_identity: str,
    execution_version_identity: str,
    governed_storage_item_ids: Iterable[str],
    classification: str,
    retention_policy_ref: str,
    reason: str,
) -> str:
    release_sha = _validate_release_sha(release_sha)
    initialize_store(root, release_sha)
    item_ids = tuple(dict.fromkeys(item.strip() for item in governed_storage_item_ids if item.strip()))
    if not item_ids:
        raise BoundaryError("checkpoint requires at least one governed item reference")
    for item_id in item_ids:
        if len(item_id) != 64 or any(ch not in "0123456789abcdef" for ch in item_id):
            raise BoundaryError(f"invalid governed item id: {item_id}")
        verify_item(_layout(root)["items"] / item_id)

    body = {
        "schema": CHECKPOINT_SCHEMA,
        "format_status": INTERNAL_FORMAT_STATUS,
        "classification": classification.strip(),
        "retention_policy_ref": retention_policy_ref.strip(),
        "organization_scope": ORGANIZATION_SCOPE,
        "operating_mode": OPERATING_MODE,
        "canonical_authority": False,
        "authority_statement": "checkpoint preserves recovery position only; canonical history remains authoritative",
        "execution_subject_identity": execution_subject_identity.strip(),
        "execution_version_identity": execution_version_identity.strip(),
        "governed_storage_item_ids": list(item_ids),
        "tool_release_sha": release_sha,
        "reason": reason.strip(),
        "created_at": _utc_now(),
        "external_effect_replay_authorized": False,
    }
    for key in ("classification", "retention_policy_ref", "execution_subject_identity", "execution_version_identity", "reason"):
        if not body[key]:
            raise BoundaryError(f"checkpoint field {key} must be non-empty")
    checkpoint_id = _sha256_bytes(_canonical_json_bytes(body))
    document = {**body, "checkpoint_id": checkpoint_id}
    path = _layout(root)["checkpoints"] / f"{checkpoint_id}.json"
    if path.exists():
        existing = _load_json(path)
        if existing != document:
            raise IntegrityError(f"immutable checkpoint collision or mismatch: {checkpoint_id}")
        return checkpoint_id
    _atomic_json_write(path, document)
    verify_checkpoint(root, path)
    return checkpoint_id


def verify_checkpoint(root: Path, path: Path) -> Dict[str, Any]:
    _assert_private_path(path)
    value = _load_json(path)
    if value.get("schema") != CHECKPOINT_SCHEMA:
        raise IntegrityError(f"unexpected checkpoint schema: {path}")
    if value.get("canonical_authority") is not False or value.get("external_effect_replay_authorized") is not False:
        raise IntegrityError(f"checkpoint authority boundary violated: {path}")
    if value.get("organization_scope") != ORGANIZATION_SCOPE:
        raise IntegrityError(f"checkpoint Organization mismatch: {path}")
    item_ids = value.get("governed_storage_item_ids")
    if not isinstance(item_ids, list) or not item_ids:
        raise IntegrityError(f"checkpoint has no governed state refs: {path}")
    for item_id in item_ids:
        if not isinstance(item_id, str):
            raise IntegrityError(f"checkpoint item ref is not a string: {path}")
        verify_item(_layout(root)["items"] / item_id)
    checkpoint_id = value.get("checkpoint_id")
    if not isinstance(checkpoint_id, str) or path.name != f"{checkpoint_id}.json":
        raise IntegrityError(f"checkpoint path/id mismatch: {path}")
    body = dict(value)
    body.pop("checkpoint_id", None)
    expected = _sha256_bytes(_canonical_json_bytes(body))
    if checkpoint_id != expected:
        raise IntegrityError(f"checkpoint identity hash mismatch: {checkpoint_id}")
    return value


def verify_store(root: Path) -> Dict[str, Any]:
    root = root.expanduser().resolve()
    paths = _layout(root)
    for key in ("state", "governed", "items", "checkpoints", "config"):
        path = paths[key]
        if not path.exists():
            raise IntegrityError(f"missing durable store directory: {path}")
        _assert_private_path(path)
    config = _load_json(paths["recovery_config"])
    _assert_private_path(paths["recovery_config"])
    if config.get("schema") != RECOVERY_CONFIG_SCHEMA or config.get("store_schema") != STORE_SCHEMA:
        raise IntegrityError("unexpected P7.03 recovery/store schema")
    if config.get("organization_scope") != ORGANIZATION_SCOPE:
        raise IntegrityError("recovery config Organization mismatch")
    if config.get("explicit_exclusions") != list(EXCLUDED_BACKUP_PATHS):
        raise IntegrityError("recovery config backup exclusions mismatch")
    _validate_release_sha(_required_text(config, "tool_release_sha"))
    runtime_release = config.get("persistent_runtime_release_sha")
    if runtime_release is not None:
        _validate_release_sha(runtime_release)
    items: Dict[str, Dict[str, Any]] = {}
    for child in sorted(paths["items"].iterdir()):
        if child.name.startswith("."):
            raise IntegrityError(f"unexpected staging entry in governed store: {child}")
        if not child.is_dir():
            raise IntegrityError(f"unexpected governed-store entry: {child}")
        items[child.name] = verify_item(child)
    checkpoints: Dict[str, Dict[str, Any]] = {}
    for child in sorted(paths["checkpoints"].iterdir()):
        if child.name.startswith("."):
            raise IntegrityError(f"unexpected staging entry in checkpoint store: {child}")
        if not child.is_file() or child.suffix != ".json":
            raise IntegrityError(f"unexpected checkpoint-store entry: {child}")
        checkpoints[child.stem] = verify_checkpoint(root, child)
    return {
        "schema": STORE_SCHEMA,
        "organization_scope": ORGANIZATION_SCOPE,
        "governed_items": len(items),
        "checkpoints": len(checkpoints),
        "tool_release_sha": config["tool_release_sha"],
        "persistent_runtime_release_sha": runtime_release,
        "integrity": "PASS",
    }


def _included_backup_files(root: Path) -> list[Path]:
    paths = _layout(root)
    files: list[Path] = [paths["recovery_config"]]
    for base in (paths["items"], paths["checkpoints"]):
        for path in sorted(base.rglob("*")):
            if path.is_symlink():
                raise IntegrityError(f"symlink not allowed in backup scope: {path}")
            if path.is_file():
                files.append(path)
            elif not path.is_dir():
                raise IntegrityError(f"unsupported filesystem entry in backup scope: {path}")
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def _backup_manifest(root: Path, release_sha: str, files: Iterable[Path]) -> Dict[str, Any]:
    entries = []
    for path in files:
        rel = path.relative_to(root).as_posix()
        entries.append({"path": rel, "sha256": _sha256_file(path), "size": path.stat().st_size})
    return {
        "schema": BACKUP_MANIFEST_SCHEMA,
        "format_status": INTERNAL_FORMAT_STATUS,
        "classification": "governed-state recovery package metadata",
        "organization_scope": ORGANIZATION_SCOPE,
        "operating_mode": OPERATING_MODE,
        "tool_release_sha": release_sha,
        "created_at": _utc_now(),
        "included_roots": ["state/governed/", "state/checkpoints/", "config/p7-03-recovery.json"],
        "explicit_exclusions": list(EXCLUDED_BACKUP_PATHS),
        "reusable_secrets_included": False,
        "telemetry_included": False,
        "cache_included": False,
        "canonical_authority_claim": False,
        "integrity_claim": "archive and byte integrity only; does not create truth, authority or approval",
        "files": entries,
    }


def create_backup(root: Path, release_sha: str, output: Optional[Path] = None) -> tuple[Path, str]:
    release_sha = _validate_release_sha(release_sha)
    initialize_store(root, release_sha)
    verify_store(root)
    paths = _layout(root)
    files = _included_backup_files(root)
    manifest = _backup_manifest(root, release_sha, files)
    backup_id = _sha256_bytes(_canonical_json_bytes(manifest))[:16]
    if output is None:
        output = paths["backups"] / f"p7-03-backup-{_stamp()}-{backup_id}.tar.gz"
    output = output.expanduser().resolve()
    if output.parent != paths["backups"].resolve():
        raise BoundaryError("P7.03 baseline writes backups only inside the owner-local runtime backups directory")
    if output.exists():
        raise BoundaryError(f"backup output already exists: {output}")
    _ensure_private_dir(output.parent)

    fd, tmp_name = tempfile.mkstemp(prefix=f".{output.name}.", suffix=".tmp", dir=str(output.parent))
    os.close(fd)
    tmp_path = Path(tmp_name)
    try:
        with tarfile.open(tmp_path, "w:gz", format=tarfile.PAX_FORMAT) as archive:
            manifest_bytes = json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
            info = tarfile.TarInfo("backup-manifest.json")
            info.size = len(manifest_bytes)
            info.mode = 0o600
            info.mtime = 0
            archive.addfile(info, io.BytesIO(manifest_bytes))
            for path in files:
                rel = path.relative_to(root).as_posix()
                info = archive.gettarinfo(str(path), arcname=rel)
                if not info.isfile():
                    raise IntegrityError(f"backup scope contains non-regular file: {path}")
                info.mode = 0o600
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                with path.open("rb") as handle:
                    archive.addfile(info, handle)
        try:
            os.chmod(tmp_path, 0o600)
        except OSError:
            if os.name != "nt":
                raise
        os.replace(tmp_path, output)
        _fsync_dir(output.parent)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    archive_sha = _sha256_file(output)
    checksum_path = output.with_name(output.name + ".sha256")
    _atomic_bytes_write(checksum_path, f"{archive_sha}  {output.name}\n".encode("ascii"))
    verify_backup(output)
    return output, archive_sha


def _safe_member_name(name: str) -> str:
    if "\\" in name:
        raise IntegrityError(f"unsafe backup member path: {name}")
    normalized = PurePosixPath(name)
    if normalized.is_absolute() or ".." in normalized.parts or not normalized.parts:
        raise IntegrityError(f"unsafe backup member path: {name}")
    return normalized.as_posix()


def _read_backup_members(archive_path: Path) -> tuple[Dict[str, Any], Dict[str, bytes]]:
    payloads: Dict[str, bytes] = {}
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            name = _safe_member_name(member.name)
            if member.issym() or member.islnk() or member.isdev() or member.isdir():
                raise IntegrityError(f"backup contains unsupported member type: {name}")
            if not member.isfile():
                raise IntegrityError(f"backup contains non-regular member: {name}")
            if name in payloads:
                raise IntegrityError(f"backup contains duplicate member: {name}")
            extracted = archive.extractfile(member)
            if extracted is None:
                raise IntegrityError(f"cannot read backup member: {name}")
            payloads[name] = extracted.read()
    manifest_bytes = payloads.get("backup-manifest.json")
    if manifest_bytes is None:
        raise IntegrityError("backup-manifest.json missing")
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntegrityError("backup manifest is not valid UTF-8 JSON") from exc
    if not isinstance(manifest, dict):
        raise IntegrityError("backup manifest must be a JSON object")
    return manifest, payloads


def verify_backup(archive_path: Path) -> Dict[str, Any]:
    archive_path = archive_path.expanduser().resolve()
    checksum_path = archive_path.with_name(archive_path.name + ".sha256")
    if not archive_path.is_file() or not checksum_path.is_file():
        raise IntegrityError("backup archive and checksum sidecar are both required")
    _assert_private_path(archive_path)
    _assert_private_path(checksum_path)
    checksum_line = checksum_path.read_text(encoding="ascii").strip()
    parts = checksum_line.split()
    if len(parts) != 2 or parts[1] != archive_path.name:
        raise IntegrityError("backup checksum sidecar format/name mismatch")
    actual_archive_sha = _sha256_file(archive_path)
    if parts[0] != actual_archive_sha:
        raise IntegrityError("backup archive SHA-256 mismatch")

    manifest, payloads = _read_backup_members(archive_path)
    if manifest.get("schema") != BACKUP_MANIFEST_SCHEMA:
        raise IntegrityError("unexpected backup manifest schema")
    if manifest.get("organization_scope") != ORGANIZATION_SCOPE:
        raise IntegrityError("backup Organization mismatch")
    if manifest.get("explicit_exclusions") != list(EXCLUDED_BACKUP_PATHS):
        raise IntegrityError("backup exclusions mismatch")
    if manifest.get("reusable_secrets_included") is not False:
        raise IntegrityError("backup claims reusable secrets are included")
    _validate_release_sha(_required_text(manifest, "tool_release_sha"))
    files = manifest.get("files")
    if not isinstance(files, list):
        raise IntegrityError("backup manifest files must be a list")
    expected_names = {"backup-manifest.json"}
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256", "size"}:
            raise IntegrityError("backup manifest file entry malformed")
        name = _safe_member_name(entry["path"])
        if any(name == prefix.rstrip("/") or name.startswith(prefix) for prefix in EXCLUDED_BACKUP_PATHS):
            raise IntegrityError(f"excluded path appears in backup manifest: {name}")
        expected_names.add(name)
        data = payloads.get(name)
        if data is None:
            raise IntegrityError(f"manifested backup member missing: {name}")
        if _sha256_bytes(data) != entry["sha256"] or len(data) != entry["size"]:
            raise IntegrityError(f"backup member integrity mismatch: {name}")
    if set(payloads) != expected_names:
        extra = sorted(set(payloads) - expected_names)
        missing = sorted(expected_names - set(payloads))
        raise IntegrityError(f"backup member set mismatch extra={extra} missing={missing}")
    return {
        "schema": BACKUP_MANIFEST_SCHEMA,
        "archive_sha256": actual_archive_sha,
        "files": len(files),
        "integrity": "PASS",
        "reusable_secrets_included": False,
        "explicit_exclusions": list(EXCLUDED_BACKUP_PATHS),
    }


def restore_backup(archive_path: Path, target_root: Path) -> Dict[str, Any]:
    verify_backup(archive_path)
    target_root = target_root.expanduser().resolve()
    if target_root.exists():
        raise BoundaryError(f"restore target must not already exist: {target_root}")
    if not target_root.parent.exists():
        _ensure_private_dir(target_root.parent)
    else:
        _assert_private_path(target_root.parent)
    staging = target_root.parent / f".{target_root.name}.restore-{uuid.uuid4().hex}"
    _ensure_private_dir(staging)
    try:
        manifest, payloads = _read_backup_members(archive_path)
        paths = _layout(staging)
        for key in ("state", "governed", "items", "checkpoints", "config", "evidence"):
            _ensure_private_dir(paths[key])
        for name, data in payloads.items():
            if name == "backup-manifest.json":
                continue
            destination = staging / Path(*PurePosixPath(name).parts)
            _atomic_bytes_write(destination, data)
        _atomic_json_write(paths["evidence"] / "restore-backup-manifest.json", manifest)
        verify_store(staging)
        _fsync_dir(staging)
        os.replace(staging, target_root)
        _fsync_dir(target_root.parent)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    result = verify_store(target_root)
    result["restore_target"] = str(target_root)
    result["backup_manifest_schema"] = manifest["schema"]
    return result


def _tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(rel).to_bytes(4, "big"))
        digest.update(rel)
        data = path.read_bytes()
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def run_proof(root: Path, release_sha: str, *, require_persistent_runtime: bool = False) -> Dict[str, Any]:
    release_sha = _validate_release_sha(release_sha)
    root = root.expanduser().resolve()
    initialize_store(root, release_sha)
    runtime_observation = _observe_persistent_runtime(root)
    if require_persistent_runtime:
        if not runtime_observation["observed"]:
            raise IntegrityError("selected-Mac proof requires observable P7.02 persistent runtime health")
        if runtime_observation["state"] != "healthy":
            raise IntegrityError(f"selected-Mac proof requires healthy persistent runtime, got {runtime_observation['state']!r}")
    live_status_before = verify_store(root)

    live_backup, live_backup_sha = create_backup(root, release_sha)
    live_restore = _layout(root)["evidence"] / f"p7-03-live-restore-{uuid.uuid4().hex[:12]}"
    live_restored_status = restore_backup(live_backup, live_restore)
    live_state_digest = _tree_digest(root / "state")
    restored_state_digest = _tree_digest(live_restore / "state")
    if live_state_digest != restored_state_digest:
        raise IntegrityError("live backup/restore state tree digest mismatch")
    shutil.rmtree(live_restore)

    work = _layout(root)["evidence"] / f".p7-03-proof-work-{uuid.uuid4().hex}"
    source = work / "source"
    restored = work / "restored"
    corrupted = work / "corrupted"
    _ensure_private_dir(work)
    try:
        initialize_store(source, release_sha)
        fixture_payload = _canonical_json_bytes(
            {
                "fixture": "P7.03 non-authoritative durable-state mechanism proof",
                "canonical_authority": False,
                "contains_reusable_secret": False,
                "sequence": 1,
            }
        )
        fixture_metadata = {
            "state_class": "governed-test-fixture",
            "organization_scope": ORGANIZATION_SCOPE,
            "semantic_type": "p7.03-proof-fixture",
            "schema_version": "1",
            "classification": "internal test evidence",
            "retention_policy_ref": "P7.03-proof-ephemeral",
            "source_release_sha": release_sha,
            "canonical_authority": False,
            "contains_reusable_secret": False,
        }
        item_id = persist_governed_item(source, release_sha, fixture_payload, fixture_metadata)
        checkpoint_id = create_checkpoint(
            source,
            release_sha,
            execution_subject_identity="p7.03-proof-execution",
            execution_version_identity="p7.03-proof-execution-v1",
            governed_storage_item_ids=[item_id],
            classification="internal test evidence",
            retention_policy_ref="P7.03-proof-ephemeral",
            reason="prove immutable checkpoint reference and backup/restore without authority or effect replay",
        )
        fixture_status = verify_store(source)
        fixture_backup, fixture_backup_sha = create_backup(source, release_sha)
        fixture_backup_check = verify_backup(fixture_backup)
        fixture_restore_status = restore_backup(fixture_backup, restored)
        if _tree_digest(source / "state") != _tree_digest(restored / "state"):
            raise IntegrityError("fixture restored state digest mismatch")
        shutil.copytree(restored, corrupted)
        corrupt_payload = corrupted / "state" / "governed" / "items" / item_id / "payload.bin"
        corrupt_payload.write_bytes(corrupt_payload.read_bytes() + b"tamper")
        try:
            verify_store(corrupted)
        except IntegrityError:
            tamper_detection = True
        else:
            tamper_detection = False
            raise IntegrityError("corruption negative proof unexpectedly passed")

        with tarfile.open(fixture_backup, "r:gz") as archive:
            names = {member.name for member in archive.getmembers()}
        excluded_absent = all(not any(name == prefix.rstrip("/") or name.startswith(prefix) for name in names) for prefix in EXCLUDED_BACKUP_PATHS)
        if not excluded_absent:
            raise IntegrityError("explicitly excluded state appeared in fixture backup")

        summary = {
            "schema": PROOF_SUMMARY_SCHEMA,
            "status": "PASS",
            "operating_mode": OPERATING_MODE,
            "organization_scope": ORGANIZATION_SCOPE,
            "tool_release_sha": release_sha,
            "persistent_runtime_observed": runtime_observation["observed"],
            "persistent_runtime_release_sha": runtime_observation["release_sha"],
            "persistent_runtime_state": runtime_observation["state"],
            "live_store_before_backup": live_status_before,
            "live_backup_basename": live_backup.name,
            "live_backup_sha256": live_backup_sha,
            "live_restore_integrity": live_restored_status["integrity"],
            "live_state_digest_matches_restore": True,
            "fixture_storage_item_id": item_id,
            "fixture_checkpoint_id": checkpoint_id,
            "fixture_store": fixture_status,
            "fixture_backup_sha256": fixture_backup_sha,
            "fixture_backup_integrity": fixture_backup_check["integrity"],
            "fixture_restore_integrity": fixture_restore_status["integrity"],
            "tamper_detection_fail_closed": tamper_detection,
            "explicit_exclusions_absent": excluded_absent,
            "reusable_secrets_in_backup": False,
            "telemetry_in_backup": False,
            "cache_in_backup": False,
            "checkpoint_canonical_authority": False,
            "external_effect_replay_authorized": False,
            "proof_fixture_canonical_authority": False,
            "storage_adapter_status": INTERNAL_FORMAT_STATUS,
            "created_at": _utc_now(),
        }
    finally:
        if work.exists():
            shutil.rmtree(work)

    summary_path = _layout(root)["evidence"] / f"p7-03-summary-{_stamp()}-{uuid.uuid4().hex[:8]}.json"
    _atomic_json_write(summary_path, summary)
    summary["summary_basename"] = summary_path.name
    return summary


def _load_metadata_file(path: Path) -> Dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise BoundaryError(f"cannot read metadata JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise BoundaryError("metadata file must contain a JSON object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.03 durable governed-state/checkpoint backup baseline")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize owner-local P7.03 durable state layout")
    init.add_argument("--runtime-root", required=True)
    init.add_argument("--release-sha", required=True)

    persist = sub.add_parser("persist", help="persist already-governed immutable bytes; does not authorize admission")
    persist.add_argument("--runtime-root", required=True)
    persist.add_argument("--release-sha", required=True)
    persist.add_argument("--payload-file", required=True)
    persist.add_argument("--metadata-file", required=True)

    checkpoint = sub.add_parser("checkpoint", help="create immutable non-authoritative recovery checkpoint")
    checkpoint.add_argument("--runtime-root", required=True)
    checkpoint.add_argument("--release-sha", required=True)
    checkpoint.add_argument("--execution-subject-identity", required=True)
    checkpoint.add_argument("--execution-version-identity", required=True)
    checkpoint.add_argument("--governed-storage-item-id", action="append", required=True)
    checkpoint.add_argument("--classification", required=True)
    checkpoint.add_argument("--retention-policy-ref", required=True)
    checkpoint.add_argument("--reason", required=True)

    verify = sub.add_parser("verify", help="verify live durable state/checkpoint integrity")
    verify.add_argument("--runtime-root", required=True)

    backup = sub.add_parser("backup", help="create and verify minimized governed-state backup")
    backup.add_argument("--runtime-root", required=True)
    backup.add_argument("--release-sha", required=True)
    backup.add_argument("--output")

    verify_b = sub.add_parser("verify-backup", help="verify archive checksum, manifest and scoped contents")
    verify_b.add_argument("--archive", required=True)

    restore = sub.add_parser("restore", help="restore to a new isolated target; never overwrite live state")
    restore.add_argument("--archive", required=True)
    restore.add_argument("--target-root", required=True)

    prove = sub.add_parser("prove", help="run live empty/non-empty-safe backup/restore plus corruption proof")
    prove.add_argument("--runtime-root", required=True)
    prove.add_argument("--release-sha", required=True)
    prove.add_argument("--require-persistent-runtime", action="store_true")
    prove.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            value = initialize_store(Path(args.runtime_root), args.release_sha)
            print(f"P7.03 init PASS release={value['tool_release_sha']}")
        elif args.command == "persist":
            payload = Path(args.payload_file).read_bytes()
            metadata = _load_metadata_file(Path(args.metadata_file))
            item_id = persist_governed_item(Path(args.runtime_root), args.release_sha, payload, metadata)
            print(f"P7.03 persist PASS storage_item_id={item_id}")
        elif args.command == "checkpoint":
            checkpoint_id = create_checkpoint(
                Path(args.runtime_root),
                args.release_sha,
                execution_subject_identity=args.execution_subject_identity,
                execution_version_identity=args.execution_version_identity,
                governed_storage_item_ids=args.governed_storage_item_id,
                classification=args.classification,
                retention_policy_ref=args.retention_policy_ref,
                reason=args.reason,
            )
            print(f"P7.03 checkpoint PASS checkpoint_id={checkpoint_id}")
        elif args.command == "verify":
            value = verify_store(Path(args.runtime_root))
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        elif args.command == "backup":
            output = None if args.output is None else Path(args.output)
            archive, sha = create_backup(Path(args.runtime_root), args.release_sha, output)
            print(f"P7.03 backup PASS archive={archive} sha256={sha}")
        elif args.command == "verify-backup":
            value = verify_backup(Path(args.archive))
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        elif args.command == "restore":
            value = restore_backup(Path(args.archive), Path(args.target_root))
            print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        elif args.command == "prove":
            value = run_proof(Path(args.runtime_root), args.release_sha, require_persistent_runtime=args.require_persistent_runtime)
            if args.json:
                print(json.dumps(value, ensure_ascii=False, sort_keys=True))
            else:
                print(
                    "P7.03 prove PASS "
                    f"live_items={value['live_store_before_backup']['governed_items']} "
                    f"live_checkpoints={value['live_store_before_backup']['checkpoints']} "
                    f"backup={value['live_backup_basename']} "
                    f"tamper_detection={str(value['tamper_detection_fail_closed']).lower()}"
                )
        else:
            parser.error("unknown command")
    except (P703Error, OSError, ValueError, json.JSONDecodeError, tarfile.TarError) as exc:
        print(f"P7.03 FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
