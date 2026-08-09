"""P5.03 — governed dependency/version resolution and compatibility semantics.

RFC-0004 ``ProductContract`` remains the single executable semantic owner for the
bounded product/platform dependency declaration. This module adds an internal,
provisional and static resolver around that exact declaration. It does not define
a second Product Contract, public SDK/API, package contract, version-negotiation
protocol, registry service, serialization format or capability-lifecycle authority.

The current Provisional baseline intentionally uses one compatibility rule only:
the dependency contract version declared by the exact effective Product Contract
must be present exactly and must have explicit governed support evidence. The
resolver never guesses compatibility from semantic-version syntax, Python package
versions, module paths, dataclass shapes or operation-token spelling.

Provider lifecycle/support evidence is supplied explicitly by the caller together
with a governance reference. The resolver may inspect that evidence; it does not
promote, deprecate or retire capabilities and does not treat the evidence object as
an independent source of Product Contract semantics.

Resolution/evaluation grants no Authentication, Authorization, permission,
Organizational Authority, approval or data right. Required operation gates and
failure behavior remain declarations owned by the exact Product Contract and are
preserved in compatibility evidence for downstream integration tooling.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .execution import GovernedVersionPin
from .identity import Identity
from .product_contract import ProductContract
from .product_contract_declaration import validate_product_contract_declaration


class DependencySupportDisposition(str, Enum):
    """Governed support state for one exact dependency contract version.

    This is provider/version support evidence, not Platform Capability lifecycle.
    Capability lifecycle remains owned by RFC-0001 governance and its canonical
    catalog/decision records.
    """

    SUPPORTED = "Supported"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"
    UNSUPPORTED = "Unsupported"


class DependencyCompatibilityDecision(str, Enum):
    """Explicit P5.03 compatibility outcome for one declared dependency."""

    COMPATIBLE = "Compatible"
    VERSION_MISMATCH = "VersionMismatch"
    UNSUPPORTED = "Unsupported"
    DEPRECATED = "Deprecated"
    RETIRED = "Retired"
    AMBIGUOUS = "Ambiguous"


class DependencyResolutionError(RuntimeError):
    """Base fail-closed error for governed dependency/version resolution."""


class ProductContractResolutionContinuityError(DependencyResolutionError):
    """The resolver was asked to rely on a different Product Contract version."""


class IncompatibleDependencyVersionError(DependencyResolutionError):
    """Another dependency version exists, but exact declared compatibility does not."""


class UnsupportedDependencyResolutionError(DependencyResolutionError):
    """No supported exact dependency contract version is governed for reliance."""


class DeprecatedDependencyResolutionError(DependencyResolutionError):
    """The exact declared dependency version is deprecated and cannot be selected."""


class RetiredDependencyResolutionError(DependencyResolutionError):
    """The exact declared dependency version is retired and cannot be selected."""


class AmbiguousDependencyResolutionError(DependencyResolutionError):
    """Governed evidence contains more than one exact provider/version assertion."""


def _require_text(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


@dataclass(frozen=True, slots=True)
class GovernedDependencyVersionEvidence:
    """One explicit governed support assertion for an exact provider contract version.

    ``governance_reference`` identifies the canonical catalog/decision/provider
    evidence from which this observation was obtained. The object is an input
    snapshot for deterministic resolution, not an authority source of its own.

    Deprecated/retired versions require an explicit migration obligation so a
    changed relied-upon boundary cannot disappear behind a generic failure.
    """

    dependency_id: Identity
    contract_version: str
    disposition: DependencySupportDisposition
    governance_reference: str
    migration_obligation: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.dependency_id, Identity) or self.dependency_id.scope != "platform":
            raise ValueError("governed dependency evidence requires a platform-scoped Identity")
        _require_text(self.contract_version, label="governed dependency contract_version")
        if not isinstance(self.disposition, DependencySupportDisposition):
            raise ValueError("governed dependency disposition must be explicit")
        _require_text(self.governance_reference, label="governance reference")
        if self.migration_obligation is not None:
            _require_text(self.migration_obligation, label="migration obligation")
        if self.disposition in (
            DependencySupportDisposition.DEPRECATED,
            DependencySupportDisposition.RETIRED,
        ) and self.migration_obligation is None:
            raise ValueError(
                "deprecated/retired dependency evidence requires an explicit migration obligation"
            )


@dataclass(frozen=True, slots=True)
class DependencyCompatibilityEvaluation:
    """Immutable explicit compatibility evidence derived from one Product Contract."""

    product_contract: GovernedVersionPin
    dependency_id: Identity
    declared_contract_version: str
    allowed_operations: tuple[str, ...]
    provider_responsibility: str
    consumer_responsibility: str
    dependency_failure_behavior: str
    operation_failure_behaviors: tuple[tuple[str, str], ...]
    decision: DependencyCompatibilityDecision
    observed_contract_versions: tuple[str, ...]
    governance_references: tuple[str, ...]
    migration_obligation: str | None
    reason: str

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("dependency compatibility evidence requires exact Product Contract Version")
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("dependency compatibility evidence requires exact dependency Identity")
        _require_text(self.declared_contract_version, label="declared dependency contract_version")
        if not isinstance(self.allowed_operations, tuple) or not self.allowed_operations:
            raise ValueError("dependency compatibility evidence requires allowed operations")
        if any(not isinstance(item, str) or not item.strip() for item in self.allowed_operations):
            raise ValueError("dependency allowed operations must be non-empty strings")
        _require_text(self.provider_responsibility, label="dependency provider responsibility")
        _require_text(self.consumer_responsibility, label="dependency consumer responsibility")
        _require_text(self.dependency_failure_behavior, label="dependency failure behavior")
        if not isinstance(self.operation_failure_behaviors, tuple) or not self.operation_failure_behaviors:
            raise ValueError("dependency evaluation must preserve operation failure behavior")
        for operation_name, failure_behavior in self.operation_failure_behaviors:
            _require_text(operation_name, label="operation name")
            _require_text(failure_behavior, label="operation failure behavior")
        if not isinstance(self.decision, DependencyCompatibilityDecision):
            raise ValueError("dependency compatibility decision must be explicit")
        if not isinstance(self.observed_contract_versions, tuple):
            raise ValueError("observed dependency versions must be an immutable tuple")
        if any(not isinstance(item, str) or not item.strip() for item in self.observed_contract_versions):
            raise ValueError("observed dependency versions must be non-empty strings")
        if not isinstance(self.governance_references, tuple):
            raise ValueError("governance references must be an immutable tuple")
        if any(not isinstance(item, str) or not item.strip() for item in self.governance_references):
            raise ValueError("governance references must be non-empty strings")
        if self.migration_obligation is not None:
            _require_text(self.migration_obligation, label="compatibility migration obligation")
        _require_text(self.reason, label="compatibility reason")


@dataclass(frozen=True, slots=True)
class DependencyCompatibilityReport:
    """Whole-Product-Contract dependency compatibility evidence.

    This report is derived and immutable. It has no permission, authority,
    capability-lifecycle or activation semantics.
    """

    product_contract: GovernedVersionPin
    product_id: Identity
    product_version: str
    evaluations: tuple[DependencyCompatibilityEvaluation, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("compatibility report requires exact Product Contract Version")
        if not isinstance(self.product_id, Identity):
            raise ValueError("compatibility report requires exact Product identity")
        _require_text(self.product_version, label="compatibility report product_version")
        if not isinstance(self.evaluations, tuple) or not self.evaluations:
            raise ValueError("compatibility report requires dependency evaluations")
        if any(not isinstance(item, DependencyCompatibilityEvaluation) for item in self.evaluations):
            raise ValueError("compatibility report contains invalid dependency evaluation")

    @property
    def is_compatible(self) -> bool:
        return all(
            item.decision is DependencyCompatibilityDecision.COMPATIBLE
            for item in self.evaluations
        )


def _operation_failure_behaviors(
    *, contract: ProductContract, dependency_id: Identity
) -> tuple[tuple[str, str], ...]:
    return tuple(
        (operation.operation_name, operation.failure_behavior)
        for operation in contract.operations
        if operation.dependency_id == dependency_id
    )


def _evaluation_for_dependency(
    *,
    contract: ProductContract,
    dependency,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> DependencyCompatibilityEvaluation:
    by_dependency = tuple(
        item for item in governed_versions if item.dependency_id == dependency.dependency_id
    )
    exact = tuple(
        item for item in by_dependency if item.contract_version == dependency.contract_version
    )
    observed_versions = tuple(dict.fromkeys(item.contract_version for item in by_dependency))
    governance_references = tuple(dict.fromkeys(item.governance_reference for item in by_dependency))
    operation_failures = _operation_failure_behaviors(
        contract=contract,
        dependency_id=dependency.dependency_id,
    )

    if len(exact) > 1:
        decision = DependencyCompatibilityDecision.AMBIGUOUS
        migration_obligation = None
        reason = (
            "More than one governed support assertion exists for the exact declared dependency "
            "contract version; resolution fails closed until the governed evidence is unambiguous."
        )
    elif not exact and by_dependency:
        decision = DependencyCompatibilityDecision.VERSION_MISMATCH
        migration_obligation = (
            "Create and review a new immutable Product Contract version before relying on any "
            f"dependency contract version other than {dependency.contract_version}. "
            f"Current Product Contract exit path: {contract.exit_path}"
        )
        reason = (
            "Governed evidence exists for the dependency, but not for the exact contract version "
            "declared by the effective Product Contract. No version range or semantic-version "
            "compatibility is inferred."
        )
    elif not exact:
        decision = DependencyCompatibilityDecision.UNSUPPORTED
        migration_obligation = contract.exit_path
        reason = (
            "No governed support evidence exists for the exact dependency identity/version "
            "declared by the effective Product Contract."
        )
    else:
        governed = exact[0]
        governance_references = (governed.governance_reference,)
        observed_versions = (governed.contract_version,)
        migration_obligation = governed.migration_obligation
        if governed.disposition is DependencySupportDisposition.SUPPORTED:
            decision = DependencyCompatibilityDecision.COMPATIBLE
            reason = (
                "Exact dependency identity and contract version match the effective Product Contract, "
                "and governed provider evidence marks that exact version Supported for the declared scope."
            )
        elif governed.disposition is DependencySupportDisposition.DEPRECATED:
            decision = DependencyCompatibilityDecision.DEPRECATED
            reason = (
                "The exact dependency contract version is governed as Deprecated; new reliance is "
                "rejected and the explicit migration obligation must be handled through a new/revised contract."
            )
        elif governed.disposition is DependencySupportDisposition.RETIRED:
            decision = DependencyCompatibilityDecision.RETIRED
            reason = (
                "The exact dependency contract version is governed as Retired and cannot be selected "
                "for governed reliance."
            )
        else:
            decision = DependencyCompatibilityDecision.UNSUPPORTED
            reason = (
                "The exact dependency contract version is explicitly governed as Unsupported and "
                "cannot be selected for governed reliance."
            )

    return DependencyCompatibilityEvaluation(
        product_contract=contract.version_pin,
        dependency_id=dependency.dependency_id,
        declared_contract_version=dependency.contract_version,
        allowed_operations=dependency.allowed_operations,
        provider_responsibility=dependency.provider_responsibility,
        consumer_responsibility=dependency.consumer_responsibility,
        dependency_failure_behavior=dependency.failure_behavior,
        operation_failure_behaviors=operation_failures,
        decision=decision,
        observed_contract_versions=observed_versions,
        governance_references=governance_references,
        migration_obligation=migration_obligation,
        reason=reason,
    )


def evaluate_product_contract_dependencies(
    *,
    contract: ProductContract,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> DependencyCompatibilityReport:
    """Evaluate explicit dependency compatibility without selecting an alternative version.

    The exact Product Contract is revalidated first. ``effective_product_contract``
    is a required continuity pin so callers cannot silently resolve against a newer
    or different Product Contract version than the one they intend to rely upon.
    """

    if not isinstance(contract, ProductContract):
        raise TypeError("dependency resolution requires an explicit ProductContract semantic owner")
    if not isinstance(effective_product_contract, GovernedVersionPin):
        raise TypeError("dependency resolution requires an exact effective Product Contract Version pin")
    if not isinstance(governed_versions, tuple) or any(
        not isinstance(item, GovernedDependencyVersionEvidence) for item in governed_versions
    ):
        raise TypeError("governed_versions must be an immutable tuple of governed dependency evidence")

    validation = validate_product_contract_declaration(contract=contract)
    if validation.product_contract != contract.version_pin:
        raise ProductContractResolutionContinuityError(
            "declaration validation evidence does not preserve the source Product Contract Version"
        )
    if effective_product_contract != contract.version_pin:
        raise ProductContractResolutionContinuityError(
            "effective Product Contract Version does not match the exact Product Contract semantic owner"
        )

    evaluations = tuple(
        _evaluation_for_dependency(
            contract=contract,
            dependency=dependency,
            governed_versions=governed_versions,
        )
        for dependency in contract.dependencies
    )
    return DependencyCompatibilityReport(
        product_contract=contract.version_pin,
        product_id=contract.product_id,
        product_version=contract.product_version,
        evaluations=evaluations,
    )


def _raise_resolution_failure(evaluation: DependencyCompatibilityEvaluation) -> None:
    message = (
        f"dependency {evaluation.dependency_id.value} "
        f"{evaluation.declared_contract_version}: {evaluation.decision.value}. "
        f"{evaluation.reason} Product Contract failure behavior: "
        f"{evaluation.dependency_failure_behavior}"
    )
    if evaluation.migration_obligation is not None:
        message += f" Migration obligation: {evaluation.migration_obligation}"

    if evaluation.decision is DependencyCompatibilityDecision.VERSION_MISMATCH:
        raise IncompatibleDependencyVersionError(message)
    if evaluation.decision is DependencyCompatibilityDecision.DEPRECATED:
        raise DeprecatedDependencyResolutionError(message)
    if evaluation.decision is DependencyCompatibilityDecision.RETIRED:
        raise RetiredDependencyResolutionError(message)
    if evaluation.decision is DependencyCompatibilityDecision.AMBIGUOUS:
        raise AmbiguousDependencyResolutionError(message)
    raise UnsupportedDependencyResolutionError(message)


def resolve_product_contract_dependencies(
    *,
    contract: ProductContract,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> DependencyCompatibilityReport:
    """Resolve exact Product Contract dependencies or fail closed deterministically.

    Only ``Compatible`` evaluations are admitted. Deprecated, retired,
    unsupported, version-mismatched or ambiguous reliance raises a typed error.
    No fallback version is selected automatically.
    """

    report = evaluate_product_contract_dependencies(
        contract=contract,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
    for evaluation in report.evaluations:
        if evaluation.decision is not DependencyCompatibilityDecision.COMPATIBLE:
            _raise_resolution_failure(evaluation)
    return report
