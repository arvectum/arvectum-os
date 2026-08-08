from dataclasses import FrozenInstanceError, replace
from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.event_provenance import EventReceipt, admit_event
from arvectum_os_ref.governed_execution import (
    ConsequentialOperationNotAdmittedError,
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
from arvectum_os_ref.runtime_consistency import (
    LOGICAL_ATOMICITY_EXCLUDED,
    LOGICAL_ATOMICITY_INCLUDED,
    CanonicalSuccessorConflictError,
    ConsequentialOutcome,
    DuplicateEventCommitConflictError,
    IdempotencyKeyConflictError,
    ReconciliationRequiredError,
    RetrySemantics,
    RuntimeConsistencyState,
    StaleCanonicalHeadError,
    StaleExecutionInputError,
    commit_canonical_mutation,
    record_external_consequence_attempt,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)


UTC = timezone.utc


class P206RuntimeConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "initiator", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-actor", "platform")),
            self.organization,
        )
        self.producer = Identity("principal", "runtime-event-producer", "platform")

        self.initial = self._record(
            subject="subject-a",
            version="subject-a-v1",
            predecessor=None,
            provenance=(self.principal.principal_id,),
            payload_value="v1",
        )
        self.canonical_workflow = self._workflow(
            subject="workflow-canonical",
            version="workflow-canonical-v1",
            operation="update-subject",
            target=self.initial,
            side_effects=(OperationSideEffectClass.CANONICAL_MUTATION,),
        )
        self.canonical_created, self.canonical_running = self._admitted_execution(
            workflow=self.canonical_workflow,
            operation="update-subject",
            input_record=self.initial,
            execution_name="execution-canonical",
        )
        self.candidate_v2 = self._record(
            subject="subject-a",
            version="subject-a-v2",
            predecessor=self.initial.version_id,
            provenance=(
                self.principal.principal_id,
                self.canonical_running.execution_subject_id,
                self.canonical_running.execution_version_id,
                self.initial.subject_id,
                self.initial.version_id,
            ),
            payload_value="v2",
            created_at=self._time(8),
        )
        self.event_v2 = self._receipt(
            execution=self.canonical_running,
            result=self.candidate_v2,
            event_name="subject-a-v2-committed",
            event_type="platform.canonical-mutation.succeeded",
        )
        self.state = RuntimeConsistencyState(canonical_records=(self.initial,))

        self.external_workflow = self._workflow(
            subject="workflow-external",
            version="workflow-external-v1",
            operation="commit-external",
            target=self.initial,
            side_effects=(
                OperationSideEffectClass.EXTERNAL_MUTATION,
                OperationSideEffectClass.COMMITMENT,
            ),
        )
        self.external_created, self.external_running = self._admitted_execution(
            workflow=self.external_workflow,
            operation="commit-external",
            input_record=self.initial,
            execution_name="execution-external",
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 9, minute, tzinfo=UTC)

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        *,
        subject: str,
        version: str,
        predecessor: Identity | None,
        provenance: tuple[Identity, ...],
        payload_value: str,
        created_at: datetime | None = None,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", subject),
            version_id=self._id("canonical-version", version),
            semantic_type="example.subject",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="example.subject/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=created_at or self._time(0),
            provenance_refs=provenance,
            integrity_metadata=(("representation", "test"),),
            payload=(("value", payload_value),),
            lifecycle_status="Active",
            predecessor_version_id=predecessor,
        )

    def _workflow(
        self,
        *,
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

    def _admitted_execution(
        self,
        *,
        workflow: WorkflowDefinition,
        operation: str,
        input_record: CanonicalRecord,
        execution_name: str,
    ) -> tuple[GovernedExecutionContext, GovernedExecutionContext]:
        created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=workflow,
            operation_name=operation,
            material_inputs=(input_record,),
            required_gates=(GovernedGateKind.AUTHORIZATION,),
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
        decision = build_governed_gate_decision(
            execution=awaiting,
            kind=GovernedGateKind.AUTHORIZATION,
            outcome=GovernedGateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=self._id("governed-basis", f"{execution_name}-authorization"),
            decision_id=self._id("gate-decision-subject", f"{execution_name}-authorization"),
            version_id=self._id("gate-decision-version", f"{execution_name}-authorization-v1"),
            created_at=self._time(3),
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=(decision,),
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
        return created, running

    def _receipt(
        self,
        *,
        execution: GovernedExecutionContext,
        result: CanonicalRecord,
        event_name: str,
        event_type: str,
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
            occurred_at=self._time(8),
            recorded_at=self._time(9),
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
            payload=(("operation", execution.operation_name), ("outcome", "Succeeded")),
        )

    def _keyed_commit(
        self,
        *,
        state: RuntimeConsistencyState | None = None,
        candidate: CanonicalRecord | None = None,
        receipt: EventReceipt | None = None,
        expected: Identity | None = None,
        token: str = "commit-subject-a-v2",
    ):
        return commit_canonical_mutation(
            state=state or self.state,
            execution=self.canonical_running,
            expected_head_version_id=expected or self.initial.version_id,
            candidate=candidate or self.candidate_v2,
            event_receipt=receipt or self.event_v2,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token=token,
        )

    def test_state_resolves_one_explicit_canonical_head(self) -> None:
        self.assertEqual(self.state.head.version_id, self.initial.version_id)

    def test_keyed_canonical_commit_publishes_record_event_and_attempt_together(self) -> None:
        result = self._keyed_commit()
        self.assertFalse(result.duplicate)
        self.assertEqual(result.outcome, ConsequentialOutcome.SUCCEEDED)
        self.assertEqual(result.state.head.version_id, self.candidate_v2.version_id)
        self.assertEqual(len(result.state.canonical_records), 2)
        self.assertEqual(len(result.state.admitted_events), 1)
        self.assertEqual(len(result.state.attempts), 1)
        self.assertEqual(result.event.related_version_ids, (self.candidate_v2.version_id,))

    def test_exact_keyed_retry_returns_committed_result_without_repeating_effects(self) -> None:
        first = self._keyed_commit()
        retry = self._keyed_commit(state=first.state)
        self.assertTrue(retry.duplicate)
        self.assertIs(retry.state, first.state)
        self.assertEqual(len(retry.state.canonical_records), 2)
        self.assertEqual(len(retry.state.admitted_events), 1)
        self.assertEqual(len(retry.state.attempts), 1)
        self.assertEqual(retry.record.version_id, first.record.version_id)
        self.assertEqual(retry.event.version_id, first.event.version_id)

    def test_retry_token_cannot_be_rebound_to_different_immutable_invocation(self) -> None:
        first = self._keyed_commit()
        conflicting_candidate = replace(
            self.candidate_v2,
            payload=(("value", "materially-different"),),
        )
        conflicting_receipt = replace(
            self.event_v2,
            payload=(("operation", "update-subject"), ("outcome", "Different")),
        )
        with self.assertRaises(IdempotencyKeyConflictError):
            self._keyed_commit(
                state=first.state,
                candidate=conflicting_candidate,
                receipt=conflicting_receipt,
            )

    def test_stale_expected_head_is_rejected_instead_of_overwriting_newer_state(self) -> None:
        committed = self._keyed_commit()
        candidate_v3 = self._record(
            subject="subject-a",
            version="subject-a-v3",
            predecessor=self.initial.version_id,
            provenance=(self.principal.principal_id, self.canonical_running.execution_version_id),
            payload_value="v3",
            created_at=self._time(10),
        )
        receipt_v3 = self._receipt(
            execution=self.canonical_running,
            result=candidate_v3,
            event_name="subject-a-v3-committed",
            event_type="platform.canonical-mutation.succeeded",
        )
        with self.assertRaises(StaleCanonicalHeadError):
            self._keyed_commit(
                state=committed.state,
                candidate=candidate_v3,
                receipt=receipt_v3,
                token="stale-v3",
            )

    def test_execution_pinned_to_old_target_version_cannot_commit_against_new_head(self) -> None:
        committed = self._keyed_commit()
        candidate_v3 = self._record(
            subject="subject-a",
            version="subject-a-v3",
            predecessor=self.candidate_v2.version_id,
            provenance=(self.principal.principal_id, self.canonical_running.execution_version_id),
            payload_value="v3",
            created_at=self._time(10),
        )
        receipt_v3 = self._receipt(
            execution=self.canonical_running,
            result=candidate_v3,
            event_name="subject-a-v3-current-conflict",
            event_type="platform.canonical-mutation.succeeded",
        )
        with self.assertRaises(StaleExecutionInputError):
            self._keyed_commit(
                state=committed.state,
                expected=self.candidate_v2.version_id,
                candidate=candidate_v3,
                receipt=receipt_v3,
                token="v3-current-conflict",
            )

    def test_candidate_must_extend_exact_expected_head(self) -> None:
        bad = replace(
            self.candidate_v2,
            predecessor_version_id=self._id("canonical-version", "not-the-head"),
        )
        with self.assertRaises(CanonicalSuccessorConflictError):
            self._keyed_commit(candidate=bad, token="bad-predecessor")

    def test_already_admitted_event_cannot_evidence_a_distinct_new_commit(self) -> None:
        admitted = admit_event(
            receipt=self.event_v2,
            execution=self.canonical_running,
            related_records=(self.candidate_v2,),
        )
        state = RuntimeConsistencyState(
            canonical_records=(self.initial,),
            admitted_events=admitted.admitted_events,
        )
        with self.assertRaises(DuplicateEventCommitConflictError):
            self._keyed_commit(state=state, token="event-already-used")
        self.assertEqual(state.head.version_id, self.initial.version_id)
        self.assertEqual(len(state.admitted_events), 1)

    def test_event_admission_conflict_does_not_publish_candidate_state(self) -> None:
        admitted = admit_event(
            receipt=self.event_v2,
            execution=self.canonical_running,
            related_records=(self.candidate_v2,),
        )
        state = RuntimeConsistencyState(
            canonical_records=(self.initial,),
            admitted_events=admitted.admitted_events,
        )
        conflicting_receipt = replace(
            self.event_v2,
            payload=(("operation", "update-subject"), ("outcome", "Conflicting")),
        )
        with self.assertRaises(RuntimeError):
            self._keyed_commit(
                state=state,
                receipt=conflicting_receipt,
                token="event-conflict",
            )
        self.assertEqual(state.head.version_id, self.initial.version_id)
        self.assertEqual(len(state.canonical_records), 1)

    def test_natural_idempotency_recognizes_already_published_exact_successor(self) -> None:
        first = commit_canonical_mutation(
            state=self.state,
            execution=self.canonical_running,
            expected_head_version_id=self.initial.version_id,
            candidate=self.candidate_v2,
            event_receipt=self.event_v2,
            retry_semantics=RetrySemantics.NATURALLY_IDEMPOTENT,
        )
        retry = commit_canonical_mutation(
            state=first.state,
            execution=self.canonical_running,
            expected_head_version_id=self.initial.version_id,
            candidate=self.candidate_v2,
            event_receipt=self.event_v2,
            retry_semantics=RetrySemantics.NATURALLY_IDEMPOTENT,
        )
        self.assertTrue(retry.duplicate)
        self.assertIs(retry.state, first.state)
        self.assertEqual(len(retry.state.attempts), 1)

    def test_non_idempotent_external_effect_requires_duplicate_protection_token(self) -> None:
        with self.assertRaises(ValueError):
            record_external_consequence_attempt(
                state=self.state,
                execution=self.external_running,
                side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
                effect_descriptor=(("target", "external-a"),),
                retry_semantics=RetrySemantics.NON_IDEMPOTENT,
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_committed_external_retry_is_duplicate_not_second_effect(self) -> None:
        first = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"), ("command", "apply")),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-a-apply",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        retry = record_external_consequence_attempt(
            state=first.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"), ("command", "apply")),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-a-apply",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(first.succeeded)
        self.assertTrue(retry.duplicate)
        self.assertIs(retry.state, first.state)
        self.assertEqual(len(retry.state.attempts), 1)

    def test_external_retry_token_conflict_is_explicit(self) -> None:
        first = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"),),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="external-key",
            reported_outcome=ConsequentialOutcome.FAILED,
        )
        with self.assertRaises(IdempotencyKeyConflictError):
            record_external_consequence_attempt(
                state=first.state,
                execution=self.external_running,
                side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
                effect_descriptor=(("target", "external-b"),),
                retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
                retry_token="external-key",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_uncertain_external_outcome_is_explicit_and_does_not_claim_success(self) -> None:
        result = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.COMMITMENT,
            effect_descriptor=(("commitment", "bounded-test"),),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="commitment-attempt-1",
            reported_outcome=ConsequentialOutcome.UNCERTAIN,
        )
        self.assertFalse(result.succeeded)
        self.assertTrue(result.reconciliation_required)
        self.assertEqual(result.attempt.outcome, ConsequentialOutcome.UNCERTAIN)
        self.assertEqual(result.state.canonical_records, self.state.canonical_records)
        self.assertEqual(result.state.admitted_events, self.state.admitted_events)

    def test_uncertain_external_outcome_blocks_blind_retry(self) -> None:
        uncertain = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.COMMITMENT,
            effect_descriptor=(("commitment", "bounded-test"),),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="commitment-uncertain",
            reported_outcome=ConsequentialOutcome.UNCERTAIN,
        )
        with self.assertRaises(ReconciliationRequiredError):
            record_external_consequence_attempt(
                state=uncertain.state,
                execution=self.external_running,
                side_effect_class=OperationSideEffectClass.COMMITMENT,
                effect_descriptor=(("commitment", "bounded-test"),),
                retry_semantics=RetrySemantics.NON_IDEMPOTENT,
                retry_token="commitment-uncertain",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_failed_external_attempt_remains_failure_and_may_retry_same_invocation(self) -> None:
        failed = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"),),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="retry-after-failure",
            reported_outcome=ConsequentialOutcome.FAILED,
        )
        self.assertFalse(failed.succeeded)
        self.assertFalse(failed.reconciliation_required)
        succeeded = record_external_consequence_attempt(
            state=failed.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"),),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="retry-after-failure",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(succeeded.succeeded)
        self.assertEqual(len(succeeded.state.attempts), 2)
        duplicate = record_external_consequence_attempt(
            state=succeeded.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(("target", "external-a"),),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="retry-after-failure",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(duplicate.duplicate)
        self.assertEqual(len(duplicate.state.attempts), 2)

    def test_consequential_effect_requires_admitted_governed_execution(self) -> None:
        with self.assertRaises(ConsequentialOperationNotAdmittedError):
            record_external_consequence_attempt(
                state=self.state,
                execution=self.external_created,
                side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
                effect_descriptor=(("target", "external-a"),),
                retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
                retry_token="not-admitted",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_external_boundary_rejects_non_external_side_effect_class(self) -> None:
        with self.assertRaises(ValueError):
            record_external_consequence_attempt(
                state=self.state,
                execution=self.canonical_running,
                side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
                effect_descriptor=(("target", "subject-a"),),
                retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
                retry_token="wrong-boundary",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_logical_atomicity_boundary_is_explicitly_bounded_and_technology_neutral(self) -> None:
        self.assertIn("expected Canonical Head validation", LOGICAL_ATOMICITY_INCLUDED)
        self.assertIn("required canonical Event admission validation", LOGICAL_ATOMICITY_INCLUDED)
        self.assertIn("durable storage transaction", LOGICAL_ATOMICITY_EXCLUDED)
        self.assertIn("external-system mutation", LOGICAL_ATOMICITY_EXCLUDED)
        self.assertIn("outbox/inbox persistence", LOGICAL_ATOMICITY_EXCLUDED)

    def test_runtime_consistency_state_is_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.state.canonical_records = ()  # type: ignore[misc]

    def test_same_external_runtime_handles_materially_distinct_commitment_side_effect(self) -> None:
        result = record_external_consequence_attempt(
            state=self.state,
            execution=self.external_running,
            side_effect_class=OperationSideEffectClass.COMMITMENT,
            effect_descriptor=(("commitment", "reputation-sensitive"), ("scope", "org-a")),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="commitment-distinct-shape",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(result.succeeded)
        self.assertEqual(result.attempt.side_effect_class, OperationSideEffectClass.COMMITMENT)
        self.assertEqual(result.state.canonical_records, self.state.canonical_records)


if __name__ == "__main__":
    unittest.main()
