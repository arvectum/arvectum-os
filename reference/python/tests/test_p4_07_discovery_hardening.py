from __future__ import annotations

from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE,
    KnowledgeConstraints,
    ValidatedKnowledge,
)
from arvectum_os_ref.memory_knowledge_search_experience import (
    MemoryKnowledgeSearchSources,
    SearchDiscoveryView,
    discover_search,
    render_search_discovery_html,
)
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import WorkspaceDestination, open_workspace_shell


class P407DiscoveryHardeningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-a", "platform")
        )
        self.principal = Principal(Identity("principal", "operator", "platform"))
        self.actor = ActorContext(self.principal, self.organization)
        opened = open_workspace_shell(
            self.actor, initial_destination=WorkspaceDestination.DISCOVER
        )
        if not hasattr(opened, "organization"):
            self.fail("expected open workspace")
        self.workspace = opened
        self.request = AccessRequest(
            self.actor, "decision-support", "internal-use", ("internal",)
        )
        self.knowledge_constraints = KnowledgeConstraints(
            "decision-support", "internal", ("internal-use",), "current"
        )
        self.discovery_constraints = DiscoveryConstraints(
            "decision-support", "internal", ("internal-use",), "retain-governed"
        )

    def record(self, proposition: str) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=Identity("subject", "knowledge-1", "org-a"),
            version_id=Identity("version", "knowledge-v1", "org-a"),
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            schema_version="1",
            organization=self.organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="platform.knowledge/test",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 20, 0, tzinfo=timezone.utc),
            provenance_refs=(Identity("evidence", proposition, "org-a"),),
            integrity_metadata=(("representation", "hardening-test"),),
            payload=(("proposition", proposition),),
            lifecycle_status="governed",
        )

    def authorization(self, subject_id: Identity) -> tuple[CurrentSourceAuthorization, ...]:
        return (
            CurrentSourceAuthorization(
                organization=self.organization,
                actor_actual_principal_id=self.principal.principal_id,
                resource_subject_id=subject_id,
                decision_version_id=Identity(
                    "authorization-version", "allow-k1", "org-a"
                ),
                allowed=True,
            ),
        )

    def test_same_ids_with_different_canonical_record_cannot_inherit_validated_knowledge_status(self) -> None:
        indexed_record = self.record("indexed exact source")
        conflicting_record = self.record("conflicting content under reused version identity")
        validated = ValidatedKnowledge(
            conflicting_record,
            conflicting_record.provenance_refs,
            self.knowledge_constraints,
            "passed",
            Identity("decision", "approve-conflict", "org-a"),
        )
        search_source = GovernedSearchSource(
            indexed_record,
            "needle indexed exact source",
            self.discovery_constraints,
        )
        sources = MemoryKnowledgeSearchSources(
            knowledge=(validated,),
            search_projection=rebuild_projection(sources=(search_source,)),
            search_sources=(search_source,),
        )
        result = discover_search(
            workspace=self.workspace,
            sources=sources,
            source_authorizations=self.authorization(indexed_record.subject_id),
            access_request=self.request,
            query_text="needle",
        )
        self.assertIsInstance(result, SearchDiscoveryView)
        assert isinstance(result, SearchDiscoveryView)
        self.assertEqual(result.hits, ())
        self.assertNotIn("conflicting content", render_search_discovery_html(result))

    def test_missing_projection_is_explicit_gap_not_claim_of_source_absence(self) -> None:
        result = discover_search(
            workspace=self.workspace,
            sources=MemoryKnowledgeSearchSources(),
            source_authorizations=(),
            access_request=self.request,
            query_text="needle",
        )
        self.assertIsInstance(result, SearchDiscoveryView)
        assert isinstance(result, SearchDiscoveryView)
        self.assertEqual(result.hits, ())
        self.assertIn("projection unavailable", result.projection_status_text.lower())
        self.assertIn("no inference", result.projection_status_text.lower())
        html = render_search_discovery_html(result)
        self.assertIn("Projection status", html)
        self.assertIn("no inference is made about canonical source absence", html)


if __name__ == "__main__":
    unittest.main()
