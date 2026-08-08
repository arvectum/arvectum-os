"""P3.09 — bounded shared-capability reuse and composition proof.

This module is an internal evidence harness, not a new Platform Capability or a
composition framework.  It proves that materially distinct bounded consumers
can compose the existing CAP-001..CAP-004 Incubating semantics through their
own RFC-0004 Provisional Product Contracts without changing the shared
capability contracts to fit a second consumer.

The proof deliberately adds no public API/SDK, stable operation naming,
product-domain schema, durable orchestration mechanism, persistence, Event
transport, IAM/PDP/PEP, separately deployable service topology or capability
lifecycle promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .execution import GovernedVersionPin
from .identity import Identity
from .product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
    CAPABILITY_CONTRACT_VERSION,
    OP_DISCOVER_SOURCES,
    OP_RECONSTRUCT_EXECUTION,
    OP_RESOLVE_DOCUMENT,
    OP_RESOLVE_SEARCH_SOURCE,
    OP_RETRIEVE_KNOWLEDGE,
    CapabilityConsumptionRequest,
    ProductCapabilityAdmission,
    validate_capability_consumption,
)
from .product_contract import ProductContract, ProductContractLifecycle, ProductContractValidationError


_REQUIRED_CAPABILITIES: Final = (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAP_003_SEARCH_PROJECTION,
    CAP_004_AUDIT_RECONSTRUCTION,
)

_REQUIRED_OPERATIONS: Final = frozenset(
    (
        (CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
        (CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
        (CAP_003_SEARCH_PROJECTION, OP_DISCOVER_SOURCES),
        (CAP_003_SEARCH_PROJECTION, OP_RESOLVE_SEARCH_SOURCE),
        (CAP_004_AUDIT_RECONSTRUCTION, OP_RECONSTRUCT_EXECUTION),
    )
)


class SharedCapabilityReuseError(ProductContractValidationError):
    """The bounded evidence does not demonstrate materially distinct shared reuse."""


@dataclass(frozen=True, slots=True)
class BoundedConsumerComposition:
    """One consumer-owned composition over existing capability operations.

    The ordered request tuple is evidence of consumer-side orchestration only.
    The platform does not interpret the workflow's business meaning and this
    representation is not a stable workflow or Product Contract schema.
    """

    workflow: GovernedVersionPin
    requests: tuple[CapabilityConsumptionRequest, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ValueError("reuse proof requires an exact governed Workflow version pin")
        if self.workflow.semantic_type != "platform.workflow":
            raise ValueError("reuse proof Workflow pin must reference platform.workflow")
        if not isinstance(self.requests, tuple) or not self.requests:
            raise ValueError("reuse proof composition must contain capability requests")
        if any(not isinstance(item, CapabilityConsumptionRequest) for item in self.requests):
            raise ValueError("reuse proof composition requests must be explicit capability requests")

        product_ids = {item.product_id for item in self.requests}
        product_versions = {item.product_version for item in self.requests}
        organizations = {item.organization for item in self.requests}
        if len(product_ids) != 1 or len(product_versions) != 1 or len(organizations) != 1:
            raise ValueError("one composition must preserve one product/version/Organization boundary")

        organization = next(iter(organizations))
        if self.workflow.subject_id.scope != organization.organization_id.value:
            raise ValueError("reuse proof Workflow must share the consumer Organization scope")

    @property
    def product_id(self) -> Identity:
        return self.requests[0].product_id

    @property
    def product_version(self) -> str:
        return self.requests[0].product_version

    @property
    def organization(self):
        return self.requests[0].organization

    @property
    def operation_signature(self) -> tuple[tuple[Identity, str, str], ...]:
        return tuple(
            (item.dependency_id, item.dependency_contract_version, item.operation_name)
            for item in self.requests
        )


@dataclass(frozen=True, slots=True)
class SharedCapabilityReuseProof:
    """Attributable evidence that two distinct consumers reuse the same capabilities."""

    first_product_id: Identity
    second_product_id: Identity
    first_product_contract_version_id: Identity
    second_product_contract_version_id: Identity
    first_workflow_version_id: Identity
    second_workflow_version_id: Identity
    shared_capability_ids: tuple[Identity, ...]
    capability_contract_version: str
    first_operation_signature: tuple[tuple[Identity, str, str], ...]
    second_operation_signature: tuple[tuple[Identity, str, str], ...]
    admissions: tuple[ProductCapabilityAdmission, ...]

    def __post_init__(self) -> None:
        if self.first_product_id == self.second_product_id:
            raise ValueError("reuse proof must preserve distinct consumer identities")
        if self.first_product_contract_version_id == self.second_product_contract_version_id:
            raise ValueError("reuse proof must preserve distinct Product Contract versions")
        if self.first_workflow_version_id == self.second_workflow_version_id:
            raise ValueError("reuse proof must preserve distinct Workflow versions")
        if self.shared_capability_ids != _REQUIRED_CAPABILITIES:
            raise ValueError("reuse proof must cover the bounded CAP-001..CAP-004 set")
        if self.first_operation_signature == self.second_operation_signature:
            raise ValueError("reuse proof compositions must remain materially distinct")


def _validate_one_composition(
    *,
    contract: ProductContract,
    composition: BoundedConsumerComposition,
) -> tuple[ProductCapabilityAdmission, ...]:
    if contract.lifecycle is not ProductContractLifecycle.PROVISIONAL:
        raise SharedCapabilityReuseError("P3.09 admits only Provisional Product Contracts")
    if contract.product_id != composition.product_id:
        raise SharedCapabilityReuseError("composition product identity does not match its Product Contract")
    if contract.product_version != composition.product_version:
        raise SharedCapabilityReuseError("composition product version does not match its Product Contract")
    if contract.organization != composition.organization:
        raise SharedCapabilityReuseError("composition Organization does not match its Product Contract")
    if contract.record.version_id.scope != composition.workflow.version_id.scope:
        raise SharedCapabilityReuseError("Product Contract and Workflow must share Organization scope")

    operation_pairs = tuple(
        (item.dependency_id, item.operation_name) for item in composition.requests
    )
    if len(operation_pairs) != len(_REQUIRED_OPERATIONS) or len(set(operation_pairs)) != len(operation_pairs):
        raise SharedCapabilityReuseError(
            "each P3.09 bounded consumer must exercise every existing shared operation exactly once"
        )
    if frozenset(operation_pairs) != _REQUIRED_OPERATIONS:
        raise SharedCapabilityReuseError(
            "each P3.09 bounded consumer must exercise the existing CAP-001..CAP-004 operation set exactly"
        )
    if any(
        item.dependency_contract_version != CAPABILITY_CONTRACT_VERSION
        for item in composition.requests
    ):
        raise SharedCapabilityReuseError("reuse proof must preserve the exact provisional capability contract version")

    return tuple(
        validate_capability_consumption(contract=contract, request=request)
        for request in composition.requests
    )


def prove_shared_capability_reuse(
    *,
    first_contract: ProductContract,
    first_composition: BoundedConsumerComposition,
    second_contract: ProductContract,
    second_composition: BoundedConsumerComposition,
) -> SharedCapabilityReuseProof:
    """Prove bounded cross-consumer reuse without creating new shared semantics.

    Material distinction is demonstrated by separate product identities, Product
    Contract versions, Workflow versions and different ordered compositions over
    the *same* existing provisional capability operations.  The function does not
    execute or generalize either workflow; concrete capability execution remains
    consumer-side and continues through ``product_capability_consumption``.
    """

    if not isinstance(first_contract, ProductContract) or not isinstance(second_contract, ProductContract):
        raise TypeError("reuse proof requires two explicit Product Contracts")
    if not isinstance(first_composition, BoundedConsumerComposition) or not isinstance(
        second_composition, BoundedConsumerComposition
    ):
        raise TypeError("reuse proof requires two explicit bounded compositions")

    if first_contract.product_id == second_contract.product_id:
        raise SharedCapabilityReuseError("P3.09 requires materially distinct consumer identities")
    if first_contract.record.version_id == second_contract.record.version_id:
        raise SharedCapabilityReuseError("distinct consumers must retain distinct Product Contract versions")
    if first_composition.workflow.version_id == second_composition.workflow.version_id:
        raise SharedCapabilityReuseError("P3.09 requires distinct exact Workflow versions")
    if first_composition.operation_signature == second_composition.operation_signature:
        raise SharedCapabilityReuseError(
            "a duplicated operation sequence is not sufficient evidence of materially distinct composition"
        )

    first_admissions = _validate_one_composition(
        contract=first_contract,
        composition=first_composition,
    )
    second_admissions = _validate_one_composition(
        contract=second_contract,
        composition=second_composition,
    )

    shared = tuple(
        capability_id
        for capability_id in _REQUIRED_CAPABILITIES
        if capability_id in {item.dependency_id for item in first_admissions}
        and capability_id in {item.dependency_id for item in second_admissions}
    )
    if shared != _REQUIRED_CAPABILITIES:
        raise SharedCapabilityReuseError("the bounded proof did not reuse the full shared capability set")

    return SharedCapabilityReuseProof(
        first_product_id=first_contract.product_id,
        second_product_id=second_contract.product_id,
        first_product_contract_version_id=first_contract.record.version_id,
        second_product_contract_version_id=second_contract.record.version_id,
        first_workflow_version_id=first_composition.workflow.version_id,
        second_workflow_version_id=second_composition.workflow.version_id,
        shared_capability_ids=shared,
        capability_contract_version=CAPABILITY_CONTRACT_VERSION,
        first_operation_signature=first_composition.operation_signature,
        second_operation_signature=second_composition.operation_signature,
        admissions=first_admissions + second_admissions,
    )
