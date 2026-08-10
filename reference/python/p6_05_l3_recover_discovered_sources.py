#!/usr/bin/env python3
"""Recover a discovered multi-checkout legacy EIS secret set without requiring clean trees.

This bounded P6.05-L3 helper consumes a local-only discovery manifest containing
verified candidate checkout and env paths. It validates repository identity and
that legacy env files are untracked, captures each checkout's tracked Git state
in memory, performs the canonical multi-source secret migration, then proves that
tracked state and HEADs are unchanged.

Pre-existing tracked dirtiness is allowed because L3 does not own or repair it;
only new tracked changes caused during this recovery are forbidden. Paths, diffs,
secret values, hashes, remote URLs and environment contents are never emitted.

No product, EIS, network, canonical-state or external action is performed.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import p6_05_l3_migrate_eis_secret as MIGRATION


TARGET_REPOSITORY = "arutyunoveth/ai-corporation"
SUPPORTED_ENV_NAMES = frozenset({".env", ".env.local"})
MAX_DISCOVERY_BYTES = 1024 * 1024


class RecoveryError(RuntimeError):
    """Safe recovery failure that never includes a path, diff, remote or secret."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class GitSnapshot:
    head: str
    tracked_status: str


@dataclass(frozen=True, slots=True)
class DiscoverySet:
    checkouts: tuple[Path, ...]
    envs: tuple[Path, ...]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _run_git(checkout: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(checkout), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )


def _normalize_remote(value: str) -> str:
    normalized = value.strip().lower().rstrip("/")
    if normalized.endswith(".git"):
        normalized = normalized[:-4]
    return normalized


def _remote_matches_target(value: str) -> bool:
    normalized = _normalize_remote(value)
    return normalized in {
        f"https://github.com/{TARGET_REPOSITORY}",
        f"git@github.com:{TARGET_REPOSITORY}",
        f"ssh://git@github.com/{TARGET_REPOSITORY}",
    }


def _inspect_discovery_file(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.is_symlink():
        raise RecoveryError("DISCOVERY_SYMLINK_NOT_ALLOWED")
    resolved = expanded.resolve(strict=False)
    if not resolved.exists() or not resolved.is_file():
        raise RecoveryError("DISCOVERY_FILE_NOT_FOUND")
    if resolved.stat().st_size > MAX_DISCOVERY_BYTES:
        raise RecoveryError("DISCOVERY_FILE_TOO_LARGE")
    return resolved


def _parse_discovery(path: Path) -> DiscoverySet:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise RecoveryError("DISCOVERY_FILE_NOT_UTF8") from exc
    except OSError as exc:
        raise RecoveryError("DISCOVERY_FILE_READ_FAILED") from exc

    checkouts: set[Path] = set()
    envs: set[Path] = set()

    for line in lines:
        if line.startswith("AI_CORPORATION_CHECKOUT="):
            raw = line.split("=", 1)[1]
            try:
                checkouts.add(Path(raw).expanduser().resolve(strict=True))
            except OSError as exc:
                raise RecoveryError("DISCOVERED_CHECKOUT_INVALID") from exc
        elif line.startswith("ENV_WITH_EIS_KEY="):
            raw = line.split("=", 1)[1]
            try:
                envs.add(Path(raw).expanduser().resolve(strict=True))
            except OSError as exc:
                raise RecoveryError("DISCOVERED_ENV_INVALID") from exc

    return DiscoverySet(
        checkouts=tuple(sorted(checkouts)),
        envs=tuple(sorted(envs)),
    )


def _verify_checkouts(checkouts: Sequence[Path]) -> int:
    verified = 0
    for checkout in checkouts:
        if not checkout.is_dir():
            raise RecoveryError("SOURCE_CHECKOUT_INVALID")
        remote = _run_git(checkout, "remote", "get-url", "origin")
        if remote.returncode != 0 or not _remote_matches_target(remote.stdout):
            raise RecoveryError("AI_CORPORATION_REMOTE_NOT_VERIFIED")
        verified += 1
    return verified


def _map_envs_to_checkouts(
    envs: Sequence[Path],
    checkouts: Sequence[Path],
) -> tuple[tuple[Path, Path], ...]:
    pairs: list[tuple[Path, Path]] = []
    for env in envs:
        if env.name not in SUPPORTED_ENV_NAMES:
            raise RecoveryError("UNSUPPORTED_LEGACY_ENV_FILENAME")
        if env.is_symlink() or not env.is_file():
            raise RecoveryError("LEGACY_ENV_NOT_REGULAR_FILE")

        matches = [checkout for checkout in checkouts if _is_relative_to(env, checkout)]
        if len(matches) != 1:
            raise RecoveryError("ENV_CHECKOUT_MAPPING_AMBIGUOUS")

        checkout = matches[0]
        relative_env = env.relative_to(checkout)
        tracked = _run_git(checkout, "ls-files", "--", str(relative_env))
        if tracked.returncode != 0:
            raise RecoveryError("AI_CORPORATION_GIT_INSPECTION_FAILED")
        if tracked.stdout.strip():
            raise RecoveryError("LEGACY_ENV_TRACKED_BY_GIT")

        if sys.platform == "darwin":
            subprocess.run(
                ["chmod", "-N", str(env)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
        try:
            os.chmod(env, 0o600)
        except OSError as exc:
            raise RecoveryError("LEGACY_ENV_CHMOD_FAILED") from exc
        pairs.append((env, checkout))

    return tuple(pairs)


def _snapshot(checkout: Path) -> GitSnapshot:
    head = _run_git(checkout, "rev-parse", "HEAD")
    if head.returncode != 0 or not head.stdout.strip():
        raise RecoveryError("AI_CORPORATION_HEAD_READ_FAILED")
    status = _run_git(
        checkout,
        "status",
        "--porcelain=v1",
        "--untracked-files=no",
    )
    if status.returncode != 0:
        raise RecoveryError("AI_CORPORATION_TRACKED_STATUS_FAILED")
    return GitSnapshot(head=head.stdout.strip(), tracked_status=status.stdout)


def _capture_snapshots(checkouts: Sequence[Path]) -> dict[Path, GitSnapshot]:
    return {checkout: _snapshot(checkout) for checkout in checkouts}


def _contains_secret_key(env: Path) -> bool:
    try:
        text = env.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise RecoveryError("POSTCHECK_ENV_NOT_UTF8") from exc
    except OSError as exc:
        raise RecoveryError("POSTCHECK_ENV_READ_FAILED") from exc

    for raw_line in text.splitlines():
        candidate = raw_line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        if candidate.startswith("export "):
            candidate = candidate[7:].lstrip()
        if "=" not in candidate:
            continue
        key, _ = candidate.split("=", 1)
        if key.strip() == MIGRATION.SECRET_ENV_KEY:
            return True
    return False


def _safe_lines(
    *,
    status: str,
    failure_code: str | None = None,
    checkout_count: int = 0,
    env_count: int = 0,
    remote_verified_count: int = 0,
    env_untracked_count: int = 0,
    tracked_dirty_before_count: int = 0,
    tracked_state_unchanged: bool = False,
    tracked_head_unchanged: bool = False,
    remaining_secret_key_count: int | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_discovered_source_recovery_status={status}",
        f"source_checkout_count={checkout_count}",
        f"source_env_count={env_count}",
        f"source_remote_verified_count={remote_verified_count}",
        f"source_env_untracked_count={env_untracked_count}",
        f"tracked_dirty_before_count={tracked_dirty_before_count}",
        f"tracked_state_unchanged={'true' if tracked_state_unchanged else 'false'}",
        f"tracked_head_unchanged={'true' if tracked_head_unchanged else 'false'}",
    ]
    if remaining_secret_key_count is not None:
        lines.append(f"source_envs_with_eis_key_remaining={remaining_secret_key_count}")
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    lines.extend(
        (
            "preexisting_tracked_changes_modified=false" if tracked_state_unchanged else "preexisting_tracked_changes_modified=not-proven",
            "secret_values_printed=false",
            "secret_values_hashed=false",
            "secret_values_committed=false",
            "product_invoked=false",
            "eis_invoked=false",
            "network_invoked=false",
            "external_actions=false",
        )
    )
    return lines


def recover_discovered_sources(
    discovery_file: Path,
    destination: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    checkout_count = 0
    env_count = 0
    remote_verified_count = 0
    env_untracked_count = 0
    tracked_dirty_before_count = 0
    tracked_state_unchanged = False
    tracked_head_unchanged = False
    remaining_secret_key_count: int | None = None
    migration_lines: tuple[str, ...] = ()
    migration_rc = 2

    try:
        if expected_checkout_count <= 0 or expected_env_count <= 0:
            raise RecoveryError("EXPECTED_SOURCE_COUNT_INVALID")

        discovery = _parse_discovery(_inspect_discovery_file(discovery_file))
        checkout_count = len(discovery.checkouts)
        env_count = len(discovery.envs)
        if checkout_count != expected_checkout_count:
            raise RecoveryError("SOURCE_CHECKOUT_COUNT_CHANGED")
        if env_count != expected_env_count:
            raise RecoveryError("SOURCE_ENV_COUNT_CHANGED")

        remote_verified_count = _verify_checkouts(discovery.checkouts)
        pairs = _map_envs_to_checkouts(discovery.envs, discovery.checkouts)
        env_untracked_count = len(pairs)

        before = _capture_snapshots(discovery.checkouts)
        tracked_dirty_before_count = sum(
            1 for snapshot in before.values() if snapshot.tracked_status.strip()
        )

        migration_rc, migration_lines = MIGRATION.migrate_secret_set(
            pairs,
            destination,
            arvectum_repo_root=(arvectum_repo_root or _repo_root()),
        )

        after = _capture_snapshots(discovery.checkouts)
        tracked_state_unchanged = all(
            after[checkout].tracked_status == before[checkout].tracked_status
            for checkout in discovery.checkouts
        )
        tracked_head_unchanged = all(
            after[checkout].head == before[checkout].head
            for checkout in discovery.checkouts
        )

        remaining_secret_key_count = sum(
            1 for env in discovery.envs if _contains_secret_key(env)
        )

        if not tracked_state_unchanged:
            raise RecoveryError("TRACKED_STATE_CHANGED_DURING_MIGRATION")
        if not tracked_head_unchanged:
            raise RecoveryError("TRACKED_HEAD_CHANGED_DURING_MIGRATION")
        if migration_rc != 0:
            return 2, tuple(
                _safe_lines(
                    status="FAIL",
                    failure_code="CANONICAL_MIGRATION_FAILED",
                    checkout_count=checkout_count,
                    env_count=env_count,
                    remote_verified_count=remote_verified_count,
                    env_untracked_count=env_untracked_count,
                    tracked_dirty_before_count=tracked_dirty_before_count,
                    tracked_state_unchanged=True,
                    tracked_head_unchanged=True,
                    remaining_secret_key_count=remaining_secret_key_count,
                )
                + list(migration_lines)
            )
        if remaining_secret_key_count != 0:
            raise RecoveryError("SOURCE_SCRUB_POSTCHECK_FAILED")

    except RecoveryError as exc:
        return 2, tuple(
            _safe_lines(
                status="FAIL",
                failure_code=exc.code,
                checkout_count=checkout_count,
                env_count=env_count,
                remote_verified_count=remote_verified_count,
                env_untracked_count=env_untracked_count,
                tracked_dirty_before_count=tracked_dirty_before_count,
                tracked_state_unchanged=tracked_state_unchanged,
                tracked_head_unchanged=tracked_head_unchanged,
                remaining_secret_key_count=remaining_secret_key_count,
            )
            + list(migration_lines)
        )

    return 0, tuple(
        _safe_lines(
            status="PASS",
            checkout_count=checkout_count,
            env_count=env_count,
            remote_verified_count=remote_verified_count,
            env_untracked_count=env_untracked_count,
            tracked_dirty_before_count=tracked_dirty_before_count,
            tracked_state_unchanged=True,
            tracked_head_unchanged=True,
            remaining_secret_key_count=0,
        )
        + list(migration_lines)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Recover the complete discovered P6.05-L3 legacy EIS secret source set "
            "while proving tracked Git state is unchanged."
        )
    )
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = recover_discovered_sources(
        args.discovery_file,
        args.destination,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
