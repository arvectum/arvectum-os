#!/usr/bin/env python3
"""P7.10 portability, host-loss and clean-environment restore proof.

This module composes the P7.03 governed backup/restore primitive.  It does not
create a second backup format or grant authority to replay external effects.
A P7.10 handoff copies an already verified P7.03 archive and checksum into an
off-host package, adds semantic/path/host evidence, and verifies that evidence
before restoring into an absent target root.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import socket
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

import p7_03_durable_state as p703

HANDOFF_SCHEMA = "arvectum.p7-10-portability-handoff.v1"
RECEIPT_SCHEMA = "arvectum.p7-10-clean-restore-receipt.v1"
MANIFEST_NAME = "p7-10-portability-manifest.json"
MANIFEST_SHA_NAME = MANIFEST_NAME + ".sha256"


class PortabilityError(RuntimeError):
    """P7.10 portability proof failed closed."""


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


def _lexical_absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.path.expanduser(str(path))))


def path_identity(path: Path) -> Dict[str, Any]:
    """Record both operator-visible and filesystem-resolved path identities.

    The distinction is intentional.  On macOS, for example, /var is commonly a
    symlink to /private/var.  Lexical inequality alone is therefore not proof of
    a different storage location.
    """

    lexical = _lexical_absolute(path)
    physical = lexical.resolve(strict=False)
    return {
        "lexical": str(lexical),
        "physical": str(physical),
        "lexical_differs_from_physical": str(lexical) != str(physical),
    }


def paths_refer_same_location(left: Path, right: Path) -> bool:
    left_lex = _lexical_absolute(left)
    right_lex = _lexical_absolute(right)
    if left_lex.exists() and right_lex.exists():
        try:
            return os.path.samefile(left_lex, right_lex)
        except OSError:
            pass
    return left_lex.resolve(strict=False) == right_lex.resolve(strict=False)


def _is_within(candidate: Path, parent: Path) -> bool:
    try:
        candidate.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        path.chmod(0o700)


def _private_file(path: Path) -> None:
    if os.name != "nt":
        path.chmod(0o600)


def _atomic_json(path: Path, value: Dict[str, Any]) -> None:
    _private_dir(path.parent)
    tmp = path.with_name("." + path.name + ".tmp")
    tmp.write_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")
    _private_file(tmp)
    os.replace(tmp, path)
    _private_file(path)


def _state_files(root: Path) -> Iterable[Path]:
    state = root / "state"
    if not state.is_dir():
        raise PortabilityError(f"durable state directory missing: {state}")
    for path in sorted(state.rglob("*")):
        if path.is_symlink():
            raise PortabilityError(f"symlink is not allowed inside governed state: {path}")
        if path.is_file():
            yield path
        elif not path.is_dir():
            raise PortabilityError(f"unsupported governed-state filesystem entry: {path}")


def governed_state_digest(root: Path) -> str:
    """Semantic byte digest independent of the host's absolute root path."""

    digest = hashlib.sha256()
    state = root / "state"
    for path in _state_files(root):
        rel = path.relative_to(state).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(rel).to_bytes(8, "big"))
        digest.update(rel)
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def selected_historical_evidence(root: Path) -> Dict[str, Any]:
    """Reconstruct one deterministic historical governed record.

    P7.10 deliberately requires at least one governed record.  A successful
    empty-store restore would prove archive plumbing, not historical continuity.
    """

    items_dir = root / "state" / "governed" / "items"
    items = sorted(path for path in items_dir.iterdir() if path.is_dir()) if items_dir.is_dir() else []
    if not items:
        raise PortabilityError("P7.10 proof requires at least one governed historical item")
    item_dir = items[0]
    manifest = p703.verify_item(item_dir)
    metadata = manifest.get("metadata")
    if not isinstance(metadata, dict):
        raise PortabilityError("selected governed item has no metadata object")
    payload = item_dir / "payload.bin"
    if not payload.is_file():
        raise PortabilityError("selected governed item payload is missing")
    return {
        "item_id": item_dir.name,
        "payload_sha256": _sha256_file(payload),
        "subject_identity": metadata.get("subject_identity"),
        "version_identity": metadata.get("version_identity"),
        "authority_mode": metadata.get("authority_mode"),
        "source_release_sha": metadata.get("source_release_sha"),
        "provenance_refs": metadata.get("provenance_refs", []),
    }


def _host_context(host_marker: str | None = None) -> Dict[str, Any]:
    marker = (host_marker or socket.gethostname()).strip()
    if not marker:
        raise PortabilityError("host marker must be non-empty")
    return {
        "marker": marker,
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python": platform.python_version(),
    }


def _write_manifest_with_checksum(package_dir: Path, manifest: Dict[str, Any]) -> None:
    manifest_path = package_dir / MANIFEST_NAME
    _atomic_json(manifest_path, manifest)
    manifest_sha = _sha256_file(manifest_path)
    sidecar = package_dir / MANIFEST_SHA_NAME
    sidecar.write_text(f"{manifest_sha}  {MANIFEST_NAME}\n", encoding="ascii")
    _private_file(sidecar)


def _verify_manifest_checksum(package_dir: Path) -> Dict[str, Any]:
    manifest_path = package_dir / MANIFEST_NAME
    sidecar = package_dir / MANIFEST_SHA_NAME
    if not manifest_path.is_file() or not sidecar.is_file():
        raise PortabilityError("handoff manifest and checksum sidecar are required")
    _private_file(manifest_path)
    _private_file(sidecar)
    parts = sidecar.read_text(encoding="ascii").strip().split()
    if len(parts) != 2 or parts[1] != MANIFEST_NAME:
        raise PortabilityError("handoff manifest checksum sidecar is malformed")
    if parts[0] != _sha256_file(manifest_path):
        raise PortabilityError("handoff manifest SHA-256 mismatch")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PortabilityError("handoff manifest is not valid UTF-8 JSON") from exc
    if not isinstance(manifest, dict) or manifest.get("schema") != HANDOFF_SCHEMA:
        raise PortabilityError("unexpected P7.10 handoff schema")
    return manifest


def prepare_handoff(
    source_root: Path,
    off_host_dir: Path,
    release_sha: str,
    *,
    host_marker: str | None = None,
) -> Dict[str, Any]:
    """Create a verified off-host handoff from an existing P7.03 store."""

    source_lex = _lexical_absolute(source_root)
    source = source_lex.resolve(strict=False)
    off_host_lex = _lexical_absolute(off_host_dir)
    off_host = off_host_lex.resolve(strict=False)
    if not source.exists():
        raise PortabilityError(f"source durable root does not exist: {source_lex}")
    if _is_within(off_host, source):
        raise PortabilityError("off-host handoff directory must be physically outside the source runtime root")
    if off_host.exists():
        raise PortabilityError(f"off-host handoff directory must not already exist: {off_host_lex}")

    store = p703.verify_store(source)
    if store.get("integrity") != "PASS":
        raise PortabilityError("P7.03 source store integrity is not PASS")
    state_digest = governed_state_digest(source)
    historical = selected_historical_evidence(source)

    archive, archive_sha = p703.create_backup(source, release_sha)
    backup = p703.verify_backup(archive)
    if backup.get("integrity") != "PASS" or backup.get("archive_sha256") != archive_sha:
        raise PortabilityError("P7.03 backup verification did not reproduce archive digest")

    _private_dir(off_host)
    package_archive = off_host / archive.name
    package_checksum = off_host / (archive.name + ".sha256")
    shutil.copyfile(archive, package_archive)
    shutil.copyfile(archive.with_name(archive.name + ".sha256"), package_checksum)
    _private_file(package_archive)
    _private_file(package_checksum)
    transferred = p703.verify_backup(package_archive)
    if transferred.get("archive_sha256") != archive_sha:
        raise PortabilityError("off-host transfer changed backup archive bytes")

    source_identity = path_identity(source_lex)
    manifest = {
        "schema": HANDOFF_SCHEMA,
        "scope": "P7.10 internal portability proof; no Production, lifecycle, support, or public API claim",
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "tool_release_sha": release_sha,
        "source_host": _host_context(host_marker),
        "source_root": source_identity,
        "path_portability": {
            "comparison_rule": "filesystem identity/physical resolution for host path equivalence; lexical path retained as evidence",
            "lexical_physical_alias_observed": source_identity["lexical_differs_from_physical"],
            "var_symlink_discrepancy_disposition": "path-presentation alias when same filesystem object; not normalized away and not treated as semantic state identity",
        },
        "backup": {
            "archive_name": package_archive.name,
            "archive_sha256": archive_sha,
            "checksum_name": package_checksum.name,
            "p7_03_integrity": transferred["integrity"],
        },
        "semantic_evidence": {
            "governed_state_sha256": state_digest,
            "selected_historical_record": historical,
        },
        "authority_and_exclusions": {
            "canonical_authority_claim_created_by_export": False,
            "reusable_secrets_included": False,
            "telemetry_included": False,
            "runtime_cache_logs_included": False,
            "external_effect_replay_authorized": False,
            "secrets_reprovision_required": True,
        },
        "host_specific_configuration": [
            "absolute runtime root is deployment-local and is not semantic identity",
            "service-manager/login persistence is host-specific and must be re-established separately",
            "credentials/secrets are non-exportable and must be reprovisioned separately",
            "network/proxy/TLS adapters remain environment-specific",
        ],
    }
    _write_manifest_with_checksum(off_host, manifest)
    return manifest


def verify_handoff(package_dir: Path) -> Dict[str, Any]:
    package = _lexical_absolute(package_dir).resolve(strict=False)
    if not package.is_dir():
        raise PortabilityError(f"handoff package directory missing: {package_dir}")
    if os.name != "nt":
        package.chmod(0o700)
    manifest = _verify_manifest_checksum(package)
    if manifest.get("organization_scope") != p703.ORGANIZATION_SCOPE:
        raise PortabilityError("handoff Organization scope mismatch")
    authority = manifest.get("authority_and_exclusions")
    if not isinstance(authority, dict):
        raise PortabilityError("handoff authority/exclusions evidence missing")
    required_false = (
        "canonical_authority_claim_created_by_export",
        "reusable_secrets_included",
        "telemetry_included",
        "runtime_cache_logs_included",
        "external_effect_replay_authorized",
    )
    if any(authority.get(key) is not False for key in required_false):
        raise PortabilityError("handoff authority/exclusion boundary violated")
    if authority.get("secrets_reprovision_required") is not True:
        raise PortabilityError("handoff must require separate secret reprovisioning")

    backup = manifest.get("backup")
    if not isinstance(backup, dict):
        raise PortabilityError("handoff backup evidence missing")
    archive_name = backup.get("archive_name")
    checksum_name = backup.get("checksum_name")
    if not isinstance(archive_name, str) or not isinstance(checksum_name, str):
        raise PortabilityError("handoff backup filenames are invalid")
    if Path(archive_name).name != archive_name or checksum_name != archive_name + ".sha256":
        raise PortabilityError("handoff backup filenames escape or mismatch package boundary")
    archive = package / archive_name
    checksum = package / checksum_name
    if not archive.is_file() or not checksum.is_file():
        raise PortabilityError("handoff backup archive/checksum missing")
    _private_file(archive)
    _private_file(checksum)
    verified = p703.verify_backup(archive)
    if verified.get("archive_sha256") != backup.get("archive_sha256"):
        raise PortabilityError("handoff archive digest differs from manifest")
    if verified.get("reusable_secrets_included") is not False:
        raise PortabilityError("P7.03 backup secret boundary violated")
    return manifest


def restore_on_clean_environment(
    package_dir: Path,
    target_root: Path,
    release_sha: str,
    *,
    host_marker: str | None = None,
    receipt_path: Path | None = None,
) -> Dict[str, Any]:
    """Restore an off-host handoff into an absent target and verify semantics."""

    target_lex = _lexical_absolute(target_root)
    target = target_lex.resolve(strict=False)
    if target_lex.exists() or target.exists():
        raise PortabilityError(f"clean restore target must be absent: {target_lex}")

    manifest = verify_handoff(package_dir)
    if manifest.get("tool_release_sha") != release_sha:
        raise PortabilityError("restore release SHA does not match handoff tool release SHA")
    target_host = _host_context(host_marker)
    source_host = manifest.get("source_host")
    if not isinstance(source_host, dict) or not source_host.get("marker"):
        raise PortabilityError("source host evidence missing")
    if target_host["marker"] == source_host["marker"]:
        raise PortabilityError("host-loss proof requires a target host marker different from the source marker")

    package = _lexical_absolute(package_dir).resolve(strict=False)
    backup = manifest["backup"]
    archive = package / backup["archive_name"]
    restored = p703.restore_backup(archive, target)
    if restored.get("integrity") != "PASS":
        raise PortabilityError("restored P7.03 store integrity is not PASS")

    actual_digest = governed_state_digest(target)
    expected_semantic = manifest.get("semantic_evidence")
    if not isinstance(expected_semantic, dict):
        raise PortabilityError("handoff semantic evidence missing")
    if actual_digest != expected_semantic.get("governed_state_sha256"):
        raise PortabilityError("restored governed-state semantic digest mismatch")
    historical = selected_historical_evidence(target)
    if historical != expected_semantic.get("selected_historical_record"):
        raise PortabilityError("selected historical reconstruction mismatch")

    forbidden = [target / name for name in ("secrets", "run", "logs", "cache")]
    if any(path.exists() for path in forbidden):
        raise PortabilityError("clean restore recreated an explicitly excluded runtime/secrets path")

    target_identity = path_identity(target_lex)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "result": "PASS",
        "scope": "clean-environment semantic restore proof; technical recovery grants no Organizational Authority",
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "tool_release_sha": release_sha,
        "source_host": source_host,
        "target_host": target_host,
        "source_root": manifest.get("source_root"),
        "target_root": target_identity,
        "source_target_markers_distinct": True,
        "target_was_absent_before_restore": True,
        "archive_sha256": backup["archive_sha256"],
        "governed_state_sha256": actual_digest,
        "selected_historical_record": historical,
        "p7_03_integrity": restored["integrity"],
        "reusable_secrets_restored": False,
        "external_effect_replay_performed": False,
        "organizational_authority_granted_by_restore": False,
        "path_portability_disposition": manifest.get("path_portability"),
        "remaining_host_specific_configuration": manifest.get("host_specific_configuration"),
    }
    if receipt_path is not None:
        _atomic_json(_lexical_absolute(receipt_path), receipt)
    return receipt


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    prepare = sub.add_parser("prepare", help="prepare verified off-host handoff package")
    prepare.add_argument("--source-root", type=Path, required=True)
    prepare.add_argument("--off-host-dir", type=Path, required=True)
    prepare.add_argument("--release-sha", required=True)
    prepare.add_argument("--host-marker")

    verify = sub.add_parser("verify", help="verify transferred handoff package")
    verify.add_argument("--package-dir", type=Path, required=True)

    restore = sub.add_parser("restore", help="restore package into an absent clean target")
    restore.add_argument("--package-dir", type=Path, required=True)
    restore.add_argument("--target-root", type=Path, required=True)
    restore.add_argument("--release-sha", required=True)
    restore.add_argument("--host-marker")
    restore.add_argument("--receipt", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare_handoff(
                args.source_root,
                args.off_host_dir,
                args.release_sha,
                host_marker=args.host_marker,
            )
        elif args.command == "verify":
            result = verify_handoff(args.package_dir)
        else:
            result = restore_on_clean_environment(
                args.package_dir,
                args.target_root,
                args.release_sha,
                host_marker=args.host_marker,
                receipt_path=args.receipt,
            )
    except (PortabilityError, p703.BoundaryError, p703.IntegrityError, OSError, ValueError) as exc:
        print(json.dumps({"result": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
