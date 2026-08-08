import unittest
from datetime import datetime, timezone

from arvectum_os_ref.canonical_inspection import (
    CanonicalInspectionBlockedState,
    CurrentSourceAuthorization,
    GovernedInspectionSourceSet,
    InspectionBlockCode,
    inspect_current_workspace_reference,
)
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import (
    SubjectNavigationReference,
    WorkspaceDestination,
    WorkspaceShellState,
    navigate_workspace,
    open_workspace_shell,
)


class P403SourceResolutionSecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(
            Identity("organization", "org-a", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator", "platform")),
            self.organization,
        )
        self.unknown_subject = Identity("subject", "unknown", "org-a")
        state = open_workspace_shell(self.actor)
        self.assertIsInstance(state, WorkspaceShellState)
        self.state = navigate_workspace(
            state,
            destination=WorkspaceDestination.RECORDS,
            reference=SubjectNavigationReference(
                self.organization,
                self.unknown_subject,
            ),
        )

    def _inspect(self, authorizations):
        return inspect_current_workspace_reference(
            self.state,
            sources=GovernedInspectionSourceSet(),
            authorizations=authorizations,
            effective_at=datetime(2026, 8, 8, tzinfo=timezone.utc),
        )

    def test_unauthorized_unknown_subject_does_not_become_source_existence_oracle(self) -> None:
        result = self._inspect(())

        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.ACCESS_DENIED)
        self.assertNotIn(self.unknown_subject.value, result.status_text)

    def test_source_unavailability_is_reached_only_after_explicit_current_allow(self) -> None:
        allow = CurrentSourceAuthorization(
            organization=self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            resource_subject_id=self.unknown_subject,
            decision_version_id=Identity(
                "authorization-decision-version",
                "allow-unknown",
                "org-a",
            ),
            allowed=True,
        )
        result = self._inspect((allow,))

        self.assertIsInstance(result, CanonicalInspectionBlockedState)
        self.assertEqual(result.code, InspectionBlockCode.SOURCE_UNAVAILABLE)
        self.assertFalse(result.governed_content_visible)


if __name__ == "__main__":
    unittest.main()
