#!/usr/bin/env python3
"""Recover mixed repo-local and standalone P6.05-L3 legacy EIS sources.

The explicit owner-operated discovery manifest may contain legacy env files both
inside independently verified ai-corporation checkouts and outside every supplied
checkout. These are distinct source classes.

Repo-local sources are attached to the most specific verified checkout. A source
outside every verified checkout is accepted as standalone only when no valid Git
worktree owns it. Any valid unverified repository ownership fails closed.
Broken non-symlink .git debris is not authority, but ancestor inspection
continues so it cannot hide an outer valid repository.

Configured secret values are compared only in memory and must all agree before
any destination creation or source scrub. Standalone filesystem parents are not
pretended to be Git checkout roots, so destination exclusion remains limited to
actual verified product checkouts plus the Arvectum OS checkout.

Product HEAD/tracked state must remain exactly unchanged. Paths, remotes, diffs,
secret values, hashes and env contents are never emitted. No product, EIS, SOAP,
network, canonical-state or external action is performed.
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
import p6_05_l3_recover_verified_containers as VERIFIED


def _run_git(path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(path), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
        env=VERIFIED._sanitized_git_env(),
    )


def _nearest_valid_git_root(path: Path) -> Path | None:
    current = path
    while True:
        marker = current / ".git"
        if marker.is_symlink():
            raise BASE.RecoveryError("LEGACY_SOURCE_GIT_SYMLINK_NOT_ALLOWED")
        if marker.exists():
            probe = _run_git(current, "rev-parse", "--show-toplevel")
            if probe.returncode == 0 and probe.stdout.strip():
                try:
                    return Path(probe.stdout.strip()).resolve(strict=True)
                except OSError as exc:
                    raise BASE.RecoveryError("LEGACY_SOURCE_GIT_OWNER_NOT_VERIFIED") from exc
        parent = current.parent
        if parent == current:
            return None
        current = parent


def _classify_env(env: Path, checkouts: Sequence[Path]) -> tuple[Path, Path | None]:
    if not BASE._supported_legacy_env_filename(env):
        raise BASE.RecoveryError("UNSUPPORTED_LEGACY_ENV_FILENAME")
    if not env.is_file():
        raise BASE.RecoveryError("LEGACY_ENV_NOT_REGULAR_FILE")

    containers = [checkout for checkout in checkouts if BASE._is_relative_to(env, checkout)]
    if containers:
        checkout = max(containers, key=lambda path: len(path.parts))
        VERIFIED._verify_no_unsupplied_valid_nested_repo(env, checkout, checkouts)
        relative_env = env.relative_to(checkout)
        tracked = _run_git(checkout, "ls-files", "--", str(relative_env))
        if tracked.returncode != 0:
            raise BASE.RecoveryError("AI_CORPORATION_GIT_INSPECTION_FAILED")
        if tracked.stdout.strip():
            raise BASE.RecoveryError("LEGACY_ENV_TRACKED_BY_GIT")
        return env, checkout

    if _nearest_valid_git_root(env.parent) is not None:
        raise BASE.RecoveryError("STANDALONE_ENV_OWNED_BY_UNVERIFIED_GIT_REPO")
    return env, None


def _owner_only_source(env: Path) -> None:
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


def _capture_snapshots(checkouts: Sequence[Path]) -> dict[Path, BASE.GitSnapshot]:
    snapshots: dict[Path, BASE.GitSnapshot] = {}
    for checkout in checkouts:
        head = _run_git(checkout, "rev-parse", "HEAD")
        if head.returncode != 0 or not head.stdout.strip():
            raise BASE.RecoveryError("AI_CORPORATION_HEAD_READ_FAILED")
        status = _run_git(checkout, "status", "--porcelain=v1", "--untracked-files=no")
        if status.returncode != 0:
            raise BASE.RecoveryError("AI_CORPORATION_TRACKED_STATUS_FAILED")
        snapshots[checkout] = BASE.GitSnapshot(head=head.stdout.strip(), tracked_status=status.stdout)
    return snapshots


def _migrate_classified(
    classified: Sequence[tuple[Path, Path | None]],
    destination: Path,
    *,
    verified_checkouts: Sequence[Path],
    arvectum_repo_root: Path,
) -> tuple[int, tuple[str, ...]]:
    destination_created = False
    destination_reused = False
    sources_with_secret_before = 0
    sources_already_scrubbed_before = 0
    sources_scrubbed = 0

    try:
        if not classified:
            raise MIGRATION.MigrationError("SOURCE_SET_EMPTY")

        inspected: list[tuple[Path, Path]] = []
        seen: set[Path] = set()
        for env, checkout in classified:
            _owner_only_source(env)
            # Direct/parent symlinks were rejected while parsing the discovery
            # manifest. For repo-local sources preserve the original migration
            # containment check. Standalone sources use only a local state label;
            # their parent is not added to destination-exclusion roots.
            if checkout is not None:
                source, source_root = MIGRATION._inspect_source(env, checkout)
            else:
                if env.stat().st_size > MIGRATION.MAX_LOCAL_FILE_BYTES:
                    raise MIGRATION.MigrationError("SOURCE_ENV_TOO_LARGE")
                source, source_root = env, env.parent
            if source in seen:
                raise MIGRATION.MigrationError("SOURCE_ENV_DUPLICATED")
            seen.add(source)
            inspected.append((source, source_root))

        target, target_exists = MIGRATION._inspect_destination(
            destination,
            source_checkout_roots=list(verified_checkouts),
            arvectum_repo_root=arvectum_repo_root,
        )

        states = [MIGRATION._read_source_state(source, source_root) for source, source_root in inspected]
        with_secret = [state for state in states if state.secret_value is not None]
        sources_with_secret_before = len(with_secret)
        sources_already_scrubbed_before = len(states) - sources_with_secret_before

        if target_exists:
            reference_secret = MIGRATION._read_existing_destination(target)
            destination_reused = True
        else:
            if not with_secret:
                raise MIGRATION.MigrationError("SECRET_SOURCE_NOT_FOUND", MIGRATION.SECRET_ENV_KEY)
            reference_secret = with_secret[0].secret_value
            assert reference_secret is not None

        for state in with_secret:
            assert state.secret_value is not None
            if not MIGRATION._same_secret(state.secret_value, reference_secret):
                raise MIGRATION.MigrationError("SOURCE_SECRETS_DIFFER", MIGRATION.SECRET_ENV_KEY)

        if not target_exists:
            MIGRATION._write_new_secret(target, reference_secret)
            destination_created = True

        for state in with_secret:
            try:
                MIGRATION._rewrite_source_without_secret(state.source_env, state.scrubbed_text)
            except Exception as exc:
                raise MIGRATION.MigrationError("SOURCE_SCRUB_INCOMPLETE_DESTINATION_PRESERVED") from exc
            sources_scrubbed += 1

    except MIGRATION.MigrationError as exc:
        return 2, tuple(
            MIGRATION._safe_lines(
                status="FAIL",
                failure=exc,
                destination_created=destination_created,
                destination_reused=destination_reused,
                source_count=len(classified),
                sources_with_secret_before=sources_with_secret_before,
                sources_already_scrubbed_before=sources_already_scrubbed_before,
                sources_scrubbed=sources_scrubbed,
            )
        )
    except OSError:
        failure = MIGRATION.MigrationError("LOCAL_FILESYSTEM_OPERATION_FAILED")
        return 2, tuple(
            MIGRATION._safe_lines(
                status="FAIL",
                failure=failure,
                destination_created=destination_created,
                destination_reused=destination_reused,
                source_count=len(classified),
                sources_with_secret_before=sources_with_secret_before,
                sources_already_scrubbed_before=sources_already_scrubbed_before,
                sources_scrubbed=sources_scrubbed,
            )
        )

    return 0, tuple(
        MIGRATION._safe_lines(
            status="PASS",
            destination_created=destination_created,
            destination_reused=destination_reused,
            source_count=len(classified),
            sources_with_secret_before=sources_with_secret_before,
            sources_already_scrubbed_before=sources_already_scrubbed_before,
            sources_scrubbed=sources_scrubbed,
        )
    )


def _with_classification_counts(
    lines: list[str], *, repo_local_source_count: int, standalone_source_count: int
) -> list[str]:
    lines.insert(4, f"repo_local_source_count={repo_local_source_count}")
    lines.insert(5, f"standalone_source_count={standalone_source_count}")
    return lines


def recover_mixed_legacy_sources(
    discovery_file: Path,
    destination: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    checkout_count = env_count = remote_verified_count = env_untracked_count = 0
    repo_local_source_count = standalone_source_count = tracked_dirty_before_count = 0
    tracked_state_unchanged = tracked_head_unchanged = False
    remaining_secret_key_count: int | None = None
    migration_lines: tuple[str, ...] = ()

    try:
        if expected_checkout_count <= 0 or expected_env_count <= 0:
            raise BASE.RecoveryError("EXPECTED_SOURCE_COUNT_INVALID")

        discovery = BASE._parse_discovery(BASE._inspect_discovery_file(discovery_file))
        checkout_count, env_count = len(discovery.checkouts), len(discovery.envs)
        if checkout_count != expected_checkout_count:
            raise BASE.RecoveryError("SOURCE_CHECKOUT_COUNT_CHANGED")
        if env_count != expected_env_count:
            raise BASE.RecoveryError("SOURCE_ENV_COUNT_CHANGED")

        remote_verified_count = VERIFIED._verify_checkouts(discovery.checkouts)
        classified: list[tuple[Path, Path | None]] = []
        for env in discovery.envs:
            item = _classify_env(env, discovery.checkouts)
            classified.append(item)
            if item[1] is None:
                standalone_source_count += 1
            else:
                repo_local_source_count += 1
        env_untracked_count = len(classified)

        before = _capture_snapshots(discovery.checkouts)
        tracked_dirty_before_count = sum(1 for snapshot in before.values() if snapshot.tracked_status.strip())

        migration_rc, migration_lines = _migrate_classified(
            classified,
            destination,
            verified_checkouts=discovery.checkouts,
            arvectum_repo_root=(arvectum_repo_root or BASE._repo_root()).resolve(strict=True),
        )

        after = _capture_snapshots(discovery.checkouts)
        tracked_state_unchanged = all(after[c].tracked_status == before[c].tracked_status for c in discovery.checkouts)
        tracked_head_unchanged = all(after[c].head == before[c].head for c in discovery.checkouts)
        remaining_secret_key_count = sum(1 for env in discovery.envs if BASE._contains_secret_key(env))

        if not tracked_state_unchanged:
            raise BASE.RecoveryError("TRACKED_STATE_CHANGED_DURING_MIGRATION")
        if not tracked_head_unchanged:
            raise BASE.RecoveryError("TRACKED_HEAD_CHANGED_DURING_MIGRATION")
        if migration_rc != 0:
            lines = _with_classification_counts(
                BASE._safe_lines(
                    status="FAIL", failure_code="CANONICAL_MIGRATION_FAILED",
                    checkout_count=checkout_count, env_count=env_count,
                    remote_verified_count=remote_verified_count,
                    env_untracked_count=env_untracked_count,
                    tracked_dirty_before_count=tracked_dirty_before_count,
                    tracked_state_unchanged=True, tracked_head_unchanged=True,
                    remaining_secret_key_count=remaining_secret_key_count,
                ),
                repo_local_source_count=repo_local_source_count,
                standalone_source_count=standalone_source_count,
            )
            return 2, tuple(lines + list(migration_lines))
        if remaining_secret_key_count != 0:
            raise BASE.RecoveryError("SOURCE_SCRUB_POSTCHECK_FAILED")

    except BASE.RecoveryError as exc:
        lines = _with_classification_counts(
            BASE._safe_lines(
                status="FAIL", failure_code=exc.code,
                checkout_count=checkout_count, env_count=env_count,
                remote_verified_count=remote_verified_count,
                env_untracked_count=env_untracked_count,
                tracked_dirty_before_count=tracked_dirty_before_count,
                tracked_state_unchanged=tracked_state_unchanged,
                tracked_head_unchanged=tracked_head_unchanged,
                remaining_secret_key_count=remaining_secret_key_count,
            ),
            repo_local_source_count=repo_local_source_count,
            standalone_source_count=standalone_source_count,
        )
        return 2, tuple(lines + list(migration_lines))

    lines = _with_classification_counts(
        BASE._safe_lines(
            status="PASS", checkout_count=checkout_count, env_count=env_count,
            remote_verified_count=remote_verified_count,
            env_untracked_count=env_untracked_count,
            tracked_dirty_before_count=tracked_dirty_before_count,
            tracked_state_unchanged=True, tracked_head_unchanged=True,
            remaining_secret_key_count=0,
        ),
        repo_local_source_count=repo_local_source_count,
        standalone_source_count=standalone_source_count,
    )
    return 0, tuple(lines + list(migration_lines))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recover mixed repo-local and standalone P6.05-L3 legacy EIS sources.")
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = recover_mixed_legacy_sources(
        args.discovery_file, args.destination,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
