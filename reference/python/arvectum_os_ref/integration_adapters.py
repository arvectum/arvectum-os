"""P5.08/R15/R16 + P6.05 — internal/provisional integration adapter boundary.

P5.08 introduced one integration-facing seam over the R14-hardened Phase 5
composition facade. R15 narrows the reusable core to what both materially
distinct consumers actually demonstrate: one exact composed facade plus bounded
capability delegation. Workspace presentation remains available, but is an
explicit optional binding for consumers that need it rather than an eagerly
constructed assumption carried by every integration.

R16 hardens Product Contract continuity at the adapter layer. A capability
adapter may still carry the exact Product Contract semantic owner needed by the
capability-specific delegates, but that declaration must exactly match the
immutable P5.02 declaration evidence already validated during facade composition.
A caller therefore cannot pair one governed facade with alternate same-version
contract semantics and create a split product/platform boundary.

P6.05 exposes the already-existing CAP-001 ``admit_document_version`` semantic
owner through this same internal seam for a bounded canonical-mutation path.
Admission is permitted only inside an exact Product Contract-pinned Governed
Execution that is already Ready/Running with every declared gate satisfied and
whose exact material input is the candidate Document Version. This does not add
retrieval, storage, DMS, public API or new capability semantics.

The adapter boundary is not a new semantic owner. Product Contract validation,
dependency/version compatibility, capability admission, access checks, workspace
scope, canonical reads, document admission and reconstruction remain delegated
to their existing semantic owners. The adapter boundary grants no Authentication,
Authorization, Organizational Authority, approval, permission or capability
lifecycle state.

The current Python/module/dataclass shapes are internal/provisional reference
evidence only. They do not establish a Stable/public SDK/API, package, route,
wire/serialization contract, registry, network protocol or deployment topology.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .document_artifact_governance import (
    AdmittedDocumentVersion,
    DocumentVersionCandidate,
    admit_document_version,
)
from .execution import GovernedVersionPin
from .governed_execution import (
    GovernedExecutionContext,
    require_consequential_operation_admission,
)
from .identity import Identity
from .integration_composition import (
    IntegrationCompositionContinuityError,
    IntegrationCompositionFacade,
    compose_integration_facade,
)
from .product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CapabilityConsumptionRequest,
    consume_document,
    consume_knowledge,
    consume_reconstruction,
    consume_search,
    consume_search_source,
)
from .product_contract import ProductContract, ProductContractScopeError
from .product_contract_declaration import validate_product_contract_declaration
from .product_contract_resolution import GovernedDependencyVersionEvidence
from .security import ActorContext
from .workflow import OperationSideEffectClass
from .workspace_shell import (
    ExactVersionNavigationReference,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
)


class IntegrationAdapterError(RuntimeError):
    """Base fail-closed error for the bounded integration adapter seam."""


@dataclass(frozen=True, slots=True)
class IntegrationWorkspaceAdapter:
    """Optional non-authoritative workspace binding anchored to one facade."""

    facade: IntegrationCompositionFacade

    def __post_init__(self) -> None:
        if not isinstance(self.facade, IntegrationCompositionFacade):
            raise TypeError("workspace adapter requires IntegrationCompositionFacade")

    def open(
        self,
        *,
        initial_destination: WorkspaceDestination = WorkspaceDestination.DISCOVER,
    ) -> WorkspaceShellState:
        return self.facade.open_workspace(initial_destination=initial_destination)

    def navigate_subject(
        self,
        state: WorkspaceShellState,
        *,
        destination: WorkspaceDestination,
        subject_id: Identity,
    ) -> WorkspaceShellState:
        self._require_state_continuity(state)
        self._require_identity_scope(subject_id, role="Subject")
        return navigate_workspace(
            state,
            destination=destination,
            reference=SubjectNavigationReference(
                organization=self.facade.context.organization,
                subject_id=subject_id,
            ),
        )

    def navigate_exact_version(
        self,
        state: WorkspaceShellState,
        *,
        destination: WorkspaceDestination,
        subject_id: Identity,
        version_id: Identity,
    ) -> WorkspaceShellState:
        self._require_state_continuity(state)
        self._require_identity_scope(subject_id, role="Subject")
        self._require_identity_scope(version_id, role="Version")
        return navigate_workspace(
            state,
            destination=destination,
            reference=ExactVersionNavigationReference(
                organization=self.facade.context.organization,
                subject_id=subject_id,
                version_id=version_id,
            ),
        )

    def _require_identity_scope(self, identity: Identity, *, role: str) -> None:
        if not isinstance(identity, Identity):
            raise TypeError(f"workspace adapter {role} reference requires Identity")
        if identity.scope != self.facade.context.organization.organization_id.value:
            raise ProductContractScopeError(
                f"workspace adapter {role} Identity is outside the composed Organization scope"
            )

    def _require_state_continuity(self, state: WorkspaceShellState) -> None:
        if not isinstance(state, WorkspaceShellState):
            raise TypeError("workspace adapter navigation requires WorkspaceShellState")
        if state.organization != self.facade.context.organization:
            raise ProductContractScopeError(
                "workspace adapter state and composed integration must share Organization scope"
            )
        if state.actor != self.facade.context.actor:
            raise ProductContractScopeError(
                "workspace adapter state Actor must match the composed integration Actor"
            )
        if (
            state.product_context is None
            or state.product_context.product_id != self.facade.context.product_id
            or state.product_context.product_contract_version_id
            != self.facade.context.product_contract.version_id
        ):
            raise IntegrationCompositionContinuityError(
                "workspace adapter state lost exact Product/Product Contract Version continuity"
            )


@dataclass(frozen=True, slots=True)
class IntegrationCapabilityAdapter:
    """Typed delegation seam for bounded CAP-001..CAP-004 reliance."""

    facade: IntegrationCompositionFacade
    contract: ProductContract

    def __post_init__(self) -> None:
        if not isinstance(self.facade, IntegrationCompositionFacade):
            raise TypeError("capability adapter requires IntegrationCompositionFacade")
        if not isinstance(self.contract, ProductContract):
            raise TypeError("capability adapter requires the RFC-0004 ProductContract semantic owner")
        if self.contract.organization != self.facade.context.organization:
            raise ProductContractScopeError(
                "capability adapter Product Contract and facade must share Organization scope"
            )
        if self.contract.product_id != self.facade.context.product_id:
            raise ProductContractScopeError(
                "capability adapter Product Contract must preserve the composed Product identity"
            )
        if self.contract.product_version != self.facade.context.product_version:
            raise IntegrationCompositionContinuityError(
                "capability adapter Product Contract lost the composed Product version"
            )
        if self.contract.version_pin != self.facade.context.product_contract:
            raise IntegrationCompositionContinuityError(
                "capability adapter requires the exact composed Product Contract Version"
            )

        adapter_declaration = validate_product_contract_declaration(contract=self.contract)
        if adapter_declaration != self.facade.declaration_evidence:
            raise IntegrationCompositionContinuityError(
                "capability adapter Product Contract declaration differs from the exact declaration "
                "validated during facade composition"
            )

    def admit(
        self,
        request: CapabilityConsumptionRequest,
        *,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
    ):
        return self.facade.admit_capability(
            request,
            governed_versions=governed_versions,
        )

    def resolve_document(
        self,
        *,
        request: CapabilityConsumptionRequest,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
        admitted: Any,
        artifact_id: Identity,
    ):
        self.admit(request, governed_versions=governed_versions)
        return consume_document(
            contract=self.contract,
            request=request,
            admitted=admitted,
            artifact_id=artifact_id,
        )

    def admit_document_version(
        self,
        *,
        execution: GovernedExecutionContext,
        candidate: DocumentVersionCandidate,
    ) -> AdmittedDocumentVersion:
        """Admit one exact CAP-001 candidate only inside admitted Governed Execution.

        Provider/version compatibility and Product Contract operation semantics are
        checked when the execution enters through ``facade.start_governed_execution``.
        This side-effect boundary then rechecks exact Product Contract continuity,
        the declared CAP-001 operation, the exact candidate material-input pin and
        RFC-0005 consequential-operation admission before delegating to CAP-001.
        """

        if not isinstance(execution, GovernedExecutionContext):
            raise TypeError("document admission requires GovernedExecutionContext")
        if not isinstance(candidate, DocumentVersionCandidate):
            raise TypeError("document admission requires DocumentVersionCandidate")
        if execution.organization != self.facade.context.organization:
            raise ProductContractScopeError(
                "document admission execution and integration facade must share Organization scope"
            )
        if execution.product_contract != self.facade.context.product_contract:
            raise IntegrationCompositionContinuityError(
                "document admission lost exact Product Contract Version continuity"
            )
        if candidate.canonical_record.organization != self.facade.context.organization:
            raise ProductContractScopeError(
                "document admission candidate must share the composed Organization scope"
            )

        operations = tuple(
            operation
            for operation in self.contract.operations
            if operation.operation_name == execution.operation_name
        )
        if len(operations) != 1:
            raise IntegrationCompositionContinuityError(
                "document admission execution operation is not declared exactly once by Product Contract"
            )
        operation = operations[0]
        if operation.dependency_id != CAP_001_DOCUMENT_ARTIFACT:
            raise IntegrationCompositionContinuityError(
                "document admission execution must use the declared CAP-001 dependency"
            )
        if set(operation.side_effect_classes) != {
            OperationSideEffectClass.CANONICAL_MUTATION
        }:
            raise IntegrationCompositionContinuityError(
                "document admission Product Contract operation must declare only canonical mutation"
            )

        candidate_record = candidate.canonical_record
        exact_input_matches = tuple(
            pin
            for pin in execution.material_inputs
            if pin.subject_id == candidate_record.subject_id
            and pin.version_id == candidate_record.version_id
            and pin.semantic_type == candidate_record.semantic_type
            and pin.authority_scope == candidate_record.authority_scope
        )
        if len(exact_input_matches) != 1:
            raise IntegrationCompositionContinuityError(
                "document admission candidate must be the exact material input pinned by execution"
            )

        require_consequential_operation_admission(
            execution,
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
        )
        return admit_document_version(candidate)

    def retrieve_knowledge(
        self,
        *,
        request: CapabilityConsumptionRequest,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
        knowledge: tuple[Any, ...],
        allow_stale: bool = False,
    ):
        self.admit(request, governed_versions=governed_versions)
        return consume_knowledge(
            contract=self.contract,
            request=request,
            knowledge=knowledge,
            allow_stale=allow_stale,
        )

    def discover_sources(
        self,
        *,
        request: CapabilityConsumptionRequest,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
        projection: Any,
        current_sources: tuple[Any, ...],
        query_text: str,
    ):
        self.admit(request, governed_versions=governed_versions)
        return consume_search(
            contract=self.contract,
            request=request,
            projection=projection,
            current_sources=current_sources,
            query_text=query_text,
        )

    def resolve_search_source(
        self,
        *,
        request: CapabilityConsumptionRequest,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
        hit: Any,
        current_sources: tuple[Any, ...],
    ):
        self.admit(request, governed_versions=governed_versions)
        return consume_search_source(
            contract=self.contract,
            request=request,
            hit=hit,
            current_sources=current_sources,
        )

    def reconstruct_execution(
        self,
        *,
        request: CapabilityConsumptionRequest,
        governed_versions: tuple[GovernedDependencyVersionEvidence, ...] | None,
        manifest: Any,
        evidence_constraints: tuple[tuple[Identity, str, tuple[str, ...], str], ...],
    ):
        self.admit(request, governed_versions=governed_versions)
        return consume_reconstruction(
            contract=self.contract,
            request=request,
            manifest=manifest,
            evidence_constraints=evidence_constraints,
        )


@dataclass(frozen=True, slots=True)
class IntegrationAdapters:
    """Reusable cross-consumer core: exact facade plus capability delegation.

    R15 intentionally does not store a workspace adapter here. The first bounded
    product may opt into workspace presentation through :func:`compose_workspace_adapter`;
    the headless evidence extension therefore carries no eager workspace binding.
    """

    facade: IntegrationCompositionFacade
    capabilities: IntegrationCapabilityAdapter

    def __post_init__(self) -> None:
        if self.capabilities.facade is not self.facade:
            raise IntegrationAdapterError(
                "integration capability adapter must share one exact composed facade"
            )

    @property
    def workspace(self) -> IntegrationWorkspaceAdapter:
        """Compatibility convenience for the current internal reference only.

        Workspace is created lazily and is not part of the shared dataclass state.
        New integration code should opt in explicitly through
        :func:`compose_workspace_adapter` so headless consumers do not accidentally
        treat workspace presentation as a universal integration requirement.
        """

        return compose_workspace_adapter(adapters=self)


def compose_workspace_adapter(*, adapters: IntegrationAdapters) -> IntegrationWorkspaceAdapter:
    """Bind optional workspace presentation to one already composed integration."""

    if not isinstance(adapters, IntegrationAdapters):
        raise TypeError("workspace binding requires IntegrationAdapters")
    return IntegrationWorkspaceAdapter(adapters.facade)


def compose_integration_adapters(
    *,
    contract: ProductContract,
    actor: ActorContext,
    effective_product_contract: GovernedVersionPin,
    governed_versions: tuple[GovernedDependencyVersionEvidence, ...],
) -> IntegrationAdapters:
    """Compose the shared adapter core only through the R14-hardened factory path."""

    facade = compose_integration_facade(
        contract=contract,
        actor=actor,
        effective_product_contract=effective_product_contract,
        governed_versions=governed_versions,
    )
    return IntegrationAdapters(
        facade=facade,
        capabilities=IntegrationCapabilityAdapter(facade, contract),
    )
