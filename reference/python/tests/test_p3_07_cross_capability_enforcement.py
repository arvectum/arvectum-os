from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import (
    AccessRequest, CrossCapabilityEnforcementError, reconstruct_audit_for_access,
    resolve_document_for_access, resolve_search_hit_for_access,
    retrieve_knowledge_for_access, search_for_access,
)
from arvectum_os_ref.document_artifact_governance import ArtifactContent, DocumentVersionCandidate, HandlingConstraints, admit_document_version
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import KnowledgeConstraints, ValidatedKnowledge
from arvectum_os_ref.search_index_projection import DiscoveryConstraints, GovernedSearchSource, rebuild_projection
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P307CrossCapabilityEnforcementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org_a = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.actor = ActorContext(Principal(self._id("principal", "alice")), self.org_a)
        self.request = AccessRequest(self.actor, "review", "read", ("internal",))

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(self, *, subject: str, version: str, semantic_type: str, organization=None, payload=()):
        organization = organization or self.org_a
        scope = organization.organization_id.value
        creation_actor = ActorContext(Principal(self._id("principal", "creator", scope)), organization)
        return CanonicalRecord(
            subject_id=self._id("subject", subject, scope), version_id=self._id("version", version, scope),
            semantic_type=semantic_type, schema_version="1", organization=organization,
            authority_mode=AuthorityMode.NATIVE, authority_scope=f"{semantic_type}/state",
            accountable_owner_id=self._id("principal", "owner", scope), creation_actor=creation_actor,
            created_at=datetime(2026, 8, 8, tzinfo=timezone.utc),
            provenance_refs=(creation_actor.actual_principal.principal_id,),
            integrity_metadata=(("representation", "p3.07-test"),), payload=payload, lifecycle_status="Retained",
        )

    def _document(self, organization=None, *, purpose="review", rights=("read",), classification="internal"):
        organization = organization or self.org_a
        record = self._record(subject="doc", version="doc-v1", semantic_type="platform.document", organization=organization)
        artifact = ArtifactContent(
            artifact_id=self._id("artifact", "a1", organization.organization_id.value), organization=organization,
            content_ref="content", media_type="text/plain", integrity_ref="sha256:x", rendition_role="source",
            handling=HandlingConstraints(classification, purpose, rights, "retain"),
        )
        return admit_document_version(candidate=DocumentVersionCandidate(record, (artifact,), "source")), artifact

    def test_cap001_denies_cross_organization_and_rights_mismatch(self):
        foreign, artifact = self._document(self.org_b)
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_document_for_access(admitted=foreign, artifact_id=artifact.artifact_id, request=self.request)
        local, artifact = self._document(rights=("write",))
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_document_for_access(admitted=local, artifact_id=artifact.artifact_id, request=self.request)

    def test_cap001_allows_only_matching_current_context(self):
        local, artifact = self._document()
        reliance = resolve_document_for_access(admitted=local, artifact_id=artifact.artifact_id, request=self.request)
        self.assertEqual(reliance.document_version_id, local.version_id)

    def test_cap002_filters_organization_purpose_right_classification_and_freshness(self):
        eligible = ValidatedKnowledge(self._record(subject="k1", version="k1-v1", semantic_type="platform.knowledge", payload=(("proposition", "eligible"),)), (self._id("evidence", "e1"),), KnowledgeConstraints("review", "internal", ("read",), "Current"), "valid", self._id("approval", "a1"))
        wrong_purpose = ValidatedKnowledge(self._record(subject="k2", version="k2-v1", semantic_type="platform.knowledge"), (self._id("evidence", "e2"),), KnowledgeConstraints("train", "internal", ("read",), "Current"), "valid", self._id("approval", "a2"))
        hits = retrieve_knowledge_for_access(knowledge=(eligible, wrong_purpose), request=self.request)
        self.assertEqual(tuple(hit.source_version_id for hit in hits), (eligible.version_id,))

    def test_cap003_discovery_and_source_access_use_same_request_context(self):
        source = GovernedSearchSource(self._record(subject="s1", version="s1-v1", semantic_type="platform.knowledge"), "needle", DiscoveryConstraints("review", "internal", ("read",), "retain"))
        projection = rebuild_projection(sources=(source,))
        hits = search_for_access(projection=projection, current_sources=(source,), query_text="needle", request=self.request)
        self.assertEqual(len(hits), 1)
        self.assertEqual(resolve_search_hit_for_access(hit=hits[0], current_sources=(source,), request=self.request).version_id, source.version_id)
        denied = AccessRequest(self.actor, "review", "export", ("internal",))
        self.assertEqual(search_for_access(projection=projection, current_sources=(source,), query_text="needle", request=denied), ())
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_search_hit_for_access(hit=hits[0], current_sources=(source,), request=denied)

    def test_cap004_redacts_disallowed_evidence_and_denies_foreign_organization(self):
        workflow = GovernedVersionPin(self._id("subject", "wf"), self._id("version", "wf-v1"), "platform.workflow", "workflow/state", "Retained")
        result = GovernedVersionPin(self._id("subject", "result"), self._id("version", "result-v1"), "example.result", "result/state", "Retained")
        manifest = ReconstructionManifest(
            organization=self.org_a, execution_subject_id=self._id("execution", "x"), initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review", workflow=workflow, material_inputs=(), gate_decisions=(), execution_versions=(), results=(result,), events=(), event_types=(),
            correlation_refs=(), causation_refs=(), provenance_refs=(workflow.subject_id, workflow.version_id, result.subject_id, result.version_id),
        )
        view = reconstruct_audit_for_access(manifest=manifest, request=self.request, evidence_constraints=((workflow.version_id, "review", ("read",), "internal"), (result.version_id, "review", ("export",), "internal")))
        states = {item.version_id: item.availability.value for item in view.evidence}
        self.assertEqual(states[workflow.version_id], "Available")
        self.assertEqual(states[result.version_id], "Redacted")
        self.assertFalse(view.complete)
        foreign_request = AccessRequest(ActorContext(self.actor.actual_principal, self.org_b), "review", "read", ("internal",))
        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(manifest=manifest, request=foreign_request, evidence_constraints=())

    def test_access_context_grants_no_organizational_authority(self):
        self.assertFalse(hasattr(self.request, "approve"))
        self.assertFalse(hasattr(self.request, "authority"))
        self.assertFalse(hasattr(self.request, "delegation"))


if __name__ == "__main__":
    unittest.main()
