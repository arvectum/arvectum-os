#!/usr/bin/env python3
"""P7.06-UI3 selected-owner Mac operational closure proof.

The proof is deliberately owner-local and non-canonical. It must run from the
exact active release after that release was reached by the existing P7.06
governed deployment path. It never creates P7.04 grants/credentials, never
provides Organizational Authority/consequential approval, and never performs a
real UI2 interaction (UI4 remains responsible for that proof).
"""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import re
import subprocess
import sys
import urllib.parse
import uuid
from http.cookies import SimpleCookie
from pathlib import Path
from typing import Any, Iterable, Optional

import p7_03_durable_state as p703

ATTESTATION_SCHEMA = "arvectum.p7_06_ui3.selected-mac-attestation/1"
LABEL = "com.arvectum.os.p7-06-ui3-operator"
HOST = "127.0.0.1"
UNLOCK = "/ui3/unlock"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CSRF_RE = re.compile(r'name="csrf" value="([^"]+)"')


class UI3ProofError(RuntimeError):
    """Selected-Mac proof could not establish the declared invariant."""


def _validate_sha(value: str) -> str:
    value = value.strip().lower()
    if not SHA_RE.fullmatch(value):
        raise UI3ProofError("release identity must be an exact Git SHA")
    return value


def _current_release(root: Path) -> str:
    current = root / "current"
    if not current.is_symlink():
        raise UI3ProofError("current release symlink is missing")
    return _validate_sha(Path(os.readlink(current)).name)


def _release_dir(root: Path, release: str) -> Path:
    return root / "releases" / release / "source" / "reference" / "python"


def _exact_python(root: Path, release: str) -> Path:
    return root / "venvs" / release / "bin" / "python"


def _run(*args: str) -> None:
    try:
        subprocess.run(
            list(args),
            check=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        command = Path(args[0]).name if args else "command"
        raise UI3ProofError(f"bounded command failed: {command}") from exc


def _service_loaded() -> bool:
    result = subprocess.run(
        ["launchctl", "print", f"gui/{os.getuid()}/{LABEL}"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def _assert_owner_file(path: Path, label: str, max_bytes: int) -> None:
    if path.is_symlink() or not path.is_file():
        raise UI3ProofError(f"{label} is missing or unsafe")
    if path.stat().st_size > max_bytes:
        raise UI3ProofError(f"{label} exceeds bounded size")
    if os.name != "nt" and path.stat().st_mode & 0o077:
        raise UI3ProofError(f"{label} is not owner-only")


def _load_json(path: Path, label: str, max_bytes: int = 65536) -> dict[str, Any]:
    _assert_owner_file(path, label, max_bytes)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise UI3ProofError(f"{label} is unreadable") from exc
    if not isinstance(value, dict):
        raise UI3ProofError(f"{label} must be a JSON object")
    return value


def _transaction_source(root: Path, target: str) -> str:
    pointer = _load_json(root / "run" / "p7-06-last-success.json", "P7.06 last-success pointer")
    source = _validate_sha(str(pointer.get("source_release", "")))
    recorded_target = _validate_sha(str(pointer.get("target_release", "")))
    if recorded_target != target:
        raise UI3ProofError("active release is not the target of the last governed P7.06 update")
    if source == target:
        raise UI3ProofError("rollback source and target must differ")
    return source


def _digest_files(root: Path, paths: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for base in paths:
        if not base.exists():
            digest.update(f"ABSENT:{base.relative_to(root).as_posix()}\n".encode())
            continue
        if base.is_symlink():
            raise UI3ProofError("symlink is not allowed in protected snapshot")
        members = [base] if base.is_file() else sorted(p for p in base.rglob("*") if p.is_file())
        for path in members:
            if path.is_symlink():
                raise UI3ProofError("symlink is not allowed in protected snapshot")
            rel = path.relative_to(root).as_posix()
            digest.update(rel.encode("utf-8") + b"\0")
            with path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
    return digest.hexdigest()


def _canonical_digest(root: Path) -> str:
    return _digest_files(root, (root / "state" / "governed", root / "state" / "checkpoints"))


def _p704_digest(root: Path) -> str:
    return _digest_files(root, (root / "config" / "p7-04-access.json", root / "secrets" / "p7-04"))


def _ui3_private_material_absent(root: Path) -> bool:
    return all(
        not path.exists()
        for path in (
            root / "config" / "p7-06-ui3.json",
            root / "secrets" / "p7-06-ui3" / "access.secret",
            root / "logs" / "p7-06-ui3.stdout.log",
            root / "logs" / "p7-06-ui3.stderr.log",
            root / "service" / f"{LABEL}.plist",
            Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist",
        )
    )


def _request(port: int, method: str, path: str, *, body: Optional[bytes] = None, headers: Optional[dict[str, str]] = None) -> tuple[int, dict[str, str], bytes]:
    request_headers = {"Host": f"{HOST}:{port}", "Connection": "close"}
    if headers:
        request_headers.update(headers)
    connection = http.client.HTTPConnection(HOST, port, timeout=5)
    try:
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        payload = response.read(256 * 1024 + 1)
        if len(payload) > 256 * 1024:
            raise UI3ProofError("HTTP response exceeded bounded proof size")
        response_headers = {key.lower(): value for key, value in response.getheaders()}
        return response.status, response_headers, payload
    finally:
        connection.close()


def _http_restart_proof(root: Path, ui3_shell: Path) -> dict[str, bool]:
    config = _load_json(root / "config" / "p7-06-ui3.json", "UI3 configuration", 16384)
    if config.get("listener_host") != HOST:
        raise UI3ProofError("UI3 listener is not exact IPv4 loopback")
    port = config.get("listener_port")
    if isinstance(port, bool) or not isinstance(port, int) or not 1024 <= port <= 65535:
        raise UI3ProofError("UI3 listener port is outside bounded range")
    secret_path = root / "secrets" / "p7-06-ui3" / "access.secret"
    _assert_owner_file(secret_path, "UI3 ingress secret", 4096)
    secret = secret_path.read_text(encoding="utf-8").rstrip("\n")
    if not secret or "\n" in secret or "\r" in secret:
        raise UI3ProofError("UI3 ingress secret is malformed")

    status, _, body = _request(port, "GET", "/")
    if status != 401:
        raise UI3ProofError("unauthenticated protected GET did not fail closed")
    if secret.encode("utf-8") in body:
        raise UI3ProofError("ingress secret leaked in unauthenticated response")

    status, _, unlock_body = _request(port, "GET", UNLOCK)
    if status != 200:
        raise UI3ProofError("unlock form is unavailable on private listener")
    match = CSRF_RE.search(unlock_body.decode("utf-8", errors="strict"))
    if not match:
        raise UI3ProofError("unlock form did not provide CSRF token")
    csrf = match.group(1)

    wrong = urllib.parse.urlencode({"csrf": csrf, "access_secret": "definitely-wrong-ui3-secret"}).encode()
    headers = {
        "Origin": f"http://{HOST}:{port}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": str(len(wrong)),
    }
    status, _, wrong_body = _request(port, "POST", UNLOCK, body=wrong, headers=headers)
    if status != 401:
        raise UI3ProofError("wrong ingress secret did not fail closed")
    if secret.encode("utf-8") in wrong_body:
        raise UI3ProofError("ingress secret leaked in denied response")

    good = urllib.parse.urlencode({"csrf": csrf, "access_secret": secret}).encode()
    headers["Content-Length"] = str(len(good))
    status, response_headers, good_body = _request(port, "POST", UNLOCK, body=good, headers=headers)
    if status != 303:
        raise UI3ProofError("correct ingress secret did not establish private process session")
    if secret.encode("utf-8") in good_body or any(secret in value for value in response_headers.values()):
        raise UI3ProofError("ingress secret leaked in successful unlock response")
    cookie_header = response_headers.get("set-cookie", "")
    jar = SimpleCookie()
    try:
        jar.load(cookie_header)
    except Exception as exc:
        raise UI3ProofError("private process session cookie is malformed") from exc
    session = jar.get("arvectum_ui3_session")
    if session is None or "HttpOnly" not in cookie_header or "SameSite=Strict" not in cookie_header:
        raise UI3ProofError("private process session cookie lacks required boundaries")
    cookie = f"arvectum_ui3_session={session.value}"

    status, _, protected_body = _request(port, "GET", "/", headers={"Cookie": cookie})
    if status != 200:
        raise UI3ProofError("authenticated private process session cannot read workspace")
    if secret.encode("utf-8") in protected_body:
        raise UI3ProofError("ingress secret leaked in protected response")

    _run("sh", str(ui3_shell), "restart")
    status, _, after_restart = _request(port, "GET", "/", headers={"Cookie": cookie})
    if status != 401:
        raise UI3ProofError("restart did not invalidate prior browser session")
    if secret.encode("utf-8") in after_restart:
        raise UI3ProofError("ingress secret leaked after restart")

    return {
        "unauthenticated_access_denied": True,
        "wrong_secret_denied": True,
        "owner_local_unlock_verified": True,
        "session_cookie_bounded": True,
        "restart_invalidated_prior_session": True,
        "ingress_secret_not_returned_by_http": True,
    }


def _write_attestation(root: Path, value: dict[str, Any]) -> tuple[Path, str]:
    evidence_dir = root / "evidence" / "p7-06-ui3"
    p703._ensure_private_dir(evidence_dir)
    path = evidence_dir / f"p7-06-ui3-selected-mac-attestation-{p703._stamp()}-{uuid.uuid4().hex[:8]}.json"
    p703._atomic_json_write(path, value)
    digest = p703._sha256_file(path)
    p703._atomic_bytes_write(path.with_suffix(path.suffix + ".sha256"), f"{digest}  {path.name}\n".encode("utf-8"))
    return path, digest


def run_selected_mac_proof(root: Path, decision_ref: str) -> dict[str, Any]:
    if sys.platform != "darwin":
        raise UI3ProofError("macOS is required")
    root = root.expanduser().resolve()
    decision_ref = decision_ref.strip()
    if not decision_ref or len(decision_ref) > 256 or any(ch in decision_ref for ch in "\r\n\0"):
        raise UI3ProofError("decision reference is invalid")

    target = _current_release(root)
    exact_dir = _release_dir(root, target)
    expected_script = exact_dir / Path(__file__).name
    if Path(__file__).resolve() != expected_script.resolve():
        raise UI3ProofError("proof runner must execute from the exact active release")
    expected_python = _exact_python(root, target)
    observed_python = Path(sys.executable).expanduser().absolute()
    if observed_python != expected_python.expanduser().absolute():
        raise UI3ProofError("proof runner must use the exact active-release Python")

    ui3_shell = exact_dir / "p7_06_ui3_macos_operator.sh"
    if not ui3_shell.is_file() or ui3_shell.is_symlink():
        raise UI3ProofError("exact-release UI3 lifecycle shell is missing")
    source = _transaction_source(root, target)
    source_dir = _release_dir(root, source)
    source_ui3 = source_dir / "p7_06_ui3_macos_operator.sh"
    source_deploy = source_dir / "p7_06_macos_deploy.sh"
    source_had_ui3 = source_ui3.is_file() and not source_ui3.is_symlink()

    canonical_before = _canonical_digest(root)
    access_before = _p704_digest(root)

    _run("sh", str(ui3_shell), "install")
    _run("sh", str(ui3_shell), "status")
    http_result = _http_restart_proof(root, ui3_shell)

    _run("sh", str(ui3_shell), "uninstall")
    if _service_loaded() or not _ui3_private_material_absent(root):
        raise UI3ProofError("UI3 uninstall was not reversible/minimized")
    _run("sh", str(ui3_shell), "install")
    _run("sh", str(ui3_shell), "status")

    if _canonical_digest(root) != canonical_before:
        raise UI3ProofError("UI3 lifecycle changed P7.03 governed/checkpoint state")
    if _p704_digest(root) != access_before:
        raise UI3ProofError("UI3 lifecycle changed P7.04 grants/credentials")

    _run("sh", str(ui3_shell), "governed-rollback-last")
    if _current_release(root) != source:
        raise UI3ProofError("governed rollback did not restore exact source release")

    update_via_ui3_wrapper = False
    pre_ui3_cleanup_verified = False
    if source_had_ui3:
        _run("sh", str(source_ui3), "status")
        _run("sh", str(source_ui3), "governed-update", f"{decision_ref}:final-update")
        update_via_ui3_wrapper = True
    else:
        if _service_loaded() or not _ui3_private_material_absent(root):
            raise UI3ProofError("rollback to pre-UI3 source did not remove UI3 private surface")
        pre_ui3_cleanup_verified = True
        if not source_deploy.is_file() or source_deploy.is_symlink():
            raise UI3ProofError("exact source P7.06 deploy adapter is missing")
        _run("sh", str(source_deploy), "update", f"{decision_ref}:final-update")

    final_release = _current_release(root)
    if final_release != target:
        raise UI3ProofError("final governed update did not restore the exact proof target")
    final_ui3 = _release_dir(root, final_release) / "p7_06_ui3_macos_operator.sh"
    if not update_via_ui3_wrapper:
        _run("sh", str(final_ui3), "install")
    _run("sh", str(final_ui3), "status")

    if _canonical_digest(root) != canonical_before:
        raise UI3ProofError("rollback/re-update changed P7.03 governed/checkpoint state")
    if _p704_digest(root) != access_before:
        raise UI3ProofError("rollback/re-update changed P7.04 grants/credentials")

    attestation: dict[str, Any] = {
        "schema": ATTESTATION_SCHEMA,
        "status": "PASS",
        "classification": "owner-local non-canonical operational proof evidence",
        "operating_mode": "Persistent Internal / owner-operated",
        "proof_release_sha": target,
        "rollback_source_release_sha": source,
        "final_release_sha": final_release,
        "exact_release_runner_verified": True,
        "exact_release_python_verified": True,
        "existing_p704_least_privilege_required": True,
        "p704_grants_or_credentials_created_by_ui3": False,
        "p704_state_unchanged": True,
        "p703_governed_checkpoint_state_unchanged": True,
        "listener_ipv4_loopback_only": True,
        "listener_launchd_pid_attribution_verified_by_status": True,
        "accidental_public_ingress_detected": False,
        **http_result,
        "uninstall_reinstall_verified": True,
        "rollback_verified": True,
        "source_had_ui3": source_had_ui3,
        "pre_ui3_rollback_cleanup_verified": pre_ui3_cleanup_verified,
        "final_reupdate_verified": True,
        "final_update_via_ui3_wrapper": update_via_ui3_wrapper,
        "interaction_provider": "none-until-p7-06-ui4",
        "real_owner_interaction_invoked": False,
        "organizational_authority_provided": False,
        "consequential_approval_provided": False,
        "canonical_mutation_performed_by_ui3": False,
        "product_external_effect_invoked": False,
        "historical_effect_replay_invoked": False,
        "reusable_secret_emitted": False,
        "browser_session_value_emitted": False,
        "operator_decision_ref": decision_ref,
        "recorded_at": p703._utc_now(),
    }
    evidence_path, evidence_sha = _write_attestation(root, attestation)
    attestation["attestation_basename"] = evidence_path.name
    attestation["attestation_sha256"] = evidence_sha
    return attestation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.06-UI3 selected-Mac closure proof")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--decision-ref", default="P7.06-UI3-selected-mac-owner-operated-proof")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run_selected_mac_proof(Path(args.runtime_root), args.decision_ref)
    except (UI3ProofError, p703.P703Error, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.06-UI3 selected-Mac FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            "P7.06-UI3 selected-Mac PASS "
            f"release={result['final_release_sha']} "
            f"evidence={result['attestation_basename']} "
            f"sha256={result['attestation_sha256']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
