from __future__ import annotations

from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE,
    MEMORY_SEMANTIC_TYPE,
    KnowledgeConstraints,
    LearningRole,
    MemoryItem,
    ValidatedKnowledge,
)
from arvectum_os_ref.memory_knowledge_search_experience import (
    KnowledgeWorkspaceView,
    MemoryKnowledgeSearchSources,
    SearchDiscoveryView,
    discover_search,
    inspect_knowledge_workspace,
)
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import WorkspaceDestination, open_workspace_shell


class P407SemanticOwnerHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.principal = Principal(Identity("principal", "operator", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        self.request = AccessRequest(
            self.actor, "decision-support", "internal-use", ("internal",)
        )
        knowledge_opened = open_workspace_shell(
            self.actor, initial_destination=WorkspaceDestination.KNOWLEDGE
        )
        discover_opened = open_workspace_shell(
            self.actor, initial_destination=WorkspaceDestination.DISCOVER
        )
        if not hasattr(knowledge_opened, "organization") or not hasattr(discover_opened, "organization"):
            self.fail("expected open workspace")
        self.knowledge_workspace = knowledge_opened
        self.discover_workspace = discover_opened

    def record(self, *, semantic_type: str, subject: str, version: str, text: str) -> CanonicalRecord:
        payload_key = "summary" if semantic_type == MEMORY_SEMANTIC_TYPE else "proposition"
        return CanonicalRecord(
            subject_id=Identity("subject", subject, "org-a"),
            version_id=Identity("version", version, "org-a"),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/hardening",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 20, 15, tzinfo=timezone.utc),
            provenance_refs=(Identity("evidence", f"e-{version}", "org-a"),),
            integrity_metadata=(("representation", "p4-07-semantic-owner-test"),),
            payload=((payload_key, text),),
            lifecycle_status="governed",
        )

    def authorization(self, subject_id: Identity) -> tuple[CurrentSourceAuthorization, ...]:
        return (
            CurrentSourceAuthorization(
                organization=self.organization,
                actor_actual_principal_id=self.principal.principal_id,
                resource_subject_id=subject_id,
                decision_version_id=Identity(
                    "authorization-version", f"allow-{subject_id.value}", "org-a"
                ),
                allowed=True,
            ),
        )

    def test_search_projection_cannot_broaden_memory_semantic_owner_constraints(self) -> None:
        record = self.record(
            semantic_type=MEMORY_SEMANTIC_TYPE,
            subject="memory-1",
            version="memory-v1",
            text="restricted retained context",
        )
        memory = MemoryItem(
            record,
            LearningRole.OBSERVATION,
            record.provenance_refs,
            KnowledgeConstraints(
                "decision-support", "confidential", ("restricted-use",), "current"
            ),
        )
        search_source = GovernedSearchSource(
            record,
            "needle restricted retained context",
            DiscoveryConstraints(
                "decision-support", "internal", ("internal-use",), "retain-governed"
            ),
        )
        sources = MemoryKnowledgeSearchSources(
            memories=(memory,),
            search_projection=rebuild_projection(sources=(search_source,)),
            search_sources=(search_source,),
        )
        result = discover_search(
            workspace=self.discover_workspace,
            sources=sources,
            source_authorizations=self.authorization(record.subject_id),
            access_request=self.request,
            query_text="needle",
        )
        self.assertIsInstance(result, SearchDiscoveryView)
        assert isinstance(result, SearchDiscoveryView)
        self.assertEqual(result.hits, ())

    def test_duplicate_exact_validated_knowledge_is_omitted_as_ambiguous(self) -> None:
        record = self.record(
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            subject="knowledge-1",
            version="knowledge-v1",
            text="validated proposition",
        )
        constraints = KnowledgeConstraints(
            "decision-support", "internal", ("internal-use",), "current"
        )
        first = ValidatedKnowledge(
            record,
            record.provenance_refs,
            constraints,
            "passed",
            Identity("decision", "approve-1", "org-a"),
        )
        second = ValidatedKnowledge(
            record,
            record.provenance_refs,
            constraints,
            "passed",
            Identity("decision", "approve-2", "org-a"),
        )
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=MemoryKnowledgeSearchSources(knowledge=(first, second)),
            source_authorizations=self.authorization(record.subject_id),
            access_request=self.request,
        )
        self.assertIsInstance(result, KnowledgeWorkspaceView)
        assert isinstance(result, KnowledgeWorkspaceView)
        self.assertEqual(result.items, ())

    def test_duplicate_exact_memory_is_omitted_as_ambiguous(self) -> None:
        record = self.record(
            semantic_type=MEMORY_SEMANTIC_TYPE,
            subject="memory-1",
            version="memory-v1",
            text="retained context",
        )
        constraints = KnowledgeConstraints(
            "decision-support", "internal", ("internal-use",), "current"
        )
        first = MemoryItem(record, LearningRole.OBSERVATION, record.provenance_refs, constraints)
        second = MemoryItem(record, LearningRole.CANDIDATE, record.provenance_refs, constraints)
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=MemoryKnowledgeSearchSources(memories=(first, second)),
            source_authorizations=self.authorization(record.subject_id),
            access_request=self.request,
        )
        self.assertIsInstance(result, KnowledgeWorkspaceView)
        assert isinstance(result, KnowledgeWorkspaceView)
        self.assertEqual(result.items, ())


if __name__ == "__main__":
    unittest.main()
