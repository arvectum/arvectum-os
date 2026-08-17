#!/usr/bin/env python3
"""P7.03 selected-Mac closure proof wrapper.

This wrapper removes ambiguity about the required-runtime CLI flag. It always
requires an observed healthy P7.02 runtime before and after the P7.03 core
backup/restore proof, verifies the core proof summary, and emits a separate
non-canonical local attestation. It does not start/stop/update the runtime and
does not authorize canonical mutation or external effects.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional

import p7_03_durable_state as p703

ATTESTATION_SCHEMA = "arvectum.p7_03.selected-mac-attestation/1"


def _required_runtime_observation(root: Path) -> Dict[str, Any]:
    observed = p703._observe_persistent_runtime(root)
    if not observed["observed"]:
        raise p703.IntegrityError("selected-Mac attestation requires observable P7.02 persistent runtime health")
    if observed["state"] != "healthy":
        raise p703.IntegrityError(
            f"selected-Mac attestation requires healthy persistent runtime, got {observed['state']!r}"
        )
    return observed


def run_selected_mac_proof(root: Path, release_sha: str) -> Dict[str, Any]:
    release_sha = p703._validate_release_sha(release_sha)
    root = root.expanduser().resolve()

    before = _required_runtime_observation(root)
    core = p703.run_proof(root, release_sha, require_persistent_runtime=True)
    after = _required_runtime_observation(root)

    if core.get("status") != "PASS":
        raise p703.IntegrityError("core P7.03 proof did not report PASS")
    if core.get("persistent_runtime_observed") is not True:
        raise p703.IntegrityError("core P7.03 proof did not attest runtime observation")
    if core.get("persistent_runtime_state") != "healthy":
        raise p703.IntegrityError("core P7.03 proof summary does not attest healthy runtime")
    if core.get("persistent_runtime_release_sha") != before["release_sha"]:
        raise p703.IntegrityError("core proof runtime release does not match pre-proof observation")
    if after["release_sha"] != before["release_sha"]:
        raise p703.IntegrityError("persistent runtime release changed during selected-Mac proof")

    attestation = {
        "schema": ATTESTATION_SCHEMA,
        "status": "PASS",
        "classification": "non-canonical operational proof evidence",
        "operating_mode": p703.OPERATING_MODE,
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "tool_release_sha": release_sha,
        "required_runtime_enforced": True,
        "persistent_runtime_release_sha_before": before["release_sha"],
        "persistent_runtime_state_before": before["state"],
        "persistent_runtime_release_sha_after": after["release_sha"],
        "persistent_runtime_state_after": after["state"],
        "core_summary_basename": core["summary_basename"],
        "live_backup_basename": core["live_backup_basename"],
        "live_backup_sha256": core["live_backup_sha256"],
        "live_restore_integrity": core["live_restore_integrity"],
        "live_state_digest_matches_restore": core["live_state_digest_matches_restore"],
        "fixture_backup_integrity": core["fixture_backup_integrity"],
        "fixture_restore_integrity": core["fixture_restore_integrity"],
        "tamper_detection_fail_closed": core["tamper_detection_fail_closed"],
        "explicit_exclusions_absent": core["explicit_exclusions_absent"],
        "reusable_secrets_in_backup": core["reusable_secrets_in_backup"],
        "telemetry_in_backup": core["telemetry_in_backup"],
        "cache_in_backup": core["cache_in_backup"],
        "checkpoint_canonical_authority": core["checkpoint_canonical_authority"],
        "external_effect_replay_authorized": core["external_effect_replay_authorized"],
        "proof_fixture_canonical_authority": core["proof_fixture_canonical_authority"],
        "created_at": p703._utc_now(),
    }

    evidence_dir = p703._layout(root)["evidence"]
    p703._ensure_private_dir(evidence_dir)
    evidence_path = evidence_dir / f"p7-03-selected-mac-attestation-{p703._stamp()}-{uuid.uuid4().hex[:8]}.json"
    p703._atomic_json_write(evidence_path, attestation)
    attestation["attestation_basename"] = evidence_path.name
    return attestation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.03 selected-Mac closure proof")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--release-sha", required=True)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run_selected_mac_proof(Path(args.runtime_root), args.release_sha)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        else:
            print(
                "P7.03 selected-Mac PASS "
                f"runtime_release={result['persistent_runtime_release_sha_after']} "
                f"backup={result['live_backup_basename']} "
                f"attestation={result['attestation_basename']}"
            )
    except (p703.P703Error, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.03 selected-Mac FAIL: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
