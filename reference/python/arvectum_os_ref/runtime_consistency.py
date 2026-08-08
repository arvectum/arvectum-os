"""P2.06 — reusable runtime consistency, idempotency and conflict semantics.

This module defines bounded, domain-neutral logical consistency rules over the
existing P2.02/P2.04/P2.05 in-memory runtime evidence.  It deliberately does
not select a database, transaction manager, lock, queue, outbox/inbox pattern,
distributed coordinator, durable idempotency store or public API/SDK.

The bounded contract exercises Accepted RFC-0002/RFC-0005/RFC-0006 semantics:

* a consequential canonical mutation declares the exact Canonical Head it was
  prepared against and refuses stale-head/current-version overwrite;
* the admitted Governed Execution must have pinned that exact target version;
* retry semantics are declared as natural, keyed or non-idempotent-with-
  duplicate-protection/reconciliation;
* a previously committed exact invocation is returned as a duplicate rather
  than repeating canonical/Event effects;
* reuse of one retry token for materially different immutable invocation
  content is an explicit conflict;
* uncertain external outcomes block blind retry and remain explicitly
  reconciliation-required;
* failed and uncertain attempts never claim success;
* the local canonical mutation boundary is logically all-or-nothing because a
  new immutable snapshot is published only after head, execution, candidate and
  Event admission validation all succeed.

That logical atomicity boundary is intentionally narrower than durable or
cross-system atomicity.  External effects, storage commits, locks, transport
acknowledgements and distributed delivery remain outside this module and would
require a subordinate ADR before a concrete mechanism is materially relied on.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .canonical import CanonicalRecord
from .canonical_lineage import CanonicalLineage
from .event_provenance import CanonicalEvent, EventReceipt, admit_event
from .governed_execution import (
    GovernedExecutionContext,
    require_consequential_operation_admission,
)
from .identity import Identity
from .workflow import OperationSideEffectClass


LOGICAL_ATOMICITY_INCLUDED: Final[tuple[str, ...]] = (
    "expected Canonical Head validation",
    "exact governed execution target-version validation",
    "successor Canonical Record lineage validation",
    "required canonical Event admission validation",
    "publication of one immutable next runtime snapshot",
)

LOGICAL_ATOMICITY_EXCLUDED: Final[tuple[str, ...]] = (
    "durable storage transaction",
    "database locking or compare-and-swap implementation",
    "external-system mutation",
    "message transport acknowledgement or delivery",
    "outbox/inbox persistence",
    "distributed coordination",
)


class RetrySemantics(str, Enum):
    """RFC-0005 retry/idempotency classifications used by the bounded runtime."""

    NATURALLY_IDEMPOTENT = "NaturallyIdempotent"
    KEYED_IDEMPOTENT = "KeyedIdempotent"
    NON_IDEMPOTENT = "NonIdempotent"


class ConsequentialOutcome(str, Enum):
    """Observed semantic outcome of one bounded consequential invocation attempt."""

    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    UNCERTAIN = "Uncertain"


class RuntimeConsistencyError(RuntimeError):
    """Base error for bounded P2.06 consistency/runtime-contract violations."""


class StaleCanonicalHeadError(RuntimeConsistencyError):
    """The invocation was prepared against a Canonical Head that is no longer current."""


class StaleExecutionInputError(RuntimeConsistencyError):
    """The execution did not pin the exact target version required by the mutation."""


class CanonicalSuccessorConflictError(RuntimeConsistencyError):
    """The proposed canonical successor cannot extend the current lineage exactly."""


class IdempotencyKeyConflictError(RuntimeConsistencyError):
    """One retry token was reused for materially different immutable invocation content."""


class DuplicateEventCommitConflictError(RuntimeConsistencyError):
    """A prior Event occurrence cannot be reused to evidence a distinct new commit."""


class ReconciliationRequiredError(RuntimeConsistencyError):
    """An earlier consequential attempt has uncertain outcome and blocks blind retry."""


@dataclass(frozen=True, slots=True)
class ConsequentialAttempt:
    """Immutable semantic evidence for one bounded invocation attempt.

    ``retry_token`` is not a transport delivery id.  For keyed and non-idempotent
    operations it correlates retries/duplicate protection for one semantic
    invocation family.  Naturally idempotent operations may omit it and are
    matched by their exact immutable invocation fingerprint instead.
    """

    execution_subject_id: Identity
    execution_version_id: Identity
    operation_name: str
    side_effect_class: OperationSideEffectClass
    retry_semantics: RetrySemantics
    retry_token: str | None
    fingerprint: tuple[str, ...]
    outcome: ConsequentialOutcome
    result_version_id: Identity | None = None
    event_version_id: Identity | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.execution_subject_id, Identity) or not isinstance(
            self.execution_version_id, Identity
        ):
            raise ValueError("consequential attempt must preserve exact Execution identities")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ValueError("consequential attempt operation_name must be explicit")
        if not isinstance(self.side_effect_class, OperationSideEffectClass):
            raise ValueError("consequential attempt side-effect class must be explicit")
        if not isinstance(self.retry_semantics, RetrySemantics):
            raise ValueError("retry semantics must be explicit")
        _validate_retry_token(self.retry_semantics, self.retry_token)
        if not isinstance(self.fingerprint, tuple) or not self.fingerprint or any(
            not isinstance(item, str) or not item for item in self.fingerprint
        ):
            raise ValueError("attempt fingerprint must be an immutable non-empty string tuple")
        if not isinstance(self.outcome, ConsequentialOutcome):
            raise ValueError("attempt outcome must be explicit")
        if self.result_version_id is not None and not isinstance(self.result_version_id, Identity):
            raise ValueError("result_version_id must be an Identity when supplied")
        if self.event_version_id is not None and not isinstance(self.event_version_id, Identity):
            raise ValueError("event_version_id must be an Identity when supplied")
        if self.outcome is not ConsequentialOutcome.SUCCEEDED and (
            self.result_version_id is not None or self.event_version_id is not None
        ):
            raise ValueError("failed/uncertain attempts must not claim committed result/Event versions")


@dataclass(frozen=True, slots=True)
class RuntimeConsistencyState:
    """Immutable bounded state for one canonical target lineage plus retry evidence.

    This state is a semantic reference snapshot, not a durable transaction/store.
    ``canonical_records`` intentionally represents one subject/authority lineage
    so Canonical Head conflict semantics are explicit and executable.
    """

    canonical_records: tuple[CanonicalRecord, ...]
    admitted_events: tuple[CanonicalEvent, ...] = ()
    attempts: tuple[ConsequentialAttempt, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.canonical_records, tuple) or not self.canonical_records:
            raise ValueError("runtime consistency state requires one canonical target lineage")
        if any(not isinstance(item, CanonicalRecord) for item in self.canonical_records):
            raise ValueError("canonical_records must contain CanonicalRecord versions")
        CanonicalLineage(self.canonical_records)
        if not isinstance(self.admitted_events, tuple) or any(
            not isinstance(item, CanonicalEvent) for item in self.admitted_events
        ):
            raise ValueError("admitted_events must be an immutable CanonicalEvent tuple")
        if not isinstance(self.attempts, tuple) or any(
            not isinstance(item, ConsequentialAttempt) for item in self.attempts
        ):
            raise ValueError("attempts must be an immutable ConsequentialAttempt tuple")

    @property
    def head(self) -> CanonicalRecord:
        return CanonicalLineage(self.canonical_records).head


@dataclass(frozen=True, slots=True)
class CanonicalCommitResult:
    """Outcome of one bounded canonical mutation invocation."""

    state: RuntimeConsistencyState
    record: CanonicalRecord
    event: CanonicalEvent
    duplicate: bool
    outcome: ConsequentialOutcome = ConsequentialOutcome.SUCCEEDED

    def __post_init__(self) -> None:
        if not isinstance(self.state, RuntimeConsistencyState):
            raise ValueError("canonical commit result must expose RuntimeConsistencyState")
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("canonical commit result must expose a CanonicalRecord")
        if not isinstance(self.event, CanonicalEvent):
            raise ValueError("canonical commit result must expose a CanonicalEvent")
        if not isinstance(self.duplicate, bool):
            raise ValueError("duplicate flag must be explicit")
        if self.outcome is not ConsequentialOutcome.SUCCEEDED:
            raise ValueError("canonical commit result can only represent a succeeded logical commit")


@dataclass(frozen=True, slots=True)
class ExternalAttemptResult:
    """Explicit bounded outcome for an external consequential invocation attempt."""

    state: RuntimeConsistencyState
    attempt: ConsequentialAttempt
    duplicate: bool

    @property
    def succeeded(self) -> bool:
        return self.attempt.outcome is ConsequentialOutcome.SUCCEEDED

    @property
    def reconciliation_required(self) -> bool:
        return self.attempt.outcome is ConsequentialOutcome.UNCERTAIN


def _identity_text(identity: Identity) -> str:
    return f"{identity.namespace}:{identity.scope}:{identity.value}"


def _validate_retry_token(semantics: RetrySemantics, retry_token: str | None) -> None:
    if not isinstance(semantics, RetrySemantics):
        raise ValueError("retry semantics must be explicit")
    if semantics in {RetrySemantics.KEYED_IDEMPOTENT, RetrySemantics.NON_IDEMPOTENT}:
        if not isinstance(retry_token, str) or not retry_token.strip():
            raise ValueError(
                "keyed/non-idempotent consequential retry requires an explicit duplicate-protection token"
            )
    elif retry_token is not None:
        raise ValueError("naturally idempotent invocation does not use a retry token in this bounded model")


def _canonical_fingerprint(
    *,
    execution: GovernedExecutionContext,
    side_effect_class: OperationSideEffectClass,
    expected_head_version_id: Identity,
    candidate: CanonicalRecord,
    event_receipt: EventReceipt,
) -> tuple[str, ...]:
    return (
        _identity_text(execution.execution_subject_id),
        _identity_text(execution.execution_version_id),
        execution.operation_name,
        side_effect_class.value,
        _identity_text(expected_head_version_id),
        repr(candidate),
        repr(event_receipt),
    )


def _external_fingerprint(
    *,
    execution: GovernedExecutionContext,
    side_effect_class: OperationSideEffectClass,
    effect_descriptor: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    return (
        _identity_text(execution.execution_subject_id),
        _identity_text(execution.execution_version_id),
        execution.operation_name,
        side_effect_class.value,
        repr(effect_descriptor),
    )


def _matching_attempts(
    state: RuntimeConsistencyState,
    *,
    retry_semantics: RetrySemantics,
    retry_token: str | None,
    fingerprint: tuple[str, ...],
) -> tuple[ConsequentialAttempt, ...]:
    if retry_semantics is RetrySemantics.NATURALLY_IDEMPOTENT:
        return tuple(
            item
            for item in state.attempts
            if item.retry_semantics is RetrySemantics.NATURALLY_IDEMPOTENT
            and item.fingerprint == fingerprint
        )

    same_token = tuple(item for item in state.attempts if item.retry_token == retry_token)
    if any(item.fingerprint != fingerprint for item in same_token):
        raise IdempotencyKeyConflictError(
            "retry token was already bound to materially different immutable invocation content"
        )
    return same_token


def _committed_duplicate(
    state: RuntimeConsistencyState,
    attempts: tuple[ConsequentialAttempt, ...],
) -> CanonicalCommitResult | None:
    committed = tuple(item for item in attempts if item.outcome is ConsequentialOutcome.SUCCEEDED)
    if not committed:
        return None
    attempt = committed[-1]
    if attempt.result_version_id is None or attempt.event_version_id is None:
        raise RuntimeConsistencyError("committed canonical attempt is missing exact result/Event versions")
    record = next(
        (item for item in state.canonical_records if item.version_id == attempt.result_version_id),
        None,
    )
    event = next(
        (item for item in state.admitted_events if item.version_id == attempt.event_version_id),
        None,
    )
    if record is None or event is None:
        raise RuntimeConsistencyError("committed idempotency evidence is inconsistent with runtime state")
    return CanonicalCommitResult(
        state=state,
        record=record,
        event=event,
        duplicate=True,
    )


def _require_exact_execution_target_pin(
    execution: GovernedExecutionContext,
    *,
    target_subject_id: Identity,
    expected_head_version_id: Identity,
) -> None:
    matching = tuple(
        pin for pin in execution.material_inputs if pin.subject_id == target_subject_id
    )
    if len(matching) != 1 or matching[0].version_id != expected_head_version_id:
        raise StaleExecutionInputError(
            "consequential mutation execution must pin the exact target version it was prepared against"
        )


def _validate_successor_candidate(
    current: CanonicalRecord,
    *,
    expected_head_version_id: Identity,
    candidate: CanonicalRecord,
) -> None:
    if candidate.subject_id != current.subject_id:
        raise CanonicalSuccessorConflictError("canonical successor must preserve target Subject Identity")
    if candidate.organization != current.organization:
        raise CanonicalSuccessorConflictError("canonical successor must preserve Organization scope")
    if candidate.authority_mode != current.authority_mode or candidate.authority_scope != current.authority_scope:
        raise CanonicalSuccessorConflictError("canonical successor must preserve the exercised authority scope")
    if candidate.semantic_type != current.semantic_type:
        raise CanonicalSuccessorConflictError("canonical successor must preserve semantic record type")
    if candidate.version_id == current.version_id:
        raise CanonicalSuccessorConflictError("canonical successor requires a new immutable Version Identity")
    if candidate.predecessor_version_id != expected_head_version_id:
        raise CanonicalSuccessorConflictError(
            "canonical successor must explicitly identify the expected current head as predecessor"
        )


def commit_canonical_mutation(
    *,
    state: RuntimeConsistencyState,
    execution: GovernedExecutionContext,
    expected_head_version_id: Identity,
    candidate: CanonicalRecord,
    event_receipt: EventReceipt,
    retry_semantics: RetrySemantics,
    retry_token: str | None = None,
) -> CanonicalCommitResult:
    """Apply one bounded logical canonical commit without silent lost update.

    The function is pure over immutable input state.  It first resolves duplicate
    invocation evidence, then validates admitted execution, exact expected head,
    exact execution target-version pinning, successor lineage and Event admission.
    Only after all checks succeed is one new ``RuntimeConsistencyState`` returned.

    This gives the reference model an executable logical all-or-nothing boundary
    for the local canonical version + required Event pair.  It is not a claim of
    durable ACID, exactly-once delivery or cross-system atomicity.
    """

    if not isinstance(state, RuntimeConsistencyState):
        raise ValueError("state must be a RuntimeConsistencyState")
    if not isinstance(execution, GovernedExecutionContext):
        raise ValueError("execution must be a GovernedExecutionContext")
    if not isinstance(expected_head_version_id, Identity):
        raise ValueError("expected Canonical Head Version Identity must be explicit")
    if not isinstance(candidate, CanonicalRecord):
        raise ValueError("candidate must be an immutable CanonicalRecord version")
    if not isinstance(event_receipt, EventReceipt):
        raise ValueError("canonical commit requires one explicit EventReceipt")
    _validate_retry_token(retry_semantics, retry_token)

    side_effect = OperationSideEffectClass.CANONICAL_MUTATION
    require_consequential_operation_admission(execution, side_effect_class=side_effect)
    fingerprint = _canonical_fingerprint(
        execution=execution,
        side_effect_class=side_effect,
        expected_head_version_id=expected_head_version_id,
        candidate=candidate,
        event_receipt=event_receipt,
    )
    attempts = _matching_attempts(
        state,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
        fingerprint=fingerprint,
    )
    duplicate = _committed_duplicate(state, attempts)
    if duplicate is not None:
        return duplicate
    if any(item.outcome is ConsequentialOutcome.UNCERTAIN for item in attempts):
        raise ReconciliationRequiredError(
            "uncertain prior canonical invocation requires reconciliation before retry"
        )

    current = state.head

    # Natural idempotency may recognize an already-published exact successor even
    # though its original expected predecessor is no longer the current head.
    if retry_semantics is RetrySemantics.NATURALLY_IDEMPOTENT and current.version_id == candidate.version_id:
        existing = next(
            (item for item in state.canonical_records if item.version_id == candidate.version_id),
            None,
        )
        if existing == candidate:
            event_result = admit_event(
                receipt=event_receipt,
                execution=execution,
                related_records=(candidate,),
                admitted_events=state.admitted_events,
            )
            if event_result.duplicate_delivery:
                return CanonicalCommitResult(
                    state=state,
                    record=existing,
                    event=event_result.event,
                    duplicate=True,
                )

    if current.version_id != expected_head_version_id:
        raise StaleCanonicalHeadError(
            "expected Canonical Head no longer matches the latest admitted canonical version"
        )
    _require_exact_execution_target_pin(
        execution,
        target_subject_id=current.subject_id,
        expected_head_version_id=expected_head_version_id,
    )
    _validate_successor_candidate(
        current,
        expected_head_version_id=expected_head_version_id,
        candidate=candidate,
    )

    candidate_history = (*state.canonical_records, candidate)
    CanonicalLineage(candidate_history)
    event_result = admit_event(
        receipt=event_receipt,
        execution=execution,
        related_records=(candidate,),
        admitted_events=state.admitted_events,
    )
    if event_result.duplicate_delivery:
        raise DuplicateEventCommitConflictError(
            "an already-admitted Event occurrence cannot evidence a distinct new canonical commit"
        )

    attempt = ConsequentialAttempt(
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        operation_name=execution.operation_name,
        side_effect_class=side_effect,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
        fingerprint=fingerprint,
        outcome=ConsequentialOutcome.SUCCEEDED,
        result_version_id=candidate.version_id,
        event_version_id=event_result.event.version_id,
    )
    next_state = RuntimeConsistencyState(
        canonical_records=candidate_history,
        admitted_events=event_result.admitted_events,
        attempts=(*state.attempts, attempt),
    )
    return CanonicalCommitResult(
        state=next_state,
        record=candidate,
        event=event_result.event,
        duplicate=False,
    )


def record_external_consequence_attempt(
    *,
    state: RuntimeConsistencyState,
    execution: GovernedExecutionContext,
    side_effect_class: OperationSideEffectClass,
    effect_descriptor: tuple[tuple[str, str], ...],
    retry_semantics: RetrySemantics,
    reported_outcome: ConsequentialOutcome,
    retry_token: str | None = None,
) -> ExternalAttemptResult:
    """Record explicit retry/uncertainty semantics around one external consequence.

    This function does not perform the external effect.  It models the semantic
    boundary that an adapter/orchestrator must honor: committed exact retries are
    duplicates, uncertain outcomes block blind retry, failures remain failures,
    and one retry token cannot be rebound to different immutable invocation
    content.  A concrete durable duplicate-protection/reconciliation mechanism is
    intentionally deferred to an ADR when one is selected and relied upon.
    """

    if not isinstance(state, RuntimeConsistencyState):
        raise ValueError("state must be a RuntimeConsistencyState")
    if side_effect_class not in {
        OperationSideEffectClass.EXTERNAL_MUTATION,
        OperationSideEffectClass.COMMITMENT,
    }:
        raise ValueError("external consequence boundary requires ExternalMutation or Commitment")
    if not isinstance(effect_descriptor, tuple) or not effect_descriptor or any(
        not isinstance(item, tuple)
        or len(item) != 2
        or not all(isinstance(part, str) and part.strip() for part in item)
        for item in effect_descriptor
    ):
        raise ValueError("effect_descriptor must be explicit immutable non-empty string pairs")
    if not isinstance(reported_outcome, ConsequentialOutcome):
        raise ValueError("reported external outcome must be explicit")
    _validate_retry_token(retry_semantics, retry_token)
    require_consequential_operation_admission(execution, side_effect_class=side_effect_class)

    fingerprint = _external_fingerprint(
        execution=execution,
        side_effect_class=side_effect_class,
        effect_descriptor=effect_descriptor,
    )
    attempts = _matching_attempts(
        state,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
        fingerprint=fingerprint,
    )
    committed = tuple(item for item in attempts if item.outcome is ConsequentialOutcome.SUCCEEDED)
    if committed:
        return ExternalAttemptResult(state=state, attempt=committed[-1], duplicate=True)
    uncertain = tuple(item for item in attempts if item.outcome is ConsequentialOutcome.UNCERTAIN)
    if uncertain:
        raise ReconciliationRequiredError(
            "prior external consequential outcome is uncertain; blind retry is prohibited"
        )

    attempt = ConsequentialAttempt(
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        operation_name=execution.operation_name,
        side_effect_class=side_effect_class,
        retry_semantics=retry_semantics,
        retry_token=retry_token,
        fingerprint=fingerprint,
        outcome=reported_outcome,
    )
    next_state = RuntimeConsistencyState(
        canonical_records=state.canonical_records,
        admitted_events=state.admitted_events,
        attempts=(*state.attempts, attempt),
    )
    return ExternalAttemptResult(state=next_state, attempt=attempt, duplicate=False)
