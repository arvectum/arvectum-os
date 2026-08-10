#!/usr/bin/env python3
"""Safely migrate one or more legacy repo-local EIS token copies into P6.05-L3.

The helper accepts an explicit set of verified product checkout/env pairs. It
compares secret values only in memory, writes or reuses one separate owner-only
destination outside source-controlled checkouts, then removes only the EIS token
assignment from every legacy source env that still contains it.

Secret values are never printed, hashed, exported to a child process, or
persisted as evidence. No network, EIS, product, canonical mutation, or external
action is performed.
"""

from __future__ import annotations

import argparse
import os
import secrets
import stat
import sys
import tempfile
from dataclasses import dataclass
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


@dataclass(frozen=True, slots=True)
class SourceState:
    source_env: Path
    checkout_root: Path
    original_text: str
    scrubbed_text: str
    secret_value: str | None


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
    source_checkout_roots: Sequence[Path],
    arvectum_repo_root: Path,
) -> tuple[Path, bool]:
    expanded = destination.expanduser()
    if expanded.is_symlink():
        raise MigrationError("DESTINATION_SYMLINK_NOT_ALLOWED")
    if expanded.parent.is_symlink():
        raise MigrationError("DESTINATION_DIRECTORY_SYMLINK_NOT_ALLOWED")

    resolved = expanded.resolve(strict=False)
    for checkout in source_checkout_roots:
        if _is_relative_to(resolved, checkout):
            raise MigrationError("DESTINATION_INSIDE_SOURCE_CHECKOUT")
    if _is_relative_to(resolved, arvectum_repo_root):
        raise MigrationError("DESTINATION_INSIDE_ARVECTUM_CHECKOUT")

    parent = resolved.parent
    if not parent.exists() or not parent.is_dir():
        raise MigrationError("DESTINATION_DIRECTORY_NOT_FOUND")
    directory_mode = stat.S_IMODE(parent.stat().st_mode)
    if not _owner_only(directory_mode):
        raise MigrationError("DESTINATION_DIRECTORY_PERMISSIONS_TOO_BROAD")

    if not resolved.exists():
        return resolved, False

    if not resolved.is_file():
        raise MigrationError("DESTINATION_NOT_REGULAR_FILE")
    if resolved.stat().st_size > MAX_LOCAL_FILE_BYTES:
        raise MigrationError("DESTINATION_TOO_LARGE")
    file_mode = stat.S_IMODE(resolved.stat().st_mode)
    if not _owner_only(file_mode):
        raise MigrationError("DESTINATION_PERMISSIONS_TOO_BROAD")
    return resolved, True


def _extract_optional_secret_and_scrubbed_text(text: str) -> tuple[str | None, str]:
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

    if matches > 1:
        raise MigrationError("SECRET_KEY_AMBIGUOUS", SECRET_ENV_KEY)
    if matches == 0:
        return None, text

    assert secret_value is not None
    if not secret_value or secret_value.lower() in PLACEHOLDER_SECRET_VALUES:
        raise MigrationError("SECRET_NOT_CONFIGURED", SECRET_ENV_KEY)
    if "\n" in secret_value or "\r" in secret_value:
        raise MigrationError("SECRET_FORMAT_INVALID", SECRET_ENV_KEY)

    return secret_value, "".join(retained)


def _extract_and_scrubbed_text(text: str) -> tuple[str, str]:
    secret_value, scrubbed = _extract_optional_secret_and_scrubbed_text(text)
    if secret_value is None:
        raise MigrationError("SECRET_KEY_NOT_FOUND", SECRET_ENV_KEY)
    return secret_value, scrubbed


def _read_source_state(source_env: Path, checkout: Path) -> SourceState:
    try:
        text = source_env.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationError("SOURCE_ENV_NOT_UTF8") from exc
    except OSError as exc:
        raise MigrationError("SOURCE_ENV_READ_FAILED") from exc
    secret_value, scrubbed_text = _extract_optional_secret_and_scrubbed_text(text)
    return SourceState(source_env, checkout, text, scrubbed_text, secret_value)


def _read_existing_destination(destination: Path) -> str:
    try:
        value = destination.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise MigrationError("DESTINATION_NOT_UTF8") from exc
    except OSError as exc:
        raise MigrationError("DESTINATION_READ_FAILED") from exc

    value = value.rstrip("\r\n")
    if not value or value.lower() in PLACEHOLDER_SECRET_VALUES:
        raise MigrationError("DESTINATION_SECRET_NOT_CONFIGURED", SECRET_ENV_KEY)
    if "\n" in value or "\r" in value:
        raise MigrationError("DESTINATION_SECRET_FORMAT_INVALID", SECRET_ENV_KEY)
    return value


def _same_secret(left: str, right: str) -> bool:
    return secrets.compare_digest(left.encode("utf-8"), right.encode("utf-8"))


def _write_new_secret(destination: Path, secret_value: str) -> None:
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(secret_value)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(destination, 0o600)
    except Exception:
        try:
            destination.unlink(missing_ok=True)
        finally:
            raise


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


def _safe_lines(
    *,
    status: str,
    failure: MigrationError | None = None,
    destination_created: bool = False,
    destination_reused: bool = False,
    source_count: int = 0,
    sources_with_secret_before: int = 0,
    sources_already_scrubbed_before: int = 0,
    sources_scrubbed: int = 0,
) -> list[str]:
    lines = [
        f"p6_05_l3_secret_migration_status={status}",
        "migration_scope=legacy_repo_local_eis_token_set_to_external_owner_only_file",
        f"source_count={source_count}",
        f"sources_with_secret_before={sources_with_secret_before}",
        f"sources_already_scrubbed_before={sources_already_scrubbed_before}",
        f"sources_scrubbed={sources_scrubbed}",
        f"destination_created={'true' if destination_created else 'false'}",
        f"destination_reused={'true' if destination_reused else 'false'}",
    ]
    if status == "PASS":
        lines.extend(
            (
                "all_source_secrets_consistent=true",
                "all_sources_scrubbed=true",
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


def migrate_secret_set(
    sources: Sequence[tuple[Path, Path]],
    destination: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    destination_created = False
    destination_reused = False
    source_count = len(sources)
    sources_with_secret_before = 0
    sources_already_scrubbed_before = 0
    sources_scrubbed = 0

    try:
        if not sources:
            raise MigrationError("SOURCE_SET_EMPTY")

        repo_root = (arvectum_repo_root or _repo_root()).resolve(strict=True)

        inspected: list[tuple[Path, Path]] = []
        seen_sources: set[Path] = set()
        for source_env, checkout_root in sources:
            source, checkout = _inspect_source(source_env, checkout_root)
            if source in seen_sources:
                raise MigrationError("SOURCE_ENV_DUPLICATED")
            seen_sources.add(source)
            inspected.append((source, checkout))

        target, target_exists = _inspect_destination(
            destination,
            source_checkout_roots=[checkout for _, checkout in inspected],
            arvectum_repo_root=repo_root,
        )

        states = [_read_source_state(source, checkout) for source, checkout in inspected]
        with_secret = [state for state in states if state.secret_value is not None]
        sources_with_secret_before = len(with_secret)
        sources_already_scrubbed_before = len(states) - sources_with_secret_before

        if target_exists:
            reference_secret = _read_existing_destination(target)
            destination_reused = True
        else:
            if not with_secret:
                raise MigrationError("SECRET_SOURCE_NOT_FOUND", SECRET_ENV_KEY)
            reference_secret = with_secret[0].secret_value
            assert reference_secret is not None

        for state in with_secret:
            assert state.secret_value is not None
            if not _same_secret(state.secret_value, reference_secret):
                raise MigrationError("SOURCE_SECRETS_DIFFER", SECRET_ENV_KEY)

        if not target_exists:
            _write_new_secret(target, reference_secret)
            destination_created = True

        for state in with_secret:
            try:
                _rewrite_source_without_secret(state.source_env, state.scrubbed_text)
            except Exception as exc:
                raise MigrationError("SOURCE_SCRUB_INCOMPLETE_DESTINATION_PRESERVED") from exc
            sources_scrubbed += 1

    except MigrationError as exc:
        return 2, tuple(
            _safe_lines(
                status="FAIL",
                failure=exc,
                destination_created=destination_created,
                destination_reused=destination_reused,
                source_count=source_count,
                sources_with_secret_before=sources_with_secret_before,
                sources_already_scrubbed_before=sources_already_scrubbed_before,
                sources_scrubbed=sources_scrubbed,
            )
        )
    except OSError:
        failure = MigrationError("LOCAL_FILESYSTEM_OPERATION_FAILED")
        return 2, tuple(
            _safe_lines(
                status="FAIL",
                failure=failure,
                destination_created=destination_created,
                destination_reused=destination_reused,
                source_count=source_count,
                sources_with_secret_before=sources_with_secret_before,
                sources_already_scrubbed_before=sources_already_scrubbed_before,
                sources_scrubbed=sources_scrubbed,
            )
        )

    return 0, tuple(
        _safe_lines(
            status="PASS",
            destination_created=destination_created,
            destination_reused=destination_reused,
            source_count=source_count,
            sources_with_secret_before=sources_with_secret_before,
            sources_already_scrubbed_before=sources_already_scrubbed_before,
            sources_scrubbed=sources_scrubbed,
        )
    )


def migrate_secret(
    source_env: Path,
    source_checkout_root: Path,
    destination: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    """Backward-compatible one-source API used by existing tests/callers."""
    return migrate_secret_set(
        [(source_env, source_checkout_root)],
        destination,
        arvectum_repo_root=arvectum_repo_root,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Migrate one or more legacy repo-local EIS token copies into the "
            "P6.05-L3 external secret boundary without printing or hashing them."
        )
    )
    parser.add_argument("--source-env", required=True, action="append", type=Path)
    parser.add_argument("--source-checkout-root", required=True, action="append", type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if len(args.source_env) != len(args.source_checkout_root):
        failure = MigrationError("SOURCE_PAIR_COUNT_MISMATCH")
        for line in _safe_lines(status="FAIL", failure=failure):
            print(line)
        return 2

    sources = list(zip(args.source_env, args.source_checkout_root, strict=True))
    rc, lines = migrate_secret_set(sources, args.destination)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
