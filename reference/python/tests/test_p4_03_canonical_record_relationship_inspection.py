import ast
import unittest
from dataclasses import replace
from datetime import datetime
from pathlib import Path

from arvectum_os_ref.canonical import AuthorityMode, CanonicalRecord
from arvectum_os_ref.canonical_inspection import (
    CanonicalInspectionBlockedState,
    CanonicalRecordInspection,
    CurrentSourceAuthorization,
    EffectiveResolutionStatus,
    GovernedInspectionSourceSet,
    InspectionBlockCode,
    InspectionObjectKind,
    InspectionReferenceBasis,
    RelationshipInspection,
    SourceValidationState,
    inspect_current_workspace_reference,
    render_canonical_inspection_html,
)
from arvectum_os_ref.canonical_lineage import CanonicalLineage
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.relationships import (
    EndpointReferenceRole,
    RelationshipEndpoint,
    RelationshipTypeReference,
    TraversalDirection,
    TypedRelationshipLineage,
    create_typed_relationship,
    version_typed_relationship,
)
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


class P403CanonicalRecordRelationshipInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org_a = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.other_principal = Principal(Identity("principal", "operator-2", "platform"))
        self.actor_a = ActorContext(self.principal, self.org_a)
        self.actor_b = ActorContext(self.principal, self.org_b)
        self.subject_id = Identity("subject", "subject-1", "org-a")
        self.v1_id = Identity("canonical-version", "subject-1-v1", "org-a")
        self.v2_id = Identity("canonical-version", "subject-1-v2", "org-a")
        self.effective_at = datetime.fromisoformat("2026-08-08T12:00:00+00:00")

        self.v1 = self._record(
            organization=self.org_a,
            actor=self.actor_a,
            subject_id=self.subject_id,
            version_id=self.v1_id,
            predecessor_version_id=None,
            created_at="2026-07-01T08:00:00+00:00",
            effective_from="2026-07-01T00:00:00+00:00",
            effective_until="2026-09-01T00:00:00+00:00",
            lifecycle_status="Established",
            payload=(("label", "historical state"),),
        )
        self.v2 = self._record(
            organization=self.org_a,
            actor=self.actor_a,
            subject_id=self.subject_id,
            version_id=self.v2_id,
            predecessor_version_id=self.v1_id,
            created_at="2026-08-07T08:00:00+00:00",
            effective_from="2026-09-01T00:00:00+00:00",
            effective_until=None,
            lifecycle_status="Established",
            payload=(("label", "future-effective head"),),
        )
        self.lineage = CanonicalLineage((self.v1, self.v2))

    def _record(
        self,
        *,
        organization: OrganizationScope,
        actor: ActorContext,
        subject_id: Identity,
        version_id: Identity,
        predecessor_version_id: Identity | None,
        created_at: str,
        effective_from: str | None,
        effective_until: str | None,
        lifecycle_status: str | None,
        payload: tuple[tuple[str, str], ...] = (),
    ) -> CanonicalRecord:
        return CanonicalRecord(
            subject_id=subject_id,
            version_id=version_id,
            semantic_type="reference.subject",
            schema_version="2",
            organization=organization,
            authority_mode=AuthorityMode.NATIVE,
            authority_scope="reference.subject/state",
            accountable_owner_id=actor.actual_principal.principal_id,
            creation_actor=actor,
            created_at=datetime.fromisoformat(created_at),
            provenance_refs=(actor.actual_principal.principal_id,),
            integrity_metadata=(("representation", "bounded-test-fixture"),),
            payload=payload,
            lifecycle_status=lifecycle_status,
            predecessor_version_id=predecessor_version_id,
            effective_from=(None if effective_from is None else datetime.fromisoformat(effective_from)),
            effective_until=(None if effective_until is None else datetime.fromisoformat(effective_until)),
        )

    def _open_reference(
        self,
        reference: SubjectNavigationReference | ExactVersionNavigationReference,
        *,
        actor: ActorContext | None = None,
    ) -> WorkspaceShellState:
        state = open_workspace_shell(actor or self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        return navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=reference,
        )

    def _subject_state(self) -> WorkspaceShellState:
        return self._open_reference(SubjectNavigationReference(self.org_a, self.subject_id))

    def _exact_state(self, version_id: Identity) -> WorkspaceShellState:
        return self._open_reference(
            ExactVersionNavigationReference(self.org_a, self.subject_id, version_id)
        )

    def _allow(
        self,
        resource_subject_id: Identity,
        *,
        actor: ActorContext | None = None,
        organization: OrganizationScope | None = None,
        decision_value: str | None = None,
        allowed: bool = True,
    ) -> CurrentSourceAuthorization:
        actual_actor = actor or self.actor_a
        org = organization or self.org_a
        represented = (
            None
            if actual_actor.represented_principal is None
            else actual_actor.represented_principal.principal_id
        )
        return CurrentSourceAuthorization(
            organization=org,
            actor_actual_principal_id=actual_actor.actual_principal.principal_id,
            represented_principal_id=represented,
            resource_subject_id=resource_subject_id,
            decision_version_id=Identity(
                "authorization-decision-version",
                decision_value or f"allow-{resource_subject_id.value}",
                org.organization_id.value,
            ),
            allowed=allowed,
        )

    def _inspect(
        self,
        state: WorkspaceShellState,
        *,
        sources: GovernedInspectionSourceSet | None = None,
        authorizations: tuple[CurrentSourceAuthorization, ...] | None = None,
    ):
        return inspect_current_workspace_reference(
            state,
            sources=sources or GovernedInspectionSourceSet((self.lineage,), ()),
            authorizations=(
                authorizations
                if authorizations is not None
                else (self._allow(self.subject_id),)
            ),
            effective_at=self.effective_at,
        )

    def _relationship_type(self) -> RelationshipTypeReference:
        return RelationshipTypeReference(
            type_id=Identity("relationship-type", "depends-on", "platform"),
            version_id=Identity("relationship-type-version", "depends-on-v1", "platform"),
            semantic_name="platform.depends-on",
            schema_version="1",
        )

    def _relationship_lineage(
        self,
        *,
        relationship_value: str = "relationship-1",
        source: RelationshipEndpoint | None = None,
        target: RelationshipEndpoint | None = None,
    ) -> TypedRelationshipLineage:
        relationship_id = Identity("relationship", relationship_value, "org-a")
        source_endpoint = source or RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY, self.subject_id
        )
        target_endpoint = target or RelationshipEndpoint(
            EndpointReferenceRole.SUBJECT_IDENTITY,
            Identity("subject", "subject-2", "org-a"),
        )
        r1 = create_typed_relationship(
            relationship_id=relationship_id,
            version_id=Identity("relationship-version", f"{relationship_value}-v1", "org-a"),
            relationship_type=self._relationship_type(),
            source=source_endpoint,
            target=target_endpoint,
            organization=self.org_a,
            actor=self.actor_a,
            authority_scope="platform.relationship/state",
            created_at=datetime.fromisoformat("2026-07-01T09:00:00+00:00"),
            lifecycle_status="Active",
            effective_from=datetime.fromisoformat("2026-07-01T00:00:00+00:00"),
            effective_until=datetime.fromisoformat("2026-09-01T00:00:00+00:00"),
            payload=(("confidence", "governed"),),
        )
        r2 = version_typed_relationship(
            r1,
            version_id=Identity("relationship-version", f"{relationship_value}-v2", "org-a"),
            actor=self.actor_a,
            created_at=datetime.fromisoformat("2026-08-07T09:00:00+00:00"),
            lifecycle_status="Active",
            effective_from=datetime.fromisoformat("2026-09-01T00:00:00+00:00"),
            effective_until=None,
            payload=(("confidence", "future-effective"),),
        )
        return TypedRelationshipLineage((r1, r2))

    def test_subject_reference_explicitly_distinguishes_head_from_effective(self) -> None:
        result = self._inspect(self._subject_state())
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.object_kind, InspectionObjectKind.RECORD)
        self.assertEqual(result.reference_basis, InspectionReferenceBasis.CANONICAL_HEAD)
        self.assertEqual(result.displayed_version_id, self.v2_id)
        self.assertEqual(result.head_version_id, self.v2_id)
        self.assertEqual(result.effective.status, EffectiveResolutionStatus.RESOLVED)
        self.assertEqual(result.effective.version_id, self.v1_id)
        self.assertNotEqual(result.head_version_id, result.effective.version_id)

    def test_exact_historical_version_is_preserved_without_head_redirect(self) -> None:
        result = self._inspect(self._exact_state(self.v1_id))
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.reference_basis, InspectionReferenceBasis.EXACT_VERSION)
        self.assertEqual(result.displayed_version_id, self.v1_id)
        self.assertEqual(result.head_version_id, self.v2_id)
        self.assertEqual(result.effective.version_id, self.v1_id)
        history = {item.version_id: item for item in result.immutable_versions}
        self.assertTrue(history[self.v1_id].is_displayed)
        self.assertTrue(history[self.v1_id].is_effective)
        self.assertFalse(history[self.v1_id].is_head)
        self.assertTrue(history[self.v2_id].is_head)

    def test_unknown_exact_version_fails_closed_without_head_fallback(self) -> None:
        unknown = Identity("canonical-version", "not-present", "org-a")
        result = self._inspect(self._exact_state(unknown))
        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.VERSION_UNAVAILABLE)
        self.assertFalse(result.governed_content_visible)
        self.assertNotIn(self.v2_id.value, result.status_text)

    def test_missing_effective_version_is_explicit_and_never_defaults_to_head(self) -> None:
        gap_v1 = replace(
            self.v1,
            effective_until=datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        )
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((CanonicalLineage((gap_v1, self.v2)),), ()),
        )
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.head_version_id, self.v2_id)
        self.assertEqual(result.effective.status, EffectiveResolutionStatus.MISSING)
        self.assertIsNone(result.effective.version_id)
        self.assertFalse(any(item.is_effective for item in result.immutable_versions))

    def test_ambiguous_effective_version_is_explicit_and_never_guessed(self) -> None:
        overlap_v1 = replace(
            self.v1,
            effective_until=datetime.fromisoformat("2026-10-01T00:00:00+00:00"),
        )
        overlap_v2 = replace(
            self.v2,
            effective_from=datetime.fromisoformat("2026-08-01T00:00:00+00:00"),
        )
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((CanonicalLineage((overlap_v1, overlap_v2)),), ()),
        )
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.effective.status, EffectiveResolutionStatus.AMBIGUOUS)
        self.assertIsNone(result.effective.version_id)
        self.assertFalse(any(item.is_effective for item in result.immutable_versions))

    def test_authority_owner_scope_lifecycle_and_validation_meaning_are_visible(self) -> None:
        result = self._inspect(self._subject_state())
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.organization, self.org_a)
        self.assertEqual(result.accountable_owner_id, self.principal.principal_id)
        self.assertEqual(result.lifecycle_status, "Established")
        self.assertEqual(result.authority.mode, AuthorityMode.NATIVE)
        self.assertEqual(result.authority.authority_scope, "reference.subject/state")
        self.assertEqual(result.authority.authoritative_source_text, "Native Arvectum OS canonical source")
        self.assertEqual(result.validation_state, SourceValidationState.STRUCTURALLY_VALIDATED)
        self.assertFalse(hasattr(result, "approved"))
        self.assertFalse(hasattr(result, "organizational_authority"))

    def test_governed_source_organization_not_identity_scope_controls_resolution(self) -> None:
        forged_subject = Identity("subject", "subject-1", "org-a")
        foreign_v1 = self._record(
            organization=self.org_b,
            actor=self.actor_b,
            subject_id=forged_subject,
            version_id=Identity("canonical-version", "foreign-v1", "org-a"),
            predecessor_version_id=None,
            created_at="2026-07-01T08:00:00+00:00",
            effective_from="2026-07-01T00:00:00+00:00",
            effective_until=None,
            lifecycle_status="Established",
        )
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((CanonicalLineage((foreign_v1,)),), ()),
            authorizations=(self._allow(self.subject_id),),
        )
        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.SOURCE_UNAVAILABLE)
        self.assertNotIn("foreign-v1", result.status_text)
        self.assertNotIn("org-b", result.status_text)

    def test_current_authorization_is_fail_closed_and_actor_bound(self) -> None:
        missing = self._inspect(self._subject_state(), authorizations=())
        denied = self._inspect(
            self._subject_state(),
            authorizations=(self._allow(self.subject_id, allowed=False),),
        )
        duplicate = self._inspect(
            self._subject_state(),
            authorizations=(
                self._allow(self.subject_id, decision_value="decision-a"),
                self._allow(self.subject_id, decision_value="decision-b"),
            ),
        )
        wrong_actor = ActorContext(self.other_principal, self.org_a)
        actor_mismatch = self._inspect(
            self._subject_state(),
            authorizations=(self._allow(self.subject_id, actor=wrong_actor),),
        )
        for result in (missing, denied, duplicate, actor_mismatch):
            with self.subTest(result=result):
                self.assertIsInstance(result, CanonicalInspectionBlockedState)
                self.assertEqual(result.code, InspectionBlockCode.ACCESS_DENIED)
                self.assertFalse(result.governed_content_visible)
                self.assertNotIn(self.subject_id.value, result.status_text)

    def test_authorization_is_checked_before_exact_version_existence_is_disclosed(self) -> None:
        unknown = Identity("canonical-version", "protected-version-question", "org-a")
        result = self._inspect(self._exact_state(unknown), authorizations=())
        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.ACCESS_DENIED)
        self.assertNotEqual(result.code, InspectionBlockCode.VERSION_UNAVAILABLE)
        self.assertNotIn(unknown.value, result.status_text)

    def test_ambiguous_governed_source_set_fails_closed(self) -> None:
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((self.lineage, CanonicalLineage((self.v1, self.v2))), ()),
        )
        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.SOURCE_AMBIGUOUS)
        self.assertFalse(result.governed_content_visible)

    def test_authorized_relationship_context_exposes_direction_roles_and_effective_state(self) -> None:
        relationship_lineage = self._relationship_lineage()
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((self.lineage,), (relationship_lineage,)),
            authorizations=(
                self._allow(self.subject_id),
                self._allow(relationship_lineage.relationship_id),
            ),
        )
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(len(result.relationships), 1)
        edge = result.relationships[0]
        self.assertEqual(edge.direction, TraversalDirection.OUTBOUND)
        self.assertEqual(edge.matched_endpoint_role, EndpointReferenceRole.SUBJECT_IDENTITY)
        self.assertEqual(edge.matched_endpoint_id, self.subject_id)
        self.assertEqual(edge.opposite_endpoint_role, EndpointReferenceRole.SUBJECT_IDENTITY)
        self.assertEqual(edge.relationship_type_name, "platform.depends-on")
        self.assertEqual(edge.effective.status, EffectiveResolutionStatus.RESOLVED)

    def test_version_endpoint_relationship_only_appears_for_matching_displayed_version(self) -> None:
        relationship_lineage = self._relationship_lineage(
            relationship_value="version-pinned",
            source=RelationshipEndpoint(EndpointReferenceRole.VERSION_IDENTITY, self.v1_id),
        )
        sources = GovernedInspectionSourceSet((self.lineage,), (relationship_lineage,))
        auth = (self._allow(self.subject_id), self._allow(relationship_lineage.relationship_id))
        v1_result = self._inspect(self._exact_state(self.v1_id), sources=sources, authorizations=auth)
        head_result = self._inspect(self._subject_state(), sources=sources, authorizations=auth)
        self.assertIsInstance(v1_result, CanonicalRecordInspection)
        self.assertEqual(len(v1_result.relationships), 1)
        self.assertEqual(v1_result.relationships[0].matched_endpoint_role, EndpointReferenceRole.VERSION_IDENTITY)
        self.assertIsInstance(head_result, CanonicalRecordInspection)
        self.assertEqual(head_result.displayed_version_id, self.v2_id)
        self.assertEqual(head_result.relationships, ())

    def test_unauthorized_relationship_is_omitted_without_relationship_metadata(self) -> None:
        relationship_lineage = self._relationship_lineage()
        result = self._inspect(
            self._subject_state(),
            sources=GovernedInspectionSourceSet((self.lineage,), (relationship_lineage,)),
            authorizations=(self._allow(self.subject_id),),
        )
        self.assertIsInstance(result, CanonicalRecordInspection)
        self.assertEqual(result.relationships, ())
        html = render_canonical_inspection_html(result)
        self.assertIn("No authorized relationship context is available", html)
        self.assertNotIn("relationship-1", html)
        self.assertNotIn("platform.depends-on", html)
        self.assertNotIn('data-relationship-edge="true"', html)

    def test_direct_relationship_inspection_preserves_type_roles_and_exact_history(self) -> None:
        lineage = self._relationship_lineage()
        r1 = lineage.relationships[0]
        state = self._open_reference(
            ExactVersionNavigationReference(self.org_a, lineage.relationship_id, r1.relationship_version_id)
        )
        result = self._inspect(
            state,
            sources=GovernedInspectionSourceSet((), (lineage,)),
            authorizations=(self._allow(lineage.relationship_id),),
        )
        self.assertIsInstance(result, RelationshipInspection)
        self.assertEqual(result.object_kind, InspectionObjectKind.RELATIONSHIP)
        self.assertEqual(result.reference_basis, InspectionReferenceBasis.EXACT_VERSION)
        self.assertEqual(result.displayed_version_id, r1.relationship_version_id)
        self.assertEqual(result.head_version_id, lineage.head.relationship_version_id)
        self.assertEqual(result.effective.version_id, r1.relationship_version_id)
        self.assertEqual(result.relationship_type_name, "platform.depends-on")
        self.assertEqual(result.source_role, EndpointReferenceRole.SUBJECT_IDENTITY)
        self.assertEqual(result.source_id, self.subject_id)
        self.assertEqual(result.target_role, EndpointReferenceRole.SUBJECT_IDENTITY)
        self.assertEqual(result.authority.mode, AuthorityMode.NATIVE)
        self.assertEqual(len(result.immutable_versions), 2)

    def test_relationship_subject_reference_shows_head_even_when_effective_differs(self) -> None:
        lineage = self._relationship_lineage()
        state = self._open_reference(SubjectNavigationReference(self.org_a, lineage.relationship_id))
        result = self._inspect(
            state,
            sources=GovernedInspectionSourceSet((), (lineage,)),
            authorizations=(self._allow(lineage.relationship_id),),
        )
        self.assertIsInstance(result, RelationshipInspection)
        self.assertEqual(result.reference_basis, InspectionReferenceBasis.CANONICAL_HEAD)
        self.assertEqual(result.displayed_version_id, lineage.head.relationship_version_id)
        self.assertEqual(result.effective.version_id, lineage.relationships[0].relationship_version_id)
        self.assertNotEqual(result.displayed_version_id, result.effective.version_id)

    def test_no_current_reference_is_a_safe_non_content_state(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        result = inspect_current_workspace_reference(
            state,
            sources=GovernedInspectionSourceSet((self.lineage,), ()),
            authorizations=(self._allow(self.subject_id),),
            effective_at=self.effective_at,
        )
        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.REFERENCE_REQUIRED)
        self.assertFalse(result.governed_content_visible)

    def test_renderer_is_readable_inert_and_escapes_governed_values(self) -> None:
        result = self._inspect(self._exact_state(self.v1_id))
        self.assertIsInstance(result, CanonicalRecordInspection)
        html = render_canonical_inspection_html(result)
        for text in (
            "Subject Identity",
            "Displayed version",
            "Exact Version",
            "Canonical Head",
            "Effective Version",
            "Native Arvectum OS canonical source",
            "Immutable version history",
            "Structurally validated canonical lineage",
            "not business approval",
            "Read-only non-authoritative presentation",
        ):
            self.assertIn(text, html)
        self.assertIn("<caption>", html)
        self.assertNotIn("href=", html)
        self.assertNotIn("<form", html)
        self.assertNotIn("/records/", html)

        unsafe_subject = Identity("subject", '<script>alert("id")</script>', "org-a")
        unsafe = self._record(
            organization=self.org_a,
            actor=self.actor_a,
            subject_id=unsafe_subject,
            version_id=Identity("canonical-version", "unsafe-v1", "org-a"),
            predecessor_version_id=None,
            created_at="2026-07-01T08:00:00+00:00",
            effective_from="2026-07-01T00:00:00+00:00",
            effective_until=None,
            lifecycle_status="Established",
            payload=(("<b>key</b>", '<img src=x onerror="alert(1)">'),),
        )
        unsafe_state = self._open_reference(SubjectNavigationReference(self.org_a, unsafe_subject))
        unsafe_result = self._inspect(
            unsafe_state,
            sources=GovernedInspectionSourceSet((CanonicalLineage((unsafe,)),), ()),
            authorizations=(self._allow(unsafe_subject),),
        )
        self.assertIsInstance(unsafe_result, CanonicalRecordInspection)
        unsafe_html = render_canonical_inspection_html(unsafe_result)
        self.assertNotIn("<script>", unsafe_html)
        self.assertNotIn("<img", unsafe_html)
        self.assertNotIn("<b>key</b>", unsafe_html)
        self.assertIn("&lt;script&gt;", unsafe_html)
        self.assertIn("&lt;img", unsafe_html)
        self.assertIn("&lt;b&gt;key&lt;/b&gt;", unsafe_html)

    def test_blocked_renderer_exposes_no_governed_metadata(self) -> None:
        blocked = self._inspect(self._subject_state(), authorizations=())
        self.assertIsInstance(blocked, CanonicalInspectionBlockedState)
        html = render_canonical_inspection_html(blocked)
        self.assertIn('role="alert"', html)
        self.assertIn("No governed source content is exposed", html)
        self.assertNotIn(self.subject_id.value, html)
        self.assertNotIn(self.v1_id.value, html)
        self.assertNotIn(self.v2_id.value, html)
        self.assertNotIn("<table", html)

    def test_inspection_layer_remains_internal_read_only_and_technology_neutral(self) -> None:
        package_root = Path(__file__).parents[1] / "arvectum_os_ref"
        source = (package_root / "canonical_inspection.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported_modules = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_modules.add(node.module)
        for fragment in (
            "mutation",
            "execution",
            "gates",
            "product_contract",
            "sqlalchemy",
            "django",
            "flask",
            "fastapi",
            "starlette",
            "graphql",
            "requests",
            "httpx",
            "sqlite",
            "psycopg",
        ):
            with self.subTest(fragment=fragment):
                self.assertFalse(any(fragment in imported for imported in imported_modules), imported_modules)
        package_init = (package_root / "__init__.py").read_text(encoding="utf-8")
        self.assertNotIn("canonical_inspection", package_init)
        self.assertNotIn("inspect_current_workspace_reference", package_init)
        self.assertNotIn("render_canonical_inspection_html", package_init)
        self.assertNotIn("CanonicalRecordInspection", package_init)


if __name__ == "__main__":
    unittest.main()
