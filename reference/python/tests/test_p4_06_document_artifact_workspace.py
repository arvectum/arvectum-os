from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import unittest

import arvectum_os_ref
from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.cross_capability_enforcement import (
    AccessRequest,
    CrossCapabilityEnforcementError,
)
from arvectum_os_ref.document_artifact_experience import (
    DocumentCanonicalState,
    DocumentReferenceBasis,
    DocumentWorkspaceBlockCode,
    DocumentWorkspaceBlockedState,
    DocumentWorkspaceInspection,
    DocumentWorkspaceSourceSet,
    ExactRelianceAvailability,
    inspect_document_workspace,
    render_document_workspace_html,
    resolve_workspace_exact_reliance,
)
from arvectum_os_ref.document_artifact_governance import (
    DOCUMENT_SEMANTIC_TYPE,
    ArtifactContent,
    ArtifactState,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    SubjectNavigationReference,
    WorkspaceDestination,
    navigate_workspace,
    open_workspace_shell,
)


class P406DocumentArtifactWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "operator", "platform"))
        self.other_principal = Principal(Identity("principal", "other-operator", "platform"))
        self.actor = ActorContext(self.principal, self.org)
        self.handling = HandlingConstraints(
            classification="internal",
            purpose="document-review",
            rights=("internal-use", "review"),
            retention_rule="retain-7y",
        )
        self.access_request = AccessRequest(
            actor=self.actor,
            purpose="document-review",
            required_right="review",
            allowed_classifications=("internal",),
        )
        opened = open_workspace_shell(
            self.actor,
            initial_destination=WorkspaceDestination.DOCUMENTS,
        )
        if not hasattr(opened, "organization"):
            self.fail("expected open workspace shell")
        self.workspace = opened

    def record(
        self,
        version: str,
        *,
        predecessor: str | None = None,
        title: str = "Governed document",
        semantic_type: str = DOCUMENT_SEMANTIC_TYPE,
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=Identity("document", "doc-1", "org-a"),
            version_id=Identity("document-version", version, "org-a"),
            semantic_type=semantic_type,
            schema_version="1",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="document/governed-state",
            accountable_owner_id=self.principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 18, 0, tzinfo=timezone.utc),
            provenance_refs=(self.principal.principal_id,),
            integrity_metadata=(("representation", "p4-06-test"),),
            payload=(("title", title),),
            lifecycle_status="admitted",
            predecessor_version_id=(
                Identity("document-version", predecessor, "org-a") if predecessor else None
            ),
        )

    def artifact(
        self,
        value: str,
        *,
        role: str,
        media_type: str = "application/octet-stream",
        storage_locator: str | None = None,
        handling: HandlingConstraints | None = None,
    ) -> ArtifactContent:
        return ArtifactContent(
            artifact_id=Identity("artifact", value, "org-a"),
            organization=self.org,
            content_ref=f"content-ref:{value}-SECRET",
            media_type=media_type,
            integrity_ref=f"sha256:{value}",
            rendition_role=role,
            handling=handling or self.handling,
            storage_locator=storage_locator or f"private://bucket/{value}-SECRET",
        )

    def admitted_version(
        self,
        record: CanonicalRecord,
        *,
        suffix: str,
    ):
        authoring = self.artifact(
            f"{suffix}-source",
            role="authoring",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
        exchange = authoring.derive(
            artifact_id=Identity("artifact", f"{suffix}-pdf", "org-a"),
            content_ref=f"content-ref:{suffix}-pdf-SECRET",
            media_type="application/pdf",
            integrity_ref=f"sha256:{suffix}-pdf",
            rendition_role="exchange",
            transformation="render-to-pdf",
            storage_locator=f"private://bucket/{suffix}-pdf-SECRET",
        )
        return admit_document_version(
            DocumentVersionCandidate(record, (authoring, exchange), "exchange")
        )

    def authorization(
        self,
        *,
        allowed: bool = True,
        principal: Principal | None = None,
        resource_subject_id: Identity | None = None,
        organization: OrganizationScope | None = None,
    ) -> CurrentSourceAuthorization:
        return CurrentSourceAuthorization(
            organization=organization or self.org,
            actor_actual_principal_id=(principal or self.principal).principal_id,
            resource_subject_id=resource_subject_id
            or Identity("document", "doc-1", "org-a"),
            decision_version_id=Identity("authorization-version", "allow-v1", "org-a"),
            allowed=allowed,
        )

    def sources(self, *, include_candidate: bool = True) -> DocumentWorkspaceSourceSet:
        v1 = self.record("v1")
        v2 = self.record("v2", predecessor="v1", title="Governed document v2")
        admitted_v1 = self.admitted_version(v1, suffix="v1")
        admitted_v2 = self.admitted_version(v2, suffix="v2")
        candidates = ()
        if include_candidate:
            candidate_artifact = self.artifact(
                "v3-generated-SECRET-ID",
                role="exchange",
                media_type="application/pdf",
                storage_locator="private://draft/v3-generated-SECRET",
            )
            candidate_record = self.record(
                "v3-candidate",
                predecessor="v2",
                title="Generated working candidate",
            )
            candidates = (
                DocumentVersionCandidate(candidate_record, (candidate_artifact,), "exchange"),
            )
        return DocumentWorkspaceSourceSet(
            lineages=(CanonicalLineage((v1, v2)),),
            admitted_versions=(admitted_v1, admitted_v2),
            working_candidates=candidates,
        )

    def subject_workspace(self):
        return navigate_workspace(
            self.workspace,
            destination=WorkspaceDestination.DOCUMENTS,
            reference=SubjectNavigationReference(
                organization=self.org,
                subject_id=Identity("document", "doc-1", "org-a"),
            ),
        )

    def exact_workspace(self, version: str = "v1"):
        return navigate_workspace(
            self.workspace,
            destination=WorkspaceDestination.DOCUMENTS,
            reference=ExactVersionNavigationReference(
                organization=self.org,
                subject_id=Identity("document", "doc-1", "org-a"),
                version_id=Identity("document-version", version, "org-a"),
            ),
        )

    def inspect_subject(
        self,
        *,
        sources: DocumentWorkspaceSourceSet | None = None,
        access_request: AccessRequest | None = None,
    ):
        return inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=sources or self.sources(),
            source_authorizations=(self.authorization(),),
            access_request=access_request or self.access_request,
        )

    def inspect_exact(
        self,
        version: str = "v1",
        *,
        access_request: AccessRequest | None = None,
    ):
        return inspect_document_workspace(
            workspace=self.exact_workspace(version),
            sources=self.sources(),
            source_authorizations=(self.authorization(),),
            access_request=access_request or self.access_request,
        )

    def test_subject_view_separates_document_version_artifact_integrity_and_locator(self) -> None:
        result = self.inspect_subject()
        self.assertIsInstance(result, DocumentWorkspaceInspection)
        assert isinstance(result, DocumentWorkspaceInspection)
        self.assertEqual(result.document_id.value, "doc-1")
        self.assertEqual(result.displayed_version_id.value, "v2")
        self.assertEqual(result.head_version_id.value, "v2")
        self.assertIs(result.reference_basis, DocumentReferenceBasis.CANONICAL_HEAD)
        self.assertIs(result.canonical_state, DocumentCanonicalState.ADMITTED)
        self.assertEqual({row.artifact_id.value for row in result.artifacts}, {"v2-source", "v2-pdf"})
        self.assertTrue(all(row.storage_locator_present for row in result.artifacts))
        self.assertTrue(all(not row.storage_locator_exposed for row in result.artifacts))
        self.assertTrue(all(row.artifact_id != result.document_id for row in result.artifacts))
        self.assertTrue(all(row.integrity_ref != result.document_id.value for row in result.artifacts))
        self.assertEqual(result.access_purpose, "document-review")
        self.assertEqual(result.required_right, "review")
        self.assertEqual(result.allowed_classifications, ("internal",))

    def test_exact_historical_version_is_preserved_and_not_redirected_to_head(self) -> None:
        result = self.inspect_exact("v1")
        self.assertIsInstance(result, DocumentWorkspaceInspection)
        assert isinstance(result, DocumentWorkspaceInspection)
        self.assertIs(result.reference_basis, DocumentReferenceBasis.EXACT_VERSION)
        self.assertEqual(result.displayed_version_id.value, "v1")
        self.assertEqual(result.head_version_id.value, "v2")
        self.assertEqual({row.artifact_id.value for row in result.artifacts}, {"v1-source", "v1-pdf"})

    def test_head_browsing_cannot_be_used_as_exact_consequential_reliance(self) -> None:
        sources = self.sources()
        result = inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=sources,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        assert isinstance(result, DocumentWorkspaceInspection)
        self.assertTrue(
            all(
                row.exact_reliance is ExactRelianceAvailability.REQUIRES_EXACT_VERSION
                for row in result.artifacts
            )
        )
        with self.assertRaisesRegex(ValueError, "explicit exact Document Version"):
            resolve_workspace_exact_reliance(
                inspection=result,
                sources=sources,
                artifact_id=Identity("artifact", "v2-pdf", "org-a"),
                source_authorizations=(self.authorization(),),
                access_request=self.access_request,
            )

    def test_exact_version_can_delegate_exact_artifact_reliance_to_cap_001(self) -> None:
        sources = self.sources()
        result = inspect_document_workspace(
            workspace=self.exact_workspace("v1"),
            sources=sources,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        assert isinstance(result, DocumentWorkspaceInspection)
        pdf = next(row for row in result.artifacts if row.artifact_id.value == "v1-pdf")
        self.assertIs(pdf.exact_reliance, ExactRelianceAvailability.AVAILABLE)
        reliance = resolve_workspace_exact_reliance(
            inspection=result,
            sources=sources,
            artifact_id=pdf.artifact_id,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertEqual(reliance.document_id.value, "doc-1")
        self.assertEqual(reliance.document_version_id.value, "v1")
        self.assertEqual(reliance.artifact_id.value, "v1-pdf")
        self.assertEqual(reliance.rendition_role, "exchange")

    def test_exact_reliance_rechecks_current_source_authorization(self) -> None:
        sources = self.sources()
        result = inspect_document_workspace(
            workspace=self.exact_workspace("v1"),
            sources=sources,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        assert isinstance(result, DocumentWorkspaceInspection)
        with self.assertRaisesRegex(PermissionError, "source access"):
            resolve_workspace_exact_reliance(
                inspection=result,
                sources=sources,
                artifact_id=Identity("artifact", "v1-pdf", "org-a"),
                source_authorizations=(self.authorization(allowed=False),),
                access_request=self.access_request,
            )

    def test_exact_reliance_rechecks_purpose_right_and_classification(self) -> None:
        sources = self.sources()
        result = inspect_document_workspace(
            workspace=self.exact_workspace("v1"),
            sources=sources,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        assert isinstance(result, DocumentWorkspaceInspection)
        denied_requests = (
            AccessRequest(self.actor, "other-purpose", "review", ("internal",)),
            AccessRequest(self.actor, "document-review", "write", ("internal",)),
            AccessRequest(self.actor, "document-review", "review", ("public",)),
        )
        for request in denied_requests:
            with self.subTest(request=request):
                with self.assertRaises(CrossCapabilityEnforcementError):
                    resolve_workspace_exact_reliance(
                        inspection=result,
                        sources=sources,
                        artifact_id=Identity("artifact", "v1-pdf", "org-a"),
                        source_authorizations=(self.authorization(),),
                        access_request=request,
                    )

    def test_handling_constraints_block_artifact_metadata_when_context_does_not_match(self) -> None:
        denied_requests = (
            AccessRequest(self.actor, "other-purpose", "review", ("internal",)),
            AccessRequest(self.actor, "document-review", "write", ("internal",)),
            AccessRequest(self.actor, "document-review", "review", ("public",)),
        )
        for request in denied_requests:
            with self.subTest(request=request):
                result = self.inspect_subject(access_request=request)
                self.assertIsInstance(result, DocumentWorkspaceBlockedState)
                assert isinstance(result, DocumentWorkspaceBlockedState)
                self.assertIs(result.code, DocumentWorkspaceBlockCode.HANDLING_ACCESS_DENIED)
                html = render_document_workspace_html(result)
                self.assertNotIn("v2-source", html)
                self.assertNotIn("v2-pdf", html)
                self.assertNotIn("sha256:v2", html)

    def test_restricted_artifact_is_omitted_without_metadata_or_count(self) -> None:
        record = self.record("v1")
        allowed = self.artifact("allowed", role="exchange", media_type="application/pdf")
        restricted = self.artifact(
            "restricted-SECRET-ID",
            role="archive",
            handling=HandlingConstraints(
                classification="restricted",
                purpose="document-review",
                rights=("review",),
                retention_rule="retain-10y-SECRET",
            ),
        )
        admitted = admit_document_version(
            DocumentVersionCandidate(record, (allowed, restricted), "exchange")
        )
        sources = DocumentWorkspaceSourceSet(
            lineages=(CanonicalLineage((record,)),),
            admitted_versions=(admitted,),
        )
        result = inspect_document_workspace(
            workspace=self.exact_workspace("v1"),
            sources=sources,
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceInspection)
        assert isinstance(result, DocumentWorkspaceInspection)
        self.assertEqual(tuple(row.artifact_id.value for row in result.artifacts), ("allowed",))
        html = render_document_workspace_html(result)
        self.assertIn("allowed", html)
        self.assertNotIn("restricted-SECRET-ID", html)
        self.assertNotIn("retain-10y-SECRET", html)
        self.assertNotIn("2 artifacts", html.lower())
        self.assertIn("omitted without counts", html)

    def test_access_request_must_match_workspace_actor_and_organization(self) -> None:
        other_actor = ActorContext(self.other_principal, self.org)
        result = self.inspect_subject(
            access_request=AccessRequest(
                other_actor,
                "document-review",
                "review",
                ("internal",),
            )
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.ACCESS_DENIED)
        self.assertNotIn("doc-1", result.status_text)

    def test_working_candidate_is_non_canonical_transient_and_has_no_promotion_action(self) -> None:
        result = self.inspect_subject()
        assert isinstance(result, DocumentWorkspaceInspection)
        self.assertEqual(len(result.working_candidates), 1)
        candidate = result.working_candidates[0]
        self.assertIs(candidate.canonical_state, DocumentCanonicalState.WORKING_CANDIDATE)
        self.assertFalse(candidate.promotion_available)
        self.assertTrue(candidate.contains_artifacts)
        self.assertTrue(candidate.contains_transient_artifacts)
        self.assertFalse(candidate.artifact_metadata_visible)
        self.assertIn("no promotion control", candidate.promotion_status_text)
        html = render_document_workspace_html(result)
        self.assertIn("v3-candidate", html)
        self.assertNotIn("v3-generated-SECRET-ID", html)
        self.assertNotIn("private://draft", html)

    def test_derivation_provenance_and_handling_constraints_are_visible(self) -> None:
        result = self.inspect_exact("v1")
        assert isinstance(result, DocumentWorkspaceInspection)
        pdf = next(row for row in result.artifacts if row.artifact_id.value == "v1-pdf")
        self.assertEqual(tuple(value.value for value in pdf.source_artifact_ids), ("v1-source",))
        self.assertEqual(pdf.transformation, "render-to-pdf")
        self.assertEqual(pdf.handling.classification, "internal")
        self.assertEqual(pdf.handling.purpose, "document-review")
        self.assertEqual(pdf.handling.rights, ("internal-use", "review"))
        self.assertEqual(pdf.handling.retention_rule, "retain-7y")

    def test_renderer_minimizes_content_and_hides_locator_values(self) -> None:
        result = self.inspect_exact("v1")
        html = render_document_workspace_html(result)
        self.assertIn("Document Subject", html)
        self.assertIn("Exact Version", html)
        self.assertIn("v1-pdf", html)
        self.assertIn("sha256:v1-pdf", html)
        self.assertIn("render-to-pdf", html)
        self.assertIn("internal-use", html)
        self.assertIn("retain-7y", html)
        self.assertIn("Access purpose", html)
        self.assertIn("document-review", html)
        self.assertIn("present, value hidden", html)
        self.assertNotIn("private://", html)
        self.assertNotIn("content-ref:", html)
        self.assertNotIn("-SECRET", html)
        self.assertNotIn("<form", html.lower())
        self.assertNotIn("fetch(", html.lower())

    def test_renderer_escapes_governed_values(self) -> None:
        malicious = self.record("v1", title="<script>alert(1)</script>")
        handling = HandlingConstraints(
            classification="internal<unsafe>",
            purpose="review<unsafe>",
            rights=("right<unsafe>",),
            retention_rule="retain<unsafe>",
        )
        artifact = ArtifactContent(
            artifact_id=Identity("artifact", "artifact<unsafe>", "org-a"),
            organization=self.org,
            content_ref="content:unsafe",
            media_type="application/<unsafe>",
            integrity_ref="sha256:<unsafe>",
            rendition_role="exchange<unsafe>",
            handling=handling,
            storage_locator="private://unsafe",
        )
        admitted = admit_document_version(
            DocumentVersionCandidate(malicious, (artifact,), "exchange<unsafe>")
        )
        request = AccessRequest(
            self.actor,
            "review<unsafe>",
            "right<unsafe>",
            ("internal<unsafe>",),
        )
        result = inspect_document_workspace(
            workspace=self.exact_workspace("v1"),
            sources=DocumentWorkspaceSourceSet(
                lineages=(CanonicalLineage((malicious,)),),
                admitted_versions=(admitted,),
            ),
            source_authorizations=(self.authorization(),),
            access_request=request,
        )
        html = render_document_workspace_html(result)
        self.assertNotIn("artifact<unsafe>", html)
        self.assertNotIn("application/<unsafe>", html)
        self.assertNotIn("review<unsafe>", html)
        self.assertIn("artifact&lt;unsafe&gt;", html)
        self.assertIn("application/&lt;unsafe&gt;", html)
        self.assertIn("review&lt;unsafe&gt;", html)

    def test_access_denial_precedes_source_and_exact_version_existence_disclosure(self) -> None:
        result = inspect_document_workspace(
            workspace=self.exact_workspace("does-not-exist"),
            sources=DocumentWorkspaceSourceSet(lineages=(), admitted_versions=()),
            source_authorizations=(self.authorization(allowed=False),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.ACCESS_DENIED)
        self.assertNotIn("does-not-exist", result.status_text)
        html = render_document_workspace_html(result)
        self.assertNotIn("does-not-exist", html)
        self.assertNotIn("doc-1", html)

    def test_authorization_is_actor_and_organization_bound(self) -> None:
        for decision in (
            self.authorization(principal=self.other_principal),
            self.authorization(organization=self.other_org),
        ):
            with self.subTest(decision=decision):
                result = inspect_document_workspace(
                    workspace=self.subject_workspace(),
                    sources=self.sources(),
                    source_authorizations=(decision,),
                    access_request=self.access_request,
                )
                self.assertIsInstance(result, DocumentWorkspaceBlockedState)
                assert isinstance(result, DocumentWorkspaceBlockedState)
                self.assertIs(result.code, DocumentWorkspaceBlockCode.ACCESS_DENIED)

    def test_unknown_exact_version_is_disclosed_only_after_current_allow(self) -> None:
        result = inspect_document_workspace(
            workspace=self.exact_workspace("does-not-exist"),
            sources=self.sources(),
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.VERSION_UNAVAILABLE)

    def test_duplicate_current_authorization_fails_closed(self) -> None:
        decision = self.authorization()
        result = inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=self.sources(),
            source_authorizations=(decision, decision),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.ACCESS_DENIED)

    def test_source_owned_organization_controls_resolution_not_identifier_scope(self) -> None:
        v1 = self.record("v1")
        foreign_record = CanonicalRecord(
            subject_id=v1.subject_id,
            version_id=v1.version_id,
            semantic_type=v1.semantic_type,
            schema_version=v1.schema_version,
            organization=self.other_org,
            authority_mode=v1.authority_mode,
            authority_scope=v1.authority_scope,
            accountable_owner_id=self.other_principal.principal_id,
            creation_actor=ActorContext(self.other_principal, self.other_org),
            created_at=v1.created_at,
            provenance_refs=(self.other_principal.principal_id,),
            integrity_metadata=v1.integrity_metadata,
            payload=v1.payload,
            lifecycle_status=v1.lifecycle_status,
        )
        foreign_artifact = ArtifactContent(
            artifact_id=Identity("artifact", "foreign", "org-b"),
            organization=self.other_org,
            content_ref="content:foreign",
            media_type="application/pdf",
            integrity_ref="sha256:foreign",
            rendition_role="exchange",
            handling=self.handling,
        )
        admitted_foreign = admit_document_version(
            DocumentVersionCandidate(foreign_record, (foreign_artifact,), "exchange")
        )
        result = inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=DocumentWorkspaceSourceSet(
                lineages=(CanonicalLineage((foreign_record,)),),
                admitted_versions=(admitted_foreign,),
            ),
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.SOURCE_UNAVAILABLE)

    def test_admitted_manifest_is_required_and_not_reconstructed_from_locator(self) -> None:
        sources = self.sources(include_candidate=False)
        result = inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=DocumentWorkspaceSourceSet(
                lineages=sources.lineages,
                admitted_versions=(),
            ),
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.ADMISSION_EVIDENCE_UNAVAILABLE)

    def test_non_document_source_is_not_presented_as_document(self) -> None:
        record = self.record("v1", semantic_type="platform.not-document")
        result = inspect_document_workspace(
            workspace=self.subject_workspace(),
            sources=DocumentWorkspaceSourceSet(
                lineages=(CanonicalLineage((record,)),),
                admitted_versions=(),
            ),
            source_authorizations=(self.authorization(),),
            access_request=self.access_request,
        )
        self.assertIsInstance(result, DocumentWorkspaceBlockedState)
        assert isinstance(result, DocumentWorkspaceBlockedState)
        self.assertIs(result.code, DocumentWorkspaceBlockCode.SOURCE_UNAVAILABLE)

    def test_p4_06_module_remains_internal_and_technology_neutral(self) -> None:
        self.assertFalse(hasattr(arvectum_os_ref, "inspect_document_workspace"))
        module_path = (
            Path(__file__).parents[1]
            / "arvectum_os_ref"
            / "document_artifact_experience.py"
        )
        source = module_path.read_text(encoding="utf-8").lower()
        prohibited_imports = (
            "import fastapi",
            "import flask",
            "import django",
            "import requests",
            "import httpx",
            "import sqlalchemy",
            "import boto",
            "import psycopg",
        )
        for token in prohibited_imports:
            with self.subTest(token=token):
                self.assertNotIn(token, source)
        self.assertNotIn("def promote", source)
        self.assertNotIn("def approve", source)
        self.assertNotIn("def upload", source)
        self.assertNotIn("def download", source)


if __name__ == "__main__":
    unittest.main()
