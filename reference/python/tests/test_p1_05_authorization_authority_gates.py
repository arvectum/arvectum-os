from dataclasses import FrozenInstanceError, replace
import unittest

from arvectum_os_ref.canonical import CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.execution import (
    ExecutionContext,
    ExecutionLifecycle,
    GovernedVersionPin,
    start_p1_04_execution,
)
from arvectum_os_ref.gates import (
    GateKind,
    GateOutcome,
    admit_p1_05_ready_execution,
    build_p1_05_gate_decision,
    evaluate_p1_05_gates,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P105AuthorizationAuthorityGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.authentication_evidence = Identity("authentication-evidence", "auth-1", "org-a")
        self.actor = ActorContext(
            self.principal,
            self.organization,
            authentication_evidence_refs=(self.authentication_evidence,),
        )
        self.decision_principal = Principal(Identity("principal", "principal-2", "platform"))
        self.decision_actor = ActorContext(self.decision_principal, self.organization)
        self.authorization_basis = Identity("governed-basis", "authorization-fixture-v1", "org-a")
        self.authority_basis = Identity("governed-basis", "authority-fixture-v1", "org-a")
        self.subject = build_p1_02_native_record(organization=self.organization, actor=self.actor)
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
        self.authorization_allow = build_p1_05_gate_decision(
            execution=self.execution,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=self.authorization_basis,
        )
        self.authority_allow = build_p1_05_gate_decision(
            execution=self.execution,
            kind=GateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=self.authority_basis,
        )

    def test_authentication_actor_attribution_does_not_imply_authorization(self) -> None:
        self.assertIn(self.authentication_evidence, self.execution.initiating_actor.authentication_evidence_refs)
        evaluation = evaluate_p1_05_gates(execution=self.execution)
        self.assertFalse(evaluation.authorization_allowed)
        self.assertFalse(evaluation.organizational_authority_allowed)
        self.assertFalse(evaluation.can_proceed)
        self.assertEqual(
            evaluation.unresolved_gates,
            (GateKind.AUTHORIZATION, GateKind.ORGANIZATIONAL_AUTHORITY),
        )
        with self.assertRaises(PermissionError):
            admit_p1_05_ready_execution(execution=self.execution)

    def test_authorization_allow_does_not_imply_organizational_authority(self) -> None:
        evaluation = evaluate_p1_05_gates(
            execution=self.execution,
            authorization=self.authorization_allow,
        )
        self.assertTrue(evaluation.authorization_allowed)
        self.assertFalse(evaluation.organizational_authority_allowed)
        self.assertFalse(evaluation.can_proceed)
        self.assertEqual(evaluation.unresolved_gates, (GateKind.ORGANIZATIONAL_AUTHORITY,))
        with self.assertRaises(PermissionError):
            admit_p1_05_ready_execution(
                execution=self.execution,
                authorization=self.authorization_allow,
            )

    def test_organizational_authority_allow_does_not_imply_authorization(self) -> None:
        evaluation = evaluate_p1_05_gates(
            execution=self.execution,
            organizational_authority=self.authority_allow,
        )
        self.assertFalse(evaluation.authorization_allowed)
        self.assertTrue(evaluation.organizational_authority_allowed)
        self.assertFalse(evaluation.can_proceed)
        with self.assertRaises(PermissionError):
            admit_p1_05_ready_execution(
                execution=self.execution,
                organizational_authority=self.authority_allow,
            )

    def test_explicit_deny_blocks_ready_transition(self) -> None:
        authorization_deny = build_p1_05_gate_decision(
            execution=self.execution,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.DENY,
            decision_actor=self.decision_actor,
            basis_ref=self.authorization_basis,
        )
        evaluation = evaluate_p1_05_gates(
            execution=self.execution,
            authorization=authorization_deny,
            organizational_authority=self.authority_allow,
        )
        self.assertFalse(evaluation.authorization_allowed)
        self.assertTrue(evaluation.organizational_authority_allowed)
        self.assertFalse(evaluation.can_proceed)
        self.assertEqual(evaluation.unresolved_gates, ())
        with self.assertRaises(PermissionError):
            admit_p1_05_ready_execution(
                execution=self.execution,
                authorization=authorization_deny,
                organizational_authority=self.authority_allow,
            )

    def test_two_independent_allows_create_new_ready_execution_version(self) -> None:
        ready = admit_p1_05_ready_execution(
            execution=self.execution,
            authorization=self.authorization_allow,
            organizational_authority=self.authority_allow,
        )
        self.assertEqual(ready.record.lifecycle_status, ExecutionLifecycle.READY.value)
        self.assertEqual(ready.execution_subject_id, self.execution.execution_subject_id)
        self.assertNotEqual(ready.execution_version_id, self.execution.execution_version_id)
        self.assertEqual(ready.record.predecessor_version_id, self.execution.execution_version_id)
        self.assertEqual(self.execution.record.lifecycle_status, ExecutionLifecycle.AWAITING_GATE.value)

    def test_ready_transition_preserves_exact_workflow_and_material_input_pins(self) -> None:
        ready = admit_p1_05_ready_execution(
            execution=self.execution,
            authorization=self.authorization_allow,
            organizational_authority=self.authority_allow,
        )
        self.assertEqual(ready.workflow, self.execution.workflow)
        self.assertEqual(ready.material_inputs, self.execution.material_inputs)
        self.assertEqual(ready.workflow.version_id, self.workflow.workflow_version_id)
        self.assertEqual(ready.material_inputs[0].version_id, self.subject.version_id)

    def test_ready_execution_pins_both_distinct_explicit_allow_decision_versions(self) -> None:
        ready = admit_p1_05_ready_execution(
            execution=self.execution,
            authorization=self.authorization_allow,
            organizational_authority=self.authority_allow,
        )
        self.assertEqual(len(ready.gate_decisions), 2)
        by_type = {pin.semantic_type: pin for pin in ready.gate_decisions}
        authorization_pin = by_type["platform.authorization-decision"]
        authority_pin = by_type["platform.organizational-authority-decision"]
        self.assertEqual(authorization_pin.version_id, self.authorization_allow.record.version_id)
        self.assertEqual(authority_pin.version_id, self.authority_allow.record.version_id)
        self.assertEqual(authorization_pin.lifecycle_status, GateOutcome.ALLOW.value)
        self.assertEqual(authority_pin.lifecycle_status, GateOutcome.ALLOW.value)
        self.assertIn(self.authorization_allow.record.version_id, ready.record.provenance_refs)
        self.assertIn(self.authority_allow.record.version_id, ready.record.provenance_refs)

    def test_gate_decisions_preserve_explicit_governed_basis_references(self) -> None:
        self.assertEqual(self.authorization_allow.basis_ref, self.authorization_basis)
        self.assertEqual(self.authority_allow.basis_ref, self.authority_basis)
        self.assertIn(self.authorization_basis, self.authorization_allow.record.provenance_refs)
        self.assertIn(self.authority_basis, self.authority_allow.record.provenance_refs)

    def test_gate_kind_cannot_substitute_for_the_other_gate(self) -> None:
        with self.assertRaises(ValueError):
            evaluate_p1_05_gates(
                execution=self.execution,
                authorization=self.authority_allow,
                organizational_authority=self.authorization_allow,
            )

    def test_gate_scope_is_bound_to_exact_execution_workflow_operation_and_target_version(self) -> None:
        wrong_workflow_version = replace(
            self.authorization_allow,
            workflow_version_id=Identity("workflow-version", "other-v1", "org-a"),
        )
        with self.assertRaises(ValueError):
            evaluate_p1_05_gates(
                execution=self.execution,
                authorization=wrong_workflow_version,
                organizational_authority=self.authority_allow,
            )

        wrong_target_version = replace(
            self.authorization_allow,
            target_version_id=Identity("canonical-version", "subject-1-v2", "org-a"),
        )
        with self.assertRaises(ValueError):
            evaluate_p1_05_gates(
                execution=self.execution,
                authorization=wrong_target_version,
                organizational_authority=self.authority_allow,
            )

    def test_ready_execution_cannot_be_constructed_with_denied_gate_pin(self) -> None:
        denied_authorization = build_p1_05_gate_decision(
            execution=self.execution,
            kind=GateKind.AUTHORIZATION,
            outcome=GateOutcome.DENY,
            decision_actor=self.decision_actor,
            basis_ref=self.authorization_basis,
        )
        denied_pin = GovernedVersionPin.from_record(denied_authorization.record)
        authority_pin = GovernedVersionPin.from_record(self.authority_allow.record)
        forged_ready_record = CanonicalRecord(
            subject_id=self.execution.execution_subject_id,
            version_id=Identity("execution-version", "forged-ready-v2", "org-a"),
            semantic_type=self.execution.record.semantic_type,
            schema_version=self.execution.record.schema_version,
            organization=self.organization,
            authority_mode=self.execution.record.authority_mode,
            authority_scope=self.execution.record.authority_scope,
            accountable_owner_id=self.execution.record.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self.execution.record.created_at,
            provenance_refs=(denied_pin.version_id, authority_pin.version_id),
            integrity_metadata=self.execution.record.integrity_metadata,
            lifecycle_status=ExecutionLifecycle.READY.value,
            predecessor_version_id=self.execution.execution_version_id,
        )
        with self.assertRaises(ValueError):
            ExecutionContext(
                record=forged_ready_record,
                workflow=self.execution.workflow,
                operation_name=self.execution.operation_name,
                material_inputs=self.execution.material_inputs,
                gate_decisions=(denied_pin, authority_pin),
            )

    def test_gate_evidence_and_ready_execution_are_immutable_and_do_not_mutate_target(self) -> None:
        ready = admit_p1_05_ready_execution(
            execution=self.execution,
            authorization=self.authorization_allow,
            organizational_authority=self.authority_allow,
        )
        with self.assertRaises(FrozenInstanceError):
            self.authorization_allow.outcome = GateOutcome.DENY  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            ready.gate_decisions = ()  # type: ignore[misc]
        self.assertEqual(self.subject.version_id.value, "subject-1-v1")
        self.assertIsNone(self.subject.predecessor_version_id)
        self.assertEqual(self.subject.payload, (("label", "domain-neutral reference subject"),))


if __name__ == "__main__":
    unittest.main()
