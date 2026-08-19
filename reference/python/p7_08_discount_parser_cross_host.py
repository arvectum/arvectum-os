#!/usr/bin/env python3
"""P7.08 persistent Discount Parser cross-host operational contour.

Private/reversible operational harness for the owner-operated Windows <-> Mac mini
evidence/reconstruction path.  It preserves P6.06 Product Contract 0.1.0 and its
CAP-004-only shared dependency.

The contour deliberately separates three steps:

* Mac mini ``issue``: create the immutable P6.07-compatible Stage 2A ticket in a
  Mac-private run directory and emit a minimized dispatch envelope containing no
  Organization/Actor identity.
* Windows ``handoff``: bind owner-local raw pre-effect/outcome evidence by
  SHA-256, validate a strict product-owned publication descriptor, and emit only
  minimized transferable evidence.
* Mac mini ``reconstruct``: verify the locally retained ticket plus the returned
  handoff, reconstruct through CAP-004 read-only support, and write an immutable
  non-canonical operational report/receipt.

No command calls Telegram, invokes Discount Parser publication, mutates a product
database, writes canonical platform state, or replays an external effect.
Transport between hosts is intentionally operator-selected; the transferred
directory is evidence, not shared mutable state or a platform transport contract.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Final

from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal

from p6_07_discount_parser_ref.contract import (
    P6_06_CANONICAL_BLOB_SHA,
    PRODUCT_COMPATIBILITY_LINE,
    PRODUCT_CONTRACT_VERSION,
    build_p6_06_product_contract_projection,
)
from p6_07_discount_parser_ref.journey import reconstruct_publication
from p6_07_discount_parser_ref.stage2a import (
    DIGEST_FILENAME as STAGE2A_DIGEST_FILENAME,
    OPERATION_NAME,
    TICKET_FILENAME as STAGE2A_TICKET_FILENAME,
    TICKET_SCHEMA as STAGE2A_TICKET_SCHEMA,
    build_stage2a_ticket,
    ticket_sha256,
    verify_stage2a_evidence,
    write_stage2a_evidence,
)


REPOSITORY_FULL_NAME: Final = "arvectum/arvectum-os"
PRODUCT_REPOSITORY: Final = "arvectum/discount-parser"
PRODUCT_CONTRACT_VERSION_ID: Final = "p6-06-arvectum-discount-parser-v0.1.0"
PURPOSE: Final = "controlled-publication-reconstruction"
CLASSIFICATION: Final = "internal"

DISPATCH_SCHEMA: Final = "arvectum-os.p7-08.discount-parser-dispatch"
DISPATCH_SCHEMA_VERSION: Final = "1"
DISPATCH_FILENAME: Final = "p7-08-discount-parser-dispatch.json"
DISPATCH_DIGEST_FILENAME: Final = "p7-08-discount-parser-dispatch.sha256"

DESCRIPTOR_SCHEMA: Final = "arvectum-discount-parser.p7-08.local-publication-evidence"
DESCRIPTOR_SCHEMA_VERSION: Final = "1"

HANDOFF_SCHEMA: Final = "arvectum-os.p7-08.discount-parser-minimized-handoff"
HANDOFF_SCHEMA_VERSION: Final = "1"
HANDOFF_FILENAME: Final = "p7-08-discount-parser-handoff.json"
HANDOFF_DIGEST_FILENAME: Final = "p7-08-discount-parser-handoff.sha256"

REPORT_SCHEMA: Final = "arvectum-os.p7-08.discount-parser-cap004-reconstruction"
REPORT_SCHEMA_VERSION: Final = "1"
REPORT_FILENAME: Final = "p7-08-discount-parser-reconstruction.json"
REPORT_DIGEST_FILENAME: Final = "p7-08-discount-parser-reconstruction.sha256"

RECEIPT_SCHEMA: Final = "arvectum-os.p7-08.discount-parser-reconstruction-receipt"
RECEIPT_SCHEMA_VERSION: Final = "1"
RECEIPT_FILENAME: Final = "p7-08-discount-parser-reconstruction-receipt.json"
RECEIPT_DIGEST_FILENAME: Final = "p7-08-discount-parser-reconstruction-receipt.sha256"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._+-]{1,160}$")

_REQUIRED_MATERIAL_ROLES: Final = frozenset(
    {
        "source-observation",
        "offer",
        "publication-candidate",
        "template-version",
        "publication-reservation",
        "publication-attempt",
        "telegram-target",
        "authorization-evidence",
    }
)
_RULE_CONFIG_ROLES: Final = frozenset({"rule-config", "filter-config"})
_ALLOWED_OPTIONAL_ROLES: Final = frozenset({"parse-run", "source", "rule-config", "filter-config"})

_FORBIDDEN_SECRET_MARKERS: Final = (
    "password=",
    "secret=",
    "token=",
    "api_key=",
    "apikey=",
    "private_key=",
    "bot_token=",
    "bearer ",
)
_FORBIDDEN_IDENTITY_KEYS: Final = frozenset(
    {
        "organization",
        "organization_id",
        "actor",
        "actor_id",
        "principal",
        "principal_id",
        "actual_principal",
        "authenticated_principal",
    }
)


class P708ContourError(ValueError):
    """P7.08 evidence is incomplete, unsafe, inconsistent, or replay-ambiguous."""


def _required_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise P708ContourError(f"{field} must be a non-empty string")
    return value.strip()


def _git_sha(value: Any, *, field: str) -> str:
    value = _required_text(value, field=field).lower()
    if not _GIT_SHA_RE.fullmatch(value):
        raise P708ContourError(f"{field} must be a full lowercase 40-character Git SHA")
    return value


def _sha256(value: Any, *, field: str) -> str:
    value = _required_text(value, field=field).lower()
    if not _SHA256_RE.fullmatch(value):
        raise P708ContourError(f"{field} must be a lowercase SHA-256 digest")
    return value


def _serialize_json(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _file_sha256(path: Path) -> str:
    try:
        return hashlib.sha256(Path(path).expanduser().read_bytes()).hexdigest()
    except OSError as exc:
        raise P708ContourError(f"cannot read evidence file: {path}") from exc


def _read_sidecar(path: Path, *, expected_name: str) -> str:
    try:
        line = Path(path).expanduser().read_text(encoding="utf-8").strip()
        digest, filename = line.split(maxsplit=1)
    except (OSError, ValueError) as exc:
        raise P708ContourError(f"invalid SHA-256 sidecar: {path}") from exc
    digest = _sha256(digest, field="sidecar digest")
    if filename.strip() != expected_name:
        raise P708ContourError("SHA-256 sidecar filename does not match evidence filename")
    return digest


def _verify_file_sidecar(*, file_path: Path, digest_path: Path) -> str:
    file_path = Path(file_path).expanduser()
    actual = _file_sha256(file_path)
    stored = _read_sidecar(Path(digest_path).expanduser(), expected_name=file_path.name)
    if actual != stored:
        raise P708ContourError(f"SHA-256 mismatch for {file_path.name}")
    return actual


def _write_immutable_json(
    *,
    output_dir: Path,
    filename: str,
    digest_filename: str,
    payload: dict[str, Any],
) -> tuple[Path, Path, str]:
    output_dir = Path(output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / filename
    digest_path = output_dir / digest_filename
    if json_path.exists() or digest_path.exists():
        raise P708ContourError(f"immutable evidence already exists in {output_dir}")
    raw = _serialize_json(payload)
    digest = hashlib.sha256(raw).hexdigest()
    with json_path.open("xb") as handle:
        handle.write(raw)
    with digest_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{digest}  {filename}\n")
    if _verify_file_sidecar(file_path=json_path, digest_path=digest_path) != digest:
        raise P708ContourError("read-after-write evidence verification failed")
    return json_path, digest_path, digest


def _load_verified_json(*, json_path: Path, digest_path: Path, expected_filename: str) -> tuple[dict[str, Any], str]:
    json_path = Path(json_path).expanduser()
    if json_path.name != expected_filename:
        raise P708ContourError(f"unexpected evidence filename: {json_path.name}")
    digest = _verify_file_sidecar(file_path=json_path, digest_path=digest_path)
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise P708ContourError(f"invalid JSON evidence: {json_path}") from exc
    if not isinstance(payload, dict):
        raise P708ContourError("evidence JSON root must be an object")
    return payload, digest


def _scan_transfer_value(value: Any, *, path: str = "$") -> None:
    """Fail closed on reusable-secret markers or raw org/actor identity fields."""
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key).strip().lower()
            if key_text in _FORBIDDEN_IDENTITY_KEYS:
                raise P708ContourError(f"raw Organization/Actor identity field is forbidden in transfer evidence: {path}.{key}")
            if any(marker in key_text for marker in ("password", "api_key", "apikey", "private_key", "bot_token", "credential")):
                raise P708ContourError(f"reusable-secret field is forbidden in transfer evidence: {path}.{key}")
            if any(marker in key_text for marker in ("secret", "token")) and child is not False:
                raise P708ContourError(f"reusable-secret field is forbidden in transfer evidence: {path}.{key}")
            _scan_transfer_value(child, path=f"{path}.{key}")
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            _scan_transfer_value(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        lowered = value.lower()
        if any(marker in lowered for marker in _FORBIDDEN_SECRET_MARKERS):
            raise P708ContourError(f"reusable-secret material is forbidden in transfer evidence: {path}")


def _safe_reference(value: Any, *, field: str) -> str:
    value = _required_text(value, field=field)
    if len(value) > 500:
        raise P708ContourError(f"{field} is too long for minimized transfer evidence")
    lowered = value.lower()
    if any(marker in lowered for marker in _FORBIDDEN_SECRET_MARKERS):
        raise P708ContourError(f"{field} contains reusable-secret material")
    return value


def _normalize_material_refs(rows: Any) -> tuple[dict[str, str], ...]:
    if not isinstance(rows, list):
        raise P708ContourError("material_refs must be a list")
    normalized: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"role", "reference"}:
            raise P708ContourError("each material_ref must contain role/reference only")
        role = _required_text(row["role"], field="material_ref role").lower()
        reference = _safe_reference(row["reference"], field=f"material_ref[{role}] reference")
        key = (role, reference)
        if key in seen:
            raise P708ContourError("duplicate material_ref is not permitted")
        seen.add(key)
        normalized.append({"role": role, "reference": reference})
    roles = {item["role"] for item in normalized}
    missing = _REQUIRED_MATERIAL_ROLES - roles
    if missing:
        raise P708ContourError(f"required material reference roles are missing: {sorted(missing)}")
    if not (roles & _RULE_CONFIG_ROLES):
        raise P708ContourError("rule-config or filter-config material reference is required")
    allowed = _REQUIRED_MATERIAL_ROLES | _ALLOWED_OPTIONAL_ROLES
    unknown = roles - allowed
    if unknown:
        raise P708ContourError(f"unsupported material reference roles: {sorted(unknown)}")
    return tuple(normalized)


def _contract_pin_row() -> dict[str, Any]:
    return {
        "version": PRODUCT_CONTRACT_VERSION,
        "blob_sha": P6_06_CANONICAL_BLOB_SHA,
        "lifecycle": "Provisional",
        "shared_dependencies": ["CAP-004"],
    }


def issue_dispatch(
    *,
    runtime_root: Path,
    organization_id: str,
    actor_id: str,
    canonical_repo_sha: str,
    execution_id: str | None = None,
    created_at: datetime | None = None,
) -> dict[str, Any]:
    """Create Mac-private Stage 2A ticket plus minimized Mac->Windows dispatch."""
    canonical_repo_sha = _git_sha(canonical_repo_sha, field="canonical_repo_sha")
    created_at = created_at or datetime.now(timezone.utc)
    ticket = build_stage2a_ticket(
        organization_id=organization_id,
        actor_id=actor_id,
        canonical_repo_sha=canonical_repo_sha,
        created_at=created_at,
        execution_id=execution_id,
    )
    execution_id = _required_text(ticket["execution_id"], field="execution_id")
    if not _SAFE_ID_RE.fullmatch(execution_id) or execution_id in {".", ".."}:
        raise P708ContourError("execution_id contains unsafe or non-portable path characters")

    run_root = Path(runtime_root).expanduser() / "product-contours" / "discount-parser" / "runs" / execution_id
    private_root = run_root / "mac-private"
    outbound_root = run_root / "outbound"
    ticket_path, ticket_digest_path, ticket_digest = write_stage2a_evidence(
        output_dir=private_root,
        ticket=ticket,
    )
    dispatch = {
        "schema": DISPATCH_SCHEMA,
        "schema_version": DISPATCH_SCHEMA_VERSION,
        "execution_id": execution_id,
        "stage2a_ticket_sha256": ticket_digest,
        "product_contract": _contract_pin_row(),
        "canonical_repo": {
            "repository": REPOSITORY_FULL_NAME,
            "ticket_issuer_sha": canonical_repo_sha,
        },
        "cross_host_boundary": {
            "source_host_role": "mac-mini-arvectum-os-owner",
            "destination_host_role": "windows-discount-parser-evidence-owner",
            "organization_identity_transferred": False,
            "actor_identity_transferred": False,
            "reusable_secrets_transferred": False,
            "mutable_shared_state_required": False,
            "max_external_sends": 1,
            "scheduler_autopost_permitted": False,
            "cap004_reconstruction_required": True,
        },
    }
    _scan_transfer_value(dispatch)
    dispatch_path, dispatch_digest_path, dispatch_digest = _write_immutable_json(
        output_dir=outbound_root,
        filename=DISPATCH_FILENAME,
        digest_filename=DISPATCH_DIGEST_FILENAME,
        payload=dispatch,
    )
    return {
        "execution_id": execution_id,
        "run_root": run_root,
        "ticket_path": ticket_path,
        "ticket_digest_path": ticket_digest_path,
        "ticket_sha256": ticket_digest,
        "dispatch_path": dispatch_path,
        "dispatch_digest_path": dispatch_digest_path,
        "dispatch_sha256": dispatch_digest,
    }


def _validate_dispatch(payload: dict[str, Any]) -> None:
    if payload.get("schema") != DISPATCH_SCHEMA or payload.get("schema_version") != DISPATCH_SCHEMA_VERSION:
        raise P708ContourError("dispatch schema mismatch")
    execution_id = _required_text(payload.get("execution_id"), field="dispatch execution_id")
    if not _SAFE_ID_RE.fullmatch(execution_id) or execution_id in {".", ".."}:
        raise P708ContourError("dispatch execution_id is unsafe")
    _sha256(payload.get("stage2a_ticket_sha256"), field="dispatch stage2a_ticket_sha256")
    if payload.get("product_contract") != _contract_pin_row():
        raise P708ContourError("dispatch lost exact P6.06 Product Contract / CAP-004-only pin")
    canonical_repo = payload.get("canonical_repo")
    if not isinstance(canonical_repo, dict) or canonical_repo.get("repository") != REPOSITORY_FULL_NAME:
        raise P708ContourError("dispatch canonical repository mismatch")
    _git_sha(canonical_repo.get("ticket_issuer_sha"), field="dispatch ticket_issuer_sha")
    boundary = payload.get("cross_host_boundary")
    expected = {
        "source_host_role": "mac-mini-arvectum-os-owner",
        "destination_host_role": "windows-discount-parser-evidence-owner",
        "organization_identity_transferred": False,
        "actor_identity_transferred": False,
        "reusable_secrets_transferred": False,
        "mutable_shared_state_required": False,
        "max_external_sends": 1,
        "scheduler_autopost_permitted": False,
        "cap004_reconstruction_required": True,
    }
    if boundary != expected:
        raise P708ContourError("dispatch cross-host safety boundary mismatch")
    _scan_transfer_value(payload)


def _descriptor_fields(descriptor: dict[str, Any]) -> dict[str, Any]:
    expected_top = {
        "schema",
        "schema_version",
        "product",
        "candidate",
        "target_ref",
        "template_version",
        "authorization",
        "containment",
        "pre_effect",
        "outcome",
        "material_refs",
    }
    if set(descriptor) != expected_top:
        raise P708ContourError("descriptor contains missing or unsupported top-level fields")
    if descriptor.get("schema") != DESCRIPTOR_SCHEMA or descriptor.get("schema_version") != DESCRIPTOR_SCHEMA_VERSION:
        raise P708ContourError("descriptor schema mismatch")
    _scan_transfer_value(descriptor)

    product = descriptor.get("product")
    if not isinstance(product, dict) or set(product) != {"repository", "repository_sha"}:
        raise P708ContourError("descriptor product row must contain repository/repository_sha")
    if product.get("repository") != PRODUCT_REPOSITORY:
        raise P708ContourError("descriptor product repository mismatch")
    product_sha = _git_sha(product.get("repository_sha"), field="product repository_sha")

    candidate = descriptor.get("candidate")
    if not isinstance(candidate, dict) or set(candidate) != {"offer_id", "status_before", "text_only"}:
        raise P708ContourError("descriptor candidate row mismatch")
    offer_id = _safe_reference(str(candidate.get("offer_id", "")), field="offer_id")
    if candidate.get("status_before") != "ready" or candidate.get("text_only") is not True:
        raise P708ContourError("only ready text-only bounded publication candidates are admitted")

    target_ref = _safe_reference(descriptor.get("target_ref"), field="target_ref")
    template_version = _safe_reference(descriptor.get("template_version"), field="template_version")

    authorization = descriptor.get("authorization")
    auth_keys = {"type", "received", "authorized_at", "scope_matches_candidate_target", "max_external_sends"}
    if not isinstance(authorization, dict) or set(authorization) != auth_keys:
        raise P708ContourError("descriptor authorization row mismatch")
    if (
        authorization.get("type") != "explicit-human-one-time"
        or authorization.get("received") is not True
        or authorization.get("scope_matches_candidate_target") is not True
        or authorization.get("max_external_sends") != 1
    ):
        raise P708ContourError("exact explicit one-time human authorization evidence is required")
    authorized_at = _required_text(authorization.get("authorized_at"), field="authorized_at")
    try:
        parsed_auth = datetime.fromisoformat(authorized_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise P708ContourError("authorized_at must be an ISO-8601 timestamp") from exc
    if parsed_auth.tzinfo is None or parsed_auth.utcoffset() is None:
        raise P708ContourError("authorized_at must be timezone-aware")

    containment = descriptor.get("containment")
    expected_containment = {
        "scheduler_disabled": True,
        "autopost_disabled": True,
        "other_publishers_running": False,
        "publish_offer_invocations": 1,
        "telegram_send_delegations": 1,
    }
    if not isinstance(containment, dict):
        raise P708ContourError("descriptor containment row is missing")
    if any(containment.get(key) != value for key, value in expected_containment.items()):
        raise P708ContourError("descriptor containment does not prove the one-send bounded path")
    calls = containment.get("telegram_send_message_calls", 0)
    photo_calls = containment.get("telegram_send_photo_calls", 0)
    if calls != 1 or photo_calls != 0:
        raise P708ContourError("the current bounded text-only path requires exactly one send_message call and zero send_photo calls")
    allowed_containment = set(expected_containment) | {"telegram_send_message_calls", "telegram_send_photo_calls"}
    if set(containment) != allowed_containment:
        raise P708ContourError("descriptor containment contains unsupported fields")

    pre_effect = descriptor.get("pre_effect")
    if not isinstance(pre_effect, dict) or set(pre_effect) != {"publication_id", "reservation_status"}:
        raise P708ContourError("descriptor pre_effect row mismatch")
    publication_id = _safe_reference(str(pre_effect.get("publication_id", "")), field="publication_id")
    if pre_effect.get("reservation_status") != "pending":
        raise P708ContourError("pre-effect reservation must be pending before the external effect")

    outcome = descriptor.get("outcome")
    outcome_keys = {
        "publish_result_status",
        "publication_status",
        "offer_status",
        "telegram_message_id",
        "external_confirmation",
        "reconciliation_required",
    }
    if not isinstance(outcome, dict) or set(outcome) != outcome_keys:
        raise P708ContourError("descriptor outcome row mismatch")
    if (
        outcome.get("publish_result_status") != "published"
        or outcome.get("publication_status") != "published"
        or outcome.get("offer_status") != "published"
        or outcome.get("external_confirmation") != "PASS"
        or outcome.get("reconciliation_required") is not False
    ):
        raise P708ContourError("only externally confirmed non-uncertain outcomes may be reconstructed")
    telegram_message_id = _safe_reference(str(outcome.get("telegram_message_id", "")), field="telegram_message_id")
    material_refs = _normalize_material_refs(descriptor.get("material_refs"))
    roles = {item["role"] for item in material_refs}
    if "telegram-target" not in roles or "authorization-evidence" not in roles:
        raise P708ContourError("target and authorization material references are required")

    return {
        "product": {"repository": PRODUCT_REPOSITORY, "repository_sha": product_sha},
        "candidate": {"offer_id": offer_id, "status_before": "ready", "text_only": True},
        "target_ref": target_ref,
        "template_version": template_version,
        "authorization": dict(authorization),
        "containment": dict(containment),
        "pre_effect": {"publication_id": publication_id, "reservation_status": "pending"},
        "outcome": {
            "publish_result_status": "published",
            "publication_status": "published",
            "offer_status": "published",
            "telegram_message_id": telegram_message_id,
            "external_confirmation": "PASS",
            "reconciliation_required": False,
        },
        "material_refs": list(material_refs),
    }


def prepare_windows_handoff(
    *,
    dispatch_path: Path,
    dispatch_digest_path: Path,
    descriptor_path: Path,
    pre_effect_path: Path,
    pre_effect_digest_path: Path,
    outcome_path: Path,
    outcome_digest_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    """Create Windows->Mac minimized transfer while retaining raw evidence on Windows."""
    dispatch, dispatch_digest = _load_verified_json(
        json_path=dispatch_path,
        digest_path=dispatch_digest_path,
        expected_filename=DISPATCH_FILENAME,
    )
    _validate_dispatch(dispatch)
    try:
        descriptor = json.loads(Path(descriptor_path).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise P708ContourError("invalid Windows-local descriptor JSON") from exc
    if not isinstance(descriptor, dict):
        raise P708ContourError("descriptor JSON root must be an object")
    fields = _descriptor_fields(descriptor)

    pre_effect_sha = _verify_file_sidecar(
        file_path=pre_effect_path,
        digest_path=pre_effect_digest_path,
    )
    outcome_sha = _verify_file_sidecar(
        file_path=outcome_path,
        digest_path=outcome_digest_path,
    )
    if pre_effect_sha == outcome_sha:
        raise P708ContourError("pre-effect and outcome evidence must remain distinct")

    handoff = {
        "schema": HANDOFF_SCHEMA,
        "schema_version": HANDOFF_SCHEMA_VERSION,
        "execution_id": dispatch["execution_id"],
        "dispatch_sha256": dispatch_digest,
        "stage2a_ticket_sha256": dispatch["stage2a_ticket_sha256"],
        "product_contract": _contract_pin_row(),
        **fields,
        "pre_effect": {
            **fields["pre_effect"],
            "sha256": pre_effect_sha,
        },
        "outcome": {
            **fields["outcome"],
            "sha256": outcome_sha,
        },
        "data_minimization": {
            "raw_pre_effect_embedded": False,
            "raw_outcome_embedded": False,
            "stage2a_ticket_embedded": False,
            "organization_identity_embedded": False,
            "actor_identity_embedded": False,
            "reusable_secrets_embedded": False,
            "windows_product_database_embedded": False,
        },
        "replay_safety": {
            "external_effect_replay_permitted": False,
            "blind_retry_uncertain_outcome_permitted": False,
            "reconstruction_side_effect_class": "ReadOnly",
        },
    }
    _scan_transfer_value(handoff)
    handoff_path, handoff_digest_path, handoff_digest = _write_immutable_json(
        output_dir=output_dir,
        filename=HANDOFF_FILENAME,
        digest_filename=HANDOFF_DIGEST_FILENAME,
        payload=handoff,
    )
    return {
        "execution_id": dispatch["execution_id"],
        "handoff_path": handoff_path,
        "handoff_digest_path": handoff_digest_path,
        "handoff_sha256": handoff_digest,
        "raw_pre_effect_retained_locally": str(Path(pre_effect_path).expanduser()),
        "raw_outcome_retained_locally": str(Path(outcome_path).expanduser()),
    }


def _load_private_ticket(
    *,
    runtime_root: Path,
    execution_id: str,
    expected_ticket_sha256: str,
) -> tuple[dict[str, Any], OrganizationScope, ActorContext]:
    run_root = Path(runtime_root).expanduser() / "product-contours" / "discount-parser" / "runs" / execution_id
    private_root = run_root / "mac-private"
    ticket_path = private_root / STAGE2A_TICKET_FILENAME
    digest_path = private_root / STAGE2A_DIGEST_FILENAME
    if not verify_stage2a_evidence(ticket_path=ticket_path, digest_path=digest_path):
        raise P708ContourError("Mac-private Stage 2A ticket verification failed")
    actual = ticket_sha256(ticket_path.read_bytes())
    if actual != expected_ticket_sha256:
        raise P708ContourError("returned handoff lost exact Mac-private Stage 2A ticket continuity")
    try:
        ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise P708ContourError("Mac-private Stage 2A ticket cannot be parsed") from exc
    if not isinstance(ticket, dict) or ticket.get("schema") != STAGE2A_TICKET_SCHEMA:
        raise P708ContourError("Mac-private Stage 2A ticket schema mismatch")
    if ticket.get("execution_id") != execution_id:
        raise P708ContourError("Mac-private Stage 2A execution id mismatch")
    contract = ticket.get("product_contract")
    if not isinstance(contract, dict):
        raise P708ContourError("Stage 2A Product Contract evidence is missing")
    if (
        contract.get("version") != PRODUCT_CONTRACT_VERSION
        or contract.get("blob_sha") != P6_06_CANONICAL_BLOB_SHA
        or contract.get("shared_dependencies") != ["CAP-004"]
    ):
        raise P708ContourError("Stage 2A lost P6.06 / CAP-004-only continuity")
    operation = ticket.get("operation")
    if not isinstance(operation, dict) or operation.get("name") != OPERATION_NAME or operation.get("max_external_sends") != 1:
        raise P708ContourError("Stage 2A governed operation continuity mismatch")
    org_row = ticket.get("organization")
    actor_row = ticket.get("actor")
    if not isinstance(org_row, dict) or not isinstance(actor_row, dict):
        raise P708ContourError("Stage 2A Organization/Actor continuity is missing")
    organization_value = _required_text(org_row.get("organization_id"), field="Stage 2A organization_id")
    actor_value = _required_text(actor_row.get("principal_id"), field="Stage 2A principal_id")
    if actor_row.get("kind") != "human" or actor_row.get("attributable") is not True:
        raise P708ContourError("Stage 2A human Actor attribution is not preserved")
    organization = OrganizationScope(Identity("organization", organization_value, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", actor_value, organization_value)),
        organization,
    )
    return ticket, organization, actor


def _validate_handoff(handoff: dict[str, Any]) -> tuple[dict[str, str], ...]:
    if handoff.get("schema") != HANDOFF_SCHEMA or handoff.get("schema_version") != HANDOFF_SCHEMA_VERSION:
        raise P708ContourError("handoff schema mismatch")
    execution_id = _required_text(handoff.get("execution_id"), field="handoff execution_id")
    if not _SAFE_ID_RE.fullmatch(execution_id) or execution_id in {".", ".."}:
        raise P708ContourError("handoff execution_id is unsafe")
    _sha256(handoff.get("dispatch_sha256"), field="handoff dispatch_sha256")
    _sha256(handoff.get("stage2a_ticket_sha256"), field="handoff stage2a_ticket_sha256")
    if handoff.get("product_contract") != _contract_pin_row():
        raise P708ContourError("handoff lost exact P6.06 / CAP-004-only boundary")
    _descriptor_fields(
        {
            "schema": DESCRIPTOR_SCHEMA,
            "schema_version": DESCRIPTOR_SCHEMA_VERSION,
            "product": handoff.get("product"),
            "candidate": handoff.get("candidate"),
            "target_ref": handoff.get("target_ref"),
            "template_version": handoff.get("template_version"),
            "authorization": handoff.get("authorization"),
            "containment": handoff.get("containment"),
            "pre_effect": {
                "publication_id": (handoff.get("pre_effect") or {}).get("publication_id"),
                "reservation_status": (handoff.get("pre_effect") or {}).get("reservation_status"),
            },
            "outcome": {
                key: (handoff.get("outcome") or {}).get(key)
                for key in (
                    "publish_result_status",
                    "publication_status",
                    "offer_status",
                    "telegram_message_id",
                    "external_confirmation",
                    "reconciliation_required",
                )
            },
            "material_refs": handoff.get("material_refs"),
        }
    )
    pre = handoff.get("pre_effect")
    outcome = handoff.get("outcome")
    if not isinstance(pre, dict) or not isinstance(outcome, dict):
        raise P708ContourError("handoff pre_effect/outcome rows are missing")
    _sha256(pre.get("sha256"), field="handoff pre_effect sha256")
    _sha256(outcome.get("sha256"), field="handoff outcome sha256")
    minimization = handoff.get("data_minimization")
    expected_false = {
        "raw_pre_effect_embedded",
        "raw_outcome_embedded",
        "stage2a_ticket_embedded",
        "organization_identity_embedded",
        "actor_identity_embedded",
        "reusable_secrets_embedded",
        "windows_product_database_embedded",
    }
    if not isinstance(minimization, dict) or set(minimization) != expected_false or any(minimization[key] is not False for key in expected_false):
        raise P708ContourError("handoff data-minimization declaration mismatch")
    replay = handoff.get("replay_safety")
    if replay != {
        "external_effect_replay_permitted": False,
        "blind_retry_uncertain_outcome_permitted": False,
        "reconstruction_side_effect_class": "ReadOnly",
    }:
        raise P708ContourError("handoff replay-safety declaration mismatch")
    _scan_transfer_value(handoff)
    return _normalize_material_refs(handoff.get("material_refs"))


def _pin(
    *,
    role: str,
    subject_value: str,
    version_value: str,
    semantic_type: str,
    scope: str,
    authority_scope: str,
    lifecycle_status: str,
) -> GovernedVersionPin:
    return GovernedVersionPin(
        Identity(f"{role}-subject", subject_value, scope),
        Identity(f"{role}-version", version_value, scope),
        semantic_type,
        authority_scope,
        lifecycle_status,
    )


def _material_ref_pin(*, role: str, reference: str, scope: str) -> GovernedVersionPin:
    digest = hashlib.sha256(f"{role}\0{reference}".encode("utf-8")).hexdigest()
    semantic_by_role = {
        "parse-run": "discount-parser.parse-run-ref",
        "source": "discount-parser.source-ref",
        "source-observation": "discount-parser.source-observation-ref",
        "offer": "discount-parser.offer-ref",
        "publication-candidate": "discount-parser.publication-candidate-ref",
        "rule-config": "discount-parser.rule-config-ref",
        "filter-config": "discount-parser.rule-config-ref",
        "template-version": "discount-parser.template-version-ref",
        "publication-reservation": "discount-parser.publication-attempt-ref",
        "publication-attempt": "discount-parser.publication-attempt-ref",
        "telegram-target": "discount-parser.telegram-message-ref",
        "authorization-evidence": "discount-parser.authorization-evidence-ref",
    }
    return _pin(
        role=role,
        subject_value=f"p7-08-{role}-{digest[:16]}",
        version_value=f"sha256-{digest}",
        semantic_type=semantic_by_role[role],
        scope=scope,
        authority_scope="external-reference/telegram-channel" if role == "telegram-target" else "product-local-reference",
        lifecycle_status="RetainedReference",
    )


def _build_manifest(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    contract: Any,
    handoff: dict[str, Any],
    handoff_digest: str,
    material_refs: tuple[dict[str, str], ...],
) -> tuple[ReconstructionManifest, tuple[tuple[Identity, str, tuple[str, ...], str], ...]]:
    scope = organization.organization_id.value
    product_sha = handoff["product"]["repository_sha"]
    template_version = handoff["template_version"]
    execution_id = handoff["execution_id"]
    ticket_sha = handoff["stage2a_ticket_sha256"]
    pre_sha = handoff["pre_effect"]["sha256"]
    outcome_sha = handoff["outcome"]["sha256"]
    publication_id = str(handoff["pre_effect"]["publication_id"])
    target_ref = handoff["target_ref"]
    message_id = str(handoff["outcome"]["telegram_message_id"])

    workflow = _pin(
        role="workflow",
        subject_value="controlled-telegram-publication",
        version_value=f"product-{product_sha}-template-{template_version}",
        semantic_type="discount-parser.controlled-publication-workflow-ref",
        scope=scope,
        authority_scope="product-local-reference",
        lifecycle_status="Applied",
    )
    ticket_pin = _pin(
        role="stage2a-ticket",
        subject_value=f"p7-08-ticket-{execution_id}",
        version_value=f"sha256-{ticket_sha}",
        semantic_type="platform.execution-handoff-evidence-ref",
        scope=scope,
        authority_scope="owner-local-evidence/reference",
        lifecycle_status="Verified",
    )
    handoff_pin = _pin(
        role="cross-host-handoff",
        subject_value=f"p7-08-handoff-{execution_id}",
        version_value=f"sha256-{handoff_digest}",
        semantic_type="platform.cross-host-evidence-ref",
        scope=scope,
        authority_scope="owner-controlled-transfer/reference",
        lifecycle_status="Verified",
    )
    pre_effect = _pin(
        role="pre-effect-evidence",
        subject_value=f"p7-08-pre-effect-{publication_id}",
        version_value=f"sha256-{pre_sha}",
        semantic_type="platform.execution-evidence-ref",
        scope=scope,
        authority_scope="owner-local-evidence/reference",
        lifecycle_status="Verified",
    )
    product_material = tuple(
        _material_ref_pin(role=item["role"], reference=item["reference"], scope=scope)
        for item in material_refs
    )
    material_inputs = (ticket_pin, handoff_pin, pre_effect, *product_material)

    execution = _pin(
        role="execution",
        subject_value=execution_id,
        version_value=f"{execution_id}-outcome-{outcome_sha}",
        semantic_type="platform.execution-context-ref",
        scope=scope,
        authority_scope="platform.execution-history/reference",
        lifecycle_status="CompletedObserved",
    )
    outcome = _pin(
        role="publication-outcome",
        subject_value=f"publication-{publication_id}",
        version_value=f"sha256-{outcome_sha}",
        semantic_type="discount-parser.publication-outcome-ref",
        scope=scope,
        authority_scope="product-local-reference",
        lifecycle_status="Published",
    )
    telegram_message = _pin(
        role="telegram-message",
        subject_value=f"{target_ref}/message/{message_id}",
        version_value=f"message-{message_id}-confirmed",
        semantic_type="discount-parser.telegram-message-ref",
        scope=scope,
        authority_scope="external-reference/telegram-message",
        lifecycle_status="ExternallyConfirmed",
    )
    reconstruction_observation = _pin(
        role="reconstruction-observation",
        subject_value=f"p7-08-reconstruction-{execution_id}",
        version_value=f"handoff-{handoff_digest}-outcome-{outcome_sha}",
        semantic_type="platform.event-ref",
        scope=scope,
        authority_scope="derived-reconstruction/reference",
        lifecycle_status="DerivedForReconstruction",
    )

    attempts = tuple(
        pin for pin in product_material
        if pin.semantic_type == "discount-parser.publication-attempt-ref"
    )
    if not attempts:
        raise P708ContourError("publication-attempt reference is required for correlation")
    attempt_subject = attempts[-1].subject_id

    provenance_refs = tuple(
        dict.fromkeys(
            (
                actor.actual_principal.principal_id,
                execution.subject_id,
                ticket_pin.version_id,
                handoff_pin.version_id,
                pre_effect.version_id,
                outcome.version_id,
                telegram_message.version_id,
                reconstruction_observation.version_id,
            )
        )
    )
    manifest = ReconstructionManifest(
        organization=organization,
        execution_subject_id=execution.subject_id,
        initiating_actor_id=actor.actual_principal.principal_id,
        operation_name=OPERATION_NAME,
        workflow=workflow,
        material_inputs=material_inputs,
        product_contract=contract.version_pin,
        gate_decisions=(),
        execution_versions=(execution,),
        results=(outcome, telegram_message),
        events=(reconstruction_observation,),
        event_types=(("discount-parser.p7-08-reconstruction-observation", "1"),),
        correlation_refs=(execution.subject_id, attempt_subject),
        causation_refs=(pre_effect.version_id, outcome.version_id),
        provenance_refs=provenance_refs,
    )

    by_version: dict[Identity, GovernedVersionPin] = {}
    for pin in (
        workflow,
        *material_inputs,
        contract.version_pin,
        execution,
        outcome,
        telegram_message,
        reconstruction_observation,
    ):
        prior = by_version.get(pin.version_id)
        if prior is None:
            by_version[pin.version_id] = pin
        elif prior != pin:
            raise P708ContourError("one Version Identity is reused with conflicting semantics")
    constraints = tuple((version_id, PURPOSE, ("read",), CLASSIFICATION) for version_id in by_version)
    return manifest, constraints


def _load_local_dispatch(*, runtime_root: Path, execution_id: str) -> tuple[dict[str, Any], str]:
    dispatch_root = (
        Path(runtime_root).expanduser()
        / "product-contours"
        / "discount-parser"
        / "runs"
        / execution_id
        / "outbound"
    )
    payload, digest = _load_verified_json(
        json_path=dispatch_root / DISPATCH_FILENAME,
        digest_path=dispatch_root / DISPATCH_DIGEST_FILENAME,
        expected_filename=DISPATCH_FILENAME,
    )
    _validate_dispatch(payload)
    if payload.get("execution_id") != execution_id:
        raise P708ContourError("local dispatch execution continuity mismatch")
    return payload, digest


def reconstruct_on_mac(
    *,
    runtime_root: Path,
    handoff_path: Path,
    handoff_digest_path: Path,
    canonical_repo_sha: str,
) -> dict[str, Any]:
    """Verify returned evidence and reconstruct once through CAP-004 on Mac mini."""
    canonical_repo_sha = _git_sha(canonical_repo_sha, field="canonical_repo_sha")
    handoff, handoff_digest = _load_verified_json(
        json_path=handoff_path,
        digest_path=handoff_digest_path,
        expected_filename=HANDOFF_FILENAME,
    )
    material_refs = _validate_handoff(handoff)
    execution_id = handoff["execution_id"]

    local_dispatch, local_dispatch_digest = _load_local_dispatch(
        runtime_root=runtime_root,
        execution_id=execution_id,
    )
    if handoff["dispatch_sha256"] != local_dispatch_digest:
        raise P708ContourError("returned handoff does not bind the exact locally issued dispatch")
    if local_dispatch["stage2a_ticket_sha256"] != handoff["stage2a_ticket_sha256"]:
        raise P708ContourError("returned handoff changed Stage 2A ticket continuity")

    run_root = (
        Path(runtime_root).expanduser()
        / "product-contours"
        / "discount-parser"
        / "runs"
        / execution_id
    )
    reconstruction_root = run_root / "reconstruction"
    receipt_path = reconstruction_root / RECEIPT_FILENAME
    receipt_digest_path = reconstruction_root / RECEIPT_DIGEST_FILENAME
    if receipt_path.exists() or receipt_digest_path.exists():
        if not (receipt_path.exists() and receipt_digest_path.exists()):
            raise P708ContourError("partial reconstruction receipt exists; operator reconciliation required")
        receipt, _ = _load_verified_json(
            json_path=receipt_path,
            digest_path=receipt_digest_path,
            expected_filename=RECEIPT_FILENAME,
        )
        if receipt.get("handoff_sha256") != handoff_digest:
            raise P708ContourError("execution already reconstructed from different evidence; refusing ambiguous replay")
        return {
            "status": "ALREADY_RECONSTRUCTED",
            "execution_id": execution_id,
            "report_path": reconstruction_root / REPORT_FILENAME,
            "report_digest_path": reconstruction_root / REPORT_DIGEST_FILENAME,
            "receipt_path": receipt_path,
            "receipt_digest_path": receipt_digest_path,
        }

    ticket, organization, actor = _load_private_ticket(
        runtime_root=runtime_root,
        execution_id=execution_id,
        expected_ticket_sha256=handoff["stage2a_ticket_sha256"],
    )
    try:
        created_at = datetime.fromisoformat(str(ticket["created_at"]).replace("Z", "+00:00"))
    except (KeyError, ValueError, TypeError) as exc:
        raise P708ContourError("Stage 2A created_at is invalid") from exc
    contract = build_p6_06_product_contract_projection(actor=actor, created_at=created_at)
    if contract.version_pin.version_id.value != PRODUCT_CONTRACT_VERSION_ID:
        raise P708ContourError("executable Product Contract projection lost exact v0.1.0 Version Identity")
    if {item.dependency_id for item in contract.dependencies} != {CAP_004_AUDIT_RECONSTRUCTION}:
        raise P708ContourError("executable Product Contract expanded beyond CAP-004")

    governance_reference = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"
    governed_versions = (
        GovernedDependencyVersionEvidence(
            CAP_004_AUDIT_RECONSTRUCTION,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            governance_reference,
        ),
    )
    adapters = compose_integration_adapters(
        contract=contract,
        actor=actor,
        effective_product_contract=contract.version_pin,
        governed_versions=governed_versions,
    )
    request = CapabilityConsumptionRequest(
        organization=organization,
        product_id=contract.product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RECONSTRUCT_EXECUTION,
        access=AccessRequest(actor, PURPOSE, "read", (CLASSIFICATION,)),
    )
    manifest, constraints = _build_manifest(
        organization=organization,
        actor=actor,
        contract=contract,
        handoff=handoff,
        handoff_digest=handoff_digest,
        material_refs=material_refs,
    )
    reconstruction = reconstruct_publication(
        adapters=adapters,
        request=request,
        governed_versions=governed_versions,
        manifest=manifest,
        evidence_constraints=constraints,
    )
    if not reconstruction.complete:
        raise P708ContourError("CAP-004 reconstruction is incomplete")
    if reconstruction.organization != organization:
        raise P708ContourError("reconstruction lost exact Organization continuity")
    if reconstruction.initiating_actor_id != actor.actual_principal.principal_id:
        raise P708ContourError("reconstruction lost exact human Actor continuity")
    if manifest.product_contract != contract.version_pin:
        raise P708ContourError("reconstruction lost exact Product Contract continuity")
    if manifest.gate_decisions:
        raise P708ContourError("reconstruction must not fabricate a retroactive platform gate decision")

    report = {
        "schema": REPORT_SCHEMA,
        "schema_version": REPORT_SCHEMA_VERSION,
        "status": "PASS",
        "scope": "Persistent Internal / owner-operated",
        "execution_id": execution_id,
        "canonical_repo": {
            "repository": REPOSITORY_FULL_NAME,
            "reconstruction_sha": canonical_repo_sha,
            "ticket_issuer_sha": local_dispatch["canonical_repo"]["ticket_issuer_sha"],
        },
        "continuity": {
            "dispatch_sha256": local_dispatch_digest,
            "handoff_sha256": handoff_digest,
            "stage2a_ticket_sha256": handoff["stage2a_ticket_sha256"],
            "organization_continuity": "PASS",
            "actor_continuity": "PASS",
            "product_contract_version": PRODUCT_CONTRACT_VERSION,
            "product_contract_blob_sha": P6_06_CANONICAL_BLOB_SHA,
            "product_contract_continuity": "PASS",
            "shared_dependencies": ["CAP-004"],
        },
        "product_evidence": {
            "repository": PRODUCT_REPOSITORY,
            "repository_sha": handoff["product"]["repository_sha"],
            "offer_id": handoff["candidate"]["offer_id"],
            "publication_id": handoff["pre_effect"]["publication_id"],
            "target_ref": handoff["target_ref"],
            "template_version": handoff["template_version"],
            "pre_effect_sha256": handoff["pre_effect"]["sha256"],
            "outcome_sha256": handoff["outcome"]["sha256"],
            "telegram_message_id": handoff["outcome"]["telegram_message_id"],
            "external_confirmation": "PASS",
            "material_reference_roles": sorted({item["role"] for item in material_refs}),
            "material_reference_count": len(material_refs),
        },
        "cap004": {
            "dependency": "CAP-004",
            "provider_contract_version": CAPABILITY_CONTRACT_VERSION,
            "operation": OP_RECONSTRUCT_EXECUTION,
            "read_only": True,
            "reconstruction_complete": True,
            "evidence_item_count": len(reconstruction.evidence),
            "evidence_roles": [item.role for item in reconstruction.evidence],
            "gate_decisions_fabricated": False,
            "derived_observation_is_canonical_event": False,
        },
        "cross_host": {
            "transport_contract_created": False,
            "mutable_shared_state_required": False,
            "raw_windows_evidence_transferred": False,
            "mac_private_ticket_transferred": False,
            "organization_identity_transferred": False,
            "actor_identity_transferred": False,
            "reusable_secrets_transferred": False,
        },
        "containment": {
            "network_calls": 0,
            "telegram_calls": 0,
            "discount_parser_publish_calls": 0,
            "product_database_mutations": 0,
            "external_mutations": 0,
            "canonical_state_mutations": 0,
            "telegram_effect_replayed": False,
        },
        "data_minimization": {
            "raw_stage2a_organization_identity_written": False,
            "raw_stage2a_actor_identity_written": False,
            "raw_windows_pre_effect_written": False,
            "raw_windows_outcome_written": False,
            "reusable_secrets_written": False,
        },
    }
    report_path, report_digest_path, report_digest = _write_immutable_json(
        output_dir=reconstruction_root,
        filename=REPORT_FILENAME,
        digest_filename=REPORT_DIGEST_FILENAME,
        payload=report,
    )
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "classification": "non-canonical operational evidence",
        "execution_id": execution_id,
        "handoff_sha256": handoff_digest,
        "report_sha256": report_digest,
        "reconstruction_complete": True,
        "external_effect_replayed": False,
        "new_authorization_consumed": False,
    }
    receipt_path, receipt_digest_path, receipt_digest = _write_immutable_json(
        output_dir=reconstruction_root,
        filename=RECEIPT_FILENAME,
        digest_filename=RECEIPT_DIGEST_FILENAME,
        payload=receipt,
    )
    return {
        "status": "PASS",
        "execution_id": execution_id,
        "report_path": report_path,
        "report_digest_path": report_digest_path,
        "report_sha256": report_digest,
        "receipt_path": receipt_path,
        "receipt_digest_path": receipt_digest_path,
        "receipt_sha256": receipt_digest,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P7.08 persistent Discount Parser Windows <-> Mac mini contour")
    sub = parser.add_subparsers(dest="command", required=True)

    issue = sub.add_parser("issue", help="Mac mini: create private Stage 2A ticket and minimized Windows dispatch")
    issue.add_argument("--runtime-root", required=True, type=Path)
    issue.add_argument("--organization-id", required=True)
    issue.add_argument("--actor-id", required=True)
    issue.add_argument("--canonical-repo-sha", required=True)
    issue.add_argument("--execution-id")

    handoff = sub.add_parser("handoff", help="Windows: create minimized evidence handoff from local evidence")
    handoff.add_argument("--dispatch", required=True, type=Path)
    handoff.add_argument("--dispatch-digest", required=True, type=Path)
    handoff.add_argument("--descriptor", required=True, type=Path)
    handoff.add_argument("--pre-effect", required=True, type=Path)
    handoff.add_argument("--pre-effect-digest", required=True, type=Path)
    handoff.add_argument("--outcome", required=True, type=Path)
    handoff.add_argument("--outcome-digest", required=True, type=Path)
    handoff.add_argument("--output-dir", required=True, type=Path)

    reconstruct = sub.add_parser("reconstruct", help="Mac mini: verify and reconstruct returned handoff through CAP-004")
    reconstruct.add_argument("--runtime-root", required=True, type=Path)
    reconstruct.add_argument("--handoff", required=True, type=Path)
    reconstruct.add_argument("--handoff-digest", required=True, type=Path)
    reconstruct.add_argument("--canonical-repo-sha", required=True)
    return parser


def _print_result(result: dict[str, Any]) -> None:
    for key, value in result.items():
        print(f"P7_08_{key.upper()}={value}")


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "issue":
            result = issue_dispatch(
                runtime_root=args.runtime_root,
                organization_id=args.organization_id,
                actor_id=args.actor_id,
                canonical_repo_sha=args.canonical_repo_sha,
                execution_id=args.execution_id,
            )
        elif args.command == "handoff":
            result = prepare_windows_handoff(
                dispatch_path=args.dispatch,
                dispatch_digest_path=args.dispatch_digest,
                descriptor_path=args.descriptor,
                pre_effect_path=args.pre_effect,
                pre_effect_digest_path=args.pre_effect_digest,
                outcome_path=args.outcome,
                outcome_digest_path=args.outcome_digest,
                output_dir=args.output_dir,
            )
        else:
            result = reconstruct_on_mac(
                runtime_root=args.runtime_root,
                handoff_path=args.handoff,
                handoff_digest_path=args.handoff_digest,
                canonical_repo_sha=args.canonical_repo_sha,
            )
    except (OSError, P708ContourError, ValueError) as exc:
        print("P7_08_RESULT=FAIL")
        print(f"P7_08_ERROR={exc}")
        return 2
    _print_result(result)
    print("P7_08_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
