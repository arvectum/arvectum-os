"""P3.08 — bounded RFC-0004 Product Contract capability-consumption boundary.

This internal reference slice proves that a product-like bounded consumer reaches the
Phase 3 Incubating capabilities only through an exact Provisional Product Contract
and an explicit current access context.

It deliberately does not define a public API/SDK, stable Product Contract manifest,
capability lifecycle transition, IAM/PDP/PEP mechanism, product-domain schema,
durable transport, serialization, service topology or production support contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from .audit_reconstruction_support import AuditReconstructionView
from .canonical import CanonicalRecord
from .cross_capability_enforcement import (
    AccessRequest,
    reconstruct_audit_for_access,
    resolve_document_for_access,
    resolve_search_hit_for_access,
    retrieve_knowledge_for_access,
    search_for_access,
)
from .document_artifact_governance import AdmittedDocumentVersion, ExactDocumentReliance
from .event_provenance import ReconstructionManifest
from .governed_execution import GovernedGateKind
from .identity import Identity
from .memory_knowledge_governance import RetrievalProjection, ValidatedKnowledge
from .product_contract import (
    CanonicalAccessMode,
    HiddenProductPlatformCouplingError,
    ProductBoundaryMechanism,
    ProductContract,
    ProductContractCanonicalAccessError,
    ProductContractDependencyError,
    ProductContractLifecycle,
    ProductContractLifecycleError,
    ProductContractOperationError,
    ProductContractScopeError,
    ProductContractSecurityBoundaryError,
    ProductContractValidationError,
)
from .search_index_projection import (
    GovernedSearchSource,
    SearchHit,
    SearchProjection,
)
from .security import OrganizationScope
from .workflow import OperationSideEffectClass


CAP_001_DOCUMENT_ARTIFACT: Final = Identity("platform-capability", "CAP-001", "platform")
CAP_002_MEMORY_KNOWLEDGE: Final = Identity("platform-capability", "CAP-002", "platform")
CAP_003_SEARCH_PROJECTION: Final = Identity("platform-capability", "CAP-003", "platform")
CAP_004_AUDIT_RECONSTRUCTION: Final = Identity("platform-capability", "CAP-004", "platform")

CAPABILITY_CONTRACT_VERSION: Final = "1.0.0"

OP_RESOLVE_DOCUMENT: Final = "p3.08.resolve-document"
OP_RETRIEVE_KNOWLEDGE: Final = "p3.08.retrieve-knowledge"
OP_DISCOVER_SOURCES: Final = "p3.08.discover-sources"
OP_RESOLVE_SEARCH_SOURCE: Final = "p3.08.resolve-search-source"
OP_RECONSTRUCT_EXECUTION: Final = "p3.08.reconstruct-execution"

_REQUIRED_ACCESS_GATES: Final = frozenset((GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE))


class ProductCapabilityConsumptionError(ProductContractValidationError):
    """The bounded Product Contract cannot admit this capability consumption."""


@dataclass(frozen=True, slots=True)
class CapabilityConsumptionRequest:
    """Exact product/capability reliance plus current access context.

    ``access`` is the P3.07 current Organization/purpose/right/classification
    context. Product Contract validation does not turn it into approval,
    delegation or Organizational Authority.
    """

    organization: OrganizationScope
    product_id: Identity
    product_version: str
    dependency_id: Identity
    dependency_contract_version: str
    operation_name: str
    access: AccessRequest
    mechanism: ProductBoundaryMechanism = ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("capability consumption Organization scope must be explicit")
        if not isinstance(self.product_id, Identity):
            raise ValueError("capability consumption product identity must be explicit")
        if self.product_id.scope != self.organization.organization_id.value:
            raise ValueError("capability consumption product identity must share Organization scope")
        if not isinstance(self.product_version, str) or not self.product_version.strip():
            raise ValueError("capability consumption product_version must be explicit")
        if not isinstance(self.dependency_id, Identity) or self.dependency_id.scope != "platform":
            raise ValueError("capability consumption dependency must be a platform-scoped Identity")
        if not isinstance(self.dependency_contract_version, str) or not self.dependency_contract_version.strip():
            raise ValueError("capability dependency contract version must be explicit")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("capability consumption operation_name must be explicit")
        if not isinstance(self.access, AccessRequest):
            raise ValueError("capability consumption requires an explicit AccessRequest")
        if self.access.organization != self.organization:
            raise ValueError("capability consumption access context must share Organization scope")
        if not isinstance(self.mechanism, ProductBoundaryMechanism):
            raise ValueError("capability consumption boundary mechanism must be explicit")


@dataclass(frozen=True, slots=True)
class ProductCapabilityAdmission:
    """Exact admitted Product Contract/capability reliance; not permission or authority."""

    product_contract_version_id: Identity
    product_id: Identity
    dependency_id: Identity
    dependency_contract_version: str
    operation_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract_version_id, Identity):
            raise ValueError("Product Contract exact Version Identity must be preserved")
        if not isinstance(self.product_id, Identity):
            raise ValueError("admission product identity must be explicit")
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("admission dependency identity must be explicit")


def _exact_dependency(contract: ProductContract, request: CapabilityConsumptionRequest):
    matches = tuple(item for item in contract.dependencies if item.dependency_id == request.dependency_id)
    if len(matches) != 1:
        raise ProductContractDependencyError("requested Phase 3 capability dependency is not declared exactly once")
    dependency = matches[0]
    if dependency.contract_version != request.dependency_contract_version:
        raise ProductContractDependencyError("requested Phase 3 capability contract version is incompatible")
    if request.operation_name not in dependency.allowed_operations:
        raise ProductContractDependencyError("requested capability operation is not allowed by the dependency")
    if not dependency.provisional:
        raise ProductContractDependencyError(
            "P3.08 bounded proof requires the dependency to be explicitly treated as provisional"
        )
    return dependency


def _exact_operation(contract: ProductContract, request: CapabilityConsumptionRequest):
    matches = tuple(item for item in contract.operations if item.operation_name == request.operation_name)
    if len(matches) != 1:
        raise ProductContractOperationError("requested capability operation is not declared exactly once")
    operation = matches[0]
    if operation.dependency_id != request.dependency_id:
        raise ProductContractOperationError("capability operation references a different dependency")
    if set(operation.side_effect_classes) != {OperationSideEffectClass.READ_ONLY}:
        raise ProductContractOperationError("P3.08 bounded consumer admits read-only capability operations only")
    if not _REQUIRED_ACCESS_GATES.issubset(set(operation.required_gates)):
        raise ProductContractSecurityBoundaryError(
            "P3.08 capability operation must preserve Authorization and DataGovernance boundaries"
        )
    return operation


def validate_capability_consumption(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
) -> ProductCapabilityAdmission:
    """Validate one exact Incubating-capability reliance before invoking its slice."""

    if not isinstance(contract, ProductContract):
        raise TypeError("capability consumption requires an explicit ProductContract")
    if not isinstance(request, CapabilityConsumptionRequest):
        raise TypeError("capability consumption requires an explicit CapabilityConsumptionRequest")
    if contract.lifecycle is not ProductContractLifecycle.PROVISIONAL:
        raise ProductContractLifecycleError(
            "P3.08 bounded consumer admits only an explicit Provisional Product Contract"
        )
    if contract.organization != request.organization:
        raise ProductContractScopeError("Product Contract and capability request must share Organization scope")
    if contract.product_id != request.product_id:
        raise ProductContractScopeError("Product Contract governs a different product identity")
    if contract.product_version != request.product_version:
        raise ProductContractScopeError("Product Contract does not cover the requested product version")
    if request.mechanism is not ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT:
        raise HiddenProductPlatformCouplingError(
            "direct table/store/index/import/endpoint/stream/shared-state capability reliance is rejected"
        )
    if request.access.organization != contract.organization:
        raise ProductContractScopeError("current access context must share the Product Contract Organization")

    _exact_dependency(contract, request)
    _exact_operation(contract, request)

    return ProductCapabilityAdmission(
        product_contract_version_id=contract.record.version_id,
        product_id=request.product_id,
        dependency_id=request.dependency_id,
        dependency_contract_version=request.dependency_contract_version,
        operation_name=request.operation_name,
    )


def _require_expected_operation(
    request: CapabilityConsumptionRequest,
    *,
    dependency_id: Identity,
    operation_name: str,
) -> None:
    if request.dependency_id != dependency_id or request.operation_name != operation_name:
        raise ProductCapabilityConsumptionError(
            "bounded consumer adapter was invoked with the wrong declared capability operation"
        )


def _require_canonical_read(contract: ProductContract, request: CapabilityConsumptionRequest, record: CanonicalRecord) -> None:
    operation = _exact_operation(contract, request)
    if not any(
        declaration.permits(record, CanonicalAccessMode.READ)
        for declaration in operation.canonical_accesses
    ):
        raise ProductContractCanonicalAccessError(
            f"Product Contract does not declare canonical Read for {record.semantic_type}"
        )


def consume_document(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    admitted: AdmittedDocumentVersion,
    artifact_id: Identity,
) -> ExactDocumentReliance:
    """Consume CAP-001 exact governed Document/Artifact access through the contract."""

    validate_capability_consumption(contract=contract, request=request)
    _require_expected_operation(
        request, dependency_id=CAP_001_DOCUMENT_ARTIFACT, operation_name=OP_RESOLVE_DOCUMENT
    )
    _require_canonical_read(contract, request, admitted.canonical_record)
    return resolve_document_for_access(admitted=admitted, artifact_id=artifact_id, request=request.access)


def consume_knowledge(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    knowledge: tuple[ValidatedKnowledge, ...],
    allow_stale: bool = False,
) -> tuple[RetrievalProjection, ...]:
    """Consume CAP-002 governed Knowledge retrieval through the contract."""

    validate_capability_consumption(contract=contract, request=request)
    _require_expected_operation(
        request, dependency_id=CAP_002_MEMORY_KNOWLEDGE, operation_name=OP_RETRIEVE_KNOWLEDGE
    )
    for item in knowledge:
        if item.canonical_record.organization == request.organization:
            _require_canonical_read(contract, request, item.canonical_record)
    return retrieve_knowledge_for_access(
        knowledge=knowledge, request=request.access, allow_stale=allow_stale
    )


def consume_search(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    projection: SearchProjection,
    current_sources: tuple[GovernedSearchSource, ...],
    query_text: str,
) -> tuple[SearchHit, ...]:
    """Consume CAP-003 non-authoritative discovery through the contract."""

    validate_capability_consumption(contract=contract, request=request)
    _require_expected_operation(
        request, dependency_id=CAP_003_SEARCH_PROJECTION, operation_name=OP_DISCOVER_SOURCES
    )
    return search_for_access(
        projection=projection,
        current_sources=current_sources,
        query_text=query_text,
        request=request.access,
    )


def consume_search_source(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    hit: SearchHit,
    current_sources: tuple[GovernedSearchSource, ...],
):
    """Exit CAP-003 to exact governed source only through a separately declared operation."""

    validate_capability_consumption(contract=contract, request=request)
    _require_expected_operation(
        request, dependency_id=CAP_003_SEARCH_PROJECTION, operation_name=OP_RESOLVE_SEARCH_SOURCE
    )
    matches = tuple(
        source
        for source in current_sources
        if source.organization == request.organization
        and source.subject_id == hit.source_subject_id
        and source.version_id == hit.source_version_id
        and source.canonical_record.semantic_type == hit.source_semantic_type
    )
    if len(matches) != 1:
        raise ProductCapabilityConsumptionError("exact governed search source is not uniquely resolvable")
    _require_canonical_read(contract, request, matches[0].canonical_record)
    return resolve_search_hit_for_access(
        hit=hit, current_sources=current_sources, request=request.access
    )


def consume_reconstruction(
    *,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    manifest: ReconstructionManifest,
    evidence_constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...],
) -> AuditReconstructionView:
    """Consume CAP-004 derived reconstruction without creating source authority."""

    validate_capability_consumption(contract=contract, request=request)
    _require_expected_operation(
        request,
        dependency_id=CAP_004_AUDIT_RECONSTRUCTION,
        operation_name=OP_RECONSTRUCT_EXECUTION,
    )
    return reconstruct_audit_for_access(
        manifest=manifest,
        request=request.access,
        evidence_constraints=evidence_constraints,
    )
