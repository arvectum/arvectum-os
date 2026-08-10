#!/usr/bin/env python3
"""Classify the single unverified P6.05-L3 Git owner against bounded known legacy repositories.

This helper is read-only. It consumes the existing fixed discovery manifest, verifies the
seven supplied ai-corporation checkouts, and classifies Git-owned env sources outside
those checkouts into safe repository categories without emitting remote URLs or paths.
It never reads env contents or secrets and performs no filesystem mutation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_recover_discovered_sources as BASE
import p6_05_l3_recover_mixed_legacy_sources as MIXED
import p6_05_l3_recover_verified_containers as VERIFIED

TENDER_APP_REPOSITORY = "arutyunoveth/tender-app"
TENDER_AI_REPOSITORY = "arutyunoveth/tender-ai"
OWNER_PREFIXES = (
    "https://github.com/arutyunoveth/",
    "git@github.com:arutyunoveth/",
    "ssh://git@github.com/arutyunoveth/",
)


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


def _same_owner_remote(value: str) -> bool:
    normalized = BASE._normalize_remote(value)
    return any(normalized.startswith(prefix) for prefix in OWNER_PREFIXES)


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
    tender_app_count = 0
    tender_ai_count = 0
    same_owner_other_count = 0
    external_other_count = 0
    no_origin_count = 0
    tracked_count = 0
    untracked_count = 0

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

            containers = [checkout for checkout in discovery.checkouts if BASE._is_relative_to(env, checkout)]
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

            unverified_git_count += 1
            remote = MIXED._run_git(owner, "remote", "get-url", "origin")
            if remote.returncode != 0 or not remote.stdout.strip():
                no_origin_count += 1
            elif _remote_matches_repository(remote.stdout, TENDER_APP_REPOSITORY):
                tender_app_count += 1
            elif _remote_matches_repository(remote.stdout, TENDER_AI_REPOSITORY):
                tender_ai_count += 1
            elif _same_owner_remote(remote.stdout):
                same_owner_other_count += 1
            else:
                external_other_count += 1

            relative_env = env.relative_to(owner)
            tracked = MIXED._run_git(owner, "ls-files", "--", str(relative_env))
            if tracked.returncode != 0:
                raise DiagnosticError("UNVERIFIED_GIT_TRACKING_INSPECTION_FAILED")
            if tracked.stdout.strip():
                tracked_count += 1
            else:
                untracked_count += 1

        if repo_local_count + standalone_count + unverified_git_count != env_count:
            raise DiagnosticError("SOURCE_CLASSIFICATION_INCOMPLETE")
        if tender_app_count + tender_ai_count + same_owner_other_count + external_other_count + no_origin_count != unverified_git_count:
            raise DiagnosticError("KNOWN_OWNER_CLASSIFICATION_INCOMPLETE")
        if tracked_count + untracked_count != unverified_git_count:
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
            tender_app_count=tender_app_count,
            tender_ai_count=tender_ai_count,
            same_owner_other_count=same_owner_other_count,
            external_other_count=external_other_count,
            no_origin_count=no_origin_count,
            tracked_count=tracked_count,
            untracked_count=untracked_count,
        ))

    return 0, tuple(_safe_lines(
        status="PASS",
        checkout_count=checkout_count,
        env_count=env_count,
        remote_verified_count=remote_verified_count,
        repo_local_count=repo_local_count,
        standalone_count=standalone_count,
        unverified_git_count=unverified_git_count,
        tender_app_count=tender_app_count,
        tender_ai_count=tender_ai_count,
        same_owner_other_count=same_owner_other_count,
        external_other_count=external_other_count,
        no_origin_count=no_origin_count,
        tracked_count=tracked_count,
        untracked_count=untracked_count,
    ))


def _safe_lines(
    *, status: str, checkout_count: int, env_count: int, remote_verified_count: int,
    repo_local_count: int, standalone_count: int, unverified_git_count: int,
    tender_app_count: int, tender_ai_count: int, same_owner_other_count: int,
    external_other_count: int, no_origin_count: int, tracked_count: int,
    untracked_count: int, failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_known_legacy_owner_diagnostic_status={status}",
        f"source_checkout_count={checkout_count}",
        f"source_env_count={env_count}",
        f"source_remote_verified_count={remote_verified_count}",
        f"repo_local_source_count={repo_local_count}",
        f"standalone_source_count={standalone_count}",
        f"unverified_git_owned_source_count={unverified_git_count}",
        f"known_owner_tender_app_count={tender_app_count}",
        f"known_owner_tender_ai_count={tender_ai_count}",
        f"known_owner_same_account_other_count={same_owner_other_count}",
        f"known_owner_external_other_count={external_other_count}",
        f"known_owner_no_origin_count={no_origin_count}",
        f"unverified_owner_tracked_env_count={tracked_count}",
        f"unverified_owner_untracked_env_count={untracked_count}",
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
    parser = argparse.ArgumentParser(description="Classify the fixed L3 unverified Git owner against bounded known legacy repositories without reading secrets.")
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = diagnose(args.discovery_file, expected_checkout_count=args.expected_checkout_count, expected_env_count=args.expected_env_count)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
