#!/usr/bin/env python3
"""Bounded P8.07 portability/handover interoperability proof.

This reference harness is not a public export API and does not authorize a customer
handover. Current Phase 8 has no permitted external portability recipient, so any
attempt to activate external transfer fails closed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

PACKAGE_SCHEMA = "arvectum.p8-07-governed-handover.v1"
RECEIPT_SCHEMA = "arvectum.p8-07-receiver-receipt.v1"
FORMAT_VERSION = "1.0"
ORGANIZATION = "ООО «Арвектум»"
PROOF_SCOPE = "p8.07.bounded-interoperability-proof"
RECEIVER_KIND = "isolated_interoperability_receiver"
PACKAGE_MEMBERS = frozenset({"package.json", "package.sha256"})


class HandoverInteroperabilityError(RuntimeError):
    pass


def _bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise HandoverInteroperabilityError(message)


def validate_migration_authority_transition(
    *, source_authority_active: bool, receiver_authority_active: bool, transition_authorization_ref: str | None
) -> None:
    if source_authority_active and receiver_authority_active:
        raise HandoverInteroperabilityError("migration would create two concurrently authoritative systems")
    if receiver_authority_active and not transition_authorization_ref:
        raise HandoverInteroperabilityError("receiver authority requires explicit governed transition authorization")


def _proof_document(receiver_id: str) -> dict[str, Any]:
    subject_id = "subject:p8-07:case-001"
    version_id = "version:p8-07:case-001:v1"
    event_id = "event:p8-07:case-001:admitted"
    outcome = {
        "outcome_id": "outcome:p8-07:case-001:verified",
        "subject_id": subject_id,
        "version_id": version_id,
        "derived_from_event_ids": [event_id],
        "status": "Verified",
        "decision": "NO_EXTERNAL_EFFECT",
    }
    return {
        "schema": PACKAGE_SCHEMA,
        "format_version": FORMAT_VERSION,
        "organization": ORGANIZATION,
        "scope": PROOF_SCOPE,
        "receiver": {"receiver_id": receiver_id, "receiver_kind": RECEIVER_KIND},
        "semantic_state": {
            "subjects": [{
                "subject_id": subject_id,
                "semantic_type": "InteroperabilityProofCase",
                "authority_mode": "Native",
                "authority_scope": "synthetic P8.07 proof fixture only",
            }],
            "versions": [{"version_id": version_id, "subject_id": subject_id, "sequence": 1, "immutable": True}],
            "relationships": [{
                "relationship_id": "relationship:p8-07:case-001:derived-from",
                "relationship_type": "derived_from",
                "source": {"subject_id": subject_id, "version_id": version_id},
                "target": {"external_reference": "external-reference:p8-07:synthetic-source"},
            }],
        },
        "history": {
            "events": [{
                "event_id": event_id,
                "event_type": "RecordAdmitted",
                "subject_id": subject_id,
                "version_id": version_id,
                "occurred_at": "2026-08-20T00:00:00Z",
                "recorded_at": "2026-08-20T00:00:01Z",
                "external_effect_replay_authorized": False,
            }],
            "selected_historical_outcome": outcome,
            "selected_historical_outcome_sha256": _sha(_bytes(outcome)),
        },
        "handling_constraints": {
            "data_classification": "Internal",
            "purpose_limitation": ["P8.07 interoperability proof"],
            "rights": {
                "read_exported_proof": True,
                "redistribute": False,
                "customer_facing_use": False,
                "cross_organization_transfer": False,
            },
            "retention": {"policy_scope": "P8.07 proof lifecycle", "receiver_must_preserve_constraint": True},
            "deletion": {"post_termination": "delete or retain only under an explicit governed instruction"},
        },
        "explicit_omissions": [
            {
                "kind": "secret",
                "identifier": "source_credentials",
                "reason": "non-exportable",
                "reprovisioning": "receiver-specific credentials require a separate authorized channel",
            },
            {
                "kind": "ephemeral_runtime",
                "identifier": "runtime_cache_and_telemetry",
                "reason": "non-canonical and unnecessary for semantic reconstruction",
                "reprovisioning": "recreate locally if required by the receiver runtime",
            },
        ],
        "authority": {
            "organizational_authority_transferred": False,
            "technical_access_granted": False,
            "credentials_exported": False,
            "external_effect_replay_authorized": False,
            "external_transfer": {
                "activated": False,
                "activation_gate": "concrete permitted external recipient and scope required",
            },
        },
        "migration": {
            "mode": "NO_AUTHORITY_TRANSFER",
            "source_authority_active": True,
            "receiver_authority_active": False,
            "transition_authorization_ref": None,
        },
        "termination_and_revocation": {
            "export_before_or_during_termination_supported": True,
            "active_credentials_must_be_revoked_separately": True,
            "receiver_access_must_be_revoked_separately": True,
            "organizational_authority_transfer_is_separate": True,
            "post_termination_retention_or_deletion_instruction_required": True,
            "handover_or_deletion_evidence_required_where_applicable": True,
        },
        "non_goals": [
            "public or stable export API",
            "universal customer export format",
            "automatic customer transfer authorization",
            "Organizational Authority transfer",
            "technical access grant",
            "external effect replay",
        ],
    }


def create_governed_handover_package(
    package_dir: Path, *, receiver_id: str, external_transfer_activated: bool = False
) -> dict[str, Any]:
    _require(bool(receiver_id.strip()), "receiver_id is required")
    if external_transfer_activated:
        raise HandoverInteroperabilityError(
            "external transfer activation is outside the current P8.07 proof; "
            "a concrete permitted recipient/scope and fresh governed implementation are required"
        )
    package_dir.mkdir(parents=True, exist_ok=True)
    _require(not any(package_dir.iterdir()), "package directory must be empty")
    document = _proof_document(receiver_id)
    data = _bytes(document)
    (package_dir / "package.json").write_bytes(data)
    (package_dir / "package.sha256").write_text(_sha(data) + "\n", encoding="utf-8")
    return document


def _read_verified(package_dir: Path, receiver_id: str) -> dict[str, Any]:
    _require(package_dir.is_dir(), "package directory does not exist")
    members = {p.name for p in package_dir.iterdir() if p.is_file()}
    _require(members == PACKAGE_MEMBERS, "unexpected or missing package members")
    raw = (package_dir / "package.json").read_bytes()
    _require((package_dir / "package.sha256").read_text().strip() == _sha(raw), "package integrity mismatch")
    try:
        doc = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HandoverInteroperabilityError("invalid package JSON") from exc
    _require(isinstance(doc, dict), "package object required")
    _require(doc.get("schema") == PACKAGE_SCHEMA, "unsupported package schema")
    _require(doc.get("format_version") == FORMAT_VERSION, "unsupported format version")
    _require(doc.get("organization") == ORGANIZATION, "organization mismatch")
    _require(doc.get("scope") == PROOF_SCOPE, "scope mismatch")
    receiver = doc.get("receiver", {})
    _require(receiver.get("receiver_id") == receiver_id, "receiver mismatch")
    _require(receiver.get("receiver_kind") == RECEIVER_KIND, "receiver kind mismatch")
    return doc


def _validate_semantics(doc: dict[str, Any]) -> None:
    state = doc.get("semantic_state", {})
    subjects, versions, relationships = state.get("subjects", []), state.get("versions", []), state.get("relationships", [])
    _require(subjects and versions and relationships, "subject/version/relationship semantics required")
    subject_ids = {item.get("subject_id") for item in subjects}
    version_map = {item.get("version_id"): item.get("subject_id") for item in versions}
    _require(None not in subject_ids and None not in version_map, "semantic identity missing")
    for version_id, subject_id in version_map.items():
        _require(subject_id in subject_ids, f"version endpoint unresolved: {version_id}")
    for relation in relationships:
        source, target = relation.get("source", {}), relation.get("target", {})
        sid, vid = source.get("subject_id"), source.get("version_id")
        _require(sid in subject_ids and version_map.get(vid) == sid, "relationship source unresolved")
        _require(target.get("subject_id") in subject_ids or bool(target.get("external_reference")), "relationship target unresolved")
    omissions = doc.get("explicit_omissions", [])
    secrets = [item for item in omissions if item.get("kind") == "secret"]
    _require(secrets and all(item.get("reprovisioning") for item in secrets), "secret omission/reprovisioning required")


def _reconstruct(doc: dict[str, Any]) -> dict[str, Any]:
    history = doc.get("history", {})
    events, outcome = history.get("events", []), history.get("selected_historical_outcome")
    _require(events and isinstance(outcome, dict), "historical evidence required")
    event_ids = {item.get("event_id") for item in events}
    _require(all(event_id in event_ids for event_id in outcome.get("derived_from_event_ids", [])), "historical event missing")
    _require(all(item.get("external_effect_replay_authorized") is False for item in events), "historical replay may not authorize external effect")
    _require(history.get("selected_historical_outcome_sha256") == _sha(_bytes(outcome)), "historical reconstruction digest mismatch")
    return outcome


def verify_receiver_package(package_dir: Path, *, expected_receiver_id: str) -> dict[str, Any]:
    doc = _read_verified(package_dir, expected_receiver_id)
    _validate_semantics(doc)
    handling = doc.get("handling_constraints", {})
    rights = handling.get("rights", {})
    _require(bool(handling.get("data_classification")) and bool(handling.get("purpose_limitation")), "classification/purpose required")
    _require(rights.get("redistribute") is False, "redistribution must remain denied")
    _require(rights.get("customer_facing_use") is False, "customer-facing use must remain denied")
    _require(rights.get("cross_organization_transfer") is False, "cross-Organization transfer must remain denied")
    _require(handling.get("retention", {}).get("receiver_must_preserve_constraint") is True, "retention propagation required")
    _require(bool(handling.get("deletion", {}).get("post_termination")), "post-termination instruction required")

    authority = doc.get("authority", {})
    for key in ("organizational_authority_transferred", "technical_access_granted", "credentials_exported", "external_effect_replay_authorized"):
        _require(authority.get(key) is False, f"handover invariant violated: {key}")
    transfer = authority.get("external_transfer", {})
    _require(transfer.get("activated") is False and bool(transfer.get("activation_gate")), "external transfer must remain fail-closed")

    migration = doc.get("migration", {})
    validate_migration_authority_transition(
        source_authority_active=migration.get("source_authority_active") is True,
        receiver_authority_active=migration.get("receiver_authority_active") is True,
        transition_authorization_ref=migration.get("transition_authorization_ref"),
    )
    termination = doc.get("termination_and_revocation", {})
    for key in (
        "export_before_or_during_termination_supported",
        "active_credentials_must_be_revoked_separately",
        "receiver_access_must_be_revoked_separately",
        "organizational_authority_transfer_is_separate",
        "post_termination_retention_or_deletion_instruction_required",
        "handover_or_deletion_evidence_required_where_applicable",
    ):
        _require(termination.get(key) is True, f"termination/revocation control missing: {key}")

    raw_lower = (package_dir / "package.json").read_bytes().lower()
    _require(b'"secret_value"' not in raw_lower and b'"credential_value"' not in raw_lower, "secret material field detected")
    outcome = _reconstruct(doc)
    return {
        "schema": RECEIPT_SCHEMA,
        "package_schema": PACKAGE_SCHEMA,
        "format_version": FORMAT_VERSION,
        "receiver_id": expected_receiver_id,
        "receiver_kind": RECEIVER_KIND,
        "integrity": "PASS",
        "semantic_interpretation": "PASS",
        "handling_constraints_interpreted": "PASS",
        "historical_reconstruction": {"status": "PASS", "outcome_id": outcome["outcome_id"]},
        "authority_transfer": "NONE",
        "technical_access_grant": "NONE",
        "external_effect_replay": "DENIED",
        "external_transfer_activated": False,
        "migration_authority_conflict": "NONE",
        "termination_revocation_path": "EXPLICIT",
    }


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "verify"):
        command = sub.add_parser(name)
        command.add_argument("--package-dir", required=True)
        command.add_argument("--receiver-id", required=True)
    args = parser.parse_args()
    try:
        result = (
            create_governed_handover_package(Path(args.package_dir), receiver_id=args.receiver_id)
            if args.command == "create"
            else verify_receiver_package(Path(args.package_dir), expected_receiver_id=args.receiver_id)
        )
    except HandoverInteroperabilityError as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
