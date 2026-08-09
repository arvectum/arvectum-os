"""P5.07 — bounded Event/provenance/portability integration support.

This module adds the smallest integration-facing evidence helper justified by the
Phase 5 J2 path. It consumes an already R14-hardened ``IntegrationCompositionFacade``
and delegates canonical Event admission to the existing P2.05 Event/provenance
semantic owner.

The helper preserves exact Organization, Actor, Product, Product Contract,
Execution and immutable Version context. It also exposes two derived views:

* a non-authoritative telemetry projection; and
* a non-canonical portable semantic fixture containing explicit identity roles and
  semantic links rather than a vendor/storage/serialization representation.

Neither derived view is authority, permission, Organizational Authority, approval,
validated knowledge, a Canonical Record or a Typed Relationship. The module does
not select a broker, event store, tracing backend, export endpoint, JSON/wire
format, schema registry, package boundary, freshness registry or durable storage.
Its current Python shape is internal/provisional reference evidence only.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final

from .canonical import AuthorityMode, CanonicalRecord
from .event_provenance import (
    CanonicalEvent,
    EventAdmissionResult,
    EventReceipt,
    admit_event,
)
from .execution import GovernedVersionPin
from .governed_execution import GovernedExecutionContext
from .identity import Identity
from .integration_composition import IntegrationCompositionFacade
from .security import ActorContext, OrganizationScope


TELEMETRY_AUTHORITY_STATUS: Final = "derived-non-authoritative"
PORTABLE_FIXTURE_AUTHORITY_STATUS: Final = "derived-non-canonical"
INTEGRATION_EVENT_AUTHORITY_SCOPE: Final = "platform.event/integration-governed-action"


class IntegrationEvidenceError(RuntimeError):
    """Supplied integration evidence cannot preserve the exact governed context."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise IntegrationEvidenceError(message)


def _ordered_unique(*groups: tuple[Identity, ...]) -> tuple[Identity, ...]:
    result: list[Identity] = []
    seen: set[Identity] = set()
    for group in groups:
        for identity in group:
            if not isinstance(identity, Identity):
                raise ValueError("integration provenance references must be Identity values")
            if identity not in seen:
                result.append(identity)
                seen.add(identity)
    return tuple(result)


def _actor_refs(actor: ActorContext) -> tuple[Identity, ...]:
    refs = [actor.actual_principal.principal_id]
    if actor.represented_principal is not None:
        refs.append(actor.represented_principal.principal_id)
    refs.extend(actor.authentication_evidence_refs)
    return _ordered_unique(tuple(refs))


@dataclass(frozen=True, slots=True)
class PortableSemanticLink:
    """One derived semantic link used only by the portable fixture.

    The link deliberately does not claim to be an RFC-0002 Canonical Typed
    Relationship. It preserves relationship meaning for migration/inspection
    without minting new canonical organizational state.
    """

    kind: str
    source_role: str
    source_id: Identity
    target_role: str
    target_id: Identity
    canonical_typed_relationship: bool = False

    def __post_init__(self) -> None:
        for label in ("kind", "source_role", "target_role"):
            value = getattr(self, label)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"portable semantic link {label} must be explicit")
        if not isinstance(self.source_id, Identity) or not isinstance(self.target_id, Identity):
            raise ValueError("portable semantic link endpoints must be Identity values")
        if self.canonical_typed_relationship is not False:
            raise ValueError("P5.07 portable links are derived and must not claim canonical relationship authority")


@dataclass(frozen=True, slots=True)
class IntegrationTelemetryProjection:
    """Derived operational projection for inspection/telemetry only."""

    authority_status: str
    organization: OrganizationScope
    actual_actor_id: Identity
    represented_actor_id: Identity | None
    product_id: Identity
    product_version: str
    product_contract: GovernedVersionPin
    execution: GovernedVersionPin
    event: GovernedVersionPin
    event_type: str
    event_schema_version: str
    correlation_refs: tuple[Identity, ...]
    causation_refs: tuple[Identity, ...]

    def __post_init__(self) -> None:
        _require(
            self.authority_status == TELEMETRY_AUTHORITY_STATUS,
            "integration telemetry must remain explicitly non-authoritative",
        )
        _require(isinstance(self.organization, OrganizationScope), "telemetry Organization scope must be explicit")
        _require(isinstance(self.actual_actor_id, Identity), "telemetry actor attribution must be explicit")
        _require(
            self.represented_actor_id is None or isinstance(self.represented_actor_id, Identity),
            "telemetry represented actor must be an Identity when supplied",
        )
        _require(isinstance(self.product_id, Identity), "telemetry product identity must be explicit")
        _require(
            isinstance(self.product_version, str) and bool(self.product_version.strip()),
            "telemetry product version must be explicit",
        )
        for label, pin in (
            ("Product Contract", self.product_contract),
            ("Execution", self.execution),
            ("Event", self.event),
        ):
            _require(isinstance(pin, GovernedVersionPin), f"telemetry {label} must be version-pinned")
        for label in ("event_type", "event_schema_version"):
            value = getattr(self, label)
            _require(isinstance(value, str) and bool(value.strip()), f"telemetry {label} must be explicit")
        for label, refs in (("correlation", self.correlation_refs), ("causation", self.causation_refs)):
            _require(
                isinstance(refs, tuple) and bool(refs) and all(isinstance(ref, Identity) for ref in refs),
                f"telemetry {label} references must be explicit",
            )


@dataclass(frozen=True, slots=True)
class IntegrationPortableSemanticFixture:
    """Derived portable semantic state without a durable serialization contract."""

    authority_status: str
    organization: OrganizationScope
    actual_actor_id: Identity
    represented_actor_id: Identity | None
    product_id: Identity
    product_version: str
    product_contract: GovernedVersionPin
    execution: GovernedVersionPin
    event: GovernedVersionPin
    event_type: str
    event_schema_version: str
    provenance_refs: tuple[Identity, ...]
    semantic_links: tuple[PortableSemanticLink, ...]

    def __post_init__(self) -> None:
        _require(
            self.authority_status == PORTABLE_FIXTURE_AUTHORITY_STATUS,
            "portable integration fixture must remain explicitly non-canonical",
        )
        _require(isinstance(self.organization, OrganizationScope), "portable fixture Organization must be explicit")
        _require(isinstance(self.actual_actor_id, Identity), "portable fixture actor must be explicit")
        _require(
            self.represented_actor_id is None or isinstance(self.represented_actor_id, Identity),
            "portable fixture represented actor must be an Identity when supplied",
        )
        _require(isinstance(self.product_id, Identity), "portable fixture product identity must be explicit")
        _require(
            isinstance(self.product_version, str) and bool(self.product_version.strip()),
            "portable fixture product version must be explicit",
        )
        for label, pin in (
            ("Product Contract", self.product_contract),
            ("Execution", self.execution),
            ("Event", self.event),
        ):
            _require(isinstance(pin, GovernedVersionPin), f"portable fixture {label} must be version-pinned")
        for label in ("event_type", "event_schema_version"):
            value = getattr(self, label)
            _require(isinstance(value, str) and bool(value.strip()), f"portable fixture {label} must be explicit")
        _require(
            isinstance(self.provenance_refs, tuple)
            and bool(self.provenance_refs)
            and all(isinstance(ref, Identity) for ref in self.provenance_refs),
            "portable fixture provenance must preserve explicit Identity references",
        )
        _require(
            len(set(self.provenance_refs)) == len(self.provenance_refs),
            "portable fixture provenance references must be de-duplicated",
        )
        _require(
            isinstance(self.semantic_links, tuple)
            and bool(self.semantic_links)
            and all(isinstance(link, PortableSemanticLink) for link in self.semantic_links),
            "portable fixture semantic links must be explicit",
        )


@dataclass(frozen=True, slots=True)
class IntegrationEventSupportResult:
    """Canonical Event admission plus two explicitly derived integration views."""

    admission: EventAdmissionResult
    telemetry: IntegrationTelemetryProjection
    portable_fixture: IntegrationPortableSemanticFixture

    def __post_init__(self) -> None:
        _require(isinstance(self.admission, EventAdmissionResult), "P5.07 result must preserve Event admission evidence")
        _require(
            isinstance(self.telemetry, IntegrationTelemetryProjection),
            "P5.07 result must expose non-authoritative telemetry",
        )
        _require(
            isinstance(self.portable_fixture, IntegrationPortableSemanticFixture),
            "P5.07 result must expose portable semantic state",
        )
        _require(
            self.telemetry.event == self.admission.event.version_pin
            and self.portable_fixture.event == self.admission.event.version_pin,
            "derived P5.07 evidence must point to the exact admitted Event version",
        )


def _validate_facade_execution_continuity(
    *,
    facade: IntegrationCompositionFacade,
    execution: GovernedExecutionContext,
) -> None:
    if not isinstance(facade, IntegrationCompositionFacade):
        raise TypeError("P5.07 integration support requires an R14-hardened IntegrationCompositionFacade")
    if not isinstance(execution, GovernedExecutionContext):
        raise TypeError("P5.07 integration support requires an exact GovernedExecutionContext version")

    context = facade.context
    _require(execution.organization == context.organization, "Event support cannot cross the composed Organization scope")
    _require(
        execution.initiating_actor == context.actor,
        "Event support must preserve the exact Actor used to compose the integration facade",
    )
    _require(
        execution.product_contract == context.product_contract,
        "Event support must preserve the exact effective Product Contract Version",
    )
    _require(
        context.product_contract.subject_id in execution.record.provenance_refs
        and context.product_contract.version_id in execution.record.provenance_refs,
        "Governed Execution provenance must already preserve exact Product Contract identity/version",
    )
    actual_actor_id = context.actor.actual_principal.principal_id
    _require(
        actual_actor_id in execution.record.provenance_refs,
        "Governed Execution provenance must already preserve the initiating actual Principal",
    )


def _portable_links(
    *,
    facade: IntegrationCompositionFacade,
    event: CanonicalEvent,
    related_records: tuple[CanonicalRecord, ...],
) -> tuple[PortableSemanticLink, ...]:
    context = facade.context
    links: list[PortableSemanticLink] = [
        PortableSemanticLink(
            kind="event-execution-version",
            source_role="event-version",
            source_id=event.version_id,
            target_role="execution-version",
            target_id=event.execution_version_id,
        ),
        PortableSemanticLink(
            kind="event-execution-correlation",
            source_role="event-version",
            source_id=event.version_id,
            target_role="execution-subject",
            target_id=event.execution_subject_id,
        ),
        PortableSemanticLink(
            kind="event-product-contract-version",
            source_role="event-version",
            source_id=event.version_id,
            target_role="product-contract-version",
            target_id=context.product_contract.version_id,
        ),
        PortableSemanticLink(
            kind="product-contract-product",
            source_role="product-contract-version",
            source_id=context.product_contract.version_id,
            target_role="product-subject",
            target_id=context.product_id,
        ),
        PortableSemanticLink(
            kind="event-initiating-actor",
            source_role="event-version",
            source_id=event.version_id,
            target_role="principal-subject",
            target_id=context.actor.actual_principal.principal_id,
        ),
    ]
    if context.actor.represented_principal is not None:
        links.append(
            PortableSemanticLink(
                kind="event-represented-actor",
                source_role="event-version",
                source_id=event.version_id,
                target_role="principal-subject",
                target_id=context.actor.represented_principal.principal_id,
            )
        )
    for record in related_records:
        links.append(
            PortableSemanticLink(
                kind="event-related-version",
                source_role="event-version",
                source_id=event.version_id,
                target_role="canonical-version",
                target_id=record.version_id,
            )
        )
    return tuple(links)


def build_integration_event_support(
    *,
    facade: IntegrationCompositionFacade,
    execution: GovernedExecutionContext,
    event_id: Identity,
    event_version_id: Identity,
    event_type: str,
    event_schema_version: str,
    occurred_at: datetime,
    recorded_at: datetime,
    related_records: tuple[CanonicalRecord, ...] = (),
    admitted_events: tuple[CanonicalEvent, ...] = (),
    authoritative_source: str = "Arvectum OS",
    authority_scope: str = INTEGRATION_EVENT_AUTHORITY_SCOPE,
    classification: str = "internal",
    access_scope: str = "organization",
    payload: tuple[tuple[str, str], ...] = (),
) -> IntegrationEventSupportResult:
    """Admit one integration-linked Event and derive bounded portable evidence.

    The function deliberately requires the existing R14-hardened facade rather
    than caller-supplied Product/Contract attribution. That keeps exact boundary
    context anchored to the already validated composition path. Canonical Event
    semantics remain owned by :func:`event_provenance.admit_event`.
    """

    _validate_facade_execution_continuity(facade=facade, execution=execution)
    context = facade.context

    if not isinstance(related_records, tuple) or any(
        not isinstance(record, CanonicalRecord) for record in related_records
    ):
        raise ValueError("P5.07 related_records must be an immutable tuple of CanonicalRecord versions")
    if any(record.organization != context.organization for record in related_records):
        raise IntegrationEvidenceError("P5.07 related governed records must share the composed Organization scope")

    actor_refs = _actor_refs(context.actor)
    product_contract_refs = (
        context.product_contract.subject_id,
        context.product_contract.version_id,
    )
    execution_refs = (execution.execution_subject_id, execution.execution_version_id)
    related_refs = tuple(
        ref for record in related_records for ref in (record.subject_id, record.version_id)
    )
    provenance_refs = _ordered_unique(
        actor_refs,
        (context.product_id,),
        product_contract_refs,
        execution_refs,
        related_refs,
    )

    receipt = EventReceipt(
        event_id=event_id,
        version_id=event_version_id,
        event_type=event_type,
        event_schema_version=event_schema_version,
        organization=context.organization,
        authority_mode=AuthorityMode.NATIVE,
        authority_scope=authority_scope,
        authoritative_source=authoritative_source,
        occurred_at=occurred_at,
        recorded_at=recorded_at,
        producer_id=context.actor.actual_principal.principal_id,
        initiating_actor_id=context.actor.actual_principal.principal_id,
        execution_subject_id=execution.execution_subject_id,
        execution_version_id=execution.execution_version_id,
        related_subject_ids=tuple(record.subject_id for record in related_records),
        related_version_ids=tuple(record.version_id for record in related_records),
        correlation_refs=(execution.execution_subject_id,),
        causation_refs=(execution.execution_version_id,),
        classification=classification,
        access_scope=access_scope,
        provenance_refs=provenance_refs,
        integrity_metadata=(("representation", "p5.07-integration-evidence"),),
        payload=payload,
    )
    admission = admit_event(
        receipt=receipt,
        execution=execution,
        related_records=related_records,
        admitted_events=admitted_events,
    )
    event = admission.event

    required_context_refs = {
        context.actor.actual_principal.principal_id,
        context.product_id,
        context.product_contract.subject_id,
        context.product_contract.version_id,
        execution.execution_subject_id,
        execution.execution_version_id,
    }
    if context.actor.represented_principal is not None:
        required_context_refs.add(context.actor.represented_principal.principal_id)
    _require(
        required_context_refs.issubset(set(event.record.provenance_refs)),
        "admitted integration Event lost exact Actor/Product/Product Contract/Execution provenance",
    )

    execution_pin = GovernedVersionPin.from_record(execution.record)
    represented_actor_id = (
        None
        if context.actor.represented_principal is None
        else context.actor.represented_principal.principal_id
    )
    telemetry = IntegrationTelemetryProjection(
        authority_status=TELEMETRY_AUTHORITY_STATUS,
        organization=context.organization,
        actual_actor_id=context.actor.actual_principal.principal_id,
        represented_actor_id=represented_actor_id,
        product_id=context.product_id,
        product_version=context.product_version,
        product_contract=context.product_contract,
        execution=execution_pin,
        event=event.version_pin,
        event_type=event.event_type,
        event_schema_version=event.event_schema_version,
        correlation_refs=event.correlation_refs,
        causation_refs=event.causation_refs,
    )
    portable_fixture = IntegrationPortableSemanticFixture(
        authority_status=PORTABLE_FIXTURE_AUTHORITY_STATUS,
        organization=context.organization,
        actual_actor_id=context.actor.actual_principal.principal_id,
        represented_actor_id=represented_actor_id,
        product_id=context.product_id,
        product_version=context.product_version,
        product_contract=context.product_contract,
        execution=execution_pin,
        event=event.version_pin,
        event_type=event.event_type,
        event_schema_version=event.event_schema_version,
        provenance_refs=event.record.provenance_refs,
        semantic_links=_portable_links(
            facade=facade,
            event=event,
            related_records=related_records,
        ),
    )
    return IntegrationEventSupportResult(
        admission=admission,
        telemetry=telemetry,
        portable_fixture=portable_fixture,
    )
