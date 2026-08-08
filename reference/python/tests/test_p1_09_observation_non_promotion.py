from dataclasses import FrozenInstanceError, replace
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.events import admit_p1_07_event, build_p1_07_event_candidate
from arvectum_os_ref.execution import GovernedVersionPin, start_p1_04_execution
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.mutation import execute_p1_06_canonical_mutation
from arvectum_os_ref.observation import (
    KnowledgePromotionRequiredError,
    Observation,
    ObservationCreationError,
    ObservationEpistemicStatus,
    build_p1_09_observation,
    require_explicit_knowledge_promotion,
)
from arvectum_os_ref.provenance import build_p1_08_reconstruction_evidence
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P109ObservationNonPromotionTests(unittest.TestCase):
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
        self.event = admit_p1_07_event(
            candidate=candidate,
            mutation=self.mutation,
        ).event
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

    def _build(self, **overrides):
        arguments = {
            "evidence": self.evidence,
            "event": self.event,
            "mutation": self.mutation,
        }
        arguments.update(overrides)
        return build_p1_09_observation(**arguments)

    def test_significant_observation_uses_canonical_record_without_new_kernel_primitive(self) -> None:
        observation = self._build()

        self.assertIsInstance(observation, Observation)
        self.assertIsInstance(observation.record, CanonicalRecord)
        self.assertEqual(observation.record.semantic_type, "platform.observation")
        self.assertEqual(observation.record.schema_version, "1")
        self.assertIs(observation.record.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(observation.record.authority_scope, "platform.learning/observation")
        self.assertEqual(observation.record.organization, self.organization)
        self.assertEqual(observation.record.lifecycle_status, "Captured")
        self.assertIsNone(observation.record.predecessor_version_id)

    def test_observation_is_explicitly_unvalidated_not_knowledge(self) -> None:
        observation = self._build()

        self.assertIs(observation.epistemic_status, ObservationEpistemicStatus.UNVALIDATED)
        self.assertIn(
            ("epistemic-status", ObservationEpistemicStatus.UNVALIDATED.value),
            observation.record.integrity_metadata,
        )
        self.assertIn(("knowledge-promotion", "not-performed"), observation.record.integrity_metadata)
        self.assertNotEqual(observation.record.semantic_type, "platform.knowledge")

    def test_observation_pins_exact_event_execution_and_effect_versions(self) -> None:
        observation = self._build()

        self.assertEqual(observation.source_event, GovernedVersionPin.from_record(self.event.record))
        self.assertEqual(
            observation.source_execution,
            GovernedVersionPin.from_record(self.mutation.execution.record),
        )
        self.assertEqual(
            observation.observed_effect,
            GovernedVersionPin.from_record(self.mutation.resulting_record),
        )

    def test_observation_preserves_reconstruction_evidence_in_provenance(self) -> None:
        observation = self._build()

        for expected in self.evidence.provenance_refs:
            self.assertIn(expected, observation.evidence_refs)
            self.assertIn(expected, observation.record.provenance_refs)
        for expected in (
            self.event.record.subject_id,
            self.event.record.version_id,
            self.mutation.execution.record.subject_id,
            self.mutation.execution.record.version_id,
            self.mutation.resulting_record.subject_id,
            self.mutation.resulting_record.version_id,
        ):
            self.assertIn(expected, observation.record.provenance_refs)
        self.assertEqual(
            len(observation.record.provenance_refs),
            len(set(observation.record.provenance_refs)),
        )

    def test_validated_knowledge_reliance_fails_without_explicit_promotion(self) -> None:
        observation = self._build()

        with self.assertRaisesRegex(KnowledgePromotionRequiredError, "explicit RFC-0007 promotion"):
            require_explicit_knowledge_promotion(observation)

    def test_creation_does_not_change_standard_workflow_or_production_behavior(self) -> None:
        workflow_before = self.workflow
        subject_before = self.subject
        result_before = self.mutation.resulting_record
        terminal_before = self.mutation.execution
        event_before = self.event

        observation = self._build()

        self.assertIs(self.workflow, workflow_before)
        self.assertIs(self.subject, subject_before)
        self.assertIs(self.mutation.resulting_record, result_before)
        self.assertIs(self.mutation.execution, terminal_before)
        self.assertIs(self.event, event_before)
        self.assertEqual(self.workflow.record.lifecycle_status, workflow_before.record.lifecycle_status)
        self.assertEqual(self.mutation.execution.record.lifecycle_status, "Succeeded")
        self.assertEqual(self.event.record.lifecycle_status, "Admitted")
        self.assertEqual(observation.record.lifecycle_status, "Captured")

    def test_repeated_capture_is_deterministic_and_observational(self) -> None:
        result_before = self.mutation.resulting_record
        terminal_before = self.mutation.execution
        event_before = self.event

        first = self._build()
        second = self._build()

        self.assertEqual(first, second)
        self.assertEqual(first.observation_id, second.observation_id)
        self.assertEqual(first.version_id, second.version_id)
        self.assertIs(self.mutation.resulting_record, result_before)
        self.assertIs(self.mutation.execution, terminal_before)
        self.assertIs(self.event, event_before)

    def test_observation_is_frozen_immutable_governed_state(self) -> None:
        observation = self._build()

        with self.assertRaises(FrozenInstanceError):
            observation.epistemic_status = ObservationEpistemicStatus.UNVALIDATED  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            observation.record.payload = ()  # type: ignore[misc]

    def test_wrong_event_version_fails_closed(self) -> None:
        wrong_event_pin = replace(
            self.evidence.events[0],
            version_id=Identity("event-version", "wrong-event-v1", "org-a"),
        )
        forged_evidence = replace(self.evidence, events=(wrong_event_pin,))

        with self.assertRaises(ObservationCreationError):
            self._build(evidence=forged_evidence)

    def test_wrong_terminal_execution_version_fails_closed(self) -> None:
        wrong_terminal_pin = replace(
            self.evidence.execution_versions[-1],
            version_id=Identity("execution-version", "wrong-terminal-v1", "org-a"),
        )
        forged_evidence = replace(
            self.evidence,
            execution_versions=(
                self.evidence.execution_versions[0],
                self.evidence.execution_versions[1],
                wrong_terminal_pin,
            ),
        )

        with self.assertRaises(ObservationCreationError):
            self._build(evidence=forged_evidence)

    def test_wrong_observed_effect_version_fails_closed(self) -> None:
        wrong_effect_pin = replace(
            self.evidence.canonical_effects[0],
            version_id=Identity("canonical-version", "subject-1-vX", "org-a"),
        )
        forged_evidence = replace(self.evidence, canonical_effects=(wrong_effect_pin,))

        with self.assertRaises(ObservationCreationError):
            self._build(evidence=forged_evidence)

    def test_changed_event_semantics_fail_closed(self) -> None:
        forged_event = replace(self.event, event_type="platform.canonical-mutation.failed")

        with self.assertRaises(ObservationCreationError):
            self._build(event=forged_event)

    def test_incomplete_reconstruction_provenance_fails_closed(self) -> None:
        incomplete = tuple(
            ref for ref in self.evidence.provenance_refs if ref != self.event.record.version_id
        )
        forged_evidence = replace(self.evidence, provenance_refs=incomplete)

        with self.assertRaises(ObservationCreationError):
            self._build(evidence=forged_evidence)

    def test_observation_cannot_be_relabelled_as_validated_by_field_replacement(self) -> None:
        observation = self._build()

        with self.assertRaises(ObservationCreationError):
            replace(observation, epistemic_status="Validated")


if __name__ == "__main__":
    unittest.main()
