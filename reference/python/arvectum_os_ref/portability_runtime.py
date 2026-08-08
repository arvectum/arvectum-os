"""P2.08 — bounded semantic portability, replay and projection runtime.

The runtime exports documented semantic meaning rather than Python object layout,
reconstructs that meaning through the existing bounded model invariants, and replays
only into derived non-authoritative projections. The JSON representation is internal
and provisional: it is not a public compatibility contract or production export API.
Replay exposes no Governed Execution, mutation, Event-admission or external-effect
adapter; a new consequential action must enter separately through Governed Execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from typing import Any, Final

from .canonical import AuthorityMode, CanonicalRecord
from .event_provenance import CanonicalEvent
from .execution import GovernedVersionPin
from .identity import Identity
from .relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipTypeReference,
    TypedRelationship,
)
from .security import ActorContext, OrganizationScope, Principal

FORMAT_ID: Final = "arvectum-os.core-runtime.semantic-portability"
FORMAT_VERSION: Final = "p2.08-internal-1"
STATUS: Final = "bounded-internal-provisional"


class PortabilityRuntimeError(ValueError):
    """Portable semantic input is invalid or loses required meaning."""


class ProjectionAuthorityBoundaryError(ValueError):
    """A derived projection was presented as governed/canonical authority."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise PortabilityRuntimeError(message)


def _identity(value: Identity) -> dict[str, str]:
    _require(isinstance(value, Identity), "portable identity must be an Identity")
    return {"namespace": value.namespace, "value": value.value, "scope": value.scope}


def _identity_from(value: Any, label: str) -> Identity:
    _require(isinstance(value, dict), f"{label} must be an identity mapping")
    _require(set(value) == {"namespace", "value", "scope"}, f"{label} identity fields mismatch")
    try:
        return Identity(value["namespace"], value["value"], value["scope"])
    except (TypeError, ValueError) as exc:
        raise PortabilityRuntimeError(f"{label} is not a valid Identity") from exc


def _identities(values: tuple[Identity, ...]) -> list[dict[str, str]]:
    return [_identity(item) for item in values]


def _identities_from(value: Any, label: str) -> tuple[Identity, ...]:
    _require(isinstance(value, list), f"{label} must be a list")
    result = tuple(_identity_from(item, f"{label}[{i}]") for i, item in enumerate(value))
    _require(len(set(result)) == len(result), f"{label} must not contain duplicates")
    return result


def _pairs(values: tuple[tuple[str, str], ...]) -> list[dict[str, str]]:
    return [{"name": name, "value": value} for name, value in values]


def _pairs_from(value: Any, label: str) -> tuple[tuple[str, str], ...]:
    _require(isinstance(value, list), f"{label} must be a list")
    result: list[tuple[str, str]] = []
    for i, item in enumerate(value):
        _require(isinstance(item, dict) and set(item) == {"name", "value"}, f"{label}[{i}] fields mismatch")
        _require(isinstance(item["name"], str) and isinstance(item["value"], str), f"{label}[{i}] must contain strings")
        result.append((item["name"], item["value"]))
    return tuple(result)


def _time_from(value: Any, label: str, *, optional: bool = False) -> datetime | None:
    if value is None:
        _require(optional, f"{label} must be explicit")
        return None
    _require(isinstance(value, str) and value.strip(), f"{label} must be an ISO datetime")
    try:
        result = datetime.fromisoformat(value)
    except ValueError as exc:
        raise PortabilityRuntimeError(f"{label} is not a valid ISO datetime") from exc
    _require(result.tzinfo is not None and result.utcoffset() is not None, f"{label} must be timezone-aware")
    return result


def _actor(value: ActorContext) -> dict[str, Any]:
    return {
        "actual_principal_id": _identity(value.actual_principal.principal_id),
        "represented_principal_id": None if value.represented_principal is None else _identity(value.represented_principal.principal_id),
        "organization_id": _identity(value.organization.organization_id),
        "authentication_evidence_refs": _identities(value.authentication_evidence_refs),
    }


def _actor_from(value: Any, organization: OrganizationScope, label: str) -> ActorContext:
    _require(isinstance(value, dict), f"{label} must be an actor mapping")
    _require(
        set(value) == {"actual_principal_id", "represented_principal_id", "organization_id", "authentication_evidence_refs"},
        f"{label} fields mismatch",
    )
    _require(_identity_from(value["organization_id"], f"{label}.organization_id") == organization.organization_id, f"{label} Organization mismatch")
    represented_raw = value["represented_principal_id"]
    represented = None if represented_raw is None else Principal(_identity_from(represented_raw, f"{label}.represented_principal_id"))
    return ActorContext(
        Principal(_identity_from(value["actual_principal_id"], f"{label}.actual_principal_id")),
        organization,
        represented_principal=represented,
        authentication_evidence_refs=_identities_from(value["authentication_evidence_refs"], f"{label}.authentication_evidence_refs"),
    )


def _record(value: CanonicalRecord) -> dict[str, Any]:
    return {
        "subject_identity": _identity(value.subject_id),
        "version_identity": _identity(value.version_id),
        "semantic_type": value.semantic_type,
        "schema_version": value.schema_version,
        "organization_id": _identity(value.organization.organization_id),
        "authority": {"mode": value.authority_mode.value, "scope": value.authority_scope},
        "accountable_owner_id": _identity(value.accountable_owner_id),
        "creation_actor": _actor(value.creation_actor),
        "created_at": value.created_at.isoformat(),
        "provenance_refs": _identities(value.provenance_refs),
        "integrity_metadata": _pairs(value.integrity_metadata),
        "payload": _pairs(value.payload),
        "lifecycle_status": value.lifecycle_status,
        "predecessor_version_identity": None if value.predecessor_version_id is None else _identity(value.predecessor_version_id),
        "effective_from": None if value.effective_from is None else value.effective_from.isoformat(),
        "effective_until": None if value.effective_until is None else value.effective_until.isoformat(),
    }


def _record_from(value: Any, organization: OrganizationScope, label: str) -> CanonicalRecord:
    fields = {
        "subject_identity", "version_identity", "semantic_type", "schema_version", "organization_id",
        "authority", "accountable_owner_id", "creation_actor", "created_at", "provenance_refs",
        "integrity_metadata", "payload", "lifecycle_status", "predecessor_version_identity",
        "effective_from", "effective_until",
    }
    _require(isinstance(value, dict) and set(value) == fields, f"{label} semantic fields mismatch")
    _require(_identity_from(value["organization_id"], f"{label}.organization_id") == organization.organization_id, f"{label} Organization mismatch")
    authority = value["authority"]
    _require(isinstance(authority, dict) and set(authority) == {"mode", "scope"}, f"{label}.authority fields mismatch")
    try:
        authority_mode = AuthorityMode(authority["mode"])
    except (TypeError, ValueError) as exc:
        raise PortabilityRuntimeError(f"{label}.authority.mode is unknown") from exc
    predecessor_raw = value["predecessor_version_identity"]
    try:
        return CanonicalRecord(
            subject_id=_identity_from(value["subject_identity"], f"{label}.subject_identity"),
            version_id=_identity_from(value["version_identity"], f"{label}.version_identity"),
            semantic_type=value["semantic_type"], schema_version=value["schema_version"],
            organization=organization, authority_mode=authority_mode, authority_scope=authority["scope"],
            accountable_owner_id=_identity_from(value["accountable_owner_id"], f"{label}.accountable_owner_id"),
            creation_actor=_actor_from(value["creation_actor"], organization, f"{label}.creation_actor"),
            created_at=_time_from(value["created_at"], f"{label}.created_at"),
            provenance_refs=_identities_from(value["provenance_refs"], f"{label}.provenance_refs"),
            integrity_metadata=_pairs_from(value["integrity_metadata"], f"{label}.integrity_metadata"),
            payload=_pairs_from(value["payload"], f"{label}.payload"),
            lifecycle_status=value["lifecycle_status"],
            predecessor_version_id=None if predecessor_raw is None else _identity_from(predecessor_raw, f"{label}.predecessor_version_identity"),
            effective_from=_time_from(value["effective_from"], f"{label}.effective_from", optional=True),
            effective_until=_time_from(value["effective_until"], f"{label}.effective_until", optional=True),
        )
    except (TypeError, ValueError) as exc:
        raise PortabilityRuntimeError(f"{label} does not reconstruct valid Canonical Record semantics") from exc


def _relationship(value: TypedRelationship) -> dict[str, Any]:
    return {
        "record_version_identity": _identity(value.record.version_id),
        "relationship_type": {
            "type_identity": _identity(value.relationship_type.type_id),
            "version_identity": _identity(value.relationship_type.version_id),
            "semantic_name": value.relationship_type.semantic_name,
            "schema_version": value.relationship_type.schema_version,
        },
        "source": {"reference_role": value.source.reference_role.value, "identity": _identity(value.source.identity)},
        "target": {"reference_role": value.target.reference_role.value, "identity": _identity(value.target.identity)},
    }


def _relationship_from(value: Any, records: dict[Identity, CanonicalRecord], label: str) -> TypedRelationship:
    _require(isinstance(value, dict) and set(value) == {"record_version_identity", "relationship_type", "source", "target"}, f"{label} fields mismatch")
    record_version = _identity_from(value["record_version_identity"], f"{label}.record_version_identity")
    _require(record_version in records, f"{label} canonical version absent from package")
    rel_type = value["relationship_type"]
    _require(isinstance(rel_type, dict) and set(rel_type) == {"type_identity", "version_identity", "semantic_name", "schema_version"}, f"{label}.relationship_type fields mismatch")

    def endpoint(name: str) -> RelationshipEndpoint:
        raw = value[name]
        _require(isinstance(raw, dict) and set(raw) == {"reference_role", "identity"}, f"{label}.{name} fields mismatch")
        try:
            role = EndpointReferenceRole(raw["reference_role"])
        except (TypeError, ValueError) as exc:
            raise PortabilityRuntimeError(f"{label}.{name}.reference_role is unknown") from exc
        return RelationshipEndpoint(role, _identity_from(raw["identity"], f"{label}.{name}.identity"))

    try:
        return TypedRelationship(
            record=records[record_version],
            relationship_type=RelationshipTypeReference(
                _identity_from(rel_type["type_identity"], f"{label}.relationship_type.type_identity"),
                _identity_from(rel_type["version_identity"], f"{label}.relationship_type.version_identity"),
                rel_type["semantic_name"], rel_type["schema_version"],
            ),
            source=endpoint("source"), target=endpoint("target"),
        )
    except (TypeError, ValueError) as exc:
        raise PortabilityRuntimeError(f"{label} does not reconstruct valid Typed Relationship semantics") from exc


def _event(value: CanonicalEvent) -> dict[str, Any]:
    return {
        "record_version_identity": _identity(value.record.version_id),
        "event_type": value.event_type, "event_schema_version": value.event_schema_version,
        "authoritative_source": value.authoritative_source,
        "occurred_at": value.occurred_at.isoformat(), "recorded_at": value.recorded_at.isoformat(),
        "producer_id": _identity(value.producer_id), "initiating_actor_id": _identity(value.initiating_actor_id),
        "execution_subject_id": _identity(value.execution_subject_id), "execution_version_id": _identity(value.execution_version_id),
        "related_subject_ids": _identities(value.related_subject_ids), "related_version_ids": _identities(value.related_version_ids),
        "correlation_refs": _identities(value.correlation_refs), "causation_refs": _identities(value.causation_refs),
        "classification": value.classification, "access_scope": value.access_scope,
    }


def _event_from(value: Any, records: dict[Identity, CanonicalRecord], label: str) -> CanonicalEvent:
    fields = {
        "record_version_identity", "event_type", "event_schema_version", "authoritative_source",
        "occurred_at", "recorded_at", "producer_id", "initiating_actor_id", "execution_subject_id",
        "execution_version_id", "related_subject_ids", "related_version_ids", "correlation_refs",
        "causation_refs", "classification", "access_scope",
    }
    _require(isinstance(value, dict) and set(value) == fields, f"{label} fields mismatch")
    record_version = _identity_from(value["record_version_identity"], f"{label}.record_version_identity")
    _require(record_version in records, f"{label} canonical version absent from package")
    try:
        return CanonicalEvent(
            record=records[record_version], event_type=value["event_type"], event_schema_version=value["event_schema_version"],
            authoritative_source=value["authoritative_source"],
            occurred_at=_time_from(value["occurred_at"], f"{label}.occurred_at"),
            recorded_at=_time_from(value["recorded_at"], f"{label}.recorded_at"),
            producer_id=_identity_from(value["producer_id"], f"{label}.producer_id"),
            initiating_actor_id=_identity_from(value["initiating_actor_id"], f"{label}.initiating_actor_id"),
            execution_subject_id=_identity_from(value["execution_subject_id"], f"{label}.execution_subject_id"),
            execution_version_id=_identity_from(value["execution_version_id"], f"{label}.execution_version_id"),
            related_subject_ids=_identities_from(value["related_subject_ids"], f"{label}.related_subject_ids"),
            related_version_ids=_identities_from(value["related_version_ids"], f"{label}.related_version_ids"),
            correlation_refs=_identities_from(value["correlation_refs"], f"{label}.correlation_refs"),
            causation_refs=_identities_from(value["causation_refs"], f"{label}.causation_refs"),
            classification=value["classification"], access_scope=value["access_scope"],
        )
    except (TypeError, ValueError) as exc:
        raise PortabilityRuntimeError(f"{label} does not reconstruct valid Event semantics") from exc


@dataclass(frozen=True, slots=True)
class SemanticPortabilityPackage:
    serialized: str

    def __post_init__(self) -> None:
        _require(isinstance(self.serialized, str) and self.serialized.strip(), "semantic portability package must be non-empty JSON")
        try:
            document = json.loads(self.serialized)
        except json.JSONDecodeError as exc:
            raise PortabilityRuntimeError("semantic portability package must be valid JSON") from exc
        metadata = document.get("format") if isinstance(document, dict) else None
        _require(isinstance(metadata, dict), "format metadata must be explicit")
        _require(metadata.get("format_id") == FORMAT_ID and metadata.get("format_version") == FORMAT_VERSION, "format identity/version mismatch")
        _require(metadata.get("status") == STATUS, "format must remain bounded/internal")
        _require(metadata.get("canonical_authority") is False, "portable representation cannot claim canonical authority")
        _require(metadata.get("derived_representation") is True, "portable representation must remain derived")
        _require(metadata.get("public_compatibility_contract") is False, "P2.08 must not freeze a public wire contract")
        _require(metadata.get("replay_consequential_effects") is False, "historical replay cannot authorize effects")

    def to_mapping(self) -> dict[str, Any]:
        result = json.loads(self.serialized)
        assert isinstance(result, dict)
        return result


@dataclass(frozen=True, slots=True)
class ReconstructedRuntimeSemantics:
    scenario_id: str
    organization: OrganizationScope
    records: tuple[CanonicalRecord, ...]
    relationships: tuple[TypedRelationship, ...]
    events: tuple[CanonicalEvent, ...]
    canonical_authority: bool = False

    def __post_init__(self) -> None:
        _require(isinstance(self.scenario_id, str) and self.scenario_id.strip(), "scenario_id must be explicit")
        _require(isinstance(self.organization, OrganizationScope), "Organization scope must be explicit")
        _require(isinstance(self.records, tuple) and self.records, "reconstruction requires records")
        _require(all(isinstance(item, CanonicalRecord) and item.organization == self.organization for item in self.records), "reconstructed records must share one Organization")
        _require(len({item.version_id for item in self.records}) == len(self.records), "reconstructed Version Identities must remain distinct")
        versions = {item.version_id for item in self.records}
        _require(all(isinstance(item, TypedRelationship) and item.record.version_id in versions for item in self.relationships), "relationship canonical versions must remain in records")
        _require(all(isinstance(item, CanonicalEvent) and item.record.version_id in versions for item in self.events), "Event canonical versions must remain in records")
        if self.canonical_authority is not False:
            raise ProjectionAuthorityBoundaryError("reconstructed package is not independent authority")


@dataclass(frozen=True, slots=True)
class RuntimeProjectionEntry:
    source_kind: str
    subject_id: Identity
    source_version_id: Identity
    semantic_type: str
    authority_mode: AuthorityMode
    authority_scope: str
    lifecycle_status: str | None
    canonical_authority: bool = False

    def __post_init__(self) -> None:
        _require(self.source_kind in {"canonical-record", "typed-relationship", "event"}, "projection source_kind is unknown")
        _require(isinstance(self.subject_id, Identity) and isinstance(self.source_version_id, Identity), "projection identities must be explicit")
        _require(self.subject_id != self.source_version_id, "projection Subject/Version roles must remain distinct")
        _require(isinstance(self.authority_mode, AuthorityMode), "projection authority mode must be explicit")
        _require(isinstance(self.authority_scope, str) and self.authority_scope.strip(), "projection authority scope must be explicit")
        _require(isinstance(self.semantic_type, str) and self.semantic_type.strip(), "projection semantic type must be explicit")
        if self.canonical_authority is not False:
            raise ProjectionAuthorityBoundaryError("derived projection entry cannot claim canonical authority")


@dataclass(frozen=True, slots=True)
class RuntimeProjectionSnapshot:
    source_scenario_id: str
    source_record_versions: tuple[Identity, ...]
    entries: tuple[RuntimeProjectionEntry, ...]
    replay_mode: str = "derived-projection-rebuild-only"
    canonical_authority: bool = False
    can_mint_governed_pins: bool = False
    consequential_side_effects_created: int = 0

    def __post_init__(self) -> None:
        _require(isinstance(self.source_scenario_id, str) and self.source_scenario_id.strip(), "projection must preserve scenario identity")
        _require(isinstance(self.source_record_versions, tuple) and self.source_record_versions, "projection must preserve source versions")
        _require(len(set(self.source_record_versions)) == len(self.source_record_versions), "projection cannot collapse source versions")
        _require(isinstance(self.entries, tuple) and self.entries, "projection entries must be explicit")
        _require(tuple(item.source_version_id for item in self.entries) == self.source_record_versions, "projection source manifest attribution mismatch")
        _require(self.replay_mode == "derived-projection-rebuild-only", "P2.08 replay mode is projection rebuild only")
        if self.canonical_authority is not False or self.can_mint_governed_pins is not False:
            raise ProjectionAuthorityBoundaryError("projection cannot become authority or mint governed pins")
        _require(self.consequential_side_effects_created == 0, "historical replay cannot create consequential side effects")

    def entries_for_subject(self, subject_id: Identity) -> tuple[RuntimeProjectionEntry, ...]:
        if not isinstance(subject_id, Identity):
            raise TypeError("projection lookup requires an Identity")
        return tuple(item for item in self.entries if item.subject_id == subject_id)


def export_runtime_semantic_package(
    *, scenario_id: str, records: tuple[CanonicalRecord, ...],
    relationships: tuple[TypedRelationship, ...] = (), events: tuple[CanonicalEvent, ...] = (),
) -> SemanticPortabilityPackage:
    _require(isinstance(scenario_id, str) and scenario_id.strip(), "scenario_id must be explicit")
    _require(isinstance(records, tuple) and records and all(isinstance(item, CanonicalRecord) for item in records), "records must contain CanonicalRecord values")
    _require(isinstance(relationships, tuple) and all(isinstance(item, TypedRelationship) for item in relationships), "relationships must contain TypedRelationship values")
    _require(isinstance(events, tuple) and all(isinstance(item, CanonicalEvent) for item in events), "events must contain CanonicalEvent values")

    ordered: list[CanonicalRecord] = []
    by_version: dict[Identity, CanonicalRecord] = {}
    for record in (*records, *(item.record for item in relationships), *(item.record for item in events)):
        existing = by_version.get(record.version_id)
        if existing is not None:
            _require(existing == record, "one Version Identity cannot represent different immutable content")
            continue
        by_version[record.version_id] = record
        ordered.append(record)
    organization = ordered[0].organization
    _require(all(item.organization == organization for item in ordered), "bounded P2.08 package must contain one Organization")
    _require(all(item.authority_mode is AuthorityMode.NATIVE for item in ordered), "bounded P2.08 package currently exercises Native authority only")
    relationship_versions = tuple(item.record.version_id for item in relationships)
    event_versions = tuple(item.record.version_id for item in events)
    _require(len(set(relationship_versions)) == len(relationship_versions), "relationship versions cannot duplicate")
    _require(len(set(event_versions)) == len(event_versions), "Event versions cannot duplicate")

    document = {
        "format": {
            "format_id": FORMAT_ID, "format_version": FORMAT_VERSION, "media_type": "application/json", "status": STATUS,
            "canonical_authority": False, "derived_representation": True, "public_compatibility_contract": False,
            "production_export_endpoint": False, "export_authorization_mechanism": False, "replay_consequential_effects": False,
        },
        "scenario": {"scenario_id": scenario_id, "organization_id": _identity(organization.organization_id), "scope": "bounded-core-runtime-semantic-snapshot"},
        "manifest": {
            "record_count": len(ordered), "record_versions": _identities(tuple(item.version_id for item in ordered)),
            "relationship_count": len(relationships), "relationship_versions": _identities(relationship_versions),
            "event_count": len(events), "event_versions": _identities(event_versions),
        },
        "records": [_record(item) for item in ordered],
        "relationships": [_relationship(item) for item in relationships],
        "events": [_event(item) for item in events],
        "portability": {
            "representation": "documented-internal-json-semantic-package", "canonical_authority": False,
            "public_compatibility_contract": False, "organization_scope": "single-organization-bounded-reference",
            "authority_modes_exercised": [AuthorityMode.NATIVE.value], "non_exportable_dependencies": [],
            "explicit_omissions": [
                "production export authorization and disclosure workflow",
                "External Reference and Governed Replica authority contracts",
                "stable public or cross-product serialization compatibility",
                "durable replay/projection storage or indexing technology",
                "reusable secrets, private keys, provider tokens and credentials",
                "capability activation, operational readiness and SLA commitments",
            ],
        },
    }
    return SemanticPortabilityPackage(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def reconstruct_runtime_semantics(*, package: SemanticPortabilityPackage) -> ReconstructedRuntimeSemantics:
    if not isinstance(package, SemanticPortabilityPackage):
        raise TypeError("reconstruction requires a SemanticPortabilityPackage")
    document = package.to_mapping()
    scenario, manifest = document.get("scenario"), document.get("manifest")
    records_raw, relationships_raw, events_raw = document.get("records"), document.get("relationships"), document.get("events")
    portability = document.get("portability")
    _require(isinstance(scenario, dict) and set(scenario) == {"scenario_id", "organization_id", "scope"}, "scenario metadata mismatch")
    _require(scenario["scope"] == "bounded-core-runtime-semantic-snapshot", "scenario scope mismatch")
    organization = OrganizationScope(_identity_from(scenario["organization_id"], "scenario.organization_id"))
    _require(isinstance(manifest, dict), "manifest must be explicit")
    _require(isinstance(records_raw, list) and records_raw, "records must be explicit")
    _require(isinstance(relationships_raw, list) and isinstance(events_raw, list), "relationship/Event lists must be explicit")
    _require(isinstance(portability, dict) and portability.get("canonical_authority") is False, "portable reconstruction cannot create authority")
    _require(portability.get("public_compatibility_contract") is False, "portable reconstruction is not a public wire contract")

    records = tuple(_record_from(raw, organization, f"records[{i}]") for i, raw in enumerate(records_raw))
    _require(manifest.get("record_count") == len(records), "record manifest count mismatch")
    _require(tuple(item.version_id for item in records) == _identities_from(manifest.get("record_versions"), "manifest.record_versions"), "record Version Identity manifest drift detected")
    by_version = {item.version_id: item for item in records}
    _require(len(by_version) == len(records), "portable records cannot reuse a Version Identity")
    relationships = tuple(_relationship_from(raw, by_version, f"relationships[{i}]") for i, raw in enumerate(relationships_raw))
    events = tuple(_event_from(raw, by_version, f"events[{i}]") for i, raw in enumerate(events_raw))
    _require(manifest.get("relationship_count") == len(relationships), "relationship manifest count mismatch")
    _require(manifest.get("event_count") == len(events), "Event manifest count mismatch")
    _require(tuple(item.record.version_id for item in relationships) == _identities_from(manifest.get("relationship_versions"), "manifest.relationship_versions"), "relationship Version Identity manifest drift detected")
    _require(tuple(item.record.version_id for item in events) == _identities_from(manifest.get("event_versions"), "manifest.event_versions"), "Event Version Identity manifest drift detected")
    return ReconstructedRuntimeSemantics(scenario["scenario_id"], organization, records, relationships, events)


def rebuild_non_authoritative_projection(*, package: SemanticPortabilityPackage) -> RuntimeProjectionSnapshot:
    """Replay a package only into a derived read model; no side-effect adapter exists."""
    reconstructed = reconstruct_runtime_semantics(package=package)
    relationship_versions = {item.record.version_id for item in reconstructed.relationships}
    event_versions = {item.record.version_id for item in reconstructed.events}
    entries = tuple(
        RuntimeProjectionEntry(
            "typed-relationship" if item.version_id in relationship_versions else "event" if item.version_id in event_versions else "canonical-record",
            item.subject_id, item.version_id, item.semantic_type, item.authority_mode, item.authority_scope, item.lifecycle_status,
        )
        for item in reconstructed.records
    )
    return RuntimeProjectionSnapshot(reconstructed.scenario_id, tuple(item.version_id for item in reconstructed.records), entries)


def pin_runtime_projection_source(*, projection_entry: RuntimeProjectionEntry, canonical_source: CanonicalRecord) -> GovernedVersionPin:
    """Mint a pin only from an independently supplied exact Canonical Record."""
    if not isinstance(projection_entry, RuntimeProjectionEntry):
        raise TypeError("projection_entry must be a RuntimeProjectionEntry")
    if not isinstance(canonical_source, CanonicalRecord):
        raise ProjectionAuthorityBoundaryError("projection cannot substitute for an exact CanonicalRecord source")
    expected = (
        projection_entry.subject_id, projection_entry.source_version_id, projection_entry.semantic_type,
        projection_entry.authority_mode, projection_entry.authority_scope, projection_entry.lifecycle_status,
    )
    actual = (
        canonical_source.subject_id, canonical_source.version_id, canonical_source.semantic_type,
        canonical_source.authority_mode, canonical_source.authority_scope, canonical_source.lifecycle_status,
    )
    if actual != expected:
        raise ProjectionAuthorityBoundaryError("projection attribution does not match the exact canonical source")
    return GovernedVersionPin.from_record(canonical_source)
