"""P6.05 executable projection of the already-declared P6.02 admission envelope.

P6.02 Provisional Product Contract 0.1.0 already declares bounded CAP-001
registration/admission of exact external Document/Artifact references where the
selected real case requires it. P6.03 Stage 1 intentionally projected only the
read-oriented subset because the integration seam did not yet expose mutation.

P6.05 does not create a new Product Contract version. This module establishes a
distinct non-authoritative executable projection envelope while pinning the exact
immutable canonical P6.02 source declaration. It remains internal, provisional
and non-public.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from datetime import datetime
from typing import Final

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    OP_RESOLVE_DOCUMENT,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessMode,
    ProductContract,
    ProductContractLifecycle,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope
from arvectum_os_ref.workflow import OperationSideEffectClass
from p6_03_tender_operator_ref.contract import build_p6_02_product_contract

P6_02_CANONICAL_CONTRACT_PATH: Final = "docs/contracts/P6-02-FIRST-REAL-PRODUCT-CONTRACT.md"
P6_02_CANONICAL_BLOB_SHA: Final = "bdf098776399a003f2df542f3ab3cd48ef83b003"
P6_02_CONTRACT_SUBJECT_VALUE: Final = "p6-02-arvectum-tender-operator"
P6_02_CONTRACT_VERSION_VALUE: Final = "p6-02-arvectum-tender-operator-v0.1.0"
P6_05_PROJECTION_SUBJECT_VALUE: Final = "p6-05-p6-02-executable-projection"

OP_ADMIT_DOCUMENT_VERSION: Final = "p6.05.admit-document-version"


def p6_02_canonical_version_pin(
    *,
    organization: OrganizationScope,
) -> GovernedVersionPin:
    """Construct the exact immutable source pin for canonical P6.02 Product Contract."""
    if not isinstance(organization, OrganizationScope):
        raise ValueError("organization must be an OrganizationScope")
    scope = organization.organization_id.value
    return GovernedVersionPin(
        subject_id=Identity("product-contract-subject", P6_02_CONTRACT_SUBJECT_VALUE, scope),
        version_id=Identity("product-contract-version", P6_02_CONTRACT_VERSION_VALUE, scope),
        semantic_type="platform.product-contract",
        authority_scope="platform.product-contract/boundary",
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )


@dataclass(frozen=True, slots=True)
class P605ExecutableProductContractProjection(ProductContract):
    """Distinct non-authoritative executable projection of canonical P6.02 declaration."""

    canonical_source_pin: GovernedVersionPin
    canonical_source_path: str
    canonical_source_blob_sha: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.canonical_source_path != P6_02_CANONICAL_CONTRACT_PATH:
            raise ValueError("canonical_source_path mismatch")
        if self.canonical_source_blob_sha != P6_02_CANONICAL_BLOB_SHA:
            raise ValueError("canonical_source_blob_sha mismatch")
        if self.canonical_source_pin.semantic_type != "platform.product-contract":
            raise ValueError("canonical_source_pin semantic_type mismatch")
        if self.canonical_source_pin.authority_scope != "platform.product-contract/boundary":
            raise ValueError("canonical_source_pin authority_scope mismatch")
        if self.canonical_source_pin.lifecycle_status != ProductContractLifecycle.PROVISIONAL.value:
            raise ValueError("canonical_source_pin lifecycle_status mismatch")
        org_scope = self.record.organization.organization_id.value
        if (
            self.canonical_source_pin.subject_id.scope != org_scope
            or self.canonical_source_pin.version_id.scope != org_scope
        ):
            raise ValueError("canonical_source_pin scope must match projection Organization")
        if self.record.subject_id == self.canonical_source_pin.subject_id:
            raise ValueError("projection subject_id must not reuse canonical source subject_id")
        if self.record.version_id == self.canonical_source_pin.version_id:
            raise ValueError("projection version_id must not reuse canonical source version_id")
        if (
            self.canonical_source_pin.subject_id not in self.record.provenance_refs
            or self.canonical_source_pin.version_id not in self.record.provenance_refs
        ):
            raise ValueError("projection provenance must include canonical source Subject and Version identities")

    @property
    def version_pin(self) -> GovernedVersionPin:
        return self.canonical_source_pin


def build_p6_05_product_contract_projection(
    *, actor: ActorContext, created_at: datetime
) -> P605ExecutableProductContractProjection:
    """Return the distinct P6.05 executable projection pinned to canonical P6.02."""

    if not isinstance(actor, ActorContext):
        raise ValueError("actor must be an attributable ActorContext")
    if not isinstance(created_at, datetime) or created_at.tzinfo is None or created_at.utcoffset() is None:
        raise ValueError("created_at must be timezone-aware")

    # Use existing P6.03 builder for declaration structure
    base = build_p6_02_product_contract(actor=actor, created_at=created_at)

    cap001 = next(
        item for item in base.dependencies if item.dependency_id == CAP_001_DOCUMENT_ARTIFACT
    )
    cap001 = replace(
        cap001,
        allowed_operations=(OP_RESOLVE_DOCUMENT, OP_ADMIT_DOCUMENT_VERSION),
    )
    dependencies = tuple(
        cap001 if item.dependency_id == CAP_001_DOCUMENT_ARTIFACT else item
        for item in base.dependencies
    )

    resolve_operation = next(
        item for item in base.operations if item.operation_name == OP_RESOLVE_DOCUMENT
    )
    if len(resolve_operation.canonical_accesses) != 1:
        raise ValueError("P6.02 CAP-001 projection must have one exact Document access declaration")
    document_access = replace(
        resolve_operation.canonical_accesses[0],
        access_modes=(CanonicalAccessMode.READ, CanonicalAccessMode.WRITE),
    )
    resolve_operation = replace(
        resolve_operation,
        canonical_accesses=(document_access,),
    )
    admission_operation = ProductOperationDeclaration(
        operation_name=OP_ADMIT_DOCUMENT_VERSION,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
        required_gates=(
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        ),
        canonical_accesses=(document_access,),
        failure_behavior=(
            "Fail closed before canonical admission unless the exact external Document Version, "
            "exact Product Contract/provider evidence and all declared Governed Execution gates "
            "remain satisfied. No external source mutation is performed."
        ),
    )
    operations = tuple(
        resolve_operation if item.operation_name == OP_RESOLVE_DOCUMENT else item
        for item in base.operations
    ) + (admission_operation,)

    organization = actor.organization
    scope = organization.organization_id.value
    owner = actor.actual_principal.principal_id
    product_id = base.product_id

    canonical_pin = p6_02_canonical_version_pin(organization=organization)

    # Compute deterministic short projection version digest
    digest_input = (
        f"{scope}:{owner.value}:{created_at.isoformat()}:"
        f"{canonical_pin.subject_id.value}:{canonical_pin.version_id.value}:"
        f"{P6_02_CANONICAL_BLOB_SHA}"
    ).encode("utf-8")
    proj_version_hash = hashlib.sha256(digest_input).hexdigest()[:16]

    projection_subject_id = Identity(
        "product-contract-projection-subject",
        P6_05_PROJECTION_SUBJECT_VALUE,
        scope,
    )
    projection_version_id = Identity(
        "product-contract-projection-version",
        f"p6-05-p6-02-projection-{proj_version_hash}",
        scope,
    )

    provenance_refs = (
        owner,
        product_id,
        canonical_pin.subject_id,
        canonical_pin.version_id,
    )

    integrity_metadata = (
        ("representation", "p6.05-non-authoritative-executable-projection"),
        ("canonical_source_path", P6_02_CANONICAL_CONTRACT_PATH),
        ("canonical_source_blob_sha", P6_02_CANONICAL_BLOB_SHA),
    )

    payload = (
        ("canonical_contract", P6_02_CANONICAL_CONTRACT_PATH),
        ("contract_version", "0.1.0"),
        ("projection", "P6.05 exact tender attachment executable projection"),
    )

    record = CanonicalRecord(
        subject_id=projection_subject_id,
        version_id=projection_version_id,
        semantic_type="platform.product-contract",
        schema_version="p6.05-projection-1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.product-contract/boundary",
        accountable_owner_id=owner,
        creation_actor=actor,
        created_at=created_at,
        provenance_refs=provenance_refs,
        integrity_metadata=integrity_metadata,
        payload=payload,
        lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
    )

    return P605ExecutableProductContractProjection(
        record=record,
        product_id=product_id,
        product_version=base.product_version,
        bounded_scope=base.bounded_scope,
        compatibility_assumptions=base.compatibility_assumptions,
        dependencies=dependencies,
        operations=operations,
        portability_responsibility=base.portability_responsibility,
        retention_deletion_responsibility=base.retention_deletion_responsibility,
        review_condition=base.review_condition,
        exit_path=base.exit_path,
        canonical_source_pin=canonical_pin,
        canonical_source_path=P6_02_CANONICAL_CONTRACT_PATH,
        canonical_source_blob_sha=P6_02_CANONICAL_BLOB_SHA,
    )
