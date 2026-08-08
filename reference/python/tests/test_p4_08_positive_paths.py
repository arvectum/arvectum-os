from __future__ import annotations

from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.document_artifact_experience import (
    DocumentWorkspaceInspection,
    DocumentWorkspaceSourceSet,
)
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.governed_execution import GovernedGateKind
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KnowledgeConstraints,
    LearningRole,
    ValidatedKnowledge,
)
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
from arvectum_os_ref.product_contract import ProductRuntimeInteraction
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workflow import (
    OperationSideEffectClass,
    WorkflowDefinition,
    WorkflowLifecycle,
    WorkflowOperation,
)
from bounded_product_ref.contract import (
    GOVERNED_RUNTIME_CONTRACT_VERSION,
    GOVERNED_RUNTIME_DEPENDENCY,
    OP_RECORD_TASK_DECISION,
    PRODUCT_TASK_AUTHORITY_SCOPE,
    PRODUCT_TASK_SEMANTIC_TYPE,
    PRODUCT_VERSION,
    build_p4_08_product_contract,
    product_id_for,
)
from bounded_product_ref.task_composition import (
    BoundedProductTask,
    compose_product_task_context,
    enter_product_task_workspace,
    start_product_task_execution,
)


UTC = timezone.utc


class P408PositivePathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.product_id = product_id_for(self.actor)
        self.document_subject_id = Identity("subject", "doc-1", "org-a")
        self.task = BoundedProductTask(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            task_id=Identity("product-task", "task-1", "org-a"),
            document_subject_id=self.document_subject_id,
            title="Review governed task context",
        )
        self.contract = build_p4_08_product_contract(
            actor=self.actor,
            created_at=self._time(0),
        )
        self.access = AccessRequest(
            actor=self.actor,
            purpose="bounded-product-review",
            required_right="read",
            allowed_classifications=("internal",),
        )
        self.document_request = self._capability_request(
            CAP_001_DOCUMENT_ARTIFACT, OP_RESOLVE_DOCUMENT
        )
        self.knowledge_request = self._capability_request(
            CAP_002_MEMORY_KNOWLEDGE, OP_RETRIEVE_KNOWLEDGE
        )
        self.entry = enter_product_task_workspace(
            contract=self.contract,
            task=self.task,
            actor=self.actor,
            capability_requests=(self.document_request, self.knowledge_request),
        )

    def _time(self, minute: int) -> datetime:
        return datetime(2026, 8, 8, 20, minute, tzinfo=UTC)

    def _capability_request(
        self, dependency_id: Identity, operation_name: str
    ) -> CapabilityConsumptionRequest:
        return CapabilityConsumptionRequest(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=dependency_id,
            dependency_contract_version=CAPABILITY_CONTRACT_VERSION,
            operation_name=operation_name,
            access=self.access,
        )

    def _record(
        self,
        *,
        subject_id: Identity,
        version_id: Identity,
        semantic_type: str,
        authority_scope: str | None = None,
        payload: tuple[tuple[str, str], ...] = (),
        lifecycle_status: str = "Retained",
        provenance_refs: tuple[Identity, ...] | None = None,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=subject_id,
            version_id=version_id,
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=authority_scope or f"{semantic_type}/state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=self._time(1),
            provenance_refs=(self.principal.principal_id,)
            if provenance_refs is None
            else provenance_refs,
            integrity_metadata=(("representation", "p4.08-positive-path"),),
            payload=payload,
            lifecycle_status=lifecycle_status,
        )

    def _authorization(
        self, subject_id: Identity, token: str
    ) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=self.org,
            actor_actual_principal_id=self.principal.principal_id,
            resource_subject_id=subject_id,
            decision_version_id=Identity("authorization-version", token, "org-a"),
            allowed=True,
        )

    def test_authorized_product_context_composes_real_document_and_knowledge_surfaces(self) -> None:
        document_record = self._record(
            subject_id=self.document_subject_id,
            version_id=Identity("version", "doc-1-v1", "org-a"),
            semantic_type="platform.document",
            payload=(("label", "governed source document"),),
        )
        artifact = ArtifactContent(
            artifact_id=Identity("artifact", "doc-1-source", "org-a"),
            organization=self.org,
            content_ref="content:doc-1-source",
            media_type="text/plain",
            integrity_ref="sha256:doc-1-source",
            rendition_role="source",
            handling=HandlingConstraints(
                classification="internal",
                purpose="bounded-product-review",
                rights=("read",),
                retention_rule="retain-reference",
            ),
        )
        admitted = admit_document_version(
            DocumentVersionCandidate(document_record, (artifact,), "source")
        )
        document_sources = DocumentWorkspaceSourceSet(
            lineages=(CanonicalLineage((document_record,)),),
            admitted_versions=(admitted,),
        )

        knowledge_subject = Identity("subject", "knowledge-1", "org-a")
        knowledge_record = self._record(
            subject_id=knowledge_subject,
            version_id=Identity("version", "knowledge-1-v1", "org-a"),
            semantic_type="platform.knowledge",
            payload=(("proposition", "Use the exact governed evidence set."),),
        )
        knowledge = ValidatedKnowledge(
            canonical_record=knowledge_record,
            evidence_refs=(Identity("evidence", "knowledge-e1", "org-a"),),
            constraints=KnowledgeConstraints(
                purpose="bounded-product-review",
                classification="internal",
                rights=("read",),
                freshness_state="Current",
            ),
            validation_result="valid",
            approval_ref=Identity("approval", "knowledge-a1", "org-a"),
        )
        knowledge_sources = MemoryKnowledgeSearchSources(knowledge=(knowledge,))

        context = compose_product_task_context(
            entry=self.entry,
            document_request=self.document_request,
            knowledge_request=self.knowledge_request,
            document_sources=document_sources,
            document_source_authorizations=(
                self._authorization(document_record.subject_id, "doc-access-v1"),
            ),
            knowledge_sources=knowledge_sources,
            knowledge_source_authorizations=(
                self._authorization(knowledge_record.subject_id, "knowledge-access-v1"),
            ),
        )

        self.assertIsInstance(context.document, DocumentWorkspaceInspection)
        self.assertEqual(context.document.displayed_version_id, document_record.version_id)
        self.assertEqual(context.document.authority_mode, AuthorityMode.NATIVE)
        self.assertEqual(len(context.document.artifacts), 1)
        self.assertFalse(context.document.artifacts[0].storage_locator_exposed)

        self.assertIsInstance(context.knowledge, KnowledgeWorkspaceView)
        self.assertEqual(len(context.knowledge.items), 1)
        self.assertEqual(context.knowledge.items[0].role, LearningRole.KNOWLEDGE)
        self.assertEqual(context.knowledge.items[0].version_id, knowledge_record.version_id)
        self.assertEqual(
            context.product_contract_version_id,
            self.contract.record.version_id,
        )

    def test_product_governed_execution_pins_exact_contract_version(self) -> None:
        task_record = self._record(
            subject_id=self.task.task_id,
            version_id=Identity("product-task-version", "task-1-v1", "org-a"),
            semantic_type=PRODUCT_TASK_SEMANTIC_TYPE,
            authority_scope=PRODUCT_TASK_AUTHORITY_SCOPE,
            payload=(("status", "Needs review"),),
            lifecycle_status="Open",
            provenance_refs=(self.principal.principal_id, self.product_id),
        )
        workflow_record = self._record(
            subject_id=Identity("workflow-subject", "p4-08-task-decision", "org-a"),
            version_id=Identity("workflow-version", "p4-08-task-decision-v1", "org-a"),
            semantic_type="platform.workflow",
            authority_scope="platform.workflow/definition",
            lifecycle_status=WorkflowLifecycle.APPROVED.value,
            provenance_refs=(self.principal.principal_id, task_record.subject_id),
        )
        workflow = WorkflowDefinition(
            record=workflow_record,
            operations=(
                WorkflowOperation(
                    semantic_name=OP_RECORD_TASK_DECISION,
                    target_subject_id=task_record.subject_id,
                    target_semantic_type=task_record.semantic_type,
                    side_effect_classes=(OperationSideEffectClass.CANONICAL_MUTATION,),
                ),
            ),
        )
        required_gates = (
            GovernedGateKind.AUTHORIZATION,
            GovernedGateKind.ORGANIZATIONAL_AUTHORITY,
            GovernedGateKind.DATA_GOVERNANCE,
            GovernedGateKind.CONSEQUENTIAL_APPROVAL,
        )
        interaction = ProductRuntimeInteraction(
            organization=self.org,
            product_id=self.product_id,
            product_version=PRODUCT_VERSION,
            dependency_id=GOVERNED_RUNTIME_DEPENDENCY,
            dependency_contract_version=GOVERNED_RUNTIME_CONTRACT_VERSION,
            workflow=workflow,
            operation_name=OP_RECORD_TASK_DECISION,
            material_inputs=(task_record,),
            required_gates=required_gates,
        )

        execution = start_product_task_execution(
            contract=self.contract,
            task=self.task,
            interaction=interaction,
            actor=self.actor,
            execution_id=Identity("execution-subject", "p4-08-task-1", "org-a"),
            version_id=Identity("execution-version", "p4-08-task-1-v1", "org-a"),
            created_at=self._time(2),
        )

        self.assertIsNotNone(execution.product_contract)
        self.assertEqual(
            execution.product_contract.version_id,
            self.contract.record.version_id,
        )
        self.assertEqual(execution.required_gates, required_gates)
        self.assertFalse(execution.gate_decisions)


if __name__ == "__main__":
    unittest.main()
