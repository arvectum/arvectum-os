"""P7.06-UI2 governed consequential-outcome evidence presentation.

The underlying runtime intentionally keeps an uncertain consequential attempt
separate from any later reconciliation decision.  UI2 must preserve that
separation even when action readiness correctly blocks blind retry and requires
reconciliation before another effect can be attempted.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from html import escape

from .identity import Identity
from .runtime_consistency import ConsequentialOutcome, RuntimeConsistencyState


class ObservedConsequentialState(str, Enum):
    NONE = "No prior consequential attempt"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNCERTAIN = "Uncertain"


@dataclass(frozen=True, slots=True)
class ConsequentialOutcomeEvidence:
    state: ObservedConsequentialState
    execution_subject_id: Identity | None = None
    execution_version_id: Identity | None = None
    retry_token_present: bool = False
    reconciliation_required: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.state, ObservedConsequentialState):
            raise ValueError("observed consequential state must be explicit")
        if not isinstance(self.retry_token_present, bool) or not isinstance(
            self.reconciliation_required, bool
        ):
            raise ValueError("retry/reconciliation flags must be explicit")
        if self.state is ObservedConsequentialState.NONE:
            if self.execution_subject_id is not None or self.execution_version_id is not None:
                raise ValueError("no-attempt state must not manufacture Execution evidence")
            if self.reconciliation_required:
                raise ValueError("no-attempt state cannot require reconciliation")
            return
        if not isinstance(self.execution_subject_id, Identity) or not isinstance(
            self.execution_version_id, Identity
        ):
            raise ValueError("observed attempt must preserve exact Execution identity")
        if self.state is ObservedConsequentialState.UNCERTAIN and not self.reconciliation_required:
            raise ValueError("uncertain consequential outcome must require reconciliation before retry")


def inspect_consequential_outcome_evidence(
    runtime_state: RuntimeConsistencyState,
) -> ConsequentialOutcomeEvidence:
    """Expose the latest observed attempt without turning it into authority."""

    if not isinstance(runtime_state, RuntimeConsistencyState):
        raise ValueError("consequential outcome inspection requires RuntimeConsistencyState")
    if not runtime_state.attempts:
        return ConsequentialOutcomeEvidence(state=ObservedConsequentialState.NONE)

    latest = runtime_state.attempts[-1]
    if latest.outcome is ConsequentialOutcome.UNCERTAIN:
        state = ObservedConsequentialState.UNCERTAIN
        reconciliation_required = True
    elif latest.outcome is ConsequentialOutcome.SUCCEEDED:
        state = ObservedConsequentialState.SUCCEEDED
        reconciliation_required = False
    else:
        state = ObservedConsequentialState.FAILED
        reconciliation_required = False
    return ConsequentialOutcomeEvidence(
        state=state,
        execution_subject_id=latest.execution_subject_id,
        execution_version_id=latest.execution_version_id,
        retry_token_present=latest.retry_token is not None,
        reconciliation_required=reconciliation_required,
    )


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.value} [{identity.scope}]"


def render_consequential_outcome_evidence_html(
    evidence: ConsequentialOutcomeEvidence,
) -> str:
    if not isinstance(evidence, ConsequentialOutcomeEvidence):
        raise ValueError("outcome rendering requires ConsequentialOutcomeEvidence")
    if evidence.state is ObservedConsequentialState.NONE:
        return (
            '<section data-observed-consequential-state="none">'
            "<h3>Observed consequential outcome</h3>"
            "<p>No prior consequential attempt is recorded for this runtime state.</p>"
            "</section>"
        )

    assert evidence.execution_subject_id is not None
    assert evidence.execution_version_id is not None
    reconciliation = (
        "<p><strong>Reconciliation required.</strong> The observed outcome remains "
        "<strong>Uncertain</strong>; UI2 does not rewrite uncertainty as success/failure and "
        "does not permit a blind retry.</p>"
        if evidence.reconciliation_required
        else "<p>No reconciliation requirement is inferred by this presentation.</p>"
    )
    return (
        f'<section data-observed-consequential-state="{escape(evidence.state.value.lower())}">'
        "<h3>Observed consequential outcome</h3>"
        f"<p>Observed governed outcome: <strong>{escape(evidence.state.value)}</strong><br>"
        f"Execution Subject: {escape(_identity_text(evidence.execution_subject_id))}<br>"
        f"Exact Execution Version: {escape(_identity_text(evidence.execution_version_id))}<br>"
        f"Retry token recorded: {'yes' if evidence.retry_token_present else 'no'}</p>"
        f"{reconciliation}"
        "</section>"
    )
