"""P8.06 — external product/extension onboarding and governed dependency resolution.

This internal reference slice proves that a separately maintained external consumer
can be admitted only through an exact Provisional Product Contract, an exact
product-owned source declaration and current governed provider/version evidence.

It deliberately does not define a public SDK/API, package/registry protocol,
installation service, stable manifest schema, authorization system, capability
lifecycle transition or durable shared state. Consumer-source evidence is caller-
supplied and pinned to an immutable repository commit/blob; the Product Contract
remains the single executable semantic owner of product/platform reliance.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import re

from .execution import GovernedVersionPin
from .identity import Identity
from .product_capability_consumption import (
    CapabilityConsumptionRequest,
    ProductCapabilityAdmission,
    validate_capability_consumption,
)
from .product_contract import (
    ProductBoundaryMechanism,
    ProductContract,
    ProductContractValidationError,
)
from .product_contract_declaration import validate_product_contract_declaration
from .product_contract_resolution import (
    DependencyCompatibilityDecision,
    GovernedDependencyVersionEvidence,
    resolve_product_contract_dependencies,
)
from .security import OrganizationScope


_GIT_SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class ExternalConsumerOnboardingError(ProductContractValidationError):
    """External source evidence cannot be reconciled with the governed boundary."""


class ExternalConsumerRelianceStateError(ExternalConsumerOnboardingError):
    """A disable/remove/upgrade transition is not safe from the current reliance state."""


class ExternalConsumerRelianceState(str, Enum):
    """Operational reliance state; explicitly not a governed lifecycle model."""

    ONBOARDED = "Onboarded"
    DISABLED = "Disabled"
    REMOVED = "Removed"


def _require_text(value: str, *, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")


def _require_git_sha(value: str, *, label: str) -> None:
    if not isinstance(value, str) or _GIT_SHA_RE.fullmatch(value) is None:
        raise ValueError(f"{label} must be an exact lowercase 40-character Git SHA")


@dataclass(frozen=True, slots=True)
class ExternalConsumerSourceEvidence:
    """Immutable evidence tying one external declaration to an exact source revision.

    The declaration format remains owned by the external product. This object is a
    bounded P8.06 evidence handoff, not a platform manifest or remote registry row.
    """

    repository: str
    commit_sha: str
    declaration_path: str
    declaration_blob_sha: str
    declaration_format_owner: str
    declaration_format_status: str
    owner: str
    consumer_id: Identity
    consumer_version: str
    organization: OrganizationScope
    declared_dependency_id: Identity
    dependency_contract_version: str
    operation_name: str
    purpose: str
    required_rights: tuple[str, ...]
    allowed_classifications: tuple[str, ...]
    boundary_mechanisms: tuple[ProductBoundaryMechanism, ...]
    shared_mutable_state: bool
    product_owned_semantics: tuple[str, ...]
    enabled_by_default: bool = False

    def __post_init__(self) -> None:
        _require_text(self.repository, label="external consumer repository")
        if self.repository.count("/") != 1 or any(char.isspace() for char in self.repository):
            raise ValueError("external consumer repository must be an exact owner/name reference")
        _require_git_sha(self.commit_sha, label="external consumer commit_sha")
        _require_text(self.declaration_path, label="external declaration path")
        if self.declaration_path.startswith("/") or ".." in self.declaration_path.split("/"):
            raise ValueError("external declaration path must be repository-relative")
        _require_git_sha(self.declaration_blob_sha, label="external declaration blob SHA")
        _require_text(self.declaration_format_owner, label="declaration format owner")
        _require_text(self.declaration_format_status, label="declaration format status")
        _require_text(self.owner, label="external consumer owner")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("external consumer Organization scope must be explicit")
        if not isinstance(self.consumer_id, Identity):
            raise ValueError("external consumer identity must be explicit")
        if self.consumer_id.scope != self.organization.organization_id.value:
            raise ValueError("external consumer identity must share Organization scope")
        _require_text(self.consumer_version, label="external consumer version")
        if not isinstance(self.declared_dependency_id, Identity) or self.declared_dependency_id.scope != "platform":
            raise ValueError("external dependency must be a platform-scoped Identity")
        _require_text(self.dependency_contract_version, label="external dependency contract version")
        _require_text(self.operation_name, label="external dependency operation")
        _require_text(self.purpose, label="external consumer purpose")
        if not isinstance(self.required_rights, tuple) or not self.required_rights:
            raise ValueError("external consumer required_rights must be an immutable non-empty tuple")
        if len(set(self.required_rights)) != len(self.required_rights) or any(
            not isinstance(value, str) or not value.strip() for value in self.required_rights
        ):
            raise ValueError("external consumer required_rights must contain unique explicit values")
        if not isinstance(self.allowed_classifications, tuple) or not self.allowed_classifications:
            raise ValueError("external consumer allowed_classifications must be explicit")
        if len(set(self.allowed_classifications)) != len(self.allowed_classifications) or any(
            not isinstance(value, str) or not value.strip() for value in self.allowed_classifications
        ):
            raise ValueError("external consumer classifications must contain unique explicit values")
        if not isinstance(self.boundary_mechanisms, tuple) or not self.boundary_mechanisms:
            raise ValueError("external consumer boundary mechanism must be explicit")
        if any(not isinstance(value, ProductBoundaryMechanism) for value in self.boundary_mechanisms):
            raise ValueError("external consumer boundary mechanisms must use governed mechanism values")
        if not isinstance(self.shared_mutable_state, bool):
            raise ValueError("shared_mutable_state attestation must be explicit")
        if not isinstance(self.product_owned_semantics, tuple) or not self.product_owned_semantics:
            raise ValueError("external consumer must preserve explicit product-owned semantics")
        if any(not isinstance(value, str) or not value.strip() for value in self.product_owned_semantics):
            raise ValueError("product-owned semantics must contain explicit values")
        if not isinstance(self.enabled_by_default, bool):
            raise ValueError("enabled_by_default must be explicit")


@dataclass(frozen=True, slots=True)
class ExternalConsumerOnboardingReceipt:
    """Derived bounded onboarding evidence; not permission, authority or registry state."""

    repository: str
    source_commit_sha: str
    declaration_path: str
    declaration_blob_sha: str
    owner: str
    consumer_id: Identity
    consumer_version: str
    organization: OrganizationScope
    product_contract: GovernedVersionPin
    dependency_id: Identity
    dependency_contract_version: str
    operation_name: str
    provider_governance_reference: str
    state: ExternalConsumerRelianceState
    transition_reason: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.repository, label="onboarding repository")
        _require_git_sha(self.source_commit_sha, label="onboarding source commit")
        _require_text(self.declaration_path, label="onboarding declaration path")
        _require_git_sha(self.declaration_blob_sha, label="onboarding declaration blob SHA")
        _require_text(self.owner, label="onboarding owner")
        if not isinstance(self.consumer_id, Identity):
            raise ValueError("onboarding consumer identity must be explicit")
        _require_text(self.consumer_version, label="onboarding consumer version")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("onboarding Organization must be explicit")
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("onboarding must preserve exact Product Contract Version")
        if not isinstance(self.dependency_id, Identity):
            raise ValueError("onboarding dependency identity must be explicit")
        _require_text(self.dependency_contract_version, label="onboarding dependency contract version")
        _require_text(self.operation_name, label="onboarding operation")
        _require_text(self.provider_governance_reference, label="provider governance reference")
        if not isinstance(self.state, ExternalConsumerRelianceState):
            raise ValueError("onboarding reliance state must be explicit")
        if self.transition_reason is not None:
            _require_text(self.transition_reason, label="onboarding transition reason")


def _require_exact_external_boundary(
    *,
    source: ExternalConsumerSourceEvidence,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
) -> None:
    if source.declaration_format_owner == "arvectum/arvectum-os":
        raise ExternalConsumerOnboardingError(
            "external declaration format must remain consumer-owned rather than becoming a platform manifest"
        )
    if source.enabled_by_default:
        raise ExternalConsumerOnboardingError(
            "external reliance must not activate merely because a declaration is installed"
        )
    if source.boundary_mechanisms != (ProductBoundaryMechanism.DECLARED_PLATFORM_CONTRACT,):
        raise ExternalConsumerOnboardingError(
            "external onboarding rejects direct table/import/endpoint/stream/shared-state coupling"
        )
    if source.shared_mutable_state:
        raise ExternalConsumerOnboardingError("external onboarding rejects hidden shared mutable state")
    if source.organization != contract.organization or source.organization != request.organization:
        raise ExternalConsumerOnboardingError("external consumer, Product Contract and request must share Organization")
    if source.consumer_id != contract.product_id or source.consumer_id != request.product_id:
        raise ExternalConsumerOnboardingError("external consumer identity does not match the Product Contract/request")
    if source.consumer_version != contract.product_version or source.consumer_version != request.product_version:
        raise ExternalConsumerOnboardingError("external consumer version does not match the Product Contract/request")
    if source.declared_dependency_id != request.dependency_id:
        raise ExternalConsumerOnboardingError("requested dependency is not the external declaration dependency")
    if source.dependency_contract_version != request.dependency_contract_version:
        raise ExternalConsumerOnboardingError("requested dependency version is not the external declaration version")
    if source.operation_name != request.operation_name:
        raise ExternalConsumerOnboardingError("requested operation is not the external declaration operation")
    if source.required_rights != (request.access.required_right,):
        raise ExternalConsumerOnboardingError(
            "current access must request exactly the single least-privilege right declared externally"
        )
    if source.purpose != request.access.purpose:
        raise ExternalConsumerOnboardingError("current access purpose must match the external declaration")
    if source.allowed_classifications != request.access.allowed_classifications:
        raise ExternalConsumerOnboardingError(
            "current classification scope must match the bounded external declaration exactly"
        )


def onboard_external_consumer(
    *,
    source: ExternalConsumerSourceEvidence,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> ExternalConsumerOnboardingReceipt:
    """Admit one exact external reliance after Product Contract and provider resolution.

    Resolution is deliberately static and fail-closed. A successful receipt records
    compatibility evidence but grants no authentication, authorization, permission,
    Organizational Authority, capability lifecycle transition or canonical mutation.
    """

    if not isinstance(source, ExternalConsumerSourceEvidence):
        raise TypeError("external onboarding requires exact source evidence")
    if not isinstance(contract, ProductContract):
        raise TypeError("external onboarding requires an explicit ProductContract")
    if not isinstance(request, CapabilityConsumptionRequest):
        raise TypeError("external onboarding requires an explicit capability request")
    if not isinstance(effective_product_contract, GovernedVersionPin):
        raise TypeError("external onboarding requires exact effective Product Contract Version")
    if not isinstance(governed_versions, tuple):
        raise TypeError("external onboarding requires immutable governed provider evidence")

    _require_exact_external_boundary(source=source, contract=contract, request=request)
    validate_product_contract_declaration(contract=contract)
    admission: ProductCapabilityAdmission = validate_capability_consumption(
        contract=contract,
        request=request,
    )
    report = resolve_product_contract_dependencies(
        contract=contract,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )

    evaluations = tuple(item for item in report.evaluations if item.dependency_id == request.dependency_id)
    if len(evaluations) != 1:
        raise ExternalConsumerOnboardingError("resolved dependency must be represented exactly once")
    evaluation = evaluations[0]
    if evaluation.decision is not DependencyCompatibilityDecision.COMPATIBLE:
        raise ExternalConsumerOnboardingError("external dependency resolution did not produce Compatible evidence")
    if request.operation_name not in evaluation.allowed_operations:
        raise ExternalConsumerOnboardingError("resolved dependency evidence does not preserve the requested operation")
    if len(evaluation.governance_references) != 1:
        raise ExternalConsumerOnboardingError("exact external provider compatibility requires one governance reference")
    if admission.product_contract_version_id != contract.record.version_id:
        raise ExternalConsumerOnboardingError("capability admission lost exact Product Contract Version continuity")

    return ExternalConsumerOnboardingReceipt(
        repository=source.repository,
        source_commit_sha=source.commit_sha,
        declaration_path=source.declaration_path,
        declaration_blob_sha=source.declaration_blob_sha,
        owner=source.owner,
        consumer_id=source.consumer_id,
        consumer_version=source.consumer_version,
        organization=source.organization,
        product_contract=report.product_contract,
        dependency_id=request.dependency_id,
        dependency_contract_version=request.dependency_contract_version,
        operation_name=request.operation_name,
        provider_governance_reference=evaluation.governance_references[0],
        state=ExternalConsumerRelianceState.ONBOARDED,
    )


def require_external_consumer_enabled(
    receipt: ExternalConsumerOnboardingReceipt,
) -> ExternalConsumerOnboardingReceipt:
    """Fail closed when caller attempts reliance after disable/remove."""

    if not isinstance(receipt, ExternalConsumerOnboardingReceipt):
        raise TypeError("external reliance requires an onboarding receipt")
    if receipt.state is not ExternalConsumerRelianceState.ONBOARDED:
        raise ExternalConsumerRelianceStateError("external consumer reliance is not enabled")
    return receipt


def disable_external_consumer(
    receipt: ExternalConsumerOnboardingReceipt,
    *,
    reason: str,
) -> ExternalConsumerOnboardingReceipt:
    """Disable reliance without mutating product/platform canonical state."""

    require_external_consumer_enabled(receipt)
    _require_text(reason, label="external consumer disable reason")
    return replace(
        receipt,
        state=ExternalConsumerRelianceState.DISABLED,
        transition_reason=reason,
    )


def remove_external_consumer(
    receipt: ExternalConsumerOnboardingReceipt,
    *,
    reason: str,
) -> ExternalConsumerOnboardingReceipt:
    """Remove reliance only from an explicitly disabled state."""

    if not isinstance(receipt, ExternalConsumerOnboardingReceipt):
        raise TypeError("external removal requires an onboarding receipt")
    if receipt.state is not ExternalConsumerRelianceState.DISABLED:
        raise ExternalConsumerRelianceStateError("external consumer must be disabled before removal")
    _require_text(reason, label="external consumer removal reason")
    return replace(
        receipt,
        state=ExternalConsumerRelianceState.REMOVED,
        transition_reason=reason,
    )


def upgrade_external_consumer(
    *,
    previous: ExternalConsumerOnboardingReceipt,
    source: ExternalConsumerSourceEvidence,
    contract: ProductContract,
    request: CapabilityConsumptionRequest,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> ExternalConsumerOnboardingReceipt:
    """Re-run exact onboarding for a new immutable consumer/contract source version."""

    if not isinstance(previous, ExternalConsumerOnboardingReceipt):
        raise TypeError("external upgrade requires the previous onboarding receipt")
    require_external_consumer_enabled(previous)
    if source.repository != previous.repository or source.consumer_id != previous.consumer_id:
        raise ExternalConsumerRelianceStateError("external upgrade must preserve repository and consumer identity")
    if source.consumer_version == previous.consumer_version:
        raise ExternalConsumerRelianceStateError("external upgrade requires a new immutable consumer version")
    if source.commit_sha == previous.source_commit_sha:
        raise ExternalConsumerRelianceStateError("external upgrade requires a new immutable source commit")
    if effective_product_contract.version_id == previous.product_contract.version_id:
        raise ExternalConsumerRelianceStateError(
            "external upgrade requires a new immutable Product Contract Version"
        )

    return onboard_external_consumer(
        source=source,
        contract=contract,
        request=request,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
