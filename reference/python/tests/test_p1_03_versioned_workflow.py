from dataclasses import FrozenInstanceError
import unittest

from arvectum_os_ref import (
    ActorContext,
    Identity,
    OperationSideEffectClass,
    OrganizationScope,
    Principal,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
    build_p1_02_native_record,
    build_p1_03_workflow,
)
from arvectum_os_ref.canonical import CanonicalRecord


class P103VersionedWorkflowTests(unittest.TestCase):
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

    def test_workflow_has_stable_subject_and_distinct_exact_version_identity(self) -> None:
        self.assertEqual(self.workflow.workflow_subject_id.namespace, "workflow-subject")
        self.assertEqual(self.workflow.workflow_subject_id.value, "reference-subject-maintenance")
        self.assertEqual(self.workflow.workflow_version_id.namespace, "workflow-version")
        self.assertEqual(self.workflow.workflow_version_id.value, "reference-subject-maintenance-v1")
        self.assertNotEqual(self.workflow.workflow_subject_id, self.workflow.workflow_version_id)
        self.assertEqual(self.workflow.workflow_subject_id.scope, "org-a")
        self.assertEqual(self.workflow.workflow_version_id.scope, "org-a")

    def test_workflow_is_governed_by_an_immutable_canonical_record_envelope(self) -> None:
        self.assertIsInstance(self.workflow.record, CanonicalRecord)
        self.assertEqual(self.workflow.record.semantic_type, "platform.workflow")
        self.assertEqual(self.workflow.record.lifecycle_status, WorkflowLifecycle.APPROVED.value)
        self.assertEqual(self.workflow.record.organization, self.organization)
        self.assertEqual(self.workflow.record.accountable_owner_id, self.principal.principal_id)
        self.assertIn(self.subject.subject_id, self.workflow.record.provenance_refs)
        self.assertIsNone(self.workflow.record.predecessor_version_id)

    def test_workflow_declares_canonical_mutation_for_reference_subject(self) -> None:
        self.assertTrue(self.workflow.declares_canonical_mutation_for(self.subject))
        self.assertFalse(
            self.workflow.declares_canonical_mutation_for(
                CanonicalRecord(
                    subject_id=Identity("canonical-subject", "other", "org-a"),
                    version_id=Identity("canonical-version", "other-v1", "org-a"),
                    semantic_type="other.subject",
                    schema_version="1",
                    organization=self.organization,
                    authority_mode=self.subject.authority_mode,
                    authority_scope="other.subject/state",
                    accountable_owner_id=self.subject.accountable_owner_id,
                    creation_actor=self.actor,
                    created_at=self.subject.created_at,
                    provenance_refs=self.subject.provenance_refs,
                    integrity_metadata=self.subject.integrity_metadata,
                )
            )
        )
        operation = self.workflow.operations[0]
        self.assertEqual(operation.semantic_name, "update-reference-subject")
        self.assertEqual(operation.target_subject_id, self.subject.subject_id)
        self.assertEqual(operation.target_semantic_type, self.subject.semantic_type)
        self.assertEqual(operation.side_effect_classes, (OperationSideEffectClass.CANONICAL_MUTATION,))

    def test_workflow_declaration_does_not_grant_authorization_or_organizational_authority(self) -> None:
        self.assertFalse(hasattr(self.workflow, "authorization_granted"))
        self.assertFalse(hasattr(self.workflow, "organizational_authority"))
        self.assertFalse(hasattr(self.workflow.operations[0], "authorized"))
        self.assertFalse(hasattr(self.workflow.operations[0], "approved"))

    def test_workflow_version_and_operation_definition_are_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.workflow.record.version_id = Identity("workflow-version", "changed", "org-a")  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            self.workflow.operations[0].semantic_name = "changed"  # type: ignore[misc]

    def test_workflow_and_target_scope_mismatch_fails_closed(self) -> None:
        other_organization = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_organization)
        other_subject = build_p1_02_native_record(
            organization=other_organization,
            actor=other_actor,
        )
        with self.assertRaises(ValueError):
            build_p1_03_workflow(
                organization=self.organization,
                actor=self.actor,
                target_record=other_subject,
            )

    def test_invalid_workflow_definition_and_operation_shape_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            WorkflowOperation(
                semantic_name="",
                target_subject_id=self.subject.subject_id,
                target_semantic_type=self.subject.semantic_type,
                side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
            )
        with self.assertRaises(ValueError):
            WorkflowOperation(
                semantic_name="duplicate-effects",
                target_subject_id=self.subject.subject_id,
                target_semantic_type=self.subject.semantic_type,
                side_effect_classes=(
                    OperationSideEffectClass.CANONICAL_MUTATION,
                    OperationSideEffectClass.CANONICAL_MUTATION,
                ),
            )
        with self.assertRaises(ValueError):
            WorkflowDefinition(record=self.subject, operations=self.workflow.operations)


if __name__ == "__main__":
    unittest.main()
