from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import inspect
import json
import unittest

import arvectum_os_ref.portability_runtime as portability_runtime_module
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import CanonicalEvent
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.portability_runtime import (
    PortabilityRuntimeError,
    ProjectionAuthorityBoundaryError,
    ReconstructedRuntimeSemantics,
    RuntimeProjectionEntry,
    RuntimeProjectionSnapshot,
    SemanticPortabilityPackage,
    export_runtime_semantic_package,
    pin_runtime_projection_source,
    rebuild_non_authoritative_projection,
    reconstruct_runtime_semantics,
)
from arvectum_os_ref.relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipTypeReference,
    create_typed_relationship,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


UTC = timezone.utc


class P208PortabilityReplayProjectionRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 10, minute, tzinfo=UTC)

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        subject: str,
        version: str,
        semantic_type: str = "example.subject",
        *,
        predecessor: Identity | None = None,
        authority_scope: str = "example.subject/state",
        lifecycle_status: str | None = "Active",
        minute: int = 0,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", subject),
            version_id=self._id("canonical-version", version),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(minute),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "test"),),
            payload=(("value", version),),
            lifecycle_status=lifecycle_status,
            predecessor_version_id=predecessor,
        )

    def _relationship_scenario(self):
        subject_a_v1 = self._record("subject-a", "subject-a-v1", minute=0)
        subject_a_v2 = self._record(
            "subject-a",
            "subject-a-v2",
            predecessor=subject_a_v1.version_id,
            minute=1,
        )
        subject_b_v1 = self._record("subject-b", "subject-b-v1", minute=0)
        relationship_type = RelationshipTypeReference(
            type_id=self._id("relationship-type", "references"),
            version_id=self._id("relationship-type-version", "references-v1"),
            semantic_name="references",
            schema_version="1",
        )
        relationship = create_typed_relationship(
            relationship_id=self._id("relationship-subject", "rel-a-b"),
            version_id=self._id("relationship-version", "rel-a-b-v1"),
            relationship_type=relationship_type,
            source=RelationshipEndpoint(
                EndpointReferenceRole.VERSION_IDENTITY,
                subject_a_v2.version_id,
            ),
            target=RelationshipEndpoint(
                EndpointReferenceRole.SUBJECT_IDENTITY,
                subject_b_v1.subject_id,
            ),
            organization=self.organization,
            actor=self.actor,
            authority_scope="platform.relationship/example",
            created_at=self._time(2),
        )
        return (subject_a_v1, subject_a_v2, subject_b_v1), relationship

    def _event_scenario(self):
        execution = self._record(
            "execution-1",
            "execution-1-v3",
            semantic_type="platform.execution-context",
            authority_scope="platform.governed-execution/context",
            lifecycle_status="Succeeded",
            minute=4,
        )
        result = self._record("result-1", "result-1-v2", minute=4)
        event_record = CanonicalRecord(
            subject_id=self._id("event-subject", "event-1"),
            version_id=self._id("event-version", "event-1-v1"),
            semantic_type="platform.event",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/history",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(5),
            provenance_refs=(
                self.principal.principal_id,
                execution.subject_id,
                execution.version_id,
                result.subject_id,
                result.version_id,
            ),
            integrity_metadata=(("representation", "test"),),
            payload=(("outcome", "completed"),),
            lifecycle_status="Admitted",
        )
        event = CanonicalEvent(
            record=event_record,
            event_type="example.completed",
            event_schema_version="1",
            authoritative_source="Arvectum OS bounded runtime",
            occurred_at=self._time(5),
            recorded_at=self._time(5),
            producer_id=self.principal.principal_id,
            initiating_actor_id=self.principal.principal_id,
            execution_subject_id=execution.subject_id,
            execution_version_id=execution.version_id,
            related_subject_ids=(result.subject_id,),
            related_version_ids=(result.version_id,),
            correlation_refs=(execution.subject_id,),
            causation_refs=(execution.version_id,),
            classification="internal",
            access_scope="organization",
        )
        return (execution, result), event

    def test_package_is_internal_derived_and_non_authoritative(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="relationship-round-trip",
            records=records,
            relationships=(relationship,),
        )
        document = package.to_mapping()
        self.assertEqual(
            document["format"]["format_id"],
            "arvectum-os.core-runtime.semantic-portability",
        )
        self.assertEqual(document["format"]["format_version"], "p2.08-internal-1")
        self.assertEqual(document["format"]["status"], "bounded-internal-provisional")
        self.assertFalse(document["format"]["canonical_authority"])
        self.assertTrue(document["format"]["derived_representation"])
        self.assertFalse(document["format"]["public_compatibility_contract"])
        self.assertFalse(document["format"]["replay_consequential_effects"])
        self.assertFalse(document["format"]["production_export_endpoint"])

    def test_relationship_scenario_round_trips_semantic_meaning(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="relationship-round-trip",
            records=records,
            relationships=(relationship,),
        )
        reconstructed = reconstruct_runtime_semantics(package=package)
        self.assertIsInstance(reconstructed, ReconstructedRuntimeSemantics)
        self.assertEqual(reconstructed.scenario_id, "relationship-round-trip")
        self.assertEqual(
            tuple(item.version_id for item in reconstructed.records),
            tuple(item.version_id for item in (*records, relationship.record)),
        )
        self.assertFalse(reconstructed.events)
        self.assertFalse(reconstructed.canonical_authority)
        self.assertTrue(all(item.canonical_authority is False for item in reconstructed.records))
        restored = reconstructed.relationships[0]
        self.assertEqual(restored.record_version_id, relationship.record.version_id)
        self.assertEqual(restored.relationship_type, relationship.relationship_type)
        self.assertEqual(restored.source, relationship.source)
        self.assertEqual(restored.target, relationship.target)

    def test_event_scenario_round_trips_exact_event_semantics(self) -> None:
        records, event = self._event_scenario()
        package = export_runtime_semantic_package(
            scenario_id="event-round-trip",
            records=records,
            events=(event,),
        )
        reconstructed = reconstruct_runtime_semantics(package=package)
        self.assertEqual(
            tuple(item.version_id for item in reconstructed.records),
            tuple(item.version_id for item in (*records, event.record)),
        )
        restored = reconstructed.events[0]
        self.assertEqual(restored.record_version_id, event.record.version_id)
        self.assertFalse(restored.canonical_authority)
        self.assertEqual(restored.execution_version_id, event.execution_version_id)
        self.assertEqual(restored.related_version_ids, event.related_version_ids)
        self.assertEqual(restored.correlation_refs, event.correlation_refs)
        self.assertEqual(restored.causation_refs, event.causation_refs)

    def test_two_distinct_scenarios_rebuild_zero_effect_non_authoritative_projections(self) -> None:
        records_a, relationship = self._relationship_scenario()
        records_b, event = self._event_scenario()
        packages = (
            export_runtime_semantic_package(
                scenario_id="relationship-round-trip",
                records=records_a,
                relationships=(relationship,),
            ),
            export_runtime_semantic_package(
                scenario_id="event-round-trip",
                records=records_b,
                events=(event,),
            ),
        )
        for package in packages:
            projection = rebuild_non_authoritative_projection(package=package)
            self.assertIsInstance(projection, RuntimeProjectionSnapshot)
            self.assertFalse(projection.canonical_authority)
            self.assertFalse(projection.can_mint_governed_pins)
            self.assertEqual(projection.consequential_side_effects_created, 0)
            self.assertEqual(projection.replay_mode, "derived-projection-rebuild-only")

    def test_projection_preserves_exact_source_version_manifest(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="projection-source-manifest",
            records=records,
            relationships=(relationship,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        expected = tuple(record.version_id for record in (*records, relationship.record))
        self.assertEqual(projection.source_record_versions, expected)
        self.assertEqual(
            tuple(entry.source_version_id for entry in projection.entries),
            expected,
        )

    def test_projection_lookup_returns_all_versions_without_head_inference(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="projection-version-discovery",
            records=records,
            relationships=(relationship,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        subject_versions = projection.entries_for_subject(records[0].subject_id)
        self.assertEqual(
            tuple(entry.source_version_id for entry in subject_versions),
            (records[0].version_id, records[1].version_id),
        )

    def test_projection_cannot_mint_governed_pin_without_exact_canonical_source(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="projection-authority-boundary",
            records=records,
            relationships=(relationship,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        entry = projection.entries[0]
        with self.assertRaises(ProjectionAuthorityBoundaryError):
            pin_runtime_projection_source(
                projection_entry=entry,
                canonical_source={"version_id": entry.source_version_id},  # type: ignore[arg-type]
            )

    def test_reconstructed_record_cannot_substitute_for_independent_canonical_source(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="reconstructed-not-authority",
            records=records,
            relationships=(relationship,),
        )
        reconstructed = reconstruct_runtime_semantics(package=package)
        entry = rebuild_non_authoritative_projection(package=package).entries[0]
        self.assertNotIsInstance(reconstructed.records[0], CanonicalRecord)
        with self.assertRaises(ProjectionAuthorityBoundaryError):
            pin_runtime_projection_source(
                projection_entry=entry,
                canonical_source=reconstructed.records[0],  # type: ignore[arg-type]
            )

    def test_exact_canonical_source_can_create_governed_pin_after_attribution_check(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="canonical-pin",
            records=records,
            relationships=(relationship,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        entry = projection.entries[0]
        pin = pin_runtime_projection_source(
            projection_entry=entry,
            canonical_source=records[0],
        )
        self.assertEqual(pin.subject_id, records[0].subject_id)
        self.assertEqual(pin.version_id, records[0].version_id)

    def test_stale_or_mismatched_canonical_source_fails_projection_pin_boundary(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="canonical-pin-mismatch",
            records=records,
            relationships=(relationship,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        v2_entry = projection.entries[1]
        with self.assertRaises(ProjectionAuthorityBoundaryError):
            pin_runtime_projection_source(
                projection_entry=v2_entry,
                canonical_source=records[0],
            )

    def test_projection_authority_scope_mismatch_fails_closed(self) -> None:
        record = self._record("subject-a", "subject-a-v1")
        package = export_runtime_semantic_package(
            scenario_id="authority-scope-attribution",
            records=(record,),
        )
        entry = rebuild_non_authoritative_projection(package=package).entries[0]
        forged = replace(entry, authority_scope="different/scope")
        with self.assertRaises(ProjectionAuthorityBoundaryError):
            pin_runtime_projection_source(
                projection_entry=forged,
                canonical_source=record,
            )

    def test_manifest_drift_is_rejected_during_reconstruction(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="manifest-drift",
            records=records,
            relationships=(relationship,),
        )
        document = package.to_mapping()
        document["manifest"]["record_versions"] = document["manifest"]["record_versions"][:-1]
        tampered = SemanticPortabilityPackage(
            serialized=json.dumps(document, sort_keys=True),
        )
        with self.assertRaises(PortabilityRuntimeError):
            reconstruct_runtime_semantics(package=tampered)

    def test_relationship_endpoint_semantic_drift_is_rejected(self) -> None:
        records, relationship = self._relationship_scenario()
        package = export_runtime_semantic_package(
            scenario_id="relationship-drift",
            records=records,
            relationships=(relationship,),
        )
        document = package.to_mapping()
        document["relationships"][0]["source"]["identity"]["value"] = "unknown-version"
        tampered = SemanticPortabilityPackage(serialized=json.dumps(document, sort_keys=True))
        with self.assertRaises(PortabilityRuntimeError):
            reconstruct_runtime_semantics(package=tampered)

    def test_event_execution_version_semantic_drift_is_rejected(self) -> None:
        records, event = self._event_scenario()
        package = export_runtime_semantic_package(
            scenario_id="event-drift",
            records=records,
            events=(event,),
        )
        document = package.to_mapping()
        document["events"][0]["execution_version_id"]["value"] = "unknown-execution-version"
        tampered = SemanticPortabilityPackage(serialized=json.dumps(document, sort_keys=True))
        with self.assertRaises(PortabilityRuntimeError):
            reconstruct_runtime_semantics(package=tampered)

    def test_cross_organization_records_fail_export(self) -> None:
        record = self._record("subject-a", "subject-a-v1")
        other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_org)
        other = CanonicalRecord(
            subject_id=Identity("canonical-subject", "subject-b", "org-b"),
            version_id=Identity("canonical-version", "subject-b-v1", "org-b"),
            semantic_type="example.subject",
            schema_version="1",
            organization=other_org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.subject/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=other_actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "test"),),
            lifecycle_status="Active",
        )
        with self.assertRaises(PortabilityRuntimeError):
            export_runtime_semantic_package(
                scenario_id="cross-org",
                records=(record, other),
            )

    def test_duplicate_version_identity_with_different_content_fails_export(self) -> None:
        record = self._record("subject-a", "subject-a-v1")
        conflicting = replace(record, payload=(("value", "different"),))
        with self.assertRaises(PortabilityRuntimeError):
            export_runtime_semantic_package(
                scenario_id="duplicate-version-conflict",
                records=(record, conflicting),
            )

    def test_serialization_is_deterministic_for_same_semantic_inputs(self) -> None:
        records, relationship = self._relationship_scenario()
        first = export_runtime_semantic_package(
            scenario_id="deterministic",
            records=records,
            relationships=(relationship,),
        )
        second = export_runtime_semantic_package(
            scenario_id="deterministic",
            records=records,
            relationships=(relationship,),
        )
        self.assertEqual(first.serialized, second.serialized)

    def test_export_and_projection_objects_are_immutable(self) -> None:
        record = self._record("subject-a", "subject-a-v1")
        package = export_runtime_semantic_package(
            scenario_id="immutability",
            records=(record,),
        )
        projection = rebuild_non_authoritative_projection(package=package)
        with self.assertRaises(FrozenInstanceError):
            package.serialized = "{}"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            projection.canonical_authority = True  # type: ignore[misc]

    def test_projection_entry_cannot_claim_canonical_authority(self) -> None:
        record = self._record("subject-a", "subject-a-v1")
        with self.assertRaises(ProjectionAuthorityBoundaryError):
            RuntimeProjectionEntry(
                source_kind="canonical-record",
                subject_id=record.subject_id,
                source_version_id=record.version_id,
                semantic_type=record.semantic_type,
                authority_mode=record.authority_mode,
                authority_scope=record.authority_scope,
                lifecycle_status=record.lifecycle_status,
                canonical_authority=True,
            )

    def test_replay_boundary_exposes_no_effect_executor_or_storage_choice(self) -> None:
        signature = inspect.signature(rebuild_non_authoritative_projection)
        self.assertEqual(tuple(signature.parameters), ("package",))
        source = inspect.getsource(portability_runtime_module).lower()
        for forbidden in (
            "sqlite3",
            "psycopg",
            "sqlalchemy",
            "kafka",
            "fastapi",
            "requests.post",
            "execute_consequential",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
