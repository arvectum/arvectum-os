#!/usr/bin/env python3
"""Supported P7.06-UI3 selected-Mac proof entry point.

The core proof intentionally exercises rollback to an exact historical release.
This runner keeps the current hardened UI3 lifecycle controller as the invoking
controller across that rollback while all service Python/module/config checks
remain pinned dynamically to the actual ``current`` release.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import p7_03_durable_state as p703
import p7_06_ui3_selected_mac_proof as core


class UI3ProofRunnerError(RuntimeError):
    pass


def _is_ui3_shell_call(args: tuple[str, ...]) -> bool:
    return (
        len(args) >= 3
        and args[0] == "sh"
        and Path(args[1]).name == "p7_06_ui3_macos_operator.sh"
    )


def run(root: Path, decision_ref: str) -> dict[str, Any]:
    root = root.expanduser().resolve()
    target = core._current_release(root)
    expected_runner = core._release_dir(root, target) / Path(__file__).name
    if Path(__file__).resolve() != expected_runner.resolve():
        raise UI3ProofRunnerError("supported proof runner must execute from the exact active release")

    target_controller = core._release_dir(root, target) / "p7_06_ui3_macos_operator.sh"
    if target_controller.is_symlink() or not target_controller.is_file():
        raise UI3ProofRunnerError("hardened exact-target UI3 controller is missing")

    original_run = core._run
    original_writer = core._write_attestation

    def hardened_run(*args: str) -> None:
        if _is_ui3_shell_call(args):
            rewritten = ("sh", str(target_controller), *args[2:])
            return original_run(*rewritten)
        return original_run(*args)

    def hardened_writer(evidence_root: Path, value: dict[str, Any]):
        value["hardened_controller_runner_verified"] = True
        value["historical_ui3_controller_replayed"] = False
        value["hardened_controller_release_sha"] = target
        return original_writer(evidence_root, value)

    core._run = hardened_run
    core._write_attestation = hardened_writer
    try:
        result = core.run_selected_mac_proof(root, decision_ref)
    finally:
        core._run = original_run
        core._write_attestation = original_writer
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Arvectum OS P7.06-UI3 selected-Mac closure proof")
    parser.add_argument("--runtime-root", required=True)
    parser.add_argument("--decision-ref", default="P7.06-UI3-selected-mac-owner-operated-proof")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = run(Path(args.runtime_root), args.decision_ref)
    except (
        UI3ProofRunnerError,
        core.UI3ProofError,
        p703.P703Error,
        OSError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
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
