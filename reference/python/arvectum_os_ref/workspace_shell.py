"""P4.02 — bounded Organization/identity scoped workspace shell.

This module is a deliberately small, reversible presentation boundary over
existing Arvectum OS identity and Organization semantics. It is internal
reference-implementation evidence only: not a public SDK/API, route schema,
frontend framework contract, IAM/session implementation, authorization engine,
Product Contract wire format or durable read-model topology.

The shell is non-authoritative. It preserves explicit Organization and Actor
context across domain-neutral navigation, distinguishes Subject references from
exact Version references, fails closed when Organization scope is unresolved or
inconsistent, and exposes no direct canonical mutation path.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from html import escape

from .identity import Identity
from .security import ActorContext, OrganizationScope


class WorkspaceDestination(str, Enum):
    """Domain-neutral P4.01 information-architecture destinations."""

    DISCOVER = "Discover"
    RECORDS = "Records"
    EXECUTIONS = "Executions"
    EVIDENCE = "Evidence"
    DOCUMENTS = "Documents"
    KNOWLEDGE = "Knowledge"


WORKSPACE_DESTINATIONS: tuple[WorkspaceDestination, ...] = tuple(WorkspaceDestination)


class PresentationAuthority(str, Enum):
    """Authority classification for disposable workspace presentation state."""

    NON_AUTHORITATIVE = "Non-authoritative presentation"


class WorkspaceBlockCode(str, Enum):
    """Safe shell-level blocked states that reveal no protected object metadata."""

    ORGANIZATION_UNRESOLVED = "organization-unresolved"
    CONTEXT_SCOPE_MISMATCH = "context-scope-mismatch"


class WorkspaceScopeViolation(PermissionError):
    """Navigation attempted to cross the shell's explicit Organization scope."""


@dataclass(frozen=True, slots=True)
class SubjectNavigationReference:
    """Navigation to one logical governed Subject without pretending it is exact."""

    organization: OrganizationScope
    subject_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("navigation Organization scope must be explicit")
        if not isinstance(self.subject_id, Identity):
            raise ValueError("subject_id must be an Identity")


@dataclass(frozen=True, slots=True)
class ExactVersionNavigationReference:
    """Navigation to one exact immutable governed Version Identity."""

    organization: OrganizationScope
    subject_id: Identity
    version_id: Identity

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("navigation Organization scope must be explicit")
        if not isinstance(self.subject_id, Identity):
            raise ValueError("subject_id must be an Identity")
        if not isinstance(self.version_id, Identity):
            raise ValueError("version_id must be an exact Identity")


WorkspaceNavigationReference = SubjectNavigationReference | ExactVersionNavigationReference


@dataclass(frozen=True, slots=True)
class WorkspaceProductContext:
    """Optional future product-entry context carried as context only.

    Presence of this internal presentation context grants no permission,
    authorization, Organizational Authority or Product Contract validity. P4.08
    remains responsible for a real Product Contract-backed entry point.
    """

    organization: OrganizationScope
    product_id: Identity
    product_contract_version_id: Identity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("product entry Organization scope must be explicit")
        if not isinstance(self.product_id, Identity):
            raise ValueError("product_id must be an Identity")
        if self.product_contract_version_id is not None and not isinstance(
            self.product_contract_version_id, Identity
        ):
            raise ValueError("product_contract_version_id must be an Identity when supplied")


@dataclass(frozen=True, slots=True)
class WorkspaceBlockedState:
    """Fail-closed shell state with no governed content or enabled navigation."""

    code: WorkspaceBlockCode
    status_text: str
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    governed_content_visible: bool = False
    navigation_enabled: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.code, WorkspaceBlockCode):
            raise ValueError("blocked workspace state requires an explicit code")
        if not isinstance(self.status_text, str) or not self.status_text.strip():
            raise ValueError("blocked workspace state requires textual meaning")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("workspace presentation state cannot become authoritative")
        if self.governed_content_visible or self.navigation_enabled:
            raise ValueError("blocked workspace state must fail closed")


@dataclass(frozen=True, slots=True)
class WorkspaceShellState:
    """Immutable, disposable shell presentation state for one Organization."""

    organization: OrganizationScope
    actor: ActorContext
    active_destination: WorkspaceDestination = WorkspaceDestination.DISCOVER
    current_reference: WorkspaceNavigationReference | None = None
    product_context: WorkspaceProductContext | None = None
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE
    destinations: tuple[WorkspaceDestination, ...] = WORKSPACE_DESTINATIONS

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("workspace Organization scope must be explicit")
        if not isinstance(self.actor, ActorContext):
            raise ValueError("workspace Actor context must be explicit and attributable")
        if self.actor.organization != self.organization:
            raise ValueError("Actor and workspace Organization scope must match")
        if not isinstance(self.active_destination, WorkspaceDestination):
            raise ValueError("active_destination must be domain-neutral workspace navigation")
        if self.destinations != WORKSPACE_DESTINATIONS:
            raise ValueError("P4.02 shell destinations are fixed to the P4.01 IA boundary")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("workspace presentation state cannot become authoritative")
        if self.current_reference is not None:
            _require_same_organization(self.organization, self.current_reference.organization)
        if self.product_context is not None:
            _require_same_organization(self.organization, self.product_context.organization)


WorkspaceOpenResult = WorkspaceShellState | WorkspaceBlockedState


def _require_same_organization(
    workspace_organization: OrganizationScope,
    candidate_organization: OrganizationScope,
) -> None:
    if candidate_organization != workspace_organization:
        # Intentionally omit target identifiers from the error surface. A scope
        # failure must not become an existence/metadata disclosure channel.
        raise WorkspaceScopeViolation("workspace navigation is outside the current Organization scope")


def open_workspace_shell(
    actor: ActorContext | None,
    *,
    product_context: WorkspaceProductContext | None = None,
    initial_destination: WorkspaceDestination = WorkspaceDestination.DISCOVER,
) -> WorkspaceOpenResult:
    """Open one scoped shell or return a fail-closed non-content state.

    ActorContext already requires explicit Organization scope. Accepting ``None``
    here models failed/unavailable context resolution without inventing a default
    Organization. Product entry context is validated only for scope coherence;
    it is never treated as permission or authority.
    """

    if not isinstance(actor, ActorContext):
        return WorkspaceBlockedState(
            code=WorkspaceBlockCode.ORGANIZATION_UNRESOLVED,
            status_text=(
                "Organization scope is unresolved. Governed content and navigation are unavailable."
            ),
        )

    if not isinstance(initial_destination, WorkspaceDestination):
        raise ValueError("initial_destination must be a WorkspaceDestination")

    if product_context is not None:
        if not isinstance(product_context, WorkspaceProductContext):
            raise ValueError("product_context must be WorkspaceProductContext when supplied")
        if product_context.organization != actor.organization:
            return WorkspaceBlockedState(
                code=WorkspaceBlockCode.CONTEXT_SCOPE_MISMATCH,
                status_text=(
                    "Workspace entry context is inconsistent with the current Organization. "
                    "Governed content and navigation are unavailable."
                ),
            )

    return WorkspaceShellState(
        organization=actor.organization,
        actor=actor,
        active_destination=initial_destination,
        product_context=product_context,
    )


def navigate_workspace(
    state: WorkspaceShellState,
    *,
    destination: WorkspaceDestination,
    reference: WorkspaceNavigationReference | None = None,
) -> WorkspaceShellState:
    """Return the next immutable shell state while preserving scope/attribution.

    This operation changes presentation/navigation state only. It neither resolves
    a Subject to a current Version nor performs authorization, approval, Product
    Contract validation, canonical mutation or any other consequential action.
    """

    if not isinstance(state, WorkspaceShellState):
        raise ValueError("navigation requires an open WorkspaceShellState")
    if not isinstance(destination, WorkspaceDestination):
        raise ValueError("destination must be a WorkspaceDestination")
    if reference is not None:
        if not isinstance(
            reference, (SubjectNavigationReference, ExactVersionNavigationReference)
        ):
            raise ValueError("reference must use an explicit workspace navigation reference type")
        _require_same_organization(state.organization, reference.organization)

    return replace(
        state,
        active_destination=destination,
        current_reference=reference,
    )


def render_workspace_shell_html(state: WorkspaceOpenResult) -> str:
    """Render a minimal inert HTML adapter without establishing route/API semantics."""

    if isinstance(state, WorkspaceBlockedState):
        return (
            '<main data-workspace-state="blocked">'
            '<h1>Workspace unavailable</h1>'
            f'<p role="alert">{escape(state.status_text)}</p>'
            '<p>Presentation state only; no governed content is exposed.</p>'
            '</main>'
        )

    if not isinstance(state, WorkspaceShellState):
        raise ValueError("state must be WorkspaceShellState or WorkspaceBlockedState")

    actor_id = escape(state.actor.actual_principal.principal_id.value)
    organization_id = escape(state.organization.organization_id.value)
    represented = ""
    if state.actor.represented_principal is not None:
        represented_id = escape(state.actor.represented_principal.principal_id.value)
        represented = f'<span data-context="represented-principal">Acting for: {represented_id}</span>'

    nav_items: list[str] = []
    for destination in state.destinations:
        current = ' aria-current="page"' if destination is state.active_destination else ""
        nav_items.append(
            f'<button type="button" data-workspace-destination="{destination.name.lower()}"{current}>'
            f'{escape(destination.value)}</button>'
        )

    reference_html = '<p data-reference-kind="none">Current reference: none</p>'
    if isinstance(state.current_reference, SubjectNavigationReference):
        reference_html = (
            '<p data-reference-kind="subject">Current reference: Subject '
            f'{escape(state.current_reference.subject_id.value)}</p>'
        )
    elif isinstance(state.current_reference, ExactVersionNavigationReference):
        reference_html = (
            '<p data-reference-kind="exact-version">Current reference: Exact version '
            f'{escape(state.current_reference.version_id.value)} '
            f'(Subject {escape(state.current_reference.subject_id.value)})</p>'
        )

    product_html = ""
    if state.product_context is not None:
        product_id = escape(state.product_context.product_id.value)
        contract = ""
        if state.product_context.product_contract_version_id is not None:
            contract = (
                " / Product Contract version "
                + escape(state.product_context.product_contract_version_id.value)
            )
        product_html = (
            '<p data-context="product-entry">Entry context: Product '
            f'{product_id}{contract}. Context only; does not grant access or authority.</p>'
        )

    return (
        '<main data-workspace-state="open" data-presentation-authority="non-authoritative">'
        '<header>'
        '<h1>Arvectum OS Workspace</h1>'
        '<div aria-label="Current governed context">'
        f'<span data-context="organization">Organization: {organization_id}</span>'
        f'<span data-context="actual-principal">Actor: {actor_id}</span>'
        f'{represented}'
        '</div>'
        f'{product_html}'
        '</header>'
        '<nav aria-label="Workspace">'
        + "".join(nav_items)
        + '</nav>'
        + reference_html
        + '<p data-authority-note="true">Presentation state only; it is not authorization, '
        'Organizational Authority, approval, or canonical organizational state.</p>'
        '</main>'
    )
