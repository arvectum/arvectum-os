#!/usr/bin/env python3
"""P6.05-L4 read-only operator context preflight.

This module validates the bounded internal Organization and operator state
file created by P6.05-L4 bootstrap.

It strictly adheres to the following constraints:
- Read-only inspection: never creates, mutates, or deletes state;
- Never auto-repairs permissions (fails closed);
- Validates the entire owner-only local boundary: target root, local-context dir, and state file;
- Rejects symlinks in target path, local-context dir, and state file;
- Verifies state file is outside source control and outside git worktrees;
- Validates the exact bounded schema (rejecting unexpected fields);
- Constructs canonical OrganizationScope, Principal, and ActorContext;
- Verifies zero authorization grants, zero delegations, zero authority claimed;
- Verifies zero authentication evidence references;
- Proves no secrets, credentials, product context, or tenant context;
- Reports truthful unproven facts on failure without disclosing metadata;
- Does not print opaque Organization or Principal identity values by default.
"""

from __future__ import annotations

import argparse
import stat
import sys
from pathlib import Path
from typing import Sequence

import p6_05_l3_recover_mixed_legacy_sources as MIXED
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from p6_05_l4_bootstrap_internal_context import (
    BootstrapError,
    BootstrapResult,
    PRINCIPAL_CATEGORY,
    _assert_no_intermediate_symlinks,
    _assert_not_symlink,
    _nearest_existing_ancestor,
    _owner_only,
    _read_and_validate_existing_context,
    _safe_bool,
    _safe_lines,
)


def inspect_operator_context_file(
    state_file: Path,
    *,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...], BootstrapResult | None]:
    root_outside_git = False
    context_owner_only = False
    result_context: BootstrapResult | None = None

    try:
        expanded = state_file.expanduser()
        _assert_not_symlink(expanded, "CONTEXT_FILE_SYMLINK_NOT_ALLOWED")
        _assert_no_intermediate_symlinks(expanded, "CONTEXT_FILE_SYMLINK_NOT_ALLOWED")

        if not expanded.exists():
            raise BootstrapError("CONTEXT_MALFORMED")

        if not expanded.is_file():
            raise BootstrapError("CONTEXT_MALFORMED")

        # Check state file permissions
        mode = stat.S_IMODE(expanded.stat().st_mode)
        if not _owner_only(mode):
            raise BootstrapError("CONTEXT_PERMISSIONS_TOO_BROAD")

        # Check local-context directory permissions
        parent_dir = expanded.parent
        _assert_not_symlink(parent_dir, "TARGET_SYMLINK_NOT_ALLOWED")
        if not parent_dir.is_dir() or not _owner_only(stat.S_IMODE(parent_dir.stat().st_mode)):
            raise BootstrapError("CONTEXT_PERMISSIONS_TOO_BROAD")

        # Check target root directory permissions
        target_root = parent_dir.parent
        _assert_not_symlink(target_root, "TARGET_SYMLINK_NOT_ALLOWED")
        if not target_root.is_dir() or not _owner_only(stat.S_IMODE(target_root.stat().st_mode)):
            raise BootstrapError("CONTEXT_PERMISSIONS_TOO_BROAD")

        ancestor = _nearest_existing_ancestor(target_root)
        _assert_not_symlink(ancestor, "TARGET_SYMLINK_NOT_ALLOWED")

        nearest_git = MIXED._nearest_valid_git_root(ancestor)
        if nearest_git is not None:
            raise BootstrapError("TARGET_INSIDE_GIT_WORKTREE")

        repo_root = (
            arvectum_repo_root or Path(__file__).resolve().parents[2]
        ).resolve(strict=True)
        resolved = expanded.resolve(strict=False)
        try:
            resolved.relative_to(repo_root)
        except ValueError:
            pass
        else:
            raise BootstrapError("TARGET_INSIDE_ARVECTUM_CHECKOUT")

        # Read and validate bounded context data
        org_scope, principal, actor_context = _read_and_validate_existing_context(
            resolved
        )
        context_owner_only = True
        root_outside_git = True
        result_context = BootstrapResult(
            organization_scope=org_scope,
            principal=principal,
            actor_context=actor_context,
            context_created=False,
            context_reused=True,
        )

    except (BootstrapError, OSError) as exc:
        code = (
            exc.code
            if isinstance(exc, BootstrapError)
            else "LOCAL_FILESYSTEM_OPERATION_FAILED"
        )
        return 2, tuple(
            _safe_lines(
                status="FAIL",
                failure_code=code,
                context_created=False,
                context_reused=False,
                context_owner_only=context_owner_only,
                root_outside_git=root_outside_git,
            )
        ), None

    return 0, tuple(
        _safe_lines(
            status="PASS",
            context_created=False,
            context_reused=True,
            context_owner_only=True,
            root_outside_git=True,
        )
    ), result_context


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Preflight read-only inspection of P6.05-L4 operator context state file."
    )
    parser.add_argument("--state-file", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines, _ = inspect_operator_context_file(args.state_file)
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
