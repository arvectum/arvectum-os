#!/usr/bin/env python3
"""Selected-Mac P7.07 repeatability + restart-survivability proof.

The proof consumes the exact retained operational Document through the real
arvectum/tender-agent ArvectumOSBridge, restarts only the already-established
P7.02 supervised runtime, then consumes the same exact Subject/Version/Artifact
again. It proves read-only state-tree stability and records minimized local
operational evidence. It does not fetch product/platform code, retrieve EIS data
or execute product/external effects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

import p7_06_governed_deploy as p706
import p7_07_persistent_tender_operator_contour as p707

UTC = timezone.utc
EVIDENCE_SCHEMA = "arvectum.p7_07.selected-mac-restart-proof/1"
CANONICAL_PRODUCT_ORIGINS = {
    "https://github.com/arvectum/tender-agent",
    "https://github.com/arvectum/tender-agent.git",
    "git@github.com:arvectum/tender-agent",
    "git@github.com:arvectum/tender-agent.git",
    "ssh://git@github.com/arvectum/tender-agent",
    "ssh://git@github.com/arvectum/tender-agent.git",
}


class P707SelectedMacProofError(RuntimeError):
    pass


def _run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if completed.returncode != 0:
        raise P707SelectedMacProofError(f"product git {' '.join(args)} failed")
    return completed.stdout.strip()


def _verify_product_repo(repo: Path) -> tuple[Path, str]:
    root = repo.expanduser().resolve(strict=True)
    if not root.is_dir():
        raise P707SelectedMacProofError("Tender Agent repository path is not a directory")
    if _run_git(root, "rev-parse", "--is-inside-work-tree") != "true":
        raise P707SelectedMacProofError("Tender Agent path is not a Git worktree")
    origin = _run_git(root, "remote", "get-url", "origin")
    if origin not in CANONICAL_PRODUCT_ORIGINS:
        raise P707SelectedMacProofError("Tender Agent origin is not canonical arvectum/tender-agent")
    branch = _run_git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    if branch != "main":
        raise P707SelectedMacProofError(f"Tender Agent checkout must be main, found {branch!r}")
    if _run_git(root, "status", "--porcelain"):
        raise P707SelectedMacProofError("Tender Agent checkout must be clean")
    head = _run_git(root, "rev-parse", "HEAD")
    if len(head) != 40 or any(ch not in "0123456789abcdef" for ch in head.lower()):
        raise P707SelectedMacProofError("Tender Agent HEAD is not a full commit SHA")
    bridge = root / p707.PRODUCT_BRIDGE_RELATIVE_PATH
    if not bridge.is_file() or bridge.is_symlink():
        raise P707SelectedMacProofError("Tender Agent governed product bridge missing/unsafe")
    return root, head.lower()


def _private_json(path: Path, *, label: str) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        raise P707SelectedMacProofError(f"{label} missing/unsafe")
    if os.name != "nt" and (path.stat().st_mode & 0o077):
        raise P707SelectedMacProofError(f"{label} must be owner-only")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise P707SelectedMacProofError(f"{label} unreadable") from exc
    if not isinstance(value, dict):
        raise P707SelectedMacProofError(f"{label} must be a JSON object")
    return value


def _health(runtime_root: Path, release_sha: str) -> dict[str, Any]:
    value = _private_json(runtime_root / "run" / "health.json", label="P7.02 health")
    if value.get("state") != "healthy" or value.get("release_sha") != release_sha:
        raise P707SelectedMacProofError("P7.02 health is not healthy/exact-release")
    if value.get("product_effects_enabled") is not False or value.get("canonical_state_written") is not False:
        raise P707SelectedMacProofError("P7.02 runtime boundary drifted")
    instance = value.get("instance_id")
    generation = value.get("generation")
    pid = value.get("pid")
    if not isinstance(instance, str) or not instance or not isinstance(generation, int) or generation < 1 or not isinstance(pid, int) or pid <= 0:
        raise P707SelectedMacProofError("P7.02 health identity/generation/pid invalid")
    try:
        os.kill(pid, 0)
    except OSError as exc:
        raise P707SelectedMacProofError("P7.02 health PID is not alive") from exc
    return value


def _state_digest(runtime_root: Path) -> str:
    state = runtime_root / "state"
    if not state.is_dir() or state.is_symlink():
        raise P707SelectedMacProofError("P7.03 state root missing/unsafe")
    digest = hashlib.sha256()
    for path in sorted(item for item in state.rglob("*") if item.is_file()):
        if path.is_symlink():
            raise P707SelectedMacProofError("P7.03 state contains symlink")
        rel = path.relative_to(state).as_posix().encode("utf-8")
        data = path.read_bytes()
        digest.update(len(rel).to_bytes(8, "big")); digest.update(rel)
        digest.update(len(data).to_bytes(8, "big")); digest.update(data)
    return digest.hexdigest()


def _atomic_json(path: Path, value: Mapping[str, Any]) -> str:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt": os.chmod(path.parent, 0o700)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt": os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp, path)
        if os.name != "nt": os.chmod(path, 0o600)
    finally:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
    return hashlib.sha256(payload).hexdigest()


def _same_reliance(left: p707.ConsumptionResult, right: p707.ConsumptionResult) -> bool:
    return (
        left.storage_item_id,
        left.subject_identity,
        left.version_identity,
        left.artifact_identity,
        left.integrity_ref,
        left.authoritative_source,
        left.product_contract_version,
    ) == (
        right.storage_item_id,
        right.subject_identity,
        right.version_identity,
        right.artifact_identity,
        right.integrity_ref,
        right.authoritative_source,
        right.product_contract_version,
    )


def run_proof(
    *,
    runtime_root: Path,
    access_root: Path,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
    product_repo: Path,
    evidence_output: Path | None = None,
) -> dict[str, Any]:
    runtime_root = runtime_root.expanduser().resolve()
    release_sha = p706.current_release(runtime_root)
    p706.verify_release(runtime_root, release_sha)
    product_repo, product_head = _verify_product_repo(product_repo)
    before_health = _health(runtime_root, release_sha)
    state_before = _state_digest(runtime_root)

    first = p707.run_consume(
        runtime_root=runtime_root,
        access_root=access_root,
        state_file=state_file,
        credential_id=credential_id,
        credential_file=credential_file,
        product_repo=product_repo,
    )
    if first.status != "PASS_EXACT_CAP001_RELIANCE":
        raise P707SelectedMacProofError("first Tender Operator reliance did not pass")
    state_after_first = _state_digest(runtime_root)
    if state_after_first != state_before:
        raise P707SelectedMacProofError("read-only first Tender Operator reliance mutated P7.03 state")

    restart_script = runtime_root / "releases" / release_sha / "source" / "reference" / "python" / "p7_02_macos_service.sh"
    if not restart_script.is_file() or restart_script.is_symlink():
        raise P707SelectedMacProofError("exact-release P7.02 restart adapter missing/unsafe")
    env = dict(os.environ)
    env["ARVECTUM_P7_02_ROOT"] = str(runtime_root)
    restarted = subprocess.run(
        ["/bin/sh", str(restart_script), "restart"],
        check=False,
        capture_output=True,
        text=True,
        env=env,
        timeout=45,
    )
    if restarted.returncode != 0:
        raise P707SelectedMacProofError("P7.02 supervised restart failed")
    after_health = _health(runtime_root, release_sha)
    if after_health["instance_id"] == before_health["instance_id"]:
        raise P707SelectedMacProofError("P7.02 restart did not replace runtime instance")
    if after_health["generation"] <= before_health["generation"]:
        raise P707SelectedMacProofError("P7.02 health generation did not advance")
    if after_health.get("previous_instance_id") != before_health["instance_id"]:
        raise P707SelectedMacProofError("P7.02 restart continuity lost previous_instance_id")
    if _state_digest(runtime_root) != state_before:
        raise P707SelectedMacProofError("P7.02 restart mutated P7.03 governed state")

    second = p707.run_consume(
        runtime_root=runtime_root,
        access_root=access_root,
        state_file=state_file,
        credential_id=credential_id,
        credential_file=credential_file,
        product_repo=product_repo,
    )
    if second.status != "PASS_EXACT_CAP001_RELIANCE" or not _same_reliance(first, second):
        raise P707SelectedMacProofError("post-restart Tender Operator reliance is not the same exact governed reliance")
    state_after = _state_digest(runtime_root)
    if state_after != state_before:
        raise P707SelectedMacProofError("P7.07 proof mutated P7.03 governed state")

    if evidence_output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        evidence_output = runtime_root / "evidence" / "p7-07" / f"selected-mac-restart-proof-{stamp}.json"
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "status": "PASS",
        "operating_mode": "Persistent Internal / owner-operated",
        "release_sha": release_sha,
        "product_repository": "arvectum/tender-agent",
        "product_head": product_head,
        "product_contract_version": "0.1.0",
        "storage_item_id": first.storage_item_id,
        "subject_identity": first.subject_identity,
        "version_identity": first.version_identity,
        "artifact_identity": first.artifact_identity,
        "integrity_ref": first.integrity_ref,
        "authoritative_source": first.authoritative_source,
        "runtime_instance_replaced": True,
        "runtime_generation_before": before_health["generation"],
        "runtime_generation_after": after_health["generation"],
        "runtime_previous_instance_continuity": True,
        "same_exact_reliance_before_after_restart": True,
        "p7_03_state_digest_before": state_before,
        "p7_03_state_digest_after": state_after,
        "p7_03_state_unchanged": True,
        "canonical_mutation_by_operational_reads": False,
        "network_retrieval_by_p7_07": False,
        "eis_or_soap_invoked_by_p7_07": False,
        "external_actions": False,
        "raw_document_bytes_exposed": False,
        "credential_secret_exposed": False,
    }
    evidence_sha = _atomic_json(evidence_output, evidence)
    return {**evidence, "evidence_path": str(evidence_output), "evidence_sha256": evidence_sha}


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime-root", type=Path, required=True)
    p.add_argument("--access-root", type=Path, required=True)
    p.add_argument("--state-file", type=Path, required=True)
    p.add_argument("--credential-id", required=True)
    p.add_argument("--credential-file", type=Path, required=True)
    p.add_argument("--product-repo", type=Path, required=True)
    p.add_argument("--evidence-output", type=Path)
    return p


def main() -> int:
    args = _parser().parse_args()
    try:
        result = run_proof(
            runtime_root=args.runtime_root,
            access_root=args.access_root,
            state_file=args.state_file,
            credential_id=args.credential_id,
            credential_file=args.credential_file,
            product_repo=args.product_repo,
            evidence_output=args.evidence_output,
        )
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2
    print("RESULT=PASS")
    print(f"RELEASE_SHA={result['release_sha']}")
    print(f"PRODUCT_HEAD={result['product_head']}")
    print(f"STORAGE_ITEM_ID={result['storage_item_id']}")
    print(f"SUBJECT={result['subject_identity']}")
    print(f"VERSION={result['version_identity']}")
    print(f"GENERATION_BEFORE={result['runtime_generation_before']}")
    print(f"GENERATION_AFTER={result['runtime_generation_after']}")
    print("P7_03_STATE_UNCHANGED=true")
    print("SAME_EXACT_RELIANCE_AFTER_RESTART=true")
    print("EXTERNAL_ACTIONS=false")
    print(f"EVIDENCE_PATH={result['evidence_path']}")
    print(f"EVIDENCE_SHA256={result['evidence_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
