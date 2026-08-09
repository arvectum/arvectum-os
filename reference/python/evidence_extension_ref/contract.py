"""P5.09 — Provisional Product Contract for the second integration proof.

The integration is intentionally materially different from the P4.08 bounded
product: it is a read-only evidence/reconstruction extension, depends only on
CAP-004, owns no product task/disposition state, opens no shared workspace and
requests no canonical mutation.

This remains extension-owned reference evidence. The Product Contract is
Provisional and its Python representation is internal; neither the extension nor
its contract promotes CAP-004, grants authority or creates a public/stable API.
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
EXTENSION_ID_VALUE: Final = "evidence-reconstruction-extension"
PRODUCT_CONTRACT_SCHEMA_VERSION: Final = "p5.09-internal-1"


def extension_id_for(actor: ActorContext) -> Identity:
    """Return the extension identity scoped to the Actor's Organization."""

    if not isinstance(actor, ActorContext):
        raise ValueError("evidence extension requires an attributable ActorContext")
    return Identity(
        "extension",
        EXTENSION_ID_VALUE,
        actor.organization.organization_id.value,
    )


def build_p5_09_product_contract(
    *,
    actor: ActorContext,
    created_at: datetime,
) -> ProductContract:
    """Build the exact immutable Provisional contract for the P5.09 extension."""

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    extension_id = extension_id_for(actor)
    owner = actor.actual_principal.principal_id

    record = CanonicalRecord(
        subject_id=Identity("product-contract-subject", "p5-09-evidence-extension", scope),
        version_id=Identity(
            "product-contract-version",
            "p5-09-evidence-extension-v0.1.0",
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
        integrity_metadata=(("representation", "p5.09-second-integration-reference-contract"),),
        payload=(("scope", "read-only governed execution evidence inspection through CAP-004"),),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    dependency = PlatformDependencyDeclaration(
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(OP_RECONSTRUCT_EXECUTION,),
        provider_responsibility=(
            "Preserve CAP-004 / RFC-0006 derived reconstruction semantics, exact governed "
            "references and honest evidence availability without replay or authority creation."
        ),
        consumer_responsibility=(
            "Use reconstruction only for read-only inspection under the current Organization, "
            "purpose, right and classification context; do not infer approval, source authority "
            "or permission from the derived view."
        ),
        failure_behavior=(
            "Fail closed without private Event/log/trace/database fallback, hidden evidence "
            "disclosure, replay, canonical mutation or cross-Organization access."
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
        # CAP-004 exposes a derived reconstruction view. It does not create a new
        # direct canonical-read surface; source disclosure remains enforced by
        # CAP-004/P3.07 against every exact evidence Version Identity.
        canonical_accesses=(),
        failure_behavior=(
            "Return only the bounded derived reconstruction result or fail closed; never "
            "fall back to private platform state or convert inspection into execution."
        ),
    )

    return ProductContract(
        record=record,
        product_id=extension_id,
        product_version=EXTENSION_VERSION,
        bounded_scope=(
            "One read-only extension inspects permitted exact governed execution/Event evidence "
            "through CAP-004 without workspace composition, product task state or mutation."
        ),
        compatibility_assumptions=(
            "CAP-004 remains Incubating / Provisional at contract baseline 1.0.0.",
            "Reconstruction remains a derived read-only view and never an authority source.",
            "Current Python types and operation tokens are internal evidence, not public compatibility promises.",
        ),
        dependencies=(dependency,),
        operations=(operation,),
        portability_responsibility=(
            "Preserve exact governed identities, Version references, correlation/causation and "
            "evidence availability semantics without requiring hidden runtime state or secret payload."
        ),
        retention_deletion_responsibility=(
            "Honor current per-evidence retention, deletion, redaction, classification and purpose "
            "constraints; absence or deletion must remain explicit rather than reconstructed."
        ),
        review_condition=(
            "Review at R15/P5.11 or earlier on material CAP-004, Product Contract, security, "
            "data-governance or integration-boundary change."
        ),
        exit_path=(
            "Revise with a new immutable Provisional version, contain or retire the extension; "
            "Stable status or platform promotion requires a separate governed decision."
        ),
    )
