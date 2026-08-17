"""P6.07 Stage 2C — real Stage 2B evidence admission and CAP-004 reconstruction.

This task-specific internal/provisional harness has two deliberately separated
local steps:

1. On the Windows evidence owner host, create a minimized non-secret Stage 2B
   handoff bound to the already verified pre-effect/outcome SHA-256 digests.
2. On the Mac mini Arvectum OS host, verify the original Stage 2A ticket plus
   the minimized Stage 2B handoff and reconstruct the confirmed publication
   through the existing CAP-004 integration seam.

The module never calls Telegram, never invokes Discount Parser publication,
never mutates the product database and never replays the external effect.  Raw
Stage 2B JSON evidence remains owner-local on Windows.  Identity values loaded
from the Stage 2A ticket are used only in-memory to preserve exact Organization
and human Actor continuity; they are not written into the Stage 2C report.

The handoff/report wire shapes below are P6.07-local evidence formats.  They are
not public APIs, Stable Product Contracts or new platform capability semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Final

from arvectum_os_ref.audit_reconstruction_support import AuditReconstructionView
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
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

from .contract import (
    P6_06_CANONICAL_BLOB_SHA,
    PRODUCT_COMPATIBILITY_LINE,
    PRODUCT_CONTRACT_VERSION,
    build_p6_06_product_contract_projection,
)
from .journey import reconstruct_publication
from .stage2a import (
    DIGEST_FILENAME as STAGE2A_DIGEST_FILENAME,
    OPERATION_NAME,
    TICKET_FILENAME as STAGE2A_TICKET_FILENAME,
    TICKET_SCHEMA as STAGE2A_TICKET_SCHEMA,
    ticket_sha256,
    verify_stage2a_evidence,
)


PURPOSE: Final = "controlled-publication-reconstruction"
CLASSIFICATION: Final = "internal"
REPOSITORY_FULL_NAME: Final = "arvectum/arvectum-os"

EXPECTED_EXECUTION_ID: Final = "p6-07-stage2-4a3b9656-19ca-486d-ab67-aca63027d126"
EXPECTED_STAGE2A_TICKET_SHA256: Final = "d01c6a5d5d7580fa91b67e07c6bd662a96c82d9e1d7c56862a4760e83f54dab7"

STAGE2B_REVIEW_PATH: Final = "docs/reviews/P6-07-stage-2b-real-windows-manual-publication.md"
STAGE2B_REVIEW_BLOB_SHA: Final = "4b2cfa04ce92d3a8978cfd41f790358936925014"
STAGE2B_CLOSURE_COMMIT: Final = "725aeef0bb13376c9045da26a30401947e12d0ed"
STAGE2B_PRODUCT_REPOSITORY: Final = "arvectum/discount-parser"
STAGE2B_PRODUCT_SHA: Final = "b6ba4e0808d640e938bdd53eb1cf87b2416cca10"
STAGE2B_OFFER_ID: Final = "148"
STAGE2B_PUBLICATION_ID: Final = "14"
STAGE2B_TARGET_REF: Final = "@arvectumtest"
STAGE2B_TEMPLATE_VERSION: Final = "v2-configurable"
STAGE2B_AUTHORIZATION_TYPE: Final = "explicit-human-one-time"
STAGE2B_AUTHORIZED_AT: Final = "2026-08-17T11:07:09Z"
STAGE2B_TELEGRAM_MESSAGE_ID: Final = "27"
STAGE2B_PRE_EFFECT_SHA256: Final = "d46ea827fd8785c10c8e76b6523e71063568a650a6dd1ecc7c3a71c7e49593b4"
STAGE2B_OUTCOME_SHA256: Final = "6aefce1a0e26a51af26fbe73de7a0b577d11258b48759be50331460b11e2700a"

STAGE2B_HANDOFF_SCHEMA: Final = "arvectum-os.p6-07-stage2c-stage2b-handoff"
STAGE2B_HANDOFF_SCHEMA_VERSION: Final = "1"
STAGE2B_HANDOFF_FILENAME: Final = "p6-07-stage2b-minimized-handoff.json"
STAGE2B_HANDOFF_DIGEST_FILENAME: Final = "p6-07-stage2b-minimized-handoff.sha256"

STAGE2C_REPORT_SCHEMA: Final = "arvectum-os.p6-07-stage2c-cap004-reconstruction"
STAGE2C_REPORT_SCHEMA_VERSION: Final = "1"
STAGE2C_REPORT_FILENAME: Final = "p6-07-stage2c-reconstruction.json"
STAGE2C_REPORT_DIGEST_FILENAME: Final = "p6-07-stage2c-reconstruction.sha256"

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")

# P6.06 requires these product-owned semantic reference groups to remain
# reconstructable.  Either rule-config or filter-config satisfies the material
# publication-rule/config group; both may be supplied.
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


class Stage2CError(ValueError):
    """P6.07 Stage 2C evidence is incomplete, inconsistent or unsafe to reconstruct."""


@dataclass(frozen=True, slots=True)
class Stage2CReconstructionResult:
    organization: OrganizationScope
    actor: ActorContext
    adapters: IntegrationAdapters
    manifest: ReconstructionManifest
    reconstruction: AuditReconstructionView
    report: dict[str, Any]


def _required_text(value: Any, *, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise Stage2CError(f"{field} must be a non-empty string")
    return value.strip()


def _sha256_bytes(payload: bytes) -> str:
    if not isinstance(payload, bytes):
        raise Stage2CError("SHA-256 input must be bytes")
    return hashlib.sha256(payload).hexdigest()


def _sha256_file(path: Path) -> str:
    path = Path(path).expanduser()
    try:
        return _sha256_bytes(path.read_bytes())
    except OSError as exc:
        raise Stage2CError(f"cannot read evidence file: {path}") from exc


def _serialize_json(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def _parse_sidecar(path: Path, *, expected_name: str) -> str:
    path = Path(path).expanduser()
    try:
        line = path.read_text(encoding="utf-8").strip()
        digest, filename = line.split(maxsplit=1)
    except (OSError, ValueError) as exc:
        raise Stage2CError(f"invalid SHA-256 sidecar: {path}") from exc
    digest = digest.lower()
    if not _SHA256_RE.fullmatch(digest):
        raise Stage2CError("SHA-256 sidecar digest must be 64 lowercase hex characters")
    if filename.strip() != expected_name:
        raise Stage2CError("SHA-256 sidecar filename does not match the expected evidence file")
    return digest


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
        raise Stage2CError("evidence already exists; refusing to overwrite immutable local evidence")

    raw = _serialize_json(payload)
    digest = _sha256_bytes(raw)
    with json_path.open("xb") as handle:
        handle.write(raw)
    with digest_path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{digest}  {filename}\n")

    if _sha256_file(json_path) != digest:
        raise Stage2CError("evidence read-back digest mismatch after write")
    if _parse_sidecar(digest_path, expected_name=filename) != digest:
        raise Stage2CError("evidence sidecar read-back mismatch after write")
    return json_path, digest_path, digest


def _normalize_material_refs(rows: tuple[str, ...]) -> tuple[dict[str, str], ...]:
    normalized: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw in rows:
        raw = _required_text(raw, field="material_ref")
        if "=" not in raw:
            raise Stage2CError("material_ref must use role=reference syntax")
        role, reference = raw.split("=", 1)
        role = _required_text(role, field="material_ref role").lower()
        reference = _required_text(reference, field="material_ref reference")
        forbidden = ("token", "password", "secret", "api_key", "private_key")
        if any(term in role.lower() or term in reference.lower() for term in forbidden):
            raise Stage2CError("material_ref must not contain reusable-secret material")
        key = (role, reference)
        if key in seen:
            raise Stage2CError("duplicate material_ref is not permitted")
        seen.add(key)
        normalized.append({"role": role, "reference": reference})

    roles = {item["role"] for item in normalized}
    missing = _REQUIRED_MATERIAL_ROLES - roles
    if missing:
        raise Stage2CError(f"required Stage 2B material reference roles are missing: {sorted(missing)}")
    if not (roles & _RULE_CONFIG_ROLES):
        raise Stage2CError("one material publication rule/filter configuration reference is required")
    allowed = _REQUIRED_MATERIAL_ROLES | _ALLOWED_OPTIONAL_ROLES
    unknown = roles - allowed
    if unknown:
        raise Stage2CError(f"unsupported Stage 2B material reference roles: {sorted(unknown)}")
    return tuple(normalized)


def build_stage2b_minimized_handoff(
    *,
    pre_effect_path: Path,
    outcome_path: Path,
    material_refs: tuple[str, ...],
    expected_pre_effect_sha256: str = STAGE2B_PRE_EFFECT_SHA256,
    expected_outcome_sha256: str = STAGE2B_OUTCOME_SHA256,
) -> dict[str, Any]:
    """Build a non-secret handoff while treating raw Windows evidence as opaque bytes.

    The raw JSON is deliberately not parsed or copied.  Its independently known
    SHA-256 digest binds this minimized handoff to the retained source evidence.
    ``material_refs`` must be stable, non-secret references inspected locally by
    the evidence owner; they are transferred only as minimized references.
    """

    expected_pre_effect_sha256 = _required_text(
        expected_pre_effect_sha256, field="expected_pre_effect_sha256"
    ).lower()
    expected_outcome_sha256 = _required_text(
        expected_outcome_sha256, field="expected_outcome_sha256"
    ).lower()
    if not _SHA256_RE.fullmatch(expected_pre_effect_sha256) or not _SHA256_RE.fullmatch(
        expected_outcome_sha256
    ):
        raise Stage2CError("expected Stage 2B evidence digests must be SHA-256 values")

    actual_pre = _sha256_file(pre_effect_path)
    actual_out = _sha256_file(outcome_path)
    if actual_pre != expected_pre_effect_sha256:
        raise Stage2CError("pre-effect evidence digest does not match canonical Stage 2B evidence")
    if actual_out != expected_outcome_sha256:
        raise Stage2CError("outcome evidence digest does not match canonical Stage 2B evidence")
    if actual_pre == actual_out:
        raise Stage2CError("pre-effect and outcome evidence must remain distinct")

    refs = _normalize_material_refs(material_refs)
    return {
        "schema": STAGE2B_HANDOFF_SCHEMA,
        "schema_version": STAGE2B_HANDOFF_SCHEMA_VERSION,
        "execution_id": EXPECTED_EXECUTION_ID,
        "stage2a_ticket_sha256": EXPECTED_STAGE2A_TICKET_SHA256,
        "product_contract": {
            "version": PRODUCT_CONTRACT_VERSION,
            "blob_sha": P6_06_CANONICAL_BLOB_SHA,
        },
        "canonical_stage2b_review": {
            "path": STAGE2B_REVIEW_PATH,
            "blob_sha": STAGE2B_REVIEW_BLOB_SHA,
            "closure_commit": STAGE2B_CLOSURE_COMMIT,
        },
        "product": {
            "repository": STAGE2B_PRODUCT_REPOSITORY,
            "repository_sha": STAGE2B_PRODUCT_SHA,
        },
        "candidate": {
            "offer_id": STAGE2B_OFFER_ID,
            "status_before": "ready",
            "text_only": True,
        },
        "target_ref": STAGE2B_TARGET_REF,
        "template_version": STAGE2B_TEMPLATE_VERSION,
        "authorization": {
            "type": STAGE2B_AUTHORIZATION_TYPE,
            "received": True,
            "authorized_at": STAGE2B_AUTHORIZED_AT,
            "scope_matches_candidate_target": True,
            "max_external_sends": 1,
        },
        "containment": {
            "scheduler_disabled": True,
            "autopost_disabled": True,
            "other_publishers_running": False,
            "publish_offer_invocations": 1,
            "telegram_send_delegations": 1,
            "telegram_send_message_calls": 1,
            "telegram_send_photo_calls": 0,
        },
        "pre_effect": {
            "sha256": actual_pre,
            "publication_id": STAGE2B_PUBLICATION_ID,
            "reservation_status": "pending",
        },
        "outcome": {
            "sha256": actual_out,
            "publish_result_status": "published",
            "publication_status": "published",
            "offer_status": "published",
            "telegram_message_id": STAGE2B_TELEGRAM_MESSAGE_ID,
            "external_confirmation": "PASS",
            "reconciliation_required": False,
        },
        "material_refs": list(refs),
        "data_minimization": {
            "raw_pre_effect_embedded": False,
            "raw_outcome_embedded": False,
            "reusable_secrets_embedded": False,
            "raw_opaque_organization_identity_embedded": False,
            "raw_opaque_actor_identity_embedded": False,
        },
    }


def write_stage2b_minimized_handoff(*, output_dir: Path, handoff: dict[str, Any]) -> tuple[Path, Path, str]:
    return _write_immutable_json(
        output_dir=output_dir,
        filename=STAGE2B_HANDOFF_FILENAME,
        digest_filename=STAGE2B_HANDOFF_DIGEST_FILENAME,
        payload=handoff,
    )


def _load_verified_json(*, json_path: Path, digest_path: Path, expected_filename: str) -> dict[str, Any]:
    json_path = Path(json_path).expanduser()
    actual = _sha256_file(json_path)
    stored = _parse_sidecar(Path(digest_path).expanduser(), expected_name=expected_filename)
    if actual != stored:
        raise Stage2CError(f"{expected_filename} SHA-256 sidecar does not match file bytes")
    try:
        payload = json.loads(json_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Stage2CError(f"invalid JSON evidence: {json_path}") from exc
    if not isinstance(payload, dict):
        raise Stage2CError("evidence JSON root must be an object")
    return payload


def _load_stage2a_context(*, ticket_path: Path, digest_path: Path) -> tuple[dict[str, Any], OrganizationScope, ActorContext]:
    ticket_path = Path(ticket_path).expanduser()
    digest_path = Path(digest_path).expanduser()
    if ticket_path.name != STAGE2A_TICKET_FILENAME or digest_path.name != STAGE2A_DIGEST_FILENAME:
        raise Stage2CError("Stage 2A ticket/digest filenames do not match the canonical handoff")
    if not verify_stage2a_evidence(ticket_path=ticket_path, digest_path=digest_path):
        raise Stage2CError("Stage 2A ticket SHA-256 verification failed")
    actual_ticket_sha = ticket_sha256(ticket_path.read_bytes())
    if actual_ticket_sha != EXPECTED_STAGE2A_TICKET_SHA256:
        raise Stage2CError("Stage 2A ticket does not match the exact real Stage 2 execution")

    try:
        ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Stage2CError("Stage 2A ticket JSON cannot be parsed") from exc
    if not isinstance(ticket, dict) or ticket.get("schema") != STAGE2A_TICKET_SCHEMA:
        raise Stage2CError("Stage 2A ticket schema mismatch")
    if ticket.get("execution_id") != EXPECTED_EXECUTION_ID:
        raise Stage2CError("Stage 2A execution id mismatch")

    contract = ticket.get("product_contract")
    if not isinstance(contract, dict):
        raise Stage2CError("Stage 2A Product Contract evidence is missing")
    if contract.get("version") != PRODUCT_CONTRACT_VERSION or contract.get("blob_sha") != P6_06_CANONICAL_BLOB_SHA:
        raise Stage2CError("Stage 2A Product Contract pin mismatch")
    if contract.get("shared_dependencies") != ["CAP-004"]:
        raise Stage2CError("Stage 2A must preserve the CAP-004-only dependency boundary")

    operation = ticket.get("operation")
    if not isinstance(operation, dict) or operation.get("name") != OPERATION_NAME:
        raise Stage2CError("Stage 2A operation continuity mismatch")
    if operation.get("max_external_sends") != 1:
        raise Stage2CError("Stage 2A max external sends continuity mismatch")

    stage2c = ticket.get("stage2c_handoff")
    if not isinstance(stage2c, dict) or stage2c.get("requires_cap004_reconstruction") is not True:
        raise Stage2CError("Stage 2A ticket does not require Stage 2C CAP-004 reconstruction")
    if stage2c.get("reconstruction_is_read_only_derived_evidence") is not True:
        raise Stage2CError("Stage 2A ticket does not preserve the read-only reconstruction boundary")

    org_row = ticket.get("organization")
    actor_row = ticket.get("actor")
    if not isinstance(org_row, dict) or not isinstance(actor_row, dict):
        raise Stage2CError("Stage 2A Organization/Actor continuity is missing")
    organization_value = _required_text(org_row.get("organization_id"), field="Stage 2A organization_id")
    actor_value = _required_text(actor_row.get("principal_id"), field="Stage 2A principal_id")
    if actor_row.get("kind") != "human" or actor_row.get("attributable") is not True:
        raise Stage2CError("Stage 2A human Actor attribution is not preserved")

    organization = OrganizationScope(Identity("organization", organization_value, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", actor_value, organization_value)),
        organization,
    )
    return ticket, organization, actor


def validate_stage2b_handoff(handoff: dict[str, Any]) -> tuple[dict[str, str], ...]:
    if not isinstance(handoff, dict):
        raise Stage2CError("Stage 2B handoff must be a JSON object")
    if handoff.get("schema") != STAGE2B_HANDOFF_SCHEMA or handoff.get("schema_version") != STAGE2B_HANDOFF_SCHEMA_VERSION:
        raise Stage2CError("Stage 2B minimized handoff schema mismatch")
    if handoff.get("execution_id") != EXPECTED_EXECUTION_ID:
        raise Stage2CError("Stage 2B handoff execution id mismatch")
    if handoff.get("stage2a_ticket_sha256") != EXPECTED_STAGE2A_TICKET_SHA256:
        raise Stage2CError("Stage 2B handoff lost exact Stage 2A ticket continuity")

    contract = handoff.get("product_contract")
    if not isinstance(contract, dict) or contract.get("version") != PRODUCT_CONTRACT_VERSION or contract.get("blob_sha") != P6_06_CANONICAL_BLOB_SHA:
        raise Stage2CError("Stage 2B handoff Product Contract pin mismatch")

    review = handoff.get("canonical_stage2b_review")
    if not isinstance(review, dict) or (
        review.get("path") != STAGE2B_REVIEW_PATH
        or review.get("blob_sha") != STAGE2B_REVIEW_BLOB_SHA
        or review.get("closure_commit") != STAGE2B_CLOSURE_COMMIT
    ):
        raise Stage2CError("Stage 2B canonical review provenance mismatch")

    product = handoff.get("product")
    if not isinstance(product, dict) or product.get("repository") != STAGE2B_PRODUCT_REPOSITORY or product.get("repository_sha") != STAGE2B_PRODUCT_SHA:
        raise Stage2CError("Stage 2B product execution provenance mismatch")

    candidate = handoff.get("candidate")
    if not isinstance(candidate, dict) or (
        str(candidate.get("offer_id")) != STAGE2B_OFFER_ID
        or candidate.get("status_before") != "ready"
        or candidate.get("text_only") is not True
    ):
        raise Stage2CError("Stage 2B candidate evidence mismatch")
    if handoff.get("target_ref") != STAGE2B_TARGET_REF or handoff.get("template_version") != STAGE2B_TEMPLATE_VERSION:
        raise Stage2CError("Stage 2B target/template evidence mismatch")

    authorization = handoff.get("authorization")
    if not isinstance(authorization, dict) or (
        authorization.get("type") != STAGE2B_AUTHORIZATION_TYPE
        or authorization.get("received") is not True
        or authorization.get("authorized_at") != STAGE2B_AUTHORIZED_AT
        or authorization.get("scope_matches_candidate_target") is not True
        or authorization.get("max_external_sends") != 1
    ):
        raise Stage2CError("Stage 2B explicit human authorization evidence mismatch")

    containment = handoff.get("containment")
    expected_containment = {
        "scheduler_disabled": True,
        "autopost_disabled": True,
        "other_publishers_running": False,
        "publish_offer_invocations": 1,
        "telegram_send_delegations": 1,
        "telegram_send_message_calls": 1,
        "telegram_send_photo_calls": 0,
    }
    if not isinstance(containment, dict) or any(containment.get(key) != value for key, value in expected_containment.items()):
        raise Stage2CError("Stage 2B containment/one-send evidence mismatch")

    pre_effect = handoff.get("pre_effect")
    if not isinstance(pre_effect, dict) or (
        pre_effect.get("sha256") != STAGE2B_PRE_EFFECT_SHA256
        or str(pre_effect.get("publication_id")) != STAGE2B_PUBLICATION_ID
        or pre_effect.get("reservation_status") != "pending"
    ):
        raise Stage2CError("Stage 2B pre-effect evidence mismatch")

    outcome = handoff.get("outcome")
    if not isinstance(outcome, dict) or (
        outcome.get("sha256") != STAGE2B_OUTCOME_SHA256
        or outcome.get("publish_result_status") != "published"
        or outcome.get("publication_status") != "published"
        or outcome.get("offer_status") != "published"
        or str(outcome.get("telegram_message_id")) != STAGE2B_TELEGRAM_MESSAGE_ID
        or outcome.get("external_confirmation") != "PASS"
        or outcome.get("reconciliation_required") is not False
    ):
        raise Stage2CError("Stage 2B confirmed outcome evidence mismatch")

    minimization = handoff.get("data_minimization")
    if not isinstance(minimization, dict) or any(
        minimization.get(key) is not False
        for key in (
            "raw_pre_effect_embedded",
            "raw_outcome_embedded",
            "reusable_secrets_embedded",
            "raw_opaque_organization_identity_embedded",
            "raw_opaque_actor_identity_embedded",
        )
    ):
        raise Stage2CError("Stage 2B minimized handoff violates the declared data-minimization boundary")

    rows = handoff.get("material_refs")
    if not isinstance(rows, list):
        raise Stage2CError("Stage 2B material_refs must be a list")
    material_args: list[str] = []
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"role", "reference"}:
            raise Stage2CError("each Stage 2B material ref must contain role/reference only")
        material_args.append(f"{row['role']}={row['reference']}")
    return _normalize_material_refs(tuple(material_args))


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
    semantic_type = semantic_by_role[role]
    authority_scope = "external-reference/telegram-channel" if role == "telegram-target" else "product-local-reference"
    return _pin(
        role=role,
        subject_value=f"stage2b-{role}-{digest[:16]}",
        version_value=f"sha256-{digest}",
        semantic_type=semantic_type,
        scope=scope,
        authority_scope=authority_scope,
        lifecycle_status="RetainedReference",
    )


def _build_manifest_and_constraints(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
    contract: Any,
    material_refs: tuple[dict[str, str], ...],
    canonical_repo_sha: str,
) -> tuple[ReconstructionManifest, tuple[tuple[Identity, str, tuple[str, ...], str], ...]]:
    scope = organization.organization_id.value

    workflow = _pin(
        role="workflow",
        subject_value="controlled-telegram-publication",
        version_value=f"product-{STAGE2B_PRODUCT_SHA}-template-{STAGE2B_TEMPLATE_VERSION}",
        semantic_type="discount-parser.controlled-publication-workflow-ref",
        scope=scope,
        authority_scope="product-local-reference",
        lifecycle_status="Applied",
    )
    stage2a_ticket = _pin(
        role="stage2a-ticket",
        subject_value="p6-07-stage2a-ticket",
        version_value=f"sha256-{EXPECTED_STAGE2A_TICKET_SHA256}",
        semantic_type="platform.execution-handoff-evidence-ref",
        scope=scope,
        authority_scope="owner-local-evidence/reference",
        lifecycle_status="Verified",
    )
    stage2b_review = _pin(
        role="stage2b-review",
        subject_value=STAGE2B_REVIEW_PATH,
        version_value=f"blob-{STAGE2B_REVIEW_BLOB_SHA}",
        semantic_type="platform.review-evidence-ref",
        scope=scope,
        authority_scope="repository-evidence/canonical-review",
        lifecycle_status="Canonical",
    )
    pre_effect = _pin(
        role="pre-effect-evidence",
        subject_value="p6-07-stage2b-pre-effect",
        version_value=f"sha256-{STAGE2B_PRE_EFFECT_SHA256}",
        semantic_type="platform.execution-evidence-ref",
        scope=scope,
        authority_scope="owner-local-evidence/reference",
        lifecycle_status="Verified",
    )
    product_material = tuple(
        _material_ref_pin(role=item["role"], reference=item["reference"], scope=scope)
        for item in material_refs
    )
    material_inputs = (stage2a_ticket, stage2b_review, pre_effect, *product_material)

    execution = _pin(
        role="execution",
        subject_value=EXPECTED_EXECUTION_ID,
        version_value=f"{EXPECTED_EXECUTION_ID}-outcome-{STAGE2B_OUTCOME_SHA256}",
        semantic_type="platform.execution-context-ref",
        scope=scope,
        authority_scope="platform.execution-history/reference",
        lifecycle_status="CompletedObserved",
    )
    outcome = _pin(
        role="publication-outcome",
        subject_value=f"publication-{STAGE2B_PUBLICATION_ID}",
        version_value=f"sha256-{STAGE2B_OUTCOME_SHA256}",
        semantic_type="discount-parser.publication-outcome-ref",
        scope=scope,
        authority_scope="product-local-reference",
        lifecycle_status="Published",
    )
    telegram_message = _pin(
        role="telegram-message",
        subject_value=f"{STAGE2B_TARGET_REF}/message/{STAGE2B_TELEGRAM_MESSAGE_ID}",
        version_value=f"message-{STAGE2B_TELEGRAM_MESSAGE_ID}-confirmed",
        semantic_type="discount-parser.telegram-message-ref",
        scope=scope,
        authority_scope="external-reference/telegram-message",
        lifecycle_status="ExternallyConfirmed",
    )

    # This is explicitly a Stage 2C admission-observation reference created for
    # reconstruction now.  It is NOT a claim that a Native platform Event was
    # already admitted on Windows before/during the Stage 2B Telegram send.
    admission_observation = _pin(
        role="stage2c-admission",
        subject_value=f"stage2b-outcome-{STAGE2B_PUBLICATION_ID}",
        version_value=f"review-{STAGE2B_REVIEW_BLOB_SHA}-outcome-{STAGE2B_OUTCOME_SHA256}",
        semantic_type="platform.event-ref",
        scope=scope,
        authority_scope="stage2c-derived-admission/reference",
        lifecycle_status="AdmittedForReconstruction",
    )

    attempts = tuple(pin for pin in product_material if pin.semantic_type == "discount-parser.publication-attempt-ref")
    attempt_subject = attempts[-1].subject_id

    provenance_refs = tuple(
        dict.fromkeys(
            (
                actor.actual_principal.principal_id,
                execution.subject_id,
                stage2a_ticket.version_id,
                stage2b_review.version_id,
                pre_effect.version_id,
                outcome.version_id,
                telegram_message.version_id,
                admission_observation.version_id,
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
        # The real one-time human authorization remains an exact product/local
        # evidence reference in material_inputs.  We do not fabricate a
        # retroactive platform GovernedGateDecision for the Windows action.
        gate_decisions=(),
        execution_versions=(execution,),
        results=(outcome, telegram_message),
        events=(admission_observation,),
        event_types=(("discount-parser.stage2b-outcome-admission", "1"),),
        correlation_refs=(execution.subject_id, attempt_subject),
        causation_refs=(pre_effect.version_id, outcome.version_id),
        provenance_refs=provenance_refs,
    )

    pins = (
        workflow,
        *material_inputs,
        contract.version_pin,
        execution,
        outcome,
        telegram_message,
        admission_observation,
    )
    by_version: dict[Identity, GovernedVersionPin] = {}
    for pin in pins:
        prior = by_version.get(pin.version_id)
        if prior is None:
            by_version[pin.version_id] = pin
        elif prior != pin:
            raise Stage2CError("Stage 2C evidence reuses one Version Identity with conflicting semantics")
    constraints = tuple(
        (version_id, PURPOSE, ("read",), CLASSIFICATION)
        for version_id in by_version
    )
    return manifest, constraints


def reconstruct_stage2b_through_cap004(
    *,
    stage2a_ticket_path: Path,
    stage2a_digest_path: Path,
    stage2b_handoff_path: Path,
    stage2b_handoff_digest_path: Path,
    canonical_repo_sha: str,
) -> Stage2CReconstructionResult:
    canonical_repo_sha = _required_text(canonical_repo_sha, field="canonical_repo_sha").lower()
    if not _GIT_SHA_RE.fullmatch(canonical_repo_sha):
        raise Stage2CError("canonical_repo_sha must be a full lowercase Git SHA")

    ticket, organization, actor = _load_stage2a_context(
        ticket_path=stage2a_ticket_path,
        digest_path=stage2a_digest_path,
    )
    handoff = _load_verified_json(
        json_path=stage2b_handoff_path,
        digest_path=stage2b_handoff_digest_path,
        expected_filename=STAGE2B_HANDOFF_FILENAME,
    )
    material_refs = validate_stage2b_handoff(handoff)

    try:
        created_at = datetime.fromisoformat(str(ticket["created_at"]).replace("Z", "+00:00"))
    except (KeyError, ValueError, TypeError) as exc:
        raise Stage2CError("Stage 2A created_at is invalid") from exc
    contract = build_p6_06_product_contract_projection(actor=actor, created_at=created_at)
    if contract.version_pin.version_id.value != "p6-06-arvectum-discount-parser-v0.1.0":
        raise Stage2CError("executable Product Contract projection lost exact v0.1.0 Version Identity")

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
    manifest, constraints = _build_manifest_and_constraints(
        organization=organization,
        actor=actor,
        contract=contract,
        material_refs=material_refs,
        canonical_repo_sha=canonical_repo_sha,
    )
    reconstruction = reconstruct_publication(
        adapters=adapters,
        request=request,
        governed_versions=governed_versions,
        manifest=manifest,
        evidence_constraints=constraints,
    )
    if not reconstruction.complete:
        raise Stage2CError("Stage 2C CAP-004 reconstruction is incomplete")
    if reconstruction.organization != organization:
        raise Stage2CError("Stage 2C reconstruction lost exact Organization continuity")
    if reconstruction.initiating_actor_id != actor.actual_principal.principal_id:
        raise Stage2CError("Stage 2C reconstruction lost exact human Actor continuity")
    if manifest.product_contract != contract.version_pin:
        raise Stage2CError("Stage 2C reconstruction lost exact Product Contract continuity")
    if manifest.gate_decisions:
        raise Stage2CError("Stage 2C must not fabricate a retroactive platform gate decision")

    report: dict[str, Any] = {
        "schema": STAGE2C_REPORT_SCHEMA,
        "schema_version": STAGE2C_REPORT_SCHEMA_VERSION,
        "status": "PASS",
        "stage": "P6.07 Stage 2C",
        "canonical_repo": {
            "repository": REPOSITORY_FULL_NAME,
            "sha": canonical_repo_sha,
        },
        "continuity": {
            "execution_id": EXPECTED_EXECUTION_ID,
            "stage2a_ticket_sha256": EXPECTED_STAGE2A_TICKET_SHA256,
            "organization_continuity": "PASS",
            "actor_continuity": "PASS",
            "product_contract_version": PRODUCT_CONTRACT_VERSION,
            "product_contract_blob_sha": P6_06_CANONICAL_BLOB_SHA,
            "product_contract_continuity": "PASS",
        },
        "stage2b": {
            "canonical_review_path": STAGE2B_REVIEW_PATH,
            "canonical_review_blob_sha": STAGE2B_REVIEW_BLOB_SHA,
            "closure_commit": STAGE2B_CLOSURE_COMMIT,
            "product_repository_sha": STAGE2B_PRODUCT_SHA,
            "offer_id": STAGE2B_OFFER_ID,
            "publication_id": STAGE2B_PUBLICATION_ID,
            "target_ref": STAGE2B_TARGET_REF,
            "template_version": STAGE2B_TEMPLATE_VERSION,
            "pre_effect_sha256": STAGE2B_PRE_EFFECT_SHA256,
            "outcome_sha256": STAGE2B_OUTCOME_SHA256,
            "telegram_message_id": STAGE2B_TELEGRAM_MESSAGE_ID,
            "external_confirmation": "PASS",
            "material_reference_roles": sorted({item["role"] for item in material_refs}),
            "material_reference_count": len(material_refs),
        },
        "cap004": {
            "dependency": "CAP-004",
            "provider_contract_version": CAPABILITY_CONTRACT_VERSION,
            "operation": OP_RECONSTRUCT_EXECUTION,
            "read_only": True,
            "reconstruction_complete": reconstruction.complete,
            "evidence_item_count": len(reconstruction.evidence),
            "evidence_roles": [item.role for item in reconstruction.evidence],
            "gate_decisions_fabricated": False,
            "admission_event_semantics": "stage2c-derived-admission-reference-not-retroactive-windows-event",
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
            "raw_stage2b_pre_effect_written": False,
            "raw_stage2b_outcome_written": False,
            "reusable_secrets_written": False,
        },
    }
    return Stage2CReconstructionResult(
        organization=organization,
        actor=actor,
        adapters=adapters,
        manifest=manifest,
        reconstruction=reconstruction,
        report=report,
    )


def write_stage2c_report(*, output_dir: Path, result: Stage2CReconstructionResult) -> tuple[Path, Path, str]:
    if not isinstance(result, Stage2CReconstructionResult):
        raise Stage2CError("Stage 2C report requires a verified reconstruction result")
    return _write_immutable_json(
        output_dir=output_dir,
        filename=STAGE2C_REPORT_FILENAME,
        digest_filename=STAGE2C_REPORT_DIGEST_FILENAME,
        payload=result.report,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="P6.07 Stage 2C local evidence handoff / CAP-004 reconstruction")
    sub = parser.add_subparsers(dest="command", required=True)

    handoff = sub.add_parser("handoff", help="create minimized Stage 2B handoff on the Windows evidence owner host")
    handoff.add_argument("--pre-effect", required=True, type=Path)
    handoff.add_argument("--outcome", required=True, type=Path)
    handoff.add_argument("--material-ref", action="append", default=[], help="safe role=reference; repeat as needed")
    handoff.add_argument("--output-dir", required=True, type=Path)

    reconstruct = sub.add_parser("reconstruct", help="reconstruct Stage 2B through CAP-004 on the Mac mini")
    reconstruct.add_argument("--stage2a-ticket", required=True, type=Path)
    reconstruct.add_argument("--stage2a-digest", required=True, type=Path)
    reconstruct.add_argument("--stage2b-handoff", required=True, type=Path)
    reconstruct.add_argument("--stage2b-handoff-digest", required=True, type=Path)
    reconstruct.add_argument("--canonical-repo-sha", required=True)
    reconstruct.add_argument("--output-dir", required=True, type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "handoff":
        handoff = build_stage2b_minimized_handoff(
            pre_effect_path=args.pre_effect,
            outcome_path=args.outcome,
            material_refs=tuple(args.material_ref),
        )
        json_path, digest_path, digest = write_stage2b_minimized_handoff(
            output_dir=args.output_dir,
            handoff=handoff,
        )
        print(f"STAGE2B_HANDOFF={json_path}")
        print(f"STAGE2B_HANDOFF_SHA256_FILE={digest_path}")
        print(f"STAGE2B_HANDOFF_SHA256={digest}")
        print("STAGE2B_HANDOFF_RESULT=PASS")
        return 0

    result = reconstruct_stage2b_through_cap004(
        stage2a_ticket_path=args.stage2a_ticket,
        stage2a_digest_path=args.stage2a_digest,
        stage2b_handoff_path=args.stage2b_handoff,
        stage2b_handoff_digest_path=args.stage2b_handoff_digest,
        canonical_repo_sha=args.canonical_repo_sha,
    )
    report_path, digest_path, digest = write_stage2c_report(
        output_dir=args.output_dir,
        result=result,
    )
    print(f"STAGE2C_REPORT={report_path}")
    print(f"STAGE2C_REPORT_SHA256_FILE={digest_path}")
    print(f"STAGE2C_REPORT_SHA256={digest}")
    print(f"STAGE2C_EXECUTION_ID={EXPECTED_EXECUTION_ID}")
    print(f"STAGE2C_RECONSTRUCTION_COMPLETE={str(result.reconstruction.complete).lower()}")
    print("STAGE2C_NETWORK_CALLS=0")
    print("STAGE2C_TELEGRAM_CALLS=0")
    print("STAGE2C_EXTERNAL_MUTATIONS=0")
    print("STAGE2C_RESULT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
