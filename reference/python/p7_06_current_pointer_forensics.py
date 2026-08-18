#!/usr/bin/env python3
"""P7.06 selected-Mac current-pointer forensics.

Performs one ordinary canonical P7.06 update from the repository checkout and
then observes the persistent runtime's ``current`` pointer for a short bounded
window. It never invokes rollback/recovery or UI3 lifecycle operations and emits
only minimized non-secret owner-local operational evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CLASSIFICATIONS = {
    "STABLE_AFTER_UPDATE",
    "UPDATE_COMMAND_FAILED",
    "EXPLICIT_P7_06_ROLLBACK_EVIDENCE",
    "EXPLICIT_P7_06_RECOVERY_EVIDENCE",
    "UNATTRIBUTED_CURRENT_MUTATION",
}
LABELS = (
    "com.arvectum.os.persistent-internal",
    "com.arvectum.os.p7-05-observer",
    "com.arvectum.os.p7-06-ui3-operator",
)


class ForensicsError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class EvidenceEntry:
    relative_path: str
    size: int
    mtime_ns: int
    sha256: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_sha(value: str, label: str = "release") -> str:
    value = value.strip().lower()
    if not SHA_RE.fullmatch(value):
        raise ForensicsError(f"{label} must be a full Git SHA")
    return value


def _current_observation(root: Path) -> str:
    current = root / "current"
    if not current.exists() and not current.is_symlink():
        return "ABSENT"
    if not current.is_symlink():
        return "NON_SYMLINK"
    value = Path(os.readlink(current)).name.strip().lower()
    return value if SHA_RE.fullmatch(value) else "INVALID_TARGET"


def _current_release(root: Path) -> str:
    value = _current_observation(root)
    if not SHA_RE.fullmatch(value):
        raise ForensicsError(f"current release pointer is invalid: {value}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _digest_paths(root: Path, paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for base in paths:
        if not base.exists():
            digest.update(f"ABSENT:{base.relative_to(root).as_posix()}\n".encode())
            continue
        if base.is_symlink():
            raise ForensicsError("symlink is not allowed in protected digest input")
        members = [base] if base.is_file() else sorted(path for path in base.rglob("*") if path.is_file())
        for path in members:
            if path.is_symlink():
                raise ForensicsError("symlink is not allowed in protected digest input")
            digest.update(path.relative_to(root).as_posix().encode() + b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
    return digest.hexdigest()


def _p703_digest(root: Path) -> str:
    return _digest_paths(root, (root / "state" / "governed", root / "state" / "checkpoints"))


def _p704_digest(root: Path) -> str:
    return _digest_paths(root, (root / "config" / "p7-04-access.json", root / "secrets" / "p7-04"))


def _inventory_p706_evidence(root: Path) -> dict[str, EvidenceEntry]:
    base = root / "evidence" / "p7-06"
    if not base.exists():
        return {}
    if base.is_symlink() or not base.is_dir():
        raise ForensicsError("P7.06 evidence root is unsafe")
    result: dict[str, EvidenceEntry] = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink():
            raise ForensicsError("symlink is not allowed inside P7.06 evidence root")
        if not path.is_file():
            continue
        rel = path.relative_to(base).as_posix()
        stat = path.stat()
        result[rel] = EvidenceEntry(rel, stat.st_size, stat.st_mtime_ns, _sha256_file(path))
    return result


def _new_evidence(before: dict[str, EvidenceEntry], after: dict[str, EvidenceEntry]) -> list[EvidenceEntry]:
    return [
        entry
        for rel, entry in sorted(after.items())
        if rel not in before or before[rel].sha256 != entry.sha256 or before[rel].mtime_ns != entry.mtime_ns
    ]


def _load_json_bounded(path: Path, *, max_bytes: int = 256 * 1024) -> dict[str, Any] | None:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > max_bytes:
            return None
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def _classify_evidence(root: Path, changed: Iterable[EvidenceEntry]) -> tuple[str | None, list[dict[str, Any]]]:
    base = root / "evidence" / "p7-06"
    facts: list[dict[str, Any]] = []
    saw_rollback = False
    saw_recovery = False
    for entry in changed:
        name = Path(entry.relative_path).name
        kind = None
        if name.startswith("rollback-payload-") and name.endswith(".json"):
            kind = "rollback"
            saw_rollback = True
        elif name.startswith("failure-rollback-") and name.endswith(".json"):
            kind = "failure-rollback"
            saw_rollback = True
        elif name.startswith("interrupted-recovery-") and name.endswith(".json"):
            kind = "interrupted-recovery"
            saw_recovery = True
        if kind is None:
            continue
        payload = _load_json_bounded(base / entry.relative_path)
        fact: dict[str, Any] = {"kind": kind, "file": entry.relative_path, "sha256": entry.sha256}
        if payload is not None:
            for key in (
                "result",
                "source_release",
                "target_release",
                "source_release_restored",
                "observed_current_before_recovery",
                "rollback_disposition",
            ):
                value = payload.get(key)
                if isinstance(value, (str, bool, int, float)) or value is None:
                    fact[key] = value
        facts.append(fact)
    if saw_recovery:
        return "EXPLICIT_P7_06_RECOVERY_EVIDENCE", facts
    if saw_rollback:
        return "EXPLICIT_P7_06_ROLLBACK_EVIDENCE", facts
    return None, facts


def _load_last_success(root: Path) -> dict[str, Any] | None:
    value = _load_json_bounded(root / "run" / "p7-06-last-success.json", max_bytes=64 * 1024)
    if value is None:
        return None
    selected: dict[str, Any] = {}
    for key in ("transaction_id", "source_release", "target_release", "plan_id"):
        item = value.get(key)
        if isinstance(item, str):
            selected[key] = item
    return selected


def _run_bounded(args: list[str], *, cwd: Path | None = None, timeout: float = 180.0) -> tuple[int, str, str]:
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
        raise ForensicsError(f"bounded command failed: {Path(args[0]).name}") from exc
    return completed.returncode, completed.stdout[-32768:], completed.stderr[-32768:]


def _sanitize_tail(value: str, root: Path, repo_root: Path) -> str:
    replacements = (
        (str(root), "<RUNTIME_ROOT>"),
        (str(repo_root), "<REPO_ROOT>"),
        (str(Path.home()), "<HOME>"),
    )
    text = value
    for raw, token in replacements:
        if raw:
            text = text.replace(raw, token)
    lines = text.splitlines()[-80:]
    return "\n".join(lines)[-16384:]


def _canonical_main(repo_root: Path) -> str:
    if not (repo_root / ".git").exists():
        raise ForensicsError("canonical repository checkout is unavailable")
    rc, branch, _ = _run_bounded(["git", "branch", "--show-current"], cwd=repo_root, timeout=15)
    if rc != 0 or branch.strip() != "main":
        raise ForensicsError("canonical checkout must be on main")
    rc, status, _ = _run_bounded(["git", "status", "--porcelain"], cwd=repo_root, timeout=15)
    if rc != 0 or status.strip():
        raise ForensicsError("canonical checkout must be clean")
    rc, origin, _ = _run_bounded(["git", "remote", "get-url", "origin"], cwd=repo_root, timeout=15)
    if rc != 0 or "github.com/arvectum/arvectum-os" not in origin.strip():
        raise ForensicsError("origin is not canonical arvectum/arvectum-os")
    rc, _, _ = _run_bounded(["git", "fetch", "--quiet", "origin", "main"], cwd=repo_root, timeout=60)
    if rc != 0:
        raise ForensicsError("canonical origin/main fetch failed")
    rc, sha, _ = _run_bounded(["git", "rev-parse", "origin/main"], cwd=repo_root, timeout=15)
    if rc != 0:
        raise ForensicsError("origin/main cannot be resolved")
    return _validate_sha(sha, "origin/main")


def _launchctl_fact(label: str) -> dict[str, Any]:
    target = f"gui/{os.getuid()}/{label}"
    rc, out, _ = _run_bounded(["launchctl", "print", target], timeout=15)
    if rc != 0:
        return {"label": label, "loaded": False}
    pid = None
    program = None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("pid = "):
            value = line.split("=", 1)[1].strip()
            if value.isdigit():
                pid = int(value)
        elif line.startswith("program = "):
            program = line.split("=", 1)[1].strip()
    return {"label": label, "loaded": True, "pid": pid, "program_basename": Path(program).name if program else None}


def _process_facts() -> list[dict[str, Any]]:
    rc, out, _ = _run_bounded(["ps", "-axo", "pid=,ppid=,command="], timeout=15)
    if rc != 0:
        return []
    facts: list[dict[str, Any]] = []
    tokens = ("p7_06", "p7-06", "arvectum.os", "ArvectumOS")
    for raw in out.splitlines():
        if not any(token in raw for token in tokens):
            continue
        fields = raw.strip().split(None, 2)
        if len(fields) < 3 or not fields[0].isdigit() or not fields[1].isdigit():
            continue
        command = fields[2]
        basenames = [Path(part).name for part in command.split()[:4]]
        actions = [token for token in ("update", "rollback-last", "recover-interrupted-latest", "serve") if token in command]
        facts.append({"pid": int(fields[0]), "ppid": int(fields[1]), "leading_basenames": basenames, "known_actions": actions})
        if len(facts) >= 32:
            break
    return facts


def _write_attestation(root: Path, value: dict[str, Any]) -> tuple[Path, str]:
    evidence_dir = root / "evidence" / "p7-06-forensics"
    evidence_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    if os.name != "nt":
        os.chmod(evidence_dir, 0o700)
    path = evidence_dir / f"p7-06-current-pointer-forensics-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}.json"
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    digest = _sha256_file(path)
    sidecar = path.with_suffix(path.suffix + ".sha256")
    fd = os.open(sidecar, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(f"{digest}  {path.name}\n")
        handle.flush()
        os.fsync(handle.fileno())
    return path, digest


def run_forensics(root: Path, repo_root: Path, decision_ref: str, watch_seconds: float) -> dict[str, Any]:
    if sys.platform != "darwin":
        raise ForensicsError("macOS is required")
    root = root.expanduser().resolve()
    repo_root = repo_root.expanduser().resolve()
    if not root.is_dir():
        raise ForensicsError("runtime root is unavailable")
    if not (1.0 <= watch_seconds <= 60.0):
        raise ForensicsError("watch window must be between 1 and 60 seconds")
    decision_ref = decision_ref.strip()
    if not decision_ref or len(decision_ref) > 256 or any(ch in decision_ref for ch in "\r\n\0"):
        raise ForensicsError("decision reference is invalid")

    origin_main = _canonical_main(repo_root)
    before_release = _current_release(root)
    if before_release == origin_main:
        raise ForensicsError("canonical target is already active; no transition is available to diagnose")

    before_evidence = _inventory_p706_evidence(root)
    p703_before = _p703_digest(root)
    p704_before = _p704_digest(root)
    before_pointer = _load_last_success(root)
    before_processes = _process_facts()
    before_launchd = [_launchctl_fact(label) for label in LABELS]

    deploy = repo_root / "reference" / "python" / "p7_06_macos_deploy.sh"
    if deploy.is_symlink() or not deploy.is_file():
        raise ForensicsError("canonical P7.06 deploy adapter is missing")

    rc, stdout, stderr = _run_bounded(["sh", str(deploy), "update", decision_ref], cwd=repo_root, timeout=240)

    after_command_release = _current_observation(root)
    after_command_evidence = _inventory_p706_evidence(root)
    changed_during_update = _new_evidence(before_evidence, after_command_evidence)
    during_update_classification, during_update_facts = _classify_evidence(root, changed_during_update)
    after_command_pointer = _load_last_success(root)

    transitions: list[dict[str, Any]] = []
    observed = after_command_release
    deadline = time.monotonic() + watch_seconds
    while time.monotonic() < deadline:
        current = _current_observation(root)
        if current != observed:
            transitions.append({
                "from": observed,
                "to": current,
                "observed_at": _utc_now(),
                "p7_06_deploy_lock_present": (root / "run" / "p7-06-deploy.lock").is_dir(),
                "relevant_processes": _process_facts(),
            })
            observed = current
        time.sleep(0.25)

    final_release = _current_observation(root)
    final_evidence = _inventory_p706_evidence(root)
    final_pointer = _load_last_success(root)
    p703_final = _p703_digest(root)
    p704_final = _p704_digest(root)
    changed_after_command = _new_evidence(after_command_evidence, final_evidence)
    evidence_classification, rollback_facts = _classify_evidence(root, changed_after_command)

    if rc != 0:
        classification = "UPDATE_COMMAND_FAILED"
    elif final_release == after_command_release == origin_main and not transitions:
        classification = "STABLE_AFTER_UPDATE"
    elif evidence_classification is not None:
        classification = evidence_classification
    else:
        classification = "UNATTRIBUTED_CURRENT_MUTATION"

    result = {
        "schema": "arvectum.p7_06.current-pointer-forensics/1",
        "status": "PASS" if classification == "STABLE_AFTER_UPDATE" else "OBSERVED",
        "classification": classification,
        "evidence_classification": "non-canonical owner-local operational diagnostic",
        "origin_main": origin_main,
        "before_release": before_release,
        "update_exit_code": rc,
        "update_stdout_tail": _sanitize_tail(stdout, root, repo_root),
        "update_stderr_tail": _sanitize_tail(stderr, root, repo_root),
        "after_update_command_release": after_command_release,
        "watch_seconds": watch_seconds,
        "transitions": transitions,
        "final_release": final_release,
        "last_success_before": before_pointer,
        "last_success_after_update_command": after_command_pointer,
        "last_success_final": final_pointer,
        "new_p706_evidence_during_update": [{"file": e.relative_path, "sha256": e.sha256, "size": e.size} for e in changed_during_update],
        "during_update_rollback_or_recovery_classification": during_update_classification,
        "during_update_rollback_or_recovery_facts": during_update_facts,
        "new_p706_evidence_after_update_command": [{"file": e.relative_path, "sha256": e.sha256, "size": e.size} for e in changed_after_command],
        "rollback_or_recovery_facts": rollback_facts,
        "launchd_before": before_launchd,
        "launchd_final": [_launchctl_fact(label) for label in LABELS],
        "relevant_processes_before": before_processes,
        "relevant_processes_final": _process_facts(),
        "p703_digest_before": p703_before,
        "p703_digest_final": p703_final,
        "p703_unchanged": p703_before == p703_final,
        "p704_digest_before": p704_before,
        "p704_digest_final": p704_final,
        "p704_unchanged": p704_before == p704_final,
        "p703_or_p704_mutation_performed_by_forensics": False,
        "rollback_invoked_by_forensics": False,
        "recovery_invoked_by_forensics": False,
        "ui3_lifecycle_invoked_by_forensics": False,
        "organizational_authority_provided": False,
        "consequential_approval_provided": False,
        "product_external_effect_invoked": False,
        "reusable_secret_emitted": False,
        "created_at": _utc_now(),
    }
    path, digest = _write_attestation(root, result)
    result["attestation_basename"] = path.name
    result["attestation_sha256"] = digest
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P7.06 selected-Mac current-pointer forensics")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--decision-ref", required=True)
    parser.add_argument("--watch-seconds", type=float, default=15.0)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run_forensics(Path(args.runtime_root), Path(args.repo_root), args.decision_ref, args.watch_seconds)
    except (ForensicsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.06 current-pointer forensics FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(f"P7.06 current-pointer forensics {result['classification']} final={result['final_release']} attestation={result['attestation_basename']}")
    return 0 if result["classification"] == "STABLE_AFTER_UPDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
