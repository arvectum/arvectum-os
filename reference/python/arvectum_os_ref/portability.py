"""P1.10 — portable semantic fixture export.

The bounded Phase 1 reference slice exports governed semantic meaning through an
explicit JSON document rather than serializing Python dataclass/object layout.
The fixture is derived, non-canonical, non-authoritative and intentionally not a
stable public compatibility contract.

This module preserves exact Organization, identity, immutable-version, authority,
workflow/gate/execution, Event/provenance and Observation non-promotion semantics
already established by P1.01–P1.09. It does not create new Canonical Records,
Typed Relationships, validated Knowledge, permissions, Organizational Authority,
or a production export endpoint.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any

from .canonical import CanonicalRecord
from .events import CanonicalEvent
from .execution import ExecutionContext, GovernedVersionPin
from .gates import GateDecision
from .identity import Identity
from .mutation import CanonicalMutationResult
from .observation import (
    Observation,
    ObservationEpistemicStatus,
    build_p1_09_observation,
)
from .provenance import (
    ReconstructionEvidence,
    build_p1_08_reconstruction_evidence,
)
from .security import ActorContext, OrganizationScope
from .workflow import WorkflowDefinition


_FIXTURE_FORMAT_ID = "arvectum-os.phase1.semantic-fixture"
_FIXTURE_FORMAT_VERSION = "1"
_FIXTURE_SCOPE = "P1.01-P1.10"
_MEDIA_TYPE = "application/json"


class PortableFixtureExportError(ValueError):
    """Supplied governed evidence cannot be exported as the bounded P1.10 fixture."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PortableFixtureExportError(message)


def _identity(identity: Identity) -> dict[str, str]:
    _require(isinstance(identity, Identity), "portable identity reference must be an Identity")
    return {
        "namespace": identity.namespace,
        "value": identity.value,
        "scope": identity.scope,
    }


def _identity_refs(refs: tuple[Identity, ...]) -> list[dict[str, str]]:
    return [_identity(ref) for ref in refs]


def _optional_identity(identity: Identity | None) -> dict[str, str] | None:
    return None if identity is None else _identity(identity)


def _actor(actor: ActorContext) -> dict[str, Any]:
    _require(isinstance(actor, ActorContext), "portable Actor attribution must be explicit")
    return {
        "actual_principal_id": _identity(actor.actual_principal.principal_id),
        "represented_principal_id": (
            None
            if actor.represented_principal is None
            else _identity(actor.represented_principal.principal_id)
        ),
        "organization_id": _identity(actor.organization.organization_id),
        "authentication_evidence_refs": _identity_refs(actor.authentication_evidence_refs),
    }


def _named_entries(entries: tuple[tuple[str, str], ...]) -> list[dict[str, str]]:
    return [{"name": name, "value": value} for name, value in entries]


def _canonical_envelope(record: CanonicalRecord) -> dict[str, Any]:
    _require(isinstance(record, CanonicalRecord), "portable record envelope requires CanonicalRecord")
    return {
        "subject_identity": _identity(record.subject_id),
        "version_identity": _identity(record.version_id),
        "semantic_type": record.semantic_type,
        "schema_version": record.schema_version,
        "organization_id": _identity(record.organization.organization_id),
        "authority": {
            "mode": record.authority_mode.value,
            "scope": record.authority_scope,
        },
        "accountable_owner_id": _identity(record.accountable_owner_id),
        "creation_actor": _actor(record.creation_actor),
        "created_at": record.created_at.isoformat(),
        "provenance_refs": _identity_refs(record.provenance_refs),
        "integrity_metadata": _named_entries(record.integrity_metadata),
        "payload": _named_entries(record.payload),
        "lifecycle_status": record.lifecycle_status,
        "predecessor_version_identity": _optional_identity(record.predecessor_version_id),
    }


def _pin(pin: GovernedVersionPin) -> dict[str, Any]:
    _require(isinstance(pin, GovernedVersionPin), "portable governed reliance must be version-pinned")
    return {
        "subject_identity": _identity(pin.subject_id),
        "version_identity": _identity(pin.version_id),
        "semantic_type": pin.semantic_type,
        "authority_scope": pin.authority_scope,
        "lifecycle_status": pin.lifecycle_status,
    }


def _workflow_semantics(workflow: WorkflowDefinition) -> dict[str, Any]:
    return {
        "operations": [
            {
                "semantic_name": operation.semantic_name,
                "target": {
                    "reference_role": "subject",
                    "identity": _identity(operation.target_subject_id),
                },
                "target_semantic_type": operation.target_semantic_type,
                "side_effect_classes": [item.value for item in operation.side_effect_classes],
            }
            for operation in workflow.operations
        ]
    }


def _gate_semantics(decision: GateDecision) -> dict[str, Any]:
    return {
        "kind": decision.kind.value,
        "outcome": decision.outcome.value,
        "basis_ref": {
            "reference_role": "governed-identity",
            "identity": _identity(decision.basis_ref),
        },
        "subject_principal": {
            "reference_role": "subject",
            "identity": _identity(decision.subject_principal_id),
        },
        "execution_subject": {
            "reference_role": "subject",
            "identity": _identity(decision.execution_subject_id),
        },
        "evaluated_execution_version": {
            "reference_role": "version",
            "identity": _identity(decision.evaluated_execution_version_id),
        },
        "workflow_version": {
            "reference_role": "version",
            "identity": _identity(decision.workflow_version_id),
        },
        "operation_name": decision.operation_name,
        "target_subject": {
            "reference_role": "subject",
            "identity": _identity(decision.target_subject_id),
        },
        "target_version": {
            "reference_role": "version",
            "identity": _identity(decision.target_version_id),
        },
    }


def _execution_semantics(execution: ExecutionContext) -> dict[str, Any]:
    return {
        "workflow": _pin(execution.workflow),
        "operation_name": execution.operation_name,
        "material_inputs": [_pin(pin) for pin in execution.material_inputs],
        "gate_decisions": [_pin(pin) for pin in execution.gate_decisions],
        "canonical_effects": [_pin(pin) for pin in execution.canonical_effects],
    }


def _event_semantics(event: CanonicalEvent) -> dict[str, Any]:
    return {
        "event_type": event.event_type,
        "event_schema_version": event.event_schema_version,
        "authoritative_source": event.authoritative_source,
        "occurred_at": event.occurred_at.isoformat(),
        "recorded_at": event.recorded_at.isoformat(),
        "producer_id": _identity(event.producer_id),
        "initiating_actor_id": _identity(event.initiating_actor_id),
        "execution_subject": {
            "reference_role": "subject",
            "identity": _identity(event.execution_subject_id),
        },
        "execution_version": {
            "reference_role": "version",
            "identity": _identity(event.execution_version_id),
        },
        "related_subjects": [
            {"reference_role": "subject", "identity": _identity(identity)}
            for identity in event.related_subject_ids
        ],
        "related_versions": [
            {"reference_role": "version", "identity": _identity(identity)}
            for identity in event.related_version_ids
        ],
        "correlation_refs": [
            {"reference_role": "subject", "identity": _identity(identity)}
            for identity in event.correlation_refs
        ],
        "causation_refs": [
            {"reference_role": "version", "identity": _identity(identity)}
            for identity in event.causation_refs
        ],
        "classification": event.classification,
        "access_scope": event.access_scope,
    }


def _observation_semantics(observation: Observation) -> dict[str, Any]:
    return {
        "epistemic_status": observation.epistemic_status.value,
        "source_event": _pin(observation.source_event),
        "source_execution": _pin(observation.source_execution),
        "observed_effect": _pin(observation.observed_effect),
        "evidence_refs": _identity_refs(observation.evidence_refs),
        "knowledge_promotion": "not-performed",
    }


def _reconstruction_semantics(evidence: ReconstructionEvidence) -> dict[str, Any]:
    return {
        "authority_status": "derived-non-canonical",
        "organization_id": _identity(evidence.organization.organization_id),
        "initiating_actor_id": _identity(evidence.initiating_actor_id),
        "operation_name": evidence.operation_name,
        "workflow": _pin(evidence.workflow),
        "material_inputs": [_pin(pin) for pin in evidence.material_inputs],
        "gate_decisions": [_pin(pin) for pin in evidence.gate_decisions],
        "execution_versions": [_pin(pin) for pin in evidence.execution_versions],
        "canonical_effects": [_pin(pin) for pin in evidence.canonical_effects],
        "events": [_pin(pin) for pin in evidence.events],
        "event_type": evidence.event_type,
        "event_schema_version": evidence.event_schema_version,
        "correlation_refs": _identity_refs(evidence.correlation_refs),
        "causation_refs": _identity_refs(evidence.causation_refs),
        "provenance_refs": _identity_refs(evidence.provenance_refs),
    }


def _record(role: str, record: CanonicalRecord, **specialized: dict[str, Any]) -> dict[str, Any]:
    exported: dict[str, Any] = {
        "role": role,
        "canonical_record": _canonical_envelope(record),
    }
    exported.update(specialized)
    return exported


def _reference(reference_role: str, identity: Identity) -> dict[str, Any]:
    return {
        "reference_role": reference_role,
        "identity": _identity(identity),
    }


def _link(
    kind: str,
    source_role: str,
    source_identity: Identity,
    target_role: str,
    target_identity: Identity,
) -> dict[str, Any]:
    return {
        "kind": kind,
        "canonical_typed_relationship": False,
        "source": _reference(source_role, source_identity),
        "target": _reference(target_role, target_identity),
    }


def _semantic_links(
    *,
    workflow: WorkflowDefinition,
    awaiting_execution: ExecutionContext,
    authorization: GateDecision,
    organizational_authority: GateDecision,
    ready_execution: ExecutionContext,
    mutation: CanonicalMutationResult,
    event: CanonicalEvent,
    observation: Observation,
) -> list[dict[str, Any]]:
    terminal_execution = mutation.execution
    input_pin = awaiting_execution.material_inputs[0]
    workflow_version = workflow.record.version_id
    links: list[dict[str, Any]] = [
        _link(
            "workflow-operation-target",
            "version",
            workflow_version,
            "subject",
            input_pin.subject_id,
        ),
        _link(
            "predecessor-version",
            "version",
            ready_execution.record.version_id,
            "version",
            awaiting_execution.record.version_id,
        ),
        _link(
            "predecessor-version",
            "version",
            terminal_execution.record.version_id,
            "version",
            ready_execution.record.version_id,
        ),
        _link(
            "predecessor-version",
            "version",
            mutation.resulting_record.version_id,
            "version",
            mutation.previous_version.version_id,
        ),
    ]

    for execution in (awaiting_execution, ready_execution, terminal_execution):
        links.extend(
            (
                _link(
                    "workflow-version-reliance",
                    "version",
                    execution.record.version_id,
                    "version",
                    execution.workflow.version_id,
                ),
                _link(
                    "material-input-version-reliance",
                    "version",
                    execution.record.version_id,
                    "version",
                    input_pin.version_id,
                ),
            )
        )

    for execution in (ready_execution, terminal_execution):
        for gate_pin in execution.gate_decisions:
            links.append(
                _link(
                    "gate-decision-version-reliance",
                    "version",
                    execution.record.version_id,
                    "version",
                    gate_pin.version_id,
                )
            )

    links.append(
        _link(
            "canonical-effect-version",
            "version",
            terminal_execution.record.version_id,
            "version",
            mutation.resulting_record.version_id,
        )
    )

    for decision in (authorization, organizational_authority):
        links.extend(
            (
                _link(
                    "evaluated-execution-version",
                    "version",
                    decision.record.version_id,
                    "version",
                    decision.evaluated_execution_version_id,
                ),
                _link(
                    "workflow-version-reliance",
                    "version",
                    decision.record.version_id,
                    "version",
                    decision.workflow_version_id,
                ),
                _link(
                    "target-version-reliance",
                    "version",
                    decision.record.version_id,
                    "version",
                    decision.target_version_id,
                ),
                _link(
                    "governed-basis-reference",
                    "version",
                    decision.record.version_id,
                    "governed-identity",
                    decision.basis_ref,
                ),
            )
        )

    links.extend(
        (
            _link(
                "event-execution-version",
                "version",
                event.record.version_id,
                "version",
                event.execution_version_id,
            ),
            _link(
                "event-related-version",
                "version",
                event.record.version_id,
                "version",
                event.related_version_ids[0],
            ),
            _link(
                "correlation",
                "version",
                event.record.version_id,
                "subject",
                event.correlation_refs[0],
            ),
            _link(
                "causation",
                "version",
                event.record.version_id,
                "version",
                event.causation_refs[0],
            ),
            _link(
                "observation-source-event",
                "version",
                observation.record.version_id,
                "version",
                observation.source_event.version_id,
            ),
            _link(
                "observation-source-execution",
                "version",
                observation.record.version_id,
                "version",
                observation.source_execution.version_id,
            ),
            _link(
                "observation-observed-effect",
                "version",
                observation.record.version_id,
                "version",
                observation.observed_effect.version_id,
            ),
        )
    )
    return links


@dataclass(frozen=True, slots=True)
class PortableSemanticFixture:
    """Immutable UTF-8 JSON text representing the bounded P1.10 semantic fixture."""

    serialized: str

    def __post_init__(self) -> None:
        if not isinstance(self.serialized, str) or not self.serialized.strip():
            raise PortableFixtureExportError("portable fixture serialization must be non-empty JSON text")
        try:
            document = json.loads(self.serialized)
        except json.JSONDecodeError as exc:
            raise PortableFixtureExportError("portable fixture serialization must be valid JSON") from exc
        _require(isinstance(document, dict), "portable fixture JSON root must be an object")
        fixture = document.get("fixture")
        _require(isinstance(fixture, dict), "portable fixture metadata must be explicit")
        _require(
            fixture.get("format_id") == _FIXTURE_FORMAT_ID
            and fixture.get("format_version") == _FIXTURE_FORMAT_VERSION,
            "portable fixture format identity/version must be explicit",
        )
        _require(
            fixture.get("canonical_authority") is False,
            "portable fixture must explicitly remain non-canonical",
        )

    def to_mapping(self) -> dict[str, Any]:
        """Return a fresh parsed mapping without exposing Python model instances."""

        document = json.loads(self.serialized)
        assert isinstance(document, dict)
        return document


def export_p1_10_semantic_fixture(
    *,
    input_record: CanonicalRecord,
    workflow: WorkflowDefinition,
    awaiting_execution: ExecutionContext,
    authorization: GateDecision,
    organizational_authority: GateDecision,
    ready_execution: ExecutionContext,
    mutation: CanonicalMutationResult,
    event: CanonicalEvent,
    evidence: ReconstructionEvidence,
    observation: Observation,
) -> PortableSemanticFixture:
    """Export the exact P1.01–P1.09 state into bounded implementation-neutral JSON.

    Export validates the already-governed evidence again and then builds a
    deterministic semantic manifest. It never reconstructs authority from a
    projection, never promotes Observation to Knowledge, and never changes the
    source objects.
    """

    for label, value, expected_type in (
        ("input_record", input_record, CanonicalRecord),
        ("workflow", workflow, WorkflowDefinition),
        ("awaiting_execution", awaiting_execution, ExecutionContext),
        ("authorization", authorization, GateDecision),
        ("organizational_authority", organizational_authority, GateDecision),
        ("ready_execution", ready_execution, ExecutionContext),
        ("mutation", mutation, CanonicalMutationResult),
        ("event", event, CanonicalEvent),
        ("evidence", evidence, ReconstructionEvidence),
        ("observation", observation, Observation),
    ):
        _require(isinstance(value, expected_type), f"P1.10 requires exact {label} governed evidence")

    try:
        reconstructed = build_p1_08_reconstruction_evidence(
            input_record=input_record,
            workflow=workflow,
            awaiting_execution=awaiting_execution,
            authorization=authorization,
            organizational_authority=organizational_authority,
            ready_execution=ready_execution,
            mutation=mutation,
            event=event,
        )
    except (TypeError, ValueError, RuntimeError) as exc:
        raise PortableFixtureExportError(
            "P1.10 source evidence does not satisfy the bounded reconstruction contract"
        ) from exc
    _require(
        reconstructed == evidence,
        "P1.10 must export the exact P1.08 reconstruction evidence supplied by the caller",
    )

    try:
        reconstructed_observation = build_p1_09_observation(
            evidence=evidence,
            event=event,
            mutation=mutation,
        )
    except (TypeError, ValueError, RuntimeError) as exc:
        raise PortableFixtureExportError(
            "P1.10 source evidence does not satisfy the bounded Observation contract"
        ) from exc
    _require(
        reconstructed_observation == observation,
        "P1.10 must export the exact P1.09 Observation supplied by the caller",
    )
    _require(
        observation.epistemic_status is ObservationEpistemicStatus.UNVALIDATED,
        "P1.10 must preserve Observation as explicitly unvalidated",
    )

    organization = input_record.organization
    governed_records = (
        input_record,
        workflow.record,
        awaiting_execution.record,
        authorization.record,
        organizational_authority.record,
        ready_execution.record,
        mutation.resulting_record,
        mutation.execution.record,
        event.record,
        observation.record,
    )
    _require(
        all(record.organization == organization for record in governed_records),
        "all exported Canonical Record versions must share the bounded Organization scope",
    )

    records = [
        _record("material-input-v1", input_record),
        _record(
            "workflow-v1",
            workflow.record,
            workflow=_workflow_semantics(workflow),
        ),
        _record(
            "authorization-decision",
            authorization.record,
            gate=_gate_semantics(authorization),
        ),
        _record(
            "organizational-authority-decision",
            organizational_authority.record,
            gate=_gate_semantics(organizational_authority),
        ),
        _record(
            "execution-awaiting-gate",
            awaiting_execution.record,
            execution=_execution_semantics(awaiting_execution),
        ),
        _record(
            "execution-ready",
            ready_execution.record,
            execution=_execution_semantics(ready_execution),
        ),
        _record("canonical-result-v2", mutation.resulting_record),
        _record(
            "execution-succeeded",
            mutation.execution.record,
            execution=_execution_semantics(mutation.execution),
        ),
        _record(
            "canonical-event",
            event.record,
            event=_event_semantics(event),
        ),
        _record(
            "observation",
            observation.record,
            observation=_observation_semantics(observation),
        ),
    ]
    version_identities = [
        item["canonical_record"]["version_identity"] for item in records
    ]
    serialized_version_keys = {
        (identity["namespace"], identity["value"], identity["scope"])
        for identity in version_identities
    }
    _require(
        len(serialized_version_keys) == len(records),
        "portable fixture must not duplicate immutable Canonical Record Version Identities",
    )

    semantic_links = _semantic_links(
        workflow=workflow,
        awaiting_execution=awaiting_execution,
        authorization=authorization,
        organizational_authority=organizational_authority,
        ready_execution=ready_execution,
        mutation=mutation,
        event=event,
        observation=observation,
    )

    decision_actor = authorization.record.creation_actor
    _require(
        organizational_authority.record.creation_actor == decision_actor,
        "bounded P1.10 fixture expects one attributable gate-decision Actor",
    )

    document: dict[str, Any] = {
        "fixture": {
            "format_id": _FIXTURE_FORMAT_ID,
            "format_version": _FIXTURE_FORMAT_VERSION,
            "media_type": _MEDIA_TYPE,
            "scope": _FIXTURE_SCOPE,
            "status": "bounded-reference-fixture",
            "canonical_authority": False,
            "derived_representation": True,
            "public_compatibility_contract": False,
            "production_export_endpoint": False,
        },
        "organization": {
            "organization_id": _identity(organization.organization_id),
            "tenant_scope": None,
        },
        "actors": [
            {"role": "initiating-actor", **_actor(awaiting_execution.initiating_actor)},
            {"role": "gate-decision-actor", **_actor(decision_actor)},
        ],
        "manifest": {
            "record_count": len(records),
            "record_versions": version_identities,
            "semantic_link_count": len(semantic_links),
            "canonical_typed_relationship_record_count": 0,
            "included_semantics": [
                "organization-and-actor-attribution",
                "canonical-record-identity-and-versioning",
                "workflow-version-and-operation",
                "authorization-and-organizational-authority-decisions",
                "execution-version-lineage-and-exact-version-pins",
                "canonical-mutation-result-lineage",
                "event-attribution-correlation-causation-and-provenance",
                "derived-reconstruction-evidence",
                "observation-unvalidated-non-promotion",
            ],
        },
        "records": records,
        "semantic_links": semantic_links,
        "reconstruction": _reconstruction_semantics(evidence),
        "portability": {
            "representation": "documented-json-semantic-fixture",
            "canonical_authority": False,
            "public_compatibility_contract": False,
            "export_authorization_mechanism": False,
            "non_exportable_dependencies": [],
            "explicit_omissions": [
                "reusable secrets, private keys, provider tokens and credentials",
                "product-domain semantics and Product Contract state",
                "durable persistence, cache, projection and index implementation state",
                "validated Knowledge, Knowledge promotion or Improvement Proposal state",
                "production, SLA, support, archival or compatibility commitments",
            ],
        },
    }

    serialized = json.dumps(
        document,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"
    return PortableSemanticFixture(serialized=serialized)
