#!/usr/bin/env python3
"""P7.06-UI1 bounded first-real-governed-item admission/persistence bridge.

This module exists only to unblock the remaining selected-Mac UI1 proof with one
real retained governed item. It is intentionally narrow:

* execute only from the exact active P7.06 release;
* reuse the existing P6.05-L4 Organization/human Actor context;
* require an exact P7.04 human local grant before protected evidence/admission;
* pin the existing P6.02 Provisional Product Contract 0.1.0;
* independently verify the already-retained P6.05-L7 exact EIS evidence manifest;
* keep Authorization, Organizational Authority, Data Governance and
  Consequential Approval as separate RFC-0005 decisions;
* admit one External Reference Document Version through the existing CAP-001 seam;
* preserve RFC-0006 admission Event/provenance and CAP-004 reconstruction;
* persist only the admitted minimized governed representation through P7.03;
* create no EIS/network/product/external effect and store no raw tender bytes.

The adapter is private, reversible, internal and non-stable. It creates no new
Product Contract version, capability lifecycle transition, public API or general
canonical-write authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Final, Mapping

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
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
    CapabilityConsumptionRequest,
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.workflow import OperationSideEffectClass, WorkflowDefinition, WorkflowOperation
from p6_03_tender_operator_ref.contract import DOCUMENT_EXTERNAL_AUTHORITY_SCOPE
from p6_05_l5_first_real_product_connection import GOVERNANCE_REFERENCE, connect_product
from p6_05_tender_attachment_ref.contract import OP_ADMIT_DOCUMENT_VERSION
import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_06_governed_deploy as p706

UTC = timezone.utc

OWNER_DECISION_PATH: Final = (
    "docs/governance/decisions/"
    "DECISION-2026-08-18-P7-06-UI1-FIRST-REAL-GOVERNED-ITEM-ADMISSION.md"
)
OWNER_APPROVAL_ASSERTION: Final = "OWNER_APPROVES_P7_06_UI1_FIRST_REAL_GOVERNED_ITEM_ADMISSION"
NOTICE_NUMBER: Final = "0344100006426000005"
APPROVED_MANIFEST_SHA256: Final = "74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121"
MANIFEST_SCHEMA: Final = "p6.05-exact-attachment-evidence-v1"
MANIFEST_PURPOSE: Final = "exact-tender-attachment-evidence"
MANIFEST_STATUS: Final = "PASS_EXACT_ATTACHMENT_EVIDENCE"
EXTERNAL_SOURCE_AUTHORITY: Final = "ЕИС / zakupki.gov.ru"
EXPECTED_DOCUMENT_COUNT: Final = 7
MAX_MANIFEST_BYTES: Final = 2 * 1024 * 1024

ACCESS_OPERATION: Final = "governed.item.admit"
ACCESS_RESOURCE: Final = "p7-06-ui1:first-real-governed-item"
ACCESS_PATH: Final = "local"

PERSISTED_SCHEMA: Final = "arvectum.p7_06.ui1-real-governed-document/1"
PERSISTED_CLASSIFICATION: Final = "restricted-pilot"
PERSISTED_RETENTION: Final = "P6.02 restricted-paid-pilot / inherit-product-source-retention"


class UI1RealStateAdmissionError(RuntimeError):
    """Fail-closed bounded admission/persistence error."""


@dataclass(frozen=True, slots=True)
class VerifiedManifest:
    value: Mapping[str, Any]
    manifest_sha256: str
    source_version: str
    retrieved_at: datetime


@dataclass(frozen=True, slots=True)
class AdmissionResult:
    status: str
    release_sha: str
    storage_item_id: str
    checkpoint_id: str | None
    subject_identity: str
    version_identity: str
    manifest_sha256: str
    idempotent_existing_item: bool
    reconstruction_complete: bool
    evidence_path: str


def _identity_text(value: Identity) -> str:
    if not isinstance(value, Identity):
        raise UI1RealStateAdmissionError("identity value required")
    return f"{value.namespace}/{value.value}@{value.scope}"


def _id(namespace: str, value: str, scope: str) -> Identity:
    return Identity(namespace, value, scope)


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_private_regular_file(path: Path, *, max_bytes: int, label: str) -> Path:
    path = path.expanduser()
    if path.is_symlink():
        raise UI1RealStateAdmissionError(f"{label} must not be a symlink")
    try:
        resolved = path.resolve(strict=True)
    except (FileNotFoundError, OSError) as exc:
        raise UI1RealStateAdmissionError(f"{label} is missing or unreadable") from exc
    if not resolved.is_file():
        raise UI1RealStateAdmissionError(f"{label} must be a regular file")
    try:
        size = resolved.stat().st_size
    except OSError as exc:
        raise UI1RealStateAdmissionError(f"{label} metadata unavailable") from exc
    if size <= 0 or size > max_bytes:
        raise UI1RealStateAdmissionError(f"{label} size outside bounded limit")
    if os.name != "nt" and (resolved.stat().st_mode & 0o077):
        raise UI1RealStateAdmissionError(f"{label} must be owner-only")
    return resolved


def _verify_owner_decision(repo_root: Path) -> None:
    path = (repo_root / OWNER_DECISION_PATH).resolve()
    try:
        path.relative_to(repo_root.resolve())
    except ValueError as exc:
        raise UI1RealStateAdmissionError("owner decision escaped exact release source") from exc
    if not path.is_file() or path.is_symlink():
        raise UI1RealStateAdmissionError("approved owner decision missing from exact release")
    text = path.read_text(encoding="utf-8")
    required = (
        "Status: `Approved`",
        OWNER_APPROVAL_ASSERTION,
        APPROVED_MANIFEST_SHA256,
        "Authorization",
        "Organizational Authority",
        "Data Governance",
        "Consequential Approval",
    )
    if any(value not in text for value in required):
        raise UI1RealStateAdmissionError("owner decision does not preserve required bounded approval")


def _verify_exact_release(runtime_root: Path) -> tuple[str, Path]:
    root = runtime_root.expanduser().resolve()
    release_sha = p706.current_release(root)
    p706.verify_release(root, release_sha)
    expected = (
        root
        / "releases"
        / release_sha
        / "source"
        / "reference"
        / "python"
        / Path(__file__).name
    )
    if Path(__file__).resolve() != expected.resolve():
        raise UI1RealStateAdmissionError(
            "real-state admission must run from the exact active release, not a mutable working tree"
        )
    repo_root = expected.parents[2]
    _verify_owner_decision(repo_root)
    return release_sha, repo_root


def _authorize_operator(
    *,
    access_root: Path,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
) -> tuple[Identity, Identity, p704.AccessDecision]:
    organization, principal = p704.load_p6_owner_context(state_file)
    decision = p704.authorize_from_credential_file(
        access_root,
        organization=organization,
        principal=principal,
        credential_id=credential_id,
        credential_file=credential_file,
        operation=ACCESS_OPERATION,
        resource=ACCESS_RESOURCE,
        access_path=ACCESS_PATH,
    )
    if not decision.allowed:
        raise UI1RealStateAdmissionError(f"P7.04 authorization denied: {decision.reason}")
    if decision.principal_kind != "human":
        raise UI1RealStateAdmissionError("bounded admission requires the attributable human operator")
    if decision.organizational_authority_satisfied or decision.consequential_approval_satisfied:
        raise UI1RealStateAdmissionError("P7.04 access must not satisfy authority or consequential approval")
    return organization, principal, decision


def load_verified_manifest(path: Path) -> VerifiedManifest:
    resolved = _safe_private_regular_file(path, max_bytes=MAX_MANIFEST_BYTES, label="P6.05-L7 manifest")
    try:
        value = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise UI1RealStateAdmissionError("P6.05-L7 manifest is not readable UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise UI1RealStateAdmissionError("P6.05-L7 manifest must be a JSON object")

    manifest_sha = value.get("manifest_sha256")
    integrity_ref = value.get("manifest_integrity_ref")
    if manifest_sha != APPROVED_MANIFEST_SHA256 or integrity_ref != f"sha256:{APPROVED_MANIFEST_SHA256}":
        raise UI1RealStateAdmissionError("P6.05-L7 manifest is not the owner-approved exact manifest")

    body = dict(value)
    body.pop("manifest_sha256", None)
    body.pop("manifest_integrity_ref", None)
    if _sha256_bytes(_canonical_json_bytes(body)) != APPROVED_MANIFEST_SHA256:
        raise UI1RealStateAdmissionError("P6.05-L7 manifest body integrity mismatch")

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
            raise UI1RealStateAdmissionError(f"P6.05-L7 manifest field {key!r} mismatches approved evidence")
    documents = value.get("documents")
    if not isinstance(documents, list) or len(documents) != EXPECTED_DOCUMENT_COUNT:
        raise UI1RealStateAdmissionError("P6.05-L7 manifest document set is incomplete")
    if any(not isinstance(item, dict) for item in documents):
        raise UI1RealStateAdmissionError("P6.05-L7 manifest document entries malformed")
    if any("sha256" not in item or "size_bytes" not in item for item in documents):
        raise UI1RealStateAdmissionError("P6.05-L7 manifest lacks exact byte-integrity evidence")

    source_version = value.get("external_source_version")
    if not isinstance(source_version, str) or not source_version.strip():
        raise UI1RealStateAdmissionError("P6.05-L7 manifest lacks exact external source version")
    retrieved_raw = value.get("retrieved_at")
    if not isinstance(retrieved_raw, str):
        raise UI1RealStateAdmissionError("P6.05-L7 manifest retrieval timestamp missing")
    try:
        retrieved_at = datetime.fromisoformat(retrieved_raw)
    except ValueError as exc:
        raise UI1RealStateAdmissionError("P6.05-L7 manifest retrieval timestamp invalid") from exc
    if retrieved_at.tzinfo is None or retrieved_at.utcoffset() is None:
        raise UI1RealStateAdmissionError("P6.05-L7 manifest retrieval timestamp must be timezone-aware")
    return VerifiedManifest(value, manifest_sha, source_version.strip(), retrieved_at)


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


def _build_candidate_and_interaction(connection, manifest: VerifiedManifest, *, base_time: datetime):
    organization = connection.organization_scope
    actor = connection.actor_context
    contract = connection.product_contract
    scope = organization.organization_id.value
    suffix = APPROVED_MANIFEST_SHA256[:16]
    execution_subject = _id("execution-subject", f"p7-06-ui1-real-state-{suffix}", scope)
    document_subject = _id("document-subject", f"eis-{NOTICE_NUMBER}-exact-attachment-evidence", scope)
    document_version = _id("document-version", f"eis-{NOTICE_NUMBER}-{suffix}", scope)

    authority = ExternalAuthorityContract(
        authoritative_system=EXTERNAL_SOURCE_AUTHORITY,
        external_object_ref=f"44fz-notice:{NOTICE_NUMBER}",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync=(
            "reuse already-retained read-only P6.05-L7 exact evidence; no EIS/SOAP/network retrieval "
            "is authorized by this admission"
        ),
        freshness_expectation="exact retained external source version pinned by P6.05-L7 manifest",
        source_version_semantics=(
            "EIS getDocsIP source version plus complete purpose-scoped seven-document manifest and exact digests"
        ),
        conflict_rule="ЕИС / zakupki.gov.ru remains authoritative; digest/version mismatch fails closed",
        failure_behavior="missing, changed or unverifiable retained evidence blocks canonical admission",
        permitted_transformations=("integrity hashing", "manifest generation", "governed reference admission"),
        retention_deletion="inherit P6.02 restricted-paid-pilot product/source retention rules",
        portability="export governed external reference, exact manifest digest and provenance without credentials",
    )
    record = CanonicalRecord(
        subject_id=document_subject,
        version_id=document_version,
        semantic_type="platform.document",
        schema_version="p7.06-ui1-real-eis-evidence-1",
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
        ),
        payload=(
            ("purpose", MANIFEST_PURPOSE),
            ("notice_number", NOTICE_NUMBER),
            ("completeness", "complete-for-declared-p6.05-proof-purpose"),
            ("manifest_integrity_ref", f"sha256:{manifest.manifest_sha256}"),
        ),
        lifecycle_status="AdmissionCandidate",
        external_authority=authority,
    )
    artifact = ArtifactContent(
        artifact_id=_id("artifact", f"exact-attachment-evidence-manifest-{suffix}", scope),
        organization=organization,
        content_ref=f"retained-evidence-manifest://sha256/{manifest.manifest_sha256}",
        media_type="application/json",
        integrity_ref=f"sha256:{manifest.manifest_sha256}",
        rendition_role="evidence-manifest",
        handling=HandlingConstraints(
            PERSISTED_CLASSIFICATION,
            "prebid-evidence-admission",
            ("read",),
            "inherit-product-source-retention",
        ),
    )
    candidate = DocumentVersionCandidate(record, (artifact,), "evidence-manifest")

    workflow_record = CanonicalRecord(
        subject_id=_id("workflow-subject", "p7-06-ui1-first-real-governed-item-admission", scope),
        version_id=_id("workflow-version", "p7-06-ui1-first-real-governed-item-admission-v1", scope),
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
            document_subject,
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
                target_subject_id=document_subject,
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
    if kind is GovernedGateKind.AUTHORIZATION:
        return _id("authorization-basis", "p7-04-exact-human-local-admission-grant", scope)
    if kind is GovernedGateKind.ORGANIZATIONAL_AUTHORITY:
        return _id("organizational-authority-basis", "decision-2026-08-18-ui1-real-state-admission", scope)
    if kind is GovernedGateKind.DATA_GOVERNANCE:
        return _id("data-governance-basis", f"p6-02-v0.1.0+p6-05-l7-{APPROVED_MANIFEST_SHA256[:16]}", scope)
    if kind is GovernedGateKind.CONSEQUENTIAL_APPROVAL:
        return _id("consequential-approval-basis", "decision-2026-08-18-ui1-real-state-admission", scope)
    raise UI1RealStateAdmissionError(f"unexpected gate kind: {kind.value}")


def _run_governed_admission(connection, manifest: VerifiedManifest, *, base_time: datetime):
    actor = connection.actor_context
    organization = connection.organization_scope
    scope = organization.organization_id.value
    candidate, interaction, execution_subject = _build_candidate_and_interaction(
        connection, manifest, base_time=base_time
    )
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
        raise UI1RealStateAdmissionError("Governed Execution required-gate set drifted")

    decisions = []
    for index, kind in enumerate(awaiting.required_gates, start=1):
        decisions.append(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=actor,
                basis_ref=_gate_basis(kind, scope),
                decision_id=_id("gate-decision-subject", f"{execution_subject.value}-{kind.value}", scope),
                version_id=_id("gate-decision-version", f"{execution_subject.value}-{kind.value}-v1", scope),
                created_at=base_time + timedelta(microseconds=2 + index),
            )
        )
    ready = admit_ready_execution(
        awaiting,
        decisions=tuple(decisions),
        version_id=_id("execution-version", f"{execution_subject.value}-v3", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=7),
    )
    admitted = connection.adapters.capabilities.admit_document_version(
        execution=ready,
        candidate=candidate,
    )
    if admitted.version_id != candidate.canonical_record.version_id:
        raise UI1RealStateAdmissionError("CAP-001 admission did not preserve exact Document Version identity")
    if admitted.canonical_record.authority_mode is not AuthorityMode.EXTERNAL_REFERENCE:
        raise UI1RealStateAdmissionError("CAP-001 admission lost External Reference authority")
    if len(admitted.artifacts) != 1 or admitted.artifacts[0].state is not ArtifactState.GOVERNED:
        raise UI1RealStateAdmissionError("CAP-001 admission did not govern the exact evidence manifest Artifact")
    if admitted.artifacts[0].integrity_ref != f"sha256:{manifest.manifest_sha256}":
        raise UI1RealStateAdmissionError("CAP-001 admitted Artifact lost exact manifest integrity reference")

    running = transition_governed_execution(
        ready,
        lifecycle=GovernedExecutionLifecycle.RUNNING,
        version_id=_id("execution-version", f"{execution_subject.value}-v4", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=8),
    )
    terminal = transition_governed_execution(
        running,
        lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
        version_id=_id("execution-version", f"{execution_subject.value}-v5", scope),
        actor=actor,
        created_at=base_time + timedelta(microseconds=9),
        additional_provenance_refs=(admitted.document_id, admitted.version_id),
    )

    producer = _id("producer", "platform.core", scope)
    event_receipt = EventReceipt(
        event_id=_id("event-subject", f"p7-06-ui1-document-admitted-{APPROVED_MANIFEST_SHA256[:16]}", scope),
        version_id=_id("event-version", f"p7-06-ui1-document-admitted-{APPROVED_MANIFEST_SHA256[:16]}-v1", scope),
        event_type="p7.06-ui1.document-admitted",
        event_schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.document/admission",
        authoritative_source="platform.core",
        occurred_at=base_time + timedelta(microseconds=10),
        recorded_at=base_time + timedelta(microseconds=11),
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
    event_result = admit_event(
        receipt=event_receipt,
        execution=terminal,
        related_records=(admitted.canonical_record,),
    )

    reconstruction_manifest = build_reconstruction_manifest(
        execution_versions=(v1, awaiting, ready, running, terminal),
        result_records=(admitted.canonical_record,),
        events=(event_result.event,),
    )
    if not reconstruction_manifest.material_inputs or not reconstruction_manifest.results:
        raise UI1RealStateAdmissionError("reconstruction manifest lost material-input/result evidence")
    if reconstruction_manifest.material_inputs[0].version_id != admitted.version_id:
        raise UI1RealStateAdmissionError("reconstruction material input lost exact admitted Version")
    if reconstruction_manifest.results[0].version_id != admitted.version_id:
        raise UI1RealStateAdmissionError("reconstruction result lost exact admitted Version")

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
            access=AccessRequest(
                actor=actor,
                purpose="review",
                required_right="read",
                allowed_classifications=("internal",),
            ),
        ),
        governed_versions=governed_versions,
        manifest=reconstruction_manifest,
        evidence_constraints=tuple((version_id, "review", ("read",), "internal") for version_id in version_ids),
    )
    if not reconstruction.complete:
        raise UI1RealStateAdmissionError("CAP-004 reconstruction is incomplete")
    return admitted, terminal, event_result.event, reconstruction, tuple(decisions)


def _persisted_payload(admitted, terminal, event, manifest: VerifiedManifest) -> bytes:
    record = admitted.canonical_record
    external = record.external_authority
    if external is None:
        raise UI1RealStateAdmissionError("admitted External Reference lacks authority contract")
    payload = {
        "schema": PERSISTED_SCHEMA,
        "subject_identity": _identity_text(record.subject_id),
        "version_identity": _identity_text(record.version_id),
        "semantic_type": record.semantic_type,
        "schema_version": record.schema_version,
        "authority_mode": record.authority_mode.value,
        "authority_scope": record.authority_scope,
        "authoritative_system": external.authoritative_system,
        "external_object_ref": external.external_object_ref,
        "manifest_sha256": manifest.manifest_sha256,
        "member_count": EXPECTED_DOCUMENT_COUNT,
        "product_contract_subject": _identity_text(terminal.product_contract.subject_id) if terminal.product_contract else None,
        "product_contract_version": _identity_text(terminal.product_contract.version_id) if terminal.product_contract else None,
        "execution_subject": _identity_text(terminal.execution_subject_id),
        "execution_version": _identity_text(terminal.execution_version_id),
        "event_subject": _identity_text(event.record.subject_id),
        "event_version": _identity_text(event.record.version_id),
        "provenance_refs": [_identity_text(item) for item in record.provenance_refs],
        "artifact_integrity_refs": [item.integrity_ref for item in admitted.artifacts],
        "raw_document_bytes_included": False,
        "reusable_secret_included": False,
        "external_actions": False,
    }
    return _canonical_json_bytes(payload)


def _target_identity_pair(connection) -> tuple[str, str]:
    scope = connection.organization_scope.organization_id.value
    suffix = APPROVED_MANIFEST_SHA256[:16]
    return (
        _identity_text(_id("document-subject", f"eis-{NOTICE_NUMBER}-exact-attachment-evidence", scope)),
        _identity_text(_id("document-version", f"eis-{NOTICE_NUMBER}-{suffix}", scope)),
    )


def _find_existing_exact_item(runtime_root: Path, *, subject_identity: str, version_identity: str):
    p703.verify_store(runtime_root)
    items_root = runtime_root.expanduser().resolve() / "state" / "governed" / "items"
    matches = []
    for child in sorted(items_root.iterdir()):
        manifest = p703.verify_item(child)
        metadata = manifest.get("metadata", {})
        if metadata.get("state_class") != "canonical-governed-state":
            continue
        if metadata.get("subject_identity") == subject_identity and metadata.get("version_identity") == version_identity:
            matches.append((child.name, manifest))
    if len(matches) > 1:
        raise UI1RealStateAdmissionError("multiple retained items claim the exact same Subject/Version")
    if not matches:
        return None
    item_id, manifest = matches[0]
    metadata = manifest["metadata"]
    if metadata.get("source_manifest_sha256") != APPROVED_MANIFEST_SHA256:
        raise UI1RealStateAdmissionError("retained exact Subject/Version conflicts with approved source manifest")
    if metadata.get("authority_mode") != AuthorityMode.EXTERNAL_REFERENCE.value:
        raise UI1RealStateAdmissionError("retained exact Subject/Version conflicts with External Reference authority")
    return item_id, manifest


def _persist_after_admission(
    runtime_root: Path,
    release_sha: str,
    *,
    admitted,
    terminal,
    event,
    manifest: VerifiedManifest,
) -> tuple[str, str]:
    provenance = tuple(
        dict.fromkeys(
            (
                _identity_text(admitted.canonical_record.accountable_owner_id),
                _identity_text(terminal.execution_subject_id),
                _identity_text(terminal.execution_version_id),
                _identity_text(event.record.subject_id),
                _identity_text(event.record.version_id),
                *(
                    (_identity_text(terminal.product_contract.subject_id), _identity_text(terminal.product_contract.version_id))
                    if terminal.product_contract is not None
                    else ()
                ),
                f"sha256:{manifest.manifest_sha256}",
            )
        )
    )
    metadata = {
        "state_class": "canonical-governed-state",
        "organization_scope": p703.ORGANIZATION_SCOPE,
        "semantic_type": admitted.canonical_record.semantic_type,
        "schema_version": admitted.canonical_record.schema_version,
        "classification": PERSISTED_CLASSIFICATION,
        "retention_policy_ref": PERSISTED_RETENTION,
        "source_release_sha": release_sha,
        "subject_identity": _identity_text(admitted.document_id),
        "version_identity": _identity_text(admitted.version_id),
        "authority_mode": admitted.canonical_record.authority_mode.value,
        "authority_scope": admitted.canonical_record.authority_scope,
        "authoritative_source": EXTERNAL_SOURCE_AUTHORITY,
        "validation_status": "CAP-001 admitted; RFC-0006 provenance admitted; CAP-004 reconstruction complete",
        "governed_admission_ref": _identity_text(event.record.version_id),
        "provenance_refs": list(provenance),
        "source_manifest_sha256": manifest.manifest_sha256,
        "product_contract_version": "0.1.0",
        "canonical_authority": True,
        "contains_reusable_secret": False,
        "raw_document_bytes_included": False,
        "external_actions": False,
    }
    payload = _persisted_payload(admitted, terminal, event, manifest)
    item_id = p703.persist_governed_item(runtime_root, release_sha, payload, metadata)
    verified = p703.verify_item(runtime_root.expanduser().resolve() / "state" / "governed" / "items" / item_id)
    if verified.get("metadata") != metadata:
        raise UI1RealStateAdmissionError("P7.03 persisted metadata verification mismatch")
    checkpoint_id = p703.create_checkpoint(
        runtime_root,
        release_sha,
        execution_subject_identity=_identity_text(terminal.execution_subject_id),
        execution_version_identity=_identity_text(terminal.execution_version_id),
        governed_storage_item_ids=(item_id,),
        classification=PERSISTED_CLASSIFICATION,
        retention_policy_ref=PERSISTED_RETENTION,
        reason="P7.06-UI1 first real retained governed item admission",
    )
    return item_id, checkpoint_id


def _atomic_owner_evidence(path: Path, value: Mapping[str, Any]) -> str:
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


def run_admission(
    *,
    runtime_root: Path,
    access_root: Path,
    state_file: Path,
    credential_id: str,
    credential_file: Path,
    l7_manifest: Path,
    owner_approval: str,
    evidence_output: Path | None = None,
) -> AdmissionResult:
    if owner_approval != OWNER_APPROVAL_ASSERTION:
        raise UI1RealStateAdmissionError("exact bounded owner approval assertion is required")

    release_sha, repo_root = _verify_exact_release(runtime_root)
    organization, principal, access_decision = _authorize_operator(
        access_root=access_root,
        state_file=state_file,
        credential_id=credential_id,
        credential_file=credential_file,
    )

    rc, _lines, connection = connect_product(state_file, arvectum_repo_root=repo_root)
    if rc != 0 or connection is None:
        raise UI1RealStateAdmissionError("P6.02 Product Contract connection/preflight failed")
    if connection.organization_scope.organization_id != organization:
        raise UI1RealStateAdmissionError("P6.05-L4 Organization continuity mismatch")
    if connection.principal.principal_id != principal:
        raise UI1RealStateAdmissionError("P6.05-L4 human Principal continuity mismatch")
    if connection.product_contract.version_pin.version_id.value != "p6-02-arvectum-tender-operator-v0.1.0":
        raise UI1RealStateAdmissionError("exact P6.02 Product Contract Version continuity lost")

    manifest = load_verified_manifest(l7_manifest)
    subject_identity, version_identity = _target_identity_pair(connection)
    existing = _find_existing_exact_item(
        runtime_root,
        subject_identity=subject_identity,
        version_identity=version_identity,
    )

    checkpoint_id: str | None = None
    reconstruction_complete = False
    idempotent = existing is not None
    if existing is not None:
        item_id = existing[0]
        reconstruction_complete = True
    else:
        base_time = datetime.now(UTC)
        admitted, terminal, event, reconstruction, gate_decisions = _run_governed_admission(
            connection, manifest, base_time=base_time
        )
        if len(gate_decisions) != 4 or {item.kind for item in gate_decisions} != {
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        }:
            raise UI1RealStateAdmissionError("four distinct required gate decisions were not preserved")
        item_id, checkpoint_id = _persist_after_admission(
            runtime_root,
            release_sha,
            admitted=admitted,
            terminal=terminal,
            event=event,
            manifest=manifest,
        )
        reconstruction_complete = bool(reconstruction.complete)

    p703_status = p703.verify_store(runtime_root)
    if p703_status.get("integrity") != "PASS":
        raise UI1RealStateAdmissionError("P7.03 store integrity failed after bounded admission")

    if evidence_output is None:
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        evidence_output = (
            runtime_root.expanduser().resolve()
            / "evidence"
            / "p7-06-ui1"
            / f"p7-06-ui1-first-real-governed-item-{stamp}.json"
        )
    evidence = {
        "schema": "arvectum.p7_06.ui1-first-real-governed-item-evidence/1",
        "status": "PASS_IDEMPOTENT_EXISTING" if idempotent else "PASS_ADMITTED_AND_PERSISTED",
        "release_sha": release_sha,
        "owner_decision": OWNER_DECISION_PATH,
        "owner_approval_assertion_present": True,
        "manifest_sha256": manifest.manifest_sha256,
        "notice_number": NOTICE_NUMBER,
        "organization_context_reused": True,
        "human_principal_reused": True,
        "p7_04_authorization": {
            "allowed": access_decision.allowed,
            "reason": access_decision.reason,
            "principal_kind": access_decision.principal_kind,
            "operation": ACCESS_OPERATION,
            "resource": ACCESS_RESOURCE,
            "access_path": ACCESS_PATH,
            "organizational_authority_satisfied": access_decision.organizational_authority_satisfied,
            "consequential_approval_satisfied": access_decision.consequential_approval_satisfied,
        },
        "required_gate_kinds": [
            GovernedGateKind.AUTHORIZATION.value,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY.value,
            GovernedGateKind.DATA_GOVERNANCE.value,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL.value,
        ],
        "all_required_gates_allow": True,
        "product_contract_version": "0.1.0",
        "authority_mode": AuthorityMode.EXTERNAL_REFERENCE.value,
        "authoritative_source": EXTERNAL_SOURCE_AUTHORITY,
        "subject_identity": subject_identity,
        "version_identity": version_identity,
        "storage_item_id": item_id,
        "checkpoint_id": checkpoint_id,
        "idempotent_existing_item": idempotent,
        "reconstruction_complete": reconstruction_complete,
        "p7_03_integrity": p703_status.get("integrity"),
        "network_invoked": False,
        "eis_or_soap_invoked": False,
        "external_actions": False,
        "raw_document_bytes_persisted": False,
        "reusable_secret_persisted": False,
        "credential_secret_exposed": False,
    }
    evidence_sha = _atomic_owner_evidence(evidence_output, evidence)
    evidence["evidence_sha256"] = evidence_sha

    return AdmissionResult(
        status=evidence["status"],
        release_sha=release_sha,
        storage_item_id=item_id,
        checkpoint_id=checkpoint_id,
        subject_identity=subject_identity,
        version_identity=version_identity,
        manifest_sha256=manifest.manifest_sha256,
        idempotent_existing_item=idempotent,
        reconstruction_complete=reconstruction_complete,
        evidence_path=str(evidence_output),
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--access-root", type=Path, required=True)
    parser.add_argument("--state-file", type=Path, required=True)
    parser.add_argument("--credential-id", required=True)
    parser.add_argument("--credential-file", type=Path, required=True)
    parser.add_argument("--l7-manifest", type=Path, required=True)
    parser.add_argument("--owner-approval", required=True)
    parser.add_argument("--evidence-output", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        result = run_admission(
            runtime_root=args.runtime_root,
            access_root=args.access_root,
            state_file=args.state_file,
            credential_id=args.credential_id,
            credential_file=args.credential_file,
            l7_manifest=args.l7_manifest,
            owner_approval=args.owner_approval,
            evidence_output=args.evidence_output,
        )
    except Exception as exc:
        print(f"RESULT=BLOCKED error={type(exc).__name__}:{exc}")
        return 2
    print(f"RESULT={result.status}")
    print(f"RELEASE_SHA={result.release_sha}")
    print(f"STORAGE_ITEM_ID={result.storage_item_id}")
    print(f"CHECKPOINT_ID={result.checkpoint_id or 'NONE'}")
    print(f"MANIFEST_SHA256={result.manifest_sha256}")
    print(f"IDEMPOTENT_EXISTING_ITEM={str(result.idempotent_existing_item).lower()}")
    print(f"RECONSTRUCTION_COMPLETE={str(result.reconstruction_complete).lower()}")
    print(f"EVIDENCE_PATH={result.evidence_path}")
    print("NETWORK_INVOKED=false")
    print("EXTERNAL_ACTIONS=false")
    print("RAW_DOCUMENT_BYTES_PERSISTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
