#!/usr/bin/env python3
"""Diagnose why the fixed P6.05-L3 secret destination is not external.

This helper is read-only. It consumes the existing fixed discovery manifest and
an intended destination path, verifies the seven supplied ai-corporation
checkouts, identifies the already-known single tender-app legacy Git owner, and
reports only safe destination-containment categories. It never reads env or
secret contents, never reads the destination value, and performs no mutation.
"""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_classify_known_legacy_owner as KNOWN
import p6_05_l3_recover_discovered_sources as BASE
import p6_05_l3_recover_mixed_legacy_sources as MIXED
import p6_05_l3_recover_verified_containers as VERIFIED


class DiagnosticError(RuntimeError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


def _owner_only(mode: int) -> bool:
    return mode & 0o077 == 0


def _safe_bool(value: bool) -> str:
    return "true" if value else "false"


def diagnose(
    discovery_file: Path,
    destination: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    checkout_count = env_count = remote_verified_count = 0
    tender_app_owner_count = 0
    destination_inside_ai_count = 0
    destination_inside_tender_app = False
    destination_inside_arvectum = False
    destination_owned_by_other_git = False
    destination_no_git_owner = False
    destination_parent_exists = False
    destination_parent_owner_only = False

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

        tender_roots: set[Path] = set()
        for env in discovery.envs:
            containers = [checkout for checkout in discovery.checkouts if BASE._is_relative_to(env, checkout)]
            if containers:
                continue
            try:
                owner = MIXED._nearest_valid_git_root(env.parent)
            except BASE.RecoveryError as exc:
                raise DiagnosticError(exc.code) from exc
            if owner is None:
                continue
            remote = MIXED._run_git(owner, "remote", "get-url", "origin")
            if remote.returncode != 0 or not remote.stdout.strip():
                continue
            if KNOWN._remote_matches_repository(remote.stdout, KNOWN.TENDER_APP_REPOSITORY):
                tender_roots.add(owner)

        tender_app_owner_count = len(tender_roots)
        if tender_app_owner_count != 1:
            raise DiagnosticError("EXPECTED_SINGLE_TENDER_APP_OWNER")

        target = destination.expanduser().resolve(strict=False)
        destination_inside_ai_count = sum(1 for checkout in discovery.checkouts if BASE._is_relative_to(target, checkout))
        tender_root = next(iter(tender_roots))
        destination_inside_tender_app = BASE._is_relative_to(target, tender_root)

        arvectum_root = (arvectum_repo_root or Path(__file__).resolve().parents[2]).resolve(strict=True)
        destination_inside_arvectum = BASE._is_relative_to(target, arvectum_root)

        parent = target.parent
        destination_parent_exists = parent.exists() and parent.is_dir()
        if destination_parent_exists:
            destination_parent_owner_only = _owner_only(stat.S_IMODE(parent.stat().st_mode))

        try:
            nearest = MIXED._nearest_valid_git_root(parent)
        except BASE.RecoveryError as exc:
            raise DiagnosticError(exc.code) from exc

        if nearest is None:
            destination_no_git_owner = True
        elif nearest in discovery.checkouts or nearest == tender_root or nearest == arvectum_root:
            pass
        else:
            destination_owned_by_other_git = True

        classifications = sum(
            [
                destination_inside_ai_count > 0,
                destination_inside_tender_app,
                destination_inside_arvectum,
                destination_owned_by_other_git,
                destination_no_git_owner,
            ]
        )
        if classifications == 0:
            raise DiagnosticError("DESTINATION_BOUNDARY_UNCLASSIFIED")

    except DiagnosticError as exc:
        return 2, tuple(_safe_lines(
            status="FAIL",
            failure_code=exc.code,
            checkout_count=checkout_count,
            env_count=env_count,
            remote_verified_count=remote_verified_count,
            tender_app_owner_count=tender_app_owner_count,
            destination_inside_ai_count=destination_inside_ai_count,
            destination_inside_tender_app=destination_inside_tender_app,
            destination_inside_arvectum=destination_inside_arvectum,
            destination_owned_by_other_git=destination_owned_by_other_git,
            destination_no_git_owner=destination_no_git_owner,
            destination_parent_exists=destination_parent_exists,
            destination_parent_owner_only=destination_parent_owner_only,
        ))

    return 0, tuple(_safe_lines(
        status="PASS",
        checkout_count=checkout_count,
        env_count=env_count,
        remote_verified_count=remote_verified_count,
        tender_app_owner_count=tender_app_owner_count,
        destination_inside_ai_count=destination_inside_ai_count,
        destination_inside_tender_app=destination_inside_tender_app,
        destination_inside_arvectum=destination_inside_arvectum,
        destination_owned_by_other_git=destination_owned_by_other_git,
        destination_no_git_owner=destination_no_git_owner,
        destination_parent_exists=destination_parent_exists,
        destination_parent_owner_only=destination_parent_owner_only,
    ))


def _safe_lines(
    *,
    status: str,
    checkout_count: int,
    env_count: int,
    remote_verified_count: int,
    tender_app_owner_count: int,
    destination_inside_ai_count: int,
    destination_inside_tender_app: bool,
    destination_inside_arvectum: bool,
    destination_owned_by_other_git: bool,
    destination_no_git_owner: bool,
    destination_parent_exists: bool,
    destination_parent_owner_only: bool,
    failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l3_destination_boundary_diagnostic_status={status}",
        f"source_checkout_count={checkout_count}",
        f"source_env_count={env_count}",
        f"source_remote_verified_count={remote_verified_count}",
        f"tender_app_owner_count={tender_app_owner_count}",
        f"destination_inside_ai_corporation_checkout_count={destination_inside_ai_count}",
        f"destination_inside_tender_app={_safe_bool(destination_inside_tender_app)}",
        f"destination_inside_arvectum_os={_safe_bool(destination_inside_arvectum)}",
        f"destination_owned_by_other_git={_safe_bool(destination_owned_by_other_git)}",
        f"destination_no_git_owner={_safe_bool(destination_no_git_owner)}",
        f"destination_parent_exists={_safe_bool(destination_parent_exists)}",
        f"destination_parent_owner_only={_safe_bool(destination_parent_owner_only)}",
    ]
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    lines.extend((
        "env_contents_read=false",
        "secret_values_read=false",
        "destination_secret_read=false",
        "filesystem_modified=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ))
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Safely classify the P6.05-L3 destination against known Git boundaries without reading secrets.")
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = diagnose(
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
