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
    path = evidence_dir / f"p7-06-current-pointer-forensics-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%Z%hœ¥ôµíÕÕ¥¹ÕÕ¥Ð ¤¹¡•álèáuô¹©Í½¸ˆ(€€€É…Ü€ô€¡©Í½¸¹‘ÕµÁÌ¡Ù…±Õ”°•¹ÍÕÉ•}…Í¥¤õ…±Í”°Í½ÉÑ}­•åÌõQÉÕ”°¥¹‘•¹ÐôÈ¤€¬€‰q¸ˆ¤¹•¹½‘” ‰ÕÑ˜´àˆ¤(€€€™€ô½Ì¹½Á•¸¡Á…Ñ °½Ì¹=}]I=91dð½Ì¹=}IPð½Ì¹=}a0°€Á¼ØÀÀ¤(€€€Ý¥Ñ ½Ì¹™‘½Á•¸¡™°€‰Ýˆˆ¤…Ì¡…¹‘±”è(€€€€€€€¡…¹‘±”¹ÝÉ¥Ñ”¡É…Ü¤(€€€€€€€¡…¹‘±”¹™±ÕÍ  ¤(€€€€€€€½Ì¹™Íå¹Œ¡¡…¹‘±”¹™¥±•¹¼ ¤¤(€€€‘¥•ÍÐ€ô}Í¡„ÈÔÙ}™¥±”¡Á…Ñ ¤(€€€Í¥‘•…È€ôÁ…Ñ ¹Ý¥Ñ¡}ÍÕ™™¥à¡Á…Ñ ¹ÍÕ™™¥à€¬€ˆ¹Í¡„ÈÔØˆ¤(€€€™€ô½Ì¹½Á•¸¡Í¥‘•…È°½Ì¹=}]I=91dð½Ì¹=}IPð½Ì¹=}a0°€Á¼ØÀÀ¤(€€€Ý¥Ñ ½Ì¹™‘½Á•¸¡™°€‰Üˆ°•¹½‘¥¹œô‰ÕÑ˜´àˆ¤…Ì¡…¹‘±”è(€€€€€€€¡…¹‘±”¹ÝÉ¥Ñ”¡˜‰í‘¥•ÍÑô€íÁ…Ñ ¹¹…µ•õq¸ˆ¤(€€€€€€€¡…¹‘±”¹™±ÕÍ  ¤(€€€€€€€½Ì¹™Íå¹Œ¡¡…¹‘±”¹™¥±•¹¼ ¤¤(€€€É•ÑÕÉ¸Á…Ñ °‘¥•ÍÐ(()‘•˜ÉÕ¹}™½É•¹Í¥Ì¡É½½ÐèA…Ñ °É•Á½}É½½ÐèA…Ñ °‘•¥Í¥½¹}É•˜èÍÑÈ°Ý…Ñ¡}Í•½¹‘Ìè™±½…Ð¤€´ø‘¥ÑmÍÑÈ°¹åtè(€€€¥˜ÍåÌ¹Á±…Ñ™½É´€„ô€‰‘…ÉÝ¥¸ˆè(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰µ…=L¥ÌÉ•ÅÕ¥É•ˆ¤(€€€É½½Ð€ôÉ½½Ð¹•áÁ…¹‘ÕÍ•È ¤¹É•Í½±Ù” ¤(€€€É•Á½}É½½Ð€ôÉ•Á½}É½½Ð¹•áÁ…¹‘ÕÍ•È ¤¹É•Í½±Ù” ¤(€€€¥˜¹½ÐÉ½½Ð¹¥Í}‘¥È ¤è(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰ÉÕ¹Ñ¥µ”É½½Ð¥ÌÕ¹…Ù…¥±…‰±”ˆ¤(€€€¥˜¹½Ð€ Ä¸À€ðôÝ…Ñ¡}Í•½¹‘Ì€ðô€ØÀ¸À¤è(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰Ý…Ñ Ý¥¹‘½ÜµÕÍÐ‰”‰•ÑÝ••¸€Ä…¹€ØÀÍ•½¹‘Ìˆ¤(€€€‘•¥Í¥½¹}É•˜€ô‘•¥Í¥½¹}É•˜¹ÍÑÉ¥À ¤(€€€¥˜¹½Ð‘•¥Í¥½¹}É•˜½È±•¸¡‘•¥Í¥½¹}É•˜¤€ø€ÈÔØ½È…¹ä¡ ¥¸‘•¥Í¥½¹}É•˜™½È ¥¸€‰qÉq¹pÀˆ¤è(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰‘•¥Í¥½¸É•™•É•¹”¥Ì¥¹Ù…±¥ˆ¤((€€€½É¥¥¹}µ…¥¸€ô}…¹½¹¥…±}µ…¥¸¡É•Á½}É½½Ð¤(€€€‰•™½É•}É•±•…Í”€ô}ÕÉÉ•¹Ñ}É•±•…Í”¡É½½Ð¤(€€€¥˜‰•™½É•}É•±•…Í”€ôô½É¥¥¹}µ…¥¸è(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰…¹½¹¥…°Ñ…É•Ð¥Ì…±É•…‘ä…Ñ¥Ù”ì¹¼ÑÉ…¹Í¥Ñ¥½¸¥Ì…Ù…¥±…‰±”Ñ¼‘¥…¹½Í”ˆ¤((€€€‰•™½É•}•Ù¥‘•¹”€ô}¥¹Ù•¹Ñ½Éå}ÀÜÀÙ}•Ù¥‘•¹”¡É½½Ð¤(€€€ÀÜÀÍ}‰•™½É”€ô}ÀÜÀÍ}‘¥•ÍÐ¡É½½Ð¤(€€€ÀÜÀÑ}‰•™½É”€ô}ÀÜÀÑ}‘¥•ÍÐ¡É½½Ð¤(€€€‰•™½É•}Á½¥¹Ñ•È€ô}±½…‘}±…ÍÑ}ÍÕ•ÍÌ¡É½½Ð¤(€€€‰•™½É•}ÁÉ½•ÍÍ•Ì€ô}ÁÉ½•ÍÍ}™…ÑÌ ¤(€€€‰•™½É•}±…Õ¹¡€ôm}±…Õ¹¡Ñ±}™…Ð¡±…‰•°¤™½È±…‰•°¥¸1	1Mt((€€€‘•Á±½ä€ôÉ•Á½}É½½Ð€¼€‰É•™•É•¹”ˆ€¼€‰ÁåÑ¡½¸ˆ€¼€‰ÀÝ|ÀÙ}µ…½Í}‘•Á±½ä¹Í ˆ(€€€¥˜‘•Á±½ä¹¥Í}Íåµ±¥¹¬ ¤½È¹½Ð‘•Á±½ä¹¥Í}™¥±” ¤è(€€€€€€€É…¥Í”½É•¹Í¥ÍÉÉ½È ‰…¹½¹¥…°@Ü¸ÀØ‘•Á±½ä…‘…ÁÑ•È¥Ìµ¥ÍÍ¥¹œˆ¤((€€€ÉŒ°ÍÑ‘½ÕÐ°ÍÑ‘•ÉÈ€ô}ÉÕ¹}‰½Õ¹‘•¡l‰Í ˆ°ÍÑÈ¡‘•Á±½ä¤°€‰ÕÁ‘…Ñ”ˆ°‘•¥Í¥½¹}É•™t°ÝõÉ•Á½}É½½Ð°Ñ¥µ•½ÕÐôÈÐÀ¤((€€€…™Ñ•É}½µµ…¹‘}É•±•…Í”€ô}ÕÉÉ•¹Ñ}½‰Í•ÉÙ…Ñ¥½¸¡É½½Ð¤(€€€…™Ñ•É}½µµ…¹‘}•Ù¥‘•¹”€ô}¥¹Ù•¹Ñ½Éå}ÀÜÀÙ}•Ù¥‘•¹”¡É½½Ð¤(€€€¡…¹•‘}‘ÕÉ¥¹}ÕÁ‘…Ñ”€ô}¹•Ý}•Ù¥‘•¹”¡‰•™½É•}•Ù¥‘•¹”°…™Ñ•É}½µµ…¹‘}•Ù¥‘•¹”¤(€€€‘ÕÉ¥¹}ÕÁ‘…Ñ•}±…ÍÍ¥™¥…Ñ¥½¸°‘ÕÉ¥¹}ÕÁ‘…Ñ•}™…ÑÌ€ô}±…ÍÍ¥™å}•Ù¥‘•¹”¡É½½Ð°¡…¹•‘}‘ÕÉ¥¹}ÕÁ‘…Ñ”¤(€€€…™Ñ•É}½µµ…¹‘}Á½¥¹Ñ•È€ô}±½…‘}±…ÍÑ}ÍÕ•ÍÌ¡É½½Ð¤((€€€ÑÉ…¹Í¥Ñ¥½¹Ìè±¥ÍÑm‘¥ÑmÍÑÈ°¹åut€ômt(€€€½‰Í•ÉÙ•€ô…™Ñ•É}½µµ…¹‘}É•±•…Í”(€€€‘•…‘±¥¹”€ôÑ¥µ”¹µ½¹½Ñ½¹¥Œ ¤€¬Ý…Ñ¡}Í•½¹‘Ì(€€€Ý¡¥±”Ñ¥µ”¹µ½¹½Ñ½¹¥Œ ¤€ð‘•…‘±¥¹”è(€€€€€€€ÕÉÉ•¹Ð€ô}ÕÉÉ•¹Ñ}½‰Í•ÉÙ…Ñ¥½¸¡É½½Ð¤(€€€€€€€¥˜ÕÉÉ•¹Ð€„ô½‰Í•ÉÙ•è(€€€€€€€€€€€ÑÉ…¹Í¥Ñ¥½¹Ì¹…ÁÁ•¹¡ì(€€€€€€€€€€€€€€€€‰™É½´ˆè½‰Í•ÉÙ•°(€€€€€€€€€€€€€€€€‰Ñ¼ˆèÕÉÉ•¹Ð°(€€€€€€€€€€€€€€€€‰½‰Í•ÉÙ•‘}…Ðˆè}ÕÑ}¹½Ü ¤°(€€€€€€€€€€€€€€€€‰ÀÝ|ÀÙ}‘•Á±½å}±½­}ÁÉ•Í•¹Ðˆè€¡É½½Ð€¼€‰ÉÕ¸ˆ€¼€‰ÀÜ´ÀØµ‘•Á±½ä¹±½¬ˆ¤¹¥Í}‘¥È ¤°(€€€€€€€€€€€€€€€€‰É•±•Ù…¹Ñ}ÁÉ½•ÍÍ•Ìˆè}ÁÉ½•ÍÍ}™…ÑÌ ¤°(€€€€€€€€€€€ô¤(€€€€€€€€€€€½‰Í•ÉÙ•€ôÕÉÉ•¹Ð(€€€€€€€Ñ¥µ”¹Í±••À À¸ÈÔ¤((€€€™¥¹…±}É•±•…Í”€ô}ÕÉÉ•¹Ñ}½‰Í•ÉÙ…Ñ¥½¸¡É½½Ð¤(€€€™¥¹…±}•Ù¥‘•¹”€ô}¥¹Ù•¹Ñ½Éå}ÀÜÀÙ}•Ù¥‘•¹”¡É½½Ð¤(€€€™¥¹…±}Á½¥¹Ñ•È€ô}±½…‘}±…ÍÑ}ÍÕ•ÍÌ¡É½½Ð¤(€€€ÀÜÀÍ}™¥¹…°€ô}ÀÜÀÍ}‘¥•ÍÐ¡É½½Ð¤(€€€ÀÜÀÑ}™¥¹…°€ô}ÀÜÀÑ}‘¥•ÍÐ¡É½½Ð¤(€€€¡…¹•‘}…™Ñ•É}½µµ…¹€ô}¹•Ý}•Ù¥‘•¹”¡…™Ñ•É}½µµ…¹‘}•Ù¥‘•¹”°™¥¹…±}•Ù¥‘•¹”¤(€€€•Ù¥‘•¹•}±…ÍÍ¥™¥…Ñ¥½¸°É½±±‰…­}™…ÑÌ€ô}±…ÍÍ¥™å}•Ù¥‘•¹”¡É½½Ð°¡…¹•‘}…™Ñ•É}½µµ…¹¤((€€€¥˜ÉŒ€„ô€Àè(€€€€€€€±…ÍÍ¥™¥…Ñ¥½¸€ô€‰UAQ}=559}%1ˆ(€€€•±¥˜•Ù¥‘•¹•}±…ÍÍ¥™¥…Ñ¥½¸¥Ì¹½Ð9½¹”è(€€€€€€€±…ÍÍ¥™¥…Ñ¥½¸€ô•Ù¥‘•¹•}±…ÍÍ¥™¥…Ñ¥½¸(€€€•±¥˜‘ÕÉ¥¹}ÕÁ‘…Ñ•}±…ÍÍ¥™¥…Ñ¥½¸¥Ì¹½Ð9½¹”è(€€€€€€€±…ÍÍ¥™¥…Ñ¥½¸€ô‘ÕÉ¥¹}ÕÁ‘…Ñ•}±…ÍÍ¥™¥…Ñ¥½¸(€€€•±¥˜™¥¹…±}É•±•…Í”€ôô…™Ñ•É}½µµ…¹‘}É•±•…Í”€ôô½É¥¥¹}µ…¥¸…¹¹½ÐÑÉ…¹Í¥Ñ¥½¹Ìè(€€€€€€€±…ÍÍ¥™¥…Ñ¥½¸€ô€‰MQ	1}QI}UAQˆ(€€€•±Í”è(€€€€€€€±…ÍÍ¥™¥…Ñ¥½¸€ô€‰U9QQI%	UQ}UII9Q}5UQQ%=8ˆ((€€€É•ÍÕ±Ð€ôì(€€€€€€€€‰Í¡•µ„ˆè€‰…ÉÙ•ÑÕ´¹ÀÝ|ÀØ¹ÕÉÉ•¹ÐµÁ½¥¹Ñ•Èµ™½É•¹Í¥Ì¼Äˆ°(€€€€€€€€‰ÍÑ…ÑÕÌˆè€‰AMLˆ¥˜±…ÍÍ¥™¥…Ñ¥½¸€ôô€‰MQ	1}QI}UAQˆ•±Í”€‰=	MIYˆ°(€€€€€€€€‰±…ÍÍ¥™¥…Ñ¥½¸ˆè±…ÍÍ¥™¥…Ñ¥½¸°(€€€€€€€€‰•Ù¥‘•¹•}±…ÍÍ¥™¥…Ñ¥½¸ˆè€‰¹½¸µ…¹½¹¥…°½Ý¹•Èµ±½…°½Á•É…Ñ¥½¹…°‘¥…¹½ÍÑ¥Œˆ°(€€€€€€€€‰½É¥¥¹}µ…¥¸ˆè½É¥¥¹}µ…¥¸°(€€€€€€€€‰‰•™½É•}É•±•…Í”ˆè‰•™½É•}É•±•…Í”°(€€€€€€€€‰ÕÁ‘…Ñ•}•á¥Ñ}½‘”ˆèÉŒ°(€€€€€€€€‰ÕÁ‘…Ñ•}ÍÑ‘½ÕÑ}Ñ…¥°ˆè}Í…¹¥Ñ¥é•}Ñ…¥°¡ÍÑ‘½ÕÐ°É½½Ð°É•Á½}É½½Ð¤°(€€€€€€€€‰ÕÁ‘…Ñ•}ÍÑ‘•ÉÉ}Ñ…¥°ˆè}Í…¹¥Ñ¥é•}Ñ…¥°¡ÍÑ‘•ÉÈ°É½½Ð°É•Á½}É½½Ð¤°(€€€€€€€€‰…™Ñ•É}ÕÁ‘…Ñ•}½µµ…¹‘}É•±•…Í”ˆè…™Ñ•É}½µµ…¹‘}É•±•…Í”°(€€€€€€€€‰Ý…Ñ¡}Í•½¹‘ÌˆèÝ…Ñ¡}Í•½¹‘Ì°(€€€€€€€€‰ÑÉ…¹Í¥Ñ¥½¹ÌˆèÑÉ…¹Í¥Ñ¥½¹Ì°(€€€€€€€€‰™¥¹…±}É•±•…Í”ˆè™¥¹…±}É•±•…Í”°(€€€€€€€€‰±…ÍÑ}ÍÕ•ÍÍ}‰•™½É”ˆè‰•™½É•}Á½¥¹Ñ•È°(€€€€€€€€‰±…ÍÑ}ÍÕ•ÍÍ}…™Ñ•É}ÕÁ‘…Ñ•}½µµ…¹ˆè…™Ñ•É}½µµ…¹‘}Á½¥¹Ñ•È°(€€€€€€€€‰±…ÍÑ}ÍÕ•ÍÍ}™¥¹…°ˆè™¥¹…±}Á½¥¹Ñ•È°(€€€€€€€€‰¹•Ý}ÀÜÀÙ}•Ù¥‘•¹•}‘ÕÉ¥¹}ÕÁ‘…Ñ”ˆèmì‰™¥±”ˆè”¹É•±…Ñ¥Ù•}Á…Ñ °€‰Í¡„ÈÔØˆè”¹Í¡„ÈÔØ°€‰Í¥é”ˆè”¹Í¥é•ô™½È”¥¸¡…¹•‘}‘ÕÉ¥¹}ÕÁ‘…Ñ•t°(€€€€€€€€‰‘ÕÉ¥¹}ÕÁ‘…Ñ•}É½±±‰…­}½É}É•½Ù•Éå}±…ÍÍ¥™¥…Ñ¥½¸ˆè‘ÕÉ¥¹}ÕÁ‘…Ñ•}±…ÍÍ¥™¥…Ñ¥½¸°(€€€€€€€€‰‘ÕÉ¥¹}ÕÁ‘…Ñ•}É½±±‰…­}½É}É•½Ù•Éå}™…ÑÌˆè‘ÕÉ¥¹}ÕÁ‘…Ñ•}™…ÑÌ°(€€€€€€€€‰¹•Ý}ÀÜÀÙ}•Ù¥‘•¹•}…™Ñ•É}ÕÁ‘…Ñ•}½µµ…¹ˆèmì‰™¥±”ˆè”¹É•±…Ñ¥Ù•}Á…Ñ °€‰Í¡„ÈÔØˆè”¹Í¡„ÈÔØ°€‰Í¥é”ˆè”¹Í¥é•ô™½È”¥¸¡…¹•‘}…™Ñ•É}½µµ…¹‘t°(€€€€€€€€‰É½±±‰…­}½É}É•½Ù•Éå}™…ÑÌˆèÉ½±±‰…­}™…ÑÌ°(€€€€€€€€‰±…Õ¹¡‘}‰•™½É”ˆè‰•™½É•}±…Õ¹¡°(€€€€€€€€‰±…Õ¹¡‘}™¥¹…°ˆèm}±…Õ¹¡Ñ±}™…Ð¡±…‰•°¤™½È±…‰•°¥¸1	1Mt°(€€€€€€€€‰É•±•Ù…¹Ñ}ÁÉ½•ÍÍ•Í}‰•™½É”ˆè‰•™½É•}ÁÉ½•ÍÍ•Ì°(€€€€€€€€‰É•±•Ù…¹Ñ}ÁÉ½•ÍÍ•Í}™¥¹…°ˆè}ÁÉ½•ÍÍ}™…ÑÌ ¤°(€€€€€€€€‰ÀÜÀÍ}‘¥•ÍÑ}‰•™½É”ˆèÀÜÀÍ}‰•™½É”°(€€€€€€€€‰ÀÜÀÍ}‘¥•ÍÑ}™¥¹…°ˆèÀÜÀÍ}™¥¹…°°(€€€€€€€€‰ÀÜÀÍ}Õ¹¡…¹•ˆèÀÜÀÍ}‰•™½É”€ôôÀÜÀÍ}™¥¹…°°(€€€€€€€€‰ÀÜÀÑ}‘¥•ÍÑ}‰•™½É”ˆèÀÜÀÑ}‰•™½É”°(€€€€€€€€‰ÀÜÀÑ}‘¥•ÍÑ}™¥¹…°ˆèÀÜÀÑ}™¥¹…°°(€€€€€€€€‰ÀÜÀÑ}Õ¹¡…¹•ˆèÀÜÀÑ}‰•™½É”€ôôÀÜÀÑ}™¥¹…°°(€€€€€€€€‰ÀÜÀÍ}½É}ÀÜÀÑ}µÕÑ…Ñ¥½¹}Á•É™½Éµ•‘}‰å}™½É•¹Í¥Ìˆè…±Í”°(€€€€€€€€‰É½±±‰…­}¥¹Ù½­•‘}‰å}™½É•¹Í¥Ìˆè…±Í”°(€€€€€€€€‰É•½Ù•Éå}¥¹Ù½­•‘}‰å}™½É•¹Í¥Ìˆè…±Í”°(€€€€€€€€‰Õ¤Í}±¥™•å±•}¥¹Ù½­•‘}‰å}™½É•¹Í¥Ìˆè…±Í”°(€€€€€€€€‰½É…¹¥é…Ñ¥½¹…±}…ÕÑ¡½É¥Ñå}ÁÉ½Ù¥‘•ˆè…±Í”°(€€€€€€€€‰½¹Í•ÅÕ•¹Ñ¥…±}…ÁÁÉ½Ù…±}ÁÉ½Ù¥‘•ˆè…±Í”°(€€€€€€€€‰ÁÉ½‘ÕÑ}•áÑ•É¹…±}•™™•Ñ}¥¹Ù½­•ˆè…±Í”°(€€€€€€€€‰É•ÕÍ…‰±•}Í•É•Ñ}•µ¥ÑÑ•ˆè…±Í”°(€€€€€€€€‰É•…Ñ•‘}…Ðˆè}ÕÑ}¹½Ü ¤°(€€€ô(€€€Á…Ñ °‘¥•ÍÐ€ô}ÝÉ¥Ñ•}…ÑÑ•ÍÑ…Ñ¥½¸¡É½½Ð°É•ÍÕ±Ð¤(€€€É•ÍÕ±Ñl‰…ÑÑ•ÍÑ…Ñ¥½¹}‰…Í•¹…µ”‰t€ôÁ…Ñ ¹¹…µ”(€€€É•ÍÕ±Ñl‰…ÑÑ•ÍÑ…Ñ¥½¹}Í¡„ÈÔØ‰t€ô‘¥•ÍÐ(€€€É•ÑÕÉ¸É•ÍÕ±Ð(()‘•˜‰Õ¥±‘}Á…ÉÍ•È ¤€´ø…ÉÁ…ÉÍ”¹ÉÕµ•¹ÑA…ÉÍ•Èè(€€€Á…ÉÍ•È€ô…ÉÁ…ÉÍ”¹ÉÕµ•¹ÑA…ÉÍ•È¡‘•ÍÉ¥ÁÑ¥½¸ô‰@Ü¸ÀØÍ•±•Ñ•µ5…ŒÕÉÉ•¹ÐµÁ½¥¹Ñ•È™½É•¹Í¥Ìˆ¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µÉÕ¹Ñ¥µ”µÉ½½Ðˆ°É•ÅÕ¥É•õQÉÕ”¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µÉ•Á¼µÉ½½Ðˆ°É•ÅÕ¥É•õQÉÕ”¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µ‘•¥Í¥½¸µÉ•˜ˆ°É•ÅÕ¥É•õQÉÕ”¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µÝ…Ñ µÍ•½¹‘Ìˆ°ÑåÁ”õ™±½…Ð°‘•™…Õ±ÐôÄÔ¸À¤(€€€Á…ÉÍ•È¹…‘‘}…ÉÕµ•¹Ð ˆ´µ©Í½¸ˆ°…Ñ¥½¸ô‰ÍÑ½É•}ÑÉÕ”ˆ¤(€€€É•ÑÕÉ¸Á…ÉÍ•È(()‘•˜µ…¥¸¡…ÉØè±¥ÍÑmÍÑÉtð9½¹”€ô9½¹”¤€´ø¥¹Ðè(€€€…ÉÌ€ô‰Õ¥±‘}Á…ÉÍ•È ¤¹Á…ÉÍ•}…ÉÌ¡…ÉØ¤(€€€ÑÉäè(€€€€€€€É•ÍÕ±Ð€ôÉÕ¹}™½É•¹Í¥Ì¡A…Ñ ¡…ÉÌ¹ÉÕ¹Ñ¥µ•}É½½Ð¤°A…Ñ ¡…ÉÌ¹É•Á½}É½½Ð¤°…ÉÌ¹‘•¥Í¥½¹}É•˜°…ÉÌ¹Ý…Ñ¡}Í•½¹‘Ì¤(€€€•á•ÁÐ€¡½É•¹Í¥ÍÉÉ½È°=MÉÉ½È°Y…±Õ•ÉÉ½È°©Í½¸¹)M=9•½‘•ÉÉ½È¤…Ì•áŒè(€€€€€€€ÁÉ¥¹Ð¡˜‰@Ü¸ÀØÕÉÉ•¹ÐµÁ½¥¹Ñ•È™½É•¹Í¥Ì%0èí•áôˆ°™¥±”õÍåÌ¹ÍÑ‘•ÉÈ¤(€€€€€€€É•ÑÕÉ¸€Ä(€€€¥˜…ÉÌ¹©Í½¸è(€€€€€€€ÁÉ¥¹Ð¡©Í½¸¹‘ÕµÁÌ¡É•ÍÕ±Ð°•¹ÍÕÉ•}…Í¥¤õ…±Í”°Í½ÉÑ}­•åÌõQÉÕ”¤¤(€€€•±Í”è(€€€€€€€ÁÉ¥¹Ð¡˜‰@Ü¸ÀØÕÉÉ•¹ÐµÁ½¥¹Ñ•È™½É•¹Í¥ÌíÉ•ÍÕ±Ñl±…ÍÍ¥™¥…Ñ¥½¸uô™¥¹…°õíÉ•ÍÕ±Ñl™¥¹…±}É•±•…Í”uô…ÑÑ•ÍÑ…Ñ¥½¸õíÉ•ÍÕ±Ñl…ÑÑ•ÍÑ…Ñ¥½¹}‰…Í•¹…µ”uôˆ¤(€€€É•ÑÕÉ¸€À¥˜É•ÍÕ±Ñl‰±…ÍÍ¥™¥…Ñ¥½¸‰t€ôô€‰MQ	1}QI}UAQˆ•±Í”€È(()¥˜}}¹…µ•}|€ôô€‰}}µ…¥¹}|ˆè(€€€É…¥Í”MåÍÑ•µá¥Ð¡µ…¥¸ ¤¤(