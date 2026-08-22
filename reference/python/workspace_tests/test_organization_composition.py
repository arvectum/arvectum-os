from __future__ import annotations

import unittest
from types import SimpleNamespace

from arvectum_os_ref.identity import Identity
from workspace_app.access import AccessContext
from workspace_app.attention import AttentionProjectionError, ProjectionFreshness
from workspace_app.discovery import DiscoveryError, DiscoveryFreshness
from workspace_app.organization import RuntimeOrganizationCompositionProvider
from workspace_app.products import ProductCompositionError


ACCESS = AccessContext(
    organization=Identity("organization", "arvectum", "test"),
    actor=Identity("actor", "owner", "test"),
    principal_kind="human",
    credential_id="cred",
    grant_id="grant",
)


class Products:
    def project(self, access: AccessContext):
        self.access = access
        return SimpleNamespace(products=(SimpleNamespace(
            product_id="tender-operator",
            label="Tender Operator",
            summary="Verified retained product context.",
            contour="P7.07",
            source_authority="ЕИС — External Reference",
            status="verified-retained-context",
            technical_refs=("evidence",),
        ),))


class Discovery:
    def search(self, access: AccessContext, *, query: str = "", kind=None):
        self.access = access
        self.kind = kind
        return SimpleNamespace(
            health=SimpleNamespace(state=DiscoveryFreshness.FRESH),
            results=(SimpleNamespace(
                object_id="a" * 20,
                title="Knowledge — governed source",
                summary="Knowledge. Governed context is available.",
                open_href="/objects/" + "a" * 20,
                source_label="Arvectum OS governed state",
                authority_mode="Native",
                state_label="validated",
                knowledge_role="Knowledge Candidate — not validated Knowledge",
                semantic_role="Knowledge Candidate",
            ),),
        )

    def inspect(self, access: AccessContext, object_id: str):  # pragma: no cover - protocol completeness
        raise NotImplementedError


class Attention:
    def project(self, access: AccessContext):
        self.access = access
        return SimpleNamespace(
            health=SimpleNamespace(state=ProjectionFreshness.FRESH),
            items=(SimpleNamespace(
                attention_id="b" * 20,
                title="Decision evidence is needed",
                reason="A governed gate remains waiting.",
                open_href="/my-work?focus=" + "b" * 20,
                source_label="Governed source",
                group=SimpleNamespace(value="decision-required"),
                urgency=SimpleNamespace(value="high"),
                technical_evidence_available=True,
            ),),
        )


class FailingProducts:
    def project(self, access: AccessContext):
        raise ProductCompositionError("protected product source unavailable")


class FailingDiscovery(Discovery):
    def search(self, access: AccessContext, *, query: str = "", kind=None):
        raise DiscoveryError("protected discovery source unavailable")


class FailingAttention:
    def project(self, access: AccessContext):
        raise AttentionProjectionError("protected attention source unavailable")


class OrganizationCompositionTests(unittest.TestCase):
    def test_composes_existing_authorized_sources_without_creating_project_authority(self) -> None:
        projection = RuntimeOrganizationCompositionProvider(Products(), Discovery(), Attention()).project(ACCESS).to_payload()
        self.assertEqual(projection["schema"], "arvectum.workspace.organization-composition/1")
        self.assertFalse(projection["projection"]["canonical_authority"])
        self.assertFalse(projection["projection"]["company_semantics_promoted_to_kernel"])
        self.assertFalse(projection["projection"]["project_lenses_are_canonical_records"])
        self.assertFalse(projection["scope"]["cross_organization_aggregation"])
        lanes = {lane["id"]: lane for lane in projection["lanes"]}
        self.assertEqual(set(lanes), {"products", "projects", "knowledge", "work"})
        self.assertEqual(lanes["products"]["items"][0]["href"], "/products/tender-operator")
        project = lanes["projects"]["items"][0]
        self.assertEqual(project["kind"], "project-lens")
        self.assertFalse(project["canonical_project_record"])
        self.assertIn("not a canonical Project record", project["summary"])
        self.assertEqual(lanes["knowledge"]["items"][0]["href"], "/objects/" + "a" * 20)
        self.assertEqual(lanes["knowledge"]["items"][0]["semantic_note"], "Knowledge Candidate — not validated Knowledge")
        self.assertEqual(lanes["work"]["items"][0]["href"], "/my-work?focus=" + "b" * 20)
        self.assertFalse(lanes["work"]["items"][0]["authority_provided"])

    def test_fails_closed_per_lane_without_inventing_company_state(self) -> None:
        projection = RuntimeOrganizationCompositionProvider(
            FailingProducts(), FailingDiscovery(), FailingAttention()
        ).project(ACCESS).to_payload()
        self.assertEqual(projection["health"]["state"], "degraded")
        lanes = {lane["id"]: lane for lane in projection["lanes"]}
        self.assertEqual(lanes["products"]["state"], "unavailable")
        self.assertEqual(lanes["projects"]["state"], "unavailable")
        self.assertEqual(lanes["knowledge"]["state"], "unavailable")
        self.assertEqual(lanes["work"]["state"], "unavailable")
        self.assertTrue(all(not lane["items"] for lane in lanes.values()))
        self.assertNotIn("protected product source unavailable", str(projection))
        self.assertNotIn("protected discovery source unavailable", str(projection))
        self.assertNotIn("protected attention source unavailable", str(projection))


if __name__ == "__main__":
    unittest.main()
