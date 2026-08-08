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
from arvectum_os_ref.workspace_shell import WorkspaceShellState, open_workspace_shell


class P409SecurityRightsAuthoritySafeUxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.organization = OrganizationScope(Identity("organization", "org-p409", "platform"))
        self.other_organization = OrganizationScope(
            Identity("organization", "org-p409-other", "platform")
        )
        self.actor = ActorContext(
            Principal(Identity("principal", "operator-p409", "platform")),
            self.organization,
        )
        workspace = open_workspace_shell(self.actor)
        self.assertIsInstance(workspace, WorkspaceShellState)
        self.workspace = workspace
        self.subject = Identity("record-subject", "protected-p409", "platform")
        self.decision_v1 = Identity("authorization-decision-version", "p409-v1", "platform")
        self.decision_v2 = Identity("authorization-decision-version", "p409-v2", "platform")

    def _decision(self, *, allowed: bool = True, organization=None, version=None):
        return CurrentSourceAuthorization(
            organization=organization or self.organization,
            actor_actual_principal_id=self.actor.actual_principal.principal_id,
            resource_subject_id=self.subject,
            decision_version_id=version or self.decision_v1,
            allowed=allowed,
        )

    def test_unique_current_allow_exposes_only_minimized_content_state(self) -> None:
        result = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._decision(),),
            allow_derived_preview=True,
        )
        self.assertEqual(result.state, AuthoritySafeUxState.AVAILABLE)
        self.assertEqual(result.action_label, AuthoritySafeActionLabel.REQUEST_ACTION)
        self.assertTrue(result.governed_content_visible)
        self.assertTrue(result.derived_preview_visible)
        self.assertFalse(result.protected_count_visible)
        self.assertEqual(result.source_authorization_decision_version_id, self.decision_v1)

    def test_denied_missing_ambiguous_and_wrong_organization_fail_closed(self) -> None:
        cases = (
            (),
            (self._decision(allowed=False),),
            (self._decision(), self._decision()),
            (self._decision(organization=self.other_organization),),
        )
        for decisions in cases:
            with self.subTest(decisions=decisions):
                result = consume_current_source_authorization(
                    workspace=self.workspace,
                    resource_subject_id=self.subject,
                    source_authorizations=decisions,
                    allow_derived_preview=True,
                )
                self.assertEqual(result.state, AuthoritySafeUxState.NOT_AVAILABLE)
                self.assertEqual(result.action_label, AuthoritySafeActionLabel.UNAVAILABLE)
                self.assertFalse(result.governed_content_visible)
                self.assertFalse(result.derived_preview_visible)
                self.assertFalse(result.protected_count_visible)

    def test_replaced_authorization_requires_reinspection_and_hides_preview(self) -> None:
        result = consume_current_source_authorization(
            workspace=self.workspace,
            resource_subject_id=self.subject,
            source_authorizations=(self._decision(version=self.decision_v2),),
            expected_decision_version_id=self.decision_v1,
            allow_derived_preview=True,
        )
        self.assertEqual(result.state, AuthoritySafeUxState.REINSPECTION_REQUIRED)
        self.assertEqual(result.action_label, AuthoritySafeActionLabel.REINSPECT)
        self.assertFalse(result.governed_content_visible)
        self.assertFalse(result.derived_preview_visible)
        self.assertFalse(result.protected_count_visible)

    def test_labels_do_not_claim_approval_permission_or_authority(self) -> None:
        labels = " ".join(value.value.lower() for value in AuthoritySafeActionLabel)
        for forbidden in ("approve", "approved", "authorized", "permission granted"):
            self.assertNotIn(forbidden, labels)


if __name__ == "__main__":
    unittest.main()
