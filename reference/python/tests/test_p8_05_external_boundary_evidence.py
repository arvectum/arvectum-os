from dataclasses import replace
from datetime import UTC, datetime
import unittest

from arvectum_os_ref.canonical import (
    AuthorityMode,
    CanonicalRecord,
    ExternalAuthorityContract,
)
from arvectum_os_ref.event_provenance import admit_event
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
from arvectum_os_ref.runtime_consistency import (
    ConsequentialOutcome,
    ReconciliationRequiredError,
    RetrySemantics,
    RuntimeConsistencyState,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowOperation,
)
from p8_05_external_boundary_evidence import (
    P804_BASELINE_MANIFEST_SHA256,
    P804_COMPARISON_MANIFEST_SHA256,
    P804_FRESH_MANIFEST_SHA256,
    P804_FRESH_OBSERVED_AT,
    P804_LIVE_RUN_ID,
    P804_NOTICE_NUMBER,
    ExternalDelivery,
    ExternalEffectLedger,
    ExternalIngressState,
    ExternalOccurrence,
    ExternalOccurrenceConflictError,
    ReconciliationResolution,
    RetryAfterReconciliationNotAllowedError,
    admit_external_ingress,
    build_external_effect_outcome_event_receipt,
    reconcile_uncertain_external_effect,
    reconstruct_external_boundary,
    record_external_effect_outcome,
    record_retry_after_reconciliation,
    require_retry_allowed_after_reconciliation,
)


class P805ExternalBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scope = "org-a"
        self.organization = OrganizationScope(Identity("organization", self.scope, "platform"))
        self.principal = Principal(Identity("principal", "operator", self.scope))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-actor", self.scope)),
            self.organization,
        )
        self.base = self._native_record()
        self.external_ref = self._external_reference_record()
        self.ingress_execution = self._running_execution(
            "ingress",
            target=self.base,
            side_effects=(OperationSideEffectClass.READ_ONLY,),
        )
        self.external_execution = self._running_execution(
            "external-effect",
            target=self.base,
            side_effects=(OperationSideEffectClass.EXTERNAL_MUTATION,),
        )
        self.reconciliation_execution = self._running_execution(
            "reconciliation",
            target=self.base,
            side_effects=(OperationSideEffectClass.READ_ONLY,),
        )
        self.retry_execution = self._running_execution(
            "external-effect-retry",
            target=self.base,
            side_effects=(OperationSideEffectClass.EXTERNAL_MUTATION,),
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.scope)

    def _time(self, minute: int, second: int = 0) -> datetime:
        return datetime(2026, 8, 20, 8, minute, second, tzinfo=UTC)

    def _native_record(self) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self._id("canonical-subject", "p8-05-base"),
            version_id=self._id("canonical-version", "p8-05-base-v1"),
            semantic_type="platform.p8-05-test-base",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.p8-05/test",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(0),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "synthetic-bounded-test"),),
            payload=(),
            lifecycle_status="Active",
        )

    def _external_reference_record(self) -> CanonicalRecord:
        authority_scope = "eis.procurement-notice/read-only"
        external_authority = ExternalAuthorityContract(
            authoritative_system="zakupki.gov.ru",
            external_object_ref=f"44fz:notice:{P804_NOTICE_NUMBER}",
            authority_scope=authority_scope,
            retrieval_or_sync="read-only retrieval",
            freshness_expectation="fresh observation with explicit recording time",
            source_version_semantics="source observation digest/version reference",
            conflict_rule="fail-closed",
            failure_behavior="unknown/incomplete remains non-success",
            permitted_transformations=("integrity hashing", "bounded comparison"),
            retention_deletion="owner-governed evidence rules",
            portability="governed references and integrity digests",
        )
        return CanonicalRecord(
            subject_id=self._id("external-subject", f"eis-notice-{P804_NOTICE_NUMBER}"),
            version_id=self._id("external-version", f"eis-notice-{P804_NOTICE_NUMBER}-p8-04"),
            semantic_type="platform.external-reference",
            schema_version="p8.05-v1",
            organization=self.organization,
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=authority_scope,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime.fromisoformat(P804_FRESH_OBSERVED_AT),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("fresh_manifest_sha256", P804_FRESH_MANIFEST_SHA256),),
            payload=(("notice_number", P804_NOTICE_NUMBER),),
            lifecycle_status="Observed",
            external_authority=external_authority,
        )

    def _workflow(
        self,
        name: str,
        *,
        target: CanonicalRecord,
        side_effects: tuple[OperationSideEffectClass, ...],
    ) -> WorkflowDefinition:
        workflow_record = CanonicalRecord(
            subject_id=self._id("workflow-subject", f"p8-05-{name}"),
            version_id=self._id("workflow-version", f"p8-05-{name}-v1"),
            semantic_type="platform.workflow",
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.workflow/definition",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(1),
            provenance_refs=(self.principal.principal_id, target.subject_id, target.version_id),
            integrity_metadata=(("representation", "p8-05-test"),),
            payload=(),
            lifecycle_status="Approved",
        )
        return WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=f"p8-05-{name}",
                    target_subject_id=target.subject_id,
                    target_semantic_type=target.semantic_type,
                    side_effect_classes=side_effects,
                ),
            ),
        )

    def _running_execution(
        self,
        name: str,
        *,
        target: CanonicalRecord,
        side_effects: tuple[OperationSideEffectClass, ...],
    ) -> GovernedExecutionContext:
        workflow = self._workflow(name, target=target, side_effects=side_effects)
        created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=workflow,
            operation_name=f"p8-05-{name}",
            material_inputs=(target,),
            required_gates=(GovernedGateKind.AUTHORIZATION,),
            execution_id=self._id("execution-subject", f"p8-05-{name}"),
            version_id=self._id("execution-version", f"p8-05-{name}-v1"),
            created_at=self._time(2),
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", f"p8-05-{name}-v2"),
            actor=self.actor,
            created_at=self._time(3),
        )
        decision = build_governed_gate_decision(
            execution=awaiting,
            kind=GovernedGateKind.AUTHORIZATION,
            outcome=GovernedGateOutcome.ALLOW,
            decision_actor=self.decision_actor,
            basis_ref=self._id("governed-basis", f"p8-05-{name}-authorization"),
            decision_id=self._id("gate-decision-subject", f"p8-05-{name}-authorization"),
            version_id=self._id("gate-decision-version", f"p8-05-{name}-authorization-v1"),
            created_at=self._time(4),
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=(decision,),
            version_id=self._id("execution-version", f"p8-05-{name}-v3"),
            actor=self.actor,
            created_at=self._time(5),
        )
        return transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", f"p8-05-{name}-v4"),
            actor=self.actor,
            created_at=self._time(6),
        )

    def _occurrence(
        self,
        *,
        occurrence_id: str = "eis-p8-04-fresh-observation",
        event_suffix: str = "1",
        occurred_at: datetime | None = None,
        digest: str | None = None,
    ) -> ExternalOccurrence:
        digest = digest or P804_FRESH_MANIFEST_SHA256
        return ExternalOccurrence(
            organization=self.organization,
            source_system="zakupki.gov.ru",
            source_object_ref=f"44fz:notice:{P804_NOTICE_NUMBER}",
            source_occurrence_id=occurrence_id,
            source_version_ref=f"sha256:{digest}",
            authority_mode=AuthorityMode.EXTERNAL_REFERENCE,
            authority_scope=self.external_ref.authority_scope,
            occurred_at=occurred_at or datetime.fromisoformat(P804_FRESH_OBSERVED_AT),
            payload_integrity_ref=f"sha256:{digest}",
            event_id=self._id("event-subject", f"p8-05-external-occurrence-{event_suffix}"),
            event_version_id=self._id("event-version", f"p8-05-external-occurrence-{event_suffix}-v1"),
            governed_provenance_refs=(self.external_ref.subject_id, self.external_ref.version_id),
        )

    def _delivery(
        self,
        occurrence: ExternalOccurrence,
        *,
        suffix: str,
        received_at: datetime,
    ) -> ExternalDelivery:
        return ExternalDelivery(
            delivery_id=self._id("delivery", f"p8-05-{suffix}"),
            occurrence=occurrence,
            received_at=received_at,
            transport_name="bounded-read-only-https-evidence",
            payload_integrity_ref=occurrence.payload_integrity_ref,
        )

    def _uncertain_ledger(self):
        ledger = ExternalEffectLedger(RuntimeConsistencyState(canonical_records=(self.base,)))
        return record_external_effect_outcome(
            ledger=ledger,
            execution=self.external_execution,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(
                ("target_system", "synthetic-external-target"),
                ("operation", "synthetic-apply"),
            ),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="p8-05-effect-1",
            reported_outcome=ConsequentialOutcome.UNCERTAIN,
        )

    def _reconcile(self, ledger, attempt, resolution):
        return reconcile_uncertain_external_effect(
            ledger=ledger,
            uncertain_attempt=attempt,
            reconciliation_execution=self.reconciliation_execution,
            reconciliation_id=self._id("reconciliation-subject", f"p8-05-{resolution.value}"),
            version_id=self._id("reconciliation-version", f"p8-05-{resolution.value}-v1"),
            evidence_ref=self._id("evidence", f"p8-05-{resolution.value}-evidence"),
            resolution=resolution,
            resolved_at=self._time(40),
        )

    def test_live_p8_04_anchor_is_exact_and_read_only_evidence_is_not_reinvented(self) -> None:
        self.assertEqual(P804_NOTICE_NUMBER, "0344100006426000005")
        self.assertEqual(P804_LIVE_RUN_ID, "toa-run-20260820083457-21337c")
        self.assertEqual(P804_FRESH_OBSERVED_AT, "2026-08-20T08:34:57.365770+00:00")
        self.assertEqual(len(P804_BASELINE_MANIFEST_SHA256), 64)
        self.assertEqual(len(P804_FRESH_MANIFEST_SHA256), 64)
        self.assertEqual(len(P804_COMPARISON_MANIFEST_SHA256), 64)

    def test_transport_delivery_is_not_automatically_a_canonical_event(self) -> None:
        occurrence = self._occurrence()
        delivery = self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35))
        state = ExternalIngressState()
        self.assertEqual(state.canonical_events, ())
        self.assertEqual(state.deliveries, ())
        self.assertIs(delivery.occurrence, occurrence)

    def test_explicit_ingress_admission_creates_one_native_observation_event_and_preserves_external_authority(self) -> None:
        occurrence = self._occurrence()
        result = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        self.assertFalse(result.duplicate_delivery)
        self.assertEqual(len(result.state.canonical_events), 1)
        event = result.admission.event
        self.assertEqual(event.record.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(occurrence.authority_mode, AuthorityMode.EXTERNAL_REFERENCE)
        self.assertEqual(event.related_version_ids, (self.external_ref.version_id,))
        payload = dict(event.record.payload)
        self.assertEqual(payload["source_system"], "zakupki.gov.ru")
        self.assertEqual(payload["source_authority_mode"], AuthorityMode.EXTERNAL_REFERENCE.value)

    def test_duplicate_delivery_does_not_create_second_canonical_event_or_rewrite_first_recording_time(self) -> None:
        occurrence = self._occurrence()
        first = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        duplicate = admit_external_ingress(
            state=first.state,
            delivery=self._delivery(occurrence, suffix="delivery-2", received_at=self._time(39)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        self.assertTrue(duplicate.duplicate_delivery)
        self.assertEqual(len(duplicate.state.canonical_events), 1)
        self.assertEqual(len(duplicate.state.deliveries), 2)
        self.assertEqual(duplicate.admission.event.recorded_at, self._time(35))

    def test_same_payload_digest_with_new_source_occurrence_is_a_new_event(self) -> None:
        first_occurrence = self._occurrence(event_suffix="1")
        first = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(first_occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        second_occurrence = self._occurrence(
            occurrence_id="eis-p8-04-fresh-observation-second-logical-occurrence",
            event_suffix="2",
            occurred_at=self._time(36),
        )
        second = admit_external_ingress(
            state=first.state,
            delivery=self._delivery(second_occurrence, suffix="delivery-2", received_at=self._time(37)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        self.assertFalse(second.duplicate_delivery)
        self.assertEqual(len(second.state.canonical_events), 2)
        self.assertNotEqual(
            second.state.canonical_events[0].event_id,
            second.state.canonical_events[1].event_id,
        )
        self.assertEqual(
            first_occurrence.payload_integrity_ref,
            second_occurrence.payload_integrity_ref,
        )

    def test_same_external_occurrence_identity_with_changed_immutable_evidence_fails_closed(self) -> None:
        occurrence = self._occurrence()
        first = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        conflicting = replace(
            occurrence,
            source_version_ref="sha256:" + "f" * 64,
            payload_integrity_ref="sha256:" + "f" * 64,
        )
        with self.assertRaises(ExternalOccurrenceConflictError):
            admit_external_ingress(
                state=first.state,
                delivery=self._delivery(conflicting, suffix="delivery-conflict", received_at=self._time(38)),
                execution=self.ingress_execution,
                related_records=(self.external_ref,),
            )

    def test_out_of_order_delivery_preserves_occurrence_time_and_append_only_recording_time(self) -> None:
        later_occurrence = self._occurrence(
            occurrence_id="later-occurrence",
            event_suffix="later",
            occurred_at=self._time(32),
        )
        earlier_occurrence = self._occurrence(
            occurrence_id="earlier-occurrence",
            event_suffix="earlier",
            occurred_at=self._time(31),
        )
        first = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(later_occurrence, suffix="later-delivery", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        second = admit_external_ingress(
            state=first.state,
            delivery=self._delivery(earlier_occurrence, suffix="earlier-late-delivery", received_at=self._time(36)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        self.assertEqual(
            tuple(event.occurred_at for event in second.state.canonical_events),
            (self._time(32), self._time(31)),
        )
        self.assertEqual(
            tuple(event.recorded_at for event in second.state.canonical_events),
            (self._time(35), self._time(36)),
        )

    def test_ingress_preserves_correlation_causation_and_exact_external_reference_provenance(self) -> None:
        occurrence = self._occurrence()
        result = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        event = result.admission.event
        self.assertIn(self.ingress_execution.execution_subject_id, event.correlation_refs)
        self.assertIn(self.ingress_execution.execution_version_id, event.causation_refs)
        self.assertIn(self.external_ref.subject_id, event.record.provenance_refs)
        self.assertIn(self.external_ref.version_id, event.record.provenance_refs)

    def test_uncertain_egress_outcome_is_explicit_event_evidence_and_blind_retry_is_blocked(self) -> None:
        ledger, uncertain = self._uncertain_ledger()
        self.assertEqual(uncertain.attempt.outcome, ConsequentialOutcome.UNCERTAIN)
        self.assertTrue(uncertain.reconciliation_required)
        receipt = build_external_effect_outcome_event_receipt(
            attempt=uncertain.attempt,
            execution=self.external_execution,
            event_id=self._id("event-subject", "p8-05-effect-uncertain"),
            version_id=self._id("event-version", "p8-05-effect-uncertain-v1"),
            source_system="synthetic-external-target",
            effect_ref="synthetic-effect-1",
            recorded_at=self._time(20),
        )
        admitted = admit_event(receipt=receipt, execution=self.external_execution)
        self.assertEqual(dict(admitted.event.record.payload)["outcome"], "Uncertain")
        with self.assertRaises(ReconciliationRequiredError):
            record_external_effect_outcome(
                ledger=ledger,
                execution=self.external_execution,
                side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
                effect_descriptor=(
                    ("target_system", "synthetic-external-target"),
                    ("operation", "synthetic-apply"),
                ),
                retry_semantics=RetrySemantics.NON_IDEMPOTENT,
                retry_token="p8-05-effect-1",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_reconciliation_that_remains_uncertain_continues_to_block_retry(self) -> None:
        ledger, uncertain = self._uncertain_ledger()
        ledger = self._reconcile(ledger, uncertain.attempt, ReconciliationResolution.STILL_UNCERTAIN)
        with self.assertRaises(ReconciliationRequiredError):
            require_retry_allowed_after_reconciliation(ledger, uncertain.attempt)

    def test_reconciliation_confirming_success_prohibits_duplicate_retry(self) -> None:
        ledger, uncertain = self._uncertain_ledger()
        ledger = self._reconcile(ledger, uncertain.attempt, ReconciliationResolution.CONFIRMED_SUCCEEDED)
        with self.assertRaises(RetryAfterReconciliationNotAllowedError):
            require_retry_allowed_after_reconciliation(ledger, uncertain.attempt)

    def test_confirmed_not_applied_allows_only_new_governed_retry_and_preserves_lineage(self) -> None:
        ledger, uncertain = self._uncertain_ledger()
        ledger = self._reconcile(ledger, uncertain.attempt, ReconciliationResolution.CONFIRMED_NOT_APPLIED)
        next_ledger, retry = record_retry_after_reconciliation(
            ledger=ledger,
            uncertain_attempt=uncertain.attempt,
            retry_execution=self.retry_execution,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(
                ("target_system", "synthetic-external-target"),
                ("operation", "synthetic-apply"),
            ),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="p8-05-effect-1-retry-1",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        self.assertTrue(retry.succeeded)
        self.assertEqual(len(next_ledger.runtime_state.attempts), 2)
        self.assertEqual(next_ledger.runtime_state.attempts[0].outcome, ConsequentialOutcome.UNCERTAIN)
        self.assertEqual(next_ledger.runtime_state.attempts[1].outcome, ConsequentialOutcome.SUCCEEDED)
        self.assertEqual(len(next_ledger.reconciliations), 1)
        self.assertEqual(len(next_ledger.retry_links), 1)
        self.assertEqual(
            next_ledger.retry_links[0].reconciliation_id,
            next_ledger.reconciliations[0].reconciliation_id,
        )

    def test_post_reconciliation_retry_rejects_original_execution_and_token(self) -> None:
        ledger, uncertain = self._uncertain_ledger()
        ledger = self._reconcile(ledger, uncertain.attempt, ReconciliationResolution.CONFIRMED_NOT_APPLIED)
        with self.assertRaises(ValueError):
            record_retry_after_reconciliation(
                ledger=ledger,
                uncertain_attempt=uncertain.attempt,
                retry_execution=self.external_execution,
                side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
                effect_descriptor=(("target_system", "synthetic-external-target"),),
                retry_semantics=RetrySemantics.NON_IDEMPOTENT,
                retry_token="p8-05-effect-1",
                reported_outcome=ConsequentialOutcome.SUCCEEDED,
            )

    def test_historical_reconstruction_is_pure_and_never_claims_live_retrieval_or_external_effect(self) -> None:
        occurrence = self._occurrence()
        ingress = admit_external_ingress(
            state=ExternalIngressState(),
            delivery=self._delivery(occurrence, suffix="delivery-1", received_at=self._time(35)),
            execution=self.ingress_execution,
            related_records=(self.external_ref,),
        )
        ledger, uncertain = self._uncertain_ledger()
        ledger = self._reconcile(ledger, uncertain.attempt, ReconciliationResolution.CONFIRMED_NOT_APPLIED)
        ledger, _retry = record_retry_after_reconciliation(
            ledger=ledger,
            uncertain_attempt=uncertain.attempt,
            retry_execution=self.retry_execution,
            side_effect_class=OperationSideEffectClass.EXTERNAL_MUTATION,
            effect_descriptor=(
                ("target_system", "synthetic-external-target"),
                ("operation", "synthetic-apply"),
            ),
            retry_semantics=RetrySemantics.NON_IDEMPOTENT,
            retry_token="p8-05-effect-1-retry-1",
            reported_outcome=ConsequentialOutcome.SUCCEEDED,
        )
        before_attempts = ledger.runtime_state.attempts
        before_events = ingress.state.canonical_events
        manifest = reconstruct_external_boundary(
            ingress_state=ingress.state,
            effect_ledger=ledger,
        )
        self.assertFalse(manifest.live_retrievals_executed)
        self.assertFalse(manifest.external_effects_executed)
        self.assertEqual(manifest.ingress_event_ids, (occurrence.event_id,))
        self.assertEqual(
            manifest.egress_outcomes,
            (ConsequentialOutcome.UNCERTAIN, ConsequentialOutcome.SUCCEEDED),
        )
        self.assertEqual(ledger.runtime_state.attempts, before_attempts)
        self.assertEqual(ingress.state.canonical_events, before_events)


if __name__ == "__main__":
    unittest.main()
