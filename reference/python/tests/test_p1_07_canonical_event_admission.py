from dataclasses import FrozenInstanceError, replace
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.events import (
    CanonicalEvent,
    EventCandidate,
    EventIdentityConflictError,
    admit_p1_07_event,
    build_p1_07_event_candidate,
)
from arvectum_os_ref.execution import start_p1_04_execution
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.mutation import execute_p1_06_canonical_mutation
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P107CanonicalEventAdmissionTests(unittest.TestCase):
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
        awaiting = start_p1_04_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            material_input=self.subject,
        )
        self.authorization = build_p1_05_gate_decision(
            execution=awaiting,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authorization-fixture-v1", "org-a"),
        )
        self.organizational_authority = build_p1_05_gate_decision(
            execution=awaiting,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authority-fixture-v1", "org-a"),
        )
        ready = admit_p1_05_ready_execution(
            execution=awaiting,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
        )
        self.mutation = execute_p1_06_canonical_mutation(
            execution=ready,
            workflow=self.workflow,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
            current_record=self.subject,
            new_version_id=Identity("canonical-version", "subject-1-v2", "org-a"),
            new_payload=(("label", "domain-neutral reference subject updated"),),
        )
        self.candidate = build_p1_07_event_candidate(mutation=self.mutation)

    def _admit(self, **overrides):
        arguments = {
            "candidate": self.candidate,
            "mutation": self.mutation,
            "admitted_events": (),
        }
        arguments.update(overrides)
        return admit_p1_07_event(**arguments)

    def test_receipt_is_not_canonical_event_until_admitted(self) -> None:
        self.assertIsInstance(self.candidate, EventCandidate)
        self.assertNotIsInstance(self.candidate, CanonicalEvent)
        self.assertNotIsInstance(self.candidate, CanonicalRecord)

        result = self._admit()

        self.assertIsInstance(result.event, CanonicalEvent)
        self.assertIsInstance(result.event.record, CanonicalRecord)
        self.assertFalse(result.duplicate_delivery)
        self.assertEqual(len(result.admitted_events), 1)

    def test_admitted_event_is_single_version_native_append_only_history(self) -> None:
        event = self._admit().event

        self.assertNotEqual(event.event_id, event.version_id)
        self.assertIsNone(event.record.predecessor_version_id)
        self.assertEqual(event.record.semantic_type, "platform.event")
        self.assertEqual(event.record.lifecycle_status, "Admitted")
        self.assertIs(event.record.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(event.authoritative_source, "Arvectum OS")
        with self.assertRaises(FrozenInstanceError):
            event.event_type = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            event.record.payload = ()  # type: ignore[misc]

    def test_event_links_exact_terminal_execution_subject_and_version(self) -> None:
        event = self._admit().event
        terminal = self.mutation.execution

        self.assertEqual(event.execution_subject_id, terminal.execution_subject_id)
        self.assertEqual(event.execution_version_id, terminal.execution_version_id)
        self.assertEqual(event.correlation_refs, (terminal.execution_subject_id,))
        self.assertEqual(event.causation_refs, (terminal.execution_version_id,))
        self.assertIn(terminal.execution_version_id, event.record.provenance_refs)

    def test_event_links_exact_resulting_target_subject_and_version(self) -> None:
        event = self._admit().event
        resulting = self.mutation.resulting_record

        self.assertEqual(event.related_subject_ids, (resulting.subject_id,))
        self.assertEqual(event.related_version_ids, (resulting.version_id,))
        self.assertIn(resulting.version_id, event.record.provenance_refs)
        self.assertNotIn(self.subject.version_id, event.related_version_ids)

    def test_event_preserves_occurrence_and_later_admission_time(self) -> None:
        event = self._admit().event

        self.assertEqual(event.occurred_at, self.mutation.resulting_record.created_at)
        self.assertEqual(event.recorded_at, event.record.created_at)
        self.assertGreater(event.recorded_at, event.occurred_at)
        self.assertIsNotNone(event.occurred_at.utcoffset())
        self.assertIsNotNone(event.recorded_at.utcoffset())

    def test_event_type_schema_classification_and_access_are_explicit(self) -> None:
        event = self._admit().event

        self.assertEqual(event.event_type, "platform.canonical-mutation.succeeded")
        self.assertEqual(event.event_schema_version, "1")
        self.assertEqual(event.record.schema_version, "1")
        self.assertEqual(event.classification, "internal")
        self.assertEqual(event.access_scope, "organization")
        self.assertEqual(event.record.authority_scope, "platform.event/canonical-state-change")

    def test_duplicate_delivery_is_idempotent_and_does_not_create_second_occurrence(self) -> None:
        first = self._admit()
        second = self._admit(admitted_events=first.admitted_events)

        self.assertTrue(second.duplicate_delivery)
        self.assertIs(second.event, first.event)
        self.assertEqual(second.admitted_events, first.admitted_events)
        self.assertEqual(len(second.admitted_events), 1)

    def test_duplicate_delivery_does_not_repeat_canonical_mutation_or_change_execution(self) -> None:
        first = self._admit()
        terminal_before = self.mutation.execution
        target_before = self.mutation.resulting_record

        second = self._admit(admitted_events=first.admitted_events)

        self.assertTrue(second.duplicate_delivery)
        self.assertIs(self.mutation.execution, terminal_before)
        self.assertIs(self.mutation.resulting_record, target_before)
        self.assertEqual(target_before.predecessor_version_id, self.subject.version_id)
        self.assertFalse(hasattr(terminal_before, "events"))

    def test_same_event_identity_with_conflicting_payload_is_rejected_without_history_rewrite(self) -> None:
        first = self._admit()
        conflicting = replace(
            self.candidate,
            payload=(("operation", self.mutation.execution.operation_name), ("outcome", "Failed")),
        )

        with self.assertRaises(EventIdentityConflictError):
            self._admit(candidate=conflicting, admitted_events=first.admitted_events)

        self.assertEqual(len(first.admitted_events), 1)
        self.assertEqual(first.admitted_events[0].record.payload, self.candidate.payload)

    def test_same_event_identity_with_conflicting_execution_link_is_rejected(self) -> None:
        first = self._admit()
        conflicting_version = Identity("execution-version", "conflicting-v1", "org-a")
        conflicting = replace(
            self.candidate,
            execution_version_id=conflicting_version,
            causation_refs=(conflicting_version,),
            provenance_refs=(
                self.candidate.producer_id,
                self.candidate.execution_subject_id,
                conflicting_version,
                self.mutation.resulting_record.subject_id,
                self.mutation.resulting_record.version_id,
            ),
        )

        with self.assertRaises(EventIdentityConflictError):
            self._admit(candidate=conflicting, admitted_events=first.admitted_events)

    def test_new_event_with_wrong_terminal_execution_version_fails_closed(self) -> None:
        wrong = replace(
            self.candidate,
            event_id=Identity("event-subject", "other-event", "org-a"),
            version_id=Identity("event-version", "other-event-v1", "org-a"),
            execution_version_id=Identity("execution-version", "wrong-terminal-v1", "org-a"),
            causation_refs=(Identity("execution-version", "wrong-terminal-v1", "org-a"),),
        )

        with self.assertRaises(ValueError):
            self._admit(candidate=wrong)

    def test_new_event_with_wrong_result_version_fails_closed(self) -> None:
        wrong_version = Identity("canonical-version", "subject-1-vX", "org-a")
        wrong = replace(
            self.candidate,
            event_id=Identity("event-subject", "other-event", "org-a"),
            version_id=Identity("event-version", "other-event-v1", "org-a"),
            related_version_ids=(wrong_version,),
            provenance_refs=(
                self.candidate.producer_id,
                self.candidate.execution_subject_id,
                self.candidate.execution_version_id,
                self.mutation.resulting_record.subject_id,
                wrong_version,
            ),
        )

        with self.assertRaises(ValueError):
            self._admit(candidate=wrong)

    def test_cross_organization_event_linkage_is_rejected(self) -> None:
        other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        wrong = replace(
            self.candidate,
            organization=other_org,
            event_id=Identity("event-subject", "other-event", "org-b"),
            version_id=Identity("event-version", "other-event-v1", "org-b"),
            execution_subject_id=Identity("execution-subject", "execution-1", "org-b"),
            execution_version_id=Identity("execution-version", "execution-1-v3", "org-b"),
            related_subject_ids=(Identity("canonical-subject", "subject-1", "org-b"),),
            related_version_ids=(Identity("canonical-version", "subject-1-v2", "org-b"),),
            correlation_refs=(Identity("execution-subject", "execution-1", "org-b"),),
            causation_refs=(Identity("execution-version", "execution-1-v3", "org-b"),),
            provenance_refs=(
                self.candidate.producer_id,
                Identity("execution-subject", "execution-1", "org-b"),
                Identity("execution-version", "execution-1-v3", "org-b"),
                Identity("canonical-subject", "subject-1", "org-b"),
                Identity("canonical-version", "subject-1-v2", "org-b"),
            ),
        )

        with self.assertRaises(ValueError):
            self._admit(candidate=wrong)

    def test_event_version_identity_cannot_be_reused_by_another_event(self) -> None:
        first = self._admit()
        other = replace(
            self.candidate,
            event_id=Identity("event-subject", "other-event", "org-a"),
        )

        with self.assertRaises(EventIdentityConflictError):
            self._admit(candidate=other, admitted_events=first.admitted_events)


if __name__ == "__main__":
    unittest.main()
