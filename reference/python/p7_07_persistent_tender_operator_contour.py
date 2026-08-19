#!/usr/bin/env python3
"""P7.07 persistent Tender Operator operational contour.

This private/reversible Phase-7 adapter closes the gap between the durable P7.03
store and real repeatable Tender Operator CAP-001 reliance without exposing the
store to the product as a contract.

One owner-approved setup may admit a minimized, rehydratable External Reference
Document Version through the existing P6.02 Provisional 0.1.0 / P6.05 executable
projection and RFC-0005 Governed Execution. Setup then provisions one exact
P7.04 local read grant and revokes its temporary setup grant. Ordinary contour
runs are read-only: the platform verifies and rehydrates the exact governed
Document Version internally, then the actual product-owned ArvectumOSBridge
invokes CAP-001 through the declared Product Contract boundary.

No EIS/SOAP/network retrieval, procurement-domain interpretation, bid/submission,
external effect, raw tender-byte persistence, general canonical-write authority,
public/stable API, Product Contract promotion or capability promotion is created.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import ModuleType
from typing import Any, Final, Mapping

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
    AdmittedDocumentVersion,
    ArtifactContent,
    ArtifactState,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.event_provenance import EventReceipt, admit_event, build_reconstruction_manifest
from arvectum_os_ref.governed_execution import (
    GovernedExecutionLifecycle,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    AccessRequest,
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    CapabilityConsumptionRequest,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.workflow import OperationSideEffectClass, WorkflowDefinition, WorkflowOperation
from p6_03_tender_operator_ref.contract import (
    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
    PRODUCT_COMPATIBILITY_LINE,
)
from p6_05_l5_first_real_product_connection import GOVERNANCE_REFERENCE, connect_product
from p6_05_tender_attachment_ref.contract import OP_ADMIT_DOCUMENT_VERSION
import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_06_governed_deploy as p706

UTC = timezone.utc

OWNER_DECISION_PATH: Final = (
    "docs/governance/decisions/"
    "DECISION-2026-08-19-P7-07-PERSISTENT-TENDER-OPERATOR-CONTOUR.md"
)
OWNER_APPROVAL_ASSERTION: Final = "OWNER_APPROVES_P7_07_TENDER_OPERATOR_OPERATIONAL_ADMISSION"
NOTICE_NUMBER: Final = "0344100006426000005"
APPROVED_MANIFEST_SHA256: Final = "74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121"
MANIFEST_SCHEMA: Final = "p6.05-exact-attachment-evidence-v1"
MANIFEST_PURPOSE: Final = "exact-tender-attachment-evidence"
MANIFEST_STATUS: Final = "PASS_EXACT_ATTACHMENT_EVIDENCE"
EXTERNAL_SOURCE_AUTHORITY: Final = "ЕИС / zakupki.gov.ru"
EXPECTED_DOCUMENT_COUNT: Final = 7
MAX_MANIFEST_BYTES: Final = 2 * 1024 * 1024
MAX_ITEM_PAYLOAD_BYTES: Final = 2 * 1024 * 1024

SETUP_ACCESS_OPERATION: Final = "p7.07.tender-operator.setup"
SETUP_ACCESS_RESOURCE: Final = "p7-07:persistent-tender-operator-operational-document"
READ_ACCESS_OPERATION: Final = OP_RESOLVE_DOCUMENT
READ_RESOURCE_PREFIX: Final = "p7-07:tender-operator-operational-document:"
ACCESS_PATH: Final = "local"

PERSISTED_SCHEMA: Final = "arvectum.p7_07.tender-operator-operational-document/1"
PERSISTED_RECORD_SCHEMA: Final = "p7.07-tender-operator-operational-evidence-1"
PERSISTED_CLASSIFICATION: Final = "restricted-pilot"
PERSISTED_PURPOSE: Final = "prebid-review"
PERSISTED_RETENTION: Final = "P6.02 restricted-paid-pilot / inherit-product-source-retention"
CONFIG_SCHEMA: Final = "arvectum.p7_07.tender-operator-contour-config/1"
EVIDENCE_SCHEMA: Final = "arvectum.p7_07.tender-operator-contour-evidence/1"
PRODUCT_BRIDGE_RELATIVE_PATH: Final = "src/modules/tender_operator_agent_demo/arvectum_os_bridge.py"
PRODUCT_BRIDGE_CLASS: Final = "ArvectumOSBridge"


class P707Error(RuntimeError):
    """Fail-closed P7.07 operational-contour error."""


@dataclass(frozen=True, slots=True)
class VerifiedManifest:
    value: Mapping[str, Any]
    manifest_sha256: str
    source_version: str
    retrieved_at: datetime


@dataclass(frozen=True, slots=True)
class SetupResult:
    status: str
    release_sha: str
    storage_item_id: str
    checkpoint_id: str | None
    subject_identity: str
    version_identity: str
    read_resource: str
    idempotent_existing_item: bool
    reconstruction_complete: bool
    evidence_path: str


@dataclass(frozen=True, slots=True)
class ConsumptionResult:
    status: str
    release_sha: str
    storage_item_id: str
    subject_identity: str
    version_identity: str
    artifact_identity: str
    integrity_ref: str
    authoritative_source: str
    product_contract_version: str
    evidence_path: str


def _id(namespace: str, value: str, scope: str) -> Identity:
    return Identity(namespace, value, scope)


def _identity_text(value: Identity) -> str:
    if not isinstance(value, Identity):
        raise P707Error("Identity required")
    return f"{value.namespace}/{value.value}@{value.scope}"


def _id_dict(value: Identity) -> dict[str, str]:
    return {"namespace": value.namespace, "value": value.value, "scope": value.scope}


def _id_load(value: Mapping[str, Any], *, label: str) -> Identity:
    if not isinstance(value, Mapping) or set(value) != {"namespace", "value", "scope"}:
        raise P707Error(f"{label} identity shape invalid")
    try:
        return Identity(str(value["namespace"]), str(value["value"]), str(value["scope"]))
    except Exception as exc:
        raise P707Error(f"{label} identity invalid") from exc


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_private_regular_file(path: Path, *, max_bytes: int, label: str) -> Path:
    path = path.expanduser()
    if path.is_symlink():
        raise P707Error(f"{label} must not be a symlink")
    try:
        resolved = path.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise P707Error(f"{label} is missing or unreadable") from exc
    if not resolved.is_file() or resolved.is_symlink():
        raise P707Error(f"{label} must be a regular file")
    size = resolved.stat().st_size
    if size <= 0 or size > max_bytes:
        raise P707Error(f"{label} size outside bounded limit")
    if os.name != "nt" and (resolved.stat().st_mode & 0o077):
        raise P707Error(f"{label} must be owner-only")
    return resolved


def _atomic_json(path: Path, value: Mapping[str, Any]) -> str:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(path.parent, 0o700)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n"
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        if os.name != "nt":
            os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        if os.name != "nt":
            os.chmod(path, 0o600)
    finally:
        try:
            os.unlink(tmp)
        except FileNotFoundError:
            pass
    return _sha256_bytes(payload)


def _config_path(runtime_root: Path) -> Path:
    return runtime_root.expanduser().resolve() / "config" / "p7-07-tender-operator.json"


def _verify_owner_decision(repo_root: Path) -> None:
    root = repo_root.resolve()
    path = (root / OWNER_DECISION_PATH).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise P707Error("P7.07 owner decision escaped exact release source") from exc
    if not path.is_file() or path.is_symlink():
        raise P707Error("P7.07 owner decision missing from exact release")
    text = path.read_text(encoding="utf-8")
    required = (
        "Status: `Approved`",
        OWNER_APPROVAL_ASSERTION,
        APPROVED_MANIFEST_SHA256,
        "Authorization",
        "Organizational Authority",
        "Data Governance",
        "Consequential Approval",
        "prebid-review",
    )
    if any(token not in text for token in required):
        raise P707Error("P7.07 owner decision does not preserve bounded approval")


def _verify_exact_release(runtime_root: Path) -> tuple[str, Path]:
    root = runtime_root.expanduser().resolve()
    release_sha = p706.current_release(root)
    p706.verify_release(root, release_sha)
    expected = (
        root / "releases" / release_sha / "source" / "reference" / "python" / Path(__file__).name
    )
    if Path(__file__).resolve() != expected.resolve():
        raise P707Error("P7.07 contour must run from the exact active release")
    repo_root = expected.parents[2]
    _verify_owner_decision(repo_root)
    return release_sha, repo_root


def load_verified_manifest(path: Path) -> VerifiedManifest:
    resolved = _safe_private_regular_file(path, max_bytes=MAX_MANIFEST_BYTES, label="P6.05-L7 manifest")
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P707Error("P6.05-L7 manifest is not readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise P707Error("P6.05-L7 manifest must be a JSON object")

    digest = value.get("manifest_sha256")
    if digest != APPROVED_MANIFEST_SHA256 or value.get("manifest_integrity_ref") != f"sha256:{digest}":
        raise P707Error("P6.05-L7 manifest is not the exact approved evidence")
    body = dict(value)
    body.pop("manifest_sha256", None)
    body.pop("manifest_integrity_ref", None)
    if _sha256_bytes(_canonical_json_bytes(body)) != digest:
        raise P707Error("P6.05-L7 manifest body integrity mismatch")

    exact = {
        "schema_version": MANIFEST_SCHEMA,
        "purpose": MANIFEST_PURPOSE,
        "status": MANIFEST_STATUS,
        "notice_number": NOTICE_NUMBER,
        "expected_document_count": EXPECTED_DOCUMENT_COUNT,
        "exact_document_count": EXPECTED_DOCUMENT_COUNT,
        "missing_names": [],
        "duplicate_names": [],
        "external_actions": False,
        "external_source_authority": EXTERNAL_SOURCE_AUTHORITY,
        "external_source_reference": f"44fz-notice:{NOTICE_NUMBER}",
    }
    for key, expected in exact.items():
        if value.get(key) != expected:
            raise P707Error(f"P6.05-L7 manifest field {key!r} mismatches approved evidence")
    documents = value.get("documents")
    if not isinstance(documents, list) or len(documents) != EXPECTED_DOCUMENT_COUNT:
        raise P707Error("P6.05-L7 manifest document set is incomplete")
    if any(not isinstance(item, dict) or "sha256" not in item or "size_bytes" not in item for item in documents):
        raise P707Error("P6.05-L7 manifest lacks exact member integrity evidence")
    source_version = value.get("external_source_version")
    retrieved_raw = value.get("retrieved_at")
    if not isinstance(source_version, str) or not source_version.strip() or not isinstance(retrieved_raw, str):
        raise P707Error("P6.05-L7 manifest source-version/retrieval evidence missing")
    try:
        retrieved_at = datetime.fromisoformat(retrieved_raw)
    except ValueError as exc:
        raise P707Error("P6.05-L7 manifest retrieval timestamp invalid") from exc
    if retrieved_at.tzinfo is None or retrieved_at.utcoffset() is None:
        raise P707Error("P6.05-L7 manifest retrieval timestamp must be timezone-aware")
    return VerifiedManifest(value, digest, source_version.strip(), retrieved_at)


def _governed_versions() -> tuple[GovernedDependencyVersionEvidence, ...]:
    return (
        GovernedDependencyVersionEvidence(
            CAP_001_DOCUMENT_ARTIFACT,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            GOVERNANCE_REFERENCE,
        ),
        GovernedDependencyVersionEvidence(
            CAP_004_AUDIT_RECONSTRUCTION,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            GOVERNANCE_REFERENCE,
        ),
    )


def _verify_connection(connection, organization: Identity, principal: Identity) -> None:
    if connection.organization_scope.organization_id != organization:
        raise P707Error("persistent Organization continuity mismatch")
    if connection.principal.principal_id != principal:
        raise P707Error("persistent human Principal continuity mismatch")
    if connection.actor_context.actual_principal.principal_id != principal:
        raise P707Error("ActorContext lost attributable human Principal")
    if connection.product_contract.version_pin.version_id.value != "p6-02-arvectum-tender-operator-v0.1.0":
        raise P707Error("exact P6.02 Product Contract 0.1.0 continuity lost")
    if connection.product_contract.product_version != PRODUCT_COMPATIBILITY_LINE:
        raise P707Error("Tender Operator compatibility line drifted")


def _credential_owner_binding(
    access_root: Path,
    *,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
) -> tuple[Identity, Identity]:
    organization, principal = p704.load_p6_owner_context(state_file)
    p704.verify_store(access_root)
    state = p704.load_access_store(access_root)
    credential = state.get("credentials", {}).get(credential_id)
    if not isinstance(credential, dict) or credential.get("status") != "active":
        raise P707Error("active persistent P7.04 credential required")
    principal_record = state.get("principals", {}).get(credential.get("principal_key"))
    if not isinstance(principal_record, dict) or principal_record.get("status") != "enabled":
        raise P707Error("credential is not bound to an enabled persistent Principal")
    if principal_record.get("kind") != "human" or principal_record.get("identity") != _id_dict(principal):
        raise P707Error("P7.07 owner-operated contour requires the persistent attributable human Principal")
    expected_secret = (access_root.expanduser().resolve() / "secrets" / "p7-04" / f"{credential_id}.secret").resolve()
    supplied = _safe_private_regular_file(credential_file, max_bytes=64 * 1024, label="P7.04 credential secret")
    if supplied != expected_secret:
        raise P707Error("credential file is not the P7.04 owner-local secret bound to credential_id")
    p704.read_credential_secret(supplied)
    return organization, principal


def _authorize_exact(
    access_root: Path,
    *,
    organization: Identity,
    principal: Identity,
    credential_id: str,
    credential_file: Path,
    operation: str,
    resource: str,
) -> p704.AccessDecision:
    decision = p704.authorize_from_credential_file(
        access_root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
        operation=operation,
        resource=resource,
        access_path=ACCESS_PATH,
    )
    if not decision.allowed:
        raise P707Error(f"P7.04 authorization denied: {decision.reason}")
    if decision.principal_kind != "human":
        raise P707Error("P7.07 owner-operated contour requires human Principal authorization")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise P707Error("P7.04 access must not satisfy Organizational Authority or consequential approval")
    return decision


def _operational_identity_pair(connection) -> tuple[Identity, Identity]:
    scope = connection.organization_scope.organization_id.value
    suffix = APPROVED_MANIFEST_SHA256[:16]
    return (
        _id("document-subject", f"eis-{NOTICE_NUMBER}-tender-operator-operational-evidence", scope),
        _id("document-version", f"eis-{NOTICE_NUMBER}-{suffix}-p7-07-operational-v1", scope),
    )


def _build_candidate_and_interaction(connection, manifest: VerifiedManifest, *, base_time: datetime):
    organization = connection.organization_scope
    actor = connection.actor_context
    contract = connection.product_contract
    scope = organization.organization_id.value
    subject, version = _operational_identity_pair(connection)
    suffix = APPROVED_MANIFEST_SHA256[:16]
    execution_subject = _id("execution-subject", f"p7-07-tender-operator-admission-{suffix}", scope)

    authority = ExternalAuthorityContract(
        authoritative_system=EXTERNAL_SOURCE_AUTHORITY,
        external_object_ref=f"44fz-notice:{NOTICE_NUMBER}",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync=(
            "reuse already-retained read-only P6.05-L7 exact evidence; P7.07 setup performs no EIS/SOAP/network retrieval"
        ),
        freshness_expectation="exact retained external source version pinned by approved P6.05-L7 manifest",
        source_version_semantics="EIS getDocsIP source version plus exact seven-document manifest digest",
        conflict_rule="ЕИС / zakupki.gov.ru remains authoritative; digest/version mismatch fails closed",
        failure_behavior="missing, changed or unverifiable retained evidence blocks P7.07 admission/reliance",
        permitted_transformations=("integrity hashing", "manifest generation", "governed reference admission"),
        retention_deletion="inherit P6.02 restricted-paid-pilot product/source retention rules",
        portability="export governed external reference, exact manifest digest and provenance without credentials",
    )
    record = CanonicalRecord(
        subject_id=subject,
        version_id=version,
        semantic_type="platform.document",
        schema_version=PERSISTED_RECORD_SCHEMA,
        organization=organization,
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=base_time,
        provenance_refs=(
            actor.actual_principal.principal_id,
            execution_subject,
            contract.version_pin.subject_id,
            contract.version_pin.version_id,
        ),
        integrity_metadata=(
            ("member_count", str(EXPECTED_DOCUMENT_COUNT)),
            ("manifest_sha256", manifest.manifest_sha256),
            ("external_source_version", manifest.source_version),
            ("raw_document_bytes_platformized", "false"),
            ("operational_contour", "P7.07"),
        ),
        payload=(
            ("purpose", PERSISTED_PURPOSE),
            ("notice_number", NOTICE_NUMBER),
            ("manifest_integrity_ref", f"sha256:{manifest.manifest_sha256}"),
            ("product_contract_version", "0.1.0"),
        ),
        lifecycle_status="AdmissionCandidate",
        external_authority=authority,
    )
    artifact = ArtifactContent(
        artifact_id=_id("artifact", f"p7-07-eis-{NOTICE_NUMBER}-{suffix}-manifest", scope),
        organization=organization,
        content_ref=f"retained-evidence-manifest://sha256/{manifest.manifest_sha256}",
        media_type="application/json",
        integrity_ref=f"sha256:{manifest.manifest_sha256}",
        rendition_role="evidence-manifest",
        handling=HandlingConstraints(
            PERSISTED_CLASSIFICATION,
            PERSISTED_PURPOSE,
            ("read",),
            "inherit-product-source-retention",
        ),
    )
    candidate = DocumentVersionCandidate(record, (artifact,), "evidence-manifest")

    workflow_record = CanonicalRecord(
        subject_id=_id("workflow-subject", "p7-07-tender-operator-operational-admission", scope),
        version_id=_id("workflow-version", "p7-07-tender-operator-operational-admission-v1", scope),
        semantic_type="platform.workflow",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.workflow/definition",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=base_time,
        provenance_refs=(
            actor.actual_principal.principal_id,
            subject,
            contract.version_pin.subject_id,
            contract.version_pin.version_id,
        ),
        integrity_metadata=(("governance_decision", OWNER_DECISION_PATH),),
        lifecycle_status="Approved",
    )
    workflow = WorkflowDefinition(
        record=workflow_record,
        operations=(
            WorkflowOperation(
                semantic_name=OP_ADMIT_DOCUMENT_VERSION,
                target_subject_id=subject,
                target_semantic_type="platform.document",
                side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
            ),
        ),
    )
    interaction = ProductRuntimeInteraction(
        organization=organization,
        product_id=contract.product_id,
        product_version=contract.product_version,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        workflow=workflow,
        operation_name=OP_ADMIT_DOCUMENT_VERSION,
        material_inputs=(record,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        ),
    )
    return candidate, interaction, execution_subject


def _gate_basis(kind: GovernedGateKind, scope: str) -> Identity:
    values = {
        GovernedGateKind.AUTHORIZATION: ("authorization-basis", "p7-07-exact-p7-04-setup-grant"),
        GovernedGateKind.ORGANIZATIONAL_AUTHORITY: ("organizational-authority-basis", "decision-2026-08-19-p7-07"),
        GovernedGateKind.DATA_GOVERNANCE: ("data-governance-basis", "p6-02-v0.1.0+p6-05-l7-exact-eis-manifest"),
        GovernedGateKind.CONSEQUENTIAL_APPROVAL: ("consequential-approval-basis", "decision-2026-08-19-p7-07"),
    }
    if kind not in values:
        raise P707Error(f"unexpected gate kind: {kind.value}")
    namespace, value = values[kind]
    return _id(namespace, value, scope)


def _run_governed_admission(connection, manifest: VerifiedManifest, *, base_time: datetime):
    actor = connection.actor_context
    organization = connection.organization_scope
    scope = organization.organization_id.value
    candidate, interaction, execution_subject = _build_candidate_and_interaction(connection, manifest, base_time=base_time)
    governed_versions = _governed_versions()
    v1 = connection.adapters.facade.start_governed_execution(
        interaction=interaction,
        execution_id=execution_subject,
        version_id=_id("execution-version", f"{execution_subject.value}-v1", scope),
        created_at=base_time + timedelta(microseconds=1),
        governed_versions=governed_versions,
    )
    awaiting = await_required_gates(
        v1,
        version_id=_id("execution-version", f"{execution_subject.value}-v2", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=2),
    )
    if tuple(awaiting.required_gates) != tuple(interaction.required_gates):
        raise P707Error("Governed Execution required-gate set drifted")

    decisions = tuple(
        build_governed_gate_decision(
            execution=awaiting,
            kind=kind,
            outcome=GovernedGateOutcome.ALLOW,
            decision_actor=actor,
            basis_ref=_gate_basis(kind, scope),
            decision_id=_id("gate-decision-subject", f"{execution_subject.value}-{kind.value}", scope),
            version_id=_id("gate-decision-version", f"{execution_subject.value}-{kind.value}-v1", scope),
            created_at=base_time + timedelta(microseconds=3 + index),
        )
        for index, kind in enumerate(awaiting.required_gates)
    )
    ready = admit_ready_execution(
        awaiting,
        decisions=decisions,
        version_id=_id("execution-version", f"{execution_subject.value}-v3", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=8),
    )
    admitted = connection.adapters.capabilities.admit_document_version(execution=ready, candidate=candidate)
    if admitted.version_id != candidate.canonical_record.version_id:
        raise P707Error("CAP-001 admission lost exact Document Version identity")
    if admitted.canonical_record.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE:
        raise P707Error("CAP-001 admission lost External Reference authority")
    artifact = admitted.resolve_artifact(candidate.artifacts[0].artifact_id)
    if artifact.state is not ArtifactState.GOVERNED or artifact.handling.purpose != PERSISTED_PURPOSE:
        raise P707Error("CAP-001 admission lost governed prebid-review handling")

    running = transition_governed_execution(
        ready,
        lifecycle=GovernedExecutionLifecycle.RUNNING,
        version_id=_id("execution-version", f"{execution_subject.value}-v4", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=9),
    )
    terminal = transition_governed_execution(
        running,
        lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
        version_id=_id("execution-version", f"{execution_subject.value}-v5", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=10),
        additional_provenance_refs=(admitted.document_id, admitted.version_id),
    )
    producer = _id("producer", "platform.core", scope)
    receipt = EventReceipt(
        event_id=_id("event-subject", f"p7-07-operational-document-admitted-{APPROVED_MANIFEST_SHA256[:16]}", scope),
        version_id=_id("event-version", f"p7-07-operational-document-admitted-{APPROVED_MANIFEST_SHA256[:16]}-v1", scope),
        event_type="p7.07.tender-operator-operational-document-admitted",
        event_schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.document/admission",
        authoritative_source="platform.core",
        occurred_at=base_time + timedelta(microseconds=11),
        recorded_at=base_time + timedelta(microseconds=12),
        producer_id=producer,
        initiating_actor_id=actor.actual_principal.principal_id,
        execution_subject_id=terminal.execution_subject_id,
        execution_version_id=terminal.execution_version_id,
        related_subject_ids=(admitted.document_id,),
        related_version_ids=(admitted.version_id,),
        correlation_refs=(terminal.execution_subject_id,),
        causation_refs=(terminal.execution_version_id,),
        classification="internal",
        access_scope="organization",
        provenance_refs=(
            producer,
            actor.actual_principal.principal_id,
            terminal.execution_subject_id,
            terminal.execution_version_id,
            admitted.document_id,
            admitted.version_id,
        ),
        integrity_metadata=(("manifest_sha256", manifest.manifest_sha256),),
        payload=(("external_actions", "false"), ("raw_document_bytes_platformized", "false")),
    )
    event_result = admit_event(receipt=receipt, execution=terminal, related_records=(admitted.canonical_record,))
    reconstruction_manifest = build_reconstruction_manifest(
        execution_versions=(v1, awaiting, ready, running, terminal),
        result_records=(admitted.canonical_record,),
        events=(event_result.event,),
    )
    pins = [reconstruction_manifest.workflow]
    pins.extend(reconstruction_manifest.material_inputs)
    pins.extend(reconstruction_manifest.gate_decisions)
    pins.extend(reconstruction_manifest.execution_versions)
    pins.extend(reconstruction_manifest.results)
    pins.extend(reconstruction_manifest.events)
    if reconstruction_manifest.product_contract is not None:
        pins.append(reconstruction_manifest.product_contract)
    version_ids = {pin.version_id for pin in pins}
    reconstruction = connection.adapters.capabilities.reconstruct_execution(
        request=CapabilityConsumptionRequest(
            organization=organization,
            product_id=connection.product_contract.product_id,
            product_version=connection.product_contract.product_version,
            dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RECONSTRUCT_EXECUTION,
            access=AccessRequest(actor, "review", "read", ("internal",)),
        ),
        governed_versions=governed_versions,
        manifest=reconstruction_manifest,
        evidence_constraints=tuple((version_id, "review", ("read",), "internal") for version_id in version_ids),
    )
    if not reconstruction.complete:
        raise P707Error("CAP-004 reconstruction is incomplete after operational admission")
    return admitted, terminal, event_result.event, reconstruction, decisions


def _external_authority_dict(value: ExternalAuthorityContract) -> dict[str, Any]:
    return {
        "authoritative_system": value.authoritative_system,
        "external_object_ref": value.external_object_ref,
        "authority_scope": value.authority_scope,
        "retrieval_or_sync": value.retrieval_or_sync,
        "freshness_expectation": value.freshness_expectation,
        "source_version_semantics": value.source_version_semantics,
        "conflict_rule": value.conflict_rule,
        "failure_behavior": value.failure_behavior,
        "permitted_transformations": list(value.permitted_transformations),
        "retention_deletion": value.retention_deletion,
        "portability": value.portability,
    }


def _external_authority_load(value: Mapping[str, Any]) -> ExternalAuthorityContract:
    required = {
        "authoritative_system", "external_object_ref", "authority_scope", "retrieval_or_sync",
        "freshness_expectation", "source_version_semantics", "conflict_rule", "failure_behavior",
        "permitted_transformations", "retention_deletion", "portability",
    }
    if not isinstance(value, Mapping) or set(value) != required:
        raise P707Error("persisted external-authority shape invalid")
    transforms = value["permitted_transformations"]
    if not isinstance(transforms, list) or any(not isinstance(item, str) for item in transforms):
        raise P707Error("persisted external-authority transformations invalid")
    return ExternalAuthorityContract(
        authoritative_system=str(value["authoritative_system"]),
        external_object_ref=str(value["external_object_ref"]),
        authority_scope=str(value["authority_scope"]),
        retrieval_or_sync=str(value["retrieval_or_sync"]),
        freshness_expectation=str(value["freshness_expectation"]),
        source_version_semantics=str(value["source_version_semantics"]),
        conflict_rule=str(value["conflict_rule"]),
        failure_behavior=str(value["failure_behavior"]),
        permitted_transformations=tuple(transforms),
        retention_deletion=str(value["retention_deletion"]),
        portability=str(value["portability"]),
    )


def _serialize_admitted(admitted: AdmittedDocumentVersion, manifest: VerifiedManifest) -> bytes:
    record = admitted.canonical_record
    external = record.external_authority
    if external is None:
        raise P707Error("operational External Reference lacks authority contract")
    value: dict[str, Any] = {
        "schema": PERSISTED_SCHEMA,
        "source_manifest_sha256": manifest.manifest_sha256,
        "record": {
            "subject_id": _id_dict(record.subject_id),
            "version_id": _id_dict(record.version_id),
            "semantic_type": record.semantic_type,
            "schema_version": record.schema_version,
            "organization_id": _id_dict(record.organization.organization_id),
            "authority_mode": record.authority_mode.value,
            "authority_scope": record.authority_scope,
            "accountable_owner_id": _id_dict(record.accountable_owner_id),
            "creation_actor_actual_principal_id": _id_dict(record.creation_actor.actual_principal.principal_id),
            "created_at": record.created_at.isoformat(),
            "provenance_refs": [_id_dict(item) for item in record.provenance_refs],
            "integrity_metadata": [list(item) for item in record.integrity_metadata],
            "payload": [list(item) for item in record.payload],
            "lifecycle_status": record.lifecycle_status,
            "external_authority": _external_authority_dict(external),
        },
        "artifacts": [
            {
                "artifact_id": _id_dict(item.artifact_id),
                "content_ref": item.content_ref,
                "media_type": item.media_type,
                "integrity_ref": item.integrity_ref,
                "rendition_role": item.rendition_role,
                "handling": {
                    "classification": item.handling.classification,
                    "purpose": item.handling.purpose,
                    "rights": list(item.handling.rights),
                    "retention_rule": item.handling.retention_rule,
                },
                "state": item.state.value,
                "source_artifact_ids": [_id_dict(source) for source in item.source_artifact_ids],
                "transformation": item.transformation,
                "storage_locator": item.storage_locator,
            }
            for item in admitted.artifacts
        ],
        "designated_rendition_role": admitted.designated_rendition_role,
        "raw_document_bytes_included": False,
        "reusable_secret_included": False,
        "external_actions": False,
    }
    return _canonical_json_bytes(value)


def _rehydrate_admitted(payload: bytes, *, connection) -> AdmittedDocumentVersion:
    if len(payload) <= 0 or len(payload) > MAX_ITEM_PAYLOAD_BYTES:
        raise P707Error("P7.07 persisted payload outside bounded size")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P707Error("P7.07 persisted payload invalid UTF-8 JSON") from exc
    if not isinstance(value, dict) or value.get("schema") != PERSISTED_SCHEMA:
        raise P707Error("P7.07 persisted payload schema mismatch")
    if value.get("source_manifest_sha256") != APPROVED_MANIFEST_SHA256:
        raise P707Error("P7.07 persisted payload lost exact source manifest")
    if value.get("raw_document_bytes_included") is not False or value.get("reusable_secret_included") is not False or value.get("external_actions") is not False:
        raise P707Error("P7.07 persisted minimization/effect boundary violated")
    raw_record = value.get("record")
    if not isinstance(raw_record, dict):
        raise P707Error("P7.07 persisted record missing")
    organization = connection.organization_scope
    actor = connection.actor_context
    if _id_load(raw_record.get("organization_id", {}), label="Organization") != organization.organization_id:
        raise P707Error("persisted record Organization differs from current P6.02 connection")
    owner = _id_load(raw_record.get("accountable_owner_id", {}), label="accountable owner")
    creation_actor_id = _id_load(raw_record.get("creation_actor_actual_principal_id", {}), label="creation actor")
    if owner != actor.actual_principal.principal_id or creation_actor_id != actor.actual_principal.principal_id:
        raise P707Error("persisted attributable actor continuity mismatch")
    try:
        created_at = datetime.fromisoformat(str(raw_record["created_at"]))
    except (KeyError, ValueError) as exc:
        raise P707Error("persisted created_at invalid") from exc
    if created_at.tzinfo is None or created_at.utcoffset() is None:
        raise P707Error("persisted created_at must be timezone-aware")
    provenance_raw = raw_record.get("provenance_refs")
    if not isinstance(provenance_raw, list) or not provenance_raw:
        raise P707Error("persisted provenance missing")
    integrity_raw = raw_record.get("integrity_metadata")
    payload_raw = raw_record.get("payload")
    if not isinstance(integrity_raw, list) or not isinstance(payload_raw, list):
        raise P707Error("persisted record metadata/payload shape invalid")
    external = _external_authority_load(raw_record.get("external_authority", {}))
    if external.authoritative_system != EXTERNAL_SOURCE_AUTHORITY:
        raise P707Error("persisted authoritative source is not EIS")
    record = CanonicalRecord(
        subject_id=_id_load(raw_record.get("subject_id", {}), label="Document Subject"),
        version_id=_id_load(raw_record.get("version_id", {}), label="Document Version"),
        semantic_type=str(raw_record.get("semantic_type", "")),
        schema_version=str(raw_record.get("schema_version", "")),
        organization=organization,
        authority_mode=AuthorityMode(str(raw_record.get("authority_mode", ""))),
        authority_scope=str(raw_record.get("authority_scope", "")),
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=tuple(_id_load(item, label="provenance") for item in provenance_raw),
        integrity_metadata=tuple(tuple(str(part) for part in item) for item in integrity_raw),
        payload=tuple(tuple(str(part) for part in item) for item in payload_raw),
        lifecycle_status=raw_record.get("lifecycle_status"),
        external_authority=external,
    )
    if record.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE or record.authority_scope != DOCUMENT_EXTERNAL_AUTHORITY_SCOPE:
        raise P707Error("rehydrated Document lost exact External Reference authority")
    if record.schema_version != PERSISTED_RECORD_SCHEMA:
        raise P707Error("rehydrated Document schema is not P7.07 operational schema")

    raw_artifacts = value.get("artifacts")
    if not isinstance(raw_artifacts, list) or len(raw_artifacts) != 1:
        raise P707Error("P7.07 operational payload must contain exactly one governed manifest Artifact")
    artifacts: list[ArtifactContent] = []
    for raw in raw_artifacts:
        if not isinstance(raw, dict) or raw.get("state") != ArtifactState.GOVERNED.value:
            raise P707Error("persisted operational Artifact state invalid")
        handling = raw.get("handling")
        if not isinstance(handling, dict):
            raise P707Error("persisted operational Artifact handling missing")
        rights = handling.get("rights")
        if not isinstance(rights, list):
            raise P707Error("persisted operational Artifact rights invalid")
        source_ids = raw.get("source_artifact_ids", [])
        if not isinstance(source_ids, list):
            raise P707Error("persisted source Artifact IDs invalid")
        artifact = ArtifactContent(
            artifact_id=_id_load(raw.get("artifact_id", {}), label="Artifact"),
            organization=organization,
            content_ref=str(raw.get("content_ref", "")),
            media_type=str(raw.get("media_type", "")),
            integrity_ref=str(raw.get("integrity_ref", "")),
            rendition_role=str(raw.get("rendition_role", "")),
            handling=HandlingConstraints(
                str(handling.get("classification", "")),
                str(handling.get("purpose", "")),
                tuple(str(item) for item in rights),
                str(handling.get("retention_rule", "")),
            ),
            state=ArtifactState.GOVERNED,
            source_artifact_ids=tuple(_id_load(item, label="source Artifact") for item in source_ids),
            transformation=raw.get("transformation"),
            storage_locator=raw.get("storage_locator"),
        )
        if artifact.handling.purpose != PERSISTED_PURPOSE or artifact.handling.classification != PERSISTED_CLASSIFICATION or artifact.handling.rights != ("read",):
            raise P707Error("rehydrated operational Artifact handling no longer matches Tender Operator read purpose")
        if artifact.integrity_ref != f"sha256:{APPROVED_MANIFEST_SHA256}":
            raise P707Error("rehydrated operational Artifact integrity lost approved manifest")
        artifacts.append(artifact)
    designated = value.get("designated_rendition_role")
    if designated != "evidence-manifest":
        raise P707Error("P7.07 designated rendition drifted")
    return AdmittedDocumentVersion(record, tuple(artifacts), str(designated))


def _metadata(admitted: AdmittedDocumentVersion, terminal, event, manifest: VerifiedManifest, release_sha: str) -> dict[str, Any]:
    record = admitted.canonical_record
    provenance = tuple(dict.fromkeys((
        _identity_text(record.accountable_owner_id),
        *(_identity_text(item) for item in record.provenance_refs),
        _identity_text(terminal.execution_subject_id),
        _identity_text(terminal.execution_version_id),
        _identity_text(event.record.subject_id),
        _identity_text(event.record.version_id),
        _identity_text(terminal.product_contract.subject_id) if terminal.product_contract else "",
        _identity_text(terminal.product_contract.version_id) if terminal.product_contract else "",
        f"sha256:{manifest.manifest_sha256}",
    )))
    provenance = tuple(item for item in provenance if item)
    return {
        "state_class": "canonical-governed-state",
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "semantic_type": record.semantic_type,
        "schema_version": record.schema_version,
        "classification": PERSISTED_CLASSIFICATION,
        "retention_policy_ref": PERSISTED_RETENTION,
        "source_release_sha": release_sha,
        "subject_identity": _identity_text(record.subject_id),
        "version_identity": _identity_text(record.version_id),
        "authority_mode": record.authority_mode.value,
        "authority_scope": record.authority_scope,
        "authoritative_source": EXTERNAL_SOURCE_AUTHORITY,
        "validation_status": "CAP-001 admitted; RFC-0006 provenance admitted; CAP-004 reconstruction complete",
        "governed_admission_ref": _identity_text(event.record.version_id),
        "provenance_refs": list(provenance),
        "source_manifest_sha256": manifest.manifest_sha256,
        "product_contract_version": "0.1.0",
        "operational_contour": "P7.07",
        "rehydratable_cap001_document": True,
        "canonical_authority": True,
        "contains_reusable_secret": False,
        "raw_document_bytes_included": False,
        "external_actions": False,
    }


def _find_existing(runtime_root: Path, *, subject_identity: str, version_identity: str):
    p703.verify_store(runtime_root)
    items = runtime_root.expanduser().resolve() / "state" / "governed" / "items"
    matches = []
    for child in sorted(items.iterdir()):
        manifest = p703.verify_item(child)
        metadata = manifest.get("metadata", {})
        if metadata.get("state_class") != "canonical-governed-state":
            continue
        if metadata.get("subject_identity") == subject_identity and metadata.get("version_identity") == version_identity:
            matches.append((child.name, manifest))
    if len(matches) > 1:
        raise P707Error("multiple retained P7.07 items claim the exact same Subject/Version")
    if not matches:
        return None
    item_id, manifest = matches[0]
    metadata = manifest["metadata"]
    expected = {
        "source_manifest_sha256": APPROVED_MANIFEST_SHA256,
        "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
        "authority_scope": DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        "authoritative_source": EXTERNAL_SOURCE_AUTHORITY,
        "product_contract_version": "0.1.0",
        "operational_contour": "P7.07",
        "rehydratable_cap001_document": True,
        "raw_document_bytes_included": False,
        "external_actions": False,
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            raise P707Error(f"retained exact P7.07 item conflicts on metadata field {key!r}")
    return item_id, manifest


def _persist(
    runtime_root: Path,
    release_sha: str,
    *,
    admitted: AdmittedDocumentVersion,
    terminal,
    event,
    manifest: VerifiedManifest,
) -> tuple[str, str]:
    payload = _serialize_admitted(admitted, manifest)
    item_id = p703.persist_governed_item(
        runtime_root,
        release_sha,
        payload,
        _metadata(admitted, terminal, event, manifest, release_sha),
    )
    verified = p703.verify_item(runtime_root.expanduser().resolve() / "state" / "governed" / "items" / item_id)
    if verified.get("payload_sha256") != _sha256_bytes(payload):
        raise P707Error("P7.03 persisted P7.07 payload verification mismatch")
    checkpoint_id = p703.create_checkpoint(
        runtime_root,
        release_sha,
        execution_subject_identity=_identity_text(terminal.execution_subject_id),
        execution_version_identity=_identity_text(terminal.execution_version_id),
        governed_storage_item_ids=(item_id,),
        classification=PERSISTED_CLASSIFICATION,
        retention_policy_ref=PERSISTED_RETENTION,
        reason="P7.07 Tender Operator operational exact-version admission",
    )
    return item_id, checkpoint_id


def _read_item_payload(runtime_root: Path, item_id: str) -> tuple[dict[str, Any], bytes]:
    item_dir = runtime_root.expanduser().resolve() / "state" / "governed" / "items" / item_id
    manifest = p703.verify_item(item_dir)
    metadata = manifest.get("metadata", {})
    if metadata.get("operational_contour") != "P7.07" or metadata.get("rehydratable_cap001_document") is not True:
        raise P707Error("configured item is not a P7.07 rehydratable operational document")
    path = _safe_private_regular_file(item_dir / "payload.bin", max_bytes=MAX_ITEM_PAYLOAD_BYTES, label="P7.07 payload")
    payload = path.read_bytes()
    if _sha256_bytes(payload) != manifest.get("payload_sha256"):
        raise P707Error("P7.07 payload digest mismatch after P7.03 verification")
    return metadata, payload


def _write_config(runtime_root: Path, *, item_id: str, subject_identity: str, version_identity: str) -> tuple[dict[str, Any], str]:
    read_resource = f"{READ_RESOURCE_PREFIX}{item_id}"
    value = {
        "schema": CONFIG_SCHEMA,
        "classification": "owner-local P7.07 operational routing; non-canonical",
        "operating_mode": "Persistent Internal / owner-operated",
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "product_id": "arvectum-tender-operator",
        "product_contract_version": "0.1.0",
        "storage_item_id": item_id,
        "subject_identity": subject_identity,
        "version_identity": version_identity,
        "read_operation": READ_ACCESS_OPERATION,
        "read_resource": read_resource,
        "access_path": ACCESS_PATH,
        "external_authority": EXTERNAL_SOURCE_AUTHORITY,
        "raw_document_bytes_required": False,
        "external_actions_enabled": False,
    }
    digest = _atomic_json(_config_path(runtime_root), value)
    return value, digest


def _load_config(runtime_root: Path) -> dict[str, Any]:
    path = _safe_private_regular_file(_config_path(runtime_root), max_bytes=128 * 1024, label="P7.07 config")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise P707Error("P7.07 config unreadable") from exc
    expected = {
        "schema": CONFIG_SCHEMA,
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "product_id": "arvectum-tender-operator",
        "product_contract_version": "0.1.0",
        "read_operation": READ_ACCESS_OPERATION,
        "access_path": ACCESS_PATH,
        "external_authority": EXTERNAL_SOURCE_AUTHORITY,
        "raw_document_bytes_required": False,
        "external_actions_enabled": False,
    }
    if not isinstance(value, dict):
        raise P707Error("P7.07 config must be JSON object")
    for key, expected_value in expected.items():
        if value.get(key) != expected_value:
            raise P707Error(f"P7.07 config field {key!r} invalid")
    item_id = value.get("storage_item_id")
    if not isinstance(item_id, str) or len(item_id) != 64 or any(ch not in "0123456789abcdef" for ch in item_id):
        raise P707Error("P7.07 config storage_item_id invalid")
    if value.get("read_resource") != f"{READ_RESOURCE_PREFIX}{item_id}":
        raise P707Error("P7.07 config read_resource is not exact item-scoped")
    return value


def _load_product_bridge(product_repo: Path, adapters) -> tuple[Any, str]:
    repo = product_repo.expanduser().resolve(strict=True)
    bridge_path = (repo / PRODUCT_BRIDGE_RELATIVE_PATH).resolve(strict=True)
    try:
        bridge_path.relative_to(repo)
    except ValueError as exc:
        raise P707Error("Tender Agent bridge escaped product repository") from exc
    if not bridge_path.is_file() or bridge_path.is_symlink():
        raise P707Error("Tender Agent product bridge missing/unsafe")
    module_name = f"arvectum_tender_agent_p707_bridge_{hashlib.sha256(str(bridge_path).encode()).hexdigest()[:12]}"
    spec = importlib.util.spec_from_file_location(module_name, bridge_path)
    if spec is None or spec.loader is None:
        raise P707Error("cannot load Tender Agent product bridge")
    module = importlib.util.module_from_spec(spec)
    assert isinstance(module, ModuleType)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    bridge_cls = getattr(module, PRODUCT_BRIDGE_CLASS, None)
    if bridge_cls is None:
        raise P707Error("Tender Agent product bridge class missing")
    bridge = bridge_cls(adapters)
    return bridge, _sha256_bytes(bridge_path.read_bytes())


def run_setup(
    *,
    runtime_root: Path,
    access_root: Path,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
    l7_manifest: Path,
    owner_approval: str,
    evidence_output: Path | None = None,
) -> SetupResult:
    if owner_approval != OWNER_APPROVAL_ASSERTION:
        raise P707Error("exact bounded P7.07 owner approval assertion is required")
    release_sha, repo_root = _verify_exact_release(runtime_root)
    organization, principal = _credential_owner_binding(
        access_root,
        state_file=state_file,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    setup_grant_id = p704.grant_access(
        access_root,
        principal,
        operation=SETUP_ACCESS_OPERATION,
        resource=SETUP_ACCESS_RESOURCE,
        access_paths=(ACCESS_PATH,),
    )
    setup_revoked = False
    try:
        setup_decision = _authorize_exact(
            access_root,
            organization=organization,
            principal=principal,
            credential_id=credential_id,
            credential_file=credential_file,
            operation=SETUP_ACCESS_OPERATION,
            resource=SETUP_ACCESS_RESOURCE,
        )
        rc, _lines, connection = connect_product(state_file, arvectum_repo_root=repo_root)
        if rc != 0 or connection is None:
            raise P707Error("P6.02 Product Contract connection/preflight failed")
        _verify_connection(connection, organization, principal)
        manifest = load_verified_manifest(l7_manifest)
        subject, version = _operational_identity_pair(connection)
        subject_text, version_text = _identity_text(subject), _identity_text(version)
        existing = _find_existing(runtime_root, subject_identity=subject_text, version_identity=version_text)
        checkpoint_id: str | None = None
        idempotent = existing is not None
        if existing is None:
            admitted, terminal, event, reconstruction, decisions = _run_governed_admission(
                connection, manifest, base_time=datetime.now(UTC)
            )
            if len(decisions) != 4 or {decision.kind for decision in decisions} != {
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            }:
                raise P707Error("P7.07 did not preserve four distinct gate decisions")
            item_id, checkpoint_id = _persist(
                runtime_root,
                release_sha,
                admitted=admitted,
                terminal=terminal,
                event=event,
                manifest=manifest,
            )
            reconstruction_complete = bool(reconstruction.complete)
        else:
            item_id = existing[0]
            reconstruction_complete = True
            _metadata_existing, payload_existing = _read_item_payload(runtime_root, item_id)
            _rehydrate_admitted(payload_existing, connection=connection)

        config, config_sha = _write_config(
            runtime_root,
            item_id=item_id,
            subject_identity=subject_text,
            version_identity=version_text,
        )
        read_grant_id = p704.grant_access(
            access_root,
            principal,
            operation=READ_ACCESS_OPERATION,
            resource=config["read_resource"],
            access_paths=(ACCESS_PATH,),
        )
        read_decision = _authorize_exact(
            access_root,
            organization=organization,
            principal=principal,
            credential_id=credential_id,
            credential_file=credential_file,
            operation=READ_ACCESS_OPERATION,
            resource=config["read_resource"],
        )
        if read_decision.grant_id != read_grant_id:
            raise P707Error("P7.04 exact persistent read grant selection drifted")
        p703_status = p703.verify_store(runtime_root)
        if p703_status.get("integrity") != "PASS":
            raise P707Error("P7.03 store integrity failed after P7.07 setup")
    finally:
        try:
            p704.revoke_grant(access_root, setup_grant_id)
            setup_revoked = True
        except Exception:
            setup_revoked = False
    if not setup_revoked:
        raise P707Error("temporary P7.07 setup grant could not be revoked")

    if evidence_output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        evidence_output = runtime_root.expanduser().resolve() / "evidence" / "p7-07" / f"setup-{stamp}.json"
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "stage": "setup",
        "status": "PASS_IDEMPOTENT_EXISTING" if idempotent else "PASS_ADMITTED_AND_CONFIGURED",
        "release_sha": release_sha,
        "owner_decision": OWNER_DECISION_PATH,
        "owner_approval_assertion_present": True,
        "manifest_sha256": manifest.manifest_sha256,
        "notice_number": NOTICE_NUMBER,
        "organization_context_reused": True,
        "human_principal_reused": True,
        "setup_authorization_allowed": setup_decision.allowed,
        "temporary_setup_grant_revoked": True,
        "persistent_read_grant_configured": True,
        "read_authorization_allowed": read_decision.allowed,
        "p7_04_satisfies_organizational_authority": False,
        "p7_04_satisfies_consequential_approval": False,
        "product_contract_version": "0.1.0",
        "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
        "authoritative_source": EXTERNAL_SOURCE_AUTHORITY,
        "subject_identity": subject_text,
        "version_identity": version_text,
        "storage_item_id": item_id,
        "checkpoint_id": checkpoint_id,
        "idempotent_existing_item": idempotent,
        "reconstruction_complete": reconstruction_complete,
        "config_sha256": config_sha,
        "p7_03_integrity": p703_status.get("integrity"),
        "network_invoked": False,
        "eis_or_soap_invoked": False,
        "external_actions": False,
        "raw_document_bytes_persisted": False,
        "reusable_secret_persisted": False,
        "credential_secret_exposed": False,
    }
    _atomic_json(evidence_output, evidence)
    return SetupResult(
        status=evidence["status"],
        release_sha=release_sha,
        storage_item_id=item_id,
        checkpoint_id=checkpoint_id,
        subject_identity=subject_text,
        version_identity=version_text,
        read_resource=config["read_resource"],
        idempotent_existing_item=idempotent,
        reconstruction_complete=reconstruction_complete,
        evidence_path=str(evidence_output),
    )


def run_consume(
    *,
    runtime_root: Path,
    access_root: Path,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
    product_repo: Path,
    evidence_output: Path | None = None,
    bridge: Any | None = None,
) -> ConsumptionResult:
    release_sha, repo_root = _verify_exact_release(runtime_root)
    organization, principal = _credential_owner_binding(
        access_root,
        state_file=state_file,
        credential_id=credential_id,
        credential_file=credential_file,
    )
    rc, _lines, connection = connect_product(state_file, arvectum_repo_root=repo_root)
    if rc != 0 or connection is None:
        raise P707Error("P6.02 Product Contract connection/preflight failed")
    _verify_connection(connection, organization, principal)
    config = _load_config(runtime_root)
    access_decision = _authorize_exact(
        access_root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
        operation=READ_ACCESS_OPERATION,
        resource=config["read_resource"],
    )
    metadata, payload = _read_item_payload(runtime_root, config["storage_item_id"])
    if metadata.get("subject_identity") != config.get("subject_identity") or metadata.get("version_identity") != config.get("version_identity"):
        raise P707Error("P7.07 config and exact governed item identities diverged")
    admitted = _rehydrate_admitted(payload, connection=connection)
    if _identity_text(admitted.document_id) != config["subject_identity"] or _identity_text(admitted.version_id) != config["version_identity"]:
        raise P707Error("rehydrated CAP-001 exact identities diverged from P7.07 config")

    bridge_sha = "injected-test-bridge"
    if bridge is None:
        bridge, bridge_sha = _load_product_bridge(product_repo, connection.adapters)
    request = CapabilityConsumptionRequest(
        organization=connection.organization_scope,
        product_id=connection.product_contract.product_id,
        product_version=connection.product_contract.product_version,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RESOLVE_DOCUMENT,
        access=AccessRequest(connection.actor_context, PERSISTED_PURPOSE, "read", (PERSISTED_CLASSIFICATION,)),
    )
    artifact = admitted.artifacts[0]
    reliance = bridge.resolve_document(
        request=request,
        governed_versions=_governed_versions(),
        admitted=admitted,
        artifact_id=artifact.artifact_id,
    )
    if reliance.document_id != admitted.document_id or reliance.document_version_id != admitted.version_id:
        raise P707Error("Tender Agent CAP-001 bridge did not preserve exact Subject/Version reliance")
    if reliance.artifact_id != artifact.artifact_id or reliance.integrity_ref != f"sha256:{APPROVED_MANIFEST_SHA256}":
        raise P707Error("Tender Agent CAP-001 bridge did not preserve exact governed Artifact integrity")
    if reliance.handling.purpose != PERSISTED_PURPOSE or reliance.handling.rights != ("read",) or reliance.handling.classification != PERSISTED_CLASSIFICATION:
        raise P707Error("Tender Agent CAP-001 reliance lost exact handling constraints")
    external = admitted.canonical_record.external_authority
    if external is None or external.authoritative_system != EXTERNAL_SOURCE_AUTHORITY:
        raise P707Error("Tender Agent operational reliance lost EIS external authority")
    p703_status = p703.verify_store(runtime_root)
    if p703_status.get("integrity") != "PASS":
        raise P707Error("P7.03 store integrity failed after read-only Tender Operator reliance")

    if evidence_output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        evidence_output = runtime_root.expanduser().resolve() / "evidence" / "p7-07" / f"consume-{stamp}.json"
    evidence = {
        "schema": EVIDENCE_SCHEMA,
        "stage": "consume",
        "status": "PASS_EXACT_CAP001_RELIANCE",
        "release_sha": release_sha,
        "storage_item_id": config["storage_item_id"],
        "subject_identity": _identity_text(reliance.document_id),
        "version_identity": _identity_text(reliance.document_version_id),
        "artifact_identity": _identity_text(reliance.artifact_id),
        "integrity_ref": reliance.integrity_ref,
        "handling_purpose": reliance.handling.purpose,
        "handling_rights": list(reliance.handling.rights),
        "classification": reliance.handling.classification,
        "p7_04_authorization_allowed": access_decision.allowed,
        "p7_04_satisfies_organizational_authority": False,
        "p7_04_satisfies_consequential_approval": False,
        "product_contract_version": "0.1.0",
        "product_bridge_file_sha256": bridge_sha,
        "authority_mode": admitted.canonical_record.authority_mode.value,
        "authoritative_source": external.authoritative_system,
        "p7_03_integrity": p703_status.get("integrity"),
        "canonical_mutation": False,
        "network_invoked_by_contour": False,
        "eis_or_soap_invoked_by_contour": False,
        "external_actions": False,
        "raw_document_bytes_exposed": False,
        "credential_secret_exposed": False,
    }
    _atomic_json(evidence_output, evidence)
    return ConsumptionResult(
        status=evidence["status"],
        release_sha=release_sha,
        storage_item_id=config["storage_item_id"],
        subject_identity=evidence["subject_identity"],
        version_identity=evidence["version_identity"],
        artifact_identity=evidence["artifact_identity"],
        integrity_ref=reliance.integrity_ref,
        authoritative_source=external.authoritative_system,
        product_contract_version="0.1.0",
        evidence_path=str(evidence_output),
    )


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--access-root", type=Path, required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--evidence-output", type=Path)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    setup = sub.add_parser("setup", help="one owner-approved governed operational admission + persistent read grant")
    _common(setup)
    setup.add_argument("--l7-manifest", type=Path, required=True)
    setup.add_argument("--owner-approval", required=True)
    consume = sub.add_parser("consume", help="repeatable read-only Tender Operator CAP-001 reliance")
    _common(consume)
    consume.add_argument("--product-repo", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "setup":
            result = run_setup(
                runtime_root=args.runtime_root,
                access_root=args.access_root,
                state_file=args.state_file,
                credential_id=args.credential_id,
                credential_file=args.credential_file,
                l7_manifest=args.l7_manifest,
                owner_approval=args.owner_approval,
                evidence_output=args.evidence_output,
            )
            print(f"RESULT={result.status}")
            print(f"RELEASE_SHA={result.release_sha}")
            print(f"STORAGE_ITEM_ID={result.storage_item_id}")
            print(f"CHECKPOINT_ID={result.checkpoint_id or 'NONE'}")
            print(f"IDEMPOTENT_EXISTING_ITEM={str(result.idempotent_existing_item).lower()}")
            print(f"RECONSTRUCTION_COMPLETE={str(result.reconstruction_complete).lower()}")
            print(f"EVIDENCE_PATH={result.evidence_path}")
        else:
            result = run_consume(
                runtime_root=args.runtime_root,
                access_root=args.access_root,
                state_file=args.state_file,
                credential_id=args.credential_id,
                credential_file=args.credential_file,
                product_repo=args.product_repo,
                evidence_output=args.evidence_output,
            )
            print(f"RESULT={result.status}")
            print(f"RELEASE_SHA={result.release_sha}")
            print(f"STORAGE_ITEM_ID={result.storage_item_id}")
            print(f"SUBJECT={result.subject_identity}")
            print(f"VERSION={result.version_identity}")
            print(f"ARTIFACT={result.artifact_identity}")
            print(f"EVIDENCE_PATH={result.evidence_path}")
        print("PRODUCT_CONTRACT_VERSION=0.1.0")
        print("EIS_AUTHORITY_PRESERVED=true")
        print("NETWORK_INVOKED=false")
        print("EXTERNAL_ACTIONS=false")
        print("RAW_DOCUMENT_BYTES_EXPOSED=false")
        return 0
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
