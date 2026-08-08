"""P2.07 — bounded Product Contract runtime validation boundary.

This module makes the RFC-0004 product/platform boundary executable for the
first reusable product-like Core Runtime entry without defining product-domain
semantics or a stable public Product Contract schema.

The implementation is intentionally internal, in-memory and provisional.  It
validates only the declarations required by the exercised runtime interaction:

* exact Product Contract Subject/Version identity and lifecycle;
* exact product identity/version and Organization scope;
* declared platform dependency/version/operation reliance;
* declared canonical read/write authority scope;
* required security/authority/data-governance gates;
* explicit portability, retention/deletion and failure responsibilities;
* rejection of hidden internal tables/imports/endpoints/streams/shared state;
* exact Product Contract version pinning into RFC-0005 Governed Execution.

Product Contract possession or validation is not authentication, authorization,
Organizational Authority, approval, capability activation or a conformance
claim.  The boundary selects no registry service, IAM provider, persistence,
wire format, SDK/API, capability lifecycle transition or product-specific rule.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .execution import GovernedVersionPin
from .governed_execution import (
    GovernedExecutionContext,
    GovernedGateKind,
    start_governed_execution,
)
from .identity import Identity
from .security import ActorContext, OrganizationScope
from .workflow import OperationSideEffectClass, WorkflowDefinition


PRODUCT_CONTRACT_SEMANTIC_TYPE: Final = "platform.product-contract"
PRODUCT_CONTRACT_AUTHORITY_SCOPE: Final = "platform.product-contract/boundary"


class ProductContractLifecycle(str, Enum):
    """RFC-0004 Product Contract lifecycle labels."""

    DRAFT = "Draft"
    PROVISIONAL = "Provisional"
    STABLE = "Stable"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"


class CanonicalAccessMode(str, Enum):
    """Boundary-relevant canonical-state access classes for the bounded validator."""

    READ = "Read"
    WRITE = "Write"


class ProductBoundaryMechanism(str, Enum):
    """Declared versus hidden product/platform coupling mechanisms.

    Only ``DECLARED_PLATFORM_CONTRACT`` is admitted by the P2.07 runtime entry.
    The remaining values exist so negative-path fitness tests can prove that a
    product-like consumer cannot smuggle platform reliance through internals.
    """

    DECLARED_PLATFORM_CONTRACT = "DeclaredPlatformContract"
    INTERNAL_TABLE = "InternalTable"
    INTERNAL_IMPORT = "InternalImport"
    UNDOCUMENTED_ENDPOINT = "UndocumentedEndpoint"
    PRIVATE_EVENT_STREAM = "PrivateEventStream"
    IMPLICIT_SHARED_STATE = "ImplicitSharedState"


class ProductContractValidationError(RuntimeError):
    """Base error for bounded RFC-0004 runtime-boundary validation failures."""


class ProductContractLifecycleError(ProductContractValidationError):
    """The supplied contract lifecycle is not admitted for this bounded entry."""


class ProductContractDependencyError(ProductContractValidationError):
    """The requested platform dependency/version/operation is not declared."""


class ProductContractOperationError(ProductContractValidationError):
    """Workflow operation semantics do not match the Product Contract declaration."""


class ProductContractCanonicalAccessError(ProductContractValidationError):
    """Required canonical read/write authority access is not declared."""


class ProductContractSecurityBoundaryError(ProductContractValidationError):
    """Required security/authority/data-governance gates are not preserved."""


class ProductContractScopeError(ProductContractValidationError):
    """Product, contract or runtime interaction crosses its declared Organization scope."""


class HiddenProductPlatformCouplingError(ProductContractValidationError):
    """The product attempted to rely on undeclared platform internals/shared state."""


def _require_text(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class PlatformDependencyDeclaration:
    """One bounded explicit platform dependency declared by the Product Contract.

    ``provisional`` is an interaction/support qualifier only.  It does not assign
    or imply an RFC-0001 Platform Capability lifecycle state.
    """

    dependency_id: Identity
    contract_version: str
    allowed_operations: tuple[str, ...]
    provider_responsibility: str
    consumer_responsibility: str
    failure_behavior: str
    provisional: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("platform dependency identity must be explicit")
        if self.dependency_id.scope != "platform":
            raise ValueError("bounded platform dependency identity must use platform scope")
        _require_text(self.contract_version, label="platform dependency contract_version")
        if not isinstance(self.allowed_operations, tuple) or not self.allowed_operations:
            raise ValueError("platform dependency must declare at least one allowed operation")
        if any(not isinstance(item, str) or not item.strip() for item in self.allowed_operations):
            raise ValueError("allowed platform operations must be non-empty strings")
        if len(set(self.allowed_operations)) != len(self.allowed_operations):
            raise ValueError("allowed platform operations must not contain duplicates")
        _require_text(self.provider_responsibility, label="provider responsibility")
        _require_text(self.consumer_responsibility, label="consumer responsibility")
        _require_text(self.failure_behavior, label="dependency failure behavior")
        if not isinstance(self.provisional, bool):
            raise ValueError("dependency provisional qualifier must be explicit")


@dataclass(frozen=True, slots=True)
class CanonicalAccessDeclaration:
    """One Product Contract declaration for canonical state crossing the boundary."""

    semantic_type: str
    authority_mode: AuthorityMode
    authority_scope: str
    access_modes: tuple[CanonicalAccessMode, ...]
    authoritative_source: str
    failure_behavior: str

    def __post_init__(self) -> None:
        _require_text(self.semantic_type, label="canonical access semantic_type")
        if not isinstance(self.authority_mode, AuthorityMode):
            raise ValueError("canonical access authority_mode must be explicit")
        _require_text(self.authority_scope, label="canonical access authority_scope")
        if not isinstance(self.access_modes, tuple) or not self.access_modes:
            raise ValueError("canonical access modes must be explicit")
        if any(not isinstance(item, CanonicalAccessMode) for item in self.access_modes):
            raise ValueError("canonical access modes must contain CanonicalAccessMode values")
        if len(set(self.access_modes)) != len(self.access_modes):
            raise ValueError("canonical access modes must not contain duplicates")
        _require_text(self.authoritative_source, label="canonical authoritative source")
        _require_text(self.failure_behavior, label="canonical access failure behavior")

    def permits(self, record: CanonicalRecord, mode: CanonicalAccessMode) -> bool:
        return (
            record.semantic_type == self.semantic_type
            and record.authority_mode is self.authority_mode
            and record.authority_scope == self.authority_scope
            and mode in self.access_modes
        )


@dataclass(frozen=True, slots=True)
class ProductOperationDeclaration:
    """Boundary-relevant semantics for one product-visible platform operation."""

    operation_name: str
    dependency_id: Identity
    side_effect_classes: tuple[OperationSideEffectClass, ...]
    required_gates: tuple[GovernedGateKind, ...]
    canonical_accesses: tuple[CanonicalAccessDeclaration, ...]
    failure_behavior: str

    def __post_init__(self) -> None:
        _require_text(self.operation_name, label="Product Contract operation_name")
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("Product Contract operation dependency_id must be an Identity")
        if self.dependency_id.scope != "platform":
            raise ValueError("Product Contract operation dependency must use platform scope")
        if not isinstance(self.side_effect_classes, tuple) or not self.side_effect_classes:
            raise ValueError("Product Contract operation side effects must be explicit")
        if any(not isinstance(item, OperationSideEffectClass) for item in self.side_effect_classes):
            raise ValueError("Product Contract side effects must use OperationSideEffectClass values")
        if len(set(self.side_effect_classes)) != len(self.side_effect_classes):
            raise ValueError("Product Contract side effects must not contain duplicates")
        if not isinstance(self.required_gates, tuple) or any(
            not isinstance(item, GovernedGateKind) for item in self.required_gates
        ):
            raise ValueError("Product Contract required_gates must use GovernedGateKind values")
        if len(set(self.required_gates)) != len(self.required_gates):
            raise ValueError("Product Contract required gates must not contain duplicates")
        if OperationSideEffectClass.CANONICAL_MUTATION in self.side_effect_classes and (
            GovernedGateKind.AUTHORIZATION not in self.required_gates
        ):
            raise ValueError("canonical mutation contract operation must require Authorization")
        if not isinstance(self.canonical_accesses, tuple) or any(
            not isinstance(item, CanonicalAccessDeclaration) for item in self.canonical_accesses
        ):
            raise ValueError("canonical_accesses must contain CanonicalAccessDeclaration values")
        _require_text(self.failure_behavior, label="Product Contract operation failure behavior")


@dataclass(frozen=True, slots=True)
class ProductContract:
    """Bounded internal representation of one exact Product Contract version.

    This dataclass is not a standardized manifest or public wire schema.  It
    carries only the RFC-0004 declarations needed by the P2.07 runtime evidence.
    """

    record: CanonicalRecord
    product_id: Identity
    product_version: str
    bounded_scope: str
    compatibility_assumptions: tuple[str, ...]
    dependencies: tuple[PlatformDependencyDeclaration, ...]
    operations: tuple[ProductOperationDeclaration, ...]
    portability_responsibility: str
    retention_deletion_responsibility: str
    review_condition: str
    exit_path: str

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Product Contract must use a CanonicalRecord envelope")
        if self.record.semantic_type != PRODUCT_CONTRACT_SEMANTIC_TYPE:
            raise ValueError("Product Contract semantic_type must be platform.product-contract")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("bounded P2.07 Product Contract record uses Native authority")
        if self.record.authority_scope != PRODUCT_CONTRACT_AUTHORITY_SCOPE:
            raise ValueError("Product Contract authority_scope must match the boundary contract scope")
        try:
            lifecycle = ProductContractLifecycle(self.record.lifecycle_status)
        except (TypeError, ValueError) as exc:
            raise ValueError("Product Contract lifecycle_status must be an RFC-0004 lifecycle value") from exc
        if not isinstance(self.product_id, Identity):
            raise ValueError("Product Contract must declare an exact product identity")
        organization_scope = self.record.organization.organization_id.value
        if self.record.subject_id.scope != organization_scope or self.record.version_id.scope != organization_scope:
            raise ValueError("Product Contract Subject/Version Identity must share Organization scope")
        if self.product_id.scope != organization_scope:
            raise ValueError("Product Contract product identity must share Organization scope")
        if self.product_id not in self.record.provenance_refs:
            raise ValueError("Product Contract provenance must identify the governed product")
        if self.record.accountable_owner_id not in self.record.provenance_refs:
            raise ValueError("Product Contract provenance must preserve its accountable owner")
        _require_text(self.product_version, label="Product Contract product_version")
        _require_text(self.bounded_scope, label="Product Contract bounded_scope")
        if not isinstance(self.compatibility_assumptions, tuple) or any(
            not isinstance(item, str) or not item.strip() for item in self.compatibility_assumptions
        ):
            raise ValueError("Product Contract compatibility_assumptions must be an immutable string tuple")
        if lifecycle is ProductContractLifecycle.PROVISIONAL and not self.compatibility_assumptions:
            raise ValueError("Provisional Product Contract must declare compatibility assumptions")
        if not isinstance(self.dependencies, tuple) or not self.dependencies or any(
            not isinstance(item, PlatformDependencyDeclaration) for item in self.dependencies
        ):
            raise ValueError("platform-interacting Product Contract requires explicit dependencies")
        if len({item.dependency_id for item in self.dependencies}) != len(self.dependencies):
            raise ValueError("Product Contract dependency identities must be unique in this bounded model")
        if not isinstance(self.operations, tuple) or not self.operations or any(
            not isinstance(item, ProductOperationDeclaration) for item in self.operations
        ):
            raise ValueError("platform-interacting Product Contract requires explicit operations")
        if len({item.operation_name for item in self.operations}) != len(self.operations):
            raise ValueError("Product Contract operation names must be unique")
        dependency_ids = {item.dependency_id for item in self.dependencies}
        if any(item.dependency_id not in dependency_ids for item in self.operations):
            raise ValueError("every Product Contract operation must reference a declared dependency")
        _require_text(self.portability_responsibility, label="Product Contract portability responsibility")
        _require_text(
            self.retention_deletion_responsibility,
            label="Product Contract retention/deletion responsibility",
        )
        _require_text(self.review_condition, label="Product Contract review condition")
        _require_text(self.exit_path, label="Product Contract exit path")

    @property
    def lifecycle(self) -> ProductContractLifecycle:
        return ProductContractLifecycle(self.record.lifecycle_status)

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    @property
    def version_pin(self) -> GovernedVersionPin:
        return GovernedVersionPin.from_record(self.record)


@dataclass(frozen=True, slots=True)
class ProductRuntimeInteraction:
    """One exact product-like request to enter reusable governed runtime behavior."""

    organization: OrganizationScope
    product_id: Identity
    product_version: str
    dependency_id: Identity
    dependency_contract_version: str
    workflow: WorkflowDefinition
    operation_name: str
    material_inputs: tuple[CanonicalRecord, ...]
    required_gates: tuple[GovernedGateKind, ...]
    mechanism: ProductBoundaryMechanism = ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("product runtime interaction Organization scope must be explicit")
        if not isinstance(self.product_id, Identity):
            raise ValueError("product runtime interaction product identity must be explicit")
        if self.product_id.scope != self.organization.organization_id.value:
            raise ValueError("product runtime product identity must share Organization scope")
        _require_text(self.product_version, label="product runtime product_version")
        if not isinstance(self.dependency_id, Identity) or self.dependency_id.scope != "platform":
            raise ValueError("product runtime dependency must be an explicit platform-scoped Identity")
        _require_text(self.dependency_contract_version, label="product runtime dependency contract version")
        if not isinstance(self.workflow, WorkflowDefinition) or self.workflow.organization != self.organization:
            raise ValueError("product runtime Workflow must share Organization scope")
        _require_text(self.operation_name, label="product runtime operation_name")
        if not isinstance(self.material_inputs, tuple) or not self.material_inputs:
            raise ValueError("product runtime interaction requires exact material input versions")
        if any(not isinstance(item, CanonicalRecord) for item in self.material_inputs):
            raise ValueError("product runtime material_inputs must contain CanonicalRecord versions")
        if any(item.organization != self.organization for item in self.material_inputs):
            raise ValueError("product runtime material inputs must share Organization scope")
        if not isinstance(self.required_gates, tuple) or any(
            not isinstance(item, GovernedGateKind) for item in self.required_gates
        ):
            raise ValueError("product runtime required_gates must use GovernedGateKind values")
        if len(set(self.required_gates)) != len(self.required_gates):
            raise ValueError("product runtime required_gates must not contain duplicates")
        if not isinstance(self.mechanism, ProductBoundaryMechanism):
            raise ValueError("product runtime boundary mechanism must be explicit")


@dataclass(frozen=True, slots=True)
class ProductContractAdmission:
    """Validated RFC-0004 boundary reliance for one exact runtime interaction.

    The result intentionally contains no authorization or Organizational
    Authority decision.  Those remain independent RFC-0003/RFC-0005 gates.
    """

    product_contract: GovernedVersionPin
    product_id: Identity
    dependency_id: Identity
    dependency_contract_version: str
    operation_name: str

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("Product Contract admission must preserve an exact governed version pin")
        if self.product_contract.semantic_type != PRODUCT_CONTRACT_SEMANTIC_TYPE:
            raise ValueError("Product Contract admission pin must reference platform.product-contract")


def _exact_dependency(
    contract: ProductContract,
    interaction: ProductRuntimeInteraction,
) -> PlatformDependencyDeclaration:
    matches = tuple(
        item for item in contract.dependencies if item.dependency_id == interaction.dependency_id
    )
    if len(matches) != 1:
        raise ProductContractDependencyError("requested platform dependency is not declared exactly once")
    dependency = matches[0]
    if dependency.contract_version != interaction.dependency_contract_version:
        raise ProductContractDependencyError("requested platform dependency contract version is incompatible")
    if interaction.operation_name not in dependency.allowed_operations:
        raise ProductContractDependencyError("requested runtime operation is not allowed by the dependency")
    return dependency


def _exact_contract_operation(
    contract: ProductContract,
    interaction: ProductRuntimeInteraction,
) -> ProductOperationDeclaration:
    matches = tuple(item for item in contract.operations if item.operation_name == interaction.operation_name)
    if len(matches) != 1:
        raise ProductContractOperationError("requested runtime operation is not declared exactly once")
    operation = matches[0]
    if operation.dependency_id != interaction.dependency_id:
        raise ProductContractOperationError("operation declaration references a different platform dependency")
    return operation


def _exact_workflow_operation(interaction: ProductRuntimeInteraction):
    matches = tuple(
        item for item in interaction.workflow.operations if item.semantic_name == interaction.operation_name
    )
    if len(matches) != 1:
        raise ProductContractOperationError("exact Workflow version must declare the requested operation once")
    return matches[0]


def _require_canonical_access(
    declarations: tuple[CanonicalAccessDeclaration, ...],
    record: CanonicalRecord,
    mode: CanonicalAccessMode,
) -> None:
    if not any(item.permits(record, mode) for item in declarations):
        raise ProductContractCanonicalAccessError(
            f"Product Contract does not permit canonical {mode.value} for {record.semantic_type}"
        )


def validate_product_contract_interaction(
    *,
    contract: ProductContract,
    interaction: ProductRuntimeInteraction,
) -> ProductContractAdmission:
    """Validate one exact product/platform runtime reliance before execution starts.

    The P2.07 slice admits ``Provisional`` contracts only.  ``Draft`` and
    ``Retired`` are invalid for governed reliance; ``Stable`` and ``Deprecated``
    require compatibility/support/deprecation evidence not represented by this
    intentionally minimal internal validator and therefore fail closed here
    rather than being accepted on incomplete evidence.
    """

    if not isinstance(contract, ProductContract):
        raise TypeError("product runtime entry requires an explicit ProductContract")
    if not isinstance(interaction, ProductRuntimeInteraction):
        raise TypeError("product runtime entry requires an explicit ProductRuntimeInteraction")
    if contract.lifecycle is not ProductContractLifecycle.PROVISIONAL:
        raise ProductContractLifecycleError(
            "bounded P2.07 runtime entry admits only an explicit Provisional Product Contract"
        )
    if contract.organization != interaction.organization:
        raise ProductContractScopeError("Product Contract and runtime interaction must share Organization scope")
    if contract.product_id != interaction.product_id:
        raise ProductContractScopeError("Product Contract governs a different product identity")
    if contract.product_version != interaction.product_version:
        raise ProductContractScopeError("Product Contract does not cover the requested product version")
    if interaction.mechanism is not ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT:
        raise HiddenProductPlatformCouplingError(
            "product runtime reliance through internal tables/imports/endpoints/streams/shared state is rejected"
        )

    _exact_dependency(contract, interaction)
    declared_operation = _exact_contract_operation(contract, interaction)
    workflow_operation = _exact_workflow_operation(interaction)

    if set(workflow_operation.side_effect_classes) != set(declared_operation.side_effect_classes):
        raise ProductContractOperationError(
            "Workflow side-effect semantics differ from the exact Product Contract operation declaration"
        )
    missing_gates = tuple(
        gate for gate in declared_operation.required_gates if gate not in interaction.required_gates
    )
    if missing_gates:
        names = ", ".join(item.value for item in missing_gates)
        raise ProductContractSecurityBoundaryError(
            f"runtime interaction omits Product Contract required gates: {names}"
        )

    for record in interaction.material_inputs:
        _require_canonical_access(
            declared_operation.canonical_accesses,
            record,
            CanonicalAccessMode.READ,
        )

    if OperationSideEffectClass.CANONICAL_MUTATION in workflow_operation.side_effect_classes:
        targets = tuple(
            record
            for record in interaction.material_inputs
            if record.subject_id == workflow_operation.target_subject_id
            and record.semantic_type == workflow_operation.target_semantic_type
        )
        if len(targets) != 1:
            raise ProductContractOperationError(
                "canonical mutation Workflow target must resolve to exactly one material input"
            )
        _require_canonical_access(
            declared_operation.canonical_accesses,
            targets[0],
            CanonicalAccessMode.WRITE,
        )

    return ProductContractAdmission(
        product_contract=contract.version_pin,
        product_id=interaction.product_id,
        dependency_id=interaction.dependency_id,
        dependency_contract_version=interaction.dependency_contract_version,
        operation_name=interaction.operation_name,
    )


def start_product_governed_execution(
    *,
    contract: ProductContract,
    interaction: ProductRuntimeInteraction,
    actor: ActorContext,
    execution_id: Identity,
    version_id: Identity,
    created_at: datetime,
) -> GovernedExecutionContext:
    """First reusable product-like runtime entry: validate contract, then start execution.

    Exact Product Contract attribution is passed into the RFC-0005 runtime only
    after RFC-0004 boundary validation succeeds.  Security and authority gates
    remain unresolved until their independent governed decisions are supplied.
    """

    admission = validate_product_contract_interaction(
        contract=contract,
        interaction=interaction,
    )
    if not isinstance(actor, ActorContext) or actor.organization != interaction.organization:
        raise ProductContractScopeError("product runtime actor must share the interaction Organization scope")
    return start_governed_execution(
        organization=interaction.organization,
        actor=actor,
        workflow=interaction.workflow,
        operation_name=interaction.operation_name,
        material_inputs=interaction.material_inputs,
        required_gates=interaction.required_gates,
        execution_id=execution_id,
        version_id=version_id,
        created_at=created_at,
        product_contract=admission.product_contract,
    )
