#!/usr/bin/env python3
"""Historical tender-app recovery helper superseded by divergent reconciliation.

This helper previously permitted exactly one legacy env source owned by historical
arutyunoveth/tender-app. Following owner decision DECISION-2026-08-14-P6-05-L3-DIVERGENT-EIS-SECRET-RECONCILIATION,
current operational recovery must use p6_05_l3_reconcile_owner_selected_divergent_sources.py.

Direct execution of this superseded path fails closed immediately without contacting
GitHub, reading secrets, or performing any filesystem mutation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

SUPERSEDED_FAILURE_CODE = "LEGACY_GITHUB_IDENTITY_PATH_SUPERSEDED"
REPLACEMENT_HELPER = "p6_05_l3_reconcile_owner_selected_divergent_sources.py"


def _safe_lines() -> list[str]:
    return [
        "p6_05_l3_owner_authorized_recovery_status=FAIL",
        f"failure_code={SUPERSEDED_FAILURE_CODE}",
        f"replacement_helper={REPLACEMENT_HELPER}",
        "secret_values_read=false",
        "secret_values_printed=false",
        "secret_values_hashed=false",
        "filesystem_modified=false",
        "product_invoked=false",
        "eis_invoked=false",
        "network_invoked=false",
        "external_actions=false",
    ]


def recover(
    discovery_file: Path,
    destination: Path,
    *,
    expected_checkout_count: int,
    expected_env_count: int,
    owner_authorization: str,
    arvectum_repo_root: Path | None = None,
) -> tuple[int, tuple[str, ...]]:
    return 2, tuple(_safe_lines())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Historical tender-app recovery helper superseded by divergent reconciliation."
    )
    parser.add_argument("--discovery-file", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--expected-checkout-count", required=True, type=int)
    parser.add_argument("--expected-env-count", required=True, type=int)
    parser.add_argument("--owner-authorization", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rc, lines = recover(
        args.discovery_file,
        args.destination,
        expected_checkout_count=args.expected_checkout_count,
        expected_env_count=args.expected_env_count,
        owner_authorization=args.owner_authorization,
    )
    for line in lines:
        print(line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
