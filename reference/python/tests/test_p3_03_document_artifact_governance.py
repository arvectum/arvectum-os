from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.document_artifact_governance import (
    DOCUMENT_SEMANTIC_TYPE,
    ArtifactContent,
    ArtifactState,
    DocumentAdmissionError,
    DocumentRelianceError,
    DocumentVersionCandidate,
    HandlingConstraints,
    admit_document_version,
    resolve_exact_document_reliance,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P303DocumentArtifactGovernanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        principal = Principal(Identity("principal", "owner", "platform"))
        self.actor = ActorContext(principal, self.org)
        self.handling = HandlingConstraints(
            classification="internal",
            purpose="governed-review",
            rights=("internal-use",),
            retention_rule="phase-3-reference",
        )

    def record(self, version: str, predecessor: str | None = None) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=Identity("document", "doc-1", "org-a"),
            version_id=Identity("document-version", version, "org-a"),
            semantic_type=DOCUMENT_SEMANTIC_TYPE,
            schema_version="1",
            organization=self.org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="document/governed-state",
            accountable_owner_id=self.actor.actual_principal.principal_id,
            creation_actor=self.actor,
            created_at=datetime(2026, 8, 8, 12, 0, tzinfo=timezone.utc),
            provenance_refs=(self.actor.actual_principal.principal_id,),
            integrity_metadata=(("representation", "bounded-reference"),),
            payload=(("title", "domain-neutral document"),),
            lifecycle_status="admitted",
            predecessor_version_id=(
                Identity("document-version", predecessor, "org-a") if predecessor else None
            ),
        )

    def artifact(self, value: str, *, role: str = "exchange") -> ArtifactContent:
        return ArtifactContent(
            artifact_id=Identity("artifact", value, "org-a"),
            organization=self.org,
            content_ref=f"content:{value}",
            media_type="application/octet-stream",
            integrity_ref=f"sha256:{value}",
            rendition_role=role,
            handling=self.handling,
            storage_locator=f"memory://{value}",
        )

    def test_document_subject_identity_is_stable_across_immutable_versions(self) -> None:
        v1 = self.record("v1")
        v2 = self.record("v2", predecessor="v1")
        lineage = CanonicalLineage((v1, v2))
        self.assertEqual(v1.subject_id, v2.subject_id)
        self.assertNotEqual(v1.version_id, v2.version_id)
        self.assertEqual(lineage.resolve_version(v1.version_id), v1)
        with self.assertRaises(FrozenInstanceError):
            v1.payload = (("title", "mutated"),)  # type: ignore[misc]

    def test_transient_artifact_is_not_governed_merely_by_existing(self) -> None:
        artifact = self.artifact("a1")
        self.assertIs(artifact.state, ArtifactState.TRANSIENT)
        self.assertIsNotNone(artifact.storage_locator)

    def test_admission_promotes_manifest_artifact_state_without_making_locator_identity(self) -> None:
        record = self.record("v1")
        artifact = self.artifact("a1")
        admitted = admit_document_version(
            DocumentVersionCandidate(record, (artifact,), "exchange")
        )
        governed = admitted.resolve_artifact(artifact.artifact_id)
        self.assertIs(governed.state, ArtifactState.GOVERNED)
        self.assertEqual(governed.artifact_id, artifact.artifact_id)
        self.assertEqual(governed.storage_locator, "memory://a1")
        self.assertNotEqual(governed.artifact_id.value, governed.storage_locator)

    def test_admission_rejects_cross_organization_artifact(self) -> None:
        artifact = ArtifactContent(
            artifact_id=Identity("artifact", "a-other", "org-b"),
            organization=self.other_org,
            content_ref="content:other",
            media_type="application/octet-stream",
            integrity_ref="sha256:other",
            rendition_role="exchange",
            handling=self.handling,
        )
        with self.assertRaises(DocumentAdmissionError):
            admit_document_version(
                DocumentVersionCandidate(self.record("v1"), (artifact,), "exchange")
            )

    def test_derived_artifact_preserves_provenance_and_handling_and_remains_transient(self) -> None:
        source = self.artifact("source", role="authoring")
        derived = source.derive(
            artifact_id=Identity("artifact", "derived", "org-a"),
            content_ref="content:derived",
            media_type="application/pdf",
            integrity_ref="sha256:derived",
            rendition_role="exchange",
            transformation="render-to-pdf",
            storage_locator="memory://derived",
        )
        self.assertEqual(derived.source_artifact_ids, (source.artifact_id,))
        self.assertEqual(derived.transformation, "render-to-pdf")
        self.assertEqual(derived.handling, source.handling)
        self.assertIs(derived.state, ArtifactState.TRANSIENT)

    def test_exact_reliance_pins_document_version_and_artifact_without_head_inference(self) -> None:
        v1 = self.record("v1")
        v2 = self.record("v2", predecessor="v1")
        a1 = self.artifact("a1")
        a2 = self.artifact("a2")
        admitted_v1 = admit_document_version(DocumentVersionCandidate(v1, (a1,), "exchange"))
        admitted_v2 = admit_document_version(DocumentVersionCandidate(v2, (a2,), "exchange"))
        lineage = CanonicalLineage((v1, v2))

        reliance = resolve_exact_document_reliance(
            lineage=lineage,
            admitted_versions=(admitted_v1, admitted_v2),
            document_version_id=v1.version_id,
            artifact_id=a1.artifact_id,
        )
        self.assertEqual(reliance.document_version_id, v1.version_id)
        self.assertEqual(reliance.artifact_id, a1.artifact_id)
        self.assertNotEqual(reliance.document_version_id, lineage.head.version_id)

    def test_exact_reliance_rejects_artifact_from_another_document_version(self) -> None:
        v1 = self.record("v1")
        v2 = self.record("v2", predecessor="v1")
        a1 = self.artifact("a1")
        a2 = self.artifact("a2")
        admitted_v1 = admit_document_version(DocumentVersionCandidate(v1, (a1,), "exchange"))
        admitted_v2 = admit_document_version(DocumentVersionCandidate(v2, (a2,), "exchange"))
        with self.assertRaises(DocumentRelianceError):
            resolve_exact_document_reliance(
                lineage=CanonicalLineage((v1, v2)),
                admitted_versions=(admitted_v1, admitted_v2),
                document_version_id=v1.version_id,
                artifact_id=a2.artifact_id,
            )

    def test_hash_and_storage_locator_do_not_define_document_identity(self) -> None:
        artifact = self.artifact("same-bytes")
        admitted = admit_document_version(
            DocumentVersionCandidate(self.record("v1"), (artifact,), "exchange")
        )
        self.assertNotEqual(admitted.document_id.value, artifact.integrity_ref)
        self.assertNotEqual(admitted.version_id.value, artifact.integrity_ref)
        self.assertNotEqual(admitted.document_id.value, artifact.storage_locator)


if __name__ == "__main__":
    unittest.main()
