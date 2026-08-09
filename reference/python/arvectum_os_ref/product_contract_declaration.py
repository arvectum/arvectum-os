"""P5.02 — machine-checkable Product Contract declaration validation baseline.

RFC-0004 defines Product Contract semantics and deliberately does not standardize a
serialization format.  The existing :mod:`arvectum_os_ref.product_contract`
``ProductContract`` object remains the single executable declaration model for the
bounded reference implementation.  This module validates that declaration as a
whole and returns immutable inspection evidence; it does not define a second
manifest, registry, public SDK/API, wire format or compatibility contract.

The P5.02 baseline is intentionally bounded to current RFC-0004 ``Provisional``
integration journeys. P5.09 reuse evidence extends the original J1/J2 assumption:
read-only operations may legitimately expose only a derived governed view and
therefore have no direct canonical-access declaration. Where canonical access is
declared, its read/write, authority-source and failure semantics remain checked.

The validator checks:

* exact Product Contract Subject/Version and Product identity/version continuity;
* accountable owner, bounded scope and compatibility assumptions;
* explicit Provisional dependency/version/operation reliance and responsibilities;
* operation side-effect/gate/failure semantics;
* declared canonical read/write, authority-source and failure semantics where applicable;
* required Authorization/Data Governance and mutation authority gates;
* Organization scope, portability, retention/deletion, review and exit declarations;
* rejection of hidden product/platform coupling mechanisms.

A successful result is declaration-validation evidence only.  It grants no
Authentication, Authorization, Organizational Authority, approval, data right,
capability lifecycle transition, Product Contract stabilization or conformance
claim.  Capability lifecycle remains owned by the canonical capability catalog;
``PlatformDependencyDeclaration.provisional`` is only the existing RFC-0004
Product Contract reliance/support qualifier.

The Python types in this module are internal and provisional reference evidence.
They are not a standardized Product Contract schema or serialization contract.
"""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import AuthorityMode
from .execution import GovernedVersionPin
from .governed_execution import GovernedGateKind
from .identity import Identity
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
    ProductContractSecurityBoundaryError,
)
from .security import OrganizationScope
from .workflow import OperationSideEffectClass


_REQUIRED_GOVERNED_DATA_GATES = frozenset(
    (
        GovernedGateKind.AUTHORIZATION,
        GovernedGateKind.DATA_GOVERNANCE,
    )
)
_REQUIRED_CANONICAL_MUTATION_GATES = frozenset(
    (
        GovernedGateKind.AUTHORIZATION,
        GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
        GovernedGateKind.DATA_GOVERNANCE,
    )
)


def _require_text(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class DeclaredDependencyEvidence:
    """Immutable exact dependency evidence derived from one Product Contract.

    The responsibility/failure fields are copied from the Product Contract so
    downstream integration tooling does not accidentally treat this derived view
    as a narrower competing dependency contract. ``provisional`` remains only the
    Product Contract reliance/support qualifier.

    There is intentionally no capability-lifecycle or ``active`` field: provider
    lifecycle remains governed by its own canonical catalog/decision authority.
    """

    dependency_id: Identity
    contract_version: str
    allowed_operations: tuple[str, ...]
    provider_responsibility: str
    consumer_responsibility: str
    failure_behavior: str
    provisional: bool

    def __post_init__(self) -> None:
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("declared dependency evidence requires an exact Identity")
        _require_text(self.contract_version, label="declared dependency contract_version")
        if not isinstance(self.allowed_operations, tuple) or not self.allowed_operations:
            raise ValueError("declared dependency evidence requires allowed operations")
        if any(not isinstance(item, str) or not item.strip() for item in self.allowed_operations):
            raise ValueError("declared dependency operations must be non-empty strings")
        _require_text(self.provider_responsibility, label="declared provider responsibility")
        _require_text(self.consumer_responsibility, label="declared consumer responsibility")
        _require_text(self.failure_behavior, label="declared dependency failure behavior")
        if not isinstance(self.provisional, bool):
            raise ValueError("declared dependency provisional qualifier must be explicit")


@dataclass(frozen=True, slots=True)
class DeclaredCanonicalAccessEvidence:
    """Boundary-relevant canonical access evidence copied from the declaration."""

    operation_name: str
    semantic_type: str
    authority_mode: AuthorityMode
    authority_scope: str
    access_modes: tuple[CanonicalAccessMode, ...]
    authoritative_source: str
    failure_behavior: str

    def __post_init__(self) -> None:
        _require_text(self.operation_name, label="declared canonical access operation_name")
        _require_text(self.semantic_type, label="declared canonical access semantic_type")
        if not isinstance(self.authority_mode, AuthorityMode):
            raise ValueError("declared canonical access authority_mode must be explicit")
        _require_text(self.authority_scope, label="declared canonical access authority_scope")
        if not isinstance(self.access_modes, tuple) or not self.access_modes:
            raise ValueError("declared canonical access modes must be explicit")
        if any(not isinstance(item, CanonicalAccessMode) for item in self.access_modes):
            raise ValueError("declared canonical access modes must use CanonicalAccessMode values")
        _require_text(self.authoritative_source, label="declared canonical authoritative_source")
        _require_text(self.failure_behavior, label="declared canonical access failure_behavior")


@dataclass(frozen=True, slots=True)
class DeclaredOperationEvidence:
    """Immutable operation/gate/failure evidence derived from one Product Contract."""

    operation_name: str
    dependency_id: Identity
    side_effect_classes: tuple[OperationSideEffectClass, ...]
    required_gates: tuple[GovernedGateKind, ...]
    failure_behavior: str

    def __post_init__(self) -> None:
        _require_text(self.operation_name, label="declared operation_name")
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("declared operation evidence requires dependency Identity")
        if not isinstance(self.side_effect_classes, tuple) or not self.side_effect_classes:
            raise ValueError("declared operation side effects must be explicit")
        if any(not isinstance(item, OperationSideEffectClass) for item in self.side_effect_classes):
            raise ValueError("declared operation side effects must use OperationSideEffectClass values")
        if not isinstance(self.required_gates, tuple) or not self.required_gates:
            raise ValueError("declared operation required gates must be explicit")
        if any(not isinstance(item, GovernedGateKind) for item in self.required_gates):
            raise ValueError("declared operation gates must use GovernedGateKind values")
        _require_text(self.failure_behavior, label="declared operation failure behavior")


@dataclass(frozen=True, slots=True)
class ProductContractDeclarationValidation:
    """Immutable evidence that one exact declaration passed the bounded P5.02 checks.

    This result deliberately contains no authorization, authority-decision,
    approval, permission, capability-lifecycle or activation state.
    """

    product_contract: GovernedVersionPin
    product_id: Identity
    product_version: str
    organization: OrganizationScope
    accountable_owner_id: Identity
    lifecycle: ProductContractLifecycle
    bounded_scope: str
    compatibility_assumptions: tuple[str, ...]
    dependencies: tuple[DeclaredDependencyEvidence, ...]
    operations: tuple[DeclaredOperationEvidence, ...]
    canonical_accesses: tuple[DeclaredCanonicalAccessEvidence, ...]
    portability_responsibility: str
    retention_deletion_responsibility: str
    review_condition: str
    exit_path: str

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("declaration validation must preserve exact Product Contract Version")
        if not isinstance(self.product_id, Identity):
            raise ValueError("declaration validation must preserve exact Product identity")
        _require_text(self.product_version, label="validated product_version")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("declaration validation must preserve Organization scope")
        if not isinstance(self.accountable_owner_id, Identity):
            raise ValueError("declaration validation must preserve accountable owner")
        if not isinstance(self.lifecycle, ProductContractLifecycle):
            raise ValueError("declaration validation must preserve Product Contract lifecycle")
        _require_text(self.bounded_scope, label="validated bounded scope")
        if not isinstance(self.compatibility_assumptions, tuple) or not self.compatibility_assumptions:
            raise ValueError("declaration validation must preserve compatibility assumptions")
        if any(not isinstance(item, str) or not item.strip() for item in self.compatibility_assumptions):
            raise ValueError("validated compatibility assumptions must be non-empty strings")
        if not isinstance(self.dependencies, tuple) or not self.dependencies:
            raise ValueError("declaration validation must preserve dependencies")
        if any(not isinstance(item, DeclaredDependencyEvidence) for item in self.dependencies):
            raise ValueError("validated dependencies must contain declaration evidence")
        if not isinstance(self.operations, tuple) or not self.operations:
            raise ValueError("declaration validation must preserve operations")
        if any(not isinstance(item, DeclaredOperationEvidence) for item in self.operations):
            raise ValueError("validated operations must contain declaration evidence")
        if not isinstance(self.canonical_accesses, tuple):
            raise ValueError("declaration validation canonical access evidence must be an immutable tuple")
        if any(not isinstance(item, DeclaredCanonicalAccessEvidence) for item in self.canonical_accesses):
            raise ValueError("validated canonical accesses must contain declaration evidence")
        _require_text(self.portability_responsibility, label="validated portability responsibility")
        _require_text(
            self.retention_deletion_responsibility,
            label="validated retention/deletion responsibility",
        )
        _require_text(self.review_condition, label="validated review condition")
        _require_text(self.exit_path, label="validated exit path")


def _validate_boundary_mechanisms(
    mechanisms: tuple[ProductBoundaryMechanism, ...],
) -> None:
    if not isinstance(mechanisms, tuple) or not mechanisms:
        raise HiddenProductPlatformCouplingError(
            "Product Contract declaration validation requires an explicit boundary mechanism"
        )
    if any(not isinstance(item, ProductBoundaryMechanism) for item in mechanisms):
        raise HiddenProductPlatformCouplingError(
            "Product Contract boundary mechanisms must use declared mechanism values"
        )
    if len(set(mechanisms)) != len(mechanisms):
        raise HiddenProductPlatformCouplingError(
            "Product Contract boundary mechanisms must not contain duplicates"
        )
    hidden = tuple(
        item
        for item in mechanisms
        if item is not ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT
    )
    if hidden:
        labels = ", ".join(item.value for item in hidden)
        raise HiddenProductPlatformCouplingError(
            f"hidden product/platform coupling is not a valid Product Contract boundary: {labels}"
        )


def _validate_dependency_operation_graph(contract: ProductContract) -> None:
    declared_operations = {
        (item.dependency_id, item.operation_name): item for item in contract.operations
    }
    for dependency in contract.dependencies:
        if not dependency.provisional:
            raise ProductContractDependencyError(
                "bounded P5.02 validation requires dependency reliance to remain explicitly Provisional"
            )
        for operation_name in dependency.allowed_operations:
            if (dependency.dependency_id, operation_name) not in declared_operations:
                raise ProductContractDependencyError(
                    "dependency allows an operation without an exact Product Contract operation declaration"
                )
    for operation in contract.operations:
        matching = tuple(
            item for item in contract.dependencies if item.dependency_id == operation.dependency_id
        )
        if len(matching) != 1:
            raise ProductContractOperationError(
                "Product Contract operation must resolve to exactly one declared dependency"
            )
        if operation.operation_name not in matching[0].allowed_operations:
            raise ProductContractOperationError(
                "Product Contract operation is not allowed by its exact dependency declaration"
            )


def _validate_operation_security_and_access(contract: ProductContract) -> None:
    for operation in contract.operations:
        gate_set = set(operation.required_gates)
        if not _REQUIRED_GOVERNED_DATA_GATES.issubset(gate_set):
            raise ProductContractSecurityBoundaryError(
                f"operation {operation.operation_name} must declare Authorization and DataGovernance gates"
            )
        if OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes and not (
            _REQUIRED_CANONICAL_MUTATION_GATES.issubset(gate_set)
        ):
            raise ProductContractSecurityBoundaryError(
                f"canonical mutation operation {operation.operation_name} must also declare OrganizationalAuthority"
            )
        if operation.canonical_accesses and OperationSideEffectClass.READ_ONLY in operation.side_effect_classes and not any(
            CanonicalAccessMode.READ in item.access_modes for item in operation.canonical_accesses
        ):
            raise ProductContractCanonicalAccessError(
                f"read operation {operation.operation_name} with canonical access must declare canonical Read access"
            )
        if OperationSideEffectClass.CANONICAL_MUTATION in operation.side_effect_classes and not any(
            CanonicalAccessMode.WRITE in item.access_modes for item in operation.canonical_accesses
        ):
            raise ProductContractCanonicalAccessError(
                f"canonical mutation operation {operation.operation_name} must declare canonical Write access"
            )
        _require_text(operation.failure_behavior, label="Product Contract operation failure behavior")
        for access in operation.canonical_accesses:
            _require_text(access.authoritative_source, label="canonical authoritative_source")
            _require_text(access.failure_behavior, label="canonical access failure_behavior")


def validate_product_contract_declaration(
    *,
    contract: ProductContract,
    boundary_mechanisms: tuple[ProductBoundaryMechanism, ...] = (
        ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,
    ),
) -> ProductContractDeclarationValidation:
    """Validate the complete bounded declaration before governed platform reliance.

    P5.02 intentionally admits only ``Provisional`` Product Contracts because the
    current integration evidence does not contain the compatibility, support,
    conformance or deprecation evidence needed to validate ``Stable``,
    ``Deprecated`` or ``Retired`` declarations. Failing closed here avoids turning
    an internal validator into a lifecycle-promotion mechanism.

    P5.09 clarified that RFC-0004 canonical-state declarations are required where
    applicable: a derived read-only operation such as reconstruction may cross the
    Product Contract boundary without exposing a new direct canonical read. Empty
    ``canonical_accesses`` therefore means no direct canonical access is declared;
    it does not grant source access or bypass the owning capability's runtime checks.
    """

    if not isinstance(contract, ProductContract):
        raise TypeError("declaration validation requires an explicit ProductContract")
    if contract.lifecycle is not ProductContractLifecycle.PROVISIONAL:
        raise ProductContractLifecycleError(
            "bounded P5.02 declaration validation admits only an explicit Provisional Product Contract"
        )

    _validate_boundary_mechanisms(boundary_mechanisms)
    _validate_dependency_operation_graph(contract)
    _validate_operation_security_and_access(contract)

    _require_text(contract.bounded_scope, label="Product Contract bounded scope")
    if not contract.compatibility_assumptions:
        raise ProductContractLifecycleError(
            "Provisional Product Contract must declare compatibility assumptions"
        )
    _require_text(contract.portability_responsibility, label="Product Contract portability responsibility")
    _require_text(
        contract.retention_deletion_responsibility,
        label="Product Contract retention/deletion responsibility",
    )
    _require_text(contract.review_condition, label="Product Contract review condition")
    _require_text(contract.exit_path, label="Product Contract exit path")

    dependencies = tuple(
        DeclaredDependencyEvidence(
            dependency_id=item.dependency_id,
            contract_version=item.contract_version,
            allowed_operations=item.allowed_operations,
            provider_responsibility=item.provider_responsibility,
            consumer_responsibility=item.consumer_responsibility,
            failure_behavior=item.failure_behavior,
            provisional=item.provisional,
        )
        for item in contract.dependencies
    )
    operations = tuple(
        DeclaredOperationEvidence(
            operation_name=item.operation_name,
            dependency_id=item.dependency_id,
            side_effect_classes=item.side_effect_classes,
            required_gates=item.required_gates,
            failure_behavior=item.failure_behavior,
        )
        for item in contract.operations
    )
    canonical_accesses = tuple(
        DeclaredCanonicalAccessEvidence(
            operation_name=operation.operation_name,
            semantic_type=access.semantic_type,
            authority_mode=access.authority_mode,
            authority_scope=access.authority_scope,
            access_modes=access.access_modes,
            authoritative_source=access.authoritative_source,
            failure_behavior=access.failure_behavior,
        )
        for operation in contract.operations
        for access in operation.canonical_accesses
    )

    return ProductContractDeclarationValidation(
        product_contract=contract.version_pin,
        product_id=contract.product_id,
        product_version=contract.product_version,
        organization=contract.organization,
        accountable_owner_id=contract.record.accountable_owner_id,
        lifecycle=contract.lifecycle,
        bounded_scope=contract.bounded_scope,
        compatibility_assumptions=contract.compatibility_assumptions,
        dependencies=dependencies,
        operations=operations,
        canonical_accesses=canonical_accesses,
        portability_responsibility=contract.portability_responsibility,
        retention_deletion_responsibility=contract.retention_deletion_responsibility,
        review_condition=contract.review_condition,
        exit_path=contract.exit_path,
    )