#!/usr/bin/env python3
"""Guarded operator entrypoint for P7.07 persistent Tender Operator contour.

The large P7.07 contour module is the private semantic/runtime implementation.
This module is the supported owner-operated CLI boundary. It adds two fail-closed
controls discovered by functional cross-review:

* any temporary setup grant created during an attempted setup is revoked even if
  the low-level setup fails while another exception is propagating; newly-created
  item-scoped read grants are also rolled back when setup does not complete;
* the product-owned Tender Agent bridge is structurally validated before Python
  executes that module. Only the narrow current IntegrationAdapters delegation
  shape is accepted for ``resolve_document``; executable top-level behavior and
  imports outside the bounded product/platform seam fail closed.

These controls remain private/reversible operational hardening. They do not make
source layout, AST shape, persistence representation or this CLI a Stable/public
Product Contract or platform API.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
from pathlib import Path
from typing import Any, Final

import p7_04_persistent_access as p704
import p7_07_persistent_tender_operator_contour as p707


BRIDGE_ALLOWED_IMPORTS: Final = frozenset(
    {
        "__future__",
        "dataclasses",
        "datetime",
        "typing",
        "arvectum_os_ref.integration_adapters",
        "p6_03_tender_operator_ref.contract",
    }
)


class P707GuardError(RuntimeError):
    """Fail-closed P7.07 operator-boundary error."""


def _bridge_path(product_repo: Path) -> Path:
    repo = product_repo.expanduser().resolve(strict=True)
    path = (repo / p707.PRODUCT_BRIDGE_RELATIVE_PATH).resolve(strict=True)
    try:
        path.relative_to(repo)
    except ValueError as exc:
        raise P707GuardError("Tender Agent bridge escaped product repository") from exc
    if not path.is_file() or path.is_symlink():
        raise P707GuardError("Tender Agent bridge must be one regular non-symlink file")
    return path


def _attribute_chain(value: ast.expr) -> tuple[str, ...]:
    result: list[str] = []
    current: ast.expr = value
    while isinstance(current, ast.Attribute):
        result.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        result.append(current.id)
    else:
        return ()
    return tuple(reversed(result))


def validate_product_bridge(product_repo: Path) -> str:
    """Validate the exact narrow bridge shape before module execution.

    This is intentionally not a general Python sandbox. It is a fail-closed shape
    guard for the one product-owned module P7.07 is about to execute.
    """

    path = _bridge_path(product_repo)
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError) as exc:
        raise P707GuardError("Tender Agent bridge is not readable valid Python") from exc

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            raise P707GuardError("Tender Agent bridge direct import is outside the bounded shape")
        if isinstance(node, ast.ImportFrom) and (node.module or "") not in BRIDGE_ALLOWED_IMPORTS:
            raise P707GuardError(
                f"Tender Agent bridge import outside bounded seam: {node.module!r}"
            )

    for index, node in enumerate(tree.body):
        if isinstance(node, ast.Expr):
            if (
                index != 0
                or not isinstance(node.value, ast.Constant)
                or not isinstance(node.value.value, str)
            ):
                raise P707GuardError("Tender Agent bridge has executable top-level expression")
            continue
        if isinstance(node, ast.ImportFrom):
            continue
        if isinstance(node, ast.If):
            if (
                not isinstance(node.test, ast.Name)
                or node.test.id != "TYPE_CHECKING"
                or node.orelse
                or any(not isinstance(child, ast.ImportFrom) for child in node.body)
            ):
                raise P707GuardError("Tender Agent bridge has executable top-level conditional")
            continue
        if isinstance(node, ast.ClassDef):
            continue
        raise P707GuardError("Tender Agent bridge has executable top-level behavior")

    classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == p707.PRODUCT_BRIDGE_CLASS
    ]
    if len(classes) != 1:
        raise P707GuardError("ArvectumOSBridge must be declared exactly once")
    bridge_class = classes[0]
    if len(bridge_class.decorator_list) != 1:
        raise P707GuardError("ArvectumOSBridge decorator shape drifted")
    decorator = bridge_class.decorator_list[0]
    if not (
        isinstance(decorator, ast.Call)
        and isinstance(decorator.func, ast.Name)
        and decorator.func.id == "dataclass"
    ):
        raise P707GuardError("ArvectumOSBridge must remain the bounded dataclass bridge")

    for node in bridge_class.body:
        if isinstance(node, ast.Expr):
            if not isinstance(node.value, ast.Constant) or not isinstance(node.value.value, str):
                raise P707GuardError("ArvectumOSBridge class body has executable expression")
            continue
        if isinstance(node, (ast.AnnAssign, ast.FunctionDef)):
            continue
        raise P707GuardError("ArvectumOSBridge class body has executable behavior")

    methods = [
        node
        for node in bridge_class.body
        if isinstance(node, ast.FunctionDef) and node.name == "resolve_document"
    ]
    if len(methods) != 1:
        raise P707GuardError("resolve_document must be declared exactly once")
    method = methods[0]
    if method.decorator_list:
        raise P707GuardError("resolve_document must remain a direct instance-method delegation")
    body = list(method.body)
    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        body = body[1:]
    if len(body) != 1 or not isinstance(body[0], ast.Return) or not isinstance(body[0].value, ast.Call):
        raise P707GuardError("resolve_document must contain one pure delegation return")
    call = body[0].value
    if _attribute_chain(call.func) != (
        "self",
        "adapters",
        "capabilities",
        "resolve_document",
    ):
        raise P707GuardError("resolve_document no longer delegates to CAP-001 IntegrationAdapters")
    if call.args:
        raise P707GuardError("resolve_document must delegate by explicit keywords only")
    expected_keywords = {"request", "governed_versions", "admitted", "artifact_id"}
    if {item.arg for item in call.keywords} != expected_keywords:
        raise P707GuardError("resolve_document governed argument set drifted")
    for item in call.keywords:
        if item.arg is None or not isinstance(item.value, ast.Name) or item.value.id != item.arg:
            raise P707GuardError("resolve_document rewrites a governed argument")

    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def _active_grants(access_root: Path, *, operation: str, resource_prefix: str) -> set[str]:
    state = p704.load_access_store(access_root)
    result: set[str] = set()
    for grant_id, grant in state.get("grants", {}).items():
        if not isinstance(grant, dict) or grant.get("status") != "active":
            continue
        resource = grant.get("resource")
        if (
            grant.get("operation") == operation
            and isinstance(resource, str)
            and resource.startswith(resource_prefix)
            and grant.get("access_paths") == [p707.ACCESS_PATH]
        ):
            result.add(grant_id)
    return result


def _cleanup_new_grants(
    access_root: Path,
    *,
    setup_before: set[str],
    read_before: set[str],
    rollback_new_reads: bool,
) -> None:
    current_setup = _active_grants(
        access_root,
        operation=p707.SETUP_ACCESS_OPERATION,
        resource_prefix=p707.SETUP_ACCESS_RESOURCE,
    )
    for grant_id in sorted(current_setup - setup_before):
        p704.revoke_grant(access_root, grant_id)

    if rollback_new_reads:
        current_reads = _active_grants(
            access_root,
            operation=p707.READ_ACCESS_OPERATION,
            resource_prefix=p707.READ_RESOURCE_PREFIX,
        )
        for grant_id in sorted(current_reads - read_before):
            p704.revoke_grant(access_root, grant_id)

    remaining_setup = _active_grants(
        access_root,
        operation=p707.SETUP_ACCESS_OPERATION,
        resource_prefix=p707.SETUP_ACCESS_RESOURCE,
    )
    if remaining_setup - setup_before:
        raise P707GuardError("new temporary P7.07 setup grant remains active after cleanup")


def guarded_setup(**kwargs: Any) -> p707.SetupResult:
    access_root = Path(kwargs["access_root"])
    setup_before = _active_grants(
        access_root,
        operation=p707.SETUP_ACCESS_OPERATION,
        resource_prefix=p707.SETUP_ACCESS_RESOURCE,
    )
    if setup_before:
        raise P707GuardError(
            "pre-existing active P7.07 setup grant requires explicit repair before retry"
        )
    read_before = _active_grants(
        access_root,
        operation=p707.READ_ACCESS_OPERATION,
        resource_prefix=p707.READ_RESOURCE_PREFIX,
    )
    succeeded = False
    try:
        result = p707.run_setup(**kwargs)
        succeeded = True
        return result
    finally:
        try:
            _cleanup_new_grants(
                access_root,
                setup_before=setup_before,
                read_before=read_before,
                rollback_new_reads=not succeeded,
            )
        except Exception as exc:
            raise P707GuardError("P7.07 setup privilege cleanup failed closed") from exc


def guarded_consume(**kwargs: Any) -> p707.ConsumptionResult:
    product_repo = Path(kwargs["product_repo"])
    validate_product_bridge(product_repo)
    return p707.run_consume(**kwargs)


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--access-root", type=Path, required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--evidence-output", type=Path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("setup")
    _common(setup)
    setup.add_argument("--l7-manifest", type=Path, required=True)
    setup.add_argument("--owner-approval", required=True)
    consume = sub.add_parser("consume")
    _common(consume)
    consume.add_argument("--product-repo", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    kwargs = vars(args).copy()
    command = kwargs.pop("command")
    try:
        if command == "setup":
            result = guarded_setup(**kwargs)
            print(f"RESULT={result.status}")
            print(f"STORAGE_ITEM_ID={result.storage_item_id}")
            print(f"EVIDENCE_PATH={result.evidence_path}")
        else:
            bridge_sha = validate_product_bridge(kwargs["product_repo"])
            result = guarded_consume(**kwargs)
            print(f"RESULT={result.status}")
            print(f"STORAGE_ITEM_ID={result.storage_item_id}")
            print(f"PRODUCT_BRIDGE_SHA256={bridge_sha}")
            print(f"EVIDENCE_PATH={result.evidence_path}")
        print("OPERATOR_ENTRYPOINT_GUARD=PASS")
        return 0
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
