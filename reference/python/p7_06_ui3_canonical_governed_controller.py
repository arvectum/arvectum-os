#!/usr/bin/env python3
"""Canonical-checkout controller for UI3 + P7.06 governed lifecycle.

The private UI3 service remains exact-release pinned to ``runtime/current``.
Deployment/rollback control, however, must execute from the real canonical Git
checkout because ``p7_06_macos_deploy.sh`` validates and advances that checkout.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
LABEL = "com.arvectum.os.p7-06-ui3-operator"
CANONICAL_ORIGINS = {
    "https://github.com/arvectum/arvectum-os",
    "https://github.com/arvectum/arvectum-os.git",
    "git@github.com:arvectum/arvectum-os",
    "git@github.com:arvectum/arvectum-os.git",
    "ssh://git@github.com/arvectum/arvectum-os",
    "ssh://git@github.com/arvectum/arvectum-os.git",
}


class UI3GovernedControllerError(RuntimeError):
    pass


def _run(
    args: Sequence[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    timeout: float = 300.0,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            list(args),
            cwd=str(cwd) if cwd is not None else None,
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise UI3GovernedControllerError(f"bounded command failed: {Path(args[0]).name}") from exc


def _validate_sha(value: str, label: str) -> str:
    value = value.strip().lower()
    if not SHA_RE.fullmatch(value):
        raise UI3GovernedControllerError(f"{label} must be a full Git SHA")
    return value


def canonical_head(repo_root: Path) -> str:
    repo_root = repo_root.expanduser().resolve()
    inside = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd=repo_root, timeout=15)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        raise UI3GovernedControllerError("canonical repository checkout is unavailable")

    branch = _run(["git", "branch", "--show-current"], cwd=repo_root, timeout=15)
    if branch.returncode != 0 or branch.stdout.strip() != "main":
        raise UI3GovernedControllerError("canonical checkout must be on main")

    dirty = _run(["git", "status", "--porcelain"], cwd=repo_root, timeout=15)
    if dirty.returncode != 0 or dirty.stdout.strip():
        raise UI3GovernedControllerError("canonical checkout must be clean")

    origin = _run(["git", "remote", "get-url", "origin"], cwd=repo_root, timeout=15)
    if origin.returncode != 0 or origin.stdout.strip() not in CANONICAL_ORIGINS:
        raise UI3GovernedControllerError("origin is not canonical arvectum/arvectum-os")

    fetched = _run(["git", "fetch", "--quiet", "origin", "main"], cwd=repo_root, timeout=90)
    if fetched.returncode != 0:
        raise UI3GovernedControllerError("canonical origin/main fetch failed")

    head = _run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=15)
    origin_main = _run(["git", "rev-parse", "origin/main"], cwd=repo_root, timeout=15)
    if head.returncode != 0 or origin_main.returncode != 0:
        raise UI3GovernedControllerError("canonical HEAD/origin-main cannot be resolved")
    head_sha = _validate_sha(head.stdout, "canonical HEAD")
    origin_sha = _validate_sha(origin_main.stdout, "origin/main")
    if head_sha != origin_sha:
        raise UI3GovernedControllerError("canonical main must equal origin/main")
    return head_sha


def _runtime_root(root: Path) -> Path:
    value = root.expanduser().resolve()
    if not value.is_dir():
        raise UI3GovernedControllerError("runtime root is unavailable or unsafe")
    return value


def current_release(root: Path) -> str:
    current = root / "current"
    if not current.is_symlink():
        raise UI3GovernedControllerError("current release pointer is missing or unsafe")
    return _validate_sha(Path(os.readlink(current)).name, "current release")


def _controller_paths(repo_root: Path) -> tuple[Path, Path]:
    ui3 = repo_root / "reference/python/p7_06_ui3_macos_operator.sh"
    deploy = repo_root / "reference/python/p7_06_macos_deploy.sh"
    for path, label in ((ui3, "UI3 controller"), (deploy, "P7.06 deploy controller")):
        if path.is_symlink() or not path.is_file():
            raise UI3GovernedControllerError(f"canonical {label} is missing or unsafe")
    return ui3, deploy


def _environment(root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["ARVECTUM_P7_02_ROOT"] = str(root)
    return env


def _service_loaded() -> bool:
    result = _run(["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"], timeout=15)
    return result.returncode == 0


def _run_ui3(repo_root: Path, root: Path, *args: str, require_success: bool = True) -> subprocess.CompletedProcess[str]:
    ui3, _ = _controller_paths(repo_root)
    result = _run(["sh", str(ui3), *args], cwd=repo_root, env=_environment(root), timeout=90)
    if require_success and result.returncode != 0:
        raise UI3GovernedControllerError(f"canonical UI3 controller failed: {args[0] if args else 'unknown'}")
    return result


def run_canonical_deploy(root: Path, repo_root: Path, deploy_args: Sequence[str]) -> None:
    """Run the unchanged P7.06 deploy adapter from the canonical Git checkout."""
    root = _runtime_root(root)
    repo_root = repo_root.expanduser().resolve()
    canonical_head(repo_root)
    _, deploy = _controller_paths(repo_root)
    if not deploy_args or deploy_args[0] not in {"update", "rollback-last"}:
        raise UI3GovernedControllerError("unsupported canonical deploy operation")
    result = _run(
        ["sh", str(deploy), *deploy_args],
        cwd=repo_root,
        env=_environment(root),
        timeout=300,
    )
    if result.returncode != 0:
        raise UI3GovernedControllerError(f"canonical P7.06 deploy failed: {deploy_args[0]}")


def _current_has_ui3(root: Path) -> bool:
    release = current_release(root)
    base = root / "releases" / release / "source/reference/python"
    module = base / "p7_06_ui3_private_operator.py"
    return module.is_file() and not module.is_symlink()


def _known_private_paths(root: Path) -> tuple[Path, ...]:
    return (
        Path.home() / "Library/LaunchAgents" / f"{LABEL}.plist",
        root / "service" / f"{LABEL}.plist",
        root / "config/p7-06-ui3.json",
        root / "secrets/p7-06-ui3/access.secret",
        root / "logs/p7-06-ui3.stdout.log",
        root / "logs/p7-06-ui3.stderr.log",
    )


def _cleanup_pre_ui3(root: Path, repo_root: Path) -> None:
    if _service_loaded():
        _run_ui3(repo_root, root, "stop")
    for path in _known_private_paths(root):
        if path.exists() and path.is_dir() and not path.is_symlink():
            raise UI3GovernedControllerError(f"unexpected directory at UI3 private-material path: {path.name}")
        path.unlink(missing_ok=True)
    secret_dir = root / "secrets/p7-06-ui3"
    try:
        secret_dir.rmdir()
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise UI3GovernedControllerError("unexpected residual material in UI3 secret directory") from exc
    if _service_loaded() or any(path.exists() or path.is_symlink() for path in _known_private_paths(root)):
        raise UI3GovernedControllerError("pre-UI3 cleanup did not remove the private surface")


def reconcile_current(root: Path, repo_root: Path) -> None:
    """Reconcile UI3 presentation only; never change P7.06 runtime release."""
    root = _runtime_root(root)
    repo_root = repo_root.expanduser().resolve()
    if _current_has_ui3(root):
        _run_ui3(repo_root, root, "install")
        _run_ui3(repo_root, root, "status")
    else:
        _cleanup_pre_ui3(root, repo_root)


def governed_operation(root: Path, repo_root: Path, operation: str, decision_ref: str | None = None) -> None:
    """Stop UI3, run canonical P7.06 operation, then reconcile exact current UI3."""
    root = _runtime_root(root)
    repo_root = repo_root.expanduser().resolve()
    canonical_head(repo_root)
    _controller_paths(repo_root)

    if operation not in {"update", "rollback-last"}:
        raise UI3GovernedControllerError("unsupported UI3 governed operation")
    if operation == "update" and (decision_ref is None or not decision_ref.strip()):
        raise UI3GovernedControllerError("governed update requires a decision reference")

    if _service_loaded():
        _run_ui3(repo_root, root, "status")
        _run_ui3(repo_root, root, "stop")

    deploy_args: list[str] = [operation]
    if operation == "update":
        deploy_args.append(decision_ref.strip())

    deploy_error: Exception | None = None
    try:
        run_canonical_deploy(root, repo_root, deploy_args)
    except (UI3GovernedControllerError, OSError) as exc:
        deploy_error = exc

    try:
        reconcile_current(root, repo_root)
    except (UI3GovernedControllerError, OSError) as reconcile_exc:
        if deploy_error is not None:
            raise UI3GovernedControllerError(
                "canonical P7.06 operation failed and UI3 reconciliation also failed"
            ) from reconcile_exc
        raise

    if deploy_error is not None:
        raise UI3GovernedControllerError(
            f"canonical P7.06 {operation} failed; resulting exact-current UI3 state was reconciled"
        ) from deploy_error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P7.06-UI3 canonical governed lifecycle controller")
    parser.add_argument("operation", choices=("update", "rollback-last"))
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--decision-ref")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        governed_operation(
            Path(args.runtime_root),
            Path(args.repo_root),
            args.operation,
            args.decision_ref,
        )
    except (UI3GovernedControllerError, OSError, ValueError) as exc:
        print(f"P7.06-UI3 canonical controller FAIL: {exc}", file=sys.stderr)
        return 1
    print(f"P7.06-UI3 canonical controller PASS operation={args.operation} current={current_release(Path(args.runtime_root).expanduser().resolve())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
