#!/usr/bin/env python3
"""Safely migrate an existing repo-local EIS token into the P6.05-L3 secret boundary.

This helper exists only to unblock a legacy local state where an already-authorized
EIS token was stored in a product checkout's .env/.env.local file. It extracts the
exact token key in memory, writes it to a separate owner-only destination outside
both source-controlled checkouts, then removes only that key from the source env
file. The token value is never printed, hashed, exported to a child process, or
persisted as evidence.

No network, EIS, product, canonical mutation, or external action is performed.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Sequence

from p6_05_l3_secure_local_config import (
    MAX_LOCAL_FILE_BYTES,
    PLACEHOLDER_SECRET_VALUES,
    SECRET_ENV_KEY,
)


class MigrationError(RuntimeError):
    """Safe migration failure that never includes the secret value."""

    def __init__(self, code: str, subject: str | None = None) -> None:
        self.code = code
        self.subject = subject
        super().__init__(code if subject is None else f"{code}: {subject}")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _owner_only(mode: int) -> bool:
    return mode & 0o077 == 0


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _inspect_source(source_env: Path, source_checkout_root: Path) -> tuple[Path, Path]:
    checkout = source_checkout_root.expanduser().resolve(strict=True)
    if not checkout.is_dir():
        raise MigrationError("SOURCE_CHECKOUT_INVALID")

    expanded = source_env.expanduser()
    if expanded.is_symlink():
        raise MigrationError("SOURCE_ENV_SYMLINK_NOT_ALLOWED")
    if expanded.parent.is_symlink():
        raise MigrationError("SOURCE_ENV_DIRECTORY_SYMLINK_NOT_ALLOWED")

    resolved = expanded.resolve(strict=False)
    if not _is_relative_to(resolved, checkout):
        raise MigrationError("SOURCE_ENV_OUTSIDE_DECLARED_CHECKOUT")
    if not resolved.exists():
        raise MigrationError("SOURCE_ENV_NOT_FOUND")
    if not resolved.is_file():
        raise MigrationError("SOURCE_ENV_NOT_REGULAR_FILE")
    if resolved.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise MigrationError("SOURCE_ENV_TOO_LARGE")

    file_mode = stat.S_IMODE(resolved.stat().st_mode)
    if not _owner_only(file_mode):
        raise MigrationError("SOURCE_ENV_PERMISSIONS_TOO_BROAD")
    return resolved, checkout


def _inspect_destination(
    destination: Path,
    *,
    source_checkout_root: Path,
    arvectum_repo_root: Path,
) -> Path:
    expanded = destination.expanduser()
    if expanded.is_symlink():
        raise MigrationError("DESTINATION_SYMLINK_NOT_ALLOWED")
    if expanded.parent.is_symlink():
        raise MigrationError("DESTINATION_DIRECTORY_SYMLINK_NOT_ALLOWED")

    resolved = expanded.resolve(strict=False)
    if _is_relative_to(resolved, source_checkout_root):
        raise MigrationError("DESTINATION_INSIDE_SOURCE_CHECKOUT")
    if _is_relative_to(resolved, arvectum_repo_root):
        raise MigrationError("DESTINATION_INSIDE_ARVECTUM_CHECKOUT")
    if resolved.exists():
        raise MigrationError("DESTINATION_ALREADY_EXISTS")

    parent = resolved.parent
    if not parent.exists() or not parent.is_dir():
        raise MigrationError("DESTINATION_DIRECTORY_NOT_FOUND")
    directory_mode = stat.S_IMODE(parent.stat().st_mode)
    if not _owner_only(directory_mode):
        raise MigrationError("DESTINATION_DIRECTORY_PERMISSIONS_TOO_BROAD")
    return resolved


def _extract_and_scrubbed_text(text: str) -> tuple[str, str]:
    matches = 0
    secret_value: str | None = None
    retained: list[str] = []

    for raw_line in text.splitlines(keepends=True):
        stripped = raw_line.strip()
        candidate = stripped
        if candidate.startswith("export "):
            candidate = candidate[7:].lstrip()
        if candidate and not candidate.startswith("#") and "=" in candidate:
            key, raw_value = candidate.split("=", 1)
            if key.strip() == SECRET_ENV_KEY:
                matches += 1
                secret_value = _unquote(raw_value.strip())
                continue
        retained.append(raw_line)

    if matches == 0:
        raise MigrationError("SECRET_KEY_NOT_FOUND", SECRET_ENV_KEY)
    if matches != 1:
        raise MigrationError("SECRET_KEY_AMBIGUOUS", SECRET_ENV_KEY)
    assert secret_value is not None
    if not secret_value or secret_value.lower() in PLACEHOLDER_SECRET_VALUES:
        raise MigrationError("SECRET_NOT_CONFIGURED", SECRET_ENV_KEY)
    if "\n" in secret_value or "\r" in secret_value:
        raise MigrationError("SECRET_FORMAT_INVALID", SECRET_ENV_KEY)

    return secret_value, "".join(retained)


def _write_new_secret(destination: Path, secret_value: str) -> None:
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(secret_value)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except Exception:
        try:
            destination.unlink(missing_ok=True)
        finally:
            raise
    os.chmod(destination, 0o600)


def _rewrite_source_without_secret(source_env: Path, scrubbed_text: str) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=".p6-05-l3-migrate-", dir=source_env.parent)
    tmp_path = Path(tmp_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(scrubbed_text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, source_env)
        os.chmod(source_env, 0o600)
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        finally:
            raise


def _safe_lines(*, status: str, failure: MigrationError | None = None, destination_created: bool = False) -> list[str]:
    lines = [
        f"p6_05_l3_secret_migration_status={status}",
        "migration_scope=legacy_repo_local_eis_token_to_external_owner_only_file",
        f"destination_created={'true' if destination_created else 'false'}",
    ]
    if status == "PASS":
        lines.extend(
            (
                "source_secret_detected=true",
                "source_secret_removed=true",
                "destination_owner_only=true",
                f"secret.{SECRET_ENV_KEY}=configured",
            )
        )
    elif failure is not None:
        lines.append(f"failure_code={failure.code}")
        if failure.subject:
            lines.append(f"failure_subject={failure.subject}")
    lines.extend(
        (
            "secret_values_printed=false",
            "secret_values_hashed=false",
            "secret_values_exported=false",
            "secret_values_persisted_as_evidence=false",
            "backup_with_secret_created=false",
            "product_invoked=false",
            "eis_invoked=false",
            "network_invoked=false",
            "external_actions=false",
        )
    )
    return lines


def migrate_secret(
    source_env: Path,
    source_checkout_root: Path,
    destination: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    destination_created = False
    try:
        repo_root = (arvectum_repo_root or _repo_root()).resolve(strict=True)
        source, checkout = _inspect_source(source_env, source_checkout_root)
        target = _inspect_destination(
            destination,
            source_checkout_root=checkout,
            arvectum_repo_root=repo_root,
        )
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise MigrationError("SOURCE_ENV_NOT_UTF8") from exc
        except OSError as exc:
            raise MigrationError("SOURCE_ENV_READ_FAILED") from exc

        secret_value, scrubbed_text = _extract_and_scrubbed_text(text)
        _write_new_secret(target, secret_value)
        destination_created = True
        try:
            _rewrite_source_without_secret(source, scrubbed_text)
        except Exception as exc:
            try:
                target.unlink(missing_ok=True)
                destination_created = False
            except OSError as rollback_exc:
                raise MigrationError("SOURCE_SCRUB_FAILED_ROLLBACK_INCOMPLETE") from rollback_exc
            raise MigrationError("SOURCE_SCRUB_FAILED_ROLLED_BACK") from exc
    except MigrationError as exc:
        return 2, tuple(_safe_lines(status="FAIL", failure=exc, destination_created=destination_created))
    except OSError as exc:
        failure = MigrationError("LOCAL_FILESYSTEM_OPERATION_FAILED")
        return 2, tuple(_safe_lines(status="FAIL", failure=failure, destination_created=destination_created))

    return 0, tuple(_safe_lines(status="PASS", destination_created=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Migrate a legacy repo-local EIS token into the P6.05-L3 external secret boundary without printing it."
    )
    parser.add_argument("--source-env", required=True, type=Path)
    parser.add_argument("--source-checkout-root", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = migrate_secret(args.source_env, args.source_checkout_root, args.destination)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
