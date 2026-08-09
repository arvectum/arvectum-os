"""Synthetic/redacted P6.05 proof of exact attachment-evidence manifest admission.

No real tender document bytes, filenames, customer data or source credentials are
stored here. The fixture proves only the governed boundary required after product-
local retrieval has produced a complete exact-byte/digest manifest.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, ExternalAuthorityContract
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
)
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.integration_adapters import IntegrationAdapters, compose_integration_adapters
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
)
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.product_contract_resolution import (
    DependencySupportDisposition,
    GovernedDependencyVersionEvidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)
from p6_03_tender_operator_ref.contract import DOCUMENT_EXTERNAL_AUTHORITY_SCOPE

from .contract import OP_ADMIT_DOCUMENT_VERSION, build_p6_05_product_contract_projection


UTC = timezone.utc
SYNTHETIC_MANIFEST_SHA256 = "7f2a3f635f02d744a8f29bdedce2d65ce6df82a0b8064f9a919f12e6810f08ec"


@dataclass(frozen=True, slots=True)
class P605SyntheticAdmissionScenario:
    organization: OrganizationScope
    actor: ActorContext
    contract: object
    adapters: IntegrationAdapters
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...]
    candidate: DocumentVersionCandidate
    interaction: ProductRuntimeInteraction


def _id(namespace: str, value: str, scope: str) -> Identity:
    return Identity(namespace, value, scope)


def build_p6_05_synthetic_admission_scenario() -> P605SyntheticAdmissionScenario:
    scope = "p6-05-org-a"
    organization = OrganizationScope(Identity("organization", scope, "platform"))
    actor = ActorContext(
        Principal(Identity("principal", "p6-05-product-operator", scope)),
        organization,
    )
    created_at = datetime(2026, 8, 9, 18, 30, tzinfo=UTC)
    contract = build_p6_05_product_contract_projection(actor=actor, created_at=created_at)

    governance_reference = "docs/contracts/PHASE-3-PROVISIONAL-CAPABILITY-CONTRACTS.md@1.0.0"
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

    authority = ExternalAuthorityContract(
        authoritative_system="synthetic-redacted-public-procurement-source",
        external_object_ref="redacted:44fz:exact-attachment-package:v1",
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        retrieval_or_sync=(
            "product-local read-only retrieval followed by exact digest manifest capture; "
            "no authoritative local synchronization"
        ),
        freshness_expectation="exact source package/version selected for the bounded P6.05 proof",
        source_version_semantics="source identity plus complete purpose-scoped member manifest and digests",
        conflict_rule="external source remains authoritative; mismatch or missing member fails closed",
        failure_behavior="missing/unavailable member blocks complete-evidence admission",
        permitted_transformations=("integrity hashing", "manifest generation"),
        retention_deletion="inherit restricted-pilot product/source rules",
        portability="export exact governed reference and manifest digest without source credentials",
    )
    record = CanonicalRecord(
        subject_id=_id("document-subject", "exact-tender-attachment-evidence", scope),
        version_id=_id("document-version", "exact-tender-attachment-evidence-v1", scope),
        semantic_type="platform.document",
        schema_version="p6.05-exact-attachment-evidence-1",
        organization=organization,
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id,),
        integrity_metadata=(
            ("member_count", "7"),
            ("manifest_sha256", SYNTHETIC_MANIFEST_SHA256),
            ("fixture", "synthetic-redacted-no-real-document-bytes"),
        ),
        payload=(
            ("purpose", "exact-tender-attachment-evidence"),
            ("completeness", "complete-for-declared-p6.05-proof-purpose"),
        ),
        lifecycle_status="AdmissionCandidate",
        external_authority=authority,
    )
    artifact = ArtifactContent(
        artifact_id=_id("artifact", "exact-attachment-evidence-manifest-v1", scope),
        organization=organization,
        content_ref="product-local://p6.05/exact-attachment-evidence-manifest/v1",
        media_type="application/json",
        integrity_ref=f"sha256:{SYNTHETIC_MANIFEST_SHA256}",
        rendition_role="evidence-manifest",
        handling=HandlingConstraints(
            "restricted-pilot",
            "prebid-evidence-admission",
            ("read",),
            "inherit-product-source-retention",
        ),
    )
    candidate = DocumentVersionCandidate(record, (artifact,), "evidence-manifest")

    workflow_record = CanonicalRecord(
        subject_id=_id("workflow-subject", "p6-05-admit-exact-attachment-evidence", scope),
        version_id=_id("workflow-version", "p6-05-admit-exact-attachment-evidence-v1", scope),
        semantic_type="platform.workflow",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.workflow/definition",
        accountable_owner_id=actor.actual_principal.principal_id,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(actor.actual_principal.principal_id, record.subject_id),
        integrity_metadata=(("representation", "p6.05-synthetic-reference"),),
        lifecycle_status="Approved",
    )
    workflow = WorkflowDefinition(
        record=workflow_record,
        operations=(
            WorkflowOperation(
                semantic_name=OP_ADMIT_DOCUMENT_VERSION,
                target_subject_id=record.subject_id,
                target_semantic_type=record.semantic_type,
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
    return P605SyntheticAdmissionScenario(
        organization=organization,
        actor=actor,
        contract=contract,
        adapters=adapters,
        governed_versions=governed_versions,
        candidate=candidate,
        interaction=interaction,
    )
