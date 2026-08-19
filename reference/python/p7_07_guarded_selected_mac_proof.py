#!/usr/bin/env python3
"""Guarded selected-Mac launcher for the P7.07 restart-survivability proof.

It wraps the existing selected-Mac proof runner and validates the product-owned
Tender Agent bridge immediately before every dynamic bridge load. The underlying
proof still owns exact release/runtime checks, product-repository provenance,
P7.03 state-tree stability, supervised P7.02 restart and same-exact-reliance
comparison.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import p7_07_guarded_operational_entrypoint as guard
import p7_07_persistent_tender_operator_contour as contour
import p7_07_selected_mac_proof_runner as proof


class P707GuardedProofError(RuntimeError):
    pass


def run_guarded_proof(**kwargs: Any) -> dict[str, Any]:
    product_repo = Path(kwargs["product_repo"])
    guard.validate_product_bridge(product_repo)

    original_loader = contour._load_product_bridge

    def validated_loader(repo: Path, adapters: Any):
        guard.validate_product_bridge(repo)
        return original_loader(repo, adapters)

    contour._load_product_bridge = validated_loader
    try:
        return proof.run_proof(**kwargs)
    finally:
        contour._load_product_bridge = original_loader


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--access-root", type=Path, required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--product-repo", type=Path, required=True)
    parser.add_argument("--evidence-output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = run_guarded_proof(**vars(args))
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2
    print("RESULT=PASS")
    print("PRODUCT_BRIDGE_GUARD=PASS")
    print(f"RELEASE_SHA={result['release_sha']}")
    print(f"PRODUCT_HEAD={result['product_head']}")
    print(f"STORAGE_ITEM_ID={result['storage_item_id']}")
    print("P7_03_STATE_UNCHANGED=true")
    print("SAME_EXACT_RELIANCE_AFTER_RESTART=true")
    print(f"EVIDENCE_PATH={result['evidence_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
