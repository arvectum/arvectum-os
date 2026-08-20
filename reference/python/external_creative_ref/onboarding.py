"""Exact P8.06 source-evidence pin for the external Creative Test Agent consumer."""

from __future__ import annotations

from typing import Final

from arvectum_os_ref.external_consumer_onboarding import ExternalConsumerSourceEvidence
from arvectum_os_ref.product_capability_consumption import (
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
)
from arvectum_os_ref.product_contract import ProductBoundaryMechanism
from arvectum_os_ref.security import ActorContext, OrganizationScope

from .contract import EXTENSION_VERSION, extension_id_for


SOURCE_REPOSITORY: Final = "arvectum/creative-test-agent"
SOURCE_COMMIT_SHA: Final = "8dd5aab83beb29be10629f06a2c4e3255e51f06c"
SOURCE_DECLARATION_PATH: Final = "integrations/arvectum_os_p8_06_onboarding.json"
SOURCE_DECLARATION_BLOB_SHA: Final = "67d6e4cfe5f32577c82a3f35aff3c33fe2f71fd3"
SOURCE_DECLARATION_FORMAT_OWNER: Final = "arvectum/creative-test-agent"
SOURCE_DECLARATION_FORMAT_STATUS: Final = "product-local-provisional-p8.06-evidence"


def build_external_source_evidence(
    *,
    organization: OrganizationScope,
    actor: ActorContext,
) -> ExternalConsumerSourceEvidence:
    """Return exact consumer-owned declaration evidence pinned to the merged source revision."""

    if not isinstance(actor, ActorContext):
        raise ValueError("external source evidence requires an attributable ActorContext")
    if actor.organization != organization:
        raise ValueError("external source evidence actor and Organization must match")
    return ExternalConsumerSourceEvidence(
        repository=SOURCE_REPOSITORY,
        commit_sha=SOURCE_COMMIT_SHA,
        declaration_path=SOURCE_DECLARATION_PATH,
        declaration_blob_sha=SOURCE_DECLARATION_BLOB_SHA,
        declaration_format_owner=SOURCE_DECLARATION_FORMAT_OWNER,
        declaration_format_status=SOURCE_DECLARATION_FORMAT_STATUS,
        owner="ООО «Арвектум»",
        consumer_id=extension_id_for(actor),
        consumer_version=EXTENSION_VERSION,
        organization=organization,
        declared_dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
        operation_name=OP_RECONSTRUCT_EXECUTION,
        purpose="creative-test-audit-reconstruction",
        required_rights=("read",),
        allowed_classifications=("internal",),
        boundary_mechanisms=(ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,),
        shared_mutable_state=False,
        product_owned_semantics=(
            "creative input and asset schemas",
            "audience simulation and scoring semantics",
            "brand-safety and rubric configuration",
            "creative-test workflows and approvals",
            "reports, recommendations and product UX",
            "model and prompt choices",
        ),
        enabled_by_default=False,
    )
