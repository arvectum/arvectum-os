#!/usr/bin/env python3
"""Reconcile owner-selected divergent P6.05-L3 legacy EIS secret sources.

This bounded canonical helper implements the 2026-08-14 owner decision for the
fixed seven-source P6.05-L3 discovery manifest.

When legacy sources diverge into exactly two equality classes (5+2 distribution),
where all four .env.local sources belong to the 5-source class, this helper:
1. validates all local Git and containment invariants without contacting GitHub;
2. verifies active repository identity arvectum/ai-corporation for manifest roots;
3. classifies all seven secret values in memory using constant-time equality;
4. selects the unique .env.local-anchored 5-source equality class;
5. establishes the selected credential at the external owner-only destination;
6. safely scrubs the ZAKUPKI_GOV_RU_SOAP_TOKEN assignment from all seven sources;
7. treats the 2-source non-selected values as stale local copies;
8. proves that all product and other local Git worktree tracked states and HEADs
   remain unchanged.

No secret value, hash, length, prefix, suffix, or encoded form is printed or persisted.
No product, EIS, SOAP, network, canonical-state, or external action is performed.
"""

from __future__ import annotations

import argparse
import os
import secrets
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import p6_05_l3_migrate_eis_secret as MIGRATION
import p6_05_l3_recover_discovered_sources as BASE
import p6_05_l3_recover_mixed_legacy_sources as MIXED
import p6_05_l3_recover_verified_containers as VERIFIED
from p6_05_l3_secure_local_config import (
    MAX_LOCAL_FILE_BYTES,
    PLACEHOLDER_SECRET_VALUES,
    SECRET_ENV_KEY,
)

OWNER_AUTHORIZATION_ASSERTION = (
    "OWNER_APPROVES_P6_05_L3_DOT_ENV_LOCAL_CLASS_RECONCILIATION"
)
EXPECTED_CHECKOUT_COUNT = 7
EXPECTED_ENV_COUNT = 7
EXPECTED_MANIFEST_AI_COUNT = 2
EXPECTED_STANDALONE_COUNT = 4
EXPECTED_OTHER_GIT_COUNT = 1
EXPECTED_DOT_ENV_LOCAL_COUNT = 4
EXPECTED_SELECTED_CLASS_COUNT = 5
EXPECTED_STALE_CLASS_COUNT = 2
EXPECTED_DISTINCT_CLASS_COUNT = 2


def _safe_bool(value: bool) -> str:
    return "true" if value else "false"


@dataclass(frozen=True, slots=True)
class ClassifiedEnv:
    env: Path
    category: str  # "manifest_ai_corporation", "standalone", "owner_approved_other_git"
    container_repo: Path | None
    is_dot_env_local: bool


@dataclass(frozen=True, slots=True)
class EnvSecretState:
    classified: ClassifiedEnv
    original_text: str
    scrubbed_text: str
    secret_value: str | None


def _capture_repo_snapshot(repo: Path) -> BASE.GitSnapshot:
    head = MIXED._run_git(repo, "rev-parse", "HEAD")
    if head.returncode != 0 or not head.stdout.strip():
        raise BASE.RecoveryError("GIT_HEAD_READ_FAILED")
    status = MIXED._run_git(repo, "status", "--porcelain=v1", "--untracked-files=no")
    if status.returncode != 0:
        raise BASE.RecoveryError("GIT_TRACKED_STATUS_FAILED")
    return BASE.GitSnapshot(head=head.stdout.strip(), tracked_status=status.stdout)


def _classify_single_env(
    env: Path,
    manifest_checkouts: Sequence[Path],
) -> ClassifiedEnv:
    if not BASE._supported_legacy_env_filename(env):
        raise BASE.RecoveryError("UNSUPPORTED_LEGACY_ENV_FILENAME")
    if not env.is_file():
        raise BASE.RecoveryError("LEGACY_ENV_NOT_REGULAR_FILE")

    is_dot_env_local = env.name == ".env.local"

    containers = [
        checkout for checkout in manifest_checkouts if BASE._is_relative_to(env, checkout)
    ]
    if containers:
        checkout = max(containers, key=lambda path: len(path.parts))
        VERIFIED._verify_no_unsupplied_valid_nested_repo(env, checkout, manifest_checkouts)
        relative_env = env.relative_to(checkout)
        tracked = MIXED._run_git(checkout, "ls-files", "--", str(relative_env))
        if tracked.returncode != 0:
            raise BASE.RecoveryError("AI_CORPORATION_GIT_INSPECTION_FAILED")
        if tracked.stdout.strip():
            raise BASE.RecoveryError("LEGACY_ENV_TRACKED_BY_GIT")
        return ClassifiedEnv(
            env=env,
            category="manifest_ai_corporation",
            container_repo=checkout,
            is_dot_env_local=is_dot_env_local,
        )

    owner = MIXED._nearest_valid_git_root(env.parent)
    if owner is None:
        return ClassifiedEnv(
            env=env,
            category="standalone",
            container_repo=None,
            is_dot_env_local=is_dot_env_local,
        )

    # Category C: other local Git worktree. Untracked verification without remote check.
    relative_env = env.relative_to(owner)
    tracked = MIXED._run_git(owner, "ls-files", "--", str(relative_env))
    if tracked.returncode != 0:
        raise BASE.RecoveryError("OTHER_GIT_WORKTREE_INSPECTION_FAILED")
    if tracked.stdout.strip():
        raise BASE.RecoveryError("OTHER_GIT_WORKTREE_ENV_TRACKED_BY_GIT")

    return ClassifiedEnv(
        env=env,
        category="owner_approved_other_git",
        container_repo=owner,
        is_dot_env_local=is_dot_env_local,
    )


def _validate_manifest_and_classify_sources(
    discovery: BASE.DiscoverySet,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
) -> tuple[tuple[ClassifiedEnv, ...], Path | None]:
    if len(discovery.checkouts) != expected_checkout_count:
        raise BASE.RecoveryError("DISCOVERY_CHECKOUT_COUNT_DRIFT")
    if len(discovery.envs) != expected_env_count:
        raise BASE.RecoveryError("DISCOVERY_ENV_COUNT_DRIFT")

    # Verify each manifest checkout remote matches arvectum/ai-corporation
    for checkout in discovery.checkouts:
        remote = MIXED._run_git(checkout, "remote", "get-url", "origin")
        if remote.returncode != 0 or not remote.stdout.strip():
            raise BASE.RecoveryError("AI_CORPORATION_REMOTE_UNVERIFIED")
        if not BASE._remote_matches_target(remote.stdout):
            raise BASE.RecoveryError("AI_CORPORATION_REMOTE_MISMATCH")

    classified_list: list[ClassifiedEnv] = []
    other_git_roots: list[Path] = []

    for env in discovery.envs:
        classified = _classify_single_env(env, discovery.checkouts)
        classified_list.append(classified)
        if classified.category == "owner_approved_other_git":
            assert classified.container_repo is not None
            if classified.container_repo not in other_git_roots:
                other_git_roots.append(classified.container_repo)

    manifest_ai_count = sum(
        1 for c in classified_list if c.category == "manifest_ai_corporation"
    )
    standalone_count = sum(1 for c in classified_list if c.category == "standalone")
    other_git_count = sum(
        1 for c in classified_list if c.category == "owner_approved_other_git"
    )

    if manifest_ai_count != EXPECTED_MANIFEST_AI_COUNT:
        raise BASE.RecoveryError("MANIFEST_AI_CORPORATION_SOURCE_COUNT_MISMATCH")
    if standalone_count != EXPECTED_STANDALONE_COUNT:
        raise BASE.RecoveryError("STANDALONE_SOURCE_COUNT_MISMATCH")
    if other_git_count != EXPECTED_OTHER_GIT_COUNT or len(other_git_roots) != 1:
        raise BASE.RecoveryError("OTHER_GIT_WORKTREE_SOURCE_COUNT_MISMATCH")

    dot_env_local_count = sum(1 for c in classified_list if c.is_dot_env_local)
    if dot_env_local_count != EXPECTED_DOT_ENV_LOCAL_COUNT:
        raise BASE.RecoveryError("DOT_ENV_LOCAL_SOURCE_COUNT_MISMATCH")

    return tuple(classified_list), other_git_roots[0]


def _read_env_secret_state(classified: ClassifiedEnv) -> EnvSecretState:
    MIXED._owner_only_source(classified.env)
    try:
        raw_bytes = classified.env.read_bytes()
    except OSError as exc:
        raise BASE.RecoveryError("LOCAL_FILESYSTEM_OPERATION_FAILED") from exc

    if len(raw_bytes) > MAX_LOCAL_FILE_BYTES:
        raise BASE.RecoveryError("SOURCE_ENV_TOO_LARGE")

    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise BASE.RecoveryError("SOURCE_ENV_NOT_VALID_UTF8") from exc

    try:
        secret_val, scrubbed_text = MIGRATION._extract_optional_secret_and_scrubbed_text(text)
    except MIGRATION.MigrationError as exc:
        raise BASE.RecoveryError(exc.code) from exc

    return EnvSecretState(
        classified=classified,
        original_text=text,
        scrubbed_text=scrubbed_text,
        secret_value=secret_val,
    )


def _classify_secrets_in_memory(
    states: Sequence[EnvSecretState],
) -> tuple[str, list[EnvSecretState], list[EnvSecretState]]:
    """Verify 5+2 distribution where all 4 .env.local are in the 5-source selected class."""
    with_secret = [s for s in states if s.secret_value is not None]
    if len(with_secret) != EXPECTED_ENV_COUNT:
        raise BASE.RecoveryError("UNEXPECTED_ALREADY_SCRUBBED_SOURCE_ON_INITIAL_RUN")

    # Group into equivalence classes using constant-time equality
    classes: list[list[EnvSecretState]] = []
    for s in with_secret:
        assert s.secret_value is not None
        matched_class = None
        for group in classes:
            assert group[0].secret_value is not None
            if secrets.compare_digest(s.secret_value, group[0].secret_value):
                matched_class = group
                break
        if matched_class is not None:
            matched_class.append(s)
        else:
            classes.append([s])

    if len(classes) != EXPECTED_DISTINCT_CLASS_COUNT:
        raise BASE.RecoveryError("DISTINCT_SECRET_CLASS_COUNT_MISMATCH")

    # Sort classes by size descending
    classes.sort(key=lambda g: len(g), reverse=True)
    class_5 = classes[0]
    class_2 = classes[1]

    if len(class_5) != EXPECTED_SELECTED_CLASS_COUNT:
        raise BASE.RecoveryError("SELECTED_SECRET_CLASS_COUNT_MISMATCH")
    if len(class_2) != EXPECTED_STALE_CLASS_COUNT:
        raise BASE.RecoveryError("STALE_SECRET_CLASS_COUNT_MISMATCH")

    # Verify all four .env.local are in class_5
    dot_env_local_in_5 = sum(1 for s in class_5 if s.classified.is_dot_env_local)
    if dot_env_local_in_5 != EXPECTED_DOT_ENV_LOCAL_COUNT:
        raise BASE.RecoveryError("DOT_ENV_LOCAL_NOT_ALL_IN_SELECTED_CLASS")

    selected_secret = class_5[0].secret_value
    assert selected_secret is not None

    return selected_secret, class_5, class_2


def _write_destination_secret(destination: Path, secret_value: str) -> None:
    parent = destination.parent
    fd, temp_path_str = tempfile.mkstemp(
        prefix="eis-secret-",
        dir=str(parent),
        text=True,
    )
    temp_path = Path(temp_path_str)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(f"{secret_value}\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(temp_path, 0o600)
        os.replace(temp_path, destination)
    except Exception as exc:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        raise BASE.RecoveryError("LOCAL_FILESYSTEM_OPERATION_FAILED") from exc


def _safe_report_lines(
    *,
    status: str,
    failure_code: str | None = None,
    owner_authorization_asserted: bool,
    source_checkout_count: int,
    source_env_count: int,
    manifest_ai_corporation_source_count: int,
    standalone_source_count: int,
    owner_approved_other_git_source_count: int,
    distinct_secret_class_count: int,
    dot_env_local_source_count: int,
    selected_secret_source_count: int,
    stale_secret_source_count: int,
    destination_created: bool,
    destination_reused: bool,
    sources_with_key_before: int,
    sources_already_scrubbed_before: int,
    sources_scrubbed: int,
    source_envs_with_eis_key_remaining: int,
    selected_class_established: bool,
    stale_local_copies_discarded: bool,
    manifest_checkout_heads_unchanged: bool,
    manifest_checkout_tracked_states_unchanged: bool,
    other_local_git_head_unchanged: bool,
    other_local_git_tracked_state_unchanged: bool,
) -> tuple[str, ...]:
    lines = [
        f"p6_05_l3_divergent_reconciliation_status={status}",
        f"owner_authorization_asserted={_safe_bool(owner_authorization_asserted)}",
        f"source_checkout_count={source_checkout_count}",
        f"source_env_count={source_env_count}",
        f"manifest_ai_corporation_source_count={manifest_ai_corporation_source_count}",
        f"standalone_source_count={standalone_source_count}",
        f"owner_approved_other_git_source_count={owner_approved_other_git_source_count}",
        f"distinct_secret_class_count={distinct_secret_class_count}",
        f"dot_env_local_source_count={dot_env_local_source_count}",
        f"selected_secret_source_count={selected_secret_source_count}",
        f"stale_secret_source_count={stale_secret_source_count}",
        f"destination_created={_safe_bool(destination_created)}",
        f"destination_reused={_safe_bool(destination_reused)}",
        f"sources_with_key_before={sources_with_key_before}",
        f"sources_already_scrubbed_before={sources_already_scrubbed_before}",
        f"sources_scrubbed={sources_scrubbed}",
        f"source_envs_with_eis_key_remaining={source_envs_with_eis_key_remaining}",
        f"selected_class_established={_safe_bool(selected_class_established)}",
        f"stale_local_copies_discarded={_safe_bool(stale_local_copies_discarded)}",
        f"manifest_checkout_heads_unchanged={_safe_bool(manifest_checkout_heads_unchanged)}",
        f"manifest_checkout_tracked_states_unchanged={_safe_bool(manifest_checkout_tracked_states_unchanged)}",
        f"other_local_git_head_unchanged={_safe_bool(other_local_git_head_unchanged)}",
        f"other_local_git_tracked_state_unchanged={_safe_bool(other_local_git_tracked_state_unchanged)}",
    ]
    if status == "PASS":
        lines.append("secret.ZAKUPKI_GOV_RU_SOAP_TOKEN=configured")
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")

    lines.extend([
        "secret_values_printed=false",
        "secret_values_hashed=false",
        "secret_values_encoded=false",
        "secret_values_persisted_as_evidence=false",
        "secret_lengths_printed=false",
        "backup_with_secret_created=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ])
    return tuple(lines)


def reconcile_divergent_sources(
    *,
    discovery_file: Path,
    destination: Path,
    expected_checkout_count: int = EXPECTED_CHECKOUT_COUNT,
    expected_env_count: int = EXPECTED_ENV_COUNT,
    owner_authorization: str,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    owner_authorization_asserted = (
        owner_authorization == OWNER_AUTHORIZATION_ASSERTION
    )
    destination_created = False
    destination_reused = False
    selected_class_established = False
    stale_local_copies_discarded = False
    sources_with_key_before = 0
    sources_already_scrubbed_before = 0
    sources_scrubbed = 0
    remaining_secret_key_count = 0

    manifest_ai_count = EXPECTED_MANIFEST_AI_COUNT
    standalone_count = EXPECTED_STANDALONE_COUNT
    other_git_count = EXPECTED_OTHER_GIT_COUNT
    dot_env_local_count = EXPECTED_DOT_ENV_LOCAL_COUNT
    selected_class_count = EXPECTED_SELECTED_CLASS_COUNT
    stale_class_count = EXPECTED_STALE_CLASS_COUNT
    distinct_class_count = EXPECTED_DISTINCT_CLASS_COUNT

    manifest_heads_unchanged = True
    manifest_tracked_unchanged = True
    other_git_head_unchanged = True
    other_git_tracked_unchanged = True

    try:
        if not owner_authorization_asserted:
            raise BASE.RecoveryError("OWNER_AUTHORIZATION_REQUIRED")

        discovery = BASE._parse_discovery(discovery_file)
        classified_envs, other_git_root = _validate_manifest_and_classify_sources(
            discovery,
            expected_checkout_count=expected_checkout_count,
            expected_env_count=expected_env_count,
        )
        assert other_git_root is not None

        # Inspect destination placement safety
        all_prohibited_roots = list(discovery.checkouts) + [other_git_root]
        arvectum_root = (arvectum_repo_root or BASE._repo_root()).resolve(strict=True)
        try:
            MIGRATION._inspect_destination(
                destination,
                source_checkout_roots=all_prohibited_roots,
                arvectum_repo_root=arvectum_root,
            )
        except MIGRATION.MigrationError as exc:
            raise BASE.RecoveryError(exc.code) from exc

        # Snapshot all git worktrees before
        ai_before = MIXED._capture_snapshots(discovery.checkouts)
        other_git_before = _capture_repo_snapshot(other_git_root)

        # Read env states in memory
        env_states = [_read_env_secret_state(c) for c in classified_envs]
        sources_with_key_before = sum(1 for s in env_states if s.secret_value is not None)
        sources_already_scrubbed_before = len(env_states) - sources_with_key_before

        dest_exists = destination.exists()

        if not dest_exists:
            # First run: require exact 5+2 distribution
            selected_secret, class_5, class_2 = _classify_secrets_in_memory(env_states)
            _write_destination_secret(destination, selected_secret)
            destination_created = True
            selected_class_established = True
        else:
            # Retry / existing destination: verify against destination
            destination_reused = True
            dest_secret = MIGRATION._read_existing_destination(destination)
            selected_class_established = True

            # Verify that any remaining .env.local matches dest_secret
            remaining_dot_env_local = [
                s for s in env_states if s.classified.is_dot_env_local and s.secret_value is not None
            ]
            if remaining_dot_env_local:
                for s in remaining_dot_env_local:
                    assert s.secret_value is not None
                    if not secrets.compare_digest(s.secret_value, dest_secret):
                        raise BASE.RecoveryError("RETRY_SECRET_DOES_NOT_MATCH_DESTINATION")
            elif sources_with_key_before > 0:
                # No remaining .env.local to prove the destination; check if any remaining source matches
                matching_remaining = [
                    s for s in env_states if s.secret_value is not None and secrets.compare_digest(s.secret_value, dest_secret)
                ]
                if not matching_remaining:
                    raise BASE.RecoveryError("RETRY_CANNOT_PROVE_DESTINATION_MATCH")

        # Scrub in ordered sequence: non-.env.local first, .env.local last
        non_dot_env_local = [s for s in env_states if not s.classified.is_dot_env_local and s.secret_value is not None]
        dot_env_local = [s for s in env_states if s.classified.is_dot_env_local and s.secret_value is not None]
        scrub_sequence = non_dot_env_local + dot_env_local

        for s in scrub_sequence:
            try:
                MIGRATION._rewrite_source_without_secret(s.classified.env, s.scrubbed_text)
            except Exception as exc:
                raise BASE.RecoveryError("SOURCE_SCRUB_INCOMPLETE_DESTINATION_PRESERVED") from exc
            sources_scrubbed += 1

        stale_local_copies_discarded = True

        # Snapshot all git worktrees after
        ai_after = MIXED._capture_snapshots(discovery.checkouts)
        other_git_after = _capture_repo_snapshot(other_git_root)

        manifest_heads_unchanged = all(
            ai_after[c].head == ai_before[c].head for c in discovery.checkouts
        )
        manifest_tracked_unchanged = all(
            ai_after[c].tracked_status == ai_before[c].tracked_status for c in discovery.checkouts
        )
        other_git_head_unchanged = other_git_after.head == other_git_before.head
        other_git_tracked_unchanged = (
            other_git_after.tracked_status == other_git_before.tracked_status
        )

        if not manifest_heads_unchanged or not manifest_tracked_unchanged:
            raise BASE.RecoveryError("AI_CORPORATION_TRACKED_STATE_CHANGED")
        if not other_git_head_unchanged or not other_git_tracked_unchanged:
            raise BASE.RecoveryError("OTHER_GIT_WORKTREE_TRACKED_STATE_CHANGED")

        remaining_secret_key_count = sum(
            1 for env in discovery.envs if BASE._contains_secret_key(env)
        )
        if remaining_secret_key_count != 0:
            raise BASE.RecoveryError("SOURCE_SCRUB_POSTCHECK_FAILED")

    except BASE.RecoveryError as exc:
        remaining_secret_key_count = sum(
            1 for env in discovery.envs if BASE._contains_secret_key(env)
        ) if 'discovery' in locals() else 0
        return 2, _safe_report_lines(
            status="FAIL",
            failure_code=exc.code,
            owner_authorization_asserted=owner_authorization_asserted,
            source_checkout_count=expected_checkout_count,
            source_env_count=expected_env_count,
            manifest_ai_corporation_source_count=manifest_ai_count,
            standalone_source_count=standalone_count,
            owner_approved_other_git_source_count=other_git_count,
            distinct_secret_class_count=distinct_class_count,
            dot_env_local_source_count=dot_env_local_count,
            selected_secret_source_count=selected_class_count,
            stale_secret_source_count=stale_class_count,
            destination_created=destination_created,
            destination_reused=destination_reused,
            sources_with_key_before=sources_with_key_before,
            sources_already_scrubbed_before=sources_already_scrubbed_before,
            sources_scrubbed=sources_scrubbed,
            source_envs_with_eis_key_remaining=remaining_secret_key_count,
            selected_class_established=selected_class_established,
            stale_local_copies_discarded=stale_local_copies_discarded,
            manifest_checkout_heads_unchanged=manifest_heads_unchanged,
            manifest_checkout_tracked_states_unchanged=manifest_tracked_unchanged,
            other_local_git_head_unchanged=other_git_head_unchanged,
            other_local_git_tracked_state_unchanged=other_git_tracked_unchanged,
        )

    return 0, _safe_report_lines(
        status="PASS",
        owner_authorization_asserted=True,
        source_checkout_count=expected_checkout_count,
        source_env_count=expected_env_count,
        manifest_ai_corporation_source_count=manifest_ai_count,
        standalone_source_count=standalone_count,
        owner_approved_other_git_source_count=other_git_count,
        distinct_secret_class_count=distinct_class_count,
        dot_env_local_source_count=dot_env_local_count,
        selected_secret_source_count=selected_class_count,
        stale_secret_source_count=stale_class_count,
        destination_created=destination_created,
        destination_reused=destination_reused,
        sources_with_key_before=sources_with_key_before,
        sources_already_scrubbed_before=sources_already_scrubbed_before,
        sources_scrubbed=sources_scrubbed,
        source_envs_with_eis_key_remaining=0,
        selected_class_established=True,
        stale_local_copies_discarded=True,
        manifest_checkout_heads_unchanged=True,
        manifest_checkout_tracked_states_unchanged=True,
        other_local_git_head_unchanged=True,
        other_local_git_tracked_state_unchanged=True,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reconcile owner-selected divergent P6.05-L3 legacy EIS secret sources.",
    )
    parser.add_argument(
        "--discovery-file",
        required=True,
        type=Path,
        help="Path to the existing fixed P6.05-L3 discovery manifest",
    )
    parser.add_argument(
        "--destination",
        required=True,
        type=Path,
        help="External destination secret file path",
    )
    parser.add_argument(
        "--expected-checkout-count",
        type=int,
        default=EXPECTED_CHECKOUT_COUNT,
        help="Expected count of ai-corporation checkout roots in manifest",
    )
    parser.add_argument(
        "--expected-env-count",
        type=int,
        default=EXPECTED_ENV_COUNT,
        help="Expected count of legacy env files in manifest",
    )
    parser.add_argument(
        "--owner-authorization",
        required=True,
        help="Exact owner authorization assertion string",
    )
    args = parser.parse_args(argv)

    rc, lines = reconcile_divergent_sources(
        discovery_file=args.discovery_file,
        destination=args.destination,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
        owner_authorization=args.owner_authorization,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
