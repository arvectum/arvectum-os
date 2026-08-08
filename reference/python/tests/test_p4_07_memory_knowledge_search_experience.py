from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import unittest

import arvectum_os_ref
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.cross_capability_enforcement import AccessRequest
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE,
    MEMORY_SEMANTIC_TYPE,
    KnowledgeCandidate,
    KnowledgeConstraints,
    LearningRole,
    MemoryItem,
    Observation,
    ValidatedKnowledge,
)
from arvectum_os_ref.memory_knowledge_search_experience import (
    CanonicalKnowledgeState,
    DiscoveryAuthority,
    DiscoveryBlockCode,
    DiscoveryBlockedState,
    ExactRelianceState,
    KnowledgeRelianceError,
    KnowledgeWorkspaceView,
    MemoryKnowledgeSearchSources,
    ObservationSource,
    SearchDiscoveryView,
    discover_search,
    inspect_knowledge_workspace,
    render_knowledge_workspace_html,
    render_search_discovery_html,
    resolve_exact_knowledge_from_search,
    resolve_exact_knowledge_from_workspace,
)
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    WorkspaceDestination,
    navigate_workspace,
    open_workspace_shell,
)


class P407MemoryKnowledgeSearchExperienceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "operator", "platform"))
        self.other_principal = Principal(Identity("principal", "other", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.other_actor = ActorContext(self.other_principal, self.org)
        self.request = AccessRequest(
            self.actor, "decision-support", "internal-use", ("internal",)
        )
        self.current = KnowledgeConstraints(
            "decision-support", "internal", ("internal-use",), "current"
        )
        self.stale = KnowledgeConstraints(
            "decision-support", "internal", ("internal-use",), "review-required"
        )

        opened = open_workspace_shell(
            self.actor, initial_destination=WorkspaceDestination.KNOWLEDGE
        )
        if not hasattr(opened, "organization"):
            self.fail("expected open workspace")
        self.knowledge_workspace = opened
        self.discover_workspace = navigate_workspace(
            opened, destination=WorkspaceDestination.DISCOVER
        )

    def record(
        self,
        subject: str,
        version: str,
        *,
        semantic_type: str,
        payload_key: str,
        payload_value: str,
        predecessor: str | None = None,
        organization: OrganizationScope | None = None,
    ) -> CanonicalRecord:
        org = organization or self.org
        actor = self.actor if org == self.org else ActorContext(
            Principal(Identity("principal", "foreign-owner", "platform")), org
        )
        return CanonicalRecord(
            subject_id=Identity("subject", subject, org.organization_id.value),
            version_id=Identity("version", version, org.organization_id.value),
            semantic_type=semantic_type,
            schema_version="1",
            organization=org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/bounded-scope",
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=datetime(2026, 8, 8, 19, 0, tzinfo=timezone.utc),
            provenance_refs=(Identity("evidence", f"e-{version}", org.organization_id.value),),
            integrity_metadata=(("representation", "p4-07-test"),),
            payload=((payload_key, payload_value),),
            lifecycle_status="governed",
            predecessor_version_id=(
                Identity("version", predecessor, org.organization_id.value)
                if predecessor else None
            ),
        )

    def authorization(
        self,
        resource: Identity,
        *,
        allowed: bool = True,
        principal: Principal | None = None,
        organization: OrganizationScope | None = None,
    ) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=organization or self.org,
            actor_actual_principal_id=(principal or self.principal).principal_id,
            resource_subject_id=resource,
            decision_version_id=Identity(
                "authorization-version", f"auth-{resource.value}", "org-a"
            ),
            allowed=allowed,
        )

    def fixture(self) -> tuple[MemoryKnowledgeSearchSources, tuple[CurrentSourceAuthorization, ...]]:
        observation = Observation(
            Identity("observation", "obs-1", "org-a"),
            self.org,
            (Identity("event", "event-1", "org-a"),),
            "Observed recurring signal",
        )
        memory_record = self.record(
            "memory-1",
            "memory-v1",
            semantic_type=MEMORY_SEMANTIC_TYPE,
            payload_key="summary",
            payload_value="Remembered operating context",
        )
        memory = MemoryItem(
            memory_record,
            LearningRole.OBSERVATION,
            memory_record.provenance_refs,
            self.current,
        )
        candidate = KnowledgeCandidate(
            Identity("knowledge-candidate", "candidate-1", "org-a"),
            self.org,
            Identity("subject", "knowledge-1", "org-a"),
            "Candidate interpretation",
            (Identity("evidence", "candidate-evidence", "org-a"),),
            self.current,
            validation_result="validator-passed",
            approval_ref=Identity("decision", "candidate-review-ref", "org-a"),
        )
        k1_record = self.record(
            "knowledge-1",
            "knowledge-v1",
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            payload_key="proposition",
            payload_value="Older validated understanding",
        )
        k2_record = self.record(
            "knowledge-1",
            "knowledge-v2",
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            payload_key="proposition",
            payload_value="Current validated needle understanding",
            predecessor="knowledge-v1",
        )
        k1 = ValidatedKnowledge(
            k1_record,
            k1_record.provenance_refs,
            self.stale,
            "passed",
            Identity("decision", "approve-k1", "org-a"),
        )
        k2 = ValidatedKnowledge(
            k2_record,
            k2_record.provenance_refs,
            self.current,
            "passed",
            Identity("decision", "approve-k2", "org-a"),
        )

        search_constraints = DiscoveryConstraints(
            "decision-support", "internal", ("internal-use",), "retain-governed"
        )
        memory_source = GovernedSearchSource(
            memory_record, "needle remembered operating context", search_constraints
        )
        knowledge_source = GovernedSearchSource(
            k2_record, "needle current validated understanding", search_constraints
        )
        search_sources = (memory_source, knowledge_source)
        projection = rebuild_projection(sources=search_sources)

        sources = MemoryKnowledgeSearchSources(
            observations=(ObservationSource(observation, self.current),),
            memories=(memory,),
            candidates=(candidate,),
            knowledge=(k1, k2),
            knowledge_lineages=(CanonicalLineage((k1_record, k2_record)),),
            search_projection=projection,
            search_sources=search_sources,
        )
        authorizations = (
            self.authorization(observation.observation_id),
            self.authorization(memory_record.subject_id),
            self.authorization(candidate.candidate_id),
            self.authorization(k2.subject_id),
        )
        return sources, authorizations

    def knowledge_view(self) -> KnowledgeWorkspaceView:
        sources, authorizations = self.fixture()
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=sources,
            source_authorizations=authorizations,
            access_request=self.request,
        )
        self.assertIsInstance(result, KnowledgeWorkspaceView)
        assert isinstance(result, KnowledgeWorkspaceView)
        return result

    def search_view(self) -> SearchDiscoveryView:
        sources, authorizations = self.fixture()
        result = discover_search(
            workspace=self.discover_workspace,
            sources=sources,
            source_authorizations=authorizations,
            access_request=self.request,
            query_text="needle",
        )
        self.assertIsInstance(result, SearchDiscoveryView)
        assert isinstance(result, SearchDiscoveryView)
        return result

    def test_epistemic_roles_remain_visibly_distinct(self) -> None:
        result = self.knowledge_view()
        self.assertEqual(
            [item.role for item in result.items],
            [
                LearningRole.OBSERVATION,
                LearningRole.MEMORY,
                LearningRole.CANDIDATE,
                LearningRole.KNOWLEDGE,
                LearningRole.KNOWLEDGE,
            ],
        )
        self.assertIs(result.items[0].canonical_state, CanonicalKnowledgeState.NON_CANONICAL)
        self.assertIs(result.items[1].canonical_state, CanonicalKnowledgeState.MEMORY)
        self.assertIs(result.items[2].canonical_state, CanonicalKnowledgeState.NON_CANONICAL)
        self.assertTrue(
            all(
                item.canonical_state is CanonicalKnowledgeState.KNOWLEDGE
                for item in result.items[-2:]
            )
        )

    def test_candidate_validation_and_approval_evidence_do_not_promote_it(self) -> None:
        candidate = next(
            item for item in self.knowledge_view().items
            if item.role is LearningRole.CANDIDATE
        )
        self.assertEqual(candidate.validation_result, "validator-passed")
        self.assertEqual(candidate.approval_ref.value, "candidate-review-ref")
        self.assertFalse(candidate.promotion_available)
        self.assertIs(candidate.exact_reliance, ExactRelianceState.NOT_APPLICABLE)
        self.assertIn("remains non-Knowledge", candidate.status_text)

    def test_memory_preserves_remembered_status_without_truth_upgrade(self) -> None:
        memory = next(
            item for item in self.knowledge_view().items
            if item.role is LearningRole.MEMORY
        )
        self.assertIn("remembered role 'Observation'", memory.status_text)
        self.assertNotEqual(memory.canonical_state, CanonicalKnowledgeState.KNOWLEDGE)

    def test_stale_knowledge_is_inspectable_but_not_reliance_eligible(self) -> None:
        stale = next(
            item for item in self.knowledge_view().items
            if item.version_id is not None and item.version_id.value == "knowledge-v1"
        )
        self.assertEqual(stale.freshness_state, "review-required")
        self.assertIs(stale.exact_reliance, ExactRelianceState.STALE)

    def test_current_exact_knowledge_requires_explicit_version_and_resolves_cap002(self) -> None:
        sources, authorizations = self.fixture()
        view = self.knowledge_view()
        current = next(
            item for item in view.items
            if item.version_id is not None and item.version_id.value == "knowledge-v2"
        )
        reliance = resolve_exact_knowledge_from_workspace(
            item=current,
            workspace=self.knowledge_workspace,
            sources=sources,
            source_authorizations=authorizations,
            access_request=self.request,
            selected_version_id=current.version_id,
        )
        self.assertEqual(reliance.version_id.value, "knowledge-v2")
        self.assertEqual(reliance.validation_result, "passed")

    def test_wrong_or_stale_exact_knowledge_selection_fails_closed(self) -> None:
        sources, authorizations = self.fixture()
        view = self.knowledge_view()
        current = next(item for item in view.items if item.version_id and item.version_id.value == "knowledge-v2")
        stale = next(item for item in view.items if item.version_id and item.version_id.value == "knowledge-v1")
        with self.assertRaisesRegex(KnowledgeRelianceError, "select the exact"):
            resolve_exact_knowledge_from_workspace(
                item=current,
                workspace=self.knowledge_workspace,
                sources=sources,
                source_authorizations=authorizations,
                access_request=self.request,
                selected_version_id=stale.version_id,
            )
        with self.assertRaisesRegex(KnowledgeRelianceError, "freshness"):
            resolve_exact_knowledge_from_workspace(
                item=stale,
                workspace=self.knowledge_workspace,
                sources=sources,
                source_authorizations=authorizations,
                access_request=self.request,
                selected_version_id=stale.version_id,
            )

    def test_knowledge_exact_reliance_rechecks_current_source_authorization(self) -> None:
        sources, authorizations = self.fixture()
        current = next(
            item for item in self.knowledge_view().items
            if item.version_id and item.version_id.value == "knowledge-v2"
        )
        denied = tuple(
            self.authorization(decision.resource_subject_id, allowed=False)
            if decision.resource_subject_id == current.subject_id else decision
            for decision in authorizations
        )
        with self.assertRaisesRegex(KnowledgeRelianceError, "not uniquely authorized"):
            resolve_exact_knowledge_from_workspace(
                item=current,
                workspace=self.knowledge_workspace,
                sources=sources,
                source_authorizations=denied,
                access_request=self.request,
                selected_version_id=current.version_id,
            )

    def test_collection_omits_unauthorized_item_without_protected_count(self) -> None:
        sources, authorizations = self.fixture()
        candidate = sources.candidates[0]
        filtered = tuple(
            decision for decision in authorizations
            if decision.resource_subject_id != candidate.candidate_id
        )
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=sources,
            source_authorizations=filtered,
            access_request=self.request,
        )
        assert isinstance(result, KnowledgeWorkspaceView)
        html = render_knowledge_workspace_html(result)
        self.assertNotIn("candidate-1", html)
        self.assertNotIn("Candidate interpretation", html)
        self.assertNotIn("4 items", html)
        self.assertIn("omitted without protected counts", html)

    def test_duplicate_source_authorization_fails_closed_for_collection_visibility(self) -> None:
        sources, authorizations = self.fixture()
        memory = sources.memories[0]
        duplicate = self.authorization(memory.canonical_record.subject_id)
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=sources,
            source_authorizations=authorizations + (duplicate,),
            access_request=self.request,
        )
        assert isinstance(result, KnowledgeWorkspaceView)
        self.assertFalse(any(
            item.resource_id == memory.canonical_record.subject_id
            and item.role is LearningRole.MEMORY
            for item in result.items
        ))

    def test_actor_context_mismatch_blocks_before_content(self) -> None:
        sources, authorizations = self.fixture()
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=sources,
            source_authorizations=authorizations,
            access_request=AccessRequest(
                self.other_actor, "decision-support", "internal-use", ("internal",)
            ),
        )
        self.assertIsInstance(result, DiscoveryBlockedState)
        assert isinstance(result, DiscoveryBlockedState)
        self.assertIs(result.code, DiscoveryBlockCode.ACCESS_CONTEXT_MISMATCH)
        html = render_knowledge_workspace_html(result)
        self.assertNotIn("knowledge-v2", html)
        self.assertNotIn("Candidate interpretation", html)

    def test_purpose_right_classification_constraints_filter_learning_items(self) -> None:
        sources, authorizations = self.fixture()
        for request in (
            AccessRequest(self.actor, "other-purpose", "internal-use", ("internal",)),
            AccessRequest(self.actor, "decision-support", "export", ("internal",)),
            AccessRequest(self.actor, "decision-support", "internal-use", ("public",)),
        ):
            with self.subTest(request=request):
                result = inspect_knowledge_workspace(
                    workspace=self.knowledge_workspace,
                    sources=sources,
                    source_authorizations=authorizations,
                    access_request=request,
                )
                assert isinstance(result, KnowledgeWorkspaceView)
                self.assertEqual(result.items, ())

    def test_search_is_explicitly_derived_non_authoritative_and_exact_versioned(self) -> None:
        result = self.search_view()
        self.assertIs(result.discovery_authority, DiscoveryAuthority.DERIVED)
        self.assertEqual(
            {hit.source_version_id.value for hit in result.hits},
            {"memory-v1", "knowledge-v2"},
        )
        self.assertTrue(all(hit.discovery_authority is DiscoveryAuthority.DERIVED for hit in result.hits))
        html = render_search_discovery_html(result)
        self.assertIn("Derived discovery/projection", html)
        self.assertIn("Search match/order is a discovery signal only", html)
        self.assertNotIn("ranking_score", html)
        self.assertNotIn("confidence score", html)

    def test_search_result_rechecks_source_authorization_and_omits_without_count(self) -> None:
        sources, authorizations = self.fixture()
        knowledge_subject = sources.knowledge[-1].subject_id
        filtered = tuple(
            decision for decision in authorizations
            if decision.resource_subject_id != knowledge_subject
        )
        result = discover_search(
            workspace=self.discover_workspace,
            sources=sources,
            source_authorizations=filtered,
            access_request=self.request,
            query_text="needle",
        )
        assert isinstance(result, SearchDiscoveryView)
        html = render_search_discovery_html(result)
        self.assertNotIn("knowledge-v2", html)
        self.assertNotIn("Current validated needle understanding", html)
        self.assertNotIn("1 result", html)
        self.assertIn("omitted without protected counts", html)

    def test_stale_projection_is_not_presented_as_current_discovery(self) -> None:
        sources, authorizations = self.fixture()
        old_source = sources.search_sources[-1]
        newer_record = self.record(
            "knowledge-1",
            "knowledge-v3",
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            payload_key="proposition",
            payload_value="Newer source",
            predecessor="knowledge-v2",
        )
        newer_source = GovernedSearchSource(
            newer_record,
            "needle newer source",
            old_source.constraints,
        )
        changed = MemoryKnowledgeSearchSources(
            observations=sources.observations,
            memories=sources.memories,
            candidates=sources.candidates,
            knowledge=sources.knowledge,
            knowledge_lineages=sources.knowledge_lineages,
            search_projection=sources.search_projection,
            search_sources=(sources.search_sources[0], newer_source),
        )
        result = discover_search(
            workspace=self.discover_workspace,
            sources=changed,
            source_authorizations=authorizations,
            access_request=self.request,
            query_text="needle",
        )
        assert isinstance(result, SearchDiscoveryView)
        self.assertFalse(any(hit.source_subject_id == newer_record.subject_id for hit in result.hits))

    def test_freshness_prevents_search_projection_from_making_stale_knowledge_current(self) -> None:
        sources, authorizations = self.fixture()
        current = sources.knowledge[-1]
        stale_copy = ValidatedKnowledge(
            current.canonical_record,
            current.evidence_refs,
            self.stale,
            current.validation_result,
            current.approval_ref,
        )
        changed = MemoryKnowledgeSearchSources(
            observations=sources.observations,
            memories=sources.memories,
            candidates=sources.candidates,
            knowledge=(sources.knowledge[0], stale_copy),
            knowledge_lineages=sources.knowledge_lineages,
            search_projection=sources.search_projection,
            search_sources=sources.search_sources,
        )
        result = discover_search(
            workspace=self.discover_workspace,
            sources=changed,
            source_authorizations=authorizations,
            access_request=self.request,
            query_text="needle",
        )
        assert isinstance(result, SearchDiscoveryView)
        self.assertFalse(any(hit.role_text == LearningRole.KNOWLEDGE.value for hit in result.hits))

    def test_search_exact_knowledge_reliance_exits_projection_through_exact_source(self) -> None:
        sources, authorizations = self.fixture()
        hit = next(
            value for value in self.search_view().hits
            if value.role_text == LearningRole.KNOWLEDGE.value
        )
        reliance = resolve_exact_knowledge_from_search(
            hit=hit,
            workspace=self.discover_workspace,
            sources=sources,
            source_authorizations=authorizations,
            access_request=self.request,
            selected_version_id=hit.source_version_id,
        )
        self.assertEqual(reliance.version_id.value, "knowledge-v2")

    def test_search_exact_reliance_rechecks_current_source_and_selection(self) -> None:
        sources, authorizations = self.fixture()
        hit = next(
            value for value in self.search_view().hits
            if value.role_text == LearningRole.KNOWLEDGE.value
        )
        with self.assertRaisesRegex(KnowledgeRelianceError, "select the exact"):
            resolve_exact_knowledge_from_search(
                hit=hit,
                workspace=self.discover_workspace,
                sources=sources,
                source_authorizations=authorizations,
                access_request=self.request,
                selected_version_id=Identity("version", "knowledge-v1", "org-a"),
            )
        changed = MemoryKnowledgeSearchSources(
            observations=sources.observations,
            memories=sources.memories,
            candidates=sources.candidates,
            knowledge=sources.knowledge,
            knowledge_lineages=sources.knowledge_lineages,
            search_projection=sources.search_projection,
            search_sources=(sources.search_sources[0],),
        )
        with self.assertRaises(KnowledgeRelianceError):
            resolve_exact_knowledge_from_search(
                hit=hit,
                workspace=self.discover_workspace,
                sources=changed,
                source_authorizations=authorizations,
                access_request=self.request,
                selected_version_id=hit.source_version_id,
            )

    def test_renderer_escapes_governed_learning_text(self) -> None:
        sources, authorizations = self.fixture()
        candidate = sources.candidates[0]
        malicious = KnowledgeCandidate(
            candidate.candidate_id,
            candidate.organization,
            candidate.subject_id,
            "<script>alert(1)</script>",
            candidate.evidence_refs,
            candidate.constraints,
        )
        changed = MemoryKnowledgeSearchSources(
            observations=sources.observations,
            memories=sources.memories,
            candidates=(malicious,),
            knowledge=sources.knowledge,
            knowledge_lineages=sources.knowledge_lineages,
            search_projection=sources.search_projection,
            search_sources=sources.search_sources,
        )
        result = inspect_knowledge_workspace(
            workspace=self.knowledge_workspace,
            sources=changed,
            source_authorizations=authorizations,
            access_request=self.request,
        )
        html = render_knowledge_workspace_html(result)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_search_preview_is_minimized(self) -> None:
        sources, authorizations = self.fixture()
        long_source = GovernedSearchSource(
            sources.search_sources[1].canonical_record,
            "needle " + ("x " * 300),
            sources.search_sources[1].constraints,
        )
        changed = MemoryKnowledgeSearchSources(
            observations=sources.observations,
            memories=sources.memories,
            candidates=sources.candidates,
            knowledge=sources.knowledge,
            knowledge_lineages=sources.knowledge_lineages,
            search_projection=rebuild_projection(sources=(sources.search_sources[0], long_source)),
            search_sources=(sources.search_sources[0], long_source),
        )
        result = discover_search(
            workspace=self.discover_workspace,
            sources=changed,
            source_authorizations=authorizations,
            access_request=self.request,
            query_text="needle",
        )
        assert isinstance(result, SearchDiscoveryView)
        knowledge = next(hit for hit in result.hits if hit.role_text == LearningRole.KNOWLEDGE.value)
        self.assertLessEqual(len(knowledge.preview), 180)
        self.assertTrue(knowledge.preview.endswith("…"))

    def test_module_has_no_promotion_path_or_public_package_export(self) -> None:
        module_path = Path(__file__).parents[1] / "arvectum_os_ref" / "memory_knowledge_search_experience.py"
        text = module_path.read_text(encoding="utf-8")
        self.assertNotIn("promote_candidate", text)
        self.assertNotIn("record_approval(", text)
        self.assertNotIn("record_validation(", text)
        self.assertFalse(hasattr(arvectum_os_ref, "discover_search"))
        self.assertFalse(hasattr(arvectum_os_ref, "inspect_knowledge_workspace"))
        self.assertNotIn("fetch(", text)
        self.assertNotIn("requests.", text)


if __name__ == "__main__":
    unittest.main()
