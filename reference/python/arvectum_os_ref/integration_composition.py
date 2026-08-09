"""P5.04/R14 — internal/provisional integration composition facade boundary.

The facade is the smallest reusable integration-facing boundary justified by the
proved Phase 5 J1/J2 journeys. It composes existing RFC-0004 Product Contract
declaration validation, P5.03 exact dependency/version resolution, bounded
capability admission, workspace entry and Product Contract-backed Governed
Execution without becoming a new semantic owner.

R14 strengthens developer safety in two places:

* callers cannot construct a facade directly and bypass P5.02/P5.03 composition;
* every dependency-backed J1/J2 reliance must supply current governed
  dependency/version evidence and is re-resolved through the P5.03 semantic owner.

The composition-time compatibility report remains immutable inspection evidence.
It is not treated as indefinitely fresh provider-support authority.

This module deliberately does not define a Stable/public SDK, API, wire format,
serialization schema, package contract, registry, network protocol or service
boundary. The current Python class/module shape is internal and provisional
reference evidence only.

Authority, canonical-state, security and data-governance decisions remain with
the existing semantic owners. Successful facade composition or dependency
compatibility grants no Authentication, Authorization, permission,
Organizational Authority, approval, data right or capability lifecycle state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .execution import GovernedVersionPin
from .governed_execution import GovernedExecutionContext
from .identity import Identity
from .product_capability_consumption import (
    CapabilityConsumptionRequest,
    ProductCapabilityAdmission,
    validate_capability_consumption,
)
from .product_contract import (
    ProductContract,
    ProductContractScopeError,
    ProductRuntimeInteraction,
    start_product_governed_execution,
)
from .product_contract_declaration import (
    ProductContractDeclarationValidation,
    validate_product_contract_declaration,
)
from .product_contract_resolution import (
    DependencyCompatibilityDecision,
    DependencyCompatibilityEvaluation,
    DependencyCompatibilityReport,
    GovernedDependencyVersionEvidence,
    resolve_product_contract_dependencies,
)
from .security import ActorContext, OrganizationScope
from .workspace_shell import (
    WorkspaceDestination,
    WorkspaceProductContext,
    WorkspaceShellState,
    open_workspace_shell,
)


class IntegrationCompositionError(RuntimeError):
    """Base fail-closed error for the bounded integration composition boundary."""


class IntegrationCompositionContinuityError(IntegrationCompositionError):
    """Requested integration reliance drifted from the exact composed boundary."""


class IntegrationCompositionConstructionError(IntegrationCompositionError):
    """The facade was constructed outside the governed P5.02/P5.03 factory path."""


class IntegrationCompositionEvidenceRequiredError(IntegrationCompositionError):
    """Current governed dependency/version evidence was omitted for J1/J2 reliance."""


_INTERNAL_COMPOSITION_TOKEN = object()


@dataclass(frozen=True, slots=True)
class IntegrationCompositionContext:
    """Exact non-authoritative integration context preserved by the facade.

    This context is identity/version evidence only. It intentionally contains no
    authorization, authority, approval or capability-lifecycle decision.
    """

    organization: OrganizationScope
    actor: ActorContext
    product_id: Identity
    product_version: str
    product_contract: GovernedVersionPin

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("integration composition Organization scope must be explicit")
        if not isinstance(self.actor, ActorContext):
            raise ValueError("integration composition Actor must be attributable")
        if self.actor.organization != self.organization:
            raise ValueError("integration composition Actor and Organization must match")
        if not isinstance(self.product_id, Identity):
            raise ValueError("integration composition product identity must be explicit")
        if self.product_id.scope != self.organization.organization_id.value:
            raise ValueError("integration composition product identity must share Organization scope")
        if not isinstance(self.product_version, str) or not self.product_version.strip():
            raise ValueError("integration composition product_version must be explicit")
        if not isinstance(self.product_contract, GovernedVersionPin):
            raise ValueError("integration composition must preserve exact Product Contract Version")


class IntegrationCompositionFacade:
    """Internal facade over existing integration semantic owners.

    The facade owns composition continuity only. It does not evaluate current
    authorization, organizational authority, data rights, canonical mutation,
    approvals or capability lifecycle. Those decisions are delegated to the
    existing bounded semantic owners invoked below.

    Construction is intentionally restricted to :func:`compose_integration_facade`
    so callers cannot fabricate derived validation/compatibility evidence and skip
    the P5.02/P5.03 fail-closed path.
    """

    __slots__ = (
        "_contract",
        "_actor",
        "_declaration",
        "_compatibility",
        "_context",
    )

    def __init__(
        self,
        *,
        contract: ProductContract,
        actor: ActorContext,
        declaration: ProductContractDeclarationValidation,
        compatibility: DependencyCompatibilityReport,
        _construction_token: object | None = None,
    ) -> None:
        if _construction_token is not _INTERNAL_COMPOSITION_TOKEN:
            raise IntegrationCompositionConstructionError(
                "IntegrationCompositionFacade must be created through compose_integration_facade() "
                "so Product Contract declaration and dependency compatibility are validated by "
                "their existing semantic owners"
            )
        if not isinstance(contract, ProductContract):
            raise TypeError("integration facade requires the RFC-0004 ProductContract semantic owner")
        if not isinstance(actor, ActorContext):
            raise TypeError("integration facade requires an attributable ActorContext")
        if not isinstance(declaration, ProductContractDeclarationValidation):
            raise TypeError("integration facade requires P5.02 declaration-validation evidence")
        if not isinstance(compatibility, DependencyCompatibilityReport):
            raise TypeError("integration facade requires P5.03 compatibility evidence")
        if actor.organization != contract.organization:
            raise ProductContractScopeError(
                "integration facade Actor and Product Contract must share Organization scope"
            )
        if declaration.product_contract != contract.version_pin:
            raise IntegrationCompositionContinuityError(
                "declaration evidence does not preserve the exact Product Contract Version"
            )
        if compatibility.product_contract != contract.version_pin:
            raise IntegrationCompositionContinuityError(
                "compatibility evidence does not preserve the exact Product Contract Version"
            )
        if (
            compatibility.product_id != contract.product_id
            or compatibility.product_version != contract.product_version
        ):
            raise IntegrationCompositionContinuityError(
                "compatibility evidence does not preserve the exact Product identity/version"
            )
        if not compatibility.is_compatible:
            raise IntegrationCompositionContinuityError(
                "integration facade cannot compose non-compatible dependency reliance"
            )

        self._contract = contract
        self._actor = actor
        self._declaration = declaration
        self._compatibility = compatibility
        self._context = IntegrationCompositionContext(
            organization=contract.organization,
            actor=actor,
            product_id=contract.product_id,
            product_version=contract.product_version,
            product_contract=contract.version_pin,
        )

    @property
    def context(self) -> IntegrationCompositionContext:
        return self._context

    @property
    def declaration_evidence(self) -> ProductContractDeclarationValidation:
        """Return immutable P5.02 evidence, not a second editable contract source."""

        return self._declaration

    @property
    def compatibility_evidence(self) -> DependencyCompatibilityReport:
        """Return the composition-time P5.03 snapshot for inspection only.

        Dependency-backed J1/J2 actions never rely on this snapshot as current
        provider-support authority. They require explicit current governed evidence
        and re-run P5.03 resolution before reliance.
        """

        return self._compatibility

    def _resolve_current_compatibility(
        self,
        *,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
    ) -> DependencyCompatibilityReport:
        if governed_versions is None:
            raise IntegrationCompositionEvidenceRequiredError(
                "dependency-backed integration reliance requires explicit current governed "
                "dependency/version evidence; composition-time compatibility evidence is "
                "inspection history and must not self-advance"
            )
        report = resolve_product_contract_dependencies(
            contract=self._contract,
            effective_product_contract=self._context.product_contract,
            governed_versions=governed_versions,
        )
        if report.product_contract != self._context.product_contract:
            raise IntegrationCompositionContinuityError(
                "current compatibility resolution lost exact Product Contract Version continuity"
            )
        if (
            report.product_id != self._context.product_id
            or report.product_version != self._context.product_version
        ):
            raise IntegrationCompositionContinuityError(
                "current compatibility resolution lost exact Product identity/version continuity"
            )
        return report

    def _require_declared_compatible_operation(
        self,
        *,
        compatibility: DependencyCompatibilityReport,
        dependency_id: Identity,
        dependency_contract_version: str,
        operation_name: str,
    ) -> DependencyCompatibilityEvaluation:
        if not isinstance(dependency_id, Identity):
            raise TypeError("integration dependency identity must be explicit")
        if not isinstance(dependency_contract_version, str) or not dependency_contract_version.strip():
            raise ValueError("integration dependency contract version must be explicit")
        if not isinstance(operation_name, str) or not operation_name.strip():
            raise ValueError("integration operation_name must be explicit")

        matches = tuple(
            item for item in compatibility.evaluations if item.dependency_id == dependency_id
        )
        if len(matches) != 1:
            raise IntegrationCompositionContinuityError(
                "integration dependency must resolve to exactly one current compatibility evaluation"
            )
        evaluation = matches[0]
        if evaluation.decision is not DependencyCompatibilityDecision.COMPATIBLE:
            raise IntegrationCompositionContinuityError(
                "integration dependency is not compatible under current governed support evidence"
            )
        if evaluation.declared_contract_version != dependency_contract_version:
            raise IntegrationCompositionContinuityError(
                "integration dependency contract version drifted from the exact Product Contract"
            )
        if operation_name not in evaluation.allowed_operations:
            raise IntegrationCompositionContinuityError(
                "integration operation is outside the exact Product Contract dependency boundary"
            )
        return evaluation

    def admit_capability(
        self,
        request: CapabilityConsumptionRequest,
        *,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None = None,
    ) -> ProductCapabilityAdmission:
        """Delegate one J1 capability admission to its existing semantic owner.

        Current provider/version support is explicitly re-resolved before reliance.
        Authorization, purpose/right/classification and capability-specific semantics
        remain owned by their existing semantic owners.
        """

        if not isinstance(request, CapabilityConsumptionRequest):
            raise TypeError("integration capability admission requires CapabilityConsumptionRequest")
        if request.organization != self._context.organization:
            raise ProductContractScopeError(
                "capability request and integration facade must share Organization scope"
            )
        if request.access.actor != self._actor:
            raise ProductContractScopeError(
                "capability request Actor must match the composed integration Actor"
            )
        if (
            request.product_id != self._context.product_id
            or request.product_version != self._context.product_version
        ):
            raise ProductContractScopeError(
                "capability request must preserve the exact composed Product identity/version"
            )
        current_compatibility = self._resolve_current_compatibility(
            governed_versions=governed_versions
        )
        self._require_declared_compatible_operation(
            compatibility=current_compatibility,
            dependency_id=request.dependency_id,
            dependency_contract_version=request.dependency_contract_version,
            operation_name=request.operation_name,
        )
        return validate_capability_consumption(contract=self._contract, request=request)

    def open_workspace(
        self,
        *,
        initial_destination: WorkspaceDestination = WorkspaceDestination.DISCOVER,
    ) -> WorkspaceShellState:
        """Open non-authoritative workspace presentation with exact contract context.

        Workspace presentation is deliberately not dependency-backed governed
        reliance and therefore does not treat provider-support freshness as an
        authorization or authority gate.
        """

        workspace = open_workspace_shell(
            self._actor,
            product_context=WorkspaceProductContext(
                organization=self._context.organization,
                product_id=self._context.product_id,
                product_contract_version_id=self._context.product_contract.version_id,
            ),
            initial_destination=initial_destination,
        )
        if not isinstance(workspace, WorkspaceShellState):
            raise IntegrationCompositionError(
                "workspace semantic owner failed closed for the composed integration context"
            )
        if (
            workspace.product_context is None
            or workspace.product_context.product_contract_version_id
            != self._context.product_contract.version_id
        ):
            raise IntegrationCompositionContinuityError(
                "workspace entry lost exact Product Contract Version continuity"
            )
        return workspace

    def start_governed_execution(
        self,
        *,
        interaction: ProductRuntimeInteraction,
        execution_id: Identity,
        version_id: Identity,
        created_at: datetime,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None = None,
    ) -> GovernedExecutionContext:
        """Delegate one J2 consequential entry to the existing Governed Execution owner.

        Current dependency/provider support is explicitly re-resolved first. The
        facade then checks exact Product Contract/dependency/operation/product
        continuity. Authorization, Organizational Authority, Data Governance,
        validation and approval gates remain unsatisfied until RFC-0003/RFC-0005
        semantic owners evaluate them.
        """

        if not isinstance(interaction, ProductRuntimeInteraction):
            raise TypeError("governed integration action requires ProductRuntimeInteraction")
        if interaction.organization != self._context.organization:
            raise ProductContractScopeError(
                "governed interaction and integration facade must share Organization scope"
            )
        if (
            interaction.product_id != self._context.product_id
            or interaction.product_version != self._context.product_version
        ):
            raise ProductContractScopeError(
                "governed interaction must preserve the exact composed Product identity/version"
            )
        current_compatibility = self._resolve_current_compatibility(
            governed_versions=governed_versions
        )
        self._require_declared_compatible_operation(
            compatibility=current_compatibility,
            dependency_id=interaction.dependency_id,
            dependency_contract_version=interaction.dependency_contract_version,
            operation_name=interaction.operation_name,
        )

        execution = start_product_governed_execution(
            contract=self._contract,
            interaction=interaction,
            actor=self._actor,
            execution_id=execution_id,
            version_id=version_id,
            created_at=created_at,
        )
        if execution.product_contract != self._context.product_contract:
            raise IntegrationCompositionContinuityError(
                "Governed Execution lost the exact Product Contract Version used by the facade"
            )
        return execution


def compose_integration_facade(
    *,
    contract: ProductContract,
    actor: ActorContext,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> IntegrationCompositionFacade:
    """Build the bounded facade from exact governed boundary evidence.

    P5.02 declaration validation runs first, followed by P5.03 exact dependency
    resolution. No default/fallback provider version is inferred and no hidden
    product/platform coupling path is introduced by the facade.

    The supplied provider/version evidence establishes composition-time contract
    health only. Dependency-backed actions must provide current governed evidence
    again so a long-lived facade cannot self-advance stale support state.
    """

    if not isinstance(contract, ProductContract):
        raise TypeError("integration composition requires an explicit ProductContract")
    if not isinstance(actor, ActorContext):
        raise TypeError("integration composition requires an attributable ActorContext")
    if actor.organization != contract.organization:
        raise ProductContractScopeError(
            "integration composition Actor and Product Contract must share Organization scope"
        )

    declaration = validate_product_contract_declaration(contract=contract)
    compatibility = resolve_product_contract_dependencies(
        contract=contract,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
    return IntegrationCompositionFacade(
        contract=contract,
        actor=actor,
        declaration=declaration,
        compatibility=compatibility,
        _construction_token=_INTERNAL_COMPOSITION_TOKEN,
    )
