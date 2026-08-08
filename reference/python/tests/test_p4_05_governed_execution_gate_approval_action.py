import ast
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.event_provenance import EventReceipt
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.execution_action_experience import (
    ActionCommitStatus,
    ActionReadiness,
    ExecutionInspectionBlockCode,
    ExecutionReferenceBasis,
    GovernedExecutionInspection,
    GovernedExecutionInspectionBlockedState,
    execute_canonical_mutation_action,
    inspect_governed_execution,
    prepare_canonical_mutation_action,
    render_governed_execution_html,
)
from arvectum_os_ref.governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedExecutionLineage,
    GovernedGateDecision,
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
    ConsequentialAttempt,
    ConsequentialOutcome,
    RetrySemantics,
    RuntimeConsistencyState,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass, build_p1_03_workflow
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


UTC = timezone.utc


class P405GovernedExecutionGateApprovalActionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.target = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )
        self.workflow = build_p1_03_workflow(
            organization=self.organization,
            actor=self.actor,
            target_record=self.target,
        )
        self.contract_pin = GovernedVersionPin(
            subject_id=self._id("product-contract-subject", "contract-a"),
            version_id=self._id("product-contract-version", "contract-a-v7"),
            semantic_type="platform.product-contract",
            authority_scope="platform.product-contract/boundary",
            lifecycle_status="Provisional",
        )
        self.required_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        self.created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            operation_name="update-reference-subject",
            material_inputs=(self.target,),
            required_gates=self.required_gates,
            execution_id=self._id("execution-subject", "execution-a"),
            version_id=self._id("execution-version", "execution-a-v1"),
            created_at=datetime(2026, 8, 8, 10, 0, tzinfo=UTC),
            product_contract=self.contract_pin,
        )
        self.awaiting = await_required_gates(
            self.created,
            version_id=self._id("execution-version", "execution-a-v2"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 10, 1, tzinfo=UTC),
        )
        self.allow_decisions = tuple(
            self._decision(kind=kind, outcome=GovernedGateOutcome.ALLOW, suffix=str(index))
            for index, kind in enumerate(self.required_gates, start=1)
        )
        self.ready = admit_ready_execution(
            self.awaiting,
            decisions=self.allow_decisions,
            version_id=self._id("execution-version", "execution-a-v3"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 10, 2, tzinfo=UTC),
        )
        self.running = transition_governed_execution(
            self.ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "execution-a-v4"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 10, 3, tzinfo=UTC),
        )
        self.lineage = GovernedExecutionLineage(
            (self.created, self.awaiting, self.ready, self.running)
        )
        self.runtime_state = RuntimeConsistencyState(canonical_records=(self.target,))
        self.candidate = self._candidate(
            version_value="subject-1-v2",
            predecessor=self.target.version_id,
        )
        self.event_receipt = self._event_receipt(
            candidate=self.candidate,
            execution=self.running,
            event_suffix="1",
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, "org-a")

    def _decision(
        self,
        *,
        kind: GovernedGateKind,
        outcome: GovernedGateOutcome,
        suffix: str,
    ) -> GovernedGateDecision:
        return build_governed_gate_decision(
            execution=self.awaiting,
            kind=kind,
            outcome=outcome,
            decision_actor=self.actor,
            basis_ref=self._id("gate-basis", f"{kind.value.lower()}-{suffix}"),
            decision_id=self._id("gate-decision-subject", f"{kind.value.lower()}-{suffix}"),
            version_id=self._id("gate-decision-version", f"{kind.value.lower()}-{suffix}-v1"),
            created_at=datetime(2026, 8, 8, 10, 1, 30, tzinfo=UTC),
        )

    def _state(
        self,
        *,
        actor: ActorContext | None = None,
        exact_version: Identity | None = None,
    ) -> WorkspaceShellState:
        actual_actor = actor or self.actor
        opened = open_workspace_shell(actual_actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        reference = (
            SubjectNavigationReference(self.organization, self.created.execution_subject_id)
            if exact_version is None
            else ExactVersionNavigationReference(
                self.organization,
                self.created.execution_subject_id,
                exact_version,
            )
        )
        return navigate_workspace(
            opened,
            destination=WorkspaceDestination.EXECUTIONS,
            reference=reference,
        )

    def _authorization(
        self,
        *,
        actor: ActorContext | None = None,
        allowed: bool = True,
        suffix: str = "1",
    ) -> CurrentSourceAuthorization:
        actual_actor = actor or self.actor
        return CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=actual_actor.actual_principal.principal_id,
            represented_principal_id=(
                None
                if actual_actor.represented_principal is None
                else actual_actor.represented_principal.principal_id
            ),
            resource_subject_id=self.created.execution_subject_id,
            decision_version_id=self._id("source-authorization-version", f"inspect-{suffix}"),
            allowed=allowed,
        )

    def _inspect(
        self,
        *,
        state: WorkspaceShellState | None = None,
        lineages: tuple[GovernedExecutionLineage, ...] | None = None,
        authorizations: tuple[CurrentSourceAuthorization, ...] | None = None,
        runtime_state: RuntimeConsistencyState | None = None,
    ):
        return inspect_governed_execution(
            state or self._state(),
            lineages=(self.lineage,) if lineages is None else lineages,
            authorizations=(self._authorization(),) if authorizations is None else authorizations,
            runtime_state=self.runtime_state if runtime_state is None else runtime_state,
        )

    def _candidate(self, *, version_value: str, predecessor: Identity) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=self.target.subject_id,
            version_id=self._id("canonical-version", version_value),
            semantic_type=self.target.semantic_type,
            schema_version=self.target.schema_version,
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=self.target.authority_scope,
            accountable_owner_id=self.target.accountable_owner_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 10, 5, tzinfo=UTC),
            provenance_refs=(
                self.actor.actual_principal.principal_id,
                self.running.execution_subject_id,
                self.running.execution_version_id,
                predecessor,
            ),
            integrity_metadata=(("representation", "p4.05-test"),),
            payload=(("label", version_value),),
            lifecycle_status="established",
            predecessor_version_id=predecessor,
        )

    def _event_receipt(
        self,
        *,
        candidate: CanonicalRecord,
        execution: GovernedExecutionContext,
        event_suffix: str,
    ) -> EventReceipt:
        producer = Identity("principal", "runtime-producer", "platform")
        return EventReceipt(
            event_id=self._id("event-subject", f"canonical-mutation-{event_suffix}"),
            version_id=self._id("event-version", f"canonical-mutation-{event_suffix}-v1"),
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS governed runtime",
            occurred_at=datetime(2026, 8, 8, 10, 5, tzinfo=UTC),
            recorded_at=datetime(2026, 8, 8, 10, 5, 1, tzinfo=UTC),
            producer_id=producer,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            execution_subject_id=execution.execution_subject_id,
            execution_version_id=execution.execution_version_id,
            related_subject_ids=(candidate.subject_id,),
            related_version_ids=(candidate.version_id,),
            correlation_refs=(execution.execution_subject_id,),
            causation_refs=(execution.execution_version_id,),
            classification="internal",
            access_scope="governed-action",
            provenance_refs=(
                producer,
                self.actor.actual_principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
            ),
            integrity_metadata=(("representation", "p4.05-test"),),
            payload=(("outcome", "succeeded"),),
        )

    def _prepare(self, *, runtime_state: RuntimeConsistencyState | None = None, candidate=None, event=None, token="action-1"):
        actual_state = runtime_state or self.runtime_state
        inspection = self._inspect(runtime_state=actual_state)
        self.assertIsInstance(inspection, GovernedExecutionInspection)
        return prepare_canonical_mutation_action(
            workspace=self._state(),
            inspection=inspection,
            execution=self.running,
            runtime_state=actual_state,
            candidate=candidate or self.candidate,
            event_receipt=event or self.event_receipt,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token=token,
        )

    def test_subject_inspection_exposes_exact_reliance_and_separate_gate_evidence(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(result.reference_basis, ExecutionReferenceBasis.EXECUTION_HEAD)
        self.assertEqual(result.displayed_execution_version_id, self.running.execution_version_id)
        self.assertEqual(result.workflow.version_id, self.workflow.workflow_version_id)
        self.assertEqual(result.material_inputs[0].version_id, self.target.version_id)
        self.assertEqual(result.product_contract.version_id, self.contract_pin.version_id)
        self.assertEqual(result.action_readiness, ActionReadiness.READY_TO_REQUEST_CANONICAL_COMMIT)
        self.assertEqual(result.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        by_kind = {row.kind: row for row in result.gates}
        self.assertEqual(by_kind[GovernedGateKind.AUTHORIZATION].outcome, GovernedGateOutcome.ALLOW)
        self.assertEqual(
            by_kind[GovernedGateKind.ORGANIZATIONAL_AUTHORITY].outcome,
            GovernedGateOutcome.ALLOW,
        )
        self.assertEqual(
            by_kind[GovernedGateKind.CONSEQUENTIAL_APPROVAL].outcome,
            GovernedGateOutcome.ALLOW,
        )
        self.assertNotEqual(
            by_kind[GovernedGateKind.AUTHORIZATION].decision_version_id,
            by_kind[GovernedGateKind.ORGANIZATIONAL_AUTHORITY].decision_version_id,
        )

    def test_unresolved_required_gates_fail_closed(self) -> None:
        lineage = GovernedExecutionLineage((self.created, self.awaiting))
        result = self._inspect(lineages=(lineage,))
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(result.lifecycle, GovernedExecutionLifecycle.AWAITING_GATE)
        self.assertEqual(result.action_readiness, ActionReadiness.AWAITING_REQUIRED_GATES)
        self.assertEqual(set(result.unresolved_gates), set(self.required_gates))
        with self.assertRaises(PermissionError):
            prepare_canonical_mutation_action(
                workspace=self._state(),
                inspection=result,
                execution=self.awaiting,
                runtime_state=self.runtime_state,
                candidate=self.candidate,
                event_receipt=self._event_receipt(
                    candidate=self.candidate,
                    execution=self.awaiting,
                    event_suffix="awaiting",
                ),
                retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
                retry_token="blocked",
            )

    def test_denied_gate_is_distinct_from_unresolved_and_blocks_action(self) -> None:
        denied = self._decision(
            kind=GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GovernedGateOutcome.DENY,
            suffix="deny",
        )
        waiting_record = replace(
            self.awaiting.record,
            version_id=self._id("execution-version", "execution-a-v2-denied"),
            created_at=datetime(2026, 8, 8, 10, 1, 50, tzinfo=UTC),
            provenance_refs=(*self.awaiting.record.provenance_refs, denied.record.version_id),
            lifecycle_status=GovernedExecutionLifecycle.WAITING.value,
            predecessor_version_id=self.awaiting.execution_version_id,
        )
        denied_waiting = GovernedExecutionContext(
            record=waiting_record,
            workflow=self.awaiting.workflow,
            operation_name=self.awaiting.operation_name,
            operation_side_effects=self.awaiting.operation_side_effects,
            material_inputs=self.awaiting.material_inputs,
            required_gates=self.awaiting.required_gates,
            gate_decisions=(denied,),
            product_contract=self.awaiting.product_contract,
        )
        lineage = GovernedExecutionLineage((self.created, self.awaiting, denied_waiting))
        result = self._inspect(lineages=(lineage,))
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(result.action_readiness, ActionReadiness.GATE_DENIED)
        self.assertIn(GovernedGateKind.ORGANIZATIONAL_AUTHORITY, result.denied_gates)
        self.assertIn(GovernedGateKind.AUTHORIZATION, result.unresolved_gates)

    def test_exact_historical_execution_version_is_inspectable_but_action_read_only(self) -> None:
        result = self._inspect(
            state=self._state(exact_version=self.ready.execution_version_id)
        )
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(result.reference_basis, ExecutionReferenceBasis.EXACT_EXECUTION_VERSION)
        self.assertEqual(result.displayed_execution_version_id, self.ready.execution_version_id)
        self.assertEqual(result.head_execution_version_id, self.running.execution_version_id)
        self.assertEqual(result.action_readiness, ActionReadiness.HISTORICAL_READ_ONLY)

    def test_source_authorization_precedes_exact_version_existence_disclosure(self) -> None:
        unknown = self._id("execution-version", "protected-question")
        result = self._inspect(
            state=self._state(exact_version=unknown),
            authorizations=(),
        )
        self.assertIsInstance(result, GovernedExecutionInspectionBlockedState)
        self.assertEqual(result.code, ExecutionInspectionBlockCode.ACCESS_DENIED)
        self.assertNotIn(unknown.value, result.status_text)

    def test_duplicate_denied_or_wrong_actor_source_authorization_fails_closed(self) -> None:
        other_actor = ActorContext(
            Principal(Identity("principal", "operator-2", "platform")),
            self.organization,
        )
        cases = (
            (self._authorization(allowed=False),),
            (self._authorization(suffix="a"), self._authorization(suffix="b")),
            (self._authorization(actor=other_actor),),
        )
        for authorizations in cases:
            with self.subTest(authorizations=authorizations):
                result = self._inspect(authorizations=authorizations)
                self.assertIsInstance(result, GovernedExecutionInspectionBlockedState)
                self.assertEqual(result.code, ExecutionInspectionBlockCode.ACCESS_DENIED)
                self.assertFalse(result.governed_content_visible)
                self.assertFalse(result.action_available)

    def test_read_authorized_different_actor_cannot_invoke_existing_execution(self) -> None:
        other_actor = ActorContext(
            Principal(Identity("principal", "operator-2", "platform")),
            self.organization,
        )
        state = self._state(actor=other_actor)
        result = self._inspect(
            state=state,
            authorizations=(self._authorization(actor=other_actor),),
        )
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(result.action_readiness, ActionReadiness.ACTOR_CONTEXT_BLOCKED)
        self.assertEqual(result.source_authorization_decision_version_id.value, "inspect-1")

    def test_action_intent_is_transient_and_does_not_mutate_runtime_state(self) -> None:
        before = self.runtime_state
        intent = self._prepare()
        self.assertIs(before, self.runtime_state)
        self.assertFalse(intent.committed)
        self.assertEqual(intent.expected_head_version_id, self.target.version_id)
        self.assertEqual(intent.execution.execution_version_id, self.running.execution_version_id)
        self.assertEqual(intent.candidate.version_id, self.candidate.version_id)
        self.assertEqual(intent.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)
        self.assertEqual(len(self.runtime_state.canonical_records), 1)
        self.assertEqual(len(self.runtime_state.admitted_events), 0)

    def test_action_commit_delegates_to_existing_governed_runtime_path(self) -> None:
        intent = self._prepare()
        result = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=intent,
            runtime_state=self.runtime_state,
        )
        self.assertEqual(result.status, ActionCommitStatus.COMMITTED)
        self.assertEqual(result.committed_record_version_id, self.candidate.version_id)
        self.assertEqual(result.event_version_id, self.event_receipt.version_id)
        self.assertFalse(result.duplicate)
        self.assertEqual(result.state.head.version_id, self.candidate.version_id)
        self.assertEqual(len(result.state.canonical_records), 2)
        self.assertEqual(len(result.state.admitted_events), 1)
        self.assertEqual(len(result.state.attempts), 1)

    def test_keyed_retry_returns_duplicate_without_second_effect(self) -> None:
        intent = self._prepare()
        first = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=intent,
            runtime_state=self.runtime_state,
        )
        second = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=intent,
            runtime_state=first.state,
        )
        self.assertEqual(second.status, ActionCommitStatus.IDEMPOTENT_DUPLICATE)
        self.assertTrue(second.duplicate)
        self.assertEqual(len(second.state.canonical_records), 2)
        self.assertEqual(len(second.state.admitted_events), 1)
        self.assertEqual(len(second.state.attempts), 1)

    def test_stale_head_is_understandable_and_does_not_mutate_current_state(self) -> None:
        intent = self._prepare()
        concurrent = self._candidate(
            version_value="subject-1-concurrent",
            predecessor=self.target.version_id,
        )
        current = RuntimeConsistencyState(canonical_records=(self.target, concurrent))
        result = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=intent,
            runtime_state=current,
        )
        self.assertEqual(result.status, ActionCommitStatus.STALE_OR_CONFLICT)
        self.assertIs(result.state, current)
        self.assertEqual(result.state.head.version_id, concurrent.version_id)
        self.assertIsNone(result.committed_record_version_id)
        self.assertIn("blocked without mutation", result.status_text)

    def test_retry_token_conflict_is_explicit(self) -> None:
        first_intent = self._prepare(token="shared-token")
        first = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=first_intent,
            runtime_state=self.runtime_state,
        )
        next_candidate = self._candidate(
            version_value="subject-1-v3",
            predecessor=self.candidate.version_id,
        )
        next_event = self._event_receipt(
            candidate=next_candidate,
            execution=self.running,
            event_suffix="2",
        )
        second_intent = self._prepare(
            runtime_state=first.state,
            candidate=next_candidate,
            event=next_event,
            token="shared-token",
        )
        second = execute_canonical_mutation_action(
            workspace=self._state(),
            intent=second_intent,
            runtime_state=first.state,
        )
        self.assertEqual(second.status, ActionCommitStatus.IDEMPOTENCY_CONFLICT)
        self.assertEqual(second.state.head.version_id, self.candidate.version_id)
        self.assertIsNone(second.committed_record_version_id)

    def test_uncertain_attempt_is_presented_as_reconciliation_required_without_token_value(self) -> None:
        attempt = ConsequentialAttempt(
            execution_subject_id=self.running.execution_subject_id,
            execution_version_id=self.running.execution_version_id,
            operation_name=self.running.operation_name,
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="sensitive-retry-token",
            fingerprint=("bounded", "uncertain", "attempt"),
            outcome=ConsequentialOutcome.UNCERTAIN,
        )
        state = RuntimeConsistencyState(
            canonical_records=(self.target,),
            attempts=(attempt,),
        )
        result = self._inspect(runtime_state=state)
        self.assertIsInstance(result, GovernedExecutionInspection)
        self.assertEqual(len(result.attempts), 1)
        self.assertTrue(result.attempts[0].retry_token_present)
        self.assertTrue(result.attempts[0].reconciliation_required)
        html = render_governed_execution_html(result)
        self.assertIn("Reconciliation", html)
        self.assertNotIn("sensitive-retry-token", html)
        self.assertIn("blind retry", html)

    def test_renderer_keeps_authorization_authority_approval_and_intent_distinct(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, GovernedExecutionInspection)
        html = render_governed_execution_html(result)
        self.assertIn("Authorization", html)
        self.assertIn("OrganizationalAuthority", html)
        self.assertIn("ConsequentialApproval", html)
        self.assertIn("separate decisions", html)
        self.assertIn("UI title, role label", html)
        self.assertIn("Action intent is transient", html)
        self.assertIn("non-authoritative presentation", html)
        self.assertIn(self.contract_pin.version_id.value, html)
        self.assertIn(self.target.version_id.value, html)

    def test_renderer_escapes_governed_text_and_does_not_create_mutating_control(self) -> None:
        result = self._inspect()
        self.assertIsInstance(result, GovernedExecutionInspection)
        malicious = replace(result, operation_name='<script>alert("x")</script>')
        html = render_governed_execution_html(malicious)
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn("<form", html.lower())
        self.assertNotIn("onclick=", html.lower())

    def test_module_remains_internal_and_free_of_durable_frontend_or_network_choices(self) -> None:
        module_path = (
            Path(__file__).resolve().parents[1]
            / "arvectum_os_ref"
            / "execution_action_experience.py"
        )
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        roots: set[str] = set()
        imported_names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    roots.add(node.module.split(".")[0])
                imported_names.update(alias.name for alias in node.names)
        forbidden = {
            "fastapi",
            "flask",
            "django",
            "starlette",
            "sqlalchemy",
            "psycopg",
            "requests",
            "httpx",
            "aiohttp",
            "selenium",
            "playwright",
            "redis",
            "kafka",
        }
        self.assertTrue(roots.isdisjoint(forbidden))
        self.assertIn("commit_canonical_mutation", imported_names)


if __name__ == "__main__":
    unittest.main()
