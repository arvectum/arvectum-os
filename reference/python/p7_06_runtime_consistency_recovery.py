#!/usr/bin/env python3
"""Bounded P7.06 runtime-consistency recovery for selected-Mac operation."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import plistlib
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RUNTIME_LABEL = "com.arvectum.os.persistent-internal"
OBSERVER_LABEL = "com.arvectum.os.p7-05-observer"
CANONICAL_REPO = "arvectum/arvectum-os"


class RecoveryError(RuntimeError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _run(args: list[str], *, cwd: Path | None = None, timeout: float = 60.0) -> tuple[int, str, str]:
    try:
        completed = subprocess.run(
            args,
            cwd=str(cwd) if cwd is not None else None,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RecoveryError(f"command failed: {Path(args[0]).name}") from exc
    return completed.returncode, completed.stdout, completed.stderr


def _validate_sha(value: str, label: str) -> str:
    normalized = value.strip().lower()
    if not SHA_RE.fullmatch(normalized):
        raise RecoveryError(f"{label} must be a full Git SHA")
    return normalized


def _canonical_head(repo_root: Path) -> str:
    repo_root = repo_root.resolve()
    rc, branch, _ = _run(["git", "branch", "--show-current"], cwd=repo_root, timeout=15)
    if rc != 0 or branch.strip() != "main":
        raise RecoveryError("canonical checkout must be on main")
    rc, dirty, _ = _run(["git", "status", "--porcelain"], cwd=repo_root, timeout=15)
    if rc != 0 or dirty.strip():
        raise RecoveryError("canonical checkout must be clean")
    rc, origin, _ = _run(["git", "remote", "get-url", "origin"], cwd=repo_root, timeout=15)
    origin = origin.strip()
    allowed_origins = {
        "https://github.com/arvectum/arvectum-os",
        "https://github.com/arvectum/arvectum-os.git",
        "git@github.com:arvectum/arvectum-os",
        "git@github.com:arvectum/arvectum-os.git",
        "ssh://git@github.com/arvectum/arvectum-os",
        "ssh://git@github.com/arvectum/arvectum-os.git",
    }
    if rc != 0 or origin not in allowed_origins:
        raise RecoveryError("origin is not canonical arvectum/arvectum-os")
    rc, _, _ = _run(["git", "fetch", "--quiet", "origin", "main"], cwd=repo_root, timeout=60)
    if rc != 0:
        raise RecoveryError("canonical origin/main fetch failed")
    rc, head, _ = _run(["git", "rev-parse", "HEAD"], cwd=repo_root, timeout=15)
    if rc != 0:
        raise RecoveryError("HEAD cannot be resolved")
    rc, origin_main, _ = _run(["git", "rev-parse", "origin/main"], cwd=repo_root, timeout=15)
    if rc != 0:
        raise RecoveryError("origin/main cannot be resolved")
    head_sha = _validate_sha(head, "HEAD")
    origin_sha = _validate_sha(origin_main, "origin/main")
    if head_sha != origin_sha:
        raise RecoveryError("local main must equal origin/main before recovery")
    return head_sha


def _current_release(root: Path) -> str:
    current = root / "current"
    if not current.is_symlink():
        raise RecoveryError("current release pointer must be a symlink")
    return _validate_sha(Path(os.readlink(current)).name, "current release")


def _load_plist(path: Path, label: str) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise RecoveryError(f"{label} LaunchAgent plist is missing or unsafe")
    if os.name != "nt" and path.stat().st_mode & 0o077:
        raise RecoveryError(f"{label} LaunchAgent plist is not owner-only")
    try:
        with path.open("rb") as handle:
            value = plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException) as exc:
        raise RecoveryError(f"{label} LaunchAgent plist is unreadable") from exc
    if not isinstance(value, dict) or value.get("Label") != label:
        raise RecoveryError(f"{label} LaunchAgent label mismatch")
    args = value.get("ProgramArguments")
    if not isinstance(args, list) or any(not isinstance(item, str) for item in args):
        raise RecoveryError(f"{label} ProgramArguments are invalid")
    return value


def _runtime_release_from_plist(root: Path, payload: dict[str, Any]) -> str:
    args = payload["ProgramArguments"]
    try:
        root_index = args.index("--runtime-root")
        release_index = args.index("--release-sha")
        runtime_root = args[root_index + 1]
        release = _validate_sha(args[release_index + 1], "runtime launchd release")
    except (ValueError, IndexError) as exc:
        raise RecoveryError("runtime LaunchAgent does not contain exact runtime/release arguments") from exc
    if runtime_root != str(root):
        raise RecoveryError("runtime LaunchAgent runtime-root mismatch")
    expected_python = root / "venvs" / release / "bin" / "python"
    expected_script = root / "releases" / release / "source/reference/python/p7_02_persistent_runtime.py"
    if len(args) < 2 or args[0] != str(expected_python) or args[1] != str(expected_script):
        raise RecoveryError("runtime LaunchAgent exact-release program pin mismatch")
    return release


def _observer_release_from_plist(root: Path, payload: dict[str, Any]) -> str:
    args = payload["ProgramArguments"]
    if len(args) < 2:
        raise RecoveryError("observer ProgramArguments are incomplete")
    py = Path(args[0])
    script = Path(args[1])
    try:
        release = _validate_sha(py.parents[1].name, "observer launchd release")
    except IndexError as exc:
        raise RecoveryError("observer Python path is not exact-release shaped") from exc
    expected_python = root / "venvs" / release / "bin" / "python"
    expected_script = root / "releases" / release / "source/reference/python/p7_05_operational_visibility.py"
    if py != expected_python or script != expected_script:
        raise RecoveryError("observer LaunchAgent exact-release program pin mismatch")
    try:
        root_index = args.index("--runtime-root")
        runtime_root = args[root_index + 1]
    except (ValueError, IndexError) as exc:
        raise RecoveryError("observer LaunchAgent runtime-root argument is missing") from exc
    if runtime_root != str(root):
        raise RecoveryError("observer LaunchAgent runtime-root mismatch")
    return release


def _launchd_pid(label: str) -> int:
    target = f"gui/{os.getuid()}/{label}"
    rc, out, _ = _run(["launchctl", "print", target], timeout=15)
    if rc != 0:
        raise RecoveryError(f"{label} launchd target is not loaded")
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("pid = "):
            value = line.split("=", 1)[1].strip()
            if value.isdigit() and int(value) > 0:
                return int(value)
    raise RecoveryError(f"{label} launchd target has no live pid")


def _verify_release_manifest(root: Path, release: str) -> None:
    release_root = root / "releases" / release
    manifest_path = release_root / "release-manifest.json"
    python_path = root / "venvs" / release / "bin" / "python"
    runtime_path = release_root / "source/reference/python/p7_02_persistent_runtime.py"
    observer_path = release_root / "source/reference/python/p7_05_operational_visibility.py"
    if not release_root.is_dir() or release_root.is_symlink():
        raise RecoveryError("running exact release directory is unavailable or unsafe")
    if not python_path.is_file() or not os.access(python_path, os.X_OK):
        raise RecoveryError("running exact-release Python is missing")
    if not runtime_path.is_file() or not observer_path.is_file():
        raise RecoveryError("running exact-release runtime/observer source is incomplete")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RecoveryError("running exact-release manifest is unreadable") from exc
    if (
        not isinstance(manifest, dict)
        or manifest.get("canonical_repository") != CANONICAL_REPO
        or manifest.get("release_sha") != release
    ):
        raise RecoveryError("running exact-release manifest identity mismatch")


def _verify_runtime_health(root: Path, release: str, launchd_pid: int) -> dict[str, Any]:
    py = root / "venvs" / release / "bin" / "python"
    runtime = root / "releases" / release / "source/reference/python/p7_02_persistent_runtime.py"
    rc, out, err = _run(
        [
            str(py),
            str(runtime),
            "check",
            "--runtime-root",
            str(root),
            "--expected-release",
            release,
            "--max-age-seconds",
            "20",
            "--json",
        ],
        timeout=30,
    )
    if rc != 0:
        detail = err.strip().splitlines()[-1] if err.strip() else "health check failed"
        raise RecoveryError(f"running release health verification failed: {detail}")
    try:
        health = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RecoveryError("running release health JSON is invalid") from exc
    if not isinstance(health, dict) or health.get("release_sha") != release:
        raise RecoveryError("running release health identity mismatch")
    if health.get("pid") != launchd_pid:
        raise RecoveryError("runtime health pid does not match launchd pid")
    return health


def _digest_paths(root: Path, paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for base in paths:
        if not base.exists():
            digest.update(f"ABSENT:{base.relative_to(root).as_posix()}\n".encode())
            continue
        if base.is_symlink():
            raise RecoveryError("symlink is not allowed in protected digest input")
        members = [base] if base.is_file() else sorted(path for path in base.rglob("*") if path.is_file())
        for path in members:
            if path.is_symlink():
                raise RecoveryError("symlink is not allowed in protected digest input")
            digest.update(path.relative_to(root).as_posix().encode() + b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
    return digest.hexdigest()


def _p703_digest(root: Path) -> str:
    return _digest_paths(root, (root / "state/governed", root / "state/checkpoints"))


def _p704_digest(root: Path) -> str:
    return _digest_paths(root, (root / "config/p7-04-access.json", root / "secrets/p7-04"))


def _atomic_replace_current(root: Path, release: str) -> None:
    destination = root / "current"
    if not destination.is_symlink():
        raise RecoveryError("current pointer ceased to be a symlink before recovery")
    prepared = root / f".current-recovery-{os.getpid()}"
    try:
        prepared.unlink(missing_ok=True)
        prepared.symlink_to(root / "releases" / release)
        if not prepared.is_symlink():
            raise RecoveryError("could not prepare recovery symlink")
        os.replace(prepared, destination)
    finally:
        prepared.unlink(missing_ok=True)


def _write_evidence(root: Path, value: dict[str, Any]) -> tuple[Path, str]:
    directory = root / "evidence/p7-06-consistency-recovery"
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        os.chmod(directory, 0o700)
    path = directory / (
        "p7-06-runtime-consistency-recovery-"
        f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}.json"
    )
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    digest = hashlib.sha256(raw).hexdigest()
    sidecar = path.with_suffix(path.suffix + ".sha256")
    fd = os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(f"{digest}  {path.name}\n")
        handle.flush()
        os.fsync(handle.fileno())
    return path, digest


def _validate_decision_ref(value: str) -> str:
    value = value.strip()
    if not value or len(value) > 256 or any(ch in value for ch in "\r\n\0"):
        raise RecoveryError("decision-ref is invalid")
    return value


def recover(root: Path, repo_root: Path, decision_ref: str) -> dict[str, Any]:
    if sys.platform != "darwin":
        raise RecoveryError("macOS is required")
    root = root.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve()
    decision_ref = _validate_decision_ref(decision_ref)
    if not root.is_dir():
        raise RecoveryError("runtime root is unavailable")
    canonical_head = _canonical_head(repo_root)

    lock_dir = root / "run/p7-06-deploy.lock"
    try:
        lock_dir.mkdir()
    except FileExistsError as exc:
        raise RecoveryError("another P7.06 deployment/recovery transaction is active") from exc
    try:
        (lock_dir / "pid").write_text(f"{os.getpid()}\n", encoding="utf-8")
        if os.name != "nt":
            os.chmod(lock_dir / "pid", 0o600)

        current_before = _current_release(root)
        runtime_plist = _load_plist(Path.home() / f"Library/LaunchAgents/{RUNTIME_LABEL}.plist", RUNTIME_LABEL)
        observer_plist = _load_plist(Path.home() / f"Library/LaunchAgents/{OBSERVER_LABEL}.plist", OBSERVER_LABEL)
        runtime_release = _runtime_release_from_plist(root, runtime_plist)
        observer_release = _observer_release_from_plist(root, observer_plist)
        if runtime_release != observer_release:
            raise RecoveryError("runtime and observer exact-release pins disagree")
        if current_before == runtime_release:
            raise RecoveryError("current pointer already matches the proven running release; recovery is unnecessary")

        _verify_release_manifest(root, runtime_release)
        runtime_pid = _launchd_pid(RUNTIME_LABEL)
        health = _verify_runtime_health(root, runtime_release, runtime_pid)

        p703_before = _p703_digest(root)
        p704_before = _p704_digest(root)

        current_before_dir = root / "releases" / current_before
        if not current_before_dir.is_dir() or current_before_dir.is_symlink():
            raise RecoveryError("pre-recovery current release directory is unavailable or unsafe")

        _atomic_replace_current(root, runtime_release)
        pointer_mutated = True
        try:
            p702 = repo_root / "reference/python/p7_02_macos_service.sh"
            p705 = repo_root / "reference/python/p7_05_macos_observer.sh"
            rc, _, err = _run(["sh", str(p702), "status"], cwd=repo_root, timeout=30)
            if rc != 0:
                detail = err.strip().splitlines()[-1] if err.strip() else "unknown"
                raise RecoveryError(f"P7.02 status failed after pointer reconciliation: {detail}")
            rc, _, err = _run(["sh", str(p705), "status"], cwd=repo_root, timeout=30)
            if rc != 0:
                detail = err.strip().splitlines()[-1] if err.strip() else "unknown"
                raise RecoveryError(f"P7.05 observer status failed after pointer reconciliation: {detail}")

            current_after = _current_release(root)
            if current_after != runtime_release:
                raise RecoveryError("current pointer did not remain on proven running release")

            p703_after = _p703_digest(root)
            p704_after = _p704_digest(root)
            if p703_before != p703_after:
                raise RecoveryError("P7.03 governed/checkpoint state changed during recovery")
            if p704_before != p704_after:
                raise RecoveryError("P7.04 access state changed during recovery")
        except (RecoveryError, OSError, ValueError, json.JSONDecodeError) as exc:
            if pointer_mutated:
                try:
                    _atomic_replace_current(root, current_before)
                    pointer_mutated = False
                except (RecoveryError, OSError) as restore_exc:
                    raise RecoveryError(
                        "post-reconciliation verification failed and pre-recovery pointer restoration also failed"
                    ) from restore_exc
            failure = {
                "schema": "arvectum.p7_06.runtime-consistency-recovery/1",
                "classification": "owner-local operational recovery evidence; non-canonical",
                "result": "FAILED_ROLLED_BACK",
                "decision_ref": decision_ref,
                "canonical_repository": CANONICAL_REPO,
                "canonical_head": canonical_head,
                "current_before": current_before,
                "proven_running_release": runtime_release,
                "current_after_failure": _current_release(root),
                "failure_reason": "post-reconciliation verification failed; pre-recovery pointer restored",
                "p703_unchanged": _p703_digest(root) == p703_before,
                "p704_unchanged": _p704_digest(root) == p704_before,
                "canonical_state_mutated": False,
                "product_external_effect_invoked": False,
                "historical_external_effect_replayed": False,
                "reusable_secret_emitted": False,
                "recorded_at": _utc_now(),
            }
            try:
                _write_evidence(root, failure)
            except OSError:
                pass
            raise exc

        result = {
            "schema": "arvectum.p7_06.runtime-consistency-recovery/1",
            "classification": "owner-local operational recovery evidence; non-canonical",
            "result": "PASS",
            "decision_ref": decision_ref,
            "canonical_repository": CANONICAL_REPO,
            "canonical_head": canonical_head,
            "current_before": current_before,
            "proven_running_release": runtime_release,
            "observer_release_pin": observer_release,
            "runtime_launchd_pid": runtime_pid,
            "runtime_health_pid": health.get("pid"),
            "current_after": current_after,
            "recovery_action": "current pointer atomically reconciled to already-running proven exact release",
            "runtime_process_restarted": False,
            "observer_reinstalled": False,
            "governed_update_invoked": False,
            "rollback_invoked": False,
            "ui3_lifecycle_invoked": False,
            "p703_unchanged": True,
            "p704_unchanged": True,
            "canonical_state_mutated": False,
            "organizational_authority_provided": False,
            "consequential_approval_provided": False,
            "product_external_effect_invoked": False,
            "historical_external_effect_replayed": False,
            "reusable_secret_emitted": False,
            "recorded_at": _utc_now(),
        }
        path, digest = _write_evidence(root, result)
        result["attestation_basename"] = path.name
        result["attestation_sha256"] = digest
        return result
    finally:
        try:
            for child in lock_dir.iterdir():
                child.unlink()
            lock_dir.rmdir()
        except FileNotFoundError:
            pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P7.06 selected-Mac runtime-consistency recovery")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--decision-ref", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = recover(Path(args.runtime_root), Path(args.repo_root), args.decision_ref)
    except (RecoveryError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.06 runtime consistency recovery FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            "P7.06 runtime consistency recovery PASS "
            f"from={result['current_before']} to={result['current_after']} "
            f"attestation={result['attestation_basename']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
