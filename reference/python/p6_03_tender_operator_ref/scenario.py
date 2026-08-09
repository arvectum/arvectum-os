"""Synthetic/redacted cross-repository fixture for P6.03 Stage 1.

The fixture contains no real partner, customer, supplier or tender payload. It
exists only to let the real product repository exercise the exact P6.02 identity
and CAP-001/CAP-004 integration seam against immutable provider evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal

from .contract import (
    DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
    PRODUCT_COMPATIBILITY_LINE,
    build_p6_02_product_contract,
)


UTC = timezone.utc


@dataclass(frozen=True, slots=True)
class Stage1SyntheticScenario:
    organization: OrganizationScope
    actor: ActorContext
    contract: Any
    adapters: IntegrationAdapters
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...]
    document_request: CapabilityConsumptionRequest
    reconstruction_request: CapabilityConsumptionRequest
    admitted_document: Any
    artifact_id: Identity
    reconstruction_manifest: ReconstructionManifest
    evidence_constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...]


def _id(namespace: str, value: str, scope: str) -> Identity:
    return Identity(namespace, value, scope)


def _pin(namespace: str, value: str, semantic_type: str, scope: str) -> GovernedVersionPin:
    return GovernedVersionPin(
        _id(f"{namespace}-subject", value, scope),
        _id(f"{namespace}-version", f"{value}-v1", scope),
        semantic_type,
        f"{semantic_type}/state",
        "Retained",
    )


def build_stage1_synthetic_scenario() -> Stage1SyntheticScenario:
    scope = "p6-03-org-a"
    organization = OrganizationScope(Identity("organization", scope, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", "p6-03-product-operator", scope)),
        organization,
    )
    created_at = datetime(2026, 8, 9, 16, 0, tzinfo=UTC)
    contract = build_p6_02_product_contract(actor=actor, created_at=created_at)

    governance_reference = (
        "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"
    )
    governed_versions = (
        GovernedDependencyVersionEvidence(
            CAP_001_DOCUMENT_ARTIFACT,
            CAPABILITY_CONTRACT_VERSION,
            DependencySupportDisposition.SUPPORTED,
            governance_reference,
        ),
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

    access = AccessRequest(
        actor,
        "prebid-review",
        "read",
        ("restricted-pilot",),
    )
    document_request = CapabilityConsumptionRequest(
        organization=organization,
        product_id=contract.product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RESOLVE_DOCUMENT,
        access=access,
    )
    reconstruction_request = CapabilityConsumptionRequest(
        organization=organization,
        product_id=contract.product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RECONSTRUCT_EXECUTION,
        access=access,
    )

    authority = ExternalAuthorityContract(
        authoritative_system="synthetic-redacted-eis-source",
        external_object_ref="redacted:44fz:case-001:document-001",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync="reference-only controlled retrieval; no authoritative local synchronization",
        freshness_expectation="exact accepted synthetic source package for this Stage 1 run",
        source_version_semantics="source package digest plus explicit retrieval provenance",
        conflict_rule="external source remains authoritative; local mismatch fails closed",
        failure_behavior="source/reference unavailability blocks governed reliance; no cached authority fallback",
        permitted_transformations=("redaction", "integrity hashing"),
        retention_deletion="synthetic Stage 1 fixture only; no real tender content retained",
        portability="export exact governed reference/provenance without source credentials",
    )
    document_record = CanonicalRecord(
        subject_id=_id("document-subject", "redacted-tender-document", scope),
        version_id=_id("document-version", "redacted-tender-document-v1", scope),
        semantic_type="platform.document",
        schema_version="p6.03-stage1-1",
        organization=organization,
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(("fixture", "synthetic-redacted-no-real-tender-content"),),
        payload=(("source", "synthetic-redacted-external-reference"),),
        lifecycle_status="AdmittedReference",
        external_authority=authority,
    )
    artifact = ArtifactContent(
        artifact_id=_id("artifact", "redacted-tender-document-artifact-v1", scope),
        organization=organization,
        content_ref="redacted://p6.03/tender/document-001",
        media_type="application/pdf",
        integrity_ref="sha256:synthetic-redacted-document-v1",
        rendition_role="source",
        handling=HandlingConstraints(
            "restricted-pilot",
            "prebid-review",
            ("read",),
            "synthetic-stage1-only",
        ),
    )
    admitted_document = admit_document_version(
        DocumentVersionCandidate(document_record, (artifact,), "source")
    )

    workflow = _pin("workflow", "tender-prebid", "product.tender-prebid-workflow", scope)
    material = GovernedVersionPin.from_record(document_record)
    execution = _pin("execution", "stage1-run", "platform.execution-context", scope)
    result = _pin(
        "result",
        "reviewed-package-ref",
        "product.client-ready-package-reference",
        scope,
    )
    event = _pin("event", "stage1-reconstruction-evidence", "platform.event", scope)
    execution_subject = execution.subject_id
    provenance_refs = tuple(
        dict.fromkeys(
            (
                actor.actual_principal.principal_id,
                execution_subject,
                workflow.subject_id,
                workflow.version_id,
                material.subject_id,
                material.version_id,
                contract.record.subject_id,
                contract.record.version_id,
                execution.subject_id,
                execution.version_id,
                result.subject_id,
                result.version_id,
                event.subject_id,
                event.version_id,
            )
        )
    )
    manifest = ReconstructionManifest(
        organization=organization,
        execution_subject_id=execution_subject,
        initiating_actor_id=actor.actual_principal.principal_id,
        operation_name="product.tender-prebid.synthetic-stage1-review",
        workflow=workflow,
        material_inputs=(material,),
        gate_decisions=(),
        execution_versions=(execution,),
        results=(result,),
        events=(event,),
        event_types=(("platform.product-integration.stage1-observed", "1"),),
        correlation_refs=(execution_subject,),
        causation_refs=(material.version_id,),
        provenance_refs=provenance_refs,
        product_contract=contract.version_pin,
    )
    pins = (workflow, material, contract.version_pin, execution, result, event)
    evidence_constraints = tuple(
        (pin.version_id, "prebid-review", ("read",), "restricted-pilot")
        for pin in pins
    )

    return Stage1SyntheticScenario(
        organization=organization,
        actor=actor,
        contract=contract,
        adapters=adapters,
        governed_versions=governed_versions,
        document_request=document_request,
        reconstruction_request=reconstruction_request,
        admitted_document=admitted_document,
        artifact_id=artifact.artifact_id,
        reconstruction_manifest=manifest,
        evidence_constraints=evidence_constraints,
    )
