"""P4.09 — bounded security/rights/minimization/authority-safe UX helpers.

This module consumes already-produced authorization evidence. It is not an IAM,
PDP, policy engine, Organizational Authority source, Product Contract, public API
or canonical-state owner. It does not decide permissions or Organizational Authority.

Its purpose is deliberately narrow: make the presentation boundary fail closed
and prevent operator UX from turning visibility, labels, previews or stale client
state into permission or authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .canonical_inspection import CurrentSourceAuthorization
from .identity import Identity
from .workspace_shell import PresentationAuthority, WorkspaceShellState


class AuthoritySafeUxState(str, Enum):
    AVAILABLE = "Available"
    REINSPECTION_REQUIRED = "Re-inspection required"
    NOT_AVAILABLE = "Not available"


class AuthoritySafeActionLabel(str, Enum):
    """Labels that describe operator intent without claiming approval/authority."""

    REQUEST_ACTION = "Request governed action"
    REINSPECT = "Re-inspect current access"
    UNAVAILABLE = "Action unavailable"


@dataclass(frozen=True, slots=True)
class AuthoritySafeUxDecision:
    state: AuthoritySafeUxState
    action_label: AuthoritySafeActionLabel
    source_authorization_decision_version_id: Identity | None
    governed_content_visible: bool
    protected_count_visible: bool = False
    derived_preview_visible: bool = False
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("workspace presentation cannot become organizational authority")
        if self.state is not AuthoritySafeUxState.AVAILABLE and (
            self.governed_content_visible
            or self.protected_count_visible
            or self.derived_preview_visible
        ):
            raise ValueError("blocked authority-safe UX state cannot leak protected content")
        if self.derived_preview_visible and not self.governed_content_visible:
            raise ValueError("a derived preview cannot outlive source-content visibility")
        if self.protected_count_visible:
            raise ValueError("protected counts are not exposed by this bounded UX helper")


def _represented_principal_id(workspace: WorkspaceShellState) -> Identity | None:
    represented = workspace.actor.represented_principal
    return None if represented is None else represented.principal_id


def consume_current_source_authorization(
    *,
    workspace: WorkspaceShellState,
    resource_subject_id: Identity,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    expected_decision_version_id: Identity | None = None,
    allow_derived_preview: bool = False,
) -> AuthoritySafeUxDecision:
    """Consume one current allow decision and return minimized presentation state.

    Matching is exact on Organization, actual Principal, represented Principal and
    protected Subject. Missing, denied or ambiguous evidence fails closed. When an
    exact prior decision version is supplied, replacement/revocation requires
    re-inspection rather than silently continuing from stale client state.

    The helper intentionally does not evaluate purpose/right/classification policy;
    capability owners must continue to perform those checks independently before
    passing any content to presentation.
    """

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("authority-safe UX requires an open WorkspaceShellState")
    if not isinstance(resource_subject_id, Identity):
        raise ValueError("resource_subject_id must be an Identity")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization) for value in source_authorizations
    ):
        raise ValueError("source_authorizations must contain CurrentSourceAuthorization values")
    if expected_decision_version_id is not None and not isinstance(
        expected_decision_version_id, Identity
    ):
        raise ValueError("expected_decision_version_id must be an Identity when supplied")

    matches = tuple(
        decision
        for decision in source_authorizations
        if decision.organization == workspace.organization
        and decision.actor_actual_principal_id == workspace.actor.actual_principal.principal_id
        and decision.represented_principal_id == _represented_principal_id(workspace)
        and decision.resource_subject_id == resource_subject_id
    )

    if len(matches) != 1 or matches[0].allowed is not True:
        return AuthoritySafeUxDecision(
            state=AuthoritySafeUxState.NOT_AVAILABLE,
            action_label=AuthoritySafeActionLabel.UNAVAILABLE,
            source_authorization_decision_version_id=None,
            governed_content_visible=False,
        )

    current = matches[0]
    if (
        expected_decision_version_id is not None
        and current.decision_version_id != expected_decision_version_id
    ):
        return AuthoritySafeUxDecision(
            state=AuthoritySafeUxState.REINSPECTION_REQUIRED,
            action_label=AuthoritySafeActionLabel.REINSPECT,
            source_authorization_decision_version_id=current.decision_version_id,
            governed_content_visible=False,
        )

    return AuthoritySafeUxDecision(
        state=AuthoritySafeUxState.AVAILABLE,
        action_label=AuthoritySafeActionLabel.REQUEST_ACTION,
        source_authorization_decision_version_id=current.decision_version_id,
        governed_content_visible=True,
        derived_preview_visible=bool(allow_derived_preview),
    )
