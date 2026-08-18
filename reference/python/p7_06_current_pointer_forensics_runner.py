#!/usr/bin/env python3
"""Safe entry point for P7.06 current-pointer forensics.

The core diagnostic writes its attestation before returning. This wrapper defers
that write so classification precedence can be finalized first: any explicit new
P7.06 rollback/recovery evidence observed during the update-command interval must
not be hidden by a later stable-looking pointer shape.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import p7_06_current_pointer_forensics as core


def _prioritize_explicit_evidence(result: dict[str, Any]) -> dict[str, Any]:
    classification = result.get("classification")
    during = result.get("during_update_rollback_or_recovery_classification")
    exit_code = result.get("update_exit_code")
    if (
        exit_code == 0
        and isinstance(during, str)
        and during in {
            "EXPLICIT_P7_06_ROLLBACK_EVIDENCE",
            "EXPLICIT_P7_06_RECOVERY_EVIDENCE",
        }
        and classification in {"STABLE_AFTER_UPDATE", "UNATTRIBUTED_CURRENT_MUTATION"}
    ):
        result["classification"] = during
        result["status"] = "OBSERVED"
    return result


def run(root: Path, repo_root: Path, decision_ref: str, watch_seconds: float) -> dict[str, Any]:
    original_writer = core._write_attestation

    def deferred_writer(_root: Path, _value: dict[str, Any]) -> tuple[Path, str]:
        return Path("DEFERRED"), "DEFERRED"

    core._write_attestation = deferred_writer
    try:
        result = core.run_forensics(root, repo_root, decision_ref, watch_seconds)
    finally:
        core._write_attestation = original_writer

    result = _prioritize_explicit_evidence(result)
    result.pop("attestation_basename", None)
    result.pop("attestation_sha256", None)
    evidence_path, digest = original_writer(root.expanduser().resolve(), result)
    result["attestation_basename"] = evidence_path.name
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
        result = run(
            Path(args.runtime_root),
            Path(args.repo_root),
            args.decision_ref,
            args.watch_seconds,
        )
    except (core.ForensicsError, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"P7.06 current-pointer forensics FAIL: {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    else:
        print(
            "P7.06 current-pointer forensics "
            f"{result['classification']} final={result['final_release']} "
            f"attestation={result['attestation_basename']}"
        )
    return 0 if result["classification"] == "STABLE_AFTER_UPDATE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
