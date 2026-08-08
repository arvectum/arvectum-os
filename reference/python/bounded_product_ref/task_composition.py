"""P4.08 — bounded product task/context composition over shared workspace surfaces.

This product-owned reference adapter proves one Product Contract-backed entry into
the shared Arvectum OS workspace. It composes existing platform presentation and
action boundaries without creating a product orchestrator inside the platform.

The module is intentionally outside ``arvectum_os_ref``. Product-domain task and
decision semantics stay here. Shared platform code owns only domain-neutral
workspace, capability, Product Contract, Governed Execution and operator-safety
semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from arvectum_os_ref.canonical import CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_experience import (
    DocumentWorkspaceResult,
    DocumentWorkspaceSourceSet,
    inspect_document_workspace,
)
from arvectum_os_ref.event_provenance import EventReceipt
from arvectum_os_ref.governed_execution import GovernedExecutionContext
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_search_experience import (
    KnowledgeWorkspaceResult,
    MemoryKnowledgeSearchSources,
    inspect_knowledge_workspace,
)
from arvectum_os_ref.operator_safety import (
    OperatorCanonicalMutationIntent,
    execute_operator_canonical_mutation_action,
    prepare_operator_canonical_mutation_action,
)
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    OP_RESOLVE_DOCUMENT,
    OP_RETRIEVE_KNOWLEDGE,
    CapabilityConsumptionRequest,
    ProductCapabilityAdmission,
    validate_capability_consumption,
)
from arvectum_os_ref.product_contract import (
    ProductContract,
    ProductContractScopeError,
    ProductRuntimeInteraction,
    start_product_governed_execution,
)
from arvectum_os_ref.runtime_consistency import RetrySemantics, RuntimeConsistencyState
from arvectum_os_ref.security import ActorContext, OrganizationScope
from arvectum_os_ref.workspace_shell import (
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceProductContext,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


class ProductCompositionError(ValueError):
    """The bounded product flow cannot safely compose the requested context."""


class ProductTaskDisposition(str, Enum):
    """Example product-owned decision semantics; not a platform lifecycle or authority."""

    NEEDS_REVIEW = "Needs review"
    READY_TO_PROCEED = "Ready to proceed"
    DECLINED = "Declined"


@dataclass(frozen=True, slots=True)
class BoundedProductTask:
    """Product-owned task identity and the governed document context it starts from."""

    organization: OrganizationScope
    product_id: Identity
    product_version: str
    task_id: Identity
    document_subject_id: Identity
    title: str

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("task Organization scope must be explicit")
        for value, label in (
            (self.product_id, "product_id"),
            (self.task_id, "task_id"),
            (self.document_subject_id, "document_subject_id"),
        ):
            if not isinstance(value, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.product_id.scope != self.organization.organization_id.value:
            raise ValueError("product identity must share the task Organization scope")
        if self.task_id.scope != self.organization.organization_id.value:
            raise ValueError("task identity must share the task Organization scope")
        if self.document_subject_id.scope != self.organization.organization_id.value:
            raise ValueError("document identity must share the task Organization scope")
        if not isinstance(self.product_version, str) or not self.product_version.strip():
            raise ValueError("product_version must be explicit")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("task title must be explicit")


@dataclass(frozen=True, slots=True)
class ProductWorkspaceEntry:
    """Exact Product Contract-backed workspace entry; never permission or authority."""

    task: BoundedProductTask
    workspace: WorkspaceShellState
    capability_admissions: tuple[ProductCapabilityAdmission, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.task, BoundedProductTask):
            raise ValueError("entry requires a product-owned task")
        if not isinstance(self.workspace, WorkspaceShellState):
            raise ValueError("entry requires an open shared workspace")
        if (
            not isinstance(self.capability_admissions, tuple)
            or len(self.capability_admissions) < 2
            or any(
                not isinstance(value, ProductCapabilityAdmission)
                for value in self.capability_admissions
            )
        ):
            raise ValueError("entry requires at least two explicit capability admissions")


@dataclass(frozen=True, slots=True)
class ProductTaskContextView:
    """Product-owned composition of two shared, non-authoritative workspace surfaces."""

    task: BoundedProductTask
    document: DocumentWorkspaceResult
    knowledge: KnowledgeWorkspaceResult
    product_contract_version_id: Identity
    capability_dependencies: tuple[Identity, ...]
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("product task context presentation cannot become authoritative")
        if len(set(self.capability_dependencies)) < 2:
            raise ValueError("task context must compose at least two shared capability surfaces")


@dataclass(frozen=True, slots=True)
class ProductTaskDecision:
    """Transient product-domain decision returned to the product boundary."""

    task_id: Identity
    disposition: ProductTaskDisposition
    note: str
    based_on_contract_version_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.task_id, Identity):
            raise ValueError("decision task_id must be an Identity")
        if not isinstance(self.disposition, ProductTaskDisposition):
            raise ValueError("disposition must remain an explicit product-domain value")
        if not isinstance(self.note, str):
            raise ValueError("decision note must be text")
        if not isinstance(self.based_on_contract_version_id, Identity):
            raise ValueError("decision must preserve the exact Product Contract version context")


def _require_task_boundary(
    *,
    contract: ProductContract,
    task: BoundedProductTask,
    actor: ActorContext,
) -> None:
    if not isinstance(contract, ProductContract):
        raise TypeError("product workspace entry requires an explicit ProductContract")
    if not isinstance(task, BoundedProductTask):
        raise TypeError("product workspace entry requires a BoundedProductTask")
    if not isinstance(actor, ActorContext):
        raise TypeError("product workspace entry requires an attributable ActorContext")
    if actor.organization != task.organization:
        raise ProductContractScopeError("actor and product task must share Organization scope")
    if contract.organization != task.organization:
        raise ProductContractScopeError("Product Contract and product task must share Organization scope")
    if contract.product_id != task.product_id or contract.product_version != task.product_version:
        raise ProductContractScopeError("Product Contract does not govern this product task version")


def _request_key(request: CapabilityConsumptionRequest) -> tuple[Identity, str]:
    return request.dependency_id, request.operation_name


def enter_product_task_workspace(
    *,
    contract: ProductContract,
    task: BoundedProductTask,
    actor: ActorContext,
    capability_requests: tuple[CapabilityConsumptionRequest, ...],
) -> ProductWorkspaceEntry:
    """Validate the bounded Product Contract before opening the shared workspace.

    The entry requires at least two distinct declared shared capability surfaces.
    Contract admission is not authorization: every request still carries its
    current Actor/Organization/purpose/right/classification access context.
    """

    _require_task_boundary(contract=contract, task=task, actor=actor)
    if (
        not isinstance(capability_requests, tuple)
        or len(capability_requests) < 2
        or any(
            not isinstance(value, CapabilityConsumptionRequest)
            for value in capability_requests
        )
    ):
        raise ProductCompositionError(
            "product entry requires at least two explicit capability requests"
        )

    admissions: list[ProductCapabilityAdmission] = []
    for request in capability_requests:
        if request.access.actor != actor:
            raise ProductContractScopeError(
                "capability request Actor must match the workspace entry Actor"
            )
        if request.product_id != task.product_id or request.product_version != task.product_version:
            raise ProductContractScopeError(
                "capability request must stay inside the product task boundary"
            )
        admissions.append(
            validate_capability_consumption(contract=contract, request=request)
        )

    if len({admission.dependency_id for admission in admissions}) < 2:
        raise ProductCompositionError(
            "product entry must consume at least two distinct shared capabilities"
        )

    workspace = open_workspace_shell(
        actor,
        product_context=WorkspaceProductContext(
            organization=task.organization,
            product_id=task.product_id,
            product_contract_version_id=contract.record.version_id,
        ),
    )
    if not isinstance(workspace, WorkspaceShellState):
        raise ProductCompositionError("Product Contract-backed workspace entry failed closed")

    return ProductWorkspaceEntry(
        task=task,
        workspace=workspace,
        capability_admissions=tuple(admissions),
    )


def _require_admitted(
    entry: ProductWorkspaceEntry,
    request: CapabilityConsumptionRequest,
    *,
    dependency_id: Identity,
    operation_name: str,
) -> None:
    if (
        request.access.actor != entry.workspace.actor
        or request.organization != entry.workspace.organization
    ):
        raise ProductContractScopeError(
            "composed capability request must match the current workspace context"
        )
    if request.dependency_id != dependency_id or request.operation_name != operation_name:
        raise ProductCompositionError(
            "wrong Product Contract capability operation for this composed surface"
        )
    key = _request_key(request)
    if not any(
        admission.dependency_id == key[0] and admission.operation_name == key[1]
        for admission in entry.capability_admissions
    ):
        raise ProductCompositionError(
            "capability operation was not admitted at the Product Contract entry point"
        )


def compose_product_task_context(
    *,
    entry: ProductWorkspaceEntry,
    document_request: CapabilityConsumptionRequest,
    knowledge_request: CapabilityConsumptionRequest,
    document_sources: DocumentWorkspaceSourceSet,
    document_source_authorizations: tuple[CurrentSourceAuthorization, ...],
    knowledge_sources: MemoryKnowledgeSearchSources,
    knowledge_source_authorizations: tuple[CurrentSourceAuthorization, ...],
) -> ProductTaskContextView:
    """Compose CAP-001 and CAP-002 operator surfaces without owning their semantics."""

    if not isinstance(entry, ProductWorkspaceEntry):
        raise TypeError("task context composition requires ProductWorkspaceEntry")
    _require_admitted(
        entry,
        document_request,
        dependency_id=CAP_001_DOCUMENT_ARTIFACT,
        operation_name=OP_RESOLVE_DOCUMENT,
    )
    _require_admitted(
        entry,
        knowledge_request,
        dependency_id=CAP_002_MEMORY_KNOWLEDGE,
        operation_name=OP_RETRIEVE_KNOWLEDGE,
    )

    document_workspace = navigate_workspace(
        entry.workspace,
        destination=WorkspaceDestination.DOCUMENTS,
        reference=SubjectNavigationReference(
            organization=entry.task.organization,
            subject_id=entry.task.document_subject_id,
        ),
    )
    document_view = inspect_document_workspace(
        workspace=document_workspace,
        sources=document_sources,
        source_authorizations=document_source_authorizations,
        access_request=document_request.access,
    )

    knowledge_workspace = navigate_workspace(
        entry.workspace,
        destination=WorkspaceDestination.KNOWLEDGE,
    )
    knowledge_view = inspect_knowledge_workspace(
        workspace=knowledge_workspace,
        sources=knowledge_sources,
        source_authorizations=knowledge_source_authorizations,
        access_request=knowledge_request.access,
    )

    product_context = entry.workspace.product_context
    if product_context is None or product_context.product_contract_version_id is None:
        raise ProductCompositionError("exact Product Contract version context is missing")

    return ProductTaskContextView(
        task=entry.task,
        document=document_view,
        knowledge=knowledge_view,
        product_contract_version_id=product_context.product_contract_version_id,
        capability_dependencies=(
            document_request.dependency_id,
            knowledge_request.dependency_id,
        ),
    )


def decide_product_task(
    *,
    context: ProductTaskContextView,
    disposition: ProductTaskDisposition,
    note: str = "",
) -> ProductTaskDecision:
    """Return domain behavior to the product; do not mutate canonical platform state."""

    if not isinstance(context, ProductTaskContextView):
        raise TypeError("product decision requires a composed ProductTaskContextView")
    return ProductTaskDecision(
        task_id=context.task.task_id,
        disposition=disposition,
        note=note,
        based_on_contract_version_id=context.product_contract_version_id,
    )


def start_product_task_execution(
    *,
    contract: ProductContract,
    task: BoundedProductTask,
    interaction: ProductRuntimeInteraction,
    actor: ActorContext,
    execution_id: Identity,
    version_id: Identity,
    created_at: datetime,
) -> GovernedExecutionContext:
    """Enter shared Governed Execution only through the exact Product Contract boundary."""

    _require_task_boundary(contract=contract, task=task, actor=actor)
    if (
        interaction.product_id != task.product_id
        or interaction.product_version != task.product_version
    ):
        raise ProductContractScopeError(
            "governed interaction must stay inside the product task boundary"
        )
    return start_product_governed_execution(
        contract=contract,
        interaction=interaction,
        actor=actor,
        execution_id=execution_id,
        version_id=version_id,
        created_at=created_at,
    )


def prepare_product_task_action(
    *,
    entry: ProductWorkspaceEntry,
    inspection: Any,
    execution: GovernedExecutionContext,
    runtime_state: RuntimeConsistencyState,
    candidate: CanonicalRecord,
    event_receipt: EventReceipt,
    retry_semantics: RetrySemantics,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    retry_token: str | None = None,
) -> OperatorCanonicalMutationIntent:
    """Prepare consequential product work only through the R10 operator-safety guard."""

    return prepare_operator_canonical_mutation_action(
        workspace=entry.workspace,
        inspection=inspection,
        execution=execution,
        runtime_state=runtime_state,
        candidate=candidate,
        event_receipt=event_receipt,
        retry_semantics=retry_semantics,
        source_authorizations=source_authorizations,
        retry_token=retry_token,
    )


def execute_product_task_action(
    *,
    entry: ProductWorkspaceEntry,
    intent: OperatorCanonicalMutationIntent,
    runtime_state: RuntimeConsistencyState,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
) -> Any:
    """Recheck current source access in R10 before any existing P4.05 commit path."""

    return execute_operator_canonical_mutation_action(
        workspace=entry.workspace,
        intent=intent,
        runtime_state=runtime_state,
        source_authorizations=source_authorizations,
    )
