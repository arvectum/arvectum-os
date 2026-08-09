from __future__ import annotations

import unittest

from arvectum_os_ref.authority_safe_ux import (
    AuthoritySafeActionLabel,
    AuthoritySafeUxState,
    consume_current_source_authorization,
)
from arvectum_os_ref.canonical_inspection import CurrentSourceAuthorization
from arvectum_os_ref.identity import Identity
from arvectum_os_ref.security import ActorContext, OrganizationScope, Principal
from arvectum_os_ref.workspace_shell import PresentationAuthority, WorkspaceShellState, open_workspace_shell


class P410AuthoritySafePositivePathTests(unittest.TestCase):
    def test_unique_current_allow_is_explicit_minimized_and_non_authoritative(self) -> None:
        organization = OrganizationScope(Identity("organization", "org-p410-ci", "platform"))
        actor = ActorContext(
            Principal(Identity("principal", "operator-p410-ci", "platform")),
            organization,
        )
        workspace = open_workspace_shell(actor)
        self.assertIsInstance(workspace, WorkspaceShellState)

        subject = Identity("record-subject", "subject-p410-ci", "platform")
        decision_version = Identity(
            "authorization-decision-version", "p410-ci-v1", "platform"
        )
        decision = CurrentSourceAuthorization(
            organization=organization,
            actor_actual_principal_id=actor.actual_principal.principal_id,
            resource_subject_id=subject,
            decision_version_id=decision_version,
            allowed=True,
        )

        result = consume_current_source_authorization(
            workspace=workspace,
            resource_subject_id=subject,
            source_authorizations=(decision,),
            allow_derived_preview=True,
        )

        self.assertEqual(result.state, AuthoritySafeUxState.AVAILABLE)
        self.assertEqual(result.action_label, AuthoritySafeActionLabel.REQUEST_ACTION)
        self.assertEqual(result.source_authorization_decision_version_id, decision_version)
        self.assertTrue(result.governed_content_visible)
        self.assertTrue(result.derived_preview_visible)
        self.assertFalse(result.protected_count_visible)
        self.assertIs(result.presentation_authority, PresentationAuthority.NON_AUTHORITATIVE)


if __name__ == "__main__":
    unittest.main()
