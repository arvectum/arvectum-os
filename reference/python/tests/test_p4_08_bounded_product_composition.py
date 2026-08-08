from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import unittest
from unittest.mock import patch

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_experience import (
    DocumentWorkspaceBlockCode,
    DocumentWorkspaceBlockedState,
    DocumentWorkspaceSourceSet,
)
from arvectum_os_ref.governed_execution import GovernedGateKind
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
    PRODUCT_CONTRACT_AUTHORITY_SCOPE,
    PRODUCT_CONTRACT_SEMANTIC_TYPE,
    PlatformDependencyDeclaration,
    ProductContract,
    ProductContractLifecycle,
    ProductContractScopeError,
    ProductOperationDeclaration,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import OperationSideEffectClass
from arvectum_os_ref.workspace_shell import PresentationAuthority, WorkspaceShellState
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


class P408BoundedProductCompositionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = Identity("product", "bounded-review-product", "org-a")
        self.task = BoundedProductTask(
            organization=self.org,
            product_id=self.product_id,
            product_version="0.1.0",
            task_id=Identity("product-task", "task-1", "org-a"),
            document_subject_id=Identity("document", "doc-1", "org-a"),
            title="Review governed task context",
        )
        self.contract = self._contract()
        self.access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.document_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version="0.1.0",
            dependency_id=CAP_001_DOCUMENT_ARTIFACT,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RESOLVE_DOCUMENT,
            access=self.access,
        )
        self.knowledge_request = CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version="0.1.0",
            dependency_id=CAP_002_MEMORY_KNOWLEDGE,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=OP_RETRIEVE_KNOWLEDGE,
            access=self.access,
        )

    def _contract(self) -> ProductContract:
        now = datetime(2026, 8, 8, 19, 30, tzinfo=timezone.utc)
        record = CanonicalRecord(
            subject_id=Identity("product-contract", "pc-bounded-review", "org-a"),
            version_id=Identity(
                "product-contract-version", "pc-bounded-review-v1", "org-a"
            ),
            semantic_type=PRODUCT_CONTRACT_SEMANTIC_TYPE,
            schema_version="0.1.0",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=PRODUCT_CONTRACT_AUTHORITY_SCOPE,
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=now,
            provenance_refs=(self.product_id, self.principal.principal_id),
            integrity_metadata=(("representation", "bounded-p4.08-reference"),),
            lifecycle_status=ProductContractLifecycle.PROVISIONAL.value,
        )
        dependencies = (
            PlatformDependencyDeclaration(
                dependency_id=CAP_001_DOCUMENT_ARTIFACT,
                contract_version=CAPABILITY_CONTRACT_VERSION,
                allowed_operations=(OP_RESOLVE_DOCUMENT,),
                provider_responsibility=(
                    "Preserve RFC-0008 governed Document/Artifact semantics."
                ),
                consumer_responsibility=(
                    "Use only current scoped workspace access."
                ),
                failure_behavior=(
                    "Fail closed without product-side fallback to platform internals."
                ),
                provisional=True,
            ),
            PlatformDependencyDeclaration(
                dependency_id=CAP_002_MEMORY_KNOWLEDGE,
                contract_version=CAPABILITY_CONTRACT_VERSION,
                allowed_operations=(OP_RETRIEVE_KNOWLEDGE,),
                provider_responsibility=(
                    "Preserve RFC-0007 Memory/Knowledge semantics."
                ),
                consumer_responsibility=(
                    "Treat retrieval as context, never authority."
                ),
                failure_behavior=(
                    "Fail closed or continue without protected Knowledge context."
                ),
                provisional=True,
            ),
        )
        operations = tuple(
            ProductOperationDeclaration(
                operation_name=name,
                dependency_id=dependency,
                side_effect_classes=(OperationSideEffectClass.READ_ONLY,),
                required_gates=(
                    GovernedGateKind.AUTHORIZATION,
                    GovernedGateKind.DATA_GOVERNANCE,
                ),
                canonical_accesses=(),
                failure_behavior="No hidden fallback or authority widening.",
            )
            for dependency, name in (
                (CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT),
                (CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE),
            )
        )
        return ProductContract(
            record=record,
            product_id=self.product_id,
            product_version="0.1.0",
            bounded_scope="P4.08 bounded product task/context composition.",
            compatibility_assumptions=(
                "CAP-001 and CAP-002 remain Incubating/Provisional reference dependencies.",
                "No public API or Stable Product Contract compatibility is implied.",
            ),
            dependencies=dependencies,
            operations=operations,
            portability_responsibility=(
                "Preserve governed identities/references; product task state remains product-owned."
            ),
            retention_deletion_responsibility=(
                "Apply source handling rules; do not duplicate protected content."
            ),
            review_condition="Review at R11 or on material boundary change.",
            exit_path=(
                "Revise, contain, replace or retire; stabilize only by separate RFC-0004 governance."
            ),
        )

    def _entry(self):
        return enter_product_task_workspace(
            contract=self.contract,
            task=self.task,
            actor=self.actor,
            capability_requests=(self.document_request, self.knowledge_request),
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
            product_version="0.1.0",
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

    def test_consequential_action_wrappers_delegate_only_to_r10_operator_safety(self) -> None:
        entry = self._entry()
        prepared = object()
        result = object()

        with patch(
            "bounded_product_ref.task_composition.prepare_operator_canonical_mutation_action",
            return_value=prepared,
        ) as prepare_guard:
            actual_prepared = prepare_product_task_action(
                entry=entry,
                inspection=object(),
                execution=object(),
                runtime_state=object(),
                candidate=object(),
                event_receipt=object(),
                retry_semantics=object(),
                source_authorizations=(),
                retry_token="retry-1",
            )
        self.assertIs(actual_prepared, prepared)
        self.assertEqual(
            prepare_guard.call_args.kwargs["workspace"], entry.workspace
        )
        self.assertEqual(
            prepare_guard.call_args.kwargs["source_authorizations"], ()
        )

        with patch(
            "bounded_product_ref.task_composition.execute_operator_canonical_mutation_action",
            return_value=result,
        ) as execute_guard:
            actual_result = execute_product_task_action(
                entry=entry,
                intent=object(),
                runtime_state=object(),
                source_authorizations=(),
            )
        self.assertIs(actual_result, result)
        self.assertEqual(
            execute_guard.call_args.kwargs["workspace"], entry.workspace
        )

    def test_platform_does_not_import_product_and_product_does_not_bypass_r10(self) -> None:
        reference_root = Path(__file__).parents[1]
        platform_root = reference_root / "arvectum_os_ref"
        platform_source = "\n".join(
            path.read_text(encoding="utf-8") for path in platform_root.glob("*.py")
        )
        product_source = (
            reference_root / "bounded_product_ref" / "task_composition.py"
        ).read_text(encoding="utf-8")

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
