"""P6.05 executable projection of the already-declared P6.02 admission envelope.

P6.02 Provisional Product Contract 0.1.0 already declares bounded CAP-001
registration/admission of exact external Document/Artifact references where the
selected real case requires it. P6.03 Stage 1 intentionally projected only the
read-oriented subset because the integration seam did not yet expose mutation.

P6.05 does not create a new Product Contract version. This module keeps the exact
P6.02 Canonical Record/version and expands only the internal executable projection
to the already-declared canonical-mutation operation. It remains internal,
provisional and non-public.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Final

from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    OP_RESOLVE_DOCUMENT,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessMode,
    ProductContract,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext
from arvectum_os_ref.workflow import OperationSideEffectClass
from p6_03_tender_operator_ref.contract import build_p6_02_product_contract


OP_ADMIT_DOCUMENT_VERSION: Final = "p6.05.admit-document-version"


def build_p6_05_product_contract_projection(
    *, actor: ActorContext, created_at: datetime
) -> ProductContract:
    """Return the exact P6.02 contract with its pre-declared CAP-001 admission slice projected."""

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

    return replace(
        base,
        dependencies=dependencies,
        operations=operations,
    )
