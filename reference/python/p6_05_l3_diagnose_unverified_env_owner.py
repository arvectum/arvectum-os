#!/usr/bin/env python3
"""Safely classify Git ownership for the explicit P6.05-L3 discovery manifest.

This diagnostic exists for the owner-operated L3 recovery path after a bounded
manifest was proven to contain an env source outside every supplied verified
ai-corporation checkout but inside another valid Git worktree.

The helper does not read env contents or secret values. It only uses the existing
manifest paths and local Git metadata to classify source ownership into safe
categories. It never emits paths, filenames, remote URLs, repository names other
than the fixed safe category labels, diffs, secret values or hashes.

No migration, chmod, source rewrite, product invocation, EIS/network operation or
external action occurs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_recover_discovered_sources as BASE
import p6_05_l3_recover_mixed_legacy_sources as MIXED
import p6_05_l3_recover_verified_containers as VERIFIED


ARVECTUM_OS_REPOSITORY = "arutyunoveth/arvectum-os"


class DiagnosticError(RuntimeError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _remote_matches_repository(value: str, repository: str) -> bool:
    normalized = BASE._normalize_remote(value)
    repository = repository.lower()
    return normalized in {
        f"https://github.com/{repository}",
        f"git@github.com:{repository}",
        f"ssh://git@github.com/{repository}",
    }


def diagnose(
    discovery_file: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
) -> tuple[int, tuple[str, ...]]:
    checkout_count = 0
    env_count = 0
    remote_verified_count = 0
    repo_local_count = 0
    standalone_count = 0
    unverified_git_count = 0
    owner_ai_corporation_count = 0
    owner_arvectum_os_count = 0
    owner_other_remote_count = 0
    owner_no_origin_count = 0
    owner_tracked_env_count = 0
    owner_untracked_env_count = 0

    try:
        if expected_checkout_count <= 0 or expected_env_count <= 0:
            raise DiagnosticError("EXPECTED_SOURCE_COUNT_INVALID")

        discovery = BASE._parse_discovery(BASE._inspect_discovery_file(discovery_file))
        checkout_count = len(discovery.checkouts)
        env_count = len(discovery.envs)
        if checkout_count != expected_checkout_count:
            raise DiagnosticError("SOURCE_CHECKOUT_COUNT_CHANGED")
        if env_count != expected_env_count:
            raise DiagnosticError("SOURCE_ENV_COUNT_CHANGED")

        try:
            remote_verified_count = VERIFIED._verify_checkouts(discovery.checkouts)
        except BASE.RecoveryError as exc:
            raise DiagnosticError(exc.code) from exc

        for env in discovery.envs:
            if not BASE._supported_legacy_env_filename(env) or not env.is_file():
                raise DiagnosticError("LEGACY_ENV_SCOPE_INVALID")

            containers = [
                checkout
                for checkout in discovery.checkouts
                if BASE._is_relative_to(env, checkout)
            ]
            if containers:
                repo_local_count += 1
                continue

            try:
                owner = MIXED._nearest_valid_git_root(env.parent)
            except BASE.RecoveryError as exc:
                raise DiagnosticError(exc.code) from exc

            if owner is None:
                standalone_count += 1
                continue

            if not BASE._is_relative_to(env, owner):
                raise DiagnosticError("UNVERIFIED_GIT_OWNER_PATH_MISMATCH")

            unverified_git_count += 1
            remote = MIXED._run_git(owner, "remote", "get-url", "origin")
            if remote.returncode != 0 or not remote.stdout.strip():
                owner_no_origin_count += 1
            elif BASE._remote_matches_target(remote.stdout):
                owner_ai_corporation_count += 1
            elif _remote_matches_repository(remote.stdout, ARVECTUM_OS_REPOSITORY):
                owner_arvectum_os_count += 1
            else:
                owner_other_remote_count += 1

            relative_env = env.relative_to(owner)
            tracked = MIXED._run_git(owner, "ls-files", "--", str(relative_env))
            if tracked.returncode != 0:
                raise DiagnosticError("UNVERIFIED_GIT_TRACKING_INSPECTION_FAILED")
            if tracked.stdout.strip():
                owner_tracked_env_count += 1
            else:
                owner_untracked_env_count += 1

        if repo_local_count + standalone_count + unverified_git_count != env_count:
            raise DiagnosticError("SOURCE_CLASSIFICATION_INCOMPLETE")
        if (
            owner_ai_corporation_count
            + owner_arvectum_os_count
            + owner_other_remote_count
            + owner_no_origin_count
            != unverified_git_count
        ):
            raise DiagnosticError("UNVERIFIED_OWNER_CLASSIFICATION_INCOMPLETE")
        if owner_tracked_env_count + owner_untracked_env_count != unverified_git_count:
            raise DiagnosticError("UNVERIFIED_TRACKING_CLASSIFICATION_INCOMPLETE")

    except DiagnosticError as exc:
        return 2, tuple(_safe_lines(
            status="FAIL",
            failure_code=exc.code,
            checkout_count=checkout_count,
            env_count=env_count,
            remote_verified_count=remote_verified_count,
            repo_local_count=repo_local_count,
            standalone_count=standalone_count,
            unverified_git_count=unverified_git_count,
            owner_ai_corporation_count=owner_ai_corporation_count,
            owner_arvectum_os_count=owner_arvectum_os_count,
            owner_other_remote_count=owner_other_remote_count,
            owner_no_origin_count=owner_no_origin_count,
            owner_tracked_env_count=owner_tracked_env_count,
            owner_untracked_env_count=owner_untracked_env_count,
        ))

    return 0, tuple(_safe_lines(
        status="PASS",
        checkout_count=checkout_count,
        env_count=env_count,
        remote_verified_count=remote_verified_count,
        repo_local_count=repo_local_count,
        standalone_count=standalone_count,
        unverified_git_count=unverified_git_count,
        owner_ai_corporation_count=owner_ai_corporation_count,
        owner_arvectum_os_count=owner_arvectum_os_count,
        owner_other_remote_count=owner_other_remote_count,
        owner_no_origin_count=owner_no_origin_count,
        owner_tracked_env_count=owner_tracked_env_count,
        owner_untracked_env_count=owner_untracked_env_count,
    ))


def _safe_lines(
    *,
    status: str,
    checkout_count: int,
    env_count: int,
    remote_verified_count: int,
    repo_local_count: int,
    standalone_count: int,
    unverified_git_count: int,
    owner_ai_corporation_count: int,
    owner_arvectum_os_count: int,
    owner_other_remote_count: int,
    owner_no_origin_count: int,
    owner_tracked_env_count: int,
    owner_untracked_env_count: int,
    failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_unverified_owner_diagnostic_status={status}",
        f"source_checkout_count={checkout_count}",
        f"source_env_count={env_count}",
        f"source_remote_verified_count={remote_verified_count}",
        f"repo_local_source_count={repo_local_count}",
        f"standalone_source_count={standalone_count}",
        f"unverified_git_owned_source_count={unverified_git_count}",
        f"unverified_owner_ai_corporation_count={owner_ai_corporation_count}",
        f"unverified_owner_arvectum_os_count={owner_arvectum_os_count}",
        f"unverified_owner_other_remote_count={owner_other_remote_count}",
        f"unverified_owner_no_origin_count={owner_no_origin_count}",
        f"unverified_owner_tracked_env_count={owner_tracked_env_count}",
        f"unverified_owner_untracked_env_count={owner_untracked_env_count}",
    ]
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    lines.extend((
        "env_contents_read=false",
        "secret_values_read=false",
        "secret_values_printed=false",
        "secret_values_hashed=false",
        "filesystem_modified=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ))
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Classify Git ownership for the fixed P6.05-L3 discovery manifest without reading secrets."
    )
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = diagnose(
        args.discovery_file,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
