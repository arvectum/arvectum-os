from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
import inspect
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.governed_execution import (
    ConsequentialOperationNotAdmittedError,
    ExecutionTransitionError,
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedExecutionLineage,
    GovernedGateKind,
    GovernedGateOutcome,
    RequiredGateDeniedError,
    RequiredGateUnresolvedError,
    TerminalExecutionSealedError,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    evaluate_required_gates,
    require_consequential_operation_admission,
    resume_governed_execution,
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


class P204GovernedExecutionRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "principal-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.decision_actor = ActorContext(
            Principal(Identity("principal", "decision-principal", "platform")),
            self.organization,
        )
        self.subject = self._record("subject-a", "subject-a-v1", "example.subject")
        self.contract = self._record(
            "contract-a",
            "contract-a-v3",
            "platform.product-contract",
            lifecycle="Provisional",
            authority_scope="platform.product-contract/boundary",
        )
        self.contract_pin = GovernedVersionPin.from_record(self.contract)
        self.workflow = self._workflow(
            "workflow-a",
            "workflow-a-v2",
            "update-subject",
            self.subject,
            (OperationSideEffectClass.CANONICAL_MUTATION,),
        )
        self.required_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.VALIDATION,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        self.created = self._start(
            self.workflow,
            "update-subject",
            (self.subject,),
            self.required_gates,
            execution="execution-a",
            version="execution-a-v1",
            contract=self.contract_pin,
        )
        self.awaiting = await_required_gates(
            self.created,
            version_id=self._id("execution-version", "execution-a-v2"),
            actor=self.actor,
            created_at=self._time(2),
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
        lifecycle: str = "Active",
        authority_scope: str = "example.subject/state",
        organization: OrganizationScope | None = None,
        actor: ActorContext | None = None,
    ) -> CanonicalRecord:
        organization = organization or self.organization
        actor = actor or self.actor
        scope = organization.organization_id.value
        return CanonicalRecord(
            subject_id=Identity("canonical-subject", subject, scope),
            version_id=Identity("canonical-version", version, scope),
            semantic_type=semantic_type,
            schema_version="1",
            organization=organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope,
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=self._time(0),
            provenance_refs=(actor.actual_principal.principal_id,),
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
            provenance_refs=(self.principal.principal_id, target.subject_id),
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

    def _start(
        self,
        workflow: WorkflowDefinition,
        operation: str,
        material_inputs: tuple[CanonicalRecord, ...],
        required_gates: tuple[GovernedGateKind, ...],
        *,
        execution: str,
        version: str,
        contract: GovernedVersionPin | None = None,
    ) -> GovernedExecutionContext:
        return start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=workflow,
            operation_name=operation,
            material_inputs=material_inputs,
            required_gates=required_gates,
            execution_id=self._id("execution-subject", execution),
            version_id=self._id("execution-version", version),
            created_at=self._time(1),
            product_contract=contract,
        )

    def _decision(
        self,
        execution: GovernedExecutionContext,
        kind: GovernedGateKind,
        *,
        outcome: GovernedGateOutcome = GovernedGateOutcome.ALLOW,
        suffix: str | None = None,
    ):
        suffix = suffix or kind.value.lower()
        return build_governed_gate_decision(
            execution=execution,
            kind=kind,
            outcome=outcome,
            decision_actor=self.decision_actor,
            basis_ref=self._id("governed-basis", f"basis-{suffix}"),
            decision_id=self._id("gate-decision-subject", f"decision-{suffix}"),
            version_id=self._id("gate-decision-version", f"decision-{suffix}-v1"),
            created_at=self._time(3),
        )

    def _allow_all(self, execution: GovernedExecutionContext):
        return tuple(
            self._decision(execution, kind, suffix=f"{kind.value.lower()}-{index}")
            for index, kind in enumerate(execution.required_gates, start=1)
        )

    def _ready(self) -> GovernedExecutionContext:
        return admit_ready_execution(
            self.awaiting,
            decisions=self._allow_all(self.awaiting),
            version_id=self._id("execution-version", "execution-a-v3"),
            actor=self.actor,
            created_at=self._time(4),
        )

    def _running(self) -> GovernedExecutionContext:
        return transition_governed_execution(
            self._ready(),
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "execution-a-v4"),
            actor=self.actor,
            created_at=self._time(5),
        )

    def test_created_pins_exact_workflow_input_and_product_contract(self) -> None:
        self.assertEqual(self.created.lifecycle, GovernedExecutionLifecycle.CREATED)
        self.assertEqual(self.created.workflow.version_id, self.workflow.workflow_version_id)
        self.assertEqual(self.created.material_inputs[0].version_id, self.subject.version_id)
        self.assertEqual(self.created.product_contract, self.contract_pin)
        for ref in (
            self.workflow.workflow_version_id,
            self.subject.version_id,
            self.contract.version_id,
        ):
            self.assertIn(ref, self.created.record.provenance_refs)

    def test_context_and_exact_pins_are_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            self.created.operation_name = "changed"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            self.created.material_inputs[0].version_id = self.subject.subject_id  # type: ignore[misc]

    def test_consequential_operation_requires_explicit_authorization_gate(self) -> None:
        with self.assertRaises(ValueError):
            self._start(
                self.workflow,
                "update-subject",
                (self.subject,),
                (GovernedGateKind.ORGANIZATIONAL_AUTHORITY,),
                execution="missing-auth",
                version="missing-auth-v1",
            )

    def test_start_fails_closed_for_scope_or_operation_mismatch(self) -> None:
        other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        other_actor = ActorContext(self.principal, other_org)
        other = self._record(
            "other",
            "other-v1",
            "example.subject",
            organization=other_org,
            actor=other_actor,
        )
        with self.assertRaises(ValueError):
            self._start(
                self.workflow,
                "update-subject",
                (other,),
                self.required_gates,
                execution="cross-org",
                version="cross-org-v1",
            )
        with self.assertRaises(ValueError):
            self._start(
                self.workflow,
                "not-declared",
                (self.subject,),
                self.required_gates,
                execution="wrong-operation",
                version="wrong-operation-v1",
            )

    def test_awaiting_gate_is_immutable_successor_without_claimed_decisions(self) -> None:
        self.assertEqual(self.awaiting.lifecycle, GovernedExecutionLifecycle.AWAITING_GATE)
        self.assertEqual(self.awaiting.record.predecessor_version_id, self.created.execution_version_id)
        self.assertFalse(self.awaiting.gate_decisions)
        self.assertEqual(self.created.lifecycle, GovernedExecutionLifecycle.CREATED)

    def test_six_gate_concepts_remain_distinct(self) -> None:
        self.assertEqual(len(set(GovernedGateKind)), 6)
        self.assertNotEqual(GovernedGateKind.AUTHORIZATION, GovernedGateKind.ORGANIZATIONAL_AUTHORITY)
        self.assertNotEqual(GovernedGateKind.DATA_GOVERNANCE, GovernedGateKind.VALIDATION)
        self.assertNotEqual(GovernedGateKind.VALIDATION, GovernedGateKind.CONSEQUENTIAL_APPROVAL)

    def test_gate_decision_pins_exact_execution_workflow_inputs_and_contract(self) -> None:
        decision = self._decision(self.awaiting, GovernedGateKind.AUTHORIZATION)
        self.assertEqual(decision.execution_subject_id, self.awaiting.execution_subject_id)
        self.assertEqual(decision.evaluated_execution_version_id, self.awaiting.execution_version_id)
        self.assertEqual(decision.workflow_version_id, self.workflow.workflow_version_id)
        self.assertEqual(decision.material_input_version_ids, (self.subject.version_id,))
        self.assertEqual(decision.product_contract_version_id, self.contract.version_id)

    def test_stale_gate_decision_cannot_be_reused_after_re_evaluation_boundary(self) -> None:
        stale = self._decision(self.awaiting, GovernedGateKind.AUTHORIZATION, suffix="stale")
        waiting = transition_governed_execution(
            self.awaiting,
            lifecycle=GovernedExecutionLifecycle.WAITING,
            version_id=self._id("execution-version", "execution-a-waiting"),
            actor=self.actor,
            created_at=self._time(4),
        )
        reevaluate = await_required_gates(
            waiting,
            version_id=self._id("execution-version", "execution-a-reevaluate"),
            actor=self.actor,
            created_at=self._time(5),
        )
        with self.assertRaises(ValueError):
            evaluate_required_gates(execution=reevaluate, decisions=(stale,))

    def test_missing_and_denied_required_gates_fail_closed(self) -> None:
        authorization = self._decision(self.awaiting, GovernedGateKind.AUTHORIZATION)
        evaluation = evaluate_required_gates(execution=self.awaiting, decisions=(authorization,))
        self.assertFalse(evaluation.can_proceed)
        self.assertIn(GovernedGateKind.ORGANIZATIONAL_AUTHORITY, evaluation.unresolved_gates)
        with self.assertRaises(RequiredGateUnresolvedError):
            admit_ready_execution(
                self.awaiting,
                decisions=(authorization,),
                version_id=self._id("execution-version", "not-ready"),
                actor=self.actor,
                created_at=self._time(4),
            )

        decisions = list(self._allow_all(self.awaiting))
        decisions[0] = self._decision(
            self.awaiting,
            GovernedGateKind.AUTHORIZATION,
            outcome=GovernedGateOutcome.DENY,
            suffix="authorization-deny",
        )
        with self.assertRaises(RequiredGateDeniedError):
            admit_ready_execution(
                self.awaiting,
                decisions=tuple(decisions),
                version_id=self._id("execution-version", "denied"),
                actor=self.actor,
                created_at=self._time(4),
            )

    def test_duplicate_gate_kind_is_rejected(self) -> None:
        one = self._decision(self.awaiting, GovernedGateKind.AUTHORIZATION, suffix="one")
        two = self._decision(self.awaiting, GovernedGateKind.AUTHORIZATION, suffix="two")
        with self.assertRaises(ValueError):
            evaluate_required_gates(execution=self.awaiting, decisions=(one, two))

    def test_ready_pins_every_exact_gate_decision_and_generic_transition_cannot_bypass_gates(self) -> None:
        ready = self._ready()
        self.assertTrue(ready.gates_satisfied)
        self.assertFalse(ready.unresolved_gates)
        for decision in ready.gate_decisions:
            self.assertIn(decision.record.version_id, ready.record.provenance_refs)
        with self.assertRaises(ExecutionTransitionError):
            transition_governed_execution(
                self.awaiting,
                lifecycle=GovernedExecutionLifecycle.READY,
                version_id=self._id("execution-version", "bypass-ready"),
                actor=self.actor,
                created_at=self._time(4),
            )

    def test_running_waiting_and_resumption_preserve_or_re_evaluate_gate_evidence_explicitly(self) -> None:
        running = self._running()
        waiting = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.WAITING,
            version_id=self._id("execution-version", "execution-a-v5"),
            actor=self.actor,
            created_at=self._time(6),
        )
        resumed = resume_governed_execution(
            waiting,
            gates_still_valid=True,
            version_id=self._id("execution-version", "execution-a-v6"),
            actor=self.actor,
            created_at=self._time(7),
        )
        self.assertEqual(resumed.lifecycle, GovernedExecutionLifecycle.RUNNING)
        self.assertEqual(resumed.gate_decisions, waiting.gate_decisions)

        suspended = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.SUSPENDED,
            version_id=self._id("execution-version", "execution-a-suspended"),
            actor=self.actor,
            created_at=self._time(6),
        )
        reevaluate = resume_governed_execution(
            suspended,
            gates_still_valid=False,
            version_id=self._id("execution-version", "execution-a-recheck"),
            actor=self.actor,
            created_at=self._time(7),
        )
        self.assertEqual(reevaluate.lifecycle, GovernedExecutionLifecycle.AWAITING_GATE)
        self.assertFalse(reevaluate.gate_decisions)
        self.assertEqual(reevaluate.unresolved_gates, reevaluate.required_gates)

    def test_terminal_success_failure_cancel_and_compensation_are_sealed(self) -> None:
        running = self._running()
        succeeded = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=self._id("execution-version", "execution-a-succeeded"),
            actor=self.actor,
            created_at=self._time(6),
        )
        with self.assertRaises(TerminalExecutionSealedError):
            transition_governed_execution(
                succeeded,
                lifecycle=GovernedExecutionLifecycle.RUNNING,
                version_id=self._id("execution-version", "after-success"),
                actor=self.actor,
                created_at=self._time(7),
            )

        failed = transition_governed_execution(
            self.awaiting,
            lifecycle=GovernedExecutionLifecycle.FAILED,
            version_id=self._id("execution-version", "execution-a-failed"),
            actor=self.actor,
            created_at=self._time(4),
        )
        cancelled = transition_governed_execution(
            self.created,
            lifecycle=GovernedExecutionLifecycle.CANCELLED,
            version_id=self._id("execution-version", "execution-a-cancelled"),
            actor=self.actor,
            created_at=self._time(2),
        )
        self.assertTrue(failed.is_terminal)
        self.assertTrue(cancelled.is_terminal)

        compensating = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.COMPENSATING,
            version_id=self._id("execution-version", "execution-a-compensating"),
            actor=self.actor,
            created_at=self._time(6),
        )
        compensated = transition_governed_execution(
            compensating,
            lifecycle=GovernedExecutionLifecycle.COMPENSATED,
            version_id=self._id("execution-version", "execution-a-compensated"),
            actor=self.actor,
            created_at=self._time(7),
        )
        self.assertTrue(compensated.is_terminal)

    def test_execution_lineage_preserves_head_exact_history_and_rejects_terminal_successor(self) -> None:
        ready = self._ready()
        running = transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "execution-a-lineage-running"),
            actor=self.actor,
            created_at=self._time(5),
        )
        lineage = GovernedExecutionLineage((self.created, self.awaiting, ready, running))
        self.assertEqual(lineage.head(), running)
        self.assertEqual(lineage.exact(self.created.execution_version_id), self.created)

        terminal = transition_governed_execution(
            running,
            lifecycle=GovernedExecutionLifecycle.SUCCEEDED,
            version_id=self._id("execution-version", "execution-a-lineage-terminal"),
            actor=self.actor,
            created_at=self._time(6),
        )
        illegal_record = CanonicalRecord(
            subject_id=terminal.execution_subject_id,
            version_id=self._id("execution-version", "execution-a-after-terminal"),
            semantic_type=terminal.record.semantic_type,
            schema_version=terminal.record.schema_version,
            organization=self.organization,
            authority_mode=terminal.record.authority_mode,
            authority_scope=terminal.record.authority_scope,
            accountable_owner_id=terminal.record.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self._time(7),
            provenance_refs=terminal.record.provenance_refs,
            integrity_metadata=terminal.record.integrity_metadata,
            payload=terminal.record.payload,
            lifecycle_status=GovernedExecutionLifecycle.RUNNING.value,
            predecessor_version_id=terminal.execution_version_id,
        )
        illegal = GovernedExecutionContext(
            record=illegal_record,
            workflow=terminal.workflow,
            operation_name=terminal.operation_name,
            operation_side_effects=terminal.operation_side_effects,
            material_inputs=terminal.material_inputs,
            required_gates=terminal.required_gates,
            gate_decisions=terminal.gate_decisions,
            product_contract=terminal.product_contract,
        )
        with self.assertRaises(TerminalExecutionSealedError):
            GovernedExecutionLineage((self.created, self.awaiting, ready, running, terminal, illegal))

    def test_direct_or_pregate_consequential_effect_is_rejected_and_only_declared_effect_is_admitted(self) -> None:
        with self.assertRaises(ConsequentialOperationNotAdmittedError):
            require_consequential_operation_admission(
                None,
                side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            )
        with self.assertRaises(ConsequentialOperationNotAdmittedError):
            require_consequential_operation_admission(
                self.awaiting,
                side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            )
        ready = self._ready()
        require_consequential_operation_admission(
            ready,
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
        )
        with self.assertRaises(ConsequentialOperationNotAdmittedError):
            require_consequential_operation_admission(
                ready,
                side_effect_class=OperationSideEffectClass.COMMITMENT,
            )

    def test_read_only_workflow_without_required_gates_can_admit_directly(self) -> None:
        workflow = self._workflow(
            "workflow-read",
            "workflow-read-v1",
            "inspect-subject",
            self.subject,
            (OperationSideEffectClass.READ_ONLY,),
        )
        created = self._start(
            workflow,
            "inspect-subject",
            (self.subject,),
            (),
            execution="execution-read",
            version="execution-read-v1",
        )
        ready = admit_ready_execution(
            created,
            decisions=(),
            version_id=self._id("execution-version", "execution-read-v2"),
            actor=self.actor,
            created_at=self._time(2),
        )
        self.assertEqual(ready.lifecycle, GovernedExecutionLifecycle.READY)
        self.assertTrue(ready.gates_satisfied)

    def test_same_runtime_supports_materially_distinct_commitment_workflow_shape(self) -> None:
        target = self._record(
            "subject-b",
            "subject-b-v1",
            "example.commitment-target",
            authority_scope="example.commitment/state",
        )
        workflow = self._workflow(
            "workflow-b",
            "workflow-b-v1",
            "create-commitment",
            target,
            (OperationSideEffectClass.EXTERNAL_MUTATION, OperationSideEffectClass.COMMITMENT),
        )
        required = (
            GovernedGateKind.ACTOR_ASSURANCE,
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        created = self._start(
            workflow,
            "create-commitment",
            (target,),
            required,
            execution="execution-b",
            version="execution-b-v1",
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", "execution-b-v2"),
            actor=self.actor,
            created_at=self._time(2),
        )
        decisions = tuple(
            self._decision(awaiting, kind, suffix=f"workflow-b-{index}")
            for index, kind in enumerate(required, start=1)
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=self._id("execution-version", "execution-b-v3"),
            actor=self.actor,
            created_at=self._time(4),
        )
        require_consequential_operation_admission(
            ready,
            side_effect_class=OperationSideEffectClass.COMMITMENT,
        )
        self.assertEqual(ready.operation_name, "create-commitment")
        self.assertEqual(set(ready.required_gates), set(required))
        self.assertIsNone(ready.product_contract)

    def test_product_contract_possession_does_not_satisfy_any_gate(self) -> None:
        self.assertEqual(self.awaiting.product_contract, self.contract_pin)
        self.assertEqual(self.awaiting.unresolved_gates, self.required_gates)
        with self.assertRaises(RequiredGateUnresolvedError):
            admit_ready_execution(
                self.awaiting,
                decisions=(),
                version_id=self._id("execution-version", "contract-does-not-authorize"),
                actor=self.actor,
                created_at=self._time(4),
            )

    def test_runtime_boundary_does_not_preempt_p2_05_p2_06_or_p1_specific_orchestration(self) -> None:
        import arvectum_os_ref.governed_execution as module

        source = inspect.getsource(module).lower()
        for forbidden in (
            "from .events",
            "from .provenance",
            "sqlite",
            "sqlalchemy",
            "kafka",
            "bpmn",
            "start_p1_04_execution",
            "build_p1_05_gate_decision",
        ):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
