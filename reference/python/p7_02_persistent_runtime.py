#!/usr/bin/env python3
"""P7.02 persistent-internal runtime envelope for the owner-operated Mac mini.

This module is deliberately a small environment adapter.  It does not expose a
network API, does not execute product effects, and does not create canonical
state.  Its responsibilities are limited to:

* loading the existing bounded Arvectum OS reference-runtime semantic modules;
* maintaining a single supervised process instance;
* publishing secret-safe, non-canonical liveness/health telemetry outside Git;
* exposing a local CLI health check used by the macOS launchd adapter.

The launchd mechanism and this process envelope are not platform contracts.
"""

from __future__ import annotations

import argparse
import fcntl
import importlib
import json
import os
import platform
import signal
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


DEFAULT_HEARTBEAT_SECONDS = 5.0
DEFAULT_STALE_AFTER_SECONDS = 20.0
HEALTH_SCHEMA = "arvectum.p7_02.runtime-health/1"
EXPECTED_MODULES = (
    "arvectum_os_ref.canonical_lineage",
    "arvectum_os_ref.governed_execution",
    "arvectum_os_ref.event_provenance",
    "arvectum_os_ref.product_contract",
    "arvectum_os_ref.portability_runtime",
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _atomic_json_write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp_name, 0o600)
        os.replace(tmp_name, path)
    finally:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            value = json.load(handle)
    except FileNotFoundError:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path}")
    return value


def _validate_release_sha(value: str) -> str:
    normalized = value.strip().lower()
    if len(normalized) != 40 or any(ch not in "0123456789abcdef" for ch in normalized):
        raise ValueError("release SHA must be a full 40-character Git commit SHA")
    return normalized


def _semantic_self_check(modules: Iterable[str] = EXPECTED_MODULES) -> list[str]:
    loaded: list[str] = []
    for module_name in modules:
        importlib.import_module(module_name)
        loaded.append(module_name)
    return loaded


def _read_previous_health(path: Path) -> Dict[str, Any]:
    try:
        return _load_json(path)
    except (OSError, ValueError, json.JSONDecodeError):
        return {}


def _new_health_payload(
    *,
    release_sha: str,
    instance_id: str,
    generation: int,
    started_at: str,
    state: str,
    semantic_modules: list[str],
    previous_instance_id: Optional[str],
) -> Dict[str, Any]:
    now = _utc_now()
    return {
        "schema": HEALTH_SCHEMA,
        "classification": "non-canonical operational telemetry",
        "operating_mode": "Persistent Internal / owner-operated",
        "organization_scope": "ООО «Арвектум»",
        "operating_role": "Arvectum OS Owner-Operator",
        "network_listener_mode": "none",
        "product_effects_enabled": False,
        "canonical_state_written": False,
        "release_sha": release_sha,
        "instance_id": instance_id,
        "previous_instance_id": previous_instance_id,
        "generation": generation,
        "pid": os.getpid(),
        "started_at": started_at,
        "heartbeat_at": now,
        "state": state,
        "semantic_imports_ok": True,
        "semantic_modules": semantic_modules,
        "python_version": platform.python_version(),
        "platform_system": platform.system(),
    }


def run_runtime(args: argparse.Namespace) -> int:
    release_sha = _validate_release_sha(args.release_sha)
    runtime_root = Path(args.runtime_root).expanduser().resolve()
    run_root = runtime_root / "run"
    run_root.mkdir(parents=True, exist_ok=True)
    os.chmod(run_root, 0o700)

    health_path = run_root / "health.json"
    lock_path = run_root / "runtime.lock"
    lock_handle = lock_path.open("a+", encoding="utf-8")
    os.chmod(lock_path, 0o600)
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("P7.02 runtime already has an active owner process", file=sys.stderr)
        return 73

    semantic_modules = _semantic_self_check()
    previous = _read_previous_health(health_path)
    previous_instance_id = previous.get("instance_id") if isinstance(previous.get("instance_id"), str) else None
    previous_generation = previous.get("generation")
    generation = previous_generation + 1 if isinstance(previous_generation, int) and previous_generation >= 0 else 1

    instance_id = str(uuid.uuid4())
    started_at = _utc_now()
    stop_requested = False

    def request_stop(_signum: int, _frame: object) -> None:
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)

    payload = _new_health_payload(
        release_sha=release_sha,
        instance_id=instance_id,
        generation=generation,
        started_at=started_at,
        state="healthy",
        semantic_modules=semantic_modules,
        previous_instance_id=previous_instance_id,
    )
    _atomic_json_write(health_path, payload)

    interval = float(args.heartbeat_seconds)
    if interval <= 0:
        raise ValueError("heartbeat interval must be positive")

    while not stop_requested:
        time.sleep(interval)
        payload["heartbeat_at"] = _utc_now()
        payload["state"] = "healthy"
        _atomic_json_write(health_path, payload)

    payload["heartbeat_at"] = _utc_now()
    payload["state"] = "stopped"
    payload["stopped_at"] = _utc_now()
    _atomic_json_write(health_path, payload)
    return 0


def check_health(args: argparse.Namespace) -> int:
    runtime_root = Path(args.runtime_root).expanduser().resolve()
    health_path = runtime_root / "run" / "health.json"
    try:
        health = _load_json(health_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.02 health FAIL: unreadable health telemetry: {exc}", file=sys.stderr)
        return 2

    if health.get("schema") != HEALTH_SCHEMA:
        print("P7.02 health FAIL: unexpected health schema", file=sys.stderr)
        return 3
    if health.get("state") != "healthy":
        print(f"P7.02 health FAIL: state={health.get('state')!r}", file=sys.stderr)
        return 4
    if health.get("network_listener_mode") != "none":
        print("P7.02 health FAIL: runtime declared a network listener", file=sys.stderr)
        return 5
    if health.get("product_effects_enabled") is not False:
        print("P7.02 health FAIL: product effects must remain disabled", file=sys.stderr)
        return 6

    if args.expected_release:
        expected = _validate_release_sha(args.expected_release)
        if health.get("release_sha") != expected:
            print(
                f"P7.02 health FAIL: release mismatch health={health.get('release_sha')} expected={expected}",
                file=sys.stderr,
            )
            return 7

    heartbeat_raw = health.get("heartbeat_at")
    if not isinstance(heartbeat_raw, str):
        print("P7.02 health FAIL: missing heartbeat timestamp", file=sys.stderr)
        return 8
    try:
        heartbeat = datetime.fromisoformat(heartbeat_raw.replace("Z", "+00:00"))
    except ValueError:
        print("P7.02 health FAIL: invalid heartbeat timestamp", file=sys.stderr)
        return 9
    age = (datetime.now(timezone.utc) - heartbeat).total_seconds()
    max_age = float(args.max_age_seconds)
    if age < -5 or age > max_age:
        print(f"P7.02 health FAIL: heartbeat age {age:.1f}s exceeds {max_age:.1f}s", file=sys.stderr)
        return 10

    pid = health.get("pid")
    if not isinstance(pid, int) or pid <= 0:
        print("P7.02 health FAIL: invalid pid", file=sys.stderr)
        return 11
    try:
        os.kill(pid, 0)
    except OSError:
        print(f"P7.02 health FAIL: pid {pid} is not alive", file=sys.stderr)
        return 12

    if args.json:
        print(json.dumps(health, ensure_ascii=False, sort_keys=True))
    else:
        print(
            "P7.02 health PASS "
            f"release={health.get('release_sha')} pid={pid} generation={health.get('generation')} age={age:.1f}s"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.02 persistent runtime envelope")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="run the persistent runtime envelope")
    run_parser.add_argument("--runtime-root", required=True)
    run_parser.add_argument("--release-sha", required=True)
    run_parser.add_argument("--heartbeat-seconds", type=float, default=DEFAULT_HEARTBEAT_SECONDS)
    run_parser.set_defaults(handler=run_runtime)

    check_parser = subparsers.add_parser("check", help="check secret-safe local health telemetry")
    check_parser.add_argument("--runtime-root", required=True)
    check_parser.add_argument("--expected-release")
    check_parser.add_argument("--max-age-seconds", type=float, default=DEFAULT_STALE_AFTER_SECONDS)
    check_parser.add_argument("--json", action="store_true")
    check_parser.set_defaults(handler=check_health)
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.handler(args))
    except (OSError, ValueError, ImportError) as exc:
        print(f"P7.02 runtime FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
