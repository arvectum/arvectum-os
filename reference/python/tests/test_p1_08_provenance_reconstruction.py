from dataclasses import FrozenInstanceError, replace
import unittest

from arvectum_os_ref.canonical import CanonicalRecord, build_p1_02_native_record
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
from arvectum_os_ref.provenance import (
    ReconstructionEvidence,
    ReconstructionEvidenceError,
    build_p1_08_reconstruction_evidence,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow


class P108ProvenanceReconstructionTests(unittest.TestCase):
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

    def _build(self, **overrides):
        arguments = {
            "input_record": self.subject,
            "workflow": self.workflow,
            "awaiting_execution": self.awaiting,
            "authorization": self.authorization,
            "organizational_authority": self.organizational_authority,
            "ready_execution": self.ready,
            "mutation": self.mutation,
            "event": self.event,
        }
        arguments.update(overrides)
        return build_p1_08_reconstruction_evidence(**arguments)

    def test_manifest_identifies_actor_workflow_input_execution_result_and_event(self) -> None:
        evidence = self._build()

        self.assertIsInstance(evidence, ReconstructionEvidence)
        self.assertEqual(evidence.organization, self.organization)
        self.assertEqual(evidence.initiating_actor_id, self.principal.principal_id)
        self.assertEqual(evidence.operation_name, self.mutation.execution.operation_name)
        self.assertEqual(evidence.workflow, GovernedVersionPin.from_record(self.workflow.record))
        self.assertEqual(evidence.material_inputs, (GovernedVersionPin.from_record(self.subject),))
        self.assertEqual(
            evidence.execution_versions,
            (
                GovernedVersionPin.from_record(self.awaiting.record),
                GovernedVersionPin.from_record(self.ready.record),
                GovernedVersionPin.from_record(self.mutation.execution.record),
            ),
        )
        self.assertEqual(
            evidence.canonical_effects,
            (GovernedVersionPin.from_record(self.mutation.resulting_record),),
        )
        self.assertEqual(evidence.events, (GovernedVersionPin.from_record(self.event.record),))
        self.assertEqual(evidence.event_type, self.event.event_type)
        self.assertEqual(evidence.event_schema_version, self.event.event_schema_version)

    def test_manifest_preserves_gate_decisions_and_governed_bases_in_provenance(self) -> None:
        evidence = self._build()

        self.assertEqual(
            evidence.gate_decisions,
            (self.authorization.version_pin, self.organizational_authority.version_pin),
        )
        for expected in (
            self.authorization.record.subject_id,
            self.authorization.record.version_id,
            self.authorization.basis_ref,
            self.organizational_authority.record.subject_id,
            self.organizational_authority.record.version_id,
            self.organizational_authority.basis_ref,
            self.workflow.record.version_id,
            self.subject.version_id,
            self.ready.execution_version_id,
            self.mutation.execution.execution_version_id,
            self.mutation.resulting_record.version_id,
            self.event.version_id,
        ):
            self.assertIn(expected, evidence.provenance_refs)
        self.assertEqual(len(evidence.provenance_refs), len(set(evidence.provenance_refs)))

    def test_correlation_and_causation_remain_explicit_and_distinct(self) -> None:
        evidence = self._build()

        self.assertEqual(evidence.correlation_refs, (self.mutation.execution.execution_subject_id,))
        self.assertEqual(evidence.causation_refs, (self.mutation.execution.execution_version_id,))
        self.assertNotEqual(evidence.correlation_refs, evidence.causation_refs)

    def test_reconstruction_manifest_is_frozen_and_not_canonical_state(self) -> None:
        evidence = self._build()

        self.assertNotIsInstance(evidence, CanonicalRecord)
        with self.assertRaises(FrozenInstanceError):
            evidence.operation_name = "changed"  # type: ignore[misc]

    def test_reconstruction_is_observational_and_does_not_mutate_sealed_history(self) -> None:
        subject_before = self.subject
        result_before = self.mutation.resulting_record
        terminal_before = self.mutation.execution
        event_before = self.event

        first = self._build()
        second = self._build()

        self.assertEqual(first, second)
        self.assertIs(self.subject, subject_before)
        self.assertIs(self.mutation.resulting_record, result_before)
        self.assertIs(self.mutation.execution, terminal_before)
        self.assertIs(self.event, event_before)
        self.assertEqual(self.event.record.predecessor_version_id, None)
        self.assertEqual(self.mutation.execution.record.lifecycle_status, "Succeeded")

    def test_wrong_workflow_version_fails_closed(self) -> None:
        forged_record = replace(
            self.workflow.record,
            version_id=Identity("workflow-version", "reference-subject-maintenance-vX", "org-a"),
        )
        forged_workflow = replace(self.workflow, record=forged_record)

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(workflow=forged_workflow)

    def test_wrong_material_input_version_fails_closed(self) -> None:
        forged_input = replace(
            self.subject,
            version_id=Identity("canonical-version", "subject-1-vX", "org-a"),
        )

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(input_record=forged_input)

    def test_broken_ready_execution_predecessor_fails_closed(self) -> None:
        forged_record = replace(
            self.ready.record,
            predecessor_version_id=Identity("execution-version", "wrong-awaiting-v1", "org-a"),
        )
        forged_ready = replace(self.ready, record=forged_record)

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(ready_execution=forged_ready)

    def test_broken_terminal_execution_predecessor_fails_closed(self) -> None:
        forged_terminal_record = replace(
            self.mutation.execution.record,
            predecessor_version_id=Identity("execution-version", "wrong-ready-v1", "org-a"),
        )
        forged_terminal = replace(self.mutation.execution, record=forged_terminal_record)
        forged_mutation = replace(self.mutation, execution=forged_terminal)

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(mutation=forged_mutation)

    def test_gate_decision_for_wrong_execution_version_fails_closed(self) -> None:
        forged_authorization = replace(
            self.authorization,
            evaluated_execution_version_id=Identity("execution-version", "wrong-awaiting-v1", "org-a"),
        )

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(authorization=forged_authorization)

    def test_incomplete_result_provenance_fails_closed(self) -> None:
        incomplete = tuple(
            ref
            for ref in self.mutation.resulting_record.provenance_refs
            if ref != self.workflow.record.version_id
        )
        forged_result = replace(self.mutation.resulting_record, provenance_refs=incomplete)
        forged_mutation = replace(self.mutation, resulting_record=forged_result)

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(mutation=forged_mutation)

    def test_wrong_event_correlation_fails_closed(self) -> None:
        forged_event = replace(
            self.event,
            correlation_refs=(Identity("correlation", "unrelated", "org-a"),),
        )

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(event=forged_event)

    def test_wrong_event_causation_fails_closed(self) -> None:
        forged_event = replace(
            self.event,
            causation_refs=(Identity("execution-version", "wrong-terminal-v1", "org-a"),),
        )

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(event=forged_event)

    def test_wrong_event_result_version_fails_closed_even_if_self_consistent(self) -> None:
        wrong_result = Identity("canonical-version", "subject-1-vX", "org-a")
        forged_record = replace(
            self.event.record,
            provenance_refs=(*self.event.record.provenance_refs, wrong_result),
        )
        forged_event = replace(
            self.event,
            record=forged_record,
            related_version_ids=(wrong_result,),
        )

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(event=forged_event)

    def test_changed_initiating_principal_in_terminal_history_fails_closed(self) -> None:
        forged_terminal_record = replace(
            self.mutation.execution.record,
            creation_actor=self.decision_actor,
        )
        forged_terminal = replace(self.mutation.execution, record=forged_terminal_record)
        forged_mutation = replace(self.mutation, execution=forged_terminal)

        with self.assertRaises(ReconstructionEvidenceError):
            self._build(mutation=forged_mutation)


if __name__ == "__main__":
    unittest.main()
