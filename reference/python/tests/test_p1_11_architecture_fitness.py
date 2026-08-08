from dataclasses import replace
import json
from unittest.mock import patch
import unittest

from arvectum_os_ref.canonical import build_p1_02_native_record
from arvectum_os_ref.events import admit_p1_07_event, build_p1_07_event_candidate
from arvectum_os_ref.execution import start_p1_04_execution
from arvectum_os_ref.fitness import (
    ProjectionAuthorityError,
    ProjectionEntry,
    ReplayProjectionError,
    pin_p1_11_projection_source,
    rebuild_p1_11_projection,
)
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.mutation import execute_p1_06_canonical_mutation
from arvectum_os_ref.observation import build_p1_09_observation
from arvectum_os_ref.portability import PortableSemanticFixture, export_p1_10_semantic_fixture
from arvectum_os_ref.provenance import build_p1_08_reconstruction_evidence
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P111NegativePathArchitectureFitnessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_principal = Principal(Identity("principal", "principal-2", "platform"))
        self.decision_actor = ActorContext(self.decision_principal, self.organization)
        self.subject = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )
        self.workflow = build_p1_03_workflow(
            organization=self.organization,
            actor=self.actor,
            target_record=self.subject,
        )
        self.awaiting = start_p1_04_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            material_input=self.subject,
        )
        self.authorization = build_p1_05_gate_decision(
            execution=self.awaiting,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authorization-fixture-v1", "org-a"),
        )
        self.organizational_authority = build_p1_05_gate_decision(
            execution=self.awaiting,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authority-fixture-v1", "org-a"),
        )
        self.ready = admit_p1_05_ready_execution(
            execution=self.awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
        )
        self.mutation = execute_p1_06_canonical_mutation(
            execution=self.ready,
            workflow=self.workflow,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            current_record=self.subject,
            new_version_id=Identity("canonical-version", "subject-1-v2", "org-a"),
            new_payload=(("label", "domain-neutral reference subject updated"),),
        )
        candidate = build_p1_07_event_candidate(mutation=self.mutation)
        self.event = admit_p1_07_event(candidate=candidate, mutation=self.mutation).event
        self.evidence = build_p1_08_reconstruction_evidence(
            input_record=self.subject,
            workflow=self.workflow,
            awaiting_execution=self.awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            ready_execution=self.ready,
            mutation=self.mutation,
            event=self.event,
        )
        self.observation = build_p1_09_observation(
            evidence=self.evidence,
            event=self.event,
            mutation=self.mutation,
        )
        self.fixture = export_p1_10_semantic_fixture(
            input_record=self.subject,
            workflow=self.workflow,
            awaiting_execution=self.awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            ready_execution=self.ready,
            mutation=self.mutation,
            event=self.event,
            evidence=self.evidence,
            observation=self.observation,
        )

    def _tampered_fixture(self, mutator) -> PortableSemanticFixture:
        document = self.fixture.to_mapping()
        mutator(document)
        return PortableSemanticFixture(
            serialized=json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        )

    @staticmethod
    def _entry(snapshot, role: str) -> ProjectionEntry:
        matches = [entry for entry in snapshot.entries if entry.source_role == role]
        if len(matches) != 1:
            raise AssertionError(f"expected exactly one projection entry for {role}")
        return matches[0]

    def test_replay_rebuilds_only_non_authoritative_projection(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)

        self.assertEqual(snapshot.replay_mode, "projection-rebuild")
        self.assertFalse(snapshot.canonical_authority)
        self.assertEqual(snapshot.consequential_side_effects_created, 0)
        self.assertEqual(len(snapshot.entries), 10)
        self.assertEqual(
            snapshot.source_record_versions,
            tuple(entry.source_version_id for entry in snapshot.entries),
        )
        self.assertTrue(all(not entry.canonical_authority for entry in snapshot.entries))

    def test_historical_replay_does_not_reinvoke_known_consequential_boundaries(self) -> None:
        with patch(
            "arvectum_os_ref.mutation.execute_p1_06_canonical_mutation",
            side_effect=AssertionError("replay must not execute canonical mutation"),
        ), patch(
            "arvectum_os_ref.events.admit_p1_07_event",
            side_effect=AssertionError("replay must not re-admit historical Event"),
        ):
            snapshot = rebuild_p1_11_projection(fixture=self.fixture)

        self.assertEqual(snapshot.consequential_side_effects_created, 0)
        self.assertEqual(
            self._entry(snapshot, "canonical-event").source_version_id,
            self.event.record.version_id,
        )
        self.assertEqual(
            self._entry(snapshot, "canonical-result-v2").source_version_id,
            self.mutation.resulting_record.version_id,
        )

    def test_replay_is_deterministic_and_observational(self) -> None:
        source_serialized = self.fixture.serialized
        source_state = (
            self.subject,
            self.workflow,
            self.awaiting,
            self.authorization,
            self.organizational_authority,
            self.ready,
            self.mutation,
            self.event,
            self.evidence,
            self.observation,
        )

        first = rebuild_p1_11_projection(fixture=self.fixture)
        second = rebuild_p1_11_projection(fixture=self.fixture)

        self.assertEqual(first, second)
        self.assertEqual(self.fixture.serialized, source_serialized)
        self.assertEqual(
            source_state,
            (
                self.subject,
                self.workflow,
                self.awaiting,
                self.authorization,
                self.organizational_authority,
                self.ready,
                self.mutation,
                self.event,
                self.evidence,
                self.observation,
            ),
        )

    def test_replay_rejects_fixture_that_stops_declaring_derived_representation(self) -> None:
        fixture = self._tampered_fixture(
            lambda document: document["fixture"].__setitem__("derived_representation", False)
        )

        with self.assertRaisesRegex(ReplayProjectionError, "derived representation"):
            rebuild_p1_11_projection(fixture=fixture)

    def test_replay_rejects_derived_link_reinterpreted_as_canonical_relationship(self) -> None:
        def mutate(document) -> None:
            document["semantic_links"][0]["canonical_typed_relationship"] = True

        fixture = self._tampered_fixture(mutate)

        with self.assertRaisesRegex(ReplayProjectionError, "canonical Typed Relationships"):
            rebuild_p1_11_projection(fixture=fixture)

    def test_replay_rejects_manifest_record_version_drift(self) -> None:
        def mutate(document) -> None:
            document["manifest"]["record_versions"][0] = {
                "namespace": "canonical-version",
                "value": "stale-or-unrelated-version",
                "scope": "org-a",
            }

        fixture = self._tampered_fixture(mutate)

        with self.assertRaisesRegex(ReplayProjectionError, "exact manifest Version Identity"):
            rebuild_p1_11_projection(fixture=fixture)

    def test_projection_lookup_exposes_all_source_versions_without_resolving_authority(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        entries = snapshot.entries_for_subject(self.subject.subject_id)

        self.assertEqual(len(entries), 2)
        self.assertEqual(
            {entry.source_version_id for entry in entries},
            {self.subject.version_id, self.mutation.resulting_record.version_id},
        )
        self.assertTrue(all(not entry.canonical_authority for entry in entries))

    def test_projection_entry_cannot_be_relabelled_as_canonical_authority(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        entry = self._entry(snapshot, "canonical-result-v2")

        with self.assertRaisesRegex(ProjectionAuthorityError, "cannot claim canonical authority"):
            replace(entry, canonical_authority=True)

    def test_projection_replay_cannot_claim_consequential_side_effect(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)

        with self.assertRaisesRegex(ReplayProjectionError, "must not claim or create"):
            replace(snapshot, consequential_side_effects_created=1)

    def test_projection_result_cannot_substitute_for_governed_execution_input_pin(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        entry = self._entry(snapshot, "material-input-v1")

        with self.assertRaisesRegex(ValueError, "GovernedVersionPin"):
            replace(self.awaiting, material_inputs=(entry,))

    def test_projection_cannot_mint_governed_pin_without_exact_canonical_source(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        entry = self._entry(snapshot, "canonical-result-v2")

        with self.assertRaisesRegex(ProjectionAuthorityError, "exact CanonicalRecord"):
            pin_p1_11_projection_source(
                projection_entry=entry,
                canonical_source=entry,
            )

    def test_stale_canonical_version_cannot_validate_newer_projection_entry(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        result_entry = self._entry(snapshot, "canonical-result-v2")

        with self.assertRaisesRegex(ProjectionAuthorityError, "Version Identity"):
            pin_p1_11_projection_source(
                projection_entry=result_entry,
                canonical_source=self.subject,
            )

    def test_exact_canonical_source_is_required_for_consequential_version_pin(self) -> None:
        snapshot = rebuild_p1_11_projection(fixture=self.fixture)
        result_entry = self._entry(snapshot, "canonical-result-v2")

        pin = pin_p1_11_projection_source(
            projection_entry=result_entry,
            canonical_source=self.mutation.resulting_record,
        )

        self.assertEqual(pin.subject_id, self.mutation.resulting_record.subject_id)
        self.assertEqual(pin.version_id, self.mutation.resulting_record.version_id)
        self.assertEqual(pin.semantic_type, self.mutation.resulting_record.semantic_type)
        self.assertEqual(pin.authority_scope, self.mutation.resulting_record.authority_scope)


if __name__ == "__main__":
    unittest.main()
