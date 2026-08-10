#!/usr/bin/env python3
"""Recover the discovered P6.05-L3 secret set through verified checkout containers.

This bounded owner-operated helper is the recovery path for local layouts where
running Git discovery from a legacy env directory is unreliable (for example
because of an orphaned/broken nested .git marker or ambient Git location
variables). It never treats such a failure as permission to discover arbitrary
repositories.

Every supplied checkout is independently verified as an ai-corporation worktree
root. Each env is then attached to the most specific verified checkout that
contains it. A valid intervening Git worktree not present in the supplied set
still fails closed. Invalid/orphaned non-symlink .git markers are treated only as
local filesystem debris; they do not override the explicit verified-container
boundary. The legacy env must remain untracked by its selected checkout.

Paths, diffs, remotes, secret values, hashes and environment contents are never
emitted. No product, EIS, network, canonical-state or external action occurs.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_migrate_eis_secret as MIGRATION
import p6_05_l3_recover_discovered_sources as BASE


_GIT_LOCATION_ENV_KEYS = {
    "GIT_DIR",
    "GIT_WORK_TREE",
    "GIT_COMMON_DIR",
    "GIT_INDEX_FILE",
    "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    "GIT_CEILING_DIRECTORIES",
    "GIT_DISCOVERY_ACROSS_FILESYSTEM",
    "GIT_PREFIX",
    "GIT_NAMESPACE",
}


def _sanitized_git_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in _GIT_LOCATION_ENV_KEYS:
        env.pop(key, None)
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def _run_git(checkout: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(checkout), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        env=_sanitized_git_env(),
    )


def _git_worktree_root(path: Path) -> Path:
    probe = _run_git(path, "rev-parse", "--show-toplevel")
    if probe.returncode != 0 or not probe.stdout.strip():
        raise BASE.RecoveryError("GIT_WORKTREE_ROOT_NOT_VERIFIED")
    try:
        return Path(probe.stdout.strip()).resolve(strict=True)
    except OSError as exc:
        raise BASE.RecoveryError("GIT_WORKTREE_ROOT_NOT_VERIFIED") from exc


def _verify_checkouts(checkouts: Sequence[Path]) -> int:
    verified = 0
    for checkout in checkouts:
        if not checkout.is_dir():
            raise BASE.RecoveryError("SOURCE_CHECKOUT_INVALID")
        if _git_worktree_root(checkout) != checkout:
            raise BASE.RecoveryError("AI_CORPORATION_CHECKOUT_NOT_WORKTREE_ROOT")
        remote = _run_git(checkout, "remote", "get-url", "origin")
        if remote.returncode != 0 or not BASE._remote_matches_target(remote.stdout):
            raise BASE.RecoveryError("AI_CORPORATION_REMOTE_NOT_VERIFIED")
        verified += 1
    return verified


def _deepest_verified_container(env: Path, checkouts: Sequence[Path]) -> Path:
    candidates = [checkout for checkout in checkouts if BASE._is_relative_to(env, checkout)]
    if not candidates:
        raise BASE.RecoveryError("ENV_OUTSIDE_VERIFIED_CHECKOUTS")
    return max(candidates, key=lambda path: len(path.parts))


def _verify_no_unsupplied_valid_nested_repo(
    env: Path,
    selected: Path,
    checkouts: Sequence[Path],
) -> None:
    """Reject valid intervening repos; tolerate only invalid non-symlink markers."""
    checkout_set = set(checkouts)
    current = env.parent

    while current != selected:
        marker = current / ".git"
        if marker.is_symlink():
            raise BASE.RecoveryError("ENV_INTERVENING_GIT_SYMLINK_NOT_ALLOWED")
        if marker.exists():
            probe = _run_git(current, "rev-parse", "--show-toplevel")
            if probe.returncode == 0 and probe.stdout.strip():
                try:
                    owner = Path(probe.stdout.strip()).resolve(strict=True)
                except OSError as exc:
                    raise BASE.RecoveryError("ENV_GIT_OWNER_NOT_IN_DISCOVERY") from exc
                if owner not in checkout_set:
                    raise BASE.RecoveryError("ENV_GIT_OWNER_NOT_IN_DISCOVERY")
                if owner != selected:
                    raise BASE.RecoveryError("ENV_VERIFIED_CONTAINER_MAPPING_INCONSISTENT")
            # A non-symlink marker that Git cannot resolve is not a verified repo
            # boundary. The explicitly verified container remains the bounded
            # source owner for this migration-only operation.

        parent = current.parent
        if parent == current:
            raise BASE.RecoveryError("ENV_VERIFIED_CONTAINER_MAPPING_INCONSISTENT")
        current = parent


def _map_envs_to_checkouts(
    envs: Sequence[Path],
    checkouts: Sequence[Path],
) -> tuple[tuple[Path, Path], ...]:
    pairs: list[tuple[Path, Path]] = []

    for env in envs:
        if not BASE._supported_legacy_env_filename(env):
            raise BASE.RecoveryError("UNSUPPORTED_LEGACY_ENV_FILENAME")
        if not env.is_file():
            raise BASE.RecoveryError("LEGACY_ENV_NOT_REGULAR_FILE")

        checkout = _deepest_verified_container(env, checkouts)
        _verify_no_unsupplied_valid_nested_repo(env, checkout, checkouts)
        if not BASE._is_relative_to(env, checkout):
            raise BASE.RecoveryError("ENV_VERIFIED_CONTAINER_MAPPING_INCONSISTENT")

        relative_env = env.relative_to(checkout)
        tracked = _run_git(checkout, "ls-files", "--", str(relative_env))
        if tracked.returncode != 0:
            raise BASE.RecoveryError("AI_CORPORATION_GIT_INSPECTION_FAILED")
        if tracked.stdout.strip():
            raise BASE.RecoveryError("LEGACY_ENV_TRACKED_BY_GIT")

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
            raise BASE.RecoveryError("LEGACY_ENV_CHMOD_FAILED") from exc
        pairs.append((env, checkout))

    return tuple(pairs)


def _snapshot(checkout: Path) -> BASE.GitSnapshot:
    head = _run_git(checkout, "rev-parse", "HEAD")
    if head.returncode != 0 or not head.stdout.strip():
        raise BASE.RecoveryError("AI_CORPORATION_HEAD_READ_FAILED")
    status = _run_git(checkout, "status", "--porcelain=v1", "--untracked-files=no")
    if status.returncode != 0:
        raise BASE.RecoveryError("AI_CORPORATION_TRACKED_STATUS_FAILED")
    return BASE.GitSnapshot(head=head.stdout.strip(), tracked_status=status.stdout)


def _capture_snapshots(checkouts: Sequence[Path]) -> dict[Path, BASE.GitSnapshot]:
    return {checkout: _snapshot(checkout) for checkout in checkouts}


def recover_verified_containers(
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

    try:
        if expected_checkout_count <= 0 or expected_env_count <= 0:
            raise BASE.RecoveryError("EXPECTED_SOURCE_COUNT_INVALID")

        discovery = BASE._parse_discovery(BASE._inspect_discovery_file(discovery_file))
        checkout_count = len(discovery.checkouts)
        env_count = len(discovery.envs)
        if checkout_count != expected_checkout_count:
            raise BASE.RecoveryError("SOURCE_CHECKOUT_COUNT_CHANGED")
        if env_count != expected_env_count:
            raise BASE.RecoveryError("SOURCE_ENV_COUNT_CHANGED")

        remote_verified_count = _verify_checkouts(discovery.checkouts)
        pairs = _map_envs_to_checkouts(discovery.envs, discovery.checkouts)
        env_untracked_count = len(pairs)

        before = _capture_snapshots(discovery.checkouts)
        tracked_dirty_before_count = sum(
            1 for snapshot in before.values() if snapshot.tracked_status.strip()
        )

        try:
            migration_rc, migration_lines = MIGRATION.migrate_secret_set(
                pairs,
                destination,
                arvectum_repo_root=(arvectum_repo_root or BASE._repo_root()),
            )
        except Exception as exc:
            raise BASE.RecoveryError("CANONICAL_MIGRATION_EXECUTION_FAILED") from exc

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
            1 for env in discovery.envs if BASE._contains_secret_key(env)
        )

        if not tracked_state_unchanged:
            raise BASE.RecoveryError("TRACKED_STATE_CHANGED_DURING_MIGRATION")
        if not tracked_head_unchanged:
            raise BASE.RecoveryError("TRACKED_HEAD_CHANGED_DURING_MIGRATION")
        if migration_rc != 0:
            return 2, tuple(
                BASE._safe_lines(
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
            raise BASE.RecoveryError("SOURCE_SCRUB_POSTCHECK_FAILED")

    except BASE.RecoveryError as exc:
        return 2, tuple(
            BASE._safe_lines(
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
        BASE._safe_lines(
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
            "Recover the complete P6.05-L3 discovered legacy EIS secret set "
            "through independently verified checkout containers."
        )
    )
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = recover_verified_containers(
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
