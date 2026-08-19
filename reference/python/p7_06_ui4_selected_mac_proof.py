#!/usr/bin/env python3
"""P7.06-UI4 selected-Mac technical proof verifier.

The verifier consumes the minimized non-canonical browser-preflight evidence and
re-evaluates the current exact-release UI3/UI4/P7.04/P7.03/P7.05 boundaries.  It
cannot attest what the human visually inspected; owner visual/navigation/friction
observations remain a separate UI4 closure input.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

import p7_06_ui3_private_operator as ui3
import p7_06_ui4_owner_preflight as ui4


class UI4SelectedMacProofError(RuntimeError):
    pass


def _owner_json(path: Path, *, limit: int = 128 * 1024) -> tuple[Mapping[str, Any], str]:
    if path.is_symlink() or not path.is_file():
        raise UI4SelectedMacProofError("UI4 browser preflight evidence is missing or unsafe")
    if path.stat().st_size <= 0 or path.stat().st_size > limit:
        raise UI4SelectedMacProofError("UI4 browser preflight evidence is outside bounded size")
    if os.name != "nt" and path.stat().st_mode & 0o077:
        raise UI4SelectedMacProofError("UI4 browser preflight evidence is not owner-only")
    raw = path.read_bytes()
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UI4SelectedMacProofError("UI4 browser preflight evidence is unreadable") from exc
    if not isinstance(value, dict):
        raise UI4SelectedMacProofError("UI4 browser preflight evidence must be a JSON object")
    return value, hashlib.sha256(raw).hexdigest()


def verify_selected_mac(runtime_root: Path) -> Mapping[str, Any]:
    root = runtime_root.expanduser().resolve()
    ui3_status = ui3.verify_private_access(root, exact=True)
    if ui3_status.get("status") != "PASS" or ui3_status.get("ui4_preflight_enabled") is not True:
        raise UI4SelectedMacProofError("exact-release private owner/UI4 preflight access is unavailable")
    if ui3_status.get("organizational_authority_provided") is not False:
        raise UI4SelectedMacProofError("UI3 unexpectedly claims Organizational Authority")
    if ui3_status.get("consequential_approval_provided") is not False:
        raise UI4SelectedMacProofError("UI3 unexpectedly claims consequential approval")
    if ui3_status.get("canonical_mutation_performed") is not False:
        raise UI4SelectedMacProofError("UI3 unexpectedly claims canonical mutation")

    cfg = ui3.load_config(root)
    access = ui3.resolve_operator_access(root, cfg.credential_id)
    current = ui4.build_owner_preflight(
        root,
        organization=access.organization,
        principal=access.principal,
        credential_id=access.credential_id,
        credential_file=access.credential_file,
    )
    evidence_path = root / "evidence" / ui4.EVIDENCE_BASENAME
    evidence, evidence_sha256 = _owner_json(evidence_path)

    exact = {
        "schema": ui4.EVIDENCE_SCHEMA,
        "preflight_id": ui4.PREFLIGHT_ID,
        "release_sha": current.release_sha,
        "organization_id": current.organization_id,
        "actor_id": current.actor_id,
        "storage_item_id": current.storage_item_id,
        "subject_identity": current.subject_identity,
        "version_identity": current.version_identity,
        "execution_subject": current.execution_subject,
        "execution_version": current.execution_version,
        "event_version": current.event_version,
        "checkpoint_id": current.checkpoint_id,
        "technical_interaction_access": True,
        "browser_preflight_post_observed": True,
        "organizational_authority_provided": False,
        "consequential_approval_provided": False,
        "canonical_mutation_requested": False,
        "canonical_mutation_performed": False,
        "product_or_external_effect_requested": False,
        "product_or_external_effect_performed": False,
        "reusable_secret_recorded": False,
        "browser_session_recorded": False,
    }
    for key, expected in exact.items():
        if evidence.get(key) != expected:
            raise UI4SelectedMacProofError(f"UI4 evidence/current-state continuity mismatch: {key}")
    expected_gates = {row.name: "Waiting" for row in current.gates}
    if evidence.get("gate_states") != expected_gates:
        raise UI4SelectedMacProofError("UI4 evidence does not preserve the four fail-closed gate states")
    recorded_at = evidence.get("recorded_at")
    if not isinstance(recorded_at, str) or not recorded_at.strip():
        raise UI4SelectedMacProofError("UI4 evidence lacks an attributable recorded timestamp")

    return {
        "status": "PASS",
        "task": "P7.06-UI4 selected-Mac technical owner-preflight proof",
        "release_sha": current.release_sha,
        "listener": ui3_status.get("listener"),
        "organization_id": current.organization_id,
        "actor_id": current.actor_id,
        "subject_identity": current.subject_identity,
        "version_identity": current.version_identity,
        "execution_version": current.execution_version,
        "event_version": current.event_version,
        "checkpoint_id": current.checkpoint_id,
        "gate_states": expected_gates,
        "browser_preflight_post_observed": True,
        "technical_interaction_access": True,
        "organizational_authority_provided": False,
        "consequential_approval_provided": False,
        "canonical_mutation_performed": False,
        "product_or_external_effect_performed": False,
        "evidence_basename": evidence_path.name,
        "evidence_sha256": evidence_sha256,
        "human_visual_navigation_attested": False,
        "operator_friction_review_pending": True,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    value.add_argument("--runtime-root", required=True)
    value.add_argument("--json", action="store_true")
    return value


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    try:
        result = verify_selected_mac(Path(args.runtime_root))
    except (UI4SelectedMacProofError, ui3.UI3Error, ui4.UI4Error, OSError, ValueError) as exc:
        print(f"P7.06-UI4 technical proof FAIL: {exc}", file=os.sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print("P7.06-UI4 technical proof PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
