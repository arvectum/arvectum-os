"""P8.06 — Provisional Product Contract for the external Creative Test Agent extension.

The separately maintained consumer lives in ``arvectum/creative-test-agent``. This
module is the canonical executable boundary evidence inside Arvectum OS; it does
not copy Creative Test Agent business schemas/workflows into the platform.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
)
from arvectum_os_ref.product_contract import (
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext
from arvectum_os_ref.workflow import OperationSideEffectClass


EXTENSION_VERSION: Final = "0.1.0"
EXTENSION_ID_VALUE: Final = "creative-test-agent-audit-reconstruction"
PRODUCT_CONTRACT_SCHEMA_VERSION: Final = "p8.06-internal-1"
PRODUCT_CONTRACT_VERSION_VALUE: Final = "creative-test-agent-audit-reconstruction-pc-v0.1.0"


def extension_id_for(actor: ActorContext) -> Identity:
    if not isinstance(actor, ActorContext):
        raise ValueError("external creative extension requires an attributable ActorContext")
    return Identity(
        "extension",
        EXTENSION_ID_VALUE,
        actor.organization.organization_id.value,
    )


def build_p8_06_product_contract(
    *,
    actor: ActorContext,
    created_at: datetime,
) -> ProductContract:
    """Build the exact immutable Provisional Product Contract for P8.06."""

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    extension_id = extension_id_for(actor)
    owner = actor.actual_principal.principal_id

    record = CanonicalRecord(
        subject_id=Identity(
            "product-contract-subject",
            "creative-test-agent-audit-reconstruction",
            scope,
        ),
        version_id=Identity(
            "product-contract-version",
            PRODUCT_CONTRACT_VERSION_VALUE,
            scope,
        ),
        semantic_type="platform.product-contract",
        schema_version=PRODUCT_CONTRACT_SCHEMA_VERSION,
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(owner, extension_id),
        integrity_metadata=(
            ("representation", "p8.06-external-creative-product-contract"),
            ("external-consumer-repository", "arvectum/creative-test-agent"),
        ),
        payload=(
            (
                "scope",
                "optional read-only governed evidence reconstruction through CAP-004",
            ),
        ),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    dependency = PlatformDependencyDeclaration(
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(OP_RECONSTRUCT_EXECUTION,),
        provider_responsibility=(
            "Resolve read-only reconstruction only from governed evidence while preserving exact "
            "identity/version provenance, Organization scope, redaction and incompleteness semantics."
        ),
        consumer_responsibility=(
            "Supply exact governed references plus current Organization/purpose/right/classification "
            "context and treat reconstruction as a derived evidence view, never as authority."
        ),
        failure_behavior=(
            "Fail closed if exact dependency/version/operation compatibility, current governed provider "
            "evidence or required access context is unavailable; never fall back to private platform state."
        ),
        provisional=True,
    )

    operation = ProductOperationDeclaration(
        operation_name=OP_RECONSTRUCT_EXECUTION,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.DATA_GOVERNANCE,
        ),
        canonical_accesses=(),
        failure_behavior=(
            "Return only the bounded derived CAP-004 reconstruction or fail closed; do not mutate "
            "canonical state, replay effects, infer approval or bypass source disclosure controls."
        ),
    )

    return ProductContract(
        record=record,
        product_id=extension_id,
        product_version=EXTENSION_VERSION,
        bounded_scope=(
            "One optional read-only extension owned by Creative Test Agent may inspect permitted "
            "governed execution/Event evidence through CAP-004. Creative inputs, scoring, workflows, "
            "reports, recommendations, UX and model/prompt choices remain product-owned."
        ),
        compatibility_assumptions=(
            "CAP-004 remains Incubating with Provisional contract baseline 1.0.0.",
            "The external declaration format is Creative Test Agent-owned and not a public platform manifest.",
            "Current Python types/tokens/adapters remain internal evidence and are not stable public API promises.",
        ),
        dependencies=(dependency,),
        operations=(operation,),
        portability_responsibility=(
            "The extension is optional and removable without hidden shared mutable state; preserve exact "
            "governed identities and evidence semantics across any permitted reconstruction export."
        ),
        retention_deletion_responsibility=(
            "Honor the current source-evidence retention, deletion, redaction, classification and purpose "
            "controls; the extension does not create an independent retained source of truth."
        ),
        review_condition=(
            "Review at P8.06/R26 or earlier on material CAP-004, Product Contract, source declaration, "
            "security/data-governance or integration-boundary change."
        ),
        exit_path=(
            "Disable and remove the optional extension, or publish a new immutable declaration and Product "
            "Contract version and rerun exact governed dependency resolution. Stable status or capability "
            "promotion requires a separate governed decision."
        ),
    )
