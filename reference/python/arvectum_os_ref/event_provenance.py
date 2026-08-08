"""P2.05 — reusable Event admission, provenance and reconstruction runtime.

This module generalizes the Phase 1 Event/provenance proof into bounded,
domain-neutral, in-memory runtime semantics. Receipt remains transient until
canonical admission; admitted Events are immutable Canonical Record
specializations; duplicate delivery of one exact immutable occurrence is
recognized without creating another Event; conflicting reuse of an Event
Identity is rejected; and reconstruction is derived from exact governed
references rather than mutable projections or telemetry.

The boundary deliberately does not select a broker, durable Event store,
delivery topology, schema registry, telemetry backend, transaction model,
public API/SDK or Product Contract validator. P2.06 remains responsible for
broader durable consistency, concurrency and idempotency semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .execution import GovernedVersionPin
from .governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLineage,
    GovernedGateDecision,
)
from .identity import Identity
from .security import OrganizationScope


EVENT_RECORD_SEMANTIC_TYPE: Final = "platform.event"
EVENT_ADMITTED_STATUS: Final = "Admitted"


class EventRuntimeError(RuntimeError):
    """Base error for bounded P2.05 Event runtime invariants."""


class EventIdentityConflictError(EventRuntimeError):
    """One Event Identity was presented with materially different immutable content."""


class EventVersionIdentityConflictError(EventRuntimeError):
    """One immutable Event Version Identity was reused by another Event occurrence."""


class ReconstructionEvidenceError(ValueError):
    """Supplied governed evidence is insufficient or internally inconsistent."""


def _require_aware_datetime(value: datetime, *, label: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be a timezone-aware datetime")


def _require_identity_tuple(value: tuple[Identity, ...], *, label: str) -> None:
    if not isinstance(value, tuple) or any(not isinstance(item, Identity) for item in value):
        raise ValueError(f"{label} must be an immutable tuple of Identity values")
    if len(set(value)) != len(value):
        raise ValueError(f"{label} must not contain duplicate Identity values")


def _require_string_pairs(value: tuple[tuple[str, str], ...], *, label: str, nonempty: bool) -> None:
    if not isinstance(value, tuple) or (nonempty and not value):
        raise ValueError(f"{label} must be an immutable tuple of string key/value pairs")
    if any(
        not isinstance(item, tuple)
        or len(item) != 2
        or not all(isinstance(part, str) for part in item)
        for item in value
    ):
        raise ValueError(f"{label} must contain only string key/value pairs")
    if nonempty and any(not key.strip() or not val.strip() for key, val in value):
        raise ValueError(f"{label} entries must be non-empty")


def _ordered_unique(*groups: tuple[Identity, ...]) -> tuple[Identity, ...]:
    result: list[Identity] = []
    seen: set[Identity] = set()
    for group in groups:
        for identity in group:
            if not isinstance(identity, Identity):
                raise ValueError("provenance references must be Identity values")
            if identity not in seen:
                result.append(identity)
                seen.add(identity)
    return tuple(result)


@dataclass(frozen=True, slots=True)
class EventReceipt:
    """Transient received representation awaiting canonical Event admission."""

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
        for label, identity in (
            ("Event Identity", self.event_id),
            ("Event Version Identity", self.version_id),
            ("producer", self.producer_id),
            ("initiating actor", self.initiating_actor_id),
            ("Execution Identity", self.execution_subject_id),
            ("Execution Version Identity", self.execution_version_id),
        ):
            if not isinstance(identity, Identity):
                raise ValueError(f"{label} must be an Identity")
        if self.event_id == self.version_id:
            raise ValueError("Event Identity and Event Version Identity are distinct roles")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("Event receipt Organization scope must be explicit")
        if self.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError(
                "bounded P2.05 admission currently supports Native Events only; external authority requires its explicit authority contract"
            )
        for label in (
            "event_type",
            "event_schema_version",
            "authority_scope",
            "authoritative_source",
            "classification",
            "access_scope",
        ):
            value = getattr(self, label)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be a non-empty string")
        _require_aware_datetime(self.occurred_at, label="Event occurrence time")
        _require_aware_datetime(self.recorded_at, label="Event recording/admission time")

        for label, refs in (
            ("related_subject_ids", self.related_subject_ids),
            ("related_version_ids", self.related_version_ids),
            ("correlation_refs", self.correlation_refs),
            ("causation_refs", self.causation_refs),
            ("provenance_refs", self.provenance_refs),
        ):
            _require_identity_tuple(refs, label=label)
        if not self.correlation_refs:
            raise ValueError("bounded execution-linked Event receipt requires explicit correlation")
        if not self.causation_refs:
            raise ValueError("bounded execution-linked Event receipt requires explicit causation")
        if not self.provenance_refs:
            raise ValueError("Event receipt provenance must be explicit")
        _require_string_pairs(self.integrity_metadata, label="integrity_metadata", nonempty=True)
        _require_string_pairs(self.payload, label="payload", nonempty=False)

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
        if any(item.scope != organization_scope for item in organization_scoped):
            raise ValueError("Event/execution/related/correlation/causation references must share Organization scope")


@dataclass(frozen=True, slots=True)
class CanonicalEvent:
    """One admitted append-only Event Canonical Record specialization."""

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
        if self.record.semantic_type != EVENT_RECORD_SEMANTIC_TYPE:
            raise ValueError("Canonical Event semantic_type must be platform.event")
        if self.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("bounded P2.05 Canonical Event currently supports Native authority")
        if self.record.lifecycle_status != EVENT_ADMITTED_STATUS:
            raise ValueError("Canonical Event lifecycle status must be Admitted")
        if self.record.predecessor_version_id is not None:
            raise ValueError("an admitted Event is normally single-version and has no predecessor")
        if self.record.schema_version != self.event_schema_version:
            raise ValueError("Event schema version must remain exact in the canonical envelope")
        if self.record.created_at != self.recorded_at:
            raise ValueError("Event Canonical Record creation time must equal recording/admission time")
        _require_aware_datetime(self.occurred_at, label="Event occurrence time")
        _require_aware_datetime(self.recorded_at, label="Event recording/admission time")
        for label in (
            "event_type",
            "event_schema_version",
            "authoritative_source",
            "classification",
            "access_scope",
        ):
            value = getattr(self, label)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{label} must be explicit")
        for label, refs in (
            ("related_subject_ids", self.related_subject_ids),
            ("related_version_ids", self.related_version_ids),
            ("correlation_refs", self.correlation_refs),
            ("causation_refs", self.causation_refs),
        ):
            _require_identity_tuple(refs, label=label)

        organization_scope = self.record.organization.organization_id.value
        scoped_refs = (
            self.record.subject_id,
            self.record.version_id,
            self.execution_subject_id,
            self.execution_version_id,
            *self.related_subject_ids,
            *self.related_version_ids,
            *self.correlation_refs,
            *self.causation_refs,
        )
        if any(ref.scope != organization_scope for ref in scoped_refs):
            raise ValueError("Canonical Event governed references must share Organization scope")

        required_provenance = {
            self.producer_id,
            self.initiating_actor_id,
            self.execution_subject_id,
            self.execution_version_id,
            *self.related_subject_ids,
            *self.related_version_ids,
        }
        if not required_provenance.issubset(set(self.record.provenance_refs)):
            raise ValueError("Canonical Event provenance must preserve actor, execution and related governed references")

    @property
    def event_id(self) -> Identity:
        return self.record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.record.version_id

    @property
    def organization(self) -> OrganizationScope:
        return self.record.organization

    @property
    def version_pin(self) -> GovernedVersionPin:
        return GovernedVersionPin.from_record(self.record)


@dataclass(frozen=True, slots=True)
class EventAdmissionResult:
    """Immutable outcome of one bounded Event admission attempt."""

    event: CanonicalEvent
    admitted_events: tuple[CanonicalEvent, ...]
    duplicate_delivery: bool

    def __post_init__(self) -> None:
        if not isinstance(self.event, CanonicalEvent):
            raise ValueError("Event admission result must expose one CanonicalEvent")
        _validate_admitted_history(self.admitted_events)
        if self.event not in self.admitted_events:
            raise ValueError("Event admission history must contain the exposed Event")


def _validate_admitted_history(admitted_events: tuple[CanonicalEvent, ...]) -> None:
    if not isinstance(admitted_events, tuple) or any(
        not isinstance(item, CanonicalEvent) for item in admitted_events
    ):
        raise ValueError("admitted Event history must be an immutable tuple of CanonicalEvent values")
    event_ids = tuple(item.event_id for item in admitted_events)
    if len(set(event_ids)) != len(event_ids):
        raise ValueError("admitted Event history must contain at most one canonical Event per Event Identity")
    version_ids = tuple(item.version_id for item in admitted_events)
    if len(set(version_ids)) != len(version_ids):
        raise ValueError("admitted Event history must not reuse immutable Event Version Identities")


def _validate_receipt_linkage(
    *,
    receipt: EventReceipt,
    execution: GovernedExecutionContext,
    related_records: tuple[CanonicalRecord, ...],
) -> None:
    if not isinstance(execution, GovernedExecutionContext):
        raise ValueError("Event admission requires the exact governed Execution Context version")
    if receipt.organization != execution.organization:
        raise ValueError("Event receipt and execution must share Organization scope")
    if receipt.execution_subject_id != execution.execution_subject_id:
        raise ValueError("Event receipt must reference the exact stable Execution Identity")
    if receipt.execution_version_id != execution.execution_version_id:
        raise ValueError("Event receipt must reference the exact Execution Context Version Identity")
    if receipt.execution_subject_id not in receipt.correlation_refs:
        raise ValueError("execution-linked Event correlation must preserve the stable Execution Identity")
    if receipt.execution_version_id not in receipt.causation_refs:
        raise ValueError("execution-linked Event causation must preserve the exact Execution Context version")
    if receipt.initiating_actor_id not in execution.record.provenance_refs:
        raise ValueError("Event initiating actor must be attributable from governed execution provenance")
    required_base_provenance = {
        receipt.producer_id,
        receipt.initiating_actor_id,
        receipt.execution_subject_id,
        receipt.execution_version_id,
    }
    if not required_base_provenance.issubset(set(receipt.provenance_refs)):
        raise ValueError("Event receipt provenance must preserve producer, initiator and exact execution references")

    if not isinstance(related_records, tuple) or any(
        not isinstance(item, CanonicalRecord) for item in related_records
    ):
        raise ValueError("related_records must be an immutable tuple of CanonicalRecord versions")
    if any(item.organization != execution.organization for item in related_records):
        raise ValueError("Event related governed records must share Execution Organization scope")
    if len({item.version_id for item in related_records}) != len(related_records):
        raise ValueError("Event related governed records must use distinct Version Identities")

    expected_subjects = {item.subject_id for item in related_records}
    expected_versions = {item.version_id for item in related_records}
    if not expected_subjects.issubset(set(receipt.related_subject_ids)):
        raise ValueError("Event receipt must preserve every supplied related Subject Identity")
    if not expected_versions.issubset(set(receipt.related_version_ids)):
        raise ValueError("Event receipt must preserve every supplied related Version Identity")
    if not (expected_subjects | expected_versions).issubset(set(receipt.provenance_refs)):
        raise ValueError("Event provenance must preserve exact supplied related governed versions")


def _canonicalize_receipt(
    *,
    receipt: EventReceipt,
    execution: GovernedExecutionContext,
) -> CanonicalEvent:
    record = CanonicalRecord(
        subject_id=receipt.event_id,
        version_id=receipt.version_id,
        semantic_type=EVENT_RECORD_SEMANTIC_TYPE,
        schema_version=receipt.event_schema_version,
        organization=receipt.organization,
        authority_mode=receipt.authority_mode,
        authority_scope=receipt.authority_scope,
        accountable_owner_id=execution.record.accountable_owner_id,
        creation_actor=execution.record.creation_actor,
        created_at=receipt.recorded_at,
        provenance_refs=receipt.provenance_refs,
        integrity_metadata=receipt.integrity_metadata,
        payload=receipt.payload,
        lifecycle_status=EVENT_ADMITTED_STATUS,
        predecessor_version_id=None,
    )
    return CanonicalEvent(
        record=record,
        event_type=receipt.event_type,
        event_schema_version=receipt.event_schema_version,
        authoritative_source=receipt.authoritative_source,
        occurred_at=receipt.occurred_at,
        recorded_at=receipt.recorded_at,
        producer_id=receipt.producer_id,
        initiating_actor_id=receipt.initiating_actor_id,
        execution_subject_id=receipt.execution_subject_id,
        execution_version_id=receipt.execution_version_id,
        related_subject_ids=receipt.related_subject_ids,
        related_version_ids=receipt.related_version_ids,
        correlation_refs=receipt.correlation_refs,
        causation_refs=receipt.causation_refs,
        classification=receipt.classification,
        access_scope=receipt.access_scope,
    )


def admit_event(
    *,
    receipt: EventReceipt,
    execution: GovernedExecutionContext,
    related_records: tuple[CanonicalRecord, ...] = (),
    admitted_events: tuple[CanonicalEvent, ...] = (),
) -> EventAdmissionResult:
    """Admit or idempotently recognize one exact immutable Event occurrence.

    The caller-supplied ``admitted_events`` tuple is bounded in-memory canonical
    history for this reference runtime. It is not a broker, event-store or
    transaction contract. Broader durable conflict/idempotency semantics remain
    P2.06 scope.
    """

    if not isinstance(receipt, EventReceipt):
        raise ValueError("Event admission requires an EventReceipt")
    _validate_admitted_history(admitted_events)
    _validate_receipt_linkage(
        receipt=receipt,
        execution=execution,
        related_records=related_records,
    )
    candidate = _canonicalize_receipt(receipt=receipt, execution=execution)

    same_identity = tuple(item for item in admitted_events if item.event_id == candidate.event_id)
    if same_identity:
        existing = same_identity[0]
        if existing != candidate:
            raise EventIdentityConflictError(
                "Event Identity already exists with materially different immutable canonical content"
            )
        return EventAdmissionResult(
            event=existing,
            admitted_events=admitted_events,
            duplicate_delivery=True,
        )

    if any(item.version_id == candidate.version_id for item in admitted_events):
        raise EventVersionIdentityConflictError(
            "Event Version Identity is already used by another canonical Event occurrence"
        )

    history = (*admitted_events, candidate)
    return EventAdmissionResult(event=candidate, admitted_events=history, duplicate_delivery=False)


@dataclass(frozen=True, slots=True)
class ReconstructionManifest:
    """Read-only exact-reference manifest for one reconstructed governed execution."""

    organization: OrganizationScope
    execution_subject_id: Identity
    initiating_actor_id: Identity
    operation_name: str
    workflow: GovernedVersionPin
    material_inputs: tuple[GovernedVersionPin, ...]
    gate_decisions: tuple[GovernedVersionPin, ...]
    execution_versions: tuple[GovernedVersionPin, ...]
    results: tuple[GovernedVersionPin, ...]
    events: tuple[GovernedVersionPin, ...]
    event_types: tuple[tuple[str, str], ...]
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]
    provenance_refs: tuple[Identity, ...]
    product_contract: GovernedVersionPin | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ReconstructionEvidenceError("reconstruction Organization scope must be explicit")
        if not isinstance(self.execution_subject_id, Identity):
            raise ReconstructionEvidenceError("reconstruction Execution Identity must be explicit")
        if not isinstance(self.initiating_actor_id, Identity):
            raise ReconstructionEvidenceError("reconstruction initiating actor must be explicit")
        if not isinstance(self.operation_name, str) or not self.operation_name.strip():
            raise ReconstructionEvidenceError("reconstruction operation_name must be explicit")
        if not isinstance(self.workflow, GovernedVersionPin):
            raise ReconstructionEvidenceError("reconstruction must pin the exact Workflow version")
        if self.product_contract is not None and not isinstance(self.product_contract, GovernedVersionPin):
            raise ReconstructionEvidenceError("Product Contract reconstruction reference must be version-pinned")

        pin_groups = (
            ("material_inputs", self.material_inputs, True),
            ("gate_decisions", self.gate_decisions, False),
            ("execution_versions", self.execution_versions, True),
            ("results", self.results, True),
            ("events", self.events, True),
        )
        for label, pins, required in pin_groups:
            if not isinstance(pins, tuple) or (required and not pins) or any(
                not isinstance(pin, GovernedVersionPin) for pin in pins
            ):
                raise ReconstructionEvidenceError(
                    f"{label} must contain exact immutable GovernedVersionPin values"
                )
            if len({pin.version_id for pin in pins}) != len(pins):
                raise ReconstructionEvidenceError(f"{label} must not contain duplicate Version Identities")

        if not isinstance(self.event_types, tuple) or len(self.event_types) != len(self.events):
            raise ReconstructionEvidenceError("event_types must align one-to-one with reconstructed Events")
        if any(
            not isinstance(item, tuple)
            or len(item) != 2
            or not all(isinstance(value, str) and value.strip() for value in item)
            for item in self.event_types
        ):
            raise ReconstructionEvidenceError("Event type/schema references must be version-identifiable")
        for label, refs in (
            ("correlation_refs", self.correlation_refs),
            ("causation_refs", self.causation_refs),
            ("provenance_refs", self.provenance_refs),
        ):
            if not isinstance(refs, tuple) or not refs or any(not isinstance(ref, Identity) for ref in refs):
                raise ReconstructionEvidenceError(f"{label} must contain explicit Identity references")
            if len(set(refs)) != len(refs):
                raise ReconstructionEvidenceError(f"{label} must not contain duplicates")

        organization_scope = self.organization.organization_id.value
        scoped_pins = (
            self.workflow,
            *self.material_inputs,
            *self.gate_decisions,
            *self.execution_versions,
            *self.results,
            *self.events,
            *((self.product_contract,) if self.product_contract is not None else ()),
        )
        if self.execution_subject_id.scope != organization_scope:
            raise ReconstructionEvidenceError("Execution Identity must share reconstruction Organization scope")
        if any(
            pin.subject_id.scope != organization_scope or pin.version_id.scope != organization_scope
            for pin in scoped_pins
        ):
            raise ReconstructionEvidenceError("reconstructed governed versions must share Organization scope")
        if any(ref.scope != organization_scope for ref in (*self.correlation_refs, *self.causation_refs)):
            raise ReconstructionEvidenceError("correlation and causation references must share Organization scope")


def _reconstruction_error(condition: bool, message: str) -> None:
    if not condition:
        raise ReconstructionEvidenceError(message)


def build_reconstruction_manifest(
    *,
    execution_versions: tuple[GovernedExecutionContext, ...],
    result_records: tuple[CanonicalRecord, ...],
    events: tuple[CanonicalEvent, ...],
) -> ReconstructionManifest:
    """Validate and summarize exact governed evidence without replaying side effects."""

    _reconstruction_error(
        isinstance(execution_versions, tuple)
        and bool(execution_versions)
        and all(isinstance(item, GovernedExecutionContext) for item in execution_versions),
        "reconstruction requires immutable governed Execution Context versions",
    )
    try:
        lineage = GovernedExecutionLineage(execution_versions)
    except (ValueError, RuntimeError) as exc:
        raise ReconstructionEvidenceError("execution history is not one valid immutable lineage") from exc
    head = lineage.head()
    _reconstruction_error(head.is_terminal, "reconstruction requires a sealed terminal Execution Context head")

    roots = tuple(item for item in execution_versions if item.record.predecessor_version_id is None)
    _reconstruction_error(len(roots) == 1, "execution lineage must contain exactly one initial version")
    root = roots[0]
    _reconstruction_error(
        all(item.organization == root.organization for item in execution_versions),
        "all reconstructed Execution Context versions must share Organization scope",
    )
    _reconstruction_error(
        all(item.workflow == root.workflow for item in execution_versions),
        "execution lineage must preserve one exact Workflow version",
    )
    _reconstruction_error(
        all(item.operation_name == root.operation_name for item in execution_versions),
        "execution lineage must preserve one semantic operation",
    )
    _reconstruction_error(
        all(item.material_inputs == root.material_inputs for item in execution_versions),
        "execution lineage must preserve the exact material input versions",
    )
    _reconstruction_error(
        all(item.required_gates == root.required_gates for item in execution_versions),
        "execution lineage must preserve one required-gate contract",
    )
    _reconstruction_error(
        all(item.product_contract == root.product_contract for item in execution_versions),
        "execution lineage must preserve the exact Product Contract attribution",
    )

    initiating_actor_id = root.record.creation_actor.actual_principal.principal_id
    _reconstruction_error(
        all(initiating_actor_id in item.record.provenance_refs for item in execution_versions),
        "execution lineage provenance must preserve the initiating actor",
    )

    decision_versions = {decision.record.version_id for decision in head.gate_decisions}
    execution_version_ids = {item.execution_version_id for item in execution_versions}
    for decision in head.gate_decisions:
        _reconstruction_error(
            isinstance(decision, GovernedGateDecision),
            "terminal execution gate evidence must use GovernedGateDecision values",
        )
        _reconstruction_error(
            decision.evaluated_execution_version_id in execution_version_ids,
            "gate decision must identify an Execution Context version present in reconstructed history",
        )
        _reconstruction_error(
            decision.record.version_id in head.record.provenance_refs,
            "terminal execution provenance must preserve each exact gate decision version",
        )
    if root.required_gates:
        _reconstruction_error(
            head.gates_satisfied,
            "result-bearing reconstruction requires every declared terminal gate to be satisfied",
        )
        _reconstruction_error(
            len(decision_versions) == len(root.required_gates),
            "terminal reconstruction must preserve one exact decision for every required gate",
        )

    _reconstruction_error(
        isinstance(result_records, tuple)
        and bool(result_records)
        and all(isinstance(item, CanonicalRecord) for item in result_records),
        "reconstruction requires at least one exact governed result version",
    )
    _reconstruction_error(
        len({item.version_id for item in result_records}) == len(result_records),
        "reconstructed result Version Identities must be distinct",
    )
    _reconstruction_error(
        all(item.organization == root.organization for item in result_records),
        "reconstructed results must share Execution Organization scope",
    )
    execution_refs = {lineage.execution_subject_id, *execution_version_ids}
    for record in result_records:
        _reconstruction_error(
            bool(execution_refs.intersection(record.provenance_refs)),
            "each reconstructed result must preserve provenance to the governed execution",
        )

    _reconstruction_error(
        isinstance(events, tuple)
        and bool(events)
        and all(isinstance(item, CanonicalEvent) for item in events),
        "reconstruction requires at least one admitted canonical Event",
    )
    _reconstruction_error(
        len({item.event_id for item in events}) == len(events),
        "reconstructed Events must use distinct Event Identities",
    )
    _reconstruction_error(
        all(item.organization == root.organization for item in events),
        "reconstructed Events must share Execution Organization scope",
    )
    for event in events:
        _reconstruction_error(
            event.execution_subject_id == lineage.execution_subject_id,
            "Event must preserve the reconstructed stable Execution Identity",
        )
        _reconstruction_error(
            event.execution_version_id in execution_version_ids,
            "Event must reference an exact Execution Context version present in reconstructed history",
        )
        _reconstruction_error(
            lineage.execution_subject_id in event.correlation_refs,
            "Event correlation must preserve the stable Execution Identity",
        )
        _reconstruction_error(
            event.execution_version_id in event.causation_refs,
            "Event causation must preserve its exact causal Execution Context version",
        )
        _reconstruction_error(
            event.initiating_actor_id == initiating_actor_id,
            "Event initiating-actor attribution must preserve the reconstructed initiating Principal",
        )

    result_version_ids = {item.version_id for item in result_records}
    event_related_versions = {ref for event in events for ref in event.related_version_ids}
    _reconstruction_error(
        result_version_ids.issubset(event_related_versions),
        "reconstructed Events must preserve every exact governed result Version Identity",
    )

    workflow = root.workflow
    gate_pins = tuple(decision.version_pin for decision in head.gate_decisions)
    execution_pins = tuple(GovernedVersionPin.from_record(item.record) for item in execution_versions)
    result_pins = tuple(GovernedVersionPin.from_record(item) for item in result_records)
    event_pins = tuple(item.version_pin for item in events)
    correlation_refs = _ordered_unique(*(item.correlation_refs for item in events))
    causation_refs = _ordered_unique(*(item.causation_refs for item in events))
    event_types = tuple((item.event_type, item.event_schema_version) for item in events)

    provenance_refs = _ordered_unique(
        (initiating_actor_id,),
        (lineage.execution_subject_id,),
        (workflow.subject_id, workflow.version_id),
        *((pin.subject_id, pin.version_id) for pin in root.material_inputs),
        *(
            ((root.product_contract.subject_id, root.product_contract.version_id),)
            if root.product_contract is not None
            else ()
        ),
        *(
            (
                decision.record.subject_id,
                decision.record.version_id,
                decision.record.creation_actor.actual_principal.principal_id,
                decision.basis_ref,
            )
            for decision in head.gate_decisions
        ),
        *((pin.subject_id, pin.version_id) for pin in execution_pins),
        *((pin.subject_id, pin.version_id) for pin in result_pins),
        *(
            (
                event.event_id,
                event.version_id,
                event.producer_id,
                event.initiating_actor_id,
            )
            for event in events
        ),
        correlation_refs,
        causation_refs,
    )

    return ReconstructionManifest(
        organization=root.organization,
        execution_subject_id=lineage.execution_subject_id,
        initiating_actor_id=initiating_actor_id,
        operation_name=root.operation_name,
        workflow=workflow,
        material_inputs=root.material_inputs,
        gate_decisions=gate_pins,
        execution_versions=execution_pins,
        results=result_pins,
        events=event_pins,
        event_types=event_types,
        correlation_refs=correlation_refs,
        causation_refs=causation_refs,
        provenance_refs=provenance_refs,
        product_contract=root.product_contract,
    )
