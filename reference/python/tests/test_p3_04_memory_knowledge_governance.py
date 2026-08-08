from __future__ import annotations

from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import (
    KNOWLEDGE_SEMANTIC_TYPE, MEMORY_SEMANTIC_TYPE, KnowledgeCandidate,
    KnowledgeConstraints, KnowledgePromotionError, LearningRole, MemoryItem,
    Observation, promote_candidate, record_approval, record_validation,
    resolve_exact_knowledge_reliance, retrieve_eligible_knowledge,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P304MemoryKnowledgeGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.actor = ActorContext(Principal(Identity("principal", "owner", "platform")), self.org)
        self.constraints = KnowledgeConstraints("decision-support", "internal", ("internal-use",), "current")

    def record(self, version: str, predecessor: str | None = None) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=Identity("knowledge", "k-1", "org-a"),
            version_id=Identity("knowledge-version", version, "org-a"),
            semantic_type=KNOWLEDGE_SEMANTIC_TYPE,
            schema_version="1", organization=self.org, authority_mode=AuthorityMode.NATIVE,
            authority_scope="knowledge/adopted-understanding",
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor, created_at=datetime(2026, 8, 8, 13, 0, tzinfo=timezone.utc),
            provenance_refs=(Identity("evidence", f"e-{version}", "org-a"),),
            integrity_metadata=(("representation", "bounded-reference"),),
            payload=(("proposition", f"validated understanding {version}"),), lifecycle_status="validated",
            predecessor_version_id=Identity("knowledge-version", predecessor, "org-a") if predecessor else None,
        )

    def candidate(self) -> KnowledgeCandidate:
        return KnowledgeCandidate(
            Identity("knowledge-candidate", "c-1", "org-a"), self.org,
            Identity("knowledge", "k-1", "org-a"), "candidate understanding",
            (Identity("evidence", "e-1", "org-a"),), self.constraints,
        )

    def validated(self, record: CanonicalRecord):
        candidate = record_approval(record_validation(self.candidate(), result="passed"), approval_ref=Identity("decision", f"approve-{record.version_id.value}", "org-a"))
        return promote_candidate(candidate=candidate, canonical_record=record)

    def test_observation_is_not_knowledge(self) -> None:
        observation = Observation(Identity("observation", "o-1", "org-a"), self.org, (Identity("event", "e-1", "org-a"),), "observed pattern")
        self.assertEqual(observation.assertion, "observed pattern")
        self.assertFalse(hasattr(observation, "approval_ref"))

    def test_memory_preserves_epistemic_role_without_silent_validation(self) -> None:
        record = CanonicalRecord(
            subject_id=Identity("memory", "m-1", "org-a"), version_id=Identity("memory-version", "v1", "org-a"),
            semantic_type=MEMORY_SEMANTIC_TYPE, schema_version="1", organization=self.org,
            authority_mode=AuthorityMode.NATIVE, authority_scope="memory/retained-context",
            accountable_owner_id=self.actor.actual_principal.principal_id, creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 13, 0, tzinfo=timezone.utc),
            provenance_refs=(Identity("observation", "o-1", "org-a"),), integrity_metadata=(("representation", "bounded-reference"),),
        )
        memory = MemoryItem(record, LearningRole.OBSERVATION, record.provenance_refs, self.constraints)
        self.assertIs(memory.remembered_role, LearningRole.OBSERVATION)
        with self.assertRaises(ValueError):
            MemoryItem(record, LearningRole.KNOWLEDGE, record.provenance_refs, self.constraints)

    def test_validation_and_approval_are_distinct_promotion_gates(self) -> None:
        with self.assertRaises(KnowledgePromotionError):
            promote_candidate(candidate=self.candidate(), canonical_record=self.record("v1"))
        validated_only = record_validation(self.candidate(), result="passed")
        with self.assertRaises(KnowledgePromotionError):
            promote_candidate(candidate=validated_only, canonical_record=self.record("v1"))
        approved = record_approval(validated_only, approval_ref=Identity("decision", "approve-v1", "org-a"))
        self.assertEqual(promote_candidate(candidate=approved, canonical_record=self.record("v1")).validation_result, "passed")

    def test_cross_organization_promotion_fails_closed(self) -> None:
        candidate = KnowledgeCandidate(Identity("candidate", "c", "org-b"), self.other_org, Identity("knowledge", "k-1", "org-a"), "x", (Identity("evidence", "e", "org-b"),), self.constraints, "passed", Identity("decision", "d", "org-b"))
        with self.assertRaises(KnowledgePromotionError):
            promote_candidate(candidate=candidate, canonical_record=self.record("v1"))

    def test_retrieval_filters_scope_purpose_rights_and_freshness(self) -> None:
        item = self.validated(self.record("v1"))
        self.assertEqual(len(retrieve_eligible_knowledge(knowledge=(item,), organization=self.org, purpose="decision-support", required_right="internal-use")), 1)
        self.assertEqual(retrieve_eligible_knowledge(knowledge=(item,), organization=self.other_org, purpose="decision-support", required_right="internal-use"), ())
        self.assertEqual(retrieve_eligible_knowledge(knowledge=(item,), organization=self.org, purpose="other", required_right="internal-use"), ())
        self.assertEqual(retrieve_eligible_knowledge(knowledge=(item,), organization=self.org, purpose="decision-support", required_right="export"), ())

    def test_retrieval_projection_is_not_canonical_authority(self) -> None:
        projection = retrieve_eligible_knowledge(knowledge=(self.validated(self.record("v1")),), organization=self.org, purpose="decision-support", required_right="internal-use")[0]
        self.assertEqual(projection.ranking_score, 1.0)
        self.assertFalse(hasattr(projection, "authority_mode"))

    def test_exact_reliance_pins_old_version_without_head_inference(self) -> None:
        v1, v2 = self.record("v1"), self.record("v2", "v1")
        k1, k2 = self.validated(v1), self.validated(v2)
        lineage = CanonicalLineage((v1, v2))
        reliance = resolve_exact_knowledge_reliance(lineage=lineage, validated=(k1, k2), version_id=v1.version_id)
        self.assertEqual(reliance.version_id, v1.version_id)
        self.assertNotEqual(reliance.version_id, lineage.head.version_id)


if __name__ == "__main__":
    unittest.main()
