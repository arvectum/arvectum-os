from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import (
    CanonicalEvent,
    EventIdentityConflictError,
    EventReceipt,
    EventVersionIdentityConflictError,
    ReconstructionEvidenceError,
    admit_event,
    build_reconstruction_manifest,
)
from arvectum_os_ref.governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    start_governed_execution,
    transition_governed_execution,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)


UTC = timezone.utc


class P205EventProvenanceRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "initiator", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-actor", "platform")),
            self.organization,
        )
        self.producer = Identity("principal", "event-producer", "platform")
        self.input_record = self._record(
            "subject-a",
            "subject-a-v1",
            "example.subject",
            provenance=(self.principal.principal_id,),
        )
        self.workflow = self._workflow(
            "workflow-a",
            "workflow-a-v1",
            "update-subject",
            self.input_record,
            (OperationSideEffectClass.CANONICAL_MUTATION,),
        )
        (
            self.execution_history,
            self.result_record,
        ) = self._execute(
            workflow=self.workflow,
            operation="update-subject",
            input_record=self.input_record,
            execution_name="execution-a",
            result_name="subject-a-v2",
            required_gates=(
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.VALIDATION,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
        )
        self.terminal = self.execution_history[-1]
        self.receipt = self._receipt(
            execution=self.terminal,
            result=self.result_record,
            event_name="event-a",
            event_type="platform.canonical-mutation.succeeded",
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 8, minute, tzinfo=UTC)

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        subject: str,
        version: str,
        semantic_type: str,
        *,
        provenance: tuple[Identity, ...],
        lifecycle: str = "Active",
        authority_scope: str = "example.subject/state",
        created_at: datetime | None = None,
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
            created_at=created_at or self._time(0),
            provenance_refs=provenance,
            integrity_metadata=(("representation", "test"),),
            payload=(("value", version),),
            lifecycle_status=lifecycle,
            predecessor_version_id=None,
        )

    def _workflow(
        self,
        subject: str,
        version: str,
        operation: str,
        target: CanonicalRecord,
        side_effects: tuple[OperationSideEffectClass, ...],
    ) -> WorkflowDefinition:
        record = CanonicalRecord(
            subject_id=self._id("workflow-subject", subject),
            version_id=self._id("workflow-version", version),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id, target.subject_id, target.version_id),
            integrity_metadata=(("representation", "test"),),
            payload=(),
            lifecycle_status="Approved",
            predecessor_version_id=None,
        )
        return WorkflowDefinition(
            record=record,
            operations=(
                WorkflowOperation(
                    semantic_name=operation,
                    target_subject_id=target.subject_id,
                    target_semantic_type=target.semantic_type,
                    side_effect_classes=side_effects,
                ),
            ),
        )

    def _execute(
        self,
        *,
        workflow: WorkflowDefinition,
        operation: str,
        input_record: CanonicalRecord,
        execution_name: str,
        result_name: str,
        required_gates: tuple[GovernedGateKind, ...],
    ) -> tuple[tuple[GovernedExecutionContext, ...], CanonicalRecord]:
        created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=workflow,
            operation_name=operation,
            material_inputs=(input_record,),
            required_gates=required_gates,
            execution_id=self._id("execution-subject", execution_name),
            version_id=self._id("execution-version", f"{execution_name}-v1"),
            created_at=self._time(1),
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", f"{execution_name}-v2"),
            actor=self.actor,
            created_at=self._time(2),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=self.decision_actor,
                basis_ref=self._id("governed-basis", f"{execution_name}-{kind.value}"),
                decision_id=self._id("gate-decision-subject", f"{execution_name}-{kind.value}"),
                version_id=self._id("gate-decision-version", f"{execution_name}-{kind.value}-v1"),
                created_at=self._time(3),
            )
            for kind in required_gates
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=self._id("execution-version", f"{execution_name}-v3"),
            actor=self.actor,
            created_at=self._time(4),
        )
        running = transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", f"{execution_name}-v4"),
            actor=self.actor,
            created_at=self._time(5),
        )
        result = self._record(
            result_name,
            f"{result_name}-record-v1",
            "example.result",
            provenance=(
                self.principal.principal_id,
                running.execution_subject_id,
                running.execution_version_id,
                workflow.record.subject_id,
                workflow.record.version_id,
                input_record.subject_id,
                input_record.version_id,
            ),
            lifecycle="Established",
            authority_scope="example.result/state",
            created_at=self._time(6),
        )
        succeeded = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=self._id("execution-version", f"{execution_name}-v5"),
            actor=self.actor,
            created_at=self._time(7),
            additional_provenance_refs=(result.subject_id, result.version_id),
        )
        return (created, awaiting, ready, running, succeeded), result

    def _receipt(
        self,
        *,
        execution: GovernedExecutionContext,
        result: CanonicalRecord,
        event_name: str,
        event_type: str,
        occurred_at: datetime | None = None,
        recorded_at: datetime | None = None,
    ) -> EventReceipt:
        return EventReceipt(
            event_id=self._id("event-subject", event_name),
            version_id=self._id("event-version", f"{event_name}-v1"),
            event_type=event_type,
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS",
            occurred_at=occurred_at or self._time(7),
            recorded_at=recorded_at or self._time(8),
            producer_id=self.producer,
            initiating_actor_id=self.principal.principal_id,
            execution_subject_id=execution.execution_subject_id,
            execution_version_id=execution.execution_version_id,
            related_subject_ids=(result.subject_id,),
            related_version_ids=(result.version_id,),
            correlation_refs=(execution.execution_subject_id,),
            causation_refs=(execution.execution_version_id,),
            classification="internal",
            access_scope="organization",
            provenance_refs=(
                self.producer,
                self.principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                result.subject_id,
                result.version_id,
            ),
            integrity_metadata=(("representation", "test-receipt"),),
            payload=(("operation", execution.operation_name), ("outcome", execution.lifecycle.value)),
        )

    def _admit(self, receipt: EventReceipt | None = None, history: tuple[CanonicalEvent, ...] = ()):
        return admit_event(
            receipt=receipt or self.receipt,
            execution=self.terminal,
            related_records=(self.result_record,),
            admitted_events=history,
        )

    def test_receipt_is_transient_and_not_a_canonical_record(self) -> None:
        self.assertIsInstance(self.receipt, EventReceipt)
        self.assertNotIsInstance(self.receipt, CanonicalRecord)
        self.assertFalse(hasattr(self.receipt, "record"))

    def test_receipt_rejects_cross_organization_governed_reference(self) -> None:
        with self.assertRaises(ValueError):
            replace(
                self.receipt,
                causation_refs=(Identity("execution-version", "elsewhere", "org-b"),),
            )

    def test_admission_creates_immutable_append_only_event(self) -> None:
        result = self._admit()
        event = result.event
        self.assertFalse(result.duplicate_delivery)
        self.assertEqual(len(result.admitted_events), 1)
        self.assertEqual(event.record.semantic_type, "platform.event")
        self.assertEqual(event.record.lifecycle_status, "Admitted")
        self.assertIsNone(event.record.predecessor_version_id)
        self.assertEqual(event.execution_version_id, self.terminal.execution_version_id)
        self.assertIn(self.result_record.version_id, event.record.provenance_refs)
        with self.assertRaises(FrozenInstanceError):
            event.event_type = "changed"  # type: ignore[misc]

    def test_duplicate_delivery_of_same_occurrence_is_idempotent(self) -> None:
        first = self._admit()
        duplicate = self._admit(history=first.admitted_events)
        self.assertTrue(duplicate.duplicate_delivery)
        self.assertIs(duplicate.event, first.event)
        self.assertEqual(duplicate.admitted_events, first.admitted_events)

    def test_conflicting_content_for_same_event_identity_is_rejected(self) -> None:
        first = self._admit()
        conflicting = replace(
            self.receipt,
            payload=(("operation", self.terminal.operation_name), ("outcome", "conflicting")),
        )
        with self.assertRaises(EventIdentityConflictError):
            self._admit(conflicting, first.admitted_events)

    def test_different_version_for_same_event_identity_is_rejected(self) -> None:
        first = self._admit()
        conflicting = replace(
            self.receipt,
            version_id=self._id("event-version", "event-a-v2"),
        )
        with self.assertRaises(EventIdentityConflictError):
            self._admit(conflicting, first.admitted_events)

    def test_event_version_identity_cannot_be_reused_by_another_event(self) -> None:
        first = self._admit()
        conflicting = replace(
            self.receipt,
            event_id=self._id("event-subject", "event-b"),
        )
        with self.assertRaises(EventVersionIdentityConflictError):
            self._admit(conflicting, first.admitted_events)

    def test_admission_rejects_wrong_execution_version(self) -> None:
        wrong = replace(
            self.receipt,
            execution_version_id=self.execution_history[-2].execution_version_id,
            causation_refs=(self.execution_history[-2].execution_version_id,),
            provenance_refs=tuple(
                self.execution_history[-2].execution_version_id if item == self.terminal.execution_version_id else item
                for item in self.receipt.provenance_refs
            ),
        )
        with self.assertRaises(ValueError):
            self._admit(wrong)

    def test_admission_rejects_related_result_not_declared_by_receipt(self) -> None:
        unrelated = self._record(
            "unrelated",
            "unrelated-v1",
            "example.result",
            provenance=(self.principal.principal_id, self.terminal.execution_version_id),
        )
        with self.assertRaises(ValueError):
            admit_event(
                receipt=self.receipt,
                execution=self.terminal,
                related_records=(unrelated,),
            )

    def test_admission_rejects_incomplete_execution_or_result_provenance(self) -> None:
        incomplete = replace(
            self.receipt,
            provenance_refs=(
                self.producer,
                self.principal.principal_id,
                self.terminal.execution_subject_id,
                self.terminal.execution_version_id,
            ),
        )
        with self.assertRaises(ValueError):
            self._admit(incomplete)

    def test_correlation_and_causation_remain_explicit_and_distinct(self) -> None:
        event = self._admit().event
        self.assertEqual(event.correlation_refs, (self.terminal.execution_subject_id,))
        self.assertEqual(event.causation_refs, (self.terminal.execution_version_id,))
        self.assertNotEqual(event.correlation_refs, event.causation_refs)

    def test_occurrence_and_recording_time_do_not_create_ordering_assumption(self) -> None:
        receipt = self._receipt(
            execution=self.terminal,
            result=self.result_record,
            event_name="clock-uncertain",
            event_type="platform.clock-uncertain.observed",
            occurred_at=self._time(9),
            recorded_at=self._time(8),
        )
        event = self._admit(receipt).event
        self.assertGreater(event.occurred_at, event.recorded_at)

    def test_event_type_and_schema_version_are_preserved_exactly(self) -> None:
        event = self._admit().event
        self.assertEqual(event.event_type, "platform.canonical-mutation.succeeded")
        self.assertEqual(event.event_schema_version, "1")
        self.assertEqual(event.record.schema_version, "1")

    def test_reconstruction_identifies_exact_governed_versions(self) -> None:
        event = self._admit().event
        manifest = build_reconstruction_manifest(
            execution_versions=self.execution_history,
            result_records=(self.result_record,),
            events=(event,),
        )
        self.assertEqual(manifest.initiating_actor_id, self.principal.principal_id)
        self.assertEqual(manifest.execution_subject_id, self.terminal.execution_subject_id)
        self.assertEqual(manifest.workflow.version_id, self.workflow.record.version_id)
        self.assertEqual(manifest.material_inputs[0].version_id, self.input_record.version_id)
        self.assertEqual(
            {pin.version_id for pin in manifest.gate_decisions},
            {decision.record.version_id for decision in self.terminal.gate_decisions},
        )
        self.assertEqual(
            {pin.version_id for pin in manifest.execution_versions},
            {item.execution_version_id for item in self.execution_history},
        )
        self.assertEqual(manifest.results[0].version_id, self.result_record.version_id)
        self.assertEqual(manifest.events[0].version_id, event.version_id)
        self.assertEqual(manifest.event_types, ((event.event_type, event.event_schema_version),))

    def test_reconstruction_rejects_unsealed_execution_head(self) -> None:
        event = self._admit().event
        with self.assertRaises(ReconstructionEvidenceError):
            build_reconstruction_manifest(
                execution_versions=self.execution_history[:-1],
                result_records=(self.result_record,),
                events=(event,),
            )

    def test_reconstruction_rejects_result_without_execution_provenance(self) -> None:
        event = self._admit().event
        bad_result = self._record(
            "bad-result",
            "bad-result-v1",
            "example.result",
            provenance=(self.principal.principal_id,),
        )
        bad_receipt = replace(
            self.receipt,
            related_subject_ids=(bad_result.subject_id,),
            related_version_ids=(bad_result.version_id,),
            provenance_refs=(
                self.producer,
                self.principal.principal_id,
                self.terminal.execution_subject_id,
                self.terminal.execution_version_id,
                bad_result.subject_id,
                bad_result.version_id,
            ),
        )
        bad_event = admit_event(
            receipt=bad_receipt,
            execution=self.terminal,
            related_records=(bad_result,),
        ).event
        with self.assertRaises(ReconstructionEvidenceError):
            build_reconstruction_manifest(
                execution_versions=self.execution_history,
                result_records=(bad_result,),
                events=(bad_event,),
            )

    def test_reconstruction_rejects_event_from_another_execution(self) -> None:
        other_input = self._record(
            "subject-b",
            "subject-b-v1",
            "example.subject",
            provenance=(self.principal.principal_id,),
        )
        other_workflow = self._workflow(
            "workflow-b",
            "workflow-b-v1",
            "commit-external",
            other_input,
            (OperationSideEffectClass.EXTERNAL_MUTATION, OperationSideEffectClass.COMMITMENT),
        )
        other_history, other_result = self._execute(
            workflow=other_workflow,
            operation="commit-external",
            input_record=other_input,
            execution_name="execution-b",
            result_name="commitment-b",
            required_gates=(GovernedGateKind.AUTHORIZATION, GovernedGateKind.DATA_GOVERNANCE),
        )
        other_receipt = self._receipt(
            execution=other_history[-1],
            result=other_result,
            event_name="event-b",
            event_type="platform.external-commitment.succeeded",
        )
        other_event = admit_event(
            receipt=other_receipt,
            execution=other_history[-1],
            related_records=(other_result,),
        ).event
        with self.assertRaises(ReconstructionEvidenceError):
            build_reconstruction_manifest(
                execution_versions=self.execution_history,
                result_records=(self.result_record,),
                events=(other_event,),
            )

    def test_reconstruction_preserves_separate_gate_decisions(self) -> None:
        event = self._admit().event
        manifest = build_reconstruction_manifest(
            execution_versions=self.execution_history,
            result_records=(self.result_record,),
            events=(event,),
        )
        kinds = {decision.kind for decision in self.terminal.gate_decisions}
        self.assertIn(GovernedGateKind.AUTHORIZATION, kinds)
        self.assertIn(GovernedGateKind.ORGANIZATIONAL_AUTHORITY, kinds)
        self.assertIn(GovernedGateKind.DATA_GOVERNANCE, kinds)
        self.assertIn(GovernedGateKind.VALIDATION, kinds)
        self.assertIn(GovernedGateKind.CONSEQUENTIAL_APPROVAL, kinds)
        self.assertEqual(len(manifest.gate_decisions), len(kinds))

    def test_reconstruction_is_read_only_and_does_not_create_governed_state(self) -> None:
        admitted = self._admit()
        before_history = admitted.admitted_events
        before_terminal = self.terminal
        manifest = build_reconstruction_manifest(
            execution_versions=self.execution_history,
            result_records=(self.result_record,),
            events=(admitted.event,),
        )
        self.assertEqual(admitted.admitted_events, before_history)
        self.assertIs(self.terminal, before_terminal)
        self.assertNotIsInstance(manifest, CanonicalRecord)

    def test_same_runtime_reconstructs_second_workflow_and_execution_shape(self) -> None:
        second_input = self._record(
            "subject-c",
            "subject-c-v1",
            "example.subject",
            provenance=(self.principal.principal_id,),
        )
        second_workflow = self._workflow(
            "workflow-c",
            "workflow-c-v4",
            "create-commitment",
            second_input,
            (OperationSideEffectClass.EXTERNAL_MUTATION, OperationSideEffectClass.COMMITMENT),
        )
        second_history, second_result = self._execute(
            workflow=second_workflow,
            operation="create-commitment",
            input_record=second_input,
            execution_name="execution-c",
            result_name="commitment-c",
            required_gates=(
                GovernedGateKind.ACTOR_ASSURANCE,
                GovernedGateKind.AUTHORIZATION,
                GovernedGateKind.DATA_GOVERNANCE,
                GovernedGateKind.CONSEQUENTIAL_APPROVAL,
            ),
        )
        second_receipt = self._receipt(
            execution=second_history[-1],
            result=second_result,
            event_name="event-c",
            event_type="platform.commitment.succeeded",
        )
        second_event = admit_event(
            receipt=second_receipt,
            execution=second_history[-1],
            related_records=(second_result,),
        ).event
        manifest = build_reconstruction_manifest(
            execution_versions=second_history,
            result_records=(second_result,),
            events=(second_event,),
        )
        self.assertEqual(manifest.operation_name, "create-commitment")
        self.assertEqual(manifest.workflow.version_id, second_workflow.record.version_id)
        self.assertEqual(manifest.results[0].version_id, second_result.version_id)
        self.assertEqual(manifest.events[0].version_id, second_event.version_id)

    def test_reconstruction_manifest_is_immutable(self) -> None:
        event = self._admit().event
        manifest = build_reconstruction_manifest(
            execution_versions=self.execution_history,
            result_records=(self.result_record,),
            events=(event,),
        )
        with self.assertRaises(FrozenInstanceError):
            manifest.operation_name = "changed"  # type: ignore[misc]


if __name__ == "__main__":
    unittest.main()
