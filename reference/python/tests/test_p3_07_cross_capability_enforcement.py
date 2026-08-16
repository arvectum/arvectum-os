from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
    reconstruct_audit_for_access,
    resolve_document_for_access,
    resolve_search_hit_for_access,
    retrieve_knowledge_for_access,
    search_for_access,
)
from arvectum_os_ref.document_artifact_governance import (
    ArtifactContent,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.event_provenance import ReconstructionManifest
from arvectum_os_ref.execution import GovernedVersionPin
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.memory_knowledge_governance import KnowledgeConstraints, ValidatedKnowledge
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    rebuild_projection,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P307CrossCapabilityEnforcementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org_a = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.actor = ActorContext(Principal(self._id("principal", "alice")), self.org_a)
        self.request = AccessRequest(self.actor, "review", "read", ("internal",))

    def _id(self, namespace: str, value: str, scope: str = "org-a") -> Identity:
        return Identity(namespace, value, scope)

    def _record(
        self,
        *,
        subject: str,
        version: str,
        semantic_type: str,
        organization=None,
        payload=(),
    ):
        organization = organization or self.org_a
        scope = organization.organization_id.value
        creator = ActorContext(Principal(self._id("principal", "creator", scope)), organization)
        return CanonicalRecord(
            subject_id=self._id("subject", subject, scope),
            version_id=self._id("version", version, scope),
            semantic_type=semantic_type,
            schema_version="1",
            organization=organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/state",
            accountable_owner_id=self._id("principal", "owner", scope),
            creation_actor=creator,
            created_at=datetime(2026, 8, 8, tzinfo=timezone.utc),
            provenance_refs=(creator.actual_principal.principal_id,),
            integrity_metadata=(("representation", "p3.07-test"),),
            payload=payload,
            lifecycle_status="Retained",
        )

    def _document(
        self,
        organization=None,
        *,
        purpose="review",
        rights=("read",),
        classification="internal",
    ):
        organization = organization or self.org_a
        record = self._record(
            subject="doc",
            version="doc-v1",
            semantic_type="platform.document",
            organization=organization,
        )
        artifact = ArtifactContent(
            self._id("artifact", "a1", organization.organization_id.value),
            organization,
            "content",
            "text/plain",
            "sha256:x",
            "source",
            HandlingConstraints(classification, purpose, rights, "retain"),
        )
        return (
            admit_document_version(
                candidate=DocumentVersionCandidate(record, (artifact,), "source")
            ),
            artifact,
        )

    def _pin(self, role: str) -> GovernedVersionPin:
        return GovernedVersionPin(
            self._id(f"{role}-subject", role),
            self._id(f"{role}-version", f"{role}-v1"),
            f"example.{role}",
            f"{role}/state",
            "Retained",
        )

    def _reconstruction_fixture(
        self,
    ) -> tuple[ReconstructionManifest, tuple[GovernedVersionPin, ...]]:
        workflow, material, execution, result, event = (
            self._pin(role)
            for role in ("workflow", "material", "execution", "result", "event")
        )
        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.org_a,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("example.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=tuple(
                dict.fromkeys(
                    (
                        self.actor.actual_principal.principal_id,
                        execution_subject,
                        workflow.subject_id,
                        workflow.version_id,
                        material.subject_id,
                        material.version_id,
                        execution.subject_id,
                        execution.version_id,
                        result.subject_id,
                        result.version_id,
                        event.subject_id,
                        event.version_id,
                    )
                )
            ),
        )
        return manifest, (workflow, material, execution, result, event)

    def test_cap001_denies_cross_organization_and_rights_mismatch(self):
        foreign, artifact = self._document(self.org_b)
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_document_for_access(
                admitted=foreign,
                artifact_id=artifact.artifact_id,
                request=self.request,
            )
        local, artifact = self._document(rights=("write",))
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_document_for_access(
                admitted=local,
                artifact_id=artifact.artifact_id,
                request=self.request,
            )

    def test_cap001_allows_only_matching_current_context(self):
        local, artifact = self._document()
        self.assertEqual(
            resolve_document_for_access(
                admitted=local,
                artifact_id=artifact.artifact_id,
                request=self.request,
            ).document_version_id,
            local.version_id,
        )

    def test_cap002_filters_current_governance_context(self):
        eligible = ValidatedKnowledge(
            self._record(
                subject="k1",
                version="k1-v1",
                semantic_type="platform.knowledge",
                payload=(("proposition", "eligible"),),
            ),
            (self._id("evidence", "e1"),),
            KnowledgeConstraints("review", "internal", ("read",), "Current"),
            "valid",
            self._id("approval", "a1"),
        )
        denied = ValidatedKnowledge(
            self._record(
                subject="k2",
                version="k2-v1",
                semantic_type="platform.knowledge",
            ),
            (self._id("evidence", "e2"),),
            KnowledgeConstraints("train", "internal", ("read",), "Current"),
            "valid",
            self._id("approval", "a2"),
        )
        self.assertEqual(
            tuple(
                hit.source_version_id
                for hit in retrieve_knowledge_for_access(
                    knowledge=(eligible, denied),
                    request=self.request,
                )
            ),
            (eligible.version_id,),
        )

    def test_cap003_discovery_and_source_access_use_same_context(self):
        source = GovernedSearchSource(
            self._record(
                subject="s1",
                version="s1-v1",
                semantic_type="platform.knowledge",
            ),
            "needle",
            DiscoveryConstraints("review", "internal", ("read",), "retain"),
        )
        projection = rebuild_projection(sources=(source,))
        hits = search_for_access(
            projection=projection,
            current_sources=(source,),
            query_text="needle",
            request=self.request,
        )
        self.assertEqual(len(hits), 1)
        self.assertEqual(
            resolve_search_hit_for_access(
                hit=hits[0],
                current_sources=(source,),
                request=self.request,
            ).version_id,
            source.version_id,
        )
        denied = AccessRequest(self.actor, "review", "export", ("internal",))
        self.assertEqual(
            search_for_access(
                projection=projection,
                current_sources=(source,),
                query_text="needle",
                request=denied,
            ),
            (),
        )
        with self.assertRaises(CrossCapabilityEnforcementError):
            resolve_search_hit_for_access(
                hit=hits[0],
                current_sources=(source,),
                request=denied,
            )

    def test_cap004_redacts_disallowed_evidence_and_denies_foreign_organization(self):
        manifest, pins = self._reconstruction_fixture()
        workflow, material, execution, result, event = pins
        constraints = tuple(
            (pin.version_id, "review", ("read",), "internal")
            for pin in (workflow, material, execution, event)
        ) + ((result.version_id, "review", ("export",), "internal"),)
        view = reconstruct_audit_for_access(
            manifest=manifest,
            request=self.request,
            evidence_constraints=constraints,
        )
        states = {item.version_id: item.availability.value for item in view.evidence}
        self.assertEqual(states[workflow.version_id], "Available")
        self.assertEqual(states[result.version_id], "Redacted")
        self.assertFalse(view.complete)

        foreign_request = AccessRequest(
            ActorContext(self.actor.actual_principal, self.org_b),
            "review",
            "read",
            ("internal",),
        )
        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=foreign_request,
                evidence_constraints=constraints,
            )

    def test_cap004_missing_or_unknown_evidence_constraints_fail_closed(self):
        manifest, pins = self._reconstruction_fixture()
        complete = tuple(
            (pin.version_id, "review", ("read",), "internal") for pin in pins
        )

        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=self.request,
                evidence_constraints=complete[:-1],
            )

        unknown = self._id("unknown-version", "outside-reconstruction")
        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=self.request,
                evidence_constraints=complete
                + ((unknown, "review", ("read",), "internal"),),
            )

    def test_cap004_rejects_malformed_evidence_constraints(self):
        manifest, pins = self._reconstruction_fixture()
        complete = tuple(
            (pin.version_id, "review", ("read",), "internal") for pin in pins
        )

        malformed_rights = (
            (pins[0].version_id, "review", "read", "internal"),
            *complete[1:],
        )
        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=self.request,
                evidence_constraints=malformed_rights,
            )

        malformed_shape = (
            (pins[0].version_id, "review", ("read",)),
            *complete[1:],
        )
        with self.assertRaises(CrossCapabilityEnforcementError):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=self.request,
                evidence_constraints=malformed_shape,
            )

    def test_access_context_grants_no_organizational_authority(self):
        self.assertFalse(hasattr(self.request, "approve"))
        self.assertFalse(hasattr(self.request, "authority"))
        self.assertFalse(hasattr(self.request, "delegation"))

    def test_cap004_accepts_identity_preserving_admission_overlap(self):
        # Build manifest with material-input/result overlap (same pin)
        workflow, material, execution, _, event = (
            self._pin(role)
            for role in ("workflow", "material", "execution", "result", "event")
        )
        # REUSED PIN: material is both input and result
        result = material

        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.org_a,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(result,),
            events=(event,),
            event_types=(("example.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=tuple(dict.fromkeys((
                self.actor.actual_principal.principal_id, execution_subject,
                workflow.subject_id, workflow.version_id,
                material.subject_id, material.version_id,
                execution.subject_id, execution.version_id,
                event.subject_id, event.version_id,
            ))),
        )

        # Access constraints: ONE row for the shared version identity
        constraints = tuple(
            (pin.version_id, "review", ("read",), "internal")
            for pin in (workflow, material, execution, event)
        )

        view = reconstruct_audit_for_access(
            manifest=manifest,
            request=self.request,
            evidence_constraints=constraints,
        )
        self.assertTrue(view.complete)

        # Verify two role entries for one version ID
        matches = [item for item in view.evidence if item.version_id == material.version_id]
        self.assertEqual(len(matches), 2)
        roles = {item.role for item in matches}
        self.assertEqual(roles, {"material-input", "result"})

    def test_cap004_rejects_ambiguous_reused_version_identity_with_conflicting_pins(self):
        workflow, material, execution, _, event = (
            self._pin(role)
            for role in ("workflow", "material", "execution", "result", "event")
        )
        # CONFLICTING PIN: same version_id, different subject_id
        conflicting_result = GovernedVersionPin(
            self._id("subject", "conflicting"),
            material.version_id,
            material.semantic_type,
            material.authority_scope,
            material.lifecycle_status,
        )

        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.org_a,
            execution_subject_id=execution_subject,
            initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review",
            workflow=workflow,
            material_inputs=(material,),
            gate_decisions=(),
            execution_versions=(execution,),
            results=(conflicting_result,),
            events=(event,),
            event_types=(("example.event", "1"),),
            correlation_refs=(execution_subject,),
            causation_refs=(execution.version_id,),
            provenance_refs=tuple(dict.fromkeys((
                self.actor.actual_principal.principal_id, execution_subject,
                workflow.subject_id, workflow.version_id,
                material.subject_id, material.version_id,
                conflicting_result.subject_id,
                execution.subject_id, execution.version_id,
                event.subject_id, event.version_id,
            ))),
        )

        constraints = tuple(
            (pin.version_id, "review", ("read",), "internal")
            for pin in (workflow, material, execution, event)
        )

        with self.assertRaisesRegex(CrossCapabilityEnforcementError, "ambiguous reused Version Identity"):
            reconstruct_audit_for_access(
                manifest=manifest,
                request=self.request,
                evidence_constraints=constraints,
            )

    def test_cap004_duplicate_shared_version_constraint_fails_closed(self):
        # Overlap manifest
        workflow, material, execution, _, event = (self._pin(role) for role in ("workflow", "material", "execution", "result", "event"))
        result = material
        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.org_a, execution_subject_id=execution_subject, initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review", workflow=workflow, material_inputs=(material,), gate_decisions=(), execution_versions=(execution,),
            results=(result,), events=(event,), event_types=(("example.event", "1"),), correlation_refs=(execution_subject,), causation_refs=(execution.version_id,),
            provenance_refs=tuple(dict.fromkeys((self.actor.actual_principal.principal_id, execution_subject, workflow.subject_id, workflow.version_id, material.subject_id, material.version_id, execution.version_id, event.subject_id, event.version_id))),
        )
        # Correct set
        valid_constraints = tuple((pin.version_id, "review", ("read",), "internal") for pin in (workflow, material, execution, event))
        # Add DUPLICATE row for the shared version ID
        duplicate = (material.version_id, "review", ("read",), "internal")
        with self.assertRaisesRegex(CrossCapabilityEnforcementError, "evidence constraints must be unique by Version Identity"):
            reconstruct_audit_for_access(manifest=manifest, request=self.request, evidence_constraints=valid_constraints + (duplicate,))

    def test_cap004_missing_shared_version_constraint_fails_closed(self):
        workflow, material, execution, _, event = (self._pin(role) for role in ("workflow", "material", "execution", "result", "event"))
        result = material
        execution_subject = self._id("execution-subject", "execution")
        manifest = ReconstructionManifest(
            organization=self.org_a, execution_subject_id=execution_subject, initiating_actor_id=self.actor.actual_principal.principal_id,
            operation_name="review", workflow=workflow, material_inputs=(material,), gate_decisions=(), execution_versions=(execution,),
            results=(result,), events=(event,), event_types=(("example.event", "1"),), correlation_refs=(execution_subject,), causation_refs=(execution.version_id,),
            provenance_refs=tuple(dict.fromkeys((self.actor.actual_principal.principal_id, execution_subject, workflow.subject_id, workflow.version_id, material.subject_id, material.version_id, execution.version_id, event.subject_id, event.version_id))),
        )
        # Missing the shared version constraint
        incomplete = tuple((pin.version_id, "review", ("read",), "internal") for pin in (workflow, execution, event))
        with self.assertRaisesRegex(CrossCapabilityEnforcementError, "evidence constraints must cover every governed reconstruction Version Identity exactly once"):
            reconstruct_audit_for_access(manifest=manifest, request=self.request, evidence_constraints=incomplete)


if __name__ == "__main__":
    unittest.main()
