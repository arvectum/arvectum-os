from __future__ import annotations

import ast
import unittest
from datetime import datetime, timezone
from pathlib import Path

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord, build_p1_02_native_record
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.event_provenance import EventReceipt
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.execution_action_experience import (
    ActionCommitStatus,
    GovernedExecutionInspection,
    inspect_governed_execution,
)
from arvectum_os_ref.governed_execution import (
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
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.operator_safety import (
    OperatorCanonicalMutationIntent,
    execute_operator_canonical_mutation_action,
    prepare_operator_canonical_mutation_action,
)
from arvectum_os_ref.runtime_consistency import RetrySemantics, RuntimeConsistencyState
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import build_p1_03_workflow
from arvectum_os_ref.workspace_shell import (
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


UTC = timezone.utc
TEST_ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = TEST_ROOT.parent / "arvectum_os_ref"


class R10OperatorSafetyCrossCapabilityHealthTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-r10", "platform"))
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-r10", "platform")),
            self.organization,
        )
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
            subject_id=self._id("product-contract-subject", "contract-r10"),
            version_id=self._id("product-contract-version", "contract-r10-v1"),
            semantic_type="platform.product-contract",
            authority_scope="platform.product-contract/boundary",
            lifecycle_status="Provisional",
        )
        self.required_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        created = start_governed_execution(
            organization=self.organization,
            actor=self.actor,
            workflow=self.workflow,
            operation_name="r10-safe-update",
            material_inputs=(self.target,),
            required_gates=self.required_gates,
            execution_id=self._id("execution-subject", "execution-r10"),
            version_id=self._id("execution-version", "execution-r10-v1"),
            created_at=datetime(2026, 8, 8, 18, 0, tzinfo=UTC),
            product_contract=self.contract_pin,
        )
        awaiting = await_required_gates(
            created,
            version_id=self._id("execution-version", "execution-r10-v2"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 18, 1, tzinfo=UTC),
        )
        decisions = tuple(
            build_governed_gate_decision(
                execution=awaiting,
                kind=kind,
                outcome=GovernedGateOutcome.ALLOW,
                decision_actor=self.actor,
                basis_ref=self._id("gate-basis", f"r10-{index}"),
                decision_id=self._id("gate-decision-subject", f"r10-{index}"),
                version_id=self._id("gate-decision-version", f"r10-{index}-v1"),
                created_at=datetime(2026, 8, 8, 18, 1, 30, tzinfo=UTC),
            )
            for index, kind in enumerate(self.required_gates, start=1)
        )
        ready = admit_ready_execution(
            awaiting,
            decisions=decisions,
            version_id=self._id("execution-version", "execution-r10-v3"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 18, 2, tzinfo=UTC),
        )
        self.running = transition_governed_execution(
            ready,
            lifecycle=GovernedExecutionLifecycle.RUNNING,
            version_id=self._id("execution-version", "execution-r10-v4"),
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 18, 3, tzinfo=UTC),
        )
        self.lineage = GovernedExecutionLineage((created, awaiting, ready, self.running))
        self.runtime_state = RuntimeConsistencyState(canonical_records=(self.target,))
        self.candidate = CanonicalRecord(
            subject_id=self.target.subject_id,
            version_id=self._id("canonical-version", "r10-target-v2"),
            semantic_type=self.target.semantic_type,
            schema_version=self.target.schema_version,
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=self.target.authority_scope,
            accountable_owner_id=self.target.accountable_owner_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 18, 4, tzinfo=UTC),
            provenance_refs=(
                self.actor.actual_principal.principal_id,
                self.running.execution_subject_id,
                self.running.execution_version_id,
                self.target.version_id,
            ),
            integrity_metadata=(("representation", "r10-test"),),
            payload=(("label", "r10-target-v2"),),
            lifecycle_status="established",
            predecessor_version_id=self.target.version_id,
        )
        producer = Identity("principal", "runtime-producer", "platform")
        self.event_receipt = EventReceipt(
            event_id=self._id("event-subject", "r10-mutation"),
            version_id=self._id("event-version", "r10-mutation-v1"),
            event_type="platform.canonical-mutation.succeeded",
            event_schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.event/governed-outcome",
            authoritative_source="Arvectum OS governed runtime",
            occurred_at=datetime(2026, 8, 8, 18, 4, tzinfo=UTC),
            recorded_at=datetime(2026, 8, 8, 18, 4, 1, tzinfo=UTC),
            producer_id=producer,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            execution_subject_id=self.running.execution_subject_id,
            execution_version_id=self.running.execution_version_id,
            related_subject_ids=(self.candidate.subject_id,),
            related_version_ids=(self.candidate.version_id,),
            correlation_refs=(self.running.execution_subject_id,),
            causation_refs=(self.running.execution_version_id,),
            classification="internal",
            access_scope="governed-action",
            provenance_refs=(
                producer,
                self.actor.actual_principal.principal_id,
                self.running.execution_subject_id,
                self.running.execution_version_id,
                self.candidate.subject_id,
                self.candidate.version_id,
            ),
            integrity_metadata=(("representation", "r10-test"),),
            payload=(("outcome", "succeeded"),),
        )

    def _id(self, namespace: str, value: str) -> Identity:
        return Identity(namespace, value, "org-r10")

    def _workspace(self) -> WorkspaceShellState:
        opened = open_workspace_shell(self.actor)
        self.assertIsInstance(opened, WorkspaceShellState)
        return navigate_workspace(
            opened,
            destination=WorkspaceDestination.EXECUTIONS,
            reference=SubjectNavigationReference(
                self.organization,
                self.running.execution_subject_id,
            ),
        )

    def _authorization(self, *, suffix: str = "1", allowed: bool = True) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            represented_principal_id=None,
            resource_subject_id=self.running.execution_subject_id,
            decision_version_id=self._id(
                "source-authorization-version",
                f"r10-source-{suffix}",
            ),
            allowed=allowed,
        )

    def _inspection(
        self,
        workspace: WorkspaceShellState,
        authorization: CurrentSourceAuthorization,
    ) -> GovernedExecutionInspection:
        result = inspect_governed_execution(
            workspace,
            lineages=(self.lineage,),
            authorizations=(authorization,),
            runtime_state=self.runtime_state,
        )
        self.assertIsInstance(result, GovernedExecutionInspection)
        return result

    def _prepare(
        self,
        workspace: WorkspaceShellState,
        authorization: CurrentSourceAuthorization,
    ) -> OperatorCanonicalMutationIntent:
        inspection = self._inspection(workspace, authorization)
        return prepare_operator_canonical_mutation_action(
            workspace=workspace,
            inspection=inspection,
            execution=self.running,
            runtime_state=self.runtime_state,
            candidate=self.candidate,
            event_receipt=self.event_receipt,
            retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
            retry_token="r10-action",
            source_authorizations=(authorization,),
        )

    def test_operator_action_binds_exact_current_source_access_decision(self) -> None:
        workspace = self._workspace()
        authorization = self._authorization()
        intent = self._prepare(workspace, authorization)

        self.assertEqual(
            intent.source_authorization_decision_version_id,
            authorization.decision_version_id,
        )
        self.assertIs(
            intent.presentation_authority,
            PresentationAuthority.NON_AUTHORITATIVE,
        )

        result = execute_operator_canonical_mutation_action(
            workspace=workspace,
            intent=intent,
            runtime_state=self.runtime_state,
            source_authorizations=(authorization,),
        )
        self.assertEqual(result.status, ActionCommitStatus.COMMITTED)
        self.assertEqual(result.state.head.version_id, self.candidate.version_id)

    def test_replaced_allow_decision_requires_reinspection_before_prepare(self) -> None:
        workspace = self._workspace()
        inspected_authorization = self._authorization(suffix="old")
        inspection = self._inspection(workspace, inspected_authorization)
        replacement = self._authorization(suffix="new")

        with self.assertRaises(PermissionError):
            prepare_operator_canonical_mutation_action(
                workspace=workspace,
                inspection=inspection,
                execution=self.running,
                runtime_state=self.runtime_state,
                candidate=self.candidate,
                event_receipt=self.event_receipt,
                retry_semantics=RetrySemantics.KEYED_IDEMPOTENT,
                retry_token="r10-replaced",
                source_authorizations=(replacement,),
            )

    def test_revoked_missing_ambiguous_or_replaced_access_blocks_prepared_action(self) -> None:
        workspace = self._workspace()
        authorization = self._authorization()
        intent = self._prepare(workspace, authorization)
        cases = (
            (),
            (self._authorization(suffix="denied", allowed=False),),
            (authorization, self._authorization(suffix="duplicate")),
            (self._authorization(suffix="replacement"),),
        )
        for current in cases:
            with self.subTest(current=current):
                result = execute_operator_canonical_mutation_action(
                    workspace=workspace,
                    intent=intent,
                    runtime_state=self.runtime_state,
                    source_authorizations=current,
                )
                self.assertEqual(result.status, ActionCommitStatus.NOT_ADMITTED)
                self.assertIs(result.state, self.runtime_state)
                self.assertEqual(len(result.state.canonical_records), 1)
                self.assertEqual(len(result.state.admitted_events), 0)
                self.assertIn("Re-inspect", result.status_text)

    def test_r10_guard_delegates_to_existing_p405_adapter_without_new_mutation_path(self) -> None:
        source = (PACKAGE_ROOT / "operator_safety.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        called_names = {
            node.func.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
        }
        self.assertIn("prepare_canonical_mutation_action", called_names)
        self.assertIn("execute_canonical_mutation_action", called_names)
        self.assertNotIn("commit_canonical_mutation", called_names)
        self.assertNotIn("execute_p1_06_canonical_mutation", called_names)

        import_roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                import_roots.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                import_roots.add(node.module.split(".", 1)[0])
        self.assertTrue(
            {
                "fastapi",
                "flask",
                "django",
                "starlette",
                "sqlalchemy",
                "psycopg",
                "requests",
                "httpx",
                "aiohttp",
                "redis",
                "kafka",
            }.isdisjoint(import_roots)
        )

    def test_accumulated_p4_surfaces_remain_non_authoritative_and_internal(self) -> None:
        modules = (
            "canonical_inspection.py",
            "provenance_inspection.py",
            "execution_action_experience.py",
            "document_artifact_experience.py",
            "memory_knowledge_search_experience.py",
            "operator_safety.py",
        )
        root_init = (PACKAGE_ROOT / "__init__.py").read_text(encoding="utf-8")
        for name in modules:
            with self.subTest(module=name):
                source = (PACKAGE_ROOT / name).read_text(encoding="utf-8")
                self.assertIn("PresentationAuthority.NON_AUTHORITATIVE", source)
        self.assertNotIn("from .operator_safety import", root_init)

    def test_document_and_knowledge_exact_reliance_keep_current_rechecks(self) -> None:
        document = ast.parse(
            (PACKAGE_ROOT / "document_artifact_experience.py").read_text(encoding="utf-8")
        )
        knowledge = ast.parse(
            (PACKAGE_ROOT / "memory_knowledge_search_experience.py").read_text(encoding="utf-8")
        )

        def keyword_names(tree: ast.Module, function_name: str) -> set[str]:
            for node in tree.body:
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    return {arg.arg for arg in node.args.kwonlyargs}
            self.fail(f"missing function {function_name}")

        self.assertTrue(
            {"source_authorizations", "access_request"}.issubset(
                keyword_names(document, "resolve_workspace_exact_reliance")
            )
        )
        for function_name in (
            "resolve_exact_knowledge_from_workspace",
            "resolve_exact_knowledge_from_search",
        ):
            self.assertTrue(
                {"source_authorizations", "access_request", "selected_version_id"}.issubset(
                    keyword_names(knowledge, function_name)
                )
            )


if __name__ == "__main__":
    unittest.main()
