#!/usr/bin/env python3
"""Prepare the P6.05-L3 local operational root outside every Git worktree.

This helper creates only non-secret local structure: an owner-only operational
root, owner-only config/secrets/evidence directories, and the exact bounded
non-secret EIS configuration required by P6.05-L3. It never reads, writes,
prints, hashes, exports, or otherwise handles the EIS token.

The target root must be outside any valid Git worktree and outside the Arvectum
OS checkout. Existing structure is reused only when its type, permissions and
fixed non-secret config are already compliant. The secret destination may be
absent or may already exist as an owner-only regular file, but its contents are
never read here.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_recover_mixed_legacy_sources as MIXED
from p6_05_l3_secure_local_config import MAX_LOCAL_FILE_BYTES

EXPECTED_CONFIG = (
    "ZAKUPKI_GOV_RU_SOAP_ENABLED=1\n"
    "ZAKUPKI_GOV_RU_SOAP_TOKEN_OWNER=individual\n"
    "ZAKUPKI_GOV_RU_SOAP_DISABLE_PROXY_FOR_EIS=1\n"
    "ZAKUPKI_GOV_RU_SOAP_REQUIRE_DIRECT_RU_ROUTE=1\n"
    "ZAKUPKI_GOV_RU_SOAP_TRUST_ENV_PROXY=0\n"
    "ZAKUPKI_GOV_RU_SOAP_DEBUG=0\n"
)


class PrepareError(RuntimeError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _owner_only(mode: int) -> bool:
    return mode & 0o077 == 0


def _safe_bool(value: bool) -> str:
    return "true" if value else "false"


def _nearest_existing_ancestor(path: Path) -> Path:
    current = path
    while not current.exists():
        parent = current.parent
        if parent == current:
            raise PrepareError("TARGET_ROOT_EXISTING_ANCESTOR_NOT_FOUND")
        current = parent
    return current


def _assert_not_symlink(path: Path, code: str) -> None:
    if path.is_symlink():
        raise PrepareError(code)


def _ensure_owner_only_directory(path: Path, *, create: bool) -> bool:
    _assert_not_symlink(path, "TARGET_DIRECTORY_SYMLINK_NOT_ALLOWED")
    created = False
    if not path.exists():
        if not create:
            raise PrepareError("TARGET_DIRECTORY_NOT_FOUND")
        path.mkdir(mode=0o700)
        created = True
    if not path.is_dir():
        raise PrepareError("TARGET_DIRECTORY_NOT_DIRECTORY")
    os.chmod(path, 0o700)
    mode = stat.S_IMODE(path.stat().st_mode)
    if not _owner_only(mode):
        raise PrepareError("TARGET_DIRECTORY_PERMISSIONS_TOO_BROAD")
    return created


def _ensure_config(config_file: Path) -> tuple[bool, bool]:
    _assert_not_symlink(config_file, "CONFIG_SYMLINK_NOT_ALLOWED")
    created = False
    if not config_file.exists():
        fd = os.open(config_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(EXPECTED_CONFIG)
                handle.flush()
                os.fsync(handle.fileno())
            os.chmod(config_file, 0o600)
        except Exception:
            config_file.unlink(missing_ok=True)
            raise
        created = True
    if not config_file.is_file():
        raise PrepareError("CONFIG_NOT_REGULAR_FILE")
    if config_file.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise PrepareError("CONFIG_TOO_LARGE")
    if not _owner_only(stat.S_IMODE(config_file.stat().st_mode)):
        raise PrepareError("CONFIG_PERMISSIONS_TOO_BROAD")
    try:
        text = config_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise PrepareError("CONFIG_NOT_UTF8") from exc
    except OSError as exc:
        raise PrepareError("CONFIG_READ_FAILED") from exc
    if text != EXPECTED_CONFIG:
        raise PrepareError("CONFIG_CONTENT_MISMATCH")
    return created, True


def _inspect_secret_destination(secret_file: Path) -> tuple[bool, bool]:
    _assert_not_symlink(secret_file, "SECRET_DESTINATION_SYMLINK_NOT_ALLOWED")
    if not secret_file.exists():
        return False, True
    if not secret_file.is_file():
        raise PrepareError("SECRET_DESTINATION_NOT_REGULAR_FILE")
    if secret_file.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise PrepareError("SECRET_DESTINATION_TOO_LARGE")
    owner_only = _owner_only(stat.S_IMODE(secret_file.stat().st_mode))
    if not owner_only:
        raise PrepareError("SECRET_DESTINATION_PERMISSIONS_TOO_BROAD")
    return True, True


def prepare(
    target_root: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    root_created = config_dir_created = secret_dir_created = evidence_dir_created = False
    config_created = False
    root_outside_git = False
    config_exact = False
    secret_destination_exists = False
    secret_destination_owner_only_or_absent = False

    try:
        expanded = target_root.expanduser()
        _assert_not_symlink(expanded, "TARGET_ROOT_SYMLINK_NOT_ALLOWED")
        existing_ancestor = _nearest_existing_ancestor(expanded)
        _assert_not_symlink(existing_ancestor, "TARGET_EXISTING_ANCESTOR_SYMLINK_NOT_ALLOWED")

        nearest_git = MIXED._nearest_valid_git_root(existing_ancestor)
        if nearest_git is not None:
            raise PrepareError("TARGET_ROOT_INSIDE_GIT_WORKTREE")

        repo_root = (arvectum_repo_root or Path(__file__).resolve().parents[2]).resolve(strict=True)
        resolved = expanded.resolve(strict=False)
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            pass
        else:
            raise PrepareError("TARGET_ROOT_INSIDE_ARVECTUM_CHECKOUT")

        parent = resolved.parent
        if not parent.exists() or not parent.is_dir():
            raise PrepareError("TARGET_ROOT_PARENT_NOT_FOUND")
        _assert_not_symlink(parent, "TARGET_ROOT_PARENT_SYMLINK_NOT_ALLOWED")

        root_created = _ensure_owner_only_directory(resolved, create=True)
        config_dir = resolved / "local-config"
        secret_dir = resolved / "local-secrets"
        evidence_dir = resolved / "evidence" / "p6-05-l3"
        config_dir_created = _ensure_owner_only_directory(config_dir, create=True)
        secret_dir_created = _ensure_owner_only_directory(secret_dir, create=True)
        _ensure_owner_only_directory(resolved / "evidence", create=True)
        evidence_dir_created = _ensure_owner_only_directory(evidence_dir, create=True)

        config_created, config_exact = _ensure_config(config_dir / "p6-05-l3.env")
        secret_destination_exists, secret_destination_owner_only_or_absent = _inspect_secret_destination(
            secret_dir / "eis-soap-token"
        )

        root_outside_git = MIXED._nearest_valid_git_root(resolved) is None
        if not root_outside_git:
            raise PrepareError("TARGET_ROOT_GIT_BOUNDARY_CHANGED")

    except (PrepareError, OSError) as exc:
        code = exc.code if isinstance(exc, PrepareError) else "LOCAL_FILESYSTEM_OPERATION_FAILED"
        return 2, tuple(_safe_lines(
            status="FAIL",
            failure_code=code,
            root_created=root_created,
            config_dir_created=config_dir_created,
            secret_dir_created=secret_dir_created,
            evidence_dir_created=evidence_dir_created,
            config_created=config_created,
            root_outside_git=root_outside_git,
            config_exact=config_exact,
            secret_destination_exists=secret_destination_exists,
            secret_destination_owner_only_or_absent=secret_destination_owner_only_or_absent,
        ))

    return 0, tuple(_safe_lines(
        status="PASS",
        root_created=root_created,
        config_dir_created=config_dir_created,
        secret_dir_created=secret_dir_created,
        evidence_dir_created=evidence_dir_created,
        config_created=config_created,
        root_outside_git=True,
        config_exact=True,
        secret_destination_exists=secret_destination_exists,
        secret_destination_owner_only_or_absent=True,
    ))


def _safe_lines(
    *,
    status: str,
    root_created: bool,
    config_dir_created: bool,
    secret_dir_created: bool,
    evidence_dir_created: bool,
    config_created: bool,
    root_outside_git: bool,
    config_exact: bool,
    secret_destination_exists: bool,
    secret_destination_owner_only_or_absent: bool,
    failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_external_operational_root_status={status}",
        f"root_created={_safe_bool(root_created)}",
        f"config_directory_created={_safe_bool(config_dir_created)}",
        f"secret_directory_created={_safe_bool(secret_dir_created)}",
        f"evidence_directory_created={_safe_bool(evidence_dir_created)}",
        f"config_created={_safe_bool(config_created)}",
        f"operational_root_outside_git={_safe_bool(root_outside_git)}",
        f"config_exact_expected_nonsecret_content={_safe_bool(config_exact)}",
        f"secret_destination_exists={_safe_bool(secret_destination_exists)}",
        f"secret_destination_owner_only_or_absent={_safe_bool(secret_destination_owner_only_or_absent)}",
    ]
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    lines.extend((
        "secret_values_read=false",
        "secret_values_printed=false",
        "secret_values_hashed=false",
        "secret_values_exported=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ))
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare the owner-only P6.05-L3 operational root outside every Git worktree without handling secrets."
    )
    parser.add_argument("--target-root", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = prepare(args.target_root)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
