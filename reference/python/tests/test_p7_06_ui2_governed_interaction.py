from __future__ import annotations

import ast
import http.client
import json
import os
import re
import tempfile
import threading
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.event_provenance import EventReceipt
from arvectum_os_ref.governed_execution import (
    GovernedExecutionContext,
    GovernedExecutionLifecycle,
    GovernedExecutionLineage,
    GovernedGateKind,
    GovernedGateOutcome,
    admit_ready_execution,
    await_required_gates,
    build_governed_gate_decision,
    start_governed_execution,
    transition_governed_execution,
)
from arvectum_os_ref.governed_interaction_preflight import (
    CORE_PREFLIGHT_GATES,
    GovernedInteractionBlocked,
    GovernedInteractionCase,
    GovernedInteractionOutcome,
    GovernedInteractionPreflight,
    PreflightGateState,
    build_governed_interaction_preflight,
    execute_governed_interaction,
    render_governed_interaction_preflight_html,
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
from arvectum_os_ref.workspace_shell import WorkspaceShellState, open_workspace_shell

import p7_03_durable_state as p703
import p7_04_persistent_access as p704
import p7_06_ui1_live_workspace as ui1
import p7_06_ui2_governed_interaction as ui2


UTC = timezone.utc
RELEASE = "c" * 40


class P706UI2GovernedInteractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-ui2", "platform"))
        self.principal = Principal(Identity("principal", "owner-ui2", "org-ui2"))
        self.actor = ActorContext(self.principal, self.organization)
        opened = open_workspace_shell(self.actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        self.workspace = opened

        self.target = build_p1_02_native_record(
            organization=self.organization,
            actor=self.actor,
        )
        self.workflow = build_p1_03_workflow(
            organization=self.organization,
            actor=self.actor,
            target_record=self.target,
        )
        self.created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            operation_name="update-reference-subject",
            material_inputs=(self.target,),
            required_gates=CORE_PREFLIGHT_GATES,
            execution_id=self._id("execution-subject", "ui2-execution"),
            version_id=self._id("execution-version", "ui2-execution-v1"),
            created_at=self._time(0),
        )
        self.awaiting = await_required_gates(
            self.created,
            version_id=self._id("execution-version", "ui2-execution-v2"),
            actor=self.actor,
            created_at=self._time(1),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=self.awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=self.actor,
                basis_ref=self._id("gate-basis", f"{kind.value}-basis"),
                decision_id=self._id("gate-decision-subject", f"{kind.value}-decision"),
                version_id=self._id("gate-decision-version", f"{kind.value}-decision-v1"),
                created_at=self._time(2 + index),
            )
            for index, kind in enumerate(CORE_PREFLIGHT_GATES)
        )
        self.ready = admit_ready_execution(
            self.awaiting,
            decisions=decisions,
            version_id=self._id("execution-version", "ui2-execution-v3"),
            actor=self.actor,
            created_at=self._time(10),
        )
        self.running = transition_governed_execution(
            self.ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "ui2-execution-v4"),
            actor=self.actor,
            created_at=self._time(11),
        )
        self.lineage = GovernedExecutionLineage(
            (self.created, self.awaiting, self.ready, self.running)
        )
        self.runtime_state = RuntimeConsistencyState(canonical_records=(self.target,))
        self.candidate = CanonicalRecord(
            subject_id=self.target.subject_id,
            version_id=self._id("canonical-version", "ui2-target-v2"),
            semantic_type=self.target.semantic_type,
            schema_version=self.target.schema_version,
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=self.target.authority_scope,
            accountable_owner_id=self.target.accountable_owner_id,
            creation_actor=self.actor,
            created_at=self._time(12),
            provenance_refs=(
                self.actor.actual_principal.principal_id,
                self.running.execution_subject_id,
                self.running.execution_version_id,
                self.target.version_id,
            ),
            integrity_metadata=(("representation", "p7.06-ui2-test"),),
            payload=(("label", "ui2 bounded successor"),),
            lifecycle_status="established",
            predecessor_version_id=self.target.version_id,
        )
        self.event_receipt = self._event(self.running)
        self.authorization = CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            represented_principal_id=None,
            resource_subject_id=self.running.execution_subject_id,
            decision_version_id=self._id("source-authorization-version", "ui2-inspection-allow-v1"),
            allowed=True,
        )
        self.case = GovernedInteractionCase(
            interaction_id="interaction-1",
            organization=self.organization,
            actor=self.actor,
            source_record=self.target,
            execution_lineage=self.lineage,
            runtime_state=self.runtime_state,
            candidate=self.candidate,
            event_receipt=self.event_receipt,
            source_authorizations=(self.authorization,),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="ui2-action-1",
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, self.organization.organization_id.value)

    @staticmethod
    def _time(offset: int):
        return datetime(2026, 8, 18, 12, 0, offset, tzinfo=UTC)

    def _event(self, execution: GovernedExecutionContext) -> EventReceipt:
        producer = self._id("principal", "ui2-runtime-producer")
        return EventReceipt(
            event_id=self._id("event-subject", f"{execution.execution_version_id.value}-commit"),
            version_id=self._id("event-version", f"{execution.execution_version_id.value}-commit-v1"),
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS governed runtime",
            occurred_at=self._time(13),
            recorded_at=self._time(14),
            producer_id=producer,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            execution_subject_id=execution.execution_subject_id,
            execution_version_id=execution.execution_version_id,
            related_subject_ids=(self.candidate.subject_id,),
            related_version_ids=(self.candidate.version_id,),
            correlation_refs=(execution.execution_subject_id,),
            causation_refs=(execution.execution_version_id,),
            classification="internal",
            access_scope="governed-action",
            provenance_refs=(
                producer,
                self.actor.actual_principal.principal_id,
                execution.execution_subject_id,
                execution.execution_version_id,
                self.candidate.subject_id,
                self.candidate.version_id,
            ),
            integrity_metadata=(("representation", "p7.06-ui2-test"),),
            payload=(("outcome", "succeeded"),),
        )

    def test_ready_preflight_preserves_exact_context_and_four_independent_gate_states(self) -> None:
        result = build_governed_interaction_preflight(self.workspace, case=self.case)
        self.assertIsInstance(result, GovernedInteractionPreflight)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.READY)
        self.assertEqual(result.organization, self.organization)
        self.assertEqual(result.actor, self.actor)
        self.assertEqual(result.source_subject_id, self.target.subject_id)
        self.assertEqual(result.source_version_id, self.target.version_id)
        self.assertEqual(result.execution_version_id, self.running.execution_version_id)
        self.assertEqual(result.workflow_version_id, self.workflow.workflow_version_id)
        self.assertEqual(tuple(row.kind for row in result.gates), CORE_PREFLIGHT_GATES)
        self.assertTrue(all(row.state is PreflightGateState.ALLOW for row in result.gates))
        self.assertEqual(
            len({row.decision_version_id for row in result.gates}),
            len(CORE_PREFLIGHT_GATES),
        )
        html = render_governed_interaction_preflight_html(
            result, interaction_id=self.case.interaction_id, csrf_token="test-csrf"
        )
        for kind in CORE_PREFLIGHT_GATES:
            self.assertIn(kind.value, html)
        self.assertIn(self.target.version_id.value, html)
        self.assertIn(self.running.execution_version_id.value, html)
        self.assertIn("Request governed action", html)
        self.assertIn("Button state is not a security boundary", html)
        self.assertNotIn(str(self.candidate.payload), html)

    def test_unresolved_required_gates_render_waiting_without_action_form(self) -> None:
        waiting_lineage = GovernedExecutionLineage((self.created, self.awaiting))
        waiting_case = replace(
            self.case,
            execution_lineage=waiting_lineage,
            event_receipt=self._event(self.awaiting),
        )
        result = build_governed_interaction_preflight(self.workspace, case=waiting_case)
        self.assertIsInstance(result, GovernedInteractionPreflight)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.WAITING)
        self.assertTrue(all(row.state is PreflightGateState.WAITING for row in result.gates))
        html = render_governed_interaction_preflight_html(
            result, interaction_id=waiting_case.interaction_id, csrf_token="test"
        )
        self.assertNotIn("<form", html)
        self.assertIn("No governed action request", html)

    def test_denied_gate_is_distinct_from_waiting_and_blocks_action(self) -> None:
        denied = build_governed_gate_decision(
            execution=self.awaiting,
            kind=GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            outcome=GovernedGateOutcome.DENY,
            decision_actor=self.actor,
            basis_ref=self._id("gate-basis", "organizational-authority-denied"),
            decision_id=self._id("gate-decision-subject", "organizational-authority-denied"),
            version_id=self._id("gate-decision-version", "organizational-authority-denied-v1"),
            created_at=self._time(9),
        )
        denied_record = replace(
            self.awaiting.record,
            version_id=self._id("execution-version", "ui2-execution-v2-denied"),
            created_at=self._time(10),
            provenance_refs=(*self.awaiting.record.provenance_refs, denied.record.version_id),
            lifecycle_status=GovernedExecutionLifecycle.WAITING.value,
            predecessor_version_id=self.awaiting.execution_version_id,
        )
        denied_execution = GovernedExecutionContext(
            record=denied_record,
            workflow=self.awaiting.workflow,
            operation_name=self.awaiting.operation_name,
            operation_side_effects=self.awaiting.operation_side_effects,
            material_inputs=self.awaiting.material_inputs,
            required_gates=self.awaiting.required_gates,
            gate_decisions=(denied,),
            product_contract=self.awaiting.product_contract,
        )
        denied_case = replace(
            self.case,
            execution_lineage=GovernedExecutionLineage(
                (self.created, self.awaiting, denied_execution)
            ),
            event_receipt=self._event(denied_execution),
        )
        result = build_governed_interaction_preflight(self.workspace, case=denied_case)
        self.assertIsInstance(result, GovernedInteractionPreflight)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.BLOCKED)
        by_kind = {row.kind: row for row in result.gates}
        self.assertEqual(
            by_kind[GovernedGateKind.ORGANIZATIONAL_AUTHORITY].state,
            PreflightGateState.DENY,
        )
        self.assertEqual(
            by_kind[GovernedGateKind.AUTHORIZATION].state,
            PreflightGateState.WAITING,
        )
        execution = execute_governed_interaction(self.workspace, case=denied_case)
        self.assertEqual(execution.outcome, GovernedInteractionOutcome.BLOCKED)
        self.assertEqual(execution.runtime_state, self.runtime_state)

    def test_missing_source_authorization_fails_closed_without_protected_identity_or_gates(self) -> None:
        blocked_case = replace(self.case, source_authorizations=())
        result = build_governed_interaction_preflight(self.workspace, case=blocked_case)
        self.assertIsInstance(result, GovernedInteractionBlocked)
        html = render_governed_interaction_preflight_html(result)
        self.assertNotIn(self.target.subject_id.value, html)
        self.assertNotIn(self.target.version_id.value, html)
        self.assertNotIn(self.running.execution_version_id.value, html)
        for kind in CORE_PREFLIGHT_GATES:
            self.assertNotIn(kind.value, html)

    def test_uncertain_attempt_requires_reconciliation_and_never_blind_retry(self) -> None:
        attempt = ConsequentialAttempt(
            execution_subject_id=self.running.execution_subject_id,
            execution_version_id=self.running.execution_version_id,
            operation_name=self.running.operation_name,
            side_effect_class=OperationSideEffectClass.CANONICAL_MUTATION,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="ui2-action-1",
            fingerprint=("ui2", "uncertain"),
            outcome=ConsequentialOutcome.UNCERTAIN,
        )
        uncertain = replace(
            self.case,
            runtime_state=RuntimeConsistencyState(
                canonical_records=(self.target,),
                attempts=(attempt,),
            ),
        )
        result = build_governed_interaction_preflight(self.workspace, case=uncertain)
        self.assertIsInstance(result, GovernedInteractionPreflight)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.RECONCILIATION_REQUIRED)
        execution = execute_governed_interaction(self.workspace, case=uncertain)
        self.assertEqual(
            execution.outcome, GovernedInteractionOutcome.RECONCILIATION_REQUIRED
        )
        self.assertEqual(execution.runtime_state, uncertain.runtime_state)
        self.assertIsNone(execution.committed_record_version_id)

    def test_allowed_interaction_delegates_to_existing_governed_runtime_and_returns_exact_evidence(self) -> None:
        result = execute_governed_interaction(self.workspace, case=self.case)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.SUCCEEDED)
        self.assertEqual(result.committed_record_version_id, self.candidate.version_id)
        self.assertEqual(result.event_version_id, self.event_receipt.version_id)
        self.assertEqual(result.runtime_state.head.version_id, self.candidate.version_id)
        self.assertEqual(len(result.runtime_state.attempts), 1)
        self.assertEqual(
            result.runtime_state.attempts[0].outcome,
            ConsequentialOutcome.SUCCEEDED,
        )

    def test_changed_source_access_between_view_and_request_is_repreflighted_and_blocked(self) -> None:
        stale = replace(self.case, source_authorizations=())
        result = execute_governed_interaction(self.workspace, case=stale)
        self.assertEqual(result.outcome, GovernedInteractionOutcome.BLOCKED)
        self.assertEqual(result.runtime_state, self.runtime_state)
        self.assertIsNone(result.committed_record_version_id)

    def test_ui2_package_composition_uses_operator_safety_not_direct_mutation_primitive(self) -> None:
        module_path = (
            Path(__file__).resolve().parents[1]
            / "arvectum_os_ref"
            / "governed_interaction_preflight.py"
        )
        source = module_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                imported.update(alias.name for alias in node.names)
        self.assertIn("prepare_operator_canonical_mutation_action", imported)
        self.assertIn("execute_operator_canonical_mutation_action", imported)
        self.assertNotIn("prepare_canonical_mutation_action", imported)
        self.assertNotIn("execute_canonical_mutation_action", imported)
        self.assertNotIn("commit_canonical_mutation", imported)


class P706UI2HTTPBoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "runtime"
        self.org = Identity("organization", "org-ui2", "platform")
        self.human = Identity("principal", "owner-ui2", self.org.value)

        p704.initialize_access_store(self.root, self.org)
        p704.register_principal(self.root, self.human, kind="human")
        issued = p704.issue_credential(self.root, self.human)
        self.credential_id = issued["credential_id"]
        self.credential_file = Path(issued["secret_path"])
        self.read_grant = p704.grant_access(
            self.root,
            self.human,
            operation=ui1.WORKSPACE_OPERATION,
            resource=ui1.WORKSPACE_RESOURCE,
            access_paths=("local",),
        )
        self.interact_grant = p704.grant_access(
            self.root,
            self.human,
            operation=ui2.INTERACTION_OPERATION,
            resource=ui2.INTERACTION_RESOURCE,
            access_paths=("local",),
        )

        org_scope = OrganizationScope(self.org)
        actor = ActorContext(Principal(self.human), org_scope)
        target = build_p1_02_native_record(organization=org_scope, actor=actor)
        workflow = build_p1_03_workflow(
            organization=org_scope, actor=actor, target_record=target
        )
        created = start_governed_execution(
            organization=org_scope,
            actor=actor,
            workflow=workflow,
            operation_name="update-reference-subject",
            material_inputs=(target,),
            required_gates=CORE_PREFLIGHT_GATES,
            execution_id=Identity("execution-subject", "http-ui2", self.org.value),
            version_id=Identity("execution-version", "http-ui2-v1", self.org.value),
            created_at=datetime(2026, 8, 18, 13, 0, 0, tzinfo=UTC),
        )
        awaiting = await_required_gates(
            created,
            version_id=Identity("execution-version", "http-ui2-v2", self.org.value),
            actor=actor,
            created_at=datetime(2026, 8, 18, 13, 0, 1, tzinfo=UTC),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=actor,
                basis_ref=Identity("gate-basis", f"http-{kind.value}", self.org.value),
                decision_id=Identity("gate-decision-subject", f"http-{kind.value}", self.org.value),
                version_id=Identity("gate-decision-version", f"http-{kind.value}-v1", self.org.value),
                created_at=datetime(2026, 8, 18, 13, 0, 2 + index, tzinfo=UTC),
            )
            for index, kind in enumerate(CORE_PREFLIGHT_GATES)
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=Identity("execution-version", "http-ui2-v3", self.org.value),
            actor=actor,
            created_at=datetime(2026, 8, 18, 13, 0, 10, tzinfo=UTC),
        )
        running = transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=Identity("execution-version", "http-ui2-v4", self.org.value),
            actor=actor,
            created_at=datetime(2026, 8, 18, 13, 0, 11, tzinfo=UTC),
        )
        candidate = CanonicalRecord(
            subject_id=target.subject_id,
            version_id=Identity("canonical-version", "http-ui2-target-v2", self.org.value),
            semantic_type=target.semantic_type,
            schema_version=target.schema_version,
            organization=org_scope,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=target.authority_scope,
            accountable_owner_id=target.accountable_owner_id,
            creation_actor=actor,
            created_at=datetime(2026, 8, 18, 13, 0, 12, tzinfo=UTC),
            provenance_refs=(
                actor.actual_principal.principal_id,
                running.execution_subject_id,
                running.execution_version_id,
                target.version_id,
            ),
            integrity_metadata=(("representation", "p7.06-ui2-http-test"),),
            payload=(("label", "http successor"),),
            lifecycle_status="established",
            predecessor_version_id=target.version_id,
        )
        producer = Identity("principal", "http-ui2-producer", self.org.value)
        event = EventReceipt(
            event_id=Identity("event-subject", "http-ui2-event", self.org.value),
            version_id=Identity("event-version", "http-ui2-event-v1", self.org.value),
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            organization=org_scope,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS governed runtime",
            occurred_at=datetime(2026, 8, 18, 13, 0, 13, tzinfo=UTC),
            recorded_at=datetime(2026, 8, 18, 13, 0, 14, tzinfo=UTC),
            producer_id=producer,
            initiating_actor_id=actor.actual_principal.principal_id,
            execution_subject_id=running.execution_subject_id,
            execution_version_id=running.execution_version_id,
            related_subject_ids=(candidate.subject_id,),
            related_version_ids=(candidate.version_id,),
            correlation_refs=(running.execution_subject_id,),
            causation_refs=(running.execution_version_id,),
            classification="internal",
            access_scope="governed-action",
            provenance_refs=(
                producer,
                actor.actual_principal.principal_id,
                running.execution_subject_id,
                running.execution_version_id,
                candidate.subject_id,
                candidate.version_id,
            ),
            integrity_metadata=(("representation", "p7.06-ui2-http-test"),),
            payload=(("outcome", "succeeded"),),
        )
        authorization = CurrentSourceAuthorization(
            organization=org_scope,
            actor_actual_principal_id=actor.actual_principal.principal_id,
            represented_principal_id=None,
            resource_subject_id=running.execution_subject_id,
            decision_version_id=Identity(
                "source-authorization-version", "http-ui2-inspection-v1", self.org.value
            ),
            allowed=True,
        )
        self.case = GovernedInteractionCase(
            interaction_id="http-action",
            organization=org_scope,
            actor=actor,
            source_record=target,
            execution_lineage=GovernedExecutionLineage((created, awaiting, ready, running)),
            runtime_state=RuntimeConsistencyState(canonical_records=(target,)),
            candidate=candidate,
            event_receipt=event,
            source_authorizations=(authorization,),
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="http-ui2-token",
        )
        self.current_case = self.case

        item_id = p703.persist_governed_item(
            self.root,
            RELEASE,
            b'{"http":"ui2"}',
            {
                "state_class": "canonical-governed-state",
                "organization_scope": p703.ORGANIZATION_SCOPE,
                "semantic_type": target.semantic_type,
                "schema_version": target.schema_version,
                "classification": "internal",
                "retention_policy_ref": "retention:ui2-test",
                "source_release_sha": RELEASE,
                "subject_identity": target.subject_id.value,
                "version_identity": target.version_id.value,
                "authority_mode": target.authority_mode.value,
                "authority_scope": target.authority_scope,
                "governed_admission_ref": "event:http-ui2-admission",
                "provenance_refs": ["event:http-ui2-admission"],
                "canonical_authority": True,
                "contains_reusable_secret": False,
            },
        )
        p703.create_checkpoint(
            self.root,
            RELEASE,
            execution_subject_identity=running.execution_subject_id.value,
            execution_version_identity=running.execution_version_id.value,
            governed_storage_item_ids=(item_id,),
            classification="internal",
            retention_policy_ref="retention:ui2-test",
            reason="UI2 test checkpoint",
        )
        health_path = self.root / "run" / "health.json"
        health_path.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.now(UTC).isoformat().replace("+00:00", "Z")
        health_path.write_text(
            json.dumps(
                {
                    "schema": "arvectum.p7_02.runtime-health/1",
                    "classification": "non-canonical operational telemetry",
                    "operating_mode": "Persistent Internal / owner-operated",
                    "organization_scope": p703.ORGANIZATION_SCOPE,
                    "operating_role": "Arvectum OS Owner-Operator",
                    "network_listener_mode": "none",
                    "product_effects_enabled": False,
                    "canonical_state_written": False,
                    "release_sha": RELEASE,
                    "instance_id": "ui2-test-runtime",
                    "previous_instance_id": None,
                    "generation": 1,
                    "pid": os.getpid(),
                    "started_at": now,
                    "heartbeat_at": now,
                    "state": "healthy",
                    "semantic_imports_ok": True,
                    "semantic_modules": [],
                    "python_version": "test",
                    "platform_system": "test",
                }
            ),
            encoding="utf-8",
        )
        if os.name != "nt":
            health_path.chmod(0o600)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _provider(self, interaction_id: str):
        if interaction_id != self.current_case.interaction_id:
            return None
        return self.current_case

    def _start(self):
        patcher = patch.object(ui1, "_verify_exact_release", return_value=RELEASE)
        patcher.start()
        self.addCleanup(patcher.stop)
        server = ui2.make_server(
            host="127.0.0.1",
            port=0,
            root=self.root,
            organization=self.org,
            principal=self.human,
            credential_id=self.credential_id,
            credential_file=self.credential_file,
            interaction_provider=self._provider,
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(lambda: thread.join(timeout=5))
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server

    @staticmethod
    def _csrf(body: str) -> str:
        match = re.search(r'name="csrf" value="([^"]+)"', body)
        if match is None:
            raise AssertionError("CSRF token not rendered")
        return match.group(1)

    def _get_interaction(self, server):
        host, port = server.server_address[:2]
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", f"/interaction?id={self.case.interaction_id}")
        response = conn.getresponse()
        body = response.read().decode()
        return conn, response, body

    def _post(self, conn, server, *, csrf: str, extra: str = "", origin: str | None = None):
        host, port = server.server_address[:2]
        body = (
            f"interaction_id={self.case.interaction_id}&csrf={csrf}"
            + extra
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": origin or f"http://{host}:{port}",
        }
        conn.request("POST", "/interaction/execute", body=body, headers=headers)
        response = conn.getresponse()
        return response, response.read().decode()

    def test_http_get_and_post_keep_ui_state_out_of_security_boundary(self) -> None:
        server = self._start()
        conn, response, body = self._get_interaction(server)
        self.assertEqual(response.status, 200)
        self.assertIn("Governed interaction preflight", body)
        self.assertIn("Request governed action", body)
        self.assertIn("form-action 'self'", response.getheader("Content-Security-Policy"))
        csrf = self._csrf(body)

        # Provider evidence changes after the button was rendered. POST must
        # re-fetch/re-preflight rather than trust the prior UI state.
        self.current_case = replace(self.case, source_authorizations=())
        response, body = self._post(conn, server, csrf=csrf)
        self.assertEqual(response.status, 200)
        self.assertIn("Blocked", body)
        self.assertNotIn("Committed exact Version", body)
        conn.close()

    def test_successful_http_post_enters_existing_governed_runtime_and_renders_exact_result(self) -> None:
        server = self._start()
        conn, response, body = self._get_interaction(server)
        self.assertEqual(response.status, 200)
        csrf = self._csrf(body)
        response, body = self._post(conn, server, csrf=csrf)
        self.assertEqual(response.status, 200)
        self.assertIn("Succeeded", body)
        self.assertIn(self.case.candidate.version_id.value, body)
        self.assertIn(self.case.event_receipt.version_id.value, body)
        self.assertIn("optimistic success", body)
        conn.close()

    def test_csrf_origin_extra_fields_and_revoked_interaction_grant_fail_closed(self) -> None:
        server = self._start()

        conn, response, body = self._get_interaction(server)
        self.assertEqual(response.status, 200)
        csrf = self._csrf(body)
        response, blocked = self._post(conn, server, csrf="wrong")
        self.assertEqual(response.status, 403)
        self.assertNotIn(self.case.candidate.version_id.value, blocked)
        conn.close()

        conn, response, body = self._get_interaction(server)
        csrf = self._csrf(body)
        response, blocked = self._post(
            conn,
            server,
            csrf=csrf,
            origin="http://evil.invalid",
        )
        self.assertEqual(response.status, 403)
        conn.close()

        conn, response, body = self._get_interaction(server)
        csrf = self._csrf(body)
        response, blocked = self._post(conn, server, csrf=csrf, extra="&candidate=forged")
        self.assertEqual(response.status, 403)
        conn.close()

        conn, response, body = self._get_interaction(server)
        csrf = self._csrf(body)
        p704.revoke_grant(self.root, self.interact_grant)
        response, blocked = self._post(conn, server, csrf=csrf)
        self.assertEqual(response.status, 403)
        self.assertNotIn(self.case.source_record.subject_id.value, blocked)
        self.assertNotIn(self.case.source_record.version_id.value, blocked)
        conn.close()

    def test_non_post_mutation_methods_and_ui2_source_do_not_create_direct_write_shortcut(self) -> None:
        server = self._start()
        host, port = server.server_address[:2]
        conn = http.client.HTTPConnection(host, port, timeout=5)
        for method in ("PUT", "PATCH", "DELETE"):
            with self.subTest(method=method):
                conn.request(method, "/interaction/execute", body="x")
                response = conn.getresponse()
                response.read()
                self.assertEqual(response.status, 405)
        conn.close()

        source = Path(ui2.__file__).read_text(encoding="utf-8")
        for token in (
            "persist_governed_item(",
            "create_checkpoint(",
            "commit_canonical_mutation(",
            "prepare_canonical_mutation_action(",
            "execute_canonical_mutation_action(",
            "build_governed_gate_decision(",
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
