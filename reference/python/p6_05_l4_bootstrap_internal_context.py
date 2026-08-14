#!/usr/bin/env python3
"""P6.05-L4 internal Organization and operator bootstrap helper.

This module provides a bounded, owner-operated bootstrap helper for the
internal Organization and operator context required by P6.05 local runtime.

It creates or reuses an external, owner-only local state file containing exactly:
1. One opaque Organization Identity representing ООО «Арвектум»;
2. One opaque human Principal Identity representing the owner-operator;
3. Construction and validation of canonical OrganizationScope, Principal,
   and ActorContext types.

It strictly adheres to the following constraints:
- Outside all Git worktrees and Arvectum OS checkouts;
- Requires exact owner assertion before any generation or filesystem mutation;
- Atomic exclusive creation (O_CREAT | O_EXCL) with owner-only permissions (0600 / 0700);
- Zero authorization grants, zero delegations, zero authority claimed;
- Zero authentication evidence refs at bootstrap;
- No IAM/SSO/RBAC/credentials/secrets/product/tenant context;
- Idempotent safe reuse without regenerating identities;
- Fail closed under any anomaly or schema mismatch.
"""

from __future__ import annotations

import argparse
import json
import os
import secrets
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import p6_05_l3_recover_mixed_legacy_sources as MIXED
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal

SCHEMA_VERSION = "p6.05-l4-local-context-1"
CONTEXT_LABEL = "ООО «Арвектум»"
PRINCIPAL_CATEGORY = "human"
OPERATING_MODE = "owner-operated"
BOOTSTRAP_SCOPE = "P6.05-L4"
MAX_CONTEXT_FILE_BYTES = 64 * 1024

REQUIRED_OWNER_ASSERTION = (
    "OWNER_APPROVES_P6_05_L4_INTERNAL_ORGANIZATION_OPERATOR_BOOTSTRAP"
)


class BootstrapError(RuntimeError):
    """Safe validation error that contains no opaque IDs or secret data."""

    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class BootstrapResult:
    organization_scope: OrganizationScope
    principal: Principal
    actor_context: ActorContext
    context_created: bool
    context_reused: bool


def _owner_only(mode: int) -> bool:
    return mode & 0o077 == 0


def _safe_bool(value: bool) -> str:
    return "true" if value else "false"


def _assert_not_symlink(path: Path, code: str) -> None:
    if path.is_symlink():
        raise BootstrapError(code)


def _nearest_existing_ancestor(path: Path) -> Path:
    current = path
    while not current.exists():
        parent = current.parent
        if parent == current:
            raise BootstrapError("TARGET_ROOT_EXISTING_ANCESTOR_NOT_FOUND")
        current = parent
    return current


def _ensure_owner_only_directory(path: Path, *, create: bool) -> bool:
    _assert_not_symlink(path, "TARGET_SYMLINK_NOT_ALLOWED")
    created = False
    if not path.exists():
        if not create:
            raise BootstrapError("LOCAL_FILESYSTEM_OPERATION_FAILED")
        path.mkdir(mode=0o700)
        created = True
    if not path.is_dir():
        raise BootstrapError("LOCAL_FILESYSTEM_OPERATION_FAILED")
    os.chmod(path, 0o700)
    mode = stat.S_IMODE(path.stat().st_mode)
    if not _owner_only(mode):
        raise BootstrapError("CONTEXT_PERMISSIONS_TOO_BROAD")
    return created


def _validate_bounded_context_data(
    data: Mapping[str, Any],
) -> tuple[OrganizationScope, Principal, ActorContext]:
    if not isinstance(data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    if data.get("schema_version") != SCHEMA_VERSION:
        raise BootstrapError("CONTEXT_SCHEMA_UNSUPPORTED")

    org_data = data.get("organization")
    if not isinstance(org_data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    org_id_data = org_data.get("identity")
    if not isinstance(org_id_data, dict):
        raise BootstrapError("ORGANIZATION_IDENTITY_INVALID")

    if (
        org_id_data.get("namespace") != "organization"
        or not isinstance(org_id_data.get("value"), str)
        or not org_id_data.get("value", "").strip()
        or org_id_data.get("scope") != "platform"
    ):
        raise BootstrapError("ORGANIZATION_IDENTITY_INVALID")

    try:
        org_identity = Identity(
            namespace=org_id_data["namespace"],
            value=org_id_data["value"],
            scope=org_id_data["scope"],
        )
        org_scope = OrganizationScope(org_identity)
    except Exception as exc:
        raise BootstrapError("ORGANIZATION_IDENTITY_INVALID") from exc

    op_data = data.get("operator")
    if not isinstance(op_data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    if op_data.get("principal_category") != PRINCIPAL_CATEGORY:
        raise BootstrapError("PRINCIPAL_CATEGORY_UNSUPPORTED")

    if op_data.get("operating_mode") != OPERATING_MODE:
        raise BootstrapError("OPERATING_MODE_UNSUPPORTED")

    prin_id_data = op_data.get("identity")
    if not isinstance(prin_id_data, dict):
        raise BootstrapError("PRINCIPAL_IDENTITY_INVALID")

    if (
        prin_id_data.get("namespace") != "principal"
        or not isinstance(prin_id_data.get("value"), str)
        or not prin_id_data.get("value", "").strip()
    ):
        raise BootstrapError("PRINCIPAL_IDENTITY_INVALID")

    if prin_id_data.get("scope") != org_identity.value:
        raise BootstrapError("PRINCIPAL_ORGANIZATION_SCOPE_MISMATCH")

    try:
        prin_identity = Identity(
            namespace=prin_id_data["namespace"],
            value=prin_id_data["value"],
            scope=prin_id_data["scope"],
        )
        principal = Principal(prin_identity)
    except Exception as exc:
        raise BootstrapError("PRINCIPAL_IDENTITY_INVALID") from exc

    authority_data = data.get("authority")
    if not isinstance(authority_data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    grants = authority_data.get("authorization_grants")
    if not isinstance(grants, list) or len(grants) != 0:
        raise BootstrapError("AUTHORIZATION_GRANTS_NOT_EMPTY")

    delegations = authority_data.get("delegations")
    if not isinstance(delegations, list) or len(delegations) != 0:
        raise BootstrapError("DELEGATIONS_NOT_EMPTY")

    if authority_data.get("organizational_authority_claimed") is not False:
        raise BootstrapError("ORGANIZATIONAL_AUTHORITY_NOT_ALLOWED")

    authn_data = data.get("authentication")
    if not isinstance(authn_data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    evidence_refs = authn_data.get("evidence_refs")
    if not isinstance(evidence_refs, list) or len(evidence_refs) != 0:
        raise BootstrapError("AUTHENTICATION_EVIDENCE_NOT_EMPTY")

    bootstrap_data = data.get("bootstrap")
    if not isinstance(bootstrap_data, dict):
        raise BootstrapError("CONTEXT_MALFORMED")

    if bootstrap_data.get("scope") != BOOTSTRAP_SCOPE:
        raise BootstrapError("CONTEXT_SCHEMA_UNSUPPORTED")

    if bootstrap_data.get("owner_authorization_asserted") is not True:
        raise BootstrapError("OWNER_AUTHORIZATION_REQUIRED")

    # Construct and validate canonical ActorContext
    try:
        actor_context = ActorContext(
            actual_principal=principal,
            organization=org_scope,
            represented_principal=None,
            authentication_evidence_refs=(),
        )
    except Exception as exc:
        raise BootstrapError("CONTEXT_MALFORMED") from exc

    return org_scope, principal, actor_context


def _read_and_validate_existing_context(
    state_file: Path,
) -> tuple[OrganizationScope, Principal, ActorContext]:
    _assert_not_symlink(state_file, "CONTEXT_FILE_SYMLINK_NOT_ALLOWED")
    if not state_file.is_file():
        raise BootstrapError("CONTEXT_MALFORMED")
    if state_file.stat().st_size > MAX_CONTEXT_FILE_BYTES:
        raise BootstrapError("CONTEXT_MALFORMED")
    if not _owner_only(stat.S_IMODE(state_file.stat().st_mode)):
        raise BootstrapError("CONTEXT_PERMISSIONS_TOO_BROAD")

    try:
        text = state_file.read_text(encoding="utf-8")
        raw_data = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError, OSError) as exc:
        raise BootstrapError("CONTEXT_MALFORMED") from exc

    return _validate_bounded_context_data(raw_data)


def bootstrap_internal_context(
    target_root: Path,
    *,
    owner_authorization: str,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...], BootstrapResult | None]:
    context_created = False
    context_reused = False
    root_outside_git = False
    context_owner_only = False
    result_context: BootstrapResult | None = None

    try:
        if owner_authorization != REQUIRED_OWNER_ASSERTION:
            raise BootstrapError("OWNER_AUTHORIZATION_REQUIRED")

        expanded = target_root.expanduser()
        _assert_not_symlink(expanded, "TARGET_SYMLINK_NOT_ALLOWED")
        existing_ancestor = _nearest_existing_ancestor(expanded)
        _assert_not_symlink(existing_ancestor, "TARGET_SYMLINK_NOT_ALLOWED")

        nearest_git = MIXED._nearest_valid_git_root(existing_ancestor)
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

        parent = resolved.parent
        if not parent.exists() or not parent.is_dir():
            raise BootstrapError("LOCAL_FILESYSTEM_OPERATION_FAILED")
        _assert_not_symlink(parent, "TARGET_SYMLINK_NOT_ALLOWED")

        _ensure_owner_only_directory(resolved, create=True)
        context_dir = resolved / "local-context"
        _ensure_owner_only_directory(context_dir, create=True)

        state_file = context_dir / "organization-operator.json"
        _assert_not_symlink(state_file, "CONTEXT_FILE_SYMLINK_NOT_ALLOWED")

        if state_file.exists():
            org_scope, principal, actor_context = _read_and_validate_existing_context(
                state_file
            )
            context_reused = True
            context_owner_only = True
            result_context = BootstrapResult(
                organization_scope=org_scope,
                principal=principal,
                actor_context=actor_context,
                context_created=False,
                context_reused=True,
            )
        else:
            # Generate opaque identities
            org_val = secrets.token_hex(16)
            prin_val = secrets.token_hex(16)

            org_id = Identity(
                namespace="organization",
                value=org_val,
                scope="platform",
            )
            org_scope = OrganizationScope(org_id)

            prin_id = Identity(
                namespace="principal",
                value=prin_val,
                scope=org_val,
            )
            principal = Principal(prin_id)

            actor_context = ActorContext(
                actual_principal=principal,
                organization=org_scope,
                represented_principal=None,
                authentication_evidence_refs=(),
            )

            payload = {
                "schema_version": SCHEMA_VERSION,
                "organization": {
                    "identity": {
                        "namespace": org_id.namespace,
                        "value": org_id.value,
                        "scope": org_id.scope,
                    },
                    "context_label": CONTEXT_LABEL,
                },
                "operator": {
                    "identity": {
                        "namespace": prin_id.namespace,
                        "value": prin_id.value,
                        "scope": prin_id.scope,
                    },
                    "principal_category": PRINCIPAL_CATEGORY,
                    "operating_mode": OPERATING_MODE,
                },
                "authority": {
                    "authorization_grants": [],
                    "delegations": [],
                    "organizational_authority_claimed": False,
                },
                "authentication": {
                    "evidence_refs": [],
                },
                "bootstrap": {
                    "scope": BOOTSTRAP_SCOPE,
                    "owner_authorization_asserted": True,
                },
            }

            serialized = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"

            try:
                fd = os.open(
                    state_file,
                    os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                    0o600,
                )
            except FileExistsError as exc:
                raise BootstrapError("CONTEXT_ALREADY_EXISTS_RACE") from exc

            try:
                with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                    handle.write(serialized)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.chmod(state_file, 0o600)
            except Exception:
                state_file.unlink(missing_ok=True)
                raise BootstrapError("LOCAL_FILESYSTEM_OPERATION_FAILED")

            # Validate created state
            _read_and_validate_existing_context(state_file)
            context_created = True
            context_owner_only = True
            result_context = BootstrapResult(
                organization_scope=org_scope,
                principal=principal,
                actor_context=actor_context,
                context_created=True,
                context_reused=False,
            )

        root_outside_git = MIXED._nearest_valid_git_root(resolved) is None
        if not root_outside_git:
            raise BootstrapError("TARGET_INSIDE_GIT_WORKTREE")

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
                context_created=context_created,
                context_reused=context_reused,
                context_owner_only=context_owner_only,
                root_outside_git=root_outside_git,
            )
        ), None

    return 0, tuple(
        _safe_lines(
            status="PASS",
            context_created=context_created,
            context_reused=context_reused,
            context_owner_only=True,
            root_outside_git=True,
        )
    ), result_context


def _safe_lines(
    *,
    status: str,
    context_created: bool,
    context_reused: bool,
    context_owner_only: bool,
    root_outside_git: bool,
    failure_code: str | None = None,
) -> list[str]:
    lines = [
        f"p6_05_l4_status={status}",
        f"context_created={_safe_bool(context_created)}",
        f"context_reused={_safe_bool(context_reused)}",
        f"organization_context={'configured' if status == 'PASS' else 'unconfigured'}",
        f"operator_principal={'configured' if status == 'PASS' else 'unconfigured'}",
        f"principal_category={PRINCIPAL_CATEGORY if status == 'PASS' else 'unconfigured'}",
        f"actor_context={'configured' if status == 'PASS' else 'unconfigured'}",
        f"organization_scope_explicit={_safe_bool(status == 'PASS')}",
        f"principal_attributable={_safe_bool(status == 'PASS')}",
        "authorization_grants=0",
        "delegations=0",
        "organizational_authority_claimed=false",
        "authentication_evidence_refs=0",
        "tenant_context_introduced=false",
        "product_context_introduced=false",
        f"context_outside_source_control={_safe_bool(root_outside_git)}",
        f"context_owner_only={_safe_bool(context_owner_only)}",
        "credentials_present=false",
        "secrets_present=false",
        "canonical_mutation=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ]
    if failure_code is not None:
        lines.append(f"failure_code={failure_code}")
    return lines


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Bootstrap bounded internal Organization and operator context for P6.05-L4."
    )
    parser.add_argument("--target-root", required=True, type=Path)
    parser.add_argument("--owner-authorization", required=True, type=str)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines, _ = bootstrap_internal_context(
        args.target_root,
        owner_authorization=args.owner_authorization,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
