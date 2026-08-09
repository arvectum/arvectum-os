"""Executable P6.03 Stage 1 mapping of the P6.02 Product Contract.

The canonical contract remains docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md
at Provisional 0.1.0. This module instantiates the exact Product/Contract identity,
Organization scope and CAP-001/CAP-004 dependency set for the Stage 1 read-oriented
proof only. It deliberately maps only operations already supported by the current
internal/provisional integration seam; mutation/admission paths from the broader
P6.02 envelope are not invented here and remain a gate before real Stage 2 reliance.

No procurement-domain schema, risk rule, RFQ/TKP logic, economics, recommendation,
external action or public compatibility promise is defined here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessDeclaration,
    CanonicalAccessMode,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext
from arvectum_os_ref.workflow import OperationSideEffectClass


PRODUCT_ID_VALUE: Final = "arvectum-tender-operator"
PRODUCT_COMPATIBILITY_LINE: Final = "restricted-paid-pilot/44fz-prebid-v1"
PRODUCT_CONTRACT_VERSION: Final = "0.1.0"
PRODUCT_CONTRACT_SCHEMA_VERSION: Final = "p6.02-provisional-0.1.0-internal-reference"
DOCUMENT_EXTERNAL_AUTHORITY_SCOPE: Final = "platform.document/external-reference"


def product_id_for(actor: ActorContext) -> Identity:
    if not isinstance(actor, ActorContext):
        raise ValueError("P6.03 Product Contract requires an attributable ActorContext")
    return Identity("product", PRODUCT_ID_VALUE, actor.organization.organization_id.value)


def _dependency(
    dependency_id: Identity,
    operation_name: str,
    *,
    provider: str,
    consumer: str,
) -> PlatformDependencyDeclaration:
    return PlatformDependencyDeclaration(
        dependency_id=dependency_id,
        contract_version=CAPABILITY_CONTRACT_VERSION,
        allowed_operations=(operation_name,),
        provider_responsibility=provider,
        consumer_responsibility=consumer,
        failure_behavior=(
            "Fail closed. The product may return explicitly to its local/manual contour, "
            "but that contour must not be represented as the Arvectum OS governed path."
        ),
        provisional=True,
    )


def build_p6_02_product_contract(*, actor: ActorContext, created_at: datetime) -> ProductContract:
    """Build the exact P6.02 identity/dependency boundary used by Stage 1.

    The executable operation projection is intentionally read-only because the
    current IntegrationAdapters seam exposes only read-oriented CAP-001/CAP-004
    operations. P6.03 does not manufacture provider support for canonical
    admission/mutation operations that are not yet available through that seam.
    """

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    organization = actor.organization
    scope = organization.organization_id.value
    owner = actor.actual_principal.principal_id
    product_id = product_id_for(actor)

    record = CanonicalRecord(
        subject_id=Identity("product-contract-subject", "p6-02-arvectum-tender-operator", scope),
        version_id=Identity(
            "product-contract-version",
            "p6-02-arvectum-tender-operator-v0.1.0",
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
        provenance_refs=(owner, product_id),
        integrity_metadata=(("representation", "p6.03-stage1-executable-contract"),),
        payload=(
            ("canonical_contract", "docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md"),
            ("contract_version", PRODUCT_CONTRACT_VERSION),
            ("stage", "P6.03 Stage 1 synthetic/redacted read-oriented proof"),
        ),
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    dependencies = (
        _dependency(
            CAP_001_DOCUMENT_ARTIFACT,
            OP_RESOLVE_DOCUMENT,
            provider=(
                "Preserve CAP-001 / RFC-0008 exact governed Document/Artifact identity, immutable "
                "version, external-authority mapping, provenance and handling constraints."
            ),
            consumer=(
                "Use only exact declared references under current Organization/Actor/purpose/right/" 
                "classification context; procurement meaning remains product-owned."
            ),
        ),
        _dependency(
            CAP_004_AUDIT_RECONSTRUCTION,
            OP_RECONSTRUCT_EXECUTION,
            provider=(
                "Preserve CAP-004 / RFC-0005/RFC-0006 read-oriented reconstruction, exact evidence "
                "references and truthful missing/redacted/deleted/unavailable state."
            ),
            consumer=(
                "Treat reconstruction as derived evidence view only; never invent missing evidence, "
                "authority, approval or product-domain interpretation."
            ),
        ),
    )

    document_access = CanonicalAccessDeclaration(
        semantic_type="platform.document",
        authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
        authority_scope=DOCUMENT_EXTERNAL_AUTHORITY_SCOPE,
        access_modes=(CanonicalAccessMode.READ,),
        authoritative_source=(
            "ЕИС/zakupki.gov.ru, partner/customer or supplier-origin source remains authoritative; "
            "Arvectum OS governs only the declared exact reference/version/provenance envelope."
        ),
        failure_behavior=(
            "Reject undeclared authority mode/scope or source access; never substitute Native authority."
        ),
    )

    operations = (
        ProductOperationDeclaration(
            operation_name=OP_RESOLVE_DOCUMENT,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
            required_gates=(GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE),
            canonical_accesses=(document_access,),
            failure_behavior=(
                "Fail closed without source disclosure, authority widening, hidden coupling or fallback "
                "to a private platform store/import/endpoint/cache."
            ),
        ),
        ProductOperationDeclaration(
            operation_name=OP_RECONSTRUCT_EXECUTION,
            dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
            side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
            required_gates=(GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE),
            canonical_accesses=(),
            failure_behavior=(
                "Fail closed on incompatible dependency/access evidence and expose permitted incomplete "
                "reconstruction honestly rather than inventing source evidence."
            ),
        ),
    )

    return ProductContract(
        record=record,
        product_id=product_id,
        product_version=PRODUCT_COMPATIBILITY_LINE,
        bounded_scope=(
            "First real Arvectum tender-operator Product Contract, Stage 1 only: synthetic/anonymized/" 
            "redacted read-oriented CAP-001 + CAP-004 proof for one explicit Organization, with all "
            "procurement semantics and every external action retained by the product/manual contour."
        ),
        compatibility_assumptions=(
            "Canonical Product Contract is P6.02 Provisional 0.1.0.",
            "CAP-001 and CAP-004 remain Incubating with Provisional provider contract 1.0.0.",
            "Current Python operation/module spellings are internal evidence, not Stable/public compatibility.",
            "Stage 1 does not admit unsupported CAP-001 canonical admission/mutation paths; Stage 2 remains gated.",
        ),
        dependencies=dependencies,
        operations=operations,
        portability_responsibility=(
            "Preserve exact Product Contract, Document/Artifact and governed evidence identities/versions; "
            "do not require export of credentials or private platform internals."
        ),
        retention_deletion_responsibility=(
            "Inherit source Organization classification, purpose, rights and retention/deletion constraints; "
            "synthetic/redacted Stage 1 fixtures contain no real partner/tender payload."
        ),
        review_condition=(
            "Review immediately after Stage 1 proof and before any real 44-ФЗ Stage 2 governed reliance, "
            "or earlier on material Product Contract/capability/security/authority change."
        ),
        exit_path=(
            "Fail closed and return explicitly to product-local/manual execution; revise the immutable "
            "Provisional Product Contract or provider mapping before expanding governed reliance."
        ),
    )
