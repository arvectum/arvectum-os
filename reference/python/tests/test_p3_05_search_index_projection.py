from __future__ import annotations

from datetime import datetime, timezone
import unittest

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.search_index_projection import (
    DiscoveryConstraints,
    GovernedSearchSource,
    ProjectionBuildError,
    ProjectionQueryError,
    ProjectionResolutionError,
    ProjectionSourceState,
    assess_projection_entry,
    inspect_projection,
    query_projection,
    rebuild_projection,
    resolve_search_hit_for_reliance,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal


class P305SearchIndexProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.other_org = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.actor = ActorContext(
            Principal(Identity("principal", "owner", "platform")), self.org
        )
        self.other_actor = ActorContext(
            Principal(Identity("principal", "owner-b", "platform")), self.other_org
        )
        self.internal = DiscoveryConstraints(
            "decision-support", "internal", ("internal-use",), "retain-governed"
        )
        self.confidential = DiscoveryConstraints(
            "decision-support", "confidential", ("internal-use",), "retain-governed"
        )

    def record(
        self,
        *,
        subject: str,
        version: str,
        semantic_type: str,
        organization: OrganizationScope | None = None,
    ) -> CanonicalRecord:
        org = organization or self.org
        actor = self.actor if org == self.org else self.other_actor
        return CanonicalRecord(
            subject_id=Identity("subject", subject, org.organization_id.value),
            version_id=Identity("version", f"{subject}-{version}", org.organization_id.value),
            semantic_type=semantic_type,
            schema_version="1",
            organization=org,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope=f"{semantic_type}/state",
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=datetime(2026, 8, 8, 14, 0, tzinfo=timezone.utc),
            provenance_refs=(Identity("evidence", f"e-{subject}-{version}", org.organization_id.value),),
            integrity_metadata=(("representation", "bounded-reference"),),
            payload=(("label", f"{subject} {version}"),),
            lifecycle_status="governed",
        )

    def source(
        self,
        *,
        subject: str,
        version: str,
        semantic_type: str,
        text: str,
        constraints: DiscoveryConstraints | None = None,
        organization: OrganizationScope | None = None,
    ) -> GovernedSearchSource:
        return GovernedSearchSource(
            self.record(
                subject=subject,
                version=version,
                semantic_type=semantic_type,
                organization=organization,
            ),
            text,
            constraints or self.internal,
        )

    def test_projection_is_derived_and_has_no_canonical_authority_fields(self) -> None:
        source = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="bounded searchable document",
        )
        entry = rebuild_projection(sources=(source,)).entries[0]
        self.assertEqual(entry.source_version_id, source.version_id)
        self.assertFalse(hasattr(entry, "authority_mode"))
        self.assertFalse(hasattr(entry, "accountable_owner_id"))

    def test_query_returns_exact_versions_across_distinct_governed_source_types(self) -> None:
        document = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="shared discovery phrase in a document",
        )
        knowledge = self.source(
            subject="knowledge-1",
            version="v7",
            semantic_type="platform.knowledge",
            text="shared discovery phrase in validated knowledge",
        )
        sources = (document, knowledge)
        projection = rebuild_projection(sources=sources)

        hits = query_projection(
            projection=projection,
            current_sources=sources,
            query_text="discovery phrase",
            organization=self.org,
            purpose="decision-support",
            required_right="internal-use",
            allowed_classifications=("internal",),
        )

        self.assertEqual(
            {(hit.source_subject_id, hit.source_version_id) for hit in hits},
            {
                (document.subject_id, document.version_id),
                (knowledge.subject_id, knowledge.version_id),
            },
        )
        self.assertTrue(all(hit.state is ProjectionSourceState.CURRENT for hit in hits))

    def test_query_filters_organization_purpose_right_and_classification(self) -> None:
        allowed = self.source(
            subject="doc-allowed",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        classified = self.source(
            subject="doc-classified",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
            constraints=self.confidential,
        )
        other_org = self.source(
            subject="doc-other",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
            organization=self.other_org,
        )
        sources = (allowed, classified, other_org)
        projection = rebuild_projection(sources=sources)

        hits = query_projection(
            projection=projection,
            current_sources=sources,
            query_text="needle",
            organization=self.org,
            purpose="decision-support",
            required_right="internal-use",
            allowed_classifications=("internal",),
        )
        self.assertEqual(tuple(hit.source_subject_id for hit in hits), (allowed.subject_id,))

        self.assertEqual(
            query_projection(
                projection=projection,
                current_sources=sources,
                query_text="needle",
                organization=self.org,
                purpose="other-purpose",
                required_right="internal-use",
                allowed_classifications=("internal",),
            ),
            (),
        )
        self.assertEqual(
            query_projection(
                projection=projection,
                current_sources=sources,
                query_text="needle",
                organization=self.org,
                purpose="decision-support",
                required_right="export",
                allowed_classifications=("internal",),
            ),
            (),
        )

    def test_query_rechecks_current_constraints_without_rebuild(self) -> None:
        initial = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        projection = rebuild_projection(sources=(initial,))
        restricted = GovernedSearchSource(
            initial.canonical_record,
            initial.searchable_text,
            DiscoveryConstraints(
                "decision-support", "confidential", ("restricted-use",), "retain-governed"
            ),
        )

        self.assertEqual(
            query_projection(
                projection=projection,
                current_sources=(restricted,),
                query_text="needle",
                organization=self.org,
                purpose="decision-support",
                required_right="internal-use",
                allowed_classifications=("internal",),
            ),
            (),
        )

    def test_diagnostics_distinguish_current_stale_missing_and_ambiguous(self) -> None:
        projected = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        entry = rebuild_projection(sources=(projected,)).entries[0]
        newer = self.source(
            subject="doc-1",
            version="v2",
            semantic_type="platform.document",
            text="needle newer governed source",
        )

        self.assertIs(
            assess_projection_entry(entry=entry, current_sources=(projected,)),
            ProjectionSourceState.CURRENT,
        )
        self.assertIs(
            assess_projection_entry(entry=entry, current_sources=(newer,)),
            ProjectionSourceState.STALE,
        )
        self.assertIs(
            assess_projection_entry(entry=entry, current_sources=()),
            ProjectionSourceState.MISSING,
        )
        self.assertIs(
            assess_projection_entry(entry=entry, current_sources=(projected, newer)),
            ProjectionSourceState.AMBIGUOUS,
        )

        diagnostic = inspect_projection(
            projection=rebuild_projection(sources=(projected,)),
            current_sources=(newer,),
        )[0]
        self.assertEqual(diagnostic.source_version_id, projected.version_id)
        self.assertIs(diagnostic.state, ProjectionSourceState.STALE)

    def test_stale_missing_and_ambiguous_entries_fail_closed_for_query(self) -> None:
        projected = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        projection = rebuild_projection(sources=(projected,))
        newer = self.source(
            subject="doc-1",
            version="v2",
            semantic_type="platform.document",
            text="needle newer governed source",
        )

        for current_sources in ((newer,), (), (projected, newer)):
            with self.subTest(current_sources=len(current_sources)):
                self.assertEqual(
                    query_projection(
                        projection=projection,
                        current_sources=current_sources,
                        query_text="needle",
                        organization=self.org,
                        purpose="decision-support",
                        required_right="internal-use",
                        allowed_classifications=("internal",),
                    ),
                    (),
                )

    def test_hit_resolution_requires_separate_source_access_and_exact_current_version(self) -> None:
        source = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        projection = rebuild_projection(sources=(source,))
        hit = query_projection(
            projection=projection,
            current_sources=(source,),
            query_text="needle",
            organization=self.org,
            purpose="decision-support",
            required_right="internal-use",
            allowed_classifications=("internal",),
        )[0]

        with self.assertRaises(ProjectionResolutionError):
            resolve_search_hit_for_reliance(
                hit=hit,
                current_sources=(source,),
                organization=self.org,
                source_access_authorized=False,
            )

        resolved = resolve_search_hit_for_reliance(
            hit=hit,
            current_sources=(source,),
            organization=self.org,
            source_access_authorized=True,
        )
        self.assertEqual(resolved.version_id, hit.source_version_id)

        newer = self.source(
            subject="doc-1",
            version="v2",
            semantic_type="platform.document",
            text="needle newer governed source",
        )
        with self.assertRaises(ProjectionResolutionError):
            resolve_search_hit_for_reliance(
                hit=hit,
                current_sources=(newer,),
                organization=self.org,
                source_access_authorized=True,
            )

    def test_rebuild_replaces_disposable_stale_state_without_authority_migration(self) -> None:
        v1 = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle old representation",
        )
        v2 = self.source(
            subject="doc-1",
            version="v2",
            semantic_type="platform.document",
            text="needle current representation",
        )
        old_projection = rebuild_projection(sources=(v1,))
        self.assertIs(
            inspect_projection(projection=old_projection, current_sources=(v2,))[0].state,
            ProjectionSourceState.STALE,
        )

        rebuilt = rebuild_projection(sources=(v2,))
        hit = query_projection(
            projection=rebuilt,
            current_sources=(v2,),
            query_text="needle",
            organization=self.org,
            purpose="decision-support",
            required_right="internal-use",
            allowed_classifications=("internal",),
        )[0]
        self.assertEqual(hit.source_version_id, v2.version_id)
        self.assertNotEqual(hit.source_version_id, v1.version_id)

    def test_ambiguous_rebuild_and_missing_organization_context_fail_closed(self) -> None:
        v1 = self.source(
            subject="doc-1",
            version="v1",
            semantic_type="platform.document",
            text="needle governed source",
        )
        v2 = self.source(
            subject="doc-1",
            version="v2",
            semantic_type="platform.document",
            text="needle governed source",
        )
        with self.assertRaises(ProjectionBuildError):
            rebuild_projection(sources=(v1, v2))

        projection = rebuild_projection(sources=(v1,))
        with self.assertRaises(ProjectionQueryError):
            query_projection(
                projection=projection,
                current_sources=(v1,),
                query_text="needle",
                organization=None,  # type: ignore[arg-type]
                purpose="decision-support",
                required_right="internal-use",
                allowed_classifications=("internal",),
            )


if __name__ == "__main__":
    unittest.main()
