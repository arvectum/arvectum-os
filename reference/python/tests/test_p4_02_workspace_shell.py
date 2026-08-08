import unittest

from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    ExactVersionNavigationReference,
    PresentationAuthority,
    SubjectNavigationReference,
    WorkspaceBlockedState,
    WorkspaceBlockCode,
    WorkspaceDestination,
    WorkspaceProductContext,
    WorkspaceScopeViolation,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
    render_workspace_shell_html,
)


class P402WorkspaceShellTests(unittest.TestCase):
    def setUp(self) -> None:
        self.org_a = OrganizationScope(Identity("organization", "org-a", "platform"))
        self.org_b = OrganizationScope(Identity("organization", "org-b", "platform"))
        self.principal = Principal(Identity("principal", "operator-1", "platform"))
        self.actor_a = ActorContext(self.principal, self.org_a)

    def test_unresolved_organization_fails_closed_without_default(self) -> None:
        state = open_workspace_shell(None)

        self.assertIsInstance(state, WorkspaceBlockedState)
        self.assertEqual(state.code, WorkspaceBlockCode.ORGANIZATION_UNRESOLVED)
        self.assertFalse(state.governed_content_visible)
        self.assertFalse(state.navigation_enabled)
        self.assertNotIn("org-a", state.status_text)
        self.assertNotIn("org-b", state.status_text)

    def test_open_shell_exposes_only_p4_01_domain_neutral_destinations(self) -> None:
        state = open_workspace_shell(self.actor_a)

        self.assertIsInstance(state, WorkspaceShellState)
        self.assertEqual(state.organization, self.org_a)
        self.assertEqual(state.actor, self.actor_a)
        self.assertEqual(
            state.destinations,
            (
                WorkspaceDestination.DISCOVER,
                WorkspaceDestination.RECORDS,
                WorkspaceDestination.EXECUTIONS,
                WorkspaceDestination.EVIDENCE,
                WorkspaceDestination.DOCUMENTS,
                WorkspaceDestination.KNOWLEDGE,
            ),
        )
        self.assertEqual(state.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)

    def test_navigation_preserves_actor_and_organization_context(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        subject = SubjectNavigationReference(
            organization=self.org_a,
            subject_id=Identity("subject", "subject-1", "org-a"),
        )

        next_state = navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=subject,
        )

        self.assertEqual(next_state.organization, self.org_a)
        self.assertEqual(next_state.actor, self.actor_a)
        self.assertEqual(next_state.current_reference, subject)
        self.assertEqual(next_state.active_destination, WorkspaceDestination.RECORDS)

    def test_wrong_organization_navigation_reference_is_rejected(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        foreign_reference = SubjectNavigationReference(
            organization=self.org_b,
            subject_id=Identity("subject", "foreign-subject", "org-b"),
        )

        with self.assertRaises(WorkspaceScopeViolation) as raised:
            navigate_workspace(
                state,
                destination=WorkspaceDestination.RECORDS,
                reference=foreign_reference,
            )

        self.assertNotIn("foreign-subject", str(raised.exception))
        self.assertNotIn("org-b", str(raised.exception))

    def test_subject_and_exact_version_references_remain_distinct(self) -> None:
        subject_id = Identity("subject", "subject-1", "org-a")
        version_id = Identity("version", "version-7", "org-a")
        subject_reference = SubjectNavigationReference(self.org_a, subject_id)
        exact_reference = ExactVersionNavigationReference(self.org_a, subject_id, version_id)

        self.assertNotEqual(type(subject_reference), type(exact_reference))
        self.assertFalse(hasattr(subject_reference, "version_id"))
        self.assertEqual(exact_reference.version_id, version_id)

    def test_exact_historical_version_is_preserved_without_head_redirect(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        exact = ExactVersionNavigationReference(
            organization=self.org_a,
            subject_id=Identity("subject", "subject-1", "org-a"),
            version_id=Identity("version", "historical-v2", "org-a"),
        )

        next_state = navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=exact,
        )

        self.assertIs(next_state.current_reference, exact)
        self.assertEqual(next_state.current_reference.version_id.value, "historical-v2")
        self.assertFalse(hasattr(next_state, "canonical_head"))
        self.assertFalse(hasattr(next_state, "effective_version"))

    def test_presentation_state_cannot_create_authorization_or_authority(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)

        for forbidden_attribute in (
            "authorized",
            "permissions",
            "organizational_authority",
            "approved",
            "canonical_mutation",
        ):
            with self.subTest(attribute=forbidden_attribute):
                self.assertFalse(hasattr(state, forbidden_attribute))

        self.assertEqual(state.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)

    def test_shell_navigation_has_no_counts_or_protected_content_inventory(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)

        for forbidden_attribute in ("counts", "facets", "results", "records", "documents"):
            with self.subTest(attribute=forbidden_attribute):
                self.assertFalse(hasattr(state, forbidden_attribute))

    def test_product_entry_context_is_scope_checked_and_non_authoritative(self) -> None:
        product_context = WorkspaceProductContext(
            organization=self.org_a,
            product_id=Identity("product", "product-1", "platform"),
            product_contract_version_id=Identity(
                "product-contract-version", "pc-v1", "org-a"
            ),
        )

        state = open_workspace_shell(self.actor_a, product_context=product_context)

        self.assertIsInstance(state, WorkspaceShellState)
        self.assertEqual(state.product_context, product_context)
        self.assertFalse(hasattr(product_context, "authorized"))
        self.assertFalse(hasattr(product_context, "organizational_authority"))

        mismatched = WorkspaceProductContext(
            organization=self.org_b,
            product_id=Identity("product", "product-1", "platform"),
        )
        blocked = open_workspace_shell(self.actor_a, product_context=mismatched)
        self.assertIsInstance(blocked, WorkspaceBlockedState)
        self.assertEqual(blocked.code, WorkspaceBlockCode.CONTEXT_SCOPE_MISMATCH)
        self.assertFalse(blocked.governed_content_visible)
        self.assertFalse(blocked.navigation_enabled)

    def test_rendered_shell_has_textual_context_and_no_route_contract(self) -> None:
        state = open_workspace_shell(self.actor_a)
        self.assertIsInstance(state, WorkspaceShellState)
        exact = ExactVersionNavigationReference(
            organization=self.org_a,
            subject_id=Identity("subject", "subject-1", "org-a"),
            version_id=Identity("version", "v3", "org-a"),
        )
        state = navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=exact,
        )

        html = render_workspace_shell_html(state)

        self.assertIn("Organization: org-a", html)
        self.assertIn("Actor: operator-1", html)
        self.assertIn("Current reference: Exact version v3", html)
        self.assertIn('aria-label="Workspace"', html)
        self.assertIn('aria-current="page"', html)
        self.assertIn("Presentation state only", html)
        self.assertNotIn("href=", html)
        self.assertNotIn("/records", html)

    def test_blocked_render_has_text_meaning_and_no_navigation(self) -> None:
        blocked = open_workspace_shell(None)
        self.assertIsInstance(blocked, WorkspaceBlockedState)

        html = render_workspace_shell_html(blocked)

        self.assertIn("Workspace unavailable", html)
        self.assertIn("Organization scope is unresolved", html)
        self.assertIn('role="alert"', html)
        self.assertNotIn("<nav", html)
        self.assertNotIn("data-workspace-destination", html)

    def test_renderer_escapes_identity_values(self) -> None:
        unsafe_org = OrganizationScope(
            Identity("organization", '<script>alert("org")</script>', "platform")
        )
        unsafe_principal = Principal(
            Identity("principal", '<img src=x onerror="alert(1)">', "platform")
        )
        state = open_workspace_shell(ActorContext(unsafe_principal, unsafe_org))
        self.assertIsInstance(state, WorkspaceShellState)

        html = render_workspace_shell_html(state)

        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&lt;img", html)


if __name__ == "__main__":
    unittest.main()
