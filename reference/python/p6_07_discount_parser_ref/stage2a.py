"""P6.07 Stage 2A pre-effect execution-ticket evidence.

Stage 2A runs on the Arvectum OS side before any real Discount Parser Telegram
send.  It creates one immutable execution ticket plus a SHA-256 digest that the
Windows Stage 2B publication must bind to.

The ticket is deliberately domain-light.  Candidate, target, publication
reservation/attempt and external outcome remain product-owned evidence created
by Discount Parser before/during Stage 2B.  This module performs no network
access, stores no reusable secret and grants no authorization for the external
mutation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from .contract import (
    P6_06_CANONICAL_BLOB_SHA,
    P6_06_CANONICAL_CONTRACT_PATH,
    PRODUCT_COMPATIBILITY_LINE,
    PRODUCT_CONTRACT_VERSION,
    PRODUCT_ID_VALUE,
)


TICKET_FILENAME: Final = "p6-07-stage2-execution-ticket.json"
DIGEST_FILENAME: Final = "p6-07-stage2-execution-ticket.sha256"
TICKET_SCHEMA: Final = "arvectum-os.p6-07-stage2a-execution-ticket"
TICKET_SCHEMA_VERSION: Final = "1"
OPERATION_NAME: Final = "discount-parser.controlled-telegram-publication"
CAPABILITY_DEPENDENCY: Final = "CAP-004"
REPOSITORY_FULL_NAME: Final = "arvectum/arvectum-os"
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class Stage2ATicketError(ValueError):
    """Stage 2A evidence is invalid or would violate the bounded handoff."""


def _required_text(value: str, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Stage2ATicketError(f"{field} must be a non-empty string")
    return value.strip()


def _utc_timestamp(value: datetime) -> str:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise Stage2ATicketError("created_at must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def build_stage2a_ticket(
    *,
    organization_id: str,
    actor_id: str,
    canonical_repo_sha: str,
    created_at: datetime,
    execution_id: str | None = None,
) -> dict[str, Any]:
    """Build one bounded pre-effect execution ticket.

    The returned object is not an authorization grant.  Stage 2B must obtain and
    preserve explicit real-action authorization independently and must record its
    exact candidate, target and product-side reservation/intent before the send.
    """

    organization_id = _required_text(organization_id, field="organization_id")
    actor_id = _required_text(actor_id, field="actor_id")
    canonical_repo_sha = _required_text(canonical_repo_sha, field="canonical_repo_sha").lower()
    if not _SHA_RE.fullmatch(canonical_repo_sha):
        raise Stage2ATicketError("canonical_repo_sha must be a full 40-character lowercase Git SHA")

    if execution_id is None:
        execution_id = f"p6-07-stage2-{uuid.uuid4()}"
    execution_id = _required_text(execution_id, field="execution_id")

    return {
        "schema": TICKET_SCHEMA,
        "schema_version": TICKET_SCHEMA_VERSION,
        "stage": "P6.07 Stage 2A",
        "status": "pre-effect-intent-recorded",
        "created_at": _utc_timestamp(created_at),
        "execution_id": execution_id,
        "organization": {
            "organization_id": organization_id,
            "ambient_default_permitted": False,
        },
        "actor": {
            "principal_id": actor_id,
            "kind": "human",
            "attributable": True,
        },
        "operation": {
            "name": OPERATION_NAME,
            "side_effect_class": "ExternalMutation",
            "max_external_sends": 1,
            "scheduler_autopost_permitted": False,
        },
        "product": {
            "identity": PRODUCT_ID_VALUE,
            "compatibility_line": PRODUCT_COMPATIBILITY_LINE,
        },
        "product_contract": {
            "path": P6_06_CANONICAL_CONTRACT_PATH,
            "version": PRODUCT_CONTRACT_VERSION,
            "blob_sha": P6_06_CANONICAL_BLOB_SHA,
            "lifecycle": "Provisional",
            "shared_dependencies": [CAPABILITY_DEPENDENCY],
        },
        "governance": {
            "constitution": "1.2.0",
            "accepted_rfc": [
                "RFC-0001@1.0.0",
                "RFC-0002@1.0.0",
                "RFC-0003@1.0.0",
                "RFC-0004@1.0.0",
                "RFC-0005@1.0.0",
                "RFC-0006@1.0.0",
            ],
            "product_contract_is_authorization": False,
            "ticket_is_authorization": False,
            "explicit_real_action_authorization_required_before_stage2b_send": True,
        },
        "stage2b_handoff": {
            "must_bind_exact_ticket_sha256": True,
            "must_preserve_execution_id": True,
            "must_preserve_same_organization_and_human_actor": True,
            "must_record_candidate_and_target_before_send": True,
            "must_record_product_pre_effect_reservation_and_intent_before_send": True,
            "must_record_explicit_real_action_authorization_before_send": True,
            "must_perform_at_most_one_external_send": True,
            "must_not_enable_scheduler_or_autopost": True,
            "must_not_blind_retry_uncertain_external_outcome": True,
            "must_return_confirmed_effect_or_explicit_uncertain_outcome": True,
        },
        "stage2c_handoff": {
            "requires_cap004_reconstruction": True,
            "reconstruction_is_read_only_derived_evidence": True,
        },
        "provenance": {
            "repository": REPOSITORY_FULL_NAME,
            "canonical_repo_sha": canonical_repo_sha,
            "canonical_product_contract_blob_sha": P6_06_CANONICAL_BLOB_SHA,
        },
        "containment": {
            "network_access": False,
            "telegram_call": False,
            "product_database_mutation": False,
            "canonical_state_mutation": False,
            "reusable_secrets": False,
        },
    }


def serialize_ticket(ticket: dict[str, Any]) -> bytes:
    """Return stable UTF-8 bytes whose exact digest is used for handoff."""

    return (json.dumps(ticket, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def ticket_sha256(ticket_bytes: bytes) -> str:
    if not isinstance(ticket_bytes, bytes):
        raise Stage2ATicketError("ticket_bytes must be bytes")
    return hashlib.sha256(ticket_bytes).hexdigest()


def write_stage2a_evidence(*, output_dir: Path, ticket: dict[str, Any]) -> tuple[Path, Path, str]:
    """Create ticket and digest exactly once; existing evidence is never overwritten."""

    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    ticket_path = output_dir / TICKET_FILENAME
    digest_path = output_dir / DIGEST_FILENAME

    if ticket_path.exists() or digest_path.exists():
        raise Stage2ATicketError("Stage 2A evidence already exists; refusing to overwrite immutable handoff")

    payload = serialize_ticket(ticket)
    digest = ticket_sha256(payload)

    with ticket_path.open("xb") as handle:
        handle.write(payload)
    with digest_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{digest}  {TICKET_FILENAME}\n")

    return ticket_path, digest_path, digest


def verify_stage2a_evidence(*, ticket_path: Path, digest_path: Path) -> bool:
    ticket_path = Path(ticket_path).expanduser()
    digest_path = Path(digest_path).expanduser()
    try:
        expected_line = digest_path.read_text(encoding="utf-8").strip()
        expected_digest, expected_name = expected_line.split(maxsplit=1)
    except (OSError, ValueError):
        return False
    if expected_name.strip() != TICKET_FILENAME:
        return False
    try:
        payload = ticket_path.read_bytes()
    except OSError:
        return False
    return expected_digest == ticket_sha256(payload)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create P6.07 Stage 2A immutable pre-effect evidence")
    parser.add_argument("--organization-id", required=True)
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--canonical-repo-sha", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--execution-id")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    ticket = build_stage2a_ticket(
        organization_id=args.organization_id,
        actor_id=args.actor_id,
        canonical_repo_sha=args.canonical_repo_sha,
        created_at=datetime.now(timezone.utc),
        execution_id=args.execution_id,
    )
    ticket_path, digest_path, digest = write_stage2a_evidence(output_dir=args.output_dir, ticket=ticket)
    if not verify_stage2a_evidence(ticket_path=ticket_path, digest_path=digest_path):
        raise SystemExit("Stage 2A verification failed after write")
    print(f"STAGE2A_TICKET={ticket_path}")
    print(f"STAGE2A_SHA256_FILE={digest_path}")
    print(f"STAGE2A_SHA256={digest}")
    print(f"STAGE2A_EXECUTION_ID={ticket['execution_id']}")
    print("STAGE2A_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
