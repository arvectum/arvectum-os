from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import unittest
from unittest.mock import patch

from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_experience import (
    DocumentWorkspaceBlockCode,
    DocumentWorkspaceBlockedState,
    DocumentWorkspaceSourceSet,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_search_experience import (
    KnowledgeWorkspaceView,
    MemoryKnowledgeSearchSources,
)
from arvectum_os_ref.product_capability_consumption import (
    CAP_001_DOCUMENT_ARTIFACT,
    CAP_002_MEMORY_KNOWLEDGE,
    CAPABILITY_CONTRACT_VERSION,
    OP_RESOLVE_DOCUMENT,
    OP_RETRIEVE_KNOWLEDGE,
    CapabilityConsumptionRequest,
)
from arvectum_os_ref.product_contract import (
    CanonicalAccessMode,
    ProductContractLifecycle,
    ProductContractScopeError,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import PresentationAuthority, WorkspaceShellState
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_DEPENDENCY,
    OP_RECORD_TASK_DECISION,
    PRODUCT_TASK_SEMANTIC_TYPE,
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from bounded_product_ref.task_composition import (
    BoundedProductTask,
    ProductCompositionError,
    ProductTaskDisposition,
    compose_product_task_context,
    decide_product_task,
    enter_product_task_workspace,
    execute_product_task_action,
    prepare_product_task_action,
)


UTC = timezone.utc


class P408BoundedProductCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.task = BoundedProductTask(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            task_id=Identity("product-task", "task-1", "org-a"),
            document_subject_id=Identity("document", "doc-1", "org-a"),
            title="Review governed task context",
        )
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=datetime(2026, 8, 8, 19, 30, tzinfo=UTC),
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.document_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=self.access,
        )
        self.knowledge_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_002_MEMORY_KNOWLEDGE,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RETRIEVE_KNOWLEDGE,
            access=self.access,
        )

    def _entry(self):
        return enter_product_task_workspace(
            contract=self.contract,
            task=self.task,
            actor=self.actor,
            capability_requests=(self.document_request, self.knowledge_request),
        )

    def test_executable_contract_is_provisional_and_declares_real_boundaries(self) -> None:
        self.assertEqual(self.contract.lifecycle, ProductContractLifecycle.PROVISIONAL)
        self.assertEqual(self.contract.product_id, self.product_id)
        self.assertEqual(self.contract.product_version, PRODUCT_VERSION)
        self.assertEqual(
            {dependency.dependency_id for dependency in self.contract.dependencies},
            {
                CAP_001_DOCUMENT_ARTIFACT,
                CAP_002_MEMORY_KNOWLEDGE,
                GOVERNED_RUNTIME_DEPENDENCY,
            },
        )

        operations = {item.operation_name: item for item in self.contract.operations}
        document_access = operations[OP_RESOLVE_DOCUMENT].canonical_accesses
        knowledge_access = operations[OP_RETRIEVE_KNOWLEDGE].canonical_accesses
        mutation_access = operations[OP_RECORD_TASK_DECISION].canonical_accesses

        self.assertEqual(document_access[0].semantic_type, "platform.document")
        self.assertEqual(document_access[0].access_modes, (CanonicalAccessMode.READ,))
        self.assertEqual(knowledge_access[0].semantic_type, "platform.knowledge")
        self.assertEqual(knowledge_access[0].access_modes, (CanonicalAccessMode.READ,))
        self.assertEqual(mutation_access[0].semantic_type, PRODUCT_TASK_SEMANTIC_TYPE)
        self.assertEqual(
            set(mutation_access[0].access_modes),
            {CanonicalAccessMode.READ, CanonicalAccessMode.WRITE},
        )

    def test_entry_requires_exact_provisional_contract_and_two_distinct_capabilities(self) -> None:
        entry = self._entry()

        self.assertIsInstance(entry.workspace, WorkspaceShellState)
        self.assertEqual(entry.workspace.organization, self.org)
        self.assertEqual(entry.workspace.actor, self.actor)
        self.assertEqual(entry.workspace.product_context.product_id, self.product_id)
        self.assertEqual(
            entry.workspace.product_context.product_contract_version_id,
            self.contract.record.version_id,
        )
        self.assertEqual(
            {value.dependency_id for value in entry.capability_admissions},
            {CAP_001_DOCUMENT_ARTIFACT, CAP_002_MEMORY_KNOWLEDGE},
        )
        self.assertEqual(
            entry.workspace.presentation_authority,
            PresentationAuthority.NON_AUTHORITATIVE,
        )

        with self.assertRaises(ProductCompositionError):
            enter_product_task_workspace(
                contract=self.contract,
                task=self.task,
                actor=self.actor,
                capability_requests=(self.document_request, self.document_request),
            )

    def test_contract_entry_does_not_grant_source_access(self) -> None:
        entry = self._entry()

        context = compose_product_task_context(
            entry=entry,
            document_request=self.document_request,
            knowledge_request=self.knowledge_request,
            document_sources=DocumentWorkspaceSourceSet((), ()),
            document_source_authorizations=(),
            knowledge_sources=MemoryKnowledgeSearchSources(),
            knowledge_source_authorizations=(),
        )

        self.assertIsInstance(context.document, DocumentWorkspaceBlockedState)
        self.assertEqual(context.document.code, DocumentWorkspaceBlockCode.ACCESS_DENIED)
        self.assertIsInstance(context.knowledge, KnowledgeWorkspaceView)
        self.assertEqual(context.knowledge.items, ())
        self.assertEqual(
            context.product_contract_version_id, self.contract.record.version_id
        )
        self.assertEqual(
            set(context.capability_dependencies),
            {CAP_001_DOCUMENT_ARTIFACT, CAP_002_MEMORY_KNOWLEDGE},
        )
        self.assertEqual(
            context.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE
        )

    def test_request_actor_or_product_scope_cannot_drift_after_entry(self) -> None:
        entry = self._entry()
        other_actor = ActorContext(
            Principal(Identity("principal", "operator-2", "platform")),
            self.org,
        )
        drifted = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=CAP_002_MEMORY_KNOWLEDGE,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RETRIEVE_KNOWLEDGE,
            access=AccessRequest(
                actor=other_actor,
                purpose=self.access.purpose,
                required_right=self.access.required_right,
                allowed_classifications=self.access.allowed_classifications,
            ),
        )

        with self.assertRaises(ProductContractScopeError):
            compose_product_task_context(
                entry=entry,
                document_request=self.document_request,
                knowledge_request=drifted,
                document_sources=DocumentWorkspaceSourceSet((), ()),
                document_source_authorizations=(),
                knowledge_sources=MemoryKnowledgeSearchSources(),
                knowledge_source_authorizations=(),
            )

    def test_product_domain_decision_remains_transient_product_owned_state(self) -> None:
        context = compose_product_task_context(
            entry=self._entry(),
            document_request=self.document_request,
            knowledge_request=self.knowledge_request,
            document_sources=DocumentWorkspaceSourceSet((), ()),
            document_source_authorizations=(),
            knowledge_sources=MemoryKnowledgeSearchSources(),
            knowledge_source_authorizations=(),
        )

        decision = decide_product_task(
            context=context,
            disposition=ProductTaskDisposition.NEEDS_REVIEW,
            note="Missing authorized document context.",
        )

        self.assertEqual(decision.task_id, self.task.task_id)
        self.assertEqual(
            decision.disposition, ProductTaskDisposition.NEEDS_REVIEW
        )
        self.assertEqual(
            decision.based_on_contract_version_id, self.contract.record.version_id
        )
        for forbidden in (
            "canonical_record",
            "authorized",
            "approved",
            "organizational_authority",
        ):
            with self.subTest(attribute=forbidden):
                self.assertFalse(hasattr(decision, forbidden))

    def test_consequential_action_wrappers_preserve_contract_guard_then_delegate_to_r10(self) -> None:
        entry = self._entry()
        prepared = object()
        result = object()
        execution = object()
        intent = object()

        with patch(
            "bounded_product_ref.task_composition._require_execution_contract"
        ) as contract_guard, patch(
            "bounded_product_ref.task_composition.prepare_operator_canonical_mutation_action",
            return_value=prepared,
        ) as prepare_guard:
            actual_prepared = prepare_product_task_action(
                entry=entry,
                inspection=object(),
                execution=execution,
                runtime_state=object(),
                candidate=object(),
                event_receipt=object(),
                retry_semantics=object(),
                source_authorizations=(),
                retry_token="retry-1",
            )
        self.assertIs(actual_prepared, prepared)
        contract_guard.assert_called_once_with(entry=entry, execution=execution)
        self.assertEqual(
            prepare_guard.call_args.kwargs["workspace"], entry.workspace
        )
        self.assertEqual(
            prepare_guard.call_args.kwargs["source_authorizations"], ()
        )

        with patch(
            "bounded_product_ref.task_composition._require_action_intent_contract"
        ) as intent_contract_guard, patch(
            "bounded_product_ref.task_composition.execute_operator_canonical_mutation_action",
            return_value=result,
        ) as execute_guard:
            actual_result = execute_product_task_action(
                entry=entry,
                intent=intent,
                runtime_state=object(),
                source_authorizations=(),
            )
        self.assertIs(actual_result, result)
        intent_contract_guard.assert_called_once_with(entry=entry, intent=intent)
        self.assertEqual(
            execute_guard.call_args.kwargs["workspace"], entry.workspace
        )

    def test_platform_does_not_import_product_and_product_does_not_bypass_r10(self) -> None:
        reference_root = Path(__file__).parents[1]
        platform_root = reference_root / "arvectum_os_ref"
        platform_source = "\n".join(
            path.read_text(encoding="utf-8") for path in platform_root.glob("*.py")
        )
        product_root = reference_root / "bounded_product_ref"
        product_source = "\n".join(
            path.read_text(encoding="utf-8") for path in product_root.glob("*.py")
        )

        self.assertNotIn("bounded_product_ref", platform_source)
        self.assertNotIn("prepare_canonical_mutation_action", product_source)
        self.assertNotIn("execute_canonical_mutation_action", product_source)
        self.assertNotIn("execution_action_experience", product_source)
        self.assertIn(
            "prepare_operator_canonical_mutation_action", product_source
        )
        self.assertIn(
            "execute_operator_canonical_mutation_action", product_source
        )


if __name__ == "__main__":
    unittest.main()
