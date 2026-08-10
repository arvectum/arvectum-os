#!/usr/bin/env python3
"""Recover the fixed P6.05-L3 legacy source set with one owner-authorized tender-app source.

This is a bounded continuation of the mixed-source recovery path. It permits exactly one
legacy env source owned by the known historical repository arutyunoveth/tender-app only
when the owner-operated invocation includes an explicit authorization assertion.

The helper does not generalize trust to tender-app, other repositories, or future files.
The tender-app source must be untracked, its origin must match exactly, and both its HEAD
and tracked Git state are captured before migration and required to remain unchanged.
The same invariants remain in force for all supplied ai-corporation checkouts.

Configured secret values are compared only in memory and must all agree before any new
destination is created or any source is scrubbed. No secret value or hash is emitted.
No product, EIS, SOAP, network, canonical-state, credential-lifecycle, or external action
is performed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_classify_known_legacy_owner as KNOWN
import p6_05_l3_recover_discovered_sources as BASE
import p6_05_l3_recover_mixed_legacy_sources as MIXED
import p6_05_l3_recover_verified_containers as VERIFIED

OWNER_AUTHORIZATION_VALUE = "OWNER_APPROVES_TENDER_APP_LEGACY_SECRET_SCRUB"


def _safe_bool(value: bool) -> str:
    return "true" if value else "false"


def _capture_one(repo: Path) -> BASE.GitSnapshot:
    head = MIXED._run_git(repo, "rev-parse", "HEAD")
    if head.returncode != 0 or not head.stdout.strip():
        raise BASE.RecoveryError("LEGACY_OWNER_HEAD_READ_FAILED")
    status = MIXED._run_git(repo, "status", "--porcelain=v1", "--untracked-files=no")
    if status.returncode != 0:
        raise BASE.RecoveryError("LEGACY_OWNER_TRACKED_STATUS_FAILED")
    return BASE.GitSnapshot(head=head.stdout.strip(), tracked_status=status.stdout)


def _classify_authorized_env(
    env: Path,
    checkouts: Sequence[Path],
    *,
    owner_authorization: str,
) -> tuple[Path, Path | None, str]:
    if not BASE._supported_legacy_env_filename(env):
        raise BASE.RecoveryError("UNSUPPORTED_LEGACY_ENV_FILENAME")
    if not env.is_file():
        raise BASE.RecoveryError("LEGACY_ENV_NOT_REGULAR_FILE")

    containers = [checkout for checkout in checkouts if BASE._is_relative_to(env, checkout)]
    if containers:
        checkout = max(containers, key=lambda path: len(path.parts))
        VERIFIED._verify_no_unsupplied_valid_nested_repo(env, checkout, checkouts)
        relative_env = env.relative_to(checkout)
        tracked = MIXED._run_git(checkout, "ls-files", "--", str(relative_env))
        if tracked.returncode != 0:
            raise BASE.RecoveryError("AI_CORPORATION_GIT_INSPECTION_FAILED")
        if tracked.stdout.strip():
            raise BASE.RecoveryError("LEGACY_ENV_TRACKED_BY_GIT")
        return env, checkout, "repo_local"

    owner = MIXED._nearest_valid_git_root(env.parent)
    if owner is None:
        return env, None, "standalone"

    remote = MIXED._run_git(owner, "remote", "get-url", "origin")
    if remote.returncode != 0 or not remote.stdout.strip():
        raise BASE.RecoveryError("UNVERIFIED_GIT_OWNER_ORIGIN_REQUIRED")
    if not KNOWN._remote_matches_repository(remote.stdout, KNOWN.TENDER_APP_REPOSITORY):
        raise BASE.RecoveryError("UNVERIFIED_GIT_OWNER_NOT_AUTHORIZED_TENDER_APP")
    if owner_authorization != OWNER_AUTHORIZATION_VALUE:
        raise BASE.RecoveryError("TENDER_APP_OWNER_AUTHORIZATION_REQUIRED")

    relative_env = env.relative_to(owner)
    tracked = MIXED._run_git(owner, "ls-files", "--", str(relative_env))
    if tracked.returncode != 0:
        raise BASE.RecoveryError("TENDER_APP_GIT_INSPECTION_FAILED")
    if tracked.stdout.strip():
        raise BASE.RecoveryError("TENDER_APP_LEGACY_ENV_TRACKED_BY_GIT")
    return env, owner, "authorized_tender_app"


def _safe_lines(
    *,
    status: str,
    checkout_count: int,
    env_count: int,
    remote_verified_count: int,
    repo_local_count: int,
    standalone_count: int,
    authorized_tender_app_count: int,
    env_untracked_count: int,
    tracked_dirty_before_count: int,
    tracked_state_unchanged: bool,
    tracked_head_unchanged: bool,
    tender_app_tracked_state_unchanged: bool,
    tender_app_head_unchanged: bool,
    owner_authorization_asserted: bool,
    remaining_secret_key_count: int | None,
    failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_owner_authorized_recovery_status={status}",
        f"source_checkout_count={checkout_count}",
        f"source_env_count={env_count}",
        f"source_remote_verified_count={remote_verified_count}",
        f"repo_local_source_count={repo_local_count}",
        f"standalone_source_count={standalone_count}",
        f"authorized_tender_app_source_count={authorized_tender_app_count}",
        f"source_env_untracked_count={env_untracked_count}",
        f"tracked_dirty_before_count={tracked_dirty_before_count}",
        f"tracked_state_unchanged={_safe_bool(tracked_state_unchanged)}",
        f"tracked_head_unchanged={_safe_bool(tracked_head_unchanged)}",
        f"tender_app_tracked_state_unchanged={_safe_bool(tender_app_tracked_state_unchanged)}",
        f"tender_app_head_unchanged={_safe_bool(tender_app_head_unchanged)}",
        f"owner_authorization_asserted={_safe_bool(owner_authorization_asserted)}",
        "preexisting_tracked_changes_modified=false" if tracked_state_unchanged and tender_app_tracked_state_unchanged else "preexisting_tracked_changes_modified=not-proven",
    ]
    if remaining_secret_key_count is not None:
        lines.append(f"source_envs_with_eis_key_remaining={remaining_secret_key_count}")
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    lines.extend((
        "secret_values_printed=false",
        "secret_values_hashed=false",
        "secret_values_committed=false",
        "backup_with_secret_created=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ))
    return lines


def recover(
    discovery_file: Path,
    destination: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
    owner_authorization: str,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    checkout_count = env_count = remote_verified_count = env_untracked_count = 0
    repo_local_count = standalone_count = authorized_tender_app_count = 0
    tracked_dirty_before_count = 0
    tracked_state_unchanged = tracked_head_unchanged = False
    tender_app_tracked_state_unchanged = tender_app_head_unchanged = False
    owner_authorization_asserted = owner_authorization == OWNER_AUTHORIZATION_VALUE
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

        remote_verified_count = VERIFIED._verify_checkouts(discovery.checkouts)

        classified: list[tuple[Path, Path | None]] = []
        tender_app_roots: list[Path] = []
        for env in discovery.envs:
            source, owner, category = _classify_authorized_env(
                env,
                discovery.checkouts,
                owner_authorization=owner_authorization,
            )
            classified.append((source, owner))
            if category == "repo_local":
                repo_local_count += 1
            elif category == "standalone":
                standalone_count += 1
            else:
                authorized_tender_app_count += 1
                assert owner is not None
                tender_app_roots.append(owner)

        if authorized_tender_app_count != 1 or len(set(tender_app_roots)) != 1:
            raise BASE.RecoveryError("EXPECTED_SINGLE_AUTHORIZED_TENDER_APP_SOURCE")
        if repo_local_count + standalone_count + authorized_tender_app_count != env_count:
            raise BASE.RecoveryError("SOURCE_CLASSIFICATION_INCOMPLETE")
        env_untracked_count = len(classified)

        tender_app_root = tender_app_roots[0]
        ai_before = MIXED._capture_snapshots(discovery.checkouts)
        tender_before = _capture_one(tender_app_root)
        tracked_dirty_before_count = sum(1 for snapshot in ai_before.values() if snapshot.tracked_status.strip())
        if tender_before.tracked_status.strip():
            tracked_dirty_before_count += 1

        verified_destination_roots = list(discovery.checkouts) + [tender_app_root]
        migration_rc, migration_lines = MIXED._migrate_classified(
            classified,
            destination,
            verified_checkouts=verified_destination_roots,
            arvectum_repo_root=(arvectum_repo_root or BASE._repo_root()).resolve(strict=True),
        )

        ai_after = MIXED._capture_snapshots(discovery.checkouts)
        tender_after = _capture_one(tender_app_root)
        tracked_state_unchanged = all(
            ai_after[c].tracked_status == ai_before[c].tracked_status for c in discovery.checkouts
        )
        tracked_head_unchanged = all(ai_after[c].head == ai_before[c].head for c in discovery.checkouts)
        tender_app_tracked_state_unchanged = tender_after.tracked_status == tender_before.tracked_status
        tender_app_head_unchanged = tender_after.head == tender_before.head
        remaining_secret_key_count = sum(1 for env in discovery.envs if BASE._contains_secret_key(env))

        if not tracked_state_unchanged:
            raise BASE.RecoveryError("TRACKED_STATE_CHANGED_DURING_MIGRATION")
        if not tracked_head_unchanged:
            raise BASE.RecoveryError("TRACKED_HEAD_CHANGED_DURING_MIGRATION")
        if not tender_app_tracked_state_unchanged:
            raise BASE.RecoveryError("TENDER_APP_TRACKED_STATE_CHANGED_DURING_MIGRATION")
        if not tender_app_head_unchanged:
            raise BASE.RecoveryError("TENDER_APP_HEAD_CHANGED_DURING_MIGRATION")
        if migration_rc != 0:
            return 2, tuple(
                _safe_lines(
                    status="FAIL",
                    failure_code="CANONICAL_MIGRATION_FAILED",
                    checkout_count=checkout_count,
                    env_count=env_count,
                    remote_verified_count=remote_verified_count,
                    repo_local_count=repo_local_count,
                    standalone_count=standalone_count,
                    authorized_tender_app_count=authorized_tender_app_count,
                    env_untracked_count=env_untracked_count,
                    tracked_dirty_before_count=tracked_dirty_before_count,
                    tracked_state_unchanged=True,
                    tracked_head_unchanged=True,
                    tender_app_tracked_state_unchanged=True,
                    tender_app_head_unchanged=True,
                    owner_authorization_asserted=owner_authorization_asserted,
                    remaining_secret_key_count=remaining_secret_key_count,
                )
                + list(migration_lines)
            )
        if remaining_secret_key_count != 0:
            raise BASE.RecoveryError("SOURCE_SCRUB_POSTCHECK_FAILED")

    except BASE.RecoveryError as exc:
        return 2, tuple(
            _safe_lines(
                status="FAIL",
                failure_code=exc.code,
                checkout_count=checkout_count,
                env_count=env_count,
                remote_verified_count=remote_verified_count,
                repo_local_count=repo_local_count,
                standalone_count=standalone_count,
                authorized_tender_app_count=authorized_tender_app_count,
                env_untracked_count=env_untracked_count,
                tracked_dirty_before_count=tracked_dirty_before_count,
                tracked_state_unchanged=tracked_state_unchanged,
                tracked_head_unchanged=tracked_head_unchanged,
                tender_app_tracked_state_unchanged=tender_app_tracked_state_unchanged,
                tender_app_head_unchanged=tender_app_head_unchanged,
                owner_authorization_asserted=owner_authorization_asserted,
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
            repo_local_count=repo_local_count,
            standalone_count=standalone_count,
            authorized_tender_app_count=authorized_tender_app_count,
            env_untracked_count=env_untracked_count,
            tracked_dirty_before_count=tracked_dirty_before_count,
            tracked_state_unchanged=True,
            tracked_head_unchanged=True,
            tender_app_tracked_state_unchanged=True,
            tender_app_head_unchanged=True,
            owner_authorization_asserted=True,
            remaining_secret_key_count=0,
        )
        + list(migration_lines)
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Recover the fixed P6.05-L3 source set with exactly one explicitly owner-authorized untracked tender-app legacy env."
    )
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    parser.add_argument("--owner-authorization", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = recover(
        args.discovery_file,
        args.destination,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
        owner_authorization=args.owner_authorization,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
