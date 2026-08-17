"""Executable P6.07 projection of the canonical P6.06 Product Contract.

The canonical contract remains
``docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md`` at Provisional 0.1.0.
This module maps only the shared CAP-004 reconstruction dependency needed by the
bounded P6.07 validation: Stage 1 synthetic/offline proof and Stage 2C read-only
reconstruction of the confirmed real Stage 2B effect. Discount Parser collection,
Offer semantics, normalization, deduplication, classification, scheduling,
publication rules, Telegram integration and publication ledger remain
product-owned.

The projection is internal/provisional reference evidence. It is not a Stable
Product Contract, public SDK/API, capability promotion or production commitment.
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


PRODUCT_ID_VALUE: Final = "arvectum-discount-parser"
PRODUCT_COMPATIBILITY_LINE: Final = "mvp-v1/controlled-telegram-publication"
PRODUCT_CONTRACT_VERSION: Final = "0.1.0"
PRODUCT_CONTRACT_SCHEMA_VERSION: Final = "p6.06-provisional-0.1.0-internal-reference"
P6_06_CANONICAL_CONTRACT_PATH: Final = "docs/contracts/P6-06-SECOND-REAL-PRODUCT-CONTRACT.md"
P6_06_CANONICAL_BLOB_SHA: Final = "23bbe792b81ddc5da736333d8a92580a718f920e"
P6_06_CONTRACT_SUBJECT_VALUE: Final = "p6-06-arvectum-discount-parser"
P6_06_CONTRACT_VERSION_VALUE: Final = "p6-06-arvectum-discount-parser-v0.1.0"


def product_id_for(actor: ActorContext) -> Identity:
    if not isinstance(actor, ActorContext):
        raise ValueError("P6.07 Product Contract projection requires an attributable ActorContext")
    return Identity("product", PRODUCT_ID_VALUE, actor.organization.organization_id.value)


def build_p6_06_product_contract_projection(
    *,
    actor: ActorContext,
    created_at: datetime,
) -> ProductContract:
    """Build the bounded executable projection used by P6.07 validation."""

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    owner = actor.actual_principal.principal_id
    product_id = product_id_for(actor)

    record = CanonicalRecord(
        subject_id=Identity("product-contract-subject", P6_06_CONTRACT_SUBJECT_VALUE, scope),
        version_id=Identity("product-contract-version", P6_06_CONTRACT_VERSION_VALUE, scope),
        semantic_type="platform.product-contract",
        schema_version=PRODUCT_CONTRACT_SCHEMA_VERSION,
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=(owner, product_id),
        integrity_metadata=(
            ("representation", "p6.07-bounded-executable-projection"),
            ("canonical-source-blob", P6_06_CANONICAL_BLOB_SHA),
        ),
        payload=(
            ("canonical_contract", P6_06_CANONICAL_CONTRACT_PATH),
            ("canonical_blob_sha", P6_06_CANONICAL_BLOB_SHA),
            ("contract_version", PRODUCT_CONTRACT_VERSION),
            (
                "stage",
                "P6.07 Stage 1 synthetic/offline proof plus Stage 2C confirmed-real-effect read-only reconstruction",
            ),
        ),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    dependency = PlatformDependencyDeclaration(
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(OP_RECONSTRUCT_EXECUTION,),
        provider_responsibility=(
            "Preserve CAP-004 / RFC-0005/RFC-0006 read-oriented reconstruction from exact governed "
            "execution/event/effect references and expose unavailable or restricted evidence honestly."
        ),
        consumer_responsibility=(
            "Preserve exact P6.06 Product Contract, Organization, Actor/trigger and product-owned "
            "publication/source/config/effect references; treat reconstruction as derived evidence only."
        ),
        failure_behavior=(
            "Fail closed without platform-internal fallback, evidence invention, external-effect replay "
            "or conversion of product-local state into platform authority."
        ),
        provisional=True,
    )

    operation = ProductOperationDeclaration(
        operation_name=OP_RECONSTRUCT_EXECUTION,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
        required_gates=(GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE),
        canonical_accesses=(),
        failure_behavior=(
            "Fail closed on contract, Organization, provider-evidence or access mismatch; permitted "
            "incomplete reconstruction must remain explicitly incomplete rather than inventing evidence."
        ),
    )

    return ProductContract(
        record=record,
        product_id=product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        bounded_scope=(
            "P6.07 bounded validation only: Stage 1 synthetic/offline proof and Stage 2C read-only "
            "reconstruction of the separately authorized, already completed Stage 2B Discount Parser "
            "publication using product-owned references plus CAP-004. No Telegram replay, product database "
            "migration, shared product schema or capability promotion."
        ),
        compatibility_assumptions=(
            "Canonical Product Contract is P6.06 Provisional 0.1.0.",
            "CAP-004 remains Incubating with Provisional provider contract 1.0.0.",
            "Current Python/module/dataclass spellings are internal evidence, not Stable/public compatibility.",
            "Stage 1 uses a fake Telegram adapter; Stage 2B real publication is separately authorized and "
            "product-owned; Stage 2C only reconstructs retained evidence and must not repeat the effect.",
        ),
        dependencies=(dependency,),
        operations=(operation,),
        portability_responsibility=(
            "Preserve exact Product Contract, Organization, execution, product boundary and external-effect "
            "references sufficient for reconstruction without exporting Telegram credentials or private internals."
        ),
        retention_deletion_responsibility=(
            "Retain only minimized exact references needed by the bounded evidence proof; lawful deletion or "
            "redaction must reduce reconstruction completeness explicitly rather than rewrite history."
        ),
        review_condition=(
            "Review after the first real governed publication or no later than 2026-09-08, or earlier on a "
            "material CAP-004, external-effect, authority, Organization or public-contract change."
        ),
        exit_path=(
            "Revise the immutable Provisional Product Contract, contain/return to product-local operation, "
            "replace the adapter or retire the boundary; stabilization requires a separate lifecycle decision."
        ),
    )
