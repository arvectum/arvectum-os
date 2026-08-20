"""P8.05 — bounded external ingress/egress Event and reconciliation semantics.

This module is a Phase 8 reference/evidence harness.  It composes the existing
P2.05 Event/provenance and P2.06 retry/uncertainty semantics without selecting
an external transport, broker, durable inbox/outbox, reconciliation service or
public/stable integration API.

Important boundary:

* a transport delivery is transient evidence, not a canonical Event;
* the canonical ingress Event is Native evidence that Arvectum OS admitted an
  observation of an externally authoritative occurrence.  The external fact
  remains External Reference/Governed Replica through the linked record;
* repeated delivery of one external occurrence is recognized before canonical
  Event admission and cannot create a second canonical Event;
* a new source occurrence remains a new Event even when its payload digest is
  byte-identical to an earlier occurrence;
* external-effect outcome uncertainty remains append-only evidence and blocks
  blind retry until attributable reconciliation;
* reconciliation never rewrites the original uncertain attempt;
* a retry after reconciliation is a new governed execution/attempt and is
  permitted only when evidence confirms the prior effect was not applied;
* historical reconstruction is pure over retained evidence and contains no
  transport/effect execution hook.

The live external anchor for P8.05 is the already completed read-only P8.04 EIS
validation.  No new EIS mutation, submission, signature, message or other
external consequential effect is authorized or performed by this harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import (
    CanonicalEvent,
    EventReceipt,
    admit_event,
)
from arvectum_os_ref.governed_execution import GovernedExecutionContext
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.runtime_consistency import (
    ConsequentialAttempt,
    ConsequentialOutcome,
    ExternalAttemptResult,
    ReconciliationRequiredError,
    RetrySemantics,
    RuntimeConsistencyState,
    record_external_consequence_attempt,
)
from arvectum_os_ref.security import OrganizationScope
from arvectum_os_ref.workflow import OperationSideEffectClass


P804_NOTICE_NUMBER = "0344100006426000005"
P804_LIVE_RUN_ID = "toa-run-20260820083457-21337c"
P804_FRESH_OBSERVED_AT = "2026-08-20T08:34:57.365770+00:00"
P804_BASELINE_MANIFEST_SHA256 = (
    "74e943d855406b04741f040fed271bddfaada9a9cc6e7da4501735a6e8725121"
)
P804_FRESH_MANIFEST_SHA256 = (
    "4113935e43291f820a43fa2efad49663103a86408788b571d7d0e6dac4974a54"
)
P804_COMPARISON_MANIFEST_SHA256 = (
    "06ca91f5689d449b2bfba95ca0ec62386e215261df74ec769b234030cc610f7b"
)


class ExternalBoundaryError(RuntimeError):
    """Base P8.05 external-boundary semantic error."""


class ExternalOccurrenceConflictError(ExternalBoundaryError):
    """One declared external occurrence identity was rebound to different facts."""


class ExternalDeliveryConflictError(ExternalBoundaryError):
    """One transport delivery identity was reused with different delivery evidence."""


class RetryAfterReconciliationNotAllowedError(ExternalBoundaryError):
    """Reconciliation evidence does not permit a new external-effect attempt."""


class ReconciliationResolution(str, Enum):
    """What an attributable reconciliation established about an uncertain effect."""

    CONFIRMED_SUCCEEDED = "ConfirmedSucceeded"
    CONFIRMED_NOT_APPLIED = "ConfirmedNotApplied"
    STILL_UNCERTAIN = "StillUncertain"


@dataclass(frozen=True, slots=True)
class ExternalOccurrence:
    """Contract-scoped identity and minimized evidence for one external occurrence.

    ``event_id`` / ``event_version_id`` are the stable canonical Event identities
    assigned for this occurrence by the applicable integration mapping.  The
    class deliberately does not prescribe how a product or Product Contract
    derives them from vendor identifiers.
    """

    organization: OrganizationScope
    source_system: str
    source_object_ref: str
    source_occurrence_id: str
    source_version_ref: str
    authority_mode: AuthorityMode
    authority_scope: str
    occurred_at: datetime
    payload_integrity_ref: str
    event_id: Identity
    event_version_id: Identity
    governed_provenance_refs: tuple[Identity, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("external occurrence Organization scope must be explicit")
        for label in (
            "source_system",
            "source_object_ref",
            "source_occurrence_id",
            "source_version_ref",
            "authority_scope",
            "payload_integrity_ref",
        ):
            value = getattr(self, label)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"external occurrence {label} must be explicit")
        if self.authority_mode not in {
            AuthorityMode.EXTERNAL_REFERENCE,
            AuthorityMode.GOVERNED_REPLICA,
        }:
            raise ValueError("external occurrence must preserve External Reference or Governed Replica authority")
        _require_aware(self.occurred_at, label="external occurrence occurred_at")
        if not isinstance(self.event_id, Identity) or not isinstance(self.event_version_id, Identity):
            raise ValueError("external occurrence Event identities must be explicit")
        if self.event_id == self.event_version_id:
            raise ValueError("Event Subject and Version identities must remain distinct")
        scope = self.organization.organization_id.value
        if self.event_id.scope != scope or self.event_version_id.scope != scope:
            raise ValueError("external occurrence Event identities must share Organization scope")
        if not isinstance(self.governed_provenance_refs, tuple) or any(
            not isinstance(ref, Identity) for ref in self.governed_provenance_refs
        ):
            raise ValueError("external occurrence governed provenance must be immutable Identity references")

    @property
    def occurrence_key(self) -> tuple[str, str, str]:
        return (self.source_system, self.source_object_ref, self.source_occurrence_id)


@dataclass(frozen=True, slots=True)
class ExternalDelivery:
    """Transient transport evidence for one delivery of an external occurrence."""

    delivery_id: Identity
    occurrence: ExternalOccurrence
    received_at: datetime
    transport_name: str
    payload_integrity_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.delivery_id, Identity):
            raise ValueError("external delivery identity must be explicit")
        if self.delivery_id.scope != self.occurrence.organization.organization_id.value:
            raise ValueError("external delivery must share Organization scope")
        _require_aware(self.received_at, label="external delivery received_at")
        if not isinstance(self.transport_name, str) or not self.transport_name.strip():
            raise ValueError("external delivery transport_name must be explicit")
        if not isinstance(self.payload_integrity_ref, str) or not self.payload_integrity_ref.strip():
            raise ValueError("external delivery payload_integrity_ref must be explicit")
        if self.payload_integrity_ref != self.occurrence.payload_integrity_ref:
            raise ValueError("delivery integrity must identify the declared external occurrence payload")


@dataclass(frozen=True, slots=True)
class ExternalIngressAdmission:
    """First canonical admission of one external occurrence."""

    occurrence: ExternalOccurrence
    event: CanonicalEvent
    first_delivery_id: Identity
    first_recorded_at: datetime

    def __post_init__(self) -> None:
        if self.event.event_id != self.occurrence.event_id:
            raise ValueError("ingress admission must preserve the occurrence Event Identity")
        if self.event.version_id != self.occurrence.event_version_id:
            raise ValueError("ingress admission must preserve the occurrence Event Version Identity")
        if self.event.occurred_at != self.occurrence.occurred_at:
            raise ValueError("ingress Event must preserve external occurrence time")
        if self.event.recorded_at != self.first_recorded_at:
            raise ValueError("ingress Event must preserve first canonical recording time")
        if self.event.record.authority_mode is not AuthorityMode.NATIVE:
            raise ValueError("P8.05 ingress Event is Native evidence of Arvectum OS admission")
        if self.occurrence.authority_mode is AuthorityMode.NATIVE:
            raise ValueError("underlying external occurrence authority must remain external")


@dataclass(frozen=True, slots=True)
class ExternalIngressState:
    """Append-only canonical admissions plus non-canonical delivery evidence."""

    admissions: tuple[ExternalIngressAdmission, ...] = ()
    deliveries: tuple[ExternalDelivery, ...] = ()

    def __post_init__(self) -> None:
        occurrence_keys = tuple(item.occurrence.occurrence_key for item in self.admissions)
        if len(set(occurrence_keys)) != len(occurrence_keys):
            raise ValueError("external ingress state cannot contain duplicate occurrence admissions")
        event_ids = tuple(item.event.event_id for item in self.admissions)
        if len(set(event_ids)) != len(event_ids):
            raise ValueError("external ingress state cannot contain duplicate canonical Event identities")
        delivery_ids = tuple(item.delivery_id for item in self.deliveries)
        if len(set(delivery_ids)) != len(delivery_ids):
            raise ValueError("external ingress state cannot contain duplicate delivery identities")

    @property
    def canonical_events(self) -> tuple[CanonicalEvent, ...]:
        return tuple(item.event for item in self.admissions)


@dataclass(frozen=True, slots=True)
class ExternalIngressResult:
    state: ExternalIngressState
    admission: ExternalIngressAdmission
    duplicate_delivery: bool


@dataclass(frozen=True, slots=True)
class ExternalReconciliation:
    """Append-only evidence resolving or preserving one uncertain external outcome."""

    reconciliation_id: Identity
    version_id: Identity
    organization: OrganizationScope
    uncertain_attempt_fingerprint: tuple[str, ...]
    uncertain_retry_token: str
    original_execution_subject_id: Identity
    original_execution_version_id: Identity
    reconciliation_execution_subject_id: Identity
    reconciliation_execution_version_id: Identity
    evidence_ref: Identity
    resolution: ReconciliationResolution
    resolved_at: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.reconciliation_id, Identity) or not isinstance(self.version_id, Identity):
            raise ValueError("reconciliation Subject/Version identities must be explicit")
        if self.reconciliation_id == self.version_id:
            raise ValueError("reconciliation Subject and Version identities must remain distinct")
        if not isinstance(self.organization, OrganizationScope):
            raise ValueError("reconciliation Organization scope must be explicit")
        scope = self.organization.organization_id.value
        scoped = (
            self.reconciliation_id,
            self.version_id,
            self.original_execution_subject_id,
            self.original_execution_version_id,
            self.reconciliation_execution_subject_id,
            self.reconciliation_execution_version_id,
            self.evidence_ref,
        )
        if any(not isinstance(ref, Identity) for ref in scoped):
            raise ValueError("reconciliation references must be Identity values")
        if any(ref.scope != scope for ref in scoped):
            raise ValueError("reconciliation governed references must share Organization scope")
        if not isinstance(self.uncertain_attempt_fingerprint, tuple) or not self.uncertain_attempt_fingerprint:
            raise ValueError("reconciliation must pin the exact uncertain attempt fingerprint")
        if not isinstance(self.uncertain_retry_token, str) or not self.uncertain_retry_token.strip():
            raise ValueError("reconciliation must pin the uncertain attempt retry token")
        if self.reconciliation_execution_subject_id == self.original_execution_subject_id:
            raise ValueError("P8.05 reconciliation uses a distinct governed Execution Identity")
        if not isinstance(self.resolution, ReconciliationResolution):
            raise ValueError("reconciliation resolution must be explicit")
        _require_aware(self.resolved_at, label="reconciliation resolved_at")


@dataclass(frozen=True, slots=True)
class ReconciledRetryLink:
    """Causation evidence from an uncertain attempt through reconciliation to retry."""

    original_attempt_fingerprint: tuple[str, ...]
    reconciliation_id: Identity
    retry_attempt_fingerprint: tuple[str, ...]
    retry_execution_subject_id: Identity
    retry_execution_version_id: Identity


@dataclass(frozen=True, slots=True)
class ExternalEffectLedger:
    """P2.06 attempt state plus append-only reconciliation/retry lineage."""

    runtime_state: RuntimeConsistencyState
    reconciliations: tuple[ExternalReconciliation, ...] = ()
    retry_links: tuple[ReconciledRetryLink, ...] = ()


@dataclass(frozen=True, slots=True)
class ExternalBoundaryReplayManifest:
    """Pure reconstruction output.  It deliberately has no transport/effect hook."""

    ingress_event_ids: tuple[Identity, ...]
    ingress_delivery_ids: tuple[Identity, ...]
    egress_attempt_fingerprints: tuple[tuple[str, ...], ...]
    egress_outcomes: tuple[ConsequentialOutcome, ...]
    reconciliation_ids: tuple[Identity, ...]
    retry_links: tuple[ReconciledRetryLink, ...]
    live_retrievals_executed: bool = False
    external_effects_executed: bool = False


def _require_aware(value: datetime, *, label: str) -> None:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{label} must be timezone-aware")


def _ordered_unique(*groups: tuple[Identity, ...]) -> tuple[Identity, ...]:
    result: list[Identity] = []
    seen: set[Identity] = set()
    for group in groups:
        for ref in group:
            if not isinstance(ref, Identity):
                raise ValueError("provenance references must be Identity values")
            if ref not in seen:
                result.append(ref)
                seen.add(ref)
    return tuple(result)


def _same_delivery(left: ExternalDelivery, right: ExternalDelivery) -> bool:
    return left == right


def admit_external_ingress(
    *,
    state: ExternalIngressState,
    delivery: ExternalDelivery,
    execution: GovernedExecutionContext,
    related_records: tuple[CanonicalRecord, ...] = (),
) -> ExternalIngressResult:
    """Explicitly admit one external occurrence or recognize duplicate delivery.

    Delivery is evaluated before P2.05 canonical Event admission.  A later
    delivery may have a different delivery identity and recording time; it does
    not rewrite the first admitted canonical Event.
    """

    if not isinstance(state, ExternalIngressState):
        raise ValueError("state must be ExternalIngressState")
    if not isinstance(delivery, ExternalDelivery):
        raise ValueError("delivery must be ExternalDelivery")
    if not isinstance(execution, GovernedExecutionContext):
        raise ValueError("ingress admission requires a GovernedExecutionContext")
    occurrence = delivery.occurrence
    if execution.organization != occurrence.organization:
        raise ValueError("external occurrence and admission execution must share Organization scope")
    if not isinstance(related_records, tuple) or any(
        not isinstance(record, CanonicalRecord) for record in related_records
    ):
        raise ValueError("related_records must be immutable CanonicalRecord versions")
    if any(record.organization != occurrence.organization for record in related_records):
        raise ValueError("external ingress related records must share Organization scope")

    same_delivery_id = tuple(item for item in state.deliveries if item.delivery_id == delivery.delivery_id)
    if same_delivery_id:
        existing_delivery = same_delivery_id[0]
        if not _same_delivery(existing_delivery, delivery):
            raise ExternalDeliveryConflictError(
                "delivery identity was already bound to materially different transport evidence"
            )
        existing_admission = next(
            (
                item
                for item in state.admissions
                if item.occurrence.occurrence_key == occurrence.occurrence_key
            ),
            None,
        )
        if existing_admission is None:
            raise ExternalBoundaryError("delivery evidence exists without its canonical occurrence admission")
        return ExternalIngressResult(
            state=state,
            admission=existing_admission,
            duplicate_delivery=True,
        )

    same_occurrence = tuple(
        item for item in state.admissions if item.occurrence.occurrence_key == occurrence.occurrence_key
    )
    if same_occurrence:
        existing = same_occurrence[0]
        if existing.occurrence != occurrence:
            raise ExternalOccurrenceConflictError(
                "same external occurrence identity was presented with materially different immutable evidence"
            )
        return ExternalIngressResult(
            state=ExternalIngressState(
                admissions=state.admissions,
                deliveries=(*state.deliveries, delivery),
            ),
            admission=existing,
            duplicate_delivery=True,
        )

    if any(item.event.event_id == occurrence.event_id for item in state.admissions):
        raise ExternalOccurrenceConflictError(
            "canonical Event Identity is already bound to a different external occurrence"
        )
    if any(item.event.version_id == occurrence.event_version_id for item in state.admissions):
        raise ExternalOccurrenceConflictError(
            "canonical Event Version Identity is already bound to a different external occurrence"
        )

    producer_id = execution.record.creation_actor.actual_principal.principal_id
    related_subjects = tuple(record.subject_id for record in related_records)
    related_versions = tuple(record.version_id for record in related_records)
    provenance = _ordered_unique(
        (
            producer_id,
            execution.execution_subject_id,
            execution.execution_version_id,
        ),
        related_subjects,
        related_versions,
        occurrence.governed_provenance_refs,
    )
    receipt = EventReceipt(
        event_id=occurrence.event_id,
        version_id=occurrence.event_version_id,
        event_type="platform.external-occurrence.observed",
        event_schema_version="p8.05-v1",
        organization=occurrence.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.event/external-ingress-observation",
        authoritative_source="Arvectum OS",
        occurred_at=occurrence.occurred_at,
        recorded_at=delivery.received_at,
        producer_id=producer_id,
        initiating_actor_id=producer_id,
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        related_subject_ids=related_subjects,
        related_version_ids=related_versions,
        correlation_refs=(execution.execution_subject_id,),
        causation_refs=(execution.execution_version_id,),
        classification="restricted-pilot",
        access_scope="organization",
        provenance_refs=provenance,
        integrity_metadata=(
            ("external_payload_integrity_ref", occurrence.payload_integrity_ref),
            ("source_version_ref", occurrence.source_version_ref),
        ),
        payload=(
            ("source_system", occurrence.source_system),
            ("source_object_ref", occurrence.source_object_ref),
            ("source_occurrence_id", occurrence.source_occurrence_id),
            ("source_authority_mode", occurrence.authority_mode.value),
            ("source_authority_scope", occurrence.authority_scope),
        ),
    )
    admission = admit_event(
        receipt=receipt,
        execution=execution,
        related_records=related_records,
        admitted_events=state.canonical_events,
    )
    if admission.duplicate_delivery:
        raise ExternalBoundaryError(
            "new external occurrence unexpectedly collided with already-admitted canonical Event"
        )
    bound = ExternalIngressAdmission(
        occurrence=occurrence,
        event=admission.event,
        first_delivery_id=delivery.delivery_id,
        first_recorded_at=delivery.received_at,
    )
    return ExternalIngressResult(
        state=ExternalIngressState(
            admissions=(*state.admissions, bound),
            deliveries=(*state.deliveries, delivery),
        ),
        admission=bound,
        duplicate_delivery=False,
    )


def record_external_effect_outcome(
    *,
    ledger: ExternalEffectLedger,
    execution: GovernedExecutionContext,
    side_effect_class: OperationSideEffectClass,
    effect_descriptor: tuple[tuple[str, str], ...],
    retry_semantics: RetrySemantics,
    reported_outcome: ConsequentialOutcome,
    retry_token: str | None = None,
) -> tuple[ExternalEffectLedger, ExternalAttemptResult]:
    """Record P2.06 egress outcome semantics without performing the external effect."""

    result = record_external_consequence_attempt(
        state=ledger.runtime_state,
        execution=execution,
        side_effect_class=side_effect_class,
        effect_descriptor=effect_descriptor,
        retry_semantics=retry_semantics,
        reported_outcome=reported_outcome,
        retry_token=retry_token,
    )
    return (
        ExternalEffectLedger(
            runtime_state=result.state,
            reconciliations=ledger.reconciliations,
            retry_links=ledger.retry_links,
        ),
        result,
    )


def reconcile_uncertain_external_effect(
    *,
    ledger: ExternalEffectLedger,
    uncertain_attempt: ConsequentialAttempt,
    reconciliation_execution: GovernedExecutionContext,
    reconciliation_id: Identity,
    version_id: Identity,
    evidence_ref: Identity,
    resolution: ReconciliationResolution,
    resolved_at: datetime,
) -> ExternalEffectLedger:
    """Append one attributable reconciliation; never rewrite the uncertain attempt."""

    if uncertain_attempt not in ledger.runtime_state.attempts:
        raise ValueError("reconciliation target attempt must exist in the retained runtime history")
    if uncertain_attempt.outcome is not ConsequentialOutcome.UNCERTAIN:
        raise ValueError("reconciliation target must be an uncertain external attempt")
    if uncertain_attempt.side_effect_class not in {
        OperationSideEffectClass.EXTERNAL_MUTATION,
        OperationSideEffectClass.COMMITMENT,
    }:
        raise ValueError("reconciliation target must represent an external consequence")
    if not uncertain_attempt.retry_token:
        raise ValueError("P8.05 reconciliation target requires explicit duplicate-protection token")
    if not isinstance(reconciliation_execution, GovernedExecutionContext):
        raise ValueError("reconciliation requires an attributable GovernedExecutionContext")
    if reconciliation_execution.organization != ledger.runtime_state.head.organization:
        raise ValueError("reconciliation must remain inside the same Organization")
    record = ExternalReconciliation(
        reconciliation_id=reconciliation_id,
        version_id=version_id,
        organization=reconciliation_execution.organization,
        uncertain_attempt_fingerprint=uncertain_attempt.fingerprint,
        uncertain_retry_token=uncertain_attempt.retry_token,
        original_execution_subject_id=uncertain_attempt.execution_subject_id,
        original_execution_version_id=uncertain_attempt.execution_version_id,
        reconciliation_execution_subject_id=reconciliation_execution.execution_subject_id,
        reconciliation_execution_version_id=reconciliation_execution.execution_version_id,
        evidence_ref=evidence_ref,
        resolution=resolution,
        resolved_at=resolved_at,
    )
    if any(item.reconciliation_id == record.reconciliation_id for item in ledger.reconciliations):
        raise ValueError("reconciliation identity must be non-recycled")
    return ExternalEffectLedger(
        runtime_state=ledger.runtime_state,
        reconciliations=(*ledger.reconciliations, record),
        retry_links=ledger.retry_links,
    )


def latest_reconciliation_for(
    ledger: ExternalEffectLedger,
    uncertain_attempt: ConsequentialAttempt,
) -> ExternalReconciliation | None:
    matches = tuple(
        item
        for item in ledger.reconciliations
        if item.uncertain_attempt_fingerprint == uncertain_attempt.fingerprint
        and item.uncertain_retry_token == uncertain_attempt.retry_token
    )
    return matches[-1] if matches else None


def require_retry_allowed_after_reconciliation(
    ledger: ExternalEffectLedger,
    uncertain_attempt: ConsequentialAttempt,
) -> ExternalReconciliation:
    """Fail closed unless reconciliation confirms that the prior effect was not applied."""

    reconciliation = latest_reconciliation_for(ledger, uncertain_attempt)
    if reconciliation is None:
        raise ReconciliationRequiredError(
            "uncertain external outcome requires attributable reconciliation before retry"
        )
    if reconciliation.resolution is ReconciliationResolution.STILL_UNCERTAIN:
        raise ReconciliationRequiredError(
            "reconciliation remains uncertain; retry is still prohibited"
        )
    if reconciliation.resolution is ReconciliationResolution.CONFIRMED_SUCCEEDED:
        raise RetryAfterReconciliationNotAllowedError(
            "reconciliation confirmed prior effect succeeded; a duplicate retry is prohibited"
        )
    return reconciliation


def record_retry_after_reconciliation(
    *,
    ledger: ExternalEffectLedger,
    uncertain_attempt: ConsequentialAttempt,
    retry_execution: GovernedExecutionContext,
    side_effect_class: OperationSideEffectClass,
    effect_descriptor: tuple[tuple[str, str], ...],
    retry_semantics: RetrySemantics,
    retry_token: str,
    reported_outcome: ConsequentialOutcome,
) -> tuple[ExternalEffectLedger, ExternalAttemptResult]:
    """Record a new governed retry only after ConfirmedNotApplied reconciliation."""

    reconciliation = require_retry_allowed_after_reconciliation(ledger, uncertain_attempt)
    if retry_execution.organization != ledger.runtime_state.head.organization:
        raise ValueError("retry execution must remain inside the same Organization")
    if retry_execution.execution_subject_id == uncertain_attempt.execution_subject_id:
        raise ValueError("post-reconciliation retry must use a new Governed Execution Identity")
    if retry_token == uncertain_attempt.retry_token:
        raise ValueError("new governed retry uses a new duplicate-protection token")
    next_ledger, result = record_external_effect_outcome(
        ledger=ledger,
        execution=retry_execution,
        side_effect_class=side_effect_class,
        effect_descriptor=effect_descriptor,
        retry_semantics=retry_semantics,
        reported_outcome=reported_outcome,
        retry_token=retry_token,
    )
    link = ReconciledRetryLink(
        original_attempt_fingerprint=uncertain_attempt.fingerprint,
        reconciliation_id=reconciliation.reconciliation_id,
        retry_attempt_fingerprint=result.attempt.fingerprint,
        retry_execution_subject_id=retry_execution.execution_subject_id,
        retry_execution_version_id=retry_execution.execution_version_id,
    )
    return (
        ExternalEffectLedger(
            runtime_state=next_ledger.runtime_state,
            reconciliations=next_ledger.reconciliations,
            retry_links=(*next_ledger.retry_links, link),
        ),
        result,
    )


def build_external_effect_outcome_event_receipt(
    *,
    attempt: ConsequentialAttempt,
    execution: GovernedExecutionContext,
    event_id: Identity,
    version_id: Identity,
    source_system: str,
    effect_ref: str,
    recorded_at: datetime,
    causation_refs: tuple[Identity, ...] = (),
) -> EventReceipt:
    """Build Native Event evidence that reports exactly the known egress outcome."""

    if attempt.execution_subject_id != execution.execution_subject_id:
        raise ValueError("effect outcome Event must link to the exact attempt Execution Identity")
    if attempt.execution_version_id != execution.execution_version_id:
        raise ValueError("effect outcome Event must link to the exact attempt Execution version")
    _require_aware(recorded_at, label="effect outcome recorded_at")
    producer_id = execution.record.creation_actor.actual_principal.principal_id
    provenance = _ordered_unique(
        (
            producer_id,
            execution.execution_subject_id,
            execution.execution_version_id,
        ),
    )
    return EventReceipt(
        event_id=event_id,
        version_id=version_id,
        event_type="platform.external-effect.outcome",
        event_schema_version="p8.05-v1",
        organization=execution.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.event/external-effect-outcome",
        authoritative_source="Arvectum OS",
        occurred_at=recorded_at,
        recorded_at=recorded_at,
        producer_id=producer_id,
        initiating_actor_id=producer_id,
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        related_subject_ids=(),
        related_version_ids=(),
        correlation_refs=(execution.execution_subject_id,),
        causation_refs=_ordered_unique((execution.execution_version_id,), causation_refs),
        classification="restricted-pilot",
        access_scope="organization",
        provenance_refs=provenance,
        integrity_metadata=(("effect_fingerprint", repr(attempt.fingerprint)),),
        payload=(
            ("source_system", source_system),
            ("effect_ref", effect_ref),
            ("outcome", attempt.outcome.value),
            ("retry_token", attempt.retry_token or ""),
        ),
    )


def reconstruct_external_boundary(
    *,
    ingress_state: ExternalIngressState,
    effect_ledger: ExternalEffectLedger,
) -> ExternalBoundaryReplayManifest:
    """Reconstruct retained boundary history without any external retrieval/effect."""

    return ExternalBoundaryReplayManifest(
        ingress_event_ids=tuple(item.event.event_id for item in ingress_state.admissions),
        ingress_delivery_ids=tuple(item.delivery_id for item in ingress_state.deliveries),
        egress_attempt_fingerprints=tuple(
            item.fingerprint for item in effect_ledger.runtime_state.attempts
        ),
        egress_outcomes=tuple(item.outcome for item in effect_ledger.runtime_state.attempts),
        reconciliation_ids=tuple(item.reconciliation_id for item in effect_ledger.reconciliations),
        retry_links=effect_ledger.retry_links,
    )
