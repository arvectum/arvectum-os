from dataclasses import FrozenInstanceError, replace
import unittest

from arvectum_os_ref.canonical import build_p1_02_native_record
from arvectum_os_ref.execution import ExecutionLifecycle, start_p1_04_execution
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.mutation import (
    CanonicalConflictError,
    execute_p1_06_canonical_mutation,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import WorkflowDefinition, build_p1_03_workflow


class P106GovernedCanonicalMutationTests(unittest.TestCase):
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
        self.awaiting_execution = start_p1_04_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            material_input=self.subject,
        )
        self.authorization = build_p1_05_gate_decision(
            execution=self.awaiting_execution,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authorization-fixture-v1", "org-a"),
        )
        self.organizational_authority = build_p1_05_gate_decision(
            execution=self.awaiting_execution,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=Identity("governed-basis", "authority-fixture-v1", "org-a"),
        )
        self.ready_execution = admit_p1_05_ready_execution(
            execution=self.awaiting_execution,
            authorization=self.authorization,
            organizational_authority=self.organizational_authority,
        )
        self.new_version_id = Identity("canonical-version", "subject-1-v2", "org-a")
        self.new_payload = (("label", "domain-neutral reference subject updated"),)

    def _mutate(self, **overrides):
        arguments = {
            "execution": self.ready_execution,
            "workflow": self.workflow,
            "authorization": self.authorization,
            "organizational_authority": self.organizational_authority,
            "current_record": self.subject,
            "new_version_id": self.new_version_id,
            "new_payload": self.new_payload,
        }
        arguments.update(overrides)
        return execute_p1_06_canonical_mutation(**arguments)

    def test_ready_governed_execution_creates_second_immutable_target_version(self) -> None:
        result = self._mutate()
        second = result.resulting_record

        self.assertEqual(second.subject_id, self.subject.subject_id)
        self.assertNotEqual(second.version_id, self.subject.version_id)
        self.assertEqual(second.version_id, self.new_version_id)
        self.assertEqual(second.predecessor_version_id, self.subject.version_id)
        self.assertEqual(second.payload, self.new_payload)
        self.assertEqual(second.semantic_type, self.subject.semantic_type)
        self.assertEqual(second.authority_scope, self.subject.authority_scope)

    def test_first_canonical_version_remains_unchanged_and_immutable(self) -> None:
        original_payload = self.subject.payload
        original_predecessor = self.subject.predecessor_version_id

        self._mutate()

        self.assertEqual(self.subject.version_id.value, "subject-1-v1")
        self.assertEqual(self.subject.payload, original_payload)
        self.assertEqual(self.subject.predecessor_version_id, original_predecessor)
        with self.assertRaises(FrozenInstanceError):
            self.subject.payload = ()  # type: ignore[misc]

    def test_direct_mutation_without_execution_context_fails_closed(self) -> None:
        with self.assertRaises(PermissionError):
            self._mutate(execution=None)

    def test_awaiting_gate_execution_cannot_mutate_canonical_state(self) -> None:
        with self.assertRaises(PermissionError):
            self._mutate(execution=self.awaiting_execution)

    def test_p1_06_consumes_exact_pinned_workflow_version(self) -> None:
        later_workflow_record = replace(
            self.workflow.record,
            version_id=Identity(
                "workflow-version",
                "reference-subject-maintenance-v2",
                "org-a",
            ),
            predecessor_version_id=self.workflow.workflow_version_id,
        )
        later_workflow = WorkflowDefinition(
            record=later_workflow_record,
            operations=self.workflow.operations,
        )

        with self.assertRaises(ValueError):
            self._mutate(workflow=later_workflow)

    def test_p1_06_consumes_exact_authorization_decision_version(self) -> None:
        different_authorization = replace(
            self.authorization,
            record=replace(
                self.authorization.record,
                version_id=Identity(
                    "authorization-decision-version",
                    "different-authorization-v1",
                    "org-a",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self._mutate(authorization=different_authorization)

    def test_p1_06_consumes_exact_organizational_authority_decision_version(self) -> None:
        different_authority = replace(
            self.organizational_authority,
            record=replace(
                self.organizational_authority.record,
                version_id=Identity(
                    "organizational-authority-decision-version",
                    "different-authority-v1",
                    "org-a",
                ),
            ),
        )

        with self.assertRaises(ValueError):
            self._mutate(organizational_authority=different_authority)

    def test_conflicting_current_version_does_not_silently_overwrite_newer_state(self) -> None:
        later_current = replace(
            self.subject,
            version_id=Identity("canonical-version", "subject-1-vX", "org-a"),
            predecessor_version_id=self.subject.version_id,
        )

        with self.assertRaises(CanonicalConflictError):
            self._mutate(current_record=later_current)

    def test_new_version_identity_must_be_distinct_and_in_same_organization_scope(self) -> None:
        with self.assertRaises(ValueError):
            self._mutate(new_version_id=self.subject.version_id)
        with self.assertRaises(ValueError):
            self._mutate(
                new_version_id=Identity("canonical-version", "subject-1-v2", "org-b")
            )

    def test_bounded_mutation_rejects_noop_payload(self) -> None:
        with self.assertRaises(ValueError):
            self._mutate(new_payload=self.subject.payload)

    def test_result_provenance_preserves_exact_execution_workflow_input_and_gate_versions(self) -> None:
        result = self._mutate()
        refs = result.resulting_record.provenance_refs

        self.assertIn(self.ready_execution.execution_version_id, refs)
        self.assertIn(self.workflow.workflow_version_id, refs)
        self.assertIn(self.subject.version_id, refs)
        self.assertIn(self.authorization.record.version_id, refs)
        self.assertIn(self.organizational_authority.record.version_id, refs)

    def test_mutation_creates_terminal_execution_version_with_exact_effect_pin(self) -> None:
        result = self._mutate()
        terminal = result.execution

        self.assertEqual(terminal.execution_subject_id, self.ready_execution.execution_subject_id)
        self.assertNotEqual(terminal.execution_version_id, self.ready_execution.execution_version_id)
        self.assertEqual(
            terminal.record.predecessor_version_id,
            self.ready_execution.execution_version_id,
        )
        self.assertEqual(terminal.record.lifecycle_status, ExecutionLifecycle.SUCCEEDED.value)
        self.assertEqual(terminal.workflow, self.ready_execution.workflow)
        self.assertEqual(terminal.material_inputs, self.ready_execution.material_inputs)
        self.assertEqual(terminal.gate_decisions, self.ready_execution.gate_decisions)
        self.assertEqual(len(terminal.canonical_effects), 1)
        self.assertEqual(terminal.canonical_effects[0].version_id, self.new_version_id)
        with self.assertRaises(FrozenInstanceError):
            terminal.canonical_effects = ()  # type: ignore[misc]

    def test_p1_06_does_not_preempt_p1_07_event_admission(self) -> None:
        result = self._mutate()

        self.assertFalse(hasattr(result, "event"))
        self.assertFalse(hasattr(result.execution, "events"))


if __name__ == "__main__":
    unittest.main()
