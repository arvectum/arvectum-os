"""P1.07 — canonical Event admission and execution linkage.

This module keeps Event receipt distinct from canonical admission. It admits one
append-only Native Event for the completed P1.06 mutation, links that Event to
the exact terminal Execution Context version and resulting canonical version,
and handles duplicate/conflicting Event Identity reuse without rewriting
history.

The boundary is deliberately in-memory, domain-neutral and non-public. It does
not select an event broker, durable event store, outbox/inbox mechanism, schema
registry, delivery protocol or projection technology. Broader provenance and
reconstruction remain P1.08 scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .canonical import AuthorityMode, CanonicalRecord
from .execution import ExecutionLifecycle, GovernedVersionPin
from .identity import Identity
from .mutation import CanonicalMutationResult
from .security import OrganizationScope


class EventIdentityConflictError(RuntimeError):
    """One Event Identity was presented with conflicting immutable content."""


@dataclass(frozen=True, slots=True)
class EventCandidate:
    """Transient received Event representation awaiting canonical admission.

    Receipt is deliberately not canonical history. Only ``admit_p1_07_event``
    can create the Canonical Record specialization used by this bounded slice.
    """

    event_id: Identity
    version_id: Identity
    event_type: str
    event_schema_version: str
    organization: OrganizationScope
    authority_mode: AuthorityMode
    authority_scope: str
    authoritative_source: str
    occurred_at: datetime
    recorded_at: datetime
    producer_id: Identity
    initiating_actor_id: Identity
    execution_subject_id: Identity
    execution_version_id: Identity
    related_subject_ids: tuple[Identity, ...]
    related_version_ids: tuple[Identity, ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    classification: str
    access_scope: str
    provenance_refs: tuple[Identity, ...]
    integrity_metadata: tuple[tuple[str, str], ...]
    payload: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        identities = (
            self.event_id,
            self.version_id,
            self.producer_id,
            self.initiating_actor_id,
            self.execution_subject_id,
            self.execution_version_id,
            *self.related_subject_ids,
            *self.related_version_ids,
            *self.correlation_refs,
            *self.causation_refs,
            *self.provenance_refs,
        )
        if any(not isinstance(identity, Identity) for identity in identities):
            raise ValueError("Event candidate references must be Identity values")
        if self.event_id == self.version_id:
            raise ValueError("Event Identity and Event Version Identity must remain distinct")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("Event candidate Organization scope must be explicit")
        if self.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("P1.07 admits only Native Events produced by governed Arvectum OS operation")
        for field_name in (
            "event_type",
            "event_schema_version",
            "authority_scope",
            "authoritative_source",
            "classification",
            "access_scope",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{field_name} must be a non-empty string")
        for field_name in ("occurred_at", "recorded_at"):
            value = getattr(self, field_name)
            if (
                not isinstance(value, datetime)
                or value.tzinfo is None
                or value.utcoffset() is None
            ):
                raise ValueError(f"{field_name} must be timezone-aware")
        if self.recorded_at < self.occurred_at:
            raise ValueError("Event recording/admission time cannot precede the bounded occurrence time")
        if not self.related_subject_ids or not self.related_version_ids:
            raise ValueError("Event candidate must preserve related governed Subject and Version references")
        if not self.correlation_refs:
            raise ValueError("Event candidate must preserve explicit correlation for the bounded execution")
        if not self.causation_refs:
            raise ValueError("Event candidate must preserve explicit causation for the bounded execution")
        if not self.provenance_refs:
            raise ValueError("Event candidate provenance must be explicit")
        if not self.integrity_metadata or any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) and value.strip() for value in item)
            for item in self.integrity_metadata
        ):
            raise ValueError("Event candidate integrity metadata must contain non-empty key/value pairs")
        if not isinstance(self.payload, tuple) or any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) for value in item)
            for item in self.payload
        ):
            raise ValueError("Event candidate payload must use immutable string key/value pairs")

        organization_scope = self.organization.organization_id.value
        organization_scoped = (
            self.event_id,
            self.version_id,
            self.execution_subject_id,
            self.execution_version_id,
            *self.related_subject_ids,
            *self.related_version_ids,
            *self.correlation_refs,
            *self.causation_refs,
        )
        if any(identity.scope != organization_scope for identity in organization_scoped):
            raise ValueError("governed Event/execution/related references must share Organization scope")


@dataclass(frozen=True, slots=True)
class CanonicalEvent:
    """One admitted immutable Event Canonical Record specialization."""

    record: CanonicalRecord
    event_type: str
    event_schema_version: str
    authoritative_source: str
    occurred_at: datetime
    recorded_at: datetime
    producer_id: Identity
    initiating_actor_id: Identity
    execution_subject_id: Identity
    execution_version_id: Identity
    related_subject_ids: tuple[Identity, ...]
    related_version_ids: tuple[Identity, ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    classification: str
    access_scope: str

    def __post_init__(self) -> None:
        if not isinstance(self.record, CanonicalRecord):
            raise ValueError("Canonical Event must use a CanonicalRecord envelope")
        if self.record.semantic_type != "platform.event":
            raise ValueError("Canonical Event semantic_type must be platform.event")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("P1.07 canonical Event must use Native authority")
        if self.record.lifecycle_status != "Admitted":
            raise ValueError("P1.07 canonical Event lifecycle status must be Admitted")
        if self.record.predecessor_version_id is not None:
            raise ValueError("an admitted P1.07 Event is single-version and has no predecessor")
        if self.record.created_at != self.recorded_at:
            raise ValueError("Event Canonical Record creation time must equal admission/recording time")
        if self.record.schema_version != self.event_schema_version:
            raise ValueError("Event schema version must remain version-identifiable in the canonical envelope")
        if self.record.authority_scope != "platform.event/canonical-state-change":
            raise ValueError("P1.07 Event authority scope must identify canonical-state-change history")
        if self.execution_version_id not in self.record.provenance_refs:
            raise ValueError("canonical Event provenance must preserve exact Execution Context version")
        if any(version_id not in self.record.provenance_refs for version_id in self.related_version_ids):
            raise ValueError("canonical Event provenance must preserve exact related Version Identities")

    @property
    def event_id(self) -> Identity:
        return self.record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.record.version_id


@dataclass(frozen=True, slots=True)
class EventAdmissionResult:
    """Immutable outcome of one bounded canonical Event admission attempt."""

    event: CanonicalEvent
    admitted_events: tuple[CanonicalEvent, ...]
    duplicate_delivery: bool

    def __post_init__(self) -> None:
        if not isinstance(self.event, CanonicalEvent):
            raise ValueError("admission result must expose one CanonicalEvent")
        if not isinstance(self.admitted_events, tuple) or any(
            not isinstance(item, CanonicalEvent) for item in self.admitted_events
        ):
            raise ValueError("admitted_events must contain CanonicalEvent values")
        if self.event not in self.admitted_events:
            raise ValueError("admission result history must contain the exposed Event")
        matching = tuple(item for item in self.admitted_events if item.event_id == self.event.event_id)
        if len(matching) != 1:
            raise ValueError("canonical Event history must contain one occurrence per Event Identity")


def build_p1_07_event_candidate(*, mutation: CanonicalMutationResult) -> EventCandidate:
    """Build the deterministic received representation for the completed P1.06 mutation."""

    if not isinstance(mutation, CanonicalMutationResult):
        raise ValueError("P1.07 requires the exact P1.06 CanonicalMutationResult")
    execution = mutation.execution
    if execution.record.lifecycle_status != ExecutionLifecycle.SUCCEEDED.value:
        raise ValueError("P1.07 requires the terminal Succeeded Execution Context version")
    if len(execution.canonical_effects) != 1:
        raise ValueError("P1.07 requires exactly one P1.06 canonical effect")
    effect_pin = GovernedVersionPin.from_record(mutation.resulting_record)
    if execution.canonical_effects[0] != effect_pin:
        raise ValueError("P1.07 requires the exact canonical effect pinned by terminal execution")

    organization_scope = execution.organization.organization_id.value
    producer_id = execution.initiating_actor.actual_principal.principal_id
    return EventCandidate(
        event_id=Identity(
            "event-subject",
            "reference-subject-maintenance-execution-1-canonical-mutation-succeeded",
            organization_scope,
        ),
        version_id=Identity(
            "event-version",
            "reference-subject-maintenance-execution-1-canonical-mutation-succeeded-v1",
            organization_scope,
        ),
        event_type="platform.canonical-mutation.succeeded",
        event_schema_version="1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.event/canonical-state-change",
        authoritative_source="Arvectum OS",
        occurred_at=mutation.resulting_record.created_at,
        recorded_at=datetime.fromisoformat("2026-08-08T04:12:00+00:00"),
        producer_id=producer_id,
        initiating_actor_id=producer_id,
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        related_subject_ids=(mutation.resulting_record.subject_id,),
        related_version_ids=(mutation.resulting_record.version_id,),
        correlation_refs=(execution.execution_subject_id,),
        causation_refs=(execution.execution_version_id,),
        classification="internal",
        access_scope="organization",
        provenance_refs=(
            producer_id,
            execution.execution_subject_id,
            execution.execution_version_id,
            mutation.resulting_record.subject_id,
            mutation.resulting_record.version_id,
        ),
        integrity_metadata=(("representation", "frozen-in-memory-reference"),),
        payload=(
            ("operation", execution.operation_name),
            ("outcome", ExecutionLifecycle.SUCCEEDED.value),
        ),
    )


def _canonicalize_candidate(
    *,
    candidate: EventCandidate,
    mutation: CanonicalMutationResult,
) -> CanonicalEvent:
    record = CanonicalRecord(
        subject_id=candidate.event_id,
        version_id=candidate.version_id,
        semantic_type="platform.event",
        schema_version=candidate.event_schema_version,
        organization=candidate.organization,
        authority_mode=candidate.authority_mode,
        authority_scope=candidate.authority_scope,
        accountable_owner_id=mutation.execution.record.accountable_owner_id,
        creation_actor=mutation.execution.initiating_actor,
        created_at=candidate.recorded_at,
        provenance_refs=candidate.provenance_refs,
        integrity_metadata=candidate.integrity_metadata,
        payload=candidate.payload,
        lifecycle_status="Admitted",
        predecessor_version_id=None,
    )
    return CanonicalEvent(
        record=record,
        event_type=candidate.event_type,
        event_schema_version=candidate.event_schema_version,
        authoritative_source=candidate.authoritative_source,
        occurred_at=candidate.occurred_at,
        recorded_at=candidate.recorded_at,
        producer_id=candidate.producer_id,
        initiating_actor_id=candidate.initiating_actor_id,
        execution_subject_id=candidate.execution_subject_id,
        execution_version_id=candidate.execution_version_id,
        related_subject_ids=candidate.related_subject_ids,
        related_version_ids=candidate.related_version_ids,
        correlation_refs=candidate.correlation_refs,
        causation_refs=candidate.causation_refs,
        classification=candidate.classification,
        access_scope=candidate.access_scope,
    )


def _require_exact_p1_06_linkage(
    *,
    candidate: EventCandidate,
    mutation: CanonicalMutationResult,
) -> None:
    execution = mutation.execution
    resulting_record = mutation.resulting_record
    if execution.record.lifecycle_status != ExecutionLifecycle.SUCCEEDED.value:
        raise ValueError("canonical Event may link only to the terminal Succeeded P1.06 execution")
    if candidate.organization != execution.organization or candidate.organization != resulting_record.organization:
        raise ValueError("Event, execution and resulting canonical version must share Organization scope")
    if candidate.execution_subject_id != execution.execution_subject_id:
        raise ValueError("Event must reference the exact P1.06 Execution Subject Identity")
    if candidate.execution_version_id != execution.execution_version_id:
        raise ValueError("Event must reference the exact terminal Execution Context Version Identity")
    if candidate.related_subject_ids != (resulting_record.subject_id,):
        raise ValueError("P1.07 Event must reference exactly the resulting target Subject Identity")
    if candidate.related_version_ids != (resulting_record.version_id,):
        raise ValueError("P1.07 Event must reference exactly the resulting target Version Identity")
    if candidate.correlation_refs != (execution.execution_subject_id,):
        raise ValueError("P1.07 Event correlation must preserve the Execution Subject Identity")
    if candidate.causation_refs != (execution.execution_version_id,):
        raise ValueError("P1.07 Event causation must preserve the terminal Execution Context version")
    expected_actor = execution.initiating_actor.actual_principal.principal_id
    if candidate.producer_id != expected_actor or candidate.initiating_actor_id != expected_actor:
        raise ValueError("Event producer/initiation attribution must preserve the P1.06 initiating Principal")
    if candidate.occurred_at != resulting_record.created_at:
        raise ValueError("P1.07 occurrence time must preserve the bounded canonical mutation occurrence time")
    if candidate.event_type != "platform.canonical-mutation.succeeded":
        raise ValueError("P1.07 bounded Event type must describe successful canonical mutation")
    if candidate.event_schema_version != "1":
        raise ValueError("P1.07 bounded Event schema version must be explicit and supported")
    expected_payload = (
        ("operation", execution.operation_name),
        ("outcome", ExecutionLifecycle.SUCCEEDED.value),
    )
    if candidate.payload != expected_payload:
        raise ValueError("P1.07 Event payload must preserve the exact bounded operation outcome")
    required_provenance = {
        execution.execution_subject_id,
        execution.execution_version_id,
        resulting_record.subject_id,
        resulting_record.version_id,
    }
    if not required_provenance.issubset(set(candidate.provenance_refs)):
        raise ValueError("P1.07 Event provenance must preserve exact execution and resulting-version references")


def _validate_admitted_history(admitted_events: tuple[CanonicalEvent, ...]) -> None:
    if not isinstance(admitted_events, tuple) or any(
        not isinstance(item, CanonicalEvent) for item in admitted_events
    ):
        raise ValueError("admitted Event history must be an immutable tuple of CanonicalEvent values")
    event_ids = tuple(item.event_id for item in admitted_events)
    if len(set(event_ids)) != len(event_ids):
        raise ValueError("admitted Event history must not contain duplicate Event Identities")
    version_ids = tuple(item.version_id for item in admitted_events)
    if len(set(version_ids)) != len(version_ids):
        raise ValueError("admitted Event history must not reuse immutable Event Version Identities")


def admit_p1_07_event(
    *,
    candidate: EventCandidate,
    mutation: CanonicalMutationResult,
    admitted_events: tuple[CanonicalEvent, ...] = (),
) -> EventAdmissionResult:
    """Admit or idempotently recognize one exact canonical Event occurrence.

    ``admitted_events`` is caller-supplied immutable history for this bounded
    in-memory harness. It is not an event store, topic, projection or persistence
    contract. Duplicate delivery returns the already-admitted Event. Reuse of
    the same Event Identity with materially different immutable content raises
    ``EventIdentityConflictError`` and leaves the supplied history untouched.
    """

    if not isinstance(candidate, EventCandidate):
        raise ValueError("canonical Event admission requires an EventCandidate receipt")
    if not isinstance(mutation, CanonicalMutationResult):
        raise ValueError("canonical Event admission requires the exact P1.06 mutation result")
    _validate_admitted_history(admitted_events)

    proposed = _canonicalize_candidate(candidate=candidate, mutation=mutation)
    same_identity = tuple(item for item in admitted_events if item.event_id == candidate.event_id)
    if same_identity:
        existing = same_identity[0]
        if existing != proposed:
            raise EventIdentityConflictError(
                "Event Identity already admitted with different immutable canonical content"
            )
        _require_exact_p1_06_linkage(candidate=candidate, mutation=mutation)
        return EventAdmissionResult(
            event=existing,
            admitted_events=admitted_events,
            duplicate_delivery=True,
        )

    if any(item.version_id == candidate.version_id for item in admitted_events):
        raise EventIdentityConflictError(
            "Event Version Identity is already used by another immutable Event occurrence"
        )

    _require_exact_p1_06_linkage(candidate=candidate, mutation=mutation)
    admitted = (*admitted_events, proposed)
    return EventAdmissionResult(
        event=proposed,
        admitted_events=admitted,
        duplicate_delivery=False,
    )
