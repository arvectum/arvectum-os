"""R10 — bounded Operator Safety guard for cross-capability workspace actions.

This module hardens the internal P4.05 operator-action boundary without becoming
an authorization engine, policy decision point, Organizational Authority source,
public API, frontend contract or second canonical-mutation path.

P4.05 already separates source inspection access from Governed Execution gates.
R10 adds one missing freshness invariant for operator-facing composition:
a prepared action is bound to the exact current source-authorization decision
used by the inspected view, and that same decision must still be the unique
current allow decision immediately before the existing P4.05 action adapter is
invoked. A changed, revoked, missing or ambiguous source-access decision requires
re-inspection; it never upgrades or substitutes for Governed Execution authority.
"""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import CanonicalRecord
from .canonical_inspection import CurrentSourceAuthorization
from .event_provenance import EventReceipt
from .execution_action_experience import (
    ActionCommitStatus,
    CanonicalMutationActionIntent,
    CanonicalMutationActionResult,
    GovernedExecutionInspection,
    execute_canonical_mutation_action,
    prepare_canonical_mutation_action,
)
from .governed_execution import GovernedExecutionContext
from .identity import Identity
from .runtime_consistency import RetrySemantics, RuntimeConsistencyState
from .workspace_shell import PresentationAuthority, WorkspaceShellState


@dataclass(frozen=True, slots=True)
class OperatorCanonicalMutationIntent:
    """Transient P4.05 intent plus the exact inspected source-access decision."""

    action_intent: CanonicalMutationActionIntent
    source_authorization_decision_version_id: Identity
    presentation_authority: PresentationAuthority = PresentationAuthority.NON_AUTHORITATIVE

    def __post_init__(self) -> None:
        if not isinstance(self.action_intent, CanonicalMutationActionIntent):
            raise ValueError("operator action requires the existing P4.05 action intent")
        if not isinstance(self.source_authorization_decision_version_id, Identity):
            raise ValueError("operator action must pin an exact source-authorization decision")
        if self.presentation_authority is not PresentationAuthority.NON_AUTHORITATIVE:
            raise ValueError("operator action presentation cannot become authority")


def _represented_principal_id(workspace: WorkspaceShellState) -> Identity | None:
    represented = workspace.actor.represented_principal
    return None if represented is None else represented.principal_id


def _current_source_authorization(
    *,
    workspace: WorkspaceShellState,
    resource_subject_id: Identity,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
) -> CurrentSourceAuthorization | None:
    """Return one exact current allow decision or fail closed with ``None``."""

    if not isinstance(workspace, WorkspaceShellState):
        raise ValueError("operator safety requires an open WorkspaceShellState")
    if not isinstance(resource_subject_id, Identity):
        raise ValueError("operator safety resource subject must be an Identity")
    if not isinstance(source_authorizations, tuple) or any(
        not isinstance(value, CurrentSourceAuthorization)
        for value in source_authorizations
    ):
        raise ValueError(
            "source_authorizations must contain CurrentSourceAuthorization values"
        )

    matches = tuple(
        decision
        for decision in source_authorizations
        if decision.organization == workspace.organization
        and decision.actor_actual_principal_id
        == workspace.actor.actual_principal.principal_id
        and decision.represented_principal_id == _represented_principal_id(workspace)
        and decision.resource_subject_id == resource_subject_id
    )
    if len(matches) != 1 or matches[0].allowed is not True:
        return None
    return matches[0]


def _same_current_source_access(
    *,
    workspace: WorkspaceShellState,
    resource_subject_id: Identity,
    expected_decision_version_id: Identity,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
) -> bool:
    current = _current_source_authorization(
        workspace=workspace,
        resource_subject_id=resource_subject_id,
        source_authorizations=source_authorizations,
    )
    return (
        current is not None
        and current.decision_version_id == expected_decision_version_id
    )


def prepare_operator_canonical_mutation_action(
    *,
    workspace: WorkspaceShellState,
    inspection: GovernedExecutionInspection,
    execution: GovernedExecutionContext,
    runtime_state: RuntimeConsistencyState,
    candidate: CanonicalRecord,
    event_receipt: EventReceipt,
    retry_semantics: RetrySemantics,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
    retry_token: str | None = None,
) -> OperatorCanonicalMutationIntent:
    """Prepare an action only while the inspected source-access decision is current.

    This check is deliberately additional to, and independent from, Governed
    Execution gates. It grants no permission or Organizational Authority.
    """

    if not isinstance(inspection, GovernedExecutionInspection):
        raise PermissionError(
            "operator action preparation requires an authorized P4.05 inspection"
        )
    if not _same_current_source_access(
        workspace=workspace,
        resource_subject_id=inspection.execution_subject_id,
        expected_decision_version_id=inspection.source_authorization_decision_version_id,
        source_authorizations=source_authorizations,
    ):
        raise PermissionError(
            "current source-access context no longer matches the inspected operator action; "
            "re-inspect before preparing the action"
        )

    action_intent = prepare_canonical_mutation_action(
        workspace=workspace,
        inspection=inspection,
        execution=execution,
        runtime_state=runtime_state,
        candidate=candidate,
        event_receipt=event_receipt,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
    )
    return OperatorCanonicalMutationIntent(
        action_intent=action_intent,
        source_authorization_decision_version_id=(
            inspection.source_authorization_decision_version_id
        ),
    )


def execute_operator_canonical_mutation_action(
    *,
    workspace: WorkspaceShellState,
    intent: OperatorCanonicalMutationIntent,
    runtime_state: RuntimeConsistencyState,
    source_authorizations: tuple[CurrentSourceAuthorization, ...],
) -> CanonicalMutationActionResult:
    """Recheck source-access freshness, then delegate to the existing P4.05 path."""

    if not isinstance(intent, OperatorCanonicalMutationIntent):
        raise ValueError("operator execution requires OperatorCanonicalMutationIntent")

    inner = intent.action_intent
    if (
        workspace.organization != inner.organization
        or workspace.actor != inner.request_actor
        or not _same_current_source_access(
            workspace=workspace,
            resource_subject_id=inner.execution.execution_subject_id,
            expected_decision_version_id=intent.source_authorization_decision_version_id,
            source_authorizations=source_authorizations,
        )
    ):
        return CanonicalMutationActionResult(
            status=ActionCommitStatus.NOT_ADMITTED,
            status_text=(
                "Current operator source-access context no longer matches the prepared "
                "action. Re-inspect before requesting a consequential commit."
            ),
            state=runtime_state,
        )

    return execute_canonical_mutation_action(
        workspace=workspace,
        intent=inner,
        runtime_state=runtime_state,
    )
