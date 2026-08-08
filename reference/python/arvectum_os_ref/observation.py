"""P1.09 — Observation creation without Knowledge promotion.

The bounded reference slice turns the already-governed P1.06/P1.07 outcome and
P1.08 reconstruction evidence into one significant RFC-0007 Observation.
Because the Observation is retained as governed learning evidence, its
representation reuses the RFC-0002 Canonical Record envelope; Observation does
not become a sixth Kernel primitive.

This module deliberately does not implement Organizational Memory, a Knowledge
Candidate, Knowledge admission, an Improvement Proposal, standard/workflow
change, or production self-modification. An Observation remains unvalidated and
cannot be used as validated Knowledge without a separate explicit RFC-0007
promotion path.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NoReturn

from .canonical import AuthorityMode, CanonicalRecord
from .events import CanonicalEvent
from .execution import GovernedVersionPin
from .identity import Identity
from .mutation import CanonicalMutationResult
from .provenance import ReconstructionEvidence


class ObservationCreationError(ValueError):
    """Supplied governed evidence cannot create the bounded Observation."""


class KnowledgePromotionRequiredError(RuntimeError):
    """Validated Knowledge reliance was attempted without explicit promotion."""


class ObservationEpistemicStatus(str, Enum):
    """Bounded epistemic state required by the P1.09 fitness scenario."""

    UNVALIDATED = "Unvalidated"


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ObservationCreationError(message)


def _ordered_unique(refs: tuple[Identity, ...]) -> tuple[Identity, ...]:
    seen: set[Identity] = set()
    ordered: list[Identity] = []
    for ref in refs:
        if ref not in seen:
            seen.add(ref)
            ordered.append(ref)
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class Observation:
    """One retained, explicitly unvalidated Observation Canonical Record."""

    record: CanonicalRecord
    epistemic_status: ObservationEpistemicStatus
    source_event: GovernedVersionPin
    source_execution: GovernedVersionPin
    observed_effect: GovernedVersionPin
    evidence_refs: tuple[Identity, ...]

    def __post_init__(self) -> None:
        _require(isinstance(self.record, CanonicalRecord), "Observation must use a CanonicalRecord envelope")
        _require(
            self.record.semantic_type == "platform.observation",
            "P1.09 Observation semantic_type must be platform.observation",
        )
        _require(
            self.record.schema_version == "1",
            "P1.09 Observation schema version must be explicit and supported",
        )
        _require(
            self.record.authority_mode is AuthorityMode.NATIVE,
            "P1.09 Observation records only Arvectum OS organizational observation state",
        )
        _require(
            self.record.authority_scope == "platform.learning/observation",
            "Observation authority scope must remain limited to the recorded observation",
        )
        _require(
            self.record.lifecycle_status == "Captured",
            "P1.09 Observation lifecycle status must be Captured",
        )
        _require(
            self.record.predecessor_version_id is None,
            "the bounded P1.09 Observation starts as one immutable initial version",
        )
        _require(
            self.epistemic_status is ObservationEpistemicStatus.UNVALIDATED,
            "an Observation must remain explicitly unvalidated",
        )
        for label, pin in (
            ("source Event", self.source_event),
            ("source Execution", self.source_execution),
            ("observed canonical effect", self.observed_effect),
        ):
            _require(isinstance(pin, GovernedVersionPin), f"Observation {label} must be version-pinned")
        _require(
            isinstance(self.evidence_refs, tuple)
            and bool(self.evidence_refs)
            and all(isinstance(ref, Identity) for ref in self.evidence_refs),
            "Observation evidence references must be explicit Identity values",
        )
        _require(
            len(set(self.evidence_refs)) == len(self.evidence_refs),
            "Observation evidence references must be de-duplicated",
        )

        required_refs = {
            self.source_event.subject_id,
            self.source_event.version_id,
            self.source_execution.subject_id,
            self.source_execution.version_id,
            self.observed_effect.subject_id,
            self.observed_effect.version_id,
        }
        _require(
            required_refs.issubset(set(self.record.provenance_refs)),
            "Observation provenance must pin Event, Execution and observed effect versions",
        )
        _require(
            set(self.evidence_refs).issubset(set(self.record.provenance_refs)),
            "Observation canonical provenance must preserve supplied reconstruction evidence",
        )

        organization_scope = self.record.organization.organization_id.value
        governed_refs = (
            self.record.subject_id,
            self.record.version_id,
            self.source_event.subject_id,
            self.source_event.version_id,
            self.source_execution.subject_id,
            self.source_execution.version_id,
            self.observed_effect.subject_id,
            self.observed_effect.version_id,
        )
        _require(
            all(ref.scope == organization_scope for ref in governed_refs),
            "Observation and version-pinned governed sources must share Organization scope",
        )
        _require(
            ("epistemic-status", ObservationEpistemicStatus.UNVALIDATED.value)
            in self.record.integrity_metadata,
            "Observation envelope must preserve explicit unvalidated epistemic status",
        )

    @property
    def observation_id(self) -> Identity:
        return self.record.subject_id

    @property
    def version_id(self) -> Identity:
        return self.record.version_id


def build_p1_09_observation(
    *,
    evidence: ReconstructionEvidence,
    event: CanonicalEvent,
    mutation: CanonicalMutationResult,
) -> Observation:
    """Create one significant Observation from exact P1.06–P1.08 evidence.

    Creation is a bounded governed capture step only. It does not validate the
    observed assertion, admit Knowledge, create an Improvement Proposal, alter
    an approved standard/workflow, or change production behavior.
    """

    _require(
        isinstance(evidence, ReconstructionEvidence),
        "P1.09 requires exact P1.08 ReconstructionEvidence",
    )
    _require(isinstance(event, CanonicalEvent), "P1.09 requires the exact admitted P1.07 Event")
    _require(
        isinstance(mutation, CanonicalMutationResult),
        "P1.09 requires the exact P1.06 CanonicalMutationResult",
    )

    terminal_execution = mutation.execution
    result = mutation.resulting_record
    organization = evidence.organization
    _require(
        event.record.organization == organization
        and terminal_execution.record.organization == organization
        and result.organization == organization,
        "Observation sources must share the reconstruction Organization scope",
    )

    event_pin = GovernedVersionPin.from_record(event.record)
    execution_pin = GovernedVersionPin.from_record(terminal_execution.record)
    effect_pin = GovernedVersionPin.from_record(result)
    _require(
        evidence.events == (event_pin,),
        "Observation must use the exact Event version verified by P1.08",
    )
    _require(
        evidence.execution_versions[-1] == execution_pin,
        "Observation must use the exact terminal Execution version verified by P1.08",
    )
    _require(
        evidence.canonical_effects == (effect_pin,),
        "Observation must use the exact canonical effect verified by P1.08",
    )
    _require(
        evidence.operation_name == terminal_execution.operation_name,
        "Observation operation must match the reconstructed execution outcome",
    )
    _require(
        evidence.event_type == event.event_type
        and evidence.event_schema_version == event.event_schema_version,
        "Observation must preserve the reconstructed Event type/schema semantics",
    )
    _require(
        event.execution_subject_id == execution_pin.subject_id
        and event.execution_version_id == execution_pin.version_id,
        "Observation Event must reference the exact terminal Execution version",
    )
    _require(
        event.related_subject_ids == (effect_pin.subject_id,)
        and event.related_version_ids == (effect_pin.version_id,),
        "Observation Event must reference the exact observed canonical effect",
    )

    actor = terminal_execution.initiating_actor
    actor_id = actor.actual_principal.principal_id
    _require(
        evidence.initiating_actor_id == actor_id
        and event.initiating_actor_id == actor_id
        and event.producer_id == actor_id,
        "Observation attribution must preserve the reconstructed initiating Principal",
    )
    _require(
        actor.organization == organization,
        "Observation creation Actor must share Organization scope",
    )

    required_evidence = {
        event_pin.subject_id,
        event_pin.version_id,
        execution_pin.subject_id,
        execution_pin.version_id,
        effect_pin.subject_id,
        effect_pin.version_id,
    }
    _require(
        required_evidence.issubset(set(evidence.provenance_refs)),
        "P1.08 evidence is incomplete for Observation creation",
    )

    scope = organization.organization_id.value
    evidence_refs = _ordered_unique(evidence.provenance_refs)
    provenance_refs = _ordered_unique(
        (
            actor_id,
            *evidence_refs,
            event_pin.subject_id,
            event_pin.version_id,
            execution_pin.subject_id,
            execution_pin.version_id,
            effect_pin.subject_id,
            effect_pin.version_id,
        )
    )
    record = CanonicalRecord(
        subject_id=Identity(
            "observation-subject",
            "reference-subject-maintenance-execution-1-outcome",
            scope,
        ),
        version_id=Identity(
            "observation-version",
            "reference-subject-maintenance-execution-1-outcome-v1",
            scope,
        ),
        semantic_type="platform.observation",
        schema_version="1",
        organization=organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope="platform.learning/observation",
        accountable_owner_id=terminal_execution.record.accountable_owner_id,
        creation_actor=actor,
        created_at=datetime.fromisoformat("2026-08-08T05:05:00+00:00"),
        provenance_refs=provenance_refs,
        integrity_metadata=(
            ("representation", "frozen-in-memory-reference"),
            ("epistemic-status", ObservationEpistemicStatus.UNVALIDATED.value),
            ("knowledge-promotion", "not-performed"),
        ),
        payload=(
            ("operation", terminal_execution.operation_name),
            ("observed-outcome", terminal_execution.record.lifecycle_status or ""),
            ("source-event-type", event.event_type),
        ),
        lifecycle_status="Captured",
        predecessor_version_id=None,
    )
    return Observation(
        record=record,
        epistemic_status=ObservationEpistemicStatus.UNVALIDATED,
        source_event=event_pin,
        source_execution=execution_pin,
        observed_effect=effect_pin,
        evidence_refs=evidence_refs,
    )


def require_explicit_knowledge_promotion(observation: Observation) -> NoReturn:
    """Negative-path guard proving Observation is not validated Knowledge.

    P1.09 intentionally has no successful Knowledge-admission path. A later
    implementation may add the explicit RFC-0007 candidate/validation/approval
    lifecycle, but callers cannot reinterpret this Observation as Knowledge in
    the meantime.
    """

    if not isinstance(observation, Observation):
        raise TypeError("knowledge-promotion guard requires an Observation")
    raise KnowledgePromotionRequiredError(
        "Observation is not validated Knowledge; explicit RFC-0007 promotion is required before Knowledge reliance"
    )
