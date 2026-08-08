from dataclasses import FrozenInstanceError
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.execution import (
    ExecutionContext,
    ExecutionLifecycle,
    GovernedVersionPin,
    start_p1_04_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import WorkflowDefinition, build_p1_03_workflow


class P104ExecutionContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.subject = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )
        self.workflow = build_p1_03_workflow(
            organization=self.organization,
            actor=self.actor,
            target_record=self.subject,
        )
        self.execution = start_p1_04_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            material_input=self.subject,
        )

    def test_execution_has_stable_subject_and_distinct_initial_version_identity(self) -> None:
        self.assertEqual(self.execution.execution_subject_id.namespace, "execution-subject")
        self.assertEqual(self.execution.execution_version_id.namespace, "execution-version")
        self.assertNotEqual(self.execution.execution_subject_id, self.execution.execution_version_id)
        self.assertEqual(self.execution.execution_subject_id.scope, "org-a")
        self.assertEqual(self.execution.execution_version_id.scope, "org-a")

    def test_execution_context_is_native_canonical_record_and_awaits_future_gates(self) -> None:
        self.assertIsInstance(self.execution.record, CanonicalRecord)
        self.assertEqual(self.execution.record.semantic_type, "platform.execution-context")
        self.assertIs(self.execution.record.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(
            self.execution.record.lifecycle_status,
            ExecutionLifecycle.AWAITING_GATE.value,
        )
        self.assertEqual(self.execution.organization, self.organization)
        self.assertEqual(self.execution.initiating_actor, self.actor)
        self.assertIsNone(self.execution.record.predecessor_version_id)

    def test_execution_pins_exact_workflow_and_material_input_versions(self) -> None:
        self.assertEqual(self.execution.workflow.subject_id, self.workflow.workflow_subject_id)
        self.assertEqual(self.execution.workflow.version_id, self.workflow.workflow_version_id)
        self.assertEqual(self.execution.operation_name, "update-reference-subject")
        self.assertEqual(len(self.execution.material_inputs), 1)
        material = self.execution.material_inputs[0]
        self.assertEqual(material.subject_id, self.subject.subject_id)
        self.assertEqual(material.version_id, self.subject.version_id)
        self.assertIn(self.workflow.workflow_version_id, self.execution.record.provenance_refs)
        self.assertIn(self.subject.version_id, self.execution.record.provenance_refs)

    def test_exact_pin_does_not_follow_later_version_with_same_subject_identity(self) -> None:
        later = CanonicalRecord(
            subject_id=self.subject.subject_id,
            version_id=Identity("canonical-version", "subject-1-v2", "org-a"),
            semantic_type=self.subject.semantic_type,
            schema_version=self.subject.schema_version,
            organization=self.organization,
            authority_mode=self.subject.authority_mode,
            authority_scope=self.subject.authority_scope,
            accountable_owner_id=self.subject.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self.execution.record.created_at,
            provenance_refs=(self.subject.version_id,),
            integrity_metadata=self.subject.integrity_metadata,
            payload=(("label", "later candidate"),),
            lifecycle_status="established",
            predecessor_version_id=self.subject.version_id,
        )
        self.assertEqual(later.subject_id, self.execution.material_inputs[0].subject_id)
        self.assertNotEqual(later.version_id, self.execution.material_inputs[0].version_id)
        self.assertEqual(self.execution.material_inputs[0].version_id, self.subject.version_id)

    def test_exact_workflow_pin_does_not_follow_later_workflow_version(self) -> None:
        later_workflow_record = CanonicalRecord(
            subject_id=self.workflow.workflow_subject_id,
            version_id=Identity("workflow-version", "reference-subject-maintenance-v2", "org-a"),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self.execution.record.created_at,
            provenance_refs=(self.workflow.workflow_version_id,),
            integrity_metadata=self.workflow.record.integrity_metadata,
            lifecycle_status="Approved",
            predecessor_version_id=self.workflow.workflow_version_id,
        )
        later_workflow = WorkflowDefinition(
            record=later_workflow_record,
            operations=self.workflow.operations,
        )
        self.assertEqual(later_workflow.workflow_subject_id, self.execution.workflow.subject_id)
        self.assertNotEqual(later_workflow.workflow_version_id, self.execution.workflow.version_id)
        self.assertEqual(self.execution.workflow.version_id, self.workflow.workflow_version_id)

    def test_workflow_version_and_execution_context_remain_distinct_governed_subjects(self) -> None:
        self.assertNotEqual(self.execution.execution_subject_id, self.workflow.workflow_subject_id)
        self.assertNotEqual(self.execution.execution_version_id, self.workflow.workflow_version_id)

    def test_start_fails_closed_for_scope_or_operation_mismatch(self) -> None:
        other_organization = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_organization)
        other_subject = build_p1_02_native_record(
            organization=other_organization,
            actor=other_actor,
        )
        with self.assertRaises(ValueError):
            start_p1_04_execution(
                organization=self.organization,
                actor=self.actor,
                workflow=self.workflow,
                material_input=other_subject,
            )

        unrelated = CanonicalRecord(
            subject_id=Identity("canonical-subject", "other", "org-a"),
            version_id=Identity("canonical-version", "other-v1", "org-a"),
            semantic_type="other.subject",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="other.subject/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self.subject.created_at,
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=self.subject.integrity_metadata,
        )
        with self.assertRaises(ValueError):
            start_p1_04_execution(
                organization=self.organization,
                actor=self.actor,
                workflow=self.workflow,
                material_input=unrelated,
            )

    def test_execution_and_pins_are_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.execution.operation_name = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            self.execution.material_inputs[0].version_id = Identity(  # type: ignore[misc]
                "canonical-version",
                "changed",
                "org-a",
            )

    def test_execution_context_does_not_preempt_authority_gates_or_mutation(self) -> None:
        self.assertFalse(hasattr(self.execution, "authorization_granted"))
        self.assertFalse(hasattr(self.execution, "organizational_authority"))
        self.assertFalse(hasattr(self.execution, "approval_granted"))
        self.assertEqual(self.subject.version_id.value, "subject-1-v1")
        self.assertIsNone(self.subject.predecessor_version_id)

    def test_invalid_governed_version_pin_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            GovernedVersionPin(
                subject_id=self.subject.subject_id,
                version_id=self.subject.subject_id,
                semantic_type=self.subject.semantic_type,
                authority_scope=self.subject.authority_scope,
            )
        with self.assertRaises(ValueError):
            GovernedVersionPin(
                subject_id=self.subject.subject_id,
                version_id=Identity("canonical-version", "subject-1-v1", "org-b"),
                semantic_type=self.subject.semantic_type,
                authority_scope=self.subject.authority_scope,
            )


if __name__ == "__main__":
    unittest.main()
